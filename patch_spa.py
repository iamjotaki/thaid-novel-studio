# -*- coding: utf-8 -*-
"""
Script to inject multi-page SPA views into web_saas_stitch/index.html
Adds:
1. Interactive Nav Bar with view switching:
   - switchView('home')     : หน้าแรก (Home & Features & Pricing & Testimonials)
   - switchView('novels')   : จัดการนิยาย (My Novels Grid, + สร้างเรื่องใหม่)
   - switchView('studio')   : ห้องแต่งนิยาย (The full-featured 3-panel writer)
   - switchView('admin')    : จัดการสมาชิก (Admin Portal & Quota & Status)
   - switchView('login')    : เข้าสู่ระบบ / สมัครสมาชิก (Auth Portal)
2. Live API integration for novels, user management, and AI creation
"""

import os
import re

INDEX_PATH = r"c:\ReadAWrite\web_saas_stitch\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Navigation Bar
old_nav = '''<!-- Center Navigation Links (Exact Shared Component Array: ["หน้าแรก", "จัดการงานเขียน", "ตลาดพล็อต AI", "ตั้งเวลาเผยแพร่", "ราคา & แพ็กเกจ"]) -->
<nav class="hidden md:flex items-center gap-space-md">
<a class="text-on-surface-variant hover:text-on-surface text-label-md font-label-md px-1 py-1 transition-colors duration-150" href="#">หน้าแรก</a>
<a class="text-primary font-bold border-b-2 border-primary pb-1 text-label-md font-label-md px-1" href="#">จัดการงานเขียน</a>
<a class="text-on-surface-variant hover:text-on-surface text-label-md font-label-md px-1 py-1 transition-colors duration-150 flex items-center gap-1" href="#">
<span>ตลาดพล็อต AI</span>
<span class="bg-secondary-container text-secondary text-[9px] font-bold px-1 rounded-full">ใหม่</span>
</a>
<a class="text-on-surface-variant hover:text-on-surface text-label-md font-label-md px-1 py-1 transition-colors duration-150" href="#">ตั้งเวลาเผยแพร่</a>
<a class="text-on-surface-variant hover:text-on-surface text-label-md font-label-md px-1 py-1 transition-colors duration-150" href="#" onclick="document.getElementById('pricingModal').classList.remove('hidden')">ราคา &amp; แพ็กเกจ</a>
</nav>'''

new_nav = '''<!-- Interactive SaaS Navigation Bar -->
<nav class="hidden md:flex items-center gap-1 lg:gap-2">
  <button id="nav-btn-home" onclick="switchView('home')" class="nav-tab text-on-surface-variant hover:text-primary text-label-md font-label-md px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5">
    <span class="material-symbols-outlined text-[18px]">home</span>
    <span>หน้าแรก</span>
  </button>
  <button id="nav-btn-novels" onclick="switchView('novels')" class="nav-tab text-on-surface-variant hover:text-primary text-label-md font-label-md px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5">
    <span class="material-symbols-outlined text-[18px]">auto_stories</span>
    <span>จัดการนิยาย</span>
  </button>
  <button id="nav-btn-studio" onclick="switchView('studio')" class="nav-tab text-primary font-bold bg-primary-fixed/40 border-b-2 border-primary text-label-md font-label-md px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5">
    <span class="material-symbols-outlined text-[18px]">edit_square</span>
    <span>ห้องแต่งนิยาย (AI Studio)</span>
  </button>
  <button id="nav-btn-admin" onclick="switchView('admin')" class="nav-tab text-on-surface-variant hover:text-primary text-label-md font-label-md px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5">
    <span class="material-symbols-outlined text-[18px]">admin_panel_settings</span>
    <span>จัดการสมาชิก (Admin)</span>
    <span class="bg-primary text-white text-[9px] font-bold px-1.5 py-0.2 rounded-full">HQ</span>
  </button>
  <button onclick="document.getElementById('pricingModal').classList.remove('hidden')" class="nav-tab text-on-surface-variant hover:text-primary text-label-md font-label-md px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5">
    <span class="material-symbols-outlined text-[18px]">workspace_premium</span>
    <span>ราคา &amp; แพ็กเกจ</span>
  </button>
</nav>'''

if old_nav in html:
    html = html.replace(old_nav, new_nav)
    print("Successfully replaced nav bar!")
else:
    print("WARNING: old_nav not found exactly, will use regex or search")

# 2. Add Auth/Login button on the right trailing section
old_avatar_block = '''<!-- User Profile Avatar -->
<div class="flex items-center gap-2 pl-space-xs border-l border-outline-variant/30">
<div class="relative cursor-pointer">
<img class="w-9 h-9 rounded-full object-cover border border-outline-variant/40" data-alt="Close up photographic avatar of a creative young Thai female author named D-nee wearing glasses, smiling warm expression, modern pastel studio background with warm persimmon ambient light" src="https://lh3.googleusercontent.com/aida-public/AB6AXuC5JIIDjVm5RJHqLt5zzKhzieb6_NGwVVHh-mDhri5gy_Xbw6sSFARJRnyaInAbeaayCXjWKfrClfP9mEVtMm9wLw1nY5LHO2SjuOCvHAnNWDygGOzJ-Me9nIaAOj9xHtL1jSbs5YwGaR8gGqWnznD-PW4r7xs5CH8Q9-FHtkFLqaz0cz3L4GbHPBRgMg64le8gyu9d0n5JM--XzN74bcb_yAVXy3kUL4i-e9N4zWbFTl89G0-xdnVX28CAH9-NqQudErnP1JRlYj0"/>
<span class="absolute bottom-0 right-0 w-2.5 h-2.5 bg-secondary border-2 border-surface-container-lowest rounded-full"></span>
</div>
<div class="hidden 2xl:flex flex-col text-left">
<span class="text-label-md font-label-md leading-none text-on-surface">D-nee (นักเขียน Pro)</span>
<span class="text-label-sm font-label-sm text-outline">Author Level 4</span>
</div>
</div>'''

