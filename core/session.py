#!/usr/bin/env python3
import os
import datetime
import sqlite3

DB_PATH = "datastorage/jarvis.db"
SESSIONS_DIR = "sessions"

def create_session(target: str) -> str:
    # create unique session ID using timestamp and target
    session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + target

    # create folder for this session
    session_path = f"sessions/{session_id}"
    os.makedirs(session_path, exist_ok=True)

    # save session to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sessions (id, target, created_at)
        VALUES (?, ?, ?)
    """, (
        session_id,
        target,
        datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    ))
    conn.commit()
    conn.close()

    print(f"Session created: {session_id}")
    return session_id


if __name__ == "__main__":
    sid = create_session("192.168.1.1")
    print(f"Session ID: {sid}")


































