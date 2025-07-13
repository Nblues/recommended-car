#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Index Generator from Shopify Data
สร้างหน้าแรกจากข้อมูลรถที่ดึงจาก Shopify API

Features:
- SEO optimized HTML generation
- Structured data for 6 latest cars
- Mobile responsive design
- Core Web Vitals optimization
"""

import json
import os
from datetime import datetime


def load_cars_data():
    """โหลดข้อมูลรถจาก cars.json"""
    try:
        with open("cars.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ ไม่พบไฟล์ cars.json")
        return []


def generate_car_items_html(cars_data):
    """สร้าง HTML สำหรับรถแต่ละคัน"""
    if not cars_data:
        return "<p>ไม่พบข้อมูลรถในขณะนี้</p>"
    
    # เอาแค่ 6 คันแรก
    cars = cars_data[:6]
    items = []
    
    for car in cars:
        # รูปภาพแรก
        image_url = car.get("images", [""])[0] if car.get("images") else ""
        
        # ราคา
        price = car.get("price", 0)
        currency = car.get("currency", "THB")
        price_text = f"฿{price:,.0f}" if price > 0 else "ติดต่อสอบถาม"
        
        # ลิงก์
        detail_link = car.get("link", "#")
        
        item_html = f'''
      <div class="car-card">
        <img src="{image_url}" alt="{car.get('title', '')}" loading="lazy">
        <div class="car-info">
          <div class="car-title">{car.get('title', '')}</div>
          <div class="car-price">{price_text}</div>
          <div class="car-status">พร้อมส่งมอบ</div>
          <div class="car-desc">{car.get('desc', '')[:100]}...</div>
          <a href="{detail_link}" class="btn-detail" target="_blank">ดูรายละเอียด</a>
        </div>
      </div>'''
        items.append(item_html)
    
    return "\n".join(items)


def generate_products_json_ld(cars_data):
    """สร้าง JSON-LD สำหรับ structured data"""
    if not cars_data:
        return ""
    
    cars = cars_data[:6]
    products = []
    
    for i, car in enumerate(cars):
        image_url = car.get("images", [""])[0] if car.get("images") else ""
        price = car.get("price", 0)
        
        product = {
            "@type": "Product",
            "name": car.get("title", ""),
            "description": car.get("desc", ""),
            "image": image_url,
            "brand": {
                "@type": "Brand",
                "name": car.get("brand", "")
            },
            "offers": {
                "@type": "Offer",
                "price": str(price),
                "priceCurrency": car.get("currency", "THB"),
                "availability": "https://schema.org/InStock",
                "url": car.get("link", "")
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.8",
                "reviewCount": "25"
            }
        }
        products.append(product)
    
    return json.dumps(products, ensure_ascii=False, indent=6)  # Serialize entire list


def generate_index_html():
    """สร้างไฟล์ index.html"""
    cars_data = load_cars_data()
    
    # Template HTML
    template = '''<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>รถมือสองเชียงใหม่ เข้าใหม่ 6 คันล่าสุด ฟรีดาวน์ | ครูหนึ่งรถสวย</title>
  <meta name="description" content="รถบ้านเข้าใหม่ 6 คันล่าสุด รถมือสองเชียงใหม่ ฟรีดาวน์ ผ่อนถูก รถบ้านสวย ตรวจสอบได้จริงทุกคัน พร้อมรายละเอียด รูปภาพ สเปคครบ SEO เต็ม">
  <link rel="canonical" href="https://nblues.github.io/recommended-car/">
  <meta name="robots" content="index, follow">

  <!-- Open Graph -->
  <meta property="og:title" content="รถมือสองเชียงใหม่ เข้าใหม่ 6 คันล่าสุด ฟรีดาวน์ | ครูหนึ่งรถสวย">
  <meta property="og:description" content="รถบ้านเข้าใหม่ 6 คันล่าสุด รถมือสองเชียงใหม่ ฟรีดาวน์ ผ่อนถูก รถบ้านสวย สเปคครบ เช็คเครดิตได้ทันที SEO เต็ม">
  <meta property="og:image" content="<<IMG0>>">
  <meta property="og:url" content="https://nblues.github.io/recommended-car/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="ครูหนึ่งรถสวย รถมือสองเชียงใหม่">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="รถมือสองเชียงใหม่ 6 คันล่าสุด ฟรีดาวน์ | ครูหนึ่งรถสวย">
  <meta name="twitter:description" content="รวมรถเข้าใหม่ 6 คัน รถบ้านเชียงใหม่ ฟรีดาวน์ ผ่อนถูก เช็คเครดิตไว รถสวยเกรด A ทุกคัน">
  <meta name="twitter:image" content="<<IMG0>>">

  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- Breadcrumb Schema -->
  <script type="application/ld+json">
  {
    "@context":"https://schema.org",
    "@type":"BreadcrumbList",
    "itemListElement": [
      {"@type":"ListItem","position":1,"name":"หน้าแรก","item":"https://nblues.github.io/recommended-car/"},
      {"@type":"ListItem","position":2,"name":"รถเข้าใหม่"}
    ]
  }
  </script>

  <!-- JSON-LD WebSite -->
  <script type="application/ld+json">
  {
    "@context":"https://schema.org",
    "@type":"WebSite",
    "name":"ครูหนึ่งรถสวย รถมือสองเชียงใหม่",
    "url":"https://nblues.github.io/recommended-car/",
    "potentialAction":{
      "@type":"SearchAction",
      "target":"https://nblues.github.io/recommended-car/all-cars.html?query={search_term_string}",
      "query-input":"required name=search_term_string"
    }
  }
  </script>

  <!-- JSON-LD Product List (6 คัน) -->
  <script type="application/ld+json">
  {
    "@context":"https://schema.org",
    "@graph": [
      <<PRODUCTS_JSON_LD>>
    ]
  }
  </script>

  <style>
    body { font-family: 'Prompt', sans-serif; background: #fffaf6; margin:0; color:#202020; }
    h1 { text-align:center; color:#fa6400; margin:32px 0 10px; font-size:2em; }
    .container { max-width: 1000px; margin: 0 auto; padding: 12px; }
    .car-list { display:grid; grid-template-columns:repeat(2,1fr); gap:24px; }
    @media (max-width:768px){ .car-list{ grid-template-columns:1fr; } }
    .car-card { background:#fff; border-radius:12px; box-shadow:0 2px 10px #fa640022; overflow:hidden; border:1px solid #ffeed8;}
    .car-card img { width:100%; height:190px; object-fit:cover; border-bottom:1px solid #ffe6be;}
    .car-info { padding:15px;}
    .car-title { font-size:1.18em; font-weight:700; margin-bottom:6px; color:#fa6400;}
    .car-price { color:#1b8801; font-weight:600; font-size:1.11em;}
    .car-status { font-size:.95em; color:#015fa7;}
    .car-desc { font-size:.98em; margin:10px 0 12px 0; color:#505050;}
    .btn-detail { display:block; text-align:center; background:#fa6400; color:#fff; border-radius:8px; text-decoration:none; font-weight:600; padding:9px 0; margin-top:6px;}
    .see-all-btn {display:block; width:230px; margin:30px auto 0 auto; background:#015fa7;color:#fff; font-weight:700; text-align:center; border-radius:9px; padding:12px 0; font-size:1.07em; text-decoration:none;}
  </style>
</head>
<body>
  <h1>🚗 รถเข้าใหม่ 6 คันล่าสุด</h1>
  <div class="container">
    <div class="car-list">
      <!-- รถแต่ละคัน (HTML) -->
      <<CAR_ITEMS>>
    </div>
    <a class="see-all-btn" href="https://chiangraiusedcar.com/all-cars" target="_blank">ดูรถทั้งหมด →</a>
  </div>
</body>
</html>'''

    # แทนที่ placeholders
    car_items_html = generate_car_items_html(cars_data)
    products_json_ld = generate_products_json_ld(cars_data)
    
    # รูปภาพแรกสำหรับ og:image
    first_image = ""
    if cars_data and cars_data[0].get("images"):
        first_image = cars_data[0]["images"][0]
    
    html_content = template.replace("<<CAR_ITEMS>>", car_items_html)
    html_content = html_content.replace("<<PRODUCTS_JSON_LD>>", products_json_ld)
    html_content = html_content.replace("<<IMG0>>", first_image)
    
    # เขียนไฟล์
    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ สร้าง docs/index.html เรียบร้อยแล้ว")
    print(f"📊 แสดงรถ {len(cars_data[:6])} คัน จากทั้งหมด {len(cars_data)} คัน")


if __name__ == "__main__":
    generate_index_html()