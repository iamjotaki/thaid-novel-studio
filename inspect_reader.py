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

def inspect():
    print("=" * 60)
    print("กำลังตรวจสอบการล็อกอินและโครงสร้าง ReadAWrite...")
    print("=" * 60)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        # ดักจับ Request / API
        captured_apis = []
        def handle_request(req):
            if "readawrite.com" in req.url and any(k in req.url for k in ["action=", "api", "ajax", "save", "article"]):
                if not any(ext in req.url for ext in [".css", ".png", ".jpg", ".jpeg", ".svg", ".js", ".woff"]):
                    captured_apis.append({
                        "url": req.url,
                        "method": req.method,
                        "headers": req.headers,
                        "post_data": req.post_data
                    })
        page.on("request", handle_request)
        
        page.goto(TARGET_URL)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)
        
        curr_url = page.url
        print("URL ปัจจุบัน:", curr_url)
        print("หัวข้อหน้าเว็บ:", page.title())
        
        if "action=login" in curr_url:
            print("\n[!] ยังไม่ได้เข้าสู่ระบบ")
            print(">>> กรุณาดับเบิ้ลคลิกไฟล์ '1_LOGIN_READAWRITE.bat' บนหน้า Desktop เพื่อล็อกอิน 1 ครั้ง <<<")
            context.close()
            return False
            
        print("\n[+] เข้าสู่ระบบเรียบร้อยแล้ว!")
        os.makedirs(r"c:\ReadAWrite\data", exist_ok=True)
        page.screenshot(path=r"c:\ReadAWrite\data\logged_in_dashboard.png")
        
        # 1. หานิยายทั้งหมดในบัญชี
        articles = page.evaluate('''() => {
            const list = [];
            // ดึงลิงก์และชื่อเรื่องจากหน้าจัดการ
            document.querySelectorAll('a[href*="article_id"], a[href*="action=edit_article"], a[href*="action=manage_article"]').forEach(a => {
                const text = a.innerText.trim();
                const href = a.getAttribute('href');
                if (text && href && !list.some(x => x.href === href)) {
                    list.push({ text, href });
                }
            });
            return list;
        }''')
        
        print(f"\nพบนิยาย/เมนูจัดการในหน้าเว็บ: {len(articles)} รายการ")
        for idx, item in enumerate(articles[:10]):
            print(f"  [{idx+1}] {item['text']} -> {item['href']}")
            
        # 2. หาปุ่มสร้างเรื่องใหม่
        new_btns = page.evaluate('''() => {
            const btns = [];
            document.querySelectorAll('a, button').forEach(el => {
                const text = el.innerText.trim();
                const href = el.getAttribute('href') || '';
                if (text.includes('สร้างเรื่องใหม่') || text.includes('เพิ่มเรื่อง') || href.includes('action=new_article')) {
                    btns.push({ text, href, tag: el.tagName, class: el.className });
                }
            });
            return btns;
        }''')
        print("\nปุ่มสร้างเรื่องใหม่:", new_btns)
        
        # บันทึกข้อมูลที่วิเคราะห์ได้
        analysis = {
            "is_logged_in": True,
            "url": curr_url,
            "title": page.title(),
            "articles": articles,
            "new_story_buttons": new_btns,
            "captured_apis": captured_apis[:20]
        }
        with open(r"c:\ReadAWrite\data\analysis.json", "w", encoding="utf-8") as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
            
        print("\n[+] บันทึกข้อมูลวิเคราะห์เรียบร้อยที่: c:\\ReadAWrite\\data\\analysis.json")
        context.close()
        return True

if __name__ == "__main__":
    inspect()
