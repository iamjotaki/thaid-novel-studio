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

with open(r"c:\ReadAWrite\novels\story_meta.json", encoding="utf-8") as f:
    story = json.load(f)

def run():
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
        
        # ปิด Popup ถ้ามี
        page.keyboard.press("Escape")
        time.sleep(1)
        
        # คลิกปุ่มเพิ่มงานเขียน
        print("1. คลิกปุ่มเพิ่มงานเขียน...")
        page.locator("button:visible:has-text('เพิ่มงานเขียน')").first.click()
        time.sleep(1.5)
        
        # กดยืนยันข้อตกลงถ้ามี
        yes_btn = page.locator("button.swal2-confirm, button:visible:has-text('Yes')")
        if yes_btn.count() > 0:
            yes_btn.first.click()
            time.sleep(2)
            
        # เลือกชนิดนิยาย
        print("2. เลือกประเภทนิยาย...")
        page.evaluate("""() => {
            article.selectArticle('original');
            document.querySelector('input[name="article_newType"][value="ORIGINAL"]').click();
            article.selectArticle('show_select_type');
            article.showtext('FICTION');
            document.querySelector('input[name="article_species"][value="FICTION"]').click();
            article.selectArticle('MULTI_CHAPTER');
            document.querySelector('input[name="article_type"][value="MULTI_CHAPTER"]').click();
            article.submitcreateArticle();
        }""")
        
        print("3. กำลังเข้าสู่หน้าตั้งค่าเรื่อง...")
        time.sleep(5)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)
        
        # 4. กรอกข้อมูลเรื่อง
        print("4. กรอกชื่อเรื่องและคำโปรย...")
        page.locator("#article_name").fill(story["title"])
        page.locator("#article_synopsis").fill(story["synopsis"])
        
        # ติ๊กปก (ไม่ใช่ AI หรือ เป็น AI)
        page.locator("#chk_is_ai_cover0").click()
        
        # ตรวจสอบหมวดหมู่หลักที่มีให้เลือก
        cat_options = page.evaluate("""() => {
            const list = [];
            // ดึงปุ่มหรือ dropdown หมวดหมู่
            document.querySelectorAll('#category_id, [data-id="category_id"], .filter-option, .dropdown-menu li a').forEach(el => {
                list.push({ text: el.innerText.trim(), id: el.id, cls: el.className });
            });
            return list;
        }""")
        print(f"ตัวเลือกหมวดหมู่ที่ตรวจพบ {len(cat_options)} รายการ")
        
        # ลองคลิกที่กล่องเลือกหมวดหมู่หลัก
        print("5. สำรวจการเลือกหมวดหมู่...")
        page.evaluate("""() => {
            const catBtn = document.querySelector('button[data-id="category_id"], .btn-group.bootstrap-select, #category_id');
            if (catBtn) catBtn.click();
        }""")
        time.sleep(1)
        
        page.screenshot(path=r"c:\ReadAWrite\data\filled_story_form.png", full_page=True)
        print("บันทึกภาพหน้าจอฟอร์มที่กรอกแล้ว: c:\\ReadAWrite\\data\\filled_story_form.png")
        
        context.close()

if __name__ == "__main__":
    run()
