# Course Blueprint

- **Course**：AI 入門即戰力：零基礎的 AI 入門應用
- **Audience**：第一次系統使用 LLM 的成人學習者，能使用瀏覽器與複製貼上
- **Workplace outcome**：學員能把一項模糊的工作或生活需求改寫成提示詞，取得可編輯的文字、摘要或規劃初稿
- **Duration and sequence**：4 個 skill-operation 單元，各 3 小時，共 12 小時
- **Lesson types**：CH1-1、CH2-1、CH3-1、CH4-1 皆為 skill-operation；CH3-1 固定使用 NotebookLM
- **Free baseline and paid-tool boundaries**：其他 LLM 不指定平台；學員使用可取得的免費或既有服務。NotebookLM 為課程固定平台，課前確認當期免費使用界線與介面
- **Shared environment**：課程提供瀏覽器可開啟的 NotebookLM、純文字來源檔、提示詞工作表與離線備援內容
- **Capstone deliverables**：四份完成物組成個人 AI 實務包：LLM 對話紀錄、日常文書包、NotebookLM 閱讀包、生活應用卡

## Artifact Dependency Graph

| lesson | input artifact | learner transformation | output artifact | next use | capstone component |
|---|---|---|---|---|---|
| CH1-1 | `assets/worksheets/unit1-practice-sheet.md` | 用五欄提示詞框架完成五個日常對話與一次修改 | `unit1-practice-sheet-complete.md` 填寫版 | CH2-1、CH4-1 沿用提示詞欄位 | LLM 對話紀錄 |
| CH2-1 | CH1-1 的五欄框架 + `assets/templates/unit2-communication-scenarios.md` | 依對象、語氣與長度改寫文字 | `unit2-communication-pack-complete.md` | CH4-1 取一個實際情境做個人化 | 日常文書包 |
| CH3-1 | `assets/sources/` 內課程來源檔 | 加入 NotebookLM、提問、摘要、抽取與條列 | `unit3-notebooklm-reading-pack-complete.md` | CH4-1 將來源整理方法轉到自己的文件 | NotebookLM 閱讀包 |
| CH4-1 | 前三單元的提示詞欄位 + `assets/prompts/unit4-lifestyle-prompts.md` | 改寫一項生活任務並完成結果 | `unit4-lifestyle-application-card.md` | 課後直接重做或更新 | 生活應用卡 |

## Core Operation Inventory

| operation_id | lesson | why learner cannot infer it | input/state | action | visible result | verification | repair |
|---|---|---|---|---|---|---|---|
| OP-01 | CH1-1 | 學員容易把搜尋問題與對話任務混在一起 | 一個日常需求 | 把需求拆成情境、任務、資料、條件、格式 | 可複製提示詞 | 五欄都有具體內容 | 回到工作表逐欄補值 |
| OP-02 | CH1-1 | LLM 輸出可能太長或不合用 | 第一版回答 | 使用長度、語氣、格式修改指令 | 第二版回答更符合用途 | 對照前後版本 | 只改一個條件後重問 |
| OP-03 | CH2-1 | 同一內容要依讀者改寫，不是複製貼上 | 請假或回覆情境 | 指定讀者與語氣，產出三版本 | 三份可編輯文字 | 每版讀者與語氣不同 | 補上讀者、場合與長度 |
| OP-04 | CH3-1 | NotebookLM 的來源、提問與引用有固定順序 | 課堂必做 3 份來源；另有 6 份延伸來源 | 建立 notebook、加入來源、提出可回到原文的問題 | 回答附來源引用 | 點引用可回到原文位置 | 用純文字備援檔重做輸入；恢復後重跑正式引用 |
| OP-05 | CH3-1 | 摘要、抽取與條列是三種不同任務 | 一段長文件 | 依輸出目的提出不同提示詞 | 一句、200 字、500 字、重點與行動 | 保留要求的欄位與長度 | 先縮小來源或改用單一任務 |
| OP-06 | CH4-1 | 生活需求需要個人條件，不能直接照抄範本 | 30 套提示詞卡 | 只改預算、時間、偏好等主要條件 | 一份個人化規劃或比較結果 | 條件有出現在輸出 | 回到提示詞，補上缺少的條件 |

## Environment Contract

| tool/version date | account role | permission | free/paid | starting file/data | success output | fallback | interface-change lookup |
|---|---|---|---|---|---|---|---|
| 任一可用 LLM／課前確認 | 學員自己的一般使用者 | 能輸入文字並複製輸出 | 依學員可取得的服務；不要求付費 | 各單元提供的 Markdown 工作表／提示詞資產與瀏覽器中的對話畫面 | 一段可複製、可保存的回答 | 各單元指定的 Markdown 備援內容完成判讀；工具恢復後重跑正式版本 | 依正在使用的服務搜尋「新對話」「複製回答」「重新生成」等當期功能名稱 |
| NotebookLM／課前實機驗證 | 學員自己的 Google 帳號 | 能建立 notebook、加入文字或檔案來源、查看回答引用 | 以課前確認的免費界線為準，不要求付費 | 課程提供的 `assets/sources/` 來源檔 | NotebookLM 回答能指向加入的來源 | 用同一份來源的純文字內容，在其他 LLM 完成摘要，但標記為非 NotebookLM 版本 | 開啟 NotebookLM 當期說明，搜尋「加入來源」「來源」「引用」 |

## Coverage Ledger policy

`COVERAGE-LEDGER.md` 先凍結核心原子，再於每個代表頁完成後填入實際證據。未完成的後續單元素材標記為 `PLANNED`，不得在 HTML 產製前宣稱 `READY`。

## Micro-sequence

第一個可測試的三課鏈為 CH1-1 → CH2-1 → CH3-1：CH1-1 產出的五欄提示詞框架，會在 CH2-1 改寫文書；CH2-1 的「讀者／語氣／格式」判斷，會在 CH3-1 轉成 NotebookLM 的來源提問格式。CH3-1 的實際來源包與閱讀完成物，再交給 CH4-1 作為生活應用的查詢與整理參考。
