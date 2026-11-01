import fs from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

// 2026-11-01 改版：對齊新版講義、山徑咖啡示範與小組企劃書段落。
const root = new URL("../", import.meta.url);
const outDir = new URL("assets/downloads/", root);
const qaDir = new URL("_review/2026-11-01/materials2/workbook-qa/", root);
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

function addSheet(wb, spec) {
  const s = wb.worksheets.add(spec.name);
  const end = String.fromCharCode(64 + spec.headers.length);
  title(s, `A1:${end}1`, spec.title || spec.name, spec.subtitle);
  grid(s, `A4:${end}4`, `A5:${end}${spec.lastRow || 16}`, spec.headers, spec.widths.map((w, i) => [`${String.fromCharCode(65 + i)}:${String.fromCharCode(65 + i)}`, w]));
  if (spec.rows?.length) s.getRange(`A5:${end}${spec.rows.length + 4}`).values = spec.rows;
  if (spec.demoRows) s.getRange(`A5:${end}${spec.demoRows + 4}`).format.fill = colors.green;
  return s;
}

const persona = Workbook.create();
const personaSpecs = [
  { name: "使用說明", title: "Persona 研究與受眾簡報", subtitle: "綠色是山徑咖啡示範；黃色列填自己組的產品。先留證據，再寫結論。", headers: ["步驟", "要做什麼", "完成證據", "快速檢查", "卡住時", "放進企劃書"], widths: [9, 31, 30, 27, 28, 22], demoRows: 1, rows: [[1, "讀三份訪談，分開填事實、假設與待查", "每列保留原話或行為來源", "三位人物沒有被合併成平均人物", "先訪談一位真實顧客", "第 2 段：市場與定位"]] },
  { name: "Persona 主檔", subtitle: "三位示範人物取自山徑咖啡品牌包；下方空白列請換成自己組的訪談。", headers: ["人物", "使用情境", "目標／工作", "痛點／障礙", "事實", "假設", "待查", "來源"], widths: [14, 28, 29, 31, 34, 27, 29, 25], demoRows: 3, rows: [
    ["阿傑", "使用入門壺兩年，想改善注水穩定度", "比較壺嘴與重量後再決定是否升級", "看規格不知道差異；不確定試握是否收費", "會看 YouTube 評測並到電商比價", "資料未提供，由小組另列假設", "哪些比較欄位最影響決定", "品牌包裡阿傑的訪談"],
    ["麗芬", "想買第二把壺，未來可能在社區教手沖", "找出新手較不容易失手的選擇", "商品介紹偏專業；缺三款使用難度比較", "會在 Facebook 社團詢問其他使用者", "資料未提供，由小組另列假設", "教學情境需要哪些產品資訊", "品牌包裡麗芬的訪談"],
    ["柏翰", "第一次從細口壺升級控流壺", "用一致方法比較實測影片", "不信任只呈現最好一次的示範", "會收藏評測影片並自己做筆記", "資料未提供，由小組另列假設", "哪些測試條件足以建立信任", "品牌包裡柏翰的訪談"]
  ] },
  { name: "訪談紀錄", subtitle: "保留情境、原話、替代方案與障礙；示範資料均為課堂模擬訪談。", headers: ["受訪者", "情境／觸發", "原話", "目前替代方案", "決策障礙", "事實／假設／待查", "後續追問"], widths: [14, 31, 44, 29, 31, 22, 28], demoRows: 3, rows: [
    ["阿傑", "已有入門壺，想改善注水穩定度", "我知道貴的壺可能比較穩，但看規格不知道差在哪。能先拿在手上試，我才敢買。", "看 YouTube 評測，再到大型電商比價", "怕買錯壺嘴與重量", "事實", "試握服務會如何影響決定？"],
    ["麗芬", "想買第二把壺，未來可能教手沖", "我想知道新手用哪一把最不容易失手，不想只聽材質多高級。", "在 Facebook 社團詢問其他使用者", "希望直接比較三款使用難度", "事實", "她會信任哪些比較證據？"],
    ["柏翰", "第一次升級控流壺", "我會看實測影片，但如果沒有標注同一個人、同一個水量，影片也很難比較。", "收藏多支評測影片並做筆記", "在意比較方法是否一致", "事實", "哪些一致條件必須標出？"]
  ] },
  { name: "信任關係圖", subtitle: "依個人人際、樞紐人物、同好社群三層找資訊來源；沒有證據就寫待查。", headers: ["關係層", "人物／來源", "訪談證據", "影響哪個判斷", "目前可接觸程度", "事實／假設／待查", "下一步"], widths: [18, 27, 37, 28, 21, 22, 27], demoRows: 3, rows: [
    ["個人人際", "品牌包未提供", "三份訪談沒有提到親友影響", "待查", "待查", "待查", "訪談誰會一起討論購買"],
    ["樞紐人物", "YouTube 評測者", "阿傑看評測；柏翰收藏實測影片", "比較產品與測試方法", "可從公開內容觀察", "事實", "記錄受眾信任的比較欄位"],
    ["同好社群", "Facebook 咖啡社團", "麗芬會詢問其他使用者", "理解使用難度與經驗", "需先確認社群規則", "事實", "整理常見問題，不推估成效"]
  ] },
  { name: "受眾摘要", subtitle: "把 Persona、關係圖與旅程缺口收成後續渠道共用的一列。", headers: ["核心 Persona", "關鍵情境", "顧客要完成的工作", "原話痛點", "行為證據", "決策障礙", "擴展 Persona", "資料狀態"], widths: [25, 31, 35, 38, 31, 31, 26, 19], demoRows: 1, rows: [["阿傑型升級使用者", "已有入門器具，開始比較第二把壺", "用可比較的證據確認重量、控流與習慣相符", "能先拿在手上試，我才敢買。", "先看評測、比價，再找可試用通路", "規格難懂、比較方法不一致、怕選錯", "麗芬型進階興趣者", "課堂模擬資料"]] }
];
personaSpecs.forEach((spec) => addSheet(persona, spec));
await renderAll(persona, personaSpecs.map((s) => s.name), "persona");
await exportBook(persona, "Persona研究與受眾簡報.xlsx");

