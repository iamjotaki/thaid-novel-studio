# -*- coding: utf-8 -*-
import os
import json
import re
import time

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
        return {"text": "", "detected": [], "score": 100}
    
    detected = []
    clean_text = text
    
    for pattern in AI_CLICHE_PATTERNS:
        matches = re.findall(pattern, clean_text)
        if matches:
            detected.append({"pattern": pattern, "count": len(matches)})
            # Safe programmatic replacements for common AI filler words
            if "อดไม่ได้ที่จะ" in pattern:
                clean_text = re.sub(r"อดไม่ได้ที่จะ", "", clean_text)
            elif "ทว่าในใจกลับ" in pattern:
                clean_text = re.sub(r"ทว่าในใจกลับ", "แต่ในใจ", clean_text)
            elif "ความเงียบ" in pattern:
                clean_text = re.sub(r"ความเงียบ(งัน)?เข้า(ปกคลุม|ครอบงำ)", "รอบตัวเงียบกริบ", clean_text)
            elif "สูดลมหายใจเข้าลึก" in pattern:
                clean_text = re.sub(r"สูดลมหายใจเข้าลึก[ๆ]?", "ผ่อนลมหายใจช้าๆ", clean_text)
    
    # Strip moralizing endings (e.g., "และนี่คือบทเรียน...", "ไม่ว่าหนทางข้างหน้าจะ...")
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

print("De-AI Linter test:")
sample_bad = "ภีมยืนมองเธอ มีประกายบางอย่างในดวงตา รอยยิ้มมุมปากที่อ่านไม่ออกผุดขึ้น ความเงียบเข้าปกคลุมห้องทำงาน เขาอดไม่ได้ที่จะก้าวเข้าไปหาเธอ ทว่าในใจกลับเต้นรัว สูดลมหายใจเข้าลึกๆ และนี่คือบทเรียนสำคัญที่เขาไม่มีวันลืม"
res = de_ai_linter(sample_bad)
print("Detected cliches:", res["total_cliches"])
print("Score:", res["score"])
print("Clean text:", res["text"])
