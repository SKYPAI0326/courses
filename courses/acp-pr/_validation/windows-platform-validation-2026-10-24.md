# Windows Premiere 平台驗證摘要

- 日期：2026-10-24（Asia/Taipei）
- 主機：`B1012-PC60`
- 應用程式：Adobe Premiere Pro 26.0.0 Build 72
- 執行方式：自動化代理操作 Premiere GUI；CH0-2 精準時間碼步驟由使用者協助重測
- 結論範圍：只支持指定 Premiere 版本與下列五個單元的實機路徑；不支持零基礎 cold follow-along、`HUMAN_VERIFIED` 或 `HUMAN_READY`

## 單元結果

| 單元 | 結果 | 實際完成的核心路徑 |
|---|---|---|
| CH0-1 | PASS | 建立序列、區分 Source／Program Monitor、Make Offline、Link Media 恢復 |
| CH0-2 | PASS（歷史實測） | Overwrite、Insert、Unlink、A1 Mute、Lift／Extract、H.264 輸出；補驗畫面顯示 Source In／Out 為 `03:01`、14–16 秒 Extract 為 `02:01` |
| CH0-3 | PATH PASS | 僅確認 Properties、Effect Controls、Text／Captions、Remove Unused、Auto Reframe Sequence、Export 六類介面入口 |
| CH1-1 | PASS | raw／修正版 SRT 匯入、字幕軌建立、錯句與修正句顯示 |
| CH1-3 | PASS | 依三組固定 timecode 重建約 25 秒直式序列、fallback 字幕、1080×1920／25 fps／H.264 輸出 |

CH0-3 的 `PATH PASS` 不代表固定五題或代表練習終態已完成。CH0-2 教材已依 inclusive Out 校正文字，但本摘要保留當時實測事實，不把後續文字修正描述為重新實機重跑。

## 版本與完成品

- Premiere 專案 SHA-256：`9A4A479799DE1361697B356BF48E349E09FADAB2F83172F767B58A7CBDBC3D52`
- `practice-cut-v1.mp4`：1920×1080、25 fps、H.264、21 秒；SHA-256 `5E1196D6C0853E6FAE1C2B114A152D6F63D59CED3DE4E263C8F35779676932D8`
- `ai-mini-cut-v2.mp4`：1080×1920、25 fps、H.264／AAC、24.96 秒；SHA-256 `1b883937edd9f7af066e8551f22f40c8bdadb13e307e1453c557d068c7f4c325`

## 原始證據索引

- 原始報告：`ACP-PR-Validation/windows-validation-evidence/REPORT.md`
  - SHA-256：`4245035baa1d242ba4be8e0962c9f504cc31aea7a0b924ad941d6537f45a0d00`
- CH0-2 3 秒 Source In／Out：`10-ch0-2-source-inout-human-pass.png`
  - SHA-256：`dd55e62338760a28eac642630d958a79662a3dfd62c4ddbf87d2126202dff2f9`
- CH0-2 14–16 秒 Extract：`12-ch0-2-extract-14-to-16-pass.png`
  - SHA-256：`29ce46ecd7cbdcd546e792c04fa6f35dfa8afffed89c04b103ad127fd31a4ad9`

原始報告與影像保存於使用者的 ACP PR NEW 驗證資料夾；本檔是供課程 evidence manifest 引用的摘要，不取代原始檔。

## 失敗與復原

- CH0-2 第一次 timecode 欄位焦點導致標記偏移；自動化重試一次仍不符後停止，保留 BLOCK 紀錄，再由使用者補做精準步驟後改判 PASS。
- CH1-3 第一次只使用參考片，未依三組 timecode 重建；精準重測改用兩分鐘原始素材建立 `ai-mini-cut-v2`，完成字幕與輸出後改判 PASS。
- CH1-1 修正版 SRT 因遊標位置造成整軌偏移；只用於驗證 Premiere 解析與文字修正，不作為 CH1-3 交付成品。
