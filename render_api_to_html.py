#!/usr/bin/env python3
"""
Ultimate API-to-HTML Renderer 2025
เรนเดอร์ HTML สดจาก API สำหรับ SEO และ Performance
"""

import json
import datetime
import os
from pathlib import Path
import asyncio
from typing import Dict, List, Optional

# Import enhanced modules
from config_manager import config_manager
from api_client import fetch_api_data
from error_handler import handle_async_exception, log_error

class APItoHTMLRenderer:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.template_path = self.base_path / "templates"
        self.output_path = self.base_path / "docs"
        
        # Ensure output directory exists
        self.output_path.mkdir(exist_ok=True)
        
        # Load templates with error handling
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """โหลด HTML templates with enhanced error handling"""
        templates = {}
        template_files = {
            'main': 'index-template.html',
            'car_card': 'car-card-template.html', 
            'car_detail': 'car-detail-template.html'
        }
        
        for template_name, filename in template_files.items():
            try:
                templates[template_name] = self.load_template(filename)
            except Exception as e:
                log_error(e, {'template': filename}, "WARNING")
                templates[template_name] = self.get_default_template(filename)
        
        return templates

    def load_template(self, filename: str) -> str:
        """โหลด HTML template with enhanced error handling"""
        try:
            template_file = self.template_path / filename
            if template_file.exists():
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not content.strip():
                        raise ValueError(f"Template {filename} is empty")
                    return content
            else:
                print(f"⚠️ Template file {filename} not found, using default")
                return self.get_default_template(filename)
        except Exception as e:
            log_error(e, {'template_file': filename}, "WARNING")
            print(f"❌ Error loading template {filename}: {e}")
            return self.get_default_template(filename)

    def get_default_template(self, template_type: str) -> str:
        """สร้าง default template หาก template file ไม่มี"""
        
        if template_type == 'index-template.html':
            return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="stylesheet" href="style.css">
    
    <!-- SEO Meta Tags -->
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="ครูหนึ่งรถสวย">
    <link rel="canonical" href="{canonical_url}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{og_description}">
    <meta property="og:image" content="{og_image}">
    <meta property="og:url" content="{og_url}">
    
    <!-- Schema.org -->
    <script type="application/ld+json">{schema_markup}</script>
</head>
<body>
    <div class="container">
        <h1>{main_heading}</h1>
        <div class="car-grid">
            {car_cards}
        </div>
        <a href="mini-cars-static.html" class="btn-main">ดูรถทั้งหมด</a>
        
        <div class="update-info">
            <small>อัพเดทล่าสุด: {last_update}</small>
        </div>
    </div>
</body>
</html>'''

        elif template_type == 'car-card-template.html':
            return '''<div class="car-card">
    <img src="{image_url}" alt="{car_title}" loading="lazy">
    <div class="car-info">
        <div class="car-title">{car_title}</div>
        <div class="car-price">฿{formatted_price}</div>
        <div class="car-status">{car_status}</div>
        <div class="car-desc">{car_description}</div>
        <a href="{detail_link}" class="btn-detail">ดูรายละเอียด</a>
    </div>
