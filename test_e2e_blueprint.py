import sys
import io
import asyncio
import requests
import json
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8080"

def test_api_blueprint():
    print("=== Testing Blueprint API Endpoints ===")
    
    # 1. Login
    login_res = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "writer@readawrite.pro",
        "password": "123456"
    })
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("[OK] Logged in as writer@readawrite.pro")

    # 2. Test AI Pitch Generation
    pitch_res = requests.post(f"{BASE_URL}/api/ai/generate_blueprint_pitch", headers=headers, json={
        "genre": "ชาย-หญิง (Straight Romance)",
        "category": "โรมานซ์",
        "tone_style": "หวานซึ้ง อบอุ่นหัวใจ, ดราม่าหน่วงตับ"
    })
    assert pitch_res.status_code == 200, f"Pitch failed: {pitch_res.text}"
    pitch_data = pitch_res.json().get("pitch") or pitch_res.json().get("blueprint")
    print(f"[OK] AI Pitch Generated: '{pitch_data['title']}' | Tags: {pitch_data.get('tags')}")
    print(f"     Characters ({len(pitch_data.get('characters', []))}): {[c['name'] for c in pitch_data.get('characters', [])]}")

    # 3. Create Blueprint Novel with 50 Chapters (Exceeding the 40-chapter limitation!)
    bp_res = requests.post(f"{BASE_URL}/api/novels/create_blueprint", headers=headers, json={
        "title": pitch_data["title"],
        "category": "โรมานซ์",
        "genre": pitch_data.get("genre", "ผัวโบ้ / กลับมาเจอกัน"),
        "tags": " ".join([f"#{t}" if not t.startswith("#") else t for t in pitch_data.get("tags", [])]) if isinstance(pitch_data.get("tags"), list) else pitch_data.get("tags", "#โรมานซ์"),
        "synopsis": pitch_data.get("synopsis", "เรื่องย่อทดสอบ"),
        "plot_concept": pitch_data.get("plot_concept", "ปมขัดแย้งหลัก"),
        "tone_style": "หวานซึ้ง อบอุ่นหัวใจ",
        "intimacy_settings": {"romance_level": 70, "nc_level": 40, "climax_level": 85},
        "target_chapters": 50,
        "character_cards": pitch_data.get("characters", [])
    })
    assert bp_res.status_code == 200, f"Create Blueprint failed: {bp_res.text}"
    novel_id = bp_res.json()["novel"]["id"]
    chapters_count = bp_res.json()["novel"]["chapters_count"]
    print(f"[OK] Novel Blueprint Created! ID: {novel_id} with {chapters_count} chapters (No 40-chapter ceiling!)")

    # 4. Test Sequential Batch Generation (3 chapters)
    batch_res = requests.post(f"{BASE_URL}/api/generate_batch", headers=headers, json={
        "novel_id": novel_id,
        "start_chapter": 1,
        "count": 3,
        "target_words": 1500
    })
    assert batch_res.status_code == 200, f"Batch Gen failed: {batch_res.text}"
    batch_data = batch_res.json()
    print(f"[OK] Batch Generation completed for {len(batch_data['results'])} chapters! Total words: {batch_data['total_words_generated']}")
    for r in batch_data['results']:
        print(f"     Chapter {r['chapter_num']}: {r['subtitle']} ({r['word_count']} words)")

    # 5. Test Scene Expansion
    expand_res = requests.post(f"{BASE_URL}/api/expand_chapter", headers=headers, json={
        "novel_id": novel_id,
        "chapter_num": 1
    })
    assert expand_res.status_code == 200, f"Expand failed: {expand_res.text}"
    print(f"[OK] Scene Expansion Chapter 1: New Word Count = {expand_res.json()['word_count']}")

    # 6. Test DOCX and TXT Export
    docx_res = requests.get(f"{BASE_URL}/api/export_docx?novel_id={novel_id}", headers=headers)
    assert docx_res.status_code == 200, f"Docx export failed: {docx_res.status_code}"
    assert len(docx_res.content) > 5000, "Docx file too small"
    print(f"[OK] A5 Book DOCX Exported successfully ({len(docx_res.content)} bytes)")

    txt_res = requests.get(f"{BASE_URL}/api/export_txt?novel_id={novel_id}", headers=headers)
    assert txt_res.status_code == 200, f"Txt export failed: {txt_res.status_code}"
    print(f"[OK] Full Manuscript TXT Exported successfully ({len(txt_res.content)} bytes)")

    return novel_id, token

async def test_ui_and_take_screenshots(novel_id, token):
    print("\n=== Running Playwright UI Verification ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        # Navigate to web app
        await page.goto(BASE_URL)
        await page.wait_for_load_state("networkidle")

        # Set auth token in localStorage
        await page.evaluate(f"localStorage.setItem('raw_auth_token', '{token}')")
        await page.reload()
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)

        # 1. Novels management page
        await page.screenshot(path="c:/ReadAWrite/data/studio_novels_page.png")
        print("[Screenshot] Saved studio_novels_page.png")

        # 2. Open Blueprint Modal
        await page.click("text=+ สร้างนิยายเรื่องใหม่")
        await page.wait_for_timeout(600)
        await page.screenshot(path="c:/ReadAWrite/data/studio_blueprint_modal.png")
        print("[Screenshot] Saved studio_blueprint_modal.png")

        # Close modal
        await page.evaluate("document.getElementById('createNovelModal').classList.add('hidden')")
        await page.wait_for_timeout(300)

        # 3. Open Studio for the 50-chapter novel
        await page.evaluate(f"openNovelInStudio('{novel_id}')")
        await page.wait_for_timeout(1500)
        await page.screenshot(path="c:/ReadAWrite/data/studio_pro_subbar.png")
        print("[Screenshot] Saved studio_pro_subbar.png")

        # 4. Open Context Memory Modal
        await page.click("text=จดจำบริบทเดิม (Context Memory)")
        await page.wait_for_timeout(600)
        await page.screenshot(path="c:/ReadAWrite/data/studio_context_memory_modal.png")
        print("[Screenshot] Saved studio_context_memory_modal.png")
        await page.click("text=เข้าใจแล้ว ปิดหน้าต่าง")
        await page.wait_for_timeout(300)

        # 5. Open Tension Arc Modal
        await page.click("text=กราฟความตึงเครียด (Tension Arc)")
        await page.wait_for_timeout(600)
        await page.screenshot(path="c:/ReadAWrite/data/studio_tension_arc_modal.png")
        print("[Screenshot] Saved studio_tension_arc_modal.png")

        await browser.close()
        print("[OK] UI Screenshots completed successfully!")

if __name__ == "__main__":
    nid, tok = test_api_blueprint()
    asyncio.run(test_ui_and_take_screenshots(nid, tok))
