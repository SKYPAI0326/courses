#!/usr/bin/env python3
"""Browser acceptance test for learner records and the repaired CH5 page."""

from __future__ import annotations

import json

from playwright.sync_api import sync_playwright


BASE_URL = "http://127.0.0.1:8765"
RECORD_PAGES = ("PRAC2.html", "PRAC3.html", "PRAC4.html", "CH5-1.html")


def main() -> int:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(accept_downloads=True)

        for name in RECORD_PAGES:
            page.goto(f"{BASE_URL}/{name}", wait_until="networkidle")
            assert page.locator('[contenteditable="true"]').count() > 0, name
            assert page.locator("[data-record-copy]").count() == 1, name
            assert page.locator("[data-record-download]").count() == 1, name

        page.goto(f"{BASE_URL}/PRAC2.html", wait_until="networkidle")
        field = page.locator('[contenteditable="true"]').first
        field.fill("Deep Review 保存測試")
        page.reload(wait_until="networkidle")
        assert field.inner_text() == "Deep Review 保存測試"

        with page.expect_download() as download_info:
            page.locator("[data-record-download]").click()
        download = download_info.value
        payload = json.loads(download.path().read_text(encoding="utf-8"))
        assert payload["page"] == "PRAC2.html"
        assert payload["fields"][0]["value"] == "Deep Review 保存測試"
        page.evaluate("localStorage.clear()")

        for width, height in ((390, 844), (430, 932), (820, 1180), (1440, 900)):
            page.set_viewport_size({"width": width, "height": height})
            page.goto(f"{BASE_URL}/CH5-1.html", wait_until="networkidle")
            assert page.evaluate(
                "document.documentElement.scrollWidth <= document.documentElement.clientWidth"
            ), (width, height)
            body = page.locator("body").inner_text()
            for required in ("3 張系列完稿", "L2 線稿", "局部修改", "release gate"):
                assert required in body, (width, required)

        browser.close()

    print("LEARNER RECORD BROWSER CHECK: PASS — persistence, JSON export, CH5 responsive contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
