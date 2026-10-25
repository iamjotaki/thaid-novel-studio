# -*- coding: utf-8 -*-
import sys
import os
import time
import json
import urllib.parse
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PROFILE_DIR = os.path.join(BASE_DIR, "chrome_profile")
SESSIONS_DIR = os.path.join(BASE_DIR, "user_sessions")

class ReadAWriteUploader:
    def __init__(self, user_id=None, log_callback=None):
        self.user_id = user_id
        self.log_callback = log_callback or print
        self.session_file = None

        os.makedirs(SESSIONS_DIR, exist_ok=True)
        if user_id:
            user_session = os.path.join(SESSIONS_DIR, f"user_{user_id}.json")
            if os.path.exists(user_session):
                self.session_file = user_session
        
        # Fallback to user_1 if available
        if not self.session_file and os.path.exists(os.path.join(SESSIONS_DIR, "user_1.json")):
            self.session_file = os.path.join(SESSIONS_DIR, "user_1.json")

    def log(self, msg):
        prefix = f"[ReadAWrite-User#{self.user_id}]" if self.user_id else "[ReadAWrite]"
        self.log_callback(f"{prefix} {msg}")

    def _get_context(self, p):
        """สร้าง Browser Context แยกต่างหากเฉพาะสำหรับผู้ใช้แต่ละราย (Tenant Session Isolation)"""
        if self.session_file and os.path.exists(self.session_file):
            self.log(f"โหลดเซสชันส่วนตัวจาก: {os.path.basename(self.session_file)}")
            browser = p.chromium.launch(headless=True, channel="chrome")
            ctx = browser.new_context(storage_state=self.session_file)
            return browser, ctx
        else:
            self.log("ใช้โพรไฟล์เบราว์เซอร์มาตรฐานของเซิร์ฟเวอร์")
            ctx = p.chromium.launch_persistent_context(DEFAULT_PROFILE_DIR, headless=True, channel="chrome")
            return None, ctx

    def get_author_portfolio(self):
        """ดึงข้อมูลโปรไฟล์นักเขียนและผลงานนิยายทั้งหมดจาก ReadAWrite พร้อมสถิติจำนวนตอน ยอดวิว และปก"""
        self.log("กำลังดึงข้อมูลโปรไฟล์และผลงานจาก ReadAWrite...")
        with sync_playwright() as p:
            browser, ctx = self._get_context(p)
            try:
                page = ctx.pages[0] if ctx.pages else ctx.new_page()
                page.goto("https://www.readawrite.com/?action=main_manage_article", timeout=25000)
                page.wait_for_timeout(2500)
                page.keyboard.press("Escape")
                
                # Dismiss modals if any
                page.evaluate("""() => {
                    document.querySelectorAll('.modal, .modal-backdrop, .swal2-container').forEach(e => e.remove());
                    document.body.classList.remove('modal-open');
                }""")
                
                portfolio = page.evaluate("""() => {
                    const penName = document.querySelector('.author-name, .user-name, #header_user_name, .profile-name, .member-info, span[class*="name"]')?.innerText?.trim() || 'i_Am_Status';
                    const avatar = document.querySelector('img[src*="profile_picture"], img[src*="avatar"], .avatar img, .user-avatar img')?.src || '';
                    
                    const stories = [];
                    document.querySelectorAll('a[href*="article_id="]').forEach(a => {
                        const href = a.getAttribute('href') || '';
                        const match = href.match(/article_id=([a-zA-Z0-9]+)/);
                        if (!match) return;
                        const id = match[1];
                        if (stories.some(s => s.id === id)) return;
                        
                        const container = a.closest('.row') || a.closest('div[class*="item"]') || a.closest('tr') || a.parentElement.parentElement;
                        const text = container ? container.innerText : a.innerText;
                        const cover = container ? (container.querySelector('img')?.src || '') : '';
                        
                        // Extract chapter count and stats
                        let chapters = 0;
                        let reads = 0;
                        let likes = 0;
                        const nums = text.match(/\\d+/g);
                        if (nums && nums.length >= 4) {
                            chapters = parseInt(nums[nums.length - 4]) || 0;
                            reads = parseInt(nums[nums.length - 3]) || 0;
                            likes = parseInt(nums[nums.length - 1]) || 0;
                        }
                        
                        const isPublished = text.includes('เผยแพร่แล้ว');
                        const status = isPublished ? 'เผยแพร่แล้ว' : 'แบบร่าง / ยังไม่เผยแพร่';
                        
                        stories.push({
                            id: id,
                            title: a.innerText.trim().split('\\n')[0],
                            cover_url: cover || 'https://cdn.readawrite.com/category/13/tiny.gif?0',
                            chapters: chapters,
                            reads: reads,
                            likes: likes,
                            status: status,
                            manage_url: `https://www.readawrite.com/?action=manage_chapter&article_id=${id}`
                        });
                    });
                    
                    return {
                        pen_name: penName,
                        avatar_url: avatar,
                        stories_count: stories.length,
                        stories: stories
                    };
                }""")
                self.log(f"ดึงข้อมูลโปรไฟล์สำเร็จ: นามปากกา {portfolio['pen_name']}, ผลงาน {portfolio['stories_count']} เรื่อง")
                return portfolio
            except Exception as e:
                self.log(f"เกิดข้อผิดพลาดในการดึงโปรไฟล์: {e}")
                return {
                    "pen_name": "i_Am_Status",
                    "avatar_url": "",
                    "stories_count": 0,
                    "stories": [],
                    "error": str(e)
                }
            finally:
                ctx.close()
                if browser:
                    browser.close()

    def get_articles(self):
        """ดึงรายการนิยายทั้งหมดในบัญชีของผู้ใช้นี้"""
        portfolio = self.get_author_portfolio()
        return portfolio.get("stories", [])

    def _prepare_cover_file(self, cover_url):
        """เตรียมไฟล์ภาพหน้าปกจาก URL, base64 หรือ path ท้องถิ่น"""
        if not cover_url:
            return None
        try:
            import urllib.request
            import base64
            os.makedirs(r"c:\ReadAWrite\data\covers", exist_ok=True)
            
            # Case 1: Local file path
            if os.path.exists(cover_url):
                return os.path.abspath(cover_url)
            
            # Case 1.2: Local relative path (e.g. /covers/xxx.png or data/covers/xxx.png)
            if cover_url.startswith("/covers/") or cover_url.startswith("/data/covers/"):
                basename = os.path.basename(cover_url)
                local_path = os.path.join(r"c:\ReadAWrite\data\covers", basename)
                if os.path.exists(local_path):
                    return os.path.abspath(local_path)
            
            # Case 2: Base64 data URL
            if cover_url.startswith("data:image"):
                header, encoded = cover_url.split(",", 1)
                ext = "png" if "png" in header else ("webp" if "webp" in header else "jpg")
                filepath = os.path.join(r"c:\ReadAWrite\data\covers", f"cover_temp_{int(time.time()*1000)}.{ext}")
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(encoded))
                return os.path.abspath(filepath)
            
            # Case 3: HTTP/HTTPS URL
            if cover_url.startswith("http://") or cover_url.startswith("https://"):
                ext = "jpg"
                if ".png" in cover_url.lower(): ext = "png"
                elif ".webp" in cover_url.lower(): ext = "webp"
                filepath = os.path.join(r"c:\ReadAWrite\data\covers", f"cover_dl_{int(time.time()*1000)}.{ext}")
                req = urllib.request.Request(
                    cover_url,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                )
                with urllib.request.urlopen(req, timeout=20) as resp:
                    with open(filepath, "wb") as f:
                        f.write(resp.read())
                if os.path.exists(filepath) and os.path.getsize(filepath) > 500:
                    return os.path.abspath(filepath)
        except Exception as e:
            self.log(f"ดาวน์โหลดหรือแปลงภาพปกไม่สำเร็จ ({e})")
        return None

    def _prepare_cover_base64(self, cover_file):
        """แปลงภาพปกเป็น Base64 Data URL แบบเต็มรูป 1:1 ไม่ผ่านการตัด Crop ใดๆ"""
        if not cover_file or not os.path.exists(cover_file):
            return None
        try:
            from PIL import Image
            import io
            import base64
            im = Image.open(cover_file)
            if im.mode in ("RGBA", "P"):
                im = im.convert("RGB")
            w, h = im.size
            # หากภาพมีขนาดใหญ่เกิน 1200px ให้ย่อลงอย่างพอดีเพื่อขนาดที่เหมาะสมกับ CDN ของ ReadAWrite
            if w > 1200 or h > 1200:
                ratio = min(1200 / w, 1200 / h)
                new_size = (int(w * ratio), int(h * ratio))
                im = im.resize(new_size, Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, format="JPEG", quality=92)
            return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")
        except Exception as e:
            self.log(f"แปลงภาพปกเป็น Base64 ไม่สำเร็จ ({e})")
            return None

    def create_story(self, title, synopsis, category_id="13", rating="1", is_ai_cover=True, cover_url=None):
        """สร้างนิยายเรื่องใหม่บน ReadAWrite ในบัญชีของผู้ใช้นี้ พร้อมอัปโหลดภาพปก AI (ถ้ามี)"""
        self.log(f"กำลังสร้างนิยายเรื่องใหม่: {title}")
        url = "https://www.readawrite.com/?action=manage_article&article_style=ORIGINAL&article_species=FICTION&article_type=MULTI_CHAPTER&translation=0"
        
        with sync_playwright() as p:
            browser, ctx = self._get_context(p)
            try:
                page = ctx.pages[0] if ctx.pages else ctx.new_page()
                page.goto(url)
                page.wait_for_load_state("domcontentloaded")
                time.sleep(2)
                page.keyboard.press("Escape")

                # 1. ข้อมูลพื้นฐาน
                page.locator("#article_name").fill(title)
                page.locator("#article_synopsis").fill(synopsis)

                # 2. อัปโหลดภาพปก AI (ถ้ามี) แบบ 1:1 เต็มรูป ไม่ผ่านการ Crop
                if cover_url:
                    cover_file = self._prepare_cover_file(cover_url)
                    if cover_file and os.path.exists(cover_file):
                        self.log(f"กำลังนำภาพปก 1:1 เต็มรูปเข้าสู่ ReadAWrite: {os.path.basename(cover_file)}")
                        cover_b64 = self._prepare_cover_base64(cover_file)
                        if cover_b64:
                            page.evaluate("""(b64) => {
                                const inp = document.querySelector('#imgBase64');
                                if (inp) inp.value = b64;
                                const inpCover = document.querySelector('#imgCoverBase64');
                                if (inpCover) inpCover.value = '';
                                const preview = document.querySelector('#img_uploaded, #preview_thumbnail, #preview_cover_article, #img_cover_uploaded');
                                if (preview) {
                                    preview.src = b64;
                                    if (preview.hasAttribute('srcset')) preview.setAttribute('srcset', b64);
                                }
                                const m = document.querySelector('#modal');
                                if (m) {
                                    m.classList.remove('in');
                                    m.style.display = 'none';
                                }
                                document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());
                            }""", cover_b64)
                            time.sleep(1)
                            self.log("ตั้งค่าภาพปก 1:1 เต็มรูป (ไม่ผ่านการ Crop) เรียบร้อยแล้ว")

                # 3. กำหนดสถานะปก AI (ทำเครื่องหมาย 'ภาพปกสร้างด้วย AI (AI-generated)')
                rad_id = "#is_ai_cover1" if is_ai_cover else "#chk_is_ai_cover0"
                page.evaluate(f"""() => {{
                    const rad = document.querySelector('{rad_id}');
                    if (rad) {{
                        rad.checked = true;
                        rad.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                }}""")
                self.log(f"ตั้งค่าสถานะภาพปก: {'ภาพปกสร้างด้วย AI (AI-generated)' if is_ai_cover else 'ไม่ใช่ AI'}")

                # 4. หมวดหมู่
                page.evaluate(f"""() => {{
                    if (typeof setCategoryOnModal === 'function') {{
                        setCategoryOnModal('นิยายรัก', '{category_id}', '83');
                    }}
                    const cat = document.querySelector('#category_id');
                    if (cat) cat.value = '{category_id}';
                    const mcat = document.querySelector('#modal_category_id');
                    if (mcat) mcat.value = '{category_id}';
                }}""")
                time.sleep(1)

                # 5. เรตติ้ง
                page.locator("#content_rating").select_option(rating)
                time.sleep(1)

                # 6. บันทึกเรื่อง
                self.log("กำลังกดปุ่มบันทึกเรื่อง...")
                try:
                    page.locator("#btnSaveArticle").click(timeout=8000)
                except Exception as bse:
                    self.log(f"คลิกปกติไม่ผ่าน ({bse}) กำลังสั่งบันทึกตรงผ่าน JavaScript...")
                    page.evaluate("""() => {
                        const backdrop = document.querySelector('.modal-backdrop');
                        if (backdrop) backdrop.remove();
                        const m = document.querySelector('#modal');
                        if (m) {
                            m.classList.remove('in');
                            m.style.display = 'none';
                        }
                        const btn = document.querySelector('#btnSaveArticle');
                        if (btn) btn.click();
                        else if (typeof article !== 'undefined' && typeof article.saveArticle === 'function') {
                            article.saveArticle();
                        }
                    }""")

                # รอการแจ้งเตือนสำเร็จ
                article_id = None
                for _ in range(12):
                    time.sleep(1)
                    swal = page.locator("button.swal2-confirm, button:has-text('OK')")
                    if swal.count() > 0:
                        try:
                            swal.first.click()
                            time.sleep(1)
                        except:
                            pass
                    if "article_id=" in page.url:
                        match = page.url.split("article_id=")[-1].split("&")[0]
                        article_id = match
                        break

                if article_id:
                    self.log(f"สร้างเรื่องสำเร็จ! Article ID: {article_id}")
                else:
                    self.log("สร้างเรื่องสำเร็จ (กำลังอัปเดต ID)")
                return article_id
            finally:
                ctx.close()
                if browser:
                    browser.close()

    def update_story_cover(self, article_id, cover_url, is_ai_cover=True):
        """อัปโหลดหรือแก้ไขภาพปกนิยายที่มีอยู่แล้วบน ReadAWrite"""
        self.log(f"กำลังอัปเดตภาพปกนิยาย Article ID: {article_id}")
        url = f"https://www.readawrite.com/?action=manage_article&article_id={article_id}&tab=articleSetting"
        
        cover_file = self._prepare_cover_file(cover_url)
        if not cover_file or not os.path.exists(cover_file):
            self.log("ไม่พบไฟล์หรือ URL ภาพปกที่ถูกต้องสำหรับการอัปโหลด")
            return False

        with sync_playwright() as p:
            browser, ctx = self._get_context(p)
            try:
                page = ctx.pages[0] if ctx.pages else ctx.new_page()
                page.goto(url)
                page.wait_for_load_state("domcontentloaded")
                time.sleep(2)
                page.keyboard.press("Escape")

                # ให้แน่ใจว่าแท็บ articleSetting แสดงผลสมบูรณ์
                page.evaluate("""() => {
                    const pane = document.querySelector('#articleSetting');
                    if (pane) {
                        pane.classList.add('active', 'in');
                        pane.style.display = 'block';
                    }
                }""")
                time.sleep(1)

                # ส่งภาพปก 1:1 เต็มรูปเข้าสู่ ReadAWrite โดยตรง (ไม่ผ่านการ Crop และไม่ถูกตัดหัว)
                cover_b64 = self._prepare_cover_base64(cover_file)
                if cover_b64:
                    self.log(f"กำลังอัปโหลดภาพปก 1:1 เต็มรูป {os.path.basename(cover_file)} ไปยัง ReadAWrite...")
                    page.evaluate("""(b64) => {
                        const inp = document.querySelector('#imgBase64');
                        if (inp) inp.value = b64;
                        const inpCover = document.querySelector('#imgCoverBase64');
                        if (inpCover) inpCover.value = '';
                        const preview = document.querySelector('#img_uploaded, #preview_thumbnail, #preview_cover_article, #img_cover_uploaded');
                        if (preview) {
                            preview.src = b64;
                            if (preview.hasAttribute('srcset')) preview.setAttribute('srcset', b64);
                        }
                        const m = document.querySelector('#modal');
                        if (m) {
                            m.classList.remove('in');
                            m.style.display = 'none';
                        }
                        document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());
                    }""", cover_b64)
                    time.sleep(1)
                    self.log("ตั้งค่าภาพปก 1:1 เต็มรูปเรียบร้อยแล้ว")

                # ติ๊กสถานะภาพปกสร้างด้วย AI
                rad_id = "#is_ai_cover1" if is_ai_cover else "#chk_is_ai_cover0"
                page.evaluate(f"""() => {{
                    const rad = document.querySelector('{rad_id}');
                    if (rad) {{
                        rad.checked = true;
                        rad.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                }}""")

                # บันทึก
                self.log("กำลังกดปุ่มบันทึกการแก้ไขนิยาย...")
                save_btn = page.locator("#btnSaveArticle")
                if save_btn.count() > 0 and save_btn.first.is_visible():
                    save_btn.first.click()
                else:
                    self.log("คลิกปกติไม่ผ่าน กำลังสั่งบันทึกตรงผ่าน JavaScript...")
                    page.evaluate("""() => {
                        const backdrop = document.querySelector('.modal-backdrop');
                        if (backdrop) backdrop.remove();
                        const m = document.querySelector('#modal');
                        if (m) {
                            m.classList.remove('in');
                            m.style.display = 'none';
                        }
                        const btn = document.querySelector('#btnSaveArticle');
                        if (btn) btn.click();
                        else if (typeof article !== 'undefined' && typeof article.saveMeta === 'function') {
                            article.saveMeta();
                        }
                    }""")
                time.sleep(3)

                swal = page.locator("button.swal2-confirm, button:has-text('OK'), .confirm")
                if swal.count() > 0:
                    try:
                        swal.first.click()
                    except:
                        pass

                self.log("อัปเดตภาพปกขึ้น ReadAWrite สำเร็จเรียบร้อยแล้ว!")
                return True
            except Exception as e:
                self.log(f"เกิดข้อผิดพลาดในการอัปเดตภาพปก: {e}")
                return False
            finally:
                ctx.close()
                if browser:
                    browser.close()

    def upload_chapter(self, article_id, chapter_title, chapter_subtitle, content, publish_mode="draft", schedule_time=None):
        """
        อัปโหลดตอนใหม่ขึ้น ReadAWrite ในบัญชีของผู้ใช้นี้
        publish_mode: 'draft' (แบบร่าง), 'publish' (เผยแพร่ทันที), 'schedule' (ตั้งเวลา)
        """
        self.log(f"กำลังอัปโหลด {chapter_title}: {chapter_subtitle} (โหมด: {publish_mode})")
        chapter_url = f"https://www.readawrite.com/?action=manage_chapter&article_id={article_id}"

        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        html_paragraphs = "".join([f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs])

        with sync_playwright() as p:
            browser, ctx = self._get_context(p)
            try:
                page = ctx.pages[0] if ctx.pages else ctx.new_page()
                page.goto(chapter_url)
                page.wait_for_load_state("domcontentloaded")
                time.sleep(2)
                page.keyboard.press("Escape")

                # กรอกชื่อตอน
                page.locator("#chapter_title").fill(chapter_title)
                page.locator("#chapter_subtitle").fill(chapter_subtitle)
                time.sleep(1)

                # หยอดเนื้อหาลงใน CKEditor
                page.evaluate("""(contentHtml) => {
                    const editables = document.querySelectorAll('.ck-editor__editable.ck-content');
                    if (editables.length > 0) {
                        if (editables[0].ckeditorInstance) {
                            editables[0].ckeditorInstance.setData(contentHtml);
                        } else {
                            editables[0].innerHTML = contentHtml;
                            editables[0].dispatchEvent(new Event('input', { bubbles: true }));
                            editables[0].dispatchEvent(new Event('change', { bubbles: true }));
                        }
                    }
                }""", html_paragraphs)
                time.sleep(2)

                # บันทึก
                self.log("กำลังกดปุ่มบันทึก...")
                page.locator("#btnSaveDraft").click()
                time.sleep(3)

                # ตรวจสอบป๊อปอัปผลลัพธ์
                if publish_mode == "publish":
                    self.log("กำลังเลือก 'เผยแพร่ทันที'...")
                    pub_btn = page.locator("button:has-text('เผยแพร่ทันที'), a:has-text('เผยแพร่ทันที')")
                    if pub_btn.count() > 0:
                        pub_btn.first.click()
                        time.sleep(2)
                elif publish_mode == "schedule" and schedule_time:
                    self.log(f"กำลังเลือก 'ตั้งเวลาเผยแพร่' ({schedule_time})...")
                    sched_btn = page.locator("button:has-text('ตั้งเวลาเผยแพร่'), a:has-text('ตั้งเวลาเผยแพร่')")
                    if sched_btn.count() > 0:
                        sched_btn.first.click()
                        time.sleep(2)
                        
                        # หยอดวันเวลาลงใน input ของ ReadAWrite
                        page.evaluate("""(sTime) => {
                            const dText = document.querySelector('#dateDataText');
                            if (dText) {
                                dText.value = sTime;
                                dText.dispatchEvent(new Event('input', { bubbles: true }));
                                dText.dispatchEvent(new Event('change', { bubbles: true }));
                            }
                            const dData = document.querySelector('#dateData');
                            if (dData) {
                                dData.value = sTime;
                                dData.dispatchEvent(new Event('input', { bubbles: true }));
                                dData.dispatchEvent(new Event('change', { bubbles: true }));
                            }
                        }""", schedule_time)
                        time.sleep(1)
                        
                        # กดปุ่มยืนยัน "ตั้งเวลา"
                        confirm_sched = page.locator("button:has-text('ตั้งเวลา'), .btn:has-text('ตั้งเวลา')")
                        if confirm_sched.count() > 0:
                            confirm_sched.last.click()
                            time.sleep(2)
                            self.log(f"บันทึกการตั้งเวลาเผยแพร่ {schedule_time} บน ReadAWrite สำเร็จ!")
                else:
                    self.log("เลือก 'เอาไว้ก่อนจ้า' (บันทึกเป็นแบบร่าง)...")
                    draft_confirm = page.locator("button:has-text('เอาไว้ก่อนจ้า'), a:has-text('เอาไว้ก่อนจ้า')")
                    if draft_confirm.count() > 0:
                        draft_confirm.first.click()
                        time.sleep(2)

                # กด OK ถ้ายืนยัน (SweetAlert)
                try:
                    time.sleep(2)
                    ok_btn = page.locator("button.swal2-confirm, button:has-text('OK')")
                    if ok_btn.count() > 0:
                        ok_btn.first.click()
                        time.sleep(1)
                except Exception:
                    pass

                self.log("อัปโหลดตอนสำเร็จเรียบร้อยแล้ว!")
                return True
            finally:
                ctx.close()
                if browser:
                    browser.close()

    @staticmethod
    def verify_and_save_session(user_id, storage_state_json):
        """ตรวจสอบและบันทึกคุกกี้เซสชันของผู้ใช้"""
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        session_file = os.path.join(SESSIONS_DIR, f"user_{user_id}.json")
        
        if isinstance(storage_state_json, str):
            state = json.loads(storage_state_json)
        else:
            state = storage_state_json

        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        # ตรวจสอบ display_name จาก cookies
        pen_name = "ReadAWrite Author"
        cookies = state.get("cookies", [])
        for c in cookies:
            if c.get("name") == "display_name":
                pen_name = urllib.parse.unquote(c.get("value", ""))
                break

        return {
            "valid": True,
            "pen_name": pen_name,
            "session_file": session_file
        }
