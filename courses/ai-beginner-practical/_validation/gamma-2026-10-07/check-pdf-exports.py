"""Verify actual Gamma PDFs against the text sent to Gamma, page by page.

This does not replace rendering and visual inspection of all pages.
"""
from pathlib import Path
import hashlib
import json
import re
import unicodedata
import pdfplumber

ROOT = Path(__file__).resolve().parent


def normalized(text):
    # Layout edits split roles with line breaks instead of semicolons.
    return re.sub(r"[\s;；•]", "", unicodedata.normalize("NFKC", text))


results = []
for case in ("case-a", "case-b"):
    pdf_path = ROOT / f"{case}-gamma-export.pdf"
    blocks = re.split(r"^---\s*$", (ROOT / f"{case}-gamma-text-stage2.txt").read_text(), flags=re.M)
    assert len(blocks) == 10
    with pdfplumber.open(pdf_path) as pdf:
        assert len(pdf.pages) == 10, (case, len(pdf.pages))
        page_texts = [page.extract_text(use_text_flow=True) or "" for page in pdf.pages]
        omissions = []
        for page_no, (block, rendered) in enumerate(zip(blocks, page_texts), 1):
            lines = [line.strip().lstrip("- ") for line in block.splitlines() if line.strip()]
            assert re.match(rf"第{page_no}頁：", lines[0]), (case, page_no)
            for line in lines[1:]:
                if normalized(line) not in normalized(rendered):
                    omissions.append({"page": page_no, "text": line})
        assert not omissions, (case, omissions)
        if case == "case-a":
            assert normalized("同申請人、同日、同項目、同金額的重複紀錄，以及金額小於10元的紀錄") in normalized(page_texts[4])
            for week in range(1, 5):
                assert normalized(f"第{week}週") in normalized(page_texts[6])
        else:
            assert normalized("兩位窗口暫定各每週30分鐘") in normalized(page_texts[7])
        (ROOT / f"{case}-pdf-text.json").write_text(json.dumps(page_texts, ensure_ascii=False, indent=2) + "\n")
        results.append({
            "case": case,
            "pdf": pdf_path.name,
            "sha256": hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
            "pages": len(pdf.pages),
            "text_omissions": omissions,
            "page_sizes_pts": [list(page.mediabox) for page in pdf.pages],
            "visual_inspection": "Recorded separately in PLATFORM-RUN.md; no automatic visual PASS",
        })

report = {"result": "PASS", "method": "NFKC, whitespace/semicolon/bullet removal, PDF text-flow order; every input bullet on its own page", "exports": results}
(ROOT / "pdf-checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report, ensure_ascii=False, indent=2))
