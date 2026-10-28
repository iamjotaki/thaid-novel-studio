from playwright.sync_api import sync_playwright
import time

def capture():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        page.goto('https://www.youtube.com/watch?v=Gpt64nY5s4M', timeout=40000)
        page.wait_for_timeout(3000)
        
        try:
            page.locator('.ytp-play-button, video').first.click()
        except Exception as e:
            print("play err:", e)
        time.sleep(2)

        timestamps = [45, 90, 150, 210, 270]
        for idx, ts in enumerate(timestamps):
            page.evaluate(f'document.querySelector("video").currentTime = {ts};')
            time.sleep(3)
            shot_path = f'c:/ReadAWrite/data/yt_walkthrough_{idx+1}.png'
            page.screenshot(path=shot_path)
            print(f'Captured {ts}s -> {shot_path}')
            
        browser.close()

if __name__ == '__main__':
    capture()
