# -*- coding: utf-8 -*-
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = r"c:\ReadAWrite\chrome_profile"
CHAPTER_URL = "https://www.readawrite.com/?action=manage_chapter&article_id=658c4eaeed43f428680aec8d7c5ec863"

def main():
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE_DIR, headless=True, channel="chrome")
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(CHAPTER_URL)
        page.wait_for_timeout(3000)
        page.keyboard.press("Escape")
        
        screenshot_path = r"c:\ReadAWrite\data\chapter_editor.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print("บันทึกภาพหน้าจอ Editor ตอน:", screenshot_path)
        
        # ค้นหา input และ textarea และ contenteditable
        fields = page.evaluate("""() => {
            const list = [];
            document.querySelectorAll('input, textarea, [contenteditable="true"], button').forEach(el => {
                if (el.offsetWidth > 0 || el.offsetHeight > 0 || el.id.includes('title') || el.id.includes('chapter')) {
                    list.push({
                        tag: el.tagName,
                        id: el.id,
                        name: el.name,
                        type: el.type,
                        cls: el.className,
                        placeholder: el.placeholder || '',
                        text: el.innerText ? el.innerText.trim().slice(0, 50) : ''
                    });
                }
            });
            return list;
        }""")
        
        print("ฟิลด์ในหน้าแต่งตอน:")
        for f in fields:
            if any(k in f['id'] or k in f['name'] or k in f['cls'] or k in f['text'] for k in ['chapter', 'title', 'save', 'draft', 'publish', 'content', 'editor', 'บันทึก', 'ร่าง', 'ตอน']):
                print(" -", f)
                
        with open(r"c:\ReadAWrite\data\chapter_editor_fields.json", "w", encoding="utf-8") as out:
            json.dump(fields, out, ensure_ascii=False, indent=2)
            
        ctx.close()

if __name__ == "__main__":
    main()
