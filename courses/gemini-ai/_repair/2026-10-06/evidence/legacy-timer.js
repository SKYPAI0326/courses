
window.addEventListener('scroll', () => {
  const total = document.body.scrollHeight - window.innerHeight;
  document.getElementById('prog').style.width = (window.scrollY / total * 100) + '%';
});

const CHALLENGES = [
  { type: '計算工具', title: '員工績效獎金試算機', desc: '輸入底薪、績效分數（A/B/C/D）、加班時數，自動計算應領獎金與稅後金額。' },
  { type: '邏輯工具', title: '會議室預訂衝突偵測器', desc: '輸入多個預訂時段（開始時間 + 結束時間），自動偵測衝突並標示出來。' },
  { type: '視覺工具', title: '月度費用環圓圖', desc: '輸入各項費用名稱與金額，生成一個 SVG 環形圓圖，顯示各項費用佔比。' },
  { type: '計算工具', title: '出差費用報銷計算器', desc: '輸入交通、住宿、餐費、其他，依公司報銷規則（設定每項上限）計算可核銷金額。' },
  { type: '生成工具', title: '週報自動格式化工具', desc: '填入本週完成事項、進行中事項、待解決問題，自動生成符合公司格式的週報文字。' },
  { type: '視覺工具', title: '目標達成率儀表板', desc: '輸入 Q1 目標值與實際值（3–5 個指標），生成一個帶有達成率比較的直條圖。' },
  { type: '邏輯工具', title: '專案風險評估矩陣', desc: '輸入風險項目名稱、發生機率（高/中/低）、影響程度（高/中/低），自動生成 3×3 風險矩陣表。' },
  { type: '計算工具', title: '電商利潤試算機', desc: '輸入商品售價、成本、平台抽成比例、廣告費，自動計算每單淨利和利潤率。' },
  { type: '生成工具', title: '客戶提案前情境備忘卡', desc: '填入客戶名稱、本次會議目的、客戶痛點、我們的解決方案，生成一張可帶入會議室的提案備忘卡。' },
  { type: '視覺工具', title: '學習進度追蹤儀表板', desc: '輸入你想學習的技能名稱、目標學習天數、已學習天數，生成一個視覺化的學習進度追蹤板。' },
  { type: '邏輯工具', title: '人力排班最佳化工具', desc: '輸入員工名稱和可上班日（勾選），以及每天最少需要人數，自動生成一週排班建議。' },
  { type: '計算工具', title: '廣告 ROI 計算器', desc: '輸入廣告投放金額、產生的訂單數、平均客單價，自動計算 ROAS、ROI 及每單獲客成本。' },
  { type: '邏輯工具', title: '公文限辦期限追蹤器', desc: '輸入多筆公文的收文日期與限辦天數，自動計算剩餘天數，並以綠／黃／紅標示是否即將逾期。' },
  { type: '計算工具', title: '活動預算核銷試算機', desc: '輸入各費用項目與金額、活動預算上限，自動計算預算執行率，超過 90% 時顯示警示。' },
];

let currentIdx = Math.floor(Math.random() * CHALLENGES.length);
let timerInterval = null;
let timeLeft = 20 * 60;
let isRunning = false;
const TOTAL = 20 * 60;
const doneRecords = [];

function showChallenge(idx) {
  const c = CHALLENGES[idx];
  document.getElementById('challenge-type').textContent = c.type;
  document.getElementById('challenge-title').textContent = c.title;
  document.getElementById('challenge-desc').textContent = c.desc;
}

function rollChallenge() {
  let newIdx;
  do { newIdx = Math.floor(Math.random() * CHALLENGES.length); } while (newIdx === currentIdx && CHALLENGES.length > 1);
  currentIdx = newIdx;
  showChallenge(currentIdx);
}

function updateTimerDisplay() {
  const m = Math.floor(timeLeft / 60);
  const s = timeLeft % 60;
  const el = document.getElementById('timer-display');
  el.textContent = `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
  el.className = 'timer-display' + (timeLeft <= 300 && timeLeft > 60 ? ' warning' : '') + (timeLeft <= 60 ? ' urgent' : '');
  document.getElementById('timer-fill').style.width = (timeLeft / TOTAL * 100) + '%';
}

function toggleTimer() {
  if (isRunning) {
    clearInterval(timerInterval);
    isRunning = false;
    document.getElementById('start-btn').textContent = '繼續計時';
  } else {
    if (timeLeft === 0) return;
    isRunning = true;
    document.getElementById('start-btn').textContent = '暫停';
    timerInterval = setInterval(() => {
      timeLeft--;
      updateTimerDisplay();
      if (timeLeft === 0) {
        clearInterval(timerInterval);
        isRunning = false;
        document.getElementById('start-btn').textContent = '開始計時';
        const c = CHALLENGES[currentIdx];
        doneRecords.push({ verified: false, title: c.title, time: new Date().toLocaleTimeString('zh-TW', {hour:'2-digit',minute:'2-digit'}) });
        renderDoneList();
        alert(`時間到！\n\n挑戰「${c.title}」完成了嗎？\n記得把你做的工具存到工具庫！`);
      }
    }, 1000);
  }
}

function resetTimer() {
  clearInterval(timerInterval);
  isRunning = false;
  timeLeft = TOTAL;
  document.getElementById('start-btn').textContent = '開始計時';
  updateTimerDisplay();
}

function renderDoneList() {
  const wrap = document.getElementById('done-record');
  const list = document.getElementById('done-list');
  if (doneRecords.length === 0) { wrap.style.display = 'none'; return; }
  wrap.style.display = 'block';
  list.innerHTML = doneRecords.map(r =>
    `<div class="done-item"><span class="done-icon">•</span><span>${r.title}</span><span class="done-time">${r.time}</span></div>`
  ).join('');
}

function copyInstructions() {
  const text = document.getElementById('instruction-box').textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = event.target;
    btn.textContent = '已複製！';
    setTimeout(() => btn.textContent = '複製指令', 1800);
  });
}

showChallenge(currentIdx);
updateTimerDisplay();
