from pathlib import Path
import csv,json,math
p=Path(__file__).resolve().parents[1]/'assets';p.mkdir(exist_ok=True)
def put(name,text): (p/name).write_text(text.strip()+'\n')
put('beginner-start.md','''# 第一次使用與保存
1. 在瀏覽器開啟 https://claude.ai/ ，登入自己的帳號。課堂先只使用這個對話工具。
2. 選「新對話／New chat」，確認不是先前另一項工作的對話。輸入框是你交代任務的地方。
3. 貼入 CH1-1 的完整文字，按送出箭頭。等待回應；不要在生成時連續重送。
4. 在同一輸入框追問「請指出三點摘要各根據哪一行原始資料」。追問會沿用前文。
5. 逐行比對後複製結果，貼到你自己的文件；不要只依賴聊天紀錄。
6. 建立資料夾「AI課程練習」。Windows 可在檔案總管按新增資料夾；Mac 可在 Finder 按新增資料夾。文件命名「01-三點摘要-你的名字」。
7. 關閉文件，再從該資料夾重開，確認文字還在。這才是本節保存成功的訊號。
8. 找不到新對話時，先回到左側選單；送出失敗時保留原文，檢查登入或限額，再重試一次。
個人對話的資料使用取決於帳號與設定；不要把付費等同於預設不訓練。練習只使用課程虛構資料。
''')
put('email-delay-facts.md','''# 延期回覆的核對資料（虛構）
已知：客戶林小姐；原交期10月16日；檢驗發現零件問題；團隊正在更換零件；訂單編號A102。
待確認：新交期、已完成比例、運費、補償、下次進度更新時間。
未核准：折扣、免運、任何賠償。

## 錯誤草稿
林小姐您好，A102已完成60%，一定會在10月20日交付。我們將補償運費，明天會更新進度。

## 核對結果
「60%」「10月20日」「補償運費」「明天更新」都沒有來源，不能寄出。

## 中性正式版
林小姐您好：關於訂單A102，原訂10月16日交付。檢驗發現零件問題，團隊目前正在更換零件，因此原交期需要調整。新的交付日期仍待確認。造成不便，敬請見諒。敬祝順心。

## 較親切版
林小姐您好，想向您說明A102的進度：檢驗時發現零件問題，我們正在更換，原訂10月16日的交期需要調整。新的日期目前還沒確認。很抱歉讓您等候。

## 內部回報版
A102：原交期10月16日，檢驗發現零件問題，目前更換中；新交期待確認。請先確認新日期，以及是否有核准的補救方案，再補齊對外回覆。
三版事實一致；最後一版把「尚缺什麼」交給內部決策者處理。
''')
lines=['決議：活動日期為10月24日。','決議：海報由小林負責，10月12日前完成。','建議：活動報名上限可設為30人，尚未通過。','建議：用線上表單收集回饋，尚未通過。','待確認：印刷費上限 NT$1,500，不是15,000。','待確認：誰負責場地聯絡？尚未指定。']
put('mock-whiteboard-text.txt','\n'.join(lines))
segments=[('Eddy (中文（台灣）)','主持人：今天討論的是十月二十四日的活動。日期已經確定，其他事項我們逐項確認。這份錄音是課程的虛構會議，請把決議、建議和待確認事項分開。'),('Flo (中文（台灣）)','小林：我負責海報，十月十二日前交第一版。海報先保留報名方式的欄位，等表單網址確認後再補上。這個期限和負責人已經確認，可以列入待辦。'),('Eddy (中文（台灣）)','主持人：好的，海報的安排通過。我提議報名上限三十人，但是還要看場地能容納多少人。今天先不要把三十人寫成已經確定的限制。'),('Grandma (中文（台灣）)','小周：我建議用線上表單收回饋。大家今天還沒有決定用哪一種工具，也沒有指定誰來做表單，所以這一項先列為建議。'),('Eddy (中文（台灣）)','主持人：印刷費的預算上限是一千五百元，不是一萬五千元。不過報價还沒有拿到，這項費用是否足夠，需要再確認。請記錄金額時保留待確認的狀態。'),('Flo (中文（台灣）)','小林：如果要做場地聯絡，請問是我還是小周負責？我這週要先完成海報，能不能下次再指定？目前也沒有確認場地聯絡的截止日期。'),('Grandma (中文（台灣）)','小周：我也還不能確認能不能接這項工作。紀錄可以先寫負責人待確認，期限待確認。不要為了讓表格完整就填成我的名字。'),('Eddy (中文（台灣）)','主持人：同意。今天已確認兩件事：活動日期十月二十四日，海報由小林在十月十二日前完成。報名上限和回饋表單是建議，印刷費與場地聯絡要再確認。會議到這裡結束。')]
put('mock-meeting-transcript.txt','課程合成語音；三位虛構發言者。\n\n'+'\n\n'.join(x[1] for x in segments));(p/'audio-segments.json').write_text(json.dumps(segments,ensure_ascii=False))
projects={
'mock-project-v1': [('星河活動案｜v1｜2026-10-01','活動10月24日。海報第一版10月12日。\n報名上限30人已核准。'),('分工與費用','海報：小林。場地聯絡：小周，10月15日前完成。\n印刷費核准上限1500元。'),('交付及未知事項','交付：海報PDF與報名表連結。\n活動後三日整理回饋。供應商名稱尚未決定。')],
'mock-project-v2': [('星河活動案｜v2｜2026-10-08','本版取代v1的時程與人數條件。活動改為10月31日。\n海報第一版改為10月19日。報名上限24人已核准。'),('分工與費用','海報：小林。場地聯絡：小周，改為10月22日前完成。\n印刷費核准上限1800元。'),('交付及未知事項','交付：海報PDF與報名表連結。\n活動後五日整理回饋。供應商名稱尚未決定。')],
'mock-project-solo': [('海岸工作坊｜v1｜2026-10-09','這是另一個專案，不沿用星河案。活動11月7日。\n海報第一版10月28日。報名上限18人。'),('分工與衝突條款','海報：小安。場地聯絡：小陳，10月30日前完成。\n本頁印刷費上限2200元；附件報價單寫2500元，尚未覆核。'),('交付及未知事項','交付：海報PDF及報到名單。\n活動後七日整理回饋。供應商名稱未定。\n費用有衝突，須詢問承辦人，不能自行選一個。')]}
(p/'pdf-content.json').write_text(json.dumps(projects,ensure_ascii=False))
put('reference-extractions.md','''# 萃取參考答案（依原始素材人工整理）
## 白板
決議：10月24日辦活動；小林10月12日前完成海報。
建議：30人上限；線上回饋表。兩項都尚未通過。
待確認：印刷費上限NT$1,500是否足夠；場地聯絡負責人。
容易誤讀：1,500與15,000差十倍，須放大原圖核對，不能只信摘要。
## 合成會議
決議與建議同白板。海報待辦：小林／10月12日／第一版，表單網址待補。
場地聯絡：負責人待確認，期限待確認。回饋表單：未通過，無負責人。
印刷費預算上限1,500元；是否足夠待報價。不得把1,500寫成已支出。
## PDF v1與v2
v1：10月24日活動（p1）；10月12日海報（p1）；印刷1500元（p2）。
v2：10月31日活動（p1）；10月19日海報（p1）；印刷1800元（p2）。
兩版供應商都尚未決定（p3），來源不能回答供應商姓名。
Solo：11月7日（p1）；小安海報（p2）；印刷2200／2500衝突（p2），先追問承辦。
參考答案可用來核對；不是平台實跑輸出截圖。
''')
put('quote-rules.md','''# 虛構報價規則
月費：基礎30000、進階60000、客製100000。期間只能3、6、12月。基礎折扣0–30%。
計算：月費×月數×(1−折扣)；年付限12月，另乘0.97。若選含稅，再乘1.05。
最終稅前與含稅總額四捨五入為整元。月付期數=月數，季付期數=月數÷3，年付一期。
前面每期取總額÷期數的整數下界；最後一期補尾差，各期合計須等於總額。
空值、負月費、錯誤期間、折扣超範圍不計算；不產生有效報價。
案例與答案在quote-test-cases.csv；這不是公司政策或稅務建議。
''')
put('quote-test-cases.csv','''case,fee,months,discount,payment,tax,net,total,installments,expected
Q01,30000,3,0,quarter,true,90000,94500,94500,valid
Q02,30000,6,0,quarter,true,180000,189000,94500|94500,valid
Q03,30000,12,0,quarter,true,360000,378000,94500|94500|94500|94500,valid
Q04,30000,12,15,year,true,296820,311661,311661,valid
Q05,30000,3,0,year,true,,,,invalid_year
Q06,-1,12,0,month,true,,,,invalid_fee
Q07,30000,,0,month,true,,,,missing_months
Q08,30000,12,31,month,true,,,,invalid_discount
Q09,30000,12,17.3,quarter,true,297720,312606,78151|78151|78151|78153,valid
''')
rows=[]
for i in range(24):
 year=2024+(i+4)//12;month=(i+4)%12+1
 revenue=120000+i*4500+(i%4)*1200;orders=60+i*2+(i%3)
 rows.append({'month':f'{year}-{month:02}','revenue':revenue,'orders':orders})
