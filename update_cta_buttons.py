#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
อัพเดตปุ่ม CTA ในหน้า car detail ทั้งหมด
"""

import os
import glob

def update_cta_buttons():
    """อัพเดตปุ่ม CTA ในไฟล์ car detail ทั้งหมด"""
    
    # หา CTA section เดิม
    old_cta = '''  <!-- CTA Section -->
  <div class="container">
    <section class="cta-section">
      <h2>สนใจรถคันนี้?</h2>
      <p>ติดต่อเราเพื่อดูรถ ทดลองขับ และจัดไฟแนนซ์</p>
      <a href="https://nblues.github.io/recommended-car/" class="cta-button" target="_blank" rel="noopener">
        📞 ติดต่อสอบถาม
      </a>
      <a href="tel:+66-xxx-xxx-xxxx" class="cta-button">
        📲 โทรเลย
      </a>
      <a href="/" class="cta-button">
        🚗 ดูรถอื่น
      </a>
    </section>
  </div>'''
    
    # CTA section ใหม่
    new_cta = '''  <!-- CTA Section -->
  <div class="container">
    <section class="cta-section">
      <h2>💬 สนใจรถคันนี้?</h2>
      <p>ติดต่อเราเพื่อดูรถ ทดลองขับ และจัดไฟแนนซ์</p>
      
      <!-- Social Contact Buttons -->
      <div style="margin: 2rem 0;">
        <a href="https://line.me/R/ti/p/@krunung-car" class="cta-button" target="_blank" rel="noopener" style="background: #00C300; color: white;">
          💬 LINE: @krunung-car
        </a>
        <a href="https://www.facebook.com/krunung.car" class="cta-button" target="_blank" rel="noopener" style="background: #1877F2; color: white;">
          📘 Facebook: ครูหนึ่งรถสวย
        </a>
        <a href="tel:089-xxx-xxxx" class="cta-button" style="background: #FF6B35; color: white;">
          📞 โทร: 089-xxx-xxxx
        </a>
      </div>
      
      <!-- Navigation Buttons -->
      <div style="margin: 2rem 0; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 2rem;">
        <a href="https://nblues.github.io/recommended-car/" class="cta-button" style="background: #28a745; color: white;">
          🏠 กลับหน้าแรก
        </a>
        <a href="https://chiangraiusedcar.com/all-cars" class="cta-button" target="_blank" rel="noopener" style="background: #007bff; color: white;">
          🚗 ดูรถทั้งหมด
        </a>
        <a href="https://nblues.github.io/recommended-car/" class="cta-button" style="background: #6c757d; color: white;">
          📋 รถแนะนำอื่น
        </a>
      </div>
    </section>
  </div>'''
    
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
            
            # แทนที่ CTA section
            if old_cta in content:
                content = content.replace(old_cta, new_cta)
                
                # เขียนกลับไฟล์
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                updated_count += 1
                print(f"✅ อัพเดต: {os.path.basename(file_path)}")
                
        except Exception as e:
            print(f"❌ ข้อผิดพลาด: {file_path} - {e}")
    
    print(f"\n🎉 อัพเดตสำเร็จ: {updated_count} ไฟล์")

if __name__ == "__main__":
    update_cta_buttons()
