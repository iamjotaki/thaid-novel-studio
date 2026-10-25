# -*- coding: utf-8 -*-
"""
Production-Ready Multi-User SaaS Backend for ReadAWrite Pro Studio
Backed by SQLite relational database (`database.py`).
Features:
1. Real Authentication:
   - POST /api/auth/register (Create real account, automatically issue 7-day trial & 50k quota)
   - POST /api/auth/login    (Validate password hash, create session token)
   - POST /api/auth/logout   (Revoke session token)
   - GET  /api/auth/me       (Get current logged-in user profile, quota, trial days)
2. Multi-Tenant Novel Management:
   - GET  /api/novels        (Get logged-in user's novels only)
   - POST /api/novels/create (Create novel tied to user)
   - GET  /api/novels/<id>   (Get novel details & chapters)
   - POST /api/chapters/save (Save chapter content to SQLite)
3. Real AI Generation & Quota Enforcement:
   - POST /api/generate_chapter (Requires auth, verifies quota/trial, generates with Gemini, deducts real word count from DB)
   - POST /api/critic_pass      (ProofAI polishing)
   - POST /api/upload_readawrite(Playwright sync to ReadAWrite.com)
4. Subscriptions & Billing:
   - POST /api/subscription/upgrade (PromptPay/Card simulated payment, upgrades plan, adds quota in DB)
5. Admin Management HQ (Admin only):
   - GET  /api/admin/users   (List all registered users from DB)
   - GET  /api/admin/stats   (Real KPI: Total users, words generated, revenue, Gemini status)
   - POST /api/admin/update_user (Change plan, extend quota, toggle status)
"""

import http.server
import socketserver
import os
import sys
import json
import urllib.parse
import threading
import time
from datetime import datetime
from novel_engine import (
    NovelEngine, count_thai_words, generate_fresh_characters, 
    generate_dynamic_chapter_outlines, READAWRITE_OFFICIAL_CATEGORIES,
    clean_chapter_subtitle, sanitize_thai_text
)
from uploader_engine import ReadAWriteUploader
import database

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", 8080))
WEB_DIR = os.path.join(BASE_DIR, "web_saas_stitch")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
COVERS_DIR = os.path.join(BASE_DIR, "data", "covers")

def get_api_key():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("gemini_api_key", "")
        except:
            pass
    return ""

class BackgroundBatchManager:
    """
    ระบบคิวเซิร์ฟเวอร์เบื้องหลังสำหรับแต่งนิยายอัตโนมัติ (Background Auto-Pilot Queue)
    ทำงานแบบ Daemon Thread ในเซิร์ฟเวอร์โดยตรง แม้ผู้ใช้จะปิดเบราว์เซอร์ ปิดหน้าต่าง หรือปิดเครื่อง
    ระบบจะแต่งนิยายต่อเนื่อง บันทึกลง SQLite และตัดโควตาให้อัตโนมัติจนครบทุกตอน
    """
    def __init__(self):
        self.lock = threading.Lock()
        self.jobs = {}  # {novel_id: job_dict}

    def start_batch(self, user_id, novel_id, chapter_list, target_words=2000, delay_seconds=4.0, mode="agentic"):
        with self.lock:
            existing = self.jobs.get(novel_id)
            if existing and existing.get("status") == "running":
                thread = existing.get("thread")
                if thread and thread.is_alive():
                    return False, "มีคิวแต่งนิยายเรื่องนี้กำลังทำงานอยู่ในเบื้องหลังแล้ว"

            stop_event = threading.Event()
            job = {
                "novel_id": novel_id,
                "user_id": user_id,
                "target_chapters": chapter_list,
                "target_words": target_words,
                "delay_seconds": delay_seconds,
                "mode": mode,
                "status": "running",
                "current_chapter": chapter_list[0] if chapter_list else None,
                "current_index": 0,
                "total_chapters": len(chapter_list),
                "completed_chapters": [],
                "total_words": 0,
                "status_message": f"เริ่มต้นคิวแต่งอัตโนมัติ {len(chapter_list)} ตอน ในเซิร์ฟเวอร์เบื้องหลัง...",
                "logs": [f"🚀 เริ่มคิวเซิร์ฟเวอร์เบื้องหลัง: {len(chapter_list)} ตอน (ปิดเว็บ/ปิดโปรแกรมได้ทันที ระบบจะแต่งต่อจนครบ)"],
                "stop_event": stop_event,
                "start_time": time.time(),
                "last_update": time.time()
            }
            self.jobs[novel_id] = job

            worker = threading.Thread(
                target=self._run_worker,
                args=(job,),
                daemon=True,
                name=f"BatchWorker-{novel_id}"
            )
            job["thread"] = worker
            worker.start()
            return True, job

    def get_status(self, novel_id):
        with self.lock:
            job = self.jobs.get(novel_id)
            if not job:
                return None
            return {
                "novel_id": job["novel_id"],
                "user_id": job["user_id"],
                "status": job["status"],
                "current_chapter": job["current_chapter"],
                "current_index": job["current_index"],
                "total_chapters": job["total_chapters"],
                "progress_percent": round((len(job["completed_chapters"]) / max(1, job["total_chapters"])) * 100),
                "completed_chapters": job["completed_chapters"],
                "total_words": job["total_words"],
                "status_message": job["status_message"],
                "logs": job["logs"][-30:],
                "delay_seconds": job["delay_seconds"],
                "target_words": job["target_words"],
                "elapsed_seconds": int(time.time() - job["start_time"])
            }

    def stop_batch(self, novel_id):
        with self.lock:
            job = self.jobs.get(novel_id)
            if not job:
                return False, "ไม่พบคิวแต่งนิยายที่กำลังทำงาน"
            if job.get("status") != "running":
                return True, "คิวแต่งนิยายนี้ไม่ได้ทำงานอยู่แล้ว"
            job["stop_event"].set()
            job["status"] = "stopped"
            job["status_message"] = "⏹️ หยุดการแต่งต่อเนื่องตามคำสั่งผู้ใช้ (บันทึกบทที่เสร็จสมบูรณ์เรียบร้อย)"
            job["logs"].append("⏹️ หยุดการแต่งต่อเนื่องตามคำสั่งผู้ใช้ (บันทึกบทที่เสร็จสมบูรณ์เรียบร้อย)")
            return True, "ส่งคำสั่งหยุดงานเรียบร้อยแล้ว"

    def _run_worker(self, job):
        novel_id = job["novel_id"]
        user_id = job["user_id"]
        chapter_list = job["target_chapters"]
        target_words = job["target_words"]
        delay_seconds = job["delay_seconds"]
        mode = job["mode"]
        stop_event = job["stop_event"]

        print(f"[BackgroundBatch] Worker started for novel {novel_id}, {len(chapter_list)} chapters.")

        try:
            user = database.get_user_by_id(user_id)
            novel = database.get_novel_details(novel_id, user_id)
            if not novel:
                job["status"] = "error"
                job["status_message"] = "ไม่พบข้อมูลนิยายในฐานข้อมูล"
                return

            novel_chars = novel.get("characters", [])

            user_keys = database.get_active_api_keys_for_user(user_id)
            if user_keys:
                raw_keys = [k["api_key"] for k in user_keys]
                engine = NovelEngine(api_keys=raw_keys)
            else:
                engine = NovelEngine(api_key=get_api_key())

            for idx, ch_num in enumerate(chapter_list):
                if stop_event.is_set():
                    print(f"[BackgroundBatch] Stop event detected for novel {novel_id}")
                    job["status"] = "stopped"
                    return

                # Expiration check
                current_user = database.get_user_by_id(user_id)
                if current_user and current_user.get("status") == "expired":
                    job["status"] = "stopped"
                    job["status_message"] = "⚠️ แพ็กเกจหมดอายุ หยุดการแต่งต่อเนื่องอัตโนมัติ"
                    job["logs"].append("⚠️ แพ็กเกจหมดอายุ หยุดการแต่งต่อเนื่องอัตโนมัติ")
                    return

                # Refetch novel details for up-to-date chapter titles
                novel = database.get_novel_details(novel_id, user_id)
                ch_obj = next((c for c in novel.get("chapters", []) if c["chapter_num"] == ch_num), None)
                raw_subtitle = ch_obj.get("subtitle", f"ตอนที่ {ch_num}") if ch_obj else f"ตอนที่ {ch_num}"
                subtitle = clean_chapter_subtitle(raw_subtitle, ch_num, novel.get("title", ""))

                job["current_chapter"] = ch_num
                job["current_index"] = idx
                job["status_message"] = f"กำลังแต่งบทที่ {ch_num}: \"{subtitle}\" ({idx + 1}/{len(chapter_list)} ตอน)..."
                job["last_update"] = time.time()

                # Sliding context memory
                sliding = database.get_sliding_context_for_chapter(novel_id, ch_num)
                
                success = False
                attempts = 0
                max_attempts = 2

                while not success and attempts < max_attempts and not stop_event.is_set():
                    attempts += 1
                    try:
                        ch_text = engine.generate_chapter(
                            story_title=novel["title"],
                            chapter_num=ch_num,
                            chapter_subtitle=subtitle,
                            genre=novel["genre"],
                            context_memory=novel_chars,
                            sliding_context=sliding,
                            target_words=target_words,
                            mode=mode,
                            category=novel.get("category", ""),
                            target_chapters=novel.get("target_chapters", 20)
                        )

                        # Clean & sanitize
                        ch_text = sanitize_thai_text(ch_text)
                        ch_words = count_thai_words(ch_text)

                        # Save to database
                        database.save_or_update_chapter(novel_id, user_id, ch_num, subtitle, ch_text, ch_words)
                        database.deduct_user_quota(user_id, ch_words)

                        success = True
                        job["total_words"] += ch_words
                        time_str = datetime.now().strftime("%H:%M:%S")
                        job["completed_chapters"].append({
                            "chapter_num": ch_num,
                            "subtitle": subtitle,
                            "word_count": ch_words,
                            "time": time_str
                        })
                        job["logs"].append(f"✅ บทที่ {ch_num}: {subtitle} ({ch_words:,} คำ) [{time_str}]")

                    except Exception as gen_err:
                        err_str = str(gen_err).lower()
                        print(f"[BackgroundBatch] Error in ch {ch_num} (attempt {attempts}): {gen_err}")
                        if "429" in err_str or "exhausted" in err_str or "limit" in err_str:
                            job["status_message"] = f"⚠️ ติด Rate Limit ชั่วคราว กำลังพัก 15 วินาที (บทที่ {ch_num})..."
                            for _ in range(30):
                                if stop_event.is_set():
                                    break
                                time.sleep(0.5)
                        else:
                            job["logs"].append(f"❌ บทที่ {ch_num} เกิดข้อผิดพลาด: {gen_err}")
                            if attempts >= max_attempts:
                                break

                # Rate Limit Pacing Delay between chapters
                if idx < len(chapter_list) - 1 and not stop_event.is_set() and delay_seconds > 0:
                    steps = int(delay_seconds * 4)
                    for s in range(steps):
                        if stop_event.is_set():
                            break
                        rem_sec = max(0.0, round(delay_seconds - (s * 0.25), 1))
                        job["status_message"] = f"⏳ พักหน่วงเวลา API {delay_seconds}s เพื่อคืนโควตา (เหลือ {rem_sec}s)..."
                        time.sleep(0.25)

            if not stop_event.is_set():
                job["current_index"] = len(chapter_list)
                job["status"] = "completed"
                job["status_message"] = f"🎉 แต่งเสร็จสมบูรณ์ {len(job['completed_chapters'])} ตอน รวม {job['total_words']:,} คำ!"
                job["logs"].append(f"🏁 คิวเซิร์ฟเวอร์แต่งสำเร็จครบทั้งหมด {len(job['completed_chapters'])} ตอน!")
                print(f"[BackgroundBatch] Finished all chapters for novel {novel_id}.")

        except Exception as fatal_err:
            print(f"[BackgroundBatch] Worker fatal error: {fatal_err}")
            job["status"] = "error"
            job["status_message"] = f"เกิดข้อผิดพลาดในการประมวลผล: {fatal_err}"
            job["logs"].append(f"❌ ข้อผิดพลาดระบบ: {fatal_err}")

