---
course: uiux-designer
schema_version: 1
---

# Evidence Schema：課程操作與平台證據

## 必填欄位

| 欄位 | 說明 |
|---|---|
| `run_id` | 同一次自主執行的固定識別碼 |
| `probe_id`／`step_id` | 對應 Probe、單元與原子操作 |
| `timestamp` | 操作發生日期；必要時加時區 |
| `platform` | Chrome／Figma／本地 Git／部署平台 |
| `precondition` | 操作前畫面、檔案或權限狀態 |
| `input` | 學員實際使用的文字、尺寸、檔案或選項 |
| `action` | 一個可重播的動作，不用「完成設計」等模糊詞 |
| `visible_result` | UI、檔案、Preview 或終端可觀察結果 |
| `expected`／`actual` | 預期與實際並列，保留落差 |
| `evidence_path` | 截圖、DOM、檔案、URL、commit 或報告位置 |
| `verdict` | 依下列狀態機判定 |
| `repair` | 失敗時的修復動作；沒有修復填 `null` |
| `rollback` | 回復測試檔、檔案或設定的方法 |

## 判定狀態

| 狀態 | 使用時機 |
|---|---|
| `NOT_RUN` | 沒有實際操作或證據 |
| `SIMULATED_PASS` | 只用靜態／模擬環境，不能代表平台通過 |
| `MACHINE_PASS` | Codex 在實際平台看到預期結果 |
| `MACHINE_PASS_PARTIAL` | 核心控制通過，但完整任務或另一個條件未驗證 |
| `CONDITIONAL` | 功能可用但有方案、權限、拆檔或可靠性限制 |
| `BLOCK` | 無法完成、沒有合理備援或付費才可用 |
| `MACHINE_READY_PENDING_HUMAN` | 課程與自動證據齊全，仍等待真人冷跟做 |
| `HUMAN_PASS` | 只有使用者／真人學員實際跟做後才能使用 |

## 成品證據層級

1. **L0 描述**：只有文字說明；不可作為放行證據。
2. **L1 UI 狀態**：DOM、面板、方案提示或 Preview URL。
3. **L2 實體檔案**：PNG／PDF／HTML／Git commit／可重開 Figma 檔。
4. **L3 任務回歸**：固定任務從起點到完成物重跑，含失敗修復與回歸。
5. **L4 真人驗收**：真人學員只用講義與素材完成，另需記錄提示次數與實際時間。

正式單元至少需要 L2；核心 Prototype／交付單元需要 L3；L4 在第二階段才可出現。

## 互相對照

- `RUN-LOG.jsonl` 保存每次操作的原始紀錄。
- `PROBE-A/B/C.md` 統整平台結果與教學解讀。
- `CORE-OPERATION-INVENTORY.md` 將一項能力拆成可重播操作。
- `COVERAGE-LEDGER-PASS1.md` 將正式課綱、原子操作、完成物與證據互相連結。

