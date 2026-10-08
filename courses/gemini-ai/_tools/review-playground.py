#!/usr/bin/env python3
"""Build auditable recommendations from reviewed cases; manual content judgement stays explicit."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_repair/2026-10-08/playground-build';cat=json.loads((ROOT/'_source/playground/catalog.json').read_text());new=json.loads((OUT/'new-case-review.json').read_text());newby={c['unit']:c for c in new['cases']};manual=json.loads((OUT/'manual-content-review.json').read_text())['cases'];families={};records=[]
for c in cat['cases']:
    cid=c['id'];source=ROOT/c['source'];s=BeautifulSoup(source.read_text(),'html.parser');ps=s.select('[data-policy-prompt]');assets=ROOT/'assets/playground'/cid
    families.setdefault(c['family'],[]).append(cid)
    if cid.startswith('PG'):
        o=newby[cid]['source'];original=(ROOT/o['path']).resolve();origin_ok=original.exists() and hashlib.sha256(original.read_bytes()).hexdigest()==o['sha256'];c['origin']={'course':original.parent.name,'page':o['path'],'sha256':o['sha256'],'blocks':o['blocks'],'adaptation':newby[cid]['adaptation']}
    else:
        original=ROOT/'_backup/2026-10-08-playground-pre/before'/c['page'];origin_ok=original.exists() and hashlib.sha256(original.read_bytes()).hexdigest()==c['origin']['sha256']
    manual_ok=manual.get(cid,{}).get('status')=='AUTHOR_ACCEPTED' and manual.get(cid,{}).get('source_sha256')==hashlib.sha256(source.read_bytes()).hexdigest()
    material_ok=all((assets/f).exists() for f in ['prompt.txt','cases.txt','answers.md']);prompt_ok=bool(ps) and (assets/'prompt.txt').read_text()==ps[0].get_text()
    record={'id':cid,'title':c['title'],'source':c['source'],'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'origin_verified':origin_ok,'prompt_download_match':prompt_ok,'materials_present':material_ok,'distinct_family':c['family'],'content_review':'AUTHOR_REVIEWED' if manual_ok else 'STALE_REQUIRES_REVIEW','platform_generation':'PENDING','human_follow_along':'PENDING','recommendation':'收錄' if origin_ok and material_ok and prompt_ok and manual_ok else ('待內容審閱' if not manual_ok else '需修復')}
    if cid.startswith('PG'):
        record['author_runtime_evidence']='browser/playground-tools-results.json'
    else:record['author_runtime_note']='原參考示範保留；新增A/B為生成工具的驗收依據，不宣稱原示範完整實現所有生成需求。'
    records.append(record)
    c['review'].update({'source':'VERIFIED' if origin_ok else 'FAIL','reusable_prompt':'AUTHOR_REVIEWED' if manual_ok else 'PENDING','case_separation':'AUTHOR_REVIEWED' if manual_ok else 'PENDING','distinct_outcome':'AUTHOR_REVIEWED' if manual_ok else 'PENDING','materials':'VERIFIED' if material_ok else 'FAIL','prompt_download':'PASS' if prompt_ok else 'FAIL'})
duplicates={k:v for k,v in families.items() if len(v)>1};assert not duplicates,duplicates
(catfile:=ROOT/'_source/playground/catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2))
(OUT/'case-review.json').write_text(json.dumps({'actor':'author-parent-content-review','cases':records,'duplicates':duplicates,'semantic_review_is_manual':True},ensure_ascii=False,indent=2))
lines=['# 案例推薦與收錄紀錄','', '依使用者2026-10-08授權正式修改，在五章主線之外建立29例遊樂園。審閱三份样本後由同一内容代理人完成六例，主代理整併既有23例並驗證。','', '| 案例 | 完成物與新增判斷 | 建議 | 來源 |','|---|---|---|---|']
for c,r in zip(cat['cases'],records):lines.append(f'| {c["id"]} {c["title"]} | {c["goal"]} | {r["recommendation"]} | {c["origin"].get("page",c["source"])} |')
lines+=['','## 合併與暫不收錄','', '- 提示詞模板組合台與黃金公式同族，模板另作參考，不充案例數。', '- 預算配色改造合併於預算工具方法；不把外觀變奏算另一種工作工具。', '- 專案風險看板讓人輸入風險與下一步，案件追蹤板按截至日計算期限與匯入唯一案件；兩者輸入、處理及完成物不同。', '- 客服語意分類、會議語意摘要需要模型與環境驗證，留在模型參考區。關鍵字初篩只標原文候選，不能冒充語意判讀。', '- Vercel/其他外部部署及多人同步留延伸參考，不列單檔離線工作案例。', '', '## 後續審核順序','', '新增候選先盤點來源與素材，再由內容審閱者說明新的學習成果及與既有案例的差異。必要條件：可追查來源；新完成物；可重用提示詞；獨立A/B/例外；完整背景、觀念、示範、操作與收束；可核對輸出。任何必要條件缺失，列需補資料，不能按分數平均放行。', '', '先產生推薦清單供使用者討論；選定後交同一內容代理人產製，主代理審閱樣本再擴批。HTML與實際工具操作分開驗收。source/TXT/ZIP/瀏覽器與參考品通過不等同Gemini實際生成或真人學習。', '', '執行 python3 _tools/review-playground.py 會驗證來源指紋、材料和提示詞同步並更新推薦；只有正文SHA256符合manual-content-review.json的人工審閱指紋才沿用作者審閱；改稿或新增案例會回到待審。這些機器項目不取代語意審查或真人判斷。']
(OUT/'RECOMMENDATIONS.md').write_text('\n'.join(lines).replace('样本','樣本').replace('内容','內容')+'\n')
if any(r['recommendation']!='收錄' for r in records):raise SystemExit('存在待審/需修案例，詳見推薦紀錄')
print('29例來源/材料/TXT對應通過，去重29族；推薦紀錄已產生，平台/真人仍待測')
