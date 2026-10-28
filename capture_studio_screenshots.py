import sys
import io
import asyncio
import requests
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8080"

async def capture_all_screenshots():
    # Login to get token
    login_res = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "writer@readawrite.pro",
        "password": "123456"
    })
    token = login_res.json()["token"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        # Load page with auth token
        await page.goto(BASE_URL)
        await page.evaluate(f"localStorage.setItem('raw_auth_token', '{token}')")
        await page.goto(BASE_URL)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)

        # 1. Novels management page
        await page.evaluate("navigate('novels')")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="c:/ReadAWrite/data/studio_novels_page.png")
        print("[OK] Saved studio_novels_page.png")

        # 2. Open Blueprint Modal
        await page.evaluate("openCreateNovelModal()")
        await page.wait_for_timeout(800)
        await page.screenshot(path="c:/ReadAWrite/data/studio_blueprint_modal.png")
        print("[OK] Saved studio_blueprint_modal.png")
        await page.evaluate("document.getElementById('createNovelModal').classList.add('hidden')")
        await page.wait_for_timeout(300)

        # 3. Open Studio for first novel
        await page.evaluate("openNovelInStudio(state.novels[0].id)")
        await page.wait_for_timeout(1500)
        await page.screenshot(path="c:/ReadAWrite/data/studio_pro_subbar.png")
        print("[OK] Saved studio_pro_subbar.png")

        # 4. Open Batch Modal
        await page.evaluate("openBatchModal()")
        await page.wait_for_timeout(600)
        await page.screenshot(path="c:/ReadAWrite/data/studio_batch_modal.png")
        print("[OK] Saved studio_batch_modal.png")
        await page.evaluate("closeBatchModal()")
        await page.wait_for_timeout(300)

        # 5. Open Context Memory Modal
        await page.evaluate("openContextMemoryModal()")
        await page.wait_for_timeout(600)
        await page.screenshot(path="c:/ReadAWrite/data/studio_context_memory_modal.png")
        print("[OK] Saved studio_context_memory_modal.png")
        await page.evaluate("closeContextMemoryModal()")
        await page.wait_for_timeout(300)

        # 6. Open Tension Arc Modal
        await page.evaluate("openTensionArcModal()")
        await page.wait_for_timeout(600)
        await page.screenshot(path="c:/ReadAWrite/data/studio_tension_arc_modal.png")
        print("[OK] Saved studio_tension_arc_modal.png")
        await page.evaluate("closeTensionArcModal()")

        await browser.close()
        print("=== ALL SCREENSHOTS COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    asyncio.run(capture_all_screenshots())
