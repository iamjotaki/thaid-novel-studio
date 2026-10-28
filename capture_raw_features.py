# -*- coding: utf-8 -*-
import urllib.request
import json
from playwright.sync_api import sync_playwright

req = urllib.request.Request('http://localhost:8080/api/auth/login', 
    data=json.dumps({'email':'writer@readawrite.pro','password':'123456'}).encode(), 
    headers={'Content-Type':'application/json'})
token = json.loads(urllib.request.urlopen(req).read().decode())['token']

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 900})
    page.goto('http://localhost:8080')
    page.evaluate(f"""() => {{
        localStorage.setItem('raw_auth_token', '{token}');
        window.location.reload();
    }}""")
    page.wait_for_timeout(1000)

    # 1. Open first novel in studio
    page.evaluate("""() => {
        if (state.novels && state.novels.length > 0) {
            openNovelInStudio(state.novels[0].id);
        }
    }""")
    page.wait_for_timeout(1000)

    # 2. Open Publish Modal to show destination selector
    page.evaluate("openPublishModal()")
    page.wait_for_timeout(1000)
    page.screenshot(path="c:/ReadAWrite/data/studio_publish_modal_new.png")
    print("[1] Publish modal screenshot saved!")

    # Close publish modal
    page.evaluate("document.getElementById('publishModal').classList.add('hidden')")
    page.wait_for_timeout(500)

    # 3. Open ReadAWrite Connect & Portfolio Modal
    page.evaluate("openReadAWriteConnectModal()")
    page.wait_for_timeout(2000)
    page.screenshot(path="c:/ReadAWrite/data/raw_live_portfolio_modal.png")
    print("[2] ReadAWrite portfolio modal screenshot saved!")

    browser.close()
