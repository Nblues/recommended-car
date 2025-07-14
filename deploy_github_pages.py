#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 GITHUB PAGES DEPLOYMENT
Deploy Car Widgets ขึ้น GitHub Pages ทันที
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

def deploy_to_github_pages():
    """Deploy ขึ้น GitHub Pages"""
    
    print("🚀 DEPLOYING TO GITHUB PAGES")
    print("=" * 40)
    
    project_root = Path(__file__).parent
    online_ready = project_root / "online-ready"
    
    if not online_ready.exists():
        print("❌ online-ready folder not found")
        return False
    
    try:
        # เปลี่ยนไปยัง project directory
        os.chdir(project_root)
        
        # ตรวจสอบว่ามี git repository แล้วหรือไม่
        if not (project_root / ".git").exists():
            print("📦 Initializing git repository...")
            subprocess.run(["git", "init"], check=True, capture_output=True)
            print("✅ Git repository initialized")
        
        # สร้าง gh-pages branch
        print("🌿 Creating gh-pages branch...")
        try:
            # ลบ gh-pages branch เก่าถ้ามี
            subprocess.run(["git", "branch", "-D", "gh-pages"], capture_output=True)
        except:
            pass
        
        # สร้าง gh-pages branch ใหม่
        subprocess.run(["git", "checkout", "-b", "gh-pages"], check=True, capture_output=True)
        print("✅ gh-pages branch created")
        
        # ลบไฟล์เก่าทั้งหมด (ยกเว้น .git และ online-ready)
        print("🧹 Cleaning up old files...")
        for item in project_root.iterdir():
            if item.name not in [".git", "online-ready", ".gitignore"]:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
        
        # คัดลอกไฟล์จาก online-ready ไปยัง root
        print("📁 Copying files from online-ready...")
        for item in online_ready.iterdir():
            if item.is_dir():
                shutil.copytree(item, project_root / item.name)
            else:
                shutil.copy2(item, project_root / item.name)
        print("✅ Files copied")
        
        # สร้าง .nojekyll file เพื่อปิด Jekyll processing
        (project_root / ".nojekyll").write_text("")
        print("✅ .nojekyll created")
        
        # สร้าง CNAME file (optional - แก้ตามต้องการ)
        # (project_root / "CNAME").write_text("your-domain.com")
        
        # Add และ commit files
        print("📝 Adding files to git...")
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        
        commit_message = f"Deploy car widgets to GitHub Pages - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True, capture_output=True)
        print("✅ Files committed")
        
        # ตรวจสอบ remote origin
        try:
            result = subprocess.run(["git", "remote", "get-url", "origin"], 
                                  capture_output=True, text=True, check=True)
            remote_url = result.stdout.strip()
            print(f"📡 Remote origin found: {remote_url}")
        except subprocess.CalledProcessError:
            print("⚠️ No remote origin found. Setting up...")
            # ถ้าไม่มี remote ให้ใช้ repo ปัจจุบัน
            repo_name = "recommended-car"
            remote_url = f"https://github.com/nblues/{repo_name}.git"
            subprocess.run(["git", "remote", "add", "origin", remote_url], 
                          capture_output=True)
            print(f"✅ Remote origin added: {remote_url}")
        
        # Push ไป GitHub
        print("🚀 Pushing to GitHub Pages...")
        try:
            subprocess.run(["git", "push", "-f", "origin", "gh-pages"], 
                          check=True, capture_output=True, timeout=60)
            print("✅ Successfully pushed to GitHub Pages!")
        except subprocess.TimeoutExpired:
            print("⚠️ Push timeout - but may still be successful")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Push failed: {e}")
            print("💡 You may need to:")
            print("   1. Set up GitHub authentication")
            print("   2. Push manually: git push -f origin gh-pages")
        
        # กลับไป main branch
        try:
            subprocess.run(["git", "checkout", "main"], capture_output=True)
        except:
            subprocess.run(["git", "checkout", "master"], capture_output=True)
        
        print("\n🎉 GITHUB PAGES DEPLOYMENT COMPLETED!")
        print("=" * 50)
        print("🌐 Your widgets should be live at:")
        print("   https://nblues.github.io/recommended-car/")
        print("")
        print("📋 What users can do:")
        print("   1. Visit the URL above")
        print("   2. Choose their preferred widget")
        print("   3. Click 'Copy Widget' button")
        print("   4. Paste in their website")
        print("   5. Customize API URLs")
        print("   6. Start getting more traffic!")
        print("")
        print("⏰ GitHub Pages may take 5-10 minutes to update")
        print("🔄 Check deployment status at:")
        print("   https://github.com/nblues/recommended-car/actions")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def create_github_pages_config():
    """สร้าง config สำหรับ GitHub Pages"""
    
    project_root = Path(__file__).parent
    
    # สร้าง GitHub Actions workflow
    workflows_dir = project_root / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_content = """name: Deploy Car Widgets to GitHub Pages

on:
  push:
    branches: [ gh-pages ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v4
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
    
    (workflows_dir / "deploy.yml").write_text(workflow_content)
    print("✅ GitHub Actions workflow created")

if __name__ == "__main__":
    # สร้าง GitHub Pages config
    create_github_pages_config()
    
    # Deploy ไป GitHub Pages
    success = deploy_to_github_pages()
    
    if success:
        print("\n🎊 SUCCESS! Car Widgets are now LIVE on GitHub Pages!")
        print("🔗 Share this URL: https://nblues.github.io/recommended-car/")
    else:
        print("\n❌ Deployment failed. Please check the errors above.")
