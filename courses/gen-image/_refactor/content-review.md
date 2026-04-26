# Content Review

詳見 `_refactor/codex-review-report.md` 的「內容問題」與「設計系統 lint」章節。

摘要：

- BLOCKER：`_refactor/codex-image-requests.md` 補圖數量與優先級互相矛盾。
- WARN：台北咖啡案例使用日圓與日文設定未交代、平台價格配額資訊時效性高、保健品訴求需法規保守語、PRAC3 時間盒偏緊、callout / details 過量。
- NIT：`Step N` 與「步驟 N」混用、部分時間描述像保證、平台品牌名密度偏高、固定日期日後易過期。

lint：

```bash
python3 ../../docs/lint-page.py courses/gen-image
```

結果：BLOCKER 0、ERROR 0、WARN 55。
