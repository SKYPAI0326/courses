---
slug: uiux-designer
unit_id: B8-web-git-deploy
title: 把設計做成網站，留下版本與公開網址
course_type: programming
duration: 13h
prerequisites: [B7-figma-handoff-export]
revision: 2026-10-09
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: 官方檔案 2026-10-09 查證；實際帳號與桌面軟體另記平台證據
---

## 內部設計（不進學員頁）

本課新增能力：從完整可執行程式理解與修改網站，實作獨立Git基準／差異／遠端與公開部署更新。依 `_design/COURSE-BLUEPRINT.md` 的同檔案整合路徑；保留 99h 行政配置，未以真人試跑鎖定分鐘。

| 活動 | 素材／產物 | 操作與決策 | 認知工作／支援 |
|---|---|---|---|
| Demo | 正文提供的完整輸入／方法示範 | 講師建模本課首次方法與可見結果 | 完整理由及步驟 |
| Together | 同一工作室任務清單／學員自己的完成物 | 正文「跟著做」需自行選層、設定與判斷 | 支援遞減，自己定位欄位、解釋檢查結果 |
| Solo | 本課不同條件／修正後完成物 | 正文「自己完成」依新限制選擇方法 | 獨立診斷與遷移，依完成條件判斷 |

素材：正式正文的可複製資料、每課 START-HERE、完成檢查表、共用視覺參考，B7 有 PSD，B8 有下載 ZIP。素材存在／版本由驗證紀錄確認，不以本段自填 PASS。

<!-- learner-content:start -->
# 把設計做成網站，留下版本與公開網址

你會拿到完整可下載專案，先理解HTML、CSS、JavaScript的分工，再在自己的資料夾修改和驗證。完成Git兩筆版本、GitHub遠端與Pages部署後，交出別人能開啟、能操作、看得見更新的網站。

## 開始前，先找到材料與起點

先能說出第15堂交付包的主要色與Button高48，並找到自己透明PNG。如果不會找檔案與副檔名，先按下一節逐步下載解壓。Git／GitHub從零開始，本堂提供安裝檢查與第一筆commit。

先開啟[本堂起始材料（HTML）](../../courses/uiux-designer/assets/B8-web-git-deploy/START-HERE.html)，讀取輸入與圖層名稱；操作在你的 Figma 檔或本堂指定工具完成。完成後到[本堂完成檢查表（可儲存／下載）](../../courses/uiux-designer/assets/B8-web-git-deploy/reference/EXPECTED-CHECK.html)記錄實際結果。

## 下載與開啟：先完成本機成功路徑

下載[studio-tasks-web.zip（HTML／CSS／JS與PNG完整專案）](../../courses/uiux-designer/assets/shared/studio-tasks-web.zip)，解壓縮後要看到 `studio-tasks-web` 資料夾。還沒下載也可先看[完整網站參考](../../courses/uiux-designer/web-starter/index.html)，但請在自己的解壓資料夾修改，不改教師網站。

1. 用檔案總管／Finder確認資料夾裡有index.html、styles.css、app.js、README.md與assets/status-badge.png。若看到兩層同名資料夾，進到有index.html那一層。
2. 直接雙擊index.html，用Chrome或Edge開啟。此專案不用套件安裝、不需要伺服器或資料庫，所有路徑都為相對路徑；正常應先見示範登入。
3. 點登入→第一筆詳情→標記完成→取消，應仍在詳情；再確認，應到已完成清單且看見Toast與徽章。回待處理捲到底，最後一筆不被底部導覽遮住。
4. 在VS Code選File → Open Folder開啟這個資料夾。左側Explorer應看到三個程式檔及assets，開啟index.html修改，按Save後回瀏覽器Reload才會看到更新。
5. 如果HTML直接顯示程式文字，確認副檔名不是.html.txt、用瀏覽器開啟而非文字編輯器；如果Button完全沒反應，確認app.js與HTML在同層，並且script的src沒打錯。徽章破圖先檢查assets/status-badge.png與大小寫。

## 把設計對回程式，而不是憑空做另一個作品

