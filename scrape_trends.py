# -*- coding: utf-8 -*-
import sys
import os
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = r"c:\ReadAWrite\chrome_profile"
TARGET_URL = "https://www.readawrite.com/?action=popular"

def main():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=True,
            channel="chrome"
        )
        page = context.pages[0] if context.pages else context.new_page()
        print("กำลังเข้าไปสำรวจหน้านิยายยอดนิยม/กำลังมาแรงของ ReadAWrite...")
        page.goto(TARGET_URL)
        page.wait_for_load_state("domcontentloaded")
        
        # ถ่ายภาพหน้าจอชาร์ตยอดนิยม
        os.makedirs(r"c:\ReadAWrite\data", exist_ok=True)
        page.screenshot(path=r"c:\ReadAWrite\data\popular_trends.png")
        
        # ดึงรายชื่อนิยายฮิตอันดับต้นๆ พร้อมหมวดหมู่และยอดอ่าน/หัวใจ
        trending_novels = page.evaluate('''() => {
            const list = [];
            document.querySelectorAll('.article-item, .box-item, .list-article-item, .item-article').forEach(item => {
                const titleEl = item.querySelector('.title, .article-title, h3, h4');
                const authorEl = item.querySelector('.author, .penname');
                const catEl = item.querySelector('.category, .tag, .badge');
                const statsEl = item.querySelector('.view, .read-count, .stats');
                
                const title = titleEl ? titleEl.innerText.trim() : '';
                const author = authorEl ? authorEl.innerText.trim() : '';
                const category = catEl ? catEl.innerText.trim() : '';
                const stats = statsEl ? statsEl.innerText.trim() : '';
                
                if (title && !list.some(x => x.title === title)) {
                    list.push({ title, author, category, stats, raw: item.innerText.slice(0, 150) });
                }
            });
            return list;
        }''')
        
        print(f"พบนิยายในหน้าจัดอันดับ: {len(trending_novels)} เรื่อง")
        
        # ถ้าหาไม่เจอ ให้ลองดึงการ์ดทั่วไป
        if not trending_novels:
            fallback = page.evaluate('''() => {
                const list = [];
                document.querySelectorAll('a[href*="article/"]').forEach(a => {
                    const text = a.innerText.trim();
                    if (text && text.length > 5 && !list.includes(text)) {
                        list.push(text);
                    }
                });
                return list.slice(0, 20);
            }''')
            print("Fallback items:", fallback)
            
        with open(r"c:\ReadAWrite\data\trends.json", "w", encoding="utf-8") as f:
            json.dump(trending_novels, f, ensure_ascii=False, indent=2)
            
        context.close()

if __name__ == "__main__":
    main()
