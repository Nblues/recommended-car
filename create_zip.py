#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📦 CREATE DEPLOYMENT PACKAGE
สร้างไฟล์ ZIP พร้อม deploy
"""

import zipfile
import os
from pathlib import Path
from datetime import datetime

def create_deployment_zip():
    """สร้าง ZIP file สำหรับ deployment"""
    
    print("📦 Creating deployment ZIP package...")
    
    # Setup paths
    project_root = Path(__file__).parent
    online_ready = project_root / "online-ready"
    
    if not online_ready.exists():
        print("❌ online-ready folder not found. Run simple_online_deploy.py first")
        return
    
    # Create ZIP filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"car-widgets-online-{timestamp}.zip"
    zip_path = project_root / zip_filename
    
    # Create ZIP file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files from online-ready folder
        for file_path in online_ready.rglob('*'):
            if file_path.is_file():
                # Calculate relative path for archive
                archive_name = file_path.relative_to(online_ready)
                zipf.write(file_path, archive_name)
                print(f"✅ Added: {archive_name}")
    
    print(f"\n🎉 ZIP package created: {zip_filename}")
    print(f"📁 Location: {zip_path.absolute()}")
    print(f"📊 Size: {zip_path.stat().st_size / 1024:.1f} KB")
    
    print("\n🚀 READY TO DEPLOY!")
    print("=" * 40)
    print("📋 Deployment Options:")
    print("1. Extract ZIP และ upload ไป Netlify")
    print("2. Extract ZIP และ upload ไป Vercel") 
    print("3. Extract ZIP และ push ไป GitHub")
    print("4. Extract ZIP และ deploy ไป Firebase")
    
    print("\n⚡ Quick Steps:")
    print(f"1. Extract {zip_filename}")
    print("2. ไปที่ netlify.com")
    print("3. Drag & drop folder ที่ extract แล้ว")
    print("4. รอ 2 นาทีใ → เสร็จ!")
    print("5. แชร์ URL กับผู้ใช้")
    
    return zip_path

if __name__ == "__main__":
    zip_path = create_deployment_zip()
    
    # Try to open the folder containing the ZIP
    try:
        import subprocess
        subprocess.run(f'explorer /select,"{zip_path.absolute()}"', shell=True)
    except:
        pass
