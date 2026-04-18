---
slug: pilot-c-python
name: "[試飛 C] Python 讀 Google Sheets API"
color: "#6b7fa3"
audience: 用過 Excel/Google Sheets、看過 ChatGPT 寫 Python 但自己從未跑過完整 .py 檔的上班族（分析師/營運/助理類）
institution: 弄一下工作室
duration: 1h
tools: Python 3.12, gspread, google-auth, Google Cloud Console, Google Sheets
prac: false
# === 課程製作團隊系統擴充欄位 ===
course_type: programming
pilot: true
pilot_purpose: 驗證「技術深度型」課程（需寫程式、設 Service Account、跑 terminal）在系統中的可行性
platform_version: Python 3.12 + gspread 6.0
---

<!--
試飛單元 C：以「Python + gspread 讀 Google Sheets」為案例，驗證 programming 類課程通過系統鏈路的能力。
觀察重點：
- 教案的 4 段式（需求→設計→實作→驗證）是否比 5 段式更適配程式課
- 試跑包的 .py + requirements.txt + credentials 能否具體到「學員複製貼上就跑」
- code-block 區塊的使用頻率與可讀性
- 「會裝 Python 不會寫程式」這個受眾設定是否真的存在（還是要下修到「從未寫過程式」）
-->

## 課程定位（Positioning）

讓已經在電腦裝好 Python 但一直不敢動手寫的上班族，在 1 小時內**從零建立 Service Account、裝好套件、執行一個 10 行以內的 `.py` 檔**，把 Google Sheets 的資料讀進 Python 並新增一列。學完不會讓你變工程師，但會讓你**跨過「打開 terminal 跑 Python 讀雲端資料」的心理門檻**，之後可以自己抄範例改成工作自動化。

## 受眾畫像（Audience Profile）

- **職業**：行銷分析師 / 業務支援 / 營運分析 / 會看資料但不寫程式的管理職
- **技術底子**：Excel/Sheets 熟手（會 VLOOKUP、pivot table）、讓 ChatGPT 寫過 Python 程式碼、用過 `python3 --version` 確認裝好了，但**從未跑完整一支 .py** 檔、看到 `def` 會緊張、沒碰過 API credential
- **現有工具棧**：Excel/Google Sheets 熟、ChatGPT 生過程式碼但不敢執行、裝了 VS Code 但只用來看檔、Python 是裝了但 terminal 只打過 `python3 --version` 這一行
- **痛點 3 條**：
  1. 老闆/自己想用 Python 做資料整理，但每次想動手就卡在「credentials 要怎麼申請」「為什麼 `pip install` 會報錯」，3 小時過去沒進展
  2. ChatGPT 生的程式碼看起來能跑，複製貼上後一堆錯誤訊息，不知道該改哪
  3. 自動化課看過很多，但教材都假設「你會寫 Python」或「你是工程師」，沒有給**完全沒跑過 .py** 的人的起步教學

## 學習成果（Outcomes，5 條）

**時間分配**：課前預備 10 分鐘（Service Account 設定，有獨立指南），課中 50 分鐘（4 個 outcomes）。

**課前預備（10 min）**：
0. **能**完成 Google Cloud 4 步驟設定：建 Project → 啟用 Google Sheets API → 建 Service Account → 下載 credentials.json，並**把 Service Account 的 email 加到目標 Sheet「共用」清單權限「編輯者」**（這一步最常漏）

**課中 Outcomes（50 min）**：
1. **能**在 terminal 執行 `pip install -r requirements.txt`，並在 `.py` 檔用 `import gspread` 無 ImportError
2. **能**用自己的話重新註解 `reader.py` 每一行（例：「這行在告訴 Python 去讀 credential 檔」），**8 行全部註解完**
3. **能**執行 `python3 reader.py`，terminal 印出從 Google Sheet 讀出的 5 列資料
4. **能**修改 `writer.py` 中 `append_row([...])` 括號裡的資料內容，執行後**在瀏覽器打開 Google Sheet 看到新增的一列，資料符合你改的內容**

