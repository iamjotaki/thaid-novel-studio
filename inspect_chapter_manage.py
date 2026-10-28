# -*- coding: utf-8 -*-
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = r"c:\ReadAWrite\chrome_profile"
ARTICLE_MANAGE_URL = "https://www.readawrite.com/?action=manage_article&article_id=658c4eaeed43f428680aec8d7c5ec863"

def main():
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE_DIR, headless=True, channel="chrome")
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(ARTICLE_MANAGE_URL)
        page.wait_for_timeout(3000)
        
        # ปิด modal ถ้ามี
        page.keyboard.press("Escape")
        
        screenshot_path = r"c:\ReadAWrite\data\manage_specific_article.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print("บันทึกภาพหน้าจอจัดการเรื่อง:", screenshot_path)
        
        # ตรวจสอบปุ่มเพิ่มตอน
        add_chapter_links = page.evaluate("""() => {
            const list = [];
            document.querySelectorAll('a, button').forEach(el => {
                const text = el.innerText.trim();
                const href = el.getAttribute('href') || '';
                if (text.includes('ตอน') || text.includes('เพิ่ม') || href.includes('chapter')) {
                    list.push({ text: text.replace(/\\n/g, ' '), href, id: el.id, cls: el.className });
                }
            });
            return list;
        }""")
        
        print("ปุ่มเกี่ยวกับตอนที่พบ:")
        for item in add_chapter_links:
            print(" -", item)
            
        with open(r"c:\ReadAWrite\data\chapter_links.json", "w", encoding="utf-8") as f:
            json.dump(add_chapter_links, f, ensure_ascii=False, indent=2)
            
        ctx.close()

if __name__ == "__main__":
    main()
