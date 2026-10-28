# -*- coding: utf-8 -*-
import json
import time
import re

from novel_engine import NovelEngine, count_thai_words

config = json.load(open('config.json', encoding='utf-8'))
api_key = config.get('gemini_api_key')
engine = NovelEngine(api_key=api_key)

AI_CLICHE_PATTERNS = [
    r"ประกายบางอย่างในดวงตา",
    r"รอยยิ้มมุมปากที่อ่านไม่ออก",
    r"ราวกับเวลาหยุดหมุน",
    r"ความเงียบ(งัน)?เข้า(ปกคลุม|ครอบงำ)",
    r"อดไม่ได้ที่จะ",
    r"ทว่าในใจกลับ",
    r"บททดสอบครั้งใหม่",
    r"ราวกับ(มี)?กระแสไฟ(ฟ้า)?แล่นผ่าน",
    r"สูดลมหายใจเข้าลึก[ๆ]?",
    r"แววตาคู่คม(ที่)?ส่องประกาย",
    r"ราวกับต้องมนตร์สะกด",
    r"รอยยิ้มที่(ส่ง|ไป)ไม่ถึงดวงตา",
    r"ก้นบึ้งของหัวใจ",
    r"สิ่งที่เรียกว่า(ความรัก|ความผูกพัน)",
    r"บรรยากาศรอบข้างพลัน",
]

def de_ai_linter(text):
    if not text:
        return {"text": "", "detected": [], "score": 100, "total_cliches": 0}
    detected = []
    clean_text = text
    for pattern in AI_CLICHE_PATTERNS:
        matches = re.findall(pattern, clean_text)
        if matches:
            detected.append({"pattern": pattern, "count": len(matches)})
            if "อดไม่ได้ที่จะ" in pattern:
                clean_text = re.sub(r"อดไม่ได้ที่จะ", "", clean_text)
            elif "ทว่าในใจกลับ" in pattern:
                clean_text = re.sub(r"ทว่าในใจกลับ", "แต่ในใจ", clean_text)
            elif "ความเงียบ" in pattern:
                clean_text = re.sub(r"ความเงียบ(งัน)?เข้า(ปกคลุม|ครอบงำ)", "รอบตัวเงียบกริบ", clean_text)
            elif "สูดลมหายใจเข้าลึก" in pattern:
                clean_text = re.sub(r"สูดลมหายใจเข้าลึก[ๆ]?", "ผ่อนลมหายใจช้าๆ", clean_text)
    
    ending_paragraphs = clean_text.strip().split("\n\n")
    if len(ending_paragraphs) > 2:
        last_para = ending_paragraphs[-1].strip()
        moral_cues = ["และนี่คือ", "บทเรียนสำคัญ", "ไม่ว่าพรุ่งนี้", "ไม่ว่าหนทางข้างหน้า", "ความหวังครั้งใหม่", "บททดสอบที่แท้จริง"]
        if any(cue in last_para for cue in moral_cues) and len(last_para) < 200:
            ending_paragraphs.pop()
            clean_text = "\n\n".join(ending_paragraphs)
    
    total_found = sum(d["count"] for d in detected)
    score = max(0, 100 - (total_found * 15))
    return {
        "text": clean_text.strip(),
        "detected": detected,
        "total_cliches": total_found,
        "score": score
    }

STYLE_EXAMPLE_ROMANCE = """
"คุณคิดว่าเงินแปดแสนจะซื้อเวลาสี่ปีที่ฉันเสียไปได้เหรอคะ คุณภีม"
เธอยิ้ม. รอยยิ้มที่ไม่เปลืองแรงแม้แต่น้อย ไม่มีน้ำตา ไม่มีเสียงสะอื้น มีเพียงความว่างเปล่าที่ทำให้อีกฝ่ายยืนตัวแข็ง
ชายหนุ่มกำหมัดแน่นจนข้อนิ้วขาวซีด กลิ่นกาแฟดำที่เริ่มเย็นชืดในแก้วกระเบื้องส่งกลิ่นขมจางๆ คลุ้งในบรรยากาศ เขาอยากจะพูดอะไรสักคำ คำแก้ตัว คำสั่ง หรือคำด่าทอเหมือนที่เคยทำ ทว่าลิ้นกลับหนักอึ้ง
"ริน... ฟังผมก่อน"
"หมดเวลาฟังแล้วค่ะ"
เสียงส้นสูงกระทบกระเบื้องหินอ่อนดังก้องในโถงทางเดิน ก่อนที่ประตูลิฟต์ผู้บริหารจะปิดลงช้าๆ ตัดขาดทุกสายตา
"""