new_avatar_block = '''<!-- User Profile Avatar & Login Trigger -->
<div class="flex items-center gap-2 pl-space-xs border-l border-outline-variant/30">
  <button onclick="switchView('login')" class="relative cursor-pointer group flex items-center gap-2 text-left">
    <img class="w-9 h-9 rounded-full object-cover border border-outline-variant/40 group-hover:ring-2 ring-primary transition-all" data-alt="Close up photographic avatar of a creative young Thai female author named D-nee wearing glasses, smiling warm expression, modern pastel studio background with warm persimmon ambient light" src="https://lh3.googleusercontent.com/aida-public/AB6AXuC5JIIDjVm5RJHqLt5zzKhzieb6_NGwVVHh-mDhri5gy_Xbw6sSFARJRnyaInAbeaayCXjWKfrClfP9mEVtMm9wLw1nY5LHO2SjuOCvHAnNWDygGOzJ-Me9nIaAOj9xHtL1jSbs5YwGaR8gGqWnznD-PW4r7xs5CH8Q9-FHtkFLqaz0cz3L4GbHPBRgMg64le8gyu9d0n5JM--XzN74bcb_yAVXy3kUL4i-e9N4zWbFTl89G0-xdnVX28CAH9-NqQudErnP1JRlYj0"/>
    <span class="absolute bottom-0 left-6 w-2.5 h-2.5 bg-secondary border-2 border-surface-container-lowest rounded-full"></span>
    <div class="hidden xl:flex flex-col">
      <span class="text-label-md font-label-md leading-none text-on-surface group-hover:text-primary font-bold">D-nee (นักเขียน Pro)</span>
      <span class="text-label-sm font-label-sm text-outline">คลิกเพื่อจัดการบัญชี/เข้าสู่ระบบ</span>
    </div>
  </button>
</div>'''

if old_avatar_block in html:
    html = html.replace(old_avatar_block, new_avatar_block)
    print("Successfully replaced avatar block!")

# 3. Wrap current workspace in <div id="view-studio" class="page-view ...">
old_workspace_start = '<!-- MAIN WORKSPACE CONTAINER -->\n<div class="flex h-[calc(100vh-6.5rem)] overflow-hidden">'
new_workspace_start = '''<!-- ======================================================== -->
<!-- 1. VIEW: AI NOVEL STUDIO (ห้องแต่งนิยาย)                -->
<!-- ======================================================== -->
<div id="view-studio" class="page-view flex h-[calc(100vh-6.5rem)] overflow-hidden">'''

if old_workspace_start in html:
    html = html.replace(old_workspace_start, new_workspace_start)
    print("Successfully marked view-studio start!")

