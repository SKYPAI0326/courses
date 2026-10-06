"""Apply exact, source-backed corrections to stale course guidance."""
from html.parser import HTMLParser
from pathlib import Path
import html
import json
import re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / "_repair/2026-10-06/re-review"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
CANVAS = "https://support.google.com/gemini/answer/16047321?hl=zh-TW"
BUILD = "https://ai.google.dev/gemini-api/docs/aistudio-build-mode"
DEPLOY = "https://ai.google.dev/gemini-api/docs/aistudio-deploying"
BILLING = "https://ai.google.dev/gemini-api/docs/billing/"
LIMITS = "https://ai.google.dev/gemini-api/docs/rate-limits"
PRICING = "https://ai.google.dev/gemini-api/docs/pricing"
RAIL_TRIAL = "https://docs.railway.com/pricing/free-trial"
RAIL_PLANS = "https://docs.railway.com/pricing/plans"
GH_PAGES = "https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site"

class Boundary(HTMLParser):
    def __init__(self, source, tag):
        super().__init__(convert_charrefs=False)
        self.source, self.tag, self.depth, self.end = source, tag, 0, None
        self.lines = [0]
        for line in source.splitlines(keepends=True):
            self.lines.append(self.lines[-1] + len(line))
    def handle_starttag(self, tag, attrs):
        if tag == self.tag: self.depth += 1
    def handle_endtag(self, tag):
        if tag == self.tag:
            self.depth -= 1
            if self.depth == 0 and self.end is None:
                line, col = self.getpos()
                i = self.lines[line - 1] + col
                self.end = self.source.index(">", i) + 1

def node_span(raw, node):
    start = sum(len(x) for x in raw.splitlines(keepends=True)[:node.sourceline - 1]) + node.sourcepos
    tail = raw[start:]
    if node.name in VOID: return start, start + tail.index(">") + 1
    parser = Boundary(tail, node.name)
    parser.feed(tail)
    assert parser.end is not None, node.name
    return start, start + parser.end

def norm(value): return " ".join(value.split())
def text_of(fragment): return norm(BeautifulSoup(fragment, "html.parser").get_text(" ", strip=True))
def match_norm(value):
    value = norm(value)
    value = re.sub(r"\s+([，。！？；：、）】」』])", r"\1", value)
    value = re.sub(r"([，。！？；：、])\s+", r"\1", value)
    return re.sub(r"\s+", "", value)

pending = {}
audit = []

def load(path):
    path = str(path)
    if path not in pending: pending[path] = (ROOT / path).read_text()
    return pending[path]

def set_inner(path, selector, expected_text, new_inner, source, reason, body=True):
    raw = load(path)
    soup = BeautifulSoup(raw, "html.parser")
    nodes = [n for n in soup.select(selector) if match_norm(n.get_text(" ", strip=True)) == match_norm(expected_text)]
    assert len(nodes) == 1, (path, selector, expected_text, len(nodes))
    node = nodes[0]
    old_text = norm(node.get_text(" ", strip=True))
    start, end = node_span(raw, node)
    open_end = raw.index(">", start) + 1
    close_start = raw.rfind("</", open_end, end)
    assert close_start >= open_end, (path, selector)
    updated = raw[:open_end] + new_inner + raw[close_start:]
    pending[path] = updated
    new_text = text_of(new_inner)
    audit.append({"path": path, "scope": "legacy" if body else "page", "before_text": old_text,
                  "after_text": new_text, "source": source, "reason": reason})

def set_meta(path, selector, old_value, new_value, source, reason):
    raw = load(path)
    soup = BeautifulSoup(raw, "html.parser")
    nodes = [n for n in soup.select(selector) if n.get("content") == old_value]
    assert len(nodes) == 1, (path, selector, len(nodes))
    start, end = node_span(raw, nodes[0])
    old = raw[start:end]
    updated, count = re.subn(r'content="[^"]*"', 'content="' + html.escape(new_value, quote=True) + '"', old, count=1)
    assert count == 1
    pending[path] = raw[:start] + updated + raw[end:]
    audit.append({"path": path, "scope": "page", "before_text": old_value, "after_text": new_value,
                  "source": source, "reason": reason})

