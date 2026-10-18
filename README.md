# 📖 ReadAWrite Pro Studio SaaS

ระบบเขียนและแต่งนิยายอัจฉริยะด้วย AI (Multi-Agent Engine) พร้อมระบบจัดคิวซิงค์และตั้งเวลาเผยแพร่อัตโนมัติขึ้น [ReadAWrite](https://www.readawrite.com)

---

## ✨ ไฮไลท์ฟีเจอร์เด่น (Features)
- 🧠 **AI Novel Studio:** แต่งนิยายภาษาไทยสละสลวย 50 ตอนจบ พล็อตกระชับ ไม่ติดสำนวน AI ด้วย Multi-Agent System (Plotter, Storyteller, Dialogue Specialist, ProofAI)
- 🎨 **AI Cover Studio:** ออกแบบภาพปกนิยายอัตโนมัติ พร้อมอัปโหลดและมาร์กสถานะ AI-generated บน ReadAWrite
- ☁️ **Cloud Scheduler:** วางแผนตารางปล่อยนิยายรายวัน/ช่วง Prime Time และส่งขึ้น ReadAWrite อัตโนมัติด้วย Headless Browser Automation (Playwright)
- 👥 **Multi-Tenant SaaS:** รองรับระบบสมาชิก, โควตารายวัน, Trial 7 วัน, และหน้า Super Admin HQ
- 💾 **ACID-Compliant Persistence:** จัดเก็บข้อมูลปลอดภัยด้วย SQLite DB รองรับการพอร์ตขึ้น Cloud/Docker 100%

---

## 🛠️ ความต้องการของระบบ (Prerequisites)
- **Python 3.10+**
- **Google Gemini API Key** (สำหรับระบบ AI แต่งนิยายและออกแบบปก)
- **Playwright Chromium** (สำหรับระบบเชื่อมต่อ ReadAWrite อัตโนมัติ)

---

## 🚀 วิธีติดตั้งและรันในเครื่อง (Local Setup)

1. **โคลนโปรเจกต์:**
   ```bash
   git clone <URL-REPOSITORY-ของคุณ>
   cd ReadAWrite
   ```

2. **สร้าง Virtual Environment และติดตั้งแพ็กเกจ:**
   ```bash
   python -m venv venv
   # บน Windows:
   venv\Scripts\activate
   # บน Linux/macOS:
   source venv/bin/activate

   pip install -r requirements.txt
   playwright install chromium
   ```

3. **ตั้งค่า Environment Variables:**
   ```bash
   cp .env.example .env
   ```
   ใส่ `GEMINI_API_KEY` ในไฟล์ `.env`

4. **เริ่มการทำงานของเซิร์ฟเวอร์:**
   ```bash
   python server_saas.py
   ```
   เปิดเบราว์เซอร์ไปที่: `http://localhost:8080`

---

## 🐳 วิธีรันด้วย Docker / VPS Cloud

```bash
# รันง่ายๆ ด้วยคำสั่งเดียว
docker compose up -d --build
```
ระบบจะสร้าง Container พร้อม Chromium และ Mount โฟลเดอร์ `data` และ `user_sessions` ไว้บนโฮสต์อย่างปลอดภัย
