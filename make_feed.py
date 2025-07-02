import requests
from datetime import datetime
import xml.etree.ElementTree as ET

json_url = "https://raw.githubusercontent.com/Nblues/Chiangmai-usedcar/main/cars.json"
cars = requests.get(json_url).json()[-6:][::-1]   # เอา 6 คันล่าสุด

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "รถมือสองเชียงใหม่ - ครูหนึ่งรถสวย"
ET.SubElement(channel, "link").text = "https://chiangraiusedcar.com/"
ET.SubElement(channel, "description").text = "รถบ้าน รถมือสอง อัปเดตรถเข้าใหม่ล่าสุดในเชียงใหม่"
ET.SubElement(channel, "language").text = "th-TH"

for car in cars:
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = f"{car.get('title','')[:60]} | {car.get('price','-')} บาท"
    ET.SubElement(item, "link").text = f"https://chiangraiusedcar.com/car-detail.html?handle={car.get('handle','')}"
    ET.SubElement(item, "guid").text = f"https://chiangraiusedcar.com/car-detail.html?handle={car.get('handle','')}"
    ET.SubElement(item, "pubDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0700")
    desc = f"""<![CDATA[
      <img src="{car.get('image','')}" alt="{car.get('title','')} รถมือสองเชียงใหม่" style="max-width:90%;border-radius:12px;" /><br>
      รุ่น: {car.get('title','')}<br>
      ราคา: {car.get('price','-')} บาท<br>
      <a href="https://chiangraiusedcar.com/car-detail.html?handle={car.get('handle','')}">ดูรายละเอียดรถ</a>
    ]]>"""
    ET.SubElement(item, "description").text = desc

tree = ET.ElementTree(rss)
tree.write("feed.xml", encoding="utf-8", xml_declaration=True)
print('✔️ สร้าง feed.xml เรียบร้อย')
