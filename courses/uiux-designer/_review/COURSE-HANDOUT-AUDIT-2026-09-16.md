---
course: uiux-designer
review: learner-handout-and-copy
date: 2026-09-16
status: MACHINE_READY_PENDING_HUMAN
---

# UI/UX 講義與文案品質審查

## 審查目的

確認學員只拿到入口頁、單元頁與列出的素材，就能理解工作情境、取得起始材料、完成一個可觀察成果，並把成果交給下一個單元。文案審查依 `uiux-designer/_design/COPY-RISK-GATE.md` 檢查公式化對比、空泛過場、模糊權威、宣傳詞與結構指紋；掃描器只把公式化對比列為 BLOCK，其他訊號交給人工判讀。

## 課綱主軸對照

正式大綱的主軸是：

```text
介面元素與設計（42h）
→ UI/UX 原型製作與資料打包（57h）
→ 可測試、可交接、可版本化的設計成果
```

目前已產出的學員試點是 33h：

| 試點單元 | 時數 | 新增能力 | 交給下一段的成果 |
|---|---:|---|---|
| A3 Auto Layout | 6h | 固定寬度、Auto height、長文字壓力測試 | 手機 Frame、設定值、壓力紀錄 |
| B4 Overlay | 2h | 一檔一核心 action、Open overlay、Chrome Preview | 可預覽的 Host／Overlay Figma 檔 |
| B6 任務測試 | 6h | 任務腳本、Actual／Expected、單一變因回歸 | 測試表與修正紀錄 |
| B7 Handoff | 6h | PNG／PDF／Inspect、限制清單 | 可追溯的 Handoff 包 |
| B8 網頁與 Git | 13h | 最小 HTML／CSS／JavaScript、本機驗證、Git commit | 可在 Chrome 開啟的網站與版本紀錄 |

尚未產出的正式單元：A1、A2、A4、A5、A6、A7、A8、B1、B2、B3、B5，共 66h。這些單元完成前，課程狀態只能維持試點，不能標記為完整 99h 講義。

## 零基礎學員路徑

目前試點頁已按下列順序組織：

```text
情境與代價
→ 起始材料與取得方式
→ 完成物預覽
→ 白話概念與判斷規則
→ 完整示範
→ 同步跟做
→ 單一變因練習
→ Checkpoint 與修復
→ 驗收與下一單元接手
```

代表性結果：

- A3 已補上短句／壓力句、402×874 Frame、200 px 寬度、Auto height／Hug、Layers 層級、6 步跟做、2 個 Checkpoint、錯誤修復與下一步 B4。
- B4 已有 Figma Starter／Chrome 的環境契約、Frame 尺寸、完整 action 設定、Preview 結果、方案限制、Solo 變化與 B6 接手條件。
- B6、B7、B8 已保留產物鏈，但真人冷讀與跨帳號重做仍待人工 Gate。

## 文案修訂規則

### 本次移除的生成式對比句型

學員頁與五份試點教案已通過 `docs/audit-copy-patterns.py --strict`，目前為 `0 BLOCK / 0 REVIEW`。原本的句型已改成直接描述：

- 說明學員要做的工作與可見結果。
- 說明平台限制與可用的備援路徑。
- 說明錯誤現象、回修位置與重跑條件。
- 說明上一段產物如何成為下一段輸入。

本輪曾出現的 REVIEW 例子已改成可觀察的文字、尺寸與操作結果；後續新增內容仍需逐行人工判讀，不能只看掃描器結果。

### 仍可使用的否定句

操作需要排除錯誤時，可以寫「若高度仍為 Fixed height，回到第 5 步」，因為它指向可觀察狀態與修復位置。品質閘門禁止的是反覆用抽象對比句濃縮課程定位，不禁止必要的錯誤提示。

## 審查命令與結果

```text
python3 docs/audit-copy-patterns.py --strict uiux-designer ../_lessons/uiux-designer
Copy pattern audit: 0 finding(s) (0 BLOCK, 0 REVIEW)

python3 .../audit_copy_continuity.py <each learner page and lesson plan>
All current UI/UX pilot pages: 0 warning(s)
```

另外已檢查入口頁與 A3 頁的本地連結，素材檔、起始頁、Probe 摘要與下一單元連結均存在。入口頁已在 Chrome 實際載入並以可及性樹與畫面檢查。

## 尚未放行的內容

- A1–A2、A4–A8、B1–B3、B5 尚未有完整學員頁與可重跑素材。
- Form 多欄位、List 多列增刪、Swap、固定元素與滾動同時成立、完整 Smart Animate、Photoshop 實際輸出、GitHub push、公開部署仍維持 `CONDITIONAL` 或 `NOT_RUN`。
- A3、B4、B6、B7、B8 尚未完成真人冷讀、跨帳號重建與三單元人工微序列驗收。

## 結論

目前完成的是「有完整學習骨架與文案閘門的 33h 機器試點」，不是 99h 正式放行課程。下一個製作循環應依同一份 Blueprint、Coverage Ledger、Environment Contract 與文案閘門，補齊 66h 正式單元，再進行真人試跑。
