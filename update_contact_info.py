#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
อัปเดตข้อมูลการติดต่อและโซเชียลมีเดียทั่วทั้งเว็บไซต์
Update Contact Information and Social Media Links

Created by: Website Contact Update System
"""

import re
from pathlib import Path
import json

class ContactInfoUpdater:
    def __init__(self):
        self.docs_path = Path("docs")
        self.contact_info = {
            "business_name": "ครูหนึ่งรถสวย",
            "phone": "094-064-9019",
            "phone_raw": "0940649019",
            "address": {
                "full": "เลขที่ 320 หมู่ 2 ต.สันพระเนตร อ.สันทราย จ.เชียงใหม่ 50210",
                "street": "320 หมู่ 2",
                "subdistrict": "สันพระเนตร",
                "district": "สันทราย", 
                "province": "เชียงใหม่",
                "postal_code": "50210"
            },
            "coordinates": "https://maps.app.goo.gl/zFa8gkWMNqLPaAGt8",
            "social_media": {
                "line": "https://lin.ee/ng5yM32",
                "facebook_page": "https://www.facebook.com/KN2car",
                "facebook_personal": "https://www.facebook.com/nuengblues", 
                "tiktok": "https://www.tiktok.com/@krunueng_usedcar",
                "youtube": "https://youtube.com/@chiangraiusedcar",
                "lemon8": "https://s.lemon8-app.com/al/GgTNvSZhvT"
            },
            "followers": {
                "facebook_page": "1,000,000+",
                "facebook_personal": "100,000+", 
                "tiktok": "150,000+"
            }
        }
    
    def create_local_business_schema(self):
        """สร้าง LocalBusiness Schema ใหม่"""
        schema = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": self.contact_info["business_name"],
            "image": "https://cdn.shopify.com/s/files/1/0718/1441/4580/files/logo.jpg",
            "telephone": self.contact_info["phone_raw"],
            "url": "https://nblues.github.io/recommended-car/",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": f"{self.contact_info['address']['street']} ต.{self.contact_info['address']['subdistrict']}",
                "addressLocality": self.contact_info['address']['district'],
                "addressRegion": self.contact_info['address']['province'],
                "postalCode": self.contact_info['address']['postal_code'],
                "addressCountry": "TH"
            },
            "geo": {
                "@type": "GeoCoordinates",
                "url": self.contact_info["coordinates"]
            },
            "sameAs": [
                self.contact_info["social_media"]["facebook_page"],
                self.contact_info["social_media"]["facebook_personal"],
                self.contact_info["social_media"]["tiktok"],
                self.contact_info["social_media"]["youtube"],
                self.contact_info["social_media"]["lemon8"]
            ],
            "openingHours": ["Mo-Su 08:00-20:00"],
            "priceRange": "฿฿",
            "servesCuisine": [],
            "description": "รถมือสองคุณภาพเชียงใหม่ ฟรีดาวน์ ผ่อนง่าย รับประกัน ส่งฟรีทั่วไทย",
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "รถมือสองคุณภาพ",
                "itemListElement": [
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Product",
                            "name": "รถยนต์มือสอง",
                            "category": "Automotive"
                        }
                    }
                ]
            }
        }
        return schema
    
    def update_index_page(self):
        """อัปเดตหน้าแรก"""
        print("📄 อัปเดตหน้าแรก...")
        
        index_path = self.docs_path / "index.html"
        if not index_path.exists():
            print("   ❌ ไม่พบไฟล์ index.html")
            return
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # อัปเดต phone number
        content = re.sub(
            r'064-140-5566',
            self.contact_info["phone"],
            content
        )
        
        # อัปเดต LocalBusiness schema
        schema = self.create_local_business_schema()
        schema_str = json.dumps(schema, ensure_ascii=False, indent=2)
        
        # หา LocalBusiness schema เก่าและแทนที่
        pattern = r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"LocalBusiness"[^<]*</script>'
        replacement = f'<script type="application/ld+json">\n{schema_str}\n</script>'
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        else:
            # เพิ่ม schema ใหม่ถ้าไม่มี
            head_end = content.find('</head>')
            if head_end != -1:
                content = content[:head_end] + f'\n{replacement}\n' + content[head_end:]
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ อัปเดตหน้าแรกสำเร็จ")
    
    def create_contact_page(self):
        """สร้างหน้าติดต่อใหม่"""
        print("📞 สร้างหน้าติดต่อ...")
        
        contact_html = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ติดต่อเรา - ครูหนึ่งรถสวย | รถมือสองเชียงใหม่</title>
    <meta name="description" content="ติดต่อ ครูหนึ่งรถสวย รถมือสองคุณภาพเชียงใหม่ โทร {self.contact_info['phone']} ฟรีดาวน์ ส่งฟรีทั่วไทย">
    <meta name="keywords" content="ติดต่อ, ครูหนึ่งรถสวย, รถมือสองเชียงใหม่, เบอร์โทร, ที่อยู่, Line, Facebook">
    <link rel="canonical" href="https://nblues.github.io/recommended-car/contact.html">
    
    <!-- Open Graph -->
    <meta property="og:title" content="ติดต่อเรา - ครูหนึ่งรถสวย">
    <meta property="og:description" content="ติดต่อ ครูหนึ่งรถสวย รถมือสองคุณภาพเชียงใหม่ โทร {self.contact_info['phone']}">
    <meta property="og:url" content="https://nblues.github.io/recommended-car/contact.html">
    <meta property="og:type" content="website">
    
    <!-- Performance -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preload" href="/style.css" as="style">
    
    <style>
        body {{
            font-family: 'Prompt', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #f47b20 0%, #e66a16 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .contact-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .contact-card {{
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .contact-card h3 {{
            color: #f47b20;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid #f47b20;
            padding-bottom: 10px;
        }}
        
        .contact-item {{
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }}
        
        .contact-item strong {{
            min-width: 80px;
            color: #666;
        }}
        
        .social-links {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .social-link {{
            display: block;
            padding: 15px 20px;
            border-radius: 10px;
            text-decoration: none;
            color: white;
            font-weight: 500;
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .social-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}
        
        .line {{ background: #06C755; }}
        .facebook {{ background: #1877F2; }}
        .tiktok {{ background: #000000; }}
        .youtube {{ background: #FF0000; }}
        .lemon8 {{ background: #FFD700; color: #333; }}
        
        .map-container {{
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .phone-highlight {{
            font-size: 2em;
            color: #f47b20;
            font-weight: bold;
            text-decoration: none;
            display: block;
            margin: 10px 0;
        }}
        
        .phone-highlight:hover {{
            color: #e66a16;
        }}
    </style>
    
    <script type="application/ld+json">
    {json.dumps(self.create_local_business_schema(), ensure_ascii=False, indent=2)}
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📞 ติดต่อเรา</h1>
            <p>ครูหนึ่งรถสวย - รถมือสองคุณภาพเชียงใหม่</p>
            <a href="tel:{self.contact_info['phone_raw']}" class="phone-highlight">{self.contact_info['phone']}</a>
        </div>
        
        <div class="contact-grid">
            <div class="contact-card">
                <h3>🏢 ข้อมูลร้าน</h3>
                <div class="contact-item">
                    <strong>📍 ที่อยู่:</strong>
                    <span>{self.contact_info['address']['full']}</span>
                </div>
                <div class="contact-item">
                    <strong>📞 โทรศัพท์:</strong>
                    <a href="tel:{self.contact_info['phone_raw']}" style="color: #f47b20; text-decoration: none;">
                        {self.contact_info['phone']}
                    </a>
                </div>
                <div class="contact-item">
                    <strong>🕐 เวลาทำการ:</strong>
                    <span>วันจันทร์ - อาทิตย์ 08:00 - 20:00 น.</span>
                </div>
                <div class="contact-item">
                    <strong>🗺️ พิกัด:</strong>
                    <a href="{self.contact_info['coordinates']}" target="_blank" rel="noopener" style="color: #f47b20;">
                        ดูแผนที่
                    </a>
                </div>
            </div>
            
            <div class="contact-card">
                <h3>📱 โซเชียลมีเดีย</h3>
                <div class="social-links">
                    <a href="{self.contact_info['social_media']['line']}" target="_blank" rel="noopener" class="social-link line">
                        💬 LINE Official Account
                    </a>
                    <a href="{self.contact_info['social_media']['facebook_page']}" target="_blank" rel="noopener" class="social-link facebook">
                        📘 Facebook Page (1M+ ผู้ติดตาม)
                    </a>
                    <a href="{self.contact_info['social_media']['facebook_personal']}" target="_blank" rel="noopener" class="social-link facebook">
                        👤 Facebook ส่วนตัว (100K+)
                    </a>
                    <a href="{self.contact_info['social_media']['tiktok']}" target="_blank" rel="noopener" class="social-link tiktok">
                        🎵 TikTok (150K+ ผู้ติดตาม)
                    </a>
                    <a href="{self.contact_info['social_media']['youtube']}" target="_blank" rel="noopener" class="social-link youtube">
                        📺 YouTube Channel
                    </a>
                    <a href="{self.contact_info['social_media']['lemon8']}" target="_blank" rel="noopener" class="social-link lemon8">
                        🍋 Lemon8
                    </a>
                </div>
            </div>
        </div>
        
        <div class="map-container">
            <h3 style="color: #f47b20; margin-bottom: 20px;">🗺️ ที่ตั้งร้าน</h3>
            <p>คลิกที่ลิงก์ด้านล่างเพื่อดูแผนที่และเส้นทาง</p>
            <a href="{self.contact_info['coordinates']}" target="_blank" rel="noopener" 
               style="display: inline-block; margin-top: 15px; padding: 15px 30px; 
                      background: #f47b20; color: white; text-decoration: none; 
                      border-radius: 10px; font-weight: bold;">
                🗺️ เปิดแผนที่ Google Maps
            </a>
        </div>
        
        <div style="text-align: center; color: rgba(255,255,255,0.8); margin-top: 30px;">
            📅 อัปเดตล่าสุด: 13/07/2025 | ✨ พร้อมให้บริการ
        </div>
    </div>
</body>
</html>"""
        
        with open(self.docs_path / "contact.html", "w", encoding="utf-8") as f:
            f.write(contact_html)
        
        print("   ✅ สร้างหน้าติดต่อสำเร็จ")
    
    def update_sitemap(self):
        """อัปเดต Sitemap เพิ่มหน้าติดต่อ"""
        print("🗺️ อัปเดต Sitemap...")
        
        sitemap_path = self.docs_path / "sitemap.xml"
        if not sitemap_path.exists():
            print("   ❌ ไม่พบไฟล์ sitemap.xml")
            return
        
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # เพิ่ม contact.html ใน sitemap
        contact_entry = '''  <url>
    <loc>https://nblues.github.io/recommended-car/contact.html</loc>
    <lastmod>2025-07-13T10:08:38+00:00</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
    <html:link rel="alternate" hreflang="th-TH" href="https://nblues.github.io/recommended-car/contact.html" />
  </url>'''
        
        # แทรกก่อน </urlset>
        if 'contact.html' not in content:
            content = content.replace('</urlset>', contact_entry + '\n</urlset>')
        
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ อัปเดต Sitemap สำเร็จ")
    
    def update_all_files(self):
        """อัปเดตข้อมูลการติดต่อในไฟล์ทั้งหมด"""
        print("🔄 อัปเดตข้อมูลการติดต่อทั่วทั้งเว็บไซต์...")
        print("=" * 60)
        
        # อัปเดตไฟล์ต่างๆ
        self.update_index_page()
        self.create_contact_page()
        self.update_sitemap()
        
        # สร้างไฟล์ข้อมูลการติดต่อ JSON
        contact_data = {
            "business_info": self.contact_info,
            "last_updated": "2025-07-13T22:30:00+07:00"
        }
        
        with open(self.docs_path / "contact-info.json", "w", encoding="utf-8") as f:
            json.dump(contact_data, f, ensure_ascii=False, indent=2)
        
        print("✅ สร้างไฟล์ contact-info.json สำเร็จ")
        
        print("=" * 60)
        print("🎉 อัปเดตข้อมูลการติดต่อเสร็จสมบูรณ์!")
        print("📞 เบอร์โทรใหม่:", self.contact_info['phone'])
        print("📍 ที่อยู่:", self.contact_info['address']['full'])
        print("📱 โซเชียลมีเดีย: 6 แพลตฟอร์ม")
        print("🎯 หน้าติดต่อ: contact.html")

if __name__ == "__main__":
    updater = ContactInfoUpdater()
    updater.update_all_files()
