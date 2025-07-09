import json
import os

with open('cars.json', encoding='utf-8') as f:
    cars = json.load(f)

os.makedirs('docs/car-detail', exist_ok=True)

TEMPLATE = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>{title} | รถมือสองคุณภาพดี</title>
  <meta name="description" content="ขาย {title} {desc}">
  <link rel="canonical" href="https://nblues.github.io/recommended-car/car-detail/{handle}.html">
  <script type="application/ld+json">
  {{
    "@context":"https://schema.org",
    "@type":"Product",
    "name":"{title}",
    "description":"{desc}",
    "image":"{img}",
    "offers": {{
      "@type":"Offer",
      "price":"{price}",
      "priceCurrency":"THB",
      "availability":"https://schema.org/InStock"
    }}
  }}
  </script>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <div class="car-detail">
    <img src="{img}" alt="{title}" style="max-width:400px;">
    <h1>{title}</h1>
    <div class="car-desc">{desc}</div>
    <div class="car-price">฿{price:,}</div>
    <a href="../index.html">← กลับหน้ารวม</a>
  </div>
</body>
</html>
"""

for car in cars:
    html = TEMPLATE.format(**car)
    fname = f'docs/car-detail/{car["handle"]}.html'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)

print(f"Generate {len(cars)} car-detail pages DONE.")