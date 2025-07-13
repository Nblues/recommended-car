import requests
import json

SHOP = "www.kn-goodcar.com"
TOKEN = "bb70cb008199a94b83c98df0e45ada67"

headers = {
    "X-Shopify-Storefront-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

query = """
{
  products(first: 20) {
    edges {
      node {
        title
        handle
        description
        vendor
        images(first: 5) { edges { node { url } } }
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

url = f"https://{SHOP}/api/2023-07/graphql.json"
resp = requests.post(url, headers=headers, json={"query": query})

if resp.status_code == 200:
    data = resp.json()["data"]["products"]["edges"]
    result = []
    for item in data:
        prod = item["node"]
        images = [img["node"]["url"] for img in prod["images"]["edges"]]
        variant = prod["variants"]["edges"][0]["node"] if prod["variants"]["edges"] else {}
        price = float(variant["price"]["amount"]) if variant else 0
        currency = variant["price"]["currencyCode"] if variant else "THB"
        sku = variant["sku"] if variant else prod["handle"]
        result.append({
            "title": prod["title"],
            "handle": prod["handle"],
            "desc": prod["description"],
            "brand": prod["vendor"],
            "images": images,
            "sku": sku,
            "price": price,
            "currency": currency,
            "link": f"https://www.kn-goodcar.com/car-detail/{prod['handle']}"
        })
    # เซฟ json
    with open("cars.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("✅ ดึงข้อมูลรถจาก Shopify ลง cars.json เรียบร้อยแล้ว")
else:
    print("❌ ERROR", resp.status_code, resp.text)