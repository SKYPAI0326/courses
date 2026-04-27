/* gen-ai-140h Interactivity v1
 * 對應 _報告/2026-04-27-互動性審核.md §4
 * 自動掛載：透過 DOMContentLoaded + querySelectorAll 自動 init 所有元件
 *
 * 各 init 函式由 Task 3-9 依序追加，每個 task 完成後在 DOMContentLoaded
 * dispatcher 內取消註解對應 init() 呼叫。
 */
(function () {
  'use strict';
  const LS_PREFIX = 'gen140_';
  const LS = {
    reflect:        LS_PREFIX + 'reflect_',         // gen140_reflect_{rk} → string
    artifact:       LS_PREFIX + 'artifact_',        // gen140_artifact_{ak} → JSON
    artifactIndex:  LS_PREFIX + 'artifact_index',   // gen140_artifact_index → JSON array
    peer:           LS_PREFIX + 'peer_',            // gen140_peer_{pk} → bool
    check:          LS_PREFIX + 'check_',           // gen140_check_{ck} → bool
    evidence:       LS_PREFIX + 'evidence_',        // gen140_evidence_{ek} → JSON
    recycle:        LS_PREFIX + 'recycle_',         // gen140_recycle_{rk} → JSON
    realtask:       LS_PREFIX + 'realtask_',        // gen140_realtask_{tk} → JSON
  };

  // 共用工具
  function lsGet(key, fallback) {
    try { const v = localStorage.getItem(key); return v == null ? fallback : v; }
    catch (_) { return fallback; }
  }
  function lsSet(key, value) {
    try { localStorage.setItem(key, value); return true; } catch (_) { return false; }
  }
  function lsGetJSON(key, fallback) {
    const v = lsGet(key, null);
    if (v == null) return fallback;
    try { return JSON.parse(v); } catch (_) { return fallback; }
  }
  function lsSetJSON(key, value) { return lsSet(key, JSON.stringify(value)); }

  function debounce(fn, ms) {
    let t;
    return function () {
      const args = arguments, ctx = this;
      clearTimeout(t);
      t = setTimeout(() => fn.apply(ctx, args), ms);
    };
  }

  // Artifact index 工具（Task 4 用）
  function addToArtifactIndex(ak, title, kind, sourcePage) {
    const idx = lsGetJSON(LS.artifactIndex, []);
    const i = idx.findIndex(x => x.ak === ak);
    const entry = { ak, title, kind, sourcePage, savedAt: new Date().toISOString() };
    if (i >= 0) idx[i] = entry; else idx.push(entry);
    lsSetJSON(LS.artifactIndex, idx);
  }

  // 暴露給其他 task 用
  window.GEN140 = { LS, lsGet, lsSet, lsGetJSON, lsSetJSON, debounce, addToArtifactIndex };

  // === Task 3 之後依序加 init 函式宣告於此處 === //
  function initInlineReflection() {
    document.querySelectorAll('.inline-reflection').forEach(function (el) {
      const rk = el.getAttribute('data-rk');
      if (!rk) return;
      const input = el.querySelector('.ir-input');
      const saved = el.querySelector('.ir-saved');
      const exportBtn = el.querySelector('.ir-export');
      const key = window.GEN140.LS.reflect + rk;

      // 載入既有
      const v = window.GEN140.lsGet(key, '');
      if (v) input.value = v;

      // autosave on input + blur
      const save = window.GEN140.debounce(function () {
        window.GEN140.lsSet(key, input.value);
        if (saved) {
          saved.hidden = false;
          saved.textContent = '已儲存到本機 · ' + new Date().toLocaleTimeString('zh-TW');
        }
      }, 500);
      input.addEventListener('input', save);
      input.addEventListener('blur', save);

      // 匯出全課所有 reflection 為 .md
      if (exportBtn) {
        exportBtn.addEventListener('click', function () {
          const all = [];
          for (let i = 0; i < localStorage.length; i++) {
            const k = localStorage.key(i);
            if (k && k.startsWith(window.GEN140.LS.reflect)) {
              all.push({ rk: k.replace(window.GEN140.LS.reflect, ''), text: localStorage.getItem(k) });
            }
          }
          const date = new Date().toISOString().slice(0, 10);
          const md = '# 我的反思紀錄_' + date + '\n\n' +
            all.map(r => '## ' + r.rk + '\n\n' + r.text).join('\n\n---\n\n');
          const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
          const a = document.createElement('a');
          a.href = URL.createObjectURL(blob);
          a.download = '我的反思紀錄_' + date + '.md';
          a.click();
          URL.revokeObjectURL(a.href);
        });
      }
    });
  }
  function initArtifactSave() {
    document.querySelectorAll('.artifact-save').forEach(function (el) {
      const ak = el.getAttribute('data-ak');
      if (!ak) return;
      const btn = el.querySelector('.as-btn');
      if (!btn) return;
      const sourceSelector = el.getAttribute('data-source');  // 例如 '#prompt-output'
      const title = el.getAttribute('data-title') || ak;
      const kind = el.getAttribute('data-kind') || 'tool-page';
      const key = window.GEN140.LS.artifact + ak;

      // 已存過的狀態
      if (window.GEN140.lsGet(key, null)) {
        btn.textContent = '已存到我的作品集 ✓';
        btn.classList.add('saved');
      }

      btn.addEventListener('click', function () {
        let content = {};
        if (sourceSelector) {
          const src = document.querySelector(sourceSelector);
          if (src) {
            if ('value' in src && src.value !== undefined) content.text = src.value;
            else content.html = src.innerHTML;
          }
        } else {
          // 沒指定 source，抓頁面內所有 textarea
          const textareas = document.querySelectorAll('textarea');
          content.fields = Array.from(textareas)
            .filter(t => !t.classList.contains('ir-input') && !t.classList.contains('ic-feedback'))
            .map(t => ({ id: t.id || t.name || '', value: t.value }));
        }
        const artifact = {
          ak, title, kind,
          sourcePage: location.pathname.split('/').slice(-2).join('/'),
          content,
          savedAt: new Date().toISOString()
        };
        window.GEN140.lsSetJSON(key, artifact);
        window.GEN140.addToArtifactIndex(ak, title, kind, artifact.sourcePage);
        btn.textContent = '已存到我的作品集 ✓';
        btn.classList.add('saved');
      });
    });
  }
  // Task 4 完成 ↑
  function initPeerHandoff() {
    document.querySelectorAll('.peer-handoff input[type=checkbox][data-pk]').forEach(function (cb) {
      const pk = cb.getAttribute('data-pk');
      const key = window.GEN140.LS.peer + pk;
      if (window.GEN140.lsGet(key, '0') === '1') cb.checked = true;
      cb.addEventListener('change', function () {
        window.GEN140.lsSet(key, cb.checked ? '1' : '0');
      });
    });
  }
  // Task 5 完成 ↑
  function initInstructorCheck() {
    document.querySelectorAll('.instructor-check').forEach(function (el) {
      const ck = el.querySelector('input[type=checkbox][data-ck]');
      const fb = el.querySelector('.ic-feedback');
      if (!ck) return;
      const ckKey = window.GEN140.LS.check + ck.getAttribute('data-ck');
      if (window.GEN140.lsGet(ckKey, '0') === '1') ck.checked = true;
      ck.addEventListener('change', function () {
        window.GEN140.lsSet(ckKey, ck.checked ? '1' : '0');
      });
      if (fb) {
        const fbKey = ckKey + '_feedback';
        const v = window.GEN140.lsGet(fbKey, '');
        if (v) fb.value = v;
        const save = window.GEN140.debounce(function () {
          window.GEN140.lsSet(fbKey, fb.value);
        }, 500);
        fb.addEventListener('input', save);
        fb.addEventListener('blur', save);
      }
    });
  }
  // Task 6 完成 ↑
  function initRealTaskRewrite() {
    document.querySelectorAll('.real-task-rewrite').forEach(function (el) {
      const tk = el.getAttribute('data-tk');
      if (!tk) return;
      const input = el.querySelector('.rt-input');
      const saved = el.querySelector('.rt-saved');
      const saveBtn = el.querySelector('.rt-save');
      const key = window.GEN140.LS.realtask + tk;

      const v = window.GEN140.lsGetJSON(key, null);
      if (v && v.text) input.value = v.text;

      const persist = window.GEN140.debounce(function () {
        window.GEN140.lsSetJSON(key, { text: input.value, savedAt: new Date().toISOString() });
        if (saved) {
          saved.hidden = false;
          saved.textContent = '已儲存 · ' + new Date().toLocaleTimeString('zh-TW');
        }
      }, 500);
      input.addEventListener('input', persist);
      input.addEventListener('blur', persist);

      if (saveBtn) {
        saveBtn.addEventListener('click', function () {
          const ak = 'realtask-' + tk;
          window.GEN140.lsSetJSON(window.GEN140.LS.artifact + ak, {
            ak, title: '真實任務改寫 · ' + tk, kind: 'reflection',
            sourcePage: location.pathname.split('/').slice(-2).join('/'),
            content: { text: input.value }, savedAt: new Date().toISOString()
          });
          window.GEN140.addToArtifactIndex(ak, '真實任務改寫 · ' + tk, 'reflection', location.pathname);
          saveBtn.textContent = '已存到作品集 ✓';
        });
      }
    });
  }
  // Task 7 完成 ↑
  function initAIRecycler() {
    document.querySelectorAll('.ai-recycler').forEach(function (el) {
      const rk = el.getAttribute('data-rk');
      if (!rk) return;
      const promptText = el.getAttribute('data-prompt') || '';
      const deeplink = el.querySelector('.ar-deeplink');
      const copyBtn = el.querySelector('.ar-copy');
      const pasteEl = el.querySelector('.ar-paste');
      const reflectEl = el.querySelector('.ar-reflect');
      const saveBtn = el.querySelector('.ar-save');
      const key = window.GEN140.LS.recycle + rk;

      if (deeplink && promptText) {
        deeplink.href = 'https://chat.openai.com/?q=' + encodeURIComponent(promptText);
        deeplink.target = '_blank';
        deeplink.rel = 'noopener';
      }
      if (copyBtn && promptText) {
        copyBtn.addEventListener('click', function () {
          navigator.clipboard.writeText(promptText).then(function () {
            copyBtn.textContent = '已複製 ✓';
            setTimeout(function () { copyBtn.textContent = '複製 prompt'; }, 1500);
          });
        });
      }

      const v = window.GEN140.lsGetJSON(key, null);
      if (v) {
        if (pasteEl && v.aiResult) pasteEl.value = v.aiResult;
        if (reflectEl && v.reflection) reflectEl.value = v.reflection;
      }
      function persist() {
        window.GEN140.lsSetJSON(key, {
          aiResult: pasteEl ? pasteEl.value : '',
          reflection: reflectEl ? reflectEl.value : '',
          savedAt: new Date().toISOString()
        });
      }
      const debouncedPersist = window.GEN140.debounce(persist, 500);
      if (pasteEl) { pasteEl.addEventListener('input', debouncedPersist); pasteEl.addEventListener('blur', debouncedPersist); }
      if (reflectEl) { reflectEl.addEventListener('input', debouncedPersist); reflectEl.addEventListener('blur', debouncedPersist); }

      if (saveBtn) {
        saveBtn.addEventListener('click', function () {
          persist();
          const ak = 'recycle-' + rk;
          window.GEN140.lsSetJSON(window.GEN140.LS.artifact + ak, {
            ak, title: 'AI 回收 · ' + rk, kind: 'prompt',
            sourcePage: location.pathname.split('/').slice(-2).join('/'),
            content: { prompt: promptText, aiResult: pasteEl ? pasteEl.value : '', reflection: reflectEl ? reflectEl.value : '' },
            savedAt: new Date().toISOString()
          });
          window.GEN140.addToArtifactIndex(ak, 'AI 回收 · ' + rk, 'prompt', location.pathname);
          saveBtn.textContent = '已存到作品集 ✓';
        });
      }
    });
  }
  // Task 8 完成 ↑
  function initEvidenceSubmit() {
    document.querySelectorAll('.evidence-submit').forEach(function (el) {
      const ek = el.getAttribute('data-ek');
      if (!ek) return;
      const url = el.querySelector('.es-url');
      const screenshot = el.querySelector('.es-screenshot');
      const code = el.querySelector('.es-code');
      const saveBtn = el.querySelector('.es-save');
      const key = window.GEN140.LS.evidence + ek;

      const v = window.GEN140.lsGetJSON(key, null);
      if (v) {
        if (url) url.value = v.url || '';
        if (screenshot) screenshot.value = v.screenshot || '';
        if (code) code.value = v.code || '';
      }
      function persist() {
        window.GEN140.lsSetJSON(key, {
          url: url ? url.value : '',
          screenshot: screenshot ? screenshot.value : '',
          code: code ? code.value : '',
          savedAt: new Date().toISOString()
        });
      }
      const debouncedPersist = window.GEN140.debounce(persist, 500);
      [url, screenshot, code].filter(Boolean).forEach(function (e) {
        e.addEventListener('input', debouncedPersist);
        e.addEventListener('blur', debouncedPersist);
      });
      if (saveBtn) {
        saveBtn.addEventListener('click', function () {
          persist();
          const ak = 'evidence-' + ek;
          window.GEN140.lsSetJSON(window.GEN140.LS.artifact + ak, {
            ak, title: '證據 · ' + ek, kind: 'evidence',
            sourcePage: location.pathname.split('/').slice(-2).join('/'),
            content: window.GEN140.lsGetJSON(key, {}),
            savedAt: new Date().toISOString()
          });
          window.GEN140.addToArtifactIndex(ak, '證據 · ' + ek, 'evidence', location.pathname);
          saveBtn.textContent = '已存到作品集 ✓';
        });
      }
    });
  }
  // Task 9 完成 ↑

  // === Init dispatcher === //
  document.addEventListener('DOMContentLoaded', function () {
    // Task 3 已完成：
    initInlineReflection();
    // Task 4 已完成：
    initArtifactSave();
    // Task 5 已完成：
    initPeerHandoff();
    // Task 6 已完成：
    initInstructorCheck();
    // Task 7 已完成：
    initRealTaskRewrite();
    // Task 8 已完成：
    initAIRecycler();
    // Task 9 已完成：
    initEvidenceSubmit();
  });
})();
