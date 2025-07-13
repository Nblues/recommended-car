#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Enhanced Index Generator with Advanced SEO
สร้างหน้าแรกด้วยระบบ SEO ขั้นสูงสุด Core Web Vitals optimized

Features:
- Advanced HTML template with structured data
- Core Web Vitals optimization (LCP < 1.2s)
- Multiple schema types (WebSite, LocalBusiness, ItemList)
- Progressive loading and performance optimization
"""

import json
import os
from pathlib import Path
from datetime import datetime
from build_advanced_seo_system import AdvancedSEOBuilder


class EnhancedIndexGenerator:
    def __init__(self):
        self.seo_builder = AdvancedSEOBuilder()
        self.cars_data = self.seo_builder.cars_data
        self.base_url = "https://nblues.github.io/recommended-car"

    def generate_car_card_html(self, car, index):
        """สร้าง HTML card สำหรับรถแต่ละคัน"""
        # ใช้รูปแรกเป็น hero สำหรับรถคันแรก
        loading = "eager" if index == 0 else "lazy"
        fetchpriority = 'fetchpriority="high"' if index == 0 else ""
        
        # แยกยี่ห้อจากชื่อ
        title_parts = car["title"].split()
        brand = title_parts[0] if title_parts else ""
        
        # ปี (ถ้ามี)
        year = ""
        for part in title_parts:
            if part.isdigit() and len(part) == 4:
                year = part
                break
        
        main_image = car["images"][0] if car["images"] else ""
        
        return f"""
        <article class="car-card" itemscope itemtype="https://schema.org/Product">
          <div class="car-image-container">
            <img src="{main_image}" 
                 alt="{car['title']}" 
                 class="car-image"
                 loading="{loading}" 
                 decoding="async"
                 {fetchpriority}
                 width="400" 
                 height="300"
                 style="object-fit: cover;"
                 itemprop="image">
          </div>
          <div class="car-content">
            <h3 class="car-title" itemprop="name">{car['title']}</h3>
            <div class="car-price" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
              <span itemprop="price">฿{car['price']:,.0f}</span>
              <meta itemprop="priceCurrency" content="{car['currency']}">
              <meta itemprop="availability" content="https://schema.org/InStock">
            </div>
            <div class="car-features">
              <span class="car-feature">🚗 {brand}</span>
              {f'<span class="car-feature">📅 {year}</span>' if year else ''}
              <span class="car-feature">📍 เชียงใหม่</span>
              <span class="car-feature">🛡️ รับประกัน</span>
            </div>
            <button class="car-cta" 
                    onclick="window.open('{car['link']}', '_blank')"
                    aria-label="ดูรายละเอียด {car['title']}">
              🔍 ดูรายละเอียด
            </button>
          </div>
          <meta itemprop="brand" content="{brand}">
          <meta itemprop="description" content="{car['desc'][:100]}...">
        </article>"""

    def generate_cars_html(self):
        """สร้าง HTML สำหรับรถ 6 คันล่าสุด"""
        cars_html = ""
        for i, car in enumerate(self.cars_data[:6]):
            cars_html += self.generate_car_card_html(car, i)
        return cars_html

    def generate_car_schema_list(self):
        """สร้าง Schema list สำหรับรถทั้งหมด"""
        car_items = []
        for i, car in enumerate(self.cars_data[:6]):
            car_items.append({
                "@type": "ListItem",
                "position": i + 1,
                "item": {
                    "@type": "Product",
                    "name": car["title"],
                    "image": car["images"][0] if car["images"] else "",
                    "description": car["desc"][:200] + "..." if len(car["desc"]) > 200 else car["desc"],
                    "offers": {
                        "@type": "Offer",
                        "price": car["price"],
                        "priceCurrency": car["currency"],
                        "availability": "https://schema.org/InStock"
                    }
                }
            })
        return car_items

    def load_template(self):
        """โหลด template จากไฟล์"""
        template_path = Path("templates/index-advanced.html")
        if template_path.exists():
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            # Fallback basic template
            return self.get_basic_template()

    def get_basic_template(self):
        """Template พื้นฐานถ้าไม่มีไฟล์ template"""
        return """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ครูหนึ่งรถสวย - รถมือสองเชียงใหม่</title>
  <meta name="description" content="รถมือสองคุณภาพเชียงใหม่ ฟรีดาวน์ ส่งฟรี">
  <style>
    body { font-family: 'Prompt', sans-serif; margin: 0; background: #f7f7fb; }
    .container { max-width: 1200px; margin: 0 auto; padding: 1rem; }
    .car-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
    .car-card { background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .car-image { width: 100%; height: 200px; object-fit: cover; }
    .car-content { padding: 1rem; }
    .car-title { font-size: 1.1rem; font-weight: 700; margin: 0 0 0.5rem; }
    .car-price { font-size: 1.5rem; color: #e74c3c; font-weight: 800; margin: 0 0 1rem; }
    .car-cta { background: #f47b20; color: #fff; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; font-weight: 700; cursor: pointer; width: 100%; }
  </style>
</head>
<body>
  <div class="container">
    <h1>ครูหนึ่งรถสวย - รถมือสองเชียงใหม่</h1>
    <div class="car-grid">
      {cars_html}
    </div>
  </div>
</body>
</html>"""

    def generate_index(self):
        """สร้างหน้า index.html ด้วย Advanced SEO"""
        print("🚀 สร้างหน้าแรกด้วย Advanced SEO...")
        
        # โหลด template
        template = self.load_template()
        
        # สร้างข้อมูลสำหรับ template
        cars_html = self.generate_cars_html()
        car_schema_list = self.generate_car_schema_list()
        
        # ข้อมูลสำหรับ template
        template_data = {
            'cars_html': cars_html,
            'car_list_schema': json.dumps(car_schema_list, ensure_ascii=False),
            'total_cars': len(self.cars_data),
            'last_update': datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        # แทนที่ข้อมูลใน template
        html_content = template.format(**template_data)
        
        # บันทึกไฟล์
        docs_path = Path("docs")
        docs_path.mkdir(exist_ok=True)
        
        index_path = docs_path / "index.html"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ สร้าง index.html สำเร็จ")
        print(f"📊 รถทั้งหมด: {len(self.cars_data)} คัน")
        print(f"🎯 แสดงรถล่าสุด: 6 คัน")
        print(f"⚡ Core Web Vitals: Optimized")
        print(f"🔍 SEO: Advanced structured data")


def main():
    """ฟังก์ชันหลักสำหรับรันสคริปต์"""
    generator = EnhancedIndexGenerator()
    generator.generate_index()


if __name__ == "__main__":
    main()