# Keep every original Canvas exercise, but replace the obsolete right-corner toggle with
# the current official Gemini Apps route: Add files -> Canvas.
canvas_pages = []
for p in sorted(ROOT.glob("part*/*.html")):
    path = p.relative_to(ROOT).as_posix()
    raw = load(path)
    if "打開 Gemini，切換到「Canvas」模式" not in raw: continue
    canvas_pages.append(path)
    set_inner(path, "#legacy-reference .step-title", "打開 Gemini，切換到「Canvas」模式",
              "建立 Gemini Apps Canvas 專案", CANVAS, "更新已改變的 Canvas 入口步驟")
    set_inner(path, "#legacy-reference .step-desc",
              "進入 gemini.google.com，點右上角切換到 Canvas 模式，這樣 AI 生成的 HTML 會直接可以預覽。",
              '登入 <strong>gemini.google.com</strong>，在輸入框下方選「新增檔案」→「Canvas」，輸入提示詞並送出；看到 Canvas 預覽才繼續。按鈕位置依目前介面為準。<a href="' + CANVAS + '" target="_blank" rel="noopener">Google 官方 Canvas 操作說明</a>。',
              CANVAS, "更新已改變的 Canvas 入口步驟")

set_inner("part1/CH1-1.html", "#legacy-reference .concept-title", "免費額度充足",
          "先查可用模型與費用", BILLING, "移除免費用量足以完成課程的無依據保證")
set_inner("part1/CH1-1.html", "#legacy-reference .concept-desc",
          "一般使用量在免費方案內完全夠用，不需要先花任何錢。",
          'Google AI Studio 免費層僅開放部分模型，實際模型與用量限制依帳號方案和官方頁面更新。首次操作前查看<a href="' + PRICING + '" target="_blank" rel="noopener">官方定價</a>和<a href="' + BILLING + '" target="_blank" rel="noopener">帳務說明</a>及帳號的 Usage／Billing 畫面；本課不保證免費額度足以完成所有生成。',
          BILLING, "免費模型與用量依方案和模型而異")

set_inner("part6/CH6-1.html", "#legacy-reference .callout-body",
          "用量算在誰頭上：這代表 app 每一次呼叫 Gemini，用的都是你自己的免費額度（免費層有每分鐘／每日次數上限）。適合做內部小工具，不適合預期會有大量使用者同時打開的公開產品。",
          '<strong>用量與費用：</strong>分享 app 時，API 呼叫會計入你的使用額度；實際限額依模型與方案而異，使用付費模型可能產生費用。發布或分享前先查看目前使用量與費用資訊，以及官方<a href="' + LIMITS + '" target="_blank" rel="noopener">使用限制</a>和<a href="' + BILLING + '" target="_blank" rel="noopener">帳務說明</a>。',
          BUILD, "改正免費額度與每分鐘／每日限制的概括說法")

# CH6-2 metadata and visible technical reference.
old_meta = "做好的 AI app 不必寄檔案。AI Studio 內建兩種給別人用的方式：Share 快速分享連結、Publish 拿到公開網址，這一節帶你走完全程免費的路線。"
new_meta = "做好的 AI app 可透過 AI Studio Build 分享或部署；帳號資格、模型使用限制與費用依當前方案而異，操作前請查看官方說明。"
for sel in ['meta[name="description"]', 'meta[property="og:description"]', 'meta[name="twitter:description"]']:
    set_meta("part6/CH6-2.html", sel, old_meta, new_meta, DEPLOY, "移除全程免費的保證")
set_inner("part6/CH6-2.html", ".lesson-tagline",
          "做好的 AI 工具不需要打包成檔案寄給同事。AI Studio 在做 app 的同一個介面裡，內建兩種「給別人用」的管道——一種是分享連結給特定人，一種是拿到一個公開網址。這一節帶你把兩種都走一次，並看清楚免費與付費的分界在哪裡。",
          "AI Studio Build 可分享 app 或部署公開網址；本節示範兩種情境，帳號資格、API 額度與費用依當前方案確認。", DEPLOY, "移除全程免費的保證", body=False)