# 4. Define the Other Views HTML (Home, Novels, Admin, Login)
other_views_html = '''
<!-- ======================================================== -->
<!-- 2. VIEW: HOME & LANDING PAGE (หน้าแรกเว็บ SaaS)           -->
<!-- ======================================================== -->
<div id="view-home" class="page-view hidden overflow-y-auto h-[calc(100vh-6.5rem)] bg-[#fbfaf8] custom-scrollbar">
  <!-- Hero Section -->
  <section class="max-w-6xl mx-auto px-6 pt-12 pb-16 text-center">
    <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary-fixed text-on-primary-fixed text-sm font-bold mb-6 border border-primary-fixed-dim shadow-xs">
      <span class="material-symbols-outlined text-[18px] text-primary">auto_awesome</span>
      <span>ระบบแต่งนิยายพลัง AI อัตโนมัติอันดับ 1 สำหรับนักเขียน ReadAWrite</span>
    </div>
    <h1 class="text-4xl md:text-6xl font-extrabold text-on-surface leading-tight tracking-tight mb-6">
      แต่งนิยายเร็วกว่าเดิม 10 เท่า <br/>
      <span class="bg-gradient-to-r from-primary via-primary-container to-secondary bg-clip-text text-transparent">
        สำนวนภาษาไทยสละสลวย พร้อมซิงค์ขึ้น ReadAWrite อัตโนมัติ
      </span>
    </h1>
    <p class="text-lg md:text-xl text-on-surface-variant max-w-3xl mx-auto mb-10 leading-relaxed">
      ลืมปัญหาตันพล็อต แต่งช้า หรือเขียนไม่ทันส่งการบ้านไปได้เลย ด้วย AI อัจฉริยะที่เข้าใจกลิ่นอาย นิยายโรมานซ์ ผัวโบ้ มาเฟีย แฟนตาซี พร้อมจำกัดคำไม่ให้ตกหล่นและส่งขึ้น ReadAWrite ได้ในคลิกเดียว
    </p>
    <div class="flex flex-wrap justify-center gap-4">
      <button onclick="switchView('studio')" class="px-8 py-3.5 bg-primary hover:bg-primary-container text-white text-base font-bold rounded-xl shadow-lg hover:shadow-xl transition-all transform active:scale-95 flex items-center gap-2">
        <span class="material-symbols-outlined text-[20px]">edit_note</span>
        <span>เริ่มแต่งนิยายตอนนี้ (ทดลองฟรี 7 วัน)</span>
      </button>
      <button onclick="document.getElementById('pricingModal').classList.remove('hidden')" class="px-6 py-3.5 bg-surface-container hover:bg-surface-container-high text-on-surface text-base font-bold rounded-xl border border-outline-variant/40 transition-all flex items-center gap-2">
        <span class="material-symbols-outlined text-[20px]">diamond</span>
        <span>ดูแพ็กเกจราคา & สมาชิก</span>
      </button>
    </div>

    <!-- Live System Highlights Grid -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mt-16 text-left">
      <div class="bg-surface-container-lowest p-6 rounded-2xl border border-outline-variant/30 shadow-xs">
        <div class="w-12 h-12 rounded-xl bg-primary-fixed flex items-center justify-center text-primary mb-4">
          <span class="material-symbols-outlined text-[28px]">speed</span>
        </div>
        <h3 class="text-lg font-bold text-on-surface mb-2">แต่งไวใน 19 วินาที</h3>
        <p class="text-sm text-on-surface-variant leading-relaxed">สปีดสูงสุดด้วย Gemini 3.5 Flash Lite ผลิตเนื้อหา 3,000-4,000 คำต่อตอนโดยไม่ค้าง</p>
      </div>
      <div class="bg-surface-container-lowest p-6 rounded-2xl border border-outline-variant/30 shadow-xs">
        <div class="w-12 h-12 rounded-xl bg-secondary-container flex items-center justify-center text-secondary mb-4">
          <span class="material-symbols-outlined text-[28px]">sync_saved_locally</span>
        </div>
        <h3 class="text-lg font-bold text-on-surface mb-2">อัปโหลด ReadAWrite</h3>
        <p class="text-sm text-on-surface-variant leading-relaxed">ส่งเนื้อหาขึ้นเป็นแบบร่าง หรือตั้งเวลาเผยแพร่อัตโนมัติผ่านระบบ Headless Browser ปลอดภัย 100%</p>
      </div>
      <div class="bg-surface-container-lowest p-6 rounded-2xl border border-outline-variant/30 shadow-xs">
        <div class="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center text-amber-700 mb-4">
          <span class="material-symbols-outlined text-[28px]">spellcheck</span>
        </div>
        <h3 class="text-lg font-bold text-on-surface mb-2">ProofAI ตรวจสำนวน</h3>
        <p class="text-sm text-on-surface-variant leading-relaxed">ตรวจคำผิด วรรคตอน สำนวนภาษาไทยแท้ ตัดคำด้วย PyThaiNLP เที่ยงตรงทุกตัวอักษร</p>
      </div>
      <div class="bg-surface-container-lowest p-6 rounded-2xl border border-outline-variant/30 shadow-xs">
        <div class="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center text-purple-700 mb-4">
          <span class="material-symbols-outlined text-[28px]">memory</span>
        </div>
        <h3 class="text-lg font-bold text-on-surface mb-2">ความจำต่อเนื่อง</h3>
        <p class="text-sm text-on-surface-variant leading-relaxed">จดจำคาแรคเตอร์ตัวละคร ปมปริศนา ไม่ให้ AI ลืมชื่อหรือเปลี่ยนบุคลิกในบทถัดไป</p>
      </div>
    </div>
  </section>

  <!-- Pricing Preview Section on Landing -->
  <section class="bg-surface-container-low py-16 border-t border-outline-variant/30">
    <div class="max-w-6xl mx-auto px-6 text-center">
      <span class="text-xs font-bold text-primary tracking-wider uppercase">แพ็กเกจสมาชิกที่เหมาะกับคุณ</span>
      <h2 class="text-3xl font-bold text-on-surface mt-2 mb-10">เลือกแผนที่ใช่สำหรับเส้นทางนักเขียนมืออาชีพ</h2>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 text-left">
        <!-- Trial Card -->
        <div class="bg-white p-6 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col justify-between">
          <div>
            <span class="text-xs font-bold text-outline">เริ่มต้นทดลอง</span>
            <h3 class="text-xl font-bold text-on-surface mt-1">7-Day Free Trial</h3>
            <div class="text-2xl font-bold text-on-surface mt-2">ฟรี <span class="text-xs text-outline font-normal">/ 7 วัน</span></div>
            <ul class="mt-4 space-y-2 text-xs text-on-surface-variant">
              <li>✓ โควตา AI 300,000 คำ</li>
              <li>✓ ซิงค์บทความขึ้น ReadAWrite</li>
              <li>✓ พล็อตตัวละครและโครงเรื่อง</li>
            </ul>
          </div>
          <button onclick="switchView('studio')" class="w-full mt-6 py-2 bg-surface-container text-on-surface hover:bg-surface-container-high font-bold text-xs rounded-lg transition-all">เริ่มใช้งานทันที</button>
        </div>
        <!-- Monthly Card -->
        <div class="bg-white p-6 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col justify-between">
          <div>
            <span class="text-xs font-bold text-secondary">รายเดือน</span>
            <h3 class="text-xl font-bold text-on-surface mt-1">Pro Monthly</h3>
            <div class="text-2xl font-bold text-primary mt-2">฿390 <span class="text-xs text-outline font-normal">/ เดือน</span></div>
            <ul class="mt-4 space-y-2 text-xs text-on-surface-variant">
              <li>✓ โควตา AI 500,000 คำต่อเดือน</li>
              <li>✓ ซิงค์อัตโนมัติไม่จำกัดเรื่อง</li>
              <li>✓ ตรวจคำผิด ProofAI อัจฉริยะ</li>
            </ul>
          </div>
          <button onclick="document.getElementById('pricingModal').classList.remove('hidden')" class="w-full mt-6 py-2 bg-primary text-white hover:bg-primary-container font-bold text-xs rounded-lg transition-all">สมัครรายเดือน</button>
        </div>
        <!-- Annual Card -->
        <div class="bg-white p-6 rounded-2xl border-2 border-primary shadow-md relative flex flex-col justify-between">
          <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-white text-[10px] font-bold px-3 py-0.5 rounded-full">คุ้มค่าที่สุด ประหยัด 2 เดือน</div>
          <div>
            <span class="text-xs font-bold text-primary">รายปี</span>
            <h3 class="text-xl font-bold text-on-surface mt-1">Pro Annual</h3>
            <div class="text-2xl font-bold text-primary mt-2">฿3,900 <span class="text-xs text-outline font-normal">/ ปี</span></div>
            <ul class="mt-4 space-y-2 text-xs text-on-surface-variant">
              <li>✓ โควตา AI 6,000,000 คำต่อปี</li>
              <li>✓ โมเดลพรีเมียมเร่งสปีด 2X</li>
              <li>✓ ตั้งเวลาเผยแพร่อัตโนมัติ 30 วัน</li>
            </ul>
          </div>
          <button onclick="document.getElementById('pricingModal').classList.remove('hidden')" class="w-full mt-6 py-2 bg-primary text-white hover:bg-primary-container font-bold text-xs rounded-lg transition-all">สมัครรายปี (฿325/ด.)</button>
        </div>
        <!-- Lifetime Card -->
        <div class="bg-white p-6 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col justify-between">
          <div>
            <span class="text-xs font-bold text-amber-700">จ่ายครั้งเดียวจบ</span>
            <h3 class="text-xl font-bold text-on-surface mt-1">Lifetime VIP</h3>
            <div class="text-2xl font-bold text-on-surface mt-2">฿6,900 <span class="text-xs text-outline font-normal">/ ตลอดชีพ</span></div>
            <ul class="mt-4 space-y-2 text-xs text-on-surface-variant">
              <li>✓ ใช้งานทุกฟีเจอร์ตลอดชีพ ไม่ต้องต่ออายุ</li>
              <li>✓ ซัปพอร์ตแบบ VIP Priority 24 ชม.</li>
              <li>✓ เข้ากลุ่มเคล็ดลับนักเขียนเงินล้าน</li>
            </ul>
          </div>
          <button onclick="document.getElementById('pricingModal').classList.remove('hidden')" class="w-full mt-6 py-2 bg-neutral-900 text-white hover:bg-black font-bold text-xs rounded-lg transition-all">สมัคร Lifetime VIP</button>
        </div>
      </div>
    </div>
  </section>
</div>

<!-- ======================================================== -->
<!-- 3. VIEW: NOVELS MANAGEMENT (หน้าจัดการนิยายของฉัน)        -->
<!-- ======================================================== -->
<div id="view-novels" class="page-view hidden overflow-y-auto h-[calc(100vh-6.5rem)] bg-[#fbfaf8] custom-scrollbar p-6">
  <div class="max-w-6xl mx-auto">
    <!-- Header with Action -->
    <div class="flex flex-wrap items-center justify-between gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-extrabold text-on-surface">นิยายและผลงานของฉัน</h1>
        <p class="text-sm text-on-surface-variant mt-1">จัดการเรื่องย่อ ตัวละคร สารบัญตอน และส่งซิงค์ไปยัง ReadAWrite</p>
      </div>
      <button onclick="document.getElementById('createNovelModal').classList.remove('hidden')" class="px-5 py-2.5 bg-primary hover:bg-primary-container text-white text-sm font-bold rounded-xl shadow-sm transition-all flex items-center gap-2">
        <span class="material-symbols-outlined text-[20px]">add_circle</span>
        <span>+ สร้างนิยายเรื่องใหม่</span>
      </button>
    </div>

    <!-- Filter & Search Bar -->
    <div class="flex flex-wrap items-center justify-between gap-4 mb-6 bg-white p-3.5 rounded-xl border border-outline-variant/30 shadow-2xs">
      <div class="flex items-center gap-2">
        <button class="px-3 py-1 bg-primary text-white text-xs font-bold rounded-lg">ทั้งหมด (3)</button>
        <button class="px-3 py-1 bg-surface-container hover:bg-surface-container-high text-on-surface-variant text-xs font-semibold rounded-lg">กำลังเขียน (2)</button>
        <button class="px-3 py-1 bg-surface-container hover:bg-surface-container-high text-on-surface-variant text-xs font-semibold rounded-lg">จบแล้ว (1)</button>
      </div>
      <div class="text-xs text-outline">
        บัญชี ReadAWrite ที่เชื่อมต่อ: <span class="text-secondary font-bold">i_Am_Status 🟢</span>
      </div>
    </div>

    <!-- Novels Grid -->
    <div id="novelsGrid" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Injected via JavaScript from /api/novels -->
    </div>
  </div>
</div>

<!-- ======================================================== -->
<!-- 4. VIEW: ADMIN MANAGEMENT PORTAL (หน้าจัดการของแอดมิน)    -->
<!-- ======================================================== -->
<div id="view-admin" class="page-view hidden overflow-y-auto h-[calc(100vh-6.5rem)] bg-[#fbfaf8] custom-scrollbar p-6">
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Admin Header -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="px-2.5 py-0.5 rounded bg-primary text-white text-xs font-bold uppercase tracking-wider">Super Admin</span>
          <h1 class="text-2xl md:text-3xl font-extrabold text-on-surface">ศูนย์ควบคุมระบบสมาชิกและสถิติแพลตฟอร์ม</h1>
        </div>
        <p class="text-sm text-on-surface-variant mt-1">ควบคุมโควตา AI จัดการสถานะสมาชิก (Active/Trial/Expired) และดูสถานะ API Gemini</p>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="loadAdminData()" class="px-3 py-2 bg-white hover:bg-surface-container border border-outline-variant/40 rounded-lg text-xs font-bold text-on-surface flex items-center gap-1">
          <span class="material-symbols-outlined text-[16px]">refresh</span>
          <span>รีเฟรชข้อมูล</span>
        </button>
      </div>
    </div>

    <!-- Admin KPI Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-white p-5 rounded-2xl border border-outline-variant/30 shadow-xs">
        <span class="text-xs font-semibold text-outline">สมาชิกทั้งหมด</span>
        <div class="text-2xl font-extrabold text-on-surface mt-1" id="stat-total-users">5 คน</div>
        <span class="text-xs text-secondary font-medium">🟢 ใช้งานอยู่ 3 คน</span>
      </div>
      <div class="bg-white p-5 rounded-2xl border border-outline-variant/30 shadow-xs">
        <span class="text-xs font-semibold text-outline">ยอดคำ AI ที่แต่งไปแล้ว</span>
        <div class="text-2xl font-extrabold text-primary mt-1" id="stat-words-generated">3,145,500 คำ</div>
        <span class="text-xs text-outline font-medium">PyThaiNLP Tokenized</span>
      </div>
      <div class="bg-white p-5 rounded-2xl border border-outline-variant/30 shadow-xs">
        <span class="text-xs font-semibold text-outline">รายได้ประมาณการเดือนนี้</span>
        <div class="text-2xl font-extrabold text-emerald-700 mt-1" id="stat-revenue">฿142,500</div>
        <span class="text-xs text-emerald-600 font-medium">+18% จากเดือนก่อน</span>
      </div>
      <div class="bg-white p-5 rounded-2xl border border-outline-variant/30 shadow-xs">
        <span class="text-xs font-semibold text-outline">สถานะ Gemini Engine</span>
        <div class="text-base font-bold text-emerald-600 mt-1 flex items-center gap-1">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
          <span>Online (Flash Lite)</span>
        </div>
        <span class="text-xs text-outline font-medium">เวลาตอบสนองเฉลี่ย: 18-22s</span>
      </div>
    </div>

    <!-- Members Management Table -->
    <div class="bg-white rounded-2xl border border-outline-variant/30 shadow-xs overflow-hidden">
      <div class="p-4 border-b border-outline-variant/30 flex items-center justify-between">
        <h3 class="text-lg font-bold text-on-surface">รายชื่อสมาชิกและการใช้งานโควตา</h3>
        <span class="text-xs text-outline">คลิกปุ่ม "จัดการ" เพื่อเพิ่มโควตาหรือเปลี่ยนแพ็กเกจ</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-surface-container-low text-xs font-bold text-on-surface-variant uppercase">
            <tr>
              <th class="p-3.5">รหัส / ผู้ใช้</th>
              <th class="p-3.5">อีเมล</th>
              <th class="p-3.5">แพ็กเกจ</th>
              <th class="p-3.5">สถานะ</th>
              <th class="p-3.5">โควตาคำ (ใช้แล้ว / ทั้งหมด)</th>
              <th class="p-3.5">วันหมดอายุ</th>
              <th class="p-3.5 text-right">การจัดการ</th>
            </tr>
          </thead>
          <tbody id="adminUserTableBody" class="divide-y divide-outline-variant/20">
            <!-- Injected via JavaScript from /api/admin/users -->
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<!-- ======================================================== -->
<!-- 5. VIEW: AUTH & LOGIN / REGISTER (หน้าเข้าสู่ระบบ)        -->
<!-- ======================================================== -->
<div id="view-login" class="page-view hidden overflow-y-auto h-[calc(100vh-6.5rem)] bg-[#fbfaf8] custom-scrollbar p-6 flex items-center justify-center">
  <div class="max-w-md w-full bg-white rounded-3xl p-8 border border-outline-variant/40 shadow-xl text-center">
    <div class="w-14 h-14 bg-primary text-white rounded-2xl mx-auto flex items-center justify-center shadow-md mb-4">
      <span class="material-symbols-outlined text-[32px]">stylus_note</span>
    </div>
    <h2 class="text-2xl font-extrabold text-on-surface">เข้าสู่ระบบ ReadAWrite Pro Studio</h2>
    <p class="text-xs text-on-surface-variant mt-1 mb-6">เชื่อมต่อบัญชีนักเขียน เพื่อใช้งาน AI และซิงค์ขึ้นเว็บอัตโนมัติ</p>

    <!-- Social Sign In -->
    <div class="space-y-3 mb-6">
      <button onclick="simulateLogin('Google')" class="w-full py-2.5 px-4 bg-white hover:bg-surface-container-low border border-outline-variant/40 rounded-xl text-xs font-bold text-on-surface flex items-center justify-center gap-3 transition-all">
        <svg class="w-4 h-4" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
        <span>เข้าสู่ระบบด้วย Google Account</span>
      </button>
      <button onclick="simulateLogin('ReadAWrite Connect')" class="w-full py-2.5 px-4 bg-primary text-white hover:bg-primary-container rounded-xl text-xs font-bold flex items-center justify-center gap-2 shadow-sm transition-all">
        <span class="material-symbols-outlined text-[16px]">sync_alt</span>
        <span>เชื่อมโยงผ่านบัญชี ReadAWrite (i_Am_Status)</span>
      </button>
    </div>

    <div class="flex items-center my-4">
      <div class="flex-1 border-t border-outline-variant/30"></div>
      <span class="px-3 text-[11px] text-outline uppercase font-semibold">หรือใช้อีเมล</span>
      <div class="flex-1 border-t border-outline-variant/30"></div>
    </div>

    <!-- Email Form -->
    <form onsubmit="event.preventDefault(); simulateLogin('Email');" class="space-y-3 text-left">
      <div>
        <label class="block text-xs font-bold text-on-surface mb-1">อีเมลผู้ใช้งาน</label>
        <input type="email" value="dnee.writer@readawrite.pro" class="w-full px-3 py-2 text-xs bg-surface-container-low rounded-lg border border-outline-variant/40 focus:border-primary outline-none" required />
      </div>
      <div>
        <label class="block text-xs font-bold text-on-surface mb-1">รหัสผ่าน</label>
        <input type="password" value="••••••••••••" class="w-full px-3 py-2 text-xs bg-surface-container-low rounded-lg border border-outline-variant/40 focus:border-primary outline-none" required />
      </div>
      <button type="submit" class="w-full py-2.5 bg-neutral-900 hover:bg-black text-white text-xs font-bold rounded-xl transition-all shadow-sm">
        เข้าสู่ระบบทันที
      </button>
    </form>
    <p class="text-[11px] text-outline mt-4">ยังไม่มีบัญชี? ระบบจะเปิดบัญชีทดลองใช้ 7 วันฟรีให้อัตโนมัติเมื่อกดเข้าสู่ระบบ</p>
  </div>
</div>

<!-- ======================================================== -->
<!-- MODAL: CREATE NOVEL DIALOG                               -->
<!-- ======================================================== -->
<div class="hidden fixed inset-0 z-50 overflow-y-auto bg-inverse-surface/40 backdrop-blur-sm flex items-center justify-center p-4" id="createNovelModal">
  <div class="bg-white max-w-lg w-full rounded-2xl shadow-2xl border border-outline-variant/40 overflow-hidden">
    <div class="p-5 border-b border-outline-variant/30 flex justify-between items-center bg-surface-container-low">
      <h3 class="text-lg font-bold text-on-surface flex items-center gap-2">
        <span class="material-symbols-outlined text-primary">add_box</span>
        <span>สร้างนิยายเรื่องใหม่</span>
      </h3>
      <button onclick="document.getElementById('createNovelModal').classList.add('hidden')" class="p-1 rounded-lg text-outline hover:text-on-surface">
        <span class="material-symbols-outlined text-[20px]">close</span>
      </button>
    </div>
    <form onsubmit="event.preventDefault(); submitCreateNovel();" class="p-5 space-y-4 text-left">
      <div>
        <label class="block text-xs font-bold text-on-surface mb-1">ชื่อเรื่องนิยาย *</label>
        <input id="newNovelTitle" type="text" placeholder="เช่น เล่ห์รักท่านประธานร้าย" class="w-full px-3 py-2 text-xs bg-surface-container-low rounded-lg border border-outline-variant/40 focus:border-primary outline-none" required />
      </div>
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs font-bold text-on-surface mb-1">หมวดหมู่หลัก</label>
          <select id="newNovelCategory" class="w-full px-3 py-2 text-xs bg-surface-container-low rounded-lg border border-outline-variant/40 focus:border-primary outline-none">
            <option value="โรมานซ์">โรมานซ์ / รักหวานแหวว</option>
            <option value="ดราม่า">ดราม่า / แก้แค้น</option>
            <option value="แฟนตาซี">แฟนตาซี / ย้อนยุค</option>
            <option value="วาย / Boy Love">นิยายวาย (Boy Love)</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold text-on-surface mb-1">สไตล์พล็อต (Genre)</label>
          <input id="newNovelGenre" type="text" value="ผัวโบ้ / กลับมาเจอกัน" class="w-full px-3 py-2 text-xs bg-surface-container-low rounded-lg border border-outline-variant/40 focus:border-primary outline-none" />
        </div>
      </div>
      <div>
        <label class="block text-xs font-bold text-on-surface mb-1">เรื่องย่อ (Synopsis)</label>
        <textarea id="newNovelSynopsis" rows="3" placeholder="เขียนเรื่องย่อสั้นๆ สำหรับให้ AI ใช้เป็นโครงสร้างเนื้อหา..." class="w-full px-3 py-2 text-xs bg-surface-container-low rounded-lg border border-outline-variant/40 focus:border-primary outline-none"></textarea>
      </div>
      <div class="flex justify-end gap-2 pt-2 border-t border-outline-variant/30">
        <button type="button" onclick="document.getElementById('createNovelModal').classList.add('hidden')" class="px-4 py-2 text-xs font-semibold text-outline hover:text-on-surface">ยกเลิก</button>
        <button type="submit" class="px-5 py-2 bg-primary hover:bg-primary-container text-white text-xs font-bold rounded-lg shadow-sm">สร้างและเปิดแต่งทันที</button>
      </div>
    </form>
  </div>
</div>

<!-- ======================================================== -->
<!-- MODAL: EDIT USER QUOTA & PLAN (ADMIN)                    -->
<!-- ======================================================== -->
<div class="hidden fixed inset-0 z-50 overflow-y-auto bg-inverse-surface/40 backdrop-blur-sm flex items-center justify-center p-4" id="editUserModal">
  <div class="bg-white max-w-md w-full rounded-2xl shadow-2xl border border-outline-variant/40 overflow-hidden">
    <div class="p-4 border-b border-outline-variant/30 flex justify-between items-center bg-surface-container-low">
      <h3 class="text-base font-bold text-on-surface flex items-center gap-1.5">
        <span class="material-symbols-outlined text-primary">manage_accounts</span>
        <span>แก้ไขสถานะและโควตาสมาชิก</span>
      </h3>
      <button onclick="document.getElementById('editUserModal').classList.add('hidden')" class="p-1 rounded-lg text-outline hover:text-on-surface">
        <span class="material-symbols-outlined text-[20px]">close</span>
      </button>
    </div>
    <form onsubmit="event.preventDefault(); submitUpdateUser();" class="p-4 space-y-3 text-left">
      <input type="hidden" id="editUserId" />
      <div>
        <label class="block text-xs font-bold text-on-surface mb-1">ชื่อผู้ใช้</label>
        <input id="editUserName" type="text" class="w-full px-3 py-1.5 text-xs bg-surface-container rounded-lg border border-outline-variant/40 text-outline cursor-not-allowed" readonly />
      </div>
      <div>
        <label class="block text-xs font-bold text-on-surface mb-1">แพ็กเกจ (Plan)</label>
        <select id="editUserPlan" class="w-full px-3 py-1.5 text-xs bg-surface-container-low rounded-lg border border-outline-variant/40 focus:border-primary outline-none">
          <option value="Pro Trial (7 วัน)">Pro Trial (7 วัน)</option>
          <option value="Pro Monthly (รายเดือน)">Pro Monthly (รายเดือน)</option>
          <option value="Pro Annual (รายปี)">Pro Annual (รายปี)</option>
          <option value="Lifetime VIP">Lifetime VIP (ตลอดชีพ)</option>
        </select>
      </div>
      <div>
        <label class="block text-xs font-bold text-on-surface mb-1">สถานะสมาชิก</label>
        <select id="editUserStatus" class="w-full px-3 py-1.5 text-xs bg-surface-container-low rounded-lg border border-outline-variant/40 focus:border-primary outline-none">
          <option value="Active (ทดลอง)">Active (ทดลอง)</option>
          <option value="Active (ปกติ)">Active (ปกติ)</option>
          <option value="Active (ตลอดชีพ)">Active (ตลอดชีพ)</option>
          <option value="Expired (หมดอายุ)">Expired (หมดอายุ)</option>
        </select>
      </div>
      <div>
        <label class="block text-xs font-bold text-on-surface mb-1">เติมโควตาคำ AI เพิ่มเติม (+คำ)</label>
        <input id="editUserQuotaAdd" type="number" step="10000" placeholder="เช่น 100000" class="w-full px-3 py-1.5 text-xs bg-surface-container-low rounded-lg border border-outline-variant/40 focus:border-primary outline-none" />
      </div>
      <div class="flex justify-end gap-2 pt-2 border-t border-outline-variant/30">
        <button type="button" onclick="document.getElementById('editUserModal').classList.add('hidden')" class="px-3 py-1.5 text-xs font-semibold text-outline hover:text-on-surface">ยกเลิก</button>
        <button type="submit" class="px-4 py-1.5 bg-primary hover:bg-primary-container text-white text-xs font-bold rounded-lg shadow-sm">บันทึกการเปลี่ยนแปลง</button>
      </div>
    </form>
  </div>
</div>
'''

