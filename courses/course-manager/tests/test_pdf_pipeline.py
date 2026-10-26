"""Non-authoring checks: no test writes a PDF or launches PDF rendering."""
import copy
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.pdf_sources import PipelineError, prepare, load_recipe, normalize_text
from src.pdf_registry import derive_state
from src.pdf_build import apply_changes, rollback_changes, build, classify_build_error, validate_review
from src.pdf_sources import sha
from scripts.pdf_pipeline import require_browser_launch_permission


class SourceTests(unittest.TestCase):
    def test_explicit_native_fallback_preserves_source_placeholder(self):
        self.html.write_text('<main><h1>原文</h1><textarea placeholder="原始欄位提示"></textarea><select><option>選項甲</option><option>選項乙</option></select></main>')
        self.recipe['paper_fallbacks']=[{'selector':'textarea,select','mode':'print-source-values','reason':'已核對原始欄位'}]
        result=prepare(self.root,self.recipe)
        self.assertIn('原始欄位提示',result['expected_text'])
        self.assertIn('選項甲',result['expected_text'])
        self.assertIn('選項乙',result['expected_text'])

    def test_cross_course_source_requires_explicit_scope(self):
        (self.root/'related').mkdir()
        (self.root/'related/CH1.html').write_text('<main><h1>相關課原文</h1></main>')
        self.recipe['sources'][0]['path']='related/CH1.html'
        with self.assertRaises(PipelineError):prepare(self.root,self.recipe)
        self.recipe['source_courses']=['demo','related']
        self.assertIn('相關課原文',prepare(self.root,self.recipe)['expected_text'])

    def test_associated_choice_label_is_preserved(self):
        self.html.write_text('<main><h1>原文</h1><input type="checkbox" id="choice"><label for="choice">原始選項</label></main>')
        result=prepare(self.root,self.recipe)
        self.assertIn('原始選項',result['expected_text'])
        self.assertNotIn('<input',result['html'])

    def test_explicit_hidden_parameter_is_not_added_as_teaching_text(self):
        self.html.write_text('<main><h1>原文</h1><input type="hidden" value="UI_PARAMETER"></main>')
        self.recipe['paper_fallbacks']=[{'selector':'input','mode':'print-source-values','reason':'原有非可見控制參數'}]
        result=prepare(self.root,self.recipe)
        self.assertNotIn('UI_PARAMETER',result['expected_text'])
        self.assertEqual(result['transformations'][0]['action'],'omit-nonvisible-form-parameter')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'demo').mkdir()
        (self.root / 'course-manager/pdf-profiles').mkdir(parents=True)
        (self.root / 'course-manager/pdf-profiles/default.css').write_text('body{color:black}')
        self.html = self.root / 'demo/CH1.html'
        self.html.write_text('<html><head><title>第一課</title></head><body><main id="main"><h1>第一課</h1><p>原文 α 42</p><details><summary>答案</summary><p>保留答案</p></details><a href="../output/pdf/demo/book.pdf">下載</a></main></body></html>')
        self.recipe = {'schema_version': 1, 'artifact_id': 'demo-book', 'course': 'demo',
                       'output': 'output/pdf/demo/book.pdf', 'profile': 'course-manager/pdf-profiles/default.css',
                       'sources': [{'path': 'demo/CH1.html', 'selectors': ['main'],
                                    'source_url': 'https://example.org/courses/demo/CH1.html',
                                    'static_content_confirmed': True}], 'font_files': [],
                       'exclude': [], 'expand': [], 'dependencies': [], 'remote_assets': {}}

    def test_preserves_content_and_expands_details_without_editing_source(self):
        original = self.html.read_bytes()
        result = prepare(self.root, self.recipe)
        self.assertIn('保留答案', result['expected_text'])
        self.assertIn('open=""', result['html'])
        self.assertEqual(self.html.read_bytes(), original)

    def test_profile_change_invalidates_fingerprint(self):
        before = prepare(self.root, self.recipe)['fingerprint']
        (self.root / self.recipe['profile']).write_text('body{color:navy}')
        self.assertNotEqual(before, prepare(self.root, self.recipe)['fingerprint'])

    def test_document_title_uses_source_instead_of_temporary_filename(self):
        self.assertIn('<title>第一課</title>',prepare(self.root,self.recipe)['html'])

    def test_recursive_css_and_image_dependencies(self):
        (self.root / 'demo/a.css').write_text('@import "b.css";')
        (self.root / 'demo/b.css').write_text('p{background:url(image.bin)}')
        image = self.root / 'demo/image.bin'
        image.write_bytes(b'original')
        self.html.write_text(self.html.read_text().replace('</head>', '<link rel="stylesheet" href="a.css"></head>'))
        before = prepare(self.root, self.recipe)
        self.assertIn('demo/image.bin', [d['path'] for d in before['dependencies']])
        image.write_bytes(b'updated')
        self.assertNotEqual(before['fingerprint'], prepare(self.root, self.recipe)['fingerprint'])

    def test_own_output_is_not_input(self):
        result = prepare(self.root, self.recipe)
        self.assertNotIn(self.recipe['output'], [d['path'] for d in result['dependencies']])

    def test_other_library_outputs_are_links_not_cyclic_byte_inputs(self):
        other=(self.root/'output/pdf/demo/other.pdf').resolve()
        self.html.write_text(self.html.read_text().replace('</main>', '<a href="../output/pdf/demo/other.pdf">模組講義</a></main>'))
        exists,is_file=Path.exists,Path.is_file
        # Simulate an existing managed output without creating any PDF fixture.
        with patch.object(Path,'exists',lambda p:p==other or exists(p)),patch.object(Path,'is_file',lambda p:p==other or is_file(p)):
            result=prepare(self.root,self.recipe)
        self.assertNotIn('output/pdf/demo/other.pdf',[d['path'] for d in result['dependencies']])

    def test_missing_dependency_blocks(self):
        self.recipe['dependencies'] = ['demo/missing.bin']
        with self.assertRaises(PipelineError): prepare(self.root, self.recipe)

    def test_dynamic_content_is_not_assumed_static(self):
        self.recipe['sources'][0]['static_content_confirmed'] = False
        with self.assertRaises(PipelineError): prepare(self.root, self.recipe)

    def test_canvas_blocks_instead_of_inventing_fallback(self):
        self.html.write_text(self.html.read_text().replace('</main>', '<canvas></canvas></main>'))
        with self.assertRaises(PipelineError): prepare(self.root, self.recipe)

    def test_overlapping_selectors_block(self):
        self.recipe['sources'][0]['selectors'] = ['main', 'main p']
        with self.assertRaises(PipelineError): prepare(self.root, self.recipe)

    def test_removing_teaching_block_is_not_ui_transform(self):
        self.recipe['exclude'] = [{'selector': 'p', 'reason': 'UI'}]
        with self.assertRaises(PipelineError): prepare(self.root, self.recipe)

    def test_unknown_hidden_content_blocks(self):
        self.html.write_text(self.html.read_text().replace('<p>保留答案', '<p hidden>保留答案'))
        with self.assertRaises(PipelineError): prepare(self.root, self.recipe)

    def test_explicit_hidden_content_expansion_preserves_text(self):
        self.html.write_text(self.html.read_text().replace('<p>保留答案', '<p hidden>保留答案'))
        self.recipe['expand'] = [{'selector': 'p[hidden]', 'reason': '原頁答案'}]
        self.assertIn('保留答案', prepare(self.root, self.recipe)['expected_text'])

    def test_source_order_changes_fingerprint_and_local_anchor_is_remapped(self):
        second = self.root / 'demo/CH2.html'
        second.write_text('<main><h1 id="answer">第二課</h1></main>')
        self.html.write_text(self.html.read_text().replace('</main>', '<a href="CH2.html#answer">下一課</a></main>'))
        self.recipe['sources'].append({'path':'demo/CH2.html','selectors':['main'],'source_url':'https://example.org/courses/demo/CH2.html','static_content_confirmed':True})
        a = prepare(self.root, self.recipe)
        self.assertIn('href="#unit-1--answer"', a['html'])
        self.recipe['sources'].reverse()
        self.assertNotEqual(a['fingerprint'], prepare(self.root, self.recipe)['fingerprint'])

    def test_path_escape_blocks(self):
        self.recipe['sources'][0]['path'] = '../outside.html'
        with self.assertRaises(PipelineError): prepare(self.root, self.recipe)

    def test_unknown_recipe_fields_block(self):
        p = self.root / 'recipe.json'
        r = copy.deepcopy(self.recipe); r['souces'] = []
        p.write_text(json.dumps(r))
        with self.assertRaises(PipelineError): load_recipe(self.root, p)

    def test_unicode_punctuation_is_preserved(self):
        self.assertEqual(normalize_text('中 文 — α\n42'), '中文—α42')

    def test_labelled_radio_is_mechanically_removed_but_answer_text_survives(self):
        self.html.write_text(self.html.read_text().replace('</main>', '<label><input type="radio">選項原文</label></main>'))
        result=prepare(self.root,self.recipe)
        self.assertNotIn('<input',result['html'])
        self.assertIn('選項原文',result['expected_text'])

    def test_native_select_requires_explicit_source_fallback(self):
        self.html.write_text(self.html.read_text().replace('</main>', '<select><option>第一項</option><option>第二項</option></select></main>'))
        with self.assertRaises(PipelineError): prepare(self.root,self.recipe)

    def test_font_change_invalidates_fingerprint(self):
        font=self.root/'demo/font.bin'; font.write_bytes(b'font-version-1')
        self.recipe['font_files']=['demo/font.bin']
        before=prepare(self.root,self.recipe)['fingerprint']
        font.write_bytes(b'font-version-2')
        self.assertNotEqual(before,prepare(self.root,self.recipe)['fingerprint'])

    def test_unpinned_remote_image_blocks(self):
        self.html.write_text(self.html.read_text().replace('</main>', '<img src="https://example.org/image.png"></main>'))
        with self.assertRaises(PipelineError): prepare(self.root,self.recipe)

    def test_changed_remote_pin_blocks(self):
        image=self.root/'demo/image.bin'; image.write_bytes(b'version')
        self.html.write_text(self.html.read_text().replace('</main>', '<img src="https://example.org/image.png"></main>'))
        self.recipe['remote_assets']={'https://example.org/image.png':{'path':'demo/image.bin','sha256':'wrong'}}
        with self.assertRaises(PipelineError): prepare(self.root,self.recipe)

    def test_duplicate_source_id_blocks(self):
        self.html.write_text(self.html.read_text().replace('</main>', '<span id="main">重複</span></main>'))
        with self.assertRaises(PipelineError): prepare(self.root,self.recipe)

    def test_build_without_explicit_flag_cannot_create_pdf(self):
        with self.assertRaises(PipelineError): build(self.root, self.recipe, create_pdf=False)
        self.assertFalse((self.root / 'course-manager/operations/pdf-build').exists())


