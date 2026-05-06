#!/usr/bin/env python3
"""
n8n Lite Pack 演練素材包生成腳本

產生 14 個 workflow 演練用的範例素材：
- 真實 PDF（reportlab）
- 真實 docx / pptx / xlsx（python-docx / pptx / openpyxl）
- markdown / txt / csv / json（純文字）
- PNG 佔位圖（PIL）
- README + 對照表

產出位置：./out/n8n-sample-pack/
打包：./out/n8n-sample-pack.zip
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from docx import Document
from pptx import Presentation
from pptx.util import Inches, Pt
from openpyxl import Workbook
from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).parent
OUT = HERE / "out" / "n8n-sample-pack"
ZIP_OUT = HERE / "out" / "n8n-sample-pack.zip"

# ── 註冊中文字型（reportlab 內建 STSong-Light 涵蓋繁中常用字） ──
pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))


def reset_dirs():
    if OUT.exists():
        shutil.rmtree(OUT)
    if ZIP_OUT.exists():
        ZIP_OUT.unlink()
    OUT.mkdir(parents=True)


def make_pdf(path: Path, title: str, body_paragraphs: list[str]):
    """用 reportlab 生繁中 PDF。"""
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    h_style = ParagraphStyle(
        "h", parent=styles["Title"],
        fontName="STSong-Light", fontSize=18, leading=24,
        alignment=TA_LEFT, spaceAfter=14,
    )
    p_style = ParagraphStyle(
        "p", parent=styles["BodyText"],
        fontName="STSong-Light", fontSize=11, leading=18,
        alignment=TA_LEFT, spaceAfter=10,
    )
    story = [Paragraph(title, h_style), Spacer(1, 6)]
    for para in body_paragraphs:
        story.append(Paragraph(para.replace("\n", "<br/>"), p_style))
    doc.build(story)


def make_docx(path: Path, title: str, body_paragraphs: list[str]):
    doc = Document()
    doc.add_heading(title, level=1)
    for p in body_paragraphs:
        doc.add_paragraph(p)
    doc.save(str(path))


def make_pptx(path: Path, title: str, slides: list[tuple[str, list[str]]]):
    prs = Presentation()
    # Title slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    slide.shapes.title.text = title
    if slide.placeholders[1]:
        slide.placeholders[1].text = "n8n Lite Pack 演練素材"
    # Content slides
    bullet_layout = prs.slide_layouts[1]
    for sub_title, bullets in slides:
        slide = prs.slides.add_slide(bullet_layout)
        slide.shapes.title.text = sub_title
        body = slide.placeholders[1].text_frame
        body.text = bullets[0] if bullets else ""
        for b in bullets[1:]:
            p = body.add_paragraph()
            p.text = b
    prs.save(str(path))


def make_xlsx(path: Path, sheet_name: str, header: list[str], rows: list[list]):
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name
    ws.append(header)
    for r in rows:
        ws.append(r)
    wb.save(str(path))


def make_png(path: Path, text: str, size=(1200, 800), bg=(245, 243, 238), fg=(45, 50, 60)):
    img = Image.new("RGB", size, bg)
    draw = ImageDraw.Draw(img)
    # Try a system font; fall back to default
    font = None
    for f in [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]:
        if os.path.exists(f):
            try:
                font = ImageFont.truetype(f, 64)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size[0] - tw) / 2, (size[1] - th) / 2), text, fill=fg, font=font)
    img.save(str(path), "PNG")


def write_text(path: Path, content: str):
    path.write_text(content, encoding="utf-8")


# ─────────────────────────────────────────────
# 各分區生成
# ─────────────────────────────────────────────


def gen_pdf_inbox():
    """#02 PDF AI 改名 — 3 個檔名無意義的 PDF，內容各異"""
    d = OUT / "pdf-inbox"
    d.mkdir()

    make_pdf(
        d / "doc-001.pdf",
        "保密協議書（NDA）",
        [
            "本協議由甲方（弄一下工作室）與乙方（客戶 A 公司）於 2026 年 5 月 6 日簽訂。",
            "甲方因業務合作之需要，將向乙方揭露包含但不限於：商業計畫、技術文件、客戶名單、財務資料等機密資訊。",
            "乙方承諾於本協議有效期間及終止後三年內，不得對外揭露任何前述機密資訊，亦不得用於本協議目的以外之用途。",
            "如乙方違反本協議，應賠償甲方因此所受之一切損失，包括但不限於直接損失、間接損失與律師費用。",
            "本協議自雙方簽署之日起生效，有效期間為兩年。",
            "甲方代表：白辰幃　　　　乙方代表：（簽名處）",
        ],
    )

    make_pdf(
        d / "doc-002.pdf",
        "服務報價單",
        [
            "報價單編號：QT-2026-Q2-038",
            "報價日期：2026 年 5 月 6 日　　有效期限：30 天",
            "客戶名稱：客戶 B 股份有限公司",
            "─────────────────────────────",
            "項目一：n8n 流程自動化顧問導入　　　數量：1 式　　單價：NT$ 80,000",
            "項目二：客製 workflow 設計（5 個流程）　數量：1 式　　單價：NT$ 60,000",
            "項目三：6 小時內部培訓工作坊　　　　　數量：1 式　　單價：NT$ 35,000",
            "項目四：3 個月維運支援（每月 4 小時）　數量：1 式　　單價：NT$ 25,000",
            "─────────────────────────────",
            "小計：NT$ 200,000　　稅金 5%：NT$ 10,000　　總計：NT$ 210,000",
            "付款條件：簽約付 50% 訂金，驗收後付清。",
        ],
    )

    make_pdf(
        d / "doc-003.pdf",
        "提示詞工程基礎教材",
        [
            "本教材帶你從零學會 Prompt Engineering 的核心概念。",
            "什麼是提示詞：給大語言模型（LLM）的輸入文字，影響模型輸出品質的關鍵。",
            "好提示詞的四個元素：角色（你是誰）、任務（要做什麼）、限制（不要做什麼）、輸出格式（怎麼回）。",
            "範例對比：『幫我寫個郵件』（壞）vs『你是業務助理。寫一封給客戶 A 的延遲交付道歉信，繁中、200 字內、語氣誠懇但不卑微』（好）。",
            "進階技巧：Few-shot prompting（給範例）、Chain-of-thought（讓模型逐步思考）、Self-consistency（多次採樣選最常見答案）。",
            "本課程後續將涵蓋 Function Calling、RAG、Agent 等高階技巧。",
        ],
    )


