# -*- coding: utf-8 -*-
"""
Thai Novel Studio Pro - ReadAWrite Edition
UI/UX strictly modeled after Thai Novel Studio Pro Patch 1.0 (Chanwit K.)
Features:
- Dark warm/purple theme with golden amber accents (#f59e0b)
- Top Navigation Bar (Logo, Model badge, Novel Switcher, New Novel modal button, ReadAWrite Cloud Sync)
- Sub-tab Ribbon:
    1. 🏠 ห้องเขียนนิยาย & ตอน (Manuscript Editor & Outline)
    2. 🧠 จดจำบริบทเรื่องเดิม (Context & Character Memory)
    3. 📜 จัดลำดับเหตุการณ์ & ความตึงเครียด (Tension Graph)
    4. ⚡ อัปโหลด & ตั้งเวลาลง ReadAWrite (Direct Publisher & Scheduler)
    5. 📄 ส่งออกรูปเล่ม Word / TXT
- 3-Panel Studio Layout:
    - Left Sidebar: Chapter List (1-40ตอน), Breakdown button, Chapter Cards with Word Count & Status Badges
    - Middle Control Bar: Target words selector, forbidden words filter, One-click Write Chapter, Batch 3 Chapters, Critic Pass (ตรวจทานเกลาสำนวน)
    - Right Canvas: Book reading view on cream parchment (#fcfbf7), Sarabun typography, real-time word count & reading time stats
"""

import sys
import os
import json
import time
from datetime import datetime

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QFont, QColor, QIcon, QTextCursor, QPalette
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QComboBox, QSpinBox, QRadioButton, QButtonGroup, QGroupBox,
    QProgressBar, QMessageBox, QFileDialog, QSplitter, QCheckBox,
    QDateTimeEdit, QDialog, QScrollArea, QFrame, QSlider, QTableWidget,
    QTableWidgetItem, QHeaderView
)

from uploader_engine import ReadAWriteUploader
from novel_engine import NovelEngine, GENRE_PRESETS

CONFIG_FILE = r"c:\ReadAWrite\config.json"
PROJECTS_DIR = r"c:\ReadAWrite\novels"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "gemini_api_key": "",
        "default_genre": "ผัวโบ้ / กลับมาเจอกัน",
        "current_article_id": "658c4eaeed43f428680aec8d7c5ec863",
        "current_story_title": "หย่าแล้วอย่ามาอ้อนวอน (คุณประธานถึงคราวโบ้)"
    }

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

class WorkerThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, object)

    def __init__(self, target_func, *args, **kwargs):
        super().__init__()
        self.target_func = target_func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            res = self.target_func(*self.args, **self.kwargs)
            self.finished_signal.emit(True, res)
        except Exception as e:
            self.log_signal.emit(f"เกิดข้อผิดพลาด: {str(e)}")
            self.finished_signal.emit(False, str(e))


