"""
Auto Cleanup Hook
เพิ่มฟังก์ชันนี้ในสคริปต์ Python ที่มีการลบไฟล์
เพื่อทำความสะอาดอัตโนมัติหลังจากการดำเนินการ
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

def auto_cleanup():
    """ฟังก์ชันทำความสะอาดอัตโนมัติ"""
    print("\n🧹 เริ่มทำความสะอาดอัตโนมัติ...")
    
    # ลบแคช Python
    cleanup_python_cache()
    
    # ลบไฟล์ชั่วคราว
    cleanup_temp_files()
    
    # บังคับ garbage collection
    import gc
    gc.collect()
    
    print("✅ ทำความสะอาดอัตโนมัติเรียบร้อย!")

def cleanup_python_cache():
    """ลบแคช Python"""
    try:
        # ลบ __pycache__ directories
        for root, dirs, files in os.walk('.'):
            for dirname in dirs:
                if dirname == '__pycache__':
                    cache_path = os.path.join(root, dirname)
                    shutil.rmtree(cache_path, ignore_errors=True)
                    print(f"🗑️ ลบ cache: {cache_path}")
        
        # ลบ .pyc files
        for root, dirs, files in os.walk('.'):
            for filename in files:
                if filename.endswith('.pyc'):
                    pyc_path = os.path.join(root, filename)
                    try:
                        os.remove(pyc_path)
                        print(f"🗑️ ลบ .pyc: {pyc_path}")
                    except:
                        pass
    except Exception as e:
        print(f"⚠️ การลบแคช Python มีปัญหา: {e}")

def cleanup_temp_files():
    """ลบไฟล์ชั่วคราว"""
    temp_patterns = ['*.tmp', '*.temp', '*~', 'Thumbs.db', '.DS_Store', 'desktop.ini']
    
    for pattern in temp_patterns:
        for temp_file in Path('.').rglob(pattern):
            try:
                temp_file.unlink()
                print(f"🗑️ ลบ temp: {temp_file}")
            except:
                pass

def force_vscode_refresh():
    """บังคับให้ VS Code รีเฟรช (ถ้าเป็นไปได้)"""
    try:
        # สร้างไฟล์ trigger เพื่อบอก VS Code ให้รีเฟรช
        trigger_file = Path('.vscode_refresh_trigger')
        trigger_file.touch()
        trigger_file.unlink(missing_ok=True)
        print("🔄 ส่งสัญญาณรีเฟรชไปยัง VS Code")
    except:
        pass

# Decorator สำหรับใช้กับฟังก์ชันที่มีการลบไฟล์
def with_auto_cleanup(func):
    """Decorator ที่เพิ่มการทำความสะอาดอัตโนมัติ"""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            auto_cleanup()
            return result
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            auto_cleanup()  # ทำความสะอาดแม้เกิดข้อผิดพลาด
            raise
    return wrapper

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    print("🧪 ทดสอบระบบ Auto Cleanup...")
    auto_cleanup()
