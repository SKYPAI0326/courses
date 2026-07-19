import fs from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = new URL("../", import.meta.url);
const sourceUrl = new URL("assets/datasets/SEO-keyword-research-sample.md", root);
const outUrl = new URL("assets/downloads/SEO關鍵字研究練習表.xlsx", root);
const outPath = fileURLToPath(outUrl);
const text = await fs.readFile(sourceUrl, "utf8");
const rows = [];
for (const line of text.split(/\r?\n/)) {
  const cells = line.trim().replace(/^\||\|$/g, "").split("|").map((v) => v.trim());
  if (cells.length !== 6 || cells[0] === "關鍵字" || /^---/.test(cells[0])) continue;
  const impressions = Number(cells[1].replace(/,/g, ""));
  const clicks = Number(cells[2].replace(/,/g, ""));
  const ctr = Number(cells[3].replace("%", "")) / 100;
  const position = Number(cells[4]);
  if (Number.isFinite(impressions) && Number.isFinite(clicks) && Number.isFinite(ctr) && Number.isFinite(position)) {
    rows.push([cells[0], impressions, clicks, ctr, position, "", "", "", ""]);
  }
}

const wb = Workbook.create();
const sheet = wb.worksheets.add("關鍵字研究");
sheet.showGridLines = false;
sheet.getRange("A1:I1").merge();
sheet.getRange("A1").values = [["SEO 關鍵字研究練習表"]];
sheet.getRange("A2:I2").merge();
sheet.getRange("A2").values = [["淺黃色欄位由學員填寫；數據來自課程模擬 GSC 匯出樣本。"]];
sheet.getRange("A4:I4").values = [["關鍵字", "曝光", "點擊", "CTR", "平均排名", "搜尋意圖", "主題群集", "內容優先序", "備註"]];
sheet.getRange(`A5:I${rows.length + 4}`).values = rows;
sheet.freezePanes.freezeRows(4);

sheet.getRange("A1:I1").format = { fill: "#C9963A", font: { bold: true, color: "#FFFFFF", size: 18 }, rowHeight: 34, verticalAlignment: "center" };
sheet.getRange("A2:I2").format = { fill: "#F5F3EE", font: { color: "#6F6B64", size: 10 }, rowHeight: 24, verticalAlignment: "center" };
sheet.getRange("A4:I4").format = { fill: "#2C2B28", font: { bold: true, color: "#FFFFFF" }, rowHeight: 28, verticalAlignment: "center", horizontalAlignment: "center" };
sheet.getRange(`A5:I${rows.length + 4}`).format = { font: { size: 10 }, rowHeight: 22, verticalAlignment: "center", borders: { preset: "inside", style: "thin", color: "#E3DED4" } };
sheet.getRange(`F5:I${rows.length + 4}`).format.fill = "#FFF4CC";
sheet.getRange(`D5:D${rows.length + 4}`).format.numberFormat = "0.0%";
sheet.getRange(`B5:C${rows.length + 4}`).format.numberFormat = "#,##0";
sheet.getRange(`E5:E${rows.length + 4}`).format.numberFormat = "0.0";
sheet.getRange(`F5:F${rows.length + 4}`).dataValidation = { rule: { type: "list", values: ["資訊型", "導航型", "商業型", "交易型"] } };
sheet.getRange(`H5:H${rows.length + 4}`).dataValidation = { rule: { type: "list", values: ["高", "中", "低"] } };
sheet.getRange("A:A").format.columnWidth = 26;
sheet.getRange("B:E").format.columnWidth = 12;
sheet.getRange("F:F").format.columnWidth = 14;
sheet.getRange("G:G").format.columnWidth = 20;
sheet.getRange("H:H").format.columnWidth = 14;
sheet.getRange("I:I").format.columnWidth = 30;
sheet.getRange(`A4:I${rows.length + 4}`).format.wrapText = true;

const guide = wb.worksheets.add("使用說明");
guide.showGridLines = false;
guide.getRange("A1:F1").merge();
guide.getRange("A1").values = [["M5-3 SEO 關鍵字研究操作說明"]];
guide.getRange("A3:A7").values = [["1"], ["2"], ["3"], ["4"], ["5"]];
guide.getRange("B3:F7").merge(true);
guide.getRange("B3:B7").values = [["先看曝光、CTR 與平均排名，找出已有曝光但點擊偏低的機會。"], ["在搜尋意圖欄選擇資訊型、導航型、商業型或交易型。"], ["把意思相近、服務同一需求的關鍵字填入同一主題群集。"], ["依品牌目標與現有內容判斷高、中、低優先序。"], ["完成後帶入 M5-3 聚類 Prompt，再人工檢查 AI 分組是否合理。"]];
guide.getRange("A1:F1").format = { fill: "#C9963A", font: { bold: true, color: "#FFFFFF", size: 17 }, rowHeight: 34 };
guide.getRange("A3:A7").format = { fill: "#2C2B28", font: { bold: true, color: "#FFFFFF" }, horizontalAlignment: "center", verticalAlignment: "center", rowHeight: 44 };
guide.getRange("B3:F7").format = { fill: "#F5F3EE", font: { size: 11 }, wrapText: true, verticalAlignment: "center", rowHeight: 44 };
guide.getRange("A:A").format.columnWidth = 8;
guide.getRange("B:F").format.columnWidth = 18;

const preview = await wb.render({ sheetName: "關鍵字研究", range: `A1:I${rows.length + 4}`, scale: 1.2, format: "png" });
await fs.mkdir(new URL("assets/downloads/qa/", root), { recursive: true });
await fs.writeFile(new URL("assets/downloads/qa/seo-workbook.png", root), new Uint8Array(await preview.arrayBuffer()));
const out = await SpreadsheetFile.exportXlsx(wb);
await out.save(outPath);
console.log(`built ${outPath} with ${rows.length} keywords`);
