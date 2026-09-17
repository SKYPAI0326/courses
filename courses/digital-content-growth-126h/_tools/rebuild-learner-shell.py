#!/usr/bin/env python3
"""Rebuild the learner-facing shell for digital-content-growth-126h.

The script deliberately keeps the teaching body from each existing lesson.
It replaces only the page chrome, navigation, production-status leakage, and
course/module landing structures.
"""

from __future__ import annotations

import re
import subprocess
import json
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import quote

from bs4 import BeautifulSoup, Comment


COURSE_DIR = Path(__file__).resolve().parents[1]
REPAIR_DIR = COURSE_DIR / "_repair" / "2026-09-17"
BACKUP_HTML_DIR = COURSE_DIR / "_backup" / "2026-09-17-pre-fillable-workbook-repair" / "html"
COURSE_TITLE = "數位內容與成長行銷人才培訓"
INSTITUTION = "弄一下工作室"
SITE_BASE_URL = "https://skypai0326.github.io/courses"
COURSE_URL = f"{SITE_BASE_URL}/digital-content-growth-126h"
ASSET_CONTRACTS_PATH = COURSE_DIR / "_tools" / "asset-contracts.json"


def load_asset_contracts() -> dict:
    return json.loads(ASSET_CONTRACTS_PATH.read_text(encoding="utf-8"))


ASSET_CONTRACTS = load_asset_contracts()


WORKBOOK_CSS = """
.workbook-panel {
  margin: 1.25rem 0 2rem;
  padding: 1.25rem;
  border: 1px solid #c8d4c9;
  border-radius: 0.75rem;
  background: #f3f7f2;
}
.workbook-panel h2 { margin: 0 0 0.5rem; font-size: 1.15rem; }
.workbook-panel p { margin: 0.35rem 0; }
.workbook-panel ol { margin: 0.75rem 0 0.9rem 1.25rem; padding: 0; }
.workbook-actions { display: flex; flex-wrap: wrap; gap: 0.6rem; align-items: center; }
.workbook-actions button { cursor: pointer; font: inherit; }
.workbook-status { color: #526256; font-size: 0.92rem; }
.workbook-field-cell { min-width: 16rem; vertical-align: top; }
.workbook-field-guide { margin-bottom: 0.45rem; color: #5d665e; font-size: 0.92rem; }
.workbook-field {
  display: block;
  box-sizing: border-box;
  width: 100%;
  min-height: 4.5rem;
  padding: 0.65rem;
  border: 1px solid #8fa391;
  border-radius: 0.35rem;
  background: #fff;
  color: #222;
  font: inherit;
  line-height: 1.55;
  resize: vertical;
}
.workbook-field:focus { outline: 2px solid #526b57; outline-offset: 2px; }
.workbook-inline-field { min-height: 2.75rem; }
.workbook-filled-value {
  min-height: 2.5rem;
  padding: 0.55rem;
  border: 1px solid #d0d8d0;
  background: #fff;
  white-space: pre-wrap;
}
.workbook-fallback { margin-top: 1.5rem; }
"""

EDITABLE_HEADER_MARKERS = (
    "填寫",
    "我的",
    "回答",
    "內容",
    "實際",
    "結果",
    "錯誤",
    "來源",
    "證據",
    "狀態",
    "修正",
    "判斷",
    "任務",
    "版本",
    "日期",
    "理由",
    "主張",
    "成果",
    "限制",
    "觀察",
    "數值",
    "預算",
    "成本",
    "CTA",
    "平台",
    "受眾",
    "用途",
    "輸入",
    "計算",
    "交付",
    "下一步",
    "新增",
    "取用",
)

PROTECTED_HEADER_MARKERS = (
    "操作",
    "預期",
    "通過證據",
    "示範",
    "參考",
    "不等於",
)


def asset_kind_for_code(code: str) -> str:
    """依集中式資產契約分成可填寫工作表與只讀參考資產。"""
    override = ASSET_CONTRACTS.get("kind_overrides", {}).get(code)
    if override:
        return override
    markers = ASSET_CONTRACTS.get("reference_name_markers", [])
    if any(marker in code for marker in markers):
        return "reference"
    return ASSET_CONTRACTS.get("default_kind", "worksheet")


def normalize_static_reference_pages() -> None:
    """Keep fixed, hand-authored reference pages under the repository Pages base."""
    stale_base = "https://skypai0326.github.io/courses/courses/"
    current_base = f"{SITE_BASE_URL}/"
    for filename in ASSET_CONTRACTS.get("static_reference_pages", []):
        path = TEMPLATE_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"static reference page missing: {path}")
        page = path.read_text(encoding="utf-8")
        normalized = page.replace(stale_base, current_base)
        if normalized != page:
            path.write_text(normalized, encoding="utf-8")


def asset_kind_label(kind: str) -> str:
    return "可填寫工作版" if kind == "worksheet" else "HTML 參考版"


def work_download_name(code: str, kind: str) -> str:
    """給下載檔使用不會和舊檔撞名且能表達資產用途的檔名。"""
    suffix = "可填寫工作版" if kind == "worksheet" else "參考版"
    return f"{code}-{suffix}-獨立版.html"


def work_page_name(code: str, kind: str) -> str:
    """站內檔名也反映用途，避免參考頁偽裝成工作版。"""
    suffix = "工作版" if kind == "worksheet" else "參考版"
    return f"{code}-{suffix}.html"
OG_IMAGE = "https://skypai0326.github.io/courses/素材/og-default.png"
TODAY = date.today().isoformat()
TEMPLATE_DIR = COURSE_DIR / "assets" / "templates"
DATASET_DIR = COURSE_DIR / "assets" / "datasets"
SOURCE_DIR = COURSE_DIR.parent.parent / "_lessons" / COURSE_DIR.name
COURSE_SHELL_CSS = COURSE_DIR / "assets" / "course-shell.css"
COURSE_FAVICON = COURSE_DIR / "assets" / "favicon.svg"