with (p/'sales-24-months.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['month','revenue','orders']);w.writeheader();w.writerows(rows)
total=sum(x['revenue'] for x in rows);orders=sum(x['orders'] for x in rows)
put('sales-expected-results.md',f'''# 固定資料核對答案
24列，2024-05至2026-04；虛構營收與訂單。營收總額{total:,}元；訂單{orders:,}筆；加權客單價=總營收÷總訂單={total/orders:.2f}元。
2025-05年增率=({rows[12]['revenue']}÷{rows[0]['revenue']}−1)×100={100*(rows[12]['revenue']/rows[0]['revenue']-1):.2f}%。
2026-04年增率=({rows[23]['revenue']}÷{rows[11]['revenue']}−1)×100={100*(rows[23]['revenue']/rows[11]['revenue']-1):.2f}%。
只保留後12月時，沒有前一年同月營收，年增率應顯示「缺前一年資料」。訂單0時客單價顯示「無法計算」。
這份數值沒有促銷、廣告或季節的成因資料；只能描述变化，不能斷言成因。
''')
put('part5-sheet-layout.md','''# 三张輸入與紀錄表
同一試算表建立Source、ReviewedQueue、ProcessingLog、Drafts。
Source與ReviewedQueue第一列表頭固定九欄：submitted_at,name,email,subject,message,category,summary,next_action,review_status。
Source保存原文；AI建議由人覆核。ReviewedQueue只追加已覆核完整新列，中途不可空白；更新Source舊列不觸發Watch New Rows。
ProcessingLog：source_key,category,route,status,draft_status,error。Drafts：source_key,recipient,subject,body,status；recipient僅測試本人，status=未寄出。
去重鍵= submitted_at + | + 小寫email + | + 去空白subject。一次處理一列，非並行防重保證。
'''.replace('三张','輸入與').replace('##','##'))
put('part5-input-contract.md','''# 九欄資料規格（全Part5共同）
submitted_at：原始提交時間文字；name：虛構姓名；email：有效格式的測試郵件；subject：主旨；message：原文。
category：inquiry／complaint／partnership／other之一；summary：不新增事實的一句摘要；next_action：待人工確認的下一步；review_status：待覆核／已覆核。
九欄均不可空白。只有已覆核且分類有效才進分流。未知資料不由AI猜成已知；有問題保留Source列並停止入列。
提交時間、email與主旨組成來源鍵；重試不改來源鍵。分類用英文固定值，覆核用中文固定值。
未覆核不進ReviewedQueue；人工覆核後追加完整新列，才供Make Watch New Rows讀取。
''')
put('part5-reviewed-queue.csv','''submitted_at,name,email,subject,message,category,summary,next_action,review_status
2026-10-09T09:00,小林,learner@example.com,詢問方案,請問基礎方案月費,inquiry,詢問基礎方案,建立給本人測試草稿,已覆核
2026-10-09T09:05,小安,learner@example.com,交期問題,商品未準時交付,complaint,反映交期,人工客服覆核,已覆核
2026-10-09T09:10,小周,learner@example.com,合作邀約,想討論共同活動,partnership,詢問合作,建立給本人測試草稿,已覆核
2026-10-09T09:15,小陳,learner@example.com,一般訊息,謝謝教材,other,致謝,記錄待處理,已覆核
''')
put('part5-test-cases.csv','''case,input,expected_route,expected_draft,expected_check
T01,inquiry且已覆核,業務,一份未寄出,來源鍵與分類正確
T02,complaint且已覆核,客服,零份,人工處理標記
T03,partnership且已覆核,合作,一份未寄出,僅測試本人
T04,other且已覆核,待處理,零份,紀錄存在
T05,待覆核或無效分類,阻擋,零份,沒有分流
T06,相同來源鍵第二次加入,重複,不新增,紀錄與草稿不重複
T07,斷開寫入連線後恢復,原分類,最多一份有效草稿,保留錯誤並從失敗步驟重跑
''')
put('part5-rebuild-guide.md','''# Make 人工重建指南（開課前須工作區實跑）
## 先建立沒有AI的最小流程
1. Google Sheets建立表，依part5-sheet-layout.md加表頭。先把T01放ReviewedQueue第一筆資料列。
2. Make新增Scenario；第一模組選Google Sheets > Watch New Rows。建立Google連線，指定Spreadsheet與ReviewedQueue；表有標題，標題列1；Limit設1。首次Choose where to start選All以讀既有測試列；正式練習再改從現在開始，避免重讀舊資料。
3. 加Google Sheets > Add a Row，選ProcessingLog，把來源欄位映射到紀錄；先Run once確認能讀一列、寫一列。無輸出先查表名、起點及中途空列，不先加AI。
## 加覆核、防重與分流
4. 觸發後Filter：review_status等於已覆核；九欄非空；email有效；category屬四個固定值。未通過要在Run once查看被擋bundle，保存原因。
5. 組source_key，Search Rows查ProcessingLog的source_key。設定零結果也可繼續，再Filter只讓未存在鍵進Router；已有鍵走重複紀錄支路。此設定需在實際帳號確認，沒有零結果輸出不可假設通過。
6. Router四路：category等於inquiry／complaint／partnership／other。每路Add a Row寫ProcessingLog，status=已記錄，draft_status=不需要或待建立。
7. inquiry／partnership路再Add a Row到Drafts，只寫測試本人與未寄出內容，不用寄信模組。完成後Update a Row把同一紀錄draft_status改為已建立。客服與other只記錄。
## 測試與恢復
8. 依T01–T07一次追加一列；每次Run once，查看bundle、ProcessingLog、Drafts三處並記錄截圖或執行ID。
9. T06檢查不新增草稿；T07只對教學表撤回寫入連線或改成無權限的測試表，再恢復原連線。不要刪除Source。紀錄已成功而草稿失敗時，從草稿步驟恢復，並先查同source_key的Drafts是否已存在。
10. 在錯誤模組啟用保存未完成執行的設定；失敗暫停排程，記error及draft_status。重新連線後再恢復失敗執行，逐一確認只有一份有效結果，才能重新開排程。
11. 每次操作需核對當日UI與方案是否支援。沒有連線／錯誤恢復證據時，狀態仍為尚未實跑。
此檔是完整重建候選路徑，不是已通過的Blueprint；只有工作區跑通後才可匯出真正Blueprint。
官方模組：https://apps.make.com/google-sheets-modules
''')
put('tool-card-template.md','''# 七欄工具卡
名稱：
何時用：
輸入：
輸出：
怎麼檢查：
失敗時重做哪一步：
成果位置／狀態：
範例：三點摘要／週報整理／五行已確認資料／三點摘要／逐點對照日期與數字／回原文補資料後重做摘要／本機AI課程練習資料夾，已核對。
''')
print('Created text assets and fixed datasets')
