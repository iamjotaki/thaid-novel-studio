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
        
        # คลิกปุ่มเพิ่มงานเขียน
        page.locator("button:visible:has-text('เพิ่มงานเขียน')").first.click()
        time.sleep(1.5)
        
        # คลิก Yes ถ้านโยบายเด้ง
        yes_btn = page.locator("button.swal2-confirm, button:visible:has-text('Yes')")
        if yes_btn.count() > 0:
            yes_btn.first.click()
            time.sleep(2)
            
        # ดึง HTML ของ modal "สร้างงานเขียน"
        html = page.evaluate('''() => {
            const modals = Array.from(document.querySelectorAll('.modal, [role="dialog"], .swal2-container, div[style*="z-index"]'));
            return modals.map(m => ({
                id: m.id,
                cls: m.className,
                html: m.innerHTML
            }));
        }''')
        
        with open(r"c:\ReadAWrite\data\create_modal_raw.json", "w", encoding="utf-8") as f:
            json.dump(html, f, ensure_ascii=False, indent=2)
            
        print("บันทึก modal raw เรียบร้อย")
        context.close()

if __name__ == "__main__":
    main()
