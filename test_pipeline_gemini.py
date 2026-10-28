# -*- coding: utf-8 -*-
import os
import json
import time
from novel_engine import NovelEngine

config = json.load(open('config.json', encoding='utf-8'))
api_key = config.get('gemini_api_key')

engine = NovelEngine(api_key=api_key)

print("Starting Agent 1: The Architect (Scene Beats)...")
t0 = time.time()
beats_prompt = """คุณคือ Agent 1: The Architect (คนวางโครงฉาก)
นิยาย: "หย่าแล้วอย่ามาอ้อนวอน (คุณประธานถึงคราวโบ้)"
แนว: ผัวโบ้ / กลับมาเจอกัน
บทที่: 3
ชื่อตอน: "พบกันในห้องประชุม... ผู้หญิงที่คุณเคยขับไล่"
ตัวละคร:
- ภีม พิชญเดชา: พระเอก (Want: ปกป้องบริษัท, Need: เรียนรู้ที่จะเห็นค่าคนที่รัก, Flaw: เย่อหยิ่ง ปากแข็ง, Speaking Style: น้ำเสียงทรงอำนาจ สุภาพแต่เย็นชา, Hidden Agenda: อยากรู้ว่าเธอสุขสบายดีไหมแต่ไม่ยอมรับ)
- รินรดา (ริน): นางเอก (Want: เซ็นสัญญาร่วมทุน, Need: ปลดล็อกแผลในใจ, Flaw: เย็นชาเกินไป, Speaking Style: กระชับ มั่นใจ ไม่แสดงอารมณ์, Hidden Agenda: ไม่ต้องการให้ภีมรู้ว่ายังจำวันเก่าๆ ได้)

จงแตกเนื้อหาเป็น 4-5 Scene Beats ตามกฎวรรณกรรมและ Micro-Pacing (ใน 1 ตอนต้องมีจุดเปลี่ยนย่อย 1 จุด):
ตอบกลับเป็น JSON Array เท่านั้น:
[
  {"beat": 1, "type": "Sensory Opening", "goal": "เปิดฉากด้วยบรรยากาศห้องประชุมหรู กลิ่นกาแฟ แอร์เย็นยะเยือก", "action": "..."},
  {"beat": 2, "type": "Rising Tension", "goal": "การมาถึงของหุ้นส่วนใหม่ และจังหวะที่สายตาประสานกัน", "action": "..."},
  {"beat": 3, "type": "Micro-Turning Point", "goal": "การเจรจาธุรกิจที่เฉียบคม รินรดาต้อนภีมจนจนมุม", "action": "..."},
  {"beat": 4, "type": "Subtext & Emotion", "goal": "บทสนทนานอกรอบที่มีนัยยะแฝง ปากบอกไม่รู้จักแต่แววตาสั่นไหว", "action": "..."},
  {"beat": 5, "type": "Cliffhanger", "goal": "จุดทิ้งปมค้าง รินรดาลุกขึ้นเดินจากไป ทิ้งคำพูดที่ทำให้ภีมสะเทือนใจ", "action": "..."}
]"""

beats_json = engine._call_gemini_sdk(beats_prompt, max_tokens=1024, temperature=0.6)
t1 = time.time()
print(f"Agent 1 finished in {t1 - t0:.2f}s")
print("Beats response preview:", beats_json[:200] if beats_json else "None")
