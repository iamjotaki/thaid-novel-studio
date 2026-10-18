# -*- coding: utf-8 -*-
"""
Database Management Module for ReadAWrite Pro Studio SaaS
Uses SQLite for robust, relational, ACID-compliant persistence.
Handles:
- User accounts (authentication, password hashing, roles, plans, quotas)
- User sessions (token management)
- Novels & Chapters (multi-tenant user isolation)
- Subscriptions & Orders (billing simulation)
- Platform analytics for Admin HQ
"""

import os
import sqlite3
import hashlib
import uuid
import json
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DB_DIR, "saas.db")

def get_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    salt = "readawrite_pro_saas_2026_salt"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pen_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user', -- 'user' or 'admin'
        plan TEXT NOT NULL DEFAULT 'trial', -- 'trial', 'monthly', 'annual', 'lifetime'
        status TEXT NOT NULL DEFAULT 'active', -- 'active', 'suspended', 'expired'
        trial_ends_at TEXT,
        quota_limit INTEGER NOT NULL DEFAULT 50000, -- Default 50k words for trial
        quota_used INTEGER NOT NULL DEFAULT 0,
        raw_account TEXT DEFAULT '',
        raw_session_status TEXT DEFAULT 'not_connected', -- 'not_connected', 'connected', 'expired'
        raw_session_file TEXT DEFAULT '',
        raw_session_updated_at TEXT DEFAULT '',
        created_at TEXT NOT NULL
    );
    """)

    # Check and add columns if upgrading existing db
    cursor.execute("PRAGMA table_info(users)")
    existing_cols = [c[1] for c in cursor.fetchall()]
    if "raw_session_status" not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN raw_session_status TEXT DEFAULT 'not_connected'")
    if "raw_session_file" not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN raw_session_file TEXT DEFAULT ''")
    if "raw_session_updated_at" not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN raw_session_updated_at TEXT DEFAULT ''")

    # 2. Sessions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        token TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)

    # 3. Novels Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS novels (
        id TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        genre TEXT,
        category TEXT,
        status TEXT NOT NULL DEFAULT 'กำลังเขียน',
        synopsis TEXT,
        cover_url TEXT,
        article_id TEXT DEFAULT '',
        reads TEXT DEFAULT '0',
        likes TEXT DEFAULT '0',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)

    # 4. Chapters Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        novel_id TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        chapter_num INTEGER NOT NULL,
        subtitle TEXT NOT NULL,
        content TEXT NOT NULL,
        word_count INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'draft', -- 'draft', 'scheduled', 'published'
        schedule_time TEXT,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (novel_id) REFERENCES novels (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)

    # 5. Orders / Billing Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        plan_name TEXT NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'completed',
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)

    # 6. User API Keys Table (BYOK - Bring Your Own Key)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        label TEXT NOT NULL,
        api_key TEXT NOT NULL,
        provider TEXT NOT NULL DEFAULT 'gemini',
        is_active INTEGER NOT NULL DEFAULT 1,
        status TEXT NOT NULL DEFAULT 'ready',
        last_used_at TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)

    # 7. Character Bible Table (คลังความทรงจำตัวละคร)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        novel_id TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'ตัวละครหลัก', -- 'พระเอก', 'นางเอก', 'ตัวร้าย', 'ตัวช่วย'
        traits TEXT,
        avatar_url TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (novel_id) REFERENCES novels (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)

    conn.commit()

    # Dynamic migrations for Novel Blueprint & Unlimited Chapters
    for col, col_def in [
        ("tone_style", "TEXT DEFAULT ''"),
        ("plot_concept", "TEXT DEFAULT ''"),
        ("intimacy_settings", "TEXT DEFAULT '{}'"),
        ("target_chapters", "INTEGER DEFAULT 20")
    ]:
        try:
            cursor.execute(f"ALTER TABLE novels ADD COLUMN {col} {col_def}")
            conn.commit()
        except:
            pass

    # Dynamic migrations for 3D Character Sheets (Want, Need, Flaw, Speaking Style, Hidden Agenda)
    for col, col_def in [
        ("want", "TEXT DEFAULT ''"),
        ("need", "TEXT DEFAULT ''"),
        ("flaw", "TEXT DEFAULT ''"),
        ("speaking_style", "TEXT DEFAULT ''"),
        ("current_emotion", "TEXT DEFAULT ''"),
        ("hidden_agenda", "TEXT DEFAULT ''")
    ]:
        try:
            cursor.execute(f"ALTER TABLE characters ADD COLUMN {col} {col_def}")
            conn.commit()
        except:
            pass

    # Seed Default Accounts if empty
    cursor.execute("SELECT COUNT(*) as cnt FROM users")
    if cursor.fetchone()["cnt"] == 0:
        now = datetime.now()
        trial_end = (now + timedelta(days=7)).isoformat()
        
        # 1. Admin Account
        admin_pass = hash_password("admin1234")
        cursor.execute("""
        INSERT INTO users (pen_name, email, password_hash, role, plan, status, trial_ends_at, quota_limit, quota_used, raw_account, created_at)
        VALUES (?, ?, ?, 'admin', 'lifetime', 'active', ?, 99999999, 125000, 'i_Am_Status', ?)
        """, ("ผู้ดูแลระบบ (Admin HQ)", "admin@readawrite.pro", admin_pass, (now + timedelta(days=3650)).isoformat(), now.isoformat()))
        admin_id = cursor.lastrowid

        # 2. Demo Author Account (นักเขียนตัวอย่าง)
        author_pass = hash_password("123456")
        cursor.execute("""
        INSERT INTO users (pen_name, email, password_hash, role, plan, status, trial_ends_at, quota_limit, quota_used, raw_account, created_at)
        VALUES (?, ?, ?, 'user', 'trial', 'active', ?, 50000, 5465, 'i_Am_Status', ?)
        """, ("รดา นิยายรัก (Demo)", "writer@readawrite.pro", author_pass, trial_end, now.isoformat()))
        author_id = cursor.lastrowid

        # 3. Seed Novel for Demo Author
        novel_id = "RAW-89210-BO"
        cursor.execute("""
        INSERT INTO novels (id, user_id, title, genre, category, status, synopsis, cover_url, article_id, reads, likes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            novel_id,
            author_id,
            "หย่าแล้วอย่ามาอ้อนวอน (คุณประธานถึงคราวโบ้)",
            "ผัวโบ้ / กลับมาเจอกัน",
            "โรมานซ์",
            "กำลังเขียน",
            "เซ็นใบหย่าในวันฝนตกหนัก สี่ปีผ่านไป เธอกลับมาในฐานะซีอีโอบริษัทคู่ค้ารายใหญ่ ส่วนเขา... จากท่านประธานผู้เย็นชา กลายมาเป็นอดีตสามีที่ยอมคุกเข่าอ้อนวอน",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuAk-VKDtqEne4VbaV5ELkdM8jmMajp3IH5K45an3Nq5QULbddUQ1cm-yvWBQBJA2Wee9ju2SXWYvt00eh4FBqf56Ux1RN6qeeBNmIkVQgUwr24hJmt43DVgxUOFnSwGAwI79C3msnxkXKPy5Mlgs5k2LuRVYiyitkOt4NFI_rr36BNcTSfoLUqzPTHtyFUGXQtnJen50yGKtw2w6hGgPJWwE1g6Uf8RAtSWCOuoqrUmC-MQ5-1VIPyD0GaDolZVVSlRyM9QNMk9e8E",
            "658c4eaeed43f428680aec8d7c5ec863",
            "148.9k",
            "12.4k",
            now.isoformat(),
            now.isoformat()
        ))

        # Seed Chapters for Demo Novel
        ch1_content = ("แผ่นกระดาษสีขาวสะอาดตาถูกวางลงบนโต๊ะกระจกใสอย่างไม่ไยดี พร้อมกับเสียงทุ้มต่ำที่เย็นยะเยือกราวกับสายลมในฤดูเหมันต์\n\n"
                       "\"เซ็นซะ 'รินรดา' แล้วเก็บของทั้งหมดออกจากคฤหาสน์ของฉันภายในคืนนี้\"\n\n"
                       "'ภีม พิชญเดชา' ประธานหนุ่มผู้กุมบังเหียนอาณาจักรธุรกิจหมื่นล้านนั่งพิงพนักเก้าอี้หนัง ดวงตาคมกริบคู่ดุจพญาเหยี่ยวมองหญิงสาวตรงหน้าด้วยแววตาไร้ซึ่งความผูกพัน\n\n"
                       "สี่ปีที่ผ่านมา... เธอเป็นเพียงภรรยาในนามที่ผู้ใหญ่จัดหาให้ แต่สำหรับเขา เธอคือสิ่งที่น่ารำคาญใจที่สุดในชีวิต\n\n"
                       "\"รินเซ็นให้แล้วค่ะ\" หญิงสาวหยิบปากกาตวัดชื่ออย่างไม่ลังเล ไม่มีน้ำตาแม้แต่หยดเดียว \"ขอให้คุณภีมมีความสุขกับชีวิตที่ไม่มีรินนะคะ\"")
        
        ch2_content = ("เสียงรองเท้าส้นสูงกระทบกับพื้นหินอ่อนขัดมันของตึกระฟ้าใจกลางเมืองหลวงดังกังวานเป็นจังหวะมั่นคง สี่ปีในต่างแดนหล่อหลอมให้ ‘รมิดา’ ไม่ใช่ผู้หญิงขี้ขลาดที่ยอมก้มหน้ารับเศษเสี้ยวความเมตตาจากใครอีกต่อไป\n\n"
                       "ในมือของเธอคือแฟ้มสัญญาโปรเจกต์ร่วมทุนมูลค่าแปดร้อยล้านบาท... และอีกไม่กี่นาทีข้างหน้า เธอจะต้องเผชิญหน้ากับ ‘ภีม พิชญเดชา’ อดีตสามีผู้เคยผลักไสเธอออกจากชีวิตด้วยถ้อยคำเย็นชาว่า ‘น่ารำคาญ’\n\n"
                       "“คุณรมิดาคะ ท่านประธานพิชญเดชากำลังรออยู่ในห้องประชุมใหญ่ค่ะ” เลขาสาวกล่าวด้วยน้ำเสียงนอบน้อม\n\n"
                       "ริมฝีปากอิ่มเคลือบลิปสติกสีแดงก่ำยกยิ้มขึ้นบางเบา รอยยิ้มที่ไม่ได้มีความอ่อนหวานเหมือนในอดีต หากแต่เป็นรอยยิ้มของพญาหงส์ที่พร้อมจะเหยียบย่ำทุกความทรงจำอันเจ็บปวด\n\n"
                       "“บอกท่านประธานของคุณด้วยนะคะ... ว่าดิฉันไม่ชอบคนมาสายแม้แต่วินาทีเดียว”")

        cursor.execute("""
        INSERT INTO chapters (novel_id, user_id, chapter_num, subtitle, content, word_count, status, updated_at)
        VALUES (?, ?, 1, 'วันที่ใบหย่าวางลงบนโต๊ะอาหาร', ?, 2840, 'published', ?)
        """, (novel_id, author_id, ch1_content, now.isoformat()))

        cursor.execute("""
        INSERT INTO chapters (novel_id, user_id, chapter_num, subtitle, content, word_count, status, updated_at)
        VALUES (?, ?, 2, 'สี่ปีแห่งการเริ่มต้นใหม่ และการกลับมาที่ไม่มีวันเหมือนเดิม', ?, 2625, 'draft', ?)
        """, (novel_id, author_id, ch2_content, now.isoformat()))

        # Seed sample completed order
        cursor.execute("""
        INSERT INTO orders (id, user_id, plan_name, amount, payment_method, status, created_at)
        VALUES (?, ?, 'Pro Annual (รายปี)', 3900, 'PromptPay QR', 'completed', ?)
        """, (f"ORD-{uuid.uuid4().hex[:8].upper()}", admin_id, now.isoformat()))

        conn.commit()

    # Auto-sanitize existing database records (clean (ตอนที่ xx) suffixes and corrupted glyphs)
    try:
        from novel_engine import sanitize_thai_text, clean_chapter_subtitle
        cursor.execute("SELECT id, title, synopsis FROM novels")
        for nid, n_title, n_syn in cursor.fetchall():
            c_title = sanitize_thai_text(n_title)
            c_syn = sanitize_thai_text(n_syn)
            if c_title != n_title or c_syn != n_syn:
                cursor.execute("UPDATE novels SET title = ?, synopsis = ? WHERE id = ?", (c_title, c_syn, nid))
        
        cursor.execute("SELECT id, chapter_num, subtitle FROM chapters")
        for cid, ch_num, sub in cursor.fetchall():
            if sub and ("ตอนที่" in sub or "บทที่" in sub or "\u05D1" in sub or "\uFFFD" in sub):
                c_sub = clean_chapter_subtitle(sub, ch_num)
                if c_sub != sub:
                    cursor.execute("UPDATE chapters SET subtitle = ? WHERE id = ?", (c_sub, cid))
        conn.commit()
    except Exception:
        pass

    conn.close()

