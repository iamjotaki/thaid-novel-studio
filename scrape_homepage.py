# -*- coding: utf-8 -*-
import sys
import os
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = r"c:\ReadAWrite\chrome_profile"
TARGET_URL = "https://www.readawrite.com"

def main():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=True,
            channel="chrome"
        )
        page = context.pages[0] if context.pages else context.new_page()
        print("กำลังเข้าไปหน้าแรก ReadAWrite...")
        page.goto(TARGET_URL)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(3000)
        
        # ปิด modal ถ้ามี
        page.keyboard.press("Escape")
        page.wait_for_timeout(1000)
        
        page.screenshot(path=r"c:\ReadAWrite\data\homepage.png", full_page=False)
        
        # ดึงนิยายมาแรง / เรื่องฮิตในแต่ละหมวดหมู่
        sections = page.evaluate('''() => {
            const results = [];
            // วนหาหัวข้อ section เช่น เรื่องฮิต, มาแรง, นิยายยอดนิยม
            document.querySelectorAll('section, .section-box, .box-category, .landing-section, .list-book-section').forEach(sec => {
                const header = sec.querySelector('h2, h3, .section-title, .title-category');
                const headerText = header ? header.innerText.trim() : '';
                const novels = [];
                sec.querySelectorAll('.book-item, .thumbnail, .item, a[href*="?action=view_article"], a[href*="/a/"]').forEach(card => {
                    const title = card.querySelector('.title, .book-title, h4, .text-ellipsis');
                    const author = card.querySelector('.author, .penname');
                    const text = card.innerText.trim().replace(/\\n+/g, ' | ');
                    if (text && text.length > 5) {
                        novels.push({
                            title: title ? title.innerText.trim() : '',
                            author: author ? author.innerText.trim() : '',
                            text: text
                        });
                    }
                });
                if (novels.length > 0) {
                    results.push({ section: headerText, items: novels.slice(0, 10) });
                }
            });
            return results;
        }''')
        
        with open(r"c:\ReadAWrite\data\homepage_trends.json", "w", encoding="utf-8") as f:
            json.dump(sections, f, ensure_ascii=False, indent=2)
            
        print(f"ดึงหมวดหมู่และนิยายมาแรงสำเร็จ {len(sections)} หมวดหมู่")
        context.close()

if __name__ == "__main__":
    main()
