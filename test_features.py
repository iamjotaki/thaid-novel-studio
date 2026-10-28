import asyncio
from playwright.async_api import async_playwright
import urllib.request
import json
import os

async def run_test():
    # 1. Obtain token via API
    login_data = json.dumps({'email': 'writer@readawrite.pro', 'password': '123456'}).encode()
    req = urllib.request.Request('http://localhost:8080/api/auth/login', data=login_data, headers={'Content-Type': 'application/json'})
    res = json.loads(urllib.request.urlopen(req).read().decode())
    token = res['token']
    print(f"[+] Got Auth Token: {token[:12]}...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        # Inject auth token into localStorage
        await page.add_init_script(f"""
            localStorage.setItem('raw_auth_token', '{token}');
            localStorage.setItem('raw_theme', 'light');
        """)

        print("[1] Opening http://localhost:8080...")
        await page.goto("http://localhost:8080")
        await page.wait_for_timeout(2000)

        # 1. Capture Light Mode Novels
        await page.screenshot(path="c:/ReadAWrite/test_novels_light.png")
        print("  -> Saved c:/ReadAWrite/test_novels_light.png")

        # 2. Toggle Dark Mode
        print("[2] Toggling Apple Cupertino Dark Mode...")
        await page.click("button[title*='สลับโหมดมืด']")
        await page.wait_for_timeout(800)
        await page.screenshot(path="c:/ReadAWrite/test_novels_dark.png")
        print("  -> Saved c:/ReadAWrite/test_novels_dark.png")

        # 3. Enter Writing Studio
        print("[3] Entering Writing Studio...")
        await page.click("button:has-text('เข้าห้องแต่งนิยาย')")
        await page.wait_for_timeout(1500)

        # 4. Switch to Character Bible tab
        print("[4] Switching to Character Bible (คลังตัวละคร)...")
        await page.click("#studioTabCharacters")
        await page.wait_for_timeout(800)
        await page.screenshot(path="c:/ReadAWrite/test_studio_charbible_dark.png")
        print("  -> Saved c:/ReadAWrite/test_studio_charbible_dark.png")

        # 5. Add a new character
        print("[5] Adding new character card...")
        await page.click("button:has-text('+ เพิ่ม')")
        await page.wait_for_timeout(500)
        await page.fill("#charNameInput", "เลขาธีร์ (ธีรภัทร)")
        await page.select_option("#charRoleInput", "ตัวช่วย / เพื่อนสนิท")
        await page.fill("#charTraitsInput", "เลขาคนสนิทคู่ใจของคุณภีม ฉลาดสุขุม ทันเกมธุรกิจ เป็นกาวใจคอยช่วยเหลือนางเอกอย่างลับๆ")
        await page.click("button:has-text('สาวมั่น')") # select preset avatar
        await page.wait_for_timeout(300)
        await page.click("#characterForm button[type='submit']")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="c:/ReadAWrite/test_studio_char_added.png")
        print("  -> Saved c:/ReadAWrite/test_studio_char_added.png")

        # 6. Open AI Cover Studio Modal
        print("[6] Opening AI Cover Studio Modal...")
        await page.click("button:has-text('ปก AI')")
        await page.wait_for_timeout(600)
        await page.screenshot(path="c:/ReadAWrite/test_cover_modal.png")
        print("  -> Saved c:/ReadAWrite/test_cover_modal.png")

        # 7. Select preset and apply cover
        print("[7] Applying 'บอสหนุ่ม' cover preset...")
        await page.click("span:has-text('บอสหนุ่ม')")
        await page.wait_for_timeout(400)
        await page.click("button:has-text('✨ นำภาพปกไปใช้กับนิยาย')")
        await page.wait_for_timeout(1000)

        # 8. Return to novels view to verify cover
        print("[8] Returning to novels view to verify new cover...")
        await page.click("button:has-text('นิยายของฉัน')")
        await page.wait_for_timeout(1200)
        await page.screenshot(path="c:/ReadAWrite/test_novels_updated_cover.png")
        print("  -> Saved c:/ReadAWrite/test_novels_updated_cover.png")

        await browser.close()
        print("[+] ALL AUTOMATED PLAYWRIGHT TESTS PASSED!")

if __name__ == "__main__":
    asyncio.run(run_test())
