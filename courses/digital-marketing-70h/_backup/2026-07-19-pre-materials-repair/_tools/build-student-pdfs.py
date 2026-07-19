from pathlib import Path
import html
import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "downloads"
FONT = "/Library/Fonts/Arial Unicode.ttf"
pdfmetrics.registerFont(TTFont("CourseCJK", FONT))

SOURCES = [
    (ROOT / "assets" / "after-class-guide.md", OUT / "回家30分鐘復跑手冊.pdf", "課後操作手冊"),
    (ROOT / "assets" / "datasets" / "prompts-all.md", OUT / "全課程Prompt工具箱.pdf", "Prompt 參考工具箱"),
    (ROOT / "assets" / "datasets" / "persona-templates.md", OUT / "Persona樣板與練習表.pdf", "Persona 練習素材"),
]

TITLE_OVERRIDES = {
    "after-class-guide.md": "回家 30 分鐘復跑手冊",
    "prompts-all.md": "全課程 Prompt 工具箱",
    "persona-templates.md": "Persona 樣板與練習表",
}


def normalize(text):
    text = html.unescape(text).replace(".md 檔", "可編輯文件").replace(".md", "文件")
    return re.sub(r"^\*(.+)\*$", r"\1", text)


def inline(text):
    text = html.escape(normalize(text))
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`(.*?)`", r"<font backColor='#F5F3EE'>\1</font>", text)
    return text


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("CourseCJK", 8)
    canvas.setFillColor(colors.HexColor("#77736C"))
    canvas.drawString(18 * mm, 10 * mm, "弄一下工作室｜數位行銷人才培訓")
    canvas.drawRightString(192 * mm, 10 * mm, f"{doc.page}")
    canvas.restoreState()


def build(source, target, label):
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("title", parent=base["Title"], fontName="CourseCJK", fontSize=24, leading=31, textColor=colors.HexColor("#2C2B28"), alignment=TA_CENTER, spaceAfter=5 * mm),
        "sub": ParagraphStyle("sub", parent=base["Normal"], fontName="CourseCJK", fontSize=9.5, leading=14, textColor=colors.HexColor("#77736C"), alignment=TA_CENTER, spaceAfter=8 * mm),
        "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName="CourseCJK", fontSize=16, leading=22, textColor=colors.HexColor("#B27E24"), spaceBefore=6 * mm, spaceAfter=2.5 * mm),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="CourseCJK", fontSize=13, leading=18, textColor=colors.HexColor("#2C2B28"), spaceBefore=5 * mm, spaceAfter=2 * mm),
        "h3": ParagraphStyle("h3", parent=base["Heading3"], fontName="CourseCJK", fontSize=11, leading=16, textColor=colors.HexColor("#5B503F"), spaceBefore=3 * mm, spaceAfter=1.5 * mm),
        "body": ParagraphStyle("body", parent=base["BodyText"], fontName="CourseCJK", fontSize=9.5, leading=15, textColor=colors.HexColor("#2C2B28"), spaceAfter=2.2 * mm),
        "bullet": ParagraphStyle("bullet", parent=base["BodyText"], fontName="CourseCJK", fontSize=9.5, leading=15, leftIndent=5 * mm, firstLineIndent=-3 * mm, spaceAfter=1.4 * mm),
        "code": ParagraphStyle("code", parent=base["Code"], fontName="CourseCJK", fontSize=7.8, leading=11, leftIndent=3 * mm, rightIndent=3 * mm, backColor=colors.HexColor("#F5F3EE"), borderPadding=4 * mm, spaceBefore=1.5 * mm, spaceAfter=3 * mm),
    }
    lines = source.read_text(encoding="utf-8").splitlines()
    title = TITLE_OVERRIDES.get(source.name, re.sub(r"^#\s+", "", lines[0]))
    story = [Paragraph(inline(title), styles["title"]), Paragraph(inline(f"{label}｜PDF 可搜尋、複製與列印"), styles["sub"])]
    in_code = False
    code = []
    i = 1
    while i < len(lines):
        line = normalize(lines[i])
        if line.strip().startswith("```"):
            if in_code:
                story.append(Preformatted("\n".join(code), styles["code"], maxLineLength=90))
                code = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code.append(line)
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [normalize(c.strip()) for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
                    rows.append([Paragraph(inline(c), styles["body"]) for c in cells])
                i += 1
            if rows:
                table = Table(rows, repeatRows=1, hAlign="LEFT")
                table.setStyle(TableStyle([
                    ("FONTNAME", (0, 0), (-1, -1), "CourseCJK"),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9E2D5")),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D8D4CB")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]))
                story.append(table)
                story.append(Spacer(1, 3 * mm))
            continue
        heading = re.match(r"^(#{2,4})\s+(.*)$", line)
        if heading:
            key = {2: "h1", 3: "h2", 4: "h3"}[len(heading.group(1))]
            story.append(Paragraph(inline(heading.group(2)), styles[key]))
        elif re.match(r"^[-*]\s+", line):
            story.append(Paragraph("• " + inline(re.sub(r"^[-*]\s+", "", line)), styles["bullet"]))
        elif re.match(r"^\d+\.\s+", line):
            marker, text = re.match(r"^(\d+\.)\s+(.*)$", line).groups()
            story.append(Paragraph(inline(marker + " " + text), styles["bullet"]))
        elif line.startswith(">"):
            story.append(Paragraph(inline(re.sub(r"^>\s?", "", line)), styles["bullet"]))
        elif line.strip() in ("", "---"):
            if line.strip() == "---":
                story.append(Spacer(1, 2 * mm))
        else:
            story.append(Paragraph(inline(line), styles["body"]))
        i += 1
    doc = SimpleDocTemplate(str(target), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=18 * mm, bottomMargin=17 * mm, title=title, author="弄一下工作室")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"built {target}")


for source, target, label in SOURCES:
    build(source, target, label)
