from pathlib import Path
import hashlib,json,re,unittest
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[4]
REVIEW=ROOT/'_repair/2026-10-06/re-review'
class CourseRepairAcceptance(unittest.TestCase):
    def setUp(self):
        self.index=BeautifulSoup((ROOT/'index.html').read_text(),'html.parser')
    def test_full_catalog_visible_on_first_load(self):
        catalog=self.index.select_one('#optional-catalog')
        self.assertIsNotNone(catalog)
        self.assertTrue(catalog.has_attr('open'),'complete six-part catalog is collapsed by default')
        page_links={a.get('href') for a in catalog.select('a[href]') if re.fullmatch(r'part[1-6]/[^#?]+\.html',a.get('href',''))}
        self.assertEqual(len(page_links),40,'catalog must expose all 40 lesson links')
    def test_curriculum_map_covers_every_lesson(self):
        path=ROOT/'_source/CURRICULUM-MAP.md'
        self.assertTrue(path.is_file(),'complete curriculum map is missing')
        section=path.read_text().split('## 全部 40 單元：用途、先修與交付',1)[1]
        entries=re.findall(r'`(part[1-6]/[^`]+\.html)`',section.split('## 已識別的內容銜接與待修缺口',1)[0])
        expected={p.relative_to(ROOT).as_posix() for p in ROOT.glob('part*/*.html')}
        self.assertEqual(len(entries),40,'curriculum map must contain exactly 40 lesson entries')
        self.assertEqual(set(entries),expected,'curriculum map must classify every lesson exactly once')
    def test_prompt_lesson_teaches_prompt_parts_and_revision(self):
        ch12=(ROOT/'_source/fragments/part1-CH1-2.fragment').read_text()
        ch13=(ROOT/'_source/fragments/part1-CH1-3.fragment').read_text()
        for label in ['情境','任務','輸入','規則','例外','輸出','驗收']:
            self.assertIn(label,ch12,f'CH1-2 does not teach prompt element: {label}')
        self.assertIn('改一條',ch12,'CH1-2 must teach a controlled prompt revision')
        self.assertIn('只改一條',ch13,'CH1-3 must connect a prompt edit to a test')
        budget=(ROOT/'_source/fragments/part2-PRAC2-1.fragment').read_text()
        meeting=(ROOT/'_source/fragments/part6-PRAC6-1.fragment').read_text()
        self.assertIn('缺資料不是 0 元',budget)
        self.assertIn('不要猜期限或責任人',meeting)
        self.assertTrue((ROOT/'_source/fragments/part2-PRAC2-1.fragment').is_file())
        page=BeautifulSoup((ROOT/'part1/CH1-3.html').read_text(),'html.parser')
        self.assertEqual(page.select_one('#prompt-timer').get_text(),(ROOT/'assets/materials/prompt-timer.txt').read_text().rstrip('\n'))

    def test_original_lesson_content_is_not_hidden_by_default(self):
        hidden=[]
        for p in sorted(ROOT.glob('part*/*.html')):
            soup=BeautifulSoup(p.read_text(),'html.parser')
            legacy=soup.select_one('#legacy-reference')
            if legacy and not legacy.has_attr('open'): hidden.append(p.relative_to(ROOT).as_posix())
        self.assertEqual(hidden,[],'original lesson bodies are hidden in: '+', '.join(hidden))
    def test_catalog_cards_show_course_role(self):
        catalog=self.index.select_one('#optional-catalog')
        cards=catalog.select('a[href]')
        self.assertEqual(len(cards),40)
        self.assertTrue(all(a.select_one('.course-role-badge') is not None for a in cards),'some catalog cards lack a learning-role label')
        self.assertTrue(all(a.get('data-learning-role') in ['core','extension','reference'] for a in cards))

    def test_every_noncore_page_has_nonempty_role_guidance(self):
        for p in sorted(ROOT.glob('part*/*.html')):
            soup=BeautifulSoup(p.read_text(),'html.parser')
            hero=soup.select_one('.lesson-hero')
            if not hero or hero.get('data-learning-role')=='core': continue
            banner=soup.select_one('#core-route-banner')
            self.assertIsNotNone(banner,p.relative_to(ROOT).as_posix())
            guidance=banner.select_one('p.body-text')
            self.assertIsNotNone(guidance,p.relative_to(ROOT).as_posix())
            self.assertTrue(guidance.get_text(' ',strip=True),p.relative_to(ROOT).as_posix())

    def test_core_jumps_explain_the_learning_bridge(self):
        kpi=BeautifulSoup((ROOT/'part3/PRAC3-3.html').read_text(),'html.parser')
        meeting=BeautifulSoup((ROOT/'part6/PRAC6-1.html').read_text(),'html.parser')
        self.assertTrue(kpi.select_one('.lesson-body a[href*="part6/CH6-1.html"]'),'KPI-to-meeting bridge is missing')
        self.assertTrue(meeting.select_one('.lesson-body a[href*="part4/CH4-1.html"]'),'meeting-to-delivery bridge is missing')

    def test_budget_case_mismatch_is_explained(self):
        frag=(ROOT/'_source/fragments/part2-PRAC2-1.fragment').read_text()
        self.assertIn('專案工時報價計算器',frag)
        self.assertIn('不能用它通過本課預算驗收',frag)

    def test_original_body_text_is_preserved(self):
        baseline=json.loads((REVIEW/'baseline.json').read_text())
        by_path={x['path']:x for x in baseline['html_files']}
        corrections=json.loads((REVIEW/'technical-corrections.json').read_text())['corrections']
        allowed={}
        for item in corrections:
            if item['scope']=='legacy':
                allowed.setdefault(item['path'],[]).append(item)
        changed=[]
        for p in sorted(ROOT.glob('part*/*.html')):
            soup=BeautifulSoup(p.read_text(),'html.parser'); legacy=soup.select_one('#legacy-reference')
            if not legacy: continue
            summary=legacy.find('summary',recursive=False)
            if summary: summary.decompose()
            text=' '.join(legacy.get_text(' ',strip=True).split())
            for correction in allowed.get(p.relative_to(ROOT).as_posix(),[]):
                after=correction['after_text']; before=correction['before_text']
                count=text.count(after)
                if count!=1:
                    changed.append(p.relative_to(ROOT).as_posix()+f' [allowlist mismatch: {count}]')
                    continue
                text=text.replace(after,before,1)
            digest=hashlib.sha256(text.encode()).hexdigest()
            if digest!=by_path[p.relative_to(ROOT).as_posix()]['legacy_text_sha256']: changed.append(p.relative_to(ROOT).as_posix())
        self.assertEqual(changed,[],'original instructional text differs outside the exact correction allowlist: '+', '.join(changed))
    def test_technical_corrections_are_source_backed(self):
        corrections=json.loads((REVIEW/'technical-corrections.json').read_text())
        self.assertEqual(corrections['checked_on'],'2026-10-06')
        self.assertEqual(len(corrections['canvas_pages']),13)
        self.assertEqual(len(corrections['corrections']),70)
        self.assertTrue(all(item['source'].startswith(('https://ai.google.dev/','https://support.google.com/','https://docs.railway.com/','https://docs.github.com/')) for item in corrections['corrections']))
        for path in corrections['canvas_pages']:
            text=BeautifulSoup((ROOT/path).read_text(),'html.parser').select_one('#legacy-reference').get_text(' ',strip=True)
            self.assertIn('新增檔案',text,path)
            self.assertNotIn('右上角切換到 Canvas',text,path)
    def test_publish_privacy_guidance_distinguishes_share_from_deployment(self):
        page=BeautifulSoup((ROOT/'part6/CH6-2.html').read_text(),'html.parser')
        legacy=page.select_one('#legacy-reference')
        text=legacy.get_text(' ',strip=True)
        self.assertIn('不宜當作所有目前帳號與發布情境的隱私保證',text)
        self.assertIn('未交代專案原始碼及對話紀錄的可見範圍',text)
        self.assertIn('不要單憑舊版提示推定',text)
        self.assertTrue(legacy.select_one('a[href="https://ai.google.dev/gemini-api/docs/aistudio-deploying"]'))
        self.assertTrue(legacy.select_one('a[href="https://ai.google.dev/gemini-api/docs/aistudio-build-mode"]'))
        self.assertNotIn('對話紀錄與程式碼保持私密',text)
if __name__=='__main__': unittest.main(verbosity=2)
