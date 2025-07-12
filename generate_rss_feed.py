#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📡 RSS Feed Generator - สร้าง RSS Feed สำหรับ Google News และ SEO

Features:
- RSS 2.0 compliant feed
- Google News optimization
- Car listings as news items
- SEO optimized descriptions
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
import html


class RSSFeedGenerator:
    def __init__(self):
        self.cars_data = self.load_cars_data()
        self.base_url = "https://nblues.github.io/recommended-car"
        self.site_info = {
            "title": "ครูหนึ่งรถสวย - รถมือสองเชียงใหม่",
            "description": "รถมือสองคุณภาพเชียงใหม่ รถเข้าใหม่ทุกวัน ฟรีดาวน์ ส่งฟรีทั่วไทย",
            "language": "th-TH",
            "webmaster": "webmaster@kn-goodcar.com",
            "category": "Used Cars"
        }

    def load_cars_data(self):
        """โหลดข้อมูลรถจาก cars.json"""
        try:
            with open("cars.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ ไม่พบไฟล์ cars.json")
            return []

    def create_rss_feed(self):
        """สร้าง RSS Feed"""
        # สร้าง RSS content as string to avoid namespace issues
        now = datetime.now(timezone.utc)
        rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{self.site_info["title"]}</title>
    <link>{self.base_url}</link>
    <description>{self.site_info["description"]}</description>
    <language>{self.site_info["language"]}</language>
    <webMaster>{self.site_info["webmaster"]}</webMaster>
    <category>{self.site_info["category"]}</category>
    <generator>KN-GoodCar Advanced RSS Generator v2.0</generator>
    <docs>https://www.rssboard.org/rss-specification</docs>
    <ttl>60</ttl>
    <lastBuildDate>{now.strftime("%a, %d %b %Y %H:%M:%S %z")}</lastBuildDate>
    <pubDate>{now.strftime("%a, %d %b %Y %H:%M:%S %z")}</pubDate>
    <atom:link href="{self.base_url}/feed.xml" rel="self" type="application/rss+xml"/>
"""
        
        # เพิ่ม items
        for i, car in enumerate(self.cars_data[:10]):
            pub_date = datetime.now(timezone.utc)
            pub_date = pub_date.replace(hour=max(0, pub_date.hour - i))
            
            title = f"รถใหม่เข้า: {car['title']}"
            car_link = f"{self.base_url}/car-detail/{car['handle']}.html"
            description = self.create_car_description(car)
            
            rss_content += f"""
    <item>
      <title>{html.escape(title)}</title>
      <link>{car_link}</link>
      <guid>{car_link}</guid>
      <description>{html.escape(description)}</description>
      <category>รถยนต์{car['title'].split()[0] if car['title'].split() else ''}</category>
      <dc:creator>ครูหนึ่งรถสวย</dc:creator>
      <pubDate>{pub_date.strftime("%a, %d %b %Y %H:%M:%S %z")}</pubDate>"""
      
            if car["images"]:
                rss_content += f"""
      <enclosure url="{car['images'][0]}" type="image/jpeg" length="0"/>"""
                
            rss_content += """
    </item>"""
        
        rss_content += """
  </channel>
</rss>"""
        
        return rss_content

    def create_car_item(self, channel, car, index):
        """สร้าง RSS item สำหรับรถแต่ละคัน"""
        item = ET.SubElement(channel, "item")
        
        # Title
        title = f"รถใหม่เข้า: {car['title']}"
        ET.SubElement(item, "title").text = title
        
        # Link
        car_link = f"{self.base_url}/car-detail/{car['handle']}.html"
        ET.SubElement(item, "link").text = car_link
        ET.SubElement(item, "guid").text = car_link
        
        # Description
        description = self.create_car_description(car)
        ET.SubElement(item, "description").text = html.escape(description)
        
        # Content (HTML)
        content = self.create_car_content(car)
        content_elem = ET.SubElement(item, "{http://purl.org/rss/1.0/modules/content/}encoded")
        content_elem.text = f"<![CDATA[{content}]]>"
        
        # Category
        ET.SubElement(item, "category").text = f"รถยนต์{car['title'].split()[0] if car['title'].split() else ''}"
        
        # Author
        ET.SubElement(item, "{http://purl.org/dc/elements/1.1/}creator").text = "ครูหนึ่งรถสวย"
        
        # Publication date (ใช้เวลาปัจจุบันลบด้วย index เพื่อจำลองเวลาที่แตกต่างกัน)
        pub_date = datetime.now(timezone.utc)
        pub_date = pub_date.replace(hour=pub_date.hour - index)
        ET.SubElement(item, "pubDate").text = pub_date.strftime("%a, %d %b %Y %H:%M:%S %z")

        # Enclosure (รูปภาพ)
        if car["images"]:
            enclosure = ET.SubElement(item, "enclosure")
            enclosure.set("url", car["images"][0])
            enclosure.set("type", "image/jpeg")
            enclosure.set("length", "0")

    def create_car_description(self, car):
        """สร้าง description สำหรับ RSS"""
        # แยกยี่ห้อจากชื่อ
        title_parts = car["title"].split()
        brand = title_parts[0] if title_parts else ""
        
        description = f"""