# ========================================================
# AUTHENTICATION & USER MANAGEMENT
# ========================================================

def register_user(pen_name, email, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email.strip().lower(),))
    if cursor.fetchone():
        conn.close()
        return None, "อีเมลนี้มีผู้ใช้งานในระบบแล้ว กรุณาใช้อีเมลอื่นหรือเข้าสู่ระบบ"

    now = datetime.now()
    trial_ends = (now + timedelta(days=7)).isoformat()
    p_hash = hash_password(password)

    cursor.execute("""
    INSERT INTO users (pen_name, email, password_hash, role, plan, status, trial_ends_at, quota_limit, quota_used, created_at)
    VALUES (?, ?, ?, 'user', 'trial', 'active', ?, 50000, 0, ?)
    """, (pen_name.strip(), email.strip().lower(), p_hash, trial_ends, now.isoformat()))
    user_id = cursor.lastrowid
    conn.commit()

    token = create_session(user_id)
    user = get_user_by_id(user_id)
    conn.close()
    return {"token": token, "user": user}, None

def login_user(email, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),))
    user_row = cursor.fetchone()
    if not user_row:
        conn.close()
        return None, "ไม่พบอีเมลนี้ในระบบ กรุณาตรวจสอบหรือสมัครสมาชิกใหม่"

    if user_row["password_hash"] != hash_password(password):
        conn.close()
        return None, "รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง"

    if user_row["status"] == "suspended":
        conn.close()
        return None, "บัญชีของคุณถูกระงับการใช้งานชั่วคราว กรุณาติดต่อฝ่ายบริการลูกค้า"

    user_id = user_row["id"]
    token = create_session(user_id)
    user = dict(user_row)
    del user["password_hash"]
    conn.close()
    return {"token": token, "user": user}, None

