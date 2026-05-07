// ════════════════════════════════════════════════════════════
// Lite Pack v1.2 · LLM Helper（共用骨架）
//
// 這段 inject 到每個用 Gemini 的 workflow Code node 開頭。
// 學員客製 workflow 時：
//   - 改 LP_CONFIG → 統一調整 model / timeout / retry / RPM
//   - 用 lpCall(...) 呼叫 LLM → 自動 throttle + retry + 429 處理
//   - 用 lpSizeOK(...) 預檢 inline data → 避免撞 20 MB API limit
//   - 用 lpThrottle() → loop 內呼叫之間 sleep
//
// 換 LLM provider（Gemini → Claude / OpenAI）：只改 lpCall 內的 url/headers/body shape，
// 業務邏輯不動。
// ════════════════════════════════════════════════════════════
const LP = {
  apiKey: '__GEMINI_API_KEY__',
  model: 'gemini-2.5-flash',
  endpoint: 'https://generativelanguage.googleapis.com/v1beta/models',
  rpmDelayMs: 6500,                       // Free tier 10 RPM；paid 改 1000
  maxRetries: 3,
  retry429Ms: 60000,                      // 429 等 60s（quota window）
  retry5xxMs: 5000,                       // 5xx 等 5s
  timeoutMs: 30000,
  maxInlineBytes: 18 * 1024 * 1024,       // 18 MB（保留 buffer to 20 MB hard limit）
};

const lpSleep = ms => new Promise(r => setTimeout(r, ms));

// 主呼叫：自動 retry 429/5xx
// 用法：const r = await lpCall.call(this, { prompt, gen: { maxOutputTokens: 200 } });
//      if (r.ok) use r.text; else use r.error
async function lpCall({ prompt, gen = {}, _att = 0 }) {
  if (!prompt || typeof prompt !== 'string') return { ok: false, text: '', error: 'empty prompt' };
  try {
    const r = await this.helpers.httpRequest({
      method: 'POST',
      url: LP.endpoint + '/' + LP.model + ':generateContent',
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': LP.apiKey },
      body: {
        contents: [{ role: 'user', parts: [{ text: prompt }] }],
        generationConfig: {
          temperature: 0.4, maxOutputTokens: 400, thinkingConfig: { thinkingBudget: 0 },
          ...gen
        }
      },
      json: true,
      timeout: LP.timeoutMs,
    });
    return {
      ok: true,
      text: r.candidates?.[0]?.content?.parts?.[0]?.text || '',
      finishReason: r.candidates?.[0]?.finishReason || 'unknown',
      attempt: _att,
    };
  } catch (e) {
    const m = (e && e.message) || String(e);
    const r429 = m.includes('429') || m.includes('RESOURCE_EXHAUSTED') || m.includes('quota');
    const r5xx = /\b5\d{2}\b/.test(m) || m.includes('UNAVAILABLE');
    if (_att < LP.maxRetries && (r429 || r5xx)) {
      await lpSleep(r429 ? LP.retry429Ms : LP.retry5xxMs);
      return lpCall.call(this, { prompt, gen, _att: _att + 1 });
    }
    return { ok: false, text: '', error: m.substring(0, 300), attempt: _att };
  }
}

// loop 內 N 筆呼叫之間 sleep（避免撞 RPM）
// 用法：for (let i = 0; i < items.length; i++) { if (i > 0) await lpThrottle(); ... }
async function lpThrottle() { await lpSleep(LP.rpmDelayMs); }

// 預檢 inline data 是否會撞 20 MB API request limit
// 用法：if (!lpSizeOK(binary.data.data)) { /* skip 或 chunk */ }
function lpSizeOK(base64OrBuf) {
  const b = typeof base64OrBuf === 'string'
    ? Math.floor(base64OrBuf.length * 0.75)
    : (base64OrBuf && base64OrBuf.length) || 0;
  return b <= LP.maxInlineBytes;
}
