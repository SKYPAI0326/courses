#!/usr/bin/env python3
"""UI/UX 共學講義：把 UIUX共學講義/<章>/_src/*.tpl 套上冷色調外殼，產出課程網頁。

用法（在課程 repo 根目錄執行）：
  python3 courses/uiux-designer/_build/build.py                 # 輸出到 courses/uiux-designer/
  python3 courses/uiux-designer/_build/build.py --out <資料夾>  # 輸出到別處（預覽用）

做的事：
  1. 依 chapters.json 產生課程首頁 index.html（已開放的章可點，其餘標「即將開放」）。
  2. 每個 status=open 的章：讀 _src/目錄.tpl 決定順序與檔名，R0→CH{n}-0、L{k}→CH{n}-{k}、目錄→index。
  3. 講義 <main> 內容原封不動，只做兩件事：{{IMG:路徑}} 換成內嵌 JPEG（與 UIUX共學講義/工具/build_page.py
     同參數：寬 >1200 縮到 1200、JPEG 品質 82），以及站內連結改成新檔名。
  4. 各頁 <style> 裡的示意圖、複製框等專屬規則保留；通用外觀規則改由 theme.css 提供。
  5. 建完自動比對每頁 <main>（去掉圖片資料、還原連結後）和 .tpl 完全相同，不同就失敗。
不會修改 UIUX共學講義 資料夾內任何檔案。
"""
import argparse, base64, datetime, html, io, json, re, sys, unicodedata
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
COURSE_DIR = HERE.parent
REPO = COURSE_DIR.parent.parent
CN = "零一二三四五六七八九十"

# 講義原始 CSS 中，改由 theme.css 統一提供的規則（選擇器正規化後比對）
BASE_SELECTORS = {
    ":root", "*", "body", "main", "h1", ".lead", "h2", "h2.sub", "h3", "p", ".part", ".box",
    ".box p:last-child, .box ul:last-child, .box ol:last-child", ".eg", "table", "th, td", "th",
    ".step", ".step h3", ".step .num", ".step img", ".see", ".see b", ".cap", "code", "details",
    "summary", ".btn", ".btn:hover", ".btn:active", ".btn::after",
}
CHROME_PREFIXES = (".toc", ".stage", ".checker")  # 整組由 theme.css 重新定義


def nfc(s):
    return unicodedata.normalize("NFC", s)


def fail(msg):
    sys.exit(f"[build] 失敗：{msg}")


