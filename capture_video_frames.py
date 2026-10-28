# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto('https://www.youtube.com/watch?v=Gpt64nY5s4M', timeout=40000)
        page.wait_for_timeout(3000)
        
        # Click play video if needed
        try:
            page.locator('.ytp-play-button, button[aria-label*="Play"], video').first.click()
        except:
            pass
            
        time.sleep(3)
        # Seek to 1 minute, 2 minutes, 3 minutes
        timestamps = [30, 90, 150, 220]
        for idx, ts in enumerate(timestamps):
            page.evaluate(f"document.querySelector('video').currentTime = {ts};")
            time.sleep(3)
            shot_path = f"c:\\ReadAWrite\\data\\video_frame_{idx+1}.png"
            page.screenshot(path=shot_path)
            print(f"Captured frame at {ts}s: {shot_path}")
            
        browser.close()

if __name__ == "__main__":
    main()