def create_session(user_id):
    conn = get_db()
    cursor = conn.cursor()
    token = str(uuid.uuid4())
    now = datetime.now()
    expires = (now + timedelta(days=30)).isoformat()
    cursor.execute("""
    INSERT INTO sessions (token, user_id, created_at, expires_at)
    VALUES (?, ?, ?, ?)
    """, (token, user_id, now.isoformat(), expires))
    conn.commit()
    conn.close()
    return token

def get_user_by_token(token):
    if not token:
        return None
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.* FROM users u
    JOIN sessions s ON u.id = s.user_id
    WHERE s.token = ? AND s.expires_at > ?
    """, (token, datetime.now().isoformat()))
    row = cursor.fetchone()
    conn.close()
    if row:
        u = dict(row)
        del u["password_hash"]
        # Calculate days left in trial
        if u["trial_ends_at"]:
            try:
                ends = datetime.fromisoformat(u["trial_ends_at"])
                remaining = (ends - datetime.now()).days
                u["trial_days_left"] = max(0, remaining)
                if remaining <= 0 and u["plan"] == "trial":
                    u["status"] = "expired"
            except:
                u["trial_days_left"] = 0
        else:
            u["trial_days_left"] = 0
        return u
    return None

def get_user_by_id(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        u = dict(row)
        del u["password_hash"]
        if u.get("trial_ends_at"):
            try:
                ends = datetime.fromisoformat(u["trial_ends_at"])
                remaining = (ends - datetime.now()).days
                u["trial_days_left"] = max(0, remaining)
                if remaining <= 0 and u.get("plan") != "lifetime" and u.get("role") != "admin":
                    u["status"] = "expired"
            except:
                u["trial_days_left"] = 0
        else:
            u["trial_days_left"] = 0
        return u
    return None

def delete_session(token):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()

# ========================================================
# NOVELS & CHAPTERS MANAGEMENT
# ========================================================

def get_user_novels(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT n.*, 
           COUNT(c.id) as chapters_count,
           COALESCE(SUM(c.word_count), 0) as words_total
    FROM novels n
    LEFT JOIN chapters c ON n.id = c.novel_id
    WHERE n.user_id = ?
    GROUP BY n.id
    ORDER BY n.updated_at DESC
    """, (user_id,))
    rows = cursor.fetchall()
    novels = [dict(r) for r in rows]
    conn.close()
    return novels

