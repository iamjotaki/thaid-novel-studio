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
        print("1. คลิกปุ่ม 'เพิ่มงานเขียน'...")
        page.locator("button:visible:has-text('เพิ่มงานเขียน')").first.click()
        time.sleep(1.5)
        
        # คลิก Yes ถ้านโยบายเด้ง
        yes_btn = page.locator("button.swal2-confirm, button:visible:has-text('Yes')")
        if yes_btn.count() > 0:
            yes_btn.first.click()
            time.sleep(2)
            
        print("2. เลือก ORIGINAL...")
        page.evaluate("""() => {
            article.selectArticle('original');
            document.querySelector('input[name="article_newType"][value="ORIGINAL"]').click();
        }""")
        time.sleep(1)
        
        print("3. เลือก FICTION (นิยายบรรยาย)...")
        page.evaluate("""() => {
            article.selectArticle('show_select_type');
            article.showtext('FICTION');
            const inp = document.querySelector('input[name="article_species"][value="FICTION"]');
            if (inp) inp.click();
        }""")
        time.sleep(1)
        
        print("4. เลือก MULTI_CHAPTER (เรื่องยาว หลายตอน)...")
        page.evaluate("""() => {
            article.selectArticle('MULTI_CHAPTER');
            const inp = document.querySelector('input[name="article_type"][value="MULTI_CHAPTER"]');
            if (inp) inp.click();
        }""")
        time.sleep(1)
        
        print("5. คลิกปุ่มสร้าง (btn_create_article)...")
        page.screenshot(path=r"c:\ReadAWrite\data\before_submit_create.png")
        page.evaluate("""() => {
            article.submitcreateArticle();
        }""")
        
        print("รอโหลดหน้าฟอร์มสร้างเรื่องใหม่...")
        time.sleep(5)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)
        
        print("URL ปัจจุบัน:", page.url)
        print("หัวข้อหน้า:", page.title())
        page.screenshot(path=r"c:\ReadAWrite\data\story_editor_real.png", full_page=True)
        print("บันทึกภาพหน้าจอ Editor:", r"c:\ReadAWrite\data\story_editor_real.png")
        
        # ดึง input ฟิลด์ทั้งหมดในหน้านี้
        inputs = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('input, select, textarea, button, [contenteditable="true"]')).map(el => ({
                tag: el.tagName,
                id: el.id,
                name: el.name,
                type: el.type,
                placeholder: el.placeholder,
                text: el.innerText ? el.innerText.trim().slice(0, 50) : '',
                cls: el.className
            }));
        }""")
        
        with open(r"c:\ReadAWrite\data\real_editor_fields.json", "w", encoding="utf-8") as f:
            json.dump(inputs, f, ensure_ascii=False, indent=2)
            
        print(f"บันทึกฟิลด์ทั้งหมด {len(inputs)} รายการเรียบร้อย")
        context.close()

if __name__ == "__main__":
    main()
