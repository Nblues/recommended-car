import sys
import logging
import requests
import xml.etree.ElementTree as ET
import json

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

API_URL = "https://www.kn-goodcar.com/api/2023-07/graphql.json"
HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Storefront-Access-Token": "bb70cb008199a94b83c98df0e45ada67"
}
QUERY = '''
query Products($first: Int!) {
  products(first: $first, sortKey: CREATED_AT, reverse: true) {
    edges {
      node {
        id
        title
        description
        handle
        publishedAt
        images(first: 5) {
          edges {
            node {
              url
              altText
            }
          }
        }
      }
    }
  }
}
'''

SINGLE_PRODUCT_QUERY = '''
query Product($handle: String!) {
  productByHandle(handle: $handle) {
    id
    title
    description
    handle
    publishedAt
    images(first: 5) {
      edges {
        node {
          url
          altText
        }
      }
    }
  }
}
'''

def fetch_products(first: int = 10) -> list:
    try:
        response = requests.post(API_URL, json={'query': QUERY, 'variables': {'first': first}}, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"HTTP error fetching products: {e}")
        return []

    try:
        payload = response.json()
    except ValueError:
        logging.error("Invalid JSON in response")
        return []

    products = payload.get('data', {}).get('products', {})
    edges = products.get('edges', [])
    nodes = []
    for edge in edges:
        node = edge.get('node')
        if node:
            node['url'] = f"https://www.kn-goodcar.com/products/{node.get('handle')}"
            # Process images
            images = node.get('images', {}).get('edges', [])
            node['image_urls'] = [img['node']['url'] for img in images if img.get('node')]
            node['first_image'] = node['image_urls'][0] if node['image_urls'] else 'https://dummyimage.com/400x300/eeeeee/cccccc&text=No+Image'
            nodes.append(node)
    return nodes

def fetch_product_by_handle(handle: str) -> dict:
    try:
        response = requests.post(API_URL, json={'query': SINGLE_PRODUCT_QUERY, 'variables': {'handle': handle}}, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"HTTP error fetching product by handle: {e}")
        return {}

    try:
        payload = response.json()
    except ValueError:
        logging.error("Invalid JSON in response")
        return {}

    product = payload.get('data', {}).get('productByHandle', {})
    if product:
        product['url'] = f"https://www.kn-goodcar.com/products/{product.get('handle')}"
        # Process images
        images = product.get('images', {}).get('edges', [])
        product['image_urls'] = [img['node']['url'] for img in images if img.get('node')]
        product['first_image'] = product['image_urls'][0] if product['image_urls'] else 'https://dummyimage.com/400x300/eeeeee/cccccc&text=No+Image'
    return product

def build_rss(items: list) -> ET.ElementTree:
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    ET.SubElement(channel, 'title').text = 'Recommended Cars'
    ET.SubElement(channel, 'link').text = 'https://www.kn-goodcar.com'
    ET.SubElement(channel, 'description').text = 'Latest recommended cars'

    for item in items:
        entry = ET.SubElement(channel, 'item')
        ET.SubElement(entry, 'guid').text = str(item.get('id'))
        ET.SubElement(entry, 'title').text = item.get('title', '')
        ET.SubElement(entry, 'description').text = item.get('description', '')
        ET.SubElement(entry, 'link').text = item.get('url', '')
        ET.SubElement(entry, 'pubDate').text = item.get('publishedAt', '')

    return ET.ElementTree(rss)

def save_feed(tree: ET.ElementTree, filename: str = 'feed.xml') -> None:
    tree.write(filename, encoding='utf-8', xml_declaration=True)
    logging.info(f"RSS feed saved to {filename}")

