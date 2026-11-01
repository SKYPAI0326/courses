import copy
import json
import tempfile
import unittest
from pathlib import Path

from src.course_improvement_loop import LoopError, artifact
from src.course_copy_reports import (reading_blocks, resolve_reference, hydrate_reading,
                                     merge_issue_updates, apply_report_patch)
from src.course_loop_runtime import validate_report_repair
from src.course_loop_stages import validate_copy_reading_decision
from src.course_copy_readability import validate_readability
from src.course_loop_executor import response_schema, build_prompt


class ReportContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.case = json.loads((Path(__file__).parent / 'fixtures/copy_report_rejected.json').read_text())
        source = self.root / 'candidate.md'; source.write_text(self.case['candidate'])
        self.task = {'target': artifact(source)}

    def ref(self, text):
        block = next(b for b in reading_blocks(self.task) if text in b['text'])
        return {'block': block['id'], 'start': 0, 'end': block['length']}

    def patch(self):
        refs = [self.ref(t) for t in ['再由自己確認內容是否保留原意', '決議和事實仍要回到紀錄核對', '不等於已替你確認材料正確']]
        return {'replacements': [{'passage': 0, 'quote_ref': refs[0], 'support_refs': refs}]}

    def test_real_rejected_report_is_repaired_without_changing_gap(self):
        original = self.case['original']; before = copy.deepcopy(original)
        fixed = apply_report_patch(self.task, original, self.patch())
        validate_report_repair(original, fixed)
        validate_copy_reading_decision(self.task, validate_readability(self.task, fixed))
        self.assertEqual(original, before)
        self.assertEqual(fixed['evaluation']['problems'], original['evaluation']['problems'])
        self.assertEqual(fixed['evaluation']['questions'], original['evaluation']['questions'])
        self.assertEqual(fixed['evaluation']['grades']['B']['level'], 'L1')
        self.assertEqual(fixed['reading_decision']['verdict'], 'gap')
        self.assertEqual(fixed['evaluation']['grades']['B']['problems'], ['P01'])

    def test_patch_cannot_carry_judgments_or_out_of_range_locations(self):
        patch = self.patch(); patch['evaluation'] = {'grades': 'pass'}
        with self.assertRaisesRegex(LoopError, '不可包含評級'):
            apply_report_patch(self.task, self.case['original'], patch)
        for ref in [{'block': 'missing', 'start': 0, 'end': 1}, {'block': 'p0001', 'start': 0, 'end': 999999}]:
            with self.assertRaises(LoopError): resolve_reference(self.task, ref)
        Path(self.task['target']['path']).write_text('來源已變')
        with self.assertRaisesRegex(LoopError, '版本已變動'): reading_blocks(self.task)

    def test_controller_keeps_omitted_issues_and_identity(self):
        prior = self.case['original']['evaluation']; update = copy.deepcopy(prior)
        update['problems'] = [{'id': 'P01', 'open': True}]; update['questions'] = []
        merged = merge_issue_updates(prior, update)
        self.assertEqual(merged['problems'], prior['problems'])
        self.assertEqual(merged['questions'], prior['questions'])
        self.assertEqual(merged['grades']['B']['level'], 'L1')
        update['problems'] = [dict(prior['problems'][0], core=False)]
        with self.assertRaisesRegex(LoopError, '不得變更'): merge_issue_updates(prior, update)

    def test_location_schema_and_prompt_include_real_blocks_and_scope(self):
        task = dict(self.task, id='test', phase='compare', profile='copy-v0.6', citation_contract='locations-v1',
                    purpose='本章既有用途', instructions='只審本章', assignment={}, current_evaluation={},
                    candidate_usage=1, candidate_limit=2, allowed_inputs={'candidate':self.task['target']})
        schema = response_schema(task)
        row = schema['properties']['reading_decision']['properties']['passages']['items']['properties']
        self.assertIn('quote_ref', row); self.assertNotIn('quote', row)
        prompt = build_prompt(task, 100000)
        self.assertIn('reading_blocks', prompt); self.assertIn('不代表本章必須逐類新增完整示範', prompt)
        task['report_patch'] = True
        self.assertEqual(response_schema(task)['required'], ['replacements'])

    def test_hydration_takes_exact_text_from_candidate(self):
        ref = self.ref('不等於已替你確認材料正確')
        raw = {'reading_decision': {'passages':[{'quote_ref':ref, 'support_refs':[ref]}]}}
        fixed = hydrate_reading(self.task, raw)
        self.assertIn('quote_ref', raw['reading_decision']['passages'][0])
        self.assertIn('不等於已替你確認材料正確；', fixed['reading_decision']['passages'][0]['quote'])

    def test_location_report_can_be_patched_before_hydration(self):
        task = dict(self.task, citation_contract='locations-v1', current_evaluation=self.case['original']['evaluation'])
        raw = copy.deepcopy(self.case['original'])
        row = raw['reading_decision']['passages'][0]
        row.pop('quote'); row.pop('support_quotes')
        row['quote_ref'] = {'block':'missing','start':0,'end':1}
        row['support_refs'] = [row['quote_ref']]
        fixed = apply_report_patch(task, raw, self.patch())
        validate_copy_reading_decision(task, validate_readability(task, fixed))
        self.assertEqual(fixed['reading_decision']['verdict'],'gap')