PARTS = [
    {
        "number": 1,
        "title": "創業企劃與能力方向・前段",
        "hours": "4h",
        "purpose": "把專長或點子整理成共同 Brief，建立後續五科共用的任務框架。",
        "output": "共同服務／品牌 Brief",
        "units": [
            ("CH1-1", "從專長／點子到應用情境", "把專長或點子改寫成可用於求職、企業專案、自由工作或個人品牌的應用情境。", "1h"),
            ("CH1-2", "問題、受眾與需求", "把模糊想法改寫成目標對象與可觀察問題。", "1h"),
            ("CH1-3", "服務價值與共同任務框架", "建立價值主張、溝通目標與後續科目共用的內容任務。", "1h"),
            ("PRAC1", "建立個人服務／微型品牌 Brief", "完成後續五科共用的主題、受眾、價值與工作簡報。", "1h"),
        ],
    },
    {
        "number": 2,
        "title": "攝影與影片編修",
        "hours": "30h",
        "purpose": "從影像任務、腳本、素材來源與視覺資產，完成一組可行銷內容。",
        "output": "短影音、平面資產、來源紀錄與行銷判斷說明",
        "units": [
            ("CH2-1", "影像在行銷中的角色", "區分品牌認知、受眾理解、信任建立與行動促成的影像任務。", "3h"),
            ("CH2-2", "受眾、訊息與內容定位", "將服務 Brief 轉成影像主題、訊息層級與內容角度。", "3h"),
            ("CH2-3", "腳本、分鏡與平台格式", "依受眾與使用情境設計開頭、敘事、CTA 與版本需求。", "4h"),
            ("CH2-4", "素材取得", "比較自行拍攝、有授權素材與 AI 生成三種路徑，完成來源與風險紀錄。", "4h"),
            ("CH2-5", "Affinity 視覺資產製作", "使用向量、影像與排版工具建立品牌與社群所需的視覺資產。", "4h"),
            ("CH2-6", "剪輯判斷", "依訊息、節奏、字幕、聲音與 CTA 做取捨，不追求特效堆疊。", "4h"),
            ("CH2-7", "Windows 本機剪輯與輸出", "使用課前驗證的免費工具完成匯入、時間軸、字幕、音訊與輸出。", "4h"),
            ("PRAC2", "完成一組可行銷內容", "交付短影音、平面素材、來源紀錄與行銷判斷說明。", "4h"),
        ],
    },
    {
        "number": 3,
        "title": "社群媒體經營",
        "hours": "30h",
        "purpose": "選擇平台角色，建立內容支柱、月曆、互動規則與成效紀錄。",
        "output": "平台策略、內容月曆、內容樣稿、互動規則與成效紀錄表",
        "units": [
            ("CH3-1", "平台角色與選擇", "區分 Instagram、Facebook、Threads 與 LINE 在觸及、互動、承接與回訪的功能。", "3h"),
            ("CH3-2", "受眾、定位與內容支柱", "建立社群主題、內容支柱與可持續的表達方式。", "4h"),
            ("CH3-3", "內容改編與跨平台分發", "將 PRAC2 素材改寫成不同平台的貼文、短影音與互動內容。", "4h"),
            ("CH3-4", "內容月曆與發布流程", "規劃頻率、節奏、素材狀態、CTA 與協作紀錄。", "4h"),
            ("CH3-5", "互動、私訊與風險處理", "建立留言、私訊、負評與敏感情境的回應原則。", "4h"),
            ("CH3-6", "自然觸及與社群成效", "讀取基本指標，區分曝光、互動、導流與轉換訊號。", "4h"),
            ("CH3-7", "LINE 延伸：名單承接與回訪", "設計從社群觸及到名單承接與後續溝通的簡單路徑。", "3h"),
            ("PRAC3", "完成社群經營方案", "交付平台策略、內容月曆、內容樣稿、互動規則與成效紀錄表。", "4h"),
        ],
    },
    {
        "number": 4,
        "title": "SEO 與網站行為追蹤",
        "hours": "24h",
        "purpose": "從搜尋意圖走到 LocalWP、GA4、GTM 與 GSC 資料支持的行銷決策。",
        "output": "SEO、GA4、GTM 證據整合與優化行動",
        "units": [
            ("CH4-1", "搜尋生態與搜尋意圖", "連結服務 Brief、受眾問題與 SEO／內容機會。", "3h"),
            ("CH4-2", "關鍵字與內容規劃", "依搜尋意圖建立關鍵字群組、頁面目的與內容優先序。", "3h"),
            ("CH4-3", "頁面與技術基本檢查", "在 LocalWP 網站檢查標題、階層、連結、索引與基本技術問題。", "3h"),
            ("CH4-4", "GA4 資料模型與 Demo Account", "區分使用者、工作階段、事件、參數與轉換，建立閱讀地圖。", "3h"),
            ("CH4-5", "GA4 報表與探索分析", "從流量來源、行為與路徑資料提出內容或渠道假設。", "3h"),
            ("CH4-6", "GTM 概念與基礎佈建", "在 LocalWP 示範網站設定標籤、觸發條件與變數。", "3h"),
            ("CH4-7", "事件驗證與轉換判讀", "使用 DebugView 或等價驗證路徑，將事件連到行銷決策。", "3h"),
            ("PRAC4", "GSC 資料包與追蹤決策", "判讀教師提供的 GSC 資料，整合 SEO、GA4 與 GTM 證據提出優化行動。", "3h"),
        ],
    },
    {
        "number": 5,
        "title": "國際數位廣告投放實務",
        "hours": "30h",
        "purpose": "從市場與受眾選擇、渠道配置、素材與預算，完成兩輪資料決策的投放企劃。",
        "output": "一平台深度投放包、另一平台轉譯版本、兩輪決策紀錄與優化報告",
        "units": [
            ("CH5-1", "國際市場與受眾選擇", "依服務條件、需求、語言、文化與可觸及性選擇市場。", "3h"),
            ("CH5-2", "自然流量與付費流量", "建立漏斗、渠道角色、目標與預算配置的判斷框架。", "3h"),
            ("CH5-3", "Google Ads 企劃", "設計搜尋意圖、關鍵字、廣告文案、落地頁與測試假設。", "4h"),
            ("CH5-4", "Meta Ads 企劃", "設計受眾、素材變體、版位、訊息與再行銷情境。", "4h"),
            ("CH5-5", "LINE Ads 延伸與渠道比較", "比較名單承接、訊息與廣告渠道的配合方式。", "2h"),
            ("CH5-6", "預算與情境模擬", "使用模擬表比較市場、渠道、素材與預算的不同結果。", "4h"),
            ("CH5-7", "兩輪資料決策實驗", "讀取 Round 1／Round 2 資料，判斷暫停、加碼或修改。", "4h"),
            ("PRAC5", "完成國際廣告投放包", "交付一個平台的深度投放包、另一平台的轉譯版本、兩輪決策紀錄、預算與優化報告。", "6h"),
        ],
    },
    {
        "number": 6,
        "title": "創業企劃與能力整合・後段",
        "hours": "8h",
        "purpose": "把前五個 Part 的成果收斂成一致的主張、能力證據、提案與 30 天行動表。",
        "output": "整合企劃書、提案簡報與 30 天行動表",
        "units": [
            ("CH6-1", "整合受眾、問題與價值", "將前面各科成果收斂成一致的服務／品牌主張。", "2h"),
            ("CH6-2", "方案、商業模式與交付", "依選定應用情境整理服務內容、專案交付方式與基本條件。", "2h"),
            ("CH6-3", "作品呈現與 30 天行動方案", "把內容、社群、SEO、追蹤與廣告成果整理成可展示的能力證據。", "2h"),
            ("PRAC6", "完成整合企劃與提案", "依選定應用情境完成企劃書、簡報與 30 天行動表。", "2h"),
        ],
    },
]


UNIT_MAP = {unit[0]: (part, unit) for part in PARTS for unit in part["units"]}
ALL_UNITS = [unit[0] for part in PARTS for unit in part["units"]]