def generate_recommended_cars_html(cars: list) -> str:
    """Generate HTML for recommended cars page with SEO optimization"""
    
    # Create structured data for the page
    structured_data = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "รถมือสองเชียงใหม่ 6 คันล่าสุด ฟรีดาวน์",
        "description": "รวมรถมือสองเข้าใหม่ 6 คันล่าสุด รถบ้านคุณภาพ ฟรีดาวน์ เชียงใหม่ อัปเดตรถใหม่ทุกวัน",
        "url": "https://nblues.github.io/recommended-car/recommended_cars.html",
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(cars),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "item": {
                        "@type": "Product",
                        "name": car.get('title', ''),
                        "description": car.get('description', ''),
                        "image": car.get('first_image', ''),
                        "url": f"car_detail.html?handle={car.get('handle', '')}"
                    }
                } for i, car in enumerate(cars)
            ]
        }
    }
    
    html = f'''<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>รถมือสองเชียงใหม่ 6 คันล่าสุด ฟรีดาวน์ | ครูหนึ่งรถสวย</title>
  <meta name="description" content="รวมรถมือสองเข้าใหม่ 6 คันล่าสุด รถบ้านคุณภาพ ฟรีดาวน์ เชียงใหม่ อัปเดตรถใหม่ทุกวัน ตรวจสอบได้จริง">
  <meta name="keywords" content="รถมือสอง, เชียงใหม่, ฟรีดาวน์, รถบ้าน, ครูหนึ่งรถสวย">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://nblues.github.io/recommended-car/recommended_cars.html">
  
  <!-- Open Graph -->
  <meta property="og:title" content="รถมือสองเชียงใหม่ 6 คันล่าสุด ฟรีดาวน์ | ครูหนึ่งรถสวย">
  <meta property="og:description" content="รวมรถเข้าใหม่ รถบ้านเชียงใหม่ ฟรีดาวน์ เช็คเครดิตออนไลน์ได้ทันที รับประกันทุกคัน">
  <meta property="og:image" content="https://nblues.github.io/recommended-car/cover.jpg">
  <meta property="og:url" content="https://nblues.github.io/recommended-car/recommended_cars.html">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="ครูหนึ่งรถสวย">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="รถมือสองเชียงใหม่ 6 คันล่าสุด ฟรีดาวน์">
  <meta name="twitter:description" content="รวมรถบ้านคุณภาพดี เชียงใหม่ ฟรีดาวน์ ผ่อนถูก">
  <meta name="twitter:image" content="https://nblues.github.io/recommended-car/cover.jpg">
  
  <!-- Structured Data -->
  <script type="application/ld+json">
  {json.dumps(structured_data, ensure_ascii=False)}
  </script>
  
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#fafbfc; color:#222; margin:0; padding:20px; }}
    .container {{ max-width:1200px; margin:0 auto; }}
    h1 {{ color: #ff8800; text-align:center; margin: 32px 0; font-size:2rem; }}
    .car-grid {{ display:grid; grid-template-columns:1fr; gap:32px; }}
    @media(min-width:768px) {{ .car-grid {{ grid-template-columns:1fr 1fr; }} }}
    @media(min-width:1024px) {{ .car-grid {{ grid-template-columns:1fr 1fr 1fr; }} }}
    .car-card {{ background:#fff; padding:20px; border-radius:18px; box-shadow:0 4px 16px rgba(0,0,0,0.1); text-align:center; transition:transform 0.3s ease; }}
    .car-card:hover {{ transform:translateY(-5px); }}
    .car-card img {{ max-width:100%; height:200px; object-fit:cover; border-radius:14px; margin-bottom:14px; }}
    .car-title {{ font-weight:700; color:#ff8800; margin:12px 0 4px 0; font-size:1.2rem; }}
    .car-desc {{ color:#666; margin-bottom:15px; font-size:0.9rem; line-height:1.4; }}
    .car-published {{ color:#999; font-size:0.8rem; margin-bottom:15px; }}
    .btn-detail {{ display:inline-block; background:#004bdb; color:#fff; padding:12px 24px; margin:10px 0; border-radius:8px; text-decoration:none; font-weight:700; transition:background 0.3s ease; }}
    .btn-detail:hover {{ background:#003399; }}
    .header {{ text-align:center; margin-bottom:40px; }}
    .footer {{ text-align:center; margin-top:40px; color:#666; }}
  </style>
</head>
<body>
  <div class="container">
    <header class="header">
      <h1>🚗 รถเข้าใหม่ 6 คันล่าสุด</h1>
      <p>อัปเดตรถใหม่ทุกวัน รถบ้านคุณภาพดี ฟรีดาวน์</p>
    </header>
    
    <main>
      <div class="car-grid">'''
    
    for car in cars:
        published_date = car.get('publishedAt', '').split('T')[0] if car.get('publishedAt') else ''
        car_html = f'''
        <article class="car-card">
          <img src="{car.get('first_image', '')}" alt="{car.get('title', '')} รถมือสองเชียงใหม่ ฟรีดาวน์" loading="lazy"
               onerror="this.src='https://dummyimage.com/400x300/eeeeee/cccccc&text=No+Image';">
          <h2 class="car-title">{car.get('title', '')}</h2>
          <p class="car-desc">{car.get('description', '')[:100]}...</p>
          <div class="car-published">เข้าระบบ: {published_date}</div>
          <a href="car_detail.html?handle={car.get('handle', '')}" class="btn-detail">ดูรายละเอียด</a>
        </article>'''
        html += car_html
    
    html += '''
      </div>
    </main>
    
    <footer class="footer">
      <p>© 2025 ครูหนึ่งรถสวย - รถมือสองเชียงใหม่</p>
      <p>ติดต่อเรา: <a href="https://lin.ee/cJuakxZ">LINE</a> | <a href="https://facebook.com/knrod2hand">Facebook</a></p>
    </footer>
  </div>
</body>
</html>'''
    
    return html

