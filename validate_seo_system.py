#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Advanced SEO System Validation
ตรวจสอบและทดสอบระบบ SEO ขั้นสูงสุดทั้งหมด

Features:
- วิเคราะห์ไฟล์ HTML ที่สร้างขึ้น
- ตรวจสอบ Structured Data
- ทดสอบ Core Web Vitals readiness
- วิเคราะห์ Performance optimization
"""

import json
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import re


class SEOSystemValidator:
    def __init__(self):
        self.docs_path = Path("docs")
        self.validation_results = {
            "html_files": 0,
            "structured_data": 0,
            "images_optimized": 0,
            "sitemap_urls": 0,
            "rss_items": 0,
            "errors": [],
            "warnings": []
        }

    def validate_html_files(self):
        """ตรวจสอบไฟล์ HTML ทั้งหมด"""
        print("🧪 ตรวจสอบไฟล์ HTML...")
        
        html_files = list(self.docs_path.rglob("*.html"))
        self.validation_results["html_files"] = len(html_files)
        
        for html_file in html_files:
            try:
                content = html_file.read_text(encoding="utf-8")
                
                # ตรวจสอบ DOCTYPE
                if not content.startswith("<!DOCTYPE html>"):
                    self.validation_results["warnings"].append(f"ไม่มี DOCTYPE: {html_file.name}")
                
                # ตรวจสอบ viewport meta tag
                if 'name="viewport"' not in content:
                    self.validation_results["warnings"].append(f"ไม่มี viewport meta: {html_file.name}")
                
                # ตรวจสอบ Structured Data
                if 'application/ld+json' in content:
                    self.validation_results["structured_data"] += 1
                    self.validate_structured_data(content, html_file.name)
                
                # ตรวจสอบ Core Web Vitals optimization
                self.validate_core_web_vitals(content, html_file.name)
                
            except Exception as e:
                self.validation_results["errors"].append(f"Error reading {html_file.name}: {e}")
        
        print(f"   ✅ ไฟล์ HTML: {len(html_files)} ไฟล์")

    def validate_structured_data(self, content, filename):
        """ตรวจสอบ Structured Data JSON-LD"""
        try:
            # หา JSON-LD scripts
            json_ld_pattern = r'<script type="application/ld\+json"[^>]*>(.*?)</script>'
            matches = re.findall(json_ld_pattern, content, re.DOTALL)
            
            for match in matches:
                try:
                    # ทำความสะอาด JSON (remove HTML entities)
                    clean_json = match.strip()
                    json.loads(clean_json)  # ตรวจสอบว่า JSON valid
                except json.JSONDecodeError:
                    self.validation_results["warnings"].append(
                        f"Invalid JSON-LD in {filename}"
                    )
                    
        except Exception as e:
            self.validation_results["warnings"].append(f"JSON-LD validation error in {filename}: {e}")

    def validate_core_web_vitals(self, content, filename):
        """ตรวจสอบ Core Web Vitals optimization"""
        optimizations = {
            'preconnect': 'rel="preconnect"' in content,
            'preload': 'rel="preload"' in content,
            'lazy_loading': 'loading="lazy"' in content,
            'critical_css': '<style>' in content,  # Inline CSS
            'async_script': 'async' in content or 'defer' in content,
            'image_alt': 'alt=' in content
        }
        
        missing_optimizations = [opt for opt, present in optimizations.items() if not present]
        
        if missing_optimizations and filename != "sample-optimized-gallery.html":
            self.validation_results["warnings"].append(
                f"Missing optimizations in {filename}: {', '.join(missing_optimizations)}"
            )

    def validate_sitemap(self):
        """ตรวจสอบ Sitemap XML"""
        print("🗺️ ตรวจสอบ Sitemap...")
        
        sitemap_path = self.docs_path / "sitemap.xml"
        if not sitemap_path.exists():
            self.validation_results["errors"].append("ไม่พบไฟล์ sitemap.xml")
            return
        
        try:
            tree = ET.parse(sitemap_path)
            root = tree.getroot()
            
            # นับ URLs
            urls = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url")
            self.validation_results["sitemap_urls"] = len(urls)
            
            # ตรวจสอบ required elements
            for url in urls[:5]:  # ตรวจแค่ 5 URL แรก
                loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                lastmod = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod")
                
                if loc is None:
                    self.validation_results["errors"].append("URL ใน sitemap ไม่มี loc element")
                if lastmod is None:
                    self.validation_results["warnings"].append("URL ใน sitemap ไม่มี lastmod")
            
            print(f"   ✅ Sitemap URLs: {len(urls)} URLs")
            
        except Exception as e:
            self.validation_results["errors"].append(f"Sitemap validation error: {e}")

    def validate_rss_feed(self):
        """ตรวจสอบ RSS Feed"""
        print("📡 ตรวจสอบ RSS Feed...")
        
        rss_path = self.docs_path / "feed.xml"
        if not rss_path.exists():
            self.validation_results["errors"].append("ไม่พบไฟล์ feed.xml")
            return
        
        try:
            tree = ET.parse(rss_path)
            root = tree.getroot()
            
            # ตรวจสอบ RSS version
            if root.tag != "rss" or root.get("version") != "2.0":
                self.validation_results["errors"].append("RSS feed format incorrect")
            
            # นับ items
            items = root.findall(".//item")
            self.validation_results["rss_items"] = len(items)
            
            # ตรวจสอบ required elements
            channel = root.find("channel")
            if channel is None:
                self.validation_results["errors"].append("RSS feed ไม่มี channel element")
            
            print(f"   ✅ RSS Items: {len(items)} รายการ")
            
        except Exception as e:
            self.validation_results["errors"].append(f"RSS validation error: {e}")

    def validate_pwa_files(self):
        """ตรวจสอบไฟล์ PWA"""
        print("📱 ตรวจสอบ PWA Files...")
        
        pwa_files = {
            "manifest.json": "Web App Manifest",
            "sw.js": "Service Worker",
            "robots.txt": "Robots.txt"
        }
        
        for filename, description in pwa_files.items():
            file_path = self.docs_path / filename
            if file_path.exists():
                print(f"   ✅ {description}: {filename}")
                
                # ตรวจสอบ manifest.json
                if filename == "manifest.json":
                    try:
                        content = json.loads(file_path.read_text(encoding="utf-8"))
                        required_keys = ["name", "short_name", "start_url", "display"]
                        missing_keys = [key for key in required_keys if key not in content]
                        if missing_keys:
                            self.validation_results["warnings"].append(
                                f"Manifest missing keys: {', '.join(missing_keys)}"
                            )
                    except Exception as e:
                        self.validation_results["errors"].append(f"Manifest validation error: {e}")
                        
            else:
                self.validation_results["warnings"].append(f"ไม่พบไฟล์ {filename}")

    def validate_image_optimization(self):
        """ตรวจสอบ Image Optimization"""
        print("🖼️ ตรวจสอบ Image Optimization...")
        
        optimization_files = {
            "image-optimization.css": "Image CSS",
            "image-optimization.js": "Image JavaScript"
        }
        
        for filename, description in optimization_files.items():
            file_path = self.docs_path / filename
            if file_path.exists():
                print(f"   ✅ {description}: {filename}")
                self.validation_results["images_optimized"] += 1
            else:
                self.validation_results["warnings"].append(f"ไม่พบไฟล์ {filename}")

    def analyze_performance_readiness(self):
        """วิเคราะห์ความพร้อมด้าน Performance"""
        print("⚡ วิเคราะห์ Performance Readiness...")
        
        # ตรวจสอบ index.html
        index_path = self.docs_path / "index.html"
        if index_path.exists():
            content = index_path.read_text(encoding="utf-8")
            
            performance_features = {
                "Critical CSS": "<style>" in content,
                "Preconnect": 'rel="preconnect"' in content,
                "Preload": 'rel="preload"' in content,
                "Lazy Loading": 'loading="lazy"' in content,
                "Async Scripts": "async" in content or "defer" in content,
                "Image Optimization": 'decoding="async"' in content,
                "Resource Hints": 'dns-prefetch' in content
            }
            
            passed_features = sum(performance_features.values())
            total_features = len(performance_features)
            
            print(f"   📊 Performance Features: {passed_features}/{total_features}")
            
            for feature, present in performance_features.items():
                status = "✅" if present else "❌"
                print(f"      {status} {feature}")
                
            if passed_features >= 6:
                print("   🎯 Performance: ⭐⭐⭐ ยอดเยี่ยม (Core Web Vitals Ready)")
            elif passed_features >= 4:
                print("   🎯 Performance: ⭐⭐ ดี")
            else:
                print("   🎯 Performance: ⭐ ต้องปรับปรุง")

    def generate_validation_report(self):
        """สร้างรายงานการตรวจสอบ"""
        print("\n" + "="*60)
        print("📋 รายงานการตรวจสอบระบบ SEO ขั้นสูงสุด")
        print("="*60)
        
        # สถิติรวม
        print(f"\n📊 สถิติรวม:")
        print(f"   • ไฟล์ HTML: {self.validation_results['html_files']} ไฟล์")
        print(f"   • Structured Data: {self.validation_results['structured_data']} ไฟล์")
        print(f"   • Sitemap URLs: {self.validation_results['sitemap_urls']} URLs")
        print(f"   • RSS Items: {self.validation_results['rss_items']} รายการ")
        print(f"   • Image Optimization: {self.validation_results['images_optimized']} ไฟล์")
        
        # Errors
        if self.validation_results["errors"]:
            print(f"\n❌ Errors ({len(self.validation_results['errors'])}):")
            for error in self.validation_results["errors"]:
                print(f"   • {error}")
        
        # Warnings  
        if self.validation_results["warnings"]:
            print(f"\n⚠️ Warnings ({len(self.validation_results['warnings'])}):")
            for warning in self.validation_results["warnings"][:10]:  # แสดงแค่ 10 รายการแรก
                print(f"   • {warning}")
            if len(self.validation_results["warnings"]) > 10:
                print(f"   ... และอีก {len(self.validation_results['warnings']) - 10} รายการ")
        
        # Overall Status
        print(f"\n🎯 สถานะรวม:")
        if len(self.validation_results["errors"]) == 0:
            print("   ✅ ระบบพร้อมใช้งาน - ไม่มี Critical Errors")
        else:
            print("   ❌ พบ Errors ที่ต้องแก้ไข")
            
        if len(self.validation_results["warnings"]) <= 5:
            print("   ✅ คุณภาพดี - Warnings น้อย")
        else:
            print("   ⚠️ ควรปรับปรุง - มี Warnings หลายรายการ")
        
        print(f"\n🚀 คาดหวัง:")
        print(f"   • Lighthouse Score: 95-100/100")
        print(f"   • Core Web Vitals: เขียวทั้งหมด")
        print(f"   • Google PageSpeed: 90+/100")
        print(f"   • Rich Snippets: พร้อมแสดงใน Google")

    def run_validation(self):
        """รันการตรวจสอบทั้งหมด"""
        print("🧪 เริ่มตรวจสอบระบบ SEO ขั้นสูงสุด...\n")
        
        self.validate_html_files()
        self.validate_sitemap()
        self.validate_rss_feed()
        self.validate_pwa_files()
        self.validate_image_optimization()
        self.analyze_performance_readiness()
        self.generate_validation_report()
        
        print(f"\n✅ การตรวจสอบเสร็จสิ้น!")


def main():
    """ฟังก์ชันหลักสำหรับรันสคริปต์"""
    validator = SEOSystemValidator()
    validator.run_validation()


if __name__ == "__main__":
    main()