ASSET_BUNDLES = {
    "CH1-1": [
        ("工作表", "CH1-1"),
        ("四種情境案例卡", "CH1-1-情境案例卡"),
        ("阿凱參考完成品", "CH1-1-阿凱參考完成品"),
        ("判斷練習與答案", "CH1-1-判斷練習"),
    ],
    "CH1-2": [
        ("工作表", "CH1-2"),
        ("阿凱參考完成品", "CH1-2-阿凱參考完成品"),
        ("線索與分類練習", "CH1-2-線索與分類練習"),
    ],
    "CH1-3": [
        ("工作表", "CH1-3"),
        ("阿凱參考完成品", "CH1-3-阿凱參考完成品"),
        ("價值主張檢核練習", "CH1-3-價值主張檢核練習"),
    ],
    "PRAC1": [
        ("共同 Brief 工作表", "PRAC1"),
        ("四種情境參考", "PRAC1-四種情境參考"),
        ("五科交接檢核", "PRAC1-五科交接檢核"),
        ("整合檢核與答案", "PRAC1-整合檢核練習"),
    ],
    "CH2-1": [
        ("影像任務工作表", "CH2-1"),
        ("四項影像任務案例卡", "CH2-1-四項影像任務案例卡"),
        ("素材來源與 AI 紀錄表", "CH2-1-素材來源與AI紀錄表"),
    ],
    "CH2-2": [
        ("影像定位工作表", "CH2-2"),
        ("受眾與訊息案例卡", "CH2-2-受眾與訊息案例卡"),
    ],
    "CH2-3": [
        ("腳本與分鏡工作表", "CH2-3"),
        ("影像平台格式卡", "CH2-3-影像平台格式卡"),
    ],
    "CH2-4": [
        ("素材來源工作表", "CH2-4"),
        ("素材來源與使用條件案例", "CH2-4-素材來源與授權案例"),
    ],
    "CH2-5": [
        ("視覺資產組工作表", "CH2-5"),
        ("Affinity Windows 課前檢查表", "CH2-5-Affinity-Windows課前檢查表"),
        ("視覺資產輸出檢核表", "CH2-5-視覺資產輸出檢核表"),
    ],
    "CH2-6": [
        ("剪輯判斷工作表", "CH2-6"),
        ("剪輯參考與音訊檢查", "CH2-6-剪輯參考與音訊檢查"),
    ],
    "CH2-7": [
        ("本機剪輯與輸出工作表", "CH2-7"),
        ("OpenShot Windows 課前前測", "CH2-7-OpenShot-Windows課前前測"),
        ("短影音輸出檢核表", "CH2-7-短影音輸出檢核表"),
    ],
    "PRAC2": [
        ("可行銷內容組交付索引", "PRAC2"),
        ("README 參考完成品", "PRAC2-README參考完成品"),
        ("評量規準", "PRAC2-評量規準"),
    ],
    "CH3-1": [
        ("平台選擇工作表", "CH3-1"),
        ("平台角色卡", "CH3-1-平台角色卡"),
        ("社群格式卡", "CH3-1-社群格式卡"),
        ("LINE 承接情境卡", "CH3-1-LINE名單承接與回訪情境卡"),
    ],
    "CH3-2": [
        ("內容支柱工作表", "CH3-2"),
        ("內容支柱案例卡", "CH3-2-內容支柱案例卡"),
        ("社群表達規則卡", "CH3-2-社群表達規則卡"),
    ],
    "CH3-3": [
        ("跨平台改編工作表", "CH3-3"),
        ("三平台參考完成品", "CH3-3-三平台參考完成品"),
        ("跨平台檢查表", "CH3-3-跨平台檢查表"),
    ],
    "CH3-4": [
        ("月曆與流程工作表", "CH3-4"),
        ("發布前檢查表", "CH3-4-發布前檢查表"),
        ("兩週月曆參考完成品", "CH3-4-兩週月曆參考完成品"),
    ],
    "CH3-5": [
        ("互動風險工作表", "CH3-5"),
        ("互動情境卡", "CH3-5-互動情境卡"),
        ("正反例回應包", "CH3-5-正反例回應包"),
    ],
    "CH3-6": [
        ("成效紀錄工作表", "CH3-6"),
        ("合成資料與資料字典", "CH3-6-合成資料與資料字典"),
    ],
    "CH3-7": [
        ("LINE 延伸工作表", "CH3-7"),
        ("LINE 承接情境卡", "CH3-7-LINE情境卡"),
        ("訊息序列參考", "CH3-7-訊息序列參考"),
    ],
    "PRAC3": [
        ("社群方案交付索引", "PRAC3"),
        ("README 參考完成品", "PRAC3-README參考完成品"),
        ("評量規準", "PRAC3-評量規準"),
    ],
    "CH4-1": [
        ("搜尋意圖工作表", "CH4-1"),
        ("搜尋與 SEO 術語卡", "CH4-1-術語卡"),
        ("SERP 文字示例", "CH4-1-SERP示例"),
    ],
    "CH4-2": [
        ("關鍵字規劃工作表", "CH4-2"),
        ("查詢資料與分群參考", "CH4-2-查詢資料與分群參考"),
        ("關鍵字規劃參考完成品", "CH4-2-關鍵字規劃參考完成品"),
    ],
    "CH4-3": [
        ("LocalWP 頁面檢查表", "CH4-3"),
        ("LocalWP 課前與復原檢查", "CH4-3-LocalWP課前與復原檢查"),
        ("頁面基準檢查參考", "CH4-3-頁面基準檢查參考"),
    ],
    "CH4-4": [
        ("GA4 閱讀地圖", "CH4-4"),
        ("GA4 資料模型術語卡", "CH4-4-GA4資料模型術語卡"),
        ("GA4 閱讀地圖參考", "CH4-4-GA4閱讀地圖參考"),
    ],
    "CH4-5": [
        ("GA4 假設紀錄", "CH4-5"),
        ("GA4 合成觀察資料", "CH4-5-GA4合成觀察資料"),
        ("GA4 假設參考完成品", "CH4-5-GA4假設參考完成品"),
    ],
    "CH4-6": [
        ("GTM 事件佈建表", "CH4-6"),
        ("GTM 事件規格卡", "CH4-6-GTM事件規格卡"),
        ("GTM 復原檢查表", "CH4-6-GTM復原檢查表"),
    ],
    "CH4-7": [
        ("追蹤驗證紀錄", "CH4-7"),
        ("錯誤驗證案例卡", "CH4-7-錯誤驗證案例卡"),
        ("追蹤驗證參考完成品", "CH4-7-追蹤驗證參考完成品"),
    ],
    "PRAC4": [
        ("SEO 與追蹤決策包索引", "PRAC4"),
        ("Search Console 合成資料", "PRAC4-SearchConsole合成資料"),
        ("README 參考完成品", "PRAC4-README參考完成品"),
        ("評量規準", "PRAC4-評量規準"),
    ],
    "CH5-1": [
        ("市場與受眾工作表", "CH5-1"),
        ("市場卡比較示例", "CH5-1-市場卡比較示例"),
        ("服務能力限制卡", "CH5-1-服務能力限制卡"),
        ("市場選擇參考完成品", "CH5-1-市場選擇參考完成品"),
    ],
    "CH5-2": [
        ("渠道漏斗工作表", "CH5-2"),
        ("自然／付費渠道比較卡", "CH5-2-渠道比較卡"),
        ("合成渠道資料", "CH5-2-合成渠道資料"),
        ("預算框架參考完成品", "CH5-2-預算框架參考完成品"),
    ],
    "CH5-3": [
        ("Google Ads 投放包", "CH5-3"),
        ("Google Ads 文案參考完成品", "CH5-3-Google Ads 文案參考完成品"),
        ("政策與權限提醒卡", "CH5-3-政策與權限提醒卡"),
    ],
    "CH5-4": [
        ("Meta Ads 投放包", "CH5-4"),
        ("Meta Ads 素材矩陣參考", "CH5-4-Meta Ads 素材矩陣參考"),
    ],
    "CH5-5": [
        ("LINE Ads 比較工作表", "CH5-5"),
        ("LINE Ads 渠道比較參考", "CH5-5-LINE Ads 渠道比較參考"),
        ("訊息流程卡", "CH5-5-訊息流程卡"),
    ],
    "CH5-6": [
        ("預算模擬工作表", "CH5-6"),
        ("公式與單位說明卡", "CH5-6-公式與單位說明卡"),
        ("合成預算輸入", "CH5-6-合成預算輸入"),
        ("預算護欄參考", "CH5-6-預算護欄參考"),
    ],
    "CH5-7": [
        ("兩輪決策工作表", "CH5-7"),
        ("兩輪合成結果", "CH5-7-兩輪合成結果"),
        ("停止與決策卡", "CH5-7-停止與決策卡"),
    ],
    "PRAC5": [
        ("投放包交付索引", "PRAC5"),
        ("README 參考完成品", "PRAC5-README參考完成品"),
        ("評量規準", "PRAC5-評量規準"),
    ],
    "CH6-1": [
        ("整合價值主張表", "CH6-1"),
        ("四份產物摘要", "CH6-1-四份產物摘要"),
        ("整合價值參考完成品", "CH6-1-整合價值參考完成品"),
        ("同伴回饋表", "CH6-1-同伴回饋表"),
    ],
    "CH6-2": [
        ("方案與交付設計表", "CH6-2"),
        ("方案層級案例卡", "CH6-2-方案層級案例卡"),
        ("成本假設卡", "CH6-2-成本假設卡"),
        ("同伴審查表", "CH6-2-同伴審查表"),
        ("方案參考完成品", "CH6-2-方案參考完成品"),
    ],
    "CH6-3": [
        ("能力證據與 30 天行動表", "CH6-3"),
        ("作品呈現參考", "CH6-3-作品呈現參考"),
        ("30 天行動參考", "CH6-3-30天行動參考"),
        ("同伴回饋規則", "CH6-3-同伴回饋規則"),
        ("檔案索引規範", "CH6-3-檔案索引規範"),
    ],
    "PRAC6": [
        ("整合企劃與提案交付索引", "PRAC6"),
        ("README 參考完成品", "PRAC6-README參考完成品"),
        ("提案評量規準", "PRAC6-提案評量規準"),
    ],
}


