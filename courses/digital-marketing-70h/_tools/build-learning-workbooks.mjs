import fs from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = new URL("../", import.meta.url);
const outDir = new URL("assets/downloads/", root);
const qaDir = new URL("_repair/2026-07-19/workbook-qa/", root);
await fs.mkdir(outDir, { recursive: true });
await fs.mkdir(qaDir, { recursive: true });

const colors = { gold: "#C9963A", ink: "#2C2B28", cream: "#F5F3EE", input: "#FFF4CC", line: "#DDD7CD", muted: "#6F6B64", white: "#FFFFFF", green: "#E5F2E8" };

function title(sheet, range, text, subtitle) {
  sheet.showGridLines = false;
  sheet.getRange(range).merge();
  const cell = range.split(":")[0];
  sheet.getRange(cell).values = [[text]];
  sheet.getRange(range).format = { fill: colors.gold, font: { bold: true, color: colors.white, size: 17 }, rowHeight: 34, verticalAlignment: "center" };
  const startCol = range.match(/[A-Z]+/)[0];
  const endCol = range.split(":")[1].match(/[A-Z]+/)[0];
  sheet.getRange(`${startCol}2:${endCol}2`).merge();
  sheet.getRange(`${startCol}2`).values = [[subtitle]];
  sheet.getRange(`${startCol}2:${endCol}2`).format = { fill: colors.cream, font: { color: colors.muted, size: 10 }, rowHeight: 28, wrapText: true, verticalAlignment: "center" };
  sheet.freezePanes.freezeRows(4);
}

function grid(sheet, headerRange, dataRange, headers, widths) {
  sheet.getRange(headerRange).values = [headers];
  sheet.getRange(headerRange).format = { fill: colors.ink, font: { bold: true, color: colors.white }, rowHeight: 30, horizontalAlignment: "center", verticalAlignment: "center", wrapText: true };
  sheet.getRange(dataRange).format = { fill: colors.input, font: { size: 10 }, rowHeight: 34, verticalAlignment: "top", wrapText: true, borders: { preset: "all", style: "thin", color: colors.line } };
  widths.forEach(([range, width]) => { sheet.getRange(range).format.columnWidth = width; });
}

async function renderAll(wb, names, prefix) {
  for (const name of names) {
    const blob = await wb.render({ sheetName: name, autoCrop: "all", scale: 1.15, format: "png" });
    await fs.writeFile(new URL(`${prefix}-${name}.png`, qaDir), new Uint8Array(await blob.arrayBuffer()));
  }
}

async function exportBook(wb, filename) {
  const output = await SpreadsheetFile.exportXlsx(wb);
  await output.save(fileURLToPath(new URL(filename, outDir)));
}

const persona = Workbook.create();
const pGuide = persona.worksheets.add("使用說明");
title(pGuide, "A1:F1", "Persona 研究與受眾簡報", "M3-2 可填寫工作簿｜黃色欄位由學員輸入；範例不等於事實，必須標示證據狀態。 ");
grid(pGuide, "A4:F4", "A5:F10", ["步驟", "要做什麼", "完成證據", "快速檢查", "卡住時", "下游用途"], [["A:A", 9], ["B:B", 28], ["C:C", 25], ["D:D", 24], ["E:E", 24], ["F:F", 24]]);
pGuide.getRange("A5:F9").values = [
  [1, "先填已知資料，不請 AI 補空白", "每一列有來源或標為待訪談", "沒有把猜測寫成事實", "先訪談 1 位真實顧客", "Persona 主檔"],
  [2, "完成至少 3 次訪談", "留下原話、情境與來源日期", "原話不是你的摘要", "用評論或客服紀錄補證據", "訪談紀錄"],
  [3, "更新六維度與決策障礙", "每列標已驗證／待訪談／不採用", "至少有一項被證據推翻", "縮小到一個核心 Persona", "Audience Brief"],
  [4, "選擇核心與擴展 Persona", "寫下選擇與不選理由", "不是只看年齡性別", "回到需求與行為證據", "M3-4／M4～M9"],
  [5, "鎖定版本與重查日期", "版本、日期、負責人完整", "後續模組引用同一版本", "新證據出現再升版", "M10 Kickoff"]
];

const pMaster = persona.worksheets.add("Persona主檔");
title(pMaster, "A1:H1", "Persona 主檔", "每列是一項可驗證描述；請勿一次生成完整人物後直接採用。 ");
grid(pMaster, "A4:H4", "A5:H22", ["Persona", "維度", "目前描述", "證據狀態", "來源／原話", "來源日期", "信心 1-5", "下一步"], [["A:A", 16], ["B:B", 18], ["C:C", 34], ["D:D", 16], ["E:E", 34], ["F:F", 14], ["G:G", 12], ["H:H", 26]]);
pMaster.getRange("B5:B10").values = [["基本資訊"], ["一天的生活／情境"], ["目標與任務"], ["痛點與阻礙"], ["資訊與平台習慣"], ["購買決策障礙"]];
pMaster.getRange("D5:D22").dataValidation = { rule: { type: "list", values: ["已驗證", "待訪談", "不採用"] } };
pMaster.getRange("G5:G22").dataValidation = { rule: { type: "list", values: ["1", "2", "3", "4", "5"] } };