class StateTests(unittest.TestCase):
    def test_import_does_not_become_current_from_today_hash(self):
        self.assertEqual(derive_state({}, 'a', 'b'), 'UNVERIFIED')

    def test_hash_match_requires_verified_build(self):
        self.assertEqual(derive_state({'fingerprint':'a','pdf_sha256':'b','verified':False},'a','b'),'UNVERIFIED')

    def test_current_stale_and_tampered_output(self):
        proof={'fingerprint':'a','pdf_sha256':'b','verified':True}
        self.assertEqual(derive_state(proof,'a','b'),'CURRENT')
        self.assertEqual(derive_state(proof,'c','b'),'STALE')
        self.assertEqual(derive_state(proof,'a','c'),'UNVERIFIED')


class BrowserLaunchFailureTests(unittest.TestCase):
    def test_preflight_blocks_before_browser_launch_inside_macos_codex_sandbox(self):
        with patch.dict(os.environ,{'CODEX_SANDBOX':'seatbelt'},clear=True), \
             patch('scripts.pdf_pipeline.sys.platform','darwin'):
            with self.assertRaisesRegex(PipelineError,'BROWSER_PERMISSION_REQUIRED'):
                require_browser_launch_permission()

    def test_preflight_allows_scoped_permission_execution(self):
        with patch.dict(os.environ,{},clear=True), patch('scripts.pdf_pipeline.sys.platform','darwin'):
            self.assertIsNone(require_browser_launch_permission())

    def test_sandbox_crash_is_short_and_actionable(self):
        raw=('BrowserType.launch: Target page, context or browser has been closed\n'
             'Browser logs:\n<launched> pid=28086\n'
             '[pid=28086] exception while trying to kill process: Error: kill EPERM\n'
             '[pid=28086] <process did exit: exitCode=null, signal=SIGABRT>')
        failure=classify_build_error(RuntimeError(raw))
        self.assertEqual(failure['code'],'BROWSER_SANDBOX_BLOCKED')
        self.assertIn('正式 PDF 未變更',failure['message'])
        self.assertIn('單次必要權限',failure['message'])
        self.assertNotIn('Browser logs',failure['message'])
        self.assertEqual(failure['raw_log'],raw)

    def test_non_browser_failure_preserves_original_message(self):
        failure=classify_build_error(RuntimeError('Image failed to load'))
        self.assertEqual(failure,{'code':'BUILD_FAILED','message':'Image failed to load','raw_log':None})

    def test_failed_launch_keeps_published_pdf_and_persists_raw_log(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t).resolve()
            (root/'demo').mkdir()
            (root/'course-manager/pdf-profiles').mkdir(parents=True)
            (root/'course-manager/pdf-profiles/default.css').write_text('body{color:black}')
            (root/'demo/CH1.html').write_text('<main><h1>第一課</h1><p>原文</p></main>')
            output=root/'output/pdf/demo/book.pdf'; output.parent.mkdir(parents=True); output.write_bytes(b'published')
            recipe={'schema_version':1,'artifact_id':'demo-book','course':'demo',
                    'output':'output/pdf/demo/book.pdf','profile':'course-manager/pdf-profiles/default.css',
                    'sources':[{'path':'demo/CH1.html','selectors':['main'],
                                'source_url':'https://example.org/demo/CH1.html','static_content_confirmed':True}],
                    'font_files':[],'exclude':[],'expand':[],'dependencies':[],'remote_assets':{}}
            raw=('BrowserType.launch: Target page, context or browser has been closed\n'
                 '[pid=28086] exception while trying to kill process: Error: kill EPERM\n'
                 '[pid=28086] <process did exit: exitCode=null, signal=SIGABRT>')
            with patch('src.pdf_sources.environment',return_value={'test':'fixed'}), \
                 patch('playwright.sync_api.sync_playwright',side_effect=RuntimeError(raw)), \
                 patch('src.pdf_build.shutil.which',return_value='/opt/homebrew/bin/pdftoppm'):
                with self.assertRaisesRegex(PipelineError,'BROWSER_SANDBOX_BLOCKED') as caught:
                    build(root,recipe,create_pdf=True)
            self.assertNotIn('pid=28086',str(caught.exception))
            self.assertEqual(output.read_bytes(),b'published')
            manifests=list((root/'course-manager/operations/pdf-build').glob('demo-book-*/manifest.json'))
            self.assertEqual(len(manifests),1)
            manifest=json.loads(manifests[0].read_text())
            self.assertEqual(manifest['error_code'],'BROWSER_SANDBOX_BLOCKED')
            self.assertEqual((root/manifest['error_log']).read_text().rstrip(),raw)


