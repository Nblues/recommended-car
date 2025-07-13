@echo off
REM ระบบทำความสะอาดอัตโนมัติสำหรับ Windows
REM รันทุกครั้งหลังจากลบไฟล์เพื่อป้องกันปัญหาแคช

echo 🚀 เริ่มระบบทำความสะอาดอัตโนมัติ...
echo.

REM ลบแคช Python
echo 🧹 ลบแคช Python...
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul

REM ลบไฟล์ชั่วคราว
echo 🧹 ลบไฟล์ชั่วคราว...
del /s /q *.tmp 2>nul
del /s /q *.temp 2>nul
del /s /q *~ 2>nul
del /s /q Thumbs.db 2>nul
del /s /q desktop.ini 2>nul

REM รีเฟรชระบบไฟล์
echo 🔄 รีเฟรชระบบไฟล์...
taskkill /f /im explorer.exe >nul 2>&1
start explorer.exe

REM รัน cleanup_system.py หากมี
if exist cleanup_system.py (
    echo 🔧 รันระบบทำความสะอาดหลัก...
    python cleanup_system.py
)

echo.
echo ✅ ทำความสะอาดเรียบร้อยแล้ว!
echo 💡 หากยังเห็นไฟล์เก่าใน VS Code ให้กด Ctrl+Shift+P แล้วเลือก "Developer: Reload Window"
pause
