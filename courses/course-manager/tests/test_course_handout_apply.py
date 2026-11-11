import json
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

import tests.test_course_loop_runtime as runtime_fixture
from src.course_handout_apply import (build_preview, build_confirmed_preview, preflight_candidate,
                                      rebase_url, record_checks, require_preserved_controls)
from src.course_improvement_loop import LoopError, artifact
from src.course_loop_runtime import human_confirmation, work


class HandoutApplyTests(unittest.TestCase):
    def test_empty_dynamic_form_host_is_an_operation_component(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / 'original.html'
            source.write_text('<div data-gen36-form="showcase"></div><script src="forms.js"></script>')
            lost = BeautifulSoup('<script src="forms.js"></script>', 'html.parser')
            with self.assertRaisesRegex(LoopError, '動態表單容器'):
                require_preserved_controls(source, lost)
            require_preserved_controls(source, BeautifulSoup(source.read_text(), 'html.parser'))

    def setUp(self):
        self.f = runtime_fixture.RuntimeTests()
        self.f.setUp()
        self.addCleanup(self.f.doCleanups)
        self.f.source = self.f.root / 'lesson.html'
        self.f.source.write_text('<html><head><style>p{color:black}</style></head><body><h1>合成候選</h1><main class="lesson-body"><section class="lesson-section" id="start"><p>案例班數2。</p></section></main><script>void 0;</script></body></html>')
        self.f.spec['units'][0]['source'] = str(self.f.source)
        self.f.start()
        self.row = work(self.f.run, 8, self.f.transport)['units'][0]
        self.state = self.f.run / 'units/CH1/state.json'
        self.mapping = self.f.root / 'mapping.json'
        self.mapping.write_text(json.dumps({'task_scope':'content-change','reason':'測試套用','intro_id':'start','sections':{}}))

    def confirm(self):
        feedback = self.f.root / 'human.md'; feedback.write_text('合成測試認可，不是真實教材回饋。')
        human_confirmation(self.f.run,'CH1',feedback,self.row['candidate']['sha256'],self.row['child_revision'],'合成測試')

    def test_h3_required_before_any_output(self):
        with self.assertRaises(LoopError):
            build_preview(self.state,self.mapping,self.f.root/'preview')
        self.assertFalse((self.f.root/'preview').exists())

    def test_preflight_reports_h1_and_preserved_components_before_h3(self):
        self.f.source.write_text('<html><body><h1>合成候選</h1><main class="lesson-body">'
                                 '<section class="lesson-section"><div class="card"><img src="a.png">'
                                 '<button>操作</button></div></section></main></body></html>')
        candidate = self.f.root / 'candidate.md'
        candidate.write_text('# 合成候選\n\n## 操作\n\n一段說明。\n')
        report_path = self.f.root / 'preflight.json'
        result = preflight_candidate(self.f.source, candidate, report_path)
        self.assertEqual(result['status'], 'passed')
        self.assertEqual(result['protected_component_counts']['cards'], 1)
        self.assertEqual(result['protected_component_counts']['images'], 1)
        self.assertTrue(result['layout_mapping_required'])
        self.assertFalse(result['preview_created'])
        self.assertFalse(result['h3_confirmed'])
        self.assertTrue(report_path.is_file())
        self.assertFalse((self.f.root / 'preview').exists())

        candidate.write_text('# 兩小時工作坊｜合成候選\n\n## 操作\n\n一段說明。\n')
        mismatch = preflight_candidate(self.f.source, candidate, self.f.root / 'mismatch.json')
        self.assertEqual(mismatch['status'], 'blocked')
        self.assertIn('h1_mismatch', [item['code'] for item in mismatch['findings']])

    def test_preview_preserves_shell_and_does_not_modify_state(self):
        self.confirm()
        before = self.state.read_bytes(); source = self.f.source.read_bytes()
        result = build_preview(self.state,self.mapping,self.f.root/'preview')
        soup = BeautifulSoup(Path(result['preview']['path']).read_text(),'html.parser')
        self.assertEqual(soup.style.string,'p{color:black}')
        self.assertEqual(soup.script.string,'void 0;')
        self.assertIn('原因已補',soup.select_one('.lesson-body').get_text())
        self.assertEqual(self.state.read_bytes(),before)
        self.assertEqual(self.f.source.read_bytes(),source)
        with self.assertRaises(LoopError):
            build_preview(self.state,self.mapping,self.f.root/'preview')

    def test_changed_source_rejected(self):
        self.confirm(); self.f.source.write_text('changed')
        with self.assertRaises(LoopError):
            build_preview(self.state,self.mapping,self.f.root/'preview')

    def test_readiness_requires_bound_checks(self):
        self.confirm(); output = self.f.root/'preview'
        manifest = build_preview(self.state,self.mapping,output)
        evidence = self.f.root/'checks.json'
        data = {'status':'pass','preview_sha256':manifest['preview']['sha256'],
                'content':True,'interaction':True,'viewports':[],'screenshots':[]}
        evidence.write_text(json.dumps(data))
        with self.assertRaises(LoopError): record_checks(output,evidence)
        proof = self.f.root/'synthetic-proof.txt'; proof.write_text('合成測試證據，非真實畫面。')
        data.update(viewports=[{'width':w,'overflow':False} for w in (390,820,1440)],screenshots=[artifact(proof)])
        evidence.write_text(json.dumps(data))
        self.assertEqual(record_checks(output,evidence)['status'],'preview_ready_for_review')
        Path(manifest['preview']['path']).write_text('changed')
        with self.assertRaises(LoopError): record_checks(output,evidence)

    def test_local_destination_preserved(self):
        self.assertEqual(rebase_url('../course/a.html#x',Path('/site/old'),Path('/site/preview')),'../course/a.html#x')
        self.assertEqual(rebase_url('https://example.com/a',Path('/site'),Path('/site/preview')),'https://example.com/a')

    def extension_inputs(self):
        source = self.f.root / 'extension.html'
        source.write_text('<html><head></head><body><h1>追加</h1><p class="tagline">舊導言</p>'
                          '<div class="lesson-body"><section class="lesson-section"><div class="section-eyebrow">01</div>'
                          '<h2>舊標題</h2><a href="material.md" target="_blank" rel="noopener">素材</a><div class="full-prompt-wrap"><pre id="prompt">既有提示詞</pre>'
                          '<button data-target="prompt">複製</button></div></section></div><nav>導覽</nav><script>void 0;</script></body></html>')
        candidate = self.f.root / 'extension.md'
        candidate.write_text('# 追加\n\n新導言[素材](material.md)\n\n## 操作\n\n1. 第一項\n2. 第二項\n\n| 句子 | 來源 |\n|---|---|\n| 甲 | A |\n\n```text\n既有提示詞\n```\n')
        feedback = self.f.root / 'extension-feedback.md'; feedback.write_text('確認接受追加候選，僅供隔離預覽。')
        receipt = self.f.root / 'confirmation.json'
        receipt.write_text(json.dumps({'schema_version':'handout-confirmation-1','status':'confirmed',
                                      'actor':'合成測試','source':artifact(source),'candidate':artifact(candidate),
                                      'feedback':artifact(feedback)}))
        mapping = self.f.root / 'extension-mapping.json'
        mapping.write_text(json.dumps({'task_scope':'content-change','reason':'驗證追加候選',
                                      'groups':{'intro':{'selector':'.tagline','mode':'intro'},
                                                '操作':{'selector':'.lesson-section','mode':'section','id':'operation'}}}))
        return source, candidate, receipt, mapping

    def test_extension_keeps_wrappers_controls_list_and_table(self):
        source, candidate, receipt, mapping = self.extension_inputs()
        before = source.read_bytes(); state_before = self.state.read_bytes()
        result = build_confirmed_preview(receipt,mapping,self.f.root/'extension-preview')
        soup = BeautifulSoup(Path(result['preview']['path']).read_text(),'html.parser')
        self.assertEqual(len(soup.select('.lesson-body > .lesson-section')),1)
        self.assertEqual(soup.select_one('.section-eyebrow').text,'01')
        self.assertEqual(len(soup.select('ol li')),2)
        self.assertEqual(soup.select_one('table td').text,'甲')
        self.assertEqual(soup.select_one('.full-prompt-wrap button')['data-target'],'prompt')
        self.assertEqual(soup.nav.text,'導覽')
        self.assertEqual(soup.select_one('a')['target'],'_blank')
        self.assertEqual(source.read_bytes(),before)
        self.assertEqual(self.state.read_bytes(),state_before)

    def test_extension_cannot_drop_empty_showcase_container(self):
        source, candidate, receipt, mapping = self.extension_inputs()
        source.write_text(source.read_text().replace('</section>', '<div data-gen36-form="showcase"></div></section>'))
        data = json.loads(receipt.read_text()); data['source'] = artifact(source)
        receipt.write_text(json.dumps(data))
        output = self.f.root / 'lost-showcase'
        with self.assertRaisesRegex(LoopError, '動態表單容器'):
            build_confirmed_preview(receipt, mapping, output)
        self.assertFalse(output.exists())
        plan = json.loads(mapping.read_text())
        plan.update(extended_blocks=True, preserve_dom=['[data-gen36-form="showcase"]'])
        mapping.write_text(json.dumps(plan))
        result = build_confirmed_preview(receipt, mapping, output)
        soup = BeautifulSoup(Path(result['preview']['path']).read_text(), 'html.parser')
        self.assertIsNotNone(soup.select_one('[data-gen36-form="showcase"]'))

    def test_extension_rejects_changed_confirmation_inputs(self):
        source, candidate, receipt, mapping = self.extension_inputs()
        candidate.write_text('已變更')
        with self.assertRaises(LoopError):
            build_confirmed_preview(receipt,mapping,self.f.root/'changed-preview')
        self.assertFalse((self.f.root/'changed-preview').exists())

    def test_extension_rejects_missing_block_mapping(self):
        source, candidate, receipt, mapping = self.extension_inputs()
        data=json.loads(mapping.read_text());del data['groups']['操作'];mapping.write_text(json.dumps(data))
        with self.assertRaises(LoopError):
            build_confirmed_preview(receipt,mapping,self.f.root/'incomplete-preview')

    def test_extension_requires_explicit_h3(self):
        source, candidate, receipt, mapping = self.extension_inputs()
        data=json.loads(receipt.read_text());data['status']='pending';receipt.write_text(json.dumps(data))
        with self.assertRaises(LoopError):
            build_confirmed_preview(receipt,mapping,self.f.root/'unconfirmed-preview')

    def test_intro_blocks_map_to_existing_header_without_loss(self):
        source, candidate, receipt, mapping = self.extension_inputs()
        source.write_text(source.read_text().replace('<div class="lesson-body">', '<div class="outcomes"></div><div class="agenda"></div><div class="lesson-body">'))
        candidate.write_text(candidate.read_text().replace('## 操作', '**本節完成物：**完整作品。\n\n本節順序。\n\n1. 操作\n\n## 操作'))
        data = json.loads(receipt.read_text()); data.update(source=artifact(source), candidate=artifact(candidate)); receipt.write_text(json.dumps(data))
        plan = json.loads(mapping.read_text())
        plan['intro_groups'] = {'intro':[0], 'header-outcomes':[1], 'header-agenda':[2,3]}
        plan['groups'] = {'intro':plan['groups']['intro'], 'header-outcomes':{'selector':'.outcomes','mode':'outcomes','markdown_label':'本節完成物：'}, 'header-agenda':{'selector':'.agenda','mode':'agenda'}, '操作':plan['groups']['操作']}
        mapping.write_text(json.dumps(plan))
        result = build_confirmed_preview(receipt,mapping,self.f.root/'header-preview')
        soup = BeautifulSoup(Path(result['preview']['path']).read_text(),'html.parser')
        self.assertEqual(soup.select_one('.outcomes').get_text(),'本節完成物：完整作品。')
        self.assertEqual(soup.select_one('.agenda li').text,'操作')
        self.assertEqual(len(result['blocks']),len(soup.select('[data-candidate-block]')))
        plan['intro_groups']['header-agenda'] = [2]
        mapping.write_text(json.dumps(plan))
        with self.assertRaises(LoopError):
            build_confirmed_preview(receipt,mapping,self.f.root/'missing-header-preview')

    def test_extended_blocks_keep_widget_and_each_prompt_control_once(self):
        source, candidate, receipt, mapping = self.extension_inputs()
        text = source.read_text().replace('<button data-target="prompt">複製</button>',
            '<div class="policy-copy-row"><button data-policy-copy="prompt">複製</button></div>')
        text = text.replace('</section>', '<aside class="policy-case"><pre id="case">案例原文</pre>'
            '<div class="policy-copy-row"><button data-policy-copy="case">複製案例</button></div></aside>'
            '<div id="widget"><input id="date" type="date"/></div></section>')
        source.write_text(text)
        candidate.write_text(candidate.read_text() + '\n### 核對\n\n案例原文\n\n'
                             '<details><summary>先做再展開</summary>\n\n答案。\n\n</details>\n')
        data = json.loads(receipt.read_text()); data.update(source=artifact(source), candidate=artifact(candidate))
        receipt.write_text(json.dumps(data))
        plan = json.loads(mapping.read_text()); plan.update(extended_blocks=True,
            preserve_prompt_controls=True, preserve_dom=['#widget']); mapping.write_text(json.dumps(plan))
        result = build_confirmed_preview(receipt,mapping,self.f.root/'extended-preview')
        soup = BeautifulSoup(Path(result['preview']['path']).read_text(),'html.parser')
        self.assertEqual(len(soup.select('#prompt')),1)
        self.assertEqual(len(soup.select('#case')),1)
        self.assertEqual(len(soup.select('[data-policy-copy]')),2)
        self.assertEqual(soup.select_one('#date')['type'],'date')
        self.assertEqual(soup.select_one('details summary').text,'先做再展開')
