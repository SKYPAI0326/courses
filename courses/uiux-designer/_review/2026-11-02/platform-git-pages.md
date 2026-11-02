# B8 平台現況核對（Git／GitHub／Pages）

核對：fresh-context 子代理，2026-11-02，唯讀。講義三段內嵌程式碼與 `web-starter/`、`studio-tasks-web.zip` 逐字一致。

## A. 平台現況

| 講義原句 | 現況 | 來源 | 嚴重度 |
|---|---|---|---|
| 從 Git 官方下載安裝；macOS 依教室準備 | git-scm.com Mac 安裝檔停在 2021；現行做法 `xcode-select --install` 或 `brew install git` | git-scm.com/install/mac | 誤導 |
| 依瀏覽器／Credential Manager 登入 | Windows 的 Git 內含 GCM 會跳瀏覽器；Mac 的 Apple Git／Homebrew Git 沒有 GCM，需 `gh auth login`、另裝 GCM，或密碼欄貼 PAT | docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git | 阻斷（Mac） |
| GitHub 不接受帳號密碼 | 正確，但沒教 PAT 或替代路徑 | docs.github.com/en/get-started/git-basics/about-remote-repositories | 誤導 |
| `git diff --cached`（首次約 250 行） | 進入分頁器，要按 q 離開，講義未提 | git-scm.com/docs/git-config（core.pager） | 阻斷 |
| Windows `git add` | 可能出現 LF／CRLF 警告，講義未提 | git-scm.com/book/en/v2/Customizing-Git-Git-Configuration | 誤導 |
| 建立 New repository | 右上角「+」→ New repository → Owner、Repository name、visibility → Create repository | docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository | 輕微 |
| Settings → Pages | 正確；窄視窗時 Settings 收在「…」 | docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site | 輕微 |
| 等部署結果完成 | push 後最多約 10 分鐘；進度看 repo 的 Actions 分頁 | docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site | 誤導 |
| noreply 地址 | Settings → Emails →「Keep my email addresses private」 | docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address | 輕微 |

其餘 12 條正確：`git --version`、`init -b`（2.28+）、repo 層 config、add／status／diff／commit／log、remote／push、不勾 README、Pages 兩種 Source、main＋/(root)、Free 帳號需 public repo、網址格式、Visit site、密碼驗證停用。

## B. 程式碼與流程

| 問題 | 實際 | 嚴重度 |
|---|---|---|
| START-HERE 是 Figma 範本文字，沒連 zip | `assets/B8-web-git-deploy/START-HERE.html` | 誤導 |
| 說 TASK-DATA.csv 是資料來源 | 網站不讀 CSV；`app.js` 用 `done` 布林值，CSV 用 `status` | 誤導 |
| 「修改三筆資料」 | `app.js:7-9` 自動產生 T04～T15，只改三筆會殘留舊情境 | 誤導 |
| 三項修改排在 `git init` 之前 | 修改會被併入第一筆基準 commit；`README.md:19` 要求先建基準 | 誤導 |
| 「先改標題」寫在命令之後 | 照順序跑會得到空 diff、commit 失敗 | 阻斷 |

## 零基礎卡點

沒教註冊 GitHub 與驗證 email；Mac 沒有安裝步驟；分頁器按 q；Mac push 無認證路徑；沒說部署要等多久、去哪看。

## 待實機確認

Mac VS Code Terminal 內 `git push` 的登入流程；Windows GCM 視窗文字；新 repo 表單預設值；Pages 頁 folder 選單標籤與實際耗時；CRLF 警告原文。