# We need to insert other_views_html right before the pricingModal
target_pricing_modal = '<!-- 4. PRICING MODAL & MEMBERSHIP DRAWER (Interactive Popover) -->'
if target_pricing_modal in html:
    html = html.replace(target_pricing_modal, other_views_html + "\n" + target_pricing_modal)
    print("Successfully injected all new views before pricingModal!")
else:
    print("WARNING: pricingModal comment target not found!")

# 5. Add JavaScript SPA Router & APIs at the bottom of the script
spa_js = '''
// ==========================================
// SPA ROUTER & VIEW SWITCHER
// ==========================================
function switchView(viewName) {
  const views = ['home', 'novels', 'studio', 'admin', 'login'];
  views.forEach(v => {
    const el = document.getElementById('view-' + v);
    if (el) {
      if (v === viewName) {
        el.classList.remove('hidden');
      } else {
        el.classList.add('hidden');
      }
    }
    const navBtn = document.getElementById('nav-btn-' + v);
    if (navBtn) {
      if (v === viewName) {
        navBtn.className = "nav-tab text-primary font-bold bg-primary-fixed/40 border-b-2 border-primary text-label-md font-label-md px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5";
      } else {
        navBtn.className = "nav-tab text-on-surface-variant hover:text-primary text-label-md font-label-md px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5";
      }
    }
  });

  if (viewName === 'novels') loadNovels();
  if (viewName === 'admin') loadAdminData();

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ==========================================
// NOVELS MANAGEMENT FUNCTIONS
// ==========================================
function loadNovels() {
  fetch('/api/novels')
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        renderNovelsGrid(data.novels);
      }
    })
    .catch(err => showToast("โหลดนิยายไม่สำเร็จ: " + err.message, "error"));
}

function renderNovelsGrid(novels) {
  const grid = document.getElementById('novelsGrid');
  if (!grid) return;
  grid.innerHTML = novels.map(n => `
    <div class="bg-white rounded-2xl border border-outline-variant/30 shadow-xs hover:shadow-md transition-all overflow-hidden flex flex-col justify-between">
      <div>
        <div class="h-44 w-full overflow-hidden relative bg-surface-container-low">
          <img src="${n.cover}" class="w-full h-full object-cover" />
          <span class="absolute top-3 right-3 px-2 py-0.5 rounded-full text-[10px] font-bold ${n.status === 'กำลังเขียน' ? 'bg-secondary text-white' : 'bg-neutral-800 text-white'}">
            ${n.status}
          </span>
          <span class="absolute bottom-3 left-3 px-2 py-0.5 rounded text-[10px] font-bold bg-black/60 text-white backdrop-blur-xs">
            ${n.category}
          </span>
        </div>
        <div class="p-4">
          <h3 class="text-base font-bold text-on-surface line-clamp-1">${n.title}</h3>
          <p class="text-xs text-primary font-medium mt-0.5">${n.genre}</p>
          <p class="text-xs text-on-surface-variant mt-2 line-clamp-2 leading-relaxed">${n.synopsis}</p>
          <div class="flex items-center gap-3 mt-4 text-[11px] text-outline border-t border-outline-variant/20 pt-3">
            <span>📝 ${n.chapters_count} ตอน</span>
            <span>📊 ${Number(n.words_total).toLocaleString()} คำ</span>
            <span>👁️ ${n.reads}</span>
            <span>❤️ ${n.likes}</span>
          </div>
        </div>
      </div>
      <div class="p-4 pt-0 flex gap-2">
        <button onclick="openNovelStudio('${n.title}', '${n.genre}')" class="flex-1 py-2 bg-primary hover:bg-primary-container text-white text-xs font-bold rounded-lg transition-all flex items-center justify-center gap-1 shadow-xs">
          <span class="material-symbols-outlined text-[16px]">edit</span>
          <span>เข้าห้องแต่งนิยาย</span>
        </button>
        <button onclick="showToast('ซิงค์ข้อมูลกับ ReadAWrite เรียบร้อยแล้ว', 'success')" class="p-2 border border-outline-variant/40 rounded-lg hover:bg-surface-container text-on-surface-variant" title="ซิงค์ ReadAWrite">
          <span class="material-symbols-outlined text-[16px]">cloud_sync</span>
        </button>
      </div>
    </div>
  `).join('');
}

function openNovelStudio(title, genre) {
  currentStory.title = title;
  currentStory.genre = genre;
  const titleDisplay = document.querySelector(".text-title-md.font-title-md.text-on-surface.font-bold");
  if (titleDisplay) titleDisplay.innerText = title;
  switchView('studio');
  showToast("📖 เปิดโครงสร้างเรื่อง: " + title, "info");
}

function submitCreateNovel() {
  const title = document.getElementById('newNovelTitle').value;
  const category = document.getElementById('newNovelCategory').value;
  const genre = document.getElementById('newNovelGenre').value;
  const synopsis = document.getElementById('newNovelSynopsis').value;

  fetch('/api/novels/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, category, genre, synopsis })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      document.getElementById('createNovelModal').classList.add('hidden');
      showToast("🎉 สร้างนิยายเรื่อง '" + title + "' เรียบร้อยแล้ว!", "success");
      loadNovels();
      openNovelStudio(title, genre);
    }
  })
  .catch(err => showToast("สร้างไม่สำเร็จ: " + err.message, "error"));
}

// ==========================================
// ADMIN DASHBOARD FUNCTIONS
// ==========================================
let allAdminUsers = [];

function loadAdminData() {
  fetch('/api/admin/stats')
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        const s = data.stats;
        document.getElementById('stat-total-users').innerText = s.total_users + ' คน';
        document.getElementById('stat-words-generated').innerText = Number(s.ai_words_generated).toLocaleString() + ' คำ';
        document.getElementById('stat-revenue').innerText = s.monthly_revenue;
      }
    });

  fetch('/api/admin/users')
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        allAdminUsers = data.users;
        renderAdminUserTable(data.users);
      }
    });
}

function renderAdminUserTable(users) {
  const tbody = document.getElementById('adminUserTableBody');
  if (!tbody) return;
  tbody.innerHTML = users.map(u => `
    <tr class="hover:bg-surface-container-lowest transition-colors">
      <td class="p-3.5">
        <div class="font-bold text-on-surface">${u.name}</div>
        <div class="text-[11px] text-outline font-mono">${u.id} • สมัคร ${u.created_at}</div>
      </td>
      <td class="p-3.5 text-outline text-xs">${u.email}</td>
      <td class="p-3.5">
        <span class="px-2 py-0.5 rounded text-xs font-semibold ${u.plan.includes('VIP') ? 'bg-amber-100 text-amber-800' : u.plan.includes('Annual') ? 'bg-primary-fixed text-primary' : 'bg-surface-container text-on-surface-variant'}">
          ${u.plan}
        </span>
      </td>
      <td class="p-3.5">
        <span class="inline-flex items-center gap-1 text-xs font-bold ${u.status.includes('Active') ? 'text-secondary' : 'text-error'}">
          <span class="w-1.5 h-1.5 rounded-full ${u.status.includes('Active') ? 'bg-secondary' : 'bg-error'}"></span>
          ${u.status}
        </span>
      </td>
      <td class="p-3.5">
        <div class="text-xs font-bold text-on-surface">${Number(u.quota_used).toLocaleString()} / ${Number(u.quota_total).toLocaleString()} คำ</div>
        <div class="w-28 bg-surface-container-high rounded-full h-1.5 mt-1 overflow-hidden">
          <div class="bg-primary h-1.5 rounded-full" style="width: ${Math.min(100, Math.round((u.quota_used / u.quota_total) * 100))}%"></div>
        </div>
      </td>
      <td class="p-3.5 text-xs text-on-surface-variant">${u.expires_in}</td>
      <td class="p-3.5 text-right">
        <button onclick="openEditUser('${u.id}')" class="px-2.5 py-1 bg-surface-container hover:bg-surface-container-high border border-outline-variant/40 rounded-lg text-xs font-bold text-primary transition-all">
          จัดการ
        </button>
      </td>
    </tr>
  `).join('');
}

function openEditUser(userId) {
  const u = allAdminUsers.find(x => x.id === userId);
  if (!u) return;
  document.getElementById('editUserId').value = u.id;
  document.getElementById('editUserName').value = u.name + " (" + u.email + ")";
  document.getElementById('editUserPlan').value = u.plan;
  document.getElementById('editUserStatus').value = u.status;
  document.getElementById('editUserQuotaAdd').value = "";
  document.getElementById('editUserModal').classList.remove('hidden');
}

function submitUpdateUser() {
  const user_id = document.getElementById('editUserId').value;
  const plan = document.getElementById('editUserPlan').value;
  const status = document.getElementById('editUserStatus').value;
  const quota_add = parseInt(document.getElementById('editUserQuotaAdd').value || "0");

  fetch('/api/admin/update_user', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id, plan, status, quota_add })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      document.getElementById('editUserModal').classList.add('hidden');
      showToast(data.message, "success");
      loadAdminData();
    }
  })
  .catch(err => showToast("แก้ไขไม่สำเร็จ: " + err.message, "error"));
}

function simulateLogin(provider) {
  showToast("🔐 เข้าสู่ระบบด้วย " + provider + " สำเร็จ! สิทธิทดลองใช้ 7 วันพร้อมใช้งาน", "success");
  switchView('novels');
}
'''

# Append JS inside the existing <script> block before </script>
if "console.log(\"ReadAWrite Studio SaaS Engine Ready!\");" in html:
    html = html.replace("console.log(\"ReadAWrite Studio SaaS Engine Ready!\");", spa_js + "\n  console.log(\"ReadAWrite Studio SaaS Engine Ready!\");")
    print("Successfully added SPA JS router and API methods!")
else:
    print("WARNING: JS hook not found!")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("ALL UPDATES SUCCESSFULLY APPLIED TO", INDEX_PATH)
