#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: make_feed.py
Function: สร้าง feed.xml (RSS 2.0) สำหรับดึงรถจาก Shopify
"""
import sys, logging, requests, xml.etree.ElementTree as ET
from datetime import datetime

# --- Shopify Config ---
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
        handle
        publishedAt
        description
        images(first:1) { edges { node { url } } }
        variants(first:1) {
          edges { node {
            priceV2 { amount }
          }}
        }
      }
    }
  }
}
'''

def fetch_products(first=6):
    try:
        res = requests.post(API_URL, json={'query': QUERY, 'variables': {'first': first}}, headers=HEADERS)
        res.raise_for_status()
        data = res.json()['data']['products']['edges']
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)
    items = []
    for edge in data:
        node = edge['node']
        img = node['images']['edges'][0]['node']['url'] if node['images']['edges'] else ""
        price = node['variants']['edges'][0]['node']['priceV2']['amount'] if node['variants']['edges'] else "0"
        items.append({
            "id": node['id'],
            "title": node['title'],
            "handle": node['handle'],
            "description": node['description'],
            "img": img,
            "price": price,
            "link": f"https://nblues.github.io/recommended-car/car-detail/{node['handle']}.html",
            "publishedAt": node['publishedAt']
        })
    return items

def build_rss(items):
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    ET.SubElement(channel, 'title').text = 'รถมือสองแนะนำล่าสุด | ครูหนึ่งรถสวย'
    ET.SubElement(channel, 'link').text = 'https://nblues.github.io/recommended-car/'
    ET.SubElement(channel, 'description').text = 'รถมือสองคุณภาพดี อัปเดตล่าสุด จาก kn-goodcar.com'
    for item in items:
        entry = ET.SubElement(channel, 'item')
        ET.SubElement(entry, 'guid').text = item['handle']
        ET.SubElement(entry, 'title').text = f"{item['title']} • ฿{int(float(item['price'])):,.0f}"
        ET.SubElement(entry, 'link').text = item['link']
        ET.SubElement(entry, 'pubDate').text = item['publishedAt'] or datetime.utcnow().isoformat()
        desc = (
            f"<![CDATA["
            f"<img src='{item['img']}' alt='{item['title']}' width='600'/><br>"
            f"{item['description']}<br><b>ราคา</b> ฿{int(float(item['price'])):,.0f>"
            f"]]>")
        ET.SubElement(entry, 'description').text = desc
    return ET.ElementTree(rss)

def save_feed(tree, filename='feed.xml'):
    tree.write(filename, encoding='utf-8', xml_declaration=True)
    print(f"RSS feed saved to {filename}")

if __name__ == '__main__':
    items = fetch_products(6)
    rss_tree = build_rss(items)
    save_feed(rss_tree)