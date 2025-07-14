# 🚀 GoDaddy Integration - READY TO USE PACKAGE

## 📁 ไฟล์ทั้งหมดที่คุณได้รับ
```
📦 GoDaddy Integration Package
├── 🛠️ Windows Service Setup
│   ├── install-service.bat         # ติดตั้ง Windows Service
│   ├── install-service.ps1         # PowerShell version (advanced)
│   └── manage-service.bat          # จัดการ Service
│
├── 🌐 GoDaddy Integration Core  
│   ├── godaddy_auto_update.php     # PHP Script สำหรับ Shared Hosting
│   ├── godaddy_ftp_sync.py         # Python FTP Sync Tool
│   ├── godaddy_widget.html         # Website Builder Widget
│   └── godaddy_widget_ready.html   # ✨ READY TO USE Widget
│
├── ⚙️ Configuration Files
│   ├── godaddy_config.ini          # Config Template  
│   └── godaddy_config_ready.ini    # ✨ READY TO USE Config
│
└── 📚 Documentation
    ├── GODADDY-INTEGRATION-GUIDE.md
    ├── HOW-TO-USE-WITH-GODADDY.md
    └── godaddy_deployment_example.txt
```

## 🎯 วิธีใช้งาน 3 ขั้นตอน (READY TO USE)

### 1️⃣ แก้ไข Config File
```bash
# เปิดไฟล์ godaddy_config_ready.ini
# แก้ไขข้อมูลเหล่านี้ให้เป็นของคุณ:

[godaddy]
domain = your-domain.com           # 🔥 แก้เป็นโดเมนจริง
ftp_host = ftp.your-domain.com     # 🔥 แก้เป็น FTP Host จริง
ftp_user = your-username           # 🔥 แก้เป็น Username จริง
ftp_pass = your-password           # 🔥 แก้เป็น Password จริง
```

### 2️⃣ เลือกวิธีการ Deploy
#### 🅰️ Shared Hosting (แนะนำ)
```bash
1. Upload godaddy_auto_update.php ไปโฟลเดอร์ root
2. ตั้ง Cron Job: php godaddy_auto_update.php
3. เสร็จแล้ว! เว็บจะอัพเดทเอง
```

#### 🅱️ Website Builder Widget  
```bash
1. เปิด godaddy_widget_ready.html
2. แก้ URLs ในบรรทัด 166-168
3. Copy โค้ดไปใส่ HTML Widget
4. Publish เสร็จแล้ว!
```

#### 🅲️ FTP Auto-Sync
```bash
1. แก้ไข godaddy_config_ready.ini
2. รัน: python godaddy_ftp_sync.py
3. ตั้ง Windows Service อัตโนมัติ
```

### 3️⃣ Test & Deploy
```bash
# Test FTP Connection
python -c "import ftplib; ftp=ftplib.FTP('ftp.your-domain.com'); ftp.login('user','pass'); print('✅ Connected')"

# Test API
curl https://your-domain.com/cars.json

# Deploy
python godaddy_ftp_sync.py
```

## 🔥 Quick Start Commands

### Windows Service (Auto-Deploy)
```powershell
# ติดตั้ง Service
.\install-service.bat

# จัดการ Service  
.\manage-service.bat

# ดู Log
Get-Content C:\CarData\logs\service.log -Tail 50
```

### FTP Sync (Manual)
```bash
# Sync ครั้งเดียว
python godaddy_ftp_sync.py

# Test Config
python -c "from godaddy_ftp_sync import test_connection; test_connection()"
```

### PHP Auto-Update (Shared Hosting)
```bash
# Upload to GoDaddy
- Upload godaddy_auto_update.php
- Set Cron: 0 */6 * * * php godaddy_auto_update.php
- URL: https://your-domain.com/godaddy_auto_update.php
```

## 📋 Checklist ก่อนใช้งาน

### ✅ ข้อมูล GoDaddy ที่ต้องมี
- [ ] Domain Name (เช่น krunung-carshop.com)
- [ ] FTP Host (เช่น ftp.krunung-carshop.com)  
- [ ] FTP Username
- [ ] FTP Password
- [ ] Hosting Type (Shared/VPS/Website Builder)

### ✅ ไฟล์ที่ต้องแก้ไข
- [ ] godaddy_config_ready.ini (FTP credentials)
- [ ] godaddy_widget_ready.html (URLs in line 166-168)
- [ ] godaddy_auto_update.php (domain in line 15)

### ✅ Test ก่อนใช้งาน
- [ ] Test FTP connection
- [ ] Test API endpoint (cars.json)
- [ ] Test Widget display
- [ ] Test auto-update schedule

## 🎛️ กำหนดการอัพเดท

### Windows Service
```ini
# ใน install-service.ps1
$IntervalMinutes = 30  # อัพเดททุก 30 นาที
```

### PHP Cron Job
```bash
# ทุก 6 ชั่วโมง
0 */6 * * * php godaddy_auto_update.php

# ทุก 30 นาที  
*/30 * * * * php godaddy_auto_update.php
```

### Widget Auto-Refresh
```javascript
// ใน godaddy_widget_ready.html
setInterval(() => {
    this.loadCars();
}, 30 * 60 * 1000); // 30 minutes
```

## 🐛 Troubleshooting

### FTP Connection Issues
```bash
# Test FTP manually
ftp ftp.your-domain.com
# Enter username/password

# Check Python FTP
python -c "
import ftplib
try:
    ftp = ftplib.FTP('ftp.your-domain.com')
    ftp.login('username', 'password')
    print('✅ FTP OK')
except Exception as e:
    print('❌ FTP Error:', e)
"
```

### API Issues
```bash
# Check API response
curl -s https://your-domain.com/cars.json | head -5

# Check file permissions
ls -la cars.json
```

### Widget Issues
```javascript
// Debug in browser console
GoDaddyCarDebug.testAPI()
GoDaddyCarDebug.reload()
```

## 📞 Support URLs

### ดู Log Files
- Service Log: `C:\CarData\logs\service.log`
- FTP Log: `C:\CarData\logs\ftp_sync.log`  
- PHP Log: Check GoDaddy cPanel Error Logs

### ดู Status
- Service Status: `sc query CarDataSyncService`
- FTP Test: `python godaddy_ftp_sync.py --test`
- Widget Test: Open browser console

## 🎉 เสร็จแล้ว!

หากทำตามขั้นตอนเหล่านี้ คุณจะได้:

✅ **Windows Service** ที่อัพเดทข้อมูลอัตโนมัติ  
✅ **GoDaddy Integration** ที่ sync ไฟล์ไปเซิร์ฟเวอร์  
✅ **Widget** ที่แสดงรถในเว็บไซต์  
✅ **PHP Auto-Update** ที่ทำงานบน Shared Hosting  
✅ **Complete Documentation** ครบทุกการใช้งาน

---
<small>📅 Created: 2025 | 🚀 Ready to Deploy | 🔧 Support: Check documentation files</small>