set_inner("part6/CH6-2.html", "#legacy-reference p.body-text",
          "本質上，Share 出去的連結還是在你的 AI Studio 專案底下執行——對方是在你做的 app 介面上操作，實際呼叫 Gemini 的額度算在你頭上。",
          '分享 app 後，使用者可在 app 介面操作；官方說明指出，API 呼叫會計入你的使用額度，使用付費模型可能產生費用。獲分享的使用者也可能查看程式碼並 fork，因此不要放入機密規則或未審核資料。操作前查看<a href="' + BUILD + '" target="_blank" rel="noopener">Build 分享說明</a>。',
          BUILD, "補上分享者用量與獲分享者可見程式碼的說明")
set_inner("part6/CH6-2.html", "#legacy-reference p.body-text",
          "如果你要的是一個「不需要邀請、任何人打進網址都能用」的正式服務，要走 Publish。面板上會先說明：「Chat history & code will stay private」「Your app will be accessible via a public URL」。",
          'Publish 部署後會提供公開 app 網址。原始教材引用的「Chat history & code will stay private」是舊版介面文字，不宜當作所有目前帳號與發布情境的隱私保證：現行<a href="' + DEPLOY + '" target="_blank" rel="noopener">部署文件</a>說明公開網址與資格，但未交代專案原始碼及對話紀錄的可見範圍。發布前查看目前確認畫面並移除個資與機密；AI Studio Share 的權限另見<a href="' + BUILD + '" target="_blank" rel="noopener">Build 分享說明</a>。',
          DEPLOY, "區分舊版 Publish 隱私提示、現行公開部署與 Share 程式碼可見權限")
set_inner("part6/CH6-2.html", "#legacy-reference .step-desc",
          "會看到私隱聲明：對話紀錄與程式碼保持私密，只有 app 本身透過公開網址開放。",
          '公開網址提供 app 存取入口；不要單憑舊版提示推定對話紀錄或原始碼在所有情境都私密。先核對當前確認畫面和<a href="' + DEPLOY + '" target="_blank" rel="noopener">官方部署說明</a>，移除個資與機密後再發布。',
          DEPLOY, "將絕對隱私承諾改成發布前的可執行檢查")
set_inner("part6/CH6-2.html", "#legacy-reference .step-desc",
          "沒有 GCP 帳單紀錄的帳號會看到免費的 Starter Tier 選項；已經有 GCP 帳單或付費 Workspace 的帳號會直接進入付費流程（下一節細講）。",
          'Starter Tier 最多可部署 2 個 app，但已有或曾有 Google Cloud Billing 的帳號，以及部分 Google Workspace、Workspace for Education 或 Google for Nonprofits 帳號可能不符合資格；標準部署需要連結 Google Cloud 專案並啟用帳單。依目前發布畫面與<a href="' + DEPLOY + '" target="_blank" rel="noopener">官方資格說明</a>確認。',
          DEPLOY, "更新 Starter Tier 資格條件")
set_inner("part6/CH6-2.html", "#legacy-reference .callout-body",
          "Starter Tier 細節：免費發布最多 2 個 app、不需要信用卡、不用自己建 GCP 專案、部署在單一 Cloud Run 區域。這是目前最簡單的免費上架路線。",
          '<strong>Starter Tier 細節：</strong>符合資格的帳號可在未建立 Google Cloud 專案或帳單時發布最多 2 個 app，並部署在單一 Cloud Run 區域。資格依帳號而異；部署資格不代表 app 的 API 使用必然免費。請依<a href="' + DEPLOY + '" target="_blank" rel="noopener">官方部署與資格說明</a>及當下畫面確認。',
          DEPLOY, "移除未經官方文件支持的免信用卡與全免費承諾")
set_inner("part6/CH6-2.html", "#legacy-reference .section-heading", "例外狀況：為什麼你可能看不到免費層",
          "例外狀況：為什麼你可能看不到 Starter Tier", DEPLOY, "使用官方方案名稱並避免預設免費資格")
