"""文案v0.6的讀者重述與理解障礙檢查；不以程式假裝判定語意。"""
import copy
from pathlib import Path

from src.course_improvement_loop import require


READABILITY_INSTRUCTIONS = """落實四項讀者檢查，不只評論自然流暢：
1. plain_restatement：不用原文的抽象製作術語，用讀者日常說法重述主要段落的意思及理由。有情境或案例時，檢查讀者能否說出誰要完成什麼、遇到什麼問題、目前缺什麼，以及下一步由誰做、為什麼；概念或推導內容可從現象或待解問題進場，不虛構工作故事。support_quotes逐字引用目前正文中支持重述的依據；不能引用其他來源替正文補背景。重述若必須猜人物、材料、原因或條件，把那些猜測寫入added_background並記閱讀缺口，不能當成原文已說清楚。
2. referents：先找理解障礙，說明原文中的人、材料、行為、條件是否可辨認；先用日常語言建立角色和工作問題，再介紹檔名、訊息編號或縮寫作查找依據，不能讓它們代替故事。專有名稱可以保留，不能只用較口語同義詞替換。先讀全文上下文，已交代的名稱不用反覆定義。
3. reason_placement：操作或判斷需要的理由，是否在讀者需要的位置已出現。核心範例應展示完整判斷：來源說了什麼、白話意思、支持或不支持什麼、為何保留或省略、接著問誰，最後寫成什麼成品。比喻只在能解釋抽象關係且不模糊事實時使用，不要求每課都加。清楚的簡單操作不必每步補理由，必要術語不能代替解釋。
4. reading_load：連讀時是否同時塞入過多日期、代碼、條件、例外或重複解釋，迫使讀者自行拆解；指出實際負擔與適合的段落／清單安排。清楚不等於縮短：刪除重複說明和無助理解的標籤，保留必要理由、來源、條件與未知。避免在交辦清單前後堆引言、摘要或轉場。依理解順序安排內容，但這是作者檢查工具，不是固定標題或每課必套的故事模板。清單適合步驟就保留，不以口語、字數短或條列少當通過依據。
每個passage都交上述四項實際結果。后三項各含verdict=supported或gap與具體explanation，不為湊問題而判gap。任何added_background或gap都須反映在remaining_gap及open B問題，整篇不得supported或B L3。若原文已清楚，明確說明支撐，不刻意找碴。選真正承載教學的完整段落，不挑一句轉場；從頭讀完再選證據。只依文字的判斷不能宣稱真人學員已理解，需以真人試走另行確認。"""


READABILITY_INSTRUCTIONS += "\n評估範圍以本章用途與既有案例為準。列到某類工作不代表本章必須逐類新增完整示範；先檢查既有解釋與案例是否已足夠理解。若建議需要新素材、新案例或新增教學目標，標明超出文案範圍並回交，不把未教授其他章內容直接判成本章B缺口。"


def readability_fields(obj):
    string = {"type": "string"}
    dimension = obj({"verdict": {"type": "string", "enum": ["supported", "gap"]}, "explanation": string})
    return {"plain_restatement": string,
            "support_quotes": {"type": "array", "items": string, "minItems": 1},
            "added_background": string,
            **{key: dimension for key in ("referents", "reason_placement", "reading_load")}}


def validate_readability(task, response):
    """核對四項都有實際依據且結論一致，再交既有B缺口檢查。"""
    result = copy.deepcopy(response)
    decision = result.get("reading_decision")
    require(isinstance(decision, dict) and isinstance(decision.get("passages"), list)
            and decision["passages"], "v0.6缺少四項讀者檢查")
    candidate = Path(task["target"]["path"]).read_text(encoding="utf-8")
    extra = set(readability_fields(lambda x: x))
    base = {"quote", "reader_understanding", "remaining_gap", "problem_id"}
    for row in decision["passages"]:
        require(isinstance(row, dict) and set(row) == base | extra, "v0.6閱讀段落缺少四項檢查欄位")
        require(isinstance(row["plain_restatement"], str) and row["plain_restatement"].strip(), "須用讀者的話重述意思")
        quotes = row["support_quotes"]
        require(isinstance(quotes, list) and quotes and all(isinstance(q, str) and q.strip() and q in candidate for q in quotes),
                "重述依據須逐字出自目前正文，不可補入其他來源")
        require(isinstance(row["added_background"], str), "須明示重述是否補入背景；沒有則留空")
        gap = bool(row["added_background"].strip())
        for key in ("referents", "reason_placement", "reading_load"):
            item = row[key]
            require(isinstance(item, dict) and set(item) == {"verdict", "explanation"}
                    and item["verdict"] in ("supported", "gap")
                    and isinstance(item["explanation"], str) and item["explanation"].strip(), "四項檢查須有具體判斷")
            gap = gap or item["verdict"] == "gap"
        require(not gap or (isinstance(row["remaining_gap"], str) and row["remaining_gap"].strip()),
                "重述補背景或四項有缺口，不得省略remaining_gap")
        for key in extra:
            row.pop(key)
    return result