def create_novel(user_id, title, genre, category, synopsis, cover_url=None):
    conn = get_db()
    cursor = conn.cursor()
    novel_id = f"RAW-{uuid.uuid4().hex[:6].upper()}"
    now = datetime.now().isoformat()
    if not cover_url:
        cover_url = "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&q=80"

    cursor.execute("""
    INSERT INTO novels (id, user_id, title, genre, category, status, synopsis, cover_url, reads, likes, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, 'กำลังเขียน', ?, ?, '0', '0', ?, ?)
    """, (novel_id, user_id, title, genre, category, synopsis, cover_url, now, now))

    # Create empty Chapter 1
    cursor.execute("""
    INSERT INTO chapters (novel_id, user_id, chapter_num, subtitle, content, word_count, status, updated_at)
    VALUES (?, ?, 1, 'จุดแตกหักที่ไม่อาจหวนกลับ', 'คลิกปุ่ม ✨ แต่งบทนี้ทันที เพื่อเริ่มแต่งนิยายด้วยพลัง AI...', 0, 'draft', ?)
    """, (novel_id, user_id, now))

    conn.commit()
    conn.close()
    return {"id": novel_id, "title": title, "genre": genre, "category": category, "synopsis": synopsis, "cover_url": cover_url}

def update_novel_article_id(novel_id, user_id, article_id):
    """ผูกหรืออัปเดต Article ID ของ ReadAWrite ให้กับนิยายเรื่องนี้"""
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("""
    UPDATE novels
    SET article_id = ?, updated_at = ?
    WHERE id = ? AND user_id = ?
    """, (str(article_id).strip(), now, novel_id, user_id))
    conn.commit()
    conn.close()

