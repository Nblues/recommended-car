import os
import json
from pathlib import Path

CARS_JSON = "cars.json"
OUTPUT_DIR = "docs/car-detail/"
SITE_URL = "https://nblues.github.io/recommended-car/"
LINE_URL = "https://lin.ee/cJuakxZ"
FB_PAGE = "https://facebook.com/knrod2hand"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>{title} | รถมือสองเชียงใหม่ ครูหนึ่งรถสวย</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{img}">
  <meta property="og:url" content="{url}">
  <meta name="robots" content="index,follow">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="{url}">
  <script type="application/ld+json">{jsonld}</script>
</head>
<body>
  <h1>{title}</h1>
  <img src="{img}" alt="{title}" width="400"><br>
  <p><b>ยี่ห้อ:</b> {brand} <b>รุ่น:</b> {model} <b>ปี:</b> {year} <b>เลขไมล์:</b> {mileage} กม.</p>
  <p><b>ราคา:</b> ฿{price} <b>สถานะ:</b> {status} <b>เกียร์:</b> {gear} <b>สี:</b> {color}</p>
  <p>{desc}</p>
  <p>
    <a href="{LINE_URL}" target="_blank">สอบถามผ่าน LINE</a>
    <a href="{FB_PAGE}" target="_blank">ดูรถบน Facebook</a>
    <a href="{SITE_URL}all-cars-1" target="_blank">← กลับหน้ารวมรถ</a>
  </p>
</body>
</html>
"""

def make_jsonld(car, canonical):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Product",
        "name": car.get("title", ""),
        "image": [car.get("img", "")],
        "description": car.get("desc", ""),
        "brand": car.get("brand", ""),
        "model": car.get("model", ""),
        "color": car.get("color", ""),
        "sku": car.get("handle", ""),
        "offers": {
            "@type": "Offer",
            "priceCurrency": "THB",
            "price": car.get("price", "0"),
            "availability": "https://schema.org/InStock",
            "url": canonical
        }
    }, ensure_ascii=False)

def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    with open(CARS_JSON, "r", encoding="utf-8") as f:
        cars = json.load(f)
    for car in cars:
        filename = f"{car['handle']}.html"
        url = f"{SITE_URL}car-detail/{filename}"
        html = HTML_TEMPLATE.format(
            title=car.get("title",""),
            desc=car.get("desc",""),
            img=car.get("img",""),
            url=url,
            price="{:,}".format(int(car.get("price",0))),
            brand=car.get("brand",""),
            model=car.get("model",""),
            year=car.get("year",""),
            mileage=car.get("mileage",""),
            status=car.get("status",""),
            gear=car.get("gear",""),
            color=car.get("color",""),
            SITE_URL=SITE_URL,
            LINE_URL=LINE_URL,
            FB_PAGE=FB_PAGE,
            jsonld=make_jsonld(car, url)
        )
        outpath = os.path.join(OUTPUT_DIR, filename)
        with open(outpath, "w", encoding="utf-8") as outf:
            outf.write(html)
        print(f"✅ สร้าง {outpath}")

if __name__ == "__main__":
    main()