import sqlite3

DB_PATH = "datastorage/jarvis.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # создаём таблицу портов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ports (
            id INTEGER PRIMARY KEY,
            host TEXT,
            port INTEGER,
            protocol TEXT,
            service TEXT,
            version TEXT
        )
    """)
    
    # создаём таблицу директорий
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS directories (
            id INTEGER PRIMARY KEY,
            url TEXT,
            status_code INTEGER,
            size TEXT
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            target TEXT,
            created_at TEXT
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS smb_shares (
            id INTEGER PRIMARY KEY,
            ip TEXT,
            disk TEXT,
            permissions TEXT,
            comment TEXT,
            session_id TEXT
        )
    """)


    conn.commit()
    conn.close()
    print("Base is ready ")


def save_port(data: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # INSERT кладёт данные в таблицу
    # ? — место куда Python подставит значения из кортежа
    cursor.execute("""
        INSERT INTO ports (host, port, protocol, service, version)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["host"],
        data["port"],
        data["protocol"],
        data["service"],
        data["version"]
    ))
    
    conn.commit()
    conn.close()


def save_directory(data: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO directories (url, status_code, size)
        VALUES (?, ?, ?)
    """, (
        data["url"],
        data["status_code"],
        data["size"]
    ))
    
    conn.commit()
    conn.close()

def get_all_ports() -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # SELECT * читает все строки из таблицы
    cursor.execute("SELECT * FROM ports")
    rows = cursor.fetchall()
    conn.close()
    
    # rows — список кортежей: (1, '192.168.1.1', 22, 'tcp', 'ssh', '8.2')
    # превращаем каждый кортеж в словарь
    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "host": row[1],
            "port": row[2],
            "protocol": row[3],
            "service": row[4],
            "version": row[5]
        })
    
    return results

def clear_ports():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ports")
    conn.commit()
    conn.close()



def save_smb_share(data: dict, session_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO smb_shares (ip, disk, permissions, comment, session_id)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["ip"],
        data["disk"],
        data["permissions"],
        data["comment"],
        session_id
    ))
    conn.commit()
    conn.close()







if __name__ == "__main__":
    init_db()
    
    save_port({
        "host": "192.168.1.1",
        "port": 80,
        "protocol": "tcp",
        "service": "http",
        "version": "Apache 2.4.9"
    })
    
    save_directory({
        "url": "http://192.168.1.1/admin",
        "status_code": 200,
        "size": "477B"
    })
    
    print(get_all_ports())






