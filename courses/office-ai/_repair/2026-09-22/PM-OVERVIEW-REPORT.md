# PM 核心入口修補報告：office-ai

## Changed

- `office-ai/index.html`
  - Hero 說明改為先說明 PM 角色、需求／限制／產出／審核主軸。
  - 在 Hero 後、課前自評前新增「課程核心：把自己當成 PM」入口區。
  - 補入「專業又親切」案例、五個風險缺口與可帶走的 PM 工作方法。
  - 同步 `description`、OG 與 Twitter 分享摘要。
- `../search-index.json`
  - 依既有產生流程重建；`office-ai/index.html` 的摘要已更新為 PM 核心定位。

## Copy review

- 敘事主線：流暢回應 → 未授權補全 → 寄出後形成承諾 → 人以 PM 身分要求與審核。
- 保留事實：LLM 可能依語言模式補出日期、折扣、交期；未宣稱模型一定如此，也未把模型描述成做出真正商業決策。
- 五個檢查點：事實、權限、時間、責任、檢查。
- 課程行動：先提供事實、指定限制、要求標示未知、審核產出、由人決定能否送出。
- 文案連貫性：`audit_copy_continuity.py` 0 warnings；未新增平台操作或未提供的技術事實。

## Verification

- backup：`office-ai/_backup/2026-09-22-pre-pm-overview/index.html`；修改前 SHA-256 與備份一致。
- restore script：`office-ai/_tools/restore-2026-09-22-pre-pm-overview.sh`；`bash -n` 通過。
- target lint：`0 BLOCKER / 0 ERROR / 0 WARN`。
- full course lint：`0 BLOCKER / 0 ERROR / 21 WARN`；21 條為既有 migration-debt，非本次目標頁新增。
- HTML structure：`office-ai/index.html` 通過；固定 office-ai 回歸頁 4/4 通過。
- substance／asset check：`block=0`、`missing_assets=0`；語意審查仍標記 `PENDING`。
- search index：949 筆；office-ai 摘要已反映 PM 核心。
- browser smoke：本地桌面預覽已確認 Hero、核心入口、五個缺口、自評區與單元清單銜接正常，未見水平溢出或導覽異常。
- RWD：本次預覽工具未提供獨立 `390px`／`430px` viewport 設定，手機尺寸尚標記 `PENDING`；未以桌面結果代替手機驗收。

## Restore

```bash
bash courses/office-ai/_tools/restore-2026-09-22-pre-pm-overview.sh
```
