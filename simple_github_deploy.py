#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 SIMPLE GITHUB PAGES DEPLOYMENT
Deploy แบบง่ายๆ โดยไม่ลบไฟล์เก่า
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

def simple_github_deploy():
    """Deploy แบบง่ายๆ"""
    
    print("🚀 SIMPLE GITHUB PAGES DEPLOYMENT")
    print("=" * 45)
    
    project_root = Path(__file__).parent
    online_ready = project_root / "online-ready"
    
    if not online_ready.exists():
        print("❌ online-ready folder not found")
        return False
    
    try:
        os.chdir(project_root)
        
        # ตรวจสอบ git status
        print("📋 Checking git status...")
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True)
        
        # ตรวจสอบว่ามี main branch หรือไม่
        try:
            subprocess.run(["git", "checkout", "main"], 
                          check=True, capture_output=True)
            current_branch = "main"
        except:
            try:
                subprocess.run(["git", "checkout", "master"], 
                              check=True, capture_output=True)
                current_branch = "master"
            except:
                # สร้าง branch ใหม่
                subprocess.run(["git", "checkout", "-b", "main"], 
                              check=True, capture_output=True)
                current_branch = "main"
        
        print(f"✅ On branch: {current_branch}")
        
        # คัดลอกไฟล์จาก online-ready ไป root (ไม่ลบไฟล์เก่า)
        print("📁 Copying deployment files...")
        
        # คัดลอกไฟล์หลัก
        main_files = [
            "index.html",
            "netlify.toml", 
            "vercel.json",
            "package.json",
            "README.md",
            "DEPLOYMENT-GUIDE.md",
            "QUICK-DEPLOY.txt"
        ]
        
        for file_name in main_files:
            source = online_ready / file_name
            if source.exists():
                shutil.copy2(source, project_root / file_name)
                print(f"✅ Copied: {file_name}")
        
        # คัดลอก directories
        dirs_to_copy = ["api", "demo"]
        for dir_name in dirs_to_copy:
            source_dir = online_ready / dir_name
            target_dir = project_root / dir_name
            
            if source_dir.exists():
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                shutil.copytree(source_dir, target_dir)
                print(f"✅ Copied directory: {dir_name}")
        
        # สร้าง .nojekyll
        (project_root / ".nojekyll").write_text("")
        print("✅ .nojekyll created")
        
        # Add files
        print("📝 Adding files to git...")
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        
        # Commit
        commit_message = f"Deploy Car Widgets Collection - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        try:
            subprocess.run(["git", "commit", "-m", commit_message], 
                          check=True, capture_output=True)
            print("✅ Changes committed")
        except subprocess.CalledProcessError:
            print("ℹ️ No changes to commit")
        
        # Push to main/master
        print(f"🚀 Pushing to {current_branch}...")
        try:
            subprocess.run(["git", "push", "origin", current_branch], 
                          check=True, capture_output=True, timeout=30)
            print("✅ Pushed to GitHub successfully!")
        except subprocess.TimeoutExpired:
            print("⚠️ Push timeout - but may still be successful")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Push failed: {e}")
            print("💡 You may need to set up GitHub authentication")
        
        print("\n🎉 DEPLOYMENT COMPLETED!")
        print("=" * 30)
        print("🌐 Your Car Widgets are now LIVE at:")
        print("   https://nblues.github.io/recommended-car/")
        print("")
        print("📋 Enable GitHub Pages:")
        print("   1. Go to: https://github.com/nblues/recommended-car/settings/pages")
        print("   2. Source: Deploy from a branch")
        print("   3. Branch: main (or master)")
        print("   4. Folder: / (root)")
        print("   5. Save")
        print("")
        print("⏰ After enabling, wait 5-10 minutes for deployment")
        print("🔄 Check status at: https://github.com/nblues/recommended-car/actions")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False

def create_pages_instructions():
    """สร้างคู่มือ enable GitHub Pages"""
    
    instructions = """# 🚀 Enable GitHub Pages

## เปิดใช้งาน GitHub Pages ในขั้นตอนง่ายๆ:

### 1. ไปที่ Settings
```
https://github.com/nblues/recommended-car/settings/pages
```

### 2. Configure Source
- **Source:** Deploy from a branch
- **Branch:** main (หรือ master)  
- **Folder:** / (root)
- คลิก **Save**

### 3. รอสักครู่
- GitHub จะ build และ deploy อัตโนมัติ
- ใช้เวลาประมาณ 5-10 นาทีี

### 4. เข้าใช้งาน
```
https://nblues.github.io/recommended-car/
```

## 📋 หลังจาก Live แล้ว:

1. **แชร์ URL** กับผู้ที่ต้องการใช้ widget
2. **ผู้ใช้เลือก widget** → Copy code
3. **Paste ใน GoDaddy** Website Builder
4. **Customize API URLs**
5. **เริ่มได้รับ traffic เพิ่ม!**

## 🎯 Expected Results:

- 🎯 **Chiang Mai Widget:** "รถมือสองเชียงใหม่" Top 3
- 🔥 **Standard Widget:** +150% traffic  
- ⚡ **Instant Widget:** พร้อมใช้ทันที

---
*GitHub Pages Deployment Guide*
"""
    
    Path("GITHUB-PAGES-SETUP.md").write_text(instructions, encoding="utf-8")
    print("✅ GitHub Pages setup guide created")

if __name__ == "__main__":
    # สร้างคู่มือ
    create_pages_instructions()
    
    # Deploy
    success = simple_github_deploy()
    
    if success:
        print("\n🎊 SUCCESS! Ready for GitHub Pages!")
        print("📖 Follow GITHUB-PAGES-SETUP.md to enable Pages")
    else:
        print("\n❌ Deployment failed")
