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
                    "content": f"""You are a senior penetration tester.
Analyze these enumeration results and suggest the top 3 initial access vectors.
For each vector explain why it's promising based on the data.
Be specific and technical.
{digest}"""
                }
            ]
        }
    )
    data = response.json()
    print("API response:", data)  # временный дебаг
    return data["choices"][0]["message"]["content"]


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
                    "content": f"""You are a senior penetration tester.
Analyze these enumeration results and suggest the top 3 initial access vectors.
For each vector explain why it's promising based on the data.
Be specific and technical.
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
