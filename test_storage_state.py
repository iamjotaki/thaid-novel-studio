# -*- coding: utf-8 -*-
import os
import json
from playwright.sync_api import sync_playwright

os.makedirs(r"c:\ReadAWrite\user_sessions", exist_ok=True)
test_state_file = r"c:\ReadAWrite\user_sessions\user_1.json"

with sync_playwright() as p:
    # 1. Export state from current profile
    ctx = p.chromium.launch_persistent_context(r"c:\ReadAWrite\chrome_profile", headless=True, channel="chrome")
    ctx.storage_state(path=test_state_file)
    ctx.close()
    print(f"Exported storage_state to {test_state_file}, size: {os.path.getsize(test_state_file)} bytes")

    # 2. Test launching a clean headless context with storage_state
    browser = p.chromium.launch(headless=True, channel="chrome")
    new_ctx = browser.new_context(storage_state=test_state_file)
    page = new_ctx.new_page()
    page.goto("https://www.readawrite.com/?action=main_manage_article")
    page.wait_for_timeout(3000)
    print("Current URL:", page.url)
    title = page.title()
    print("Page Title:", title)
    
    # Check if we can find author pen name in cookies
    cookies = new_ctx.cookies("https://www.readawrite.com")
    pen_name = None
    for c in cookies:
        if c["name"] == "display_name":
            import urllib.parse
            pen_name = urllib.parse.unquote(c["value"])
    print("Author Pen Name from cookies:", pen_name)
    browser.close()
