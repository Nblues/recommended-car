#!/usr/bin/env python3
import sys, json, requests

URL = "https://raw.githubusercontent.com/Nblues/recommended-car/main/cars.json"
resp = requests.get(URL)
if resp.status_code != 200:
    print(f"❌ ดึงไม่สำเร็จ {resp.status_code}")
    print(resp.text[:200])
    sys.exit(1)

text = resp.text.strip()
if not text:
    print("❌ body ว่างเปล่า")
    sys.exit(1)

try:
    cars = resp.json()
except json.JSONDecodeError:
    print("❌ ไม่ใช่ JSON:")
    print(text[:200])
    sys.exit(1)

with open("cars.json", "w", encoding="utf-8") as f:
    json.dump(cars, f, ensure_ascii=False, indent=2)
print("✅ update cars.json เสร็จ")