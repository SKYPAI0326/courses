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
  // function initPeerHandoff()      { ... }   ← Task 5
  // function initInstructorCheck()  { ... }   ← Task 6
  // function initRealTaskRewrite()  { ... }   ← Task 7
  // function initAIRecycler()       { ... }   ← Task 8
  // function initEvidenceSubmit()   { ... }   ← Task 9

  // === Init dispatcher === //
  document.addEventListener('DOMContentLoaded', function () {
    // Task 3 已完成：
    initInlineReflection();
    // Task 4 已完成：
    initArtifactSave();
    // Task 5 完成時取消註解：
    // initPeerHandoff();
    // Task 6 完成時取消註解：
    // initInstructorCheck();
    // Task 7 完成時取消註解：
    // initRealTaskRewrite();
    // Task 8 完成時取消註解：
    // initAIRecycler();
    // Task 9 完成時取消註解：
    // initEvidenceSubmit();
  });
})();
