# Python SSR Service Installation Guide
## Ultimate Windows Service Setup 2025

เครื่องมือสำหรับติดตั้งและจัดการ Python SSR เป็น Windows Service อย่างสมบูรณ์

## 📦 ไฟล์ที่ได้รับ:

### 1. **install-service.bat** - ติดตั้งพื้นฐาน
```batch
# รันด้วยสิทธิ์ Administrator
.\install-service.bat
```

### 2. **install-service.ps1** - ติดตั้งขั้นสูง (PowerShell)
```powershell
# Auto-elevate และ Advanced options
.\install-service.ps1
.\install-service.ps1 -Force -Interval 15
```

### 3. **manage-service.bat** - จัดการ Service
```batch
# เมนูจัดการ Service แบบ Interactive
.\manage-service.bat
```

## 🚀 วิธีติดตั้ง:

### **Option 1: ติดตั้งด้วย PowerShell (แนะนำ)**
```powershell
# 1. เปิด PowerShell as Administrator
# 2. รันคำสั่ง:
.\install-service.ps1

# หรือ Custom interval:
.\install-service.ps1 -Interval 15 -Force
```

### **Option 2: ติดตั้งด้วย Batch File**
```batch
# 1. เปิด Command Prompt as Administrator  
# 2. รันคำสั่ง:
.\install-service.bat
```

### **Option 3: จัดการด้วย Management Script**
```batch
# รันเมนูจัดการ (ไม่ต้อง Admin สำหรับดูสถานะ):
.\manage-service.bat
```

## 🎯 ฟีเจอร์ของ Service:

### ✅ **Auto-Update System**
- อัพเดท HTML จาก API ทุก 30 นาที (หรือตามที่ตั้งค่า)
- รันในพื้นหลังแบบอัตโนมัติ
- เริ่มต้นพร้อม Windows

### ✅ **Smart Installation**
- ตรวจสอบสิทธิ์ Administrator อัตโนมัติ
- ลบ Service เก่าก่อนติดตั้งใหม่
- Error handling ครบถ้วน

### ✅ **Easy Management**
- Start/Stop/Restart Service
- ดูสถานะแบบ Real-time
- ลิงก์ไป Event Viewer
- ทดสอบ Python Script

## 📋 คำสั่งจัดการ Service:

### **Basic Commands:**
```batch
# เริ่ม Service
sc start PythonSSRService

# หยุด Service  
sc stop PythonSSRService

# ดูสถานะ
sc query PythonSSRService

# ลบ Service
sc delete PythonSSRService
```

### **PowerShell Commands:**
```powershell
# เริ่ม Service
Start-Service PythonSSRService

# หยุด Service
Stop-Service PythonSSRService

# ดูสถานะ
Get-Service PythonSSRService

# ลบ Service (PS 6+)
Remove-Service PythonSSRService
```

## 🔧 การแก้ไขปัญหา:

### **❌ "Access Denied"**
```
🔧 วิธีแก้:
1. เปิด PowerShell/CMD as Administrator
2. คลิกขวาที่ PowerShell → "Run as Administrator"
```

### **❌ "Service Failed to Start"**
```
🔧 วิธีแก้:
1. ตรวจสอบ Python path: where python
2. ทดสอบ script: python python_ssr_generator.py --help
3. ดู Event Viewer: eventvwr.exe
```

### **❌ "Python Script Not Found"**
```
🔧 วิธีแก้:
1. ตรวจสอบไฟล์อยู่ในโฟลเดอร์เดียวกัน
2. รัน install-service จากโฟลเดอร์ที่ถูกต้อง
```

## 📊 สถานะ Service:

### **🟢 RUNNING** - ทำงานปกติ
- HTML จะ update ทุก 30 นาที
- ไฟล์ใหม่จะปรากฏใน docs/

### **🔴 STOPPED** - หยุดทำงาน  
- ไม่มีการ update อัตโนมัติ
- ต้อง start ใหม่

### **❌ NOT INSTALLED** - ยังไม่ได้ติดตั้ง
- รันคำสั่งติดตั้งก่อน

## 🎉 ผลลัพธ์ที่ได้:

### ✅ **Auto-Generated Files:**
- `docs/index.html` - หน้าหลักล่าสุด
- `docs/index-ssr-YYYYMMDD-HHMM.html` - ไฟล์ Backup
- อัพเดทข้อมูลรถใหม่อัตโนมัติ

### ✅ **Service Benefits:**
- 🔄 อัพเดทตลอด 24/7
- 🚀 เริ่มต้นพร้อม Windows  
- 📊 จัดการง่ายผ่าน GUI
- 🔍 Logging ครบถ้วน

## 💡 Tips:

1. **ใช้ PowerShell Installer** - มีฟีเจอร์มากกว่า
2. **ตั้ง Interval สั้น** สำหรับทดสอบ (-Interval 5)
3. **ใช้ Management Script** - จัดการง่าย
4. **ตรวจ Event Viewer** - ถ้ามีปัญหา

---

**🎯 ตอนนี้ Python SSR Service พร้อมใช้งานแล้ว!**
**รันคำสั่งติดตั้งและเว็บไซต์จะอัพเดทอัตโนมัติตลอดเวลา! 🚀**
