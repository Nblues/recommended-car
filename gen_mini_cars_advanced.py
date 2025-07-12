#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Enhanced Mini Cars Widget Generator
สร้าง Widget รถเข้าใหม่ 6 คันด้วย Advanced SEO และ Performance Optimization

Features:
- Optimized for embedding in GoDaddy or other websites
- Core Web Vitals optimization
- Lazy loading and performance optimization
- Structured data for rich snippets
"""

import json
import os
from pathlib import Path
from datetime import datetime
from build_advanced_seo_system import AdvancedSEOBuilder


class MiniCarsWidgetGenerator:
    def __init__(self):
        self.seo_builder = AdvancedSEOBuilder()
        self.cars_data = self.seo_builder.cars_data
        self.base_url = "https://nblues.github.io/recommended-car"

    def generate_mini_car_html(self, car, index):
        """สร้าง HTML card สำหรับ mini widget"""
        # ใช้ lazy loading สำหรับรูปที่ 2 เป็นต้นไป
        loading = "eager" if index == 0 else "lazy"
        
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
        
        # Optimized image URL for thumbnail
        thumb_image = main_image.replace('.jpg', '_300x225.jpg').replace('.png', '_300x225.png')
        
        return f"""
        <div class="car-mini" onclick="window.open('{car['link']}', '_blank')" 
             itemscope itemtype="https://schema.org/Product">
          <img src="{thumb_image}" 
               alt="{car['title']}" 
               class="car-image"
               loading="{loading}" 
               decoding="async"
               width="300" 
               height="225"
               itemprop="image">
          <div class="car-content">
            <h3 class="car-title" itemprop="name">{car['title'][:50]}{'...' if len(car['title']) > 50 else ''}</h3>
            <div class="car-price" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
              <span itemprop="price">฿{car['price']:,.0f}</span>
              <meta itemprop="priceCurrency" content="{car['currency']}">
              <meta itemprop="availability" content="https://schema.org/InStock">
            </div>
            <div class="car-features">
              <span class="car-feature">🚗 {brand}</span>
              {f'<span class="car-feature">📅 {year}</span>' if year else ''}
              <span class="car-feature">📍 เชียงใหม่</span>
            </div>
            <button class="car-cta" aria-label="ดูรายละเอียด {car['title']}">
              ดูรายละเอียด
            </button>
          </div>
          <meta itemprop="brand" content="{brand}">
          <meta itemprop="description" content="{car['desc'][:100]}...">
        </div>"""

    def generate_widget_cars_html(self):
        """สร้าง HTML สำหรับรถ 6 คันใน widget"""
        cars_html = ""
        for i, car in enumerate(self.cars_data[:6]):
            cars_html += self.generate_mini_car_html(car, i)
        return cars_html

    def generate_car_schema_list(self):
        """สร้าง Schema list สำหรับ widget"""
        car_items = []
        for i, car in enumerate(self.cars_data[:6]):
            car_items.append({
                "@type": "ListItem",
                "position": i + 1,
                "item": {
                    "@type": "Product",
                    "name": car["title"],
                    "image": car["images"][0] if car["images"] else "",
                    "description": car["desc"][:100] + "..." if len(car["desc"]) > 100 else car["desc"],
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
        template_path = Path("templates/mini-cars-advanced.html")
        if template_path.exists():
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return self.get_basic_template()

    def get_basic_template(self):
        """Template พื้นฐานถ้าไม่มีไฟล์ template"""
        return """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Widget รถเข้าใหม่ 6 คัน | ครูหนึ่งรถสวย</title>
  <style>
    body { font-family: 'Prompt', sans-serif; margin: 0; background: #f7f7fb; padding: 0.5rem; }
    .widget-container { max-width: 900px; margin: 0 auto; background: #fff; border-radius: 16px; overflow: hidden; }
    .cars-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; padding: 1.5rem; }
    .car-mini { background: #fff; border: 1px solid #e9ecef; border-radius: 12px; overflow: hidden; cursor: pointer; }
    .car-image { width: 100%; height: 180px; object-fit: cover; }
    .car-content { padding: 1rem; }
    .car-title { font-size: 1rem; font-weight: 700; margin: 0 0 0.5rem; }
    .car-price { font-size: 1.4rem; color: #e74c3c; font-weight: 800; margin: 0 0 0.75rem; }
    .car-cta { background: #f47b20; color: #fff; padding: 0.6rem 1rem; border: none; border-radius: 6px; font-weight: 700; cursor: pointer; width: 100%; }
  </style>
</head>
<body>
  <div class="widget-container">
    <div class="cars-grid">
      {cars_widget_html}
    </div>
  </div>
</body>
</html>"""

    def generate_widget(self):
        """สร้าง mini-cars-static.html widget"""
        print("🎯 สร้าง Mini Cars Widget ด้วย Advanced SEO...")
        
        # โหลด template
        template = self.load_template()
        
        # สร้างข้อมูลสำหรับ template
        cars_html = self.generate_widget_cars_html()
        car_schema_list = self.generate_car_schema_list()
        
        # รูปรถคันแรกสำหรับ OG image
        first_car_image = self.cars_data[0]["images"][0] if self.cars_data and self.cars_data[0]["images"] else ""
        
        # ข้อมูลสำหรับ template
        template_data = {
            'cars_widget_html': cars_html,
            'car_schema_list': json.dumps(car_schema_list, ensure_ascii=False),
            'total_cars': len(self.cars_data),
            'last_update': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'first_car_image': first_car_image
        }
        
        # แทนที่ข้อมูลใน template
        html_content = template.format(**template_data)
        
        # บันทึกไฟล์
        docs_path = Path("docs")
        docs_path.mkdir(exist_ok=True)
        
        widget_path = docs_path / "mini-cars-static.html"
        with open(widget_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ สร้าง mini-cars-static.html สำเร็จ")
        print(f"📊 รถทั้งหมด: {len(self.cars_data)} คัน")
        print(f"🎯 Widget รถล่าสุด: 6 คัน")
        print(f"⚡ Performance: Optimized for embedding")
        print(f"🔍 SEO: Widget structured data")


def main():
    """ฟังก์ชันหลักสำหรับรันสคริปต์"""
    generator = MiniCarsWidgetGenerator()
    generator.generate_widget()


if __name__ == "__main__":
    main()