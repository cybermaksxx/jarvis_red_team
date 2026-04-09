#!/usr/bin/env python3
import json

def parse_ffuf(file_path: str) -> list:
    with open(file_path, "r") as f:
        data = json.load(f)
    
    results = []
    for item in data["results"]:
        result = {
            "found": item["input"]["FUZZ"],
            "url": item["url"],
            "host": item["host"],
            "status_code": item["status"],
            "size": item["length"],
        }
        results.append(result)
    
    return results


if __name__ == "__main__":
    # тест директорий
    print("=== DIRS ===")
    results = parse_ffuf("/tmp/ffuf2_test.json")
    for r in results:
        print(f"{r['status_code']} | {r['url']} | size: {r['size']}")
    
    # тест субдоменов
    print("=== SUBDOMAINS ===")
    results = parse_ffuf("/tmp/ffuf_test.json")
    for r in results:
        print(f"{r['status_code']} | {r['host']} | size: {r['size']}")












































