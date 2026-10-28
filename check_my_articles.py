# -*- coding: utf-8 -*-
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = r"c:\ReadAWrite\chrome_profile"
TARGET_URL = "https://www.readawrite.com/?action=main_manage_article"

def main():
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE_DIR, headless=True, channel="chrome")
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(TARGET_URL)
        page.wait_for_timeout(3000)
        
        # ปิด modal ถ้ามี
        page.keyboard.press("Escape")
        
        # ถ่ายภาพหน้าจอ
        screenshot_path = r"c:\ReadAWrite\data\articles_list_updated.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print("บันทึกภาพหน้าจอ:", screenshot_path)
        
        # ดึงนิยายในบัญชี
        articles = page.evaluate("""() => {
            const list = [];
            document.querySelectorAll('a[href*="article_id"]').forEach(a => {
                const text = a.innerText.trim();
                const href = a.getAttribute('href');
                if (text && href && !list.some(x => x.href === href)) {
                    list.push({ text: text.replace(/\\n/g, ' '), href });
                }
            });
            return list;
        }""")
        
        print(f"พบนิยายในบัญชี: {len(articles)} เรื่อง")
        for a in articles:
            print(f" - {a['text']} -> {a['href']}")
            
        with open(r"c:\ReadAWrite\data\my_novels.json", "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
            
        ctx.close()

if __name__ == "__main__":
    main()
