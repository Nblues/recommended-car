# 🚗 การแมพข้อมูลรถยนต์ - โปรเจคครูหนึ่งรถสวย

## 📋 สถานะการซิงค์ข้อมูล ✅

**อัปเดตล่าสุด**: 14 ธันวาคม 2024  
**สถานะ**: ✅ ข้อมูลซิงค์สมบูรณ์แล้ว

## 📁 ไฟล์ที่ได้รับการอัปเดต

### 1. `car-widget-fixed.html` - Widget หลัก
- ✅ **API Integration**: ดึงข้อมูลสดจาก Shopify GraphQL
- ✅ **Fallback Data**: ข้อมูลสำรองตรงกับไฟล์อื่น 
- ✅ **JSON-LD Schema**: อัปเดตให้ตรงกับข้อมูลทั้ง 6 คัน
- ✅ **Auto-refresh**: รีเฟรชทุก 5 นาที + เมื่อกลับมาที่หน้า

### 2. `all-cars.html` - หน้ารวมรถทั้งหมด
- ✅ **Car Data**: ข้อมูลรถ 6 คันเหมือนกับ widget
- ✅ **Filter System**: กรองตามยี่ห้อ ปี ราคา
- ✅ **Links**: ลิงค์ไปยัง car-detail.html ด้วย handle ที่ถูกต้อง

### 3. `car-detail.html` - หน้ารายละเอียดรถ
- ✅ **Car Database**: ข้อมูลครบถ้วนทั้ง 6 คัน
- ✅ **Dynamic Loading**: รับ handle จาก URL parameter
- ✅ **Specs Data**: ข้อมูลสเปคละเอียดแต่ละคัน

## 🚙 รถทั้ง 6 คันที่ซิงค์แล้ว

| รถ | ราคา | Handle | สถานะ |
|---|---|---|---|
| Toyota Estima Hybrid 2007 | ฿419,000 | `toyota-eztima-hybrid...` | ✅ |
| Ford Ranger WildTrak 2020 | ฿559,000 | `ford-ranger-4dr-dcab...` | ✅ |
| Toyota C-HR Hybrid 2019 | ฿649,000 | `toyota-chr-1-8-hv...` | ✅ |
| Hyundai H-1 Elite 2022 | ฿1,169,000 | `hyundai-h-1-elite...` | ✅ |
| Isuzu D-MAX Hi-Lander 2011 | ฿289,000 | `d-max-hi-lander...` | ✅ |
| Ford Ranger Open Cab 2018 | ฿369,000 | `ford-ranger-2-2-cab...` | ✅ |

## 🔄 ระบบ API และ Fallback

### Shopify API
- **Domain**: kn-goodcar.com
- **Access Token**: bb70cb008199a94b83c98df0e45ada67
- **Query**: ดึงรถ 6 คันล่าสุดด้วย GraphQL

### Auto-Update System
- รีเฟรชข้อมูลทุก 5 นาที
- รีเฟรชเมื่อผู้ใช้กลับมาที่หน้า
- แสดง loading state ขณะโหลด
- ใช้ fallback data เมื่อ API ล้มเหลว

## 🔗 การลิงค์ระหว่างหน้า

```
car-widget-fixed.html → ดูรายละเอียด → car-detail.html?handle=xxx
all-cars.html → ดูรายละเอียด → car-detail.html?handle=xxx
car-detail.html ← รับ handle parameter และแสดงข้อมูล
```

## 📊 Schema.org SEO

ทุกไฟล์มี JSON-LD Schema ที่สอดคล้องกัน:
- Product Schema สำหรับแต่ละคัน
- Organization Schema สำหรับครูหนึ่งรถสวย
- BreadcrumbList สำหรับ SEO navigation

## 🛠️ การพัฒนาต่อ

### หากต้องการเพิ่มรถใหม่:
1. อัปเดตใน `data-mapping.json` ก่อน
2. อัปเดตในไฟล์ทั้ง 3 ให้ตรงกัน:
   - `car-widget-fixed.html` (fallback data)
   - `all-cars.html` (allCars array)
   - `car-detail.html` (carsData object)

### หากต้องการแก้ไขข้อมูล:
1. ตรวจสอบใน `data-mapping.json`
2. แก้ไขให้ตรงกันทุกไฟล์
3. อัปเดต JSON-LD Schema

## ✅ Checklist การตรวจสอบ

- [x] ข้อมูลรถทั้ง 6 คันตรงกันทุกไฟล์
- [x] Handle/ID เหมือนกันทุกที่
- [x] ราคาเหมือนกันทุกที่  
- [x] รูปภาพ URL เหมือนกันทุกที่
- [x] คำอธิบายเหมือนกันทุกที่
- [x] ลิงค์ car-detail.html ทำงานถูกต้อง
- [x] API fallback ทำงานถูกต้อง
- [x] JSON-LD Schema ถูกต้อง
- [x] Auto-refresh ทำงานถูกต้อง

---

**💡 สำคัญ**: ข้อมูลทั้งหมดซิงค์กันแล้ว ระบบพร้อมใช้งาน! 🎯
