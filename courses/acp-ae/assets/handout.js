(function(){
  var fill=document.getElementById('prog');
  var strip=document.querySelector('.progress-strip');
  function updateProgress(){
    if(!fill||!strip)return;
    var h=document.documentElement;
    var available=h.scrollHeight-h.clientHeight;
    var pct=available>0?(h.scrollTop/available)*100:0;
    fill.style.width=pct+'%';
    strip.setAttribute('aria-valuenow',String(Math.round(pct)));
  }
  window.addEventListener('scroll',updateProgress,{passive:true});
  updateProgress();

  var storageKey='progress:'+location.pathname;
  var saved=parseInt(localStorage.getItem(storageKey)||'0',10);
  if(saved>0){window.addEventListener('load',function(){window.scrollTo(0,saved);});}
  var timer;
  window.addEventListener('scroll',function(){
    window.clearTimeout(timer);
    timer=window.setTimeout(function(){localStorage.setItem(storageKey,String(window.scrollY));},200);
  },{passive:true});

  var filter=document.querySelector('[data-filter]');
  var status=document.getElementById('filter-status');
  if(filter){
    filter.addEventListener('input',function(){
      var q=filter.value.trim().toLowerCase();
      var cards=Array.from(document.querySelectorAll('[data-search]'));
      var shown=0;
      cards.forEach(function(card){
        var hit=!q||(card.getAttribute('data-search')||'').toLowerCase().indexOf(q)!==-1;
        card.hidden=!hit;
        if(hit)shown+=1;
      });
      if(status)status.textContent=q?'找到 '+shown+' 個單元':'共 '+cards.length+' 個單元';
    });
  }
})();
