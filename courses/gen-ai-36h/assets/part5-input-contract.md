# 九欄資料規格（全Part5共同）
submitted_at：原始提交時間文字；name：虛構姓名；email：有效格式的測試郵件；subject：主旨；message：原文。
category：inquiry／complaint／partnership／other之一；summary：不新增事實的一句摘要；next_action：待人工確認的下一步；review_status：待覆核／已覆核。
九欄均不可空白。只有已覆核且分類有效才進分流。未知資料不由AI猜成已知；有問題保留Source列並停止入列。
提交時間、email與主旨組成來源鍵；重試不改來源鍵。分類用英文固定值，覆核用中文固定值。
未覆核不進ReviewedQueue；人工覆核後追加完整新列，才供Make Watch New Rows讀取。
