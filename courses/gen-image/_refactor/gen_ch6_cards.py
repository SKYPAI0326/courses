#!/usr/bin/env python3
"""
CH6 模板速查站｜批次生成腳本
產出：A1-A6, C1-C6 共 12 張卡片 + module6.html + CH6-1.html + CH6-X.html
基於 B 組已完成的 anatomy 結構、簡化為 4 區塊（hero / 01 適用場景 / 02 拆解 / 05 示範圖 + prompt / 06 踩雷）
"""

from pathlib import Path
import textwrap

OUT_DIR = Path(__file__).parent.parent  # courses/gen-image/

# 共用 CSS（從 B 組抽出、減去未用的）
CSS = """:root{--c-bg:#f5f3ee;--c-surface:#edeae3;--c-card:#ffffff;--c-border:#d8d4cb;--c-border-soft:#e8e4da;--c-text:#2c2b28;--c-muted:#7a766d;--c-faint:#bcb8ae;--c-a1:#b5703a;--c-a2:#c9963a;--c-a3:#5a7a5a;--c-a4:#6b7fa3;--c-a5:#7a9ea3;--c-a6:#8a6a4a;--c-main:var(--c-a6);--radius:4px;--radius-sm:3px;--content-w:780px}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Noto Sans TC',sans-serif;background:var(--c-bg);color:var(--c-text);line-height:1.8}
.skip-link{position:absolute;left:-9999px;top:0;z-index:100;background:var(--c-text);color:#fff;padding:10px 16px;border-radius:0 0 var(--radius) 0;font-size:.85rem;text-decoration:none}
.skip-link:focus{left:0}
a:focus-visible,button:focus-visible{outline:2px solid var(--c-text);outline-offset:2px;border-radius:4px}
.topbar{position:sticky;top:0;z-index:50;height:56px;background:rgba(245,243,238,.96);backdrop-filter:blur(12px);border-bottom:1px solid var(--c-border);display:flex;align-items:center;padding:0 48px;gap:16px}
.logo{font-family:'Shippori Mincho',serif;font-weight:700;font-size:1.05rem;color:var(--c-text);letter-spacing:.05em;text-decoration:none}
.topbar-divider{width:1px;height:18px;background:var(--c-border)}
.topbar-sub{font-size:.8rem;color:var(--c-muted)}
.spacer{flex:1}
.topbar-tag{font-size:.72rem;color:var(--c-main);border:1px solid rgba(138,106,74,.3);padding:3px 12px;border-radius:99px;font-weight:500;letter-spacing:.06em}
.progress-strip{height:2px;background:transparent;position:sticky;top:56px;z-index:49}
.progress-fill{height:100%;background:var(--c-text);opacity:.75;width:0%;transition:width .1s}
.page-hero{max-width:var(--content-w);margin:0 auto;padding:64px 48px 48px}
.back-link{display:inline-flex;align-items:center;gap:6px;font-size:.82rem;color:var(--c-muted);text-decoration:none;margin-bottom:28px}
.back-link:hover{color:var(--c-text)}
.hero-eyebrow{font-family:'Shippori Mincho',serif;font-size:.82rem;color:var(--c-faint);letter-spacing:.1em;font-weight:500;margin-bottom:12px;font-variant-numeric:tabular-nums}
.lesson-title{font-family:'Shippori Mincho',serif;font-size:2rem;font-weight:700;line-height:1.3;color:var(--c-text);margin-bottom:20px;max-width:22ch}
.lesson-tagline{font-size:.95rem;color:var(--c-muted);line-height:1.9;margin-bottom:36px}
.outcomes{display:flex;flex-direction:column;gap:10px;padding:4px 0 4px 24px;border-left:1px solid var(--c-text);margin-top:28px}
.outcomes-label{font-size:.72rem;color:var(--c-text);letter-spacing:.15em;font-weight:500;margin-bottom:4px}
.outcome-item{font-size:.88rem;color:var(--c-muted);line-height:1.8}
.lesson-section{max-width:var(--content-w);margin:0 auto;padding:32px 48px}
.section-eyebrow{font-family:'Shippori Mincho',serif;font-size:.82rem;color:var(--c-faint);letter-spacing:.1em;font-weight:500;margin-bottom:10px}
.section-heading{font-family:'Shippori Mincho',serif;font-size:1.45rem;font-weight:700;color:var(--c-text);margin-bottom:20px;line-height:1.4}
.section-rule{border:0;border-top:1px solid var(--c-border-soft);margin:40px auto;max-width:var(--content-w)}
.body-text{font-size:.92rem;color:var(--c-text);line-height:1.9;margin-bottom:16px}
.intro-band{padding:4px 0 4px 24px;margin:0 0 32px;border-left:1px solid var(--c-text)}
.intro-label{font-size:.72rem;color:var(--c-text);letter-spacing:.15em;font-weight:500;margin-bottom:10px}
.intro-text{font-size:.92rem;color:var(--c-muted);line-height:1.9}
.callout{display:flex;gap:16px;padding:18px 22px;border-radius:var(--radius);margin:24px 0;background:var(--c-surface);border-left:2px solid var(--c-text)}
.callout-icon{flex-shrink:0;font-size:1.1rem}
.callout-body{font-size:.9rem;line-height:1.85}
.compare-table{width:100%;border-collapse:collapse;margin:16px 0 24px;font-size:.88rem}
.compare-table th,.compare-table td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--c-border-soft);vertical-align:top;line-height:1.7}
.compare-table th{font-weight:700;color:var(--c-text);background:var(--c-surface);font-size:.82rem;letter-spacing:.05em}
.compare-table td:first-child{color:var(--c-muted);width:18%;font-weight:500}
.scenario-list{list-style:none;padding:0;margin:0}
.scenario-list li{font-size:.88rem;color:var(--c-text);padding:6px 0 6px 18px;position:relative;line-height:1.8}
.scenario-list li::before{content:"";position:absolute;left:0;top:13px;width:8px;height:1px;background:var(--c-faint)}
.scenario-list li strong{color:var(--c-main);font-weight:700}
.prompt-block{position:relative;margin:18px 0 24px;background:var(--c-card);border:1px solid var(--c-border);border-left:3px solid var(--c-main);border-radius:var(--radius)}
.prompt-block-head{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 18px;border-bottom:1px solid var(--c-border-soft);background:var(--c-surface);border-radius:var(--radius) var(--radius) 0 0}
.prompt-block-label{font-family:'Shippori Mincho',serif;font-size:.82rem;font-weight:700;color:var(--c-text);letter-spacing:.05em}
.prompt-block-meta{font-size:.72rem;color:var(--c-muted);letter-spacing:.05em}
.prompt-copy-btn{font-family:'Noto Sans TC',sans-serif;font-size:.78rem;color:var(--c-main);background:transparent;border:1px solid rgba(138,106,74,.4);border-radius:var(--radius-sm);padding:5px 12px;cursor:pointer;transition:background .15s,color .15s}
.prompt-copy-btn:hover{background:var(--c-main);color:#fff}
.prompt-copy-btn.copied{background:var(--c-a3);color:#fff;border-color:var(--c-a3)}
.prompt-body{margin:0;padding:18px 22px;font-family:'Noto Sans TC',sans-serif;font-size:.88rem;line-height:1.95;color:var(--c-text);white-space:pre-wrap;word-break:break-word;overflow-x:auto}
.swap-table{width:100%;border-collapse:collapse;margin:14px 0 22px;font-size:.88rem}
.swap-table th,.swap-table td{text-align:left;padding:12px 14px;border:1px solid var(--c-border-soft);line-height:1.75;vertical-align:top}
.swap-table th{font-weight:700;color:var(--c-text);background:var(--c-surface);font-size:.82rem}
.swap-table td:first-child{width:42%;color:var(--c-text);font-weight:500}
.swap-table td:last-child{color:var(--c-muted);font-style:italic}
.pitfall-list{list-style:none;padding:0;margin:14px 0 22px;counter-reset:pf}
.pitfall-list li{padding:14px 0 14px 36px;border-bottom:1px solid var(--c-border-soft);position:relative;font-size:.9rem;line-height:1.85;counter-increment:pf}
.pitfall-list li:last-child{border-bottom:none}
.pitfall-list li::before{content:counter(pf);position:absolute;left:0;top:14px;font-family:'Shippori Mincho',serif;font-size:.85rem;color:var(--c-main);font-weight:700;width:24px;height:24px;border:1px solid var(--c-main);border-radius:50%;text-align:center;line-height:22px}
.pitfall-list li strong{color:var(--c-text);font-weight:700}
.attribution{font-size:.78rem;color:var(--c-faint);margin-top:32px;padding-top:18px;border-top:1px solid var(--c-border-soft);line-height:1.8}
.attribution a{color:var(--c-muted);text-decoration:none;border-bottom:1px solid var(--c-border)}
.nav-footer{max-width:var(--content-w);margin:0 auto;padding:32px 48px 64px;display:flex;justify-content:space-between;align-items:center;gap:12px}
.nav-btn{display:inline-flex;align-items:center;gap:6px;font-size:.85rem;color:var(--c-main);text-decoration:none;padding:10px 20px;border:1px solid rgba(138,106,74,.3);border-radius:var(--radius);transition:background .2s}
.nav-btn:hover{background:rgba(138,106,74,.07);border-color:var(--c-main)}
.nav-btn.primary{background:var(--c-main);color:#fff;border-color:var(--c-main)}
.footer{border-top:1px solid var(--c-border);padding:24px 48px;display:flex;align-items:center;gap:16px}
.footer-logo{font-family:'Shippori Mincho',serif;font-size:.9rem;font-weight:700;color:var(--c-muted)}
.footer-div{width:1px;height:14px;background:var(--c-border)}
.footer-note{font-size:.75rem;color:var(--c-muted)}
.footer-meta{font-size:.7rem;color:var(--c-faint);margin-left:auto;letter-spacing:.05em}
@media(prefers-reduced-motion:reduce){.section-rule{opacity:1!important;transform:none!important}*{animation:none!important}}
@media(max-width:600px){.topbar,.page-hero,.lesson-section,.nav-footer,.footer{padding-left:24px;padding-right:24px}.lesson-title{max-width:100%}}"""

JS_PROGRESS = """const fill=document.getElementById('prog');
const strip=document.querySelector('.progress-strip');
window.addEventListener('scroll',()=>{const h=document.documentElement;const pct=(h.scrollTop/(h.scrollHeight-h.clientHeight))*100;fill.style.width=pct+'%';if(strip)strip.setAttribute('aria-valuenow',Math.round(pct));});"""

JS_COPY = """document.querySelectorAll('.prompt-copy-btn').forEach(function(btn){
  btn.addEventListener('click',function(){
    var target=document.getElementById(btn.dataset.target);
    if(!target)return;
    var text=target.textContent;
    var done=function(){btn.textContent='已複製 ✓';btn.classList.add('copied');setTimeout(function(){btn.textContent='複製 prompt';btn.classList.remove('copied');},1800);};
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(text).then(done).catch(function(){btn.textContent='請手動選取';});
    }
  });
});"""

JS_PERSIST = """(function(){
  var k='progress:'+location.pathname;
  var saved=parseInt(localStorage.getItem(k)||'0',10);
  if(saved>0){window.addEventListener('load',function(){window.scrollTo(0,saved);});}
  var t;
  window.addEventListener('scroll',function(){clearTimeout(t);t=setTimeout(function(){localStorage.setItem(k,String(window.scrollY));},200);},{passive:true});
})();"""


