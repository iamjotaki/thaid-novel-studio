# -*- coding: utf-8 -*-
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = r"c:\ReadAWrite\chrome_profile"
URL = "https://www.readawrite.com/?action=manage_article&article_style=ORIGINAL&article_species=FICTION&article_type=MULTI_CHAPTER&translation=0"

def main():
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE_DIR, headless=True, channel="chrome")
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(URL)
        page.wait_for_timeout(3000)
        
        info = page.evaluate("""() => {
            const data = {
                hidden_cat: document.querySelector('#category_id') ? document.querySelector('#category_id').value : 'none',
                dropdowns: []
            };
            
            // ค้นหา select หรือ dropdown ทุกอัน
            document.querySelectorAll('.bootstrap-select, select, [id*="cat"]').forEach(el => {
                data.dropdowns.push({
                    tag: el.tagName,
                    id: el.id,
                    name: el.name,
                    html: el.outerHTML.slice(0, 300)
                });
            });
            return data;
        }""")
        
        print("Category Info:")
        print(json.dumps(info, indent=2, ensure_ascii=False))
        ctx.close()

if __name__ == "__main__":
    main()