def gen_batch_inbox():
    """#03 批次錯誤恢復 — 4 個正常 + 1 個損壞"""
    d = OUT / "batch-inbox"
    d.mkdir()
    for i in range(1, 5):
        write_text(
            d / f"good-{i:02d}.txt",
            f"這是第 {i} 份正常的批次處理輸入檔。\n內容只是純文字，n8n 應該能順利讀進來、處理、寫出。",
        )
    # 損壞檔（非 UTF-8 二進制）— 觸發 #03 的錯誤恢復路徑
    (d / "corrupted.bin").write_bytes(bytes([0xFF, 0xFE, 0x00, 0x42, 0xC3, 0x28, 0x00]) * 50)


def gen_daily_input():
    """#04 定時 AI 日報 — .md / .txt 混合"""
    d = OUT / "daily-input"
    d.mkdir()
    write_text(
        d / "週一會議記錄.md",
        """# 5/6 週一例會

## 出席
白辰幃、客戶 A 經理、PM Vincent

## 議題
1. **n8n 課程進度**：14 個 workflow 已完工，今日進入 0-10 全面驗證階段。
2. **客戶 B 提案**：本週五前交報價單（總額 21 萬，含 6h 工作坊 + 3 個月維運）。
3. **GAI 認證研習**：下週 PR review 時把模擬考引擎 export 成 standalone JSON。

## 待辦
- [ ] 5/6 下班前修完 #10 RPM 限速問題（**P0**）
- [ ] 5/8 寄報價單給客戶 B（**P1**）
- [ ] 5/10 跟 PM Vincent 對齊認證研習宣傳素材（**P2**）

## 風險
GAI Free Tier RPM 限速可能影響課堂 demo 流暢度，需準備 paid key 備援。
""",
    )
    write_text(
        d / "客戶反饋本週.txt",
        """週客戶反饋彙整 2026/5/6

客戶 A：
- n8n Cloudflare Tunnel 設定文件清楚，自己完成接 webhook
- 反映 #04 定時日報希望支援 PDF 內容（已於 v0.7 加 Switch 完成）

客戶 B：
- 詢問是否能客製分類規則（合約 / 設計稿 / 報價單）
- 報價要求：總價控制在 20 萬內，分期付款

客戶 C：
- 對 #10 客戶資料夾整理高度有興趣（自己有大量未分類客戶檔）
- 詢問是否能改 prompt 換業務術語

整體：自動化流程教學的需求高度集中在「文件處理」「客戶整理」兩塊。下季可考慮把這兩塊獨立成單堂課程。
""",
    )
    write_text(
        d / "專案進度Q2.md",
        """# 專案進度 · 2026 Q2

## 已完成
- AI 資料工廠（n8n）課程改版 v1.0 → v1.6（PDF 修補、批次優化、rule-based fallback）
- Lite Pack 14 個 workflow 全部上線
- Cloud vs self-host 補充章節
- Win/Mac 雙系統 setup-wizard 強化

## 進行中
- 結業後補充教材（LLM Copilot 系列 8 頁 + Cloud 決策 1 頁）
- 課前 0-10 全面驗證（Mac + Win 雙端）

## 即將啟動
- GAI 認證研習模擬考引擎獨立化
- 工作坊招生頁改版（landing 風格）
""",
    )


