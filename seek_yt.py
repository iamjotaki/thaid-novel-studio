from playwright.sync_api import sync_playwright
import time

def seek_and_capture():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        page.goto('https://www.youtube.com/watch?v=Gpt64nY5s4M', timeout=40000)
        page.wait_for_timeout(4000)
        
        times = [90, 150, 210, 270]
        for idx, t in enumerate(times):
            page.evaluate(f"""
                const player = document.getElementById('movie_player');
                if (player) {{
                    player.seekTo({t}, true);
                    player.playVideo();
                }}
            """)
            time.sleep(3)
            page.screenshot(path=f'c:/ReadAWrite/data/yt_player_{idx+1}.png')
            print(f"Captured seekTo {t}s")
            
        browser.close()

if __name__ == '__main__':
    seek_and_capture()