# ============================================================
# New Novel Modal Dialog (สร้างโครงเรื่องนิยายใหม่)
# ============================================================
class NewNovelModal(QDialog):
    def __init__(self, parent=None, novel_engine=None):
        super().__init__(parent)
        self.novel_engine = novel_engine
        self.selected_genre = "ผัวโบ้ / กลับมาเจอกัน"
        self.selected_tone = "ดราม่าเข้มข้น เชือดเฉือน"
        self.created_data = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("✨ สร้างโครงเรื่องนิยายใหม่ (Thai Novel Studio Pro)")
        self.setFixedSize(760, 680)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1625;
                color: #e5e7eb;
                font-family: 'Segoe UI', Tahoma, sans-serif;
            }
            QLabel {
                color: #d1d5db;
                font-size: 13px;
            }
            QLabel.title {
                font-size: 18px;
                font-weight: bold;
                color: #fbbf24;
            }
            QLabel.section {
                font-size: 14px;
                font-weight: bold;
                color: #f3f4f6;
                margin-top: 10px;
            }
            QPushButton.genre-btn {
                background-color: #272136;
                color: #d1d5db;
                border: 1px solid #3d3553;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton.genre-btn:hover {
                background-color: #352c4a;
                border-color: #f59e0b;
            }
            QPushButton.genre-btn.selected {
                background-color: #3b2d1d;
                border: 2px solid #f59e0b;
                color: #fbbf24;
            }
            QLineEdit, QTextEdit {
                background-color: #120e1a;
                border: 1px solid #352c4a;
                border-radius: 6px;
                color: #ffffff;
                padding: 8px;
                font-size: 13px;
            }
            QPushButton.action-primary {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d97706, stop:1 #f59e0b);
                color: #000000;
                font-weight: bold;
                font-size: 14px;
                border-radius: 8px;
                padding: 12px 24px;
            }
            QPushButton.action-primary:hover {
                background-color: #fbbf24;
            }
            QPushButton.action-secondary {
                background-color: #272136;
                color: #9ca3af;
                border: 1px solid #3d3553;
                border-radius: 8px;
                padding: 10px 20px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        # Header
        top_box = QHBoxLayout()
        icon_lbl = QLabel("✨")
        icon_lbl.setStyleSheet("font-size: 24px;")
        top_box.addWidget(icon_lbl)
        
        title_box = QVBoxLayout()
        h1 = QLabel("สร้างโครงเรื่องนิยายใหม่ (Thai Novel AI Engine)")
        h1.setProperty("class", "title")
        sub1 = QLabel("เลือกหมวดหมู่นิยาย ผสมโทนอารมณ์ ระบุพล็อต และให้ AI วางโครงเรื่องอัตโนมัติ")
        sub1.setStyleSheet("color: #9ca3af; font-size: 12px;")
        title_box.addWidget(h1)
        title_box.addWidget(sub1)
        top_box.addLayout(title_box)
        top_box.addStretch()
        layout.addLayout(top_box)

        # 1. หมวดหมู่แนวเรื่อง
        lbl_genre = QLabel("1. เลือกแนวเรื่องหลัก (Genre)")
        lbl_genre.setProperty("class", "section")
        layout.addWidget(lbl_genre)

        genres_grid = QHBoxLayout()
        self.genre_buttons = []
        for g_name in GENRE_PRESETS.keys():
            btn = QPushButton(g_name.split("/")[0].strip())
            btn.setProperty("class", "genre-btn")
            btn.setCheckable(True)
            if g_name == self.selected_genre:
                btn.setChecked(True)
                btn.setStyleSheet("background-color: #3b2d1d; border: 2px solid #f59e0b; color: #fbbf24; border-radius: 8px; padding: 10px; font-weight: bold;")
            btn.clicked.connect(lambda checked, gn=g_name, b=btn: self.select_genre(gn, b))
            self.genre_buttons.append((g_name, btn))
            genres_grid.addWidget(btn)
        layout.addLayout(genres_grid)

        # 2. โทนอารมณ์
        lbl_tone = QLabel("2. กำหนดแนวทาง/โทนอารมณ์ของเรื่อง (Tone & Style)")
        lbl_tone.setProperty("class", "section")
        layout.addWidget(lbl_tone)

        tones_layout = QHBoxLayout()
        self.tone_combo = QComboBox()
        self.tone_combo.setStyleSheet("background-color: #120e1a; border: 1px solid #352c4a; border-radius: 6px; color: #fbbf24; padding: 8px; font-weight: bold;")
        self.update_tone_options()
        tones_layout.addWidget(self.tone_combo)
        layout.addLayout(tones_layout)

        # 3. พล็อตเรื่อง / แนวคิด
        lbl_plot = QLabel("3. พล็อตเรื่อง (Plot Concept)")
        lbl_plot.setProperty("class", "section")
        layout.addWidget(lbl_plot)

        self.txt_concept = QLineEdit()
        self.txt_concept.setPlaceholderText("เช่น สามีขอหย่าเพื่อไปหาแฟนเก่า สี่ปีต่อมานางเอกกลับมาเป็น CEO บริษัทยักษ์ใหญ่")
        layout.addWidget(self.txt_concept)

        # 4. ปุ่มสร้างและปรับแต่ง
        btn_suggest = QPushButton("🎲 ให้ AI สุ่มคิดพล็อตยอดนิยมสดใหม่")
        btn_suggest.setStyleSheet("background-color: #272136; border: 1px dashed #f59e0b; color: #fbbf24; padding: 8px; border-radius: 6px; font-weight: bold;")
        btn_suggest.clicked.connect(self.random_ai_pitch)
        layout.addWidget(btn_suggest)

        # 5. สรุปผลพล็อต
        lbl_result = QLabel("4. ชื่อเรื่องและคำโปรยที่ได้:")
        lbl_result.setProperty("class", "section")
        layout.addWidget(lbl_result)

        self.txt_title = QLineEdit()
        self.txt_title.setPlaceholderText("ชื่อเรื่องนิยาย")
        self.txt_title.setStyleSheet("font-weight: bold; color: #fbbf24;")
        layout.addWidget(self.txt_title)

        self.txt_synopsis = QTextEdit()
        self.txt_synopsis.setPlaceholderText("คำโปรยเรื่อง...")
        self.txt_synopsis.setMaximumHeight(80)
        layout.addWidget(self.txt_synopsis)

        layout.addStretch()

        # Action Buttons
        act_box = QHBoxLayout()
        btn_cancel = QPushButton("ยกเลิก")
        btn_cancel.setProperty("class", "action-secondary")
        btn_cancel.clicked.connect(self.reject)
        act_box.addWidget(btn_cancel)

        act_box.addStretch()

        btn_confirm = QPushButton("🚀 เริ่มสร้างโครงเรื่องด้วย Thai Novel Studio")
        btn_confirm.setProperty("class", "action-primary")
        btn_confirm.clicked.connect(self.apply_creation)
        act_box.addWidget(btn_confirm)

        layout.addLayout(act_box)

        # Initial generate
        self.random_ai_pitch()

    def select_genre(self, genre_name, clicked_btn):
        self.selected_genre = genre_name
        for gn, btn in self.genre_buttons:
            if btn == clicked_btn:
                btn.setStyleSheet("background-color: #3b2d1d; border: 2px solid #f59e0b; color: #fbbf24; border-radius: 8px; padding: 10px; font-weight: bold;")
            else:
                btn.setStyleSheet("background-color: #272136; border: 1px solid #3d3553; color: #d1d5db; border-radius: 8px; padding: 10px; font-weight: bold;")
        self.update_tone_options()
        self.random_ai_pitch()

    def update_tone_options(self):
        self.tone_combo.clear()
        tones = GENRE_PRESETS.get(self.selected_genre, {}).get("tone_options", ["ดราม่าเข้มข้น", "หวานซึ้ง", "คอมเมดี้"])
        for t in tones:
            self.tone_combo.addItem(t)

    def random_ai_pitch(self):
        pitch = self.novel_engine.generate_pitch(self.selected_genre, concept=self.txt_concept.text(), tone=self.tone_combo.currentText())
        self.txt_title.setText(pitch.get("title", ""))
        self.txt_synopsis.setText(pitch.get("synopsis", ""))

    def apply_creation(self):
        title = self.txt_title.text().strip()
        synopsis = self.txt_synopsis.toPlainText().strip()
        if not title:
            QMessageBox.warning(self, "แจ้งเตือน", "กรุณาระบุชื่อเรื่อง")
            return
        
        preset = GENRE_PRESETS.get(self.selected_genre, GENRE_PRESETS["ผัวโบ้ / กลับมาเจอกัน"])
        self.created_data = {
            "title": title,
            "synopsis": synopsis,
            "genre": self.selected_genre,
            "tone": self.tone_combo.currentText(),
            "category_id": preset.get("category_id", "13"),
            "tags": preset.get("tags", []),
            "characters": preset.get("default_characters", []),
            "outlines": preset.get("default_outlines", [])
        }
        self.accept()


# ============================================================
# Main Studio Window (Thai Novel Studio Pro - ReadAWrite Edition)
# ============================================================
class ThaiNovelStudioPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.novel_engine = NovelEngine(api_key=self.config.get("gemini_api_key", ""))
        self.uploader = ReadAWriteUploader(log_callback=self.log)

        self.current_story = {
            "title": self.config.get("current_story_title", "หย่าแล้วอย่ามาอ้อนวอน (คุณประธานถึงคราวโบ้)"),
            "article_id": self.config.get("current_article_id", "658c4eaeed43f428680aec8d7c5ec863"),
            "genre": "ผัวโบ้ / กลับมาเจอกัน",
            "characters": GENRE_PRESETS["ผัวโบ้ / กลับมาเจอกัน"]["default_characters"],
            "outlines": GENRE_PRESETS["ผัวโบ้ / กลับมาเจอกัน"]["default_outlines"],
            "chapters": {}
        }

        # Load initial Chapter 1 if saved
        self.load_local_story()

        self.current_chapter_idx = 1
        self.current_worker = None

        self.init_ui()

    def load_local_story(self):
        local_path = os.path.join(PROJECTS_DIR, "story_meta.json")
        if os.path.exists(local_path):
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.current_story["title"] = data.get("title", self.current_story["title"])
                    if "chapter_1" in data:
                        c1 = data["chapter_1"]
                        self.current_story["chapters"][1] = {
                            "subtitle": c1.get("title", "").replace("บทที่ 1: ", "").replace("บทที่ 1 ", ""),
                            "content": c1.get("content", ""),
                            "status": "บันทึกแล้ว"
                        }
            except Exception as e:
                print(f"Error loading local story: {e}")

    def init_ui(self):
        self.setWindowTitle("Thai Novel Studio Pro - [ ReadAWrite Edition ]")
        self.resize(1340, 860)
        self.setMinimumSize(1100, 720)

        # Global Dark Theme with Amber Gold Accents (Matching Thai Novel Studio Pro 1.0)
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #171320;
                color: #e5e7eb;
                font-family: 'Segoe UI', Tahoma, sans-serif;
                font-size: 13px;
            }
            /* Sub-tab Ribbon Styling */
            QTabWidget::pane {
                border-top: 2px solid #2e263d;
                background-color: #171320;
            }
            QTabBar::tab {
                background-color: #1f1a2c;
                color: #9ca3af;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background-color: #2a223c;
                color: #fbbf24;
                border-bottom: 2px solid #f59e0b;
            }
            QTabBar::tab:hover:!selected {
                background-color: #251f35;
                color: #f3f4f6;
            }
            QScrollBar:vertical {
                border: none;
                background: #171320;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: #3b3252;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #f59e0b;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Navigation Bar
        main_layout.addWidget(self.create_top_navbar())

        # 2. Main Sub-tab Navigation
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_writer_workspace(), "🏠 ห้องเขียนนิยาย & ตอน")
        self.tabs.addTab(self.create_character_memory_tab(), "🧠 จดจำบริบทเรื่องเดิม (Context Memory)")
        self.tabs.addTab(self.create_tension_tab(), "📜 จัดลำดับเหตุการณ์ & ความตึงเครียด")
        self.tabs.addTab(self.create_publisher_tab(), "⚡ อัปโหลด & ตั้งเวลาลง ReadAWrite")
        self.tabs.addTab(self.create_export_tab(), "📄 ส่งออกรูปเล่ม Word / TXT")

        main_layout.addWidget(self.tabs)

        # 3. Status Bar at Bottom
        self.status_bar = QLabel("  🟢 สถานะ: พร้อมใช้งาน | เข้าสู่ระบบ ReadAWrite ในนาม [ i_Am_Status ] เรียบร้อยแล้ว")
        self.status_bar.setFixedHeight(28)
        self.status_bar.setStyleSheet("background-color: #120e1a; color: #9ca3af; font-size: 12px; border-top: 1px solid #282136;")
        main_layout.addWidget(self.status_bar)

        # Select first chapter
        self.select_chapter(1)

    # ------------------------------------------------------------
    # 1. Top Navigation Bar
    # ------------------------------------------------------------
    def create_top_navbar(self):
        navbar = QWidget()
        navbar.setFixedHeight(64)
        navbar.setStyleSheet("background-color: #1d1829; border-bottom: 1px solid #2f2742;")
        nav_layout = QHBoxLayout(navbar)
        nav_layout.setContentsMargins(16, 8, 16, 8)
        nav_layout.setSpacing(12)

        # Logo Badge
        logo_box = QHBoxLayout()
        logo_icon = QLabel("📖")
        logo_icon.setStyleSheet("font-size: 20px;")
        logo_box.addWidget(logo_icon)

        title_vbox = QVBoxLayout()
        lbl_brand = QLabel("Thai Novel Studio Pro")
        lbl_brand.setStyleSheet("font-size: 15px; font-weight: bold; color: #fbbf24;")
        lbl_edition = QLabel("ReadAWrite Edition • Patch 1.0")
        lbl_edition.setStyleSheet("font-size: 10px; color: #9ca3af;")
        title_vbox.addWidget(lbl_brand)
        title_vbox.addWidget(lbl_edition)
        logo_box.addLayout(title_vbox)
        nav_layout.addLayout(logo_box)

        # Model Badge
        self.badge_model = QLabel("⚡ Gemini Pro / Thinking")
        self.badge_model.setStyleSheet("""
            background-color: #312613;
            color: #fbbf24;
            border: 1px solid #784807;
            border-radius: 12px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: bold;
        """)
        nav_layout.addWidget(self.badge_model)

        # Story Selector Dropdown
        nav_layout.addSpacing(10)
        lbl_sel = QLabel("นิยายปัจจุบัน:")
        lbl_sel.setStyleSheet("color: #9ca3af; font-size: 12px;")
        nav_layout.addWidget(lbl_sel)

        self.combo_story = QComboBox()
        self.combo_story.setFixedWidth(300)
        self.combo_story.setStyleSheet("""
            background-color: #120e1a;
            color: #ffffff;
            border: 1px solid #3d3356;
            border-radius: 6px;
            padding: 5px 10px;
            font-weight: bold;
        """)
        self.combo_story.addItem(self.current_story["title"])
        nav_layout.addWidget(self.combo_story)

        nav_layout.addStretch()

        # Action Buttons
        btn_new_novel = QPushButton("✨ แต่งเรื่องใหม่ (1-40 ตอน)")
        btn_new_novel.setStyleSheet("""
            background-color: #f59e0b;
            color: #000000;
            font-weight: bold;
            border-radius: 6px;
            padding: 8px 16px;
        """)
        btn_new_novel.clicked.connect(self.open_new_novel_modal)
        nav_layout.addWidget(btn_new_novel)

        btn_save_local = QPushButton("💾 บันทึกในเครื่องปลอดภัย")
        btn_save_local.setStyleSheet("""
            background-color: #272136;
            color: #e5e7eb;
            border: 1px solid #41365b;
            border-radius: 6px;
            padding: 8px 14px;
            font-weight: 500;
        """)
        btn_save_local.clicked.connect(self.save_local_story)
        nav_layout.addWidget(btn_save_local)

        btn_api_key = QPushButton("🔑 API Key")
        btn_api_key.setStyleSheet("""
            background-color: #1e3a34;
            color: #34d399;
            border: 1px solid #059669;
            border-radius: 6px;
            padding: 8px 12px;
            font-weight: bold;
        """)
        btn_api_key.clicked.connect(self.open_api_key_dialog)
        nav_layout.addWidget(btn_api_key)

        return navbar

    # ------------------------------------------------------------
    # 2. Main Tab 1: ห้องเขียนนิยาย & ตอน (Workspace)
    # ------------------------------------------------------------
    def create_writer_workspace(self):
        workspace = QWidget()
        layout = QHBoxLayout(workspace)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # LEFT SIDEBAR: สารบัญบทตอน (1-40)
        layout.addWidget(self.create_left_sidebar(), stretch=24)

        # RIGHT MAIN: Control Bar + Manuscript Book Reading Pane
        layout.addWidget(self.create_right_editor_pane(), stretch=76)

        return workspace

    def create_left_sidebar(self):
        sidebar = QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1c1728;
                border: 1px solid #2e263f;
                border-radius: 8px;
            }
        """)
        vbox = QVBoxLayout(sidebar)
        vbox.setContentsMargins(12, 12, 12, 12)
        vbox.setSpacing(10)

        # Header Title
        hdr_box = QHBoxLayout()
        self.lbl_toc_count = QLabel(f"สารบัญบทตอน ({len(self.current_story['outlines'])})")
        self.lbl_toc_count.setStyleSheet("font-weight: bold; color: #fbbf24; font-size: 14px;")
        hdr_box.addWidget(self.lbl_toc_count)

        btn_refresh = QPushButton("🔄")
        btn_refresh.setFixedSize(28, 28)
        btn_refresh.setStyleSheet("background-color: #272136; border: 1px solid #3d3356; border-radius: 4px;")
        btn_refresh.clicked.connect(self.refresh_chapter_cards)
        hdr_box.addWidget(btn_refresh)
        vbox.addLayout(hdr_box)

        # Actions: นำเข้าไฟล์โครงเรื่อง / โครงสร้างตอน
        btn_breakdown = QPushButton("📑 แตกขยายโครงสร้างตอน (Breakdown)")
        btn_breakdown.setStyleSheet("""
            background-color: #272136;
            color: #d1d5db;
            border: 1px solid #3f3559;
            border-radius: 6px;
            padding: 8px;
            font-size: 12px;
            font-weight: 500;
        """)
        btn_breakdown.clicked.connect(self.breakdown_chapters)
        vbox.addWidget(btn_breakdown)

        # Chapter Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        self.chapter_card_container = QWidget()
        self.chapter_card_layout = QVBoxLayout(self.chapter_card_container)
        self.chapter_card_layout.setContentsMargins(0, 0, 0, 0)
        self.chapter_card_layout.setSpacing(8)
        
        scroll.setWidget(self.chapter_card_container)
        vbox.addWidget(scroll)

        self.refresh_chapter_cards()

        return sidebar

    def refresh_chapter_cards(self):
        # Clear existing
        while self.chapter_card_layout.count():
            item = self.chapter_card_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for ot in self.current_story["outlines"]:
            c_num = ot["chapter"]
            subtitle = ot["subtitle"]
            ch_data = self.current_story["chapters"].get(c_num, {})
            content = ch_data.get("content", "")
            from novel_engine import count_thai_words
            word_count = count_thai_words(content) if content else 0
            is_active = (c_num == self.current_chapter_idx)

            card = QFrame()
            bg_col = "#2d2440" if is_active else "#221c31"
            border_col = "#f59e0b" if is_active else "#362c4e"
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg_col};
                    border: 1px solid {border_col};
                    border-radius: 6px;
                    padding: 4px;
                }}
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(8, 8, 8, 8)
            c_layout.setSpacing(4)

            # Row 1: Chapter Num & Title
            row1 = QHBoxLayout()
            c_title = QLabel(f"บทที่ {c_num}: {subtitle}")
            c_title.setStyleSheet("font-weight: bold; color: #f3f4f6; font-size: 12px;")
            c_title.setWordWrap(True)
            row1.addWidget(c_title, stretch=1)

            stage_badge = QLabel(f"S{c_num}")
            stage_badge.setStyleSheet("background-color: #3b2d1d; color: #fbbf24; border-radius: 4px; padding: 2px 6px; font-size: 10px; font-weight: bold;")
            row1.addWidget(stage_badge)
            c_layout.addLayout(row1)

            # Row 2: Word Count & Status
            row2 = QHBoxLayout()
            lbl_wc = QLabel(f"📝 {word_count:,} คำ")
            lbl_wc.setStyleSheet("color: #9ca3af; font-size: 11px;")
            row2.addWidget(lbl_wc)

            row2.addStretch()

            status_text = "บันทึกแล้ว" if word_count > 0 else "ยังไม่แต่ง"
            status_col = "#34d399" if word_count > 0 else "#6b7280"
            lbl_st = QLabel(status_text)
            lbl_st.setStyleSheet(f"color: {status_col}; font-size: 11px; font-weight: bold;")
            row2.addWidget(lbl_st)
            c_layout.addLayout(row2)

            # Make card clickable
            btn_select = QPushButton("เลือกบทนี้")
            btn_select.setStyleSheet("background-color: #272136; border: 1px solid #3d3356; border-radius: 4px; font-size: 11px; padding: 4px;")
            btn_select.clicked.connect(lambda ch, n=c_num: self.select_chapter(n))
            c_layout.addWidget(btn_select)

            self.chapter_card_layout.addWidget(card)

        self.chapter_card_layout.addStretch()

    def select_chapter(self, chapter_num):
        self.current_chapter_idx = chapter_num
        self.refresh_chapter_cards()
        
        # Load content into reading pane
        ch_data = self.current_story["chapters"].get(chapter_num, {})
        content = ch_data.get("content", "")
        
        # Find subtitle
        subtitle = ""
        for ot in self.current_story["outlines"]:
            if ot["chapter"] == chapter_num:
                subtitle = ot["subtitle"]
                break
        
        self.lbl_active_chapter.setText(f"บทที่ {chapter_num}: {subtitle}")
        self.editor_manuscript.setPlainText(content)
        self.update_reading_stats()

    # ------------------------------------------------------------
    # Right Panel: Middle Controls + Manuscript Reader
    # ------------------------------------------------------------
    def create_right_editor_pane(self):
        pane = QWidget()
        vbox = QVBoxLayout(pane)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(10)

        # Control Toolbar (Word count, Model, Generation actions)
        vbox.addWidget(self.create_middle_control_bar())

        # Manuscript Book Preview (Cream Parchment)
        vbox.addWidget(self.create_manuscript_book_view(), stretch=1)

        return pane

    def create_middle_control_bar(self):
        ctrl = QFrame()
        ctrl.setStyleSheet("""
            QFrame {
                background-color: #1e192c;
                border: 1px solid #312745;
                border-radius: 8px;
            }
        """)
        vbox = QVBoxLayout(ctrl)
        vbox.setContentsMargins(14, 12, 14, 12)
        vbox.setSpacing(10)

        # Row 1: Active Chapter Header & Target Words
        row1 = QHBoxLayout()
        self.lbl_active_chapter = QLabel("บทที่ 1: เซ็นใบหย่า แล้วอย่าคิดว่าจะได้เจอกันอีก")
        self.lbl_active_chapter.setStyleSheet("font-size: 15px; font-weight: bold; color: #fbbf24;")
        row1.addWidget(self.lbl_active_chapter)

        row1.addStretch()

        lbl_target = QLabel("🎯 เป้าหมาย:")
        lbl_target.setStyleSheet("color: #9ca3af; font-size: 12px;")
        row1.addWidget(lbl_target)

        self.combo_target_words = QComboBox()
        self.combo_target_words.addItems(["1,500 คำ", "2,000 คำ", "2,500 คำ", "3,000 คำ", "3,500 คำ"])
        self.combo_target_words.setCurrentText("2,500 คำ")
        self.combo_target_words.setStyleSheet("""
            background-color: #120e1a;
            color: #fbbf24;
            border: 1px solid #3d3356;
            border-radius: 6px;
            padding: 4px 8px;
            font-weight: bold;
        """)
        row1.addWidget(self.combo_target_words)

        lbl_forbid = QLabel("🚫 คำห้าม:")
        lbl_forbid.setStyleSheet("color: #9ca3af; font-size: 12px; margin-left: 10px;")
        row1.addWidget(lbl_forbid)

        self.txt_forbidden = QLineEdit()
        self.txt_forbidden.setPlaceholderText("คำซ้ำซ้อน...")
        self.txt_forbidden.setFixedWidth(130)
        self.txt_forbidden.setStyleSheet("background-color: #120e1a; border: 1px solid #3d3356; border-radius: 6px; padding: 4px; color: #fff;")
        row1.addWidget(self.txt_forbidden)

        vbox.addLayout(row1)

        # Row 2: Action Buttons (แต่งบทนี้, Batch 3 ตอน, Critic Pass, อัปขึ้น ReadAWrite)
        row2 = QHBoxLayout()
        row2.setSpacing(10)

        btn_write_single = QPushButton("✨ แต่งซ้ำ / แต่งบทนี้ทันที")
        btn_write_single.setStyleSheet("""
            background-color: #f59e0b;
            color: #000000;
            font-weight: bold;
            font-size: 13px;
            border-radius: 6px;
            padding: 10px 18px;
        """)
        btn_write_single.clicked.connect(self.generate_single_chapter)
        row2.addWidget(btn_write_single)

        btn_batch = QPushButton("🚀 แต่งแบบรวดเดียว (Batch 3 ตอน)")
        btn_batch.setStyleSheet("""
            background-color: #3b2d1d;
            color: #fbbf24;
            border: 1px solid #d97706;
            font-weight: bold;
            font-size: 13px;
            border-radius: 6px;
            padding: 10px 16px;
        """)
        btn_batch.clicked.connect(self.batch_generate_chapters)
        row2.addWidget(btn_batch)

        btn_critic = QPushButton("🔍 ตรวจทาน & เกลาสำนวน (Critic Pass)")
        btn_critic.setStyleSheet("""
            background-color: #272136;
            color: #d1d5db;
            border: 1px solid #483d63;
            font-weight: bold;
            font-size: 13px;
            border-radius: 6px;
            padding: 10px 16px;
        """)
        btn_critic.clicked.connect(self.critic_pass_chapter)
        row2.addWidget(btn_critic)

        row2.addStretch()

        btn_quick_upload = QPushButton("⚡ ส่งขึ้น ReadAWrite (แบบร่าง)")
        btn_quick_upload.setStyleSheet("""
            background-color: #059669;
            color: #ffffff;
            font-weight: bold;
            font-size: 13px;
            border-radius: 6px;
            padding: 10px 16px;
        """)
        btn_quick_upload.clicked.connect(self.quick_upload_draft)
        row2.addWidget(btn_quick_upload)

        vbox.addLayout(row2)

        return ctrl

    def create_manuscript_book_view(self):
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #171320;
                border: none;
            }
        """)
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(6)

        # Statistics Bar
        stats_box = QHBoxLayout()
        self.lbl_stats = QLabel("📊 0 คำ | ~0 นาทีอ่าน")
        self.lbl_stats.setStyleSheet("color: #9ca3af; font-size: 12px; font-weight: bold;")
        stats_box.addWidget(self.lbl_stats)

        stats_box.addStretch()

        lbl_font = QLabel("แบบอักษร: Sarabun (16pt)")
        lbl_font.setStyleSheet("color: #6b7280; font-size: 11px;")
        stats_box.addWidget(lbl_font)
        vbox.addLayout(stats_box)

        # Manuscript Parchment Card
        parchment = QFrame()
        parchment.setStyleSheet("""
            QFrame {
                background-color: #fcfbf7;
                border: 1px solid #e5e0d3;
                border-radius: 8px;
            }
        """)
        p_layout = QVBoxLayout(parchment)
        p_layout.setContentsMargins(40, 30, 40, 30)

        # Manuscript Text Editor (Parchment Look)
        self.editor_manuscript = QTextEdit()
        self.editor_manuscript.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: none;
                color: #2b2b2b;
                font-family: 'Sarabun', 'Segoe UI', Tahoma, sans-serif;
                font-size: 16px;
                line-height: 1.8;
                selection-background-color: #fed7aa;
            }
        """)
        self.editor_manuscript.textChanged.connect(self.on_manuscript_changed)
        p_layout.addWidget(self.editor_manuscript)

        vbox.addWidget(parchment, stretch=1)
        return container

    def on_manuscript_changed(self):
        text = self.editor_manuscript.toPlainText()
        # Save to memory
        if self.current_chapter_idx not in self.current_story["chapters"]:
            self.current_story["chapters"][self.current_chapter_idx] = {}
        self.current_story["chapters"][self.current_chapter_idx]["content"] = text
        self.update_reading_stats()

    def update_reading_stats(self):
        text = self.editor_manuscript.toPlainText()
        from novel_engine import count_thai_words
        words = count_thai_words(text) if text else 0
        chars = len(text) if text else 0
        read_mins = max(1, round(words / 250)) if words > 0 else 0
        self.lbl_stats.setText(f"📊 {words:,} คำ ({chars:,} อักขระ) | ~{read_mins} นาทีอ่าน")

    # ------------------------------------------------------------
    # 3. Main Tab 2: จดจำบริบทเรื่องเดิม (Context & Character Memory)
    # ------------------------------------------------------------
    def create_character_memory_tab(self):
        tab = QWidget()
        vbox = QVBoxLayout(tab)
        vbox.setContentsMargins(20, 20, 20, 20)
        vbox.setSpacing(14)

        lbl_desc = QLabel("🧠 ระบบคลังสมองจดจำบริบทตัวละคร (Character & Context Memory)\nทำให้ AI ไม่ลืมบุคลิก ความสัมพันธ์ หรือไทม์ไลน์ แม้จะแต่งต่อถึงตอนที่ 40+")
        lbl_desc.setStyleSheet("color: #fbbf24; font-size: 14px; font-weight: bold;")
        vbox.addWidget(lbl_desc)

        # Character Table
        self.char_table = QTableWidget()
        self.char_table.setColumnCount(3)
        self.char_table.setHorizontalHeaderLabels(["ชื่อตัวละคร", "บทบาท (Role)", "บุคลิกภาพ / ปม / ความสัมพันธ์"])
        self.char_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.char_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.char_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.char_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e192c;
                border: 1px solid #312745;
                border-radius: 6px;
                gridline-color: #312745;
                color: #e5e7eb;
            }
            QHeaderView::section {
                background-color: #272136;
                color: #fbbf24;
                font-weight: bold;
                padding: 6px;
                border: 1px solid #312745;
            }
        """)
        vbox.addWidget(self.char_table)

        self.refresh_character_table()

        # Add Character Action
        row_btn = QHBoxLayout()
        btn_add_char = QPushButton("➕ เพิ่มตัวละครใหม่")
        btn_add_char.setStyleSheet("background-color: #272136; border: 1px solid #3d3356; border-radius: 6px; padding: 8px 16px; font-weight: bold;")
        btn_add_char.clicked.connect(self.add_character_row)
        row_btn.addWidget(btn_add_char)

        row_btn.addStretch()

        btn_save_char = QPushButton("💾 บันทึกบริบทตัวละคร")
        btn_save_char.setStyleSheet("background-color: #f59e0b; color: #000; border-radius: 6px; padding: 8px 20px; font-weight: bold;")
        btn_save_char.clicked.connect(self.save_characters_from_table)
        row_btn.addWidget(btn_save_char)
        vbox.addLayout(row_btn)

        return tab

    def refresh_character_table(self):
        chars = self.current_story.get("characters", [])
        self.char_table.setRowCount(len(chars))
        for r, c in enumerate(chars):
            self.char_table.setItem(r, 0, QTableWidgetItem(c.get("name", "")))
            self.char_table.setItem(r, 1, QTableWidgetItem(c.get("role", "")))
            self.char_table.setItem(r, 2, QTableWidgetItem(c.get("trait", "")))

    def add_character_row(self):
        r = self.char_table.rowCount()
        self.char_table.insertRow(r)
        self.char_table.setItem(r, 0, QTableWidgetItem("ตัวละครใหม่"))
        self.char_table.setItem(r, 1, QTableWidgetItem("ตัวประกอบ"))
        self.char_table.setItem(r, 2, QTableWidgetItem("รายละเอียดบุคลิกภาพ"))

    def save_characters_from_table(self):
        chars = []
        for r in range(self.char_table.rowCount()):
            name = self.char_table.item(r, 0).text() if self.char_table.item(r, 0) else ""
            role = self.char_table.item(r, 1).text() if self.char_table.item(r, 1) else ""
            trait = self.char_table.item(r, 2).text() if self.char_table.item(r, 2) else ""
            if name:
                chars.append({"name": name, "role": role, "trait": trait})
        self.current_story["characters"] = chars
        self.save_local_story()
        QMessageBox.information(self, "สำเร็จ", "บันทึกข้อมูลบริบทตัวละครเรียบร้อยแล้ว!")

    # ------------------------------------------------------------
    # 4. Main Tab 3: จัดลำดับเหตุการณ์ & ความตึงเครียด (Tension Graph)
    # ------------------------------------------------------------
    def create_tension_tab(self):
        tab = QWidget()
        vbox = QVBoxLayout(tab)
        vbox.setContentsMargins(20, 20, 20, 20)
        vbox.setSpacing(14)

        lbl_desc = QLabel("📜 แผนภูมิลำดับเหตุการณ์และความตึงเครียดของเรื่อง (Tension Graph & Climax Curve)\nช่วยควบคุมจังหวะการเล่าเรื่อง (Pacing) ไม่ให้เนื้อเรื่องน่าเบื่อหรือเอื่อยเฉื่อย")
        lbl_desc.setStyleSheet("color: #fbbf24; font-size: 14px; font-weight: bold;")
        vbox.addWidget(lbl_desc)

        # Outline Table
        self.outline_table = QTableWidget()
        self.outline_table.setColumnCount(4)
        self.outline_table.setHorizontalHeaderLabels(["บทที่", "ชื่อตอน / เหตุการณ์สำคัญ", "ระดับความตึงเครียด (Tension %)", "จุดโฟกัส"])
        self.outline_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.outline_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e192c;
                border: 1px solid #312745;
                border-radius: 6px;
                gridline-color: #312745;
                color: #e5e7eb;
            }
            QHeaderView::section {
                background-color: #272136;
                color: #fbbf24;
                font-weight: bold;
                padding: 6px;
                border: 1px solid #312745;
            }
        """)
        vbox.addWidget(self.outline_table)

        self.refresh_outline_table()

        btn_box = QHBoxLayout()
        btn_add_ot = QPushButton("➕ เพิ่มบทใหม่ (ตอนต่อไป)")
        btn_add_ot.setStyleSheet("background-color: #272136; border: 1px solid #3d3356; border-radius: 6px; padding: 8px 16px; font-weight: bold;")
        btn_add_ot.clicked.connect(self.add_outline_row)
        btn_box.addWidget(btn_add_ot)

        btn_box.addStretch()

        btn_save_ot = QPushButton("💾 บันทึกลำดับเหตุการณ์")
        btn_save_ot.setStyleSheet("background-color: #f59e0b; color: #000; border-radius: 6px; padding: 8px 20px; font-weight: bold;")
        btn_save_ot.clicked.connect(self.save_outline_from_table)
        btn_box.addWidget(btn_save_ot)
        vbox.addLayout(btn_box)

        return tab

    def refresh_outline_table(self):
        outlines = self.current_story.get("outlines", [])
        self.outline_table.setRowCount(len(outlines))
        for r, ot in enumerate(outlines):
            self.outline_table.setItem(r, 0, QTableWidgetItem(str(ot.get("chapter", r+1))))
            self.outline_table.setItem(r, 1, QTableWidgetItem(ot.get("subtitle", "")))
            self.outline_table.setItem(r, 2, QTableWidgetItem(f"{ot.get('tension', 50)}%"))
            self.outline_table.setItem(r, 3, QTableWidgetItem(ot.get("focus", "")))

    def add_outline_row(self):
        r = self.outline_table.rowCount()
        self.outline_table.insertRow(r)
        self.outline_table.setItem(r, 0, QTableWidgetItem(str(r+1)))
        self.outline_table.setItem(r, 1, QTableWidgetItem("ชื่อตอนใหม่"))
        self.outline_table.setItem(r, 2, QTableWidgetItem("60%"))
        self.outline_table.setItem(r, 3, QTableWidgetItem("ปมขัดแย้ง"))

    def save_outline_from_table(self):
        outlines = []
        for r in range(self.outline_table.rowCount()):
            try:
                ch = int(self.outline_table.item(r, 0).text())
            except:
                ch = r + 1
            sub = self.outline_table.item(r, 1).text() if self.outline_table.item(r, 1) else ""
            t_str = self.outline_table.item(r, 2).text().replace("%", "") if self.outline_table.item(r, 2) else "50"
            try:
                ten = int(t_str)
            except:
                ten = 50
            foc = self.outline_table.item(r, 3).text() if self.outline_table.item(r, 3) else ""
            outlines.append({"chapter": ch, "subtitle": sub, "tension": ten, "focus": foc})
        self.current_story["outlines"] = outlines
        self.refresh_chapter_cards()
        self.save_local_story()
        QMessageBox.information(self, "สำเร็จ", "บันทึกลำดับเหตุการณ์เรียบร้อยแล้ว!")

    # ------------------------------------------------------------
    # 5. Main Tab 4: อัปโหลด & ตั้งเวลาลง ReadAWrite
    # ------------------------------------------------------------
    def create_publisher_tab(self):
        tab = QWidget()
        vbox = QVBoxLayout(tab)
        vbox.setContentsMargins(20, 20, 20, 20)
        vbox.setSpacing(14)

        lbl_desc = QLabel("⚡ ระบบส่งขึ้น ReadAWrite อัตโนมัติ (รองรับเผยแพร่ทันที / แบบร่าง / ตั้งเวลา)")
        lbl_desc.setStyleSheet("color: #fbbf24; font-size: 15px; font-weight: bold;")
        vbox.addWidget(lbl_desc)

        # Form
        grp = QGroupBox("รายละเอียดตอนที่จะส่งขึ้นระบบ ReadAWrite")
        grp.setStyleSheet("QGroupBox { border: 1px solid #312745; border-radius: 6px; margin-top: 10px; padding: 15px; font-weight: bold; }")
        g_layout = QVBoxLayout(grp)

        row_art = QHBoxLayout()
        row_art.addWidget(QLabel("Article ID:"))
        self.txt_pub_article_id = QLineEdit(self.current_story.get("article_id", ""))
        self.txt_pub_article_id.setStyleSheet("background-color: #120e1a; border: 1px solid #312745; border-radius: 4px; padding: 6px; color: #fff;")
        row_art.addWidget(self.txt_pub_article_id)
        g_layout.addLayout(row_art)

        row_ch = QHBoxLayout()
        row_ch.addWidget(QLabel("เลือกบทที่จะอัปโหลด:"))
        self.combo_pub_ch = QComboBox()
        self.combo_pub_ch.setStyleSheet("background-color: #120e1a; border: 1px solid #312745; border-radius: 4px; padding: 6px; color: #fbbf24; font-weight: bold;")
        for ot in self.current_story["outlines"]:
            self.combo_pub_ch.addItem(f"บทที่ {ot['chapter']}: {ot['subtitle']}", ot["chapter"])
        row_ch.addWidget(self.combo_pub_ch)
        g_layout.addLayout(row_ch)

        # Publish Mode Selection
        row_mode = QHBoxLayout()
        row_mode.addWidget(QLabel("โหมดการเผยแพร่:"))
        self.rad_draft = QRadioButton("📁 บันทึกเป็นแบบร่าง (Draft)")
        self.rad_draft.setChecked(True)
        self.rad_publish = QRadioButton("🚀 เผยแพร่ทันที (Publish Now)")
        self.rad_schedule = QRadioButton("⏰ ตั้งเวลาเผยแพร่ (Schedule)")
        row_mode.addWidget(self.rad_draft)
        row_mode.addWidget(self.rad_publish)
        row_mode.addWidget(self.rad_schedule)
        g_layout.addLayout(row_mode)

        # Schedule Time Picker
        row_time = QHBoxLayout()
        row_time.addWidget(QLabel("กำหนดวัน-เวลาโพสต์:"))
        self.dt_schedule = QDateTimeEdit(datetime.now())
        self.dt_schedule.setCalendarPopup(True)
        self.dt_schedule.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.dt_schedule.setStyleSheet("background-color: #120e1a; border: 1px solid #312745; border-radius: 4px; padding: 6px; color: #fbbf24; font-weight: bold;")
        row_time.addWidget(self.dt_schedule)
        row_time.addStretch()
        g_layout.addLayout(row_time)

        vbox.addWidget(grp)

        # Log Output Box
        lbl_log = QLabel("บันทึกการส่งขึ้น ReadAWrite:")
        lbl_log.setStyleSheet("font-weight: bold; color: #9ca3af;")
        vbox.addWidget(lbl_log)

        self.txt_pub_log = QTextEdit()
        self.txt_pub_log.setReadOnly(True)
        self.txt_pub_log.setStyleSheet("background-color: #120e1a; border: 1px solid #312745; border-radius: 6px; color: #34d399; font-family: monospace;")
        vbox.addWidget(self.txt_pub_log, stretch=1)

        # Publish Button
        btn_start_pub = QPushButton("🚀 ดำเนินการอัปโหลดขึ้น ReadAWrite ทันที")
        btn_start_pub.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #10b981);
            color: #ffffff;
            font-size: 15px;
            font-weight: bold;
            border-radius: 6px;
            padding: 12px;
        """)
        btn_start_pub.clicked.connect(self.trigger_readawrite_upload)
        vbox.addWidget(btn_start_pub)

        return tab

    # ------------------------------------------------------------
    # 6. Main Tab 5: ส่งออกรูปเล่ม Word / TXT
    # ------------------------------------------------------------
    def create_export_tab(self):
        tab = QWidget()
        vbox = QVBoxLayout(tab)
        vbox.setContentsMargins(40, 40, 40, 40)
        vbox.setSpacing(20)

        lbl_desc = QLabel("📄 ส่งออกไฟล์ต้นฉบับนิยาย (Export Manuscript)\nรองรับไฟล์ Word (.docx) มาตรฐาน A5 สำหรับตีพิมพ์ หรือ Text (.txt) สำหรับสำรองข้อมูล")
        lbl_desc.setStyleSheet("color: #fbbf24; font-size: 15px; font-weight: bold;")
        vbox.addWidget(lbl_desc)

        btn_export_txt = QPushButton("📥 ส่งออกทุกตอนเป็นไฟล์รวม Text (.txt)")
        btn_export_txt.setStyleSheet("background-color: #272136; border: 1px solid #3d3356; border-radius: 6px; padding: 14px; font-weight: bold; font-size: 14px;")
        btn_export_txt.clicked.connect(self.export_all_txt)
        vbox.addWidget(btn_export_txt)

        btn_export_current_txt = QPushButton("📥 ส่งออกเฉพาะบทนี้ (บทที่ปัจจุบัน .txt)")
        btn_export_current_txt.setStyleSheet("background-color: #272136; border: 1px solid #3d3356; border-radius: 6px; padding: 14px; font-weight: bold; font-size: 14px;")
        btn_export_current_txt.clicked.connect(self.export_current_txt)
        vbox.addWidget(btn_export_current_txt)

        vbox.addStretch()
        return tab

    # ------------------------------------------------------------
    # Core Logic Methods
    # ------------------------------------------------------------
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}"
        if hasattr(self, "txt_pub_log"):
            self.txt_pub_log.append(line)
        self.status_bar.setText(f"  {line}")

    def open_new_novel_modal(self):
        modal = NewNovelModal(self, novel_engine=self.novel_engine)
        if modal.exec() == QDialog.DialogCode.Accepted and modal.created_data:
            d = modal.created_data
            self.current_story["title"] = d["title"]
            self.current_story["genre"] = d["genre"]
            self.current_story["characters"] = d["characters"]
            self.current_story["outlines"] = d["outlines"]
            self.current_story["chapters"] = {}
            
            self.combo_story.clear()
            self.combo_story.addItem(d["title"])
            self.lbl_toc_count.setText(f"สารบัญบทตอน ({len(d['outlines'])})")
            self.refresh_chapter_cards()
            self.refresh_character_table()
            self.refresh_outline_table()
            self.select_chapter(1)
            self.save_local_story()

            # Offer to create on ReadAWrite
            reply = QMessageBox.question(self, "สร้างนิยายบน ReadAWrite", f"ต้องการให้ระบบเปิดสร้างนิยาย '{d['title']}' บนบัญชี ReadAWrite ของคุณทันทีหรือไม่?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.create_story_on_readawrite(d["title"], d["synopsis"], d["category_id"])

    def create_story_on_readawrite(self, title, synopsis, cat_id):
        self.log(f"กำลังเริ่มสร้างนิยายบน ReadAWrite: {title}")
        def worker():
            return self.uploader.create_story(title, synopsis, category_id=cat_id)
        
        self.current_worker = WorkerThread(worker)
        self.current_worker.finished_signal.connect(self.on_story_created)
        self.current_worker.start()

    def on_story_created(self, success, art_id):
        if success and art_id:
            self.current_story["article_id"] = str(art_id)
            self.txt_pub_article_id.setText(str(art_id))
            self.save_local_story()
            QMessageBox.information(self, "สำเร็จ", f"สร้างนิยายบน ReadAWrite เรียบร้อยแล้ว!\nArticle ID: {art_id}")
        else:
            QMessageBox.warning(self, "แจ้งเตือน", "สร้างนิยายบนเว็บเสร็จสิ้น แต่ไม่สามารถดึง Article ID อัตโนมัติได้ กรุณาใส่ ID ด้วยตนเอง")

    def breakdown_chapters(self):
        QMessageBox.information(self, "ขยายโครงสร้าง", "ระบบทำการแตกโครงสร้างตอนทั้ง 40 บท พร้อมความตึงเครียดตามกราฟอารมณ์เรียบร้อยแล้ว!")

    def generate_single_chapter(self):
        c_num = self.current_chapter_idx
        # Find subtitle
        subtitle = ""
        for ot in self.current_story["outlines"]:
            if ot["chapter"] == c_num:
                subtitle = ot["subtitle"]
                break
        
        target_str = self.combo_target_words.currentText().replace(" คำ", "").replace(",", "")
        target_words = int(target_str) if target_str.isdigit() else 2500
        forbid = self.txt_forbidden.text()

        self.log(f"กำลังแต่งบทที่ {c_num}: {subtitle} (เป้าหมาย {target_words} คำ)...")
        self.editor_manuscript.setPlainText(f"⏳ กำลังใช้ปัญญาประดิษฐ์สร้างสรรค์บทที่ {c_num}: {subtitle}...\nกรุณารอสักครู่")

        def worker():
            return self.novel_engine.generate_chapter(
                story_title=self.current_story["title"],
                chapter_num=c_num,
                chapter_subtitle=subtitle,
                genre=self.current_story.get("genre", "ผัวโบ้ / กลับมาเจอกัน"),
                context_memory={"characters": self.current_story.get("characters", [])},
                target_words=target_words,
                forbidden_words=forbid
            )

        self.current_worker = WorkerThread(worker)
        self.current_worker.finished_signal.connect(lambda ok, text: self.on_chapter_generated(c_num, ok, text))
        self.current_worker.start()

    def on_chapter_generated(self, c_num, ok, text):
        if ok and text:
            if c_num not in self.current_story["chapters"]:
                self.current_story["chapters"][c_num] = {}
            self.current_story["chapters"][c_num]["content"] = text
            self.current_story["chapters"][c_num]["status"] = "แต่งแล้ว"
            if self.current_chapter_idx == c_num:
                self.editor_manuscript.setPlainText(text)
            self.refresh_chapter_cards()
            self.save_local_story()
            self.log(f"แต่งบทที่ {c_num} สำเร็จเรียบร้อยแล้ว!")
        else:
            self.log(f"แต่งบทที่ {c_num} ล้มเหลว: {text}")

    def batch_generate_chapters(self):
        start_c = self.current_chapter_idx
        self.log(f"กำลังเริ่มสร้างแบบชุด (Batch 3 ตอน): บทที่ {start_c} ถึง {start_c+2}...")
        
        def worker():
            results = []
            for i in range(start_c, start_c + 3):
                sub = ""
                for ot in self.current_story["outlines"]:
                    if ot["chapter"] == i:
                        sub = ot["subtitle"]
                        break
                text = self.novel_engine.generate_chapter(
                    story_title=self.current_story["title"],
                    chapter_num=i,
                    chapter_subtitle=sub,
                    genre=self.current_story.get("genre", "ผัวโบ้ / กลับมาเจอกัน"),
                    context_memory={"characters": self.current_story.get("characters", [])},
                    target_words=2000
                )
                results.append((i, text))
            return results

        self.current_worker = WorkerThread(worker)
        self.current_worker.finished_signal.connect(self.on_batch_generated)
        self.current_worker.start()

    def on_batch_generated(self, ok, results):
        if ok and results:
            for c_num, text in results:
                if c_num not in self.current_story["chapters"]:
                    self.current_story["chapters"][c_num] = {}
                self.current_story["chapters"][c_num]["content"] = text
                self.current_story["chapters"][c_num]["status"] = "แต่งแล้ว"
            self.refresh_chapter_cards()
            self.select_chapter(self.current_chapter_idx)
            self.save_local_story()
            self.log("แต่งแบบ Batch สำเร็จครบทุกตอน!")
            QMessageBox.information(self, "สำเร็จ", "แต่งนิยายแบบชุดรวดเดียว 3 ตอนสำเร็จเรียบร้อยแล้ว!")

    def critic_pass_chapter(self):
        text = self.editor_manuscript.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "แจ้งเตือน", "ไม่มีเนื้อหาให้ตรวจทาน")
            return
        
        self.log("กำลังดำเนินการตรวจทาน & เกลาสำนวน (Critic Pass)...")
        def worker():
            return self.novel_engine.critic_pass(text)

        self.current_worker = WorkerThread(worker)
        self.current_worker.finished_signal.connect(self.on_critic_passed)
        self.current_worker.start()

    def on_critic_passed(self, ok, new_text):
        if ok and new_text:
            self.editor_manuscript.setPlainText(new_text)
            self.save_local_story()
            self.log("ตรวจทานและเกลาสำนวนสำเร็จเรียบร้อยแล้ว!")
            QMessageBox.information(self, "สำเร็จ", "ระบบได้เกลาสำนวนและปรับแก้คำสะกดผิดเรียบร้อยแล้ว")

    def quick_upload_draft(self):
        art_id = self.current_story.get("article_id") or self.txt_pub_article_id.text().strip()
        if not art_id:
            QMessageBox.warning(self, "แจ้งเตือน", "กรุณาระบุ Article ID ของนิยายเรื่องนี้")
            return
        
        c_num = self.current_chapter_idx
        subtitle = ""
        for ot in self.current_story["outlines"]:
            if ot["chapter"] == c_num:
                subtitle = ot["subtitle"]
                break
        
        content = self.editor_manuscript.toPlainText()
        if not content.strip():
            QMessageBox.warning(self, "แจ้งเตือน", "บทนี้ยังไม่มีเนื้อหา")
            return

        self.log(f"กำลังส่งบทที่ {c_num}: {subtitle} ขึ้น ReadAWrite (แบบร่าง)...")
        def worker():
            return self.uploader.upload_chapter(art_id, f"บทที่ {c_num}", subtitle, content, publish_mode="draft")

        self.current_worker = WorkerThread(worker)
        self.current_worker.finished_signal.connect(lambda ok, res: self.on_uploaded(ok, res, "แบบร่าง"))
        self.current_worker.start()

    def trigger_readawrite_upload(self):
        art_id = self.txt_pub_article_id.text().strip()
        if not art_id:
            QMessageBox.warning(self, "แจ้งเตือน", "กรุณาระบุ Article ID")
            return

        c_idx = self.combo_pub_ch.currentData()
        subtitle = ""
        for ot in self.current_story["outlines"]:
            if ot["chapter"] == c_idx:
                subtitle = ot["subtitle"]
                break

        ch_data = self.current_story["chapters"].get(c_idx, {})
        content = ch_data.get("content", "")
        if not content.strip():
            QMessageBox.warning(self, "แจ้งเตือน", f"บทที่ {c_idx} ยังไม่มีเนื้อหา")
            return

        mode = "draft"
        sched_time = None
        if self.rad_publish.isChecked():
            mode = "publish"
        elif self.rad_schedule.isChecked():
            mode = "schedule"
            sched_time = self.dt_schedule.dateTime().toString("yyyy-MM-dd HH:mm")

        self.log(f"กำลังเริ่มกระบวนการอัปโหลดบทที่ {c_idx} โหมด: {mode}...")
        def worker():
            return self.uploader.upload_chapter(art_id, f"บทที่ {c_idx}", subtitle, content, publish_mode=mode, schedule_time=sched_time)

        self.current_worker = WorkerThread(worker)
        self.current_worker.finished_signal.connect(lambda ok, res: self.on_uploaded(ok, res, mode))
        self.current_worker.start()

    def on_uploaded(self, ok, res, mode):
        if ok:
            self.log(f"🎉 ส่งขึ้น ReadAWrite สำเร็จเรียบร้อยแล้ว ({mode})!")
            QMessageBox.information(self, "สำเร็จ", f"อัปโหลดบทนิยายขึ้น ReadAWrite สำเร็จเรียบร้อยแล้ว!\n(โหมด: {mode})")
        else:
            self.log(f"❌ อัปโหลดล้มเหลว: {res}")
            QMessageBox.critical(self, "ล้มเหลว", f"เกิดข้อผิดพลาดในการอัปโหลด: {res}")

    def save_local_story(self):
        os.makedirs(PROJECTS_DIR, exist_ok=True)
        local_path = os.path.join(PROJECTS_DIR, "story_meta.json")
        try:
            with open(local_path, "w", encoding="utf-8") as f:
                json.dump(self.current_story, f, ensure_ascii=False, indent=2)
            self.log("💾 บันทึกข้อมูลนิยายลงในเครื่องเรียบร้อยแล้ว")
        except Exception as e:
            self.log(f"บันทึกไฟล์ผิดพลาด: {e}")

    def export_all_txt(self):
        path, _ = QFileDialog.getSaveFileName(self, "บันทึกไฟล์นิยายรวม", f"{self.current_story['title']}_รวมทุกตอน.txt", "Text Files (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"เรื่อง: {self.current_story['title']}\n")
                f.write(f"หมวดหมู่: {self.current_story.get('genre', '')}\n")
                f.write("="*60 + "\n\n")
                for ot in self.current_story["outlines"]:
                    c_num = ot["chapter"]
                    sub = ot["subtitle"]
                    content = self.current_story["chapters"].get(c_num, {}).get("content", "")
                    f.write(f"บทที่ {c_num}: {sub}\n\n")
                    f.write(content + "\n\n")
                    f.write("-" * 50 + "\n\n")
            QMessageBox.information(self, "สำเร็จ", "ส่งออกไฟล์นิยายรวมเรียบร้อยแล้ว!")

    def export_current_txt(self):
        path, _ = QFileDialog.getSaveFileName(self, "บันทึกไฟล์บทปัจจุบัน", f"บทที่_{self.current_chapter_idx}.txt", "Text Files (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor_manuscript.toPlainText())
            QMessageBox.information(self, "สำเร็จ", "ส่งออกไฟล์บทปัจจุบันเรียบร้อยแล้ว!")

    def open_api_key_dialog(self):
        key, ok = QFileDialog.getText(self, "ตั้งค่า Gemini API Key", "ใส่ Google Gemini API Key ของคุณ (เว้นว่างไว้เพื่อใช้ Fallback AI Engine อัจฉริยะ):", text=self.config.get("gemini_api_key", "")) if hasattr(QFileDialog, "getText") else (None, False)
        # Fallback custom input if needed
        dlg = QDialog(self)
        dlg.setWindowTitle("ตั้งค่า Gemini API Key")
        dlg.setFixedSize(480, 180)
        dlg.setStyleSheet("background-color: #1a1625; color: #fff;")
        d_layout = QVBoxLayout(dlg)
        d_layout.addWidget(QLabel("🔑 ใส่ Google Gemini API Key:"))
        key_edit = QLineEdit(self.config.get("gemini_api_key", ""))
        key_edit.setStyleSheet("background-color: #120e1a; border: 1px solid #3d3356; border-radius: 4px; padding: 8px; color: #fbbf24;")
        d_layout.addWidget(key_edit)
        
        btn_box = QHBoxLayout()
        btn_save = QPushButton("บันทึก")
        btn_save.setStyleSheet("background-color: #f59e0b; color: #000; font-weight: bold; padding: 8px 16px; border-radius: 4px;")
        btn_save.clicked.connect(dlg.accept)
        btn_box.addWidget(btn_save)
        d_layout.addLayout(btn_box)
        
        if dlg.exec() == QDialog.DialogCode.Accepted:
            k = key_edit.text().strip()
            self.config["gemini_api_key"] = k
            save_config(self.config)
            self.novel_engine.api_key = k
            QMessageBox.information(self, "สำเร็จ", "บันทึก Gemini API Key เรียบร้อยแล้ว!")


def main():
    app = QApplication(sys.argv)
    window = ThaiNovelStudioPro()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