def gen_client_inbox():
    """#10 客戶資料夾整理 — mixed file types，覆蓋 6 個分類"""
    d = OUT / "client-inbox"
    d.mkdir()

    # PDF 合約類
    make_pdf(
        d / "合約_NDA_客戶A.pdf",
        "保密協議書 NDA",
        [
            "本協議用於甲方與乙方共同合作期間之資訊保密。",
            "乙方不得將任何商業機密揭露給第三方。",
            "違反本協議將承擔法律責任。",
        ],
    )
    # PDF 報價類
    make_pdf(
        d / "Q3-報價單.pdf",
        "Q3 報價單",
        [
            "報價單編號：QT-2026-Q3-012",
            "客戶：客戶 C",
            "服務內容：n8n 自動化導入 + 工作坊。",
            "總計：NT$ 180,000",
        ],
    )
    # PPTX 簡報類
    make_pptx(
        d / "客戶提案-v1.pptx",
        "客戶 X 自動化導入提案",
        [
            ("專案概述", ["背景：客戶 X 目前手動處理客戶資料夾", "目標：自動分類 + 命名 + 通知", "預計效益：每週節省 8 小時人工"]),
            ("解決方案", ["n8n 流程自動化平台", "Gemini AI 分類引擎", "Cloudflare Tunnel 公開 webhook"]),
            ("時程與報價", ["導入：4 週", "培訓：6 小時工作坊", "報價：總額 NT$ 210,000"]),
        ],
    )
    # DOCX 教材類（兩份）
    make_docx(
        d / "01提示詞基礎.docx",
        "01 提示詞基礎",
        [
            "什麼是提示詞：給 LLM 的輸入文字。",
            "好提示詞的四個元素：角色、任務、限制、輸出格式。",
            "範例：『你是業務助理。寫一封給客戶的道歉信。』",
        ],
    )
    make_docx(
        d / "02提示詞進階.docx",
        "02 提示詞進階",
        [
            "Few-shot prompting：在 prompt 內給 2-5 個範例。",
            "Chain-of-thought：讓模型逐步思考。",
            "Self-consistency：多次採樣選最常見答案。",
        ],
    )
    # XLSX 報表類
    make_xlsx(
        d / "業務報表-2026Q2.xlsx",
        "Q2 業績",
        ["客戶", "案件", "金額", "狀態"],
        [
            ["客戶A", "n8n 導入", 200000, "已成交"],
            ["客戶B", "工作坊", 35000, "提案中"],
            ["客戶C", "顧問諮詢", 60000, "已成交"],
        ],
    )
    # PNG 圖檔
    make_png(d / "螢幕擷取-產品介面.png", "產品介面 V1\n2026/05/06")
    # MD 紀錄類
    write_text(
        d / "會議記錄-0506.md",
        """# 5/6 例會紀錄

## 出席
白辰幃、PM Vincent

## 結論
- #10 改 v1.6 加 rule-based fallback
- 課前驗證走完 0-10 動線
- 下午 14:30 跟客戶 B 對齊報價
""",
    )