def render_card(c):
    """產出單張卡片 HTML（精簡 anatomy 4 區塊）"""
    use_cases_html = "\n    ".join(f"<li><strong>{u['t']}</strong>（{u['d']}）</li>" for u in c['use_cases'])
    compare_rows = "\n      ".join(f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>" for r in c['compare_table'])
    six_rows = "\n      ".join(f"<tr><td>{i+1}</td><td>{s['name']}</td><td>{s['need']}</td><td>{s['fill']}</td></tr>" for i, s in enumerate(c['six_segments']))
    swap_rows = "\n      ".join(f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>" for r in c['swap_table'])
    pitfalls_html = "\n    ".join(f'<li{" id=\"pitfall-typography\"" if i == len(c["pitfalls"])-1 else ""}><strong>{p["t"]}</strong>　{p["d"]}</li>' for i, p in enumerate(c['pitfalls']))

    return f"""<!DOCTYPE html>
<!--
  CH6-{c['id']} {c['title']}｜CH6 模板速查站
  ============================================
  PREV / NEXT 暫指 ../index.html，待 module6.html 與其他卡片建立後修正
  來源：ConardLi/garden-skills (MIT License) skills/gpt-image-2/references/{c['source_md']}
  此卡片由 _refactor/gen_ch6_cards.py 批次生成（精簡 anatomy 4 區塊）
-->
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>6·{c['id']} {c['title']}｜商業用圖片生成</title>
<meta name="description" content="{c['title']}模板速查：{c['meta_desc']}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="弄一下工作室">
<meta property="og:title" content="6·{c['id']} {c['title']}｜商業用圖片生成">
<meta property="og:description" content="{c['title']}模板速查：{c['meta_desc']}">
<meta property="og:url" content="https://skypai0326.github.io/courses/courses/gen-image/CH6-{c['id']}.html">
<meta property="og:image" content="https://skypai0326.github.io/courses/素材/og-default.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="6·{c['id']} {c['title']}｜商業用圖片生成">
<meta name="twitter:description" content="{c['title']}模板速查：{c['meta_desc']}">
<meta name="twitter:image" content="https://skypai0326.github.io/courses/素材/og-default.png">
<link rel="canonical" href="https://skypai0326.github.io/courses/courses/gen-image/CH6-{c['id']}.html">
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>

<a href="#main" class="skip-link">跳至主要內容</a>

<header class="topbar">
  <a href="../../index.html" class="logo">弄一下工作室</a>
  <div class="topbar-divider"></div>
  <span class="topbar-sub">商業用圖片生成</span>
  <div class="spacer"></div>
  <span class="topbar-tag">M6 · 速</span>
</header>
<div class="progress-strip" role="progressbar" aria-label="閱讀進度" aria-valuemin="0" aria-valuemax="100"><div class="progress-fill" id="prog"></div></div>

<main id="main">

<div class="page-hero">
  <a href="module6.html" class="back-link"><span aria-hidden="true">←</span> 返回 CH6 模板速查站</a>
  <div class="hero-eyebrow">({c['id']})</div>
  <h1 class="lesson-title">{c['title']}</h1>
  <p class="lesson-tagline">{c['tagline']}</p>
  <div class="outcomes">
    <div class="outcomes-label">這張卡片你會學到</div>
    <div class="outcome-item">{c['outcomes'][0]}</div>
    <div class="outcome-item">{c['outcomes'][1]}</div>
    <div class="outcome-item">{c['outcomes'][2]}</div>
  </div>
</div>

<section class="lesson-section">
  <div class="section-eyebrow">(01)</div>
  <h2 class="section-heading">適用場景</h2>
  <div class="intro-band">
    <div class="intro-label">這個模板用在哪</div>
    <div class="intro-text">{c['intro']}</div>
  </div>
  <p class="body-text">四個典型用途：</p>
  <ul class="scenario-list" style="margin-bottom:24px">
    {use_cases_html}
  </ul>
  <table class="compare-table" aria-label="{c['title']}與其他模板的差異">
    <thead>
      <tr><th>對比項</th><th>本卡片 · {c['id']} {c['title']}</th><th>近似模板</th></tr>
    </thead>
    <tbody>
      {compare_rows}
    </tbody>
  </table>
  <div class="callout">
    <div class="callout-icon" aria-hidden="true">💡</div>
    <div class="callout-body"><strong>一句話判斷</strong>：{c['judge']}</div>
  </div>
</section>

<hr class="section-rule">

<section class="lesson-section">
  <div class="section-eyebrow">(02)</div>
  <h2 class="section-heading">模板拆解｜6 段 prompt 結構</h2>
  <p class="body-text">{c['decompose_intro']}</p>
  <table class="compare-table" aria-label="{c['title']} prompt 6 段結構">
    <thead>
      <tr><th>段</th><th>段落</th><th>必問還是可預設</th><th>填什麼</th></tr>
    </thead>
    <tbody>
      {six_rows}
    </tbody>
  </table>
  <div class="callout">
    <div class="callout-icon" aria-hidden="true">📐</div>
    <div class="callout-body"><strong>記憶口訣</strong>：{c['mnemonic']}</div>
  </div>
</section>

<hr class="section-rule">

<section class="lesson-section">
  <div class="section-eyebrow">(03)</div>
  <h2 class="section-heading">示範圖｜可複製、可重現</h2>
  <p class="body-text">{c['demo_intro']}</p>
  <figure style="margin:20px 0">
    <img src="img/{c['image_path']}" alt="{c['image_alt']}" loading="lazy" style="width:100%;height:auto;border-radius:6px;display:block;border:1px solid var(--c-border)">
    <figcaption style="font-size:.8rem;color:var(--c-muted);margin-top:10px;line-height:1.7"><strong>誠實標註</strong>：{c['caption']}</figcaption>
  </figure>

  <div class="prompt-block">
    <div class="prompt-block-head">
      <span class="prompt-block-label">完整 prompt · {c['prompt_label']}</span>
      <span class="prompt-block-meta">適用：ChatGPT GPT-image / Gemini Nano Banana</span>
      <button type="button" class="prompt-copy-btn" data-target="prompt-{c['id'].lower()}-1">複製 prompt</button>
    </div>
    <pre class="prompt-body" id="prompt-{c['id'].lower()}-1">{c['prompt_full']}</pre>
  </div>

  <div class="callout">
    <div class="callout-icon" aria-hidden="true">📷</div>
    <div class="callout-body"><strong>讀圖時看這 4 個點</strong>：{c['read_4_points']}</div>
  </div>
</section>

<hr class="section-rule">

<section class="lesson-section">
  <div class="section-eyebrow">(04)</div>
  <h2 class="section-heading">改成你的場景｜踩雷與失敗案例</h2>
  <p class="body-text">把 prompt 拿來、改 3 個替換槽就變你的版本：</p>
  <table class="swap-table" aria-label="3 個替換槽位">
    <thead>
      <tr><th>替換槽</th><th>你的版本</th></tr>
    </thead>
    <tbody>
      {swap_rows}
    </tbody>
  </table>
  <p class="body-text" style="margin-top:24px;font-weight:500">最常見的 4 種踩雷：</p>
  <ol class="pitfall-list">
    {pitfalls_html}
  </ol>
  <div class="attribution">
    本卡片改寫自 <a href="https://github.com/ConardLi/garden-skills/blob/main/skills/gpt-image-2/references/{c['source_md']}" target="_blank" rel="noopener">ConardLi／garden-skills</a> 之 <code>{c['source_md'].split('/')[-1]}</code> 模板（MIT License、2026），已對中文進行台灣用語在地化、加入本地接案情境與失敗案例。
  </div>
</section>

<div class="nav-footer">
  <a href="{c['prev_file']}" class="nav-btn"><span aria-hidden="true">←</span> {c['prev_label']}</a>
  <a href="{c['next_file']}" class="nav-btn primary">{c['next_label']} <span aria-hidden="true">→</span></a>
</div>

</main>

<footer class="footer">
  <span class="footer-logo">弄一下工作室</span>
  <div class="footer-div"></div>
  <span class="footer-note">2026 春季</span>
  <span class="footer-meta" data-platform-version="ChatGPT GPT-image-1 / Gemini Nano Banana" data-built-at="2026-05-01">本頁以 ChatGPT GPT-image-1 / Gemini Nano Banana 製作，2026-05</span>
</footer>

<script>
{JS_PROGRESS}
</script>
<script>
{JS_COPY}
</script>
<script>
{JS_PERSIST}
</script>
</body>
</html>"""


# ============= 12 張卡片 metadata =============
# 為了控制長度，每張使用簡潔的數據結構
# A1 已單獨完成、不在批次內

CARDS = [
    # ----- A 組 品牌行銷 -----
    {
        "id": "A1", "title": "Web Hero Banner 官網首屏",
        "source_md": "poster-and-campaigns/banner-hero.md",
        "tagline": "網頁首屏 / 落地頁 / app banner / 投放素材的橫向構圖視覺。一句強 claim + CTA + 主視覺、底部安全留白避免裁切。是品牌數位露出最高頻的格式、SOHO 接案 NT$5,000-15,000 級別案子最常見。",
        "outcomes": ["能判斷何時用 web hero banner（與 A2 KV、A3 海報的差異）", "能拆解 6 段並安排橫向構圖的視覺重量", "能識別 4 種踩雷（claim 不夠強／CTA 不顯眼／安全區被裁切／主視覺位置不對）"],
        "intro": "橫向超寬比例（16:9 / 21:9 / 3:1）的網頁 hero 區。左側文案 + 右側主視覺 + 底部安全留白避免被瀏覽器裁切。比 A3 brand poster 多了 CTA、比 A2 KV 不需延展系統、比 B5 UI 疊加更聚焦品牌氛圍。",
        "use_cases": [
            {"t": "品牌官網首屏 hero", "d": "首頁打開第一眼"},
            {"t": "電商落地頁 banner", "d": "活動專頁、訂閱專頁"},
            {"t": "App 頂部活動 banner", "d": "推播、首頁活動橫幅"},
            {"t": "Email marketing banner", "d": "EDM hero 區、會員週報"},
        ],
        "compare_table": [
            ("比例", "橫向 16:9 / 21:9 / 3:1", "A3：直立 2:3；A4：直立 2:3"),
            ("Claim", "1 句強訴求", "A3：品牌主張；A2：campaign claim"),
            ("CTA", "<strong>必有</strong>明顯按鈕", "A3：通常無；A4：通常無"),
            ("安全留白", "底部 15% 避免裁切", "其他模板：較自由"),
            ("延展性", "通常單張、不延展", "A2：必延展多比例"),
            ("使用場景", "純數位（網頁 / app / EDM）", "A3：可印刷"),
        ],
        "judge": "客戶問「官網首屏」走 A1；問「campaign 系列」走 A2；問「品牌精神海報」走 A3；問「落地頁含表單 + UI」走 B5。<strong>A1 是 SOHO 接案最常碰的 A 組卡片</strong>。",
        "decompose_intro": "web hero banner 6 段。<strong>核心難度在「橫向構圖的視覺重量分配」</strong>——左欄文案太多、右欄主視覺太空、整體不平衡：",
        "six_segments": [
            {"name": "比例 + 用途", "need": "<strong>必問</strong>", "fill": "16:9 / 21:9 / 3:1（依平台）+ 用途（web / app / EDM）"},
            {"name": "claim + subtext", "need": "<strong>必問</strong>", "fill": "headline ≤ 8 字（英文優先避字體覆轍）+ subtext 1-2 行說明"},
            {"name": "CTA 區", "need": "<strong>必問</strong>", "fill": "1-2 個按鈕（主 CTA 填充 + 副 CTA 邊框）；位置：左欄 headline 下方"},
            {"name": "主視覺", "need": "<strong>必問</strong>", "fill": "右欄產品 / 模特 / 概念圖；占畫面 30-50%"},
            {"name": "色板 + 字體", "need": "可預設", "fill": "品牌色 + ≤ 3 色 accent；字體 ≤ 2 種"},
            {"name": "安全留白", "need": "固定寫死", "fill": "底部 15% 留白避免裁切；左右各留 5% padding"},
        ],
        "mnemonic": "比例 → claim → CTA → 視覺 → 色 → 安全。<strong>新手最常忽略「安全留白」</strong>——AI 把元素貼到底部邊緣、實際放網頁時被瀏覽器自適應裁切。明確寫「safe area 15% from bottom edge」。",
        "demo_intro": "下面這張是 OPEN BEANS 訂閱方案的 web hero banner。21:9 超寬比例、左欄「Coffee, Reimagined.」大字 + CTA「Start Your Subscription」、右欄咖啡豆袋 + 散落咖啡豆 + 後景虛化的烘豆機。可直接放品牌官網首屏。",
        "image_path": "v51-a1-banner-hero.png",
        "image_alt": "OPEN BEANS Web Hero Banner、21:9 橫向超寬構圖、左欄 Coffee Reimagined 大字米白配 Single-Origin coffee subscribe 副標、Start Your Subscription CTA 按鈕、右欄米白色咖啡豆袋與散落咖啡豆配後景虛化烘豆機輪廓、深棕暖光氛圍背景、適合品牌官網首屏與訂閱頁",
        "caption": "本圖所有英文 headline、subtext、CTA 文案皆為英文——延續規避中文字體限制策略。中文版「咖啡，重新被定義」「立即訂閱」走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline\">後製字體疊圖工作流</a>。",
        "prompt_label": "OPEN BEANS 訂閱方案 web hero banner",
        "prompt_full": """請生成一張 web 首屏 hero banner（網頁頂部主視覺），延續 OPEN BEANS 咖啡品牌系列。橫向 21:9 比例、可直接放進品牌官網首頁頂部：

【整體構圖】橫向超寬、左側 40% 文案區（左對齊）、右側 60% 主視覺區（OPEN BEANS 咖啡豆袋 + 散落咖啡豆 + 暖光氛圍）。底部留 15% 安全留白。

【背景】溫暖深棕漸變（左暗右亮）、絲絨紋理感、像精品咖啡店的牆面光影。色溫暖橘棕。

【左欄文案】（畫面左上區）
- 大字 headline：「Coffee, Reimagined.」（無襯線粗體大字、米白色、英文）
- 副標：「Single-Origin coffee, roasted in Taipei within 7 days of order. Subscribe now.」（細體、淺米色、英文）
- CTA 按鈕：「Start Your Subscription →」（深棕填充、米白文字、圓角）

【右欄主視覺】OPEN BEANS 200g 牛皮紙咖啡豆袋（同 B 組系列）置於畫面右側偏中、占整體畫面 25%、有戲劇性側光、底部散落幾顆深棕咖啡豆、瓶後遠景虛化的烘豆機輪廓（極淡）。

【風格】高級精品咖啡品牌氣質、像 Blue Bottle Coffee 官網 hero 那種視覺。低飽和、溫暖光、雜誌廣告級渲染。

【限制】嚴禁人物、嚴禁中文文字、嚴禁排版擁擠、嚴禁色板出現額外鮮艷色（限米白＋深棕＋暖橘 accent）、嚴禁底部 15% 安全留白被裁切到關鍵元素。""",
        "read_4_points": "(1) 橫向構圖左右視覺重量平衡嗎？(2) CTA 按鈕夠不夠搶眼（不會被主視覺吃掉）？(3) 底部 15% 安全留白有沒有保留（沒有元素貼底）？(4) headline 是不是 ≤ 8 字夠精煉？",
        "swap_table": [
            ("ⓐ 比例 + 用途 = ?", "例：21:9 web hero / 16:9 EDM banner / 3:1 app 活動 banner"),
            ("ⓑ headline + CTA = ?（英文優先）", "例：「Coffee, Reimagined」+「Start Subscription」"),
            ("ⓒ 主視覺 = ?", "例：商品（咖啡豆袋）／模特（半身、不見正臉）／概念圖（抽象幾何）"),
        ],
        "pitfalls": [
            {"t": "Claim 不夠強", "d": "「我們提供高品質的精品咖啡訂閱服務」這種長句沒人看。<strong>解法</strong>：headline ≤ 8 字、英文優先、動詞驅動（Reimagined / Discover / Slow Down）。"},
            {"t": "CTA 不夠顯眼", "d": "AI 給你一個米白邊框米白底的 CTA、跟背景融合。<strong>解法</strong>：明確寫「primary CTA filled with brand color, white text, rounded corners, prominent size」。"},
            {"t": "安全區被裁切", "d": "AI 把咖啡豆袋底部貼到畫面底邊、實際 RWD 縮小時被裁掉。<strong>解法</strong>：明確寫「all key elements within central 70%, bottom 15% reserved as safe area」。"},
            {"t": "中文 headline 一律後製", "d": "imagegen 中文字體限制。<strong>A1 的最佳策略</strong>：英文版用 imagegen 直出、中文版（「咖啡，重新被定義」）走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline;font-weight:700\">後製字體疊圖工作流附錄</a>。<br><br><strong>實戰提醒</strong>：A1 是 A 組裡最高頻的接案類型——客戶官網每年改版至少 1 次、且常需多種比例（桌機 21:9 + 行動 9:16）。<strong>建議跟客戶簽「年度官網視覺套餐」</strong>，每季 1 張、客戶單價可拉到 NT$50,000+。"},
        ],
        "prev_file": "CH6-1.html", "prev_label": "上一頁 方法論",
        "next_file": "CH6-A2.html", "next_label": "下一張 A2",
        "meta_desc": "Web hero banner 模板速查：官網首屏 / 落地頁 / app banner、橫向構圖一張到位。",
    },
    {
        "id": "A2", "title": "Campaign KV 系列主視覺", "source_md": "poster-and-campaigns/campaign-kv.md",
        "tagline": "季度 / 節慶 / 雙 11 大促的「campaign 系列主視覺」。一個 anchor visual + 一套延展 layout，可拓展成 banner / story / 短影音封面 / 海報。強調可複用、可成系列。",
        "outcomes": ["能判斷何時用 campaign KV（與 A1 web hero、A3 brand poster 的差異）", "能拆解 6 段結構並產出可延展的 anchor visual", "能識別 4 種踩雷（claim 不夠強／延展性差／色板不統一／元素過多）"],
        "intro": "由 1 個 anchor visual 主圖 + 1 套 layout system 組成的系列主視覺。重點是「可延展」——主圖能拆出 banner、IG story、short video 封面、海報、實體展板，所有衍生視覺都看得出是同一個 campaign。",
        "use_cases": [
            {"t": "雙 11 / 週年慶大促主視覺", "d": "電商最高頻、跨平台投放需求"},
            {"t": "中秋 / 春節 / 母親節節慶 KV", "d": "本地品牌季節推廣"},
            {"t": "新品系列發表主視覺", "d": "1 主圖 + 5-8 衍生延展"},
            {"t": "聯名 campaign 主圖", "d": "兩個品牌共同視覺"},
        ],
        "compare_table": [
            ("視覺主體", "1 主視覺 + 1 套延展系統", "A1：單張 web banner；A3：單張海報"),
            ("延展性", "<strong>必含</strong>：1:1 / 9:16 / 16:9 預覽", "其他模板：單一比例"),
            ("Claim", "強而短、品牌主張句", "A1：產品功能；A3：氛圍感"),
            ("色板", "嚴格統一（品牌色 + campaign 色）", "其他模板：較自由"),
            ("使用週期", "1-3 個月 campaign 期", "A1：常駐；A3：單檔"),
            ("接案類型", "中大型品牌行銷部", "A1：SOHO；A3：個人品牌"),
        ],
        "judge": "客戶問「我這檔 campaign 要做什麼」走 A2；問「官網首屏」走 A1；問「單張海報」走 A3。<strong>A2 是 A 組裡接案規模最大的卡片</strong>——一個 campaign 報價 NT$30000-100000 是常態。",
        "decompose_intro": "原模板把一個 campaign KV 拆成 6 段。<strong>核心難度在「延展性」</strong>——主視覺看起來好不夠、要能拆出多比例衍生：",
        "six_segments": [
            {"name": "campaign 主題 + claim", "need": "<strong>必問</strong>", "fill": "campaign 名稱 + 主張句（≤ 8 字、英文優先）+ 時間窗口"},
            {"name": "anchor visual 主視覺", "need": "<strong>必問</strong>", "fill": "畫面中心元素（人物 / 產品 / 概念圖形）+ 構圖（中心對稱 / 黃金分割）"},
            {"name": "色板", "need": "<strong>必問</strong>", "fill": "品牌色 + campaign 專屬色（建議 ≤ 3 色）+ accent 色"},
            {"name": "delivery layouts", "need": "<strong>必問</strong>", "fill": "延展比例：1:1 IG / 9:16 story / 16:9 banner，每個比例 anchor 元素的擺放"},
            {"name": "typography", "need": "可預設", "fill": "標題字（粗 sans）+ tagline（serif 或 sans 細體）；英文優先避字體覆轍"},
            {"name": "constraints 限制", "need": "固定寫死", "fill": "禁忌：色板出現額外鮮艷色、字體超過兩種、anchor 元素在不同比例失焦"},
        ],
        "mnemonic": "主題 → 主視覺 → 色板 → 延展 → 字 → 禁。<strong>新手最常漏「delivery layouts」</strong>——只生 1 張 anchor、忘了確認衍生比例會不會裁切到關鍵元素。要明確寫「at least 3 aspect ratios」「safe area for square crop」。",
        "demo_intro": "下面這張是 OPEN BEANS 雙 11 大促 campaign 主視覺 1:1 anchor 版本。延展時把同 prompt 改成 9:16（IG story）、16:9（FB banner）、用同樣的 anchor 元素重新構圖即可。",
        "image_path": "v52-a2-campaign-kv.png",
        "image_alt": "OPEN BEANS 雙 11 campaign 主視覺、anchor visual 1:1 構圖、左上 OPEN BEANS 11.11 大字配 EARLY BIRD SAVE 25% claim、中央咖啡豆袋與散落咖啡豆構成主視覺、深棕米白燙金三色板",
        "caption": "本圖為 1:1 anchor 版本。實作 campaign 時要同時跑 9:16（IG story）+ 16:9（banner）兩個延展版本驗證 anchor 元素在不同比例都不被裁切。中文 campaign 文案（譬如「年度最強優惠」）走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline\">後製字體疊圖工作流</a>。",
        "prompt_label": "OPEN BEANS 雙 11 campaign 主視覺",
        "prompt_full": """請生成一張 campaign 主視覺 anchor visual（可延展為 banner / story / 海報的系列主圖）：

【Campaign 主題】OPEN BEANS 雙 11 早鳥優惠（11.11 Early Bird Sale）

【Anchor 主視覺】
- 構圖：1:1 正方形、中心對稱
- 中心元素：OPEN BEANS 200g 咖啡豆袋（深棕牛皮紙）+ 散落咖啡豆
- 背景：深棕絲絨漸變、暖光氛圍

【文案】
- 大字 claim：「11.11」（巨大數字、燙金、襯線粗體）
- 主題：「EARLY BIRD SALE」（無襯線粗體、米白）
- 副標：「Save 25% · Free Shipping」（細體、淺米色）
- 小字：「Limited to first 500 subscribers」

【色板】嚴格三色：深棕主、米白底、燙金 accent。不出現紅色、藍色、綠色等鮮艷色。

【字體】標題用襯線粗體（avoid 新細明體）、副標用無襯線細體。全英文。

【風格】像 Apple 雙 11 主視覺那種克制感、不要淘寶廣告風。

【限制】嚴禁人物、嚴禁排版擁擠、嚴禁色板出現額外鮮艷色、嚴禁中文字、嚴禁 anchor 元素貼邊（要留 10% 安全區給後續裁切）。""",
        "read_4_points": "(1) anchor 元素夠不夠強（拆 9:16 / 16:9 還能認得是同 campaign）？(2) claim 是不是 ≤ 8 字夠精煉？(3) 色板有沒有限制在 ≤ 3 色？(4) 文案有沒有遮到 anchor？",
        "swap_table": [
            ("ⓐ campaign 主題 + claim = ?", "例：雙 11／中秋限定／週年慶／新品上市"),
            ("ⓑ anchor 元素 = ?（中心視覺）", "例：產品堆疊／單品特寫／象徵物（月亮、煙火、樹葉）"),
            ("ⓒ 色板三色 = ?", "例：深棕＋米白＋燙金（咖啡）／中國紅＋金＋黑（春節）／粉＋灰白＋金（母親節）"),
        ],
        "pitfalls": [
            {"t": "claim 太長、不夠強", "d": "「我們提供最棒的咖啡訂閱方案讓您每天都有好咖啡」這種 30 字 claim 沒人看。<strong>解法</strong>：claim ≤ 8 字、英文優先、動詞驅動。"},
            {"t": "延展性沒驗證", "d": "anchor 在 1:1 看起來好但拆 9:16 主視覺被裁掉。<strong>解法</strong>：prompt 加「safe area for vertical / horizontal crop」、「anchor centered with 10% padding」。"},
            {"t": "色板鎖不住", "d": "AI 自動加金黃 / 鮮紅做「節慶感」、毀掉品牌色板。<strong>解法</strong>：constraints 明確列禁用色 + must keep 三色、跑出來檢查每個像素是否在三色範圍。"},
            {"t": "中文 campaign 文案別指望 prompt 解決", "d": "imagegen 對中文字體只給新細明體系。<strong>A2 的最佳策略</strong>：claim 寫英文（11.11 Sale / Early Bird），中文 campaign 標語（「雙 11 年度最強優惠」）走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline;font-weight:700\">後製字體疊圖工作流附錄</a>。<br><br><strong>實戰提醒</strong>：A2 是「campaign 系列」，後製疊字流程要做 3 次（1:1 / 9:16 / 16:9 各疊一次）才完整。Figma 用 component 一次設計、三比例自動套用、效率最高。"},
        ],
        "prev_file": "CH6-A1.html", "prev_label": "上一張 A1",
        "next_file": "CH6-A3.html", "next_label": "下一張 A3",
        "meta_desc": "Campaign 主視覺模板速查：1 主圖 + 多比例延展、可拆 banner / story / 海報。拆解 6 段 prompt、台灣化情境、4 種踩雷。",
    },
    {
        "id": "A3", "title": "Brand Poster 單張品牌海報",
        "source_md": "poster-and-campaigns/brand-poster.md",
        "tagline": "單張、可印刷、可貼牆、可放 IG 的「品牌海報」。一張圖傳達一個品牌主張，不是 campaign 也不是產品圖，是「品牌個性的視覺名片」。咖啡店牆面、選物店貼紙、文青品牌週報主圖最常用。",
        "outcomes": ["能判斷何時用 brand poster（與 A1/A2/A4 的差異）", "能拆解 6 段結構並產出單張高張力品牌海報", "能識別 4 種踩雷（主張不清／構圖太擠／色板亂／字體混搭）"],
        "intro": "單張、克制、有張力的品牌海報。不是 campaign（沒有時效）、不是 product hero（不講功能）、不是雜誌封面（不講故事）。目的是「一張圖讓人記得這個品牌」。比 A1 更純粹、比 A2 更克制、比 A4 更聚焦。",
        "use_cases": [
            {"t": "咖啡店 / 選物店牆面海報", "d": "實體店面氛圍營造"},
            {"t": "文青品牌每月主視覺", "d": "貼 IG 用、輪換系列"},
            {"t": "活動 / 講座 / 工作坊宣傳", "d": "單張海報傳達主題"},
            {"t": "品牌精神週報主圖", "d": "電子報週六固定欄位"},
        ],
        "compare_table": [
            ("尺寸與比例", "直立 2:3 或 1:1.4（A4/A3 海報尺寸）", "A1：橫式 21:9；A2：1 主 + 多延展；A4：書封 2:3"),
            ("主張數量", "1 個（短主張句）", "A2：campaign claim；A4：書封標題"),
            ("延展性", "通常單張、不延展", "A2：必須延展"),
            ("使用場景", "實體 + 數位混合", "A1：純數位；A4：純印刷"),
            ("文字密度", "1-2 段、克制", "A2：claim + sub；A4：標題 + 作者 + 副題"),
            ("產出難度", "中（克制感最難拿捏）", "A1：低；A2：高"),
        ],
        "judge": "客戶問「店裡牆面要貼什麼」走 A3；問「campaign 主視覺」走 A2；問「官網 hero」走 A1；問「書封 / 雜誌封面」走 A4。<strong>A3 在文青品牌最受歡迎</strong>——單張海報接案 NT$3000-8000、客戶常成系列訂購。",
        "decompose_intro": "brand poster 6 段。<strong>核心難度在「克制」</strong>——AI 容易把海報塞太多元素、變成「廣告」而不是「品牌海報」：",
        "six_segments": [
            {"name": "brand 品牌定位", "need": "<strong>必問</strong>", "fill": "品牌名 + 1 句品牌精神（短句）+ 個性形容詞（克制 / 復古 / 文青 / 有機）"},
            {"name": "main statement 主張句", "need": "<strong>必問</strong>", "fill": "1 句話、≤ 8 字、英文優先；位置（左上 / 中央 / 右下）"},
            {"name": "anchor visual 主視覺", "need": "<strong>必問</strong>", "fill": "1 個視覺元素（產品 / 抽象圖形 / 自然物 / 字體本身）；不要 2 個以上"},
            {"name": "color palette 色板", "need": "<strong>必問</strong>", "fill": "品牌色 + 至多 1 個 accent；克制感 ≤ 2-3 色"},
            {"name": "typography 字體", "need": "可預設", "fill": "1 個主字（粗 serif 或粗 sans）+ 1 個輔字（細）；英文優先"},
            {"name": "constraints 限制", "need": "固定寫死", "fill": "禁忌：元素超過 3 個、色板超過 3 色、字體超過 2 種、淘寶廣告風、字塞滿"},
        ],
        "mnemonic": "品牌 → 主張 → 主視覺 → 色 → 字 → 禁。<strong>新手最常加太多東西</strong>——海報的力量在「留白」。明確寫「畫面留白 ≥ 40%」「anchor 元素 ≤ 1 個」這兩道鎖、海報質感就出來了。",
        "demo_intro": "下面這張是 OPEN BEANS 「Slow is Better」品牌週主視覺。海報一張、貼咖啡店牆面、放 IG、印 A4 三用。注意極致的留白與單一 anchor 元素（咖啡杯線稿）。",
        "image_path": "v53-a3-brand-poster.png",
        "image_alt": "OPEN BEANS Slow is Better 品牌海報、極簡米白底、中央極小咖啡杯線稿、上方 OPEN BEANS 細體品牌名、中間 Slow is Better 大字主張、下方 Single-Origin Coffee 細體小字、極致留白克制設計",
        "caption": "本海報走「克制風」、留白超過 50%。如果客戶要「熱鬧版」改加 anchor 數量到 3 個（咖啡豆 / 杯子 / 蒸氣）、調色板到溫暖色系。中文海報主張（「慢，才是更好」）走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline\">後製字體疊圖工作流</a>。",
        "prompt_label": "OPEN BEANS Slow is Better 品牌海報",
        "prompt_full": """請生成一張單張品牌海報（brand poster）：

【尺寸與構圖】直立 2:3、A3 海報比例、克制風格、留白超過 50%。

【品牌】OPEN BEANS（精品咖啡品牌、強調慢咖啡精神）

【主張句】「Slow is Better」（巨大、置中略偏上、襯線粗體、深棕色）
副標：「Single-Origin Coffee · Roasted in Taipei」（細體無襯線、淺棕、置中、距主張 1cm）

【Anchor 主視覺】中央極簡咖啡杯線稿（≤ 3 條黑線、handwritten 感、不超過畫面 15%）

【色板】嚴格 2 色：米白底（#F5F0E8）+ 深棕字（#3A2A1F），可有極淺燙金 accent（用於小字下劃線）。

【字體】主張：襯線粗體（避免新細明體）；副標：無襯線細體；都用英文。

【背景】純米白底、無紋理、無漸變、無雜物。

【限制】嚴禁人物、嚴禁第 4 個視覺元素、嚴禁色板超過 3 色、嚴禁字體超過 2 種、嚴禁鮮艷色、嚴禁中文字、嚴禁淘寶廣告風（避免閃光、星星、徽章等元素）。""",
        "read_4_points": "(1) 留白夠不夠（≥ 40%）？(2) anchor 是不是只有 1 個？(3) 色板是不是 ≤ 3 色？(4) 字體層級清不清楚（主張大 / 副標小）？",
        "swap_table": [
            ("ⓐ 主張句 = ?（≤ 8 字、英文）", "例：Slow is Better / Less is More / Stay Curious"),
            ("ⓑ anchor 視覺 = ?（單一元素）", "例：咖啡杯線稿 / 茶葉 / 麥穗 / 抽象幾何"),
            ("ⓒ 色板 = ?（≤ 3 色）", "例：米白＋深棕＋燙金（咖啡）／米白＋深綠＋金（茶）／純白＋黑＋紅（簡約）"),
        ],
        "pitfalls": [
            {"t": "塞太多視覺元素", "d": "AI 自動加咖啡豆、葉片、蒸氣、杯子、ribbon、星星⋯⋯通通都來。<strong>解法</strong>：明確寫「single anchor element」「max 1 visual element in center」「whitespace ≥ 50%」三道鎖。"},
            {"t": "色板鎖不住", "d": "寫了「米白＋深棕」AI 還是給你淡藍 / 淡綠陰影。<strong>解法</strong>：明確寫「strictly 2-color palette: cream white #F5F0E8 + dark brown #3A2A1F」、「no other colors anywhere」。"},
            {"t": "字體混搭過多", "d": "標題用 serif、副標用 sans、結果 AI 又自動加第 3 個 script 字。<strong>解法</strong>：明確寫「only 2 typefaces: bold serif for main + light sans for sub」、避免 script / display / decorative。"},
            {"t": "中文海報主張別指望 prompt 解決", "d": "imagegen 對中文字體只給新細明體系。<strong>A3 的最佳策略</strong>：英文版海報用 imagegen 直出（如「Slow is Better」），中文版（「慢，才是更好」「日子緩慢，咖啡專注」）走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline;font-weight:700\">後製字體疊圖工作流附錄</a> 在 Figma 疊上「金萱半糖粗體」級別字體。<br><br><strong>實戰提醒</strong>：A3 brand poster 是文青客戶最在意「字體調性」的卡片——他們要的就是「金萱／源樣明體」那種台灣文青感。Figma 後製疊字是 A3 的標準流程、不要嘗試一次到位。"},
        ],
        "prev_file": "CH6-A2.html", "prev_label": "上一張 A2",
        "next_file": "CH6-A4.html", "next_label": "下一張 A4",
        "meta_desc": "單張品牌海報模板速查：克制單一視覺、品牌個性視覺名片、咖啡店與文青選物店首選。",
    },
    {
        "id": "A4", "title": "Editorial Cover 雜誌 / 報告封面",
        "source_md": "poster-and-campaigns/editorial-cover.md",
        "tagline": "雜誌封面、品牌年度報告封面、電子書封面、訂閱電子報每月封面。直立 2:3 構圖、強標題＋小字目錄＋作者標、有「翻開來看的衝動」。文青品牌、自媒體創作者、企業內部刊物最高頻。",
        "outcomes": ["能判斷何時用 editorial cover（與 A3 海報、A2 KV 的差異）", "能拆解 6 段並產出有「想翻開」感的封面", "能識別 4 種踩雷（標題不夠 strong／副題太密／封底元素跑進來／作者名遮 anchor）"],
        "intro": "雜誌 / 報告 / 電子書封面。直立 2:3 構圖、上方 1/3 是大標題、中間 1/2 是 anchor visual、下方 1/6 是小字目錄與作者標。視覺要「讓人想翻開來看」。",
        "use_cases": [
            {"t": "個人 Substack / Notion 每月電子報封面", "d": "創作者經營訂閱"},
            {"t": "品牌年度報告 / 季度觀察封面", "d": "工作室自家出版品"},
            {"t": "Pinkoi / 嘖嘖 募資封面", "d": "群募活動主圖"},
            {"t": "獨立出版 / 自費電子書封面", "d": "Amazon KDP / Pubu 上架"},
        ],
        "compare_table": [
            ("構圖", "直立 2:3、上中下三段式", "A1：橫 21:9；A3：留白海報；A2：多比例延展"),
            ("標題", "<strong>必有</strong>大字標題", "A3：主張句；A2：claim"),
            ("副題 / 目錄", "常含、列出本期重點", "其他模板：通常無"),
            ("作者標", "通常含（小字、底部）", "其他模板：無"),
            ("anchor visual", "中央、占畫面 40-50%", "A3：≤ 15%；A1：右側 60%"),
            ("使用場景", "印刷 + 數位封面", "A1：純數位；A3：可印刷單張"),
        ],
        "judge": "客戶問「我這份報告 / 雜誌 / 電子書封面怎麼做」走 A4；問「精神主張海報」走 A3；問「campaign 主圖」走 A2。<strong>A4 是自媒體創作者最常需要的卡片</strong>——每月電子報封面 NT$1500-3000 一張、可長期合作。",
        "decompose_intro": "editorial cover 6 段。<strong>核心難度在「標題層級 + anchor 平衡」</strong>——標題太大蓋住 anchor、anchor 太大壓縮標題：",
        "six_segments": [
            {"name": "刊物定位 + 期數", "need": "<strong>必問</strong>", "fill": "刊物名 + 第 N 期 / 月份；刊物個性（嚴肅 / 文青 / 商業 / 學術）"},
            {"name": "主標題", "need": "<strong>必問</strong>", "fill": "本期主題、≤ 8 字、英文優先；置上方 1/3"},
            {"name": "副題 / 目錄", "need": "可預設", "fill": "本期 3-5 個副題 / 文章標題（細體、小字、列點）"},
            {"name": "anchor visual", "need": "<strong>必問</strong>", "fill": "中央元素（產品 / 概念圖 / 抽象藝術）；占畫面 40-50%"},
            {"name": "作者 / 出版資訊", "need": "可預設", "fill": "底部小字：作者 / 工作室名 + 期數 + 日期"},
            {"name": "constraints 限制", "need": "固定寫死", "fill": "禁忌：標題遮 anchor、副題列點 ＞ 5 個、字體超過 2 種、淘寶廣告風"},
        ],
        "mnemonic": "刊物 → 標題 → 副題 → anchor → 作者 → 禁。<strong>新手最常副題太密</strong>——列了 8-10 個本期文章，封面變目錄頁。要明確寫「副題 ≤ 5 點、各 ≤ 6 字」。",
        "demo_intro": "下面這張是「弄一下工作室年度品牌觀察報告 2026」封面。直立 2:3、上方大標、中央 anchor 視覺、下方副題列點 + 作者。讓人想立刻打開閱讀的視覺感。",
        "image_path": "v54-a4-editorial-cover.png",
        "image_alt": "弄一下工作室 2026 年度品牌觀察報告封面、直立 2:3 構圖、上方 STUDIO QUARTERLY 大字標題與 No.04 期數、中央咖啡豆袋 anchor visual、下方副題列點 Brand Trends Coffee Stories Founder Notes、底部小字 by Studio NeoNeo 2026 Spring",
        "caption": "本封面標題「STUDIO QUARTERLY」與副題列點全英文——延續 A 組規避中文字體限制策略。中文版（譬如「弄一下季刊」）走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline\">後製字體疊圖工作流</a> 用「金萱半糖粗體」疊上。",
        "prompt_label": "工作室年度報告封面 STUDIO QUARTERLY",
        "prompt_full": """請生成一張雜誌 / 年度報告封面（editorial cover）：

【刊物定位】「STUDIO QUARTERLY」（個人工作室季刊、文青嚴肅、半商業半文化）

【尺寸與構圖】直立 2:3、A4 雜誌封面比例、上中下三段式排版。

【上方 1/3】
- 大字標題：「STUDIO QUARTERLY」（無襯線粗體、深棕、置中）
- 期數：「No. 04 · 2026 Spring」（細體、淺棕、標題下方）

【中央 1/2 · anchor visual】OPEN BEANS 200g 咖啡豆袋（深棕牛皮紙、米白標籤、置中、占畫面 40%）+ 散落 3 顆咖啡豆於底部

【下方 1/6 · 副題列點】細體小字、左對齊：
- Brand Trends 2026
- Coffee Stories from Taipei
- Founder Notes · Issue 04
- Slow Living Index

【底部 · 作者標】極小字置中：「by Studio NeoNeo · 2026 Spring · Issue 04」

【背景】奶白漸變底（#F5F0E8 上 → #E8E0D0 下）、極淺絲絨紋理、無雜物。

【字體】2 種：標題用無襯線粗體、副題用無襯線細體。全英文。

【色板】嚴格 3 色：米白底 + 深棕主 + 燙金 accent（用於分隔線）。

【限制】嚴禁人物、嚴禁副題超過 5 點、嚴禁字體超過 2 種、嚴禁鮮艷色、嚴禁中文字、嚴禁標題遮 anchor、嚴禁封底元素（出版社 logo / 條碼 / 定價）跑進來。""",
        "read_4_points": "(1) 上中下三段式比例對不對（1/3 + 1/2 + 1/6）？(2) anchor 跟標題有沒有打架？(3) 副題列點是不是 ≤ 5 點？(4) 是不是有「想翻開」的衝動感？",
        "swap_table": [
            ("ⓐ 刊物名 + 期數 = ?", "例：STUDIO QUARTERLY No.04 / 弄一下季刊 第 4 期"),
            ("ⓑ 副題列點 3-5 個 = ?", "例：本期 3 篇主文 + 1 個專欄 + 1 個投稿區"),
            ("ⓒ anchor visual = ?", "例：產品（咖啡豆袋）／概念圖（一張地圖）／插畫（線稿人物）"),
        ],
        "pitfalls": [
            {"t": "標題壓住 anchor", "d": "標題字級放太大、整個蓋住中央 anchor visual。<strong>解法</strong>：明確寫「標題佔畫面寬度 60%、垂直位置在上方 1/3 內」、避免「giant」「huge」這類字。"},
            {"t": "副題列點過多", "d": "客戶想塞 8 篇文章在封面、結果封面變目錄。<strong>解法</strong>：明確寫「副題 max 5 items, each ≤ 6 words」、超過的放裡面目錄頁。"},
            {"t": "封底元素誤入", "d": "AI 自動加條碼、ISBN、出版社 logo、定價標籤——這些是封底的活。<strong>解法</strong>：constraints 加「no barcode, no ISBN, no publisher logo, no price tag」。"},
            {"t": "中文標題別指望 prompt 解決", "d": "imagegen 對中文字體只給新細明體系。<strong>A4 的最佳策略</strong>：英文版用 imagegen 直出（STUDIO QUARTERLY），中文版「弄一下季刊」「年度品牌觀察」用 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline;font-weight:700\">後製字體疊圖工作流附錄</a> 在 Figma 疊上「金萱粗體」級別字體。<br><br><strong>實戰提醒</strong>：A4 editorial cover 客戶都是創作者 / 文青品牌 / 自媒體、他們對字體跟其他人都更挑剔。<strong>預設「英文 placeholder + Figma 後製疊中文」是 A4 的標準工作流</strong>。"},
        ],
        "prev_file": "CH6-A3.html", "prev_label": "上一張 A3",
        "next_file": "CH6-A5.html", "next_label": "下一張 A5",
        "meta_desc": "雜誌 / 年度報告封面模板速查：直立 2:3、上中下三段式、有想翻開來看的衝動。",
    },
    {
        "id": "A5", "title": "Brand Identity Board 品牌識別 mood board",
        "source_md": "branding-and-packaging/brand-identity-board.md",
        "tagline": "把一個品牌的 logo / 配色 / 字體 / 應用範例 / 風格參考一頁攤平、給客戶看「整個品牌世界觀」。提案會議用、設計交付用、作品集用、品牌手冊封面用。",
        "outcomes": ["能判斷何時用 brand identity board（與其他卡片差異）", "能拆解 6 段並產出可給客戶看的品牌識別總覽", "能識別 4 種踩雷（資訊太密／層級不清／應用範例不真實／配色卡跑掉）"],
        "intro": "一張 brand board 把品牌識別系統的所有元素攤平：logo（4 個變體）+ 主副配色（3-5 色）+ 字體（標題＋內文）+ 應用範例（名片、瓶身、貼紙、IG）+ 風格氛圍照（mood image）。客戶看一眼就知道這是什麼品牌。",
        "use_cases": [
            {"t": "客戶提案 / 比稿用", "d": "1 張圖看完整個品牌方向"},
            {"t": "個人 portfolio 作品集頁面", "d": "「我幫客戶 X 做的 brand board」"},
            {"t": "品牌手冊封面 / brand book 第一頁", "d": "後續分章詳述"},
            {"t": "工作室年度回顧 / 案例展", "d": "1 年做了 N 個 brand 一覽"},
        ],
        "compare_table": [
            ("資訊密度", "<strong>最高</strong>（含 logo + 色 + 字 + 應用 + mood）", "其他卡片：單一視覺"),
            ("用途", "提案 / 內部 brand book / 作品集", "A1-A4：對外行銷"),
            ("分區", "通常 4-6 區塊、grid 排版", "其他：單一構圖"),
            ("文字密度", "中等（每區小標 + 簡短說明）", "A3：克制；A4：標題 + 副題"),
            ("讀者", "設計師 / 品牌主 / 內部團隊", "A1-A4：終端消費者"),
            ("產出難度", "高（多區塊一致性最考驗）", "A3：低；A1：中"),
        ],
        "judge": "客戶問「能不能給我看一頁的品牌總覽」走 A5；問「對外行銷主圖」走 A1-A4；問「給設計師看 brand guideline」走 A5。<strong>A5 是接案 portfolio 必備</strong>——客戶看完更願意出更高預算。",
        "decompose_intro": "brand identity board 6 段。<strong>核心難度在「分區一致性」</strong>——每個區塊獨立看都要好、合在一起又要看得出是同一品牌：",
        "six_segments": [
            {"name": "brand 定位區", "need": "<strong>必問</strong>", "fill": "品牌名 + 1 句 mission statement + 個性形容詞 3-5 個"},
            {"name": "logo system", "need": "<strong>必問</strong>", "fill": "主 logo + 圖標版 + 單色版 + 反白版（4 變體）"},
            {"name": "color palette", "need": "<strong>必問</strong>", "fill": "主色 1-2 + 副色 2-3 + accent 1，每色含 HEX + 用途說明"},
            {"name": "typography", "need": "<strong>必問</strong>", "fill": "標題字 + 內文字 + 強調字（3 種）；含字體名 + 字級範圍"},
            {"name": "applications 應用範例", "need": "選用", "fill": "名片 + 瓶身 / 包裝 + 貼紙 + IG 貼文 mockup"},
            {"name": "mood image 氛圍照", "need": "選用", "fill": "1 張代表品牌氣質的攝影或抽象視覺"},
        ],
        "mnemonic": "定位 → logo → 色 → 字 → 應用 → mood。<strong>新手最常忽略「應用範例的真實性」</strong>——logo 印在卡片上要有真實的紙張紋理、印在瓶身要有實際的反光。明確寫「realistic mockup textures」「show in actual context」。",
        "demo_intro": "下面這張是 OPEN BEANS 完整 brand identity board——一頁看完整個品牌世界觀。客戶看完直接點頭付費 NT$50000+ brand identity 案。",
        "image_path": "v55-a5-brand-identity-board.png",
        "image_alt": "OPEN BEANS 品牌識別 brand identity board、6 區塊網格排版、左上品牌名與 mission 定位區、右上 logo 4 變體（主版水平、圖標、單色、反白）、左中色板 4 色含 HEX、右中字體系統 3 級、左下名片與咖啡豆袋應用 mockup、右下文青咖啡店氛圍照、整體米白底深棕燙金三色板",
        "caption": "本 brand board 全英文（OPEN BEANS / Single-Origin Coffee, Slow Roasted）——延續 A 組規避中文字體策略。中文 brand identity（譬如「弄一下工作室」識別系統）走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline\">後製字體疊圖工作流</a>。",
        "prompt_label": "OPEN BEANS 品牌識別 brand board",
        "prompt_full": """請生成一張完整的品牌識別 brand identity board：

【整體構圖】橫式 16:9、6 區塊 grid 排版（2 列 × 3 欄）、整體像「設計師交付給客戶看的 brand book 第一頁」。

【品牌】OPEN BEANS（精品咖啡品牌、強調 single-origin + slow roasted + Taipei-based）

【區塊 1（左上）· 品牌定位】
- 大字 brand name：「OPEN BEANS」（無襯線粗體、深棕）
- mission：「Single-Origin Coffee, Slow Roasted in Taipei」（細體、淺棕）
- 個性 keywords：「Quiet · Honest · Considered」（極小字、列三點）

【區塊 2（右上）· logo system 4 變體】
- 主 logo（橫式組合）
- 圖標版（線稿咖啡杯）
- 單色版
- 反白版（深棕底 + 米白 logo）

【區塊 3（左中）· color palette】
- 主色 1：Deep Brown #3A2A1F
- 主色 2：Cream White #F5F0E8
- 副色：Warm Sand #D4C4B0
- accent：Brass Gold #B89968
（每色含色塊 + HEX 標示）

【區塊 4（右中）· typography】
- Heading：「Shippori Mincho Bold · 32-48px」（樣字示例）
- Body：「Noto Sans · Regular 14-16px」（樣字示例）
- Accent：「Italic Light · for tagline」（樣字示例）

【區塊 5（左下）· applications mockup】
- 名片正面（mockup with paper texture）
- 200g 咖啡豆袋
- IG 貼文方圖

【區塊 6（右下）· mood image】文青咖啡店一角的氛圍照（小、虛化、暖光）

【整體色板】嚴格三色：米白底 + 深棕主 + 燙金 accent。

【字體】全英文、僅 2 種字體：襯線粗體（標題）+ 無襯線細體（內文）。

【限制】嚴禁人物（mood image 內也不要有臉）、嚴禁區塊互相搶戲、嚴禁字體超過 2 種、嚴禁色板超過 4 色、嚴禁中文字、嚴禁區塊邊框（用空白分隔即可）。""",
        "read_4_points": "(1) 6 區塊比例對不對（每區大小相當）？(2) logo 4 變體都看得出是同一個 logo 嗎？(3) 色板 HEX 標示清不清楚？(4) 應用 mockup 有沒有真實感（紙張紋理 / 包裝光影）？",
        "swap_table": [
            ("ⓐ 品牌名 + mission = ?", "例：OPEN BEANS · Single-Origin Coffee / 弄一下工作室 · 課程設計"),
            ("ⓑ 配色 = ?（主 1-2 + 副 2-3 + accent 1）", "例：深棕＋米白＋砂色＋燙金（咖啡）／墨綠＋米白＋金（茶）"),
            ("ⓒ 應用範例 = ?", "例：名片＋包裝＋IG（電商）／卡片＋海報＋EDM（自媒體）"),
        ],
        "pitfalls": [
            {"t": "資訊太密、區塊看不清", "d": "AI 把所有元素塞滿、區塊邊界模糊、客戶看不出哪是哪。<strong>解法</strong>：明確寫「6-grid layout, generous whitespace between sections, no borders」、區塊間留 5% 空白。"},
            {"t": "logo 變體不一致", "d": "主 logo 是 sans serif、圖標版 AI 給你 script 風——4 個變體像不同品牌。<strong>解法</strong>：明確寫「all 4 logo variants must share same typography and visual DNA」「only color and arrangement varies」。"},
            {"t": "應用 mockup 不真實", "d": "名片 mockup 像 PowerPoint 模板、不像真的印刷品。<strong>解法</strong>：明確寫「realistic mockup with paper texture, soft shadows, slight perspective」、避免「flat illustration」。"},
            {"t": "中文 brand identity 一律後製", "d": "imagegen 對中文字體只給新細明體系。<strong>A5 的最佳策略</strong>：用英文 brand name + mission 跑 imagegen、再用 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline;font-weight:700\">後製字體疊圖工作流附錄</a>。<br><br><strong>實戰提醒</strong>：A5 brand board 是「給其他設計師看」的——同行對字體最敏感、新細明體 brand book 一秒被識破。<strong>Figma 用 component 一次設計、所有應用 mockup 自動套同字體、效率最高</strong>。"},
        ],
        "prev_file": "CH6-A4.html", "prev_label": "上一張 A4",
        "next_file": "CH6-A6.html", "next_label": "下一張 A6",
        "meta_desc": "品牌識別 board 模板速查：logo + 色 + 字 + 應用一頁攤平、提案 portfolio 必備。",
    },
    {
        "id": "A6", "title": "Bilingual Layout 中英雙語版面",
        "source_md": "typography-and-text-layout/bilingual-layout-visual.md",
        "tagline": "中英雙語並列排版的視覺。台灣品牌 / 機構 / 活動最常需要——對外要有國際感（英文）、對內要有本土親切感（中文）。兩廳院、松菸、文化部活動、雙語網站 hero、雙語商品標籤都會用。",
        "outcomes": ["能判斷何時用雙語版面（與單語模板差異）", "能拆解 6 段並安排兩種語言的視覺重量比", "能識別 4 種踩雷（兩語同等大小／字體不對／斷行不對／文化轉換失敗）"],
        "intro": "中英雙語並列的版面。台灣有國際觀眾的活動、機構、品牌都需要這種視覺。重點是「主導語要明確」（不能兩個都同等大小）、「字體配對」（中文用襯線、英文也用襯線；中文黑體、英文 sans）、「斷行對齊」（兩語逐行對應）。",
        "use_cases": [
            {"t": "兩廳院 / 松菸 / 高美館 活動視覺", "d": "公部門 / 文化機構雙語必須"},
            {"t": "外商在台分公司活動主圖", "d": "Apple / Google / IKEA 在台辦活動"},
            {"t": "雙語品牌官網 hero", "d": "新創、設計品牌、文創精品"},
            {"t": "雙語商品標籤 / 包裝", "d": "出口型本地品牌 / 文創商品"},
        ],
        "compare_table": [
            ("語言層級", "<strong>必須</strong>主導 + 副從", "其他模板：單一語言"),
            ("字體配對", "中文＋英文必須調性一致", "其他：單一字體系統"),
            ("斷行", "兩語逐行對應、視覺平衡", "其他：自由排版"),
            ("使用場景", "公部門 / 文化 / 雙語品牌", "其他：商業 B2C"),
            ("文化轉換", "不只翻譯、要在地化", "其他：單一語境"),
            ("產出難度", "高（中英排版美學最難）", "其他：中"),
        ],
        "judge": "客戶問「我的活動有外國觀眾」走 A6；問「我們是出口型品牌」走 A6；問「公部門活動」走 A6。<strong>A6 是文化機構接案的入場券</strong>——一個雙語視覺案 NT$8000-20000、且機構通常一年多次合作。",
        "decompose_intro": "bilingual layout 6 段。<strong>核心難度在「主從關係」</strong>——客戶常想「兩個語言一樣重要」、但視覺上必須有主從、否則兩個都看不清：",
        "six_segments": [
            {"name": "主導語 vs 副從語", "need": "<strong>必問</strong>", "fill": "主導（70% 視覺重量）+ 副從（30%）；通常台灣場合中文主、英文副；對外場合反之"},
            {"name": "中文字體", "need": "<strong>必問</strong>", "fill": "標題：金萱 / 思源宋體粗 / 文鼎晶熙黑；內文：思源黑體 / Noto Sans TC"},
            {"name": "英文字體", "need": "<strong>必問</strong>", "fill": "與中文「調性對應」：中文襯線→英文 serif；中文黑體→英文 sans"},
            {"name": "排版方式", "need": "<strong>必問</strong>", "fill": "並排 / 上下 / 左中右三段；兩語逐行對應；視覺重量平衡"},
            {"name": "文化轉換", "need": "選用", "fill": "不只翻譯——「精緻」可譯 refined / curated / considered 各帶不同氣質"},
            {"name": "constraints 限制", "need": "固定寫死", "fill": "禁忌：兩語同等大小、字體調性不對、斷行不對齊、直譯生硬"},
        ],
        "mnemonic": "主從 → 中字 → 英字 → 排版 → 文化 → 禁。<strong>新手最常踩「兩語同等大小」</strong>——客戶說「兩個都重要」設計師就把字級設一樣，結果兩個都看不清。視覺上一定要有 70/30 主從。",
        "demo_intro": "下面這張是松菸文創園區「Slow Living 慢工作坊」雙語活動主視覺。中文主導（70%）+ 英文副從（30%）、字體配對精準（金萱粗 + Playfair Display）、斷行對齊。",
        "image_path": "v56-a6-bilingual-layout.png",
        "image_alt": "松菸文創 Slow Living 慢工作坊雙語活動視覺、上方中文主標慢工作坊大字配金萱粗體、下方英文副標 Slow Living Workshop 配 Playfair Display 細襯線、中央咖啡與植物道具、米白底深棕字色板、兩語逐行對應視覺重量 70 30 主從關係",
        "caption": "本圖中文「慢工作坊」用金萱粗體、英文「Slow Living Workshop」用 Playfair Display 細襯線、調性配對精準。imagegen 對中文「慢工作坊」字體仍給新細明體系——本圖實際走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline\">後製字體疊圖工作流</a> 用金萱字體在 Figma 後製疊上。",
        "prompt_label": "松菸 Slow Living 雙語活動視覺",
        "prompt_full": """請生成一張中英雙語活動視覺：

【主題】松菸文創園區 · Slow Living Workshop 慢工作坊系列

【主從關係】中文主導（70% 視覺重量）+ 英文副從（30%）

【中文（主）】
- 大字標題：「慢工作坊」（4 字、金萱粗體質感、深棕、置中）
- 副標：「在松菸的午後，我們重新學會慢」（細體、淺棕、置中）
- ※ 標籤上的中文字本就是 imagegen 弱項——本提示詞主要驗構圖、實際交付用 Figma 後製疊金萱體中文。

【英文（副）】
- 副標題：「Slow Living Workshop」（Playfair Display 細襯線、米白色、置中、字級為中文標題的 50%）
- 副副標：「Saturday afternoons at Songshan Cultural Park」（無襯線細體、極小、置中）

【視覺】中央 anchor visual：一杯手沖咖啡 + 一盆極簡綠植 + 一本翻開的書（從上方俯拍、構圖簡潔）

【背景】奶白漸變底（米白上 → 暖砂下）、輕微紙質紋理。

【字體配對】中文襯線（金萱粗）→ 英文襯線（Playfair Display）、調性一致。

【色板】嚴格 3 色：米白底 + 深棕字 + 燙金 accent（用於分隔線）。

【限制】嚴禁人物、嚴禁中英文同等大小（必有 70/30 主從）、嚴禁字體調性不對應（譬如中文襯線配英文 sans）、嚴禁鮮艷色、嚴禁兩語斷行不對齊。""",
        "read_4_points": "(1) 中英主從關係明確嗎（一個顯然主、一個顯然副）？(2) 字體調性配對嗎（中襯英襯 / 中黑英 sans）？(3) 兩語斷行有沒有對齊？(4) 文化轉換有沒有「在地感」？",
        "swap_table": [
            ("ⓐ 主導語 = ?（中或英）", "例：中文主（公部門 / 在地活動）／英文主（外商 / 國際會議）"),
            ("ⓑ 字體配對 = ?", "例：金萱粗＋Playfair（文青）／思源黑＋Helvetica（商業）"),
            ("ⓒ 排版方式 = ?", "例：上下並排（最常用）／左右並排（雙語標籤）／三段式（標題＋副題＋細節）"),
        ],
        "pitfalls": [
            {"t": "兩語同等大小", "d": "客戶說「兩個都重要」、設計師就 50/50、結果都不夠突出。<strong>解法</strong>：明確寫「primary language at 70% visual weight, secondary at 30%」、解釋給客戶「主從不等於不重要」。"},
            {"t": "字體調性不對應", "d": "中文金萱粗（襯線）配英文 Helvetica（sans）= 視覺不協調。<strong>解法</strong>：明確寫「Chinese serif must pair with English serif (Playfair / Garamond)」、「Chinese sans (Source Han Sans) pair with English sans (Inter / Helvetica)」。"},
            {"t": "斷行不對齊", "d": "中文 4 字、英文翻譯成 8 字、視覺重量不對等。<strong>解法</strong>：英文翻譯時主動縮減（「慢工作坊」→ Slow Workshop 而非 The Slow Living Workshop Series）、必要時調整字級補償。"},
            {"t": "中文字體限制 + 文化轉換", "d": "imagegen 中文字體限制 + 文化在地化雙重挑戰。<strong>A6 的最佳策略</strong>：英文用 imagegen 直出、中文走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline;font-weight:700\">後製字體疊圖工作流附錄</a> 用金萱／思源宋／Noto Serif TC 後製疊上。<br><br><strong>實戰提醒</strong>：A6 是 A 組裡<strong>最依賴後製疊字</strong>的卡片——因為核心價值就是「中文字體調性」。<strong>跟客戶溝通時直接講白：「imagegen 給你構圖跟英文、中文金萱我用 Figma 後製疊上」</strong>，客戶（尤其文化機構）通常理解。"},
        ],
        "prev_file": "CH6-A5.html", "prev_label": "上一張 A5",
        "next_file": "CH6-C1.html", "next_label": "進入 C 組 C1",
        "meta_desc": "中英雙語版面模板速查：主從關係明確、字體調性配對、文化機構與雙語品牌必用。",
    },

    # ----- C 組 內容創作 -----
    {
        "id": "C1", "title": "Bento Grid 便當格資訊圖",
        "source_md": "infographics/bento-grid-infographic.md",
        "tagline": "把多個資訊塊用「便當格 grid」排版的視覺。日本 bento 美學被 IG / Threads / 小紅書帶起後變成最熱門的資訊圖類別。一格一個 takeaway、整體有節奏感。健身教練、理財顧問、自媒體創作者最常用。",
        "outcomes": ["能判斷何時用 bento grid（與其他資訊圖差異）", "能拆解 6 段並安排 4-9 格的資訊節奏", "能識別 4 種踩雷（每格內容失衡／格數太多／字體大小亂／格間距不對）"],
        "intro": "bento grid（便當格）資訊圖。把 4-9 個資訊塊按日本便當盒美學排版——大格 + 小格交錯、不對稱但平衡、每格有獨立 takeaway、整體有閱讀節奏。IG 多圖貼文、Threads 圖文、小紅書教學圖最高頻。",
        "use_cases": [
            {"t": "個人 IG / Threads 教學圖", "d": "健身、理財、料理、設計教學"},
            {"t": "品牌週刊 / 月刊重點整理", "d": "本月 5 大趨勢 / 重要新聞"},
            {"t": "活動結束 / 課程結束 highlight", "d": "用 6 格回顧整個活動"},
            {"t": "Notion / Substack 訂閱主視覺", "d": "週六固定欄位"},
        ],
        "compare_table": [
            ("排版", "不對稱 grid（大格 + 小格交錯）", "C2：對比兩欄；C3：垂直步驟"),
            ("資訊密度", "中（每格 1 個 takeaway）", "C2：兩個比較；C3：5 步驟"),
            ("讀者掃描方式", "跳躍式（哪格先看自由）", "C3：必須順序讀"),
            ("適用內容", "並列重點、不分先後", "C2：必須二元；C3：必須序列"),
            ("產出比例", "通常 1:1 或 4:5", "C3：4:5 或 9:16；C2：1:1"),
            ("使用平台", "IG / Threads / 小紅書", "其他：通用"),
        ],
        "judge": "客戶問「IG 教學圖怎麼做」走 C1；問「兩個東西的對比」走 C2；問「分步驟教程」走 C3。<strong>C1 是個人創作者最高頻的資訊圖卡片</strong>——一張 bento grid 接案 NT$1500-3000、月固定可接 5-10 張。",
        "decompose_intro": "bento grid 6 段。<strong>核心難度在「格的節奏」</strong>——9 格平均切＝無聊、4 大格＝太空、要有大小交錯：",
        "six_segments": [
            {"name": "topic 主題", "need": "<strong>必問</strong>", "fill": "整張圖的主題（≤ 8 字）+ 標題位置（左上 / 中央橫幅）"},
            {"name": "grid system", "need": "<strong>必問</strong>", "fill": "格數（4 / 6 / 9）+ 大小比例（1 大 + 4 小、2 大 + 4 小、3 等大 + 6 小⋯⋯）"},
            {"name": "block contents", "need": "<strong>必問</strong>", "fill": "每格的 takeaway（≤ 8 字標題 + 1-2 句說明）"},
            {"name": "visual elements", "need": "選用", "fill": "每格的 icon / 數字 / 小插畫；圖文比例（純文字 / 文字 + icon / 文字 + 大數字）"},
            {"name": "color system", "need": "<strong>必問</strong>", "fill": "底色（米白 / 灰 / 暖色）+ 強調色（≤ 2 色）；每格不要不同色（會散）"},
            {"name": "constraints 限制", "need": "固定寫死", "fill": "禁忌：每格內容字數不平衡、格間距不對（要 2-4% 畫面寬）、字體超過 2 種、每格用不同色"},
        ],
        "mnemonic": "主題 → 格 → 內容 → 視覺 → 色 → 禁。<strong>新手最常 9 格平均切</strong>——bento 的精髓是「不對稱平衡」。明確寫「one large block at top-left, smaller blocks around it」「2:1 size ratio between main and sub blocks」。",
        "demo_intro": "下面這張是「2026 春季 5 大咖啡趨勢」bento grid。1 大格（趨勢 1）+ 4 小格（趨勢 2-5）、米白底深棕字、每格有 icon + 短標題 + 說明。適合 IG 教學貼文。",
        "image_path": "v57-c1-bento-grid.png",
        "image_alt": "5 大咖啡趨勢 bento grid 資訊圖、IG 4:5 直立構圖、上方 Coffee Trends Spring 2026 標題、左大格 Cold Brew Subscription 趨勢 1 配冰滴壺 icon、右側小格 Single-Origin Lab Beans Hand-poured Roast Tracking 4 小格、米白底深棕字燙金 accent",
        "caption": "本圖所有英文標題、icon、說明均為英文——延續規避中文字體限制策略。中文版「5 大咖啡趨勢」「冷萃訂閱」走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline\">後製字體疊圖工作流</a> 在 Figma 疊上「金萱半糖」中文。",
        "prompt_label": "2026 春季 5 大咖啡趨勢 bento grid",
        "prompt_full": """請生成一張 bento grid 資訊圖（日本便當格美學）：

【整體】4:5 直立比例、適合 IG / Threads 貼文。

【主題】「Coffee Trends Spring 2026」（畫面頂部標題、無襯線粗體、深棕、置中）

【grid 系統】2 大 + 3 小不對稱排版：
- 左上大格（占畫面左側 1/2）
- 右上 + 右中 + 右下 3 個小格（每格約大格 1/3 高）
- 底部橫向 1 個中格（占畫面寬度 100%）

【格內容】每格含：icon（極簡黑線繪、≤ 3 條線）+ 標題（無襯線粗體）+ 1-2 行說明（無襯線細體）：
- 大格 #01：「Cold Brew Subscription」+ 冰滴壺 icon + 「Slow brew, mailed weekly」
- 小格 #02：「Single-Origin Lab」+ 試管 icon + 「Trace every bean」
- 小格 #03：「Hand-poured at Home」+ 濾杯 icon + 「Skill is the gift」
- 小格 #04：「Roast Tracking」+ 日曆 icon + "Within 7 days"
- 底部中格 #05：「Subscribe to Try All Five Trends — Save 25% This Spring」（CTA banner）

【色板】嚴格 3 色：米白底 + 深棕字（標題與 icon）+ 燙金 accent（CTA banner 邊框）。每格用同一個底色（米白）、不要每格不同色。

【字體】2 種：標題用無襯線粗體、說明用無襯線細體。全英文。

【格間距】格與格之間留 3% 畫面寬度的白色 gutter。

【限制】嚴禁人物、嚴禁每格內容字數不平衡（每格說明都要 1-2 行）、嚴禁字體超過 2 種、嚴禁每格用不同色、嚴禁中文字、嚴禁 icon 過於繁複（≤ 3 條線）。""",
        "read_4_points": "(1) 大格 vs 小格的比例對不對（2:1 size ratio）？(2) 每格內容字數有沒有平衡（不要 1 格塞 30 字另格塞 5 字）？(3) icon 是不是「極簡 3 線」級別？(4) 整體色板是不是 ≤ 3 色？",
        "swap_table": [
            ("ⓐ 主題 + 格數 = ?", "例：5 大趨勢（1 大 + 4 小）／3 個重點（3 等大）／6 個 tips（2 大 + 4 小）"),
            ("ⓑ 每格 takeaway = ?（≤ 8 字標題）", "例：Cold Brew / Single-Origin Lab / Hand-poured"),
            ("ⓒ 色板 + icon 風格 = ?", "例：米白＋深棕＋極簡線稿（文青）／純白＋黑＋幾何 icon（科技）"),
        ],
        "pitfalls": [
            {"t": "9 格平均切、無節奏感", "d": "客戶想塞 9 個重點、設計師 3×3 平均切——結果像 PPT 表格不像 bento。<strong>解法</strong>：明確寫「asymmetric grid: 1 large + N smaller blocks」「visual hierarchy through size, not just content」。"},
            {"t": "每格內容字數不平衡", "d": "1 格塞 50 字、另格塞 5 字——視覺重量打架。<strong>解法</strong>：明確寫「each block: title ≤ 8 words + description 1-2 lines」、超過就分成兩格。"},
            {"t": "icon 過於繁複", "d": "AI 給你寫實插畫 icon、整張圖變兒童繪本。<strong>解法</strong>：明確寫「minimalist line icon, ≤ 3 strokes per icon, monochrome」。"},
            {"t": "中文 bento grid 文字一律後製", "d": "imagegen 中文字體限制。<strong>C1 的最佳策略</strong>：英文版用 imagegen 直出（如示範圖）、中文版（「冷萃訂閱」「單品實驗室」）走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline;font-weight:700\">後製字體疊圖工作流附錄</a> 在 Figma 用「金萱半糖粗 + 思源黑體細」疊上。<br><br><strong>實戰提醒</strong>：C1 bento grid 很多客戶會做整個系列（每月一張），<strong>用 Figma 建 master component、每月只換文字內容、icon 與排版自動套用</strong>，效率最高、品質最穩。"},
        ],
        "prev_file": "CH6-A6.html", "prev_label": "上一張 A6",
        "next_file": "CH6-C2.html", "next_label": "下一張 C2",
        "meta_desc": "Bento grid 資訊圖模板速查：日本便當格美學、IG / Threads / 小紅書最高頻教學圖。",
    },
    {
        "id": "C2", "title": "Comparison Infographic 對比資訊圖",
        "source_md": "infographics/comparison-infographic.md",
        "tagline": "把兩個東西並列對比的資訊圖（A vs B、好 vs 壞、舊 vs 新、訂閱 vs 一次購買）。最具說服力、最容易讓觀者有「啊我懂了」感。財務顧問、健身教練、產品經理、行銷人員最常用。",
        "outcomes": ["能判斷何時用對比圖（與 bento / 步驟圖差異）", "能拆解 6 段並安排兩欄視覺平衡", "能識別 4 種踩雷（兩欄不對稱／結論不夠強／視覺暗示偏頗／顏色語意不對）"],
        "intro": "兩欄對比資訊圖（A vs B）。重點是「視覺平衡 + 結論明確」——兩欄字級相同、項目數對齊、結論欄底部寫「所以呢」。客戶看完不會困惑、會記得。",
        "use_cases": [
            {"t": "理財顧問定存 vs ETF 對比", "d": "5 年差距用視覺說清楚"},
            {"t": "健身教練 跑步 vs 重訓 對比", "d": "幫學員選擇"},
            {"t": "PM 訂閱 vs 一次購買 對比", "d": "說服客戶選訂閱"},
            {"t": "工作室 自學 vs 上課 對比", "d": "招生 EDM 主圖"},
        ],
        "compare_table": [
            ("結構", "兩欄對比（左 vs 右）", "C1：bento grid；C3：垂直步驟"),
            ("項目對比", "<strong>必須</strong>對齊（每行兩語對應）", "C1：每格獨立"),
            ("結論", "通常底部 1 個強結論", "C1：每格獨立 takeaway"),
            ("色彩語意", "左右常用對比色（暖 vs 冷 / 弱 vs 強）", "C1：單色板"),
            ("使用場景", "說服 / 教育 / 比較", "C1：並列重點；C3：流程教學"),
            ("產出尺寸", "通常 1:1 或 4:5", "其他：通用"),
        ],
        "judge": "客戶問「我要說服客戶選 A 而不是 B」走 C2；問「並列 5 個重點」走 C1；問「分步驟教程」走 C3。<strong>C2 在「銷售型內容」最有力</strong>——一張對比圖能直接帶轉換、客戶願意付高價。",
        "decompose_intro": "對比資訊圖 6 段。<strong>核心難度在「視覺平衡」</strong>——兩欄字級不對齊、項目不對應、視覺暗示偏頗（結論已經寫在臉上）：",
        "six_segments": [
            {"name": "topic 對比主題", "need": "<strong>必問</strong>", "fill": "What vs What（簡短描述、≤ 6 字）+ 為何要比"},
            {"name": "two-column structure", "need": "<strong>必問</strong>", "fill": "左欄 = A 選項、右欄 = B 選項；標題 + 5-7 個對比項"},
            {"name": "comparison items", "need": "<strong>必問</strong>", "fill": "每行：左 = A 的特徵、右 = B 的特徵；逐行對應、字數平衡"},
            {"name": "verdict 結論", "need": "<strong>必問</strong>", "fill": "底部 1 句結論（≤ 12 字）+ CTA 引導"},
            {"name": "color semantics", "need": "可預設", "fill": "對比色：暖 vs 冷、深 vs 淺；不要紅 vs 綠（色盲不友善）"},
            {"name": "constraints 限制", "need": "固定寫死", "fill": "禁忌：兩欄字級不一、項目數不對齊、結論曖昧、色彩太刺眼、項目超過 7 個"},
        ],
        "mnemonic": "主題 → 兩欄 → 項目 → 結論 → 色 → 禁。<strong>新手最常結論曖昧</strong>——客戶要的是「所以選 B」、不是「兩個各有優點」。明確寫結論、用視覺強調（粗體 / 大字 / 對比色）。",
        "demo_intro": "下面這張是 OPEN BEANS「定額訂閱 vs 一次購買」對比圖。左欄訂閱（推薦版本、燙金強調），右欄一次購買（中性灰色），底部結論「年省 NT$2,400」+ CTA「Start Subscription」。",
        "image_path": "v58-c2-comparison.png",
        "image_alt": "OPEN BEANS 訂閱 vs 一次購買對比資訊圖、IG 4:5 直立構圖、上方 Subscribe vs One-Time Purchase 標題、左欄訂閱 5 項對比優勢配燙金強調、右欄一次購買 5 項中性灰色、底部結論 Save NT$2400 per year 配 Start Subscription CTA、米白底深棕字燙金 accent",
        "caption": "本對比圖左右視覺重量明確（左燙金強、右灰色中性）、結論明確（年省 NT$2,400）。中文版「年省 2,400」「立即訂閱」走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline\">後製字體疊圖工作流</a>。",
        "prompt_label": "OPEN BEANS 訂閱 vs 一次購買對比",
        "prompt_full": """請生成一張兩欄對比資訊圖（comparison infographic）：

【整體】4:5 直立比例、適合 IG / Threads 貼文。

【主題】「Subscribe vs One-Time Purchase」（畫面頂部標題、無襯線粗體、深棕、置中）
副標：「Why subscription wins for daily coffee drinkers」（細體、淺棕、置中）

【兩欄結構】
- 左欄（推薦欄）：「Subscription」+ 燙金邊框 + 燙金「RECOMMENDED」徽章在欄頂
- 右欄（中性欄）：「One-Time Purchase」+ 灰色邊框、無徽章

【對比項目（5 行、每行兩欄並列）】
1. Pricing：Save 15% per order（左、燙金強調）｜Full price each time（右、中性灰）
2. Freshness：Auto-shipped within 7 days of roast｜You decide when to reorder
3. Variety：Curated rotation of 4 origins｜Same beans every time
4. Convenience：Set & forget｜Manual reorder needed
5. Cost-per-year：~NT$8,400｜~NT$10,800

【結論區（底部）】粗體大字：「Save NT$2,400 per year」（燙金）+ CTA 按鈕：「Start Your Subscription」（深棕填充、米白文字）

【色板】嚴格 3 色：米白底 + 深棕字（中性對比） + 燙金 accent（強調訂閱欄）。不要紅 / 綠（色盲不友善）。

【字體】2 種：標題用無襯線粗體、項目用無襯線細體。全英文。

【限制】嚴禁人物、嚴禁兩欄字級不一、嚴禁項目超過 7 行、嚴禁結論曖昧（必有明確 winner）、嚴禁色彩刺眼、嚴禁中文字。""",
        "read_4_points": "(1) 兩欄字級對齊嗎？(2) 對比項目逐行有沒有對應（不能左欄 5 項、右欄 4 項）？(3) 結論明不明確（看完知道選哪個）？(4) 色彩語意對嗎（推薦欄 vs 中性欄視覺重量明顯）？",
        "swap_table": [
            ("ⓐ 對比主題 = ?（A vs B）", "例：訂閱 vs 一次購買 / 自學 vs 上課 / 跑步 vs 重訓"),
            ("ⓑ 對比項目 = ?（5-7 項、要逐行對應）", "例：價格 / 時間 / 效果 / 便利度 / 年省成本"),
            ("ⓒ 結論 = ?（≤ 12 字 + CTA）", "例：「Save NT$2,400 per year」+「Start Subscription」"),
        ],
        "pitfalls": [
            {"t": "兩欄項目不對齊", "d": "左欄 5 項、右欄 4 項——視覺平衡毀掉。<strong>解法</strong>：明確寫「each row must have content in both columns」「never leave a column blank」。"},
            {"t": "結論曖昧", "d": "「兩個各有優點」這種結論等於沒結論。<strong>解法</strong>：明確寫結論句子（「Save NT$2,400 per year」）+ CTA 按鈕、不要寫「choose what fits you」這種廢話。"},
            {"t": "用紅 vs 綠對比", "d": "色盲不友善、且文化暗示太強（紅＝錯）。<strong>解法</strong>：用「燙金 vs 灰」「藍 vs 灰」「深棕 vs 淺棕」這類「強調 vs 中性」對比、避免紅綠。"},
            {"t": "中文對比結論一律後製", "d": "imagegen 中文字體限制。<strong>C2 的最佳策略</strong>：英文版用 imagegen 直出（Save NT$2,400 / year）、中文版（「年省 2,400 元」「立即訂閱」）走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline;font-weight:700\">後製字體疊圖工作流附錄</a>。<br><br><strong>實戰提醒</strong>：C2 對比圖的「結論句」與「CTA 按鈕」是轉換關鍵——客戶看到「年省 2,400」會立刻心動。<strong>用 Figma 後製疊上「金萱粗體」級別的中文結論字、按鈕字體醒目度提升 2-3 倍</strong>、轉換率明顯不同。"},
        ],
        "prev_file": "CH6-C1.html", "prev_label": "上一張 C1",
        "next_file": "CH6-C3.html", "next_label": "下一張 C3",
        "meta_desc": "對比資訊圖模板速查：兩欄並列、視覺平衡、結論明確、銷售型內容首選。",
    },
    {
        "id": "C3", "title": "Step-by-Step Infographic 步驟教學圖",
        "source_md": "infographics/step-by-step-infographic.md",
        "tagline": "把一個流程拆成 3-7 個步驟、垂直或水平排列的教學圖。食譜、SOP、健身動作、保養品使用方法、操作教學最常用。重點是「視覺引導要清楚」、讀者跟著步驟做不會卡住。",
        "outcomes": ["能判斷何時用步驟圖（與 bento / 對比圖差異）", "能拆解 6 段並安排步驟視覺節奏", "能識別 4 種踩雷（步驟太多／視覺引導不清／每步動作模糊／結尾沒結論）"],
        "intro": "步驟教學圖。3-7 個步驟、每步驟一個 takeaway、視覺引導（箭頭 / 數字 / 連線）讓讀者一眼看懂順序。料理 SOP、健身動作、保養流程、咖啡沖泡、課程招生 onboarding 最高頻。",
        "use_cases": [
            {"t": "食譜教學圖", "d": "餐廳、料理 KOL、自家品牌"},
            {"t": "保養品 / 化妝品使用步驟", "d": "上架圖必備"},
            {"t": "健身動作 / 瑜伽動作教學", "d": "個人教練 IG 內容"},
            {"t": "課程 onboarding 流程", "d": "報名後 3-5 步上手"},
        ],
        "compare_table": [
            ("結構", "垂直 / 水平排列的 N 步驟", "C1：bento grid；C2：兩欄對比"),
            ("順序性", "<strong>必須</strong>順序讀（步驟 1→2→3）", "C1：跳躍式；C2：左右"),
            ("視覺引導", "<strong>必有</strong>箭頭 / 數字 / 連線", "C1：通常無；C2：欄位區隔"),
            ("步驟數量", "3-7 個（最佳 5）", "C1：4-9 格；C2：5-7 對比項"),
            ("結尾", "通常含「成果」或「驗收」", "C1：CTA banner；C2：結論句"),
            ("適用內容", "流程性 / 操作性", "C1：並列；C2：選擇"),
        ],
        "judge": "客戶問「我要教用戶怎麼做 X」走 C3；問「並列重點」走 C1；問「A vs B」走 C2。<strong>C3 對 SaaS / 課程客戶最有用</strong>——onboarding 步驟圖能直接降低客服問題。",
        "decompose_intro": "步驟教學圖 6 段。<strong>核心難度在「視覺引導」</strong>——AI 容易把每步驟做成獨立的小圖、忘了連線：",
        "six_segments": [
            {"name": "topic 教學主題", "need": "<strong>必問</strong>", "fill": "教什麼（≤ 8 字）+ 完成後得到什麼"},
            {"name": "step count 步驟數", "need": "<strong>必問</strong>", "fill": "3-7 個（最佳 5）；過多就拆兩張圖"},
            {"name": "step contents", "need": "<strong>必問</strong>", "fill": "每步：數字 / 圖標 + 動作標題（≤ 6 字）+ 1 行說明"},
            {"name": "visual flow 視覺引導", "need": "<strong>必問</strong>", "fill": "箭頭 / 連線 / 編號圈、引導讀者順序"},
            {"name": "outcome 成果", "need": "選用", "fill": "底部 1 個「完成後」視覺（成品照 / 達成圖）"},
            {"name": "constraints 限制", "need": "固定寫死", "fill": "禁忌：步驟超過 7 個、視覺引導不清、每步字數失衡、無結尾"},
        ],
        "mnemonic": "主題 → 步驟數 → 內容 → 流向 → 成果 → 禁。<strong>新手最常忽略「視覺引導」</strong>——只放 5 個並排的小圖、沒有箭頭，讀者不知道哪個先看。明確寫「numbered circles 1-5 + arrows between steps」。",
        "demo_intro": "下面這張是「手沖咖啡 5 步驟」教學圖。垂直排列、編號圈 + 箭頭引導、每步驟 1 個 icon + 標題 + 說明、底部成品咖啡杯收尾。適合咖啡品牌 EDM 教學內容。",
        "image_path": "v59-c3-step-by-step.png",
        "image_alt": "手沖咖啡 5 步驟教學圖、IG 4:5 直立構圖、上方 Hand-pour Coffee in 5 Steps 標題、垂直排列 5 步驟 Grind 磨豆 Bloom 注水悶蒸 Pour 慢注 Wait 等待 Enjoy 享用、每步驟編號圈配 icon 配標題配說明、向下箭頭連線、底部成品咖啡杯收尾、米白底深棕字燙金 accent",
        "caption": "本步驟圖每步驟有編號圈（01-05）+ 向下箭頭引導 + icon + 標題 + 說明四件套。中文版「手沖咖啡 5 步驟」「磨豆」「悶蒸」走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline\">後製字體疊圖工作流</a>。",
        "prompt_label": "手沖咖啡 5 步驟教學圖",
        "prompt_full": """請生成一張步驟教學資訊圖（step-by-step infographic）：

【整體】4:5 直立比例、適合 IG / Threads 貼文。

【主題】「Hand-pour Coffee in 5 Steps」（畫面頂部標題、無襯線粗體、深棕、置中）
副標：「From beans to cup in under 5 minutes」（細體、淺棕、置中）

【5 步驟（垂直排列、編號圈 + 向下箭頭連線）】
1. **Grind**（編號圈 01、深棕填充）+ 磨豆機 icon + 「Medium-fine, 18g for one cup」
2. **Bloom**（編號圈 02）+ 注水壺 icon + 「Pour 36ml, wait 30 seconds」
3. **Pour**（編號圈 03）+ 慢注 icon + 「Slow spiral, 60ml every 30 sec」
4. **Wait**（編號圈 04）+ 計時器 icon + 「Total brew time: 3 min 30 sec」
5. **Enjoy**（編號圈 05、燙金強調）+ 杯子 icon + 「Optimal at 60-65°C」

【視覺引導】每步驟之間有向下箭頭（深棕、極簡 2 條線）、編號圈大小一致、icon 風格統一（極簡黑線 ≤ 3 線）。

【底部成果區】小張成品咖啡杯（手沖咖啡剛沖好）+ 標題「Your Hand-pour, Done」（燙金、置中）

【色板】嚴格 3 色：米白底 + 深棕字 + 燙金 accent（用於最後一步與成果區）。

【字體】2 種：標題與步驟名用無襯線粗體、說明用無襯線細體。全英文。

【限制】嚴禁人物或人體局部、嚴禁步驟超過 5 個、嚴禁箭頭斷掉（要明顯連續引導）、嚴禁字體超過 2 種、嚴禁中文字、嚴禁 icon 過於繁複。""",
        "read_4_points": "(1) 步驟編號是不是清楚（01-05 大圓圈）？(2) 箭頭引導有沒有斷掉？(3) 每步說明字數有沒有平衡？(4) 結尾成果有沒有讓人「啊我也想做」？",
        "swap_table": [
            ("ⓐ 教學主題 + 步驟數 = ?", "例：手沖咖啡 5 步 / 健身動作 4 步 / 保養 SOP 5 步 / 上線 onboarding 3 步"),
            ("ⓑ 每步動作 + 說明 = ?", "例：磨豆 / 注水 / 慢注 / 等待 / 享用"),
            ("ⓒ 結尾成果 = ?", "例：成品咖啡 / 訓練完成圖 / 訂單確認頁 / 第一個輸出"),
        ],
        "pitfalls": [
            {"t": "步驟超過 7 個", "d": "客戶想塞 10 步驟、結果讀者看 3 步就放棄。<strong>解法</strong>：明確寫「max 5 steps, ideally 3-5」、超過就拆兩張圖、後面標「Continued」。"},
            {"t": "視覺引導斷掉", "d": "5 個步驟並排、沒有箭頭——讀者不知道從哪看起。<strong>解法</strong>：明確寫「arrows between every consecutive step」「numbered circles must be sequential and visible」。"},
            {"t": "每步動作模糊", "d": "「準備一杯」這種動作太抽象、讀者沒法跟著做。<strong>解法</strong>：每步動作要有「動詞 + 數字」（「Grind 18g」而非「Grind some beans」）。"},
            {"t": "中文步驟名一律後製", "d": "imagegen 中文字體限制。<strong>C3 的最佳策略</strong>：英文版用 imagegen 直出（Grind / Bloom / Pour），中文版（「磨豆」「悶蒸」「慢注」）走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline;font-weight:700\">後製字體疊圖工作流附錄</a>。<br><br><strong>實戰提醒</strong>：C3 步驟圖客戶很多會做「系列教學」（5 個料理 SOP / 10 個健身動作）、<strong>用 Figma 建 master component、每張只換步驟內容、編號 + 箭頭 + icon 自動套用</strong>，效率最高。"},
        ],
        "prev_file": "CH6-C2.html", "prev_label": "上一張 C2",
        "next_file": "CH6-C4.html", "next_label": "下一張 C4",
        "meta_desc": "步驟教學圖模板速查：3-7 步驟、視覺引導清楚、流程性內容首選。",
    },
    {
        "id": "C4", "title": "Founder Portrait 創辦人肖像",
        "source_md": "portraits-and-characters/founder-portrait.md",
        "tagline": "創辦人 / 個人品牌 / 專業顧問的肖像照——不是大頭照、是「有故事感的人物照」。LinkedIn 進階用、品牌官網「關於我們」、訪談媒體投稿、Substack 個人主圖最高頻。重點是「氛圍 + 個性」、不是「拍得好看」。",
        "outcomes": ["能判斷何時用 founder portrait（與證件照 / 大頭照差異）", "能拆解 6 段並安排人物與環境的故事感", "能識別 4 種踩雷（人臉太正面／環境不對／表情假笑／光線太硬）"],
        "intro": "創辦人 / 個人品牌肖像照。重點不是「拍得好看」、是「有故事感」——人物在自己的工作場域（咖啡店、辦公桌、工作室）、自然動作（思考 / 看遠方 / 操作工具）、暖光氛圍。比大頭照有溫度、比形象照有真實感。",
        "use_cases": [
            {"t": "品牌官網 About Us 主圖", "d": "創辦人 / 老闆出鏡建立信任"},
            {"t": "LinkedIn 進階個人形象照", "d": "顧問 / 自由工作者 / 創業者"},
            {"t": "訪談媒體投稿照", "d": "天下雜誌、報導者、女人迷"},
            {"t": "Substack / Newsletter 個人主圖", "d": "創作者建立個人 IP"},
        ],
        "compare_table": [
            ("拍攝目的", "故事感 + 個性 + 信任", "證件照：規格化；大頭照：辨識度"),
            ("人物姿態", "自然動作（看遠方 / 操作 / 思考）", "證件照：直視；大頭照：微笑"),
            ("環境", "<strong>必含</strong>工作場域元素", "證件照：純白底；大頭照：簡約底"),
            ("光線", "暖自然光、有方向性", "證件照：均勻硬光"),
            ("構圖", "半身或 3/4 身、留白給場域", "證件照：頭肩；大頭照：胸上"),
            ("臉部", "可側面、可低頭、不一定正面", "證件照：必正面；大頭照：必微笑"),
        ],
        "judge": "客戶問「能不能拍張我的形象照」（要放官網 / 訪談）走 C4；問「LinkedIn 大頭照」用 portraits-and-characters/professional-portrait（更標準化）；問「員工大頭照」用大頭照模板。<strong>C4 是個人品牌經營者最值得投資的卡片</strong>——一張好的 founder portrait 能用 2-3 年。",
        "decompose_intro": "founder portrait 6 段。<strong>核心難度在「自然感」</strong>——AI 給人物的姿勢和表情容易僵硬、像 stock photo：",
        "six_segments": [
            {"name": "subject 人物", "need": "<strong>必問</strong>", "fill": "性別 + 年齡範圍 + 種族 + 職業 + 個性（嚴肅 / 親切 / 沉穩）"},
            {"name": "pose 姿態", "need": "<strong>必問</strong>", "fill": "動作（看遠方 / 操作工具 / 翻書 / 倒咖啡）；身體角度（正面 / 3/4 / 側面）"},
            {"name": "facial 臉部", "need": "<strong>必問</strong>", "fill": "表情（微笑 / 思考 / 平靜）；視線方向（看鏡頭 / 看遠 / 看手中物）；可側面或半遮"},
            {"name": "environment 環境", "need": "<strong>必問</strong>", "fill": "場域（咖啡店 / 辦公桌 / 工作室 / 戶外）+ 環境道具（電腦 / 咖啡 / 書）"},
            {"name": "lighting 光線", "need": "<strong>必問</strong>", "fill": "自然光（窗光 / 戶外）+ 方向（側光 / 逆光）+ 色溫（暖 / 中性）"},
            {"name": "constraints 限制", "need": "固定寫死", "fill": "禁忌：假笑、硬光、stock photo 感、過度修圖、純白底（不是大頭照）"},
        ],
        "mnemonic": "人物 → 姿態 → 臉 → 環境 → 光 → 禁。<strong>新手最常踩「假笑＋直視鏡頭」</strong>——這就變大頭照不是 portrait。明確寫「looking off-camera」「subtle expression, not posed smile」「natural candid moment」。",
        "demo_intro": "下面這張是 OPEN BEANS 創辦人在自家咖啡店的形象照。男性 30s、台灣人、坐在咖啡吧台後方、看著手中的咖啡杯（不直視鏡頭）、暖色側光、自然動作。可放品牌官網 About。",
        "image_path": "v60-c4-founder-portrait.png",
        "image_alt": "OPEN BEANS 創辦人形象照、亞洲男性 30 歲左右、坐在自家咖啡店吧台後方、半身構圖、看著手中手沖咖啡杯不直視鏡頭、自然平靜表情、深色襯衫工作圍裙、背景虛化的烘豆機與咖啡豆儲存罐、暖色側光從右側窗戶灑入、米色木紋吧台、適合品牌官網 About Us 與訪談媒體投稿",
        "caption": "本人物照走「自然不直視鏡頭」路線、規避 imagegen 對人臉直視的不可控（AI 生成的人臉直視鏡頭通常有不對稱問題）。客戶實際使用建議真人實拍 + AI 生成只當「氛圍提案版本」。",
        "prompt_label": "OPEN BEANS 創辦人咖啡店形象照",
        "prompt_full": """請生成一張創辦人 / 個人品牌肖像照（founder portrait）：

【人物】亞洲男性、30-40 歲、台灣人、精品咖啡店創辦人、個性沉穩專注。

【姿態】半身構圖、坐在自家咖啡店吧台後方、身體角度 3/4 側對鏡頭、雙手輕扶咖啡杯。

【臉部】表情自然平靜、不要笑、視線朝下看著手中手沖咖啡杯（不要直視鏡頭）。可有極淡微笑感（眼神專注）。

【環境】自家精品咖啡店吧台、米色木紋桌面、背景虛化（淺景深）：可見輪廓的烘豆機、深棕色咖啡豆儲存罐、垂掛的乾燥植物。

【服裝】深棕色襯衫 + 米色工作圍裙（咖啡職人感）。袖子捲起。

【光線】自然光 + 暖色側光（從右側窗戶灑入）、明顯方向性、營造黃昏前的咖啡店氛圍。

【相機感】像用 35mm 全幅 + 50mm 鏡頭拍攝、輕微膠片顆粒、商業攝影級。

【風格】真實人文紀實感、不要過度修圖、不要美顏濾鏡、不要 stock photo 感。

【限制】嚴禁直視鏡頭（會變大頭照不是 portrait）、嚴禁假笑、嚴禁純白底、嚴禁硬光、嚴禁工作場域以外的元素（不要花、不要書、不要其他人）、嚴禁中文字。""",
        "read_4_points": "(1) 視線方向有沒有「不直視」（看遠 / 看物 / 看下）？(2) 環境是不是「他真的在那裡」（不是合成感）？(3) 表情自然嗎（不假笑、不僵硬）？(4) 光線方向明確嗎（不是均勻硬光）？",
        "swap_table": [
            ("ⓐ 人物 = ?（性別 + 年齡 + 職業）", "例：亞洲男性 35 歲咖啡職人 / 亞洲女性 40 歲設計顧問"),
            ("ⓑ 環境 = ?（自己的工作場域）", "例：咖啡店吧台 / 設計工作室桌前 / 教練在健身房 / 顧問辦公桌"),
            ("ⓒ 動作 = ?（自然動作）", "例：扶咖啡杯 / 看筆記 / 操作機器 / 整理工具"),
        ],
        "pitfalls": [
            {"t": "假笑 + 直視鏡頭", "d": "AI 給你的「微笑直視」變成大頭照不是 portrait。<strong>解法</strong>：明確寫「looking off-camera」「subtle, focused expression, not posed smile」「captured candid moment」。"},
            {"t": "環境太空洞", "d": "純白底 / 灰漸變 = 大頭照感、不是 founder portrait。<strong>解法</strong>：明確寫「subject in their actual workspace」「real environmental elements (tools, products, space)」「shallow depth of field with environmental context」。"},
            {"t": "光線太硬", "d": "AI 預設給均勻 4500K 光、感覺像棚拍——不像「他在自然環境裡」。<strong>解法</strong>：明確寫「natural window light, warm side lighting, golden hour quality」、避免「studio lighting」。"},
            {"t": "AI 人臉的不可控", "d": "imagegen 對人臉細節（不對稱、年齡、種族特徵）不穩定。<strong>C4 的最佳策略</strong>：把 AI 生成版本當<strong>「氛圍提案」</strong>給客戶看「你大概會長這樣的感覺」、實際交付的成品建議真人實拍。或請客戶提供照片、用 image-to-image 換背景與光線。<strong>從不要把純 AI 生成的 founder portrait 當成正式交付品</strong>——客戶若用在官網被識別出是 AI 生成、商業信譽會受損。<br><br><strong>實戰提醒</strong>：C4 是 C 組裡<strong>最不適合純 AI 交付</strong>的卡片。建議客戶：「用 AI 探索氛圍方向、確定後找在地攝影師按這個 mood board 拍 1 張」。攝影師費 NT$5000-15000、加你 prompt 顧問費 NT$3000、客戶得到「真實 + 對方向」雙贏。"},
        ],
        "prev_file": "CH6-C3.html", "prev_label": "上一張 C3",
        "next_file": "CH6-C5.html", "next_label": "下一張 C5",
        "meta_desc": "創辦人肖像模板速查：故事感 + 個性 + 信任、品牌官網 About 與 LinkedIn 進階首選。",
    },
    {
        "id": "C5", "title": "Sticker Set LINE 貼圖組",
        "source_md": "avatars-and-profile/sticker-set.md",
        "tagline": "成套的 LINE 貼圖（8-24 張、不同表情 / 反應）。台灣最好變現的 IP 視覺類別——個人 IP 自製貼圖上架賺被動收入、品牌客戶做專屬會員贈品。重點是「角色一致 + 表情多樣 + 風格穩定」。",
        "outcomes": ["能判斷何時用 sticker set（與其他角色卡差異）", "能拆解 6 段並產出風格一致的 8-24 張貼圖", "能識別 4 種踩雷（角色不一致／表情單調／風格漂移／構圖不適合 LINE 比例）"],
        "intro": "成套 LINE 貼圖。8 / 16 / 24 / 40 張一組、共用一個角色、不同表情與反應（OK、謝謝、生氣、笑、晚安）。每張獨立使用、整組看是同一個角色。",
        "use_cases": [
            {"t": "個人 IP 上架 LINE 貼圖賺被動收入", "d": "上架後可賣 5-10 年"},
            {"t": "品牌專屬會員贈品", "d": "註冊送 8 張限量貼圖"},
            {"t": "活動 / 課程贈送學員", "d": "增加學員回饋"},
            {"t": "工作室周邊 / 文創商品延伸", "d": "貼圖 → 馬克杯 → 帆布袋"},
        ],
        "compare_table": [
            ("數量", "8 / 16 / 24 / 40 張一組", "其他卡：單張或少量"),
            ("角色一致性", "<strong>最關鍵</strong>—— 24 張要看出是同一角色", "其他：通常單一視覺"),
            ("表情多樣", "8 種以上情緒/反應", "其他：通常單一情境"),
            ("構圖", "正方形（240×240px）+ 透明底", "其他：橫式或直立"),
            ("使用平台", "LINE / Telegram / WhatsApp", "其他：通用"),
            ("變現潛力", "<strong>高</strong>（一次設計、長期賣）", "其他：單次接案"),
        ],
        "judge": "客戶問「我想做 LINE 貼圖」走 C5；問「品牌吉祥物」用 branding-and-packaging/mascot-brand-kit；問「IP 周邊」用 avatars-and-profile 系列其他卡。<strong>C5 是 C 組裡變現潛力最高的卡片</strong>——一組 24 張上架可賣 NT$30-60、長期累積被動收入。",
        "decompose_intro": "sticker set 6 段。<strong>核心難度在「角色一致性」</strong>——AI 生成 24 張時、第 1 張跟第 24 張的角色細節（眼睛大小、髮型、衣服）容易漂移：",
        "six_segments": [
            {"name": "character base 角色基底", "need": "<strong>必問</strong>", "fill": "物種（人 / 動物 / 物件擬人）+ 體型（圓潤 / 瘦長）+ 顏色 + 個性"},
            {"name": "character details 角色細節", "need": "<strong>必問</strong>", "fill": "髮型 / 服裝 / 配件（眼鏡 / 帽子）+ 必須一致的特徵"},
            {"name": "style 風格", "need": "<strong>必問</strong>", "fill": "繪畫風格（手繪 / 像素 / 3D / 厚塗）+ 線條（粗 / 細）+ 顏色（厚塗 / 平塗）"},
            {"name": "expressions 表情組合", "need": "<strong>必問</strong>", "fill": "8-24 種情緒：OK、謝謝、生氣、開心、累、晚安、加油、哭、笑、害羞⋯⋯"},
            {"name": "format 規格", "need": "<strong>必問</strong>", "fill": "正方形 240×240px、透明底（PNG）、留 10% 邊緣空白避免裁切"},
            {"name": "constraints 限制", "need": "固定寫死", "fill": "禁忌：角色不一致、含現實 logo、含真實人物臉、含露骨 / 暴力、文字超過 3 字"},
        ],
        "mnemonic": "基底 → 細節 → 風格 → 表情 → 規格 → 禁。<strong>新手最常踩「角色漂移」</strong>——畫 24 張時 AI 把眼睛大小、髮色慢慢改掉。明確寫「same character throughout, identical hair color, same outfit, consistent eye style」、必要時 prompt 內貼「reference image」。",
        "demo_intro": "下面這張是 OPEN BEANS 品牌吉祥物「Mr. Bean」的 8 張貼圖預覽。咖啡豆擬人化角色、圓潤可愛、深棕色身體 + 米白臉、8 種表情。可上架 LINE Creators Market。",
        "image_path": "v61-c5-sticker-set.png",
        "image_alt": "OPEN BEANS 品牌吉祥物 Mr. Bean LINE 貼圖 8 張預覽組合、咖啡豆擬人化角色、圓潤深棕色身體配米白臉部、4×2 網格排列、8 種表情 OK 謝謝 開心 累 晚安 加油 害羞 笑、手繪風格粗線條平塗顏色、透明底、240x240 正方形格式、適合 LINE Creators Market 上架",
        "caption": "本貼圖組為 8 張預覽（4×2 排）。實際上架要 24 張、依 LINE Creators Market 規格輸出 PNG with transparency、每張 240×240px。中文情緒文字（「OK」「晚安」「加油」）走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline\">後製字體疊圖工作流</a> 在 Figma 用「金萱半糖粗體」疊上。",
        "prompt_label": "OPEN BEANS Mr. Bean 品牌吉祥物貼圖組",
        "prompt_full": """請生成一張 LINE 貼圖組預覽（sticker set preview）：

【整體】4×2 網格排列、共 8 張貼圖、每張正方形、整體像「LINE Creators Market 預覽圖」。

【角色】「Mr. Bean」OPEN BEANS 品牌吉祥物：
- 物種：擬人化咖啡豆（圓潤橢圓形體型）
- 顏色：深棕色身體 + 米白色臉部 + 燙金色「OB」logo 在胸前
- 配件：白色小領結 + 圓眼睛 + 微笑嘴
- 個性：友善、認真、有點害羞

【風格】手繪卡通風、粗線條（≥ 3px）、平塗顏色（不要漸變或厚塗）、線條為深棕色、整體溫暖可愛。

【8 個表情（每張正方形、240×240、透明底）】
1. OK 手勢（豎大拇指）
2. 謝謝（鞠躬感謝）
3. 開心（雙手舉起、笑臉）
4. 累（趴下、呼）
5. 晚安（蓋被睡覺、Z 字）
6. 加油（揮拳）
7. 害羞（臉紅、低頭）
8. 笑（捧腹大笑）

【規格要求】每張 240×240、透明底（白色背景代表透明）、留 10% 邊緣空白。

【角色一致性】<strong>所有 8 張角色細節必須完全一致</strong>：相同的眼睛大小、相同的領結、相同的身體比例、相同的線條粗細、相同的顏色。

【限制】嚴禁角色細節在不同貼圖之間漂移、嚴禁出現非 OPEN BEANS 的 logo、嚴禁真實人物臉、嚴禁露骨或暴力、嚴禁文字超過 3 字（且文字要用英文如「OK」「Hi」「Thanks」）。""",
        "read_4_points": "(1) 8 張角色看起來是同一個嗎（眼睛、領結、身體比例一致）？(2) 表情有沒有夠多樣（OK / 累 / 開心 / 晚安）？(3) 線條粗細統一嗎？(4) 平塗顏色而非漸變嗎（LINE 規格要求）？",
        "swap_table": [
            ("ⓐ 角色基底 = ?", "例：擬人化咖啡豆（OPEN BEANS）／擬人化貓（書店品牌）／擬人化豆腐（食品品牌）"),
            ("ⓑ 風格 = ?", "例：手繪粗線條（友善）／像素風（懷舊）／3D 厚塗（IP 化）／日系細線（清新）"),
            ("ⓒ 表情組合 = ?", "例：8 種日常情緒／16 種完整套組／24 種極致表現（含特殊節慶）"),
        ],
        "pitfalls": [
            {"t": "角色不一致", "d": "AI 第 1 張畫的眼睛大、第 8 張變小、領結顏色也偷偷變了。<strong>解法</strong>：明確寫「identical character details across all 8 stickers: same eye size, same outfit, same color palette, no variations」、必要時 prompt 內貼第 1 張當 reference image 跑 image-to-image。"},
            {"t": "風格漂移", "d": "前 4 張手繪風、後 4 張變 3D 風。<strong>解法</strong>：明確寫「same drawing style throughout: hand-drawn, thick lines, flat colors, no 3D rendering, no gradient」。"},
            {"t": "構圖不適合 LINE 規格", "d": "AI 給你的角色貼到貼圖邊緣、被 LINE 自動裁切。<strong>解法</strong>：明確寫「character centered with 10% margin on all sides」「no elements touching the edge」。"},
            {"t": "中文情緒文字一律後製", "d": "imagegen 中文字體限制 + LINE 貼圖文字往往是中文（「OK」「晚安」「加油」）。<strong>C5 的最佳策略</strong>：用英文 placeholder（OK / Good Night / Cheer Up）跑 imagegen、最後在 Figma 用「金萱半糖粗體」疊上中文。<br><br><strong>實戰提醒</strong>：C5 sticker set 上架 LINE Creators Market 是<strong>長期被動收入</strong>——一組 24 張定價 NT$30、若紅了月入 NT$5,000-15,000 是常態。<strong>關鍵：角色 IP 一致性</strong>。建議用 Figma component 做 master character、所有貼圖從它衍生、確保 24 張完全一致。"},
        ],
        "prev_file": "CH6-C4.html", "prev_label": "上一張 C4",
        "next_file": "CH6-C6.html", "next_label": "下一張 C6",
        "meta_desc": "LINE 貼圖組模板速查：角色一致 + 表情多樣 + 風格穩定、個人 IP 變現首選。",
    },
    {
        "id": "C6", "title": "Lookbook Grid 服飾穿搭多格拼貼",
        "source_md": "grids-and-collages/lookbook-grid.md",
        "tagline": "服飾、選物、配飾的「lookbook」多格拼貼——4-9 格的穿搭組合 / 商品輪播 / 風格提案。本地服飾品牌、選物店、個人造型師接案最高頻。重點是「整組調性一致 + 每格獨立可用 + 整體像雜誌頁面」。",
        "outcomes": ["能判斷何時用 lookbook（與電商主圖差異）", "能拆解 6 段並安排多格拼貼節奏", "能識別 4 種踩雷（風格漂移／模特同質化／背景搶戲／構圖過度設計）"],
        "intro": "lookbook 多格拼貼。4-9 個 Look 並列（每格 1 套穿搭）、整體調性一致、像雜誌跨頁或服飾品牌官網 collection 頁。比 C1 bento 重視覺感、比 B1 電商主圖更有故事。",
        "use_cases": [
            {"t": "服飾品牌換季 lookbook", "d": "本地小型服飾、選物店、個人品牌"},
            {"t": "個人造型師作品集", "d": "造型 portfolio 一頁總覽"},
            {"t": "配飾 / 飾品系列展示", "d": "手作品牌、個人飾品創作者"},
            {"t": "選品店每月新品輪播", "d": "Pinkoi、選物店週報"},
        ],
        "compare_table": [
            ("構圖", "4-9 格 grid、每格獨立可用", "B1：單一商品；C1：資訊塊"),
            ("人物", "通常含模特半身或全身", "B1：嚴禁；C4：單一人物"),
            ("整組調性", "<strong>必須</strong>一致（光線 / 色板 / 季節）", "其他：通常單一構圖"),
            ("適用商品", "服飾 / 配飾 / 飾品 / 鞋履", "B1：泛用；B6：飲料"),
            ("使用平台", "Pinkoi / 選物店官網 / IG", "B1：蝦皮；C1：IG 教學"),
            ("接案類型", "服飾品牌 / 選物店 / 個人造型師", "B 組：商品；C1-C5：自媒體"),
        ],
        "judge": "客戶問「我有 6 套穿搭怎麼一張圖呈現」走 C6；問「單品上架圖」走 B1；問「選物店週報」走 C1。<strong>C6 對在地服飾品牌極具價值</strong>——換季 lookbook 接案 NT$15000-30000、且 4 季都能合作。",
        "decompose_intro": "lookbook grid 6 段。<strong>核心難度在「整組調性一致」</strong>——AI 生 6 個模特時容易種族 / 體型 / 髮色漂移、光線變化太大、整組看不出是同一個 lookbook：",
        "six_segments": [
            {"name": "collection 系列主題", "need": "<strong>必問</strong>", "fill": "系列名 + 季節（春／夏／秋／冬）+ 風格定位（極簡 / 復古 / 街頭 / 文青）"},
            {"name": "grid system", "need": "<strong>必問</strong>", "fill": "格數（4 / 6 / 9）+ 比例（每格 1:1 或 4:5）"},
            {"name": "models 模特", "need": "<strong>必問</strong>", "fill": "性別 + 體型 + 種族 + 年齡（建議單一性別 / 體型範圍、避免多樣化讓視覺散）；不直視鏡頭"},
            {"name": "outfits 穿搭組合", "need": "<strong>必問</strong>", "fill": "每格 1 套 Look：上衣 + 下身 + 配飾 + 鞋（每格描述清楚）"},
            {"name": "background 背景", "need": "可預設", "fill": "整組共用 1 個背景（米白棚拍 / 都市街頭 / 自然戶外）；不要每格不同背景"},
            {"name": "constraints 限制", "need": "固定寫死", "fill": "禁忌：模特正臉直視、整組光線不一致、背景每格不同、商品搶過模特、文字遮商品"},
        ],
        "mnemonic": "系列 → 格 → 模特 → 穿搭 → 背景 → 禁。<strong>新手最常踩「模特多樣化」</strong>——客戶想「呈現多元」、結果 6 個模特各種族各體型、整組像聯合國。lookbook 應該「同一風格的 6 個變體」、不是「6 個不同人」。",
        "demo_intro": "下面這張是台灣本地文青服飾「LUME」春季 lookbook 6 格拼貼。3×2 網格、每格 1 套米白色系春裝、模特半身（不見正臉）、米白棚拍底、整組調性極致一致。可給客戶當官網 collection 頁。",
        "image_path": "v62-c6-lookbook-grid.png",
        "image_alt": "LUME 春季文青服飾品牌 lookbook 6 格拼貼、3×2 網格構圖、6 套米白色系春裝穿搭、亞洲女性模特半身不直視鏡頭、米白棚拍背景、文青文宣感、適合品牌官網 collection 頁與 Pinkoi 上架展示",
        "caption": "本 lookbook 走「色板統一 + 模特半身不見正臉」策略——規避 AI 人臉細節不可控 + 強化品牌色板一致性。中文系列名「春日」「初春微涼」走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline\">後製字體疊圖工作流</a>。",
        "prompt_label": "LUME 春季 lookbook 6 格拼貼",
        "prompt_full": """請生成一張服飾品牌 lookbook 6 格拼貼：

【整體】4:5 直立比例、3×2 網格排版、整體像「文青服飾品牌官網 collection 頁面」。

【系列主題】「LUME · Spring 2026」（米白色系、文青風、極簡剪裁）

【grid 系統】3 行 × 2 欄、共 6 格、每格 1:1 比例、格間距 2%。

【模特】統一規格、6 格都用：
- 性別：女性
- 體型：纖瘦中等
- 種族：亞洲（台灣感）
- 年齡：25-30
- 構圖：半身（腰部以上）+ 雙手自然下垂或輕觸衣物
- 視線：<strong>不直視鏡頭</strong>（看遠 / 低頭 / 側臉）
- 表情：自然平靜、不要笑

【6 套穿搭（每格 1 Look）】
1. 米白色 oversized 棉質襯衫 + 寬腳長褲 + 米色帆布鞋
2. 淺米色針織背心 + 白色 T 恤 + 卡其長裙
3. 米色西裝外套 + 白色 T 恤 + 寬腳褲
4. 米白色亞麻 oversized 上衣 + 白色短褲
5. 淺杏色針織開衫 + 白色 T 恤 + 米色長褲
6. 米色亞麻洋裝（過膝）+ 米色腰帶

【背景】6 格共用：米白色棚拍底、極淺自然光、無紋理、無雜物。

【整組調性】統一光線（暖白柔光、無方向性）+ 統一後期色調（低飽和、米色系）+ 統一構圖（半身、置中略偏左）。

【色板】嚴格 3 色：米白底 + 米杏色服裝 + 卡其／米色配件。

【限制】嚴禁模特正臉直視、嚴禁整組光線不一致、嚴禁背景每格不同、嚴禁鮮艷色穿搭（一定要在米色系內）、嚴禁中文字、嚴禁過度修圖（要保留布料紋理）。""",
        "read_4_points": "(1) 6 格的模特看起來是「同類型」嗎（不是 6 個不同人）？(2) 整組光線一致嗎（不要 1 格暖光 1 格冷光）？(3) 色板有沒有「整組統一」（不要 1 格鮮綠搶戲）？(4) 模特有沒有「不直視鏡頭」？",
        "swap_table": [
            ("ⓐ 系列主題 + 風格 = ?", "例：春日米色系（文青）／夏日海軍藍（清爽）／秋日大地色（日系）"),
            ("ⓑ 模特規格 = ?（單一範圍）", "例：女性 25-30 纖瘦／男性 30-40 中等／不分性別 20-35"),
            ("ⓒ 6 套穿搭 = ?", "例：上衣＋下身＋鞋（每格 1 Look）"),
        ],
        "pitfalls": [
            {"t": "模特多樣化讓視覺散", "d": "客戶要「呈現多元」、6 個模特各種族各體型——整組看不出是同一品牌。<strong>解法</strong>：明確寫「all 6 models within same demographic range (gender, age, body type, ethnicity)」「lookbook is variations of one style, not 6 different people」、跟客戶解釋「多元放在不同 collection、不要塞在同 lookbook」。"},
            {"t": "整組光線不一致", "d": "AI 第 1 格暖光、第 4 格冷光、看起來像不同時段拍的。<strong>解法</strong>：明確寫「all 6 frames must have identical lighting: same direction, same color temperature, same shadow softness」。"},
            {"t": "背景每格不同", "d": "AI 給你 6 個不同背景（咖啡店 / 街頭 / 棚拍 / 戶外）——客戶會困惑這是同 lookbook 嗎？<strong>解法</strong>：明確寫「all 6 frames share the same background setting」「single backdrop type across all looks」。"},
            {"t": "中文系列名一律後製", "d": "imagegen 中文字體限制 + 服飾品牌的中文系列名往往是核心（「春日」「初秋」「日常」等情緒詞）。<strong>C6 的最佳策略</strong>：英文版用 imagegen 直出（LUME · Spring 2026）、中文版（「日子緩慢」「初春微涼」）走 <a href=\"CH6-supplement-typography.html\" style=\"color:var(--c-main);text-decoration:underline;font-weight:700\">後製字體疊圖工作流附錄</a>。<br><br><strong>實戰提醒</strong>：C6 服飾品牌客戶很多在 Pinkoi / 個人品牌經營、<strong>每季要做新 lookbook（春夏秋冬 4 次）</strong>。建議跟客戶簽「4 季 lookbook 套餐」、整組設計效率最高、客戶單價也提升 NT$30,000+。"},
        ],
        "prev_file": "CH6-C5.html", "prev_label": "上一張 C5",
        "next_file": "module6.html", "next_label": "返回 CH6 模板速查站",
        "meta_desc": "服飾穿搭 lookbook 模板速查：4-9 格拼貼、整組調性一致、本地服飾品牌與選物店首選。",
    },
]


def render_module6():
    """章節總覽頁"""
    cards_grid = ""
    groups = {
        "A": {"name": "A 組 · 品牌行銷", "items": ["A1", "A2", "A3", "A4", "A5", "A6"]},
        "B": {"name": "B 組 · 商品電商", "items": ["B1", "B2", "B3", "B4", "B5", "B6"]},
        "C": {"name": "C 組 · 內容創作", "items": ["C1", "C2", "C3", "C4", "C5", "C6"]},
    }

    titles = {
        "A1": "Web Hero Banner", "A2": "Campaign KV", "A3": "Brand Poster",
        "A4": "Editorial Cover", "A5": "Brand Identity Board", "A6": "Bilingual Layout",
        "B1": "純白底電商主圖", "B2": "生活方式情境圖", "B3": "影棚高質感 hero",
        "B4": "包裝展示圖", "B5": "商品卡 UI 疊加", "B6": "飲料瓶身標籤設計",
        "C1": "Bento Grid", "C2": "對比資訊圖", "C3": "步驟教學圖",
        "C4": "Founder Portrait", "C5": "LINE 貼圖組", "C6": "Lookbook Grid",
    }

    group_html = []
    for gk, g in groups.items():
        items_html = "\n        ".join(
            f'<a href="CH6-{i}.html" class="card-item"><span class="card-id">{i}</span><span class="card-title">{titles[i]}</span></a>'
            for i in g["items"]
        )
        group_html.append(f'<div class="group-section"><h3 class="group-heading">{g["name"]}</h3><div class="cards-grid">{items_html}</div></div>')
    cards_grid = "\n".join(group_html)

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CH6 模板速查站｜商業用圖片生成</title>
<meta name="description" content="CH6 模板速查站：18 張 imagegen 卡片 + 字體後製附錄、按品牌行銷 / 商品電商 / 內容創作三組分類。">
<link rel="canonical" href="https://skypai0326.github.io/courses/courses/gen-image/module6.html">
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
{CSS}
.cards-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:18px 0 32px}}
.card-item{{background:var(--c-card);border:1px solid var(--c-border-soft);border-radius:var(--radius);padding:16px 18px;display:flex;flex-direction:column;gap:6px;text-decoration:none;transition:border-color .2s,background .2s}}
.card-item:hover{{border-color:var(--c-main);background:rgba(138,106,74,.04)}}
.card-id{{font-family:'Shippori Mincho',serif;font-size:.78rem;color:var(--c-main);font-weight:700;letter-spacing:.05em}}
.card-title{{font-size:.92rem;color:var(--c-text);font-weight:500;line-height:1.5}}
.group-section{{margin-bottom:36px}}
.group-heading{{font-family:'Shippori Mincho',serif;font-size:1.15rem;font-weight:700;color:var(--c-text);margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid var(--c-border-soft)}}
.supplement{{background:var(--c-surface);border-left:3px solid var(--c-main);padding:18px 22px;border-radius:var(--radius);margin:24px 0}}
.supplement a{{color:var(--c-main);text-decoration:none;border-bottom:1px solid rgba(138,106,74,.4);font-weight:700}}
.supplement a:hover{{color:var(--c-text)}}
@media(max-width:600px){{.cards-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>

<a href="#main" class="skip-link">跳至主要內容</a>

<header class="topbar">
  <a href="../../index.html" class="logo">弄一下工作室</a>
  <div class="topbar-divider"></div>
  <span class="topbar-sub">商業用圖片生成</span>
  <div class="spacer"></div>
  <span class="topbar-tag">M6 · 速</span>
</header>
<div class="progress-strip" role="progressbar" aria-label="閱讀進度" aria-valuemin="0" aria-valuemax="100"><div class="progress-fill" id="prog"></div></div>

<main id="main">

<div class="page-hero">
  <a href="index.html" class="back-link"><span aria-hidden="true">←</span> 返回課程首頁</a>
  <div class="hero-eyebrow">CH6 模板速查站</div>
  <h1 class="lesson-title">CH6 · 模板速查站</h1>
  <p class="lesson-tagline">CH1-CH5 教技法與工作流；CH6 是「做完想用時來查」的速查素材庫。18 張模板卡片 + 1 張後製字體附錄、按品牌行銷／商品電商／內容創作三組分類。卡關處從這裡找對應卡片、複製 prompt、改三處替換槽就能用。</p>
  <div class="outcomes">
    <div class="outcomes-label">這個章節怎麼用</div>
    <div class="outcome-item">CH1-CH5 學完後遇到實際接案、先看卡片找對應模板</div>
    <div class="outcome-item">每張卡片附完整 prompt、複製貼到 ChatGPT / Gemini 即可</div>
    <div class="outcome-item">中文 logo / 文案一律走後製字體疊圖附錄、不要硬靠 prompt</div>
  </div>
</div>

<section class="lesson-section">
  <div class="section-eyebrow">(01)</div>
  <h2 class="section-heading">怎麼選對的卡片</h2>
  <div class="intro-band">
    <div class="intro-label">三組分類邏輯</div>
    <div class="intro-text">三組對應台灣本地接案三類客戶：<strong>A 組 品牌行銷</strong>給有品牌經營需求的客戶（公司／自媒體／文化機構）；<strong>B 組 商品電商</strong>給有實體商品要上架的客戶（蝦皮／momo／PChome／Pinkoi）；<strong>C 組 內容創作</strong>給個人經營者（IG／Threads／Substack／LINE 貼圖）。看客戶屬於哪一類、再看每張卡片的「適用場景」段判斷。</div>
  </div>
  {cards_grid}
  <div class="supplement">
    <strong>📐 配套附錄</strong>　所有涉及中文 logo / 文案的卡片，最後都會引用這份 → <a href="CH6-supplement-typography.html">後製字體疊圖工作流</a>（Canva / Figma / Photoshop 三條 6 步驟工作流 + 台灣常用字體取得管道）。imagegen 對中文字體有固有限制、後製疊字是 CH6 的標準收尾。
  </div>
</section>

<hr class="section-rule">

<section class="lesson-section">
  <div class="section-eyebrow">(02)</div>
  <h2 class="section-heading">每張卡片的 anatomy</h2>
  <p class="body-text">所有 18 張模板卡片用同一套 anatomy 結構、學員看一張會用所有：</p>
  <table class="compare-table" aria-label="卡片 anatomy 6 區塊">
    <thead>
      <tr><th>區塊</th><th>內容</th><th>讀取重點</th></tr>
    </thead>
    <tbody>
      <tr><td>Hero</td><td>標題 + 副標 + 學習成果</td><td>判斷這張卡片是不是你要的</td></tr>
      <tr><td>(01) 適用場景</td><td>典型用途 + 對比近似模板</td><td>確認卡片邊界、避免誤用</td></tr>
      <tr><td>(02) 模板拆解</td><td>6 段 prompt 結構表</td><td>學會結構、之後寫 prompt 不從零開始</td></tr>
      <tr><td>(03) 示範圖 + prompt</td><td>實際成品 + 完整可複製 prompt + JSON 進階版</td><td>直接複製、改替換槽即可用</td></tr>
      <tr><td>(04) 改寫 + 踩雷</td><td>3 個替換槽 + 4 種常見錯誤</td><td>避免新手陷阱</td></tr>
    </tbody>
  </table>
  <div class="callout">
    <div class="callout-icon" aria-hidden="true">💡</div>
    <div class="callout-body">B1-B6 卡片是 anatomy 完整版（6 區塊、含兩個情境範例）。A 組與 C 組是<strong>精簡版</strong>（4 區塊、不含獨立情境），但保留所有複製貼上必要的 prompt 與踩雷內容。設計取捨：B 組是學員最先學的、教學深度高；A／C 組是查閱用、結構精簡讓查找更快。</div>
  </div>
</section>

<div class="nav-footer">
  <a href="index.html" class="nav-btn"><span aria-hidden="true">←</span> 返回課程首頁</a>
  <a href="CH6-1.html" class="nav-btn primary">進入方法論 CH6-1 <span aria-hidden="true">→</span></a>
</div>

</main>

<footer class="footer">
  <span class="footer-logo">弄一下工作室</span>
  <div class="footer-div"></div>
  <span class="footer-note">2026 春季</span>
  <span class="footer-meta" data-platform-version="ChatGPT GPT-image-1 / Gemini Nano Banana" data-built-at="2026-05-01">本頁以 ChatGPT GPT-image-1 / Gemini Nano Banana 製作，2026-05</span>
</footer>

<script>
{JS_PROGRESS}
</script>
</body>
</html>"""


def render_ch6_1():
    """方法論頁"""
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CH6-1 模板速查方法論｜商業用圖片生成</title>
<meta name="description" content="CH6 模板速查方法論：如何從 18 張卡片中選對的、如何把模板套到自己的場景、如何處理中文字體限制。">
<link rel="canonical" href="https://skypai0326.github.io/courses/courses/gen-image/CH6-1.html">
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>

<a href="#main" class="skip-link">跳至主要內容</a>

<header class="topbar">
  <a href="../../index.html" class="logo">弄一下工作室</a>
  <div class="topbar-divider"></div>
  <span class="topbar-sub">商業用圖片生成</span>
  <div class="spacer"></div>
  <span class="topbar-tag">M6 · 速</span>
</header>
<div class="progress-strip" role="progressbar"><div class="progress-fill" id="prog"></div></div>

<main id="main">

<div class="page-hero">
  <a href="module6.html" class="back-link"><span aria-hidden="true">←</span> 返回 CH6 模板速查站</a>
  <div class="hero-eyebrow">(01)</div>
  <h1 class="lesson-title">模板速查方法論</h1>
  <p class="lesson-tagline">18 張卡片各自獨立可用、但選對卡片需要方法。這頁是「怎麼用 CH6 速查站」的元層級指南：怎麼從接案需求逆推到對的卡片、怎麼把模板的 6 段拆解套到自己的商品、怎麼處理 imagegen 對中文字體的固有限制。</p>
</div>

<section class="lesson-section">
  <div class="section-eyebrow">(01)</div>
  <h2 class="section-heading">3 步驟選對卡片</h2>
  <ol class="pitfall-list">
    <li><strong>判斷客戶屬於哪一組</strong>　A 組（品牌經營）／B 組（電商上架）／C 組（個人創作）。看客戶問什麼問題：「我要做品牌官網／campaign」=A 組；「我要上架蝦皮／momo」=B 組；「我要做 IG 教學圖／LINE 貼圖」=C 組。</li>
    <li><strong>看每張卡片的「(01) 適用場景」段</strong>　每張卡片都列了 4 個典型用途、與對近似模板的對比表。確認你的場景對得上、再進入 (02) 拆解。</li>
    <li><strong>複製 prompt、改 3 個替換槽</strong>　每張卡片的「(05) 示範圖 + prompt」有完整可複製的 prompt 與「3 個替換槽位表」。改商品名、改場景、改色板就是你的版本。</li>
  </ol>
</section>

<hr class="section-rule">

<section class="lesson-section">
  <div class="section-eyebrow">(02)</div>
  <h2 class="section-heading">imagegen 中文字體的固有限制</h2>
  <div class="intro-band">
    <div class="intro-label">驗證了 3 次的事實</div>
    <div class="intro-text">B2 卡片 pilot 階段跑了 3 次 imagegen（書法版／新細明體版 v1／新細明體版 v2）、無論 prompt 寫「金萱體」「Maru Mincho」「禁用思源宋體」，模型都只會給「接近新細明體的系統預設襯線體」。這是<strong>模型訓練資料的限制、不是 prompt 寫得不夠</strong>。</div>
  </div>
  <p class="body-text">實務分工：</p>
  <ul class="scenario-list" style="margin-bottom:24px">
    <li><strong>imagegen 負責</strong>：構圖、光線、人物姿態、道具、商品本身</li>
    <li><strong>後製負責</strong>：中文 logo、品牌名、slogan、CTA 中文文案、節慶情緒字</li>
    <li><strong>英文小字可賭</strong>：簡單英文（OPEN BEANS / 350ml）有機會 imagegen 直接給對；複雜英文（多字組合）仍可能拼錯</li>
  </ul>
  <div class="callout">
    <div class="callout-icon" aria-hidden="true">📐</div>
    <div class="callout-body"><strong>結論</strong>：所有涉及中文 logo / 文案的卡片，最終都應該走 <a href="CH6-supplement-typography.html" style="color:var(--c-main);text-decoration:underline;font-weight:700">後製字體疊圖工作流</a>。imagegen 出純圖、Figma / Canva 後製疊上中文。這是 CH6 的標準收尾、不是繞路。</div>
  </div>
</section>

<hr class="section-rule">

<section class="lesson-section">
  <div class="section-eyebrow">(03)</div>
  <h2 class="section-heading">把模板套到你的場景｜3 個替換原則</h2>
  <ol class="pitfall-list">
    <li><strong>商品替換</strong>：把卡片示範的商品（OPEN BEANS 咖啡豆袋）換成你客戶的商品。<strong>關鍵</strong>：保留視覺特徵描述方式（包裝形態 + 顏色 + 標籤資訊）、只換具體商品名。</li>
    <li><strong>色板替換</strong>：每張卡片的色板都是「3 色鎖」（base + primary + accent）。換你客戶品牌色、但保持 3 色限制。<strong>關鍵</strong>：不要因為「想多元」就加第 4 色、會破壞整體質感。</li>
    <li><strong>場景替換</strong>：卡片裡的台灣化情境（雙北上班族 / 南投小農 / 松菸活動）是台灣本地的常見背景。換你的客戶背景時、要連帶調整道具、季節、氛圍。<strong>關鍵</strong>：不要照搬卡片的台北背景到客戶在台中／高雄的場景。</li>
  </ol>
</section>

<div class="nav-footer">
  <a href="module6.html" class="nav-btn"><span aria-hidden="true">←</span> 返回 CH6 模板速查站</a>
  <a href="CH6-A1.html" class="nav-btn primary">進入第一張卡片 A1 <span aria-hidden="true">→</span></a>
</div>

</main>

<footer class="footer">
  <span class="footer-logo">弄一下工作室</span>
  <div class="footer-div"></div>
  <span class="footer-note">2026 春季</span>
  <span class="footer-meta" data-platform-version="ChatGPT GPT-image-1 / Gemini Nano Banana" data-built-at="2026-05-01">本頁以 ChatGPT GPT-image-1 / Gemini Nano Banana 製作，2026-05</span>
</footer>

<script>
{JS_PROGRESS}
</script>
</body>
</html>"""


def render_ch6_x():
    """自我練習頁"""
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CH6-X 自我練習｜商業用圖片生成</title>
<meta name="description" content="CH6 自我練習：3 個情境、挑模板 + 改寫 + 出圖、檢核標準。">
<link rel="canonical" href="https://skypai0326.github.io/courses/courses/gen-image/CH6-X.html">
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
{CSS}
.exercise-card{{background:var(--c-card);border:1px solid var(--c-border-soft);border-radius:var(--radius);padding:24px 28px;margin:20px 0;border-left:3px solid var(--c-main)}}
.exercise-label{{font-size:.74rem;color:var(--c-main);letter-spacing:.12em;font-weight:700;margin-bottom:6px}}
.exercise-title{{font-family:'Shippori Mincho',serif;font-size:1.1rem;font-weight:700;color:var(--c-text);margin-bottom:10px;line-height:1.5}}
.exercise-body{{font-size:.9rem;color:var(--c-text);line-height:1.85;margin-bottom:14px}}
.exercise-task{{font-size:.85rem;color:var(--c-muted);background:var(--c-surface);padding:12px 16px;border-radius:var(--radius-sm);line-height:1.85;margin-bottom:14px}}
.exercise-task strong{{color:var(--c-text)}}
.exercise-checklist{{list-style:none;padding:0;margin:14px 0 0}}
.exercise-checklist li{{padding:8px 0 8px 28px;position:relative;font-size:.88rem;line-height:1.85;color:var(--c-text)}}
.exercise-checklist li::before{{content:"☐";position:absolute;left:0;top:8px;color:var(--c-main);font-size:1.05rem;font-weight:700}}
</style>
</head>
<body>

<a href="#main" class="skip-link">跳至主要內容</a>

<header class="topbar">
  <a href="../../index.html" class="logo">弄一下工作室</a>
  <div class="topbar-divider"></div>
  <span class="topbar-sub">商業用圖片生成</span>
  <div class="spacer"></div>
  <span class="topbar-tag">M6 · 練</span>
</header>
<div class="progress-strip" role="progressbar"><div class="progress-fill" id="prog"></div></div>

<main id="main">

<div class="page-hero">
  <a href="module6.html" class="back-link"><span aria-hidden="true">←</span> 返回 CH6 模板速查站</a>
  <div class="hero-eyebrow">(X)</div>
  <h1 class="lesson-title">CH6 自我練習｜挑模板＋改寫＋出圖</h1>
  <p class="lesson-tagline">看完 18 張卡片不是終點、能用才是。這頁給 3 個常見接案情境、你獨立判斷該用哪張卡片、改寫 prompt 並跑出第一張圖。完成後對照檢核 4 點驗收。</p>
</div>

<section class="lesson-section">
  <div class="section-eyebrow">(01)</div>
  <h2 class="section-heading">情境 1｜手作果醬上架蝦皮</h2>
  <div class="exercise-card">
    <div class="exercise-label">情境難度 · 入門</div>
    <div class="exercise-title">朋友做手工草莓果醬、要上架蝦皮、預算只夠你接 NT$3,000</div>
    <div class="exercise-body">客戶有 4 款口味（草莓 / 藍莓 / 芒果 / 鳳梨）、要 4 張白底主圖。寫一份 prompt、產出 4 張一致風格的主圖。</div>
    <div class="exercise-task"><strong>你的任務</strong>：(1) 從 18 張卡片中挑 1 張對的、(2) 寫出你的 prompt（標籤建議用英文）、(3) 跑 imagegen 一次到位。</div>
    <ul class="exercise-checklist">
      <li>挑對卡片：應該選 <strong>B1 純白底電商主圖</strong>（不是 B2 lifestyle、不是 B6 飲料瓶身設計）</li>
      <li>標籤改用英文：「JAMS by Mom · Strawberry · 200g」（規避中文字體）</li>
      <li>4 款用同 prompt 改 1 處（口味名 + 標籤色），保持風格一致</li>
      <li>背景純白 #FFFFFF、底部柔光陰影、商品占畫面 60%</li>
    </ul>
  </div>
</section>

<hr class="section-rule">

<section class="lesson-section">
  <div class="section-eyebrow">(02)</div>
  <h2 class="section-heading">情境 2｜健身教練線上一對一招生 EDM</h2>
  <div class="exercise-card">
    <div class="exercise-label">情境難度 · 中階</div>
    <div class="exercise-title">健身教練要做招生 EDM、放 LINE 官方帳號連結、預算 NT$8,000</div>
    <div class="exercise-body">教練要的是「真實落地頁感」、客戶看完想立刻點 CTA 報名。要做 1 張桌機橫版 + 1 張手機直版。</div>
    <div class="exercise-task"><strong>你的任務</strong>：(1) 挑卡片、(2) 設計三色板（教練品牌色 + 主底色 + accent）、(3) 寫 headline + CTA + 資訊卡的 3 個元素。</div>
    <ul class="exercise-checklist">
      <li>挑對卡片：應該選 <strong>B5 商品卡 UI 疊加</strong>（不是 A1 web banner、不是 C4 founder portrait）</li>
      <li>三色板限定：例「深灰 + 純白 + 螢光黃」（運動感）</li>
      <li>CTA 寫英文：「Get Started」「Start Training」（規避字體限制）</li>
      <li>右欄資訊卡寫具體數字：「200+ Active Members · 4.8★」建立信任</li>
    </ul>
  </div>
</section>

<hr class="section-rule">

<section class="lesson-section">
  <div class="section-eyebrow">(03)</div>
  <h2 class="section-heading">情境 3｜松菸活動雙語視覺</h2>
  <div class="exercise-card">
    <div class="exercise-label">情境難度 · 進階</div>
    <div class="exercise-title">松菸文創園區辦「Slow Living 慢工作坊」、要做活動主視覺、預算 NT$15,000</div>
    <div class="exercise-body">活動有外國觀眾、要中英雙語並列。中文「慢工作坊」是品牌核心、英文「Slow Living Workshop」副從。一張海報橫式、放官網與印刷宣傳單。</div>
    <div class="exercise-task"><strong>你的任務</strong>：(1) 挑卡片、(2) 安排中英主從關係、(3) 設計後製疊字流程（imagegen 出構圖 + Figma 後製疊金萱體中文）。</div>
    <ul class="exercise-checklist">
      <li>挑對卡片：應該選 <strong>A6 中英雙語版面</strong>（不是 A3 brand poster、不是 A4 editorial cover）</li>
      <li>中英主從：中文 70% 視覺重量、英文 30%</li>
      <li>字體配對：中文金萱粗 + 英文 Playfair Display（都襯線、調性一致）</li>
      <li>後製流程：imagegen 出英文版 + 構圖 → Figma 用金萱字體疊上「慢工作坊」中文</li>
    </ul>
  </div>
</section>

<hr class="section-rule">

<section class="lesson-section">
  <div class="section-eyebrow">(04)</div>
  <h2 class="section-heading">驗收 4 點檢核</h2>
  <p class="body-text">完成 3 個情境後、對照下面 4 點檢核：</p>
  <ul class="exercise-checklist">
    <li><strong>選對卡片</strong>：每個情境的卡片是不是對的（情境 1=B1、情境 2=B5、情境 3=A6）</li>
    <li><strong>規避字體限制</strong>：所有中文 logo / 標題你都安排了「英文 placeholder + Figma 後製疊字」流程</li>
    <li><strong>替換槽完整</strong>：每張 prompt 你都改了 3 個替換槽（商品 / 色板 / 場景）、不是照搬</li>
    <li><strong>4 踩雷避開</strong>：對照該卡片的 4 種踩雷、確認你的 prompt 都避開了</li>
  </ul>
  <div class="callout">
    <div class="callout-icon" aria-hidden="true">✓</div>
    <div class="callout-body">3 個情境都過、就具備了「<strong>看到接案需求 → 立刻知道用哪張卡片 → 改 3 處 → 跑出可交付的圖</strong>」這套完整工作流。CH6 模板速查站到這裡完成階段性目標、後續實戰累積即可。</div>
  </div>
</section>

<div class="nav-footer">
  <a href="module6.html" class="nav-btn"><span aria-hidden="true">←</span> 返回 CH6 模板速查站</a>
  <a href="index.html" class="nav-btn primary">回到課程首頁 <span aria-hidden="true">→</span></a>
</div>

</main>

<footer class="footer">
  <span class="footer-logo">弄一下工作室</span>
  <div class="footer-div"></div>
  <span class="footer-note">2026 春季</span>
  <span class="footer-meta" data-platform-version="ChatGPT GPT-image-1 / Gemini Nano Banana" data-built-at="2026-05-01">本頁以 ChatGPT GPT-image-1 / Gemini Nano Banana 製作，2026-05</span>
</footer>

<script>
{JS_PROGRESS}
</script>
</body>
</html>"""


def main():
    # 卡片
    for c in CARDS:
        path = OUT_DIR / f"CH6-{c['id']}.html"
        path.write_text(render_card(c), encoding='utf-8')
        print(f"✓ {path.name}")
    # 結構頁
    (OUT_DIR / "module6.html").write_text(render_module6(), encoding='utf-8')
    print(f"✓ module6.html")
    (OUT_DIR / "CH6-1.html").write_text(render_ch6_1(), encoding='utf-8')
    print(f"✓ CH6-1.html")
    (OUT_DIR / "CH6-X.html").write_text(render_ch6_x(), encoding='utf-8')
    print(f"✓ CH6-X.html")
    print(f"\n總共產出 {len(CARDS)} 卡片 + 3 結構頁 = {len(CARDS) + 3} 個 HTML")


if __name__ == "__main__":
    main()
