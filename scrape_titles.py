# -*- coding: utf-8 -*-
import sys
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
        page.goto(TARGET_URL)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)
        page.keyboard.press("Escape")
        
        # เลื่อนหน้าจอลงมาเรื่อยๆ เพื่อดึงข้อมูลแบนเนอร์และนิยายแนะนำ
        for _ in range(3):
            page.mouse.wheel(0, 1000)
            page.wait_for_timeout(1000)
            
        page.screenshot(path=r"c:\ReadAWrite\data\homepage_scroll.png", full_page=True)
        
        # ดึงข้อความและ alt/title ของการ์ดนิยายทั้งหมด
        cards = page.evaluate('''() => {
            const list = [];
            // ดึง alt จากรูปปกนิยาย หรือ title ในลิงก์
            document.querySelectorAll('img, a').forEach(el => {
                const alt = el.getAttribute('alt') || '';
                const title = el.getAttribute('title') || '';
                const text = el.innerText ? el.innerText.trim() : '';
                const href = el.getAttribute('href') || '';
                
                [alt, title, text].forEach(val => {
                    if (val && val.length > 3 && !list.includes(val) && !val.includes('readAwrite') && !val.includes('Google Play')) {
                        if (!val.startsWith('http') && val.length < 100) {
                            list.push(val);
                        }
                    }
                });
            });
            return list;
        }''')
        
        with open(r"c:\ReadAWrite\data\scraped_titles.json", "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False, indent=2)
            
        print(f"ดึงข้อความ/ชื่อเรื่องมาได้ {len(cards)} รายการ")
        for c in cards[:30]:
            print(" -", c)
            
        context.close()

if __name__ == "__main__":
    main()