def esc(value: str) -> str:
    return escape(value, quote=True)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def arrow(value: str) -> str:
    return f'<span aria-hidden="true">{value}</span>'


def meta_head(title: str, description: str, url: str) -> str:
    return f'''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{INSTITUTION}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="canonical" href="{esc(url)}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<style>:focus-visible {{ outline: 2px solid #2f3b32; outline-offset: 3px; }}</style>
<link rel="stylesheet" href="assets/course-shell.css">'''


def topbar(tag: str, logo_href: str = "index.html") -> str:
    return f'''<a href="#main" class="skip-link">跳至主要內容</a>
<header class="topbar">
  <a class="logo" href="{logo_href}">{INSTITUTION}</a>
  <div class="topbar-divider"></div>
  <span class="topbar-sub">{COURSE_TITLE}</span>
  <span class="spacer"></span>
  <span class="topbar-tag">{esc(tag)}</span>
</header>'''


def footer(platform: str = "Windows 教室；課程提供模板、示範資料與備援路徑") -> str:
    return f'''<footer class="footer" data-platform-version="{esc(platform)}" data-built-at="{TODAY}">
  <span class="footer-logo">{INSTITUTION}</span>
  <span>｜</span>
  <span>{COURSE_TITLE}</span>
</footer>'''


def part_url(number: int) -> str:
    return f"module{number}.html"


def unit_url(code: str) -> str:
    return f"{code}.html"


def template_code_from_href(href: str) -> str | None:
    match = re.fullmatch(r"assets/templates/([^/]+)\.md", href or "")
    return match.group(1) if match else None


def template_actions(code: str) -> str:
    kind = asset_kind_for_code(code)
    label = "下載可填寫工作版" if kind == "worksheet" else "下載 HTML 參考版"
    return (
        f'<span class="asset-actions">'
        f'<a class="asset-action" href="assets/templates/{esc(code)}.html" '
        f'target="_blank" rel="noopener">開啟閱讀版（新分頁）</a>'
        f'<a class="asset-action secondary" href="assets/templates/{esc(work_page_name(code, kind))}" '
        f'download="{esc(work_download_name(code, kind))}">{label}</a>'
        f'</span>'
    )


def asset_bundle_html(code: str) -> str:
    entries = []
    for label, asset_code in ASSET_BUNDLES.get(code, [("工作表", code)]):
        if not (TEMPLATE_DIR / f"{asset_code}.md").exists():
            continue
        entries.append(
            f'<div class="asset-item"><span class="asset-label">{esc(label)}</span>'
            f'{template_actions(asset_code)}</div>'
        )
    if not entries:
        return (
            '<p class="asset-missing">本單元的正式工作表尚未提供；請先使用頁面中的完整示例與文字備援，'
            '並把缺少的材料列入待補證據。</p>'
        )
    return (
        '<div class="asset-bundle">' + "".join(entries) + "</div>"
        '<p class="asset-note">先開啟閱讀版理解欄位；需要作答時下載「可填寫工作版」，'
        '只需閱讀的案例與參考資料請使用「HTML 參考版」。工作版可在頁面內填寫、保存草稿並下載完成版。</p>'
    )


def parent_lesson_for_asset(asset_code: str) -> str:
    """找出附件所屬單元，避免附件頁把返回連結指向不存在的同名講義。"""
    for lesson_code, entries in ASSET_BUNDLES.items():
        if any(code == asset_code for _, code in entries):
            return lesson_code
    return asset_code


def enhance_asset_links(main: BeautifulSoup, document: BeautifulSoup) -> None:
    """讓學員先進入閱讀版，並依資產類型提供工作版或參考版。"""
    for link in list(main.find_all("a", href=True)):
        href = link.get("href", "")
        code = template_code_from_href(href)
        if code:
            if link.find_parent(class_="asset-actions"):
                continue
            kind = asset_kind_for_code(code)
            label = "下載可填寫工作版" if kind == "worksheet" else "下載 HTML 參考版"
            wrapper = document.new_tag("span", attrs={"class": "asset-actions"})
            link["href"] = f"assets/templates/{code}.html"
            link["target"] = "_blank"
            link["rel"] = ["noopener"]
            link["class"] = ["asset-action"]
            link.clear()
            link.append("開啟閱讀版（新分頁）")
            download = document.new_tag(
                "a",
                href=f"assets/templates/{work_page_name(code, kind)}",
                download=work_download_name(code, kind),
                attrs={"class": "asset-action secondary"},
            )
            download.append(label)
            link.replace_with(wrapper)
            wrapper.append(link)
            wrapper.append(download)
        elif href.startswith("assets/") and href.lower().endswith(".csv"):
            link["download"] = Path(href).name
            classes = link.get("class", [])
            link["class"] = [*classes, "asset-download"]


