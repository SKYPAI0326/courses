# 完成品檢查

完成後應有兩個同層 Frame：

- `Screen / Host`：402×874，作為 Flow 起點。
- `Dialog / Overlay`：320×200，內含文字 `確認完成`。

Prototype 面板應顯示：

```text
On click → Open overlay → Dialog / Overlay
```

在 Present 預覽點擊 Host 後，畫面中應看到 `確認完成`。若畫面仍是空白，先檢查是否已把文字放在 `Dialog / Overlay` 的子層，而不是畫布外的獨立文字。

## Swap

- [ ] `SWAP-01` 有來源、目的地、狀態差異與 Preview Expected／Actual。
- [ ] 沒有可用的 Swap action 時標為 `NOT_RUN`，並保留面板截圖。
