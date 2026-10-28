# -*- coding: utf-8 -*-
"""
Apple.com Cupertino Luxury Theme Integration for ReadAWrite Pro Studio SaaS
Generated via Google Stitch Screen ID: d708be20dd334573a17d52c2f777608e
Features:
- Translucent Frosted Glass Header (backdrop-blur-xl bg-white/80)
- Strict Guest vs Authenticated Nav rules:
  * Guest: ONLY sees หน้าแรก, ฟีเจอร์เด่น, ราคา & สมาชิก, คำถามที่พบบ่อย + [เข้าสู่ระบบ], [ทดลองใช้ฟรี 7 วัน]
  * Authenticated Author: sees หน้าแรก, นิยายของฉัน, ห้องแต่งนิยาย, ราคา & สมาชิก + Quota Badge, Trial Pill, Pen Name & Logout
  * Super Admin: sees additional [Admin HQ] titanium badge
- Monumental Apple Keynote Hero
- Cinema Display macOS Studio Preview
- Apple Bento Grid (4 High-Tech Tiles with 28px rounded corners)
- Apple One Style Pricing Comparison Matrix (Trial, Monthly, Annual, Lifetime)
- Real SQLite multi-tenant backend + live Gemini 3.5 Flash Lite + Real Quota deduction
"""

import os