## 前置知識依賴鏈（Prerequisite Chain）

```yaml
dependencies:
  CH1-1: []  # 試飛只有 1 單元
```

## 試跑包交付規格（Verification Assets）

**類型**：programming

**⚠️ 給課程設計師**：programming 類試跑包是**學員照著跑能成功執行**的最小程式包，不是解答本。具體產出：

### 1. `requirements.txt`（3 行）

```
gspread==6.0.0
google-auth==2.29.0
google-auth-oauthlib==1.2.0
```

### 2. `reader.py`（8 行以內，必含註釋）

讀取指定 Google Sheet 第一個工作表的前 5 列，print 到 terminal。骨架：

```python
import gspread
from google.oauth2.service_account import Credentials

# 載入 Service Account 憑證
creds = Credentials.from_service_account_file("credentials.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"])
gc = gspread.authorize(creds)

# 開啟指定 Sheet（用 Sheet URL 或 key）
sheet = gc.open_by_key("YOUR_SHEET_KEY_HERE").sheet1

# 讀前 5 列並印出
for row in sheet.get_all_values()[:5]:
    print(row)
```

### 3. `writer.py`（8 行以內）

append 一行資料到同一個 Sheet。骨架：

```python
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

creds = Credentials.from_service_account_file("credentials.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"])
gc = gspread.authorize(creds)
sheet = gc.open_by_key("YOUR_SHEET_KEY_HERE").sheet1

# 新增一列：[目前時間, "hello", "from python"]
sheet.append_row([datetime.now().isoformat(), "hello", "from python"])
```

### 4. `credentials.json.template`（空殼檔 + 填寫說明）

```json
{
  "_說明": "請從 Google Cloud Console 下載 Service Account JSON 取代本檔，並把檔名改成 credentials.json（去掉 .template）",
  "_步驟": [
    "1. cloud.google.com/console → 建立 Project（名稱：pilot-c-python）",
    "2. APIs & Services > Enable API → 找 Google Sheets API 啟用",
    "3. Credentials > Create → Service Account → 命名 pilot-c-sa → Create",
    "4. Service Account 清單點進去 > Keys > Add Key > Create new key > JSON → 下載",
    "5. 把下載的檔案改名 credentials.json，放進專案資料夾"
  ],
  "_格式範例": {
    "type": "service_account",
    "project_id": "你的專案 id",
    "private_key_id": "...",
    "private_key": "-----BEGIN PRIVATE KEY-----...",
    "client_email": "pilot-c-sa@你的專案.iam.gserviceaccount.com"
  }
}
```

### 5. `setup.md`（5 步驟環境建置指南）

1. Python 版本驗證：`python3 --version` 需 ≥ 3.10
2. 建立專案資料夾 `mkdir pilot-c && cd pilot-c`
3. 安裝套件 `pip install -r requirements.txt`
4. Google Cloud Console 建 Service Account（詳 `credentials.json.template` 內的步驟）
5. **關鍵**：把 Service Account 的 email（`pilot-c-sa@....iam.gserviceaccount.com`）加到你目標 Google Sheet 的「共用」清單、權限「編輯者」——不做這步 Python 會讀不到 Sheet

### 6. `sample-sheet-link.md`

使用者要自己建立 Google Sheet 並貼連結到這裡。範本第一列表頭：`timestamp, message, source`，前 5 列可以手動填假資料讓 reader.py 有東西可讀。

### 檔案擺放

```
_pilots/_trial-packs/pilot-c-python/
  ├── requirements.txt
  ├── reader.py
  ├── writer.py
  ├── credentials.json.template
  ├── setup.md
  └── sample-sheet-link.md
```

## 單元矩陣

### Part 1：試飛（1h，僅 1 單元）

- **CH1-1：Python 讀 Google Sheets API 入門** — 建 Service Account → 裝套件 → 跑 reader.py → 執行 writer.py 並驗證（60 min）
