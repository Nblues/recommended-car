import requests
from datetime import datetime
import xml.etree.ElementTree as ET

shop_domain = "kn-goodcar.com"
access_token = "bb70cb008199a94b83c98df0e45ada67"

query = '''
{
  products(first: 6, sortKey: CREATED_AT, reverse: true) {
    edges {
      node {
        title
        handle
        images(first:1) { edges { node { originalSrc altText } } }
        variants(first:1) { edges { node { price } } }
      }
    }
  }
}
'''

res = requests.post(
    f'https://{shop_domain}/api/2023-07/graphql.json',
    headers={
        "Content-Type": "application/json",
        "X-Shopify-Storefront-Access-Token": access_token
    },
    json={'query': query}
)
cars = [e['node'] for e in res.json()['data']['products']['edges']]

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "รถมือสองเชียงใหม่ - ครูหนึ่งรถสวย"
ET.SubElement(channel, "link").text = "https://chiangraiusedcar.com/"
ET.SubElement(channel, "description").text = "รถบ้าน รถมือสอง อัปเดตรถเข้าใหม่ล่าสุดในเชียงใหม่"
ET.SubElement(channel, "language").text = "th-TH"

for car in cars:
    img = car['images']['edges'][0]['node']['originalSrc'] if car['images']['edges'] else ''
    alt = car['images']['edges'][0]['node'].get('altText', '') if car['images']['edges'] else car['title']
    price = car['variants']['edges'][0]['node']['price'] if car['variants']['edges'] else '-'
    link = f"https://chiangraiusedcar.com/car-detail.html?handle={car['handle']}"
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = f"{car['title']} | {price} บาท"
    ET.SubElement(item, "link").text = link
    desc = f'''<![CDATA[
      <img src="{img}" alt="{alt} รถมือสองเชียงใหม่" /><br>
      ราคา {price} บาท
    ]]>'''
    ET.SubElement(item, "description").text = desc
    ET.SubElement(item, "guid").text = link
    ET.SubElement(item, "pubDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0700")

tree = ET.ElementTree(rss)
tree.write("feed.xml", encoding="utf-8", xml_declaration=True)