const plan = Workbook.create();
const commonWidths = [18, 28, 28, 28, 28, 28, 28, 28];
const planSpecs = [
  { name: "導覽", title: "整合行銷企劃工作簿", subtitle: "小組企劃書的選配試算表；用來算預算與 KPI，主成果仍放在共用簡報。", headers: ["產品", "使用方式", "主要輸入", "完成物", "更新時機", "檢查", "企劃書段落", "備註"], rows: [["山徑咖啡", "示範列只說明填法", "品牌包與課堂完成物", "可回查的計算與決策", "有新證據時", "不把模擬數字當真實成效", "第 1～8 段", "下方空白列換成自己組產品"]] },
  { name: "1 顧客心理", subtitle: "整理購買時刻、判斷方式與有證據的心理線索。", headers: ["產品", "購買時刻", "直覺／比較／兩者", "心理線索", "訪談原話", "可採取做法", "證據來源", "企劃書內容"], rows: [["山徑咖啡", "比較第二把手沖壺", "比較", "降低選錯風險", "能先拿在手上試，我才敢買。", "提早說明 20 分鐘試握服務", "阿傑訪談與服務摘要", "購買心理地圖"]] },
  { name: "2 市場與定位", subtitle: "把受眾、旅程缺口、定位與核心訊息放在同一列。", headers: ["產品", "核心 Persona", "旅程最大缺口", "推廣方向", "定位聲明", "核心訊息", "證據", "待查"], rows: [["山徑咖啡", "已有入門器具、想升級但怕買錯的人", "比較資訊不足", "先比較再試握", "提供可比較、可試握的手沖壺選擇", "先比較使用差異，再決定是否升級", "三份訪談、商品頁與服務摘要", "正式市場資料"]] },
  { name: "3 社群", subtitle: "主平台、開場、腳本與月曆要沿用同一核心訊息。", headers: ["產品", "主平台", "開場句", "內容角色", "腳本／素材", "行動呼籲", "發布位置", "來源"], rows: [["山徑咖啡", "依平台選擇表決定", "看規格還是不知道三款差在哪？", "比較教育", "用同一人、同一水量示範三款", "到商品頁看完整比較", "依小組決定", "柏翰訪談與社群摘要"]] },
  { name: "4 搜尋", subtitle: "曝光與點擊填原始值；點閱率由公式計算。", headers: ["產品", "查詢", "搜尋意圖", "曝光", "點擊", "點閱率", "承接頁任務", "資料期間／來源"], rows: [["山徑咖啡", "手沖壺推薦", "商業型", 4200, 126, null, "比較三款使用差異並導向試握", "品牌包搜尋資料，近 28 天"]] },
  { name: "5 成效指標與追蹤", subtitle: "先寫事件與分母；完成率由公式計算，不交給 AI 算。", headers: ["產品", "目標", "事件／行為", "開始數", "完成數", "完成率", "資料來源", "觀察與下一步"], rows: [["山徑咖啡", "完成試握預約", "預約開始 → 預約完成", 120, 54, null, "課堂模擬基線", "先驗證事件完整，再判讀成效"]] },
  { name: "6 廣告", subtitle: "小組決定是否投放與分配；預算合計、剩餘預算由公式計算。", headers: ["產品", "預算項目", "本次分配", "總預算上限", "預算合計", "剩餘預算", "活動類型", "單一變因"], rows: [["山徑咖啡", "90 天廣告專案", null, 45000, null, null, "依旅程與目標決定", "標題、圖片或受眾擇一"]] },
  { name: "7 名單與 Email", subtitle: "分開名單來源、同意範圍、觸發與退出條件。", headers: ["產品", "名單來源", "現有數量", "可用數量", "同意範圍", "觸發", "第一封信任務", "退出條件"], rows: [["山徑咖啡", "門市預約留下的 Email", 420, 240, "240 筆有獨立行銷同意", "完成表單並符合寄送資格", "確認預約並提供比較內容", "完成預約、退出或不同意"]] },
  { name: "8 整合策略與 A3", subtitle: "把渠道角色、KPI、時程與 A3 決策收在同一列。", headers: ["產品", "唯一目標", "渠道角色", "KPI／基線", "時程", "關鍵證據", "下一輪決策", "A3 狀態"], rows: [["山徑咖啡", "先看懂三款差異，再開始試握預約", "搜尋與社群解釋比較；Email 與 LINE 承接", "月瀏覽 2,400；開始 120；完成 54", "第 4、8、12 週檢查", "品牌包課堂模擬基線", "先驗證事件，再決定保留或調整", "待實際執行後追蹤"]] },
  { name: "AI 使用紀錄", subtitle: "記錄 AI 做了什麼、人工改了什麼，以及採用理由。", headers: ["產品", "日期", "任務", "使用資料", "AI 建議摘要", "人工修改", "採用／不採用理由", "待查"], rows: [["山徑咖啡", "2026-11-01", "檢查企劃書七段矛盾", "受眾、核心訊息、行動呼籲、事件與指標", "只列缺口，不代替決策", "逐項回查品牌包", "超出來源的建議不採用", "正式執行資料"]] }
];
planSpecs.forEach((spec) => addSheet(plan, { ...spec, widths: commonWidths, demoRows: 1 }));