def delete_novel(novel_id, user_id):
    """ลบนิยาย ตอนย่อยทั้งหมด และตัวละครที่เกี่ยวข้องอย่างถาวร"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    u_row = cursor.fetchone()
    is_admin = u_row and u_row["role"] == "admin"

    if is_admin:
        cursor.execute("SELECT id, title FROM novels WHERE id = ?", (novel_id,))
    else:
        cursor.execute("SELECT id, title FROM novels WHERE id = ? AND user_id = ?", (novel_id, user_id))
    
    novel = cursor.fetchone()
    if not novel:
        conn.close()
        return False, "ไม่พบนิยาย หรือคุณไม่มีสิทธิ์ในการลบนิยายเรื่องนี้"
    
    title = novel["title"]
    cursor.execute("DELETE FROM characters WHERE novel_id = ?", (novel_id,))
    cursor.execute("DELETE FROM chapters WHERE novel_id = ?", (novel_id,))
    cursor.execute("DELETE FROM novels WHERE id = ?", (novel_id,))
    conn.commit()
    conn.close()
    return True, f"ลบนิยายเรื่อง '{title}' และข้อมูลตอนทั้งหมดเรียบร้อยแล้ว"

NARRATIVE_BEAT_TITLES = [
    # Act 1: Setup & Inciting Incident (บทที่ 1 - 10)
    "วันที่ใบหย่าวางลงบนโต๊ะอาหาร",
    "เงามืดในอดีตที่หวนคืน",
    "ข้อเสนอที่ไม่ปรารถนา",
    "การเผชิญหน้าใต้เงาจันทร์",
    "สัญญาที่ไม่อาจหลีกเลี่ยง",
    "ความจริงที่ซ่อนอยู่หลังรอยยิ้ม",
    "ก้าวแรกในกรงขังทองคำ",
    "คืนที่สายฝนไม่หยุดโปรย",
    "คำลวงอันแสนหวาน",
    "แววตาที่เปลี่ยนไป",
    
    # Act 2A: Rising Tension & Complication (บทที่ 11 - 25)
    "ใกล้ชิดเกินกว่าจะต้านทาน",
    "เมื่อหน้ากากเริ่มปริแตก",
    "กลลวงกลางค่ำคืน",
    "หัวใจที่เริ่มทรยศตนเอง",
    "ความลับในห้องปิดตาย",
    "รอยแผลที่ไม่อาจลบเลือน",
    "เกมแค้นที่มีชีวิตเป็นเดิมพัน",
    "คืนแห่งความหวั่นไหว",
    "คำเตือนจากความมืด",
    "สายใยที่ยากจะตัดขาด",
    "คำสั่งของหัวใจ",
    "เมื่อไฟแค้นถูกจุดติด",
    "สัมผัสอันตราย",
    "ความจริงที่เริ่มกระจ่าง",
    "จุดเปลี่ยนแห่งความเงียบงัน",

    # Act 2B: Midpoint & Major Crisis (บทที่ 26 - 40)
    "รอยร้าวที่ไม่อาจประสาน",
    "ค่ำคืนที่ความลับพังทลาย",
    "น้ำตาของคนที่แพ้พ่าย",
    "คำสารภาพที่สายเกินกาล",
    "ชะตากรรมที่ไม่อาจหลีกหนี",
    "วิกฤตแห่งการพลัดพราก",
    "เพลิงริษยาที่ลุกท่วม",
    "ความไว้ใจที่แหลกสลาย",
    "เดิมพันครั้งสุดท้าย",
    "จุดพลิกผันครั้งใหญ่ (วิกฤตของหัวใจ)",
    "ในความมืดที่ไร้ทางออก",
    "เสียงสะอื้นที่ไร้คนฟัง",
    "บาดแผลจากคนคุ้นเคย",
    "ทางแยกที่ต้องเลือกเดิน",
    "พายุลูกใหญ่ก่อนฟ้าสาง",

    # Act 3: Climax & Resolution (บทที่ 41 - 50+)
    "การทวงคืนสิ่งที่สูญเสีย",
    "เมื่อความกล้าเผชิญหน้าความจริง",
    "ปลดเปลื้องพันธนาการ",
    "คำขอร้องจากก้นบึ้งหัวใจ",
    "ปาฏิหาริย์แห่งรักแท้",
    "แสงสว่างที่ปลายอุโมงค์",
    "การชดใช้ที่สาสม",
    "วันที่หัวใจได้คำตอบ",
    "สายลมแห่งการเริ่มต้นใหม่",
    "ดอกไม้ที่เบ่งบานอีกครั้งในรอยแผล"
]

def create_novel_blueprint(user_id, title, genre, category, synopsis, tone_style="", plot_concept="", intimacy_settings="{}", target_chapters=20, cover_url=None, outlines=None):
    """
    สร้างนิยายฉบับ Blueprint พร้อมผังตอนเริ่มต้นตามเป้าหมาย (รองรับ 10, 20, 50, 100+ ตอน ไม่จำกัดเพดาน 40 ตอน)
    และตั้งชื่อบทภาษาไทยสละสลวยครบทุกตอน (ไม่ปล่อยให้ขึ้นแค่ ตอนที่ N)
    """
    conn = get_db()
    cursor = conn.cursor()
    novel_id = f"RAW-{uuid.uuid4().hex[:6].upper()}"
    now = datetime.now().isoformat()
    if not cover_url:
        cover_url = "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&q=80"

    cursor.execute("""
    INSERT INTO novels (id, user_id, title, genre, category, status, synopsis, cover_url, reads, likes, tone_style, plot_concept, intimacy_settings, target_chapters, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, 'กำลังเขียน', ?, ?, '0', '0', ?, ?, ?, ?, ?, ?)
    """, (novel_id, user_id, title, genre, category, synopsis, cover_url, tone_style, plot_concept, json.dumps(intimacy_settings) if isinstance(intimacy_settings, dict) else str(intimacy_settings), target_chapters, now, now))

    # Generate Chapters with descriptive titles for EVERY SINGLE chapter
    num_to_create = max(1, int(target_chapters))
    dynamic_outlines = None
    if not outlines or len(outlines) < num_to_create:
        try:
            import novel_engine
            dynamic_outlines = novel_engine.generate_dynamic_chapter_outlines(title, genre, synopsis, num_to_create, category=category)
        except Exception as e:
            dynamic_outlines = None

    for ch_idx in range(1, num_to_create + 1):
        subtitle = None
        # 1. First preference: AI Blueprint outline if provided
        if outlines and ch_idx - 1 < len(outlines):
            item = outlines[ch_idx - 1]
            if isinstance(item, dict):
                sub = item.get("subtitle") or item.get("title")
                if sub and not sub.startswith("ชื่อตอนที่"):
                    subtitle = sub
            elif isinstance(item, str) and not item.startswith("ชื่อตอนที่"):
                subtitle = item
        
        # 2. Second preference: Dynamic procedural outline tailored to story title
        if not subtitle and dynamic_outlines and ch_idx - 1 < len(dynamic_outlines):
            subtitle = dynamic_outlines[ch_idx - 1].get("subtitle")

        # 3. Third preference: Fallback bank
        if not subtitle:
            if ch_idx == 1:
                subtitle = "จุดแตกหักที่ไม่อาจหวนกลับ"
            elif ch_idx == num_to_create:
                subtitle = "บทสรุปความสัมพันธ์ที่แท้จริง"
            elif ch_idx - 1 < len(NARRATIVE_BEAT_TITLES):
                subtitle = NARRATIVE_BEAT_TITLES[ch_idx - 1]
            else:
                # For chapters 51 to 100+
                theme_idx = (ch_idx - 1) % len(NARRATIVE_BEAT_TITLES)
                subtitle = NARRATIVE_BEAT_TITLES[theme_idx]

        try:
            from novel_engine import clean_chapter_subtitle
            subtitle = clean_chapter_subtitle(subtitle, ch_idx, title)
        except Exception:
            pass

        cursor.execute("""
        INSERT INTO chapters (novel_id, user_id, chapter_num, subtitle, content, word_count, status, updated_at)
        VALUES (?, ?, ?, ?, '', 0, 'draft', ?)
        """, (novel_id, user_id, ch_idx, subtitle, now))

    conn.commit()
    conn.close()
    return {
        "id": novel_id,
        "title": title,
        "genre": genre,
        "category": category,
        "synopsis": synopsis,
        "tone_style": tone_style,
        "target_chapters": num_to_create,
        "chapters_count": num_to_create,
        "cover_url": cover_url
    }

def get_sliding_context_for_chapter(novel_id, current_chapter_num, window_size=3):
    """
    Sliding Context Memory:
    1. Past Arcs Recap: สรุปเหตุการณ์ในบทก่อนหน้าเพื่อคุมทิศทางพล็อต
    2. Verbatim Last N Paragraphs: ดึง 2-3 ย่อหน้าสุดท้ายของบทก่อนหน้าแบบคำต่อคำ เพื่อให้ AI จับจังหวะภาษา (Tone & Rhythm) ต่อเนื่องได้เนียนกริบ
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT chapter_num, subtitle, content, word_count
    FROM chapters
    WHERE novel_id = ? AND chapter_num < ? AND length(content) > 50
    ORDER BY chapter_num ASC
    """, (novel_id, current_chapter_num))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return ""

    context_lines = []
    older_chapters = rows[:-window_size] if len(rows) > window_size else []
    recent_chapters = rows[-window_size:] if len(rows) > window_size else rows

    if older_chapters:
        context_lines.append("[สรุปเหตุการณ์ในบทก่อนหน้า (Past Arcs Recap)]:")
        for r in older_chapters:
            context_lines.append(f"- บทที่ {r['chapter_num']}: {r['subtitle']} ({r['word_count']:,} คำ)")

    if recent_chapters:
        context_lines.append("\n[ภาพรวมเหตุการณ์และประเด็นคั่งค้างในบทล่าสุด]:")
        for r in recent_chapters[:-1]:
            content = r['content']
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            summary_snippet = paragraphs[-1] if paragraphs else content[-300:]
            context_lines.append(f"- บทที่ {r['chapter_num']}: {r['subtitle']} -> ปมท้ายบท: {summary_snippet[:150]}...")

        # The immediate previous chapter: provide VERBATIM last 2-3 paragraphs for rhythm & tone continuity
        last_ch = recent_chapters[-1]
        paras = [p.strip() for p in last_ch['content'].split('\n\n') if p.strip()]
        verbatim_paras = "\n\n".join(paras[-3:]) if len(paras) >= 3 else last_ch['content'][-800:]
        context_lines.append(f"\n[2-3 ย่อหน้าสุดท้ายของบทที่ {last_ch['chapter_num']}: {last_ch['subtitle']} (Verbatim Continuity Context - จับจังหวะและน้ำเสียงต่อเนื่อง)]:\n{verbatim_paras.strip()}")

    return "\n".join(context_lines)

def get_novel_details(novel_id, user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM novels WHERE id = ? AND user_id = ?", (novel_id, user_id))
    novel_row = cursor.fetchone()
    if not novel_row:
        conn.close()
        return None

    cursor.execute("SELECT * FROM chapters WHERE novel_id = ? ORDER BY chapter_num ASC", (novel_id,))
    chapter_rows = cursor.fetchall()

    cursor.execute("SELECT * FROM characters WHERE novel_id = ? ORDER BY id ASC", (novel_id,))
    char_rows = cursor.fetchall()
    conn.close()

    novel = dict(novel_row)
    novel["chapters"] = [dict(c) for c in chapter_rows]
    novel["characters"] = [dict(ch) for ch in char_rows]
    return novel

def save_or_update_chapter(novel_id, user_id, chapter_num, subtitle, content, word_count):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    try:
        from novel_engine import clean_chapter_subtitle
        subtitle = clean_chapter_subtitle(subtitle, chapter_num)
    except Exception:
        pass

    cursor.execute("SELECT id FROM chapters WHERE novel_id = ? AND chapter_num = ?", (novel_id, chapter_num))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("""
        UPDATE chapters SET subtitle = ?, content = ?, word_count = ?, updated_at = ?
        WHERE id = ?
        """, (subtitle, content, word_count, now, existing["id"]))
    else:
        cursor.execute("""
        INSERT INTO chapters (novel_id, user_id, chapter_num, subtitle, content, word_count, status, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, 'draft', ?)
        """, (novel_id, user_id, chapter_num, subtitle, content, word_count, now))

    # Touch novel updated_at
    cursor.execute("UPDATE novels SET updated_at = ? WHERE id = ?", (now, novel_id))
    conn.commit()
    conn.close()

def update_chapter_publish_status(novel_id, user_id, chapter_num, status="scheduled", schedule_time=None):
    """อัปเดตสถานะการเผยแพร่และวันเวลาตั้งเวลาของบทนิยาย"""
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("""
        UPDATE chapters
        SET status = ?, schedule_time = ?, updated_at = ?
        WHERE novel_id = ? AND user_id = ? AND chapter_num = ?
    """, (status, schedule_time, now, novel_id, user_id, chapter_num))
    cursor.execute("UPDATE novels SET updated_at = ? WHERE id = ?", (now, novel_id))
    conn.commit()
    conn.close()

# ========================================================
# QUOTA ENFORCEMENT & BILLING
# ========================================================

def deduct_user_quota(user_id, words_count):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET quota_used = quota_used + ? WHERE id = ?", (words_count, user_id))
    conn.commit()
    cursor.execute("SELECT quota_limit, quota_used FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def upgrade_user_plan(user_id, plan_name, payment_method):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now()

    plans_info = {
        "monthly": {"name": "Pro Monthly (รายเดือน)", "amount": 390, "quota_add": 500000, "days": 30},
        "annual": {"name": "Pro Annual (รายปี)", "amount": 3900, "quota_add": 6000000, "days": 365},
        "lifetime": {"name": "Lifetime VIP (ตลอดชีพ)", "amount": 6900, "quota_add": 99999999, "days": 3650}
    }

    info = plans_info.get(plan_name.lower(), plans_info["monthly"])
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"

    # Insert transaction
    cursor.execute("""
    INSERT INTO orders (id, user_id, plan_name, amount, payment_method, status, created_at)
    VALUES (?, ?, ?, ?, ?, 'completed', ?)
    """, (order_id, user_id, info["name"], info["amount"], payment_method, now.isoformat()))

    # Update User Plan & Quota
    cursor.execute("""
    UPDATE users 
    SET plan = ?, status = 'active', quota_limit = quota_limit + ?, trial_ends_at = ?
    WHERE id = ?
    """, (plan_name.lower(), info["quota_add"], (now + timedelta(days=info["days"])).isoformat(), user_id))

    conn.commit()
    conn.close()
    return {"order_id": order_id, "plan": info["name"], "amount": info["amount"]}

# ========================================================
# ADMIN FUNCTIONS
# ========================================================

def get_admin_stats():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total_users, SUM(quota_used) as total_words FROM users")
    u_stat = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) as total_novels FROM novels")
    n_stat = cursor.fetchone()

    cursor.execute("SELECT SUM(amount) as total_revenue FROM orders")
    o_stat = cursor.fetchone()

    conn.close()
    return {
        "total_users": u_stat["total_users"] or 0,
        "total_words_generated": u_stat["total_words"] or 0,
        "total_novels": n_stat["total_novels"] or 0,
        "total_revenue": o_stat["total_revenue"] or 0
    }

def get_all_users_admin():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, pen_name, email, role, plan, status, trial_ends_at, quota_limit, quota_used, created_at FROM users ORDER BY id DESC")
    rows = cursor.fetchall()
    users = []
    now = datetime.now()
    for r in rows:
        u = dict(r)
        if u.get("trial_ends_at"):
            try:
                ends = datetime.fromisoformat(u["trial_ends_at"])
                u["trial_days_left"] = max(0, (ends - now).days)
            except:
                u["trial_days_left"] = 0
        else:
            u["trial_days_left"] = 0
        users.append(u)
    conn.close()
    return users

def update_user_admin(user_id, plan=None, status=None, quota_add=0):
    conn = get_db()
    cursor = conn.cursor()
    if plan:
        cursor.execute("UPDATE users SET plan = ? WHERE id = ?", (plan, user_id))
    if status:
        cursor.execute("UPDATE users SET status = ? WHERE id = ?", (status, user_id))
    if quota_add and quota_add > 0:
        cursor.execute("UPDATE users SET quota_limit = quota_limit + ? WHERE id = ?", (quota_add, user_id))
    conn.commit()
    conn.close()
    return True

# ========================================================
# MULTI-TENANT READAWRITE SESSION MANAGEMENT
# ========================================================

def update_user_readawrite_session(user_id, raw_account, raw_session_file, raw_session_status="connected"):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("""
    UPDATE users 
    SET raw_account = ?, raw_session_file = ?, raw_session_status = ?, raw_session_updated_at = ?
    WHERE id = ?
    """, (raw_account, raw_session_file, raw_session_status, now, user_id))
    conn.commit()
    conn.close()
    return True

def disconnect_user_readawrite_session(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE users 
    SET raw_account = '', raw_session_file = '', raw_session_status = 'not_connected', raw_session_updated_at = ''
    WHERE id = ?
    """, (user_id,))
    conn.commit()
    conn.close()
    return True

