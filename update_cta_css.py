#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
อัพเดต CSS สำหรับปุ่ม CTA ในหน้า car detail ทั้งหมด
"""

import os
import glob

def update_cta_css():
    """อัพเดต CSS สำหรับปุ่ม CTA"""
    
    # CSS เดิม
    old_css = '''    .cta-button{display:inline-block;background:#fff;color:#f47b20;padding:1rem 2rem;border-radius:8px;text-decoration:none;font-weight:700;margin:.5rem;transition:transform .2s}
    .cta-button:hover{transform:translateY(-2px)}'''
    
    # CSS ใหม่
    new_css = '''    .cta-button{display:inline-block;background:#fff;color:#f47b20;padding:1rem 2rem;border-radius:8px;text-decoration:none;font-weight:700;margin:.5rem;transition:transform .2s;box-shadow:0 4px 8px rgba(0,0,0,0.1)}
    .cta-button:hover{transform:translateY(-2px);box-shadow:0 6px 12px rgba(0,0,0,0.15)}
    .cta-button:active{transform:translateY(0)}'''
    
    # ค้นหาไฟล์ HTML ทั้งหมดในโฟลเดอร์ car-detail
    car_detail_files = glob.glob("docs/car-detail/*.html")
    updated_count = 0
    
    for file_path in car_detail_files:
        if 'navigation-test.html' in file_path or 'dummy' in file_path:
            continue
            
        try:
            # อ่านไฟล์
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # แทนที่ CSS
            if old_css in content:
                content = content.replace(old_css, new_css)
                
                # เขียนกลับไฟล์
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                updated_count += 1
                print(f"✅ อัพเดต CSS: {os.path.basename(file_path)}")
                
        except Exception as e:
            print(f"❌ ข้อผิดพลาด: {file_path} - {e}")
    
    print(f"\n🎉 อัพเดต CSS สำเร็จ: {updated_count} ไฟล์")

if __name__ == "__main__":
    update_cta_css()