| Figma完成物 | 網站對應 | 本課簡化範圍 |
|---|---|---|
| Primary／Text／Muted／Surface色碼 | styles.css的`:root`變數 | 色碼與前課一致 |
| Button H48、Label置中 | button樣式與padding | HTML按鈕自身包含文字 |
| List與長Row | task-list／task-card與任務資料 | 實際文字換行與動態列 |
| Detail、Confirm、List Done | detail-screen、dialog、done-tab | 確認改變記憶體內狀態 |
| Header／Bottom nav／FAB | sticky／fixed、scroll-top | 瀏覽器實際滾動，底部留160 |
| Photoshop透明徽章 | assets/status-badge.png | 來自第15堂；更換自己輸出也需同檔名／尺寸 |
| Login | login-screen的示範帳號 | 不驗證真實密碼；不用後端 |
| Swap／Smart Animate | Figma測試分支保留 | 這個最小網站不實作全部動畫與選單分支 |

網站的任務狀態只在此次頁面記憶體裡，Reload會恢復預設。你的成品說明應寫清楚這一點，不能向接手者宣稱有登入驗證或長期資料儲存。

## HTML、CSS、JavaScript各負責什麼

HTML描述內容與結構，例如 `<button id="complete-task">標記完成</button>`；CSS用選擇器決定外觀，`#complete-task`找唯一id，`.task-card`找一群相同class；JavaScript接收事件並改狀態。`document.querySelector('#confirm-dialog')`找到Dialog，`showModal()`開啟彈窗，`close()`關掉。id必須唯一且與選擇器一致，改一端不改另一端會找不到物件。

JavaScript中的tasks是資料陣列，每筆有id、title、due、done；selectedTask記住目前點哪一筆，showDone決定看待處理還是已完成。function是可重用的一段動作；renderList先依狀態篩選，再依每筆資料建立Row；addEventListener把按鈕點選和動作繫結。`textContent`更新文字、`hidden`顯示或隱藏一個畫面、`disabled`阻止已完成任務再提交。這些是本作品所需的基礎，不要求先背所有語法。

讀確認事件時，依序找四件事：目前任務done改true→關Dialog→重畫已完成清單→顯示Toast。取消只關Dialog，不改done，所以結果不同。`setTimeout`讓Toast四秒後消失；狀態仍留在列表，不靠短暫提示儲存唯一結果。

下面是完整核心程式，與下載包一致。先在自己的專案比對，再只改本堂指定條件。

範例head的canonical與og:url指向課程參考網站；部署自己的作品時將兩個網址改成你的實際Pages網址，避免搜尋與分享指到教師網站。

### index.html：內容、狀態畫面與連結

```html
<!doctype html>
<html lang="zh-TW">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>工作室待處理清單</title>
  <meta name="description" content="工作室任務示範：查看詳情、取消或確認完成，並檢查已完成狀態。">
  <meta property="og:title" content="工作室待處理清單">
  <meta property="og:description" content="查看、確認與完成工作室任務的示範網站。">
  <meta property="og:url" content="https://skypai0326.github.io/courses/courses/uiux-designer/web-starter/">
  <meta property="og:image" content="https://skypai0326.github.io/courses/素材/og-default.png">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="工作室待處理清單">
  <meta name="twitter:description" content="工作室任務與確認示範網站。">
  <link rel="canonical" href="https://skypai0326.github.io/courses/courses/uiux-designer/web-starter/">
  <style>.skip-link{position:absolute;left:-9999px}.skip-link:focus-visible{left:12px;top:12px;z-index:10;background:white;padding:12px}</style>
  <link rel="stylesheet" href="styles.css">
  <script src="app.js" defer></script>
</head>
<body>
  <a href="#main" class="skip-link">跳至主要內容</a>
  <header class="app-header"><h1>工作室任務</h1></header>
  <main id="main">
    <section id="login-screen">
      <h2>登入工作室</h2>
      <p>用示範帳號查看任務；重新整理後會回到預設資料。</p>
      <label>工作室帳號<input value="studio@example.test" readonly></label>
      <label>密碼<input type="password" value="demo-only" readonly></label>
      <button id="login-button" type="button">登入</button>
    </section>
    <section id="list-screen" hidden>
      <h2 id="list-title">待處理清單</h2>
      <div id="task-list" class="task-list"></div>
      <p id="empty-message" hidden>目前沒有這個狀態的任務。</p>
    </section>
    <section id="detail-screen" hidden>
      <button id="back-button" class="secondary" type="button">← 返回清單</button>
      <h2 id="detail-title"></h2>
      <p id="detail-due" class="muted"></p>
      <p>核對內容、期限與交付檔名後，再標記完成。</p>
      <button id="complete-task" type="button">標記完成</button>
    </section>
    <p id="feedback" class="toast" role="status" aria-live="polite"></p>
  </main>
  <nav id="bottom-nav" aria-label="任務狀態" hidden>
    <button id="pending-tab" aria-current="page" type="button">待處理</button>
    <button id="done-tab" type="button">已完成</button>
  </nav>
  <button id="scroll-top" class="floating" type="button" aria-label="回到清單頂部" hidden>↑</button>
  <dialog id="confirm-dialog" aria-labelledby="dialog-title">
    <h2 id="dialog-title">確認完成？</h2>
    <p>這筆任務將移到已完成清單。</p>
    <div class="actions">
      <button id="cancel-button" class="secondary" type="button">取消</button>
      <button id="confirm-button" type="button">確認完成</button>
    </div>
  </dialog>
</body>
</html>
```

