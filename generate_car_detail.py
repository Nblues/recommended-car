import json, os

with open('cars.json', encoding='utf-8') as f:
    cars = json.load(f)
os.makedirs('docs/car-detail', exist_ok=True)
TEMPLATE = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>{title} | รถมือสองเชียงใหม่ ฟรีดาวน์</title>
  <meta name="description" content="{desc} ฟรีดาวน์ เชียงใหม่">
  <link rel="canonical" href="https://chiangraiusedcar.com/car-detail/{handle}.html">
  <meta property="og:title" content="{title} | รถมือสองเชียงใหม่ ฟรีดาวน์">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{img}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://chiangraiusedcar.com/car-detail/{handle}.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title} | รถมือสองเชียงใหม่">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{img}">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "{title}",
    "description": "{desc}",
    "image": "{img}",
    "brand": "{{'@type':'Brand','name':'{brand}'}}",
    "model": "{{'@type':'ProductModel','name':'{model}'}}",
    "offers": {{
      "@type": "Offer",
      "priceCurrency": "THB",
      "price": "{price}",
      "availability": "https://schema.org/InStock",
      "url": "https://chiangraiusedcar.com/car-detail/{handle}.html"
    }}
  }}
  </script>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <div class="car-detail">
    <img src="{img}" alt="{title}" loading="lazy" style="max-width:100%;border-radius:16px;box-shadow:0 4px 24px #0002" onerror="this.onerror=null;this.src='https://dummyimage.com/600x400/eeeeee/cccccc&text=No+Image';">
    <h1>{title}</h1>
    <div class="car-desc">{desc}</div>
    <div class="car-price">฿{price}</div>
    <a href="../index.html" style="display:inline-block;margin:16px 0 0;">← กลับหน้ารวมรถ</a>
  </div>
</body>
</html>
"""
for car in cars:
    # Convert price to int for formatting
    car_copy = car.copy()
    car_copy['price'] = int(car['price'])
    html = TEMPLATE.format(**car_copy)
    with open(f'docs/car-detail/{car["handle"]}.html', 'w', encoding='utf-8') as f:
        f.write(html)
print("Generate car-detail pages DONE.")