def gen_leads_inbox():
    """#11 CSV 線索清洗 — 含重複/缺欄/格式不一的雜亂資料"""
    d = OUT / "leads-inbox"
    d.mkdir()
    csv_content = """name,email,phone,company,source,note
王大明,wang@example.com,0912-345-678,A公司,LinkedIn,有興趣
李美麗,LiMei@Example.COM,0922 333 444,B 股份有限公司,展會,需要報價
,nobody@x.tw,0911111111,C 工作室,網站,
王大明,wang@example.com,0912345678,A公司,Email,重複線索
陳志強,chen@d.com,,D 文創,推薦,熱門客戶
林小芳,lin@e.com.tw,02-2345-6789,E 顧問,LinkedIn,
張三,san@f.tw,0900000000,F,Phone,
李四,si@g.tw,0987654321,G 公司,Email,要 quote
,blank@x,,,,
趙六,zhao@h.com,+886-921-555-666,H 集團,展會,VIP
錢七,qian@i.tw,0933 222 111,I 設計,LinkedIn,
孫八,sun@j.tw,,J,網站,需 demo
陳志強,chen@d.com,0966-555-777,D 文創,推薦,重複
周九,zhou@k.com,02 12345678,K 顧問,Email,合約洽談中
吳十,wu@L.com,0988123456,L 公司,展會,熱門
鄭一,zheng@m.tw,,M,網站,
小張,xiao@n.com,0911-000-999,N 工作室,LinkedIn,需要諮詢
小王,xwang@o.tw,0900-111-222,O 科技,Email,
小李,xli@p.com,03-1234567,P 顧問,Phone,VIP
,,,,,
測試 1,test@q.tw,0900-000-001,Q,Test,測試資料勿留
測試 2,test@q.tw,0900-000-002,Q,Test,重複測試
劉一二,liu@r.com,0922-888-999,R 集團,LinkedIn,合約簽訂中
何三四,he@s.tw,02-87654321,S 文創,推薦,
段五六,duan@t.com,+886-911-222-333,T 顧問,展會,VIP
姚七八,yao@u.tw,0966-111-222,U 公司,網站,
邵九十,shao@v.com,0955-444-333,V 工作室,Email,
小陳,xchen@w.tw,03-7654321,W 集團,Phone,
小林,xlin@x.tw,0922 555 666,X 設計,LinkedIn,熱門
黃十一,huang@y.com,0911 222 333,Y,展會,
"""
    write_text(d / "leads-raw.csv", csv_content)


