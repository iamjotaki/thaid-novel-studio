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
    print("=" * 60)
    print("กำลังเปิดเบราว์เซอร์สำหรับ ReadAWrite Automation...")
    print("=" * 60)
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-default-browser-check"
            ],
            viewport={"width": 1280, "height": 800}
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(TARGET_URL)
        
        # ตรวจสอบว่าล็อกอินหรือยัง
        print("กำลังตรวจสอบสถานะการเข้าสู่ระบบ...")
        time.sleep(2)
        
        is_logged_in = False
        # ตรวจเช็คว่าอยู่ในหน้าจัดการนิยายหรือไม่
        if "action=main_manage_article" in page.url and "action=login" not in page.url:
            is_logged_in = True
            
        if not is_logged_in:
            print("\n>>> กรุณากดล็อกอินเข้าบัญชี ReadAWrite ของคุณในหน้าต่างเบราว์เซอร์ที่เปิดขึ้นมา <<<")
            print(">>> ระบบกำลังรอคุณล็อกอินสำเร็จ... <<<")
            # ถ้ามีปุ่ม login ให้ลองกดเปิด modal ให้ผู้ใช้สะดวก
            try:
                page.evaluate("if (window.Login && Login.showFormLoginAndRegister) { Login.showFormLoginAndRegister('login'); }")
            except Exception:
                pass
                
            # รอจนกว่า URL จะเป็นหน้าจัดการ หรือมีสัญลักษณ์ว่าล็อกอินแล้ว (รอสูงสุด 180 วินาที)
            for i in range(180):
                time.sleep(1)
                curr_url = page.url
                if "action=main_manage_article" in curr_url and "action=login" not in curr_url:
                    is_logged_in = True
                    break
                # หรือเช็คว่ามี element ของผู้ใช้ที่ล็อกอินแล้ว
                has_user = page.locator(".user-profile, .dropdown-user, #menu_profile, a[href*='action=profile']").count()
                if has_user > 0:
                    is_logged_in = True
                    break
                    
        if not is_logged_in:
            print("หมดเวลาการรอเข้าสู่ระบบ หรือยังไม่ได้ล็อกอิน")
            context.close()
            return
            
        print("\nเข้าสู่ระบบสำเร็จแล้ว! กำลังเริ่มวิเคราะห์โครงสร้างหน้าจัดการนิยาย...")
        page.goto(TARGET_URL)
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # เก็บภาพหน้าจอ
        os.makedirs(r"c:\ReadAWrite\data", exist_ok=True)
        screenshot_path = r"c:\ReadAWrite\data\manage_article.png"
        page.screenshot(path=screenshot_path)
        print(f"บันทึกภาพหน้าจอ: {screenshot_path}")
        
        # ตรวจสอบรายการนิยาย
        articles = page.evaluate('''() => {
            const items = [];
            // ดึง element นิยาย
            document.querySelectorAll('.article-item, .box-item, [class*="article"], .item-manage').forEach(el => {
                const titleEl = el.querySelector('.title, h3, h4, a[href*="article_id"]');
                const title = titleEl ? titleEl.innerText.trim() : '';
                const link = el.querySelector('a[href*="article_id"]');
                const href = link ? link.getAttribute('href') : '';
                if (title && href) {
                    items.push({ title, href, rawText: el.innerText.slice(0, 100) });
                }
            });
            return items;
        }''')
        
        print(f"พบนิยายในบัญชี: {len(articles)} เรื่อง")
        for idx, art in enumerate(articles[:5]):
            print(f" [{idx+1}] {art['title']} ({art['href']})")
            
        # ตรวจสอบปุ่ม "สร้างเรื่องใหม่"
        new_story_btns = page.evaluate('''() => {
            const btns = [];
            document.querySelectorAll('a, button').forEach(el => {
                const text = el.innerText.trim();
                const href = el.getAttribute('href') || '';
                if (text.includes('สร้างเรื่องใหม่') || text.includes('เพิ่มเรื่อง') || href.includes('action=new_article')) {
                    btns.push({ text, href, class: el.className });
                }
            });
            return btns;
        }''')
        print("ปุ่มสร้างเรื่องใหม่:", new_story_btns)
        
        # บันทึกข้อมูลที่ตรวจพบ
        result_data = {
            "current_url": page.url,
            "title": page.title(),
            "articles": articles,
            "new_story_buttons": new_story_btns
        }
        with open(r"c:\ReadAWrite\data\manage_info.json", "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
            
        print("วิเคราะห์หน้าจัดการเรียบร้อยแล้ว!")
        print("เบราว์เซอร์จะยังคงเปิดอยู่เพื่อให้คุณตรวจสอบ...")
        time.sleep(5)
        context.close()

if __name__ == "__main__":
    main()
