# -*- coding: utf-8 -*-
"""
Full Production-Grade SaaS UI Builder for ReadAWrite Pro Studio
Generates c:\\ReadAWrite\\web_saas_stitch\\index.html with:
1. Real Authentication Gatekeeper (Default view is Landing Page for guests)
2. Interactive Login & Registration (with 7-Day Trial automatic issuance)
3. Dynamic Navbar (Guest vs Authenticated Author vs Super Admin)
4. Multi-Tenant Novels Library (SQLite backed)
5. 3-Panel AI Writing Studio (Real Gemini generation, real quota deduction)
6. Real Checkout & Payment Simulation (PromptPay QR, Instant Plan Upgrade)
7. Super Admin Portal (Role-protected, Live KPIs, User Quota & Plan management)
"""

import os

HTML_CONTENT = r'''<!DOCTYPE html>
<html class="light" lang="th">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>ReadAWrite Pro Studio - ระบบแต่งนิยายพลัง AI อัตโนมัติสำหรับนักเขียน</title>
  
  <!-- Google Fonts: Plus Jakarta Sans, Sarabun (Authentic Thai Prose), JetBrains Mono -->
  <link href="https://fonts.googleapis.com" rel="preconnect"/>
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;family=Sarabun:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet"/>
  <!-- Material Symbols Outlined -->
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: "#df6238",
            "primary-dark": "#b84824",
            "primary-light": "#fef2ee",
            secondary: "#006a61",
            "secondary-light": "#e0f2f1",
            surface: "#fbfaf8",
            "surface-card": "#ffffff",
            "border-ui": "#e8e4df",
            "text-main": "#1c1917",
            "text-muted": "#78716c"
          },
          fontFamily: {
            sans: ["Plus Jakarta Sans", "Sarabun", "sans-serif"],
            thai: ["Sarabun", "sans-serif"],
            mono: ["JetBrains Mono", "monospace"]
          }
        }
      }
    }
  </script>
  <style>
    .material-symbols-outlined {
      font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
      line-height: 1;
      display: inline-block;
      vertical-align: middle;
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 5px;
      height: 5px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #f5f5f4;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #d6d3d1;
      border-radius: 4px;
    }
  </style>
</head>
<body class="bg-[#fbfaf8] text-text-main font-sans antialiased selection:bg-primary-light selection:text-primary">

  <!-- ======================================================== -->
  <!-- TOP BANNER (DYNAMIC: GUEST PROMO OR USER TRIAL COUNTDOWN) -->
  <!-- ======================================================== -->
  <aside id="topBanner" class="bg-gradient-to-r from-primary/10 via-amber-50 to-teal-50 border-b border-border-ui px-4 py-2 text-xs">
    <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-2">
      <!-- Left Notice -->
      <div id="bannerText" class="flex items-center gap-2">
        <span class="flex h-2 w-2 relative">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
          <span class="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
        </span>
        <span class="font-bold text-primary">🎉 ยินดีต้อนรับสู่ ReadAWrite Pro Studio</span>
        <span class="hidden sm:inline text-text-muted">— สมัครสมาชิกวันนี้ ทดลองใช้ฟรี 7 วันเต็ม โควตา 50,000 คำ แต่งนิยายด้วย AI อัตโนมัติ</span>
      </div>
      <!-- Right Action -->
      <div id="bannerAction" class="flex items-center gap-3">
        <button onclick="openAuthModal('register')" class="bg-primary hover:bg-primary-dark text-white font-bold px-3 py-1 rounded-full text-[11px] shadow-xs transition-all flex items-center gap-1">
          <span class="material-symbols-outlined text-[14px]">bolt</span>
          <span>เริ่มทดลองใช้ฟรี 7 วัน</span>
        </button>
      </div>
    </div>
  </aside>

  <!-- ======================================================== -->
  <!-- TOP MAIN NAVIGATION BAR                                 -->
  <!-- ======================================================== -->
  <header class="bg-white border-b border-border-ui sticky top-0 z-40 shadow-xs">
    <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
      
      <!-- Brand Logo -->
      <div class="flex items-center gap-3 cursor-pointer" onclick="navigate('home')">
        <div class="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-white shadow-sm">
          <span class="material-symbols-outlined text-[24px]">stylus_note</span>
        </div>
        <div class="flex flex-col">
          <div class="flex items-center gap-1.5">
            <span class="text-xl font-extrabold text-primary tracking-tight">ReadAWrite</span>
            <span class="bg-primary text-white text-[9px] font-black px-1.5 py-0.5 rounded tracking-wider uppercase">PRO STUDIO</span>
          </div>
          <span class="text-[10px] text-text-muted font-medium">SaaS Cloud for Authors</span>
        </div>
      </div>

      <!-- Center Navigation Links -->
      <nav id="mainNav" class="hidden md:flex items-center gap-1">
        <button id="nav-home" onclick="navigate('home')" class="nav-btn px-3 py-1.5 rounded-lg text-sm font-bold text-primary bg-primary-light flex items-center gap-1.5 transition-all">
          <span class="material-symbols-outlined text-[18px]">home</span>
          <span>หน้าแรก</span>
        </button>
        <button id="nav-novels" onclick="navigate('novels')" class="nav-btn px-3 py-1.5 rounded-lg text-sm font-semibold text-text-muted hover:text-text-main hover:bg-stone-100 flex items-center gap-1.5 transition-all">
          <span class="material-symbols-outlined text-[18px]">auto_stories</span>
          <span>จัดการนิยาย</span>
        </button>
        <button id="nav-studio" onclick="navigate('studio')" class="nav-btn px-3 py-1.5 rounded-lg text-sm font-semibold text-text-muted hover:text-text-main hover:bg-stone-100 flex items-center gap-1.5 transition-all">
          <span class="material-symbols-outlined text-[18px]">edit_square</span>
          <span>ห้องแต่งนิยาย (AI Studio)</span>
        </button>
        <button id="nav-pricing" onclick="openCheckoutModal('monthly')" class="nav-btn px-3 py-1.5 rounded-lg text-sm font-semibold text-text-muted hover:text-text-main hover:bg-stone-100 flex items-center gap-1.5 transition-all">
          <span class="material-symbols-outlined text-[18px]">diamond</span>
          <span>ราคา &amp; แพ็กเกจ</span>
        </button>
        <!-- Admin Link (Hidden for regular users, shown only for Admin) -->
        <button id="nav-admin" onclick="navigate('admin')" class="hidden nav-btn px-3 py-1.5 rounded-lg text-sm font-bold text-amber-700 bg-amber-50 hover:bg-amber-100 flex items-center gap-1.5 transition-all border border-amber-200">
          <span class="material-symbols-outlined text-[18px]">shield_person</span>
          <span>จัดการระบบ (Admin HQ)</span>
        </button>
      </nav>

      <!-- Right Actions: Dynamic (Guest vs Authenticated) -->
      <div id="navAuthArea" class="flex items-center gap-3">
        <!-- Rendered by JS -->
      </div>

    </div>
  </header>

  <!-- ======================================================== -->
  <!-- 1. VIEW: LANDING & MARKETING PAGE (DEFAULT FOR GUESTS)    -->
  <!-- ======================================================== -->
  <main id="view-home" class="page-view overflow-y-auto">
    <!-- Hero Section -->
    <section class="max-w-6xl mx-auto px-4 pt-14 pb-20 text-center">
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary-light border border-primary/20 text-primary text-xs font-bold mb-6 shadow-xs animate-bounce">
        <span class="material-symbols-outlined text-[16px]">verified</span>
        <span>ระบบแต่งนิยายพลัง AI อัตโนมัติอันดับ 1 สำหรับนักเขียน ReadAWrite</span>
      </div>
      <h1 class="text-4xl sm:text-5xl md:text-6xl font-black text-text-main leading-tight tracking-tight mb-6">
        แต่งนิยายเร็วกว่าเดิม 10 เท่า <br/>
        <span class="bg-gradient-to-r from-primary via-orange-600 to-amber-600 bg-clip-text text-transparent">
          สำนวนภาษาไทยสละสลวย ซิงค์ลง ReadAWrite ในคลิกเดียว
        </span>
      </h1>
      <p class="text-base sm:text-lg text-text-muted max-w-2xl mx-auto mb-10 leading-relaxed font-thai">
        หมดปัญหาหมดไฟ ตันพล็อต หรือส่งงานไม่ทัน ด้วย AI อัจฉริยะที่เข้าใจจริตนิยายไทยทุกแนว (ผัวโบ้, ย้อนเวลา, มาเฟีย, แฟนตาซี) ผลิตเนื้อหา 3,500 คำใน 19 วินาที พร้อมส่งขึ้นเว็บแบบไม่ต้องก๊อปแปะ
      </p>

      <!-- CTA Buttons -->
      <div class="flex flex-wrap justify-center gap-4">
        <button onclick="handleStartWritingClick()" class="px-8 py-3.5 bg-primary hover:bg-primary-dark text-white text-base font-bold rounded-xl shadow-lg hover:shadow-xl transition-all transform active:scale-95 flex items-center gap-2">
          <span class="material-symbols-outlined text-[22px]">rocket_launch</span>
          <span>เริ่มทดลองใช้ฟรี 7 วัน (โควตา 50,000 คำ)</span>
        </button>
        <button onclick="openCheckoutModal('monthly')" class="px-6 py-3.5 bg-white hover:bg-stone-50 text-text-main text-base font-bold rounded-xl border border-border-ui shadow-xs transition-all flex items-center gap-2">
          <span class="material-symbols-outlined text-[20px]">view_timeline</span>
          <span>ดูแพ็กเกจ &amp; ค่าบริการ</span>
        </button>
      </div>

      <!-- Feature Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mt-16 text-left">
        <div class="bg-white p-6 rounded-2xl border border-border-ui shadow-xs hover:border-primary/40 transition-all">
          <div class="w-12 h-12 rounded-xl bg-orange-50 text-primary flex items-center justify-center mb-4">
            <span class="material-symbols-outlined text-[28px]">speed</span>
          </div>
          <h3 class="text-base font-bold text-text-main mb-1.5">แต่งไวใน 19 วินาที</h3>
          <p class="text-xs text-text-muted leading-relaxed font-thai">ประมวลผลด้วย Gemini 3.5 Flash Lite ความเร็วแสง ผลิต 2,500 - 4,500 คำต่อตอนโดยไม่ค้าง</p>
        </div>

        <div class="bg-white p-6 rounded-2xl border border-border-ui shadow-xs hover:border-secondary/40 transition-all">
          <div class="w-12 h-12 rounded-xl bg-teal-50 text-secondary flex items-center justify-center mb-4">
            <span class="material-symbols-outlined text-[28px]">cloud_sync</span>
          </div>
          <h3 class="text-base font-bold text-text-main mb-1.5">ซิงค์ ReadAWrite ออโต้</h3>
          <p class="text-xs text-text-muted leading-relaxed font-thai">สั่ง Playwright Headless ส่งบทความขึ้นเป็นแบบร่าง หรือตั้งเวลาเผยแพร่อัตโนมัติ ปลอดภัย 100%</p>
        </div>

        <div class="bg-white p-6 rounded-2xl border border-border-ui shadow-xs hover:border-amber-400 transition-all">
          <div class="w-12 h-12 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center mb-4">
            <span class="material-symbols-outlined text-[28px]">spellcheck</span>
          </div>
          <h3 class="text-base font-bold text-text-main mb-1.5">ProofAI ตรวจสำนวน</h3>
          <p class="text-xs text-text-muted leading-relaxed font-thai">ขัดเกลาคำผิด วรรคตอน สำนวนกระชับ ตัดคำไทยแท้ด้วยเอนจิน PyThaiNLP แม่นยำทุกตัวอักษร</p>
        </div>

        <div class="bg-white p-6 rounded-2xl border border-border-ui shadow-xs hover:border-purple-400 transition-all">
          <div class="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center mb-4">
            <span class="material-symbols-outlined text-[28px]">psychology</span>
          </div>
          <h3 class="text-base font-bold text-text-main mb-1.5">ความจำตัวละครต่อเนื่อง</h3>
          <p class="text-xs text-text-muted leading-relaxed font-thai">ระบบคลังความจำจดจำชื่อ คาแรคเตอร์ ปมความหลัง ป้องกัน AI ลืมตัวละครในตอนถัดไป</p>
        </div>
      </div>
    </section>

    <!-- Pricing Section on Landing Page -->
    <section class="bg-white py-16 border-t border-border-ui">
      <div class="max-w-6xl mx-auto px-4 text-center">
        <span class="text-xs font-bold text-primary tracking-wider uppercase">แพ็กเกจสมาชิกที่โปร่งใส คุ้มค่าที่สุด</span>
        <h2 class="text-3xl font-extrabold text-text-main mt-2 mb-3">เลือกระดับที่เหมาะกับเป้าหมายการเขียนของคุณ</h2>
        <p class="text-sm text-text-muted max-w-xl mx-auto mb-12 font-thai">ทดลองใช้ฟรี 7 วันโดยไม่ต้องผูกบัตรเครดิต เมื่อครบกำหนดสามารถเลือกอัปเกรดเพื่อรับโควตาคำเพิ่มเติมได้ทันที</p>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 text-left">
          
          <!-- Plan 1: Trial -->
          <div class="bg-stone-50 p-6 rounded-2xl border border-border-ui flex flex-col justify-between">
            <div>
              <span class="text-xs font-bold text-text-muted uppercase">เริ่มต้นทดลอง</span>
              <h3 class="text-lg font-bold text-text-main mt-1">7-Day Free Trial</h3>
              <div class="text-3xl font-black text-text-main mt-2">ฟรี <span class="text-xs font-normal text-text-muted">/ 7 วัน</span></div>
              <p class="text-xs text-text-muted mt-2 font-thai">เหมาะสำหรับทดลองเขียนนิยาย 1-2 เรื่อง</p>
              <ul class="mt-6 space-y-2.5 text-xs text-text-muted font-thai">
                <li class="flex items-center gap-2"><span class="material-symbols-outlined text-teal-600 text-[16px]">check_circle</span>โควตา AI 50,000 คำ</li>
                <li class="flex items-center gap-2"><span class="material-symbols-outlined text-teal-600 text-[16px]">check_circle</span>โมเดล Gemini 3.5 Flash Lite</li>
                <li class="flex items-center gap-2"><span class="material-symbols-outlined text-teal-600 text-[16px]">check_circle</span>ซิงค์ขึ้น ReadAWrite ได้ 1 เรื่อง</li>
              </ul>
            </div>
            <button onclick="handleStartWritingClick()" class="w-full mt-8 py-2.5 bg-white hover:bg-stone-200 border border-border-ui text-text-main font-bold text-xs rounded-xl transition-all">
              สมัครทดลองใช้ฟรี
            </button>
          </div>

          <!-- Plan 2: Monthly -->
          <div class="bg-white p-6 rounded-2xl border border-border-ui shadow-sm flex flex-col justify-between">
            <div>
              <span class="text-xs font-bold text-primary uppercase">ยอดนิยมรายเดือน</span>
              <h3 class="text-lg font-bold text-text-main mt-1">Pro Monthly</h3>
              <div class="text-3xl font-black text-primary mt-2">฿390 <span class="text-xs font-normal text-text-muted">/ เดือน</span></div>
              <p class="text-xs text-text-muted mt-2 font-thai">สำหรับนักเขียนที่ต้องการปล่อยนิยายสม่ำเสมอ</p>
              <ul class="mt-6 space-y-2.5 text-xs text-text-muted font-thai">
                <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">check_circle</span>โควตา AI 500,000 คำ/เดือน</li>
                <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">check_circle</span>ซิงค์ ReadAWrite ไม่จำกัดเรื่อง</li>
                <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">check_circle</span>ตรวจสำนวน ProofAI ไม่จำกัด</li>
              </ul>
            </div>
            <button onclick="openCheckoutModal('monthly')" class="w-full mt-8 py-2.5 bg-primary hover:bg-primary-dark text-white font-bold text-xs rounded-xl shadow-xs transition-all">
              เลือกแพ็กเกจรายเดือน
            </button>
          </div>

          <!-- Plan 3: Annual (Featured) -->
          <div class="bg-white p-6 rounded-2xl border-2 border-primary shadow-md relative flex flex-col justify-between">
            <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-white text-[10px] font-bold px-3 py-0.5 rounded-full shadow-xs">
              แนะนำคุ้มค่าที่สุด (ประหยัด 2 เดือน)
            </div>
            <div>
              <span class="text-xs font-bold text-primary uppercase">รายปี Pro Unlimited</span>
              <h3 class="text-lg font-bold text-text-main mt-1">Pro Annual</h3>
              <div class="text-3xl font-black text-primary mt-2">฿3,900 <span class="text-xs font-normal text-text-muted">/ ปี</span></div>
              <p class="text-xs text-text-muted mt-2 font-thai">เฉลี่ยเพียงเดือนละ ฿325 เท่านั้น</p>
              <ul class="mt-6 space-y-2.5 text-xs text-text-muted font-thai">
                <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">check_circle</span>โควตา AI 6,000,000 คำ/ปี</li>
                <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">check_circle</span>ตั้งเวลาปล่อยล่วงหน้า 30 วัน</li>
                <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">check_circle</span>ระบบ Batch แต่ง 3 ตอนรวด</li>
              </ul>
            </div>
            <button onclick="openCheckoutModal('annual')" class="w-full mt-8 py-2.5 bg-primary hover:bg-primary-dark text-white font-bold text-xs rounded-xl shadow-xs transition-all">
              เลือกแพ็กเกจรายปี
            </button>
          </div>

          <!-- Plan 4: Lifetime VIP -->
          <div class="bg-stone-900 text-white p-6 rounded-2xl border border-stone-800 shadow-md flex flex-col justify-between">
            <div>
              <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">จ่ายครั้งเดียวตลอดชีพ</span>
              <h3 class="text-lg font-bold text-white mt-1">Lifetime VIP</h3>
              <div class="text-3xl font-black text-amber-400 mt-2">฿6,900 <span class="text-xs font-normal text-stone-400">/ ครั้งเดียว</span></div>
              <p class="text-xs text-stone-400 mt-2 font-thai">ใช้งานตลอดชีพ ไม่ต้องจ่ายรายเดือนอีกต่อไป</p>
              <ul class="mt-6 space-y-2.5 text-xs text-stone-300 font-thai">
                <li class="flex items-center gap-2"><span class="material-symbols-outlined text-amber-400 text-[16px]">verified</span>ใช้งานฟีเจอร์ทุกอย่างตลอดชีพ</li>
                <li class="flex items-center gap-2"><span class="material-symbols-outlined text-amber-400 text-[16px]">verified</span>ซัปพอร์ตส่วนตัวแบบ VIP 24 ชม.</li>
                <li class="flex items-center gap-2"><span class="material-symbols-outlined text-amber-400 text-[16px]">verified</span>สิทธิ์เข้าถึงโมเดลใหม่ก่อนใคร</li>
              </ul>
            </div>
            <button onclick="openCheckoutModal('lifetime')" class="w-full mt-8 py-2.5 bg-amber-500 hover:bg-amber-600 text-stone-900 font-bold text-xs rounded-xl transition-all shadow-xs">
              สมัคร Lifetime VIP
            </button>
          </div>

        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-stone-100 border-t border-border-ui py-8 text-center text-xs text-text-muted">
      <div class="max-w-6xl mx-auto px-4 flex flex-wrap items-center justify-between gap-4">
        <div>&copy; 2026 ReadAWrite Pro Studio SaaS. พัฒนาขึ้นเพื่อยกระดับผลงานนักเขียนไทย</div>
        <div class="flex items-center gap-4">
          <span class="flex items-center gap-1 text-teal-700 font-semibold">
            <span class="material-symbols-outlined text-[16px]">lock</span> ระบบปลอดภัย SSL 256-bit
          </span>
          <span>•</span>
          <span>เชื่อมต่อ ReadAWrite.com</span>
        </div>
      </div>
    </footer>
  </main>

  <!-- ======================================================== -->
  <!-- 2. VIEW: MY NOVELS MANAGEMENT (AUTHENTICATED AUTHORS)    -->
  <!-- ======================================================== -->
  <main id="view-novels" class="page-view hidden overflow-y-auto p-6">
    <div class="max-w-6xl mx-auto">
      
      <!-- Top Action Bar -->
      <div class="flex flex-wrap items-center justify-between gap-4 mb-8">
        <div>
          <h1 class="text-2xl sm:text-3xl font-extrabold text-text-main">นิยายและผลงานของฉัน</h1>
          <p class="text-xs text-text-muted mt-1 font-thai">จัดการเรื่องย่อ ตัวละคร สารบัญตอน และส่งซิงค์ไปยัง ReadAWrite</p>
        </div>
        <button onclick="openCreateNovelModal()" class="px-5 py-2.5 bg-primary hover:bg-primary-dark text-white text-xs font-bold rounded-xl shadow-xs transition-all flex items-center gap-1.5">
          <span class="material-symbols-outlined text-[18px]">add_circle</span>
          <span>+ สร้างนิยายเรื่องใหม่</span>
        </button>
      </div>

      <!-- Novels Grid Container -->
      <div id="novelsGrid" class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Rendered by JS via /api/novels -->
      </div>

    </div>
  </main>

  <!-- ======================================================== -->
  <!-- 3. VIEW: AI NOVEL STUDIO (THE 3-PANEL WORKSPACE)          -->
  <!-- ======================================================== -->
  <main id="view-studio" class="page-view hidden h-[calc(100vh-6.5rem)] flex overflow-hidden">
    
    <!-- Left Sidebar: Chapter List (300px) -->
    <aside class="w-[300px] flex-shrink-0 bg-white border-r border-border-ui flex flex-col justify-between overflow-y-auto custom-scrollbar p-4">
      <div>
        <!-- Novel Meta Card -->
        <div class="bg-stone-50 rounded-xl p-3 border border-border-ui mb-4">
          <span class="text-[10px] font-bold text-teal-700 bg-teal-50 px-2 py-0.5 rounded-full uppercase" id="studioNovelGenre">ผัวโบ้ / กลับมาเจอกัน</span>
          <h3 class="text-sm font-bold text-text-main mt-1.5 line-clamp-2" id="studioNovelTitle">กำลังโหลดชื่อนิยาย...</h3>
        </div>

        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-bold text-text-muted uppercase">สารบัญตอน</span>
          <button onclick="addChapterPrompt()" class="text-[11px] font-bold text-primary hover:underline flex items-center gap-0.5">
            <span class="material-symbols-outlined text-[14px]">add</span> เพิ่มตอนใหม่
          </button>
        </div>

        <!-- Chapters List -->
        <div id="studioChaptersList" class="space-y-1.5">
          <!-- Rendered by JS -->
        </div>
      </div>

      <div class="pt-4 border-t border-border-ui text-center text-xs text-text-muted">
        <span class="flex items-center justify-center gap-1 text-teal-700 font-semibold">
          <span class="material-symbols-outlined text-[15px]">cloud_done</span> ซิงค์คลาวด์อัตโนมัติ
        </span>
      </div>
    </aside>

    <!-- Center: AI Controls (380px) -->
    <section class="w-[380px] flex-shrink-0 bg-white border-r border-border-ui flex flex-col justify-between overflow-y-auto custom-scrollbar p-5">
      <div class="space-y-5">
        
        <div>
          <h2 class="text-base font-extrabold text-text-main flex items-center gap-1.5">
            <span class="material-symbols-outlined text-primary text-[20px]">smart_toy</span>
            <span>แผงควบคุม AI ผู้ช่วยแต่งนิยาย</span>
          </h2>
          <p class="text-xs text-text-muted mt-0.5 font-thai">กำหนดทิศทางความยาวและสั่ง AI แต่งเนื้อหา</p>
        </div>

        <!-- Word Count Slider -->
        <div class="bg-stone-50 p-4 rounded-xl border border-border-ui">
          <div class="flex justify-between items-center mb-2">
            <label class="text-xs font-bold text-text-main">เป้าหมายจำนวนคำ</label>
            <span id="targetWordsDisplay" class="text-xs font-bold text-primary bg-primary-light px-2 py-0.5 rounded-full">2,500 คำ</span>
          </div>
          <input id="targetWordsSlider" type="range" min="1000" max="4500" step="500" value="2500" class="w-full accent-primary cursor-pointer"/>
          <div class="flex justify-between text-[10px] text-text-muted mt-1">
            <span>1,000 คำ (ตอนสั้น)</span>
            <span>2,500 คำ (มาตรฐาน)</span>
            <span>4,500 คำ (จุใจ)</span>
          </div>
        </div>

        <!-- AI Model Status -->
        <div class="bg-stone-50 p-3 rounded-xl border border-border-ui text-xs">
          <div class="flex items-center justify-between font-bold text-text-main">
            <span>โมเดล AI ที่ใช้</span>
            <span class="text-teal-700 flex items-center gap-1">
              <span class="w-2 h-2 rounded-full bg-teal-500 animate-ping"></span>
              Gemini 3.5 Flash Lite ⚡
            </span>
          </div>
          <p class="text-[11px] text-text-muted mt-1 font-thai">แต่งไวสุดใน 19 วินาที ปลดล็อกนิยายภาษาไทยสละสลวย</p>
        </div>

        <!-- Action Buttons -->
        <div class="space-y-2 pt-2">
          <!-- Main Generate Button -->
          <button id="btnGenerate" onclick="triggerGenerateChapter()" class="w-full py-3 bg-primary hover:bg-primary-dark text-white font-bold text-sm rounded-xl shadow-md transition-all transform active:scale-98 flex items-center justify-center gap-2">
            <span class="material-symbols-outlined text-[20px]">auto_awesome</span>
            <span>✨ แต่งบทนี้ทันทีด้วย AI</span>
          </button>

          <!-- Critic Polish Button -->
          <button id="btnCritic" onclick="triggerCriticPass()" class="w-full py-2.5 bg-stone-100 hover:bg-stone-200 text-text-main font-bold text-xs rounded-xl transition-all flex items-center justify-center gap-1.5">
            <span class="material-symbols-outlined text-[18px]">spellcheck</span>
            <span>🔍 เกลาสำนวน &amp; ตรวจคำผิด (ProofAI)</span>
          </button>

          <!-- Sync ReadAWrite Button -->
          <button id="btnSync" onclick="triggerReadAWriteSync()" class="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white font-bold text-xs rounded-xl shadow-xs transition-all flex items-center justify-center gap-1.5">
            <span class="material-symbols-outlined text-[18px]">send</span>
            <span>🚀 ซิงค์ส่งขึ้น ReadAWrite อัตโนมัติ</span>
          </button>

          <!-- Manual Save Button -->
          <button id="btnSave" onclick="saveCurrentChapter()" class="w-full py-2 border border-border-ui hover:bg-stone-50 text-text-muted hover:text-text-main font-semibold text-xs rounded-xl transition-all flex items-center justify-center gap-1">
            <span class="material-symbols-outlined text-[16px]">save</span>
            <span>💾 บันทึกเนื้อหาบทนี้ลงฐานข้อมูล</span>
          </button>
        </div>

      </div>

      <!-- Current Quota Indicator in Sidebar -->
      <div class="bg-orange-50 p-3 rounded-xl border border-primary/20 text-xs">
        <div class="flex justify-between items-center font-bold text-primary">
          <span>โควตาคำของคุณ</span>
          <span id="studioQuotaText">...</span>
        </div>
        <div class="w-full bg-orange-200 h-1.5 rounded-full mt-2 overflow-hidden">
          <div id="studioQuotaBar" class="bg-primary h-1.5 rounded-full" style="width: 20%;"></div>
        </div>
      </div>
    </section>

    <!-- Right: Manuscript Reader View (Flex-1) -->
    <section class="flex-1 bg-[#fcfbf7] overflow-y-auto custom-scrollbar p-8 lg:p-12">
      <div class="max-w-3xl mx-auto bg-white p-8 sm:p-12 rounded-2xl shadow-sm border border-border-ui min-h-full flex flex-col justify-between">
        <div>
          <!-- Chapter Heading -->
          <div class="border-b border-border-ui pb-6 mb-8 text-center">
            <span class="text-xs font-bold text-primary tracking-wider uppercase" id="editorStoryTitle">ชื่อเรื่อง</span>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-text-main mt-1" id="editorChapterTitle">บทที่ 1: ชื่อตอน</h1>
            <p class="text-xs text-text-muted mt-2" id="editorChapterStats">0 คำ • แบบร่าง</p>
          </div>

          <!-- Prose Content Area (Editable) -->
          <div id="manuscriptContent" contenteditable="true" class="font-thai text-base leading-relaxed text-stone-800 space-y-4 focus:outline-none min-h-[400px]">
            <!-- Injected by JS -->
          </div>
        </div>

        <div class="mt-8 pt-4 border-t border-border-ui flex items-center justify-between text-xs text-text-muted">
          <span id="realtimeWordsCounter">📊 0 คำ</span>
          <span>แบบร่างในเครื่อง พร้อมบันทึก</span>
        </div>
      </div>
    </section>

  </main>

  <!-- ======================================================== -->
  <!-- 4. VIEW: ADMIN MANAGEMENT PORTAL (HQ)                    -->
  <!-- ======================================================== -->
  <main id="view-admin" class="page-view hidden overflow-y-auto p-6">
    <div class="max-w-6xl mx-auto space-y-6">
      
      <!-- Admin Header -->
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="bg-amber-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">Super Admin</span>
            <h1 class="text-2xl font-black text-text-main">ศูนย์ควบคุมระบบสมาชิก &amp; แพลตฟอร์ม</h1>
          </div>
          <p class="text-xs text-text-muted mt-1 font-thai">จัดการสถานะสมาชิก เติมโควตาคำ AI ตรวจสอบรายได้ และดูความสมบูรณ์ของระบบ</p>
        </div>
        <button onclick="loadAdminData()" class="px-3 py-1.5 bg-white hover:bg-stone-50 border border-border-ui rounded-lg text-xs font-bold text-text-main flex items-center gap-1 shadow-xs">
          <span class="material-symbols-outlined text-[16px]">refresh</span>
          <span>รีเฟรชข้อมูล</span>
        </button>
      </div>

      <!-- KPI Summary Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white p-5 rounded-2xl border border-border-ui shadow-xs">
          <span class="text-xs font-semibold text-text-muted">สมาชิกที่ลงทะเบียน</span>
          <div class="text-2xl font-black text-text-main mt-1" id="adminStatUsers">-</div>
          <span class="text-[11px] text-teal-700 font-semibold">SQLite Database Backed</span>
        </div>
        <div class="bg-white p-5 rounded-2xl border border-border-ui shadow-xs">
          <span class="text-xs font-semibold text-text-muted">ยอดคำ AI ที่ผลิตไปแล้ว</span>
          <div class="text-2xl font-black text-primary mt-1" id="adminStatWords">-</div>
          <span class="text-[11px] text-text-muted">นับด้วย PyThaiNLP</span>
        </div>
        <div class="bg-white p-5 rounded-2xl border border-border-ui shadow-xs">
          <span class="text-xs font-semibold text-text-muted">รายได้จากแพ็กเกจ</span>
          <div class="text-2xl font-black text-teal-700 mt-1" id="adminStatRevenue">-</div>
          <span class="text-[11px] text-teal-600 font-semibold">ยอดจริงจากตาราง Orders</span>
        </div>
        <div class="bg-white p-5 rounded-2xl border border-border-ui shadow-xs">
          <span class="text-xs font-semibold text-text-muted">สถานะ Gemini Engine</span>
          <div class="text-sm font-bold text-teal-700 mt-1 flex items-center gap-1">
            <span class="w-2 h-2 rounded-full bg-teal-500 animate-ping"></span>
            Online (Flash Lite ⚡)
          </div>
          <span class="text-[11px] text-text-muted">Playwright Uploader: พร้อมซิงค์</span>
        </div>
      </div>

      <!-- User List Table -->
      <div class="bg-white rounded-2xl border border-border-ui shadow-xs overflow-hidden">
        <div class="p-4 border-b border-border-ui flex items-center justify-between">
          <h3 class="text-sm font-bold text-text-main">รายชื่อสมาชิกและการใช้งานโควตาคำ</h3>
          <span class="text-xs text-text-muted">คลิก "จัดการ" เพื่อปรับแพ็กเกจหรือเติมโควตา</span>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-stone-50 font-bold text-text-muted border-b border-border-ui">
              <tr>
                <th class="p-3">ID / นามปากกา</th>
                <th class="p-3">อีเมล</th>
                <th class="p-3">บทบาท</th>
                <th class="p-3">แพ็กเกจ</th>
                <th class="p-3">สถานะ</th>
                <th class="p-3">โควตาคำ (ใช้ไป / ทั้งหมด)</th>
                <th class="p-3 text-right">การจัดการ</th>
              </tr>
            </thead>
            <tbody id="adminUserTableBody" class="divide-y divide-border-ui font-thai">
              <!-- Rendered by JS -->
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </main>

  <!-- ======================================================== -->
  <!-- MODAL: AUTHENTICATION (LOGIN / REGISTER WITH TRIAL)       -->
  <!-- ======================================================== -->
  <div id="authModal" class="hidden fixed inset-0 z-50 overflow-y-auto bg-stone-900/50 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white max-w-md w-full rounded-3xl shadow-2xl border border-border-ui overflow-hidden">
      
      <!-- Modal Header -->
      <div class="p-5 border-b border-border-ui flex items-center justify-between bg-stone-50">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white">
            <span class="material-symbols-outlined text-[18px]">stylus_note</span>
          </div>
          <span class="font-extrabold text-sm text-text-main">ReadAWrite Pro Studio</span>
        </div>
        <button onclick="closeAuthModal()" class="p-1 rounded-lg text-text-muted hover:text-text-main">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>

      <!-- Auth Tabs -->
      <div class="flex border-b border-border-ui text-xs font-bold">
        <button id="tabBtnRegister" onclick="switchAuthTab('register')" class="flex-1 py-3 text-center border-b-2 border-primary text-primary bg-primary-light/50">
          สมัครสมาชิกใหม่ (รับสิทธิ์ทดลองฟรี 7 วัน)
        </button>
        <button id="tabBtnLogin" onclick="switchAuthTab('login')" class="flex-1 py-3 text-center text-text-muted hover:text-text-main">
          เข้าสู่ระบบ
        </button>
      </div>

      <!-- Tab 1: Register Form -->
      <form id="formRegister" onsubmit="handleRegisterSubmit(event)" class="p-6 space-y-4 text-xs font-thai">
        <div class="bg-amber-50 p-3 rounded-xl border border-amber-200 text-amber-800 text-[11px] leading-relaxed">
          ✨ <strong>สิทธิ์พิเศษสำหรับคุณ:</strong> สมัครแล้วรับโควตา AI 50,000 คำ และสิทธิ์ทดลองใช้ 7 วันทันทีโดยไม่ต้องผูกบัตรเครดิต!
        </div>
        <div>
          <label class="block font-bold text-text-main mb-1">นามปากกา / ชื่อผู้ใช้ *</label>
          <input id="regPenName" type="text" placeholder="เช่น รดา นิยายรัก" class="w-full px-3 py-2 bg-stone-50 border border-border-ui rounded-xl outline-none focus:border-primary text-xs" required />
        </div>
        <div>
          <label class="block font-bold text-text-main mb-1">อีเมล *</label>
          <input id="regEmail" type="email" placeholder="author@example.com" class="w-full px-3 py-2 bg-stone-50 border border-border-ui rounded-xl outline-none focus:border-primary text-xs" required />
        </div>
        <div>
          <label class="block font-bold text-text-main mb-1">รหัสผ่าน *</label>
          <input id="regPassword" type="password" placeholder="ตั้งรหัสผ่านอย่างน้อย 6 ตัวอักษร" class="w-full px-3 py-2 bg-stone-50 border border-border-ui rounded-xl outline-none focus:border-primary text-xs" required />
        </div>
        <button type="submit" class="w-full py-3 bg-primary hover:bg-primary-dark text-white font-bold rounded-xl shadow-xs transition-all text-xs">
          สมัครและเริ่มแต่งนิยายทันที
        </button>
      </form>

      <!-- Tab 2: Login Form -->
      <form id="formLogin" onsubmit="handleLoginSubmit(event)" class="hidden p-6 space-y-4 text-xs font-thai">
        <div>
          <label class="block font-bold text-text-main mb-1">อีเมลผู้ใช้งาน</label>
          <input id="loginEmail" type="email" placeholder="author@example.com" class="w-full px-3 py-2 bg-stone-50 border border-border-ui rounded-xl outline-none focus:border-primary text-xs" required />
        </div>
        <div>
          <label class="block font-bold text-text-main mb-1">รหัสผ่าน</label>
          <input id="loginPassword" type="password" placeholder="••••••••" class="w-full px-3 py-2 bg-stone-50 border border-border-ui rounded-xl outline-none focus:border-primary text-xs" required />
        </div>
        <button type="submit" class="w-full py-3 bg-stone-900 hover:bg-black text-white font-bold rounded-xl shadow-xs transition-all text-xs">
          เข้าสู่ระบบ
        </button>

        <!-- Quick Demo Login Buttons for convenience -->
        <div class="pt-4 border-t border-border-ui">
          <span class="block text-[10px] text-text-muted mb-2 uppercase font-bold text-center">ทางลัดทดสอบระบบ (Quick Demo)</span>
          <div class="grid grid-cols-2 gap-2">
            <button type="button" onclick="quickLogin('admin@readawrite.pro', 'admin1234')" class="py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 rounded-lg text-[11px] font-bold">
              👑 เข้าสู่ระบบเป็น Admin
            </button>
            <button type="button" onclick="quickLogin('writer@readawrite.pro', '123456')" class="py-1.5 bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-200 rounded-lg text-[11px] font-bold">
              ✍️ เข้าเป็นนักเขียน Demo
            </button>
          </div>
        </div>
      </form>

    </div>
  </div>

  <!-- ======================================================== -->
  <!-- MODAL: CREATE NEW NOVEL                                  -->
  <!-- ======================================================== -->
  <div id="createNovelModal" class="hidden fixed inset-0 z-50 overflow-y-auto bg-stone-900/50 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white max-w-lg w-full rounded-3xl shadow-2xl border border-border-ui overflow-hidden">
      <div class="p-5 border-b border-border-ui flex items-center justify-between bg-stone-50">
        <h3 class="font-bold text-sm text-text-main flex items-center gap-1.5">
          <span class="material-symbols-outlined text-primary text-[20px]">add_box</span>
          <span>สร้างนิยายเรื่องใหม่</span>
        </h3>
        <button onclick="document.getElementById('createNovelModal').classList.add('hidden')" class="p-1 rounded-lg text-text-muted hover:text-text-main">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>
      <form onsubmit="handleCreateNovelSubmit(event)" class="p-6 space-y-4 text-xs font-thai">
        <div>
          <label class="block font-bold text-text-main mb-1">ชื่อเรื่องนิยาย *</label>
          <input id="novelTitle" type="text" placeholder="เช่น เล่ห์รักท่านประธานร้าย" class="w-full px-3 py-2 bg-stone-50 border border-border-ui rounded-xl outline-none focus:border-primary text-xs" required />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block font-bold text-text-main mb-1">หมวดหมู่</label>
            <select id="novelCategory" class="w-full px-3 py-2 bg-stone-50 border border-border-ui rounded-xl outline-none focus:border-primary text-xs">
              <option value="โรมานซ์">โรมานซ์ / รักหวานแหวว</option>
              <option value="ดราม่า">ดราม่า / แก้แค้น</option>
              <option value="แฟนตาซี">แฟนตาซี / ย้อนยุค</option>
              <option value="วาย / Boy Love">นิยายวาย (Boy Love)</option>
            </select>
          </div>
          <div>
            <label class="block font-bold text-text-main mb-1">สไตล์พล็อต (Genre)</label>
            <input id="novelGenre" type="text" value="ผัวโบ้ / กลับมาเจอกัน" class="w-full px-3 py-2 bg-stone-50 border border-border-ui rounded-xl outline-none focus:border-primary text-xs" />
          </div>
        </div>
        <div>
          <label class="block font-bold text-text-main mb-1">เรื่องย่อ (Synopsis)</label>
          <textarea id="novelSynopsis" rows="3" placeholder="เขียนเรื่องย่อสำหรับให้ AI จดจำโครงสร้างเนื้อหา..." class="w-full px-3 py-2 bg-stone-50 border border-border-ui rounded-xl outline-none focus:border-primary text-xs"></textarea>
        </div>
        <div class="flex justify-end gap-2 pt-2 border-t border-border-ui">
          <button type="button" onclick="document.getElementById('createNovelModal').classList.add('hidden')" class="px-4 py-2 font-bold text-text-muted hover:text-text-main">ยกเลิก</button>
          <button type="submit" class="px-5 py-2 bg-primary hover:bg-primary-dark text-white font-bold rounded-xl shadow-xs">สร้างและเข้าห้องแต่งทันที</button>
        </div>
      </form>
    </div>
  </div>

  <!-- ======================================================== -->
  <!-- MODAL: CHECKOUT & PAYMENT UPGRADE                        -->
  <!-- ======================================================== -->
  <div id="checkoutModal" class="hidden fixed inset-0 z-50 overflow-y-auto bg-stone-900/50 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white max-w-lg w-full rounded-3xl shadow-2xl border border-border-ui overflow-hidden">
      <div class="p-5 border-b border-border-ui flex items-center justify-between bg-stone-50">
        <div>
          <span class="text-[10px] font-bold text-primary uppercase">อัปเกรดสถานะสมาชิก</span>
          <h3 class="text-base font-extrabold text-text-main" id="checkoutPlanTitle">Pro Monthly (รายเดือน)</h3>
        </div>
        <button onclick="document.getElementById('checkoutModal').classList.add('hidden')" class="p-1 rounded-lg text-text-muted hover:text-text-main">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>

      <div class="p-6 space-y-5 text-xs font-thai">
        <!-- Order Summary Box -->
        <div class="bg-primary-light/50 p-4 rounded-2xl border border-primary/20 flex items-center justify-between">
          <div>
            <span class="font-bold text-primary block" id="checkoutPlanDesc">โควตา 500,000 คำ / 30 วัน</span>
            <span class="text-text-muted text-[11px]">ปลดล็อกแต่งนิยาย AI ไม่จำกัด พร้อมซิงค์ ReadAWrite</span>
          </div>
          <div class="text-2xl font-black text-primary" id="checkoutAmount">฿390</div>
        </div>

        <!-- Payment Method Tabs -->
        <div>
          <label class="block font-bold text-text-main mb-2">เลือกวิธีชำระเงิน</label>
          <div class="grid grid-cols-2 gap-3">
            <button type="button" class="p-3 border-2 border-primary bg-primary-light/20 rounded-xl text-left flex items-center gap-2">
              <span class="material-symbols-outlined text-primary text-[22px]">qr_code_scanner</span>
              <div>
                <span class="font-bold block text-text-main text-xs">พร้อมเพย์ QR Code</span>
                <span class="text-[10px] text-text-muted">สแกนจ่ายได้ทุกธนาคาร</span>
              </div>
            </button>
            <button type="button" class="p-3 border border-border-ui rounded-xl text-left flex items-center gap-2 hover:bg-stone-50">
              <span class="material-symbols-outlined text-text-muted text-[22px]">credit_card</span>
              <div>
                <span class="font-bold block text-text-main text-xs">บัตรเครดิต/เดบิต</span>
                <span class="text-[10px] text-text-muted">Visa, Mastercard</span>
              </div>
            </button>
          </div>
        </div>

        <!-- Simulated PromptPay QR Visual -->
        <div class="bg-stone-50 p-4 rounded-2xl border border-border-ui text-center">
          <div class="w-40 h-40 bg-white p-2 mx-auto rounded-xl border border-border-ui shadow-xs flex items-center justify-center">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=PROMPTPAY-READAWRITE-SAAS" class="w-full h-full object-contain" alt="PromptPay QR Code"/>
          </div>
          <p class="text-[11px] text-text-muted mt-2">ยอดชำระ: <strong class="text-primary text-xs" id="qrAmountDisplay">฿390.00</strong> (จำลองระบบชำระเงินจริง)</p>
        </div>

        <button onclick="confirmSubscriptionUpgrade()" class="w-full py-3.5 bg-primary hover:bg-primary-dark text-white font-bold rounded-xl shadow-md transition-all text-xs flex items-center justify-center gap-2">
          <span class="material-symbols-outlined text-[18px]">verified</span>
          <span>ยืนยันการชำระเงิน (อัปเกรดทันที)</span>
        </button>
      </div>
    </div>
  </div>

  <!-- ======================================================== -->
  <!-- MODAL: ADMIN EDIT USER QUOTA & PLAN                      -->
  <!-- ======================================================== -->
  <div id="adminEditModal" class="hidden fixed inset-0 z-50 overflow-y-auto bg-stone-900/50 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white max-w-md w-full rounded-3xl shadow-2xl border border-border-ui overflow-hidden">
      <div class="p-5 border-b border-border-ui flex items-center justify-between bg-stone-50">
        <h3 class="font-bold text-sm text-text-main flex items-center gap-1.5">
          <span class="material-symbols-outlined text-primary text-[20px]">manage_accounts</span>
          <span>จัดการข้อมูลสมาชิก</span>
        </h3>
        <button onclick="document.getElementById('adminEditModal').classList.add('hidden')" class="p-1 rounded-lg text-text-muted hover:text-text-main">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>
      <form onsubmit="handleAdminUpdateSubmit(event)" class="p-6 space-y-4 text-xs font-thai">
        <input type="hidden" id="adminEditUserId"/>
        <div>
          <label class="block font-bold text-text-main mb-1">สมาชิก</label>
          <input id="adminEditUserName" type="text" class="w-full px-3 py-2 bg-stone-100 border border-border-ui rounded-xl text-text-muted text-xs cursor-not-allowed" readonly />
        </div>
        <div>
          <label class="block font-bold text-text-main mb-1">แพ็กเกจ (Plan)</label>
          <select id="adminEditPlan" class="w-full px-3 py-2 bg-stone-50 border border-border-ui rounded-xl outline-none focus:border-primary text-xs">
            <option value="trial">Pro Trial (ทดลอง 7 วัน)</option>
            <option value="monthly">Pro Monthly (รายเดือน)</option>
            <option value="annual">Pro Annual (รายปี)</option>
            <option value="lifetime">Lifetime VIP (ตลอดชีพ)</option>
          </select>
        </div>
        <div>
          <label class="block font-bold text-text-main mb-1">สถานะบัญชี</label>
          <select id="adminEditStatus" class="w-full px-3 py-2 bg-stone-50 border border-border-ui rounded-xl outline-none focus:border-primary text-xs">
            <option value="active">Active (ใช้งานปกติ)</option>
            <option value="expired">Expired (หมดอายุ)</option>
            <option value="suspended">Suspended (ระงับชั่วคราว)</option>
          </select>
        </div>
        <div>
          <label class="block font-bold text-text-main mb-1">เติมโควตาคำ AI เพิ่มเติม (+คำ)</label>
          <input id="adminEditQuotaAdd" type="number" step="10000" placeholder="เช่น 100000" class="w-full px-3 py-2 bg-stone-50 border border-border-ui rounded-xl outline-none focus:border-primary text-xs" />
        </div>
        <div class="flex justify-end gap-2 pt-2 border-t border-border-ui">
          <button type="button" onclick="document.getElementById('adminEditModal').classList.add('hidden')" class="px-4 py-2 font-bold text-text-muted hover:text-text-main">ยกเลิก</button>
          <button type="submit" class="px-5 py-2 bg-primary hover:bg-primary-dark text-white font-bold rounded-xl shadow-xs">บันทึกการเปลี่ยนแปลง</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Toast Notification Container -->
  <div id="toastContainer" class="fixed bottom-5 right-5 z-50 flex flex-col gap-2"></div>

  <!-- ======================================================== -->
  <!-- CLIENT JAVASCRIPT: AUTHENTICATION, ROUTING & LIVE APIS   -->
  <!-- ======================================================== -->
  <script>
    // --- Application State ---
    const state = {
      currentUser: null,
      token: localStorage.getItem('raw_auth_token') || '',
      currentView: 'home',
      novels: [],
      activeNovel: null,
      activeChapter: null,
      selectedPlanForUpgrade: 'monthly'
    };

    // --- Toast Notifications ---
    function showToast(msg, type = 'info') {
      const container = document.getElementById('toastContainer');
      const t = document.createElement('div');
      const bg = type === 'success' ? 'bg-teal-700 text-white' : type === 'error' ? 'bg-rose-600 text-white' : 'bg-stone-900 text-white';
      t.className = `${bg} px-4 py-3 rounded-2xl shadow-xl text-xs font-semibold flex items-center gap-2 transform transition-all duration-300`;
      t.innerHTML = `<span>${msg}</span>`;
      container.appendChild(t);
      setTimeout(() => {
        t.style.opacity = '0';
        setTimeout(() => t.remove(), 300);
      }, 4000);
    }

    // --- Authentication & Session Initialization ---
    async function initAuth() {
      if (!state.token) {
        renderGuestNav();
        navigate('home');
        return;
      }

      try {
        const res = await fetch('/api/auth/me', {
          headers: { 'Authorization': `Bearer ${state.token}` }
        });
        const data = await res.json();
        if (data.authenticated && data.user) {
          state.currentUser = data.user;
          renderUserNav(data.user);
          // If returning author, default to novels
          navigate('novels');
        } else {
          // Token expired or invalid
          localStorage.removeItem('raw_auth_token');
          state.token = '';
          state.currentUser = null;
          renderGuestNav();
          navigate('home');
        }
      } catch (err) {
        console.error('Auth verification failed', err);
        renderGuestNav();
        navigate('home');
      }
    }

    // --- Navigation Rendering (Guest vs User) ---
    function renderGuestNav() {
      const area = document.getElementById('navAuthArea');
      const adminBtn = document.getElementById('nav-admin');
      if (adminBtn) adminBtn.classList.add('hidden');

      area.innerHTML = `
        <button onclick="openAuthModal('login')" class="text-xs font-bold text-text-muted hover:text-text-main px-3 py-1.5 rounded-lg hover:bg-stone-100 transition-all">
          เข้าสู่ระบบ
        </button>
        <button onclick="openAuthModal('register')" class="px-4 py-2 bg-primary hover:bg-primary-dark text-white text-xs font-bold rounded-xl shadow-xs transition-all flex items-center gap-1">
          <span class="material-symbols-outlined text-[16px]">bolt</span>
          <span>ทดลองใช้ฟรี 7 วัน</span>
        </button>
      `;

      // Reset Top Banner
      document.getElementById('bannerText').innerHTML = `
        <span class="flex h-2 w-2 relative">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
          <span class="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
        </span>
        <span class="font-bold text-primary">🎉 สิทธิพิเศษ!</span>
        <span class="text-text-muted">สมัครวันนี้ทดลองใช้ฟรี 7 วันเต็ม โควตา 50,000 คำ แต่งนิยายด้วย AI อัตโนมัติ</span>
      `;
      document.getElementById('bannerAction').innerHTML = `
        <button onclick="openAuthModal('register')" class="bg-primary hover:bg-primary-dark text-white font-bold px-3 py-1 rounded-full text-[11px] shadow-xs transition-all flex items-center gap-1">
          <span class="material-symbols-outlined text-[14px]">bolt</span>
          <span>เริ่มทดลองใช้ฟรี 7 วัน</span>
        </button>
      `;
    }

    function renderUserNav(user) {
      const area = document.getElementById('navAuthArea');
      const adminBtn = document.getElementById('nav-admin');
      
      // Show/Hide Admin Button based on real role
      if (adminBtn) {
        if (user.role === 'admin') adminBtn.classList.remove('hidden');
        else adminBtn.classList.add('hidden');
      }

      const remainingQuota = user.quota_limit - user.quota_used;
      const trialDays = user.trial_days_left !== undefined ? user.trial_days_left : 7;

      area.innerHTML = `
        <!-- Quota Chip -->
        <div class="hidden sm:flex items-center gap-1.5 bg-orange-50 text-primary border border-primary/20 px-3 py-1 rounded-full text-xs font-bold">
          <span class="material-symbols-outlined text-[15px]">bolt</span>
          <span id="navQuotaDisplay">โควตา: ${remainingQuota.toLocaleString()} คำ</span>
        </div>

        <!-- Trial Countdown Chip -->
        <div class="hidden lg:flex items-center gap-1.5 bg-stone-100 text-stone-700 px-3 py-1 rounded-full text-xs font-semibold">
          <span class="material-symbols-outlined text-[15px]">timer</span>
          <span>${user.plan === 'lifetime' ? 'ตลอดชีพ' : `เหลือ ${trialDays} วัน`}</span>
        </div>

        <!-- Profile Avatar & Logout Dropdown -->
        <div class="flex items-center gap-2 pl-2 border-l border-border-ui">
          <div class="w-8 h-8 rounded-full bg-primary text-white font-bold flex items-center justify-center text-xs shadow-xs">
            ${user.pen_name ? user.pen_name.charAt(0) : 'U'}
          </div>
          <div class="hidden xl:flex flex-col text-left">
            <span class="text-xs font-bold text-text-main line-clamp-1">${user.pen_name}</span>
            <span class="text-[10px] text-text-muted capitalize">${user.plan} member</span>
          </div>
          <button onclick="handleLogout()" class="p-1.5 text-text-muted hover:text-rose-600 rounded-lg hover:bg-stone-100 transition-all" title="ออกจากระบบ">
            <span class="material-symbols-outlined text-[18px]">logout</span>
          </button>
        </div>
      `;

      // Update Top Banner for Authenticated User
      document.getElementById('bannerText').innerHTML = `
        <span class="font-bold text-teal-800">👤 บัญชี: ${user.pen_name}</span>
        <span class="text-text-muted">• สถานะ: ${user.plan === 'lifetime' ? 'Lifetime VIP ตลอดชีพ' : user.plan === 'annual' ? 'Pro Annual (รายปี)' : user.plan === 'monthly' ? 'Pro Monthly (รายเดือน)' : 'Pro Trial 7 วัน'} (${remainingQuota.toLocaleString()} คำคงเหลือ)</span>
      `;
      document.getElementById('bannerAction').innerHTML = `
        <button onclick="openCheckoutModal('monthly')" class="bg-primary hover:bg-primary-dark text-white font-bold px-3 py-1 rounded-full text-[11px] shadow-xs transition-all flex items-center gap-1">
          <span class="material-symbols-outlined text-[14px]">diamond</span>
          <span>อัปเกรดแพ็กเกจ</span>
        </button>
      `;
    }

    // --- Navigation & Route Protection ---
    function navigate(viewName) {
      // Route Guard: Require login for Novels, Studio, Admin
      if (['novels', 'studio', 'admin'].includes(viewName) && !state.currentUser) {
        showToast('🔒 กรุณาเข้าสู่ระบบก่อนเข้าใช้งานส่วนนี้', 'info');
        openAuthModal('login');
        return;
      }

      // Route Guard: Only Admin can access admin view
      if (viewName === 'admin' && state.currentUser?.role !== 'admin') {
        showToast('⛔ ขออภัย หน้านี้สำหรับ Super Admin เท่านั้น', 'error');
        return;
      }

      state.currentView = viewName;

      // Toggle views
      const views = ['home', 'novels', 'studio', 'admin'];
      views.forEach(v => {
        const el = document.getElementById(`view-${v}`);
        if (el) {
          if (v === viewName) el.classList.remove('hidden');
          else el.classList.add('hidden');
        }

        const navBtn = document.getElementById(`nav-${v}`);
        if (navBtn) {
          if (v === viewName) {
            navBtn.className = "nav-btn px-3 py-1.5 rounded-lg text-sm font-bold text-primary bg-primary-light flex items-center gap-1.5 transition-all";
          } else {
            navBtn.className = "nav-btn px-3 py-1.5 rounded-lg text-sm font-semibold text-text-muted hover:text-text-main hover:bg-stone-100 flex items-center gap-1.5 transition-all";
          }
        }
      });

      if (viewName === 'novels') loadNovels();
      if (viewName === 'admin') loadAdminData();

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function handleStartWritingClick() {
      if (state.currentUser) navigate('novels');
      else openAuthModal('register');
    }

    // --- Auth Modal & Logic ---
    function openAuthModal(tab = 'register') {
      document.getElementById('authModal').classList.remove('hidden');
      switchAuthTab(tab);
    }

    function closeAuthModal() {
      document.getElementById('authModal').classList.add('hidden');
    }

    function switchAuthTab(tab) {
      const regForm = document.getElementById('formRegister');
      const loginForm = document.getElementById('formLogin');
      const regTab = document.getElementById('tabBtnRegister');
      const loginTab = document.getElementById('tabBtnLogin');

      if (tab === 'register') {
        regForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
        regTab.className = "flex-1 py-3 text-center border-b-2 border-primary text-primary bg-primary-light/50 font-bold";
        loginTab.className = "flex-1 py-3 text-center text-text-muted hover:text-text-main font-semibold";
      } else {
        regForm.classList.add('hidden');
        loginForm.classList.remove('hidden');
        loginTab.className = "flex-1 py-3 text-center border-b-2 border-primary text-primary bg-primary-light/50 font-bold";
        regTab.className = "flex-1 py-3 text-center text-text-muted hover:text-text-main font-semibold";
      }
    }

    async function handleRegisterSubmit(e) {
      e.preventDefault();
      const pen_name = document.getElementById('regPenName').value.trim();
      const email = document.getElementById('regEmail').value.trim();
      const password = document.getElementById('regPassword').value.trim();

      try {
        const res = await fetch('/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ pen_name, email, password })
        });
        const data = await res.json();
        if (data.success) {
          localStorage.setItem('raw_auth_token', data.token);
          state.token = data.token;
          state.currentUser = data.user;
          renderUserNav(data.user);
          closeAuthModal();
          showToast(data.message, 'success');
          navigate('novels');
        } else {
          showToast(data.error || 'การสมัครสมาชิกไม่สำเร็จ', 'error');
        }
      } catch (err) {
        showToast('เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์', 'error');
      }
    }

    async function handleLoginSubmit(e) {
      e.preventDefault();
      const email = document.getElementById('loginEmail').value.trim();
      const password = document.getElementById('loginPassword').value.trim();
      doLogin(email, password);
    }

    async function quickLogin(email, password) {
      doLogin(email, password);
    }

    async function doLogin(email, password) {
      try {
        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (data.success) {
          localStorage.setItem('raw_auth_token', data.token);
          state.token = data.token;
          state.currentUser = data.user;
          renderUserNav(data.user);
          closeAuthModal();
          showToast(data.message, 'success');
          navigate('novels');
        } else {
          showToast(data.error || 'เข้าสู่ระบบไม่สำเร็จ', 'error');
        }
      } catch (err) {
        showToast('เกิดข้อผิดพลาดในการเชื่อมต่อ', 'error');
      }
    }

    async function handleLogout() {
      try {
        await fetch('/api/auth/logout', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${state.token}` }
        });
      } catch (e) {}

      localStorage.removeItem('raw_auth_token');
      state.token = '';
      state.currentUser = null;
      renderGuestNav();
      navigate('home');
      showToast('ออกจากระบบเรียบร้อยแล้ว', 'info');
    }

    // --- Novels Management (My Novels) ---
    async function loadNovels() {
      if (!state.token) return;
      try {
        const res = await fetch('/api/novels', {
          headers: { 'Authorization': `Bearer ${state.token}` }
        });
        const data = await res.json();
        if (data.success) {
          state.novels = data.novels;
          renderNovelsGrid(data.novels);
        }
      } catch (err) {
        showToast('โหลดรายการนิยายล้มเหลว', 'error');
      }
    }

    function renderNovelsGrid(novels) {
      const grid = document.getElementById('novelsGrid');
      if (!grid) return;

      if (!novels || novels.length === 0) {
        grid.className = "col-span-3 text-center py-16 bg-white rounded-3xl border border-dashed border-border-ui";
        grid.innerHTML = `
          <div class="w-16 h-16 rounded-2xl bg-orange-50 text-primary flex items-center justify-center mx-auto mb-4">
            <span class="material-symbols-outlined text-[36px]">auto_stories</span>
          </div>
          <h3 class="text-lg font-bold text-text-main">ยินดีต้อนรับสู่อาณาจักรนิยายของคุณ!</h3>
          <p class="text-xs text-text-muted max-w-md mx-auto mt-1 mb-6 font-thai">คุณยังไม่มีนิยายในระบบ เริ่มต้นสร้างผลงานชิ้นแรกของคุณเพื่อปลดล็อกพลัง AI แต่งนิยายได้ทันที</p>
          <button onclick="openCreateNovelModal()" class="px-6 py-3 bg-primary hover:bg-primary-dark text-white text-xs font-bold rounded-xl shadow-xs transition-all inline-flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[18px]">add_circle</span>
            <span>+ สร้างนิยายเรื่องแรกของคุณ</span>
          </button>
        `;
        return;
      }

      grid.className = "grid grid-cols-1 md:grid-cols-3 gap-6";
      grid.innerHTML = novels.map(n => `
        <div class="bg-white rounded-2xl border border-border-ui shadow-xs hover:shadow-md transition-all overflow-hidden flex flex-col justify-between">
          <div>
            <div class="h-44 w-full overflow-hidden relative bg-stone-100">
              <img src="${n.cover_url || 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&q=80'}" class="w-full h-full object-cover" />
              <span class="absolute top-3 right-3 px-2 py-0.5 rounded-full text-[10px] font-bold bg-teal-700 text-white">
                ${n.status}
              </span>
              <span class="absolute bottom-3 left-3 px-2 py-0.5 rounded text-[10px] font-bold bg-black/60 text-white">
                ${n.category}
              </span>
            </div>
            <div class="p-4">
              <h3 class="text-sm font-bold text-text-main line-clamp-1">${n.title}</h3>
              <p class="text-xs text-primary font-medium mt-0.5">${n.genre}</p>
              <p class="text-xs text-text-muted mt-2 line-clamp-2 font-thai leading-relaxed">${n.synopsis || 'ไม่มีเรื่องย่อ'}</p>
              <div class="flex items-center gap-3 mt-4 text-[11px] text-text-muted border-t border-border-ui pt-3">
                <span>📝 ${n.chapters_count || 1} ตอน</span>
                <span>📊 ${Number(n.words_total || 0).toLocaleString()} คำ</span>
              </div>
            </div>
          </div>
          <div class="p-4 pt-0">
            <button onclick="openNovelInStudio('${n.id}')" class="w-full py-2 bg-primary hover:bg-primary-dark text-white text-xs font-bold rounded-xl transition-all flex items-center justify-center gap-1 shadow-xs">
              <span class="material-symbols-outlined text-[16px]">edit</span>
              <span>เข้าห้องแต่งนิยาย</span>
            </button>
          </div>
        </div>
      `).join('');
    }

    function openCreateNovelModal() {
      document.getElementById('createNovelModal').classList.remove('hidden');
    }

    async function handleCreateNovelSubmit(e) {
      e.preventDefault();
      const title = document.getElementById('novelTitle').value.trim();
      const category = document.getElementById('novelCategory').value;
      const genre = document.getElementById('novelGenre').value.trim();
      const synopsis = document.getElementById('novelSynopsis').value.trim();

      try {
        const res = await fetch('/api/novels/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${state.token}`
          },
          body: JSON.stringify({ title, category, genre, synopsis })
        });
        const data = await res.json();
        if (data.success) {
          document.getElementById('createNovelModal').classList.add('hidden');
          showToast(data.message, 'success');
          await loadNovels();
          openNovelInStudio(data.novel.id);
        } else {
          showToast(data.error || 'สร้างไม่สำเร็จ', 'error');
        }
      } catch (err) {
        showToast('เกิดข้อผิดพลาดในการสร้างนิยาย', 'error');
      }
    }

    // --- 3-Panel Studio Logic ---
    async function openNovelInStudio(novelId) {
      try {
        const res = await fetch(`/api/novels/${novelId}`, {
          headers: { 'Authorization': `Bearer ${state.token}` }
        });
        const data = await res.json();
        if (data.success) {
          state.activeNovel = data.novel;
          document.getElementById('studioNovelTitle').innerText = data.novel.title;
          document.getElementById('studioNovelGenre').innerText = data.novel.genre;
          document.getElementById('editorStoryTitle').innerText = data.novel.title;

          renderStudioChapters(data.novel.chapters);
          if (data.novel.chapters && data.novel.chapters.length > 0) {
            selectChapter(data.novel.chapters[0].chapter_num);
          }
          navigate('studio');
        }
      } catch (err) {
        showToast('เปิดห้องแต่งนิยายล้มเหลว', 'error');
      }
    }

    function renderStudioChapters(chapters) {
      const container = document.getElementById('studioChaptersList');
      if (!container) return;
      container.innerHTML = chapters.map(c => `
        <button onclick="selectChapter(${c.chapter_num})" class="w-full text-left p-2.5 rounded-xl border ${state.activeChapter?.chapter_num === c.chapter_num ? 'bg-primary-light border-primary text-primary font-bold' : 'border-transparent hover:bg-stone-50 text-text-main'} transition-all flex items-center justify-between">
          <div class="truncate">
            <div class="text-xs truncate">บทที่ ${c.chapter_num}: ${c.subtitle}</div>
            <div class="text-[10px] text-text-muted font-normal">${Number(c.word_count).toLocaleString()} คำ • ${c.status}</div>
          </div>
          <span class="material-symbols-outlined text-[16px] text-text-muted">chevron_right</span>
        </button>
      `).join('');
    }

    function selectChapter(chNum) {
      if (!state.activeNovel) return;
      const ch = state.activeNovel.chapters.find(x => x.chapter_num === chNum) || {
        chapter_num: chNum,
        subtitle: `ตอนที่ ${chNum}`,
        content: '',
        word_count: 0,
        status: 'draft'
      };
      state.activeChapter = ch;

      document.getElementById('editorChapterTitle').innerText = `บทที่ ${ch.chapter_num}: ${ch.subtitle}`;
      document.getElementById('editorChapterStats').innerText = `${Number(ch.word_count).toLocaleString()} คำ • สถานะ: ${ch.status}`;

      const manuscript = document.getElementById('manuscriptContent');
      if (ch.content) {
        const paras = ch.content.split('\n\n').filter(p => p.trim().length > 0);
        manuscript.innerHTML = paras.map(p => `<p class="indent-8">${p.replace(/\n/g, '<br/>')}</p>`).join('');
      } else {
        manuscript.innerHTML = `<div class="p-8 text-center text-text-muted"><p>ยังไม่มีเนื้อหาในบทนี้</p><p class="text-xs mt-1">คลิกปุ่ม <strong>"✨ แต่งบทนี้ทันทีด้วย AI"</strong> ทางซ้ายเพื่อเริ่มแต่ง</p></div>`;
      }

      document.getElementById('realtimeWordsCounter').innerText = `📊 ${Number(ch.word_count).toLocaleString()} คำ`;
      renderStudioChapters(state.activeNovel.chapters);
    }

    async function triggerGenerateChapter() {
      if (!state.activeNovel || !state.activeChapter) {
        showToast('กรุณาเลือกนิยายและตอนก่อน', 'error');
        return;
      }

      const targetWords = parseInt(document.getElementById('targetWordsSlider').value);
      const manuscript = document.getElementById('manuscriptContent');

      showToast(`⏳ AI กำลังแต่งบทที่ ${state.activeChapter.chapter_num} ความยาว ~${targetWords.toLocaleString()} คำ...`, 'info');
      manuscript.innerHTML = `
        <div class="p-12 text-center text-primary animate-pulse">
          <span class="material-symbols-outlined text-[40px] mb-2">auto_awesome</span>
          <div class="font-bold text-base">กำลังแต่งเนื้อหาบทที่ ${state.activeChapter.chapter_num}...</div>
          <div class="text-xs text-text-muted mt-1">ใช้เวลาประมวลผลประมาณ 15-20 วินาที ด้วย Gemini 3.5 Flash Lite</div>
        </div>
      `;

      try {
        const res = await fetch('/api/generate_chapter', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${state.token}`
          },
          body: JSON.stringify({
            novel_id: state.activeNovel.id,
            title: state.activeNovel.title,
            genre: state.activeNovel.genre,
            chapter_num: state.activeChapter.chapter_num,
            subtitle: state.activeChapter.subtitle,
            target_words: targetWords
          })
        });
        const data = await res.json();
        if (data.success) {
          state.activeChapter.content = data.text;
          state.activeChapter.word_count = data.word_count;
          
          // Render Prose
          const paras = data.text.split('\n\n').filter(p => p.trim().length > 0);
          manuscript.innerHTML = paras.map(p => `<p class="indent-8">${p.replace(/\n/g, '<br/>')}</p>`).join('');
          
          document.getElementById('editorChapterStats').innerText = `${data.word_count.toLocaleString()} คำ • สถานะ: draft`;
          document.getElementById('realtimeWordsCounter').innerText = `📊 ${data.word_count.toLocaleString()} คำ`;

          // Update user quota state
          if (state.currentUser) {
            state.currentUser.quota_used = data.quota_used;
            renderUserNav(state.currentUser);
          }

          showToast(data.message, 'success');
        } else {
          showToast(data.error || 'แต่งนิยายไม่สำเร็จ', 'error');
          manuscript.innerHTML = `<div class="p-8 text-center text-rose-600 font-bold">${data.error}</div>`;
        }
      } catch (err) {
        showToast('การเชื่อมต่อกับเซิร์ฟเวอร์ล้มเหลว', 'error');
      }
    }

    async function triggerCriticPass() {
      if (!state.activeChapter?.content) {
        showToast('ยังไม่มีเนื้อหาให้ตรวจทาน', 'error');
        return;
      }

      showToast('🔍 ProofAI กำลังตรวจทานและเกลาสำนวน...', 'info');
      try {
        const res = await fetch('/api/critic_pass', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${state.token}`
          },
          body: JSON.stringify({ text: state.activeChapter.content })
        });
        const data = await res.json();
        if (data.success) {
          state.activeChapter.content = data.text;
          const paras = data.text.split('\n\n').filter(p => p.trim().length > 0);
          document.getElementById('manuscriptContent').innerHTML = paras.map(p => `<p class="indent-8">${p.replace(/\n/g, '<br/>')}</p>`).join('');
          showToast('✨ ProofAI เกลาสำนวนเรียบร้อยแล้ว!', 'success');
        }
      } catch (e) {
        showToast('เกลาสำนวนไม่สำเร็จ', 'error');
      }
    }

    async function triggerReadAWriteSync() {
      if (!state.activeChapter?.content) {
        showToast('ยังไม่มีเนื้อหาที่จะส่ง', 'error');
        return;
      }
      showToast('🚀 กำลังซิงค์ขึ้น ReadAWrite อัตโนมัติ (แบบร่าง)...', 'info');
      try {
        const res = await fetch('/api/upload_readawrite', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${state.token}`
          },
          body: JSON.stringify({
            article_id: state.activeNovel?.article_id || '658c4eaeed43f428680aec8d7c5ec863',
            chapter_num: state.activeChapter.chapter_num,
            subtitle: state.activeChapter.subtitle,
            content: state.activeChapter.content,
            publish_mode: 'draft'
          })
        });
        const data = await res.json();
        if (data.success) showToast(data.message, 'success');
        else showToast('อัปโหลดไม่สำเร็จ', 'error');
      } catch (e) {
        showToast('เชื่อมต่อระบบซิงค์ล้มเหลว', 'error');
      }
    }

    async function saveCurrentChapter() {
      if (!state.activeNovel || !state.activeChapter) return;
      const content = document.getElementById('manuscriptContent').innerText;
      try {
        const res = await fetch('/api/chapters/save', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${state.token}`
          },
          body: JSON.stringify({
            novel_id: state.activeNovel.id,
            chapter_num: state.activeChapter.chapter_num,
            subtitle: state.activeChapter.subtitle,
            content: content
          })
        });
        const data = await res.json();
        if (data.success) showToast(data.message, 'success');
      } catch (e) {
        showToast('บันทึกล้มเหลว', 'error');
      }
    }

    function addChapterPrompt() {
      if (!state.activeNovel) return;
      const nextNum = state.activeNovel.chapters.length + 1;
      const title = prompt(`ตั้งชื่อตอนสำหรับบทที่ ${nextNum}:`, `ตอนที่ ${nextNum}`);
      if (!title) return;
      state.activeNovel.chapters.push({
        chapter_num: nextNum,
        subtitle: title,
        content: '',
        word_count: 0,
        status: 'draft'
      });
      selectChapter(nextNum);
      showToast(`เพิ่มบทที่ ${nextNum} เรียบร้อยแล้ว`, 'success');
    }

    // --- Subscription & Upgrade Checkout ---
    function openCheckoutModal(plan) {
      if (!state.currentUser) {
        showToast('กรุณาเข้าสู่ระบบก่อนเลือกแพ็กเกจ', 'info');
        openAuthModal('login');
        return;
      }

      state.selectedPlanForUpgrade = plan;
      const plans = {
        monthly: { title: 'Pro Monthly (รายเดือน)', desc: 'โควตา 500,000 คำ / 30 วัน', amount: '฿390' },
        annual: { title: 'Pro Annual (รายปี)', desc: 'โควตา 6,000,000 คำ / 365 วัน', amount: '฿3,900' },
        lifetime: { title: 'Lifetime VIP (ตลอดชีพ)', desc: 'โควตาไม่จำกัด / ใช้งานตลอดชีพ', amount: '฿6,900' }
      };

      const p = plans[plan] || plans.monthly;
      document.getElementById('checkoutPlanTitle').innerText = p.title;
      document.getElementById('checkoutPlanDesc').innerText = p.desc;
      document.getElementById('checkoutAmount').innerText = p.amount;
      document.getElementById('qrAmountDisplay').innerText = `${p.amount}.00`;
      document.getElementById('checkoutModal').classList.remove('hidden');
    }

    async function confirmSubscriptionUpgrade() {
      try {
        const res = await fetch('/api/subscription/upgrade', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${state.token}`
          },
          body: JSON.stringify({
            plan: state.selectedPlanForUpgrade,
            payment_method: 'PromptPay QR'
          })
        });
        const data = await res.json();
        if (data.success) {
          state.currentUser = data.user;
          renderUserNav(data.user);
          document.getElementById('checkoutModal').classList.add('hidden');
          showToast(data.message, 'success');
        } else {
          showToast(data.error || 'ชำระเงินไม่สำเร็จ', 'error');
        }
      } catch (e) {
        showToast('การเชื่อมต่อล้มเหลว', 'error');
      }
    }

    // --- Super Admin HQ Functions ---
    let adminUsersList = [];

    async function loadAdminData() {
      try {
        const statRes = await fetch('/api/admin/stats', {
          headers: { 'Authorization': `Bearer ${state.token}` }
        });
        const statData = await statRes.json();
        if (statData.success) {
          document.getElementById('adminStatUsers').innerText = `${statData.stats.total_users} คน`;
          document.getElementById('adminStatWords').innerText = `${Number(statData.stats.total_words_generated).toLocaleString()} คำ`;
          document.getElementById('adminStatRevenue').innerText = `฿${Number(statData.stats.total_revenue).toLocaleString()}`;
        }

        const userRes = await fetch('/api/admin/users', {
          headers: { 'Authorization': `Bearer ${state.token}` }
        });
        const userData = await userRes.json();
        if (userData.success) {
          adminUsersList = userData.users;
          renderAdminUsers(userData.users);
        }
      } catch (err) {
        showToast('โหลดข้อมูลแอดมินล้มเหลว', 'error');
      }
    }

    function renderAdminUsers(users) {
      const tbody = document.getElementById('adminUserTableBody');
      if (!tbody) return;
      tbody.innerHTML = users.map(u => `
        <tr class="hover:bg-stone-50">
          <td class="p-3">
            <span class="font-bold text-text-main">${u.pen_name}</span>
            <div class="text-[10px] text-text-muted font-mono">ID #${u.id} • ${u.created_at.split('T')[0]}</div>
          </td>
          <td class="p-3 text-text-muted">${u.email}</td>
          <td class="p-3">
            <span class="px-2 py-0.5 rounded font-bold uppercase text-[10px] ${u.role === 'admin' ? 'bg-amber-100 text-amber-800' : 'bg-stone-100 text-stone-700'}">${u.role}</span>
          </td>
          <td class="p-3">
            <span class="px-2 py-0.5 rounded font-semibold text-[11px] ${u.plan === 'lifetime' ? 'bg-amber-100 text-amber-800 font-bold' : u.plan === 'annual' ? 'bg-primary-light text-primary font-bold' : 'bg-stone-100 text-stone-700'}">${u.plan}</span>
          </td>
          <td class="p-3">
            <span class="font-bold text-[11px] ${u.status === 'active' ? 'text-teal-700' : 'text-rose-600'}">${u.status}</span>
          </td>
          <td class="p-3">
            <span class="font-bold text-[11px]">${Number(u.quota_used).toLocaleString()} / ${Number(u.quota_limit).toLocaleString()} คำ</span>
            <div class="w-24 bg-stone-200 h-1 rounded-full mt-1 overflow-hidden">
              <div class="bg-primary h-1 rounded-full" style="width: ${Math.min(100, Math.round((u.quota_used/u.quota_limit)*100))}%"></div>
            </div>
          </td>
          <td class="p-3 text-right">
            <button onclick="openAdminEditModal(${u.id})" class="px-2.5 py-1 bg-stone-100 hover:bg-stone-200 border border-border-ui rounded-lg text-primary font-bold">
              จัดการ
            </button>
          </td>
        </tr>
      `).join('');
    }

    function openAdminEditModal(userId) {
      const u = adminUsersList.find(x => x.id === userId);
      if (!u) return;
      document.getElementById('adminEditUserId').value = u.id;
      document.getElementById('adminEditUserName').value = `${u.pen_name} (${u.email})`;
      document.getElementById('adminEditPlan').value = u.plan;
      document.getElementById('adminEditStatus').value = u.status;
      document.getElementById('adminEditQuotaAdd').value = '';
      document.getElementById('adminEditModal').classList.remove('hidden');
    }

    async function handleAdminUpdateSubmit(e) {
      e.preventDefault();
      const user_id = document.getElementById('adminEditUserId').value;
      const plan = document.getElementById('adminEditPlan').value;
      const status = document.getElementById('adminEditStatus').value;
      const quota_add = parseInt(document.getElementById('adminEditQuotaAdd').value || '0');

      try {
        const res = await fetch('/api/admin/update_user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${state.token}`
          },
          body: JSON.stringify({ user_id, plan, status, quota_add })
        });
        const data = await res.json();
        if (data.success) {
          document.getElementById('adminEditModal').classList.add('hidden');
          showToast(data.message, 'success');
          loadAdminData();
        } else {
          showToast(data.error || 'อัปเดตไม่สำเร็จ', 'error');
        }
      } catch (err) {
        showToast('การเชื่อมต่อล้มเหลว', 'error');
      }
    }

    // --- Onload Initialization ---
    window.addEventListener('DOMContentLoaded', () => {
      // Setup Slider Listener
      const slider = document.getElementById('targetWordsSlider');
      if (slider) {
        slider.addEventListener('input', (e) => {
          document.getElementById('targetWordsDisplay').innerText = `${Number(e.target.value).toLocaleString()} คำ`;
        });
      }

      // Initialize Authentication and Route to Home or Dashboard
      initAuth();
    });
  </script>
</body>
</html>
'''

INDEX_PATH = r"c:\ReadAWrite\web_saas_stitch\index.html"

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Successfully generated clean production-grade SaaS UI at: {INDEX_PATH}")
