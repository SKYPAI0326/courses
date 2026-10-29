# 課程目錄共用入口

本檔適用於`courses/`及所有課程子目錄；子目錄的課程專屬規範仍須載入。

## 文案迭代

使用者說「文案迭代」時，無論目前在哪個課程目錄，都使用本目錄下`course-manager/`的共用功能。先讀[文案使用入口](course-manager/docs/course-copy-quickstart.md)、[現行規範v0.6](course-manager/docs/course-copy-profile-v0.6.md)及[控制器說明](course-manager/docs/course-loop-runtime.md)，套用course-copywriter的事實保留邊界。不要另建課程專屬文案流程，也不要求使用者切換目錄或指定版本。

- 從使用者指定路徑或目前所在課程目錄定位對象，依既有大綱／講義辨認學員與用途。只有對象、章節範圍或用途仍不明且會改變成果時，才詢問必要資訊；不把只有啟動詞自動視為整課改寫授權。
- 新run使用共用入口預設的v0.6；先找既有run，舊run保留原規範、雜湊及用量，不自動升級或重開。
- 使用`course-manager/scripts/course_copy_loop.py`準備，`course-manager/scripts/course_loop.py`接續。上述路徑均相對於本檔所在的`courses/`，不是目前工作目錄；實際命令用解析後的完整路徑，來源及run也用完整路徑，不必切換目錄。
- 沿用既有模型、單章兩版與八次low預設上限；整課須明列共用呼叫總額。未取得新的分工授權不另派代理。依四項讀者檢查修正與覆核，不用機械檢查或AI分數代替實際理解。
- 預設隔離候選；正式套用與發布依本次既有授權接續，不能代填H3。指定整課須列齊並追蹤全部章節，不把部分通過當整課完成。缺必要事實或需改操作時依現行規範回交，不虛構補齊。

有本機開發紀錄時讀取`course-manager/operations/course-content-scoring/開發進度追蹤.md`的相關狀態；來源、規範及控制器不可缺少，歷史試跑紀錄不作為其他課程已通過的證據。
