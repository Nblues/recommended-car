#!/usr/bin/env python3
import sys
import logging
import requests
import xml.etree.ElementTree as ET

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
        sys.exit(1)

    try:
        payload = response.json()
    except ValueError:
        logging.error("Invalid JSON in response")
        sys.exit(1)

    products = payload.get('data', {}).get('products', {})
    edges = products.get('edges', [])
    nodes = []
    for edge in edges:
        node = edge.get('node')
        if node:
            node['url'] = f"https://www.kn-goodcar.com/products/{node.get('handle')}"
            nodes.append(node)
    return nodes

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

if __name__ == '__main__':
    products = fetch_products(first=20)
    if not products:
        logging.warning("No products found; feed will be empty.")
    rss_tree = build_rss(products)
    save_feed(rss_tree)