set_inner("part6/CH6-2.html", "#legacy-reference p.body-text",
          "Starter Tier 不是每個帳號都看得到。如果你的 Google 帳號已經有 GCP 帳單紀錄，或用的是付費版 Google Workspace 帳號，Publish 流程不會出現免費選項，會直接進入「確認專案與帳單」的三步驟付費流程，選一個 GCP 專案，之後照 Cloud Run 用量計價。公司配發的帳號很常見這種情況，因為公司帳號通常本來就掛在有帳單的 GCP 組織底下。",
          'Starter Tier 不是每個帳號都能使用。已有或曾有 Google Cloud Billing 的帳號，以及關聯免費或付費 Google Workspace、Workspace for Education、Google for Nonprofits 訂閱的企業帳號可能不符合資格。若不符合，標準部署需要選擇 Google Cloud 專案並啟用帳單；最終流程依帳號畫面與<a href="' + DEPLOY + '" target="_blank" rel="noopener">官方資格條件</a>為準。',
          DEPLOY, "更新不符合 Starter Tier 的帳號條件")
set_inner("part6/CH6-2.html", "#legacy-reference .callout-body",
          "對策：如果你想確保走免費路線，優先用個人 Google 帳號測試 Publish。如果公司帳號真的只能走付費流程，又不想產生費用，可以改用 6.3 教的 GitHub + Railway 路線，一樣能拿到公開網址。",
          '<strong>對策：</strong>個人帳號也不保證符合 Starter Tier 資格；先確認當前發布選項及 API 使用費用。若標準部署需要帳單，先評估預算，不要把 Railway 當成免 API 費用的替代方案；Railway 另有自己的方案與資源費用。可參考<a href="' + DEPLOY + '" target="_blank" rel="noopener">AI Studio 部署說明</a>與<a href="https://docs.railway.com/pricing/plans" target="_blank" rel="noopener">Railway 方案</a>。',
          DEPLOY, "避免把外部託管誤當成免成本路線")
set_inner("part6/CH6-2.html", "#legacy-reference .section-heading", "使用限制：免費額度的真相",
          "使用限制與費用：分享前要查什麼", BUILD, "更新段落主題以涵蓋模型方案與費用")
set_inner("part6/CH6-2.html", "#legacy-reference p.body-text",
          "不管是 Share 出去給同事，還是 Publish 成公開網址，app 呼叫 Gemini 用的都是你自己帳號的免費額度——這個額度是「每分鐘／每日次數」的上限，被所有打開這個網址的人共用，不是每人各自一份。",
          'Share 或 Publish 後，app 的 Gemini API 呼叫會計入建立者的使用額度；限額依模型、專案與使用方案而異，付費模型可能產生費用。不要預設所有模型都有相同的每分鐘或每日上限；分享前查看 AI Studio 的 Usage／Billing，以及官方<a href="' + LIMITS + '" target="_blank" rel="noopener">各模型使用限制</a>與<a href="' + BILLING + '" target="_blank" rel="noopener">帳務說明</a>。',
          BUILD, "改正全都屬免費配額且限額固定的說法")
set_inner("part6/CH6-2.html", "#legacy-reference .deploy-con", "所有使用者共用你的免費額度上限",
          "API 呼叫計入建立者的使用額度；付費模型可能收費", BUILD, "修正配額與成本卡片")
set_inner("part6/CH6-2.html", "#legacy-reference .callout-body",
          "資安提醒：公開的 URL 意味著任何人都能打開來用，也就是任何人都能用掉你的免費額度。內部工具（給同事、給部門用）建議走 Share + email 邀請，把使用範圍限制在你認識的人；只有真的需要對外公開服務時，才考慮 Publish。下一節看另一條路線——把程式碼放上 GitHub，透過 Railway 部署，作為 AI Studio 之外的備援選項。",
          '<strong>分享與成本提醒：</strong>公開網址可能讓更多人使用 app；API 呼叫計入建立者的使用額度，付費模型可能產生費用。AI Studio 分享的 app 使用者也可能查看程式碼並 fork。內部測試可限制分享對象，但仍須檢查資料、權限和成本。下一節介紹 GitHub + Railway 外部部署；它是選修方案，也有自己的費用，<a href="' + BUILD + '" target="_blank" rel="noopener">官方 Build 說明</a>列出目前分享行為。',
          BUILD, "更正公開連結、免費額度與程式碼私密性的過度概括")

