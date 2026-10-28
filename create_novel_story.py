# -*- coding: utf-8 -*-
import sys
import os
import time
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = r"c:\ReadAWrite\chrome_profile"
CREATE_URL = "https://www.readawrite.com/?action=manage_article&article_style=ORIGINAL&article_species=FICTION&article_type=MULTI_CHAPTER&translation=0"

with open(r"c:\ReadAWrite\novels\story_meta.json", encoding="utf-8") as f:
    story = json.load(f)

def main():
    print("=" * 60)
    print("กำลังเริ่มสร้างเรื่องใหม่บน ReadAWrite...")
    print("ชื่อเรื่อง:", story["title"])
    print("=" * 60)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE_DIR, headless=True, channel="chrome")
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(CREATE_URL)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)
        
        # 1. กรอกชื่อเรื่องและคำโปรย
        print("1. กรอกชื่อเรื่องและคำโปรย...")
        page.locator("#article_name").fill(story["title"])
        page.locator("#article_synopsis").fill(story["synopsis"])
        
        # 2. ติ๊กสถานะปก (ใช้ evaluate เพื่อไม่ติดปัญหา css ซ่อน input)
        print("2. ตั้งค่าสถานะภาพปก...")
        page.evaluate("""() => {
            const rad = document.querySelector('#chk_is_ai_cover0');
            if (rad) {
                rad.checked = true;
                rad.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }""")
        
        # 3. เลือกหมวดหมู่ (นิยายรัก - id: 13, parent: 83)
        print("3. เลือกหมวดหมู่นิยายรัก...")
        page.evaluate("""() => {
            if (typeof setCategoryOnModal === 'function') {
                setCategoryOnModal('นิยายรัก', '13', '83');
            }
            const cat = document.querySelector('#category_id');
            if (cat) cat.value = '13';
            const mcat = document.querySelector('#modal_category_id');
            if (mcat) mcat.value = '13';
        }""")
        time.sleep(1)
        
        # 4. เลือกระดับเนื้อหา (ทั่วไป)
        print("4. เลือกระดับเนื้อหา (ทั่วไป)...")
        page.locator("#content_rating").select_option("1")
        time.sleep(1)
        
        # ถ่ายภาพหน้าจอก่อนกดบันทึก
        os.makedirs(r"c:\ReadAWrite\data", exist_ok=True)
        page.screenshot(path=r"c:\ReadAWrite\data\before_save_story.png", full_page=True)
        print("บันทึกภาพก่อนบันทึก: c:\\ReadAWrite\\data\\before_save_story.png")
        
        # 5. กดปุ่มบันทึกเรื่อง
        print("5. กำลังกดปุ่มบันทึกสร้างเรื่อง...")
        page.locator("#btnSaveArticle").click()
        
        # รอการบันทึกและสังเกต URL เปลี่ยนแปลง
        for i in range(15):
            time.sleep(1)
            curr = page.url
            print(f"[{i+1}s] URL: {curr}")
            if "article_id=" in curr:
                print("พบ article_id ใน URL สำเร็จ!")
                break
                
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        
        final_url = page.url
        print("URL ปัจจุบันหลังบันทึก:", final_url)
        page.screenshot(path=r"c:\ReadAWrite\data\after_save_story.png", full_page=True)
        print("บันทึกภาพหลังบันทึก: c:\\ReadAWrite\\data\\after_save_story.png")
        
        ctx.close()

if __name__ == "__main__":
    main()
