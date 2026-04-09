#!/usr/bin/env python3

class TaskQueue:
    def __init__(self):
        # создай пустой список tasks
        self.tasks = []

    def add_task(self, tool: str, target: str, priority: str, session_id: str):
        # создай словарь task с четырьмя ключами
        # добавь его в self.tasks
        task = {
            "tool": tool,
            "target": target,
            "priority": priority,
            "session_id": session_id
        }
        self.tasks.append(task)

    def get_next_task(self):
        # возвращает первую задачу с HIGH приоритетом
        # если HIGH нет — возвращает первую MEDIUM
        # если очередь пустая — возвращает None
        for task in self.tasks:
            if task["priority"] == "HIGH":
                self.tasks.remove(task)
                return task
        for task in self.tasks:
            if task["priority"] == "MEDIUM":
                self.tasks.remove(task)
                return task
        return None

    def is_empty(self) -> bool:
        # возвращает True если задач нет
        return len(self.tasks) == 0


if __name__ == "__main__":
    queue = TaskQueue()
    
    queue.add_task("dirsearch", "http://192.168.1.1", "HIGH", "session_001")
    queue.add_task("ssh_scan", "192.168.1.1", "MEDIUM", "session_001")
    
    print(queue.is_empty())     # False — две задачи в очереди
    print(queue.get_next_task()) # dirsearch — HIGH первым
    print(queue.get_next_task()) # ssh_scan — MEDIUM вторым
    print(queue.is_empty())     # True — очередь пуста
    print(queue.get_next_task()) # None — нечего брать




























