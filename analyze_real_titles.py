# -*- coding: utf-8 -*-
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\ReadAWrite\data\scraped_titles.json', 'r', encoding='utf-8') as f:
    titles = json.load(f)

# Filter out navigation and UI strings
excluded = {
    'นิยาย', 'แฟนฟิค', 'การ์ตูน', 'หน้าหลัก', 'วิธีรับการแจ้งเตือน', 'ดูทั้งหมด', 'รูปโปรไฟล์',
    'กลับไปใช้หน้าเว็บแบบเก่า', 'My Writing', 'My Reading', 'My Page', 'My Profile',
    'ประวัติการสั่งซื้อ', 'รายการที่ซื้อแล้ว', 'Pre-order ที่สั่งซื้อ', 'คูปองของฉัน',
    'ออกจากระบบ', 'กำลังโหลด', 'app store', 'google play', 'อ่านต่อ', 'จัดสรร'
}

clean_novels = []
for t in titles:
    t = t.strip()
    if not t or t in excluded or len(t) < 4 or 'ยอดสะสม' in t or 'Readtober' in t or 'Donate' in t:
        continue
    clean_novels.append(t)

print(f"Total clean real novel titles: {len(clean_novels)}")
print("\n--- SAMPLE REAL NOVEL TITLES FROM READAWRITE ---")
for t in clean_novels[:35]:
    print(" •", t)
