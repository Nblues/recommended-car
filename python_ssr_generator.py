#!/usr/bin/env python3
"""
Ultimate Python SSR 2025 - Server-Side Rendering
เรนเดอร์ HTML สดจาก API สำหรับ SEO และ Performance สูงสุด
"""

import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import argparse
import logging

# Import our enhanced modules
from config_manager import config_manager
from api_client import fetch_api_data, EnhancedAPIClient

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class CarData:
    """Data class สำหรับข้อมูลรถ"""
    id: str
    title: str
    handle: str
    description: str
    price: float
    status: str
    images: List[str]
    brand: str = ""
    model: str = ""
    year: str = ""
    fuel: str = ""
    transmission: str = ""
    mileage: str = ""
    created_at: str = ""
    updated_at: str = ""

class PythonSSRGenerator:
    """Ultimate Python SSR Generator 2025"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.docs_path = self.base_path / "docs"
        self.templates_path = self.base_path / "templates"
        
        # Ensure docs directory exists
        self.docs_path.mkdir(exist_ok=True)
        
        # SEO Configuration - can be moved to config_manager later
        self.seo_config = {
            'site_name': 'ครูหนึ่งรถสวย',
            'site_description': 'รถมือสองเชียงใหม่ ฟรีดาวน์ ผ่อนง่าย รถบ้านสวย ส่งฟรีทั่วไทย',
            'keywords': 'รถมือสอง, รถมือสองเชียงใหม่, ครูหนึ่งรถสวย, ฟรีดาวน์, รถบ้าน',
            'author': 'ครูหนึ่งรถสวย',
            'canonical_url': 'https://your-domain.com/',
            'og_image': 'https://your-domain.com/images/car-showcase.jpg',
            'phone': '094-064-9019',
            'address': '320 หมู่ 2 ต.สันพระเนตร อ.สันทราย จ.เชียงใหม่ 50170'
        }

    async def fetch_api_data(self, api_source: str) -> Optional[Dict[str, Any]]:
        """ดึงข้อมูลจาก API แบบ async with enhanced error handling"""
        logger.info(f"🔍 Fetching data from {api_source} API...")
        
        try:
            # Use enhanced API client
            response = await fetch_api_data(api_source, use_cache=True)
            
            if response.success:
                logger.info(f"✅ Successfully fetched from {api_source}: {len(response.data.get('products', []))} products")
                if response.from_cache:
                    logger.info("📋 Data served from cache")
                else:
                    logger.info(f"⏱️ Response time: {response.response_time:.2f}s")
                return response.data
            else:
                logger.error(f"❌ API Error for {api_source}: {response.error}")
                
                # Try to return cached data as fallback
                if not response.from_cache:
                    logger.info("🔄 Attempting to use cached data as fallback...")
                    fallback_response = await fetch_api_data(api_source, use_cache=True)
                    if fallback_response.success and fallback_response.from_cache:
                        logger.warning("⚠️ Using stale cached data due to API failure")
                        return fallback_response.data
                
                return None

        except Exception as e:
            logger.error(f"❌ Unexpected error fetching from {api_source}: {str(e)}")
            return None

    def process_car_data(self, raw_data: Dict[str, Any], api_source: str) -> List[CarData]:
        """ประมวลผลข้อมูลรถจาก API เป็น CarData objects"""
        logger.info("🔄 Processing car data...")
        
        try:
            # Extract cars based on API source
            if api_source == 'shopify':
                cars_raw = raw_data.get('products', [])
            else:
                cars_raw = raw_data.get('products', raw_data if isinstance(raw_data, list) else [])

            processed_cars = []
            for car_raw in cars_raw:
                try:
                    # Extract basic information
                    car_id = str(car_raw.get('id', car_raw.get('handle', '')))
                    title = car_raw.get('title', 'ไม่ระบุชื่อ')
                    handle = car_raw.get('handle', f"car-{car_id}")
                    
                    # Clean description - handle both desc and body_html
                    body_html = car_raw.get('body_html', car_raw.get('desc', ''))
                    description = self.clean_html_text(body_html)
                    
                    # Extract price - handle different formats
                    variants = car_raw.get('variants', [])
                    if variants:
                        price = float(variants[0].get('price', 0))
                    else:
                        # Try to extract price from description
                        price_match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', body_html)
                        price = float(price_match.group().replace(',', '')) if price_match else 450000.0
                    
                    # Extract images
                    images_raw = car_raw.get('images', [])
                    if isinstance(images_raw, list) and images_raw:
                        if isinstance(images_raw[0], str):
                            # Direct string URLs
                            images = images_raw
                        else:
                            # Object format with src property
                            images = [img.get('src', '') for img in images_raw if img.get('src')]
                    else:
                        images = []
                    
                    if not images:
                        images = ['https://via.placeholder.com/300x200?text=No+Image']
                    
                    # Extract other fields
                    status = car_raw.get('status', 'พร้อมขาย')
                    brand = car_raw.get('brand', '')
                    
                    # Try to extract car details from title or tags
                    extracted_brand, model, year = self.extract_car_details(title)
                    if not brand:
                        brand = extracted_brand
                    
                    car_data = CarData(
                        id=car_id,
                        title=title,
                        handle=handle,
                        description=description,
                        price=price,
                        status=status,
                        images=images,
                        brand=brand,
                        model=model,
                        year=year,
                        created_at=car_raw.get('created_at', ''),
                        updated_at=car_raw.get('updated_at', '')
                    )
                    
                    processed_cars.append(car_data)
                    
                except Exception as e:
                    logger.warning(f"⚠️ Error processing car {car_raw.get('id', 'unknown')}: {str(e)}")
                    continue

            # Sort by newest first
            processed_cars.sort(key=lambda x: x.created_at or x.updated_at, reverse=True)
            
            logger.info(f"✅ Successfully processed {len(processed_cars)} cars")
            return processed_cars[:6]  # Return only first 6 cars

        except Exception as e:
            logger.error(f"❌ Error processing car data: {str(e)}")
            return []

    def clean_html_text(self, html_text: str) -> str:
        """ทำความสะอาด HTML tags และจัดรูปแบบข้อความ"""
        if not html_text:
            return "รถมือสองคุณภาพดี"
        
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', html_text)
        
        # Remove extra whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        # Truncate if too long
        if len(clean_text) > 150:
            clean_text = clean_text[:147] + '...'
        
        return clean_text

    def extract_car_details(self, title: str) -> tuple:
        """สกัดรายละเอียดรถจากชื่อ"""
        title_upper = title.upper()
        
        # Common car brands
        brands = ['TOYOTA', 'HONDA', 'NISSAN', 'MAZDA', 'FORD', 'HYUNDAI', 
                 'KIA', 'MITSUBISHI', 'ISUZU', 'CHEVROLET', 'BMW', 'MERCEDES', 'AUDI']
        
        brand = ""
        for b in brands:
            if b in title_upper:
                brand = b.title()
                break
        
        # Extract year (4 digits)
        year_match = re.search(r'\b(19|20)\d{2}\b', title)
        year = year_match.group() if year_match else ""
        
        # Extract model (simplified)
        model = ""
        if brand:
            title_without_brand = title.replace(brand.upper(), '').replace(brand.lower(), '').strip()
            model_match = re.search(r'^([A-Za-z0-9\-]+)', title_without_brand)
            if model_match:
                model = model_match.group().strip()
        
        return brand, model, year

    def format_price(self, price: float) -> str:
        """จัดรูปแบบราคา"""
        return f"{price:,.0f}".replace(',', ',')

    def generate_schema_markup(self, cars: List[CarData]) -> str:
        """สร้าง Schema.org JSON-LD markup"""
        schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "LocalBusiness",
                    "@id": f"{self.seo_config['canonical_url']}#business",
                    "name": self.seo_config['site_name'],
                    "description": self.seo_config['site_description'],
                    "telephone": self.seo_config['phone'],
                    "address": {
                        "@type": "PostalAddress",
                        "streetAddress": "320 หมู่ 2 ต.สันพระเนตร",
                        "addressLocality": "เชียงใหม่",
                        "addressRegion": "เชียงใหม่",
                        "postalCode": "50170",
                        "addressCountry": "TH"
                    },
                    "geo": {
                        "@type": "GeoCoordinates",
                        "latitude": 18.7883,
                        "longitude": 98.9853
                    },
                    "openingHours": "Mo-Su 08:00-18:00",
                    "priceRange": "฿฿"
                },
                {
                    "@type": "WebSite",
                    "@id": f"{self.seo_config['canonical_url']}#website",
                    "url": self.seo_config['canonical_url'],
                    "name": f"{self.seo_config['site_name']} - {self.seo_config['site_description']}",
                    "publisher": {"@id": f"{self.seo_config['canonical_url']}#business"}
                },
                {
                    "@type": "ItemList",
                    "itemListElement": []
                }
            ]
        }
        
        # Add car products to schema
        for i, car in enumerate(cars):
            car_schema = {
                "@type": "ListItem",
                "position": i + 1,
                "item": {
                    "@type": "Product",
                    "@id": f"{self.seo_config['canonical_url']}car-detail/{car.handle}.html",
                    "name": car.title,
                    "description": car.description,
                    "image": car.images[0] if car.images else "",
                    "offers": {
                        "@type": "Offer",
                        "price": car.price,
                        "priceCurrency": "THB",
                        "availability": "https://schema.org/InStock" if car.status == "พร้อมขาย" else "https://schema.org/OutOfStock"
                    }
                }
            }
            schema["@graph"][2]["itemListElement"].append(car_schema)
        
        return json.dumps(schema, ensure_ascii=False, indent=2)

    def render_car_card(self, car: CarData, index: int = 0) -> str:
        """เรนเดอร์ car card HTML"""
        formatted_price = self.format_price(car.price)
        detail_link = f"car-detail/{car.handle}.html"
        image_url = car.images[0] if car.images else 'https://via.placeholder.com/300x200'
        animation_delay = (index * 0.1) + 0.1
        
        return f'''
        <div class="car-card" style="animation-delay: {animation_delay}s;">
            <img src="{image_url}" 
                 alt="{car.title}" 
                 loading="{'eager' if index < 2 else 'lazy'}"
                 onerror="this.src='https://via.placeholder.com/300x200?text=Loading...'">
            <div class="car-info">
                <div class="car-title">{car.title}</div>
                <div class="car-price">฿{formatted_price}</div>
                <div class="car-status">{car.status}</div>
                <div class="car-desc">{car.description}</div>
                <a href="{detail_link}" class="btn-detail">ดูรายละเอียด</a>
            </div>
        </div>'''

    def generate_html_page(self, cars: List[CarData], api_source: str) -> str:
        """สร้างหน้า HTML สมบูรณ์"""
        logger.info("🎨 Generating HTML page...")
        
        # Generate components
        car_cards_html = '\n'.join([self.render_car_card(car, i) for i, car in enumerate(cars)])
        schema_markup = self.generate_schema_markup(cars)
        last_update = datetime.now().strftime("%d/%m/%Y %H:%M น.")
        
        # Create page title with car count
        page_title = f"รถมือสองเชียงใหม่ เข้าใหม่ {len(cars)} คันล่าสุด ฟรีดาวน์ | {self.seo_config['site_name']}"
        
        # Generate meta description with current cars
        brands_list = list(set([car.brand for car in cars if car.brand]))
        brands_text = ', '.join(brands_list[:3]) if brands_list else "Toyota, Honda, Nissan"
        meta_description = f"รถบ้านเข้าใหม่ {len(cars)} คันล่าสุด {brands_text} รถมือสองเชียงใหม่ ฟรีดาวน์ ผ่อนถูก รถบ้านสวย ตรวจสอบได้จริงทุกคัน อัพเดท {last_update}"
        
        html_template = f'''<!DOCTYPE html>
<html lang="th" itemscope itemtype="https://schema.org/WebPage">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Ultimate SEO 2025 -->
    <title>{page_title}</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{self.seo_config['keywords']}, {brands_text}">
    <meta name="author" content="{self.seo_config['author']}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{self.seo_config['canonical_url']}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{page_title}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:image" content="{self.seo_config['og_image']}">
    <meta property="og:url" content="{self.seo_config['canonical_url']}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{self.seo_config['site_name']}">
    <meta property="og:locale" content="th_TH">
    
    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page_title}">
    <meta name="twitter:description" content="{meta_description}">
    <meta name="twitter:image" content="{self.seo_config['og_image']}">
    
    <!-- Performance Critical Resources -->
    <link rel="preload" href="style.css" as="style">
    <link rel="stylesheet" href="style.css">
    <link rel="preload" href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;600;700;800&display=swap" as="style">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;600;700;800&display=swap">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
    
    <!-- PWA -->
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#f47b20">
    
    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
    {schema_markup}
    </script>
    
    <!-- Performance Monitoring -->
    <script>
    if ('PerformanceObserver' in window) {{
        const observer = new PerformanceObserver((list) => {{
            list.getEntries().forEach((entry) => {{
                if (entry.entryType === 'largest-contentful-paint') {{
                    console.log('LCP:', entry.startTime);
                }}
            }});
        }});
        observer.observe({{entryTypes: ['largest-contentful-paint']}});
    }}
    </script>
</head>

<body>
    <!-- Main Content -->
    <div class="container">
        <header>
            <h1>รถมือสองเชียงใหม่ เข้าใหม่ {len(cars)} คันล่าสุด</h1>
            <p class="subtitle">ฟรีดาวน์ ผ่อนง่าย รถบ้านสวย ส่งฟรีทั่วไทย</p>
        </header>
        
        <!-- Cars Grid -->
        <main>
            <div class="car-grid">
                {car_cards_html}
            </div>
        </main>
        
        <!-- Call to Action -->
        <section class="cta-section">
            <a href="mini-cars-static.html" class="btn-main">ดูรถทั้งหมด ({len(cars)}+ คัน)</a>
        </section>
        
        <!-- Footer Info -->
        <footer class="update-info">
            <div class="server-info">
                <strong>🔥 Server-Side Rendered</strong> - อัพเดทสดจาก API
            </div>
            <div class="update-details">
                <small>
                    📅 อัพเดทล่าสุด: {last_update} | 
                    🌐 API Source: {api_source.upper()} | 
                    📊 จำนวนรถ: {len(cars)} คัน |
                    ⚡ Generated in Python SSR
                </small>
            </div>
            <div class="contact-info">
                <p>📞 โทร: {self.seo_config['phone']} | 📍 {self.seo_config['address']}</p>
            </div>
        </footer>
    </div>

    <!-- Additional Styles for SSR -->
    <style>
    .subtitle {{
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }}
    
    .cta-section {{
        text-align: center;
        margin: 3rem 0;
    }}
    
    .server-info {{
        text-align: center;
        background: linear-gradient(135deg, #27ae60, #2ecc71);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
        font-weight: 600;
    }}
    
    .update-details {{
        text-align: center;
        background: #f8f9fa;
        padding: 10px;
        border-radius: 6px;
        margin: 10px 0;
        color: #666;
    }}
    
    .contact-info {{
        text-align: center;
        margin: 15px 0;
        padding: 15px;
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        border-radius: 8px;
    }}
    
    .contact-info p {{
        margin: 0;
        font-weight: 600;
    }}
    
    /* SSR Optimization */
    .car-card {{
        contain: layout style paint;
    }}
    
    img {{
        contain: layout style;
    }}
    </style>

    <!-- Service Worker Registration -->
    <script>
    if ('serviceWorker' in navigator) {{
        navigator.serviceWorker.register('sw.js')
            .then(reg => console.log('SW registered'))
            .catch(err => console.log('SW registration failed'));
    }}
    </script>
</body>
</html>'''

        return html_template

    async def render_and_save(self, api_source: str = 'local', output_file: str = 'index-ssr.html') -> bool:
        """เรนเดอร์และบันทึกไฟล์ HTML"""
        logger.info(f"🚀 Starting Python SSR rendering from '{api_source}' API...")
        
        start_time = datetime.now()
        
        # Fetch data from API
        raw_data = await self.fetch_api_data(api_source)
        if not raw_data:
            logger.error(f"❌ Failed to fetch data from {api_source}")
            return False
        
        # Process car data
        cars = self.process_car_data(raw_data, api_source)
        if not cars:
            logger.error("❌ No car data found")
            return False
        
        # Generate HTML
        html_content = self.generate_html_page(cars, api_source)
        
        # Save to file
        output_path = self.docs_path / output_file
        try:
            # Ensure docs directory exists
            self.docs_path.mkdir(exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            end_time = datetime.now()
            render_time = (end_time - start_time).total_seconds()
            file_size = os.path.getsize(output_path)
            
            logger.info(f"✅ SSR HTML generated successfully!")
            logger.info(f"📁 File: {output_path}")
            logger.info(f"📊 Size: {file_size:,} bytes")
            logger.info(f"⏱️  Render time: {render_time:.2f} seconds")
            logger.info(f"🚗 Cars rendered: {len(cars)}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving HTML file: {str(e)}")
            return False

    async def auto_update_scheduler(self, api_source: str = 'local', interval_minutes: int = 30):
        """อัพเดทอัตโนมัติ"""
        logger.info(f"⏰ Starting auto-update scheduler: every {interval_minutes} minutes")
        
        while True:
            try:
                timestamp = datetime.now().strftime("%Y%m%d-%H%M")
                output_file = f'index-ssr-{timestamp}.html'
                
                success = await self.render_and_save(api_source, output_file)
                if success:
                    # Also update the main index file
                    await self.render_and_save(api_source, 'index.html')
                    logger.info(f"🔄 Auto-update completed: {output_file}")
                
                logger.info(f"⏳ Waiting {interval_minutes} minutes for next update...")
                await asyncio.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                logger.info("🛑 Auto-update scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Error in auto-update: {str(e)}")
                await asyncio.sleep(60)  # Wait 1 minute before retry

async def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description='Ultimate Python SSR 2025 - Server-Side Rendering')
    parser.add_argument('--api', default='local', choices=['local', 'shopify', 'custom'], 
                       help='API source to fetch data from')
    parser.add_argument('--output', default='index-ssr.html', 
                       help='Output HTML filename')
    parser.add_argument('--auto', action='store_true', 
                       help='Enable auto-update mode')
    parser.add_argument('--interval', type=int, default=30, 
                       help='Auto-update interval in minutes')
    
    args = parser.parse_args()
    
    # Create SSR generator
    ssr = PythonSSRGenerator()
    
    if args.auto:
        await ssr.auto_update_scheduler(args.api, args.interval)
    else:
        success = await ssr.render_and_save(args.api, args.output)
        if success:
            print("\n🎉 Python SSR rendering completed successfully!")
            print(f"🌐 Open docs/{args.output} in your browser to view the result")
        else:
            print("\n💥 Python SSR rendering failed!")
            exit(1)

if __name__ == "__main__":
    asyncio.run(main())