print("=== STARTING 4-AGENT PIPELINE TEST ===")
start_time = time.time()

# 1. AGENT 1: THE ARCHITECT
print("\n[1/4] Running Agent 1: The Architect (Scene Beats)...")
prompt_agent1 = f"""คุณคือ Agent 1: The Architect (คนวางโครงฉาก)
จงรับข้อมูลเพื่อแตกเป็น "ลำดับเหตุการณ์ย่อย (Scene Beats)" 4-5 Beats ต่อ 1 ตอน
นิยาย: "หย่าแล้วอย่ามาอ้อนวอน (คุณประธานถึงคราวโบ้)"
แนว: ผัวโบ้ / กลับมาเจอกัน
บทที่: 3
ชื่อตอน: "พบกันในห้องประชุม... ผู้หญิงที่คุณเคยขับไล่"
กฎวรรณกรรม:
- The 3-Chapter Rule (เปิดฉากมัดใจคนอ่าน แนะนำปมขัดแย้งเข้มข้น)
- Micro-Pacing (ใน 1 ตอน ต้องมีจุดเปลี่ยนย่อย 1 จุดเสมอ ห้ามย่ำอยู่กับที่)
- Stakes (เดิมพัน: อดีตสามีที่เคยเหยียบย่ำ ต้องก้มหัวขอร้องในฐานะคู่ค้า)
- Cliffhanger (จบตอนด้วยจังหวะชวนลุ้น ตัดฉากทิ้งปม)

ตอบกลับเป็น JSON Array 4-5 beats:
[
  {{"beat": 1, "type": "Sensory Opening", "summary": "เปิดฉากด้วยบรรยากาศตึงเครียดในห้องประชุม กลิ่นแอร์เย็นยะเยือก"}},
  {{"beat": 2, "type": "Rising Action", "summary": "รินรดาเดินเข้ามาด้วยลุคซีอีโอหญิงแกร่ง ภีมช็อกจนตัวชา"}},
  {{"beat": 3, "type": "Micro-Turning Point", "summary": "รินรดาตอกกลับเรื่องสัญญาอย่างเลือดเย็น ปฏิเสธข้อต่อรองของภีม"}},
  {{"beat": 4, "type": "Subtext & Dialogue", "summary": "การปะทะคารมนอกรอบ ภีมพยายามทวงถามเรื่องในอดีต แต่รินรดาตอกกลับด้วยความเฉยชา"}},
  {{"beat": 5, "type": "Cliffhanger", "summary": "รินรดาก้าวออกจากห้อง ทิ้งคำพูดที่ทำให้ภีมตระหนักว่าเขาหมดค่าแล้วจริงๆ"}}
]"""

resp_beats = engine._call_gemini_sdk(prompt_agent1, max_tokens=1024, temperature=0.6)
print("Agent 1 response received.")

# 2. AGENT 2: THE DRAFTER
print("\n[2/4] Running Agent 2: The Drafter (Sensory & Action Writer)...")
prompt_agent2 = f"""คุณคือ Agent 2: The Drafter (คนเขียนร่างแรก)
จงเขียนเนื้อหานิยายภาษาไทยบทที่ 3 ตามโครงฉาก (Scene Beats) ด้านล่างนี้:
<scene_beats>
{resp_beats}
</scene_beats>

<style_example>
{STYLE_EXAMPLE_ROMANCE}
</style_example>

[Style Rules: Burstiness & Sensory]
- เลียนแบบจังหวะการเล่าเรื่องและการเว้นวรรคจาก <style_example>
- บรรยายผ่านประสาทสัมผัสทั้ง 5 (กลิ่น, รส, เสียง, สัมผัส, แสงเงา)
- Show, Don't Tell (ห้ามบอกอารมณ์ตรงๆ ให้เล่าผ่านพฤติกรรม สรีระ ภาษากาย)
- ห้ามเขียนประโยคยาวเท่ากันติดต่อกันเกิน 3 ประโยค สลับประโยคสั้นกระชับกับประโยคยาว
- ละประธานตามธรรมชาติภาษาไทย ไม่ต้องใส่ 'เขา' หรือ 'เธอ' ทุกประโยค
- แต่งเนื้อหาละเอียดเข้มข้น ไม่ต่ำกว่า 1,500 คำภาษาไทย"""

