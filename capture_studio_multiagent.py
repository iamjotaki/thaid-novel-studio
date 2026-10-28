# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import database
import json

def capture_studio():
    # Login user
    u, _ = database.login_user('admin@readawrite.pro', 'admin1234')
    token = u['token']
    user_json = json.dumps(u['user'], ensure_ascii=False)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        
        # Navigate to set token
        page.goto("http://localhost:8080/")
        page.evaluate(f"""() => {{
            localStorage.setItem('raw_token', '{token}');
            localStorage.setItem('raw_user', '{user_json}');
        }}""")
        
        # Reload to initialize authenticated state
        page.goto("http://localhost:8080/")
        page.wait_for_timeout(1500)
        
        # Click first novel "เข้าสตูดิโอ"
        page.evaluate("""() => {
            if (window.state && window.state.novels && window.state.novels.length > 0) {
                window.loadNovelStudio(window.state.novels[0].id);
            }
        }""")
        page.wait_for_timeout(2000)

        # Populate demo beats and show linter badge
        page.evaluate("""() => {
            const beats = [
                { beat: 1, type: "Sensory Opening", goal: "เปิดฉากสัมผัสบรรยากาศ", action: "กลิ่นแอร์เย็นยะเยือกในห้องประชุม แสงแดดยามบ่ายสาดสะท้อนผิวกระจก" },
                { beat: 2, type: "Rising Action", goal: "เผชิญหน้าอดีตสามี", action: "การก้าวเข้ามาของรินรดาในฐานะตัวแทนคู่ค้า ภีมชะงักตัวแข็ง" },
                { beat: 3, type: "Micro-Turning Point", goal: "ตอกกลับเรื่องสัญญา", action: "รินรดาปฏิเสธข้อต่อรองเดิมด้วยแววตาเฉยชา พลิกสถานการณ์เป็นผู้คุมเกม" },
                { beat: 4, type: "Subtext & Emotion", goal: "บทสนทนามีนัยยะ", action: "ภีมพยายามทวงถามเรื่องเมื่อ 4 ปีก่อน รินรดายิ้มว่างเปล่าและตอบว่า 'คนแปลกหน้า'" },
                { beat: 5, type: "Cliffhanger", goal: "ทิ้งปมค้างคา", action: "เสียงรองเท้าส้นสูงเดินจากไป ทิ้งภีมไว้กับความจริงที่ว่าเธอไม่รักเขาแล้ว" }
            ];
            if (window.renderSceneBeats) window.renderSceneBeats(beats);
            const badge = document.getElementById('linterBadge');
            if (badge) badge.classList.remove('hidden');
        }""")
        page.wait_for_timeout(1000)

        screenshot_path = "c:/ReadAWrite/data/studio_multi_agent_pro.png"
        page.screenshot(path=screenshot_path)
        print("Captured real authenticated studio:", screenshot_path)
        browser.close()

if __name__ == "__main__":
    capture_studio()
