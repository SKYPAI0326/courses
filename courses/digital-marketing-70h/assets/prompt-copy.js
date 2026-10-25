(function(){
  'use strict';

  const BUTTON_LABEL='複製 Prompt';
  const SUCCESS_LABEL='已複製';
  const ERROR_LABEL='複製失敗';

  function getPromptText(target){
    let text=target.innerText.replace(/\r\n?/g,'\n').trimStart();
    const excluded=target.querySelectorAll(':scope > .dialog-label, :scope > .prompt-comment');
    excluded.forEach(function(node){
      const prefix=node.innerText.trim();
      const candidate=text.trimStart();
      if(prefix&&candidate.startsWith(prefix)) text=candidate.slice(prefix.length);
    });
    return text
      .split('\n')
      .map(function(line){return line.replace(/[ \t]+$/,'')})
      .join('\n')
      .replace(/\n{3,}/g,'\n\n')
      .trim();
  }

  function fallbackCopy(text){
    const field=document.createElement('textarea');
    field.value=text;
    field.setAttribute('readonly','');
    field.style.position='fixed';
    field.style.inset='0 auto auto -9999px';
    document.body.appendChild(field);
    field.select();
    field.setSelectionRange(0,field.value.length);
    const copied=document.execCommand('copy');
    field.remove();
    if(!copied) throw new Error('copy command failed');
  }

  async function copyText(text){
    if(navigator.clipboard&&window.isSecureContext){
      await navigator.clipboard.writeText(text);
      return;
    }
    fallbackCopy(text);
  }

  function setButtonState(button,status,label,state){
    window.clearTimeout(button._promptCopyTimer);
    button.textContent=label;
    button.classList.toggle('is-copied',state==='copied');
    button.classList.toggle('is-error',state==='error');
    status.textContent=state==='copied'?'Prompt 已複製到剪貼簿':'Prompt 複製失敗，請重新選取內容';
    button._promptCopyTimer=window.setTimeout(function(){
      button.textContent=BUTTON_LABEL;
      button.classList.remove('is-copied','is-error');
      status.textContent='';
    },1800);
  }

  function enhance(target,index){
    if(target.dataset.copyPromptReady==='true') return;
    target.dataset.copyPromptReady='true';

    if(target.firstChild&&target.firstChild.nodeType===Node.TEXT_NODE&&!target.firstChild.textContent.trim()){
      target.firstChild.remove();
    }

    const toolbar=document.createElement('div');
    toolbar.className='prompt-copy-toolbar';

    const button=document.createElement('button');
    button.type='button';
    button.className='prompt-copy-button';
    button.textContent=BUTTON_LABEL;
    button.setAttribute('aria-label','複製這段 Prompt');

    const status=document.createElement('span');
    status.className='prompt-copy-status';
    status.id='prompt-copy-status-'+index;
    status.setAttribute('role','status');
    status.setAttribute('aria-live','polite');
    button.setAttribute('aria-describedby',status.id);

    button.addEventListener('click',async function(){
      const text=getPromptText(target);
      if(!text){
        setButtonState(button,status,ERROR_LABEL,'error');
        return;
      }
      try{
        await copyText(text);
        setButtonState(button,status,SUCCESS_LABEL,'copied');
      }catch(error){
        setButtonState(button,status,ERROR_LABEL,'error');
      }
    });

    toolbar.append(button,status);
    target.before(toolbar);
  }

  function init(){
    document.querySelectorAll('[data-copy-prompt]').forEach(enhance);
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',init,{once:true});
  }else{
    init();
  }
})();