def cn_num(n):
    if n <= 10:
        return CN[n]
    if n < 20:
        return "十" + (CN[n - 10] if n > 10 else "")
    return CN[n // 10] + "十" + (CN[n % 10] if n % 10 else "")


# ── CSS ─────────────────────────────────────────────
def split_rules(css):
    """回傳 [(prelude, body)]；@media 的 body 是巢狀字串。"""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, depth, start, prev_end, pre = [], 0, 0, 0, ""
    for i, ch in enumerate(css):
        if ch == "{":
            if depth == 0:
                pre, start = css[prev_end:i].strip(), i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                out.append((pre, css[start + 1:i]))
                prev_end = i + 1
    if depth != 0 or css[prev_end:].strip():
        fail("CSS 大括號不成對或有殘留內容")
    return out


def norm_sel(s):
    return re.sub(r"\s+", " ", s.strip())


def sanitize_decls(body, where):
    def radius(m):
        val = m.group(1)
        new = re.sub(r"(\d+(?:\.\d+)?)px", lambda n: "8px" if 8 < float(n.group(1)) < 50 else n.group(0), val)
        return f"border-radius:{new}"
    body = re.sub(r"border-radius\s*:\s*([^;}]+)", radius, body)
    body = re.sub(r"box-shadow\s*:\s*0 0 0 (\d+px) (#[0-9A-Fa-f]{3,6})", r"outline:\1 solid \2", body)
    if "box-shadow" in body or "gradient" in body:
        fail(f"{where} 有無法自動轉換的 box-shadow／gradient：{body.strip()[:80]}")
    return body


def page_css(css, where):
    kept = []
    for pre, body in split_rules(css):
        if pre.startswith("@media"):
            inner = [f"{p}{{{sanitize_decls(b, where).strip()}}}" for p, b in split_rules(body)
                     if keep_rule(p)]
            if inner:
                kept.append(f"{norm_sel(pre)}{{{''.join(inner)}}}")
        elif pre.startswith("@"):
            fail(f"{where} 有不認得的 CSS 區塊：{pre}")
        elif keep_rule(pre):
            kept.append(f"{norm_sel(pre)}{{{sanitize_decls(body, where).strip()}}}")
    return "\n".join(kept)


def keep_rule(sel):
    s = norm_sel(sel)
    if s in BASE_SELECTORS:
        return False
    parts = [p.strip() for p in s.split(",")]
    if all(p.startswith(CHROME_PREFIXES) for p in parts):
        return False
    return True


def minify(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    return css.strip()


# ── 圖片 ─────────────────────────────────────────────
def embed(path):
    if not path.is_file():
        fail(f"找不到圖片：{path}")
    im = Image.open(path).convert("RGB")
    if im.width > 1200:
        im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


# ── 解析 .tpl ─────────────────────────────────────────
def parse_tpl(path):
    t = nfc(path.read_text(encoding="utf-8"))
    def one(pat, what):
        m = re.search(pat, t, re.S)
        if not m:
            fail(f"{path.name} 缺 {what}")
        return m
    title = one(r"<title>(.*?)</title>", "<title>").group(1).strip()
    style = one(r"<style>(.*?)</style>", "<style>").group(1)
    body = one(r"<body>(.*)</body>", "<body>").group(1)
    m = one(r"^(.*?)<main>(.*)</main>(.*)$", "<main>")
    before, main, after = m.group(1), m.group(2), m.group(3)
    m2 = re.match(r"^(.*?)<main>(.*)</main>(.*)$", body, re.S)
    if m2.group(1).strip():
        fail(f"{path.name} 的 <main> 前面還有內容，模板不認得")
    rest = re.sub(r"<script>.*?</script>", "", m2.group(3), flags=re.S)
    if rest.strip():
        fail(f"{path.name} 的 </main> 後面有 <script> 以外的內容")
    scripts = re.findall(r"<script>.*?</script>", m2.group(3), re.S)
    return {"title": title, "style": style, "main": m2.group(2), "scripts": scripts}


def parse_toc(main):
    items, stage = [], None
    for m in re.finditer(r'<p class="stage">(.*?)</p>|<li><a href="([^"]+)"><span class="no">(.*?)</span><span><span class="t">(.*?)</span>', main):
        if m.group(1) is not None:
            stage = m.group(1)
        else:
            items.append({"href": nfc(m.group(2)), "no": m.group(3), "t": m.group(4), "stage": stage})
    if not items:
        fail("目錄.tpl 找不到任何 .toc 連結")
    return items


def out_name(stem, ch_no):
    if stem == "目錄":
        return "index.html"
    m = re.match(r"^R0-", stem)
    if m:
        return f"CH{ch_no}-0.html"
    m = re.match(r"^L(\d+)-", stem)
    if m:
        return f"CH{ch_no}-{int(m.group(1))}.html"
    fail(f"不認得的講義檔名：{stem}（只支援 R0-*、L<數字>-*、目錄）")


def rewrite_links(main, name_map, where):
    def sub(m):
        href = nfc(m.group(1))
        if re.match(r"^(https?:|mailto:|#)", href):
            return m.group(0)
        if href in name_map:
            return f'href="{name_map[href]}"'
        fail(f"{where} 有對不上的站內連結：{href}")
    return re.sub(r'href="([^"]*)"', sub, main)


def text_of(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


# ── 外殼 ─────────────────────────────────────────────
def head(cfg, title, desc, url, css):
    e = html.escape
    return f"""<!doctype html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="弄一下工作室">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(url)}">
<meta property="og:image" content="{e(cfg['og_image'])}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<link rel="canonical" href="{e(url)}">
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700&amp;family=Noto+Sans+TC:wght@400;500;700&amp;display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<a href="#main" class="skip-link">跳至主要內容</a>
"""


def topbar(root, course_href, cfg, tag):
    """舊版 .topbar：站名｜課程名（連到總目錄）｜目前位置標籤。"""
    sub = (f'<a class="sub" href="{course_href}">{cfg["short"]}</a>' if course_href
           else f'<span class="sub">{cfg["short"]}</span>')
    tag_html = f'<span class="tag">{tag}</span>' if tag else ""
    return f'<header class="topbar"><a class="logo" href="{root}">弄一下工作室</a>{sub}{tag_html}</header>\n'


def foot(cfg, built, note):
    return (f'<footer class="footer"><span>弄一下工作室 · {cfg["short"]}</span>'
            f'<small data-platform-version="{cfg["platform_version"]}" data-built-at="{built}">{note}</small></footer>\n')


def pager(prev, nxt):
    """舊版 .nav：左邊外框按鈕回上一份，右邊實心按鈕到下一份。prev/nxt = (href, 文字)。"""
    if not prev and not nxt:
        return ""
    out = ['<nav class="nav" aria-label="上一份與下一份">']
    if prev:
        out.append(f'<a href="{prev[0]}">← {prev[1]}</a>')
    if nxt:
        out.append(f'<a class="primary" href="{nxt[0]}">{nxt[1]} →</a>')
    out.append("</nav>\n")
    return "".join(out)


# ── 建置 ─────────────────────────────────────────────
def build_chapter(cfg, ch, src_root, out_dir, theme, built, report):
    n = ch["no"]
    src = src_root / ch["src"] / "_src"
    chap_dir = src_root / ch["src"]
    if not src.is_dir():
        fail(f"找不到章節來源：{src}")
    tpls = {nfc(p.stem): p for p in src.glob("*.tpl")}
    if "目錄" not in tpls:
        fail(f"{src} 缺 目錄.tpl")
    toc_tpl = parse_tpl(tpls["目錄"])
    toc = parse_toc(toc_tpl["main"])
    name_map = {"目錄.html": "index.html"}
    for stem in tpls:
        name_map[f"{stem}.html"] = out_name(stem, n)
    toc_stems = [it["href"][:-5] for it in toc]
    missing = [s for s in toc_stems if s not in tpls]
    extra = [s for s in tpls if s != "目錄" and s not in toc_stems]
    if missing:
        fail(f"目錄連到不存在的講義：{missing}")
    if extra:
        fail(f"有講義沒列在目錄：{extra}")

    ch_label = f"第{cn_num(n)}章"
    dest = out_dir / ch["dir"]
    dest.mkdir(parents=True, exist_ok=True)
    order = ["目錄"] + toc_stems
    for idx, stem in enumerate(order):
        tpl = parse_tpl(tpls[stem])
        where = f"{ch['src']}/{stem}.tpl"
        main = rewrite_links(tpl["main"], name_map, where)
        imgs = re.findall(r"\{\{IMG:([^}]+)\}\}", main)
        main = re.sub(r"\{\{IMG:([^}]+)\}\}", lambda m: embed(chap_dir / m.group(1)), main)
        left = re.findall(r"\{\{[^}]+\}\}", main)
        if left:
            fail(f"{where} 有沒替換的佔位符：{left}")
        css = minify(theme + "\n/* page */\n" + page_css(tpl["style"], where))
        lead = re.search(r'<p class="lead">(.*?)</p>', tpl["main"], re.S)
        desc = text_of(lead.group(1))[:150] if lead else tpl["title"]
        fname = name_map[f"{stem}.html"]
        url = f"{cfg['site_url']}{ch['dir']}/{'' if fname == 'index.html' else fname}"
        title = f"{tpl['title']}｜{cfg['short']}"
        if stem == "目錄":
            tag = f"{ch_label}目錄"
            first = toc[0]
            prev = ("../index.html", "課程總目錄")
            nxt = (name_map[first["href"]], f"從{first['no']}開始：{first['t']}")
        else:
            it = toc[idx - 1]
            tag = f"{ch_label} · {it['no']}"
            if idx == 1:
                prev = ("index.html", f"{ch_label}目錄")
            else:
                p = toc[idx - 2]
                prev = (name_map[p["href"]], f"上一份：{p['t']}")
            if idx < len(order) - 1:
                q = toc[idx]
                nxt = (name_map[q["href"]], f"下一份：{q['t']}")
            else:
                nxt = ("index.html", f"這一章做完了，回到{ch_label}目錄")
        page = (head(cfg, title, desc, url, css) + topbar("../../../index.html", "../index.html", cfg, tag)
                + f'<main id="main">{main}</main>\n' + pager(prev, nxt) + foot(cfg, built, "共學講義")
                + "".join(s + "\n" for s in tpl["scripts"]) + "</body>\n</html>\n")
        out = dest / fname
        out.write_text(page, encoding="utf-8")
        verify_main(out, tpl["main"], name_map, where)
        report.append((f"{ch['dir']}/{fname}", stem, len(imgs), out.stat().st_size))
    lead = re.search(r'<p class="lead">(.*?)</p>', toc_tpl["main"], re.S)
    return (lead.group(1).strip() if lead else ""), [(name_map[it["href"]], it) for it in toc]


def verify_main(out, tpl_main, name_map, where):
    got = re.search(r'<main id="main">(.*)</main>', out.read_text(encoding="utf-8"), re.S).group(1)
    got = re.sub(r"data:image/jpeg;base64,[A-Za-z0-9+/=]+", "{{IMG}}", got)
    exp = re.sub(r"\{\{IMG:[^}]+\}\}", "{{IMG}}", tpl_main)
    exp = re.sub(r'href="([^"]*)"', lambda m: f'href="{name_map.get(nfc(m.group(1)), m.group(1))}"', exp)
    if got != exp:
        i = next(k for k in range(min(len(got), len(exp))) if got[k] != exp[k]) if got[:len(exp)] != exp[:len(got)] else min(len(got), len(exp))
        fail(f"{where} 的 <main> 內容和來源不同，位置 {i}：\n來源：{exp[i-40:i+60]!r}\n輸出：{got[i-40:i+60]!r}")


def build_home(cfg, manifest, out_dir, theme, built, opened):
    """課程總目錄：舊版首頁的 hero＋從哪裡開始＋總覽表。opened = {章號: (章設定, 目錄lead, [(檔名, 目錄項)])}。"""
    e = html.escape
    chapters, phases = manifest["chapters"], manifest["phases"]
    rows = []
    for ph in phases:
        rows.append(f'<tr><th class="phase-heading" colspan="3" scope="colgroup">{e(ph["name"])}</th></tr>')
        for ch in chapters:
            if not ph["from"] <= ch["no"] <= ph["to"]:
                continue
            label = f"第{cn_num(ch['no'])}章"
            if ch["status"] == "open":
                _, _, toc = opened[ch["no"]]
                parts = "".join(f'<li><a href="{ch["dir"]}/{f}"><span class="pn">{e(it["no"])}</span>{e(it["t"])}</a></li>'
                                for f, it in toc)
                name = (f'<a class="unit-link" href="{ch["dir"]}/index.html">{e(ch["title"])}</a>'
                        f'<ol class="unit-parts">{parts}</ol>')
                rows.append(f'<tr class="is-open"><td class="unit-no">{label}</td><td class="unit-name">{name}</td>'
                            f'<td class="unit-status"><span class="status-open">已開放</span></td></tr>')
            else:
                rows.append(f'<tr class="is-soon"><td class="unit-no">{label}</td><td class="unit-name">{e(ch["title"])}</td>'
                            f'<td class="unit-status"><span class="status-soon">陸續開放中</span></td></tr>')
    first_no = min(opened)
    ch, lead, toc = opened[first_no]
    ch_label = f"第{cn_num(first_no)}章"
    f0, it0 = toc[0]
    start = (f'<section class="section" aria-labelledby="start-title"><h2 id="start-title">從哪裡開始？</h2>'
             f'<p class="section-lead">{e(cfg["start_lead"])}</p>'
             f'<div class="start-panel"><div class="start-kicker">開始位置｜{ch_label}</div>'
             f'<h3 class="start-title">{e(ch["title"])}</h3><p class="start-copy">{lead}</p>'
             f'<div class="actions"><a class="primary-action" href="{ch["dir"]}/{f0}">從{ch_label}{e(it0["no"])}開始 <span aria-hidden="true">→</span></a>'
             f'<a class="secondary-action" href="{ch["dir"]}/index.html">{ch_label}目錄</a>'
             f'<a class="secondary-action" href="#overview">查看總目錄</a></div></div></section>')
    n_open = sum(1 for c in chapters if c["status"] == "open")
    overview = (f'<section class="section" id="overview" aria-labelledby="overview-title">'
                f'<h2 id="overview-title">課程總目錄：{len(chapters)} 章</h2>'
                f'<p class="section-lead">目前開放 {n_open} 章，其餘章節陸續開放中。從第一章開始，一章做完再進下一章。</p>'
                f'<table class="overview-table"><thead><tr><th scope="col">章</th><th scope="col">名稱</th><th scope="col">狀態</th></tr></thead>'
                f'<tbody>{"".join(rows)}</tbody></table></section>')
    main = (f'<section class="hero"><div class="kicker">{e(cfg["kicker"])}</div><h1>{e(cfg["title"])}</h1>'
            f'<p class="hero-lead">{e(cfg["lead"])}</p></section>{start}{overview}')
    page = (head(cfg, cfg["title"], cfg["lead"], cfg["site_url"], minify(theme))
            + topbar("../../index.html", None, cfg, f"{n_open}／{len(chapters)} 章已開放")
            + f'<main id="main" class="home">{main}</main>\n' + foot(cfg, built, "課程總目錄") + "</body>\n</html>\n")
    (out_dir / "index.html").write_text(page, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(COURSE_DIR))
    args = ap.parse_args()
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((HERE / "chapters.json").read_text(encoding="utf-8"))
    cfg = manifest["course"]
    src_root = (REPO / manifest["source_root"]).resolve()
    theme = (HERE / "theme.css").read_text(encoding="utf-8")
    built = datetime.date.today().isoformat()
    report, opened = [], {}
    for ch in manifest["chapters"]:
        if ch["status"] == "open":
            lead, toc = build_chapter(cfg, ch, src_root, out_dir, theme, built, report)
            opened[ch["no"]] = (ch, lead, toc)
        elif ch["status"] != "soon":
            fail(f"第 {ch['no']} 章 status 只能是 open 或 soon")
    if not opened:
        fail("至少要有一章 status=open")
    build_home(cfg, manifest, out_dir, theme, built, opened)
    print(f"輸出到：{out_dir}")
    print(f"{'檔案':<22}{'圖片':>4}{'大小':>10}  來源")
    for f, stem, nimg, size in report:
        print(f"{f:<22}{nimg:>4}{size/1024:>8.0f}KB  {stem}")
    print(f"index.html（課程首頁）")
    print(f"共 {len(report)} 頁，{sum(r[2] for r in report)} 張圖，<main> 內容逐頁比對與來源一致。")


if __name__ == "__main__":
    main()
