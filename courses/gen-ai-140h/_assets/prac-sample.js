// 範本 Prompt 複製按鈕 — 共用於 140h 課程所有 CH*.html
// 支援兩種 DOM 結構：button 在 .ps-prompt 內（主流）或作為 sibling（CH1-2/-3 pilot 版）
document.addEventListener('click',function(e){
  var btn=e.target.closest('.copy-btn');
  if(!btn)return;
  var prompt=btn.parentElement;
  if(!prompt||!prompt.classList.contains('ps-prompt')){
    prompt=btn.previousElementSibling;
  }
  if(!prompt||!prompt.classList.contains('ps-prompt'))return;
  var text=prompt.textContent.replace(/複製\s*$/,'').trim();
  var done=function(){
    var original=btn.textContent;
    btn.textContent='已複製';
    btn.classList.add('copied');
    btn.setAttribute('aria-label','已複製到剪貼簿');
    setTimeout(function(){btn.textContent=original;btn.classList.remove('copied');btn.setAttribute('aria-label','複製此範例 Prompt 到剪貼簿');},1800);
  };
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(done).catch(function(){
      var ta=document.createElement('textarea');ta.value=text;document.body.appendChild(ta);ta.select();
      try{document.execCommand('copy');done();}catch(err){}finally{document.body.removeChild(ta);}
    });
  }else{
    var ta=document.createElement('textarea');ta.value=text;document.body.appendChild(ta);ta.select();
    try{document.execCommand('copy');done();}catch(err){}finally{document.body.removeChild(ta);}
  }
});
