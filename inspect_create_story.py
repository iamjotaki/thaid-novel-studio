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
        print("คลิกปุ่ม 'เพิ่มงานเขียน'...")
        page.locator("button:visible:has-text('เพิ่มงานเขียน')").first.click()
        time.sleep(1.5)
        
        # ตรวจสอบปุ่ม Yes
        yes_btn = page.locator("button.swal2-confirm, button:visible:has-text('Yes')")
        if yes_btn.count() > 0:
            print("พบนโยบายข้อตกลง -> กำลังคลิกปุ่ม 'Yes'...")
            yes_btn.first.click()
            time.sleep(3)
            
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)
        print("URL ปัจจุบัน:", page.url)
        print("หัวข้อหน้าเว็บ:", page.title())
        
        screenshot_path = r"c:\ReadAWrite\data\after_yes_story.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print("บันทึกภาพหน้าจอ:", screenshot_path)
        
        # ตรวจสอบโครงสร้างในหน้านี้
        form_elements = page.evaluate('''() => {
            const list = [];
            document.querySelectorAll('input, select, textarea, button, [contenteditable="true"]').forEach(el => {
                if (el.offsetWidth > 0 || el.offsetHeight > 0) {
                    list.push({
                        tag: el.tagName,
                        type: el.type || '',
                        name: el.name || '',
                        id: el.id || '',
                        placeholder: el.placeholder || '',
                        text: el.innerText ? el.innerText.trim().slice(0, 100) : '',
                        cls: el.className || ''
                    });
                }
            });
            return list;
        }''')
        
        print(f"\nพบฟิลด์ในหน้าเว็บทั้งหมด {len(form_elements)} จุด:")
        for f in form_elements:
            if any(k in f['name'] or k in f['id'] or k in f['placeholder'] or k in f['text'] for k in ['title', 'name', 'desc', 'category', 'type', 'penname', 'cover', 'submit', 'save', 'ชื่อ', 'หมวด', 'บันทึก', 'ต่อ']):
                print(f"  * [{f['tag']}] name='{f['name']}' id='{f['id']}' type='{f['type']}' text='{f['text']}' placeholder='{f['placeholder']}'")
                
        with open(r"c:\ReadAWrite\data\story_creation_fields.json", "w", encoding="utf-8") as out:
            json.dump(form_elements, out, ensure_ascii=False, indent=2)
            
        context.close()

if __name__ == "__main__":
    main()
