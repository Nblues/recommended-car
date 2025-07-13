#!/usr/bin/env python3
"""
ระบบทำความสะอาดไฟล์และแคช (อัปเดท)
- ลบไฟล์ HTML ที่ไม่ได้อยู่ใน cars.json
- ล้างแคชทุกประเภท
- ทำความสะอาดไฟล์ขยะ
- ระบบ Auto Cleanup
"""
import os
import json
import shutil
import tempfile
import glob
from pathlib import Path
from auto_cleanup_utils import auto_cleanup, with_auto_cleanup

def load_cars_data():
    """โหลดข้อมูลรถจาก cars.json"""
    try:
        with open('cars.json', 'r', encoding='utf-8') as f:
            cars = json.load(f)
        return cars
    except FileNotFoundError:
        print("❌ ไม่พบไฟล์ cars.json")
        return []

def get_valid_handles():
    """ดึง handle ของรถที่ถูกต้องจาก cars.json"""
    cars = load_cars_data()
    valid_handles = set()
    
    for car in cars:
        handle = car.get('handle', '')
        if handle:
            valid_handles.add(f"{handle}.html")
    
    return valid_handles

def cleanup_html_files():
    """ลบไฟล์ HTML ที่ไม่ได้อยู่ใน cars.json"""
    car_detail_dir = Path('docs/car-detail')
    if not car_detail_dir.exists():
        print("❌ ไม่พบโฟลเดอร์ docs/car-detail")
        return
    
    valid_handles = get_valid_handles()
    print(f"📋 รถที่ถูกต้องใน cars.json: {len(valid_handles)} คัน")
    
    # ดึงไฟล์ HTML ทั้งหมด
    html_files = list(car_detail_dir.glob('*.html'))
    print(f"📁 ไฟล์ HTML ทั้งหมด: {len(html_files)} ไฟล์")
    
    deleted_files = []
    for html_file in html_files:
        if html_file.name not in valid_handles:
            try:
                html_file.unlink()  # ลบไฟล์
                deleted_files.append(html_file.name)
                print(f"🗑️ ลบ: {html_file.name}")
            except Exception as e:
                print(f"❌ ไม่สามารถลบ {html_file.name}: {e}")
    
    print(f"\n✅ ลบไฟล์เรียบร้อย: {len(deleted_files)} ไฟล์")
    return deleted_files

def clear_python_cache():
    """ล้างแคช Python"""
    print("\n🧹 ล้างแคช Python...")
    
    # ลบโฟลเดอร์ __pycache__
    for pycache_dir in glob.glob('**/__pycache__', recursive=True):
        try:
            shutil.rmtree(pycache_dir)
            print(f"🗑️ ลบ __pycache__: {pycache_dir}")
        except Exception as e:
            print(f"❌ ไม่สามารถลบ {pycache_dir}: {e}")
    
    # ลบไฟล์ .pyc
    for pyc_file in glob.glob('**/*.pyc', recursive=True):
        try:
            os.remove(pyc_file)
            print(f"🗑️ ลบ .pyc: {pyc_file}")
        except Exception as e:
            print(f"❌ ไม่สามารถลบ {pyc_file}: {e}")

def clear_temp_files():
    """ล้างไฟล์ชั่วคราว"""
    print("\n🧹 ล้างไฟล์ชั่วคราว...")
    
    temp_patterns = [
        '**/*.tmp',
        '**/*.temp',
        '**/*~',
        '**/Thumbs.db',
        '**/.DS_Store',
        '**/desktop.ini'
    ]
    
    for pattern in temp_patterns:
        for temp_file in glob.glob(pattern, recursive=True):
            try:
                os.remove(temp_file)
                print(f"🗑️ ลบ temp: {temp_file}")
            except Exception as e:
                print(f"❌ ไม่สามารถลบ {temp_file}: {e}")

def clear_vscode_cache():
    """ล้างแคช VS Code (ถ้าเป็นไปได้)"""
    print("\n🧹 ล้างแคช VS Code...")
    
    vscode_dirs = [
        '.vscode/.ropeproject',
        '.vscode/settings.json.backup',
        'node_modules/.cache',
        '.next/cache',
        '.cache'
    ]
    
    for vscode_dir in vscode_dirs:
        if os.path.exists(vscode_dir):
            try:
                if os.path.isfile(vscode_dir):
                    os.remove(vscode_dir)
                else:
                    shutil.rmtree(vscode_dir)
                print(f"🗑️ ลบ VS Code cache: {vscode_dir}")
            except Exception as e:
                print(f"❌ ไม่สามารถลบ {vscode_dir}: {e}")

def force_file_deletion(filepath):
    """บังคับลบไฟล์แม้จะถูกล็อค"""
    try:
        # ลองลบปกติก่อน
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except:
        pass
    
    try:
        # ใช้ Path.unlink() สำหรับการลบที่แข็งแกร่งกว่า
        Path(filepath).unlink(missing_ok=True)
        return True
    except:
        pass
    
    return False

@with_auto_cleanup
def main():
    """ฟังก์ชันหลัก - รวมระบบ Auto Cleanup"""
    print("🚀 เริ่มระบบทำความสะอาด (พร้อม Auto Cleanup)...")
    print("=" * 50)
    
    # 1. ลบไฟล์ HTML ที่ไม่ต้องการ
    deleted_files = cleanup_html_files()
    
    # 2. บังคับลบไฟล์ที่อาจติดแคช
    problem_files = [
        'docs/car-detail/bmw-320d-2019.html'
    ]
    
    for file_path in problem_files:
        if force_file_deletion(file_path):
            print(f"💪 บังคับลบ: {file_path}")
    
    # 3. ล้างแคชต่างๆ
    clear_python_cache()
    clear_temp_files()
    clear_vscode_cache()
    
    # 4. สรุปผล
    print("\n" + "=" * 50)
    print("✅ ทำความสะอาดเรียบร้อยแล้ว!")
    
    # ตรวจสอบสถานะปัจจุบัน
    car_detail_dir = Path('docs/car-detail')
    if car_detail_dir.exists():
        remaining_html = len(list(car_detail_dir.glob('*.html')))
        valid_cars = len(get_valid_handles())
        print(f"📊 ไฟล์ HTML ที่เหลือ: {remaining_html}")
        print(f"📊 รถในข้อมูล: {valid_cars}")
        
        if remaining_html == valid_cars:
            print("🎉 จำนวนไฟล์ตรงกับข้อมูลแล้ว!")
        else:
            print(f"⚠️ ยังมีไฟล์เพิ่ม: {remaining_html - valid_cars} ไฟล์")
    
    print("\n💡 หากยังเห็นไฟล์เก่าใน VS Code:")
    print("   1. กด Ctrl+Shift+P")
    print("   2. เลือก 'Developer: Reload Window'")
    print("   3. หรือรัน auto_cleanup.bat")

if __name__ == "__main__":
    main()
