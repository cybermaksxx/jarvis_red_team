#!/usr/bin/env python3
import sys
import re
import requests
sys.path.append(".")

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from core.task_queue import TaskQueue
from core.session import create_session
from tools.executor import run_command
from tools.parser.nmap_parser import parse_nmap
from tools.parser.ffuf_parser import parse_ffuf
from datastorage.database import init_db, save_port, clear_ports, save_directory, save_smb_share
from rules.rules_engine import apply_rules

console = Console()


def is_ip(target: str) -> bool:
    return bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target))


def get_baseline_size(target: str) -> int:
    try:
        r = requests.get(
            f"http://{target}",
            headers={"Host": f"nonexistent12345.{target}"},
            timeout=5
        )
        return len(r.content)
    except:
        return 0


def print_banner():
    banner = """
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
     ██║███████║██████╔╝██║   ██║██║███████╗
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
    """
    console.print(Panel(banner, subtitle="[dim]Pentesting Assistant v1.0[/dim]", style="bold blue"))

    try:
        from voice.jarvis_voice import speak_intro
        speak_intro()
    except Exception:
            pass






def run_session(target: str):
    init_db()
    clear_ports()
    session_id = create_session(target)

    console.print(f"\n[bold cyan][*][/bold cyan] Session: [yellow]{session_id}[/yellow]")
    console.print(f"[bold cyan][*][/bold cyan] Target:  [yellow]{target}[/yellow]\n")

    # nmap
    with console.status(f"[bold green]Running nmap on {target}...[/bold green]", spinner="dots"):
        nmap_cmd = f"nmap -sS -sV -sC {target} -p- -T3 -oX sessions/{session_id}/nmap.xml"
        result = run_command(nmap_cmd, timeout=300)

    if not result["success"]:
        console.print(f"[bold red][-][/bold red] Nmap failed: {result['stderr']}")
        return

    # порты в таблицу
    ports = parse_nmap(f"sessions/{session_id}/nmap.xml")

    table = Table(title="Open Ports", style="cyan", header_style="bold cyan")
    table.add_column("Host", style="white")
    table.add_column("Port", style="yellow")
    table.add_column("Service", style="green")
    table.add_column("Version", style="dim")

    for port in ports:
        save_port(port)
        table.add_row(
            port["host"],
            f"{port['port']}/{port['protocol']}",
            port["service"],
            port["version"]
        )

    console.print(table)

    # rule engine
    console.print(f"\n[bold cyan][*][/bold cyan] Applying rules...")
    queue = TaskQueue()
    apply_rules(session_id, queue)

    # execution loop
    console.print(f"[bold cyan][*][/bold cyan] Executing tasks...\n")
    smb_scanned = set()

    while not queue.is_empty():
        task = queue.get_next_task()
        tool = task["tool"]
        task_target = task["target"]

        if tool == "run_ffuf_dirs":
            with console.status(f"[bold green]Running ffuf dirs on {task_target}...[/bold green]", spinner="dots"):
                cmd = f"ffuf -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -u http://{task_target}/FUZZ -of json -o sessions/{session_id}/ffuf_dirs.json -mc 200,301,302"
                result = run_command(cmd, timeout=120)

            if result["success"]:
                dirs = parse_ffuf(f"sessions/{session_id}/ffuf_dirs.json")
                if dirs:
                    dir_table = Table(title="Web Directories", style="green", header_style="bold green")
                    dir_table.add_column("Status", style="yellow", width=8)
                    dir_table.add_column("URL", style="white")

                    for d in dirs:
                        save_directory(d)
                        dir_table.add_row(str(d["status_code"]), d["url"])

                    console.print(dir_table)
            else:
                console.print(f"[bold red][-][/bold red] ffuf failed: {result['stderr']}")

        elif tool == "run_smbmap":
            if task_target in smb_scanned:
                continue
            smb_scanned.add(task_target)

            with console.status(f"[bold green]Running smbmap on {task_target}...[/bold green]", spinner="dots"):
                cmd = f"smbmap -H {task_target} | tee sessions/{session_id}/shares.txt"
                result = run_command(cmd, timeout=60)

            if result["success"]:
                from tools.parser.smbmap_parser import parse_smbmap
                shares = parse_smbmap(f"sessions/{session_id}/shares.txt")
                if shares:
                    smb_table = Table(title="SMB Shares", style="magenta", header_style="bold magenta")
                    smb_table.add_column("IP", style="white")
                    smb_table.add_column("Share", style="yellow")
                    smb_table.add_column("Permissions", style="green")
                    smb_table.add_column("Comment", style="dim")

                    for s in shares:
                        save_smb_share(s, session_id)
                        color = "green" if "READ" in s["permissions"] else "red"
                        smb_table.add_row(
                            s["ip"],
                            s["disk"],
                            f"[{color}]{s['permissions']}[/{color}]",
                            s["comment"]
                        )

                    console.print(smb_table)
            else:
                console.print(f"[bold red][-][/bold red] smbmap failed")

        elif tool == "run_ftp_anon":
            with console.status(f"[bold green]Checking FTP anonymous on {task_target}...[/bold green]", spinner="dots"):
                cmd = f"curl -s --connect-timeout 10 ftp://{task_target}/ --user anonymous:anonymous"
                result = run_command(cmd, timeout=30)

            if result["success"] and result["stdout"]:
                console.print(f"[bold green][+][/bold green] FTP ANONYMOUS LOGIN WORKS on {task_target}!")
                for line in result["stdout"].strip().split("\n"):
                    if line.strip():
                        console.print(f"    [yellow]{line.strip()}[/yellow]")
            else:
                console.print(f"[bold red][-][/bold red] FTP anonymous failed on {task_target}")

    # vhost
    if not is_ip(target):
        with console.status(f"[bold green]Running vhost scan on {target}...[/bold green]", spinner="dots"):
            baseline = get_baseline_size(target)
            vhost_cmd = f"ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -H 'Host: FUZZ.{target}' -u http://{target} -of json -o sessions/{session_id}/ffuf_vhost.json -mc 200,301,302 -fs {baseline}"
            result = run_command(vhost_cmd, timeout=300)

        if result["success"]:
            vhosts = parse_ffuf(f"sessions/{session_id}/ffuf_vhost.json")
            if vhosts:
                vhost_table = Table(title="Subdomains", style="blue", header_style="bold blue")
                vhost_table.add_column("Subdomain", style="white")
                vhost_table.add_column("Status", style="yellow")
                vhost_table.add_column("Size", style="dim")

                for v in vhosts:
                    vhost_table.add_row(v["host"], str(v["status_code"]), str(v["size"]))

                console.print(vhost_table)
            else:
                console.print(f"[bold red][-][/bold red] No subdomains found")

    # AI
    with console.status("[bold green]Running AI analysis...[/bold green]", spinner="dots"):
        try:
            from ai.digest_builder import build_digest
            from ai.ai_module import analyze

            digest = build_digest(session_id)
            ai_result = analyze(digest)

            console.print(Panel(
                ai_result,
                title="[bold yellow]AI Analysis[/bold yellow]",
                style="yellow"
            ))
        except Exception as e:
            console.print(f"[bold red][-][/bold red] AI analysis failed: {e}")


if __name__ == "__main__":
    print_banner()
    target = console.input("\n[bold cyan]Enter target:[/bold cyan] ")
    run_session(target)
