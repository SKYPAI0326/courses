#!/usr/bin/env python3
"""Regression tests for learner-facing content preservation.

These tests intentionally inspect the published learner pages, not the
teacher lesson plans. A lesson plan containing the missing material does not
make the learner page complete.
"""

from pathlib import Path
import unittest

from bs4 import BeautifulSoup


COURSE_DIR = Path(__file__).resolve().parents[1]


class LearnerRenderContractTests(unittest.TestCase):
    def assert_page_contains(self, unit: str, markers: list[str]) -> None:
        page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
        for marker in markers:
            with self.subTest(unit=unit, marker=marker):
                self.assertIn(marker, page)

    def assert_page_hides_production_content(self, unit: str) -> None:
        page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
        for marker in (
            "講師授課筆記",
            "Verification Asset Spec",
            "BLOCK：待建立",
            "教師需補交",
            "course_type =",
            "商業情境案例（Case）",
            "動手練習題（Hands-on Exercise）",
            "教師示範 / Demo",
            "**Search intent",
        ):
            with self.subTest(unit=unit, marker=marker):
                self.assertNotIn(marker, page)

    def test_learner_pages_do_not_expose_raw_markdown_asset_links(self) -> None:
        pages = sorted(COURSE_DIR.glob("*.html"))
        for page_path in pages:
            page = page_path.read_text(encoding="utf-8")
            with self.subTest(page=page_path.name):
                self.assertNotIn("下載原始模板（UTF-8）", page)
                self.assertNotRegex(page, r'href="assets/templates/[^\"]+\.md"')
                if 'class="asset-bundle"' in page:
                    self.assertIn('class="asset-note"', page)

    def test_every_markdown_asset_has_a_learner_html_counterpart(self) -> None:
        assets = COURSE_DIR / "assets" / "templates"
        markdown_assets = sorted(assets.glob("*.md"))
        self.assertEqual(len(markdown_assets), 126)
        for asset in markdown_assets:
            with self.subTest(asset=asset.name):
                self.assertTrue(asset.with_suffix(".html").exists())

    def test_asset_pages_offer_html_work_downloads_and_favicon(self) -> None:
        self.assertTrue((COURSE_DIR / "assets" / "favicon.svg").exists())
        for page_path in sorted(COURSE_DIR.glob("*.html")):
            page = page_path.read_text(encoding="utf-8")
            with self.subTest(page=page_path.name):
                self.assertIn('rel="icon"', page)
        for page_path in sorted((COURSE_DIR / "assets" / "templates").glob("*.html")):
            page = page_path.read_text(encoding="utf-8")
            with self.subTest(asset=page_path.name):
                self.assertIn('rel="icon"', page)
                if "下載 HTML 工作版" in page:
                    self.assertRegex(page, r'download="[^"]+工作版\.html"')
                else:
                    self.assertRegex(page, r'下載 HTML (?:參考包|工作版)')
                self.assertNotIn("UTF-8 原始模板", page)

    def test_learner_visible_text_does_not_require_markdown(self) -> None:
        pages = sorted(COURSE_DIR.glob("CH*.html")) + sorted(COURSE_DIR.glob("PRAC*.html"))
        pages += sorted((COURSE_DIR / "assets" / "templates").glob("*.html"))
        for page_path in pages:
            soup = BeautifulSoup(page_path.read_text(encoding="utf-8"), "html.parser")
            visible_text = soup.get_text(" ", strip=True)
            with self.subTest(page=page_path.name):
                self.assertNotIn("Markdown", visible_text)
                self.assertNotIn(".md", visible_text)
                self.assertNotIn("原始模板", visible_text)

    def test_ch5_3_preserves_teaching_flow_and_assets(self) -> None:
        self.assert_page_contains(
            "CH5-3",
            [
                "Search intent",
                "<strong>Search intent（搜尋意圖）</strong>",
                "操作示範 / Demo",
                "十三步驟示範",
                "檢查點與修復",
                "變化題",
                "assets/templates/CH5-3.html",
                "assets/templates/CH5-3.html",
            ],
        )
        self.assert_page_hides_production_content("CH5-3")

    def test_ch6_2_preserves_concepts_demo_and_assets(self) -> None:
        self.assert_page_contains(
            "CH6-2",
            [
                "方案範圍",
                "完整示範 / Demo",
                "七步驟示範",
                "檢查點與修復",
                "assets/templates/CH6-2.html",
                "assets/templates/CH6-2.html",
            ],
        )
        self.assert_page_hides_production_content("CH6-2")

    def test_m1_pages_expose_usable_material_bundles(self) -> None:
        expected_links = {
            "CH1-1": [
                "assets/templates/CH1-1-情境案例卡.html",
                "assets/templates/CH1-1-阿凱參考完成品.html",
                "assets/templates/CH1-1-判斷練習.html",
            ],
            "CH1-2": [
                "assets/templates/CH1-2.html",
                "assets/templates/CH1-2-阿凱參考完成品.html",
                "assets/templates/CH1-2-線索與分類練習.html",
            ],
            "CH1-3": [
                "assets/templates/CH1-3.html",
                "assets/templates/CH1-3-阿凱參考完成品.html",
                "assets/templates/CH1-3-價值主張檢核練習.html",
            ],
            "PRAC1": [
                "assets/templates/PRAC1.html",
                "assets/templates/PRAC1.html",
                "assets/templates/PRAC1-四種情境參考.html",
                "assets/templates/PRAC1-五科交接檢核.html",
                "assets/templates/PRAC1-整合檢核練習.html",
            ],
        }
        for unit, links in expected_links.items():
            page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
            for link in links:
                with self.subTest(unit=unit, link=link):
                    self.assertIn(link, page)

        for asset in (
            "CH1-1.md",
            "CH1-2.md",
            "CH1-3.md",
            "PRAC1.md",
            "CH1-1-情境案例卡.md",
            "CH1-1-阿凱參考完成品.md",
            "CH1-1-判斷練習.md",
            "CH1-2-阿凱參考完成品.md",
            "CH1-2-線索與分類練習.md",
            "CH1-3-阿凱參考完成品.md",
            "CH1-3-價值主張檢核練習.md",
            "PRAC1-四種情境參考.md",
            "PRAC1-五科交接檢核.md",
            "PRAC1-整合檢核練習.md",
        ):
            content = (COURSE_DIR / "assets" / "templates" / asset).read_text(encoding="utf-8-sig")
            for marker in ("對應 lesson", "課程類型", "資產狀態", "本次完成品：BLOCK", "_lessons/"):
                with self.subTest(asset=asset, marker=marker):
                    self.assertNotIn(marker, content)

    def test_m1_pages_preserve_the_learning_chain(self) -> None:
        expected_markers = {
            "CH1-1": ["兩種可能的使用情境", "選擇表的完整示例", "可重做"],
            "CH1-2": ["至少兩筆線索", "問題假設", "交給 CH1-3"],
            "CH1-3": ["價值主張", "共同訊息", "交給 PRAC1"],
            "PRAC1": ["共同 Brief 的 8 個必要欄位", "五科如何共用 Brief", "阿凱的共同專案 Brief v1", "五科交接檢查"],
        }
        for unit, markers in expected_markers.items():
            page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
            for marker in markers:
                with self.subTest(unit=unit, marker=marker):
                    self.assertIn(marker, page)

    def test_m2_core_templates_are_domain_specific(self) -> None:
        expected = {
            "CH2-1": ["四項影像任務比較", "可見證據與下一步", "AI 或素材草稿紀錄"],
            "CH2-2": ["訊息層級", "內容角度", "平台與素材限制"],
            "CH2-3": ["腳本與分鏡", "時間／序號", "轉譯版本"],
            "CH2-4": ["素材需求清單", "來源與使用條件", "AI 使用紀錄"],
            "CH2-5": ["視覺資產組", "交付資料夾", "Windows／Affinity 前測"],
            "CH2-6": ["時間軸與取捨", "替代版本", "輸出前檢查"],
            "CH2-7": ["環境前測", "專案與檔案索引", "執行與輸出檢查"],
            "PRAC2": ["README 摘要", "交付索引", "行銷判斷說明"],
        }
        for unit, markers in expected.items():
            page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
            template = (COURSE_DIR / "assets" / "templates" / f"{unit}.md").read_text(encoding="utf-8-sig")
            template_page = (COURSE_DIR / "assets" / "templates" / f"{unit}.html").read_text(encoding="utf-8")
            self.assertIn(f"assets/templates/{unit}.html", page)
            for marker in markers:
                with self.subTest(unit=unit, marker=marker):
                    self.assertIn(marker, template_page)
                    self.assertIn(marker, template)
            for marker in ("對應 lesson", "課程類型", "資產狀態", "本次完成品：BLOCK", "_lessons/"):
                with self.subTest(unit=unit, production_marker=marker):
                    self.assertNotIn(marker, template)

    def test_m2_pages_expose_operational_material_bundles(self) -> None:
        expected_links = {
            "CH2-1": ["CH2-1-四項影像任務案例卡", "CH2-1-素材來源與AI紀錄表"],
            "CH2-2": ["CH2-2-受眾與訊息案例卡"],
            "CH2-3": ["CH2-3-影像平台格式卡"],
            "CH2-4": ["CH2-4-素材來源與授權案例"],
            "CH2-5": ["CH2-5-Affinity-Windows課前檢查表", "CH2-5-視覺資產輸出檢核表"],
            "CH2-6": ["CH2-6-剪輯參考與音訊檢查"],
            "CH2-7": ["CH2-7-OpenShot-Windows課前前測", "CH2-7-短影音輸出檢核表"],
            "PRAC2": ["PRAC2-README參考完成品", "PRAC2-評量規準"],
        }
        for unit, asset_codes in expected_links.items():
            page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
            for asset_code in asset_codes:
                with self.subTest(unit=unit, asset=asset_code):
                    self.assertIn(f"assets/templates/{asset_code}.html", page)
                    self.assertIn(f"assets/templates/{asset_code}.html", page)
                    asset = (COURSE_DIR / "assets" / "templates" / f"{asset_code}.md").read_text(encoding="utf-8-sig")
                    for marker in ("對應 lesson", "課程類型", "資產狀態", "_lessons/"):
                        self.assertNotIn(marker, asset)

    def test_m3_templates_are_platform_specific(self) -> None:
        expected = {
            "CH3-1": ["平台角色比較", "內容旅程", "LINE（延伸）"],
            "CH3-2": ["定位句", "內容支柱", "表達規則"],
            "CH3-3": ["三平台版本", "版本差異判斷", "發布前檢查"],
            "CH3-4": ["兩週內容月曆", "狀態定義", "發布流程"],
            "CH3-5": ["互動紀錄", "回應設計", "安全邊界"],
            "CH3-6": ["資料字典", "內容比較", "下一輪假設"],
            "CH3-7": ["承接情境", "同意與分眾", "訊息序列"],
            "PRAC3": ["方案摘要", "交付檔案索引", "一致性檢查"],
        }
        for unit, markers in expected.items():
            page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
            template = (COURSE_DIR / "assets" / "templates" / f"{unit}.md").read_text(encoding="utf-8-sig")
            self.assertIn(f"assets/templates/{unit}.html", page)
            for marker in markers:
                with self.subTest(unit=unit, marker=marker):
                    self.assertIn(marker, template)
            for marker in ("對應 lesson", "課程類型", "資產狀態", "本次完成品：BLOCK", "_lessons/"):
                with self.subTest(unit=unit, production_marker=marker):
                    self.assertNotIn(marker, template)

    def test_m3_pages_expose_operational_material_bundles(self) -> None:
        expected_links = {
            "CH3-1": ["CH3-1-平台角色卡", "CH3-1-社群格式卡", "CH3-1-LINE名單承接與回訪情境卡"],
            "CH3-2": ["CH3-2-內容支柱案例卡", "CH3-2-社群表達規則卡"],
            "CH3-3": ["CH3-3-三平台參考完成品", "CH3-3-跨平台檢查表"],
            "CH3-4": ["CH3-4-發布前檢查表", "CH3-4-兩週月曆參考完成品"],
            "CH3-5": ["CH3-5-互動情境卡", "CH3-5-正反例回應包"],
            "CH3-6": ["CH3-6-合成資料與資料字典"],
            "CH3-7": ["CH3-7-LINE情境卡", "CH3-7-訊息序列參考"],
            "PRAC3": ["PRAC3-README參考完成品", "PRAC3-評量規準"],
        }
        for unit, asset_codes in expected_links.items():
            page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
            for asset_code in asset_codes:
                with self.subTest(unit=unit, asset=asset_code):
                    self.assertIn(f"assets/templates/{asset_code}.html", page)
                    self.assertIn(f"assets/templates/{asset_code}.html", page)
                    asset = (COURSE_DIR / "assets" / "templates" / f"{asset_code}.md").read_text(encoding="utf-8-sig")
                    for marker in ("對應 lesson", "課程類型", "資產狀態", "_lessons/"):
                        self.assertNotIn(marker, asset)

    def test_m4_templates_preserve_environment_boundaries(self) -> None:
        expected = {
            "CH4-1": ["查詢與意圖", "內容機會", "資料狀態"],
            "CH4-2": ["關鍵字群組", "優先序", "內容規劃"],
            "CH4-3": ["測試環境", "頁面訊號", "修正與復原"],
            "CH4-4": ["商業問題到資料語言", "術語對照", "Demo Account 觀察紀錄"],
            "CH4-5": ["假設", "資料範圍", "判讀與行動"],
            "CH4-6": ["事件規格", "佈建紀錄", "LocalWP 測試"],
            "CH4-7": ["四層證據", "錯誤分類", "安全停止"],
            "PRAC4": ["決策摘要", "證據矩陣", "放行條件"],
        }
        for unit, markers in expected.items():
            page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
            template = (COURSE_DIR / "assets" / "templates" / f"{unit}.md").read_text(encoding="utf-8-sig")
            self.assertIn(f"assets/templates/{unit}.html", page)
            for marker in markers:
                with self.subTest(unit=unit, marker=marker):
                    self.assertIn(marker, template)
            for marker in ("對應 lesson", "課程類型", "資產狀態", "本次完成品：BLOCK", "_lessons/"):
                with self.subTest(unit=unit, production_marker=marker):
                    self.assertNotIn(marker, template)

        prac4 = (COURSE_DIR / "assets" / "templates" / "PRAC4-SearchConsole合成資料.md").read_text(encoding="utf-8-sig")
        self.assertIn("不能在本機直接 Demo", prac4)

    def test_m4_pages_expose_environment_specific_materials(self) -> None:
        expected_links = {
            "CH4-1": ["CH4-1-術語卡", "CH4-1-SERP示例"],
            "CH4-2": ["CH4-2-查詢資料與分群參考", "CH4-2-關鍵字規劃參考完成品"],
            "CH4-3": ["CH4-3-LocalWP課前與復原檢查", "CH4-3-頁面基準檢查參考"],
            "CH4-4": ["CH4-4-GA4資料模型術語卡", "CH4-4-GA4閱讀地圖參考"],
            "CH4-5": ["CH4-5-GA4合成觀察資料", "CH4-5-GA4假設參考完成品"],
            "CH4-6": ["CH4-6-GTM事件規格卡", "CH4-6-GTM復原檢查表"],
            "CH4-7": ["CH4-7-錯誤驗證案例卡", "CH4-7-追蹤驗證參考完成品"],
            "PRAC4": ["PRAC4-SearchConsole合成資料", "PRAC4-README參考完成品", "PRAC4-評量規準"],
        }
        for unit, asset_codes in expected_links.items():
            page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
            for asset_code in asset_codes:
                with self.subTest(unit=unit, asset=asset_code):
                    self.assertIn(f"assets/templates/{asset_code}.html", page)
                    self.assertIn(f"assets/templates/{asset_code}.html", page)

    def test_m5_templates_focus_on_decision_and_guards(self) -> None:
        expected = {
            "CH5-1": ["能力與限制", "市場比較", "選擇決策"],
            "CH5-2": ["渠道任務", "預算框架", "判斷"],
            "CH5-3": ["搜尋企劃", "廣告群組", "預算與驗收"],
            "CH5-4": ["渠道任務", "受眾與素材矩陣", "測試設計"],
            "CH5-5": ["渠道比較", "LINE 承接條件", "決策"],
            "CH5-6": ["輸入假設", "三種情境", "計算與判讀"],
            "CH5-7": ["實驗設計", "第一輪結果", "第二輪決策"],
            "PRAC5": ["決策摘要", "交付檔案", "一致性與權限"],
        }
        for unit, markers in expected.items():
            page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
            template = (COURSE_DIR / "assets" / "templates" / f"{unit}.md").read_text(encoding="utf-8-sig")
            self.assertIn(f"assets/templates/{unit}.html", page)
            for marker in markers:
                with self.subTest(unit=unit, marker=marker):
                    self.assertIn(marker, template)
            for marker in ("對應 lesson", "課程類型", "資產狀態", "本次完成品：BLOCK", "_lessons/"):
                with self.subTest(unit=unit, production_marker=marker):
                    self.assertNotIn(marker, template)

    def test_m5_pages_expose_campaign_materials_without_real_spend(self) -> None:
        expected_links = {
            "CH5-1": ["CH5-1-市場卡比較示例", "CH5-1-服務能力限制卡", "CH5-1-市場選擇參考完成品"],
            "CH5-2": ["CH5-2-渠道比較卡", "CH5-2-合成渠道資料", "CH5-2-預算框架參考完成品"],
            "CH5-3": ["CH5-3-Google Ads 文案參考完成品", "CH5-3-政策與權限提醒卡"],
            "CH5-4": ["CH5-4-Meta Ads 素材矩陣參考"],
            "CH5-5": ["CH5-5-LINE Ads 渠道比較參考", "CH5-5-訊息流程卡"],
            "CH5-6": ["CH5-6-公式與單位說明卡", "CH5-6-合成預算輸入", "CH5-6-預算護欄參考"],
            "CH5-7": ["CH5-7-兩輪合成結果", "CH5-7-停止與決策卡"],
            "PRAC5": ["PRAC5-README參考完成品", "PRAC5-評量規準"],
        }
        for unit, asset_codes in expected_links.items():
            page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
            for asset_code in asset_codes:
                with self.subTest(unit=unit, asset=asset_code):
                    self.assertIn(f"assets/templates/{asset_code}.html", page)
                    self.assertIn(f"assets/templates/{asset_code}.html", page)

        for asset_code in ("CH5-3-政策與權限提醒卡", "PRAC5-README參考完成品"):
            asset = (COURSE_DIR / "assets" / "templates" / f"{asset_code}.md").read_text(encoding="utf-8-sig")
            self.assertTrue("付款" in asset or "付費" in asset)

    def test_m6_templates_integrate_upstream_evidence(self) -> None:
        expected = {
            "CH6-1": ["上游產物對照表", "共同受眾問題", "能力證據與限制"],
            "CH6-2": ["方案範圍", "交付設計", "成本與資源假設"],
            "CH6-3": ["目標讀者與閱讀任務", "能力證據排序", "30 天行動"],
            "PRAC6": ["提案主線", "證據矩陣", "交接與 30 天行動"],
        }
        for unit, markers in expected.items():
            page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
            template = (COURSE_DIR / "assets" / "templates" / f"{unit}.md").read_text(encoding="utf-8-sig")
            self.assertIn(f"assets/templates/{unit}.html", page)
            for marker in markers:
                with self.subTest(unit=unit, marker=marker):
                    self.assertIn(marker, template)
                    self.assertIn(marker, (COURSE_DIR / "assets" / "templates" / f"{unit}.html").read_text(encoding="utf-8"))
            for marker in ("對應 lesson", "課程類型", "資產狀態", "本次完成品：BLOCK", "_lessons/"):
                with self.subTest(unit=unit, production_marker=marker):
                    self.assertNotIn(marker, template)

    def test_m6_pages_expose_integration_materials(self) -> None:
        expected_links = {
            "CH6-1": ["CH6-1-四份產物摘要", "CH6-1-整合價值參考完成品", "CH6-1-同伴回饋表"],
            "CH6-2": ["CH6-2-方案層級案例卡", "CH6-2-成本假設卡", "CH6-2-同伴審查表", "CH6-2-方案參考完成品"],
            "CH6-3": ["CH6-3-作品呈現參考", "CH6-3-30天行動參考", "CH6-3-同伴回饋規則", "CH6-3-檔案索引規範"],
            "PRAC6": ["PRAC6-README參考完成品", "PRAC6-提案評量規準"],
        }
        for unit, asset_codes in expected_links.items():
            page = (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8")
            for asset_code in asset_codes:
                with self.subTest(unit=unit, asset=asset_code):
                    self.assertIn(f"assets/templates/{asset_code}.html", page)
                    self.assertIn(f"assets/templates/{asset_code}.html", page)
                    asset = (COURSE_DIR / "assets" / "templates" / f"{asset_code}.md").read_text(encoding="utf-8-sig")
                    for marker in ("對應 lesson", "課程類型", "資產狀態", "本次完成品：BLOCK", "_lessons/"):
                        self.assertNotIn(marker, asset)

    def test_core_pages_have_locatable_teaching_stages(self) -> None:
        units = sorted(
            path.stem
            for path in COURSE_DIR.glob("*.html")
            if path.stem.startswith(("CH", "PRAC"))
        )
        self.assertEqual(len(units), 40)
        for unit in units:
            page = BeautifulSoup(
                (COURSE_DIR / f"{unit}.html").read_text(encoding="utf-8"),
                "html.parser",
            )
            sections = page.select("main section.lesson-section")
            with self.subTest(unit=unit):
                self.assertGreaterEqual(len(sections), 5)


if __name__ == "__main__":
    unittest.main()
