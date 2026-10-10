from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
LESSON_DIRS = [ROOT / f"part{i}" for i in range(1, 8)]
asset_links = 0
failures = []

for directory in LESSON_DIRS:
    for path in sorted(directory.glob("*.html")):
        page = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        for link in page.select('a[href^="../assets/"]'):
            asset_links += 1
            rel = set(link.get("rel", []))
            if link.get("target") != "_blank" or "noopener" not in rel:
                failures.append(f"{path.relative_to(ROOT)}: {link.get('href')}")
        for link in page.select("a.nav-btn"):
            if link.get("target") == "_blank":
                failures.append(f"{path.relative_to(ROOT)}: course navigation must stay in the same tab")

assert asset_links, "No local asset links found in lesson pages"
assert not failures, "Asset links must open safely in a new tab; course navigation must remain same-tab:\n" + "\n".join(failures)
print(f"PASS: {asset_links} learner-asset links open in a new tab; lesson navigation stays in the same tab.")