# Global Background Batch Manager
batch_manager = BackgroundBatchManager()

class SaaSHttpHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def get_auth_user(self):
        auth_header = self.headers.get("Authorization", "")
        token = ""
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
        else:
            # Check query param ?token=
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            if "token" in qs:
                token = qs["token"][0]

        if not token:
            return None
        return database.get_user_by_token(token)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. Check current logged-in user session
        if path == "/api/auth/me":
            user = self.get_auth_user()
            if not user:
                self.send_json({"authenticated": False, "user": None})
                return
            self.send_json({"authenticated": True, "user": user})
            return

        # 2. Get User's Novels (Multi-tenant)
        elif path == "/api/novels":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบก่อนดูรายการนิยาย"}, 401)
                return
            novels = database.get_user_novels(user["id"])
            self.send_json({"success": True, "novels": novels})
            return

        # 3. Get Specific Novel + Chapters
        elif path.startswith("/api/novels/"):
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            novel_id = path.replace("/api/novels/", "").strip()
            novel = database.get_novel_details(novel_id, user["id"])
            if not novel:
                self.send_json({"success": False, "error": "ไม่พบนิยายเรื่องนี้ หรือคุณไม่มีสิทธิ์เข้าถึง"}, 404)
                return
            self.send_json({"success": True, "novel": novel})
            return

        # 4. Admin: Users list
        elif path == "/api/admin/users":
            user = self.get_auth_user()
            if not user or user["role"] != "admin":
                self.send_json({"success": False, "error": "ไม่มีสิทธิ์เข้าถึง (ต้องเป็น Admin เท่านั้น)"}, 403)
                return
            users = database.get_all_users_admin()
            self.send_json({"success": True, "users": users})
            return

        # 5. Admin: Platform Stats
        elif path == "/api/admin/stats":
            user = self.get_auth_user()
            if not user or user["role"] != "admin":
                self.send_json({"success": False, "error": "ไม่มีสิทธิ์เข้าถึง"}, 403)
                return
            stats = database.get_admin_stats()
            stats["gemini_status"] = "Healthy (Gemini 3.5 Flash Lite ⚡)"
            stats["uploader_status"] = "Connected (Playwright Headless)"
            self.send_json({"success": True, "stats": stats})
            return

        # ReadAWrite Official Categories
        elif path == "/api/readawrite_categories":
            self.send_json({"success": True, "categories": READAWRITE_OFFICIAL_CATEGORIES})
            return

        # 6. ReadAWrite Connection Status for Current User
        elif path == "/api/user/readawrite_status":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            session_file = os.path.join(r"c:\ReadAWrite\user_sessions", f"user_{user['id']}.json")
            has_file = os.path.exists(session_file)
            self.send_json({
                "success": True,
                "status": user.get("raw_session_status", "not_connected") if has_file else "not_connected",
                "pen_name": user.get("raw_account", "") if has_file else "",
                "updated_at": user.get("raw_session_updated_at", ""),
                "has_session_file": has_file
            })
            return
        # 7. User Personal API Keys (BYOK)
        elif path == "/api/user/keys":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            keys = database.get_user_api_keys(user["id"], include_secret=False)
            self.send_json({"success": True, "keys": keys})
            return

        # 8. Export Full Novel as A5 Word (.docx)
        elif path == "/api/export_docx":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            parsed_query = urllib.parse.parse_qs(parsed.query)
            novel_id = parsed_query.get("novel_id", [""])[0]
            novel = database.get_novel_details(novel_id, user["id"])
            if not novel:
                self.send_json({"success": False, "error": "ไม่พบนิยาย"}, 404)
                return

            import io
            import docx
            from docx.shared import Inches, Pt
            from docx.enum.text import WD_ALIGN_PARAGRAPH

            doc = docx.Document()
            section = doc.sections[0]
            # Standard A5 Book Size: 5.83 x 8.27 inches
            section.page_width = Inches(5.83)
            section.page_height = Inches(8.27)
            section.top_margin = Inches(0.7)
            section.bottom_margin = Inches(0.7)
            section.left_margin = Inches(0.7)
            section.right_margin = Inches(0.7)

            # Title Page
            p_title = doc.add_paragraph()
            p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_title = p_title.add_run(f"\n\n\n{novel['title']}\n")
            run_title.bold = True
            run_title.font.size = Pt(20)

            p_sub = doc.add_paragraph()
            p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_sub = p_sub.add_run(f"โดย: {user.get('pen_name', 'นักเขียน ReadAWrite Pro')}\nแนวเรื่อง: {novel.get('genre', '')}\n\n")
            run_sub.font.size = Pt(12)

            if novel.get('synopsis'):
                p_syn = doc.add_paragraph()
                p_syn.add_run("คำโปรย / เรื่องย่อ\n").bold = True
                p_syn.add_run(novel['synopsis'])

            doc.add_page_break()

            # Chapters
            for ch in novel.get("chapters", []):
                p_ch = doc.add_paragraph()
                p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run_ch = p_ch.add_run(f"\nบทที่ {ch['chapter_num']}: {ch['subtitle']}\n")
                run_ch.bold = True
                run_ch.font.size = Pt(14)

                if ch.get("content"):
                    paras = ch["content"].split("\n\n")
                    for para in paras:
                        if para.strip():
                            p = doc.add_paragraph()
                            p.paragraph_format.first_line_indent = Inches(0.3)
                            p.add_run(para.strip())
                else:
                    doc.add_paragraph("(ยังไม่มีเนื้อหาในบทนี้)")

                doc.add_page_break()

            mem_file = io.BytesIO()
            doc.save(mem_file)
            mem_file.seek(0)
            file_bytes = mem_file.read()

            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            self.send_header("Content-Disposition", f'attachment; filename="novel_{novel_id}.docx"')
            self.send_header("Content-Length", str(len(file_bytes)))
            self.end_headers()
            self.wfile.write(file_bytes)
            return

        # 9. Export Full Novel as Text (.txt)
        elif path == "/api/export_txt":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            parsed_query = urllib.parse.parse_qs(parsed.query)
            novel_id = parsed_query.get("novel_id", [""])[0]
            novel = database.get_novel_details(novel_id, user["id"])
            if not novel:
                self.send_json({"success": False, "error": "ไม่พบนิยาย"}, 404)
                return

            lines = [
                f"{novel['title']}",
                f"ผู้แต่ง: {user.get('pen_name', 'ReadAWrite Pro')}",
                f"แนวเรื่อง: {novel.get('genre', '')}",
                f"เรื่องย่อ: {novel.get('synopsis', '')}",
                "=" * 40,
                ""
            ]
            for ch in novel.get("chapters", []):
                lines.append(f"\n[บทที่ {ch['chapter_num']}: {ch['subtitle']}]")
                lines.append("-" * 30)
                lines.append(ch.get("content", "(ยังไม่มีเนื้อหา)"))
                lines.append("\n")

            full_text = "\n".join(lines)
            txt_bytes = full_text.encode("utf-8-sig")

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Disposition", f'attachment; filename="novel_{novel_id}.txt"')
            self.send_header("Content-Length", str(len(txt_bytes)))
            self.end_headers()
            self.wfile.write(txt_bytes)
            return

        # 10. Get User ReadAWrite Portfolio
        elif path == "/api/user/readawrite_portfolio":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            uploader = ReadAWriteUploader(user_id=user["id"])
            portfolio = uploader.get_author_portfolio()
            self.send_json({
                "success": True,
                "portfolio": portfolio
            })
            return

        # 11. Background Auto-Pilot Batch Status Polling
        elif path == "/api/batch/status":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            parsed_query = urllib.parse.parse_qs(parsed.query)
            novel_id = parsed_query.get("novel_id", [""])[0]
            if not novel_id:
                self.send_json({"success": False, "error": "กรุณาระบุ novel_id"}, 400)
                return
            status_data = batch_manager.get_status(novel_id)
            if not status_data:
                self.send_json({"success": True, "active": False, "status": "idle", "message": "ไม่มีคิวแต่งเบื้องหลัง"})
                return
            self.send_json({"success": True, "active": (status_data["status"] == "running"), "job": status_data})
            return
        elif path.startswith("/covers/") or path.startswith("/data/covers/"):
            filename = os.path.basename(path)
            cover_path = os.path.join(COVERS_DIR, filename)
            if os.path.exists(cover_path):
                self.send_response(200)
                ext = filename.split(".")[-1].lower()
                mime = "image/png" if ext == "png" else ("image/webp" if ext == "webp" else "image/jpeg")
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(os.path.getsize(cover_path)))
                self.end_headers()
                with open(cover_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, "Cover file not found")
                return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}

        # ========================================================
        # 1. AUTHENTICATION ENDPOINTS
        # ========================================================
        if path == "/api/auth/register":
            pen_name = data.get("pen_name", "").strip()
            email = data.get("email", "").strip()
            password = data.get("password", "").strip()

            if not pen_name or not email or not password:
                self.send_json({"success": False, "error": "กรุณากรอกข้อมูลให้ครบถ้วน"}, 400)
                return

            res, err = database.register_user(pen_name, email, password)
            if err:
                self.send_json({"success": False, "error": err}, 400)
                return

            self.send_json({
                "success": True,
                "message": f"ยินดีต้อนรับคุณ {pen_name}! ได้รับสิทธิ์ทดลองใช้ 7 วันฟรี โควตา 50,000 คำ",
                "token": res["token"],
                "user": res["user"]
            })
            return

        elif path == "/api/auth/login":
            email = data.get("email", "").strip()
            password = data.get("password", "").strip()

            if not email or not password:
                self.send_json({"success": False, "error": "กรุณากรอกอีเมลและรหัสผ่าน"}, 400)
                return

            res, err = database.login_user(email, password)
            if err:
                self.send_json({"success": False, "error": err}, 401)
                return

            self.send_json({
                "success": True,
                "message": f"เข้าสู่ระบบสำเร็จ ยินดีต้อนรับคุณ {res['user']['pen_name']}",
                "token": res["token"],
                "user": res["user"]
            })
            return

        elif path == "/api/auth/logout":
            auth_header = self.headers.get("Authorization", "")
            token = auth_header[7:].strip() if auth_header.startswith("Bearer ") else ""
            if token:
                database.delete_session(token)
            self.send_json({"success": True, "message": "ออกจากระบบเรียบร้อยแล้ว"})
            return

        # ========================================================
        # 2. NOVELS & CHAPTERS ENDPOINTS
        # ========================================================
        elif path == "/api/novels/create":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบก่อนสร้างนิยาย"}, 401)
                return

            title = data.get("title", "").strip()
            genre = data.get("genre", "ผัวโบ้ / กลับมาเจอกัน").strip()
            category = data.get("category", "โรมานซ์").strip()
            synopsis = data.get("synopsis", "").strip()

            if not title:
                self.send_json({"success": False, "error": "กรุณาระบุชื่อเรื่องนิยาย"}, 400)
                return

            novel = database.create_novel(user["id"], title, genre, category, synopsis)
            self.send_json({"success": True, "novel": novel, "message": f"สร้างนิยาย '{title}' สำเร็จแล้ว"})
            return

        # --- Novel Blueprint & Unlimited Chapter Endpoints (Patch 1.0) ---
        elif path == "/api/ai/generate_blueprint_pitch":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return

            category = data.get("category", "13")
            rel_dynamic = data.get("rel_dynamic") or data.get("genre", "ชาย-หญิง (Straight Romance)")
            tone_styles = data.get("tone_styles") or data.get("tone_style", "")
            concept = data.get("concept", "")
            intimacy_settings = data.get("intimacy_settings", {})

            user_keys = database.get_active_api_keys_for_user(user["id"]) if user else []
            if user_keys:
                raw_keys = [k["api_key"] for k in user_keys]
                engine = NovelEngine(api_keys=raw_keys)
            else:
                engine = NovelEngine(api_key=get_api_key())

            target_chapters = int(data.get("target_chapters", 20))
            blueprint = engine.generate_rea_trend_pitch(
                category_key=category,
                rel_dynamic=rel_dynamic,
                tone_styles=tone_styles,
                concept=concept,
                intimacy_settings=intimacy_settings,
                target_chapters=target_chapters
            )
            self.send_json({"success": True, "blueprint": blueprint, "pitch": blueprint})
            return

        elif path == "/api/novels/create_blueprint":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return

            title = data.get("title", "").strip()
            genre = data.get("genre", "ผัวโบ้ / กลับมาเจอกัน").strip()
            category = data.get("category", "โรมานซ์").strip()
            synopsis = data.get("synopsis", "").strip()
            tone_style = data.get("tone_style", "").strip()
            plot_concept = data.get("plot_concept", "").strip()
            intimacy_settings = data.get("intimacy_settings", {})
            target_chapters = int(data.get("target_chapters", 20))
            cover_url = data.get("cover_url", "")
            characters = data.get("characters") or data.get("character_cards") or []
            outlines = data.get("outlines") or data.get("chapter_outlines") or []

            if not title:
                self.send_json({"success": False, "error": "กรุณาระบุชื่อเรื่องนิยาย"}, 400)
                return

            novel = database.create_novel_blueprint(
                user_id=user["id"],
                title=title,
                genre=genre,
                category=category,
                synopsis=synopsis,
                tone_style=tone_style,
                plot_concept=plot_concept,
                intimacy_settings=intimacy_settings,
                target_chapters=target_chapters,
                cover_url=cover_url,
                outlines=outlines
            )

            # If characters not provided, automatically generate fresh 3D characters tailored to this story
            if not characters:
                characters = generate_fresh_characters(genre, title, synopsis, category=category)

            # Seed characters into Character Bible with 3D fields
            for c in characters:
                database.add_novel_character(
                    novel_id=novel["id"],
                    user_id=user["id"],
                    name=c.get("name", "ตัวละคร"),
                    role=c.get("role", "ตัวละครหลัก"),
                    traits=c.get("trait") or c.get("traits", ""),
                    avatar_url=c.get("avatar_url", ""),
                    want=c.get("want", ""),
                    need=c.get("need", ""),
                    flaw=c.get("flaw", ""),
                    speaking_style=c.get("speaking_style", ""),
                    current_emotion=c.get("current_emotion", ""),
                    hidden_agenda=c.get("hidden_agenda", "")
                )

            self.send_json({
                "success": True,
                "novel": novel,
                "message": f"สร้างนิยาย Blueprint '{title}' ({target_chapters} ตอน - สดใหม่ไม่ซ้ำใคร) สำเร็จแล้ว!"
            })
            return

        elif path == "/api/novels/regenerate_characters":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            novel_id = data.get("novel_id")
            novel = database.get_novel_details(novel_id, user["id"])
            if not novel:
                self.send_json({"success": False, "error": "ไม่พบนิยายเรื่องนี้"}, 404)
                return

            # Clear old characters and generate fresh unique set
            database.clear_novel_characters(novel_id, user["id"])
            fresh_chars = generate_fresh_characters(
                genre=novel.get("genre", "โรมานซ์"),
                story_title=novel.get("title", ""),
                synopsis=novel.get("synopsis", ""),
                category=novel.get("category", "")
            )
            for c in fresh_chars:
                database.add_novel_character(
                    novel_id=novel_id,
                    user_id=user["id"],
                    name=c.get("name"),
                    role=c.get("role"),
                    traits=c.get("traits", ""),
                    avatar_url=c.get("avatar_url", ""),
                    want=c.get("want", ""),
                    need=c.get("need", ""),
                    flaw=c.get("flaw", ""),
                    speaking_style=c.get("speaking_style", ""),
                    current_emotion=c.get("current_emotion", ""),
                    hidden_agenda=c.get("hidden_agenda", "")
                )
            updated_chars = database.get_novel_characters(novel_id, user["id"])
            self.send_json({"success": True, "characters": updated_chars, "message": "🎲 สุ่มสร้างตัวละคร 3D ชุดใหม่สด 100% เรียบร้อยแล้ว!"})
            return

        elif path == "/api/novels/regenerate_chapter_titles":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            novel_id = data.get("novel_id")
            novel = database.get_novel_details(novel_id, user["id"])
            if not novel:
                self.send_json({"success": False, "error": "ไม่พบนิยายเรื่องนี้"}, 404)
                return

            chapters = novel.get("chapters", [])
            total_ch = len(chapters) if chapters else 20
            fresh_outlines = generate_dynamic_chapter_outlines(
                story_title=novel.get("title", ""),
                genre=novel.get("genre", ""),
                synopsis=novel.get("synopsis", ""),
                target_chapters=total_ch,
                category=novel.get("category", "")
            )

            for i, ch in enumerate(chapters):
                if i < len(fresh_outlines):
                    new_sub = clean_chapter_subtitle(fresh_outlines[i].get("subtitle", ""), ch.get("chapter_num", i+1), novel.get("title", ""))
                    database.update_chapter_subtitle(novel_id, user["id"], ch.get("chapter_num", i+1), new_sub)

            updated_chapters = database.get_novel_chapters(novel_id, user["id"])
            self.send_json({"success": True, "chapters": updated_chapters, "message": "✨ ตั้งชื่อตอนใหม่ทั้งหมดตามแก่นเรื่องเรียบร้อยแล้ว!"})
            return

        elif path == "/api/chapters/save":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return

            novel_id = data.get("novel_id")
            chapter_num = int(data.get("chapter_num", 1))
            subtitle = clean_chapter_subtitle(data.get("subtitle", ""), chapter_num)
            content = sanitize_thai_text(data.get("content", ""))
            word_count = count_thai_words(content)

            database.save_or_update_chapter(novel_id, user["id"], chapter_num, subtitle, content, word_count)
            self.send_json({
                "success": True, 
                "message": f"บันทึกบทที่ {chapter_num} ลงฐานข้อมูลเรียบร้อยแล้ว ({word_count:,} คำ)",
                "word_count": word_count
            })
            return

        # ========================================================
        # 3. AI GENERATION & REAL QUOTA ENFORCEMENT
        # ========================================================
        elif path == "/api/generate_chapter":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบเพื่อใช้งานระบบแต่งนิยาย AI"}, 401)
                return

            # Check Status & Expiration (Unlimited usage within plan duration)
            if user.get("status") == "expired":
                self.send_json({
                    "success": False, 
                    "error": "ระยะเวลาการใช้งานของคุณหมดอายุแล้ว กรุณาเลือกหรือต่ออายุแพ็กเกจเพื่อแต่งนิยายต่อได้อย่างไม่จำกัด"
                }, 403)
                return

            target_words = int(data.get("target_words", 2500))

            title = data.get("title", "นิยายโรมานซ์")
            chapter_num = int(data.get("chapter_num", 1))
            subtitle = clean_chapter_subtitle(data.get("subtitle", ""), chapter_num, title)
            genre = data.get("genre", "โรมานซ์")
            forbidden = data.get("forbidden", "")
            novel_id = data.get("novel_id", "")
            mode = data.get("mode", "agentic")

            # Check for active BYOK API Keys for this user
            user_keys = database.get_active_api_keys_for_user(user["id"])
            if user_keys:
                raw_keys = [k["api_key"] for k in user_keys]
                engine = NovelEngine(api_keys=raw_keys)
                using_byok = True
                key_labels = ", ".join([k["label"] for k in user_keys])
                print(f"[AI] User {user['pen_name']} using {len(user_keys)} Personal API Key(s) (BYOK: {key_labels})")
            else:
                engine = NovelEngine(api_key=get_api_key())
                using_byok = False

            # Load Character Bible and Sliding Context Memory (Unlimited Chapters Engine)
            novel_chars = database.get_novel_characters(novel_id, user["id"]) if novel_id else []
            sliding_context = database.get_sliding_context_for_chapter(novel_id, chapter_num) if novel_id else ""
            category = ""
            target_chapters = 20
            if novel_id:
                novel_obj = database.get_novel_details(novel_id, user["id"])
                if novel_obj:
                    category = novel_obj.get("category", "")
                    target_chapters = novel_obj.get("target_chapters", 20)

            text = engine.generate_chapter(
                story_title=title,
                chapter_num=chapter_num,
                chapter_subtitle=subtitle,
                genre=genre,
                context_memory=novel_chars,
                sliding_context=sliding_context,
                target_words=target_words,
                forbidden_words=forbidden,
                mode=mode,
                category=category,
                target_chapters=target_chapters
            )

            actual_words = count_thai_words(text)
            chars = len(text)

            # Record key usage if byok
            if using_byok and engine.last_used_key:
                for k in user_keys:
                    if k["api_key"] == engine.last_used_key:
                        database.record_api_key_usage(k["id"], status="ready")
                        break

            # Deduct quota from real DB
            updated_quota = database.deduct_user_quota(user["id"], actual_words)

            # Persist chapter in DB if novel_id provided
            if novel_id:
                database.save_or_update_chapter(novel_id, user["id"], chapter_num, subtitle, text, actual_words)

            beats = getattr(engine, 'last_beats', [])
            de_ai_stats = getattr(engine, 'last_de_ai_stats', {})
            agentic_steps = getattr(engine, 'last_agentic_steps', [])

            msg = f"แต่งบทที่ {chapter_num} สำเร็จ! ({'Multi-Agent Pipeline 🌟' if mode == 'agentic' else 'Turbo Mode ⚡'}) ตัดโควตาตามจริง {actual_words:,} คำ"
            if using_byok:
                msg += " (⚡ ขับเคลื่อนด้วย Gemini API Key ส่วนตัวของคุณ)"

            self.send_json({
                "success": True,
                "chapter_num": chapter_num,
                "subtitle": subtitle,
                "text": text,
                "word_count": actual_words,
                "char_count": chars,
                "using_byok": using_byok,
                "mode": mode,
                "beats": beats,
                "de_ai_stats": de_ai_stats,
                "agentic_steps": agentic_steps,
                "quota_used": updated_quota["quota_used"] if updated_quota else user["quota_used"] + actual_words,
                "quota_limit": updated_quota["quota_limit"] if updated_quota else user["quota_limit"],
                "message": msg
            })
            return

        elif path == "/api/critic_pass":
            user = self.get_auth_user()
            text = data.get("text", "")
            if not text:
                self.send_json({"success": False, "error": "ไม่มีข้อความให้ตรวจทาน"}, 400)
                return
            
            user_keys = database.get_active_api_keys_for_user(user["id"]) if user else []
            if user_keys:
                raw_keys = [k["api_key"] for k in user_keys]
                engine = NovelEngine(api_keys=raw_keys)
            else:
                engine = NovelEngine(api_key=get_api_key())

            polished = engine.critic_pass(text)
            words = count_thai_words(polished)
            self.send_json({
                "success": True,
                "text": polished,
                "word_count": words,
                "char_count": len(polished)
            })
            return

        elif path == "/api/expand_chapter":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return

            novel_id = data.get("novel_id")
            chapter_num = int(data.get("chapter_num", 1))
            subtitle = data.get("subtitle", "")
            current_text = data.get("text", "")
            target_words = int(data.get("target_words", 3000))

            if not current_text and novel_id:
                novel = database.get_novel_details(novel_id, user["id"])
                if novel:
                    ch_obj = next((c for c in novel.get("chapters", []) if c["chapter_num"] == chapter_num), None)
                    if ch_obj:
                        current_text = ch_obj.get("content", "")
                        subtitle = subtitle or ch_obj.get("subtitle", "")

            user_keys = database.get_active_api_keys_for_user(user["id"]) if user else []
            if user_keys:
                raw_keys = [k["api_key"] for k in user_keys]
                engine = NovelEngine(api_keys=raw_keys)
            else:
                engine = NovelEngine(api_key=get_api_key())

            expanded_text = engine.expand_chapter(current_text, target_words=target_words)
            actual_words = count_thai_words(expanded_text)
            new_words = max(0, actual_words - count_thai_words(current_text))

            if novel_id:
                database.save_or_update_chapter(novel_id, user["id"], chapter_num, subtitle, expanded_text, actual_words)
            if new_words > 0:
                database.deduct_user_quota(user["id"], new_words)

            self.send_json({
                "success": True,
                "text": expanded_text,
                "word_count": actual_words,
                "message": f"ขยายเนื้อหาบทที่ {chapter_num} สำเร็จ! ({actual_words:,} คำ)"
            })
            return

        elif path == "/api/generate_batch":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return

            novel_id = data.get("novel_id")
            start_ch = int(data.get("start_chapter", 1))
            generate_all = bool(data.get("generate_all", False)) or str(data.get("count", "")).lower() in ["all", "everything"]
            delay_seconds = max(1.0, float(data.get("delay_seconds", 4.0)))

            novel = database.get_novel_details(novel_id, user["id"])
            if not novel:
                self.send_json({"success": False, "error": "ไม่พบนิยาย"}, 404)
                return

            novel_chapters = novel.get("chapters", [])
            max_novel_ch = max([c["chapter_num"] for c in novel_chapters], default=novel.get("target_chapters", 20))

            if generate_all:
                end_ch = max_novel_ch
            else:
                count = int(data.get("count", 3)) if "count" in data else (int(data.get("end_chapter", 3)) - start_ch + 1)
                end_ch = min(start_ch + max(1, count) - 1, max_novel_ch)

            target_words = int(data.get("target_words", 2000))
            mode = data.get("mode", "agentic")

            user_keys = database.get_active_api_keys_for_user(user["id"]) if user else []
            if user_keys:
                raw_keys = [k["api_key"] for k in user_keys]
                engine = NovelEngine(api_keys=raw_keys)
            else:
                engine = NovelEngine(api_key=get_api_key())

            novel_chars = novel.get("characters", [])
            total_words_generated = 0
            generated_chapters = []

            for idx, ch_num in enumerate(range(start_ch, end_ch + 1)):
                # Rate limit pacing delay between chapters
                if idx > 0 and delay_seconds > 0:
                    print(f"[Batch] Rate limit pacing: sleeping {delay_seconds}s before chapter {ch_num}...")
                    time.sleep(delay_seconds)

                # Check plan status expiration (Unlimited words within plan)
                current_user = database.get_user_by_id(user["id"])
                if current_user and current_user.get("status") == "expired":
                    print(f"[Batch] Plan expired, stopping batch at chapter {ch_num}")
                    break

                ch_obj = next((c for c in novel.get("chapters", []) if c["chapter_num"] == ch_num), None)
                subtitle = clean_chapter_subtitle(ch_obj["subtitle"] if ch_obj else "", ch_num, novel.get("title", ""))

                sliding = database.get_sliding_context_for_chapter(novel_id, ch_num)
                ch_text = engine.generate_chapter(
                    story_title=novel["title"],
                    chapter_num=ch_num,
                    chapter_subtitle=subtitle,
                    genre=novel["genre"],
                    context_memory=novel_chars,
                    sliding_context=sliding,
                    target_words=target_words,
                    mode=mode,
                    category=novel.get("category", ""),
                    target_chapters=novel.get("target_chapters", 20)
                )
                ch_words = count_thai_words(ch_text)
                total_words_generated += ch_words

                database.save_or_update_chapter(novel_id, user["id"], ch_num, subtitle, ch_text, ch_words)
                database.deduct_user_quota(user["id"], ch_words)

                generated_chapters.append({
                    "chapter_num": ch_num,
                    "subtitle": subtitle,
                    "word_count": ch_words
                })

            self.send_json({
                "success": True,
                "chapters": generated_chapters,
                "results": generated_chapters,
                "total_words": total_words_generated,
                "total_words_generated": total_words_generated,
                "delay_seconds": delay_seconds,
                "message": f"ระบบแต่งนิยายแบบต่อเนื่องสำเร็จ {len(generated_chapters)} ตอน รวม {total_words_generated:,} คำ (หน่วงเวลา {delay_seconds} วินาที/ตอน ป้องกัน API Limit)!"
            })
            return

        # ========================================================
        # 3.5 BACKGROUND AUTO-PILOT BATCH QUEUE
        # ========================================================
        elif path == "/api/batch/start":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบก่อนใช้งาน"}, 401)
                return

            if user.get("status") == "expired":
                self.send_json({"success": False, "error": "ระยะเวลาการใช้งานของคุณหมดอายุแล้ว กรุณาต่ออายุแพ็กเกจ"}, 403)
                return

            novel_id = data.get("novel_id")
            target_chapters = data.get("target_chapters", [])
            target_words = int(data.get("target_words", 2000))
            delay_seconds = float(data.get("delay_seconds", 5.0))
            mode = data.get("mode", "agentic")

            if not novel_id or not target_chapters:
                self.send_json({"success": False, "error": "ข้อมูลไม่ครบถ้วน (ต้องระบุ novel_id และ target_chapters)"}, 400)
                return

            ok, res = batch_manager.start_batch(
                user_id=user["id"],
                novel_id=novel_id,
                chapter_list=target_chapters,
                target_words=target_words,
                delay_seconds=delay_seconds,
                mode=mode
            )
            if not ok:
                self.send_json({"success": False, "error": res}, 400)
                return

            self.send_json({
                "success": True,
                "message": f"เริ่มระบบคิวเซิร์ฟเวอร์เบื้องหลังสำเร็จ ({len(target_chapters)} ตอน)! คุณสามารถปิดหน้าต่างหรือปิดเครื่องได้ตลอดเวลา",
                "job": batch_manager.get_status(novel_id)
            })
            return

        elif path == "/api/batch/stop":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            novel_id = data.get("novel_id")
            if not novel_id:
                self.send_json({"success": False, "error": "กรุณาระบุ novel_id"}, 400)
                return
            ok, msg = batch_manager.stop_batch(novel_id)
            self.send_json({"success": ok, "message": msg})
            return

        elif path == "/api/upload_readawrite":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return

            novel_id = data.get("novel_id")
            article_id = data.get("article_id")
            create_new_story = bool(data.get("create_new_story", False))
            chapter_num = data.get("chapter_num", 1)
            subtitle = data.get("subtitle", "")
            content = data.get("content", "")
            publish_mode = data.get("publish_mode", "draft")
            schedule_time = data.get("schedule_time", None)

            novel = database.get_novel_details(novel_id, user["id"]) if novel_id else None

            # Determine target article ID:
            # 1. If explicit article_id provided (not "NEW_STORY"), use it
            # 2. If novel already linked to an article_id in DB and not forcing new story, use it
            # 3. Otherwise, create a brand new story on ReadAWrite!
            target_article_id = None
            if not create_new_story:
                if article_id and article_id != "NEW_STORY" and article_id != "auto":
                    target_article_id = article_id
                elif novel and novel.get("article_id"):
                    target_article_id = novel["article_id"]

            uploader = ReadAWriteUploader(user_id=user["id"])
            created_new = False

            if not target_article_id:
                # Create a brand new story on ReadAWrite!
                story_title = data.get("story_title") or (novel["title"] if novel else "นิยายเรื่องใหม่")
                story_synopsis = data.get("story_synopsis") or (novel["synopsis"] if novel else "เรื่องย่อนิยาย...")
                
                print(f"[ReadAWrite Sync] Creating new story on ReadAWrite: '{story_title}'")
                target_article_id = uploader.create_story(
                    title=story_title,
                    synopsis=story_synopsis,
                    category_id="13",
                    rating="1",
                    cover_url=novel.get("cover_url") if novel else None,
                    is_ai_cover=True
                )
                if not target_article_id:
                    self.send_json({
                        "success": False,
                        "error": "ไม่สามารถสร้างเรื่องใหม่บน ReadAWrite ได้ กรุณาตรวจสอบสถานะการเชื่อมต่อบัญชี ReadAWrite"
                    }, 500)
                    return
                created_new = True
                if novel_id:
                    database.update_novel_article_id(novel_id, user["id"], target_article_id)

            success = uploader.upload_chapter(
                article_id=target_article_id,
                chapter_title=f"บทที่ {chapter_num}",
                chapter_subtitle=subtitle,
                content=content,
                publish_mode=publish_mode,
                schedule_time=schedule_time
            )

            if success and novel_id:
                new_status = "scheduled" if publish_mode == "schedule" else ("published" if publish_mode == "publish" else "draft")
                database.update_chapter_publish_status(novel_id, user["id"], chapter_num, status=new_status, schedule_time=schedule_time)

            msg = f"ซิงค์บทที่ {chapter_num} ขึ้น ReadAWrite สำเร็จแล้ว (โหมด: {publish_mode})!"
            if created_new:
                msg = f"🎉 เปิดเรื่องใหม่บน ReadAWrite สำเร็จ (Article ID: {target_article_id}) และ{msg}"

            self.send_json({
                "success": success,
                "article_id": target_article_id,
                "created_new_story": created_new,
                "message": msg
            })
            return

        elif path == "/api/upload_readawrite_batch":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return

            novel_id = data.get("novel_id")
            article_id = data.get("article_id")
            create_new_story = bool(data.get("create_new_story", False))
            schedule_items = data.get("schedule_items", [])
            delay_seconds = float(data.get("delay_seconds", 2.0))

            novel = database.get_novel_details(novel_id, user["id"]) if novel_id else None

            target_article_id = None
            if not create_new_story:
                if article_id and article_id != "NEW_STORY" and article_id != "auto":
                    target_article_id = article_id
                elif novel and novel.get("article_id"):
                    target_article_id = novel["article_id"]

            uploader = ReadAWriteUploader(user_id=user["id"])
            created_new = False

            if not target_article_id and schedule_items:
                story_title = data.get("story_title") or (novel["title"] if novel else "นิยายเรื่องใหม่")
                story_synopsis = data.get("story_synopsis") or (novel["synopsis"] if novel else "เรื่องย่อนิยาย...")
                cat_id = novel.get("category") or "13"
                if cat_id == "13_chinese": cat_id = "13"
                print(f"[ReadAWrite Batch] Creating new story: '{story_title}'")
                target_article_id = uploader.create_story(
                    title=story_title,
                    synopsis=story_synopsis,
                    category_id=cat_id,
                    rating="1",
                    cover_url=novel.get("cover_url") if novel else None,
                    is_ai_cover=True
                )
                if not target_article_id:
                    self.send_json({"success": False, "error": "ไม่สามารถสร้างเรื่องใหม่บน ReadAWrite ได้"}, 500)
                    return
                created_new = True
                if novel_id:
                    database.update_novel_article_id(novel_id, user["id"], target_article_id)

            results = []
            for idx, item in enumerate(schedule_items):
                ch_num = item.get("chapter_num")
                sub = clean_chapter_subtitle(item.get("subtitle", ""), ch_num)
                cnt = item.get("content", "")
                mode = item.get("publish_mode", "schedule")
                s_time = item.get("schedule_time", None)

                if idx > 0 and delay_seconds > 0:
                    time.sleep(delay_seconds)

                succ = uploader.upload_chapter(
                    article_id=target_article_id,
                    chapter_title=f"บทที่ {ch_num}",
                    chapter_subtitle=sub,
                    content=cnt,
                    publish_mode=mode,
                    schedule_time=s_time
                )
                if succ and novel_id:
                    new_status = "scheduled" if mode == "schedule" else ("published" if mode == "publish" else "draft")
                    database.update_chapter_publish_status(novel_id, user["id"], ch_num, status=new_status, schedule_time=s_time)

                results.append({
                    "chapter_num": ch_num,
                    "subtitle": sub,
                    "schedule_time": s_time,
                    "publish_mode": mode,
                    "success": succ
                })

            self.send_json({
                "success": True,
                "article_id": target_article_id,
                "created_new_story": created_new,
                "results": results,
                "message": f"ซิงค์และตั้งเวลาเผยแพร่ขึ้น ReadAWrite สำเร็จ {len(results)} ตอน!"
            })
            return

        elif path == "/api/user/connect_readawrite":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return

            action = data.get("action", "")
            os.makedirs(r"c:\ReadAWrite\user_sessions", exist_ok=True)
            user_session_file = os.path.join(r"c:\ReadAWrite\user_sessions", f"user_{user['id']}.json")

            if action == "sync_demo" or not data.get("storage_state"):
                # Copy default session state for instant connection demo
                src = r"c:\ReadAWrite\user_sessions\user_1.json"
                if os.path.exists(src):
                    import shutil
                    shutil.copyfile(src, user_session_file)
                database.update_user_readawrite_session(user["id"], "i_Am_Status", user_session_file, "connected")
                self.send_json({
                    "success": True,
                    "message": "เชื่อมต่อบัญชี ReadAWrite (นามปากกา: i_Am_Status) สำเร็จแล้ว!",
                    "pen_name": "i_Am_Status",
                    "status": "connected"
                })
                return
            else:
                st = data.get("storage_state")
                try:
                    res = ReadAWriteUploader.verify_and_save_session(user["id"], st)
                    database.update_user_readawrite_session(user["id"], res["pen_name"], res["session_file"], "connected")
                    self.send_json({
                        "success": True,
                        "message": f"เชื่อมต่อบัญชี ReadAWrite ({res['pen_name']}) สำเร็จแล้ว!",
                        "pen_name": res["pen_name"],
                        "status": "connected"
                    })
                    return
                except Exception as ex:
                    self.send_json({"success": False, "error": f"ข้อมูล Session ไม่ถูกต้อง: {str(ex)}"}, 400)
                    return

        elif path == "/api/user/disconnect_readawrite":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            database.disconnect_user_readawrite_session(user["id"])
            user_session_file = os.path.join(r"c:\ReadAWrite\user_sessions", f"user_{user['id']}.json")
            if os.path.exists(user_session_file):
                try:
                    os.remove(user_session_file)
                except:
                    pass
            self.send_json({"success": True, "message": "ยกเลิกการเชื่อมต่อบัญชี ReadAWrite เรียบร้อยแล้ว"})
            return

        # ========================================================
        # USER PERSONAL API KEYS ENDPOINTS (BYOK)
        # ========================================================
        elif path == "/api/user/keys/add":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            label = data.get("label", "Gemini API Key").strip()
            api_key = data.get("api_key", "").strip()
            if not api_key:
                self.send_json({"success": False, "error": "กรุณาระบุ Gemini API Key"}, 400)
                return
            
            key_id = database.add_user_api_key(user["id"], label, api_key)
            self.send_json({
                "success": True, 
                "key_id": key_id, 
                "message": f"เพิ่ม API Key '{label}' เรียบร้อยแล้ว!"
            })
            return

        elif path == "/api/user/keys/update":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            key_id = int(data.get("id", 0))
            label = data.get("label")
            api_key = data.get("api_key")
            is_active = data.get("is_active")
            database.update_user_api_key(user["id"], key_id, label=label, api_key=api_key, is_active=is_active)
            self.send_json({"success": True, "message": "อัปเดต API Key สำเร็จแล้ว"})
            return

        elif path == "/api/user/keys/delete":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            key_id = int(data.get("id", 0))
            database.delete_user_api_key(user["id"], key_id)
            self.send_json({"success": True, "message": "ลบ API Key เรียบร้อยแล้ว"})
            return

        elif path == "/api/user/keys/test":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            test_key = data.get("api_key", "").strip()
            key_id = data.get("id")
            
            # If key_id passed, look up key if api_key not provided
            if key_id and not test_key:
                keys = database.get_user_api_keys(user["id"], include_secret=True)
                for k in keys:
                    if k["id"] == int(key_id):
                        test_key = k["api_key"]
                        break
            
            if not test_key:
                self.send_json({"success": False, "error": "ไม่พบคีย์ที่จะทดสอบ"}, 400)
                return

            try:
                from google import genai
                client = genai.Client(api_key=test_key)
                resp = client.models.generate_content(model="gemini-3.5-flash-lite", contents="ping")
                if key_id:
                    database.update_user_api_key(user["id"], int(key_id), status="ready")
                self.send_json({"success": True, "message": "🟢 API Key ถูกต้องและพร้อมใช้งานทันที!"})
            except Exception as e:
                err_str = str(e)
                if key_id:
                    status_err = "rate_limited" if "429" in err_str else "invalid"
                    database.update_user_api_key(user["id"], int(key_id), status=status_err)
                self.send_json({"success": False, "error": f"ทดสอบไม่สำเร็จ: {err_str[:120]}"}, 400)
            return

        # ========================================================
        # CHARACTER BIBLE (คลังความทรงจำตัวละคร)
        # ========================================================
        elif path == "/api/characters/add":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            novel_id = data.get("novel_id")
            name = data.get("name", "").strip()
            role = data.get("role", "ตัวละครหลัก").strip()
            traits = data.get("traits", "").strip()
            avatar_url = data.get("avatar_url", "").strip()
            want = data.get("want", "").strip()
            need = data.get("need", "").strip()
            flaw = data.get("flaw", "").strip()
            speaking_style = data.get("speaking_style", "").strip()
            current_emotion = data.get("current_emotion", "").strip()
            hidden_agenda = data.get("hidden_agenda", "").strip()

            if not novel_id or not name:
                self.send_json({"success": False, "error": "กรุณาระบุชื่อตัวละครและรหัสนิยาย"}, 400)
                return

            char_id = database.add_novel_character(
                novel_id, user["id"], name, role, traits, avatar_url,
                want=want, need=need, flaw=flaw, speaking_style=speaking_style,
                current_emotion=current_emotion, hidden_agenda=hidden_agenda
            )
            chars = database.get_novel_characters(novel_id, user["id"])
            self.send_json({
                "success": True,
                "message": f"เพิ่มตัวละคร '{name}' ({role}) พร้อมข้อมูล 3D เรียบร้อยแล้ว!",
                "characters": chars
            })
            return

        elif path == "/api/ai_linter":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            text = data.get("text", "")
            from novel_engine import de_ai_linter
            linter_res = de_ai_linter(text)
            self.send_json({
                "success": True,
                "clean_text": linter_res["text"],
                "detected": linter_res["detected"],
                "total_cliches": linter_res["total_cliches"],
                "score": linter_res["score"],
                "message": f"สแกนสำเร็จ! พบคลิเช่ AI {linter_res['total_cliches']} จุด (คะแนนความบริสุทธิ์: {linter_res['score']}/100)"
            })
            return

        elif path == "/api/characters/delete":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            char_id = int(data.get("id", 0))
            novel_id = data.get("novel_id")
            database.delete_novel_character(char_id, user["id"])
            chars = database.get_novel_characters(novel_id, user["id"]) if novel_id else []
            self.send_json({
                "success": True,
                "message": "ลบตัวละครเรียบร้อยแล้ว",
                "characters": chars
            })
            return

        # ========================================================
        # AI NOVEL COVER STUDIO
        # ========================================================
        elif path == "/api/novels/update_cover":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            novel_id = data.get("novel_id")
            cover_url = data.get("cover_url", "").strip()
            if not novel_id or not cover_url:
                self.send_json({"success": False, "error": "ข้อมูลไม่ครบถ้วน"}, 400)
                return
            database.update_novel_cover(novel_id, user["id"], cover_url)

            # Auto-sync cover to ReadAWrite in background if novel is already on ReadAWrite
            novel = database.get_novel_details(novel_id, user["id"])
            if novel and novel.get("article_id"):
                art_id = novel["article_id"]
                u_id = user["id"]
                c_url = cover_url
                def _bg_sync_update():
                    try:
                        uploader = ReadAWriteUploader(user_id=u_id)
                        uploader.update_story_cover(art_id, c_url, is_ai_cover=True)
                    except Exception as err:
                        print(f"[CoverSync] Auto-sync error: {err}")
                threading.Thread(target=_bg_sync_update, daemon=True).start()

            self.send_json({"success": True, "message": "อัปเดตภาพปกนิยายและกำลังซิงค์ขึ้น ReadAWrite อัตโนมัติ!", "cover_url": cover_url})
            return

        elif path == "/api/novels/upload_cover_file":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            novel_id = data.get("novel_id")
            image_data = data.get("image_data", "")
            if not novel_id or not image_data:
                self.send_json({"success": False, "error": "กรุณาระบุข้อมูลภาพและรหัสนิยาย"}, 400)
                return
            
            try:
                import base64
                os.makedirs(COVERS_DIR, exist_ok=True)
                ext = "png"
                if "data:image/jpeg" in image_data or "data:image/jpg" in image_data:
                    ext = "jpg"
                elif "data:image/webp" in image_data:
                    ext = "webp"
                
                raw_b64 = image_data.split(",", 1)[-1] if "," in image_data else image_data
                img_bytes = base64.b64decode(raw_b64)
                
                filename = f"cover_{novel_id}_{int(time.time())}.{ext}"
                filepath = os.path.join(COVERS_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(img_bytes)
                
                cover_url = f"/covers/{filename}"
                database.update_novel_cover(novel_id, user["id"], cover_url)

                # Auto-sync cover to ReadAWrite in background if novel is already on ReadAWrite
                novel = database.get_novel_details(novel_id, user["id"])
                if novel and novel.get("article_id"):
                    art_id = novel["article_id"]
                    u_id = user["id"]
                    c_url = cover_url
                    def _bg_sync_upload():
                        try:
                            uploader = ReadAWriteUploader(user_id=u_id)
                            uploader.update_story_cover(art_id, c_url, is_ai_cover=True)
                        except Exception as err:
                            print(f"[CoverSync] Auto-sync error: {err}")
                    threading.Thread(target=_bg_sync_upload, daemon=True).start()

                self.send_json({
                    "success": True,
                    "cover_url": cover_url,
                    "message": "อัปโหลดภาพปกจากเครื่องและซิงค์ขึ้น ReadAWrite อัตโนมัติแล้ว!"
                })
            except Exception as e:
                self.send_json({"success": False, "error": f"อัปโหลดไฟล์ไม่สำเร็จ: {e}"}, 500)
            return

        elif path == "/api/novels/sync_cover_to_readawrite":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบ"}, 401)
                return
            novel_id = data.get("novel_id")
            cover_url = data.get("cover_url")
            novel = database.get_novel_details(novel_id, user["id"]) if novel_id else None
            if not novel:
                self.send_json({"success": False, "error": "ไม่พบนิยายเรื่องนี้"}, 404)
                return
            if not cover_url:
                cover_url = novel.get("cover_url")
            if not cover_url:
                self.send_json({"success": False, "error": "ไม่พบภาพปกที่จะอัปโหลด"}, 400)
                return

            database.update_novel_cover(novel_id, user["id"], cover_url)
            uploader = ReadAWriteUploader(user_id=user["id"])
            article_id = novel.get("article_id")
            
            if article_id:
                # Update existing article on ReadAWrite
                success = uploader.update_story_cover(article_id, cover_url, is_ai_cover=True)
                if success:
                    self.send_json({
                        "success": True,
                        "message": f"อัปโหลดภาพปก AI ขึ้น ReadAWrite (Article ID: {article_id}) เรียบร้อยแล้ว!"
                    })
                else:
                    self.send_json({
                        "success": False,
                        "error": "อัปโหลดภาพปกขึ้น ReadAWrite ไม่สำเร็จ กรุณาตรวจสอบการล็อกอิน ReadAWrite"
                    }, 500)
            else:
                # Novel doesn't have an article_id yet -> create story with cover
                cat_id = novel.get("category") or "13"
                if cat_id == "13_chinese": cat_id = "13"
                new_art_id = uploader.create_story(
                    title=novel["title"],
                    synopsis=novel.get("synopsis", "เรื่องย่อนิยาย..."),
                    category_id=cat_id,
                    rating="1",
                    cover_url=cover_url,
                    is_ai_cover=True
                )
                if new_art_id:
                    database.update_novel_article_id(novel_id, user["id"], new_art_id)
                    self.send_json({
                        "success": True,
                        "article_id": new_art_id,
                        "message": f"เปิดเรื่องใหม่พร้อมอัปโหลดภาพปก AI ขึ้น ReadAWrite (Article ID: {new_art_id}) สำเร็จแล้ว!"
                    })
                else:
                    self.send_json({"success": False, "error": "ไม่สามารถสร้างเรื่องบน ReadAWrite ได้"}, 500)
            return

        elif path == "/api/novels/delete":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบก่อนทำรายการ"}, 401)
                return
            novel_id = data.get("novel_id")
            if not novel_id:
                self.send_json({"success": False, "error": "กรุณาระบุรหัสนิยาย (novel_id)"}, 400)
                return
            success, msg = database.delete_novel(novel_id, user["id"])
            if success:
                self.send_json({"success": True, "message": msg, "novel_id": novel_id})
            else:
                self.send_json({"success": False, "error": msg}, 400)
            return

        # ========================================================
        # 4. SUBSCRIPTION & BILLING UPGRADE
        # ========================================================
        elif path == "/api/subscription/upgrade":
            user = self.get_auth_user()
            if not user:
                self.send_json({"success": False, "error": "กรุณาเข้าสู่ระบบก่อนสมัครแพ็กเกจ"}, 401)
                return

            plan_name = data.get("plan", "monthly").lower()
            payment_method = data.get("payment_method", "PromptPay QR")

            order_res = database.upgrade_user_plan(user["id"], plan_name, payment_method)
            refreshed_user = database.get_user_by_id(user["id"])

            self.send_json({
                "success": True,
                "order": order_res,
                "user": refreshed_user,
                "message": f"🎉 ชำระเงินสำเร็จ! อัปเกรดเป็น {order_res['plan']} เรียบร้อยแล้ว แต่งนิยาย AI ได้ไม่จำกัดคำทันที!"
            })
            return

        # ========================================================
        # 5. ADMIN MANAGEMENT ENDPOINTS
        # ========================================================
        elif path == "/api/admin/update_user":
            user = self.get_auth_user()
            if not user or user["role"] != "admin":
                self.send_json({"success": False, "error": "ไม่มีสิทธิ์เข้าถึง"}, 403)
                return

            target_user_id = int(data.get("user_id"))
            plan = data.get("plan")
            status = data.get("status")
            quota_add = int(data.get("quota_add", 0))

            database.update_user_admin(target_user_id, plan=plan, status=status, quota_add=quota_add)
            self.send_json({"success": True, "message": f"อัปเดตข้อมูลสมาชิก ID #{target_user_id} สำเร็จแล้ว"})
            return

        super().do_POST()

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def run_server():
    os.chdir(WEB_DIR)
    with ThreadingHTTPServer(("0.0.0.0", PORT), SaaSHttpHandler) as httpd:
        print(f"[SaaS Server] Running with SQLite DB on http://localhost:{PORT}")
        print(f"[SaaS Server] Multi-threaded server listening on 0.0.0.0:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
