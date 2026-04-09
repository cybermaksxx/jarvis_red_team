#!/usr/bin/env python3

def parse_dirsearch(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    results = []

    for line in lines:
        line = line.strip()

        
        if line.startswith("#") or not line:
            continue

        parts = line.split()

        # it must be 3 elements at least
        if len(parts) < 3:
            continue

        result = {
            "status_code": int(parts[0]),
            "size": parts[1],        
            "url": parts[2],
        }

        results.append(result)

    return results


if __name__ == "__main__":
    results = parse_dirsearch("output_dirs.txt")

    for r in results:
        print(f"{r['status_code']} | {r['size']} | {r['url']}")


















