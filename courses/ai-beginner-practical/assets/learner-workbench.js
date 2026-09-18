(function(){
  const form=document.querySelector('[data-workbench-form]');
  if(!form)return;
  const key=form.dataset.workbenchKey;
  const filename=form.dataset.exportFilename||'learner-workbench.md';
  const title=form.dataset.exportTitle||'學員工作台紀錄';
  const status=form.querySelector('[data-workbench-status]');
  const label=form.querySelector('[data-workbench-progress-label]');
  const bar=form.querySelector('[data-workbench-progress-fill]');
  const fields=Array.from(form.querySelectorAll('[data-field]'));
  let saveTimer;
  const get=name=>{const el=form.querySelector('[data-field="'+name+'"]');if(!el)return'';return el.type==='checkbox'?(el.checked?'已勾選':'未勾選'):(el.value||'').trim()};
  const raw=name=>{const el=form.querySelector('[data-field="'+name+'"]');if(!el)return'';return el.type==='checkbox'?el.checked:(el.value||'')};
  const setStatus=message=>{if(status)status.textContent=message};
  function updateProgress(){
    const required=fields.filter(el=>el.dataset.required==='true');
    const done=required.filter(el=>el.type==='checkbox'?el.checked:el.value.trim()!=='').length;
    const pct=required.length?Math.round(done/required.length*100):0;
    if(label)label.textContent='完成進度 '+pct+'%（'+done+'/'+required.length+'）';
    if(bar)bar.style.width=pct+'%';
  }
  function snapshot(){const data={};fields.forEach(el=>{data[el.dataset.field]=el.type==='checkbox'?el.checked:el.value});return data}
  function save(message){try{localStorage.setItem(key,JSON.stringify(snapshot()));setStatus(message||'已暫存於目前瀏覽器（非雲端）')}catch(e){setStatus('目前瀏覽器不能暫存，請按「匯出 Markdown」留存。')}updateProgress()}
  function restore(){try{const saved=JSON.parse(localStorage.getItem(key)||'null');if(saved){fields.forEach(el=>{if(!(el.dataset.field in saved))return;if(el.type==='checkbox')el.checked=Boolean(saved[el.dataset.field]);else el.value=saved[el.dataset.field]||''});setStatus('已恢復上次填寫內容（只存在目前瀏覽器）')}}catch(e){setStatus('目前瀏覽器不能暫存，請完成一段就匯出。')}updateProgress()}
  function copyPrompt(target,button){const node=document.getElementById(target);const text=node?node.textContent.trim():'';const done=()=>{setStatus('提示詞已複製，請貼到你的工具。');if(button){const old=button.textContent;button.textContent='已複製';setTimeout(()=>button.textContent=old,1200)}};if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done).catch(()=>fallback())}else fallback();function fallback(){const temp=document.createElement('textarea');temp.value=text;document.body.appendChild(temp);temp.select();try{document.execCommand('copy');done()}catch(e){setStatus('請手動選取提示詞複製。')}temp.remove()}}
  function exportMarkdown(){
    const md=['# '+title,'','> 這份檔案由頁內工作台匯出；原始輸入、回答與判斷請一併保留。'];
    form.querySelectorAll('.wb-panel').forEach(panel=>{
      const heading=panel.querySelector('h3');
      if(heading)md.push('','## '+heading.textContent.trim());
      panel.querySelectorAll('[data-field]').forEach(el=>{const field=el.closest('.wb-field')||el.closest('.wb-check');const fieldLabel=field&&field.querySelector('label,span')?field.querySelector('label,span').textContent.trim():el.dataset.field;md.push('', '**'+fieldLabel+'**', el.type==='checkbox'?'['+(raw(el.dataset.field)?'x':' ')+']':(get(el.dataset.field)||'（未填）'))});
    });
    md.push('','匯出時間：'+new Date().toLocaleString('zh-TW'));
    const blob=new Blob([md.join('\n')],{type:'text/markdown;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=filename;document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(url);setStatus('已匯出 '+filename+'；請另外保存檔案。');
  }
  fields.forEach(el=>{el.addEventListener('input',()=>{updateProgress();clearTimeout(saveTimer);saveTimer=setTimeout(()=>save(),450)});el.addEventListener('change',()=>{updateProgress();save()})});
  form.querySelectorAll('[data-copy-target]').forEach(button=>button.addEventListener('click',()=>copyPrompt(button.dataset.copyTarget,button)));
  const action=name=>form.querySelector('[data-action="'+name+'"]');
  if(action('save'))action('save').addEventListener('click',()=>save('已儲存到目前瀏覽器（非雲端）'));
  if(action('export'))action('export').addEventListener('click',exportMarkdown);
  if(action('print'))action('print').addEventListener('click',()=>window.print());
  if(action('reset'))action('reset').addEventListener('click',()=>{if(!window.confirm('確定清除目前瀏覽器中的工作台內容？已匯出的檔案不會受影響。'))return;form.reset();try{localStorage.removeItem(key)}catch(e){}setStatus('已清除本機填寫內容');updateProgress()});
  restore();
})();
