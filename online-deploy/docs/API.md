# 🔗 API Documentation

## Required API Format

Widgets ต้องการ JSON format ดังนี้:

### 1. Shopify Format (Recommended)
```json
{
  "products": [
    {
      "id": 1,
      "title": "ชื่อรถ",
      "handle": "url-slug",
      "price": 500000,
      "images": [
        "https://example.com/image.jpg"
      ],
      "body_html": "รายละเอียดรถ",
      "created_at": "2024-01-01T10:00:00Z",
      "variants": [
        {
          "price": 500000
        }
      ]
    }
  ]
}
```

### 2. Simple Cars Format
```json
{
  "cars": [
    {
      "id": 1,
      "title": "ชื่อรถ",
      "price": 500000,
      "image": "https://example.com/image.jpg",
      "description": "รายละเอียดรถ"
    }
  ]
}
```

### 3. Custom Format
Widget จะ auto-detect format อัตโนมัติ

## Sample API Endpoints

- `/api/cars.json` - ข้อมูลรถทั้งหมด
- `/api/chiang-mai-cars.json` - ข้อมูลรถเชียงใหม่

## CORS Headers Required

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET
Access-Control-Allow-Headers: Content-Type
```

## Error Handling

Widget จะแสดง error message หากไม่สามารถโหลด API ได้