🚗 {car['title']}
💰 ราคา: ฿{car['price']:,.0f}
🏢 ยี่ห้อ: {brand}
📍 สถานที่: เชียงใหม่
✅ สถานะ: พร้อมขาย

🎯 พิเศษ:
• ฟรีดาวน์ 100%
• รับประกัน 1 ปี
• ส่งฟรีทั่วไทย
• ผ่อนเริ่มต้น 3,000/เดือน

📞 สนใจติดต่อ: ครูหนึ่งรถสวย
🌐 ดูรายละเอียดเพิ่มเติม: {self.base_url}/car-detail/{car['handle']}.html

{car['desc'][:200]}...
""".strip()
        
        return description

    def create_car_content(self, car):
        """สร้าง HTML content สำหรับ RSS"""
        main_image = car["images"][0] if car["images"] else ""
        
        content = f"""
<div style="font-family: 'Prompt', sans-serif; max-width: 600px; margin: 0 auto;">
  <h2 style="color: #f47b20; margin: 0 0 1rem;">{car['title']}</h2>
  
  {f'<img src="{main_image}" alt="{car["title"]}" style="width: 100%; max-width: 500px; border-radius: 8px; margin: 1rem 0;">' if main_image else ''}
  
  <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
    <h3 style="color: #2c3e50; margin: 0 0 1rem;">📊 ข้อมูลรถยนต์</h3>
    <table style="width: 100%; border-collapse: collapse;">
      <tr>
        <td style="padding: 0.5rem; font-weight: bold; color: #7f8c8d;">ราคา:</td>
        <td style="padding: 0.5rem; color: #e74c3c; font-weight: bold; font-size: 1.2em;">฿{car['price']:,.0f}</td>
      </tr>
      <tr style="background: #fff;">
        <td style="padding: 0.5rem; font-weight: bold; color: #7f8c8d;">ยี่ห้อ:</td>
        <td style="padding: 0.5rem;">{car['title'].split()[0] if car['title'].split() else 'ไม่ระบุ'}</td>
      </tr>
      <tr>
        <td style="padding: 0.5rem; font-weight: bold; color: #7f8c8d;">สถานที่:</td>
        <td style="padding: 0.5rem;">เชียงใหม่, ประเทศไทย</td>
      </tr>
      <tr style="background: #fff;">
        <td style="padding: 0.5rem; font-weight: bold; color: #7f8c8d;">การรับประกัน:</td>
        <td style="padding: 0.5rem;">1 ปีเต็ม</td>
      </tr>
    </table>
  </div>
  
  <div style="background: linear-gradient(135deg, #f47b20, #e66a16); color: white; padding: 1.5rem; border-radius: 8px; margin: 1rem 0; text-align: center;">
    <h3 style="margin: 0 0 1rem;">🎯 สิทธิพิเศษ</h3>
    <ul style="list-style: none; padding: 0; margin: 0;">
      <li style="margin: 0.5rem 0;">🆓 ฟรีดาวน์ 100%</li>
      <li style="margin: 0.5rem 0;">🛡️ รับประกัน 1 ปี</li>
      <li style="margin: 0.5rem 0;">🚚 ส่งฟรีทั่วไทย</li>
      <li style="margin: 0.5rem 0;">💰 ผ่อนเริ่มต้น 3,000/เดือน</li>
    </ul>
  </div>
  
  <div style="margin: 1.5rem 0;">
    <h3 style="color: #2c3e50;">📝 รายละเอียด</h3>
    <p style="line-height: 1.6; color: #555;">{html.escape(car['desc'][:500])}...</p>
  </div>
  
  <div style="text-align: center; margin: 2rem 0;">
    <a href="{car['link']}" 
       style="background: #f47b20; color: white; padding: 1rem 2rem; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
      📞 ติดต่อสอบถาม
    </a>
  </div>
  
  <hr style="border: none; border-top: 1px solid #eee; margin: 2rem 0;">
  
  <div style="text-align: center; color: #7f8c8d; font-size: 0.9em;">
    <p>ครูหนึ่งรถสวย - รถมือสองคุณภาพเชียงใหม่</p>
    <p>📧 ติดต่อ: info@kn-goodcar.com | 📞 โทร: xxx-xxx-xxxx</p>
    <p>🌐 เว็บไซต์: <a href="{self.base_url}" style="color: #f47b20;">{self.base_url}</a></p>
  </div>
</div>
"""
        return content

    def generate_feed(self):
        """สร้างและบันทึก RSS feed"""
        print("📡 สร้าง RSS Feed สำหรับ Google News...")
        
        # สร้าง RSS content
        rss_content = self.create_rss_feed()
        
        # บันทึกไฟล์
        docs_path = Path("docs")
        docs_path.mkdir(exist_ok=True)
        
        feed_path = docs_path / "feed.xml"
        with open(feed_path, "w", encoding="utf-8") as f:
            f.write(rss_content)
        
        print(f"✅ สร้าง RSS Feed สำเร็จ")
        print(f"📊 Items: {min(len(self.cars_data), 10)} รายการ")
        print(f"🔗 URL: {self.base_url}/feed.xml")
        print(f"🎯 Google News: Ready")
        print(f"📅 อัปเดต: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """ฟังก์ชันหลักสำหรับรันสคริปต์"""
    generator = RSSFeedGenerator()
    generator.generate_feed()


if __name__ == "__main__":
    main()