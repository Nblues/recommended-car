#!/usr/bin/env python3
import json
import sys
import logging
import requests
from datetime import datetime
from pathlib import Path

# Configuration from existing scripts
SHOP = "www.kn-goodcar.com"
TOKEN = "bb70cb008199a94b83c98df0e45ada67"
API_URL = f"https://{SHOP}/api/2023-07/graphql.json"

HEADERS = {
    "X-Shopify-Storefront-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

# GraphQL query to get detailed product info (based on fetch_api_to_json.py)
QUERY = """
{
  products(first: 6, sortKey: CREATED_AT, reverse: true) {
    edges {
      node {
        title
        handle
        description
        vendor
        images(first: 5) { 
          edges { 
            node { 
              url 
            } 
          } 
        }
        variants(first: 1) {
          edges {
            node {
              price {
                amount
                currencyCode
              }
              sku
            }
          }
        }
      }
    }
  }
}
"""

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_cars_from_api():
    """Fetch latest 6 cars from Shopify API"""
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"query": QUERY}, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if "errors" in data:
            logging.error(f"GraphQL errors: {data['errors']}")
            return None
            
        products = data.get("data", {}).get("products", {}).get("edges", [])
        
        cars = []
        for item in products:
            prod = item["node"]
            images = [img["node"]["url"] for img in prod["images"]["edges"]]
            variant = prod["variants"]["edges"][0]["node"] if prod["variants"]["edges"] else {}
            price = float(variant["price"]["amount"]) if variant and variant.get("price") else 0
            currency = variant["price"]["currencyCode"] if variant and variant.get("price") else "THB"
            sku = variant.get("sku", "") if variant else ""
            
            cars.append({
                "title": prod["title"],
                "handle": prod["handle"],
                "desc": prod["description"] or "",
                "brand": prod["vendor"] or "",
                "images": images,
                "sku": sku,
                "price": price,
                "currency": currency,
                "link": f"https://www.kn-goodcar.com/car-detail/{prod['handle']}"
            })
        
        logging.info(f"Fetched {len(cars)} cars from API")
        return cars
        
    except Exception as e:
        logging.error(f"Failed to fetch from API: {e}")
        return None

def load_cars_from_json():
    """Load cars from local cars.json as fallback"""
    try:
        cars_file = Path("cars.json")
        if not cars_file.exists():
            logging.error("cars.json not found")
            return []
            
        with open(cars_file, "r", encoding="utf-8") as f:
            all_cars = json.load(f)
        
        # Get first 6 cars (assuming they're already sorted by newest)
        cars = all_cars[:6]
        logging.info(f"Loaded {len(cars)} cars from cars.json")
        return cars
        
    except Exception as e:
        logging.error(f"Failed to load cars.json: {e}")
        return []

def format_price(price, currency="THB"):
    """Format price with Thai currency"""
    if price > 0:
        if currency == "THB":
            return f"{price:,.0f} บาท"
        else:
            return f"{price:,.0f} {currency}"
    return "ราคาต่อรอง"

def get_car_image(car):
    """Get primary car image with fallback"""
    images = car.get("images", [])
    if images and len(images) > 0:
        return images[0]
    # Fallback image for cars without photos
    return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iI2Y1ZjVmNSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IiM5OTk5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7guKPguLnguJrguKPguJo8L3RleHQ+PC9zdmc+"

def generate_car_html(car):
    """Generate HTML for a single car card"""
    image_url = get_car_image(car)
    price_text = format_price(car.get("price", 0), car.get("currency", "THB"))
    
    # Truncate description for display
    desc = car.get("desc", "")
    if len(desc) > 150:
        desc = desc[:150] + "..."
    
    return f"""
      <div class="car-card">
        <img src="{image_url}" alt="{car.get('title', '')}" loading="lazy" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iI2Y1ZjVmNSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IiM5OTk5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7guKPguLnguJrguKPguJo8L3RleHQ+PC9zdmc+'">
        <div class="car-info">
          <h3 class="car-title">{car.get('title', '')}</h3>
          <div class="car-price">{price_text}</div>
          <p class="car-desc">{desc}</p>
          <a href="{car.get('link', '#')}" class="btn-detail" target="_blank">ดูรายละเอียด</a>
        </div>
      </div>"""