def pandoc_html(source: Path) -> str:
    try:
        result = subprocess.run(
            ["pandoc", "--from=gfm", "--to=html5", "--wrap=none", str(source)],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return f'<pre class="asset-source-fallback">{esc(source.read_text(encoding="utf-8"))}</pre>'


def read_frontmatter(source: Path) -> dict[str, str]:
    """Read the small scalar metadata block used by this course's lessons."""
    lines = source.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("'\"")
    return metadata


def repair_literal_emphasis(fragment: BeautifulSoup) -> None:
    """Repair emphasis that Pandoc leaves literal around mixed Latin/CJK text."""
    allowed_parents = {"p", "li", "td", "th", "h3", "h4"}
    ignored_parents = {"code", "pre", "script", "style"}
    pattern = re.compile(r"\*\*(.+?)\*\*")
    for text_node in list(fragment.find_all(string=True)):
        parent = text_node.parent
        if not parent or parent.name in ignored_parents or parent.name not in allowed_parents:
            continue
        value = str(text_node)
        if not pattern.search(value):
            continue
        safe_value = escape(value, quote=False)
        markup = pattern.sub(
            lambda match: f"<strong>{match.group(1)}</strong>",
            safe_value,
        )
        replacement = BeautifulSoup(markup, "html.parser")
        for child in list(replacement.contents):
            text_node.insert_before(child)
        text_node.extract()


def learner_body_from_source(source: Path) -> tuple[str, str]:
    """Convert lesson Markdown into learner sections without production blocks."""
    fragment = BeautifulSoup(pandoc_html(source), "html.parser")
    repair_literal_emphasis(fragment)
    blocks: list[tuple[str, list[object]]] = []
    heading: str | None = None
    children: list[object] = []

    def flush() -> None:
        nonlocal heading, children
        if heading is not None:
            blocks.append((heading, children))
        heading = None
        children = []

    for node in list(fragment.contents):
        if isinstance(node, Comment):
            continue
        if getattr(node, "name", None) == "h2":
            flush()
            heading = clean_text(node.get_text(" ", strip=True))
            continue
        if heading is not None:
            children.append(node)
    flush()

    internal_markers = ("講師授課筆記", "試跑包需求清單")
    duplicate_flow_markers = ("商業情境案例", "動手練習題")
    learner_blocks = [
        (title, nodes)
        for title, nodes in blocks
        if not any(marker in title for marker in internal_markers)
        and not any(marker in title for marker in duplicate_flow_markers)
    ]

    # 教學流程原稿以一個 h2 包住多個 h3 階段；若整段只輸出成一個
    # lesson-section，學員頁會失去情境、概念、示範與操作的定位。把教學
    # 流程的 h3 展開成可掃讀的學習段落，保留原本的節點順序與內容。
    expanded_blocks: list[tuple[str, list[object]]] = []
    for title, nodes in learner_blocks:
        if not title.startswith("教學流程"):
            expanded_blocks.append((title, nodes))
            continue

        prelude: list[object] = []
        current_title: str | None = None
        current_nodes: list[object] = []
        for node in nodes:
            if getattr(node, "name", None) == "h3":
                if current_title is not None:
                    expanded_blocks.append((current_title, current_nodes))
                current_title = clean_text(node.get_text(" ", strip=True)).replace(
                    "教師示範 / Demo", "完整示範 / Demo"
                )
                current_nodes = prelude
                prelude = []
            elif current_title is None:
                prelude.append(node)
            else:
                current_nodes.append(node)
        if current_title is not None:
            expanded_blocks.append((current_title, current_nodes))
        elif prelude:
            expanded_blocks.append((title, prelude))

    rendered: list[str] = []
    visible_text: list[str] = []
    for index, (title, nodes) in enumerate(expanded_blocks, start=1):
        section = fragment.new_tag("section", attrs={"class": "lesson-section"})
        eyebrow = fragment.new_tag("div", attrs={"class": "section-eyebrow"})
        eyebrow.string = f"({index:02d})"
        section.append(eyebrow)
        heading_node = fragment.new_tag("h2", attrs={"class": "section-heading"})
        heading_node.string = title
        section.append(heading_node)
        visible_text.append(title)

        for node in nodes:
            if isinstance(node, Comment):
                continue
            name = getattr(node, "name", None)
            if name == "h3":
                if node.get_text(" ", strip=True) == "教師示範 / Demo":
                    node.string = "完整示範 / Demo"
                node["class"] = ["content-heading"]
            elif name == "h4":
                node["class"] = ["mini-heading"]
            elif name == "p":
                node["class"] = ["body-text"]
            elif name in {"ul", "ol"}:
                node["class"] = ["content-list"]
            elif name == "table":
                wrapper = fragment.new_tag("div", attrs={"class": "table-wrap"})
                node.wrap(wrapper)
                node = wrapper
            elif name == "pre":
                node["class"] = ["code-block"]
            elif name == "blockquote":
                blockquote_text = node.get_text(" ", strip=True)
                if "course_type =" in blockquote_text:
                    # course_type is production metadata, not learner instruction.
                    # Keep its artifact text available to the orientation metadata,
                    # but do not expose the metadata line in the handout.
                    visible_text.append(blockquote_text)
                    continue
                node["class"] = ["callout"]
            if getattr(node, "get_text", None):
                visible_text.append(node.get_text(" ", strip=True).replace("教師示範", "完整示範"))
            section.append(node)

        if rendered:
            rendered.append('<hr class="section-rule"/>')
        rendered.append(str(section))

    return "".join(rendered), clean_text(" ".join(visible_text))


def ensure_utf8_bom(path: Path) -> None:
    raw = path.read_bytes()
    if not raw.startswith(b"\xef\xbb\xbf"):
        path.write_bytes(b"\xef\xbb\xbf" + raw)


def build_fillable_asset_fragment(html: str, code: str) -> tuple[str, int]:
    """將 worksheet 的回答欄轉成可填寫欄位，保留原提示作為欄位說明。"""
    marker = '<article class="asset-document">'
    start = html.find(marker)
    end = html.find("</article>", start)
    if start < 0 or end < 0:
        return html, 0

    fragment = BeautifulSoup(html[start + len(marker) : end], "html.parser")
    field_count = 0
    safe_code = re.sub(r"[^A-Za-z0-9_-]+", "-", code)

    def add_textarea(cell: BeautifulSoup, field_id: str, guide: str, inline: bool = False) -> None:
        nonlocal field_count
        cell.clear()
        if guide:
            hint = fragment.new_tag("div", attrs={"class": "workbook-field-guide"})
            hint.string = guide
            cell.append(hint)
        textarea = fragment.new_tag(
            "textarea",
            attrs={
                "class": "workbook-field workbook-inline-field" if inline else "workbook-field",
                "data-workbook-field": "text",
                "data-field-id": field_id,
                "rows": "2" if inline else "4",
                "placeholder": "在此填寫你的回答",
            },
        )
        cell.append(textarea)
        field_count += 1

    for table_index, table in enumerate(fragment.find_all("table"), start=1):
        rows = table.find_all("tr")
        header_cells = rows[0].find_all(["td", "th"], recursive=False) if rows else []
        headers = [cell.get_text(" ", strip=True) for cell in header_cells]
        for row_index, row in enumerate(rows[1:], start=1):
            cells = row.find_all(["td", "th"], recursive=False)
            if len(cells) < 2:
                continue
            for column_index, cell in enumerate(cells[1:], start=2):
                if cell.find("input"):
                    continue
                header = headers[column_index - 1] if column_index - 1 < len(headers) else ""
                cell_text = cell.get_text(" ", strip=True)
                is_blank = not cell_text or "＿＿" in cell_text
                is_explicit_entry = (
                    any(marker in header for marker in EDITABLE_HEADER_MARKERS)
                    and not any(marker in header for marker in PROTECTED_HEADER_MARKERS)
                )
                if not is_blank and not is_explicit_entry:
                    continue
                guide = cell.get_text(" ", strip=True)
                cell["class"] = [*cell.get("class", []), "workbook-field-cell"]
                add_textarea(
                    cell,
                    f"{safe_code}-table-{table_index}-{row_index}-{column_index}",
                    guide,
                )

    for checkbox_index, checkbox in enumerate(fragment.find_all("input", attrs={"type": "checkbox"}), start=1):
        checkbox["data-workbook-field"] = "checkbox"
        checkbox["data-field-id"] = f"{safe_code}-checkbox-{checkbox_index}"
        field_count += 1

    for item_index, item in enumerate(fragment.find_all("li"), start=1):
        if item.find("input"):
            continue
        text = item.get_text(" ", strip=True)
        if not text.endswith(("：", ":")) and "＿＿" not in text:
            continue
        label = re.sub(r"[：:]\s*$", "", text).replace("＿＿", "")
        add_textarea(item, f"{safe_code}-list-{item_index}", label, inline=True)

    if field_count == 0:
        fallback = fragment.new_tag("section", attrs={"class": "workbook-fallback"})
        heading = fragment.new_tag("h2")
        heading.string = "我的補充與待驗證事項"
        fallback.append(heading)
        paragraph = fragment.new_tag("p")
        paragraph.string = "這份工作表沒有可由格式自動判定的欄位；請把閱讀後的判斷、限制與下一步寫在這裡。"
        fallback.append(paragraph)
        add_textarea(fallback, f"{safe_code}-fallback", "", inline=False)
        fragment.append(fallback)

    transformed = html[: start + len(marker)] + str(fragment) + html[end:]
    return transformed, field_count


def workbook_controls_html(code: str, kind: str) -> str:
    if kind == "reference":
        return (
            '<section class="workbook-panel" data-workbook-controls="reference">'
            '<h2>資產用途：HTML 參考版</h2>'
            '<p>這份資產用來閱讀案例、示例或規則。請回到單元講義，依學員工作版完成自己的產物。</p>'
            '</section>'
        )
    return (
        '<section class="workbook-panel" data-workbook-controls="worksheet">'
        '<h2>這份工作版要完成什麼</h2>'
        '<p>把答案填入有邊框的欄位；完成後先儲存草稿，再下載完成版 HTML，作為本單元的交付物。</p>'
        '<ol><li>閱讀欄位上方的提示，填入你的判斷或證據。</li>'
        '<li>勾選完成檢查，確認產物符合本單元要求。</li>'
        '<li>按「下載完成版 HTML」，再把完成版帶到講義指定的下一個使用位置。</li></ol>'
        '<div class="workbook-actions">'
        '<button class="asset-action" type="button" data-workbook-save>儲存草稿</button>'
        '<button class="asset-action secondary" type="button" data-workbook-export>下載完成版 HTML</button>'
        '<button class="asset-action secondary" type="button" data-workbook-clear>清除本機草稿</button>'
        '<span class="workbook-status" data-workbook-status>尚未載入草稿</span>'
        '</div></section>'
    )


def workbook_runtime() -> str:
    return r'''<script data-workbook-runtime>
(() => {
  const root = document.body;
  const fields = [...document.querySelectorAll('[data-workbook-field]')];
  const saveButton = document.querySelector('[data-workbook-save]');
  const exportButton = document.querySelector('[data-workbook-export]');
  const clearButton = document.querySelector('[data-workbook-clear]');
  const status = document.querySelector('[data-workbook-status]');
  if (!fields.length || !saveButton || !exportButton) return;

  const workbookId = root.dataset.workbookId;
  const storageKey = `course-workbook:${workbookId}`;
  const setStatus = (message) => { if (status) status.textContent = message; };
  const collect = () => Object.fromEntries(fields.map((field) => [
    field.dataset.fieldId,
    field.type === 'checkbox' ? field.checked : field.value,
  ]));

  const restore = () => {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
      fields.forEach((field) => {
        const value = saved[field.dataset.fieldId];
        if (value === undefined) return;
        if (field.type === 'checkbox') field.checked = Boolean(value);
        else field.value = value;
      });
      setStatus(Object.keys(saved).length ? '已載入本機草稿' : '尚未載入草稿');
    } catch (error) {
      setStatus('本機儲存不可用；仍可直接下載完成版 HTML');
    }
  };

  saveButton.addEventListener('click', () => {
    try {
      localStorage.setItem(storageKey, JSON.stringify(collect()));
      setStatus('草稿已儲存到這台電腦');
    } catch (error) {
      setStatus('本機儲存不可用；請直接下載完成版 HTML');
    }
  });

  clearButton?.addEventListener('click', () => {
    if (!window.confirm('確定清除這份工作版在本機保存的內容嗎？')) return;
    try { localStorage.removeItem(storageKey); } catch (error) { /* continue */ }
    fields.forEach((field) => {
      if (field.type === 'checkbox') field.checked = false;
      else field.value = '';
    });
    setStatus('本機草稿已清除');
  });

  exportButton.addEventListener('click', () => {
    const clone = document.documentElement.cloneNode(true);
    clone.querySelectorAll('[data-workbook-controls], [data-workbook-runtime]').forEach((node) => node.remove());
    clone.querySelectorAll('[data-workbook-field]').forEach((field) => {
      if (field.type === 'checkbox') {
        if (field.checked) field.setAttribute('checked', 'checked');
        else field.removeAttribute('checked');
        return;
      }
      const output = document.createElement('div');
      output.className = 'workbook-filled-value';
      output.textContent = field.value.trim() || '（未填寫）';
      field.replaceWith(output);
    });
    const html = '<!doctype html>\n' + clone.outerHTML;
    const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${workbookId}-完成版.html`;
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    // 某些瀏覽器會在 click 尚未交給下載佇列前就撤銷 Blob URL，造成
    // 狀態顯示成功但 Downloads 沒有檔案。延後清理並保留實際 DOM 節點。
    window.setTimeout(() => {
      URL.revokeObjectURL(link.href);
      link.remove();
    }, 1500);
    setStatus('完成版已下載');
  });

  restore();
})();
</script>'''


def standalone_work_html(html: str, code: str, kind: str) -> str:
    """建立可從 Downloads 直接開啟的參考版或可填寫工作版。"""
    inline_css = COURSE_SHELL_CSS.read_text(encoding="utf-8")
    html = html.replace(
        '<link rel="stylesheet" href="../course-shell.css">',
        f'<style data-course-shell="inline">{inline_css}{WORKBOOK_CSS if kind == "worksheet" else ""}</style>',
    )
    if COURSE_FAVICON.exists():
        svg = COURSE_FAVICON.read_text(encoding="utf-8")
        html = html.replace('href="../favicon.svg"', f'href="data:image/svg+xml,{quote(svg)}"')

    def absolute_href(match: re.Match[str]) -> str:
        href = match.group(1)
        if href.startswith("../../"):
            href = f"{COURSE_URL}/{href[6:]}"
        elif re.fullmatch(r"[^/#?]+\.html", href):
            href = f"{COURSE_URL}/assets/templates/{href}"
        return f'href="{href}"'

    html = re.sub(r'href="([^"]+)"', absolute_href, html)
    html = html.replace("模板閱讀版", asset_kind_label(kind))
    html = re.sub(
        r'<a class="asset-action secondary" href="[^"]+" download="[^"]+">'
        r'(?:下載可填寫工作版|下載 HTML 參考版)</a>',
        f'<span class="asset-action secondary" aria-current="page">目前為{asset_kind_label(kind)}</span>',
        html,
    )
    html = html.replace(
        "這是本單元的可讀模板。你可以先在本頁查看欄位，再下載 HTML 工作版自行編輯；原始講義仍保留在上一頁。",
        "這是可攜式 HTML 參考版，樣式已內嵌；可直接在 Windows 瀏覽器離線開啟，"
        "回到單元講義取得學員工作版。"
        if kind == "reference"
        else "這是可攜式可填寫工作版，樣式與操作工具已內嵌；可在 Windows 瀏覽器離線填寫、保存草稿並下載完成版。",
    )
    html = re.sub(
        r'<body class="asset-page"[^>]*>',
        f'<body class="asset-page workbook-page" data-workbook-kind="{kind}" data-workbook-id="{esc(code)}">',
        html,
        count=1,
    )
    if kind == "worksheet":
        html, _ = build_fillable_asset_fragment(html, code)
        html = html.replace(
            '</header>\n<main class="asset-main"',
            f'</header>\n{workbook_controls_html(code, kind)}\n<main class="asset-main"',
        )
        html = html.replace("</body>", f"{workbook_runtime()}\n</body>")
    else:
        html = html.replace(
            '</header>\n<main class="asset-main"',
            f'</header>\n{workbook_controls_html(code, kind)}\n<main class="asset-main"',
        )
    return html


def build_asset_pages(selected: set[str] | None = None) -> None:
    """產生閱讀版與可離線開啟的 HTML 工作版。"""
    for source in sorted(TEMPLATE_DIR.glob("*.md")):
        if selected is not None and source.stem not in selected:
            continue
        ensure_utf8_bom(source)
        code = source.stem
        kind = asset_kind_for_code(code)
        expected_work_page = work_page_name(code, kind)
        for legacy_name in (f"{code}-工作版.html", f"{code}-參考版.html"):
            legacy_path = TEMPLATE_DIR / legacy_name
            if legacy_name != expected_work_page and legacy_path.exists():
                legacy_path.unlink()
        title_line = next(
            (line[2:].strip() for line in source.read_text(encoding="utf-8-sig").splitlines() if line.startswith("# ")),
            f"{code} 模板",
        )
        body = pandoc_html(source)
        body_soup = BeautifulSoup(body, "html.parser")
        first_h1 = body_soup.find("h1")
        if first_h1:
            first_h1.decompose()
        body = learnerize_asset_language(str(body_soup).strip())
        canonical = f"{COURSE_URL}/assets/templates/{code}.html"
        parent_code = parent_lesson_for_asset(code)
        download_label = "下載可填寫工作版" if kind == "worksheet" else "下載 HTML 參考版"
        asset_description = "可直接閱讀或下載可填寫工作版" if kind == "worksheet" else "可直接閱讀或下載 HTML 參考版"
        asset_lead = (
            "先閱讀欄位與提示，再下載可填寫工作版完成自己的產物。"
            if kind == "worksheet"
            else "這份資產用來閱讀案例、示例或規則；需要作答時請回到單元下載可填寫工作版。"
        )
        html = f'''<!doctype html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title_line)}｜模板閱讀版｜{COURSE_TITLE}</title>
<meta name="description" content="{esc(title_line)}的學員模板閱讀版，{asset_description}。">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{INSTITUTION}">
<meta property="og:title" content="{esc(title_line)}｜模板閱讀版">
<meta property="og:description" content="{esc(title_line)}的學員模板閱讀版，{asset_description}。">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title_line)}｜模板閱讀版">
<meta name="twitter:description" content="{esc(title_line)}的學員模板閱讀版，{asset_description}。">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="canonical" href="{esc(canonical)}">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<style>:focus-visible {{ outline: 2px solid #2f3b32; outline-offset: 3px; }}</style>
<link rel="stylesheet" href="../course-shell.css">
</head>
<body class="asset-page" data-asset-kind="{kind}" data-asset-id="{esc(code)}">
{topbar(f"{code} · 模板閱讀版", "../../index.html")}
<header class="asset-hero">
  <a class="breadcrumb" href="../../{parent_code}.html"><span aria-hidden="true">←</span> 返回 {parent_code} 講義</a>
  <div class="hero-eyebrow">學員資產 · LEARNER ASSET</div>
  <h1 class="asset-title">{esc(title_line)}</h1>
  <p class="asset-lead">{asset_lead}</p>
  <div class="asset-toolbar">
    <a class="asset-action" href="../../{parent_code}.html">返回 {parent_code} 講義</a>
    <a class="asset-action secondary" href="{work_page_name(code, kind)}" download="{esc(work_download_name(code, kind))}">{download_label}</a>
  </div>
</header>
<main class="asset-main" id="main">
  <article class="asset-document">
{body}
  </article>
</main>
{footer("學員模板閱讀版")}
</body>
        </html>
'''
        source.with_suffix(".html").write_text(html, encoding="utf-8")
        work_path = TEMPLATE_DIR / work_page_name(code, kind)
        work_path.write_text(standalone_work_html(html, code, kind), encoding="utf-8")

    for dataset in sorted(DATASET_DIR.glob("*.csv")):
        ensure_utf8_bom(dataset)


def render_index() -> str:
    parts_html = []
    for part in PARTS:
        parts_html.append(f'''<a class="part-card" href="{part_url(part["number"])}">
  <span class="part-label">PART {part["number"]} · {part["hours"]}</span>
  <h2>{esc(part["title"])}</h2>
  <p>{esc(part["purpose"])}</p>
  <span class="part-output"><strong>本 Part 主要產物：</strong>{esc(part["output"])}</span>
</a>''')
    description = "從共同 Brief 出發，串起內容、社群、SEO／追蹤、廣告與整合提案。"
    return f'''<!doctype html>
<html lang="zh-TW">
<head>
{meta_head(f"{COURSE_TITLE}｜{INSTITUTION}", description, f"{COURSE_URL}/index.html")}
</head>
<body class="course-page">
{topbar("126h · 整合課程", "../../index.html")}
<header class="course-hero">
  <div class="hero-eyebrow">{INSTITUTION} · INTEGRATED PROGRAM</div>
  <h1 class="hero-title">{COURSE_TITLE}</h1>
  <p class="hero-desc">把專長或點子轉成可被看見、可被推廣、可被驗證的方案。你會沿著同一條能力主線，依自己的應用情境完成可展示的工作成果。</p>
  <hr class="hero-rule">
</header>
<main class="course-main" id="main">
  <section class="intro-panel">
    <h2>你會沿著一條能力主線前進</h2>
    <p>問題與需求 → 服務／品牌方向 → 影像與平面內容 → 社群經營 → SEO／GA4／GTM → 國際廣告 → 整合企劃與提案。求職作品集、企業專案、自由工作與個人品牌都可以使用這條主線。</p>
  </section>
  <div class="capability-chain"><strong>讀法：</strong>先從 Part 1 建立共同主題，再依序使用前一個 Part 的產物。每個 Part 都有自己的導覽頁與完成物，單元頁會說明起始材料、操作與驗證。</div>
  <div class="section-label">六個 Part</div>
  <div class="part-grid">{''.join(parts_html)}</div>
  <nav class="module-nav"><a class="nav-btn primary" href="module1.html">從 Part 1 開始 {arrow('→')}</a><a class="nav-btn" href="../../index.html">{arrow('←')} 所有課程</a></nav>
</main>
{footer()}
</body>
</html>
'''


def render_module(part: dict) -> str:
    n = part["number"]
    previous = f'<a class="nav-btn" href="module{n - 1}.html">{arrow("←")} Part {n - 1}</a>' if n > 1 else f'<a class="nav-btn" href="index.html">{arrow("←")} 課程總覽</a>'
    following = f'<a class="nav-btn primary" href="module{n + 1}.html">Part {n + 1} {arrow("→")}</a>' if n < len(PARTS) else f'<a class="nav-btn primary" href="index.html">回課程總覽 {arrow("→")}</a>'
    units_html = []
    for code, title, purpose, hours in part["units"]:
        kind = "prac" if code.startswith("PRAC") else ""
        badge = " · 整合實作" if kind else ""
        units_html.append(f'''<a class="unit-link {kind}" href="{unit_url(code)}">
  <span class="unit-code">{code}{badge}</span>
  <span><span class="unit-title">{esc(title)}</span><span class="unit-purpose">{esc(purpose)}</span></span>
  <span class="unit-hours">{hours} <span class="unit-arrow" aria-hidden="true">→</span></span>
</a>''')
    description = part["purpose"]
    return f'''<!doctype html>
<html lang="zh-TW">
<head>
{meta_head(f"Part {n}｜{part["title"]}", description, f"{COURSE_URL}/module{n}.html")}
</head>
<body class="module-page">
{topbar(f"PART {n} · {part["hours"]}")}
<header class="module-hero">
  <a class="breadcrumb" href="index.html">{arrow('←')} 課程總覽</a>
  <div class="hero-eyebrow">PART {n} · {part["hours"]}</div>
  <h1 class="module-title">{esc(part["title"])}</h1>
  <p class="module-lead">{esc(description)}</p>
</header>
<main class="module-main" id="main">
  <section class="module-summary">
    <div class="summary-item"><strong>{part["hours"]}</strong><span>本 Part 時數</span></div>
    <div class="summary-item"><strong>{len(part["units"])} 個單元</strong><span>包含 CH 與整合實作</span></div>
    <div class="summary-item"><strong>完成一組成果</strong><span>{esc(part["output"])}</span></div>
  </section>
  <section class="orientation-panel">
    <h2>進入本 Part 前，你要知道的事</h2>
    <p>本頁列出學習順序。每個單元會先說明任務與起始材料，再進入概念、示範、練習與驗證。完成本 Part 後，把這組產物交給下一個 Part 使用。</p>
  </section>
  <div class="section-label">單元順序</div>
  <div class="unit-list">{''.join(units_html)}</div>
  <nav class="module-nav">{previous}{following}</nav>
</main>
{footer()}
</body>
</html>
'''


def extract_artifact(text: str) -> str:
    patterns = [
        r"(?:本節完成物|完成物|交付物)\s*[：:]\s*([^。\n]{2,180})",
        r"(?:留下|取得)\s+([`「][^`」]{2,120}[`」])",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            value = clean_text(match.group(1)).strip("。；; ")
            if value and "依本頁" not in value:
                return value
    return "依本頁完成驗證段落保存版本化產物"


def extract_platform(soup: BeautifulSoup) -> str:
    meta = soup.find(attrs={"data-platform-version": True})
    if meta:
        return meta.get("data-platform-version", "")
    return "Windows 教室；課程提供模板、示範資料與備援路徑"


def learnerize_asset_language(html: str) -> str:
    """把製作端資產狀態改寫成學員可採取的行動提示。"""
    replacements = [
        ("Markdown 下載檔只作為文字備份，不是唯一閱讀入口。", "HTML 工作版可直接複製或另存，不需要處理製作端原始檔。"),
        ("Markdown 原始檔", "製作端原始檔"),
        ("Markdown", "HTML 工作版"),
        (".md", ".html"),
        ("課前確認：正式案例卡與上游參考品尚未全部可尋址。", "使用備援：先使用本頁模板與示例建立本機版本，正式案例取得後再替換。"),
        ("課前確認：教師社群資料包與資料字典尚未全部可尋址。", "使用備援：先使用本頁模板與去識別示例，正式資料取得後再替換。"),
        ("課前確認：LINE 情境卡與參考序列尚未全部可尋址。", "使用備援：先使用本頁模板、虛構測試狀態與紙面序列，不需要 LINE 帳號或真實名單。"),
        ("課前確認：", "使用前先確認："),
        ("依課前檢查", "依本頁的資產與備援說明"),
        ("課前需提供", "若課堂尚未提供"),
        ("教師需補交", "若尚未取得"),
        ("教師仍需提供去識別情境，否則用本頁案例做角色演練並標記模擬。", "若課堂尚未提供去識別情境，先用本頁案例做角色演練並標記模擬。"),
        ("教師仍需提供三平台改編包、發布流程示例與 LINE 情境列，否則使用本頁示例並標記待補。", "若課堂尚未提供三平台改編包、發布流程示例與 LINE 情境列，先使用本頁示例並標記待補。"),
        ("仍需課前由課堂提供", "若課堂尚未提供"),
        ("需要教師課前提供", "若課堂尚未提供"),
        ("尚未全部可尋址", "目前未納入本頁資產"),
        ("否則保留模擬與待補狀態", "先以模擬版本完成，並標記仍待補的部分"),
        ("待課前確認", "待補證據"),
    ]
    for source, target in replacements:
        html = html.replace(source, target)
    return html


def extract_internal_notes(path: Path) -> list[str]:
    if not path.exists():
        return []
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    notes = []
    for section in soup.find_all("section"):
        heading = section.find("h2")
        if heading and "講師授課筆記" in heading.get_text(" ", strip=True):
            notes.append(f"## {path.stem}\n\n{clean_text(section.get_text(' ', strip=True))}\n")
    return notes


def render_lesson(code: str) -> str:
    """Render one learner page from its stable Markdown lesson source."""
    source = SOURCE_DIR / f"{code}.md"
    if not source.exists():
        raise RuntimeError(f"missing lesson source: {source}")
    metadata = read_frontmatter(source)
    part, unit = UNIT_MAP[code]
    title = metadata.get("title", unit[1])
    tagline = metadata.get("learning_objective", unit[2])
    description = tagline
    platform = metadata.get("platform_version", "Windows 教室；課程提供模板、示範資料與備援路徑")
    content_html, body_text = learner_body_from_source(source)
    artifact = extract_artifact(body_text)
    artifact = artifact.replace(".md", ".html")
    asset_html = asset_bundle_html(code)

    idx = ALL_UNITS.index(code)
    previous_code = ALL_UNITS[idx - 1] if idx > 0 else None
    next_code = ALL_UNITS[idx + 1] if idx + 1 < len(ALL_UNITS) else None
    previous_href = unit_url(previous_code) if previous_code else part_url(part["number"])
    previous_label = previous_code or f"Part {part["number"]}"
    next_href = unit_url(next_code) if next_code else (part_url(part["number"] + 1) if part["number"] < len(PARTS) else "index.html")
    next_label = next_code or (f"Part {part["number"] + 1}" if part["number"] < len(PARTS) else "課程總覽")
    outcomes_html = f'<div class="outcome-item">{esc(unit[2])}</div>'
    content_html = learnerize_asset_language(content_html).strip()
    part_tag = f"PART {part["number"]} · {part["title"]}"
    unit_title = f"({code}) {title}｜{COURSE_TITLE}"
    url = f"{COURSE_URL}/{code}.html"
    return f'''<!doctype html>
<html lang="zh-TW">
<head>
{meta_head(unit_title, description, url)}
</head>
<body class="lesson-page">
{topbar(part_tag)}
<header class="page-hero">
  <a class="breadcrumb" href="{part_url(part["number"])}">{arrow('←')} 返回 Part {part["number"]}</a>
  <div class="hero-eyebrow">{code} · {unit[3]}</div>
  <h1 class="lesson-title">{esc(title)}</h1>
  <p class="lesson-tagline">{esc(tagline or unit[2])}</p>
  <div class="outcomes"><div class="outcomes-label">本單元完成後</div>{outcomes_html}</div>
</header>
<main class="lesson-main" id="main">
  <section class="lesson-orientation">
    <div class="section-eyebrow">學習導覽</div>
    <h2>這一頁要完成什麼</h2>
    <p class="orientation-lead">{esc(unit[2])} 完成後，你會留下可交接的成果，並把它交給 {esc(next_label)} 使用。</p>
    <div class="orientation-grid">
      <div class="orientation-item"><strong>起始材料</strong>{asset_html}</div>
      <div class="orientation-item"><strong>完成物</strong><span>{esc(artifact)}</span></div>
      <div class="orientation-item"><strong>閱讀順序</strong><span>情境與任務 → 概念／案例 → 操作或練習 → 驗證 → 下一個使用位置。</span></div>
    </div>
  </section>
{content_html}
  <nav class="nav-footer">
    <a class="nav-btn" href="{previous_href}">{arrow('←')} {esc(previous_label)}</a>
    <a class="nav-btn" href="{part_url(part["number"])}">回 Part {part["number"]}</a>
    <a class="nav-btn primary" href="{next_href}">{esc(next_label)} {arrow('→')}</a>
  </nav>
</main>
{footer(platform)}
</body>
</html>
'''


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--unit",
        action="append",
        dest="units",
        help="只重建指定單元；可重複提供，例如 --unit CH5-3 --unit CH6-2",
    )
    parser.add_argument(
        "--asset",
        action="append",
        dest="assets",
        help="只重建指定模板閱讀版；可重複提供，例如 --asset CH1-1 --asset PRAC1",
    )
    args = parser.parse_args()
    normalize_static_reference_pages()
    if args.assets:
        available = {path.stem for path in TEMPLATE_DIR.glob("*.md")}
        unknown_assets = [code for code in args.assets if code not in available]
        if unknown_assets:
            raise SystemExit(f"unknown asset: {', '.join(unknown_assets)}")
        build_asset_pages(set(args.assets))
        print(f"rebuilt {len(set(args.assets))} learner asset pages")
        return
    selected_units = args.units or ALL_UNITS
    unknown = [code for code in selected_units if code not in UNIT_MAP]
    if unknown:
        raise SystemExit(f"unknown unit: {', '.join(unknown)}")

    if args.units:
        for code in selected_units:
            (COURSE_DIR / f"{code}.html").write_text(render_lesson(code), encoding="utf-8")
        print(f"rebuilt {len(selected_units)} learner pages from Markdown sources")
        return

    internal_notes: list[str] = []
    for code in ALL_UNITS:
        internal_notes.extend(extract_internal_notes(BACKUP_HTML_DIR / f"{code}.html"))
    if not internal_notes:
        for code in ALL_UNITS:
            internal_notes.extend(extract_internal_notes(COURSE_DIR / f"{code}.html"))
    (COURSE_DIR / "index.html").write_text(render_index(), encoding="utf-8")
    for part in PARTS:
        (COURSE_DIR / f"module{part['number']}.html").write_text(render_module(part), encoding="utf-8")
    for code in ALL_UNITS:
        (COURSE_DIR / f"{code}.html").write_text(render_lesson(code), encoding="utf-8")
    build_asset_pages()

    internal_dir = REPAIR_DIR / "internal-notes"
    internal_dir.mkdir(parents=True, exist_ok=True)
    (internal_dir / "EXTRACTED-TEACHER-NOTES.md").write_text(
        "# Extracted teacher notes\n\n" + "\n".join(internal_notes), encoding="utf-8"
    )
    print(f"rebuilt {len(PARTS) + len(ALL_UNITS) + 1} learner pages")
    print(f"archived {len(internal_notes)} internal sections")


if __name__ == "__main__":
    main()
