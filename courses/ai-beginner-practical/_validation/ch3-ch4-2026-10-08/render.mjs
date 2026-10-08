import fs from 'node:fs';
import {marked} from '/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js';
for(const u of ['CH3-1','CH4-1']){
 const base='_validation/ch3-ch4-2026-10-08/'+u;
 let rendered=marked.parse(fs.readFileSync(base+'-render-input.md','utf8'));
 const payloads=JSON.parse(fs.readFileSync(base+'-raw-payloads.json','utf8'));
 for(const [i,raw]of Object.entries(payloads)){
  const token='<div data-raw-token="'+i+'"></div>';
  if(!rendered.includes(token))throw new Error('Missing raw payload '+i);
  rendered=rendered.replace(token,()=>raw);
 }
 fs.writeFileSync(base+'-rendered.html',rendered);
}
