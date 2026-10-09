(() => {
  const root = document.querySelector('[data-record-key]');
  if (!root || !root.dataset.recordKey) return;
  const key = 'uiux-record-' + root.dataset.recordKey;
  const fields = [...root.querySelectorAll('input[name],textarea[name]')];
  const status = document.querySelector('#save-status');
  const values = () => Object.fromEntries(fields.map(el => [el.name, el.type === 'checkbox' ? el.checked : el.value]));
  const apply = data => fields.forEach(el => {
    if (!(el.name in data)) return;
    if (el.type === 'checkbox') el.checked = data[el.name] === true;
    else el.value = String(data[el.name] ?? '');
  });
  try { const saved = JSON.parse(localStorage.getItem(key) || 'null'); if (saved) { apply(saved.values); status.textContent = '已載入本瀏覽器上次儲存的紀錄。'; } }
  catch { status.textContent = '瀏覽器儲存不可用；請下載JSON保留紀錄。'; }
  root.querySelector('[data-save]').addEventListener('click', () => {
    try { localStorage.setItem(key, JSON.stringify({key,values:values()})); status.textContent='已儲存到本瀏覽器。換電腦前請下載JSON。'; }
    catch { status.textContent='儲存失敗，請下載JSON保留。'; }
  });
  root.querySelector('[data-export]').addEventListener('click', () => {
    const file = new Blob([JSON.stringify({version:1,key,savedAt:new Date().toISOString(),values:values()},null,2)],{type:'application/json'});
    const url = URL.createObjectURL(file); const a = document.createElement('a');a.href=url;a.download=root.dataset.recordKey+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
    status.textContent='已啟動下載；請確認下載資料夾中的JSON檔。';
  });
  root.querySelector('[data-import]').addEventListener('change', async event => {
    const file = event.target.files[0]; if (!file) return;
    try { const data=JSON.parse(await file.text()); if(data.key!==key || typeof data.values!=='object' || data.values===null) throw new Error();apply(data.values);status.textContent='已載入JSON，請檢查後按儲存。'; }
    catch { status.textContent='載入失敗：請選本堂、同修訂版的紀錄JSON。'; }
  });
  root.querySelector('[data-print]').addEventListener('click',()=>window.print());
})();
