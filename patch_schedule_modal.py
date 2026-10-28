# -*- coding: utf-8 -*-
"""
Script to inject Publish & Auto-Schedule Modal into build_apple_saas.py
"""

with open(r'c:\ReadAWrite\build_apple_saas.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace Studio button
old_btn = '<button id="btnSync" onclick="triggerReadAWriteSync()"'
new_btn = '<button id="btnSync" onclick="openPublishModal()"'
text = text.replace(old_btn, new_btn)

old_btn_text = '<span>🚀 ซิงค์ส่งขึ้น ReadAWrite</span>'
new_btn_text = '<span>🚀 ซิงค์ส่ง &amp; ตั้งเวลาเผยแพร่ออโต้</span>'
text = text.replace(old_btn_text, new_btn_text)

# 2. Add publish modal HTML
publish_modal_html = """
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
"""

target_toast = '<!-- Toast Notification Container -->'
text = text.replace(target_toast, publish_modal_html + '\n  ' + target_toast)

# 3. Add JavaScript logic
old_js_sync = """    async function triggerReadAWriteSync() {
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
    }"""

new_js_sync = """    let currentPublishMode = 'schedule';

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
    }"""

text = text.replace(old_js_sync, new_js_sync)

with open(r'c:\ReadAWrite\build_apple_saas.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Successfully patched build_apple_saas.py!')