def generate_json_ld(cars):
    """Generate JSON-LD structured data for SEO"""
    current_time = datetime.now().isoformat()
    
    # WebPage Schema
    webpage_schema = {
        "@type": "WebPage",
        "@id": "https://nblues.github.io/recommended-car/mini-cars-static.html",
        "url": "https://nblues.github.io/recommended-car/mini-cars-static.html",
        "name": "รถมือสองเชียงใหม่ เข้าใหม่ 6 คันล่าสุด ฟรีดาวน์ | ครูหนึ่งรถสวย",
        "description": "รถบ้านเข้าใหม่ 6 คันล่าสุด รถมือสองเชียงใหม่ ฟรีดาวน์ ผ่อนถูก รถบ้านสวย ตรวจสอบได้จริงทุกคัน",
        "datePublished": current_time,
        "dateModified": current_time,
        "inLanguage": "th-TH"
    }
    
    # ItemList Schema for the 6 cars
    itemlist_items = []
    product_schemas = []
    
    for i, car in enumerate(cars, 1):
        image_url = get_car_image(car)
        
        # Item for ItemList
        itemlist_items.append({
            "@type": "ListItem",
            "position": i,
            "name": car.get("title", ""),
            "url": car.get("link", "")
        })
        
        # Individual Product Schema
        product_schema = {
            "@type": "Product",
            "@id": f"https://www.kn-goodcar.com/products/{car.get('handle', '')}",
            "name": car.get("title", ""),
            "description": car.get("desc", "")[:500],  # Limit description length
            "image": image_url,
            "url": car.get("link", ""),
            "brand": {
                "@type": "Brand",
                "name": car.get("brand", "ครูหนึ่งรถสวย")
            },
            "category": "รถยนต์มือสอง",
            "offers": {
                "@type": "Offer",
                "price": str(car.get("price", 0)),
                "priceCurrency": car.get("currency", "THB"),
                "availability": "https://schema.org/InStock",
                "seller": {
                    "@type": "Organization",
                    "name": "ครูหนึ่งรถสวย"
                }
            }
        }
        product_schemas.append(product_schema)
    
    itemlist_schema = {
        "@type": "ItemList",
        "name": "รถมือสองเชียงใหม่ เข้าใหม่ 6 คันล่าสุด",
        "description": "รถบ้านเข้าใหม่ล่าสุด รถมือสองเชียงใหม่ คุณภาพดี",
        "numberOfItems": len(cars),
        "itemListElement": itemlist_items
    }
    
    # Combine all schemas
    all_schemas = [webpage_schema, itemlist_schema] + product_schemas
    
    return {
        "@context": "https://schema.org",
        "@graph": all_schemas
    }

