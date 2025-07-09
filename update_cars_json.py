import requests
import json

# ตัวอย่างดึงจาก Shopify API หรือ REST API (เปลี่ยน endpoint ตามจริง)
API_URL = "https://www.kn-goodcar.com/api/cars"  # ต้นทางรถทั้งหมด (JSON)

response = requests.get(API_URL)
cars = response.json()

# ตัดเอาแค่ 6 คันแรก
latest_6 = cars[:6]

with open("cars.json", "w", encoding="utf-8") as f:
    json.dump(latest_6, f, ensure_ascii=False, indent=2)

print("อัปเดต cars.json เรียบร้อย 6 คันล่าสุด!")