HTML_CONTENT = r'''<!DOCTYPE html>
<html class="scroll-smooth light" lang="th">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>ReadAWrite Pro Studio — Luxury Apple Aesthetic AI Novel Platform</title>
  
  <!-- Apple Cupertino Fonts & Thai Sarabun -->
  <link href="https://fonts.googleapis.com" rel="preconnect"/>
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&amp;family=Sarabun:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet"/>
  <!-- Material Symbols Outlined -->
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
  <script>
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            "apple-subtle": "#f5f5f7",
            "apple-coral": "#e85a2d",
            "apple-coral-hover": "#d64f24",
            "apple-coral-light": "#fef2ee",
            "apple-blue": "#0071e3",
            "apple-space": "#1d1d1f",
            "apple-titanium": "#86868b",
            "apple-border": "rgba(0, 0, 0, 0.08)"
          },
          fontFamily: {
            sans: ["Plus Jakarta Sans", "Sarabun", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
            thai: ["Sarabun", "sans-serif"],
            mono: ["JetBrains Mono", "monospace"]
          }
        }
      }
    };
  </script>
  <style>
    .material-symbols-outlined {
      font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
      display: inline-block;
      vertical-align: middle;
      line-height: 1;
    }
    .cinema-screen-shadow {
      box-shadow: 0 30px 100px -20px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(0, 0, 0, 0.05);
    }
    .bento-card-hover {
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .bento-card-hover:hover {
      transform: translateY(-3px);
      box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.08);
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 5px;
      height: 5px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #f5f5f7;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #d6d3d1;
      border-radius: 4px;
    }
  </style>
</head>
<body class="bg-[#f5f5f7] text-apple-space antialiased selection:bg-apple-coral-light selection:text-apple-coral font-sans">

  <!-- ======================================================== -->
  <!-- 1. TRANSLUCENT GLOBAL HEADER (APPLE.COM FROSTED NAVBAR)   -->
  <!-- ======================================================== -->
  <header class="sticky top-0 z-50 h-[52px] bg-white/80 backdrop-blur-xl border-b border-apple-border shadow-xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-full flex items-center justify-between">
      
      <!-- Left: Apple-Style Brand Logo -->
      <div class="flex items-center gap-3 cursor-pointer group" onclick="navigate('home')">
        <div class="w-7 h-7 rounded-full bg-apple-coral flex items-center justify-center text-white shadow-xs group-hover:scale-105 transition-transform">
          <span class="material-symbols-outlined text-[17px]" style="font-variation-settings: 'FILL' 1;">edit_note</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="text-base font-bold tracking-tight text-apple-space">ReadAWrite Pro</span>
          <span class="bg-black/5 text-apple-titanium text-[9px] font-bold px-1.5 py-0.5 rounded tracking-wider uppercase">STUDIO</span>
        </div>
      </div>

      <!-- Center: Contextual Navigation Links (Strict Rules applied!) -->
      <nav id="mainNav" class="hidden md:flex items-center gap-6 text-xs font-semibold text-apple-titanium">
        <!-- Rendered dynamically by JS: Guest Links vs Authenticated Author Links -->
      </nav>

      <!-- Right Actions: Dynamic (Guest vs Authenticated Author) -->
      <div id="navAuthArea" class="flex items-center gap-3">
        <!-- Rendered dynamically by JS -->
      </div>

    </div>
  </header>

  <!-- ======================================================== -->
  <!-- VIEW 1: APPLE KEYNOTE LANDING PAGE (DEFAULT FOR GUEST)   -->
  <!-- ======================================================== -->
  <main id="view-home" class="page-view overflow-y-auto">
    
    <!-- Monumental Hero Section -->
    <section class="relative pt-16 md:pt-24 pb-20 px-4 text-center overflow-hidden" id="hero">
      <!-- Ambient Radial Glow -->
      <div class="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[350px] bg-gradient-to-tr from-orange-200/30 via-red-100/20 to-blue-200/20 blur-3xl pointer-events-none -z-10 rounded-full"></div>
      
      <div class="max-w-4xl mx-auto space-y-6">
        <!-- Status Pill Tag -->
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/80 backdrop-blur-md border border-black/[0.06] shadow-xs text-xs text-apple-titanium">
          <span class="flex h-2 w-2 relative">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-apple-coral opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-apple-coral"></span>
          </span>
          <span class="font-medium text-apple-space">เปิดตัวสถาปัตยกรรมใหม่ Gemini 3.5 Flash Lite ⚡</span>
        </div>

        <!-- Monumental Headline -->
        <h1 class="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-apple-space leading-tight max-w-3xl mx-auto">
          แต่งนิยาย. ทรงพลัง. สละสลวย. ระดับโปร.
        </h1>

        <!-- Editorial Subtitle -->
        <p class="text-base sm:text-lg text-apple-titanium max-w-2xl mx-auto leading-relaxed font-thai">
          พบกับสตูดิโอแต่งนิยายพลัง Gemini 3.5 Flash Lite เร็วที่สุดในไทย 3,500 คำใน 19 วินาที พร้อมส่งขึ้น ReadAWrite อัตโนมัติในคลิกเดียว
        </p>

        <!-- CTA Row (Apple Pill Buttons) -->
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-3">
          <button onclick="handleStartWritingClick()" class="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-apple-coral hover:bg-apple-coral-hover text-white rounded-full px-8 py-3.5 text-xs font-bold shadow-md transition-all hover:scale-[1.02] active:scale-[0.98]">
            <span>เริ่มทดลองใช้ฟรี 7 วัน</span>
            <span class="material-symbols-outlined text-[18px]">bolt</span>
          </button>
          <a href="#features" class="inline-flex items-center gap-1.5 text-apple-blue hover:text-blue-700 text-xs font-bold group px-4 py-2 transition-colors">
            <span>ดูการทำงานของ AI</span>
            <span class="material-symbols-outlined text-[18px] transition-transform group-hover:translate-x-1">chevron_right</span>
          </a>
        </div>
      </div>

      <!-- Floating Studio Product Mockup in Apple Cinema Frame -->
      <div class="mt-14 max-w-5xl mx-auto relative px-2 sm:px-6">
        <div class="rounded-3xl bg-white border border-black/[0.08] cinema-screen-shadow p-4 sm:p-6 text-left relative overflow-hidden backdrop-blur-2xl">
          <!-- macOS Window Control Bar -->
          <div class="flex items-center justify-between pb-4 border-b border-black/[0.05] px-2">
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-[#ff5f56] border border-[#e0443e]"></span>
              <span class="w-3 h-3 rounded-full bg-[#ffbd2e] border border-[#dea123]"></span>
              <span class="w-3 h-3 rounded-full bg-[#27c93f] border border-[#1aab29]"></span>
              <span class="ml-3 text-[11px] font-bold text-apple-titanium tracking-wider">READAWRITE STUDIO PRO — DESKTOP V4.2</span>
            </div>
            <!-- Live Pills -->
            <div class="flex items-center gap-2">
              <div class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-apple-subtle border border-black/[0.04] text-[10px] text-teal-700 font-bold">
                <span class="material-symbols-outlined text-[13px]">cloud_done</span>
                <span>ซิงค์ ReadAWrite พร้อมใช้งาน</span>
              </div>
              <div class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-orange-50 border border-orange-200 text-[10px] font-bold text-apple-coral">
                <span class="material-symbols-outlined text-[13px]">speed</span>
                <span>19.2 วินาที</span>
              </div>
              <div class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-blue-50 border border-blue-200 text-[10px] font-bold text-apple-blue">
                <span class="material-symbols-outlined text-[13px]">format_ink_highlighter</span>
                <span>3,500 คำ</span>
              </div>
            </div>
          </div>

          <!-- Studio Inner Content -->
          <div class="grid grid-cols-1 md:grid-cols-12 gap-6 pt-5">
            <!-- Sidebar Mini -->
            <div class="hidden md:block md:col-span-3 border-r border-black/[0.05] pr-4 space-y-3 text-xs">
              <div class="text-[10px] font-bold text-apple-titanium uppercase tracking-wider">โครงเรื่อง &amp; บทนิยาย</div>
              <div class="p-2.5 rounded-xl bg-orange-50/70 border border-orange-200/60 text-apple-coral font-bold flex items-center justify-between">
                <span class="truncate">บทที่ 2: สี่ปีแห่งการเริ่มต้นใหม่</span>
                <span class="material-symbols-outlined text-[14px]">edit</span>
              </div>
              <div class="p-2.5 rounded-xl hover:bg-apple-subtle text-apple-space font-medium flex items-center justify-between text-apple-titanium">
                <span class="truncate">บทที่ 1: หมอกควัน ณ ซอยหลังวัง</span>
                <span class="text-[10px]">เผยแพร่แล้ว</span>
              </div>
              <div class="p-2.5 rounded-xl hover:bg-apple-subtle text-apple-space font-medium flex items-center justify-between text-apple-titanium">
                <span class="truncate">บทที่ 3: ข้อตกลงใต้แสงจันทร์</span>
                <span class="text-[10px]">แบบร่าง</span>
              </div>
              <div class="p-3 rounded-2xl bg-apple-subtle border border-black/[0.05] space-y-1">
                <div class="flex items-center gap-1 text-[11px] font-bold text-apple-space">
                  <span class="material-symbols-outlined text-[14px] text-apple-coral">psychology</span>
                  <span>ความจำตัวละคร</span>
                </div>
                <p class="text-[10px] text-apple-titanium leading-relaxed font-thai">
                  ระบบจำกัดบริบท 'พันแสง' และ 'พิมพ์ดาว' ล็อกชื่อและบทบาทแม่นยำ 100%
                </p>
              </div>
            </div>

            <!-- Central Canvas -->
            <div class="col-span-1 md:col-span-9 space-y-3 px-1 sm:px-3 font-thai">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-black/[0.04] pb-2">
                <div>
                  <span class="text-[11px] font-bold text-apple-coral">นิยายโรมานซ์ดราม่า · ผัวโบ้กลับมาเจอกัน</span>
                  <h3 class="text-base font-bold text-apple-space">
                    บทที่ 2: สี่ปีแห่งการเริ่มต้นใหม่ และการกลับมาที่ไม่มีวันเหมือนเดิม
                  </h3>
                </div>
                <span class="text-[11px] text-emerald-600 font-semibold inline-flex items-center gap-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> ซิงค์คลาวด์สมบูรณ์
                </span>
              </div>

              <div class="space-y-3 text-sm text-stone-800 leading-relaxed bg-[#fdfdfd] p-5 rounded-2xl border border-black/[0.03]">
                <p class="indent-6">
                  สายลมยามพลบค่ำพัดพากลิ่นไอฝนจางๆ ผ่านช่องหน้าต่างไม้สักโบราณเข้ามาแตะปลายจมูกของพิมพ์ดาว เธอหยุดปลายนิ้วที่กำลังจัดวางถ้วยชาศิลาดล ดวงตาคู่เรียวยังคงจับจ้องไปยังจดหมายตราครั่งสีชาดที่วางสงบนิ่งอยู่บนโต๊ะทำงาน
                </p>
                <p class="bg-orange-50/60 p-3 rounded-xl border-l-2 border-apple-coral text-xs">
                  <span class="font-bold text-apple-coral block mb-0.5">⚡ ผลิตโดย Gemini 3.5 Flash Lite (สปีด 19 วินาที)</span>
                  "ถ้าเธอคิดว่าสี่ปีที่ปารีสจะลบล้างสัญญาใจของเราสองคนได้... เธอคงประเมินความทรงจำของฉันต่ำเกินไป พิมพ์ดาว" เสียงทุ้มต่ำอันคุ้นเคยดังขึ้นจากเงามืดตรงชานเรือน ไม่ใช่เสียงในจินตนาการ แต่เป็นเขาจริงๆ—พันแสง ในชุดสูทผ้าลินินสีเข้มกับสายตาคมกริบที่สะกดลมหายใจของเธอไว้ในพริบตา
                </p>
                <p class="indent-6 text-apple-titanium">
                  พิมพ์ดาวกำชายเสื้อแน่นจนข้อนิ้วขึ้นสีขาว สี่ปีที่เธอพยายามสร้างชีวิตใหม่ ปัดเป่าความทรงจำที่แตกสลาย แต่เพียงแค่เสี้ยววินาทีที่สบตาเขา ทุกปราการที่สร้างไว้กลับพังทลายลงอย่างไม่อาจทัดทาน...
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Apple Bento Grid (Feature Highlights - 4 Tiles with 28px rounded corners) -->
    <section class="py-24 px-4 max-w-7xl mx-auto" id="features">
      <div class="text-center max-w-3xl mx-auto mb-16 space-y-2">
        <span class="text-xs font-bold tracking-wider text-apple-coral uppercase">นวัตกรรมระดับอุตสาหกรรม</span>
        <h2 class="text-3xl sm:text-4xl font-extrabold text-apple-space">
          ออกแบบเพื่อนักเขียนนิยายตัวจริง
        </h2>
        <p class="text-base text-apple-titanium font-thai">
          เทคโนโลยี AI โมเดลล้ำหน้า ผสานความสละสลวยทางวรรณศิลป์ไทยแบบไม่มีสะดุด
        </p>
      </div>

      <!-- Bento Grid (4 Tiles) -->
      <div class="grid grid-cols-1 md:grid-cols-12 gap-6">
        <!-- Tile 1: Processing Speed (Span 7) -->
        <div class="md:col-span-7 bg-white rounded-3xl p-8 sm:p-10 border border-black/[0.06] bento-card-hover flex flex-col justify-between">
          <div class="space-y-3 max-w-lg">
            <div class="w-12 h-12 rounded-2xl bg-orange-50 border border-orange-100 flex items-center justify-center text-apple-coral">
              <span class="material-symbols-outlined text-[28px]">speed</span>
            </div>
            <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-orange-100/60 text-apple-coral text-xs font-bold">
              <span>ความเร็วระดับมิลลิวินาที</span>
            </div>
            <h3 class="text-2xl font-bold text-apple-space">
              19 วินาที — สปีดการประมวลผลเร็วที่สุดในไทย
            </h3>
            <p class="text-sm text-apple-titanium leading-relaxed font-thai">
              ผลิตนิยายความยาว 3,500 คำ ได้อย่างราบรื่น ไม่มีสะดุด ไม่ตัดจบกลางคัน พร้อมการตอบสนองที่ความหน่วงต่ำเพียง 12ms ช่วยให้สมาธิการสร้างสรรค์ของนักเขียนไม่ขาดตอนแม้แต่เสี้ยววินาที
            </p>
          </div>
          <div class="mt-8 pt-6 border-t border-black/[0.05] grid grid-cols-3 gap-4">
            <div class="bg-apple-subtle p-4 rounded-2xl text-center">
              <div class="text-[11px] text-apple-titanium font-semibold">Processing Time</div>
              <div class="text-xl font-bold text-apple-space mt-1">19.2s</div>
              <div class="text-[10px] text-emerald-600 font-bold">เร็วขึ้น 4.8x</div>
            </div>
            <div class="bg-apple-subtle p-4 rounded-2xl text-center">
              <div class="text-[11px] text-apple-titanium font-semibold">Throughput</div>
              <div class="text-xl font-bold text-apple-space mt-1">184 w/s</div>
              <div class="text-[10px] text-apple-coral font-bold">คำต่อวินาที</div>
            </div>
            <div class="bg-apple-subtle p-4 rounded-2xl text-center">
              <div class="text-[11px] text-apple-titanium font-semibold">API Latency</div>
              <div class="text-xl font-bold text-apple-space mt-1">12ms</div>
              <div class="text-[10px] text-apple-blue font-bold">Zero Throttling</div>
            </div>
          </div>
        </div>

        <!-- Tile 2: Headless RAW Sync (Span 5) -->
        <div class="md:col-span-5 bg-white rounded-3xl p-8 sm:p-10 border border-black/[0.06] bento-card-hover flex flex-col justify-between">
          <div class="space-y-3">
            <div class="w-12 h-12 rounded-2xl bg-blue-50 border border-blue-100 flex items-center justify-center text-apple-blue">
              <span class="material-symbols-outlined text-[28px]">cloud_sync</span>
            </div>
            <h3 class="text-2xl font-bold text-apple-space">
              ซิงค์ไร้รอยต่อสู่ ReadAWrite
            </h3>
            <p class="text-sm text-apple-titanium leading-relaxed font-thai">
              อัปโหลดโครงเรื่อง บทสนทนา และตอนนิยายขึ้น ReadAWrite.com ได้ทันทีผ่านระบบ Headless Automation ปลอดภัย 100% ไม่ต้องคัดลอกวางเองให้เสียเวลา
            </p>
          </div>
          <div class="mt-8 p-4 rounded-2xl bg-apple-subtle border border-black/[0.05] space-y-2 text-xs">
            <div class="flex items-center gap-2 font-bold text-emerald-700">
              <span class="material-symbols-outlined text-[16px]">verified_user</span>
              <span>256-Bit Encrypted Session</span>
            </div>
            <div class="flex items-center justify-between text-apple-titanium text-[11px]">
              <span>สถานะเชื่อมต่อ:</span>
              <span class="font-bold text-apple-space">i_Am_Status (RAW Cloud Ready)</span>
            </div>
          </div>
        </div>

        <!-- Tile 3: ProofAI 2.4 (Span 5) -->
        <div class="md:col-span-5 bg-white rounded-3xl p-8 sm:p-10 border border-black/[0.06] bento-card-hover flex flex-col justify-between">
          <div class="space-y-3">
            <div class="w-12 h-12 rounded-2xl bg-purple-50 border border-purple-100 flex items-center justify-center text-purple-600">
              <span class="material-symbols-outlined text-[28px]">spellcheck</span>
            </div>
            <h3 class="text-2xl font-bold text-apple-space">
              ProofAI 2.4 วรรณศิลป์ไทย
            </h3>
            <p class="text-sm text-apple-titanium leading-relaxed font-thai">
              ตรวจสำนวน คำผิด วรรคตอน และการซ้ำซากของคำด้วยเอนจินเฉพาะทางวิเคราะห์รากศัพท์ภาษาไทยด้วย PyThaiNLP
            </p>
            <div class="p-4 rounded-2xl bg-apple-subtle border border-black/[0.04] space-y-2 text-xs font-thai">
              <div class="text-apple-titanium line-through">"เขาได้รับโอกาสที่ดีในชีวิตเป็นอย่างมาก"</div>
              <div class="text-apple-coral font-bold flex items-center gap-1.5">
                <span class="material-symbols-outlined text-[14px]">arrow_forward</span>
                <span>"วาสนาชะตาชีวิตเปิดทางให้เขาอย่างที่ไม่เคยคาดฝัน"</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Tile 4: Character Context Memory (Span 7) -->
        <div class="md:col-span-7 bg-white rounded-3xl p-8 sm:p-10 border border-black/[0.06] bento-card-hover flex flex-col justify-between">
          <div class="space-y-3">
            <div class="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600">
              <span class="material-symbols-outlined text-[28px]">psychology</span>
            </div>
            <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100/70 text-emerald-800 text-xs font-bold">
              <span>บริบทไม่รู้จบ 1,000,000 โทเค็น</span>
            </div>
            <h3 class="text-2xl font-bold text-apple-space">
              ความจำปัญญาประดิษฐ์ — คลังบริบทตัวละคร
            </h3>
            <p class="text-sm text-apple-titanium leading-relaxed font-thai">
              หมดปัญหา AI สับสนชื่อตัวละคร เปลี่ยนสีตา ลืมปูมหลัง หรือลืมความสัมพันธ์ในอดีต รองรับ Lore, Codex, กฎของเวทมนตร์ และสายสัมพันธ์ตัวละครมากกว่า 100 ตอนได้อย่างแม่นยำถาวร
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Apple One Style Pricing Comparison Matrix (4 Clean Columns) -->
    <section class="py-24 px-4 bg-white border-y border-black/[0.06]" id="pricing">
      <div class="max-w-7xl mx-auto space-y-16">
        <div class="text-center max-w-3xl mx-auto space-y-2">
          <span class="text-xs font-bold tracking-wider text-apple-coral uppercase">ความคุ้มค่าระดับพรีเมียม</span>
          <h2 class="text-3xl sm:text-4xl font-extrabold text-apple-space">
            เลือกแพ็กเกจที่ลงตัวกับจินตนาการของคุณ
          </h2>
          <p class="text-base text-apple-titanium font-thai">
            ทดลองใช้ฟังก์ชันเต็มฟรี 7 วัน ยกเลิกได้ตลอดเวลา ไม่มีข้อผูกมัด
          </p>
        </div>

        <!-- 4-Column Matrix -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          
          <!-- Column 1: 7-Day Free Trial -->
          <div class="bg-apple-subtle rounded-3xl p-8 border border-black/[0.06] flex flex-col justify-between bento-card-hover">
            <div class="space-y-6">
              <div>
                <span class="text-xs font-bold text-apple-titanium uppercase tracking-wider">เริ่มต้นทดลอง</span>
                <h3 class="text-xl font-bold text-apple-space mt-1">7-Day Free Trial</h3>
                <div class="mt-4 flex items-baseline gap-1">
                  <span class="text-3xl font-black text-apple-space">฿0</span>
                  <span class="text-xs font-medium text-apple-titanium">/ 7 วันแรก</span>
                </div>
                <p class="text-xs text-apple-titanium mt-2 font-thai">สัมผัสประสบการณ์โมเดลเต็มรูปแบบโดยไม่ต้องจ่ายเงินล่วงหน้า</p>
              </div>
              <div class="pt-4 border-t border-black/[0.06] space-y-3 text-xs font-thai">
                <div class="flex items-center gap-2 text-apple-space font-medium">
                  <span class="material-symbols-outlined text-[16px] text-emerald-600">check_circle</span>
                  <span>โควตา 50,000 คำ</span>
                </div>
                <div class="flex items-center gap-2 text-apple-space font-medium">
                  <span class="material-symbols-outlined text-[16px] text-emerald-600">check_circle</span>
                  <span>โมเดล Gemini 3.5 Flash Lite</span>
                </div>
                <div class="flex items-center gap-2 text-apple-space font-medium">
                  <span class="material-symbols-outlined text-[16px] text-emerald-600">check_circle</span>
                  <span>ทดลอง ProofAI ภาษาไทย</span>
                </div>
              </div>
            </div>
            <div class="mt-8 pt-4">
              <button onclick="handleStartWritingClick()" class="w-full py-2.5 px-4 rounded-full bg-white hover:bg-stone-100 text-apple-space font-bold text-xs border border-black/[0.08] shadow-xs transition-all">
                เริ่มทดลองทันที
              </button>
            </div>
          </div>

          <!-- Column 2: Pro Monthly -->
          <div class="bg-white rounded-3xl p-8 border border-black/[0.08] shadow-xs flex flex-col justify-between bento-card-hover">
            <div class="space-y-6">
              <div>
                <span class="text-xs font-bold text-apple-blue uppercase tracking-wider">รายเดือนยอดนิยม</span>
                <h3 class="text-xl font-bold text-apple-space mt-1">Pro Monthly</h3>
                <div class="mt-4 flex items-baseline gap-1">
                  <span class="text-3xl font-black text-apple-space">฿390</span>
                  <span class="text-xs font-medium text-apple-titanium">/ เดือน</span>
                </div>
                <p class="text-xs text-apple-titanium mt-2 font-thai">ยืดหยุ่น เหมาะสำหรับนักเขียนที่ต้องการปล่อยงานต่อเนื่อง</p>
              </div>
              <div class="pt-4 border-t border-black/[0.06] space-y-3 text-xs font-thai">
                <div class="flex items-center gap-2 text-apple-space font-medium">
                  <span class="material-symbols-outlined text-[16px] text-apple-coral">check_circle</span>
                  <span>โควตา 500,000 คำ/เดือน</span>
                </div>
                <div class="flex items-center gap-2 text-apple-space font-medium">
                  <span class="material-symbols-outlined text-[16px] text-apple-coral">check_circle</span>
                  <span>ซิงค์ RAW อัตโนมัติไม่จำกัด</span>
                </div>
                <div class="flex items-center gap-2 text-apple-space font-medium">
                  <span class="material-symbols-outlined text-[16px] text-apple-coral">check_circle</span>
                  <span>ProofAI เกลาสำนวนไม่จำกัด</span>
                </div>
              </div>
            </div>
            <div class="mt-8 pt-4">
              <button onclick="openCheckoutModal('monthly')" class="w-full py-2.5 px-4 rounded-full bg-apple-space hover:bg-black text-white font-bold text-xs shadow-xs transition-all">
                เลือกแพ็กเกจรายเดือน
              </button>
            </div>
          </div>

          <!-- Column 3: Pro Annual (Featured / Best Value) -->
          <div class="bg-white rounded-3xl p-8 border-2 border-apple-coral shadow-md flex flex-col justify-between relative bento-card-hover">
            <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-apple-coral text-white text-[10px] font-bold px-3 py-0.5 rounded-full shadow-xs">
              แนะนำคุ้มค่าที่สุด (ประหยัด 2 เดือน)
            </div>
            <div class="space-y-6">
              <div>
                <span class="text-xs font-bold text-apple-coral uppercase tracking-wider">รายปีไม่จำกัด</span>
                <h3 class="text-xl font-bold text-apple-space mt-1">Pro Annual</h3>
                <div class="mt-4 flex items-baseline gap-1">
                  <span class="text-3xl font-black text-apple-coral">฿3,900</span>
                  <span class="text-xs font-medium text-apple-titanium">/ ปี (฿325/ด.)</span>
                </div>
                <p class="text-xs text-apple-titanium mt-2 font-thai">สำหรับนักเขียนมืออาชีพที่ต้องการความคุ้มค่าสูงสุด</p>
              </div>
              <div class="pt-4 border-t border-black/[0.06] space-y-3 text-xs font-thai">
                <div class="flex items-center gap-2 text-apple-space font-medium">
                  <span class="material-symbols-outlined text-[16px] text-apple-coral">check_circle</span>
                  <span>โควตา 6,000,000 คำ/ปี</span>
                </div>
                <div class="flex items-center gap-2 text-apple-space font-medium">
                  <span class="material-symbols-outlined text-[16px] text-apple-coral">check_circle</span>
                  <span>ตั้งเวลาล่วงหน้า 30 วัน</span>
                </div>
                <div class="flex items-center gap-2 text-apple-space font-medium">
                  <span class="material-symbols-outlined text-[16px] text-apple-coral">check_circle</span>
                  <span>แต่ง 3 ตอนรวดในคลิกเดียว</span>
                </div>
              </div>
            </div>
            <div class="mt-8 pt-4">
              <button onclick="openCheckoutModal('annual')" class="w-full py-2.5 px-4 rounded-full bg-apple-coral hover:bg-apple-coral-hover text-white font-bold text-xs shadow-md transition-all">
                เลือกแพ็กเกจรายปี
              </button>
            </div>
          </div>

          <!-- Column 4: Lifetime VIP -->
          <div class="bg-apple-space rounded-3xl p-8 border border-black/10 text-white flex flex-col justify-between bento-card-hover shadow-md">
            <div class="space-y-6">
              <div>
                <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">ครั้งเดียวจบ</span>
                <h3 class="text-xl font-bold text-white mt-1">Lifetime VIP</h3>
                <div class="mt-4 flex items-baseline gap-1">
                  <span class="text-3xl font-black text-amber-400">฿6,900</span>
                  <span class="text-xs font-medium text-stone-400">/ ตลอดชีพ</span>
                </div>
                <p class="text-xs text-stone-400 mt-2 font-thai">ไม่ต้องจ่ายรายเดือนอีกต่อไป เข้าถึงโมเดลใหม่ตลอดชีพ</p>
              </div>
              <div class="pt-4 border-t border-white/10 space-y-3 text-xs font-thai">
                <div class="flex items-center gap-2 text-white font-medium">
                  <span class="material-symbols-outlined text-[16px] text-amber-400">verified</span>
                  <span>โควตาไม่จำกัดตลอดชีพ</span>
                </div>
                <div class="flex items-center gap-2 text-white font-medium">
                  <span class="material-symbols-outlined text-[16px] text-amber-400">verified</span>
                  <span>ซัปพอร์ตส่วนตัวแบบ VIP</span>
                </div>
                <div class="flex items-center gap-2 text-white font-medium">
                  <span class="material-symbols-outlined text-[16px] text-amber-400">verified</span>
                  <span>เข้ากลุ่มนักเขียนท็อปชาร์ต RAW</span>
                </div>
              </div>
            </div>
            <div class="mt-8 pt-4">
              <button onclick="openCheckoutModal('lifetime')" class="w-full py-2.5 px-4 rounded-full bg-amber-500 hover:bg-amber-600 text-stone-900 font-bold text-xs shadow-xs transition-all">
                สมัคร Lifetime VIP
              </button>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="py-20 px-4 max-w-4xl mx-auto space-y-8" id="faq">
      <div class="text-center space-y-2">
        <h2 class="text-2xl sm:text-3xl font-extrabold text-apple-space">คำถามที่พบบ่อย (FAQ)</h2>
        <p class="text-xs text-apple-titanium">ข้อสงสัยเกี่ยวกับการใช้งานและระบบสมาชิก</p>
      </div>

      <div class="space-y-4 font-thai text-xs">
        <div class="bg-white p-5 rounded-2xl border border-black/[0.06] shadow-xs">
          <div class="font-bold text-apple-space text-sm mb-1.5">โควตา 50,000 คำตอนทดลองฟรี ใช้ได้จริงไหม?</div>
          <p class="text-apple-titanium leading-relaxed">ใช้ได้จริง 100% ครับ ระบบจะนับคำตามจริงด้วย PyThaiNLP เทียบเท่าการเขียนนิยายประมาณ 15-20 ตอนขนาดมาตรฐาน โดยไม่ต้องใส่บัตรเครดิต</p>
        </div>
        <div class="bg-white p-5 rounded-2xl border border-black/[0.06] shadow-xs">
          <div class="font-bold text-apple-space text-sm mb-1.5">ข้อมูลนิยายจะหลุดไปให้คนอื่นเห็นหรือไม่?</div>
          <p class="text-apple-titanium leading-relaxed">ระบบมีฐานข้อมูลแยกบัญชีแบบ Multi-Tenant พล็อตนิยาย คาแรคเตอร์ และเนื้อหาทั้งหมดจะผูกกับบัญชีของคุณเท่านั้น คนอื่นหรือผู้เยี่ยมชมไม่สามารถเข้าถึงได้</p>
        </div>
        <div class="bg-white p-5 rounded-2xl border border-black/[0.06] shadow-xs">
          <div class="font-bold text-apple-space text-sm mb-1.5">ถ้าโควตาหมดกลางคัน สามารถเติมคำได้ไหม?</div>
          <p class="text-apple-titanium leading-relaxed">สามารถกดปุ่ม "อัปเกรดแพ็กเกจ" หรือเติมโควตาคำผ่านระบบพร้อมเพย์ QR Code ได้ทันที โควตาจะเข้าบัญชีแบบ Real-time</p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-white border-t border-black/[0.06] py-10 text-center text-xs text-apple-titanium">
      <div class="max-w-7xl mx-auto px-4 flex flex-wrap items-center justify-between gap-4">
        <div>&copy; 2026 ReadAWrite Pro Studio. ออกแบบด้วยแรงบันดาลใจระดับโลก Cupertino Luxury Aesthetic</div>
        <div class="flex items-center gap-4">
          <span>ความปลอดภัย SSL 256-Bit</span>
          <span>•</span>
          <span>Google Gemini 3.5 Flash Lite</span>
        </div>
      </div>
    </footer>
  </main>

  <!-- ======================================================== -->
  <!-- VIEW 2: MY NOVELS MANAGEMENT (AUTHENTICATED ONLY)        -->
  <!-- ======================================================== -->
  <main id="view-novels" class="page-view hidden overflow-y-auto p-6 max-w-7xl mx-auto">
    <div class="flex flex-wrap items-center justify-between gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-extrabold text-apple-space">นิยายและผลงานของฉัน</h1>
        <p class="text-xs text-apple-titanium mt-1 font-thai">คลังนิยายส่วนตัว ควบคุมพล็อต ตอน และการซิงค์ ReadAWrite</p>
      </div>
      <button onclick="openCreateNovelModal()" class="px-5 py-2.5 bg-apple-coral hover:bg-apple-coral-hover text-white text-xs font-bold rounded-full shadow-xs transition-all flex items-center gap-1.5">
        <span class="material-symbols-outlined text-[18px]">add_circle</span>
        <span>+ สร้างนิยายเรื่องใหม่</span>
      </button>
    </div>

    <!-- Novels Grid -->
    <div id="novelsGrid" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Rendered dynamically by JS from /api/novels -->
    </div>
  </main>

  <!-- ======================================================== -->
  <!-- VIEW 3: 3-PANEL AI WRITING STUDIO (AUTHENTICATED ONLY)   -->
  <!-- ======================================================== -->
  <main id="view-studio" class="page-view hidden h-[calc(100vh-52px)] flex overflow-hidden">
    
    <!-- Left Sidebar: Chapter List (280px) -->
    <aside class="w-[280px] flex-shrink-0 bg-white border-r border-apple-border flex flex-col justify-between overflow-y-auto custom-scrollbar p-4">
      <div>
        <div class="bg-apple-subtle rounded-2xl p-3 border border-black/[0.04] mb-4">
          <span class="text-[10px] font-bold text-apple-coral bg-orange-50 px-2 py-0.5 rounded-full uppercase" id="studioNovelGenre">ผัวโบ้ / กลับมาเจอกัน</span>
          <h3 class="text-sm font-bold text-apple-space mt-1.5 line-clamp-2" id="studioNovelTitle">กำลังโหลด...</h3>
        </div>

        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-bold text-apple-titanium uppercase">สารบัญบทนิยาย</span>
          <button onclick="addChapterPrompt()" class="text-[11px] font-bold text-apple-coral hover:underline flex items-center gap-0.5">
            <span class="material-symbols-outlined text-[14px]">add</span> เพิ่มตอน
          </button>
        </div>

        <div id="studioChaptersList" class="space-y-1.5">
          <!-- Rendered by JS -->
        </div>
      </div>

      <div class="pt-3 border-t border-apple-border text-center text-xs text-apple-titanium">
        <span class="flex items-center justify-center gap-1 text-teal-700 font-semibold text-[11px]">
          <span class="material-symbols-outlined text-[14px]">cloud_done</span> ซิงค์อัตโนมัติ SQLite Cloud
        </span>
      </div>
    </aside>

    <!-- Center: AI Controls Island (360px) -->
    <section class="w-[360px] flex-shrink-0 bg-[#fafafa] border-r border-apple-border flex flex-col justify-between overflow-y-auto custom-scrollbar p-5">
      <div class="space-y-5">
        <div>
          <h2 class="text-base font-extrabold text-apple-space flex items-center gap-1.5">
            <span class="material-symbols-outlined text-apple-coral text-[20px]">smart_toy</span>
            <span>แผงควบคุม AI Co-Pilot</span>
          </h2>
          <p class="text-xs text-apple-titanium mt-0.5 font-thai">กำหนดเป้าหมายคำและสั่งสร้างเนื้อหา</p>
        </div>

        <!-- Slider -->
        <div class="bg-white p-4 rounded-2xl border border-black/[0.06] shadow-xs">
          <div class="flex justify-between items-center mb-2">
            <label class="text-xs font-bold text-apple-space">เป้าหมายจำนวนคำ</label>
            <span id="targetWordsDisplay" class="text-xs font-bold text-apple-coral bg-orange-50 px-2.5 py-0.5 rounded-full">2,500 คำ</span>
          </div>
          <input id="targetWordsSlider" type="range" min="1000" max="4500" step="500" value="2500" class="w-full accent-apple-coral cursor-pointer"/>
          <div class="flex justify-between text-[10px] text-apple-titanium mt-1">
            <span>1,000 คำ</span>
            <span>2,500 คำ</span>
            <span>4,500 คำ</span>
          </div>
        </div>

        <!-- AI Engine Status -->
        <div class="bg-white p-3 rounded-2xl border border-black/[0.06] text-xs">
          <div class="flex items-center justify-between font-bold text-apple-space">
            <span>โมเดล AI</span>
            <span class="text-teal-700 flex items-center gap-1">
              <span class="w-2 h-2 rounded-full bg-teal-500 animate-ping"></span>
              Gemini 3.5 Flash Lite ⚡
            </span>
          </div>
          <p class="text-[11px] text-apple-titanium mt-1 font-thai">ประมวลผลเร็วที่สุดในไทย ~19 วินาที</p>
        </div>

        <!-- Action Buttons -->
        <div class="space-y-2 pt-2">
          <button id="btnGenerate" onclick="triggerGenerateChapter()" class="w-full py-3 bg-apple-coral hover:bg-apple-coral-hover text-white font-bold text-xs rounded-full shadow-md transition-all flex items-center justify-center gap-1.5">
            <span class="material-symbols-outlined text-[18px]">auto_awesome</span>
            <span>✨ แต่งบทนี้ทันทีด้วย AI</span>
          </button>
          <button id="btnCritic" onclick="triggerCriticPass()" class="w-full py-2.5 bg-white hover:bg-stone-100 text-apple-space font-bold text-xs rounded-full border border-black/[0.08] transition-all flex items-center justify-center gap-1.5">
            <span class="material-symbols-outlined text-[16px]">spellcheck</span>
            <span>🔍 เกลาสำนวน ProofAI</span>
          </button>
          <button id="btnSync" onclick="openPublishModal()" class="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white font-bold text-xs rounded-full shadow-xs transition-all flex items-center justify-center gap-1.5">
            <span class="material-symbols-outlined text-[16px]">send</span>
            <span>🚀 ซิงค์ส่ง &amp; ตั้งเวลาเผยแพร่ออโต้</span>
          </button>
          <button id="btnSave" onclick="saveCurrentChapter()" class="w-full py-2 border border-black/[0.08] hover:bg-white text-apple-titanium hover:text-apple-space font-semibold text-xs rounded-full transition-all flex items-center justify-center gap-1">
            <span class="material-symbols-outlined text-[15px]">save</span>
            <span>💾 บันทึกเนื้อหาลงระบบ</span>
          </button>
        </div>
      </div>

      <!-- Quota Chip -->
      <div class="bg-orange-50/70 p-3 rounded-2xl border border-orange-200 text-xs">
        <div class="flex justify-between items-center font-bold text-apple-coral">
          <span>โควตาคำคงเหลือ</span>
          <span id="studioQuotaText">...</span>
        </div>
        <div class="w-full bg-orange-200 h-1.5 rounded-full mt-2 overflow-hidden">
          <div id="studioQuotaBar" class="bg-apple-coral h-1.5 rounded-full" style="width: 20%;"></div>
        </div>
      </div>
    </section>

    <!-- Right: Manuscript Reader View (Apple Pages Minimalist) -->
    <section class="flex-1 bg-[#fcfbf7] overflow-y-auto custom-scrollbar p-8 lg:p-12">
      <div class="max-w-3xl mx-auto bg-white p-8 sm:p-12 rounded-3xl shadow-sm border border-black/[0.06] min-h-full flex flex-col justify-between">
        <div>
          <div class="border-b border-black/[0.06] pb-6 mb-8 text-center font-thai">
            <span class="text-xs font-bold text-apple-coral tracking-wider uppercase" id="editorStoryTitle">ชื่อเรื่อง</span>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-apple-space mt-1" id="editorChapterTitle">บทที่ 1: ชื่อตอน</h1>
            <p class="text-xs text-apple-titanium mt-2" id="editorChapterStats">0 คำ • แบบร่าง</p>
          </div>
          <div id="manuscriptContent" contenteditable="true" class="font-thai text-base leading-relaxed text-stone-800 space-y-4 focus:outline-none min-h-[400px]">
            <!-- Injected by JS -->
          </div>
        </div>
        <div class="mt-8 pt-4 border-t border-black/[0.06] flex items-center justify-between text-xs text-apple-titanium">
          <span id="realtimeWordsCounter">📊 0 คำ</span>
          <span>แบบร่างในเครื่อง พร้อมบันทึก</span>
        </div>
      </div>
    </section>

  </main>

  <!-- ======================================================== -->
  <!-- VIEW 4: SUPER ADMIN HQ (SUPER ADMIN ONLY)                -->
  <!-- ======================================================== -->
  <main id="view-admin" class="page-view hidden overflow-y-auto p-6 max-w-7xl mx-auto space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="bg-amber-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">Super Admin</span>
          <h1 class="text-2xl font-black text-apple-space">ศูนย์ควบคุมระบบสมาชิก &amp; แพลตฟอร์ม</h1>
        </div>
        <p class="text-xs text-apple-titanium mt-1 font-thai">จัดการสถานะสมาชิก เติมโควตาคำ AI ตรวจสอบรายได้ และดูความสมบูรณ์ของระบบ</p>
      </div>
      <button onclick="loadAdminData()" class="px-4 py-2 bg-white hover:bg-stone-50 border border-black/[0.08] rounded-full text-xs font-bold text-apple-space flex items-center gap-1 shadow-xs">
        <span class="material-symbols-outlined text-[16px]">refresh</span>
        <span>รีเฟรชข้อมูล</span>
      </button>
    </div>

    <!-- KPI Summary Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-white p-5 rounded-3xl border border-black/[0.06] shadow-xs">
        <span class="text-xs font-semibold text-apple-titanium">สมาชิกที่ลงทะเบียน</span>
        <div class="text-2xl font-black text-apple-space mt-1" id="adminStatUsers">-</div>
        <span class="text-[11px] text-teal-700 font-semibold">SQLite Database Backed</span>
      </div>
      <div class="bg-white p-5 rounded-3xl border border-black/[0.06] shadow-xs">
        <span class="text-xs font-semibold text-apple-titanium">ยอดคำ AI ที่ผลิตไปแล้ว</span>
        <div class="text-2xl font-black text-apple-coral mt-1" id="adminStatWords">-</div>
        <span class="text-[11px] text-apple-titanium">นับด้วย PyThaiNLP</span>
      </div>
      <div class="bg-white p-5 rounded-3xl border border-black/[0.06] shadow-xs">
        <span class="text-xs font-semibold text-apple-titanium">รายได้จากแพ็กเกจ</span>
        <div class="text-2xl font-black text-teal-700 mt-1" id="adminStatRevenue">-</div>
        <span class="text-[11px] text-teal-600 font-semibold">ยอดจริงจากตาราง Orders</span>
      </div>
      <div class="bg-white p-5 rounded-3xl border border-black/[0.06] shadow-xs">
        <span class="text-xs font-semibold text-apple-titanium">สถานะ Gemini Engine</span>
        <div class="text-sm font-bold text-teal-700 mt-1 flex items-center gap-1">
          <span class="w-2 h-2 rounded-full bg-teal-500 animate-ping"></span>
          Online (Flash Lite ⚡)
        </div>
        <span class="text-[11px] text-apple-titanium">Playwright: พร้อมซิงค์</span>
      </div>
    </div>

    <!-- User List Table -->
    <div class="bg-white rounded-3xl border border-black/[0.06] shadow-xs overflow-hidden">
      <div class="p-5 border-b border-black/[0.06] flex items-center justify-between">
        <h3 class="text-sm font-bold text-apple-space">รายชื่อสมาชิกและการใช้งานโควตาคำ</h3>
        <span class="text-xs text-apple-titanium">คลิก "จัดการ" เพื่อปรับแพ็กเกจหรือเติมโควตา</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs font-thai">
          <thead class="bg-apple-subtle font-bold text-apple-titanium border-b border-black/[0.06]">
            <tr>
              <th class="p-3.5">ID / นามปากกา</th>
              <th class="p-3.5">อีเมล</th>
              <th class="p-3.5">บทบาท</th>
              <th class="p-3.5">แพ็กเกจ</th>
              <th class="p-3.5">สถานะ</th>
              <th class="p-3.5">โควตาคำ (ใช้ไป / ทั้งหมด)</th>
              <th class="p-3.5 text-right">การจัดการ</th>
            </tr>
          </thead>
          <tbody id="adminUserTableBody" class="divide-y divide-black/[0.04]">
            <!-- Rendered by JS -->
          </tbody>
        </table>
      </div>
    </div>
  </main>

  <!-- ======================================================== -->
  <!-- MODAL: AUTHENTICATION (LOGIN / REGISTER WITH 7-DAY TRIAL)-->
  <!-- ======================================================== -->
  <div id="authModal" class="hidden fixed inset-0 z-50 overflow-y-auto bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white max-w-md w-full rounded-3xl shadow-2xl border border-black/[0.08] overflow-hidden">
      <div class="p-5 border-b border-black/[0.06] flex items-center justify-between bg-apple-subtle">
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 rounded-full bg-apple-coral flex items-center justify-center text-white">
            <span class="material-symbols-outlined text-[16px]">stylus_note</span>
          </div>
          <span class="font-bold text-sm text-apple-space">ReadAWrite Pro Studio</span>
        </div>
        <button onclick="closeAuthModal()" class="p-1 rounded-full text-apple-titanium hover:text-apple-space">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>

      <!-- Auth Tabs -->
      <div class="flex border-b border-black/[0.06] text-xs font-bold">
        <button id="tabBtnRegister" onclick="switchAuthTab('register')" class="flex-1 py-3 text-center border-b-2 border-apple-coral text-apple-coral bg-orange-50/50">
          สมัครสมาชิกใหม่ (ฟรี 7 วัน)
        </button>
        <button id="tabBtnLogin" onclick="switchAuthTab('login')" class="flex-1 py-3 text-center text-apple-titanium hover:text-apple-space">
          เข้าสู่ระบบ
        </button>
      </div>

      <!-- Tab 1: Register Form -->
      <form id="formRegister" onsubmit="handleRegisterSubmit(event)" class="p-6 space-y-4 text-xs font-thai">
        <div class="bg-orange-50/70 p-3 rounded-2xl border border-orange-200 text-apple-coral text-[11px] leading-relaxed">
          ✨ <strong>สิทธิพิเศษสำหรับคุณ:</strong> สมัครแล้วรับโควตา AI 50,000 คำ และสิทธิ์ทดลองใช้ 7 วันทันทีโดยไม่ต้องใส่บัตรเครดิต!
        </div>
        <div>
          <label class="block font-bold text-apple-space mb-1">นามปากกา / ชื่อผู้ใช้ *</label>
          <input id="regPenName" type="text" placeholder="เช่น รดา นิยายรัก" class="w-full px-3 py-2 bg-apple-subtle border border-black/[0.06] rounded-xl outline-none focus:border-apple-coral text-xs" required />
        </div>
        <div>
          <label class="block font-bold text-apple-space mb-1">อีเมล *</label>
          <input id="regEmail" type="email" placeholder="author@example.com" class="w-full px-3 py-2 bg-apple-subtle border border-black/[0.06] rounded-xl outline-none focus:border-apple-coral text-xs" required />
        </div>
        <div>
          <label class="block font-bold text-apple-space mb-1">รหัสผ่าน *</label>
          <input id="regPassword" type="password" placeholder="อย่างน้อย 6 ตัวอักษร" class="w-full px-3 py-2 bg-apple-subtle border border-black/[0.06] rounded-xl outline-none focus:border-apple-coral text-xs" required />
        </div>
        <button type="submit" class="w-full py-3 bg-apple-coral hover:bg-apple-coral-hover text-white font-bold rounded-full shadow-xs transition-all text-xs">
          สมัครและเริ่มแต่งนิยายทันที
        </button>
      </form>

      <!-- Tab 2: Login Form -->
      <form id="formLogin" onsubmit="handleLoginSubmit(event)" class="hidden p-6 space-y-4 text-xs font-thai">
        <div>
          <label class="block font-bold text-apple-space mb-1">อีเมล</label>
          <input id="loginEmail" type="email" placeholder="author@example.com" class="w-full px-3 py-2 bg-apple-subtle border border-black/[0.06] rounded-xl outline-none focus:border-apple-coral text-xs" required />
        </div>
        <div>
          <label class="block font-bold text-apple-space mb-1">รหัสผ่าน</label>
          <input id="loginPassword" type="password" placeholder="••••••••" class="w-full px-3 py-2 bg-apple-subtle border border-black/[0.06] rounded-xl outline-none focus:border-apple-coral text-xs" required />
        </div>
        <button type="submit" class="w-full py-3 bg-apple-space hover:bg-black text-white font-bold rounded-full shadow-xs transition-all text-xs">
          เข้าสู่ระบบ
        </button>

        <div class="pt-4 border-t border-black/[0.06]">
          <span class="block text-[10px] text-apple-titanium mb-2 uppercase font-bold text-center">ทางลัดทดสอบระบบ (Quick Demo)</span>
          <div class="grid grid-cols-2 gap-2">
            <button type="button" onclick="quickLogin('admin@readawrite.pro', 'admin1234')" class="py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 rounded-xl text-[11px] font-bold">
              👑 เข้าสู่ระบบเป็น Admin
            </button>
            <button type="button" onclick="quickLogin('writer@readawrite.pro', '123456')" class="py-1.5 bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-200 rounded-xl text-[11px] font-bold">
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
  <div id="createNovelModal" class="hidden fixed inset-0 z-50 overflow-y-auto bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white max-w-lg w-full rounded-3xl shadow-2xl border border-black/[0.08] overflow-hidden">
      <div class="p-5 border-b border-black/[0.06] flex items-center justify-between bg-apple-subtle">
        <h3 class="font-bold text-sm text-apple-space flex items-center gap-1.5">
          <span class="material-symbols-outlined text-apple-coral text-[20px]">add_box</span>
          <span>สร้างนิยายเรื่องใหม่</span>
        </h3>
        <button onclick="document.getElementById('createNovelModal').classList.add('hidden')" class="p-1 rounded-full text-apple-titanium hover:text-apple-space">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>
      <form onsubmit="handleCreateNovelSubmit(event)" class="p-6 space-y-4 text-xs font-thai">
        <div>
          <label class="block font-bold text-apple-space mb-1">ชื่อเรื่องนิยาย *</label>
          <input id="novelTitle" type="text" placeholder="เช่น เล่ห์รักท่านประธานร้าย" class="w-full px-3 py-2 bg-apple-subtle border border-black/[0.06] rounded-xl outline-none focus:border-apple-coral text-xs" required />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block font-bold text-apple-space mb-1">หมวดหมู่</label>
            <select id="novelCategory" class="w-full px-3 py-2 bg-apple-subtle border border-black/[0.06] rounded-xl outline-none focus:border-apple-coral text-xs">
              <option value="โรมานซ์">โรมานซ์ / รักหวานแหวว</option>
              <option value="ดราม่า">ดราม่า / แก้แค้น</option>
              <option value="แฟนตาซี">แฟนตาซี / ย้อนยุค</option>
              <option value="วาย / Boy Love">นิยายวาย (Boy Love)</option>
            </select>
          </div>
          <div>
            <label class="block font-bold text-apple-space mb-1">สไตล์พล็อต (Genre)</label>
            <input id="novelGenre" type="text" value="ผัวโบ้ / กลับมาเจอกัน" class="w-full px-3 py-2 bg-apple-subtle border border-black/[0.06] rounded-xl outline-none focus:border-apple-coral text-xs" />
          </div>
        </div>
        <div>
          <label class="block font-bold text-apple-space mb-1">เรื่องย่อ (Synopsis)</label>
          <textarea id="novelSynopsis" rows="3" placeholder="เขียนเรื่องย่อสำหรับให้ AI จดจำโครงสร้างเนื้อหา..." class="w-full px-3 py-2 bg-apple-subtle border border-black/[0.06] rounded-xl outline-none focus:border-apple-coral text-xs"></textarea>
        </div>
        <div class="flex justify-end gap-2 pt-2 border-t border-black/[0.06]">
          <button type="button" onclick="document.getElementById('createNovelModal').classList.add('hidden')" class="px-4 py-2 font-bold text-apple-titanium hover:text-apple-space">ยกเลิก</button>
          <button type="submit" class="px-5 py-2 bg-apple-coral hover:bg-apple-coral-hover text-white font-bold rounded-full shadow-xs">สร้างและเข้าห้องแต่งทันที</button>
        </div>
      </form>
    </div>
  </div>

  <!-- ======================================================== -->
  <!-- MODAL: CHECKOUT & UPGRADE (PROMPTPAY QR)                 -->
  <!-- ======================================================== -->
  <div id="checkoutModal" class="hidden fixed inset-0 z-50 overflow-y-auto bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white max-w-lg w-full rounded-3xl shadow-2xl border border-black/[0.08] overflow-hidden">
      <div class="p-5 border-b border-black/[0.06] flex items-center justify-between bg-apple-subtle">
        <div>
          <span class="text-[10px] font-bold text-apple-coral uppercase">อัปเกรดสถานะสมาชิก</span>
          <h3 class="text-base font-extrabold text-apple-space" id="checkoutPlanTitle">Pro Monthly (รายเดือน)</h3>
        </div>
        <button onclick="document.getElementById('checkoutModal').classList.add('hidden')" class="p-1 rounded-full text-apple-titanium hover:text-apple-space">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>

      <div class="p-6 space-y-5 text-xs font-thai">
        <div class="bg-orange-50/70 p-4 rounded-2xl border border-orange-200 flex items-center justify-between">
          <div>
            <span class="font-bold text-apple-coral block" id="checkoutPlanDesc">โควตา 500,000 คำ / 30 วัน</span>
            <span class="text-apple-titanium text-[11px]">ปลดล็อกแต่งนิยาย AI ไม่จำกัด พร้อมซิงค์ ReadAWrite</span>
          </div>
          <div class="text-2xl font-black text-apple-coral" id="checkoutAmount">฿390</div>
        </div>

        <div>
          <label class="block font-bold text-apple-space mb-2">วิธีชำระเงิน</label>
          <div class="p-3 border-2 border-apple-coral bg-orange-50/30 rounded-2xl flex items-center gap-2">
            <span class="material-symbols-outlined text-apple-coral text-[22px]">qr_code_scanner</span>
            <div>
              <span class="font-bold block text-apple-space text-xs">พร้อมเพย์ QR Code</span>
              <span class="text-[10px] text-apple-titanium">สแกนจ่ายได้ทุกธนาคารไทย</span>
            </div>
          </div>
        </div>

        <div class="bg-apple-subtle p-4 rounded-2xl border border-black/[0.06] text-center">
          <div class="w-40 h-40 bg-white p-2 mx-auto rounded-2xl border border-black/[0.06] shadow-xs flex items-center justify-center">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=PROMPTPAY-READAWRITE-SAAS" class="w-full h-full object-contain" alt="PromptPay QR Code"/>
          </div>
          <p class="text-[11px] text-apple-titanium mt-2">ยอดชำระ: <strong class="text-apple-coral text-xs" id="qrAmountDisplay">฿390.00</strong> (จำลองระบบชำระเงินจริง)</p>
        </div>

        <button onclick="confirmSubscriptionUpgrade()" class="w-full py-3.5 bg-apple-coral hover:bg-apple-coral-hover text-white font-bold rounded-full shadow-md transition-all text-xs flex items-center justify-center gap-2">
          <span class="material-symbols-outlined text-[18px]">verified</span>
          <span>ยืนยันการชำระเงิน (อัปเกรดทันที)</span>
        </button>
      </div>
    </div>
  </div>

  <!-- ======================================================== -->
  <!-- MODAL: ADMIN EDIT USER QUOTA & PLAN                      -->
  <!-- ======================================================== -->
  <div id="adminEditModal" class="hidden fixed inset-0 z-50 overflow-y-auto bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white max-w-md w-full rounded-3xl shadow-2xl border border-black/[0.08] overflow-hidden">
      <div class="p-5 border-b border-black/[0.06] flex items-center justify-between bg-apple-subtle">
        <h3 class="font-bold text-sm text-apple-space flex items-center gap-1.5">
          <span class="material-symbols-outlined text-apple-coral text-[20px]">manage_accounts</span>
          <span>จัดการข้อมูลสมาชิก</span>
        </h3>
        <button onclick="document.getElementById('adminEditModal').classList.add('hidden')" class="p-1 rounded-full text-apple-titanium hover:text-apple-space">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>
      <form onsubmit="handleAdminUpdateSubmit(event)" class="p-6 space-y-4 text-xs font-thai">
        <input type="hidden" id="adminEditUserId"/>
        <div>
          <label class="block font-bold text-apple-space mb-1">สมาชิก</label>
          <input id="adminEditUserName" type="text" class="w-full px-3 py-2 bg-stone-100 border border-black/[0.06] rounded-xl text-apple-titanium text-xs cursor-not-allowed" readonly />
        </div>
        <div>
          <label class="block font-bold text-apple-space mb-1">แพ็กเกจ (Plan)</label>
          <select id="adminEditPlan" class="w-full px-3 py-2 bg-apple-subtle border border-black/[0.06] rounded-xl outline-none focus:border-apple-coral text-xs">
            <option value="trial">Pro Trial (ทดลอง 7 วัน)</option>
            <option value="monthly">Pro Monthly (รายเดือน)</option>
            <option value="annual">Pro Annual (รายปี)</option>
            <option value="lifetime">Lifetime VIP (ตลอดชีพ)</option>
          </select>
        </div>
        <div>
          <label class="block font-bold text-apple-space mb-1">สถานะบัญชี</label>
          <select id="adminEditStatus" class="w-full px-3 py-2 bg-apple-subtle border border-black/[0.06] rounded-xl outline-none focus:border-apple-coral text-xs">
            <option value="active">Active (ใช้งานปกติ)</option>
            <option value="expired">Expired (หมดอายุ)</option>
            <option value="suspended">Suspended (ระงับชั่วคราว)</option>
          </select>
        </div>
        <div>
          <label class="block font-bold text-apple-space mb-1">เติมโควตาคำ AI เพิ่มเติม (+คำ)</label>
          <input id="adminEditQuotaAdd" type="number" step="10000" placeholder="เช่น 100000" class="w-full px-3 py-2 bg-apple-subtle border border-black/[0.06] rounded-xl outline-none focus:border-apple-coral text-xs" />
        </div>
        <div class="flex justify-end gap-2 pt-2 border-t border-black/[0.06]">
          <button type="button" onclick="document.getElementById('adminEditModal').classList.add('hidden')" class="px-4 py-2 font-bold text-apple-titanium hover:text-apple-space">ยกเลิก</button>
          <button type="submit" class="px-5 py-2 bg-apple-coral hover:bg-apple-coral-hover text-white font-bold rounded-full shadow-xs">บันทึกการเปลี่ยนแปลง</button>
        </div>
      </form>
    </div>
  </div>

  
  <!-- ======================================================== -->
  <!-- MODAL: PUBLISH & AUTO-SCHEDULE MODAL                     -->
  <!-- ======================================================== -->
  <div id="publishModal" class="hidden fixed inset-0 z-50 overflow-y-auto bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white max-w-lg w-full rounded-3xl shadow-2xl border border-black/[0.08] overflow-hidden">
      
      <!-- Modal Header -->
      <div class="p-5 border-b border-black/[0.06] flex items-center justify-between bg-apple-subtle">
        <div>
          <span class="text-[10px] font-bold text-teal-700 uppercase">ReadAWrite Cloud Scheduler</span>
          <h3 class="text-base font-extrabold text-apple-space" id="publishModalTitle">ซิงค์ส่งขึ้น ReadAWrite &amp; ตั้งเวลาอัตโนมัติ</h3>
        </div>
        <button onclick="document.getElementById('publishModal').classList.add('hidden')" class="p-1 rounded-full text-apple-titanium hover:text-apple-space">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>

      <div class="p-6 space-y-5 text-xs font-thai">
        <!-- Target Chapter Info -->
        <div class="bg-apple-subtle p-3.5 rounded-2xl border border-black/[0.04]">
          <div class="font-bold text-apple-space text-sm" id="publishModalChapterName">บทที่ 2: สี่ปีแห่งการเริ่มต้นใหม่</div>
          <div class="text-[11px] text-apple-titanium mt-0.5">เชื่อมต่อบัญชี: <strong class="text-teal-700 font-bold">i_Am_Status (🟢 คลาวด์พร้อมซิงค์)</strong></div>
        </div>

        <!-- Mode Selection Tabs -->
        <div>
          <label class="block font-bold text-apple-space mb-2">เลือกรูปแบบการเผยแพร่</label>
          <div class="grid grid-cols-3 gap-2">
            <button type="button" id="pubModeDraft" onclick="selectPublishMode('draft')" class="p-3 rounded-2xl border-2 border-transparent bg-apple-subtle hover:bg-stone-200/60 text-left transition-all">
              <span class="material-symbols-outlined text-stone-600 text-[20px] block mb-1">drafts</span>
              <span class="font-bold block text-apple-space text-xs">แบบร่าง</span>
              <span class="text-[10px] text-apple-titanium">รอตรวจทานในเว็บ</span>
            </button>
            <button type="button" id="pubModePublish" onclick="selectPublishMode('publish')" class="p-3 rounded-2xl border-2 border-transparent bg-apple-subtle hover:bg-stone-200/60 text-left transition-all">
              <span class="material-symbols-outlined text-emerald-600 text-[20px] block mb-1">public</span>
              <span class="font-bold block text-apple-space text-xs">เผยแพร่ทันที</span>
              <span class="text-[10px] text-apple-titanium">ออนไลน์ให้อ่านทันที</span>
            </button>
            <button type="button" id="pubModeSchedule" onclick="selectPublishMode('schedule')" class="p-3 rounded-2xl border-2 border-teal-600 bg-teal-50 text-left transition-all">
              <span class="material-symbols-outlined text-teal-700 text-[20px] block mb-1">schedule</span>
              <span class="font-bold block text-teal-800 text-xs">⏰ ตั้งเวลาออโต้</span>
              <span class="text-[10px] text-teal-700">ปล่อยตามวันเวลา</span>
            </button>
          </div>
        </div>

        <!-- Schedule Options Area (Visible when mode == 'schedule') -->
        <div id="scheduleOptionsContainer" class="bg-teal-50/60 p-4 rounded-2xl border border-teal-200 space-y-3">
          <div class="font-bold text-teal-900 flex items-center gap-1.5 text-xs">
            <span class="material-symbols-outlined text-teal-700 text-[18px]">event</span>
            <span>กำหนดวันและเวลาที่จะให้ระบบเผยแพร่อัตโนมัติ</span>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-[11px] font-bold text-apple-space mb-1">วันที่ (Date)</label>
              <input id="schedDateInput" type="date" class="w-full px-3 py-2 bg-white border border-teal-200 rounded-xl outline-none text-xs" />
            </div>
            <div>
              <label class="block text-[11px] font-bold text-apple-space mb-1">เวลา (Time)</label>
              <input id="schedTimeInput" type="time" value="18:00" class="w-full px-3 py-2 bg-white border border-teal-200 rounded-xl outline-none text-xs" />
            </div>
          </div>

          <!-- Prime Time Quick Buttons -->
          <div>
            <span class="block text-[10px] font-bold text-teal-800 mb-1.5">⚡ ช่วงเวลายอดนิยมของนักอ่านนิยาย (Prime Time):</span>
            <div class="flex flex-wrap gap-1.5">
              <button type="button" onclick="setQuickTime('18:00')" class="px-2.5 py-1 bg-white hover:bg-teal-100 border border-teal-200 rounded-lg text-[10px] font-bold text-teal-800">18:00 น. (เลิกงาน)</button>
              <button type="button" onclick="setQuickTime('19:30')" class="px-2.5 py-1 bg-white hover:bg-teal-100 border border-teal-200 rounded-lg text-[10px] font-bold text-teal-800">19:30 น. (พีคสุด)</button>
              <button type="button" onclick="setQuickTime('20:00')" class="px-2.5 py-1 bg-white hover:bg-teal-100 border border-teal-200 rounded-lg text-[10px] font-bold text-teal-800">20:00 น. (ค่ำ)</button>
              <button type="button" onclick="setQuickTime('21:00')" class="px-2.5 py-1 bg-white hover:bg-teal-100 border border-teal-200 rounded-lg text-[10px] font-bold text-teal-800">21:00 น. (ก่อนนอน)</button>
            </div>
          </div>

          <p class="text-[10px] text-teal-700 leading-relaxed font-thai border-t border-teal-200/70 pt-2">
            💡 <strong>การทำงานอัตโนมัติ:</strong> เมื่อกดส่ง ระบบจะสั่ง Playwright นำเนื้อหาไปตั้งเวลาบนเซิร์ฟเวอร์ของ ReadAWrite.com ทันที เมื่อถึงเวลานัดหมาย ระบบ ReadAWrite จะปล่อยบทความให้อ่านอัตโนมัติ <strong>โดยที่คุณปิดคอมพิวเตอร์และเข้านอนได้เลย!</strong>
          </p>
        </div>

        <button onclick="confirmPublishToReadAWrite()" class="w-full py-3.5 bg-teal-700 hover:bg-teal-800 text-white font-bold rounded-full shadow-md transition-all text-xs flex items-center justify-center gap-1.5">
          <span class="material-symbols-outlined text-[18px]">cloud_upload</span>
          <span id="confirmPublishBtnText">⏰ ยืนยันการตั้งเวลาเผยแพร่อัตโนมัติ</span>
        </button>
      </div>

    </div>
  </div>

  <!-- Toast Notification Container -->
  <div id="toastContainer" class="fixed bottom-5 right-5 z-50 flex flex-col gap-2"></div>

  <!-- ======================================================== -->
  <!-- CLIENT JAVASCRIPT: AUTHENTICATION, ROUTING & LIVE APIS   -->
  <!-- ======================================================== -->
  <script>
    const state = {
      currentUser: null,
      token: localStorage.getItem('raw_auth_token') || '',
      currentView: 'home',
      novels: [],
      activeNovel: null,
      activeChapter: null,
      selectedPlanForUpgrade: 'monthly'
    };

    function showToast(msg, type = 'info') {
      const container = document.getElementById('toastContainer');
      const t = document.createElement('div');
      const bg = type === 'success' ? 'bg-teal-700 text-white' : type === 'error' ? 'bg-rose-600 text-white' : 'bg-apple-space text-white';
      t.className = `${bg} px-4 py-3 rounded-2xl shadow-xl text-xs font-semibold flex items-center gap-2 transform transition-all duration-300`;
      t.innerHTML = `<span>${msg}</span>`;
      container.appendChild(t);
      setTimeout(() => {
        t.style.opacity = '0';
        setTimeout(() => t.remove(), 300);
      }, 4000);
    }

    async function initAuth() {
      if (!state.token) {
        renderGuestMode();
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
          renderAuthenticatedMode(data.user);
          navigate('novels');
        } else {
          localStorage.removeItem('raw_auth_token');
          state.token = '';
          state.currentUser = null;
          renderGuestMode();
          navigate('home');
        }
      } catch (err) {
        renderGuestMode();
        navigate('home');
      }
    }

    // --- Strict Visibility Rules for Guest Mode ---
    function renderGuestMode() {
      const nav = document.getElementById('mainNav');
      const authArea = document.getElementById('navAuthArea');

      // Guest Navigation Links ONLY: [หน้าแรก], [ฟีเจอร์เด่น], [ราคา & สมาชิก], [คำถามที่พบบ่อย]
      // NEVER show จัดการนิยาย, ห้องแต่งนิยาย, หรือ Admin HQ to guests!
      nav.innerHTML = `
        <a href="#hero" onclick="navigate('home')" class="text-apple-coral font-bold hover:text-apple-coral transition-colors">หน้าแรก</a>
        <a href="#features" class="hover:text-apple-space transition-colors">ฟีเจอร์เด่น</a>
        <a href="#pricing" class="hover:text-apple-space transition-colors">ราคา &amp; สมาชิก</a>
        <a href="#faq" class="hover:text-apple-space transition-colors">คำถามที่พบบ่อย</a>
      `;

      // Guest Actions ONLY: [เข้าสู่ระบบ], [ทดลองใช้ฟรี 7 วัน]
      authArea.innerHTML = `
        <button onclick="openAuthModal('login')" class="text-xs font-bold text-apple-titanium hover:text-apple-space px-2 py-1 transition-colors">
          เข้าสู่ระบบ
        </button>
        <button onclick="openAuthModal('register')" class="inline-flex items-center gap-1 bg-apple-coral hover:bg-apple-coral-hover text-white rounded-full px-4 sm:px-5 py-1.5 text-xs font-bold shadow-xs transition-all hover:scale-[1.02] active:scale-[0.98]">
          <span>ทดลองใช้ฟรี 7 วัน</span>
          <span class="material-symbols-outlined text-[15px]">arrow_forward</span>
        </button>
      `;
    }

    // --- Strict Visibility Rules for Authenticated User Mode ---
    function renderAuthenticatedMode(user) {
      const nav = document.getElementById('mainNav');
      const authArea = document.getElementById('navAuthArea');
      const remainingQuota = user.quota_limit - user.quota_used;
      const trialDays = user.trial_days_left !== undefined ? user.trial_days_left : 7;

      // Authenticated Links: [หน้าแรก], [นิยายของฉัน], [ห้องแต่งนิยาย], [ราคา & แพ็กเกจ]
      // + [Admin HQ] ONLY if user.role === 'admin'
      let adminHtml = '';
      if (user.role === 'admin') {
        adminHtml = `
          <button onclick="navigate('admin')" class="px-2.5 py-1 rounded-full text-xs font-bold text-amber-800 bg-amber-100 hover:bg-amber-200 border border-amber-300 flex items-center gap-1 transition-all">
            <span class="material-symbols-outlined text-[14px]">shield_person</span>
            <span>จัดการระบบ (Admin HQ)</span>
          </button>
        `;
      }

      nav.innerHTML = `
        <button onclick="navigate('home')" class="hover:text-apple-space transition-colors">หน้าแรก</button>
        <button onclick="navigate('novels')" class="text-apple-coral font-bold hover:text-apple-coral flex items-center gap-1 transition-colors">
          <span class="material-symbols-outlined text-[16px]">auto_stories</span>
          <span>นิยายของฉัน</span>
        </button>
        <button onclick="navigate('studio')" class="hover:text-apple-space flex items-center gap-1 transition-colors">
          <span class="material-symbols-outlined text-[16px]">edit_square</span>
          <span>ห้องแต่งนิยาย (Studio)</span>
        </button>
        <button onclick="openCheckoutModal('monthly')" class="hover:text-apple-space flex items-center gap-1 transition-colors">
          <span class="material-symbols-outlined text-[16px]">diamond</span>
          <span>ราคา &amp; แพ็กเกจ</span>
        </button>
        ${adminHtml}
      `;

      // Authenticated Right Actions: Quota Chip, Trial Pill, Pen Name & Logout
      authArea.innerHTML = `
        <div class="hidden sm:flex items-center gap-1.5 bg-orange-50 text-apple-coral border border-orange-200 px-3 py-1 rounded-full text-xs font-bold">
          <span class="material-symbols-outlined text-[15px]">bolt</span>
          <span>โควตา: ${remainingQuota.toLocaleString()} คำ</span>
        </div>
        <div class="hidden lg:flex items-center gap-1.5 bg-apple-subtle text-apple-space px-3 py-1 rounded-full text-xs font-semibold">
          <span class="material-symbols-outlined text-[15px]">timer</span>
          <span>${user.plan === 'lifetime' ? 'ตลอดชีพ' : `เหลือ ${trialDays} วัน`}</span>
        </div>
        <div class="flex items-center gap-2 pl-2 border-l border-apple-border">
          <div class="w-7 h-7 rounded-full bg-apple-coral text-white font-bold flex items-center justify-center text-xs shadow-xs">
            ${user.pen_name ? user.pen_name.charAt(0) : 'U'}
          </div>
          <span class="hidden xl:inline text-xs font-bold text-apple-space line-clamp-1">${user.pen_name}</span>
          <button onclick="handleLogout()" class="p-1 text-apple-titanium hover:text-rose-600 rounded-full hover:bg-stone-100 transition-colors" title="ออกจากระบบ">
            <span class="material-symbols-outlined text-[18px]">logout</span>
          </button>
        </div>
      `;
    }

    // --- Navigation & Route Guard ---
    function navigate(viewName) {
      if (['novels', 'studio', 'admin'].includes(viewName) && !state.currentUser) {
        showToast('🔒 กรุณาเข้าสู่ระบบก่อนเข้าใช้งานส่วนนี้', 'info');
        openAuthModal('login');
        return;
      }

      if (viewName === 'admin' && state.currentUser?.role !== 'admin') {
        showToast('⛔ ขออภัย หน้านี้สำหรับ Super Admin เท่านั้น', 'error');
        return;
      }

      state.currentView = viewName;
      const views = ['home', 'novels', 'studio', 'admin'];
      views.forEach(v => {
        const el = document.getElementById(`view-${v}`);
        if (el) {
          if (v === viewName) el.classList.remove('hidden');
          else el.classList.add('hidden');
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
        regTab.className = "flex-1 py-3 text-center border-b-2 border-apple-coral text-apple-coral bg-orange-50/50 font-bold";
        loginTab.className = "flex-1 py-3 text-center text-apple-titanium hover:text-apple-space font-semibold";
      } else {
        regForm.classList.add('hidden');
        loginForm.classList.remove('hidden');
        loginTab.className = "flex-1 py-3 text-center border-b-2 border-apple-coral text-apple-coral bg-orange-50/50 font-bold";
        regTab.className = "flex-1 py-3 text-center text-apple-titanium hover:text-apple-space font-semibold";
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
          renderAuthenticatedMode(data.user);
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
          renderAuthenticatedMode(data.user);
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
      renderGuestMode();
      navigate('home');
      showToast('ออกจากระบบเรียบร้อยแล้ว', 'info');
    }

    // --- Novels Management ---
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
        grid.className = "col-span-3 text-center py-20 bg-white rounded-3xl border border-dashed border-black/[0.08]";
        grid.innerHTML = `
          <div class="w-16 h-16 rounded-2xl bg-orange-50 text-apple-coral flex items-center justify-center mx-auto mb-4">
            <span class="material-symbols-outlined text-[36px]">auto_stories</span>
          </div>
          <h3 class="text-xl font-bold text-apple-space">ยินดีต้อนรับสู่อาณาจักรนิยายของคุณ!</h3>
          <p class="text-xs text-apple-titanium max-w-md mx-auto mt-1 mb-6 font-thai">คุณยังไม่มีนิยายในระบบ เริ่มต้นสร้างผลงานชิ้นแรกของคุณเพื่อปลดล็อกพลัง AI แต่งนิยายได้ทันที</p>
          <button onclick="openCreateNovelModal()" class="px-6 py-3 bg-apple-coral hover:bg-apple-coral-hover text-white text-xs font-bold rounded-full shadow-xs transition-all inline-flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[18px]">add_circle</span>
            <span>+ สร้างนิยายเรื่องแรกของคุณ</span>
          </button>
        `;
        return;
      }

      grid.className = "grid grid-cols-1 md:grid-cols-3 gap-6";
      grid.innerHTML = novels.map(n => `
        <div class="bg-white rounded-3xl border border-black/[0.06] shadow-xs hover:shadow-md transition-all overflow-hidden flex flex-col justify-between bento-card-hover">
          <div>
            <div class="h-44 w-full overflow-hidden relative bg-stone-100">
              <img src="${n.cover_url || 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&q=80'}" class="w-full h-full object-cover" />
              <span class="absolute top-3 right-3 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-teal-700 text-white">
                ${n.status}
              </span>
              <span class="absolute bottom-3 left-3 px-2 py-0.5 rounded text-[10px] font-bold bg-black/60 text-white">
                ${n.category}
              </span>
            </div>
            <div class="p-5">
              <h3 class="text-base font-bold text-apple-space line-clamp-1">${n.title}</h3>
              <p class="text-xs text-apple-coral font-medium mt-0.5">${n.genre}</p>
              <p class="text-xs text-apple-titanium mt-2 line-clamp-2 font-thai leading-relaxed">${n.synopsis || 'ไม่มีเรื่องย่อ'}</p>
              <div class="flex items-center gap-3 mt-4 text-[11px] text-apple-titanium border-t border-black/[0.04] pt-3">
                <span>📝 ${n.chapters_count || 1} ตอน</span>
                <span>📊 ${Number(n.words_total || 0).toLocaleString()} คำ</span>
              </div>
            </div>
          </div>
          <div class="p-5 pt-0">
            <button onclick="openNovelInStudio('${n.id}')" class="w-full py-2.5 bg-apple-coral hover:bg-apple-coral-hover text-white text-xs font-bold rounded-full transition-all flex items-center justify-center gap-1 shadow-xs">
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

    // --- Studio Logic ---
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
        <button onclick="selectChapter(${c.chapter_num})" class="w-full text-left p-2.5 rounded-xl border ${state.activeChapter?.chapter_num === c.chapter_num ? 'bg-orange-50 border-apple-coral text-apple-coral font-bold' : 'border-transparent hover:bg-stone-50 text-apple-space'} transition-all flex items-center justify-between">
          <div class="truncate">
            <div class="text-xs truncate">บทที่ ${c.chapter_num}: ${c.subtitle}</div>
            <div class="text-[10px] text-apple-titanium font-normal">${Number(c.word_count).toLocaleString()} คำ • ${c.status}</div>
          </div>
          <span class="material-symbols-outlined text-[16px] text-apple-titanium">chevron_right</span>
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
        manuscript.innerHTML = `<div class="p-8 text-center text-apple-titanium"><p>ยังไม่มีเนื้อหาในบทนี้</p><p class="text-xs mt-1">คลิกปุ่ม <strong>"✨ แต่งบทนี้ทันทีด้วย AI"</strong> ทางซ้ายเพื่อเริ่มแต่ง</p></div>`;
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

      showToast(`⏳ Gemini AI กำลังแต่งบทที่ ${state.activeChapter.chapter_num} (~${targetWords.toLocaleString()} คำ)...`, 'info');
      manuscript.innerHTML = `
        <div class="p-12 text-center text-apple-coral animate-pulse">
          <span class="material-symbols-outlined text-[40px] mb-2">auto_awesome</span>
          <div class="font-bold text-base">กำลังแต่งเนื้อหาบทที่ ${state.activeChapter.chapter_num}...</div>
          <div class="text-xs text-apple-titanium mt-1">ใช้เวลาประมวลผลประมาณ 15-20 วินาที ด้วย Gemini 3.5 Flash Lite</div>
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
          
          const paras = data.text.split('\n\n').filter(p => p.trim().length > 0);
          manuscript.innerHTML = paras.map(p => `<p class="indent-8">${p.replace(/\n/g, '<br/>')}</p>`).join('');
          
          document.getElementById('editorChapterStats').innerText = `${data.word_count.toLocaleString()} คำ • สถานะ: draft`;
          document.getElementById('realtimeWordsCounter').innerText = `📊 ${data.word_count.toLocaleString()} คำ`;

          if (state.currentUser) {
            state.currentUser.quota_used = data.quota_used;
            renderAuthenticatedMode(state.currentUser);
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
      showToast('🔍 ProofAI กำลังเกลาสำนวน...', 'info');
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

    let currentPublishMode = 'schedule';

    function openPublishModal() {
      if (!state.activeChapter?.content) {
        showToast('ยังไม่มีเนื้อหาที่จะส่ง กรุณาแต่งนิยายก่อน', 'error');
        return;
      }
      document.getElementById('publishModalChapterName').innerText = `บทที่ ${state.activeChapter.chapter_num}: ${state.activeChapter.subtitle} (${Number(state.activeChapter.word_count).toLocaleString()} คำ)`;
      
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      const dateStr = tomorrow.toISOString().split('T')[0];
      document.getElementById('schedDateInput').value = dateStr;

      selectPublishMode('schedule');
      document.getElementById('publishModal').classList.remove('hidden');
    }

    function selectPublishMode(mode) {
      currentPublishMode = mode;
      const modes = ['draft', 'publish', 'schedule'];
      modes.forEach(m => {
        const btn = document.getElementById('pubMode' + m.charAt(0).toUpperCase() + m.slice(1));
        if (m === mode) {
          btn.className = 'p-3 rounded-2xl border-2 border-teal-600 bg-teal-50 text-left transition-all';
        } else {
          btn.className = 'p-3 rounded-2xl border-2 border-transparent bg-apple-subtle hover:bg-stone-200/60 text-left transition-all';
        }
      });

      const schedContainer = document.getElementById('scheduleOptionsContainer');
      const btnText = document.getElementById('confirmPublishBtnText');
      if (mode === 'schedule') {
        schedContainer.classList.remove('hidden');
        btnText.innerText = '⏰ ยืนยันการตั้งเวลาเผยแพร่อัตโนมัติ';
      } else if (mode === 'publish') {
        schedContainer.classList.add('hidden');
        btnText.innerText = '🚀 ยืนยันการเผยแพร่ทันที';
      } else {
        schedContainer.classList.add('hidden');
        btnText.innerText = '📁 ยืนยันการบันทึกเป็นแบบร่าง';
      }
    }

    function setQuickTime(t) {
      document.getElementById('schedTimeInput').value = t;
    }

    async function confirmPublishToReadAWrite() {
      const d = document.getElementById('schedDateInput').value;
      const t = document.getElementById('schedTimeInput').value;
      const scheduleTime = `${d} ${t}`;

      showToast(currentPublishMode === 'schedule' ? `⏰ กำลังตั้งเวลาเผยแพร่บน ReadAWrite (${scheduleTime})...` : `🚀 กำลังส่งขึ้น ReadAWrite...`, 'info');
      document.getElementById('publishModal').classList.add('hidden');

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
            publish_mode: currentPublishMode,
            schedule_time: scheduleTime
          })
        });
        const data = await res.json();
        if (data.success) {
          showToast(data.message, 'success');
          if (currentPublishMode === 'schedule') {
            state.activeChapter.status = `ตั้งเวลา ${t} น.`;
          } else if (currentPublishMode === 'publish') {
            state.activeChapter.status = 'เผยแพร่แล้ว';
          }
          renderStudioChapters(state.activeNovel.chapters);
        } else {
          showToast(data.error || 'ซิงค์ไม่สำเร็จ', 'error');
        }
      } catch (e) {
        showToast('การเชื่อมต่อล้มเหลว: ' + e.message, 'error');
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

    // --- Subscription Checkout ---
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
          renderAuthenticatedMode(data.user);
          document.getElementById('checkoutModal').classList.add('hidden');
          showToast(data.message, 'success');
        } else {
          showToast(data.error || 'ชำระเงินไม่สำเร็จ', 'error');
        }
      } catch (e) {
        showToast('การเชื่อมต่อล้มเหลว', 'error');
      }
    }

    // --- Super Admin HQ ---
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
        <tr class="hover:bg-apple-subtle">
          <td class="p-3.5">
            <span class="font-bold text-apple-space">${u.pen_name}</span>
            <div class="text-[10px] text-apple-titanium font-mono">ID #${u.id} • ${u.created_at.split('T')[0]}</div>
          </td>
          <td class="p-3.5 text-apple-titanium">${u.email}</td>
          <td class="p-3.5">
            <span class="px-2 py-0.5 rounded-full font-bold uppercase text-[10px] ${u.role === 'admin' ? 'bg-amber-100 text-amber-800' : 'bg-stone-100 text-stone-700'}">${u.role}</span>
          </td>
          <td class="p-3.5">
            <span class="px-2.5 py-0.5 rounded-full font-semibold text-[11px] ${u.plan === 'lifetime' ? 'bg-amber-100 text-amber-800 font-bold' : u.plan === 'annual' ? 'bg-orange-100 text-apple-coral font-bold' : 'bg-stone-100 text-stone-700'}">${u.plan}</span>
          </td>
          <td class="p-3.5">
            <span class="font-bold text-[11px] ${u.status === 'active' ? 'text-teal-700' : 'text-rose-600'}">${u.status}</span>
          </td>
          <td class="p-3.5">
            <span class="font-bold text-[11px]">${Number(u.quota_used).toLocaleString()} / ${Number(u.quota_limit).toLocaleString()} คำ</span>
            <div class="w-24 bg-stone-200 h-1 rounded-full mt-1 overflow-hidden">
              <div class="bg-apple-coral h-1 rounded-full" style="width: ${Math.min(100, Math.round((u.quota_used/u.quota_limit)*100))}%"></div>
            </div>
          </td>
          <td class="p-3.5 text-right">
            <button onclick="openAdminEditModal(${u.id})" class="px-3 py-1 bg-white hover:bg-stone-100 border border-black/[0.08] rounded-full text-apple-coral font-bold shadow-xs">
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

    window.addEventListener('DOMContentLoaded', () => {
      const slider = document.getElementById('targetWordsSlider');
      if (slider) {
        slider.addEventListener('input', (e) => {
          document.getElementById('targetWordsDisplay').innerText = `${Number(e.target.value).toLocaleString()} คำ`;
        });
      }
      initAuth();
    });
  </script>
</body>
</html>
'''

INDEX_PATH = r"c:\ReadAWrite\web_saas_stitch\index.html"

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Successfully integrated Apple Theme with strict Navbar visibility into: {INDEX_PATH}")