### styles.css：共用規則與手機斷點

```css
:root {
  --primary: #245B45;
  --text: #1E293B;
  --muted: #5F6C80;
  --surface: #F5F7FA;
}
* { box-sizing: border-box; }
[hidden] { display: none !important; }
body {
  margin: 0;
  background: var(--surface);
  color: var(--text);
  font-family: "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
  font-size: 16px;
  line-height: 1.5;
}
.app-header {
  position: sticky;
  top: 0;
  z-index: 2;
  background: white;
  border-bottom: 1px solid #CBD5E1;
  padding: 16px 24px;
}
h1 { max-width: 720px; margin: auto; font-size: 24px; line-height: 32px; }
h2 { font-size: 24px; line-height: 32px; margin: 0 0 20px; }
main { max-width: 768px; margin: auto; padding: 32px 24px 160px; }
label { display: block; margin: 16px 0; }
input { width: 100%; display: block; margin-top: 8px; padding: 12px 16px; font: inherit; border: 1px solid var(--muted); border-radius: 8px; }
button { min-height: 48px; padding: 12px 16px; font: inherit; color: white; background: var(--primary); border: 1px solid var(--primary); border-radius: 8px; cursor: pointer; }
button:focus-visible, input:focus-visible { outline: 3px solid #92400E; outline-offset: 3px; }
button:disabled { background: #E2E8F0; color: var(--muted); border-color: #E2E8F0; cursor: default; }
.secondary { background: white; color: var(--text); border-color: var(--muted); }
.muted { color: var(--muted); font-size: 14px; line-height: 22px; }
.task-list { display: flex; flex-direction: column; gap: 12px; }
.task-card { background: white; padding: 16px; border-radius: 8px; border: 1px solid #CBD5E1; display: flex; gap: 16px; align-items: center; }
.task-copy { flex: 1; min-width: 0; overflow-wrap: anywhere; }
.task-copy h3 { font-size: 18px; line-height: 28px; margin: 0 0 8px; }
.task-copy p { margin: 0; }
.badge { width: 32px; height: 32px; }
#bottom-nav { position: fixed; z-index: 2; bottom: 0; left: 0; right: 0; background: white; border-top: 1px solid #CBD5E1; display: flex; justify-content: center; }
#bottom-nav button { flex: 1; max-width: 384px; min-height: 64px; background: white; color: var(--text); border: 0; border-radius: 0; }
#bottom-nav [aria-current="page"] { color: var(--primary); border-bottom: 4px solid var(--primary); font-weight: 700; }
.floating { position: fixed; bottom: 88px; right: 24px; width: 48px; padding: 0; z-index: 3; border-radius: 50%; }
.toast { position: fixed; bottom: 152px; left: 24px; right: 24px; max-width: 720px; margin: 0 auto; padding: 12px 16px; background: var(--text); color: white; border-radius: 8px; z-index: 4; }
.toast:empty { display: none; }
dialog { width: min(320px, calc(100% - 48px)); padding: 24px; border: 0; border-radius: 8px; color: var(--text); }
dialog::backdrop { background: rgba(0, 0, 0, .25); }
dialog h2 { margin-bottom: 16px; }
.actions { display: flex; gap: 12px; }
.actions button { flex: 1; padding-left: 8px; padding-right: 8px; }
@media (max-width: 560px) {
  .task-card { flex-direction: column; align-items: stretch; }
  .task-card button { width: 100%; }
  #login-button { width: 100%; }
}
@media (prefers-reduced-motion: reduce) {
  * { scroll-behavior: auto !important; }
}
```

