# -*- coding: utf-8 -*-
import sys
import re
import urllib.request
import ssl

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://www.readawrite.com/', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
try:
    html = urllib.request.urlopen(req, context=ctx, timeout=10).read().decode('utf-8', errors='ignore')
    print("Homepage HTML Length:", len(html))
    
    # Extract article titles
    article_titles = re.findall(r'class="[^"]*title[^"]*"[^>]*>([^<]+)<', html)
    print("Found titles:", len(article_titles))
    for t in article_titles[:15]:
        t_clean = t.strip()
        if len(t_clean) > 2:
            print(" -", t_clean)
except Exception as e:
    print("Error:", e)
