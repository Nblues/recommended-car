#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: generate_car_detail.py
สร้าง car-detail/xxx.html แยกแต่ละคัน จาก feed.xml (ไม่ต้องใช้ cars.json แล้ว)
"""
import os
import xml.etree.ElementTree as ET

# --- config
FEED_FILE = "feed.xml"
OUT_DIR = "docs/car-detail"
TEMPLATE = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>{title} | รถมือสองคุณภาพดี</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{detail_url}">
  <meta property="og:title" content="{title} | รถมือสองคุณภาพดี">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{img}">
  <meta property="og:url" content="{detail_url}">
  <meta property="og:type" content="product">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{img}">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "{title}",
    "description": "{desc}",
    "image": "{img}",
    "offers": {{
      "@type": "Offer",
      "price": "{price}",
      "priceCurrency": "THB",
      "availability": "https://schema.org/InStock"
    }}
  }}
  </script>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <div class="car-detail">
    <img src="{img}" alt="{title}" style="max-width:400px;">
    <h1>{title}</h1>
    <div class="car-desc">{desc}</div>
    <div class="car-price">฿{price:,}</div>
    <a href="../index.html">← กลับหน้ารวม</a>
  </div>
</body>
</html>
"""

def parse_feed(feed_file):
    tree = ET.parse(feed_file)
    root = tree.getroot()
    items = []
    for item in root.findall("./channel/item"):
        handle = item.findtext("guid") or item.findtext("handle")
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        desc = item.findtext("description") or ""
        pubDate = item.findtext("pubDate") or ""
        # ดึงรูปจาก description (CDAT)
        import re
        img_match = re.search(r"<img[^>]+src=['\"]([^'\"]+)['\"]", desc)
        img = img_match.group(1) if img_match else ""
        # ดึงราคา (จาก title หรือ description)
        price_match = re.search(r"฿([\d,]+)", title+desc)
        price = price_match.group(1).replace(",","") if price_match else "0"
        # ลบ tag html ใน desc
        desc_clean = re.sub(r"<[^>]+>", "", desc).strip()
        items.append({
            "handle": handle.strip(),
            "title": title.strip(),
            "desc": desc_clean,
            "img": img,
            "price": int(price),
            "detail_url": f"https://nblues.github.io/recommended-car/car-detail/{handle}.html"
        })
    return items

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    items = parse_feed(FEED_FILE)
    for car in items:
        html = TEMPLATE.format(**car)
        outpath = os.path.join(OUT_DIR, f"{car['handle']}.html")
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(html)
    print(f"Generate {len(items)} car-detail pages DONE.")

if __name__ == "__main__":
    main()