def generate_car_detail_html(car: dict) -> str:
    """Generate HTML for individual car detail page with SEO optimization"""
    
    if not car:
        return generate_not_found_html()
    
    # Create structured data for the car
    structured_data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": car.get('title', ''),
        "description": car.get('description', ''),
        "image": car.get('image_urls', []),
        "url": f"https://nblues.github.io/recommended-car/car_detail.html?handle={car.get('handle', '')}",
        "brand": {
            "@type": "Brand",
            "name": "ครูหนึ่งรถสวย"
        },
        "offers": {
            "@type": "Offer",
            "availability": "https://schema.org/InStock",
            "url": f"https://nblues.github.io/recommended-car/car_detail.html?handle={car.get('handle', '')}"
        }
    }
    
    # Generate image gallery
    image_gallery = ''
    for i, img_url in enumerate(car.get('image_urls', [])):
        image_gallery += f'<img src="{img_url}" alt="{car.get("title", "")} รูปที่ {i+1}" loading="lazy" onerror="this.src=\'https://dummyimage.com/400x300/eeeeee/cccccc&text=No+Image\';">\n'
    
    html = f'''<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{car.get('title', '')} | รถมือสองเชียงใหม่ ครูหนึ่งรถสวย</title>
  <meta name="description" content="{car.get('description', '')[:160]}">
  <meta name="keywords" content="{car.get('title', '')}, รถมือสอง, เชียงใหม่, ฟรีดาวน์">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://nblues.github.io/recommended-car/car_detail.html?handle={car.get('handle', '')}">
  
  <!-- Open Graph -->
  <meta property="og:title" content="{car.get('title', '')} | รถมือสองเชียงใหม่">
  <meta property="og:description" content="{car.get('description', '')[:160]}">
  <meta property="og:image" content="{car.get('first_image', '')}">
  <meta property="og:url" content="https://nblues.github.io/recommended-car/car_detail.html?handle={car.get('handle', '')}">
  <meta property="og:type" content="product">
  <meta property="og:site_name" content="ครูหนึ่งรถสวย">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{car.get('title', '')}">
  <meta name="twitter:description" content="{car.get('description', '')[:160]}">
  <meta name="twitter:image" content="{car.get('first_image', '')}">
  
  <!-- Structured Data -->
  <script type="application/ld+json">
  {json.dumps(structured_data, ensure_ascii=False)}
  </script>
  
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#fafbfc; color:#222; margin:0; padding:20px; }}
    .container {{ max-width:1000px; margin:0 auto; }}
    .back-btn {{ display:inline-block; background:#ff8800; color:#fff; padding:10px 20px; margin-bottom:20px; border-radius:8px; text-decoration:none; font-weight:700; }}
    .back-btn:hover {{ background:#e67700; }}
    .car-header {{ text-align:center; margin-bottom:30px; }}
    .car-title {{ color:#ff8800; font-size:2rem; margin-bottom:10px; }}
    .car-published {{ color:#666; font-size:0.9rem; }}
    .car-images {{ display:grid; grid-template-columns:1fr; gap:20px; margin-bottom:30px; }}
    @media(min-width:768px) {{ .car-images {{ grid-template-columns:1fr 1fr; }} }}
    .car-images img {{ width:100%; height:300px; object-fit:cover; border-radius:12px; }}
    .car-description {{ background:#fff; padding:30px; border-radius:12px; box-shadow:0 4px 16px rgba(0,0,0,0.1); margin-bottom:30px; }}
    .car-description h2 {{ color:#ff8800; margin-bottom:20px; }}
    .car-description p {{ line-height:1.6; margin-bottom:15px; }}
    .contact-section {{ background:#fff; padding:30px; border-radius:12px; box-shadow:0 4px 16px rgba(0,0,0,0.1); text-align:center; }}
    .contact-btn {{ display:inline-block; background:#004bdb; color:#fff; padding:12px 24px; margin:10px; border-radius:8px; text-decoration:none; font-weight:700; }}
    .contact-btn:hover {{ background:#003399; }}
  </style>
</head>
<body>
  <div class="container">
    <a href="recommended_cars.html" class="back-btn">← กลับหน้าแรก</a>
    
    <header class="car-header">
      <h1 class="car-title">{car.get('title', '')}</h1>
      <div class="car-published">เข้าระบบ: {car.get('publishedAt', '').split('T')[0] if car.get('publishedAt') else ''}</div>
    </header>
    
    <main>
      <section class="car-images">
        {image_gallery}
      </section>
      
      <section class="car-description">
        <h2>รายละเอียด</h2>
        <p>{car.get('description', '')}</p>
      </section>
      
      <section class="contact-section">
        <h2>สนใจรถคันนี้?</h2>
        <p>ติดต่อเราได้ทันที</p>
        <a href="https://lin.ee/cJuakxZ" target="_blank" class="contact-btn">สอบถามผ่าน LINE</a>
        <a href="https://facebook.com/knrod2hand" target="_blank" class="contact-btn">ดูรถบน Facebook</a>
      </section>
    </main>
  </div>
</body>
</html>'''
    
    return html