`@media (max-width:560px)`是手機斷點：窄畫面將任務列改成上下，Button全寬。`box-sizing:border-box`讓寬度包含內距與邊框；max-width限制桌面閱讀寬；main底部160px給固定導覽、漂浮按鈕留出空間。Breakpoint來自內容需要，不是把Figma402寫成所有手機固定寬。

### app.js：資料、畫面切換與事件

```javascript
const tasks = [
  { id: 'T01', title: '整理交付包', due: '今天18:00', done: false },
  { id: 'T02', title: '確認活動報名資料並補上聯絡電話', due: '明天12:00', done: false },
  { id: 'T03', title: '更新本週任務說明', due: '星期五17:00', done: false }
];
// 增加示範任務，讓清單有足夠長度可測滾動。
for (let n = 4; n <= 15; n += 1) {
  tasks.push({ id: `T${String(n).padStart(2, '0')}`, title: `核對工作室任務${n}`, due: '本週17:00', done: false });
}
const screens = ['login-screen', 'list-screen', 'detail-screen'];
const dialog = document.querySelector('#confirm-dialog');
const feedback = document.querySelector('#feedback');
let selectedTask = null;
let showDone = false;
let toastTimer;

function showScreen(id) {
  screens.forEach(name => { document.querySelector('#' + name).hidden = name !== id; });
  document.querySelector('#bottom-nav').hidden = id === 'login-screen';
  document.querySelector('#scroll-top').hidden = id !== 'list-screen';
  window.scrollTo(0, 0);
}
function renderList() {
  const list = document.querySelector('#task-list');
  list.replaceChildren();
  const visibleTasks = tasks.filter(task => task.done === showDone);
  document.querySelector('#empty-message').hidden = visibleTasks.length !== 0;
  document.querySelector('#list-title').textContent = showDone ? '已完成清單' : '待處理清單';
  document.querySelector('#pending-tab').setAttribute('aria-current', showDone ? 'false' : 'page');
  document.querySelector('#done-tab').setAttribute('aria-current', showDone ? 'page' : 'false');
  visibleTasks.forEach(task => {
    const card = document.createElement('article'); card.className = 'task-card';
    const copy = document.createElement('div'); copy.className = 'task-copy';
    const title = document.createElement('h3'); title.textContent = task.title;
    const meta = document.createElement('p'); meta.className = 'muted';
    meta.textContent = `${task.done ? '已完成' : '待處理'} · ${task.due}`;
    copy.append(title, meta); card.append(copy);
    if (task.done) {
      const badge = document.createElement('img'); badge.className = 'badge';
      badge.src = 'assets/status-badge.png'; badge.alt = '已完成'; card.append(badge);
    }
    const open = document.createElement('button'); open.type = 'button';
    open.textContent = '檢視詳情'; open.setAttribute('aria-label', '檢視詳情：' + task.title);
    open.addEventListener('click', () => {
      selectedTask = task;
      document.querySelector('#detail-title').textContent = task.title;
      document.querySelector('#detail-due').textContent = '期限：' + task.due;
      const complete = document.querySelector('#complete-task');
      complete.disabled = task.done; complete.textContent = task.done ? '已完成' : '標記完成';
      showScreen('detail-screen');
    });
    card.append(open); list.append(card);
  });
}
function openList(done) {
  showDone = done; renderList(); showScreen('list-screen');
}
document.querySelector('#login-button').addEventListener('click', () => openList(false));
document.querySelector('#back-button').addEventListener('click', () => openList(showDone));
document.querySelector('#pending-tab').addEventListener('click', () => openList(false));
document.querySelector('#done-tab').addEventListener('click', () => openList(true));
document.querySelector('#complete-task').addEventListener('click', () => dialog.showModal());
document.querySelector('#cancel-button').addEventListener('click', () => dialog.close());
document.querySelector('#confirm-button').addEventListener('click', () => {
  if (!selectedTask || selectedTask.done) return;
  selectedTask.done = true; dialog.close(); openList(true);
  feedback.textContent = '任務已完成，已移到已完成清單。';
  clearTimeout(toastTimer); toastTimer = setTimeout(() => { feedback.textContent = ''; }, 4000);
});
dialog.addEventListener('click', event => {
  const box = dialog.getBoundingClientRect();
  if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) dialog.close();
});
document.querySelector('#scroll-top').addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
showScreen('login-screen');
```

