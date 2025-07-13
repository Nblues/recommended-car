#!/usr/bin/env python3
"""
Update ALL car detail HTML files to enterprise-level with CTA buttons
ให้ทุกไฟล์มี social media buttons และ layout ที่สวยงาม
"""

import os
import glob
import re

def update_all_car_detail_files():
    # Template CSS สำหรับ car detail pages
    css_template = '''  <!-- Critical CSS Inline -->
  <style>
    /* Critical CSS สำหรับ LCP < 1.2s - Enterprise Level */
    body{font-family:'Prompt',sans-serif !important;margin:0 !important;background:#f7f7fb !important;line-height:1.6;color:#2c3e50 !important}
    .container{max-width:1200px !important;margin:0 auto !important;padding:1rem !important}
    .car-header{background:#fff !important;border-radius:12px !important;padding:2rem !important;margin-bottom:2rem !important;box-shadow:0 4px 12px rgba(0,0,0,.08) !important}
    .car-title{font-size:2rem !important;font-weight:700 !important;margin:0 0 1rem !important;color:#2c3e50 !important}
    .car-price{font-size:2.5rem !important;color:#e74c3c !important;font-weight:800 !important;margin:0 0 1rem !important}
    .car-badge{display:inline-block !important;background:#27ae60 !important;color:#fff !important;padding:.5rem 1rem !important;border-radius:20px !important;font-size:.9rem !important;margin:.5rem .5rem 0 0 !important}
    .car-gallery{display:grid !important;grid-template-columns:2fr 1fr !important;gap:1rem !important;margin:2rem 0 !important}
    .main-image{border-radius:8px !important;overflow:hidden !important;background:#f0f0f0 !important}
    .thumbnail-grid{display:grid !important;grid-template-columns:1fr 1fr !important;gap:.5rem !important}
    .thumbnail{border-radius:6px !important;overflow:hidden !important;background:#f0f0f0 !important;cursor:pointer !important;transition:transform .2s !important}
    .thumbnail:hover{transform:scale(1.05) !important}
    .car-details{background:#fff !important;border-radius:12px !important;padding:2rem !important;margin-bottom:2rem !important;box-shadow:0 4px 12px rgba(0,0,0,.08) !important}
    .detail-grid{display:grid !important;grid-template-columns:repeat(auto-fit,minmax(200px,1fr)) !important;gap:1rem !important;margin:1rem 0 !important}
    .detail-item{padding:1rem !important;background:#f8f9fa !important;border-radius:8px !important;border-left:4px solid #f47b20 !important}
    .detail-label{font-weight:600 !important;color:#7f8c8d !important;font-size:.9rem !important}
    .detail-value{font-size:1.1rem !important;margin-top:.25rem !important}
    .cta-section{background:linear-gradient(135deg,#f47b20,#e66a16) !important;border-radius:12px !important;padding:2rem !important;text-align:center !important;color:#fff !important;margin:2rem 0 !important}
    .cta-button{display:inline-block !important;background:#fff !important;color:#f47b20 !important;padding:1rem 2rem !important;border-radius:8px !important;text-decoration:none !important;font-weight:700 !important;margin:.5rem !important;transition:transform .2s !important;box-shadow:0 4px 8px rgba(0,0,0,0.1) !important}
    .cta-button:hover{transform:translateY(-2px) !important;box-shadow:0 6px 12px rgba(0,0,0,0.15) !important}
    .cta-button:active{transform:translateY(0) !important}
    .breadcrumb{margin:1rem 0 !important;font-size:.9rem !important}
    .breadcrumb a{color:#f47b20 !important;text-decoration:none !important}
    .breadcrumb a:hover{text-decoration:underline !important}
    @media(max-width:768px){.car-gallery{grid-template-columns:1fr !important}.car-title{font-size:1.5rem !important}.car-price{font-size:2rem !important}}
  </style>'''

    # Template CTA section
    cta_template = '''
  <!-- CTA Section -->
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
        <a href="https://nblues.github.io/recommended-car/#cars" class="cta-button" style="background: #17a2b8; color: white;">
          🚗 ดูรถทั้งหมด
        </a>
      </div>
    </section>
  </div>'''

    # หาไฟล์ HTML ทั้งหมดในโฟลเดอร์ car-detail
    html_files = glob.glob('docs/car-detail/*.html')
    
    print(f"กำลังอัปเดต {len(html_files)} ไฟล์ให้เป็น enterprise-level...")
    
    updated_count = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. ลบ external CSS ที่ขัดแย้ง
            content = re.sub(
                r'<link rel="stylesheet" href="../car-detail-enhanced\.css"[^>]*>',
                '<!-- CSS conflicts removed -->',
                content
            )
            content = re.sub(
                r'<noscript><link rel="stylesheet" href="../car-detail-enhanced\.css"></noscript>',
                '',
                content
            )
            
            # 2. เพิ่ม CSS inline ถ้ายังไม่มี
            if 'Critical CSS สำหรับ LCP' not in content:
                # หาตำแหน่งหลัง </head> tag
                head_end = content.find('</head>')
                if head_end != -1:
                    content = content[:head_end] + css_template + '\n' + content[head_end:]
            
            # 3. เพิ่ม CTA section ถ้ายังไม่มี
            if 'สนใจรถคันนี้?' not in content:
                # หาตำแหน่งก่อน </body>
                body_end = content.find('</body>')
                if body_end != -1:
                    content = content[:body_end] + cta_template + '\n' + content[body_end:]
            
            # 4. ปรับปรุง meta tags ให้เป็น SEO-friendly
            if 'ครูหนึ่งรถสวย' not in content:
                content = re.sub(
                    r'<meta property="og:site_name" content="[^"]*">',
                    '<meta property="og:site_name" content="ครูหนึ่งรถสวย">',
                    content
                )
            
            # เขียนไฟล์กลับ ถ้ามีการเปลี่ยนแปลง
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_count += 1
                print(f"✅ อัปเดต: {os.path.basename(file_path)}")
            else:
                print(f"⚡ ไม่เปลี่ยนแปลง: {os.path.basename(file_path)}")
            
        except Exception as e:
            print(f"❌ ข้อผิดพลาดกับไฟล์ {file_path}: {e}")
    
    print(f"\n🎉 อัปเดตเสร็จสิ้น: {updated_count}/{len(html_files)} ไฟล์")
    print("ทุกไฟล์ car detail ได้รับการอัปเดตเป็น enterprise-level พร้อม social CTA buttons!")

if __name__ == "__main__":
    update_all_car_detail_files()