def generate_html(cars):
    """Generate complete HTML page with SEO"""
    
    # Get primary image for Open Graph
    og_image = get_car_image(cars[0]) if cars else "https://via.placeholder.com/1200x630/fa6400/ffffff?text=รถมือสองเชียงใหม่"
    
    # Generate car cards HTML
    car_cards = ""
    for car in cars:
        car_cards += generate_car_html(car)
    
    # Generate JSON-LD
    json_ld = generate_json_ld(cars)
    
    html_template = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- SEO Meta Tags -->
  <title>รถมือสองเชียงใหม่ เข้าใหม่ 6 คันล่าสุด ฟรีดาวน์ | ครูหนึ่งรถสวย</title>
  <meta name="description" content="รถบ้านเข้าใหม่ 6 คันล่าสุด รถมือสองเชียงใหม่ ฟรีดาวน์ ผ่อนถูก รถบ้านสวย ตรวจสอบได้จริงทุกคัน พร้อมรายละเอียด รูปภาพ สเปคครบ">
  <meta name="keywords" content="รถมือสอง, รถมือสองเชียงใหม่, รถบ้าน, ฟรีดาวน์, ผ่อนรถ, รถสวย, ครูหนึ่งรถสวย">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://nblues.github.io/recommended-car/mini-cars-static.html">
  
  <!-- Open Graph (Facebook) -->
  <meta property="og:title" content="รถมือสองเชียงใหม่ เข้าใหม่ 6 คันล่าสุด ฟรีดาวน์ | ครูหนึ่งรถสวย">
  <meta property="og:description" content="รถบ้านเข้าใหม่ 6 คันล่าสุด รถมือสองเชียงใหม่ ฟรีดาวน์ ผ่อนถูก รถบ้านสวย สเปคครบ เช็คเครดิตได้ทันที">
  <meta property="og:image" content="{og_image}">
  <meta property="og:url" content="https://nblues.github.io/recommended-car/mini-cars-static.html">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="ครูหนึ่งรถสวย รถมือสองเชียงใหม่">
  <meta property="og:locale" content="th_TH">
  
  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="รถมือสองเชียงใหม่ 6 คันล่าสุด ฟรีดาวน์ | ครูหนึ่งรถสวย">
  <meta name="twitter:description" content="รวมรถเข้าใหม่ 6 คัน รถบ้านเชียงใหม่ ฟรีดาวน์ ผ่อนถูก เช็คเครดิตไว รถสวยเกรด A ทุกคัน">
  <meta name="twitter:image" content="{og_image}">
  
  <!-- JSON-LD Structured Data -->
  <script type="application/ld+json">
{json.dumps(json_ld, ensure_ascii=False, indent=2)}
  </script>
  
  <!-- Inline CSS for standalone use -->
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    
    body {{
      font-family: 'Sarabun', 'Prompt', 'Helvetica Neue', Arial, sans-serif;
      background: linear-gradient(135deg, #fffaf6 0%, #fff5ee 100%);
      color: #2c2c2c;
      line-height: 1.6;
      min-height: 100vh;
    }}
    
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }}
    
    .header {{
      text-align: center;
      margin-bottom: 40px;
    }}
    
    .main-title {{
      font-size: 2.5em;
      color: #fa6400;
      margin-bottom: 10px;
      font-weight: 700;
      text-shadow: 2px 2px 4px rgba(250, 100, 0, 0.1);
    }}
    
    .subtitle {{
      font-size: 1.2em;
      color: #666;
      margin-bottom: 20px;
    }}
    
    .car-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 25px;
      margin-bottom: 40px;
    }}
    
    @media (min-width: 768px) {{
      .car-grid {{
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
      }}
    }}
    
    @media (max-width: 480px) {{
      .car-grid {{
        grid-template-columns: 1fr;
        gap: 20px;
      }}
      
      .main-title {{
        font-size: 1.8em;
      }}
    }}
    
    .car-card {{
      background: #ffffff;
      border-radius: 15px;
      box-shadow: 0 8px 25px rgba(250, 100, 0, 0.1);
      overflow: hidden;
      border: 2px solid #fff5ee;
      transition: all 0.3s ease;
      position: relative;
    }}
    
    .car-card:hover {{
      transform: translateY(-5px);
      box-shadow: 0 15px 35px rgba(250, 100, 0, 0.15);
      border-color: #fa6400;
    }}
    
    .car-card img {{
      width: 100%;
      height: 200px;
      object-fit: cover;
      border-bottom: 3px solid #fff5ee;
      transition: transform 0.3s ease;
    }}
    
    .car-card:hover img {{
      transform: scale(1.05);
    }}
    
    .car-info {{
      padding: 20px;
    }}
    
    .car-title {{
      font-size: 1.25em;
      font-weight: 700;
      margin-bottom: 10px;
      color: #fa6400;
      line-height: 1.3;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    
    .car-price {{
      color: #1b8801;
      font-weight: 700;
      font-size: 1.3em;
      margin-bottom: 12px;
      background: linear-gradient(135deg, #1b8801, #25a002);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}
    
    .car-desc {{
      font-size: 0.95em;
      margin: 12px 0 15px 0;
      color: #555;
      line-height: 1.5;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    
    .btn-detail {{
      display: block;
      text-align: center;
      background: linear-gradient(135deg, #fa6400, #ff7a1a);
      color: white;
      border-radius: 10px;
      text-decoration: none;
      font-weight: 600;
      padding: 12px 20px;
      margin-top: 15px;
      font-size: 1em;
      transition: all 0.3s ease;
      border: none;
      cursor: pointer;
    }}
    
    .btn-detail:hover {{
      background: linear-gradient(135deg, #e55a00, #fa6400);
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(250, 100, 0, 0.3);
    }}
    
    .see-all-container {{
      text-align: center;
      margin-top: 50px;
    }}
    
    .see-all-btn {{
      display: inline-block;
      background: linear-gradient(135deg, #015fa7, #1976d2);
      color: white;
      font-weight: 700;
      text-align: center;
      border-radius: 12px;
      padding: 15px 40px;
      font-size: 1.1em;
      text-decoration: none;
      transition: all 0.3s ease;
      box-shadow: 0 5px 20px rgba(1, 95, 167, 0.2);
    }}
    
    .see-all-btn:hover {{
      background: linear-gradient(135deg, #014a85, #015fa7);
      transform: translateY(-3px);
      box-shadow: 0 8px 25px rgba(1, 95, 167, 0.3);
    }}
    
    .footer-note {{
      text-align: center;
      margin-top: 30px;
      padding: 20px;
      background: rgba(250, 100, 0, 0.05);
      border-radius: 10px;
      color: #666;
      font-size: 0.9em;
    }}
    
    .loading-placeholder {{
      text-align: center;
      padding: 50px 20px;
      color: #999;
    }}
    
    /* Accessibility improvements */
    @media (prefers-reduced-motion: reduce) {{
      .car-card,
      .btn-detail,
      .see-all-btn {{
        transition: none;
      }}
      
      .car-card:hover {{
        transform: none;
      }}
      
      .car-card:hover img {{
        transform: none;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <header class="header">
      <h1 class="main-title">🚗 รถเข้าใหม่ 6 คันล่าสุด</h1>
      <p class="subtitle">รถมือสองเชียงใหม่ คุณภาพดี ฟรีดาวน์ ผ่อนถูก</p>
    </header>
    
    <main class="car-grid">
{car_cards}
    </main>
    
    <div class="see-all-container">
      <a class="see-all-btn" href="https://www.kn-goodcar.com/" target="_blank" rel="noopener">
        ดูรถทั้งหมด →
      </a>
    </div>
    
    <footer class="footer-note">
      <p>🌟 ครูหนึ่งรถสวย - รถมือสองเชียงใหม่ คุณภาพดี ราคาถูก ตรวจสอบได้จริง</p>
      <p>📞 ติดต่อสอบถาม หรือนัดชมรถได้ทันที</p>
    </footer>
  </div>
</body>
</html>"""
    
    return html_template

def main():
    """Main function to build the static HTML"""
    logging.info("Starting to build mini cars static HTML...")
    
    # Try to fetch from API first
    cars = fetch_cars_from_api()
    
    # Fallback to cars.json if API fails
    if not cars:
        logging.info("API failed, falling back to cars.json...")
        cars = load_cars_from_json()
    
    if not cars:
        logging.error("No cars data available from API or cars.json")
        sys.exit(1)
    
    # Ensure we have exactly 6 cars (or fewer if not available)
    cars = cars[:6]
    
    logging.info(f"Generating HTML for {len(cars)} cars...")
    
    # Generate HTML
    html_content = generate_html(cars)
    
    # Ensure docs directory exists
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # Save HTML file
    output_file = docs_dir / "mini-cars-static.html"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        logging.info(f"✅ Successfully generated {output_file}")
        logging.info(f"📁 File size: {output_file.stat().st_size / 1024:.1f} KB")
        
        # Display summary
        print(f"\n🎉 Mini Cars Static HTML Generated Successfully!")
        print(f"📂 Output: {output_file}")
        print(f"🚗 Cars included: {len(cars)}")
        print(f"📏 File size: {output_file.stat().st_size / 1024:.1f} KB")
        print(f"🔗 Ready for GoDaddy Website Builder embedding")
        
    except Exception as e:
        logging.error(f"Failed to save HTML file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()