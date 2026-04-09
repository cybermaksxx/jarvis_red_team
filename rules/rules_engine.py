#!/usr/bin/env python3
import sys
sys.path.append(".")
from core.task_queue import TaskQueue
import yaml
import sqlite3

DB_PATH = "datastorage/jarvis.db"

def load_rules() -> list:
    # открой rules.yaml и верни список правил
    # подсказка: yaml.safe_load(f)
    with open("rules/rules.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data["rules"]


def apply_rules(session_id: str, queue) -> None:
    # читает порты из базы для данной сессии
    # для каждого порта проверяет все правила
    # если условие совпадает — добавляет задачу в очередь

    rules = load_rules()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT host, port, service FROM ports")
    ports = cursor.fetchall()
    conn.close()

    for port in ports:
        host = port[0]
        service = port[2]

        for rule in rules:
            # проверяем совпадение сервиса
            if rule["condition"]["service"] == service:
                print(f"Rule matched: {rule['name']} on {host}")
                queue.add_task(
                    tool=rule["action"],
                    target=host,
                    priority=rule["priority"],
                    session_id=session_id
                )


if __name__ == "__main__":
    queue = TaskQueue()
    apply_rules("test_session", queue)
    
    print("\nTasks in queue:")
    while not queue.is_empty():
        print(queue.get_next_task())