# ========================================================
# USER API KEYS (BYOK - BRING YOUR OWN KEY)
# ========================================================

def mask_key(k: str) -> str:
    if not k:
        return ""
    if len(k) <= 8:
        return "••••••••"
    return k[:6] + "••••••••" + k[-4:]

def get_user_api_keys(user_id, include_secret=False):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, user_id, label, api_key, provider, is_active, status, last_used_at, created_at
    FROM user_api_keys
    WHERE user_id = ?
    ORDER BY id ASC
    """, (user_id,))
    rows = cursor.fetchall()
    keys = []
    for r in rows:
        d = dict(r)
        if not include_secret:
            d["masked_key"] = mask_key(d["api_key"])
            d["api_key"] = ""
        else:
            d["masked_key"] = mask_key(d["api_key"])
        keys.append(d)
    conn.close()
    return keys

def get_active_api_keys_for_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, label, api_key, provider
    FROM user_api_keys
    WHERE user_id = ? AND is_active = 1
    ORDER BY id ASC
    """, (user_id,))
    rows = cursor.fetchall()
    keys = [dict(r) for r in rows]
    conn.close()
    return keys

def add_user_api_key(user_id, label, api_key, provider="gemini"):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("""
    INSERT INTO user_api_keys (user_id, label, api_key, provider, is_active, status, created_at)
    VALUES (?, ?, ?, ?, 1, 'ready', ?)
    """, (user_id, label.strip(), api_key.strip(), provider, now))
    key_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return key_id

