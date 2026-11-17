// 對比檢查器：定稿裡的 <figure data-kind="互動" data-value="對比檢查器"> 在執行時畫出這個元件。
// 計算與介面文字照搬第一章 L7-對比檢查.tpl 的 script，只改掛載點：在 figure 裡、figcaption 前面插入 .checker。
// 介面文字只在執行時出現，不進定稿正文，網頁比對才會一致。
(function(){
  function lum(hex){
    return [0,2,4].map(function(i){return parseInt(hex.substr(i,2),16)/255;})
      .map(function(v){return v<=0.04045? v/12.92 : Math.pow((v+0.055)/1.055,2.4);})
      .reduce(function(s,v,i){return s+v*[0.2126,0.7152,0.0722][i];},0);
  }
  function clean(s){ return s.trim().replace(/^#/,'').toUpperCase(); }
  function ok(h){ return /^[0-9A-F]{6}$/.test(h); }
  window.contrastRatio = function(a,b){
    var l1=lum(a), l2=lum(b), hi=Math.max(l1,l2), lo=Math.min(l1,l2);
    return (hi+0.05)/(lo+0.05);
  };
  document.querySelectorAll('figure[data-kind="互動"][data-value="對比檢查器"]').forEach(function(fig){
    var box=document.createElement('div');
    box.className='checker';
    fig.insertBefore(box, fig.querySelector('figcaption'));
    box.innerHTML =
      '<div class="row">'+
      '<label>文字色碼<input class="fg" maxlength="7" placeholder="例如 1E293B" autocomplete="off"></label>'+
      '<label>背景色碼<input class="bg" maxlength="7" placeholder="例如 FFFFFF" autocomplete="off"></label>'+
      '</div>'+
      '<div class="preview"><div class="p1">登入後檢視待處理的任務。</div><div class="p2">請輸入工作室帳號</div></div>'+
      '<div class="out">填好兩個色碼，這裡會顯示對比。</div>';
    var fg=box.querySelector('.fg'), bg=box.querySelector('.bg'), out=box.querySelector('.out'), pv=box.querySelector('.preview');
    function update(){
      var f=clean(fg.value), b=clean(bg.value);
      if(!f && !b){ out.innerHTML='填好兩個色碼，這裡會顯示對比。'; pv.style.color=''; pv.style.background=''; return; }
      if(!ok(f) || !ok(b)){ out.innerHTML='<span class="err">請輸入六位色碼（0～9、A～F），例如 1E293B。</span>'; return; }
      var r=window.contrastRatio(f,b), shown=Math.floor(r*100)/100;
      pv.style.color='#'+f; pv.style.background='#'+b;
      out.innerHTML='<span class="ratio">'+shown.toFixed(2)+':1</span>'+(r>=4.5?'<span class="pass">通過（至少 4.5）</span>':'<span class="fail">不通過（未達 4.5）</span>');
    }
    fg.addEventListener('input',update); bg.addEventListener('input',update);
  });
})();