class TransactionTests(unittest.TestCase):
    def test_apply_and_rollback_non_pdf_payload(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t); dest=root/'current.txt'; dest.write_bytes(b'before')
            candidate=root/'candidate.txt'; candidate.write_bytes(b'after')
            op=root/'operation'; op.mkdir()
            records=apply_changes(root, [(dest,candidate)], op)
            self.assertEqual(dest.read_bytes(), b'after')
            rollback_changes(root,records,apply=False)
            self.assertEqual(dest.read_bytes(), b'after')
            rollback_changes(root,records,apply=True)
            self.assertEqual(dest.read_bytes(), b'before')

    def test_rollback_blocks_later_edits(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t); dest=root/'current.txt'; dest.write_bytes(b'before')
            candidate=root/'candidate.txt'; candidate.write_bytes(b'after')
            op=root/'operation'; op.mkdir()
            records=apply_changes(root,[(dest,candidate)],op)
            dest.write_bytes(b'later work')
            with self.assertRaises(PipelineError): rollback_changes(root,records,apply=True)
            self.assertEqual(dest.read_bytes(),b'later work')


class ReviewGateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve()
        self.image=self.root/'page-1.bin'; self.image.write_bytes(b'non-PDF review fixture')
        self.review={'accepted':True,'pdf_sha256':'fixture-hash','reviewer':{'kind':'author','name':'unit fixture'},
                     'pages':[{'page':1,'image':'page-1.bin','sha256':sha(self.image),'reviewed':True,'issues':[]}],
                     'checks':{k:True for k in ('missing_glyphs','clipping','overlap','tables_and_code','images','links')}}

    def validate(self):
        return validate_review(self.review,'fixture-hash',1,['page-1.bin'],self.root)

    def test_complete_record_is_accepted_structurally(self): self.assertEqual(self.validate(),self.review)
    def test_blank_template_is_not_approval(self):
        self.review['accepted']=False
        with self.assertRaises(PipelineError):self.validate()
    def test_different_pdf_hash_blocks(self):
        self.review['pdf_sha256']='different'
        with self.assertRaises(PipelineError):self.validate()
    def test_missing_page_blocks(self):
        self.review['pages']=[]
        with self.assertRaises(PipelineError):self.validate()
    def test_duplicate_page_blocks(self):
        self.review['pages']*=2
        with self.assertRaises(PipelineError):self.validate()
    def test_unreviewed_page_blocks(self):
        self.review['pages'][0]['reviewed']=False
        with self.assertRaises(PipelineError):self.validate()
    def test_modified_page_image_blocks(self):
        self.image.write_bytes(b'changed image')
        with self.assertRaises(PipelineError):self.validate()
    def test_open_visual_issue_blocks(self):
        self.review['pages'][0]['issues']=['clipped table']
        with self.assertRaises(PipelineError):self.validate()
    def test_missing_quality_check_blocks(self):
        self.review['checks']['links']=False
        with self.assertRaises(PipelineError):self.validate()
    def test_unknown_reviewer_blocks(self):
        self.review['reviewer']['kind']='unspecified'
        with self.assertRaises(PipelineError):self.validate()


if __name__ == '__main__': unittest.main()
