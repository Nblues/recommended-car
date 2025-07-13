#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗺️ Dynamic Sitemap Generator - สร้าง Sitemap อัตโนมัติ
สำหรับ Google Indexing ที่รวดเร็วทะลุเพดาน

Features:
- Dynamic XML Sitemap generation
- Auto-submit to Google Search Console
- Priority และ Frequency optimization
- Image sitemap integration
- Multi-language support (th-TH)
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
import requests
import argparse


class SitemapGenerator:
    def __init__(self):
        self.base_url = "https://nblues.github.io/recommended-car"
        self.cars_data = self.load_cars_data()
        self.sitemap_urls = []

    def load_cars_data(self):
        """โหลดข้อมูลรถจาก cars.json"""
        try:
            with open("cars.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ ไม่พบไฟล์ cars.json")
            return []

    def add_url(self, loc, lastmod=None, changefreq="weekly", priority="0.8", images=None):
        """เพิ่ม URL ไปยัง sitemap"""
        url_data = {
            "loc": loc,
            "lastmod": lastmod or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "changefreq": changefreq,
            "priority": priority
        }
        
        if images:
            url_data["images"] = images
            
        self.sitemap_urls.append(url_data)

    def generate_main_pages(self):
        """สร้าง URL สำหรับหน้าหลัก"""
        # หน้าแรก (Priority สูงสุด)
        self.add_url(
            loc=f"{self.base_url}/",
            changefreq="hourly",
            priority="1.0"
        )
        
        # หน้า index.html
        self.add_url(
            loc=f"{self.base_url}/index.html",
            changefreq="hourly", 
            priority="1.0"
        )
        
        # Widget หน้า
        self.add_url(
            loc=f"{self.base_url}/mini-cars-static.html",
            changefreq="daily",
            priority="0.9"
        )

    def generate_car_detail_pages(self):
        """สร้าง URL สำหรับหน้ารถแต่ละคัน"""
        for car in self.cars_data:
            car_url = f"{self.base_url}/car-detail/{car['handle']}.html"
            
            # เตรียมข้อมูลรูปภาพสำหรับ Image Sitemap
            images = []
            for img_url in car["images"][:5]:  # เอาแค่ 5 รูปแรก
                images.append({
                    "loc": img_url,
                    "title": car["title"],
                    "caption": f"รูป{car['title']} - {car['brand']}"
                })
            
            self.add_url(
                loc=car_url,
                changefreq="weekly",
                priority="0.8",
                images=images
            )

    def generate_sitemap_xml(self):
        """สร้างไฟล์ sitemap.xml"""
        # สร้าง root element
        urlset = ET.Element("urlset")
        urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        urlset.set("xmlns:image", "http://www.google.com/schemas/sitemap-image/1.1")
        urlset.set("xmlns:xhtml", "http://www.w3.org/1999/xhtml")

        for url_data in self.sitemap_urls:
            url_elem = ET.SubElement(urlset, "url")
            
            # เพิ่ม elements หลัก
            ET.SubElement(url_elem, "loc").text = url_data["loc"]
            ET.SubElement(url_elem, "lastmod").text = url_data["lastmod"]
            ET.SubElement(url_elem, "changefreq").text = url_data["changefreq"]
            ET.SubElement(url_elem, "priority").text = url_data["priority"]
            
            # เพิ่ม hreflang สำหรับ Multi-language
            xhtml_link = ET.SubElement(url_elem, "{http://www.w3.org/1999/xhtml}link")
            xhtml_link.set("rel", "alternate")
            xhtml_link.set("hreflang", "th-TH")
            xhtml_link.set("href", url_data["loc"])
            
            # เพิ่ม Image Sitemap
            if "images" in url_data:
                for image in url_data["images"]:
                    image_elem = ET.SubElement(url_elem, "{http://www.google.com/schemas/sitemap-image/1.1}image")
                    ET.SubElement(image_elem, "{http://www.google.com/schemas/sitemap-image/1.1}loc").text = image["loc"]
                    ET.SubElement(image_elem, "{http://www.google.com/schemas/sitemap-image/1.1}title").text = image["title"]
                    ET.SubElement(image_elem, "{http://www.google.com/schemas/sitemap-image/1.1}caption").text = image["caption"]

        # สร้าง XML tree
        tree = ET.ElementTree(urlset)
        ET.indent(tree, space="  ", level=0)
        
        # บันทึกไฟล์
        docs_path = Path("docs")
        docs_path.mkdir(exist_ok=True)
        
        sitemap_path = docs_path / "sitemap.xml"
        tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)
        
        print(f"✅ สร้าง sitemap.xml สำเร็จ: {len(self.sitemap_urls)} URLs")
        return sitemap_path

    def generate_sitemap_index(self):
        """สร้าง sitemap index สำหรับ sitemap หลายไฟล์"""
        sitemapindex = ET.Element("sitemapindex")
        sitemapindex.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        
        # Main sitemap
        sitemap_elem = ET.SubElement(sitemapindex, "sitemap")
        ET.SubElement(sitemap_elem, "loc").text = f"{self.base_url}/sitemap.xml"
        ET.SubElement(sitemap_elem, "lastmod").text = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        
        # News sitemap (ถ้ามี)
        if Path("docs/news-sitemap.xml").exists():
            news_sitemap = ET.SubElement(sitemapindex, "sitemap")
            ET.SubElement(news_sitemap, "loc").text = f"{self.base_url}/news-sitemap.xml"
            ET.SubElement(news_sitemap, "lastmod").text = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

        tree = ET.ElementTree(sitemapindex)
        ET.indent(tree, space="  ", level=0)
        
        docs_path = Path("docs")
        index_path = docs_path / "sitemap-index.xml"
        tree.write(index_path, encoding="utf-8", xml_declaration=True)
        
        print("✅ สร้าง sitemap-index.xml สำเร็จ")

    def submit_to_google(self):
        """ส่ง sitemap ให้ Google Search Console อัตโนมัติ"""
        try:
            # Google Search Console API endpoint
            sitemap_url = f"{self.base_url}/sitemap.xml"
            google_endpoint = f"https://www.google.com/ping?sitemap={sitemap_url}"
            
            # ส่งคำขอไปยัง Google
            response = requests.get(google_endpoint, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ ส่ง sitemap ให้ Google สำเร็จ: {sitemap_url}")
            else:
                print(f"❌ ส่ง sitemap ไม่สำเร็จ: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error ส่ง sitemap: {e}")

    def submit_to_bing(self):
        """ส่ง sitemap ให้ Bing Webmaster Tools"""
        try:
            sitemap_url = f"{self.base_url}/sitemap.xml"
            bing_endpoint = f"https://www.bing.com/ping?sitemap={sitemap_url}"
            
            response = requests.get(bing_endpoint, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ ส่ง sitemap ให้ Bing สำเร็จ: {sitemap_url}")
            else:
                print(f"❌ ส่ง sitemap ให้ Bing ไม่สำเร็จ: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error ส่ง sitemap ให้ Bing: {e}")

    def generate_robots_txt(self):
        """สร้างไฟล์ robots.txt ที่เพอร์เฟ็คสำหรับ SEO"""
        robots_content = f"""User-agent: *
Allow: /

# Sitemap locations
Sitemap: {self.base_url}/sitemap.xml
Sitemap: {self.base_url}/sitemap-index.xml

# Block unimportant pages
Disallow: /tmp/
Disallow: /.git/
Disallow: /node_modules/

# Crawl-delay for polite crawling
Crawl-delay: 1

# SEO Optimized for ครูหนึ่งรถสวย
# รถมือสองเชียงใหม่ ฟรีดาวน์ ส่งฟรีทั่วไทย
# Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        docs_path = Path("docs")
        robots_path = docs_path / "robots.txt"
        
        with open(robots_path, "w", encoding="utf-8") as f:
            f.write(robots_content)
        
        print("✅ สร้าง robots.txt สำเร็จ")

    def build_sitemap(self, submit_google=False):
        """สร้าง sitemap ทั้งหมด"""
        print("🗺️ เริ่มสร้าง Dynamic Sitemap...")
        
        # เคลียร์ข้อมูลเก่า
        self.sitemap_urls = []
        
        # สร้าง URLs
        self.generate_main_pages()
        self.generate_car_detail_pages()
        
        # สร้างไฟล์ sitemap
        sitemap_path = self.generate_sitemap_xml()
        self.generate_sitemap_index()
        self.generate_robots_txt()
        
        print(f"📊 สรุป Sitemap:")
        print(f"   - URLs ทั้งหมด: {len(self.sitemap_urls)}")
        print(f"   - รถยนต์: {len(self.cars_data)} คัน")
        print(f"   - รูปภาพ: {sum(len(url.get('images', [])) for url in self.sitemap_urls)}")
        
        # ส่งให้ Search Engines ถ้าต้องการ
        if submit_google:
            print("\n🚀 ส่ง sitemap ให้ Search Engines...")
            self.submit_to_google()
            self.submit_to_bing()
        
        print("✅ สร้าง Dynamic Sitemap สำเร็จ!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="สร้าง Dynamic Sitemap สำหรับ SEO")
    parser.add_argument("--submit-google", action="store_true", 
                       help="ส่ง sitemap ให้ Google Search Console อัตโนมัติ")
    
    args = parser.parse_args()
    
    generator = SitemapGenerator()
    generator.build_sitemap(submit_google=args.submit_google)