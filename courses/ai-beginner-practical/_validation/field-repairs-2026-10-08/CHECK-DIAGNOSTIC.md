# 標題保護斷言校正
原備份h1含自閉br，BeautifulSoup快照將其序列成br內含後半句及結束br；初次保護比對直接用<br/>字串換空格無法命中。已查看before/after真diff，確認實際h1仍完整「第一次用 LLM 完成工作任務」，殼層其他部分不變。斷言改用記錄的before／after精準映射及正文文字相等，沒有放寬其他殼層。單次標題syntax修復後lint 0BLOCKER；此為測試parser快照表示法，不是新增頁面修補。

進一步定位：唯一未授權DOM快照差異在原天氣選做例br序列（原檔實際位元組不變），由最前h1 void-br修正改變BeautifulSoup全頁序列化狀態造成。已停止頁面修補，改用HTMLParser明確節點起止位置比較允許區外的原始位元組；保留完整其他區內容，沒有忽略差異或改舊例。