def gen_knowledge_docs():
    """#12 本地知識庫 RAG — 4 份知識文件"""
    d = OUT / "knowledge-docs"
    d.mkdir()
    write_text(
        d / "公司介紹.md",
        """# 弄一下工作室

弄一下工作室是一家專注於 AI 自動化教學與顧問導入的工作室，2024 年成立。

## 服務項目
- AI 資料工廠課程（n8n + Gemini）
- Gen AI 認證研習與商業應用工作坊
- 自動化流程顧問導入（n8n + Cloudflare Tunnel）

## 創辦人
白辰幃，曾任數家科技公司產品經理與設計師，專注於把複雜技術轉成可教可用的流程。

## 客戶
中小企業、行銷團隊、設計工作室、顧問公司、課程講師。
""",
    )
    write_text(
        d / "產品 FAQ.md",
        """# 產品常見問題

## Q1：n8n 跟 Make 差別？
n8n 是自架版自動化平台（資料留本機），Make 是雲端 SaaS。n8n 適合資料隱私敏感、流程量大、想客製節點的團隊。

## Q2：免費版 Gemini 有哪些限制？
免費 tier 限制：每分鐘 10 次（RPM）/ 每天 250 次（RPD）/ 每分鐘 25 萬 tokens（TPM）。批次處理多檔可能撞限速。

## Q3：要怎麼把 n8n 對外公開？
用 Cloudflare Tunnel 一鍵接通，或自架 reverse proxy。本工作室提供完整 setup-wizard 自動化。

## Q4：客戶導入大約多久？
標準 4 週，含需求訪談、流程設計、實作、培訓、驗收。
""",
    )
    write_text(
        d / "退款政策.md",
        """# 退款政策

## 課程退款
- 開課前 7 天以上：全額退款
- 開課前 1-7 天：退 80%
- 開課後 24 小時內未上課：退 50%
- 開課後超過 24 小時或已上課：不退款

## 顧問導入退款
- 簽約後 7 天內，未開始實作：全額退款
- 開始實作後：依完成比例計算

## 工具授權退款
帳號開通後不退款，但可轉讓給他人使用。
""",
    )
    write_text(
        d / "客戶案例集.md",
        """# 客戶案例集

## 案例 1：A 公司（電商）
- 痛點：每天人工分類客戶 email，每週耗 8 小時
- 解法：用 #09 Gmail 分類 workflow 自動歸檔到 4 路 Switch
- 效益：每週節省 8 小時，分類準確度 92%

## 案例 2：B 公司（行銷）
- 痛點：銷售線索 CSV 雜亂，重複資料多
- 解法：用 #11 CSV 清洗評分 workflow 自動 dedupe + AI 評分
- 效益：500 筆線索 5 分鐘清完，過往要兩天

## 案例 3：C 工作室（設計）
- 痛點：客戶提供的檔案資料夾混亂，每月整理 4 小時
- 解法：用 #10 客戶資料夾自動整理 + Telegram 通知
- 效益：每月節省 4 小時，加上完整交接清單給客戶
""",
    )


def gen_ops_input():
    """#13 ops snapshot — 系統 metrics CSV"""
    d = OUT / "ops-input"
    d.mkdir()
    csv_content = """timestamp,service,metric,value,unit
2026-05-06T08:00:00,api-gateway,requests_per_min,1240,count
2026-05-06T08:00:00,api-gateway,error_rate,0.8,percent
2026-05-06T08:00:00,api-gateway,p95_latency,180,ms
2026-05-06T09:00:00,api-gateway,requests_per_min,1580,count
2026-05-06T09:00:00,api-gateway,error_rate,1.2,percent
2026-05-06T09:00:00,api-gateway,p95_latency,210,ms
2026-05-06T10:00:00,api-gateway,requests_per_min,1820,count
2026-05-06T10:00:00,api-gateway,error_rate,4.5,percent
2026-05-06T10:00:00,api-gateway,p95_latency,520,ms
2026-05-06T11:00:00,api-gateway,requests_per_min,1950,count
2026-05-06T11:00:00,api-gateway,error_rate,8.2,percent
2026-05-06T11:00:00,api-gateway,p95_latency,890,ms
2026-05-06T08:00:00,db-primary,connections,45,count
2026-05-06T08:00:00,db-primary,query_p95,12,ms
2026-05-06T09:00:00,db-primary,connections,52,count
2026-05-06T09:00:00,db-primary,query_p95,18,ms
2026-05-06T10:00:00,db-primary,connections,78,count
2026-05-06T10:00:00,db-primary,query_p95,45,ms
2026-05-06T11:00:00,db-primary,connections,95,count
2026-05-06T11:00:00,db-primary,query_p95,120,ms
"""
    write_text(d / "metrics-2026-05-06.csv", csv_content)


