import fs from 'node:fs';
import {marked} from '/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js';
for(const u of ['CH1-1','CH3-1','CH4-1']){
 const b='_validation/field-repairs-2026-10-08/'+u;
 let x=marked.parse(fs.readFileSync(b+'-render-input.md','utf8'));
 for(const [k,v] of Object.entries(JSON.parse(fs.readFileSync(b+'-raw-payloads.json','utf8')))){
  const token='<div data-raw-token="'+k+'"></div>';if(!x.includes(token))throw Error(token);x=x.replace(token,()=>v);
 }
 fs.writeFileSync(b+'-rendered.html',x);
}