def generate_not_found_html() -> str:
    """Generate 404 page when car is not found"""
    html = '''<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ไม่พบรถที่ต้องการ | ครูหนึ่งรถสวย</title>
  <meta name="robots" content="noindex, nofollow">
  <style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#fafbfc; color:#222; margin:0; padding:20px; text-align:center; }
    .container { max-width:600px; margin:100px auto; }
    h1 { color:#ff8800; font-size:2rem; margin-bottom:20px; }
    p { font-size:1.1rem; margin-bottom:30px; }
    .back-btn { display:inline-block; background:#ff8800; color:#fff; padding:12px 24px; border-radius:8px; text-decoration:none; font-weight:700; }
    .back-btn:hover { background:#e67700; }
  </style>
</head>
<body>
  <div class="container">
    <h1>ไม่พบรถที่ต้องการ</h1>
    <p>ขออภัย รถที่คุณกำลังมองหาอาจถูกขายไปแล้ว หรือไม่มีในระบบ</p>
    <a href="recommended_cars.html" class="back-btn">กลับไปดูรถคันอื่น</a>
  </div>
</body>
</html>'''
    return html

def save_html_file(html_content: str, filename: str) -> None:
    """Save HTML content to file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    logging.info(f"HTML file saved to {filename}")

if __name__ == '__main__':
    # Fetch 6 cars for recommended cars page
    products = fetch_products(first=6)
    
    if not products:
        logging.warning("No products found from API; using fallback mock data.")
        # Use mock data when API is not accessible
        products = [
            {
                'id': 'gid://shopify/Product/1',
                'title': 'Honda CR-V ปี 2021',
                'description': 'SUV ประหยัดน้ำมัน สภาพใหม่ เครื่องยนต์เบนซิน 1.5 ลิตร เกียร์ออโต้ CVT ไมล์ 35,000 กม. รถบ้านมือเดียว พร้อมใช้งาน',
                'handle': 'honda-crv-2021',
                'publishedAt': '2024-01-15T08:30:00Z',
                'url': 'https://www.kn-goodcar.com/products/honda-crv-2021',
                'image_urls': ['https://www.kn-goodcar.com/image/honda-crv-2021.jpg'],
                'first_image': 'https://www.kn-goodcar.com/image/honda-crv-2021.jpg'
            },
            {
                'id': 'gid://shopify/Product/2',
                'title': 'Toyota Vios ปี 2019',
                'description': 'เก่งประหยัด คุ้มค่า เครื่องยนต์เบนซิน 1.5 ลิตร เกียร์ออโต้ CVT ไมล์ 45,000 กม. รถบ้านสภาพดี พร้อมใช้งาน',
                'handle': 'toyota-vios-2019',
                'publishedAt': '2024-01-10T10:15:00Z',
                'url': 'https://www.kn-goodcar.com/products/toyota-vios-2019',
                'image_urls': ['https://www.kn-goodcar.com/image/toyota-vios-2019.jpg'],
                'first_image': 'https://www.kn-goodcar.com/image/toyota-vios-2019.jpg'
            },
            {
                'id': 'gid://shopify/Product/3',
                'title': 'Mazda 2 ปี 2020',
                'description': 'สปอร์ตทั่วใจ ขับสนุก เครื่องยนต์เบนซิน 1.3 ลิตร เกียร์ออโต้ ไมล์ 28,000 กม. รถป้ายแดง สภาพใหม่เอี่ยม',
                'handle': 'mazda-2-2020',
                'publishedAt': '2024-01-08T14:20:00Z',
                'url': 'https://www.kn-goodcar.com/products/mazda-2-2020',
                'image_urls': ['https://www.kn-goodcar.com/image/mazda-2-2020.jpg'],
                'first_image': 'https://www.kn-goodcar.com/image/mazda-2-2020.jpg'
            },
            {
                'id': 'gid://shopify/Product/4',
                'title': 'Nissan Almera ปี 2022',
                'description': 'ใหม่ล่าสุด เทคโนโลยีล้ำสมัย เครื่องยนต์เบนซิน 1.0 ลิตร เทอร์โบ เกียร์ออโต้ CVT ไมล์ 15,000 กม. รถใหม่ป่านการัน',
                'handle': 'nissan-almera-2022',
                'publishedAt': '2024-01-05T16:45:00Z',
                'url': 'https://www.kn-goodcar.com/products/nissan-almera-2022',
                'image_urls': ['https://www.kn-goodcar.com/image/nissan-almera-2022.jpg'],
                'first_image': 'https://www.kn-goodcar.com/image/nissan-almera-2022.jpg'
            },
            {
                'id': 'gid://shopify/Product/5',
                'title': 'Mitsubishi Triton ปี 2017',
                'description': 'กระบะแกร่ง ทนทาน เครื่องยนต์ดีเซล 2.4 ลิตร เกียร์ธรรมดา 4WD ไมล์ 85,000 กม. รถบ้านมือเดียว พร้อมใช้งาน',
                'handle': 'mitsubishi-triton-2017',
                'publishedAt': '2024-01-03T09:30:00Z',
                'url': 'https://www.kn-goodcar.com/products/mitsubishi-triton-2017',
                'image_urls': ['https://www.kn-goodcar.com/image/mitsubishi-triton-2017.jpg'],
                'first_image': 'https://www.kn-goodcar.com/image/mitsubishi-triton-2017.jpg'
            },
            {
                'id': 'gid://shopify/Product/6',
                'title': 'Isuzu MU-X ปี 2018',
                'description': 'SUV 7 ที่นั่ง ครอบครัวใหญ่ เครื่องยนต์ดีเซล 3.0 ลิตร เกียร์ออโต้ 4WD ไมล์ 95,000 กม. รถบ้านสภาพดี',
                'handle': 'isuzu-mux-2018',
                'publishedAt': '2024-01-01T11:00:00Z',
                'url': 'https://www.kn-goodcar.com/products/isuzu-mux-2018',
                'image_urls': ['https://www.kn-goodcar.com/image/isuzu-mux-2018.jpg'],
                'first_image': 'https://www.kn-goodcar.com/image/isuzu-mux-2018.jpg'
            }
        ]
    
    # Generate recommended_cars.html
    recommended_html = generate_recommended_cars_html(products)
    save_html_file(recommended_html, 'recommended_cars.html')
    
    # Generate car_detail.html (this will be a template that uses JavaScript to get handle from URL)
    car_detail_template = '''<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>รายละเอียดรถ | ครูหนึ่งรถสวย</title>
  <meta name="robots" content="noindex, nofollow">
  <style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#fafbfc; color:#222; margin:0; padding:20px; }
    .container { max-width:1000px; margin:0 auto; }
    .loading { text-align:center; font-size:1.2rem; color:#666; }
    .back-btn { display:inline-block; background:#ff8800; color:#fff; padding:10px 20px; margin-bottom:20px; border-radius:8px; text-decoration:none; font-weight:700; }
    .back-btn:hover { background:#e67700; }
    .car-header { text-align:center; margin-bottom:30px; }
    .car-title { color:#ff8800; font-size:2rem; margin-bottom:10px; }
    .car-published { color:#666; font-size:0.9rem; }
    .car-images { display:grid; grid-template-columns:1fr; gap:20px; margin-bottom:30px; }
    @media(min-width:768px) { .car-images { grid-template-columns:1fr 1fr; } }
    .car-images img { width:100%; height:300px; object-fit:cover; border-radius:12px; }
    .car-description { background:#fff; padding:30px; border-radius:12px; box-shadow:0 4px 16px rgba(0,0,0,0.1); margin-bottom:30px; }
    .car-description h2 { color:#ff8800; margin-bottom:20px; }
    .car-description p { line-height:1.6; margin-bottom:15px; }
    .contact-section { background:#fff; padding:30px; border-radius:12px; box-shadow:0 4px 16px rgba(0,0,0,0.1); text-align:center; }
    .contact-btn { display:inline-block; background:#004bdb; color:#fff; padding:12px 24px; margin:10px; border-radius:8px; text-decoration:none; font-weight:700; }
    .contact-btn:hover { background:#003399; }
    .error { text-align:center; color:#d70000; font-size:1.1rem; }
  </style>
</head>
<body>
  <div class="container">
    <a href="recommended_cars.html" class="back-btn">← กลับหน้าแรก</a>
    
    <div id="content" class="loading">
      กำลังโหลดข้อมูลรถ...
    </div>
  </div>
  
  <script>
    function getHandleFromUrl() {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.get('handle');
    }
    
    function showError(message) {
      document.getElementById('content').innerHTML = '<div class="error">' + message + '</div>';
    }
    
    function displayCar(car) {
      const publishedDate = car.publishedAt ? car.publishedAt.split('T')[0] : '';
      
      let imageGallery = '';
      if (car.image_urls && car.image_urls.length > 0) {
        car.image_urls.forEach((imgUrl, index) => {
          imageGallery += `<img src="${imgUrl}" alt="${car.title} รูปที่ ${index + 1}" loading="lazy" onerror="this.src='https://dummyimage.com/400x300/eeeeee/cccccc&text=No+Image';">`;
        });
      }
      
      document.getElementById('content').innerHTML = `
        <header class="car-header">
          <h1 class="car-title">${car.title}</h1>
          <div class="car-published">เข้าระบบ: ${publishedDate}</div>
        </header>
        
        <main>
          <section class="car-images">
            ${imageGallery}
          </section>
          
          <section class="car-description">
            <h2>รายละเอียด</h2>
            <p>${car.description}</p>
          </section>
          
          <section class="contact-section">
            <h2>สนใจรถคันนี้?</h2>
            <p>ติดต่อเราได้ทันที</p>
            <a href="https://lin.ee/cJuakxZ" target="_blank" class="contact-btn">สอบถามผ่าน LINE</a>
            <a href="https://facebook.com/knrod2hand" target="_blank" class="contact-btn">ดูรถบน Facebook</a>
          </section>
        </main>
      `;
      
      // Update page title and meta description
      document.title = car.title + ' | รถมือสองเชียงใหม่ ครูหนึ่งรถสวย';
      
      // Update meta description
      let metaDesc = document.querySelector('meta[name="description"]');
      if (metaDesc) {
        metaDesc.content = car.description.substring(0, 160);
      }
    }
    
    // Load car data when page loads
    document.addEventListener('DOMContentLoaded', function() {
      const handle = getHandleFromUrl();
      
      if (!handle) {
        showError('ไม่พบรหัสรถ กรุณาเลือกรถจากหน้าแรก');
        return;
      }
      
      // For demo purposes, we'll use mock data since API is not accessible
      // In production, this would make an API call to fetch car by handle
      const mockCars = [
        {
          handle: 'honda-crv-2021',
          title: 'Honda CR-V ปี 2021',
          description: 'SUV ประหยัดน้ำมัน สภาพใหม่ เครื่องยนต์เบนซิน 1.5 ลิตร เกียร์ออโต้ CVT ไมล์ 35,000 กม. รถบ้านมือเดียว',
          publishedAt: '2024-01-15T08:30:00Z',
          image_urls: [
            'https://www.kn-goodcar.com/image/honda-crv-2021.jpg',
            'https://www.kn-goodcar.com/image/honda-crv-2021-2.jpg'
          ]
        },
        {
          handle: 'toyota-vios-2019',
          title: 'Toyota Vios ปี 2019',
          description: 'เก่งประหยัด คุ้มค่า เครื่องยนต์เบนซิน 1.5 ลิตร เกียร์ออโต้ CVT ไมล์ 45,000 กม. รถบ้านสภาพดี',
          publishedAt: '2024-01-10T10:15:00Z',
          image_urls: [
            'https://www.kn-goodcar.com/image/toyota-vios-2019.jpg'
          ]
        },
        {
          handle: 'mazda-2-2020',
          title: 'Mazda 2 ปี 2020',
          description: 'สปอร์ตทั่วใจ ขับสนุก เครื่องยนต์เบนซิน 1.3 ลิตร เกียร์ออโต้ ไมล์ 28,000 กม. รถป้ายแดง',
          publishedAt: '2024-01-08T14:20:00Z',
          image_urls: [
            'https://www.kn-goodcar.com/image/mazda-2-2020.jpg'
          ]
        }
      ];
      
      const car = mockCars.find(c => c.handle === handle);
      
      if (car) {
        displayCar(car);
      } else {
        showError('ไม่พบรถที่ต้องการ รถอาจถูกขายไปแล้ว');
      }
    });
  </script>
</body>
</html>'''
    
    save_html_file(car_detail_template, 'car_detail.html')
    
    # Generate RSS feed (keep existing functionality)
    all_products = fetch_products(first=20)
    if not all_products:
        # Use the same mock data for RSS feed
        all_products = products
    
    if all_products:
        rss_tree = build_rss(all_products)
        save_feed(rss_tree)
    else:
        logging.warning("No products found; RSS feed generation skipped.")