const pInterview = persona.worksheets.add("訪談紀錄");
title(pInterview, "A1:I1", "顧客訪談紀錄", "至少保留三位受訪者的原話；不要只寫結論。 ");
grid(pInterview, "A4:I4", "A5:I18", ["日期", "受訪者代碼", "情境／觸發", "原話", "目前替代方案", "決策障礙", "行為證據", "對 Persona 的影響", "後續追問"], [["A:A", 14], ["B:B", 14], ["C:C", 25], ["D:D", 38], ["E:E", 24], ["F:F", 24], ["G:G", 25], ["H:H", 28], ["I:I", 24]]);

const pBrief = persona.worksheets.add("Audience Brief");
title(pBrief, "A1:F1", "Audience Brief｜後續模組共同輸入", "完成後鎖定版本；M3-4 與 M4～M10 引用同一份，不重新生成 Persona。 ");
grid(pBrief, "A4:F4", "A5:F16", ["區塊", "採用內容", "證據來源", "已驗證／待驗證", "對行銷的影響", "後續使用模組"], [["A:A", 23], ["B:B", 38], ["C:C", 30], ["D:D", 18], ["E:E", 34], ["F:F", 20]]);
pBrief.getRange("A5:A14").values = [["版本／日期"], ["核心 Persona"], ["關鍵情境"], ["Jobs-to-be-Done"], ["原話痛點"], ["行為證據"], ["常用平台"], ["決策障礙"], ["擴展 Persona"], ["不採用族群與理由"]];
pBrief.getRange("D5:D16").dataValidation = { rule: { type: "list", values: ["已驗證", "待驗證", "不適用"] } };
await renderAll(persona, ["使用說明", "Persona主檔", "訪談紀錄", "Audience Brief"], "persona");
await exportBook(persona, "Persona研究與受眾簡報.xlsx");

const plan = Workbook.create();
const nav = plan.worksheets.add("導覽");
title(nav, "A1:F1", "整合行銷企劃工作簿", "M2→M3→M10 產物接力｜先完成上游 brief，再進入策略與執行。 ");
grid(nav, "A4:F4", "A5:F12", ["順序", "分頁", "來源模組", "主要輸入", "完成物", "通過標準"], [["A:A", 9], ["B:B", 24], ["C:C", 14], ["D:D", 30], ["E:E", 28], ["F:F", 38]]);
nav.getRange("A5:F12").values = [
  [1, "Copy Workflow", "M2C-1", "範例 brief／Prompt", "AI 初稿與人工修訂紀錄", "能說明採納與不採納理由"],
  [2, "Audience Brief", "M3-2", "訪談與 Persona 主檔", "鎖版受眾簡報", "結論皆有證據狀態"],
  [3, "Message Brief", "M3-4", "Audience Brief／定位", "核心訊息與可信證據", "渠道只改表達、不重做定位"],
  [4, "Kickoff Brief", "M10-1", "Audience／Message／旅程", "問題定義與假設清單", "無來源內容標為待驗證"],
  [5, "Strategy Brief", "M10-2", "Kickoff Brief", "90 天渠道與 KPI 策略", "每個取捨都有理由"],
  [6, "Execution Pack", "M10-3", "Strategy／M4～M9 產物", "四週執行與追蹤表", "內容、CTA、事件、KPI 對齊"],
  [7, "AI 使用紀錄", "全程", "Prompt／AI 輸出", "人工判斷軌跡", "可辨識 AI 與人的貢獻"],
  [8, "A3 Final Report", "M10-4", "全部前置產物與結果", "一頁決策摘要", "主管 60 秒能回答是否繼續投入"]
];

function addBriefSheet(name, subtitle, rows) {
  const s = plan.worksheets.add(name);
  title(s, "A1:F1", name, subtitle);
  grid(s, "A4:F4", `A5:F${Math.max(rows.length + 4, 16)}`, ["區塊", "學員輸入", "來源／版本", "證據狀態", "決策理由", "下一步／下游用途"], [["A:A", 25], ["B:B", 42], ["C:C", 28], ["D:D", 17], ["E:E", 34], ["F:F", 30]]);
  s.getRange(`A5:A${rows.length + 4}`).values = rows.map((x) => [x]);
  s.getRange(`D5:D${Math.max(rows.length + 4, 16)}`).dataValidation = { rule: { type: "list", values: ["已驗證", "待驗證", "不適用"] } };
  return s;
}

