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
  // function initInlineReflection() { ... }   ← Task 3
  // function initArtifactSave()     { ... }   ← Task 4
  // function initPeerHandoff()      { ... }   ← Task 5
  // function initInstructorCheck()  { ... }   ← Task 6
  // function initRealTaskRewrite()  { ... }   ← Task 7
  // function initAIRecycler()       { ... }   ← Task 8
  // function initEvidenceSubmit()   { ... }   ← Task 9

  // === Init dispatcher === //
  document.addEventListener('DOMContentLoaded', function () {
    // Task 3 完成時取消註解：
    // initInlineReflection();
    // Task 4 完成時取消註解：
    // initArtifactSave();
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
