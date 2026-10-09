from pathlib import Path
import json,re,html
root=Path(__file__).resolve().parents[1];meta=json.loads((root/'_repair/2026-10-09/lesson-meta.json').read_text())
# Reuse the explicit parent/offset parser, without invoking its rendering loop.
scope={'__file__':str(root/'_tools/render-lessons.py')};source=(root/'_tools/render-lessons.py').read_text();exec(source.split("a=argparse.ArgumentParser();")[0],scope);Anchors=scope['Anchors']
p=root/'index.html';text=p.read_text();parser=Anchors(text);changes=[]
for n in parser.nodes:
 cls=n['attrs'].get('class','').split()
 if 'lesson-title' in cls:
  a=n['parent']
  while a and 'lesson-card' not in a['attrs'].get('class','').split():a=a['parent']
  if a:
   unit=Path(a['attrs']['href']).stem;m=meta[unit];changes.append((n['inner'],n['close'],html.escape(m['title'])))
 elif 'hero-desc' in cls:changes.append((n['inner'],n['close'],'從一次對話開始，練習整理文字、核對來源、生成小工具，再接人工覆核後的 Make 流程。每一部分都有可保存的成果與檢查方法，最後交付一項自己完成的專題。'))
 elif 'part-title' in cls and 'Make' in text[n['inner']:n['close']]:changes.append((n['inner'],n['close'],'人工覆核與 Make 自動化'))
 elif 'lesson-status' in cls:
  if any(x in text[n['inner']:n['close']] for x in ['範本卡','工具集','系統圖','Demo','自動化']):changes.append((n['inner'],n['close'],'實作成果'))
 elif 'footer-note' in cls:changes.append((n['inner'],n['close'],'36h · 零基礎工作應用 · 28 單元，依完成物與實際測試驗收'))
for start,end,new in sorted(changes,reverse=True):text=text[:start]+new+text[end:]
# Replace individual exact prose leaves using parsed text-node boundaries in the small remaining intro.
old='沒寫過程式、平常以 Office / Google Workspace 為主的上班族。想把 AI 用進日常工作（文書、會議、知識整理），並學會用 Make / n8n 把重複任務變成自動化流程。每個 Part 都帶走一份可立刻套用的 deliverable。'
new='適合平常使用 Office 或 Google Workspace、尚未用過 AI 的上班族。先使用虛構素材跟著做，再換任務獨立練習。基本對話用 Claude，來源筆記用 NotebookLM，自動化以 Make 為主；n8n 為選做。'
if old in text:text=text.replace(old,new,1)
text=text.replace('Make + n8n','Make 主線').replace('PRACTICE · 帶走範本','PRACTICE · 獨立練習').replace('每章帶走範本','每章保存成果')
p.write_text(text)
outline=(root.parents[1]/'_outlines/gen-ai-36h.md').read_text()
outline=outline.replace('tools: ChatGPT, Gemini, Claude, NotebookLM, Gemini Canvas, Make.com, n8n','tools: Claude（基本對話）, NotebookLM（來源筆記）, Make（主線）, ChatGPT/Gemini/n8n（選做）').replace('## Part 5：自動化流程設計 Make + n8n（6h）','## Part 5：人工覆核與 Make 自動化（6h）')
for unit,m in meta.items():outline=re.sub(r'^- '+re.escape(unit)+r'：.*$', '- '+unit+'：'+m['title'],outline,flags=re.M)
outline+='''\n## 學習路徑與驗收（2026-10-09修訂）

1. 提供資料與要求，追問、核對、保存。
2. 根據讀者處理文字與附件，不新增無來源承諾。
3. 找來源引用、核對版本與衝突。
4. 先凍結規則，再生成、測試、保存小工具。
5. 網頁AI由人覆核；新列進ReviewedQueue才觸發Make，紀錄／草稿不寄出。
6. 七欄工具卡在本機保存，JSON備份恢復。
7. 文件／来源筆記／小工具／自動化依類型驗收，個人HTML展示真實成果。

所有核心頁保留完整輸入、核對答案、修復與獨立練習。PRAC包含於各Part時數；一件主要成果為最低門檻，選做不加嚴必做。素材索引：courses/gen-ai-36h/assets/START-HERE.md。
正式開課仍需NotebookLM、Claude、Make目標帳號全路徑及零基礎真人試走。靜態與程式檢查不能取代實跑；未驗項目見課程修訂報告。
'''
(root/'_repair/2026-10-09/outline-updated.md').write_text(outline)
# Local governance documentation remains consistent with approved scope.
p=root/'CLAUDE.md';text=p.read_text();text=text.replace('主軸：工具應用 + 零代碼工具 + Make/n8n 自動化 + 結業專題','主軸：基本對話與核對 + 來源筆記 + 小工具測試 + 人工覆核後 Make 自動化 + 結業專題；n8n 為選做')
text+='''\n## 2026-10-09 教學修訂

正式正文由 `_repair/2026-10-09/lesson-plans/` 的 learner-content 範圍轉製；同步至全站 `_lessons/gen-ai-36h/`。28頁URL、設計、導覽與密碼關卡保留。
七欄工具卡統一；PRAC6/7使用各自本機保存鍵與JSON備份。Make使用ReviewedQueue新列觸發，九欄、四分類、待覆核／已覆核，不寄真客戶。
素材見 `assets/START-HERE.md`；備份、還原、執行證據與待驗項目見 `_repair/2026-10-09/`。未完成瀏覽器／平台／真人試走不得稱開課就緒。
''';p.write_text(text)
print('Synced index 28 titles; prepared same-course outline and governance')
