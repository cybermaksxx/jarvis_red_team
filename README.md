# J.A.R.V.I.S — Pentesting Assistant

> **Status: v1.0 complete — actively developed and fixing bugs**
> The first version of this project is fully functional. Development will continue after a short break with new features, improvements, and additional tools.

A local AI-assisted pentesting assistant for Kali Linux. It automates the repetitive parts of an engagement — host discovery, enumeration, tool execution, result parsing — and uses AI to analyze findings and suggest attack vectors.

Built as a real learning project by a junior penetration tester. Not a script kiddie tool — every module was written and understood from scratch.

---

## How it works

```
Target input
    ↓
nmap — full port scan
    ↓
Rule Engine — decides what to run next based on findings
    ↓
ffuf — directory bruteforce (HTTP targets)
ffuf — vhost/subdomain scan (domain targets, auto-calibrated)
smbmap — SMB share enumeration (ports 139/445)
FTP — anonymous login check (port 21)
    ↓
AI Analysis — summarizes findings, suggests top attack vectors
    ↓
Rich terminal output with tables and panels
```

---

## Current tool stack

| Tool | Purpose | Trigger |
|---|---|---|
| nmap | Full port scan with service detection | Always |
| ffuf (dirs) | Web directory bruteforce | Port 80 / 443 |
| ffuf (vhost) | Subdomain enumeration with baseline filter | Domain target |
| smbmap | SMB share enumeration | Port 139 / 445 |
| FTP check | Anonymous login via curl | Port 21 |
| AI (OpenRouter) | Attack vector analysis | End of session |

---

## Project structure

```
jarvis/
│
├── core/
│   ├── orchestrator.py        # Central coordinator — runs the full pipeline
│   ├── session.py             # Session management and folder creation
│   └── task_queue.py          # Priority task queue
│
├── rules/
│   ├── rule_engine.py         # Reads rules, matches findings, creates tasks
│   └── rules.yaml             # Human-readable rules: "if http → run ffuf"
│
├── tools/
│   ├── executor.py            # Runs system commands, returns structured results
│   └── parser/
│       ├── nmap_parser.py
│       ├── ffuf_parser.py
│       └── smbmap_parser.py
│
├── ai/
│   ├── ai_module.py           # OpenRouter API wrapper
│   └── digest_builder.py      # Compresses session data for AI input
│
├── datastorage/
│   └── database.py            # SQLite — persistent storage for all findings
│
├── voice/
│   ├── jarvis_voice.py        # Plays Jarvis intro audio on startup
│   └── jarvis_cut.ogg         # Audio file
│
└── sessions/                  # Auto-created — one folder per pentest session
```

---

## Installation

```bash
git clone <repo>
cd jarvis_red_team
pip install -r requirements.txt --break-system-packages
```

External tools required on Kali:
```bash
sudo apt install nmap ffuf smbmap curl alsa-utils -y
```

---

## Usage

```bash
python3 core/orchestrator.py
```

Enter an IP address or domain name when prompted. The system handles everything else automatically.

For domain targets, vhost scanning runs automatically with baseline size filtering to eliminate false positives.

---

## AI setup

The AI module uses [OpenRouter](https://openrouter.ai) — free tier available. Add your API key to `ai/ai_module.py`:

```python
OPENROUTER_API_KEY = "your_key_here"
```

Recommended free models:
- `meta-llama/llama-3.1-8b-instruct:free`
- `mistralai/mistral-7b-instruct:free`

---

## What's coming next

After a short break, development continues with:

- Wake word detection — say "wake up Jarvis" to start
- enum4linux integration for deeper SMB/Samba enumeration
- NFS enumeration (showmount)
- Report generator — auto-generate markdown reports per session
- Session resume — pick up a scan where it left off
- Config file — move all settings out of code into config.yaml
- Fix: filter findings by session_id to eliminate cross-session data pollution

---

## Built with

Python 3 · nmap · ffuf · smbmap · SQLite · OpenRouter API · rich · pygame

---

*Built on Kali Linux. Every line written and understood from scratch.*
