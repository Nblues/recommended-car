#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os

with open("cars.json", encoding="utf-8") as f:
    cars = json.load(f)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{images[0]}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{images[0]}">
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{title}",
  "image": {images},
  "description": "{desc}",
  "brand": {brand},
  "sku": "{sku}",
  "hasMerchantReturnPolicy": {{
    "@type": "MerchantReturnPolicy",
    "returnPolicyCategory": "https://schema.org/NoReturns"
  }},
  "shippingDetails": {{
    "@type": "OfferShippingDetails",
    "shippingRate": {{
      "@type": "MonetaryAmount",
      "value": 0,
      "currency": "{currency}"
    }},
    "deliveryTime": {{
      "@type": "ShippingDeliveryTime",
      "handlingTime": {{
        "@type": "QuantitativeValue",
        "minValue": 0,
        "maxValue": 1,
        "unitCode": "d"
      }},
      "transitTime": {{
        "@type": "QuantitativeValue",
        "minValue": 1,
        "maxValue": 5,
        "unitCode": "d"
      }}
    }}
  }},
  "offers": {{
    "@type": "Offer",
    "priceCurrency": "{currency}",
    "price": {price},
    "availability": "https://schema.org/InStock",
    "url": "{url}"
  }}
}}
  </script>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <nav><a href="../all-cars.html">← กลับหน้ารวมรถ</a></nav>
  <main class="car-detail">
    <h1>{title}</h1>
    <div class="gallery">
      {gallery_html}
    </div>
    <p>ราคา: {price_display} {currency}</p>
    <p>{full_desc}</p>
    <a class="btn" href="https://lin.ee/cJuakxZ" target="_blank">สอบถามผ่าน LINE</a>
    <a class="btn" href="{fb_link}" target="_blank">ดูรถบน Facebook</a>
  </main>
</body>
</html>
"""

out_dir = "docs/car-detail"
os.makedirs(out_dir, exist_ok=True)

for car in cars:
    slug = car.get("handle") or car.get("slug")
    title = car["title"]
    desc = car.get("short_desc", car.get("desc", ""))
    full_desc = car.get("full_desc", desc)
    currency = car.get("currency", "THB")
    price = car.get("price", 0)
    price_display = f"{price}"
    url = f"https://chiangraiusedcar.com/car-detail/{slug}.html"
    sku = car.get("sku", slug)

    images = [car.get("img")] if car.get("img") else car.get("images", [])
    gallery_html = "".join([f'<img src="{img}" alt="{title}">\n      ' for img in images])

    # brand = เอาจาก cars.json ถ้ามี ถ้าไม่มีก็เอาจากชื่อ title
    brand_name = car.get("brand", title.split()[0])
    brand = json.dumps({"@type": "Brand", "name": brand_name}, ensure_ascii=False)

    fb_link = car.get("fb_link", "https://facebook.com/ครูหนึ่งรถสวย")

    html = HTML_TEMPLATE.format(
        title=title,
        desc=desc,
        full_desc=full_desc,
        currency=currency,
        price=price,
        price_display=price_display,
        url=url,
        images=json.dumps(images, ensure_ascii=False),
        gallery_html=gallery_html,
        brand=brand,
        fb_link=fb_link,
        sku=sku
    )

    out_path = os.path.join(out_dir, f"{slug}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

print("✅ generate_car_detail.py: schema.org ครบทุกฟิลด์สำหรับ Google Merchant แล้ว")