def gen_readme():
    write_text(
        OUT / "README.md",
        """# n8n Lite Pack 演練素材包

對應 14 個 workflow 的測試素材。把對應子資料夾的內容**複製**到你的 starter-kit 內（**不要動原本的 shared 資料夾結構**）：

## 使用方法

1. 解壓本 zip 到任意地方
2. 把各子資料夾內的檔**複製**到 `n8n-starter-kit/shared/<對應資料夾>/`
3. 開 n8n UI → 對應 workflow → Execute

## 對照表

| 子資料夾 | 對應 workflow | 用途 |
|---|---|---|
| `pdf-inbox/` | #02 PDF AI 改名 | 3 個檔名無意義 PDF（合約 / 報價單 / 教材內容）測試 AI 改名 |
| `batch-inbox/` | #03 批次錯誤恢復 | 4 個正常 + 1 個損壞檔（corrupted.bin）測試錯誤路徑 |
| `daily-input/` | #04 定時 AI 日報 | .md + .txt 混合測試多格式摘要 |
| `client-inbox/` | #10 客戶資料夾整理 | PDF/PPTX/DOCX/XLSX/PNG/MD mixed，覆蓋 6 個分類 |
| `leads-inbox/` | #11 CSV 線索清洗 | 30 筆雜亂線索（含重複/缺欄/格式不一）測試清洗評分 |
| `knowledge-docs/` | #12 本地知識庫 RAG | 4 份知識文件（公司 / FAQ / 退款 / 案例）測試 RAG 索引 |
| `ops-input/` | #13 ops snapshot | API gateway + DB metrics CSV（含異常 spike）測試告警 |

**不需要素材的 workflow**（webhook trigger / OAuth credential / 設定驅動）：
- #01 webhook hello world
- #05 Telegram 通知測試
- #06 Webhook → Gemini → 本機檔（POST 觸發）
- #07 Quick Tunnel receiver
- #08 Expression 練習
- #09 Gmail 分類（需 OAuth）
- #14 API monitor（在 workflow 內設定 API list）

## 重新產生

如果想客製或補檔，跑這個腳本：

```bash
pip install reportlab python-docx python-pptx openpyxl pillow
python3 build_sample_pack.py
```
""",
    )


def make_zip():
    with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(OUT):
            for f in files:
                full = Path(root) / f
                rel = full.relative_to(OUT.parent)
                z.write(full, rel)
    print(f"✓ 打包：{ZIP_OUT} ({ZIP_OUT.stat().st_size / 1024:.1f} KB)")


def main():
    print(f"產出位置：{OUT}")
    reset_dirs()
    gen_pdf_inbox()
    print("✓ pdf-inbox/ — 3 個 PDF")
    gen_batch_inbox()
    print("✓ batch-inbox/ — 4 個正常 + 1 個損壞")
    gen_daily_input()
    print("✓ daily-input/ — 3 個 markdown/txt")
    gen_client_inbox()
    print("✓ client-inbox/ — 8 個 mixed")
    gen_leads_inbox()
    print("✓ leads-inbox/ — 1 個 CSV")
    gen_knowledge_docs()
    print("✓ knowledge-docs/ — 4 個 markdown")
    gen_ops_input()
    print("✓ ops-input/ — 1 個 metrics CSV")
    gen_readme()
    print("✓ README.md")
    make_zip()


if __name__ == "__main__":
    main()