# CH6-3: keep the full external-hosting lesson, but make it accurate and explicitly optional.
old_c36 = "帳號不符合免費 Starter Tier、或已經用完 2 個免費 Publish 名額時，把程式碼推上 GitHub、用 Railway 開一條自己的部署線。"
new_c36 = "示範將 AI Studio Build 專案同步到 GitHub，再部署至 Railway。此選修路線有獨立的資格、用量與費用；AI Studio 亦支援 GitHub 同步與 Cloud Run 部署。"
for sel in ['meta[name="description"]', 'meta[property="og:description"]', 'meta[name="twitter:description"]']:
    set_meta("part6/CH6-3.html", sel, old_c36, new_c36, BUILD, "將外部部署定位為可選方案，移除過時觸發條件")
set_inner("part6/CH6-3.html", ".lesson-tagline",
          "帳號不符合免費 Starter Tier、或需要第 3 個以上的 app 時，把程式碼推上 GitHub、用 Railway 開一條自己的部署線。",
          '示範將 AI Studio Build 專案同步到 GitHub，再部署至 Railway。這是選修外部部署路線；先比較<a href="' + BUILD + '" target="_blank" rel="noopener">AI Studio GitHub／Cloud Run 選項</a>，並核對 Railway 當前條件與費用。', BUILD,
          "更新外部部署課程定位", body=False)
set_inner("part6/CH6-3.html", "#legacy-reference .section-heading", "情境：這是備援路線，不是必經之路",
          "情境：這是選修外部部署路線", BUILD, "把補充路線定位與目前官方路徑對齊")
set_inner("part6/CH6-3.html", "#legacy-reference p.body-text",
          "上一節的 Publish 是內建路線——一個按鈕，AI Studio 幫你把 app 放到公開網址，符合 Starter Tier 資格的話完全免費。但有三種情況，內建路線不夠用：",
          'AI Studio Build 目前可將完整應用部署到 Cloud Run，也支援與 GitHub 同步；Starter Tier 符合資格時最多可發布 2 個 app，標準部署需設定帳單，API 使用費另依模型方案計算。Railway 是可選的外部主機，適合需要比較 GitHub 工作流程或管理方式時評估，不代表免除 API 成本。查閱<a href="' + DEPLOY + '" target="_blank" rel="noopener">官方部署說明</a>與<a href="' + BUILD + '" target="_blank" rel="noopener">Build 說明</a>後，再判斷下列情境是否適用：',
          DEPLOY, "更新 AI Studio 當前部署選項與費用邊界")
set_inner("part6/CH6-3.html", "#legacy-reference .deploy-title", "公司帳號看不到免費層",
          "帳號不符合 Starter Tier 資格", DEPLOY, "移除對公司帳號的過度概括")
set_inner("part6/CH6-3.html", "#legacy-reference .deploy-desc",
          "用公司的 Google Workspace 帳號，因為帳單設定或組織政策，Starter Tier 選項沒有出現在畫面上。",
          'Google Workspace、Workspace for Education、Google for Nonprofits 或曾有 Google Cloud Billing 的帳號可能不符合 Starter Tier；以<a href="' + DEPLOY + '" target="_blank" rel="noopener">官方資格說明</a>與目前帳號畫面確認。',
          DEPLOY, "更新 Starter Tier 資格例外")
set_inner("part6/CH6-3.html", "#legacy-reference .deploy-title", "已用完 2 個免費名額",
          "需要超過 Starter Tier 的 2 個 app", DEPLOY, "移除免費名額和使用資格的誤解")
