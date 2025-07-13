#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚗 Enhanced Car Detail Generator with Advanced SEO
สร้างหน้ารายละเอียดรถแต่ละคันด้วยระบบ SEO ขั้นสูงสุด

Features:
- Advanced Product schema with complete data
- Core Web Vitals optimization
- Rich snippets support
- Image gallery optimization
- Breadcrumb navigation
"""

import json
import os
from pathlib import Path
from datetime import datetime
from build_advanced_seo_system import AdvancedSEOBuilder
from optimize_images import ImageOptimizer


class EnhancedCarDetailGenerator:
    def __init__(self):
        self.seo_builder = AdvancedSEOBuilder()
        self.image_optimizer = ImageOptimizer()
        self.cars_data = self.seo_builder.cars_data
        self.base_url = "https://nblues.github.io/recommended-car"

    def load_template(self):
        """โหลด template จากไฟล์"""
        template_path = Path("templates/car-detail-advanced.html")
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
  <title>{car_title} | ครูหนึ่งรถสวย</title>
  <meta name="description" content="{car_description}">
  <style>
    body { font-family: 'Prompt', sans-serif; margin: 0; background: #f7f7fb; }
    .container { max-width: 1200px; margin: 0 auto; padding: 1rem; }
    .car-header { background: #fff; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; }
    .car-title { font-size: 2rem; font-weight: 700; margin: 0 0 1rem; }
    .car-price { font-size: 2.5rem; color: #e74c3c; font-weight: 800; margin: 0 0 1rem; }
    .car-gallery { display: grid; grid-template-columns: 2fr 1fr; gap: 1rem; margin: 2rem 0; }
    .main-image img { width: 100%; border-radius: 8px; }
    .thumbnail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }
    .thumbnail img { width: 100%; border-radius: 6px; cursor: pointer; }
  </style>
</head>
<body>
  <div class="container">
    <div class="car-header">
      <h1 class="car-title">{car_title}</h1>
      <div class="car-price">฿{car_price:,.0f}</div>
    </div>
    <div class="car-gallery">
      <div class="main-image">
        {hero_image_html}
      </div>
      <div class="thumbnail-grid">
        {thumbnail_images_html}
      </div>
    </div>
    <div class="car-description">
      {car_full_description}
    </div>
  </div>
</body>
</html>"""

    def generate_car_detail_page(self, car):
        """สร้างหน้ารายละเอียดรถแต่ละคัน"""
        # โหลด template
        template = self.load_template()
        
        # สร้าง URL สำหรับรถ
        car_url = f"{self.base_url}/car-detail/{car['handle']}.html"
        
        # สร้าง description ที่เหมาะสำหรับ SEO
        car_description = car['desc'][:160] + "..." if len(car['desc']) > 160 else car['desc']
        car_description = car_description.replace('"', "'")  # ป้องกัน quote issues
        
        # แยกยี่ห้อจากชื่อ
        title_parts = car["title"].split()
        car_brand = title_parts[0] if title_parts else "Unknown"
        
        # สร้าง hero image HTML
        main_image = car["images"][0] if car["images"] else ""
        hero_image_html = self.image_optimizer.generate_hero_image_html(
            main_image, 
            f"{car['title']} - รูปหลัก"
        ) if main_image else ""
        
        # สร้าง thumbnail images HTML
        thumbnail_images_html = ""
        for i, image_url in enumerate(car["images"][1:5]):  # รูปที่ 2-5
            thumbnail_html = self.image_optimizer.generate_responsive_image_html(
                image_url,
                f"{car['title']} - รูปที่ {i+2}",
                "lazy"
            )
            thumbnail_images_html += f'<div class="thumbnail">{thumbnail_html}</div>\n'
        
        # สร้าง Structured Data
        product_schema = json.dumps(
            self.seo_builder.generate_product_schema(car),
            ensure_ascii=False,
            indent=2
        )
        
        breadcrumb_schema = json.dumps(
            self.seo_builder.generate_breadcrumb_schema(car["title"], car_url),
            ensure_ascii=False,
            indent=2
        )
        
        local_business_schema = json.dumps(
            self.seo_builder.generate_structured_data_schemas()[0],  # LocalBusiness
            ensure_ascii=False,
            indent=2
        )
        
        faq_schema = json.dumps(
            self.seo_builder.generate_structured_data_schemas()[1],  # FAQ
            ensure_ascii=False,
            indent=2
        )
        
        # ข้อมูลสำหรับ template
        template_data = {
            'car_title': car['title'],
            'car_description': car_description,
            'car_url': car_url,
            'car_main_image': main_image,
            'car_price': car['price'],
            'car_brand': car_brand,
            'car_full_description': car['desc'],
            'car_link': car['link'],
            'hero_image_html': hero_image_html,
            'thumbnail_images_html': thumbnail_images_html,
            'product_schema': product_schema,
            'breadcrumb_schema': breadcrumb_schema,
            'local_business_schema': local_business_schema,
            'faq_schema': faq_schema
        }
        
        # แทนที่ข้อมูลใน template
        html_content = template.format(**template_data)
        
        return html_content

    def generate_all_car_details(self):
        """สร้างหน้ารายละเอียดสำหรับรถทุกคัน"""
        print("🚗 สร้างหน้ารายละเอียดรถด้วย Advanced SEO...")
        
        # สร้างโฟลเดอร์
        docs_path = Path("docs")
        car_detail_path = docs_path / "car-detail"
        car_detail_path.mkdir(parents=True, exist_ok=True)
        
        generated_count = 0
        
        for car in self.cars_data:
            try:
                # สร้าง HTML content
                html_content = self.generate_car_detail_page(car)
                
                # บันทึกไฟล์
                file_path = car_detail_path / f"{car['handle']}.html"
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                
                generated_count += 1
                
            except Exception as e:
                print(f"❌ Error generating {car['handle']}: {e}")
        
        print(f"✅ สร้างหน้ารายละเอียดรถสำเร็จ: {generated_count} หน้า")
        print(f"📊 รถทั้งหมด: {len(self.cars_data)} คัน")
        print(f"⚡ Core Web Vitals: Optimized")
        print(f"🔍 SEO: Product schema, Breadcrumbs, Local business")
        print(f"🖼️ Images: Hero optimization, Responsive gallery")


def main():
    """ฟังก์ชันหลักสำหรับรันสคริปต์"""
    generator = EnhancedCarDetailGenerator()
    generator.generate_all_car_details()


if __name__ == "__main__":
    main()