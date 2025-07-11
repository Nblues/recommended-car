#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os

# โหลดข้อมูลจาก cars.json
with open("cars.json", encoding="utf-8") as f:
    cars = json.load(f)

# แม่แบบ HTML
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{images[0]}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{images[0]}">
  <script type="application/ld+json">
{{
  "@context":"https://schema.org",
  "@type":"Product",
  "name":"{title}",
  "image":{images},
  "description":"{desc}",
  "brand":{brand},
  "offers": {{
    "@type": "Offer",
    "priceCurrency": "{currency}",
    "price": {price},
    "availability": "https://schema.org/InStock",
    "url": "{url}"
  }}
}}
  </script>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <nav><a href="../all-cars.html">← กลับหน้ารวมรถ</a></nav>
  <main class="car-detail">
    <h1>{title}</h1>
    <div class="gallery">
      {gallery_html}
    </div>
    <p>ราคา: {price_display} {currency}</p>
    <p>{full_desc}</p>
    <a class="btn" href="https://lin.ee/cJuakxZ" target="_blank">สอบถามผ่าน LINE</a>
    <a class="btn" href="{fb_link}" target="_blank">ดูรถบน Facebook</a>
  </main>
</body>
</html>
"""

# สร้างโฟลเดอร์ output
out_dir = "docs/car-detail"
os.makedirs(out_dir, exist_ok=True)

for car in cars:
    slug = car["slug"]  # ex: toyota-camry-2020
    title = car["title"]
    desc = car.get("short_desc","")
    full_desc = car.get("full_desc", desc)
    currency = car.get("currency","THB")
    price = car.get("price",0)
    # แสดงราคากลับเป็นตัวเลขไม่คั่น comma
    price_display = f"{price}"
    url = f"https://chiangraiusedcar.com/car-detail/{slug}.html"

    # แพ็คภาพและ gallery
    images = car.get("images", [])
    gallery_html = ""
    for img in images:
        gallery_html += f'<img src="{img}" alt="{title}">\n      '

    # JSON-LD brand object ไม่ใช่ string
    brand = json.dumps({"@type":"Brand", "name":car["brand"]}, ensure_ascii=False)

    fb_link = car.get("fb_link","https://facebook.com/ครูหนึ่งรถสวย")

    html = HTML_TEMPLATE.format(
        title=title,
        desc=desc,
        full_desc=full_desc,
        currency=currency,
        price=price,
        price_display=price_display,
        url=url,
        images=json.dumps(images, ensure_ascii=False),
        gallery_html=gallery_html,
        brand=brand,
        fb_link=fb_link
    )

    # เขียนไฟล์
    out_path = os.path.join(out_dir, f"{slug}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

print("✅ generate_car_detail.py รันจบ สร้างครบทุกไฟล์แล้ว")