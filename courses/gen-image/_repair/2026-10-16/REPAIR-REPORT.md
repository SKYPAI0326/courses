# gen-image 2026-10-16 修復報告

## 結論

現行版已完成逐批修正與 fresh reviewer 回歸，內容審查為 PASS，機器狀態可進 `MACHINE_READY_PENDING_HUMAN`。真人冷讀、登入平台當日實跑、理解／遷移測試與完整授課試跑尚未完成，因此不宣告發布完成。

## 執行批次

1. 盤點與備份：保存修復前課程頁、來源與大綱，提供 `_tools/restore-2026-10-16-pre-repair.sh`；`bash -n` 通過，未執行還原。
2. 課型與來源：修正 13 個核心 lesson source、outline 與 style guide，補齊 Demo／Together／Solo、停止條件、證據與離線路徑。
3. 學員素材：新增 platform check、prompt templates、brand DNA、QA／release gate、離線 candidate workbook 與 skeleton quick card。
4. Reference pack：以內建圖像生成工具製作 6 張課程專用、無人物／logo／正式文字素材；manifest 保存 prompt、用途、尺寸與 SHA256。
5. Learner-facing HTML：修正課程目錄 42 頁，更新平台能力表述、reference-first、正式文字後製、公平比較、來源／權利與人工 release gate。
6. Fresh review：依三輪唯讀審查逐批清除問題；最終 BLOCKER 0、MAJOR 0、MINOR 0，verdict PASS。

## Reference pack 證據

- Manifest：`assets/downloads/reference-pack-manifest.md`
- OFFLINE-01：1536×1024，SHA256 `94d0242e6196669bf7c19117147b1674953123a47dd9e43b8f5d9620299980b0`
- Quick card PDF：SHA256 `71210814d615bbe6282beaa8f9315fb83656f1582bc88f9759676e8849d0b6a5`
- 六張素材重算 hash 與 manifest 全數吻合。

## 最終機器檢查

- lint：42 頁；BLOCKER 0、ERROR 0、WARN 31。
- 結構：checked 42、blocked 0。
- substance：pages 34、block 0、missing_assets 0。
- 本地參照：42 頁、374 refs、missing 0。
- `git diff --check`：exit 0。
- 瀏覽器 smoke：修正版 10 頁於 1440×900 與 390×844 無水平溢位、無破圖、`.lesson-body` 存在；最終三頁再測亦通過。
- Restore script：`bash -n` exit 0。
- Course validator：13 份核心 source 均有單一成對 learner-content 邊界；重建證據 hash 後 exit 0、errors 0、valid records 3，狀態 `MACHINE_READY_PENDING_HUMAN`。

## 尚待人工完成

- 真人 entry／completion／understanding／transfer cold follow-along。
- 登入實際圖像平台確認當日模型、方案、reference、局部編修、來源訊號與輸出能力。
- 以真實平台輸出走完核心三課微序列與 CH5-1 release gate。
- 完成授課試跑後再決定是否發布。
