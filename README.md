# J.A.R.V.I.S — AI-Assisted Pentesting Assistant

> **v1.0 is functional and deployed. This project is under active development.**
> The original repository lives on Codeberg where development happens continuously. This mirror receives periodic large commits. Significant improvements and new tools are coming.

---

## What is this

A local AI-assisted pentesting assistant built for Kali Linux. It automates the repetitive enumeration phase of an engagement — port scanning, web directory bruteforce, subdomain discovery, SMB enumeration, FTP checks — then uses an AI model to analyze the findings and suggest realistic initial access vectors based strictly on what was actually found.

Built from scratch as a real learning project by a junior penetration tester. Every module was written and understood line by line. Not a wrapper around existing tools — a system that orchestrates them intelligently.

---

## How the pipeline works

```
python3 core/orchestrator.py
          ↓
    Enter target (IP or domain)
          ↓
    nmap — full port scan (-p- -sV -sC)
          ↓
    Rule Engine — reads findings, decides what runs next
          ↓
    ┌─────────────────────────────────────────┐
    │  HTTP/HTTPS → ffuf directory bruteforce  │
    │  Domain     → ffuf vhost scan            │
    │               (auto-calibrated baseline) │
    │  SMB 139/445 → smbmap share enum        │
    │  FTP 21      → anonymous login check    │
    └─────────────────────────────────────────┘
          ↓
    AI Analysis — digest sent to OpenRouter
    Suggests attack vectors based only on real findings
          ↓
    Rich terminal output — tables, panels, spinners
    Jarvis voice intro on startup
```

---

## Current tool stack

| Tool | What it does | When it runs |
|---|---|---|
| nmap | Full port scan with version detection | Always, first |
| ffuf (dirs) | Web directory bruteforce | Port 80 or 443 found |
| ffuf (vhost) | Subdomain enumeration | Domain target only |
| smbmap | SMB share enumeration | Port 139 or 445 found |
| FTP anon check | Anonymous login via curl | Port 21 found |
| AI (OpenRouter) | Attack vector analysis | After all tools finish |

---

## Project structure

```
jarvis_red_team/
│
├── core/
│   ├── orchestrator.py       # Central brain — runs the full pipeline
│   ├── session.py            # Creates session folders and IDs
│   └── task_queue.py         # Priority queue for tool execution
│
├── rules/
│   ├── rule_engine.py        # Reads rules, matches findings, queues tasks
│   └── rules.yaml            # "if port 80 open → run ffuf"
│
├── tools/
│   ├── executor.py           # Runs shell commands, returns structured results
│   └── parser/
│       ├── nmap_parser.py    # XML → structured port/service data
│       ├── ffuf_parser.py    # JSON → dirs and vhosts
│       └── smbmap_parser.py  # Text → share list with permissions
│
├── ai/
│   ├── ai_module.py          # OpenRouter API — sends digest, returns analysis
│   └── digest_builder.py     # Compresses session findings for AI input
│
├── datastorage/
│   └── database.py           # SQLite — stores all findings per session
│                             # Wiped clean at the start of every new session
│
├── voice/
│   ├── jarvis_voice.py       # Plays intro audio on startup
│   └── jarvis_cut.ogg        # Jarvis audio clip
│
└── sessions/                 # Auto-created — one folder per scan session
```

---

## Installation

```bash
git clone https://codeberg.org/YOUR_USERNAME/jarvis_red_team
cd jarvis_red_team
pip install -r requirements.txt --break-system-packages
sudo apt install nmap ffuf smbmap curl alsa-utils -y
```

---

## Usage

```bash
python3 core/orchestrator.py
```

Enter an IP or domain when prompted. Everything else runs automatically.

Domain targets get vhost scanning with automatic baseline size calibration to filter false positives.

---

## AI setup

Uses [OpenRouter](https://openrouter.ai) — free tier is enough. Add your key to `ai/ai_module.py`:

```python
OPENROUTER_API_KEY = "your_key_here"
```

Tested free models that work well:
- `arcee-ai/trinity-large-preview:free`
- `meta-llama/llama-3.1-8b-instruct:free`
- `mistralai/mistral-7b-instruct:free`

---

## What is coming next

This is v1.0. The foundation works. A lot is still being built.

**Tools being added:**
- `enum4linux` — deeper SMB/Samba enumeration (users, groups, password policies)
- `showmount` — NFS share enumeration
- `nikto` — web server vulnerability scanning
- `whatweb` — web technology fingerprinting
- SSH version CVE lookup — automatic check against known CVE database

**System improvements:**
- Wake word detection — say "wake up Jarvis" to launch
- Config file (`config.yaml`) — move all settings out of code
- Report generator — auto-generate markdown pentest reports per session
- Session history — browse and compare previous scans
- Better AI prompt tuning — more accurate, less hallucination
- Port-based rules instead of service-name only — more reliable triggering

**Known issues being fixed:**
- AI occasionally hallucinates findings not present in the data (prompt improvements ongoing)
- Rule engine triggers duplicate tasks for services on multiple ports

---

## Original repository

Development happens on Codeberg:
**https://codeberg.org/cybermaksx/jarvis_red_team**

This GitHub mirror receives larger periodic commits. If you want to follow active development, watch the Codeberg repo.

---

## Built with

Python 3 · nmap · ffuf · smbmap · SQLite · OpenRouter API · rich · pygame · Kali Linux

---

*Started as a learning project. Built line by line. Still being built.*