addBriefSheet("Copy Workflow", "保存 Prompt、AI 初稿、人工修訂與採納理由；M3 完成後換入真實品牌 brief。", ["版本／日期", "任務與範例 brief", "原始 Prompt", "AI 初稿", "人工修訂", "採納內容", "不採納內容", "判斷理由", "下次改進"]);
addBriefSheet("Audience Brief", "引用 Persona 工作簿的鎖版內容；後續不得每頁重新生成。", ["版本／日期", "核心 Persona", "關鍵情境", "Jobs-to-be-Done", "原話痛點", "行為證據", "常用平台", "決策障礙", "擴展 Persona", "不採用族群與理由"]);
addBriefSheet("Message Brief", "統一 Persona、定位、核心訊息、可信證據與禁用空話。", ["版本／日期", "主 Persona", "定位句", "核心訊息", "可信證據 1", "可信證據 2", "可信證據 3", "不可使用的空話", "渠道可變項", "不可變的事實層"]);
addBriefSheet("Kickoff Brief", "M10-1｜匯入、校正與鎖版，不重新教授 Persona。", ["專案名稱／版本", "品牌與商業目標", "鎖定 Persona", "旅程缺口", "90 天問題定義", "已驗證證據", "待驗證假設", "不做範圍", "成功條件", "負責人與時程"]);
addBriefSheet("Strategy Brief", "M10-2｜每個渠道與 KPI 都要能追溯到旅程缺口與來源版本。", ["來源版本", "唯一策略目標", "核心訊息與證據", "主要旅程缺口", "渠道角色", "不選渠道與理由", "漏斗階段", "KPI 定義／基線／目標", "資料來源", "預算與人力", "關鍵假設", "W4／W8／W12 決策點"]);

const exec = plan.worksheets.add("Execution Pack");
title(exec, "A1:K1", "Execution Pack｜四週執行與追蹤", "每列是一個可交付任務；內容、CTA、事件與 KPI 必須引用同一策略版本。 ");
grid(exec, "A4:K4", "A5:K24", ["週次", "渠道／任務", "來源版本", "Persona", "核心訊息", "CTA", "漏斗階段", "追蹤事件", "KPI／停止條件", "負責人／期限", "狀態／QA"], [["A:A", 9], ["B:B", 26], ["C:C", 22], ["D:D", 18], ["E:E", 30], ["F:F", 20], ["G:G", 16], ["H:H", 22], ["I:I", 28], ["J:J", 20], ["K:K", 20]]);
exec.getRange("A5:A24").dataValidation = { rule: { type: "list", values: ["W1", "W2", "W3", "W4"] } };
exec.getRange("K5:K24").dataValidation = { rule: { type: "list", values: ["未開始", "進行中", "待 QA", "已完成", "暫停"] } };

const ai = plan.worksheets.add("AI 使用紀錄");
title(ai, "A1:H1", "AI 使用與人工判斷紀錄", "保留 AI 任務、輸出、人工修改與採納理由，作為 M10-4 報告證據。 ");
grid(ai, "A4:H4", "A5:H20", ["日期", "模組／任務", "工具", "Prompt 版本", "AI 建議摘要", "人工修改", "採納／不採納理由", "待重查項目"], [["A:A", 14], ["B:B", 22], ["C:C", 16], ["D:D", 18], ["E:E", 34], ["F:F", 34], ["G:G", 34], ["H:H", 28]]);

const a3 = plan.worksheets.add("A3 Final Report");
title(a3, "A1:F1", "A3 Final Report｜60 秒決策摘要", "每項結論都要能回查來源；沒有結果時標示待驗證，不得補造數字。 ");
grid(a3, "A4:F4", "A5:F16", ["六區塊", "決策摘要", "數據／證據", "來源版本", "AI 與人工判斷", "下一輪決策"], [["A:A", 24], ["B:B", 42], ["C:C", 34], ["D:D", 24], ["E:E", 34], ["F:F", 34]]);
a3.getRange("A5:A14").values = [["1 問題／機會"], ["2 關鍵證據"], ["3 策略選擇與取捨"], ["4 執行與追蹤"], ["5 結果"], ["三個無效項目"], ["6 下一輪決策"], ["仍待驗證假設"], ["下一次重查日期"], ["主管 yes／no 所需補件"]];

const planSheets = ["導覽", "Copy Workflow", "Audience Brief", "Message Brief", "Kickoff Brief", "Strategy Brief", "Execution Pack", "AI 使用紀錄", "A3 Final Report"];
await renderAll(plan, planSheets, "plan");
await exportBook(plan, "整合行銷企劃工作簿.xlsx");

const personaCheck = await persona.inspect({ kind: "region", sheetId: "Persona主檔", range: "A1:H12", maxChars: 3000 });
const planCheck = await plan.inspect({ kind: "region", sheetId: "A3 Final Report", range: "A1:F14", maxChars: 3000 });
const errors = await plan.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 50 }, summary: "final formula error scan" });
console.log(personaCheck.ndjson);
console.log(planCheck.ndjson);
console.log(errors.ndjson);
console.log("built Persona研究與受眾簡報.xlsx and 整合行銷企劃工作簿.xlsx");