## 跟著做：三種修改，分別驗證

1. 在HTML把標題「工作室任務」改為自己的示範工作室名稱；Save與Reload，應只有標題文字改變。
2. 在CSS把`--primary`改為第01堂你已核對對比的色碼；檢查登入、完成Button與Nav選中狀態同時更新。不要逐個Button加不同顏色。
3. 在app.js只改T02的title為更長任務：「核對本週活動報名名單並補齊聯絡電話與到場時間」。寬390與430時應換行，不蓋住檢視詳情Button；點進去仍是同一筆資料。
4. 走完整取消／確認流程，檢查已完成Tab只多該筆、待處理Tab少該筆、徽章清楚。再Reload，說明為什麼預設資料會回來。

## Git安裝與資料夾起點

Git記錄本機版本；GitHub存遠端repo；GitHub Pages把其中的靜態檔公開成網站。它們是不同步驟。先從[Git官方下載](https://git-scm.com/downloads)安裝適合系統版本；macOS看到系統開發工具安裝提示可依教室準備完成，Windows使用Git安裝器並重開VS Code。在VS Code Terminal → New Terminal輸入：

```text
git --version
```

應看到版本號；找不到command時先安裝／重開終端機，不繼續init。以下使用支援`git init -b`的Git2.28以上。

終端機是在目前資料夾執行命令。先確認它指向你解壓的獨立專案；不要在這門課整個網站repository根目錄做init。Mac/Linux用`pwd`，Windows PowerShell用`Get-Location`；列檔可用`ls`（PowerShell亦可）。目錄中應看到index.html、styles.css、app.js。最簡單是在VS Code開啟正確資料夾再建立新Terminal；路徑錯就先用`cd`切到實際專案，拖曳資料夾路徑時保留引號。

## 示範：第一個commit先建立基準

下列命令一行一行執行。姓名與email改成你要用於commit的身分；只設本repo，不改全域。Email可使用GitHub設定提供的noreply地址。先在repo外確認你的檔案不含真實密碼或個資。

```bash
git init -b main
git config user.name "你的姓名"
git config user.email "你的Git提交Email"
git add index.html styles.css app.js README.md assets/status-badge.png
git status
git diff --cached
git commit -m "Create studio task website"
git log --oneline -1
```

第一次尚未add的檔案叫Untracked；普通`git diff`不顯示未追蹤檔的內容，所以先add再用`git diff --cached`檢視準備提交的內容。Commit完成後應有一筆hash與訊息；`git status`應顯示working tree clean。這個commit是基準，不是部署。

## 跟著做：改一個標題，讀diff再提交

```bash
git diff -- index.html
git add index.html
git diff --cached -- index.html
git commit -m "Update studio heading"
git log --oneline -2
```

這段前先修改HTML標題並Save；第一個diff應只顯示標題變化。若顯示所有行，檢查編輯器換行或格式化，不把不懂的改動全部提交。兩筆log應分別是建立網站與更新標題。更換CSS或JS同樣只add實際改的檔名。命令沒有變化時先確認檔案Save與目前資料夾，不靠重複commit製造紀錄。

## GitHub：從本機版本送到自己的遠端

1. 在自己的GitHub帳號建立New repository，名稱 `studio-tasks-web`，選Public作純示範網站；不要在這一步新增README／license／gitignore，因為本機已建立基準。公開前檢查只含示範資料。
2. 複製該repo的HTTPS URL。下方USERNAME換為自己的GitHub使用者名稱，不要照抄尖括號或教師帳號。
3. 在同一個專案終端機執行：

```bash
git remote add origin https://github.com/USERNAME/studio-tasks-web.git
git remote -v
git push -u origin main
```

4. 如Git要求驗證，依Git提供的瀏覽器／Credential Manager登入自己的帳號。GitHub不接受直接用帳號密碼當HTTPS Git密碼；不要把密碼寫進命令或貼進講義。
5. 在GitHub repo頁Reload，應看到index.html、styles.css、app.js與assets；開Commits應看到兩筆。`remote -v`只有證明目的地，不能證明push成功。

如果origin已存在，先`git remote -v`確認是不是自己的repo；正確就不重複add。URL錯才用`git remote set-url origin 正確URL`。Push被拒絕，讀錯誤：權限問題改正確帳號／repo；遠端已有README造成history不同，初學主線可改建真正空白的示範repo再繫結，保留本機版本。不要用force push掩蓋不懂的版本衝突。

## GitHub Pages：公開網址與更新驗收

1. 在自己的repo開Settings → Pages。Build and deployment的Source選Deploy from a branch，Branch選main、資料夾選`/(root)`，Save。GitHub Free公開repo可用這條路徑；需有admin或maintainer權限才能設定。
2. 等部署結果完成，檢視Pages提供的Visit site／網址。通常形式為 `https://USERNAME.github.io/studio-tasks-web/`，使用頁面實際顯示的網址；不能把repo程式頁當網站網址。
3. 開網站，用無痕或另一個裝置走登入→詳情→取消→確認；檢查CSS有套用、徽章沒破圖、390／430時沒有橫向溢位、長列表最後一筆看得完整。
4. 回本機再改標題，Save，確認本機畫面，執行`git add index.html`、`git commit -m "Publish updated heading"`、`git push`。等新部署完成，在公開網站Reload確認新標題。這樣才證明後續更新會到網站。
5. 記錄repo URL、網站URL、最新commit與線上觀察日期，放進第15堂交付包README。沒帳號或離線時本機網站與Git可以先完成，公開URL仍需在有權環境補做，不能用localhost或截圖當公開部署完成。

**排錯：**Pages404先查main與root、index.html位於根目錄、部署尚未完成；樣式或圖片404查相對路徑及大小寫（`assets`不是`Assets`）；線上還是舊標題查最新push與部署commit，再Reload或無痕；Button無效開啟瀏覽器Console看錯誤，再查JS路徑和id選擇器。Pages只能提供此靜態網站，不會替你增加正式登入或資料庫。


## 自己完成：改變條件再檢查

用自己的第15堂透明PNG替換assets/status-badge.png，並將任務換成第14堂「活動報名確認」新情境。獨立修改標題、三筆資料與主要色；在390／430、取消／確認、空狀態與長列進行檢查。以明確檔名提交至少兩筆有意義的修改，並線上驗證新標題與徽章。最後README說明和完整Figma原型哪些一致、哪些簡化、狀態為何會在Reload重置。

## 完成條件與理解檢查

- 解壓的獨立專案本機可開，完整取消／確認／清單狀態與長內容正確；理解三檔與id／class分工。
- Git至少有建立基準與修改兩筆commit，能讀普通diff與staged diff，repo root正確。
- 自己的GitHub有實際檔案與commit，Pages公開URL可用；後續更新已線上確認，未執行部分據實記錄。

**想一想：**為何第一次把下載檔放進資料夾後，git diff可能什麼都不顯示？

<details><summary>展開參考答案與理由</summary><p>未追蹤檔還沒有Git基準，普通diff不顯示它們。先git status看Untracked，用明確檔名git add，再git diff --cached看將提交的完整內容；建立第一筆commit後，普通diff才可比較後續修改。</p></details>

## 本堂查證來源

- [MDN：網站入門](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Your_first_website)
- [Git：第一次設定](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)
- [Git：紀錄版本](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)
- [GitHub：建立repo](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [GitHub Pages：設定來源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

來源查證：2026-10-09。
<!-- learner-content:end -->

## 講師授課筆記（不進講義）

先用正文入口題檢查前提，再以短示範讓學員同步操作。每次核心狀態改變立即檢查；主要時間用於自行製作、同儕解釋、錯誤修復與新條件作品。先核對學員真實工具權限與檔案；未達完成條件回到本堂修復位置，不以教師代做當成完成。此稿為作者設計與自審，真人理解／遷移與平台實測須另留證據。
