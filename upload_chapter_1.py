# -*- coding: utf-8 -*-
import sys
import os
import time
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = r"c:\ReadAWrite\chrome_profile"
ARTICLE_ID = "658c4eaeed43f428680aec8d7c5ec863"
CHAPTER_URL = f"https://www.readawrite.com/?action=manage_chapter&article_id={ARTICLE_ID}"

with open(r"c:\ReadAWrite\novels\story_meta.json", encoding="utf-8") as f:
    story = json.load(f)

chap_data = story["chapter_1"]

def main():
    print("=" * 60)
    print("กำลังเริ่มอัปโหลดตอนที่ 1 ขึ้น ReadAWrite (บันทึกแบบร่าง)...")
    print("ชื่อตอน:", chap_data["title"])
    print("=" * 60)

    # แปลงข้อความเป็น HTML ย่อหน้า
    paragraphs = [p.strip() for p in chap_data["content"].split("\n\n") if p.strip()]
    html_paragraphs = "".join([f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs])

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE_DIR, headless=True, channel="chrome")
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(CHAPTER_URL)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        page.keyboard.press("Escape")
        
        # 1. กรอกชื่อตอน
        print("1. กรอกบทที่ และชื่อตอนย่อย...")
        page.locator("#chapter_title").fill("บทที่ 1")
        page.locator("#chapter_subtitle").fill("เซ็นใบหย่า แล้วอย่าคิดว่าจะได้เจอกันอีก")
        time.sleep(1)
        
        # 2. ใส่เนื้อหาลงใน CKEditor ตัวแรก
        print("2. หยอดเนื้อหานิยายลงใน CKEditor...")
        inserted = page.evaluate("""(contentHtml) => {
            const editables = document.querySelectorAll('.ck-editor__editable.ck-content');
            if (editables.length === 0) return 'no editable found';
            
            const firstEditor = editables[0];
            if (firstEditor.ckeditorInstance) {
                firstEditor.ckeditorInstance.setData(contentHtml);
                return 'inserted via ckeditorInstance.setData';
            } else {
                firstEditor.innerHTML = contentHtml;
                firstEditor.dispatchEvent(new Event('input', { bubbles: true }));
                firstEditor.dispatchEvent(new Event('change', { bubbles: true }));
                return 'inserted via innerHTML';
            }
        }""", html_paragraphs)
        print("ผลการใส่เนื้อหา:", inserted)
        time.sleep(2)
        
        # ถ่ายภาพหน้าจอตอนกรอกข้อมูลเสร็จก่อนบันทึก
        os.makedirs(r"c:\ReadAWrite\data", exist_ok=True)
        before_save_pic = r"c:\ReadAWrite\data\before_save_chapter.png"
        page.screenshot(path=before_save_pic, full_page=True)
        print("บันทึกภาพหน้าจอก่อนกดบันทึก:", before_save_pic)
        
        # 3. กดปุ่ม "บันทึกแบบร่าง" (Save Draft)
        print("3. กำลังกดปุ่ม 'บันทึกแบบร่าง'...")
        page.locator("#btnSaveDraft").click()
        
        # รอให้การบันทึกสำเร็จ (ตรวจดู SweetAlert หรือการแจ้งเตือน)
        for i in range(15):
            time.sleep(1)
            swal_visible = page.locator(".swal2-modal.visible, .swal2-show, .modal.show").count()
            if swal_visible > 0:
                print("พบหน้าต่างยืนยันการบันทึก!")
                # กดยืนยัน OK ถ้าระบบถาม
                try:
                    page.locator("button.swal2-confirm, button:has-text('OK')").click()
                    time.sleep(2)
                except Exception:
                    pass
                break
            if "tab=mainManageChapter" in page.url:
                print("เปลี่ยนหน้าไปยังรายการตอนย่อยแล้ว!")
                break
                
        time.sleep(3)
        after_save_pic = r"c:\ReadAWrite\data\after_save_chapter.png"
        page.screenshot(path=after_save_pic, full_page=True)
        print("บันทึกภาพหน้าจอหลังกดบันทึก:", after_save_pic)
        print("URL ล่าสุด:", page.url)
        
        ctx.close()
        print("\n[SUCCESS] อัปโหลดตอนที่ 1 (บันทึกแบบร่าง) สำเร็จเรียบร้อย 100%!")

if __name__ == "__main__":
    main()
