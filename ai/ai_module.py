#!/usr/bin/env python3
import requests

OPENROUTER_API_KEY = "PUT-YOUR-API-KEY-HERE"
MODEL = "arcee-ai/trinity-large-preview:free"


def analyze(digest: str) -> str:
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": f"""You are a senior penetration tester reviewing a recon report.

STRICT RULES — follow these or your analysis is worthless:
- Analyze ONLY the data explicitly listed below. Never invent findings.
- Do NOT suggest brute force or password spraying as a vector. These are last resort tactics, not initial access vectors.
- Do NOT suggest "check for default credentials" generically. Only mention credentials if there is a specific service that is known to ship with defaults (e.g. exposed admin panel, Tomcat manager, Jenkins).
- Do NOT repeat generic advice like "run a vulnerability scanner" or "enumerate further". That is not analysis.
- If the attack surface is limited (e.g. only SSH open), say so honestly and explain what specifically could be investigated based on the version or configuration visible in the data.
- For every vector you suggest, cite the EXACT finding from the data that supports it (port number, version string, service name).
- Focus on: version-specific CVEs, exposed management interfaces, anonymous access, protocol misconfigurations, service chains that could lead to access.

Based strictly on the data below, suggest up to 3 realistic initial access vectors. If fewer than 3 are genuinely supported by the data, suggest fewer.

{digest}"""
                }
            ]
        }
    )

    data = response.json()

    if "error" in data:
        return f"AI error: {data['error']['message']}"

    return data["choices"][0]["message"]["content"]


if __name__ == "__main__":
    import sqlite3
    import sys
    sys.path.append(".")
    from ai.digest_builder import build_digest

    conn = sqlite3.connect("datastorage/jarvis.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM sessions ORDER BY created_at DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        digest = build_digest(row[0])
        print("[*] Sending to AI...")
        result = analyze(digest)
        print("\n=== AI ANALYSIS ===")
        print(result)