draft_text = engine._call_gemini_sdk(prompt_agent2, max_tokens=6000, temperature=0.82)
print(f"Agent 2 drafted {count_thai_words(draft_text)} words.")

# 3. AGENT 3: THE DIALOGUE SPECIALIST
print("\n[3/4] Running Agent 3: The Dialogue Specialist (คนเกลาบทพูด)...")
prompt_agent3 = f"""คุณคือ Agent 3: The Dialogue Specialist (ผู้เชี่ยวชาญด้านบทสนทนา)
อ่านร่างเนื้อหานิยายด้านล่าง แล้วปรับปรุง "บทสนทนา (Dialogue)" ให้สมจริงเหมือนมนุษย์คุยกัน:
1. ใส่ Subtext (ความหมายแฝง): ปากพูดอย่างหนึ่ง แต่แฝงความรู้สึกอีกอย่าง
2. น้ำเสียงและจังหวะ: สรรพนามที่ใช้, จังหวะลังเล, การพูดแทรก, การเงียบตัดบท
3. ห้ามพูดเหมือนอ่านหนังสือเรียนหรือบอท AI
4. คงเนื้อหาการบรรยายเดิมไว้ แต่แทนที่บทพูดให้คมคายและบาดลึกยิ่งขึ้น
5. ตอบกลับเฉพาะเนื้อหาฉบับปรับปรุงบทสนทนาแล้วเท่านั้น:

{draft_text}"""

dialogue_text = engine._call_gemini_sdk(prompt_agent3, max_tokens=6000, temperature=0.75)
if not dialogue_text or len(dialogue_text) < 300:
    dialogue_text = draft_text
print("Agent 3 dialogue refinement complete.")

# 4. AGENT 4: THE RUTHLESS EDITOR & LINTER
print("\n[4/4] Running Agent 4: The Ruthless Editor (De-AI-ify & Rhythm Polisher)...")
prompt_agent4 = f"""คุณคือ Agent 4: The Ruthless Editor (บรรณาธิการคัดกรองคำ)
อ่านเนื้อหานิยายด้านล่าง แล้วเกลาให้เป็น "ภาษาของมนุษย์แท้ 100%" (De-AI-ify):
1. ตัดคำเชื่อมเยิ่นเย้อ (เช่น อย่างไรก็ตาม, ทว่า, อดไม่ได้ที่จะ, ในเวลาเดียวกันนั้น)
2. ลบคำซ้ำซากสไตล์ AI (เช่น ประกายบางอย่างในดวงตา, รอยยิ้มมุมปากที่อ่านไม่ออก, ราวกับเวลาหยุดหมุน, สูดลมหายใจเข้าลึกๆ)
3. ห้ามจบตอนด้วยการสรุปข้อคิด สรุปคำสอนใจ หรือบรรยายปรัชญาชีวิตเด็ดขาด!
4. ตัดจบที่การกระทำ (Action) หรือประโยคพูดสุดท้าย (Cliffhanger)
5. ตอบกลับเฉพาะเนื้อหาที่เกลาเสร็จแล้วเท่านั้น:

{dialogue_text}"""

edited_text = engine._call_gemini_sdk(prompt_agent4, max_tokens=6000, temperature=0.5)
if not edited_text or len(edited_text) < 300:
    edited_text = dialogue_text

# Programmatic De-AI Linter
linter_res = de_ai_linter(edited_text)
final_text = linter_res["text"]
final_words = count_thai_words(final_text)

total_elapsed = time.time() - start_time
print(f"\n=== PIPELINE FINISHED IN {total_elapsed:.2f}s ===")
print(f"Final Word Count: {final_words:,} words")
print(f"Linter Score: {linter_res['score']}/100 (Clichés neutralized: {linter_res['total_cliches']})")
print("\n--- SAMPLE EXCERPT (FIRST 400 CHARS) ---")
print(final_text[:400])
print("\n--- SAMPLE CLIFFHANGER (LAST 300 CHARS) ---")
print(final_text[-300:])
