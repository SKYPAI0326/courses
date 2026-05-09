# scale-up · 大規模演練素材（v1.2）

當你跑完小量教學版、想看「批次自動化省時感」時，把這裡的檔搬進對應 inbox：

| 子資料夾 | 對應 workflow | 量級 | 預期效益 |
|---|---|---|---|
| `pdf-inbox-12/` | #02 PDF AI 改名 | 12 PDF | 學員手動改 12 個檔需 5-8 分鐘；workflow 約 80 秒（含 throttle） |
| `batch-inbox-30/` | #03 批次錯誤恢復 | 30 檔含 7 邊界 | 看清楚 success/failure 分流規模 |
| `client-inbox-40/` | #10 客戶資料夾整理 | 40 mixed | 看 chunk batch + 6 類分流 + index report 完整效益 |
| `leads-inbox-100/` | #11 CSV 線索清洗 | 100+5dup | 看 normalize + dedupe + AI 評分批次價值（注意 RPM）|
| `ops-input-200/` | #13 ops 快照 | 200 行 metrics | 看異常 spike 偵測 + AI 分析 |

## ⚠ Gemini Free tier 限制提醒

跑大規模時注意：
- **Free tier 上限**：10 RPM / 250 RPD / 250K TPM（[官方](https://ai.google.dev/gemini-api/docs/rate-limits)）
- **#02 跑 12 個 PDF**：v1.2 已加 throttle（每筆 sleep 6.5 秒），約 80 秒跑完，安全
- **#03 跑 30 個檔**：throttle 後約 200 秒，會分到下一分鐘 RPM window
- **#11 跑 100 行**：是「1 次 batch prompt」設計，1 次 API call，安全
- **#13 跑 200 行**：是「aggregate 後 1 次 prompt」，安全

如果撞 429：v1.2 已加 60 秒自動 retry × 3，看 workflow log 出現 `retry on 429` 是正常的，等就好。

## 使用流程

```bash
# Mac
cp scale-up/pdf-inbox-12/* ~/Downloads/n8n-starter-kit/shared/pdf-inbox/

# Windows（PowerShell）
Copy-Item scale-up\pdf-inbox-12\* C:\Users\<you>\Downloads\n8n-starter-kit\shared\pdf-inbox\
```

跑完想還原小量教學版：把對應 inbox 清空，從原 `n8n-sample-pack/<inbox>/` 重新複製。