def update_user_api_key(user_id, key_id, label=None, api_key=None, is_active=None, status=None):
    conn = get_db()
    cursor = conn.cursor()
    fields = []
    values = []
    if label is not None:
        fields.append("label = ?")
        values.append(label.strip())
    if api_key is not None and api_key.strip():
        fields.append("api_key = ?")
        values.append(api_key.strip())
    if is_active is not None:
        fields.append("is_active = ?")
        values.append(1 if is_active else 0)
    if status is not None:
        fields.append("status = ?")
        values.append(status)

    if fields:
        values.extend([key_id, user_id])
        sql = f"UPDATE user_api_keys SET {', '.join(fields)} WHERE id = ? AND user_id = ?"
        cursor.execute(sql, tuple(values))
        conn.commit()
    conn.close()
    return True

def delete_user_api_key(user_id, key_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_api_keys WHERE id = ? AND user_id = ?", (key_id, user_id))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    return changes > 0

def record_api_key_usage(key_id, status="ready"):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("""
    UPDATE user_api_keys
    SET last_used_at = ?, status = ?
    WHERE id = ?
    """, (now, status, key_id))
    conn.commit()
    conn.close()
    return True

# ========================================================
# CHARACTER BIBLE (คลังความทรงจำตัวละคร)
# ========================================================

def get_novel_characters(novel_id, user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, novel_id, user_id, name, role, traits, avatar_url,
           want, need, flaw, speaking_style, current_emotion, hidden_agenda, created_at
    FROM characters
    WHERE novel_id = ? AND user_id = ?
    ORDER BY id ASC
    """, (novel_id, user_id))
    rows = cursor.fetchall()
    chars = [dict(r) for r in rows]
    conn.close()
    return chars

def add_novel_character(novel_id, user_id, name, role, traits, avatar_url="", want="", need="", flaw="", speaking_style="", current_emotion="", hidden_agenda=""):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    if not avatar_url:
        # Default aesthetic avatar based on role
        if "พระเอก" in role:
            avatar_url = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80"
        elif "นางเอก" in role:
            avatar_url = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80"
        elif "ร้าย" in role:
            avatar_url = "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80"
        else:
            avatar_url = "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=150&auto=format&fit=crop&q=80"

    cursor.execute("""
    INSERT INTO characters (novel_id, user_id, name, role, traits, avatar_url, want, need, flaw, speaking_style, current_emotion, hidden_agenda, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (novel_id, user_id, name.strip(), role.strip(), traits.strip(), avatar_url,
          want.strip(), need.strip(), flaw.strip(), speaking_style.strip(), current_emotion.strip(), hidden_agenda.strip(), now))
    char_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return char_id

def delete_novel_character(character_id, user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM characters WHERE id = ? AND user_id = ?", (character_id, user_id))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    return changes > 0

def update_novel_cover(novel_id, user_id, cover_url):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE novels SET cover_url = ?, updated_at = ? WHERE id = ? AND user_id = ?", (cover_url, datetime.now().isoformat(), novel_id, user_id))
    changes = conn.total_changes
    conn.commit()
    conn.close()
def clear_novel_characters(novel_id, user_id):
    """ลบตัวละครทั้งหมดของนิยายเรื่องนี้เพื่อเตรียมสุ่มชุดใหม่"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM characters WHERE novel_id = ? AND user_id = ?", (novel_id, user_id))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    return changes > 0

def update_chapter_subtitle(novel_id, user_id, chapter_num, subtitle):
    """อัปเดตชื่อตอน (Subtitle) ของตอนใดตอนหนึ่ง"""
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    try:
        from novel_engine import clean_chapter_subtitle
        cleaned_sub = clean_chapter_subtitle(subtitle, int(chapter_num))
    except Exception:
        cleaned_sub = subtitle.strip()
    cursor.execute("""
    UPDATE chapters 
    SET subtitle = ?, updated_at = ?
    WHERE novel_id = ? AND user_id = ? AND chapter_num = ?
    """, (cleaned_sub, now, novel_id, user_id, int(chapter_num)))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    return changes > 0

def get_novel_chapters(novel_id, user_id):
    """ดึงรายการตอนทั้งหมดของนิยายเรื่องนี้เรียงตาม chapter_num"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chapters WHERE novel_id = ? AND user_id = ? ORDER BY chapter_num ASC", (novel_id, user_id))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Initialize database immediately on module import
init_db()
