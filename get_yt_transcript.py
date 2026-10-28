# -*- coding: utf-8 -*-
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://www.youtube.com/watch?v=Gpt64nY5s4M', timeout=30000)
        page.wait_for_timeout(3000)
        
        try:
            page.locator('#expand').first.click()
            page.wait_for_timeout(1000)
        except:
            pass
            
        try:
            page.locator('button:has-text("แสดงข้อความถอดเสียง"), button:has-text("Show transcript")').first.click()
            page.wait_for_timeout(2000)
            segments = page.locator('ytd-transcript-segment-renderer').all_inner_texts()
            print(f"พบ transcript {len(segments)} ช่วงเวลา:")
            full_text = " ".join([s.split("\n")[-1].strip() for s in segments])
            print("Full transcript:")
            print(full_text)
            with open(r"c:\ReadAWrite\data\yt_transcript.txt", "w", encoding="utf-8") as f:
                f.write(full_text)
        except Exception as e:
            print("Error:", e)
            
        browser.close()

if __name__ == "__main__":
    main()