set_inner("part6/CH6-3.html", "#legacy-reference .deploy-desc",
          "Starter Tier 免費 Publish 名額有限，前面章節已經上架過幾個工具，第 3 個以上的 app 需要別的地方放。",
          'Starter Tier 限符合資格帳號最多 2 個部署；更多 app 可評估標準部署與帳單，或其他主機。各方案用量與費用依當前官方說明確認。',
          DEPLOY, "修正 Starter Tier 名額描述")
set_inner("part6/CH6-3.html", "#legacy-reference .callout-body",
          "符合資格就用內建的就好。如果你的帳號可以看到 Starter Tier、名額也還沒用完，直接照上一節的 Share／Publish 走就夠了。這一節是給前面三種情況的備援方案，不是每個人都需要走完。",
          '<strong>先比較內建選項：</strong>AI Studio Build 可同步 GitHub，也可部署到 Cloud Run；Starter Tier 僅適用符合資格的帳號。Railway 是外部選修路線，不能用來規避 Gemini API 使用費。先看<a href="' + DEPLOY + '" target="_blank" rel="noopener">AI Studio 部署說明</a>與<a href="' + RAIL_PLANS + '" target="_blank" rel="noopener">Railway 方案費用</a>，再決定是否需要下方操作。',
          DEPLOY, "說明 Railway 不代表免費部署")
set_inner("part6/CH6-3.html", "#legacy-reference p.body-text",
          "Railway 是一個能直接讀 GitHub repo、自動建置並跑起來的部署平台。註冊時建議直接用 GitHub 帳號登入——這樣連結的帳號才算「Full Trial」，沒驗證過的帳號是「Limited Trial」，對外連網會受限。",
          'Railway 可從 GitHub 專案部署。Trial 分為 Full 與 Limited，能否取得完整網路功能取決於 Railway 的帳號驗證條件；僅連結 GitHub 不保證驗證通過。請在註冊時查看目前帳號狀態與<a href="' + RAIL_TRIAL + '" target="_blank" rel="noopener">Railway Trial 官方條件</a>。',
          RAIL_TRIAL, "更新 Trial 驗證條件，不保證連結 GitHub 即為 Full Trial")
set_inner("part6/CH6-3.html", "#legacy-reference p.body-text",
          "Trial 條件：一次性 $5 credit，30 天內有效，不需要信用卡。限制是 1GB RAM、共享 vCPU、每個專案最多 5 個服務——對一個單機 app 來說綽綽有餘。",
          'Railway 官方目前列出一次性 US$5 Trial credit，最長 30 天或額度用完即止；Trial 資源上限、外連網路條件與資料保存依帳號狀態而異。官方文件未在此保證免信用卡；開始前查看<a href="' + RAIL_TRIAL + '" target="_blank" rel="noopener">Trial 條件</a>。',
          RAIL_TRIAL, "更新 Railway Trial 的期限、限制和付款方式說法")
set_inner("part6/CH6-3.html", "#legacy-reference .step-desc",
          "Railway 會偵測到這是 React + Vite 專案，自動跑建置流程，不需要手動下指令。",
          'Railway 會依 repo 中的專案檔案偵測建置與啟動方式；實際指令可能不同。若部署失敗，先看 Build／Deploy Logs，再依專案設定調整。',
          "https://docs.railway.com/quick-start", "避免假設每個 AI Studio 專案都有同一套 React + Vite 設定")
set_inner("part6/CH6-3.html", "#legacy-reference .deploy-pro", "長期免費，不限時間",
          "符合資格時最多部署 2 個 app；專案／Billing 條件見官方說明", DEPLOY, "不將 Starter Tier 延伸描述成全程免費")
set_inner("part6/CH6-3.html", "#legacy-reference .deploy-pro", "$5 credit，30 天免費",
          "一次性 US$5 Trial credit；最長 30 天或額度用完", RAIL_TRIAL, "更新 Railway Trial 條件")
set_inner("part6/CH6-3.html", "#legacy-reference .deploy-pro", "不需信用卡",
          "資格與付款方式依目前 Trial 頁面確認", RAIL_TRIAL, "移除未經官方文件支持的免信用卡承諾")