</div>'''

        elif template_type == 'car-detail-template.html':
            return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{car_title} | ครูหนึ่งรถสวย</title>
    <meta name="description" content="{car_description}">
    <link rel="stylesheet" href="../ultimate-car-detail-style.css">
</head>
<body>
    <div class="container">
        <h1>{car_title}</h1>
        <div class="car-detail-content">
            {car_detail_html}
        </div>
    </div>
</body>
</html>'''

    @handle_async_exception("fetch_api_data")
    async def fetch_api_data(self, api_name: str) -> Optional[Dict]:
        """ดึงข้อมูลจาก API แบบ async with enhanced error handling"""
        try:
            print(f"🔍 Fetching data from {api_name} API...")
            
            # Use enhanced API client
            response = await fetch_api_data(api_name, use_cache=True)
            
            if response.success:
                print(f"✅ Successfully fetched from {api_name}")
                if response.from_cache:
                    print("📋 Data served from cache")
                else:
                    print(f"⏱️ Response time: {response.response_time:.2f}s")
                return response.data
            else:
                print(f"❌ API Error for {api_name}: {response.error}")
                log_error(Exception(response.error), {
                    'api_name': api_name,
                    'status_code': response.status_code
                }, "ERROR")
                return None

        except Exception as e:
            log_error(e, {'api_name': api_name}, "ERROR")
            print(f"❌ Unexpected error fetching from {api_name}: {e}")
            return None

    def process_car_data(self, raw_data: Dict, api_source: str) -> List[Dict]:
        """ประมวลผลข้อมูลรถจาก API with enhanced error handling"""
        try:
            if api_source == 'shopify':
                cars = raw_data.get('products', [])
            else:
                # Handle both array and object formats
                if isinstance(raw_data, list):
                    cars = raw_data
                else:
                    cars = raw_data.get('products', raw_data)

            processed_cars = []
            for car in cars[:6]:  # เอาแค่ 6 คันแรก
                try:
                    # Handle different price formats
                    price = 0
                    variants = car.get('variants', [])
                    if variants:
                        if isinstance(variants[0], dict):
                            price = float(variants[0].get('price', 0))
                        else:
                            price = float(variants[0])
                    
                    processed_car = {
                        'id': car.get('id', ''),
                        'title': car.get('title', 'ไม่ระบุชื่อ'),
                        'handle': car.get('handle', f"car-{car.get('id', 'unknown')}"),
                        'description': self.clean_html(car.get('body_html', car.get('desc', ''))),
                        'price': price,
                        'status': car.get('status', 'พร้อมขาย'),
                        'images': car.get('images', []),
                        'created_at': car.get('created_at', ''),
                        'updated_at': car.get('updated_at', '')
                    }
                    processed_cars.append(processed_car)
                    
                except Exception as e:
                    log_error(e, {'car_data': car}, "WARNING")
                    print(f"⚠️ Error processing car: {e}")
                    continue

            # เรียงตามวันที่ใหม่ที่สุด
            processed_cars.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return processed_cars

        except Exception as e:
            log_error(e, {'api_source': api_source}, "ERROR")
            print(f"❌ Error processing car data: {e}")
            return []

    def clean_html(self, html_text: str) -> str:
        """ทำความสะอาด HTML tags"""
        import re
        clean_text = re.sub('<[^<]+?>', '', html_text)
        return clean_text[:120] + '...' if len(clean_text) > 120 else clean_text

    def format_price(self, price: float) -> str:
        """จัดรูปแบบราคา"""
        return f"{price:,.0f}".replace(',', ',')

    def generate_schema_markup(self, cars: List[Dict]) -> str:
        """สร้าง Schema.org markup"""
        schema = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "itemListElement": []
        }
        
        for i, car in enumerate(cars):
            item = {
                "@type": "ListItem",
                "position": i + 1,
                "item": {
                    "@type": "Product",
                    "name": car['title'],
                    "description": car['description'],
                    "offers": {
                        "@type": "Offer",
                        "price": car['price'],
                        "priceCurrency": "THB"
                    }
                }
            }
            schema["itemListElement"].append(item)
        
        return json.dumps(schema, ensure_ascii=False, indent=2)

    def render_car_cards(self, cars: List[Dict]) -> str:
        """เรนเดอร์ car cards HTML with enhanced error handling"""
        cards_html = ""
        
        for car in cars:
            try:
                # Handle different image formats
                images = car.get('images', [])
                if images:
                    if isinstance(images[0], str):
                        # Direct string URLs
                        image_url = images[0]
                    else:
                        # Object format with src property
                        image_url = images[0].get('src', 'https://via.placeholder.com/300x200')
                else:
                    image_url = 'https://via.placeholder.com/300x200'
                
                detail_link = f"car-detail/{car.get('handle', 'unknown')}.html"
                
                card_html = self.templates['car_card'].format(
                    image_url=image_url,
                    car_title=car.get('title', 'ไม่ระบุชื่อ'),
                    formatted_price=self.format_price(car.get('price', 0)),
                    car_status=car.get('status', 'พร้อมขาย'),
                    car_description=car.get('description', ''),
                    detail_link=detail_link
                )
                cards_html += card_html
                
            except Exception as e:
                log_error(e, {'car_id': car.get('id', 'unknown')}, "WARNING")
                print(f"⚠️ Error rendering car card for {car.get('title', 'unknown')}: {e}")
                continue
        
        return cards_html

    def render_main_page(self, cars: List[Dict]) -> str:
        """เรนเดอร์หน้าหลัก"""
        car_cards_html = self.render_car_cards(cars)
        schema_markup = self.generate_schema_markup(cars)
        now = datetime.datetime.now()
        
        main_html = self.templates['main'].format(
            title="รถมือสองเชียงใหม่ เข้าใหม่ 6 คันล่าสุด ฟรีดาวน์ | ครูหนึ่งรถสวย",
            description="รถบ้านเข้าใหม่ 6 คันล่าสุด รถมือสองเชียงใหม่ ฟรีดาวน์ ผ่อนถูก รถบ้านสวย ตรวจสอบได้จริงทุกคัน",
            keywords="รถมือสอง, รถมือสองเชียงใหม่, ครูหนึ่งรถสวย, ฟรีดาวน์",
            canonical_url="https://your-domain.com/",
            og_title="รถมือสองเชียงใหม่ เข้าใหม่ 6 คันล่าสุด ฟรีดาวน์",
            og_description="รถบ้านเข้าใหม่ 6 คันล่าสุด รถมือสองเชียงใหม่ ฟรีดาวน์ ผ่อนถูก",
            og_image="https://your-domain.com/images/car-showcase.jpg",
            og_url="https://your-domain.com/",
            schema_markup=schema_markup,
            main_heading="รถมือสองเชียงใหม่ เข้าใหม่ 6 คันล่าสุด",
            car_cards=car_cards_html,
            last_update=now.strftime("%d/%m/%Y %H:%M น.")
        )
        
        return main_html

    async def render_and_save(self, api_source: str = 'local', output_filename: str = 'index.html'):
        """เรนเดอร์และบันทึกไฟล์ HTML"""
        print(f"🚀 Starting API-to-HTML rendering from '{api_source}' API...")
        
        # Fetch data from API
        raw_data = await self.fetch_api_data(api_source)
        if not raw_data:
            print(f"❌ Failed to fetch data from {api_source} API")
            return False
        
        # Process car data
        cars = self.process_car_data(raw_data, api_source)
        if not cars:
            print("❌ No car data to process")
            return False
        
        print(f"✅ Successfully processed {len(cars)} cars")
        
        # Render HTML
        html_content = self.render_main_page(cars)
        
        # Save to file
        output_file = self.output_path / output_filename
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ HTML rendered and saved to: {output_file}")
            print(f"📊 File size: {os.path.getsize(output_file):,} bytes")
            return True
            
        except Exception as e:
            print(f"❌ Error saving HTML file: {e}")
            return False

    async def auto_update_scheduler(self, api_source: str = 'local', interval_minutes: int = 30):
        """อัพเดท HTML อัตโนมัติตามช่วงเวลาที่กำหนด"""
        print(f"⏰ Starting auto-update scheduler: every {interval_minutes} minutes")
        
        while True:
            try:
                await self.render_and_save(api_source, f'index-auto-{datetime.datetime.now().strftime("%Y%m%d-%H%M")}.html')
                print(f"⏳ Waiting {interval_minutes} minutes for next update...")
                await asyncio.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                print("🛑 Auto-update scheduler stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in auto-update: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry

# CLI Functions
async def main():
    """Main function สำหรับรัน command line"""
    import argparse
    
    parser = argparse.ArgumentParser(description='API-to-HTML Renderer 2025')
    parser.add_argument('--api', default='local', choices=['local', 'shopify', 'custom'], 
                       help='API source to fetch data from')
    parser.add_argument('--output', default='index-api.html', 
                       help='Output HTML filename')
    parser.add_argument('--auto', action='store_true', 
                       help='Enable auto-update mode')
    parser.add_argument('--interval', type=int, default=30, 
                       help='Auto-update interval in minutes')
    
    args = parser.parse_args()
    
    renderer = APItoHTMLRenderer()
    
    if args.auto:
        await renderer.auto_update_scheduler(args.api, args.interval)
    else:
        success = await renderer.render_and_save(args.api, args.output)
        if success:
            print("🎉 HTML rendering completed successfully!")
        else:
            print("💥 HTML rendering failed!")

if __name__ == "__main__":
    # รัน async main function
    asyncio.run(main())

# Usage Examples:
# python render_api_to_html.py --api local --output index.html
# python render_api_to_html.py --api shopify --auto --interval 15
# python render_api_to_html.py --api custom --output live-cars.html
