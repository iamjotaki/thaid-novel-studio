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
        
        info = page.evaluate("""() => {
            const data = {
                iframes: [],
                contenteditables: [],
                save_buttons: []
            };
            
            document.querySelectorAll('iframe').forEach(f => {
                data.iframes.push({ id: f.id, cls: f.className, src: f.src });
            });
            
            document.querySelectorAll('[contenteditable="true"]').forEach(el => {
                data.contenteditables.push({ id: el.id, cls: el.className });
            });
            
            document.querySelectorAll('button, input[type=button], input[type=submit]').forEach(b => {
                data.save_buttons.push({ id: b.id, cls: b.className, text: b.innerText ? b.innerText.trim() : '' });
            });
            
            return data;
        }""")
        
        print("Editor Box Info:")
        print(json.dumps(info, indent=2, ensure_ascii=False))
        ctx.close()

if __name__ == "__main__":
    main()
