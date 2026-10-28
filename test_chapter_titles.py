# -*- coding: utf-8 -*-
import urllib.request
import json

req = urllib.request.Request('http://localhost:8080/api/auth/login', 
    data=json.dumps({'email':'writer@readawrite.pro','password':'123456'}).encode(), 
    headers={'Content-Type':'application/json'})
token = json.loads(urllib.request.urlopen(req).read().decode())['token']

req2 = urllib.request.Request('http://localhost:8080/api/novels/create_blueprint', 
    data=json.dumps({
        'title': 'บ่วงรักทัณฑ์อสูร',
        'category': 'นิยายรัก',
        'genre': 'ผัวโบ้ / กลับมาเจอกัน',
        'synopsis': 'เมื่อเธอหวนกลับมาพร้อมรอยแค้นที่ไม่มีวันให้อภัย',
        'target_chapters': 10
    }).encode(), 
    headers={'Content-Type':'application/json', 'Authorization': f'Bearer {token}'})
res2 = json.loads(urllib.request.urlopen(req2).read().decode())
novel_id = res2['novel']['id']

req3 = urllib.request.Request(f'http://localhost:8080/api/novels/{novel_id}', 
    headers={'Authorization': f'Bearer {token}'})
details = json.loads(urllib.request.urlopen(req3).read().decode())['novel']

print(f"Novel: {details['title']} ({details['id']})")
print("Chapter Subtitles:")
for ch in details['chapters']:
    print(f"  บทที่ {ch['chapter_num']}: {ch['subtitle']}")