set_inner("part6/CH6-3.html", "#legacy-reference .deploy-con", "30 天後轉 Free plan，資料 30 天後可能被刪",
          'Trial 結束後轉 Free plan（每月 US$1 credit）；Trial stateful volumes 會在 credit 到期 30 天後刪除，詳見<a href="' + RAIL_TRIAL + '" target="_blank" rel="noopener">資料保存說明</a>',
          RAIL_TRIAL, "釐清到期後方案與刪除範圍")
set_inner("part6/CH6-3.html", "#legacy-reference .deploy-pro", "每月 $5，內含 $5 用量",
          "Hobby US$5／月，含 US$5 資源用量額度；以官方方案頁為準", RAIL_PLANS, "核對 Railway Hobby 方案並附官方頁")
set_inner("part6/CH6-3.html", "#legacy-reference .deploy-pro", "每月 $1 credit",
          "每月 US$1 credit，不累積；以官方方案頁為準", RAIL_PLANS, "核對 Railway Free 方案並附官方頁")
set_inner("part6/CH6-3.html", "#legacy-reference .deploy-con", "用量不累積，只夠小工具勉強跑",
          "額度是否足夠取決於實際資源使用量", RAIL_PLANS, "避免無依據估算小工具容量")
set_inner("part6/CH6-3.html", "#legacy-reference p.body-text",
          "結論：能用內建就用內建。Railway 這條路是給名額用完、帳號受限、或需要版本控制的情況，不是預設路線。",
          '結論：先比較 AI Studio Build 的 GitHub 同步與 Cloud Run。Railway 適合需要其外部部署工作流程時再評估；Starter Tier 資格、API 費用和 Railway 主機費用分別確認，不能只因名額或帳號限制就假設 Railway 更便宜。',
          BUILD, "修正以名額或帳號資格直接推薦 Railway 的結論")
set_inner("part6/CH6-3.html", "#legacy-reference .section-heading", "為什麼不能直接用 GitHub Pages",
          "GitHub Pages 能託管靜態檔，但不能提供伺服器端 API 執行環境", GH_PAGES, "更正 GitHub Pages 支援建置流程的事實")
set_inner("part6/CH6-3.html", "#legacy-reference .callout-body",
          "GitHub Pages 只能放靜態網頁。AI Studio 產出的 app 是一個 React + TypeScript + Vite 專案（App.tsx、components/、services/geminiService.ts），需要先跑建置流程才能變成可執行的網頁，而且呼叫 Gemini API 的邏輯需要一個能跑後端環境的主機。GitHub Pages 沒有建置流程、也沒有伺服器端運算，放不了這種專案——這正是需要 Railway 這類平台的原因。",
          '<strong>GitHub Pages 的邊界：</strong>它可以用 GitHub Actions 建置並託管靜態網站，但不支援伺服器端語言。含 Gemini API 呼叫的 app 必須把金鑰放在伺服器端，不能把 key 寫進公開前端程式；可評估 AI Studio Cloud Run 或其他具伺服器端執行環境的主機。參考<a href="' + GH_PAGES + '" target="_blank" rel="noopener">GitHub Pages 官方說明</a>與<a href="' + BUILD + '" target="_blank" rel="noopener">AI Studio Build 金鑰說明</a>。',
          GH_PAGES, "更正 GitHub Pages 不能建置、不能支援 JavaScript 的舊說法")

set_inner("part6/PRAC6-1.html", "#legacy-reference > summary",
          "原始完整課程內容、案例與提示詞（保留）",
          "原始完整課程內容、案例與提示詞（保留；Share／Publish／Railway 為選修，不列必修驗收）",
          BUILD, "避免保留的舊發布流程被誤認為必修", body=False)

for path, raw in pending.items():
    (ROOT / path).write_text(raw)
(REVIEW / "technical-corrections.json").write_text(json.dumps({
    "checked_on": "2026-10-06", "canvas_pages": canvas_pages, "corrections": audit
}, ensure_ascii=False, indent=2) + "\n")
print(f"Applied {len(audit)} source-backed corrections across {len(pending)} pages; Canvas steps updated on {len(canvas_pages)} pages.")
