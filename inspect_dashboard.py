# -*- coding: utf-8 -*-
import sys
import os
import time
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = r"c:\ReadAWrite\chrome_profile"
TARGET_URL = "https://www.readawrite.com/?action=main_manage_article"

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
        time.sleep(2)
        
        # ปิด Popup โดเนท
        page.keyboard.press("Escape")
        time.sleep(1)
        try:
            page.locator(".modal.show, .modal[style*='display: block']").locator("button.close, .close").click(timeout=2000)
        except Exception:
            pass
            
        time.sleep(1)
        screenshot_path = r"c:\ReadAWrite\data\manage_clean.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print("บันทึกภาพหน้าจอ:", screenshot_path)
        
        elements = page.evaluate('''() => {
            const res = [];
            document.querySelectorAll('a, button, input[type=button], input[type=submit]').forEach(el => {
                const text = el.innerText.trim();
                const href = el.getAttribute('href') || '';
                const id = el.id || '';
                const cls = el.className || '';
                if (text || href) {
                    res.push({ text: text.replace(/\\n/g, ' '), href, id, cls, tag: el.tagName });
                }
            });
            return res;
        }''')
        
        print("รายการปุ่มและลิงก์ที่เกี่ยวข้อง:")
        filtered = []
        for el in elements:
            t = el['text']
            h = el['href']
            if any(k in t or k in h for k in ['สร้าง', 'เพิ่ม', 'เรื่อง', 'จัดการ', 'เขียน', 'article', 'new', 'ตอน']):
                print(f" - [{el['tag']}] '{t}' | href: {h} | id: {el['id']} | cls: {el['cls']}")
                filtered.append(el)
                
        with open(r"c:\ReadAWrite\data\buttons.json", "w", encoding="utf-8") as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)
            
        context.close()

if __name__ == "__main__":
    main()
