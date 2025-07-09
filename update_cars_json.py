import requests
import json

API_URL = "https://www.kn-goodcar.com/api/cars"  # เปลี่ยนเป็น API endpoint จริง

def update_cars_json():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        cars = response.json()
        latest_6 = cars[:6]
        with open("cars.json", "w", encoding="utf-8") as f:
            json.dump(latest_6, f, ensure_ascii=False, indent=2)
        print("อัปเดต cars.json เรียบร้อย 6 คันล่าสุด!")
    except Exception as e:
        print("เกิดข้อผิดพลาด:", e)

if __name__ == "__main__":
    update_cars_json()