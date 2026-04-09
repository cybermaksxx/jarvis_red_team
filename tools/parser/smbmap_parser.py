#!/usr/bin/env python3

def parse_smbmap(file_path: str) -> list:
    """
    Парсит вывод smbmap (shares.txt) и извлекает информацию о шарах.
    
    Returns:
        list[dict]: Список словарей с ключами: ip, disk, permissions, comment
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    results = []
    current_ip = None

    for line in lines:
        line = line.rstrip("\n")
        
        # Пропускаем пустые строки и декоративные элементы
        if not line.strip() or line.startswith(("=", "-", "[*]", "SMBMap", "http")):
            continue

        # Извлекаем IP из строки статуса хоста: [+] IP: 10.114.148.37:445 ...
        if "[+]" in line and "IP:" in line:
            try:
                # Находим часть после "IP:" и до первого пробела/табуляции
                ip_part = line.split("IP:")[1].strip()
                current_ip = ip_part.split()[0]  # Берём только IP:порт
            except IndexError:
                continue
            continue

        # Пропускаем строки с заголовками таблицы
        if "Disk" in line and "Permissions" in line:
            continue
        if line.strip().startswith("----"):
            continue

        # Парсим строки с шарами (начинаются с отступа и имени шара)
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            # Разделяем по множественным пробелам/табам — smbmap использует фиксированную ширину колонок
            parts = [p for p in line.split("  ") if p.strip()]
            
            if len(parts) >= 2 and current_ip:
                disk = parts[0].strip()
                permissions = parts[1].strip()
                # Комментарий может отсутствовать или быть в третьей части
                comment = parts[2].strip() if len(parts) > 2 else ""

                result = {
                    "ip": current_ip,
                    "disk": disk,
                    "permissions": permissions,
                    "comment": comment,
                }
                results.append(result)

    return results


if __name__ == "__main__":
    results = parse_smbmap("shares.txt")

    for r in results:
        print(f"{r['ip']:20} | {r['disk']:15} | {r['permissions']:12} | {r['comment']}")






























