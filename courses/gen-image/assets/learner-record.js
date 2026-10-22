(function () {
  'use strict';

  var fields = Array.prototype.slice.call(document.querySelectorAll('[contenteditable="true"]'));
  var controls = document.querySelectorAll('[data-learner-record-controls]');
  if (!fields.length || !controls.length) return;

  var pageId = location.pathname.split('/').pop() || 'lesson';
  var keyPrefix = 'learner-record:' + location.pathname + ':';

  function setStatus(message) {
    Array.prototype.forEach.call(document.querySelectorAll('[data-record-status]'), function (node) {
      node.textContent = message;
    });
  }

  function labelFor(field, index) {
    var row = field.closest('tr');
    var header = row && row.querySelector('th');
    return header ? header.textContent.trim() : '欄位 ' + (index + 1);
  }

  function readRecord() {
    return {
      unit: document.querySelector('h1') ? document.querySelector('h1').textContent.trim() : document.title,
      page: pageId,
      exported_at: new Date().toISOString(),
      fields: fields.map(function (field, index) {
        return { label: labelFor(field, index), value: field.textContent.trim() };
      })
    };
  }

  function jsonText() {
    return JSON.stringify(readRecord(), null, 2);
  }

  fields.forEach(function (field, index) {
    var key = keyPrefix + index;
    try {
      var saved = localStorage.getItem(key);
      if (saved !== null) field.textContent = saved;
    } catch (error) {
      setStatus('此瀏覽器無法使用本機儲存，請下載或複製紀錄。');
    }
    field.addEventListener('input', function () {
      try {
        localStorage.setItem(key, field.textContent);
        setStatus('已儲存在此瀏覽器。');
      } catch (error) {
        setStatus('無法自動儲存，請下載或複製紀錄。');
      }
    });
  });

  Array.prototype.forEach.call(document.querySelectorAll('[data-record-copy]'), function (button) {
    button.addEventListener('click', function () {
      var text = jsonText();
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          setStatus('已複製 JSON 紀錄。');
        }, function () {
          setStatus('複製失敗，請改用下載。');
        });
        return;
      }
      var area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      var copied = document.execCommand('copy');
      area.remove();
      setStatus(copied ? '已複製 JSON 紀錄。' : '複製失敗，請改用下載。');
    });
  });

  Array.prototype.forEach.call(document.querySelectorAll('[data-record-download]'), function (button) {
    button.addEventListener('click', function () {
      var blob = new Blob([jsonText()], { type: 'application/json;charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var link = document.createElement('a');
      link.href = url;
      link.download = pageId.replace(/\.html$/i, '') + '-learner-record.json';
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
      setStatus('已下載 JSON 紀錄；可帶到其他裝置或交件。');
    });
  });

  var style = document.createElement('style');
  style.textContent = '.record-actions{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:12px 0 4px}.record-actions button{border:1px solid var(--c-border,#c9c5bc);border-radius:999px;background:var(--c-card,#fff);color:var(--c-text,#222);padding:8px 14px;font:inherit;font-size:.86rem;cursor:pointer}.record-actions button:hover,.record-actions button:focus-visible{border-color:var(--c-text,#222);outline:none}.record-status{flex-basis:100%;font-size:.8rem;color:var(--c-muted,#666);margin:0}';
  document.head.appendChild(style);
})();
