import requests, json

API_URL = "https://www.kn-goodcar.com/api/cars"  # ปรับ URL ให้ตรงกับ endpoint JSON จริง
resp = requests.get(API_URL)
cars = resp.json()
latest_6 = cars[:6]
with open("cars.json", "w", encoding="utf-8") as f:
    json.dump(latest_6, f, ensure_ascii=False, indent=2)
print("อัปเดต cars.json เรียบร้อย 6 คันล่าสุด!")