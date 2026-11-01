import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.course_copy_profile import copy_spec, copy_course_spec
from src.course_improvement_loop import LoopError, read_json
from src.course_loop_executor import build_prompt, response_schema
from src.course_loop_runtime import prepare
from src.course_loop_review import missing_required_text
from src.course_loop_stages import create_stage, next_task, validate_copy_reading_audit, validate_copy_reading_decision
from src.course_copy_readability import validate_readability


class CopyProfileTests(unittest.TestCase):
    def test_course_manifest_keeps_every_unit_and_one_explicit_budget(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for name in ('CH1', 'CH2'):
                (root / (name + '.md')).write_text('# ' + name + '\n既有內容。')
            manifest = root / 'course.json'
            data = {'id': 'copy-course', 'max_model_calls': 8, 'units': [
                {'id': name, 'title': name, 'purpose': '讀懂既有案例', 'source': name + '.md'}
                for name in ('CH1', 'CH2')]}
            manifest.write_text(json.dumps(data))
            spec = copy_course_spec(manifest)
            self.assertEqual([u['id'] for u in spec['units']], ['CH1', 'CH2'])
            self.assertEqual(spec['limits']['max_model_calls'], 8)
            prepare(spec, root / 'run')
            for name in ('CH1', 'CH2'):
                self.assertTrue((root / 'run/units' / name / 'original.md').exists())
            result = subprocess.run([sys.executable, 'scripts/course_copy_loop.py',
                '--course-manifest', str(manifest), '--run', str(root / 'cli-run')], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertEqual(json.loads(result.stdout)['model_calls'], 0)
            data.pop('max_model_calls'); manifest.write_text(json.dumps(data))
            with self.assertRaisesRegex(LoopError, '總額'):
                copy_course_spec(manifest)

    def test_html_protected_blocks_and_existing_controller(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "lesson.html"
            source.write_text('<h1>講義</h1><pre><code>x &lt; 3</code></pre>')
            spec = copy_spec(source, "CH1", "講義", "理解既有案例", keep=["既有數字"])
            checks = spec["units"][0]["checks"]
            self.assertEqual(checks[1]["texts"], ["x < 3", "既有數字"])
            self.assertEqual(missing_required_text(source, ["x < 3"]), [])
            self.assertEqual(missing_required_text(source, ["x < 4"]), ["x < 4"])
            self.assertTrue(all(Path(p).exists() for p in spec["rules"]))
            self.assertTrue(any(p.endswith('course-copy-profile-v0.6.md') for p in spec['rules']))
            run = Path(td) / "run"
            result = prepare(spec, run)
            self.assertEqual(result["model_calls"], 0)
            self.assertFalse(result["dispatch_enabled"])
            self.assertEqual((run / "units/CH1/original.html").read_text(), source.read_text())
            config = read_json(run / "units/CH1/config.json")
            self.assertEqual(config["profile"], "copy-v0.6")
            self.assertEqual(config["citation_contract"], "locations-v1")
            state = run / "units/CH1/state.json"
            create_stage(config, state)
            task = next_task(state)
            self.assertEqual(task["profile"], "copy-v0.6")
            self.assertIn("主要教學段落", task["instructions"])
            with self.assertRaises(LoopError):
                prepare(spec, run)

    def test_markdown_code_is_preserved(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / 'lesson.md'
            source.write_text('# 文案\n```python\nx = 3\n```\n~~~text\n既有提示詞\n~~~\n')
            spec = copy_spec(source, 'CH1', '標題', '用途')
            self.assertEqual(spec['units'][0]['checks'][1]['texts'], ['x = 3', '既有提示詞'])
            self.assertEqual(spec['limits']['max_model_calls'], 8)
            self.assertNotEqual(spec['roles']['writer'], spec['roles']['reviewer'])

    def test_v06_restatement_and_four_dimensions_are_enforced(self):
        import copy
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / 'candidate.md'
            source.write_text('摘要寫到日期時，記下它出自哪則消息，讓接手者能回去確認。')
            task = {'target': {'path': str(source)}}
            passage = {'quote': source.read_text(), 'reader_understanding': '記錄日期的消息出處供查核。',
                       'remaining_gap': '', 'problem_id': None,
                       'plain_restatement': '寫日期時一起記下消息出處，別人才能查。',
                       'support_quotes': [source.read_text()], 'added_background': '',
                       **{key: {'verdict': 'supported', 'explanation': '正文說清楚日期、出處與接手者查核的關係。'}
                          for key in ('referents', 'reason_placement', 'reading_load')}}
            response = {'reading_decision': {'verdict': 'supported', 'explanation': '理解與理由明確。', 'passages': [passage]},
                        'evaluation': {'problems': [], 'grades': {'B': {'level': 'L3', 'problems': []}}}}
            validate_copy_reading_decision(task, validate_readability(task, response))
            self.assertIn('plain_restatement', response['reading_decision']['passages'][0])
            for field in ('plain_restatement', 'support_quotes', 'added_background', 'referents', 'reason_placement', 'reading_load'):
                bad = copy.deepcopy(response); del bad['reading_decision']['passages'][0][field]
                with self.subTest(missing=field), self.assertRaisesRegex(LoopError, '缺少四項'):
                    validate_readability(task, bad)
            for field in ('added_background', 'referents', 'reason_placement', 'reading_load'):
                bad = copy.deepcopy(response); row = bad['reading_decision']['passages'][0]
                if field == 'added_background': row[field] = '我自行假設有主管核准。'
                else: row[field]['verdict'] = 'gap'
                with self.subTest(contradiction=field), self.assertRaisesRegex(LoopError, '不得省略remaining_gap'):
                    validate_readability(task, bad)
            bad = copy.deepcopy(response); bad['reading_decision']['passages'][0]['support_quotes'] = ['其他來源才寫的背景']
            with self.assertRaisesRegex(LoopError, '目前正文'):
                validate_readability(task, bad)

    def test_reading_gap_cannot_be_graded_b_l3(self):
        with tempfile.TemporaryDirectory() as td:
            candidate = Path(td) / 'candidate.md'
            candidate.write_text('# 講義\n## 任務\n打開素材並完成表格。\n', encoding='utf-8')
            response = {"reading_audit": {"sections": [{"heading": "任務", "quote": "打開素材並完成表格。",
                "reader_understanding": "讀者只知道要填表", "continuity": "未說明素材與表格的關係",
                "verdict": "gap"}], "overall": "gap"},
                "evaluation": {"grades": {"B": {"level": "L3", "problems": []}}}}
            with self.assertRaisesRegex(LoopError, "不得給B L3"):
                validate_copy_reading_audit({"target": {"path": str(candidate)}}, response)
            response["evaluation"]["grades"]["B"] = {"level": "L1", "problems": ["P1"]}
            validate_copy_reading_audit({"target": {"path": str(candidate)}}, response)
            candidate.write_text(candidate.read_text() + '## 後續\n檢查來源再寄出。\n', encoding='utf-8')
            with self.assertRaisesRegex(LoopError, "逐一覆蓋主要區段"):
                validate_copy_reading_audit({"target": {"path": str(candidate)}}, response)

    def test_v04_uses_prose_review_without_reading_audit(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "source.md"
            candidate = Path(td) / "candidate.md"
            source.write_text("原稿", encoding="utf-8")
            candidate.write_text("候選正文", encoding="utf-8")
            task = {"id": "copy-compare", "phase": "compare", "profile": "copy-v0.4", "purpose": "學員理解案例",
                    "instructions": "引用主要承載教學的完整連續段落", "assignment": {},
                    "target": {"path": str(candidate)}, "current_evaluation": {},
                    "candidate_usage": 1, "candidate_limit": 2,
                    "allowed_inputs": {"source": {"path": str(source), "sha256": "source"},
                                       "candidate": {"path": str(candidate), "sha256": "candidate"}}}
            self.assertNotIn("reading_audit", response_schema(task)["required"])
            prompt = build_prompt(task, 10000)
            self.assertNotIn("reading_audit", prompt)
            self.assertIn("完整連續段落", prompt)
            self.assertLess(prompt.index('"id": "candidate"'), prompt.index('"id": "source"'))
            self.assertLess(prompt.index('"id": "candidate"'), prompt.index('"current_evaluation"'))

    def test_cli_prepares_only_and_rejects_binary(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / 'lesson.md'; source.write_text('# 既有講義\n段落待改善。')
            p = subprocess.run([sys.executable, 'scripts/course_copy_loop.py', '--source', str(source),
                                '--unit', 'CH1', '--title', '講義', '--purpose', '閱讀既有案例',
                                '--run', str(Path(td) / 'run')], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(json.loads(p.stdout)['model_calls'], 0)
            with self.assertRaises(LoopError):
                copy_spec(Path(td) / 'lesson.pdf', 'CH1', '標題', '用途')

    def test_v05_rejects_missing_fabricated_and_contradictory_reading_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / 'candidate.md'
            source.write_text('這是撤除逐列提示的整合練習，舊包用來驗證來源重查。')
            task = {'target': {'path': str(source)}}
            response = {'evaluation': {'problems': [{'id': 'P1', 'open': True}],
                        'grades': {'B': {'level': 'L3', 'problems': ['P1']}}}}
            with self.assertRaisesRegex(LoopError, '缺少reading_decision'):
                validate_copy_reading_decision(task, response)
            response['reading_decision'] = {'verdict': 'gap', 'explanation': '製作術語未交代材料與任務。',
                'passages': [{'quote': source.read_text(), 'reader_understanding': '讀者只知道被要求重查。',
                              'remaining_gap': '不知道舊包是哪些材料、重查什麼。', 'problem_id': 'P1'}]}
            with self.assertRaisesRegex(LoopError, '不得給B L3'):
                validate_copy_reading_decision(task, response)
            response['evaluation']['grades']['B']['level'] = 'L2'
            validate_copy_reading_decision(task, response)
            response['evaluation']['problems'][0]['open'] = False
            with self.assertRaisesRegex(LoopError, '仍open的B問題'):
                validate_copy_reading_decision(task, response)
            response['evaluation']['problems'][0]['open'] = True
            response['reading_decision']['passages'][0]['quote'] = '根本沒有出現在候選的說明段落。'
            with self.assertRaisesRegex(LoopError, '逐字出自目前候選'):
                validate_copy_reading_decision(task, response)
