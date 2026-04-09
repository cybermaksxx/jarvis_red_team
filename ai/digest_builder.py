#!/usr/bin/env python3
import sqlite3

DB_PATH = "datastorage/jarvis.db"

def build_digest(session_id: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # шаг 1 — получи целевой хост из таблицы sessions
    cursor.execute("SELECT target FROM sessions WHERE id = ?", (session_id,))
    session = cursor.fetchone()
    target = session[0] if session else "unknown"

    # шаг 2 — получи все порты
    cursor.execute("SELECT host, port, protocol, service, version FROM ports")
    ports = cursor.fetchall()

    # шаг 3 — получи все директории
    cursor.execute("SELECT url, status_code FROM directories")
    dirs = cursor.fetchall()

    # шаг 4 — получи все smb шары
    cursor.execute("SELECT ip, disk, permissions FROM smb_shares WHERE session_id = ?", (session_id,))
    shares = cursor.fetchall()

    conn.close()

    # шаг 5 — собери текст
    # подсказка: используй f-string и \n для переносов строк
    digest = f"Target: {target}\n\n"

    digest += "=== OPEN PORTS ===\n"
    for port in ports:
        digest += f"{port[0]} | {port[1]}/{port[2]} | {port[3]} | {port[4]}\n"

    digest += "\n=== WEB DIRECTORIES ===\n"
    for d in dirs:
        # напиши сам — по образцу портов выше
        digest += f"{d[0]} | {d[1]}\n" 
        
    digest += "\n=== SMB SHARES ===\n"
    for s in shares:
        # напиши сам
        digest += f"{s[0]} | {s[1]} | {s[2]}\n"

    return digest


if __name__ == "__main__":
    # для теста — возьми последний session_id из базы
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM sessions ORDER BY created_at DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        digest = build_digest(row[0])
        print(digest)