const search = plan.worksheets.getItem("4 搜尋");
search.getRange("F5").formulas = [["=IFERROR(E5/D5,0)"]];
search.getRange("F5:F16").fillDown();
search.getRange("F5:F16").format.numberFormat = "0.0%";
const measure = plan.worksheets.getItem("5 成效指標與追蹤");
measure.getRange("F5").formulas = [["=IFERROR(E5/D5,0)"]];
measure.getRange("F5:F16").fillDown();
measure.getRange("F5:F16").format.numberFormat = "0.0%";
const ads = plan.worksheets.getItem("6 廣告");
ads.getRange("E5").formulas = [["=SUM(C6:C16)"]];
ads.getRange("F5").formulas = [["=D5-E5"]];
ads.getRange("C5:F16").format.numberFormat = "#,##0";
await plan.recalculate();
await renderAll(plan, planSpecs.map((s) => s.name), "plan");
await exportBook(plan, "整合行銷企劃工作簿.xlsx");

console.log(JSON.stringify({ personaSample: persona.worksheets.getItem("Persona 主檔").getRange("A4:H7").values }));
console.log(JSON.stringify({ searchFormulas: search.getRange("F5:F16").formulas, completionFormulas: measure.getRange("F5:F16").formulas, budgetFormulas: ads.getRange("E5:F5").formulas }));
console.log("built Persona研究與受眾簡報.xlsx and 整合行銷企劃工作簿.xlsx");
