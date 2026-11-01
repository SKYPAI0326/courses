import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.course_improvement_loop import LoopError, artifact, read_json, save
from src.course_loop_executor import build_prompt, execute_codex, response_schema
from src.course_loop_runtime import (activate, finish, human_confirmation, prepare, report,
                                     recover, retry, repair_report, validate_report_repair, status, supply_check, work)


class RuntimeTests(unittest.TestCase):
    def test_new_location_contract_reaches_review_with_controller_owned_issues(self):
        self.spec['units'][0].update(profile='copy-v0.6', citation_contract='locations-v1')
        self.start()
        def located(job, model, timeout, effort):
            provider = self.transport(job, model, timeout, effort)
            task = read_json(job / 'task.json')
            if task['phase'] in ('compare', 'review'):
                from src.course_copy_reports import reading_blocks
                self.assertEqual(task['citation_contract'], 'locations-v1')
                block = reading_blocks(task)[0]
                ref = {'block':block['id'], 'start':0, 'end':block['length']}
                answer = read_json(job / 'answer.json')
                answer['evaluation']['problems'] = [{'id':'P1','open':False}]
                answer['reading_decision'] = {'verdict':'supported','explanation':'合成流程測試。','passages':[{
                    'quote_ref':ref,'support_refs':[ref],'reader_understanding':'班數與原因。','remaining_gap':'','problem_id':None,
                    'plain_restatement':'有兩班。','added_background':'', **{k:{'verdict':'supported','explanation':'僅測流程。'}
                    for k in ('referents','reason_placement','reading_load')}}]}
                save(job / 'answer.json',answer)
            return provider
        result = work(self.run, 8, located)
        self.assertIsNone(result['last_error'])
        self.assertEqual(result['units'][0]['status'],'waiting_human')
        self.assertEqual(result['model_calls'],4)
        state = read_json(self.run/'units/CH1/state.json')
        self.assertEqual(state['unit']['problems'][0]['description'],'缺少原因')

    def test_report_repair_cannot_change_judgment(self):
        original = {'evaluation': {'problems': [{'id': 'P1', 'open': True}], 'questions': [],
                    'grades': {'B': {'level': 'L1', 'problems': ['P1'], 'questions': []}}},
                    'reading_decision': {'verdict': 'gap', 'passages': [{'quote': '錯引文', 'support_quotes': ['錯引文'],
                                          'remaining_gap': '仍需說明', 'problem_id': 'P1'}]}}
        corrected = copy.deepcopy(original)
        corrected['reading_decision']['passages'][0].update(quote='真正引文', support_quotes=['真正引文'])
        validate_report_repair(original, corrected)
        corrected['evaluation']['grades']['B']['level'] = 'L3'
        with self.assertRaisesRegex(LoopError, '不得改變原判級'):
            validate_report_repair(original, corrected)

    def test_report_repair_keeps_raw_output_candidate_and_call_budget(self):
        self.spec['units'][0]['profile'] = 'copy-v0.6'
        self.start()
        def rejected_compare(job, model, timeout, effort):
            provider = self.transport(job, model, timeout, effort)
            task = read_json(job / 'task.json')
            if task['phase'] == 'compare':
                answer = read_json(job / 'answer.json')
                for grade in answer['evaluation']['grades'].values(): grade['problems'] = ['P1']
                answer['reading_decision'] = {'verdict': 'supported', 'explanation': '合成測試。', 'passages': [{
                    'quote': '案例班數2。原因已補。', 'reader_understanding': '班數與原因。', 'remaining_gap': '', 'problem_id': None,
                    'plain_restatement': '有兩班。', 'support_quotes': ['「案例班數2。原因已補。」'], 'added_background': '',
                    **{k: {'verdict': 'supported', 'explanation': '僅測流程。'} for k in ('referents','reason_placement','reading_load')}}]}
                save(job / 'answer.json', answer)
            return provider
        stopped = work(self.run, 3, rejected_compare)
        self.assertEqual(stopped['model_calls'], 3)
        runtime = read_json(self.run / 'run.json'); old = Path(list(runtime['jobs'].values())[-1]['directory'])
        raw = (old / 'answer.json').read_bytes()
        def corrected_report(job, model, timeout, effort):
            from src.course_copy_reports import reading_blocks
            task = read_json(job / 'task.json'); block = reading_blocks(task)[0]
            start = block['text'].index('案例班數2。原因已補。')
            ref = {'block':block['id'], 'start':start, 'end':start+len('案例班數2。原因已補。')}
            save(job / 'answer.json', {'replacements':[{'passage':0,'quote_ref':ref,'support_refs':[ref]}]})
            return {'model':model, 'context_id':'repair-context', 'fresh_process':True, 'usage':{}}
        repaired = repair_report(self.run, 'CH1', '已辨認引文與closed ID格式錯誤', '合成授權', corrected_report)
        self.assertIsNone(repaired['last_error'])
        self.assertEqual(repaired['model_calls'], 4)
        self.assertEqual(repaired['units'][0]['candidate_usage'], '1/2')
        self.assertEqual((old / 'answer.json').read_bytes(), raw)
        def reviewed(job, model, timeout, effort):
            task = read_json(job / 'task.json')
            self.assertEqual(task['phase'], 'review')
            self.assertNotIn('grades', task['current_evaluation'])
            answer = read_json(Path(read_json(self.run / 'run.json')['jobs'][next(
                k for k in read_json(self.run / 'run.json')['jobs'] if k.endswith('compare'))]['directory']) / 'assembled-answer.json')
            answer['check_resolutions'] = {}
            save(job / 'answer.json', answer)
            return {'model':model, 'context_id':'fresh-review-context', 'fresh_process':True, 'usage':{}}
        complete = work(self.run, 2, reviewed)
        self.assertIsNone(complete['last_error'])
        self.assertEqual(complete['units'][0]['status'], 'waiting_human')
        self.assertEqual(complete['model_calls'], 5)
        with self.assertRaises(LoopError):
            repair_report(self.run, 'CH1', '不能再試', '測試', corrected_report)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.run = self.root / "run"
        self.source = self.root / "lesson.md"
        self.source.write_text("案例班數2。")
        self.rules = self.root / "rules.md"
        self.rules.write_text("不得虛構；兩版上限；候選須人工閱讀。")
        self.spec = {"id": "test-course", "roles": {"assessor": "test-evaluator", "writer": "test-writer", "reviewer": "test-evaluator"},
                     "rules": [str(self.rules)], "limits": {"max_model_calls": 12, "timeout_seconds": 30,
                                                          "max_input_chars": 100000, "reasoning_effort": "medium"},
                     "units": [{"id": "CH1", "title": "合成課", "purpose": "理解班數", "source": str(self.source),
                                "checks": [{"id": "links", "kind": "local_links", "description": "路徑存在"}], "dependencies": []}]}
        self.calls = []

    def start(self):
        prepare(self.spec, self.run)
        activate(self.run, "測試", "僅合成教材，最多12次模擬呼叫")

    def ev(self, problem=False, solved=False):
        return {"problems": [{"id": "P1", "description": "缺少原因", "core": False, "open": not solved}] if problem else [],
                "questions": [], "grades": {k: {"level": "L2" if problem and not solved else "L3",
                                                   "problems": ["P1"] if problem and not solved else [], "questions": [], "cap": None} for k in "ABC"},
                "regression": False, "next_fix": {"problem": "P1", "method": "補原因"} if problem and not solved else None}

    def transport(self, job, model, timeout, effort):
        task = read_json(job / "task.json")
        self.calls.append((task["phase"], model))
        answer = {"documents": {"report": "# 合成報告\n僅測流程，不是模型評估。"}}
        if task["phase"] == "assess":
            answer["documents"]["handoff"] = "補足案例原因，保留班數。"
            answer["evaluation"] = self.ev(True)
        elif task["phase"] == "rewrite":
            answer["documents"]["candidate"] = "# 合成候選\n案例班數2。原因已補。"
        else:
            answer["evaluation"] = self.ev(True, True)
        if task["phase"] == "review":
            answer["check_resolutions"] = {}
            self.assertNotIn("grades", task["current_evaluation"])
            self.assertFalse(any(k.endswith(":report") for k in task["allowed_inputs"]))
        save(job / "answer.json", answer)
        return {"model": model, "context_id": task["id"], "fresh_process": True, "usage": {"input_tokens": 1}}

    def test_end_to_end_h3_then_integration(self):
        self.start()
        result = work(self.run, 8, self.transport)
        self.assertIsNone(result["last_error"])
        self.assertEqual(self.calls, [("assess", "test-evaluator"), ("rewrite", "test-writer"),
                                     ("compare", "test-writer"), ("review", "test-evaluator")])
        row = result["units"][0]
        self.assertEqual(row["status"], "waiting_human")
        feedback = self.root / "feedback.md"
        feedback.write_text("合成測試回饋，不是實際使用者的教材認可。")
        human_confirmation(self.run, "CH1", feedback, row["candidate"]["sha256"], row["child_revision"], "合成測試")
        self.assertEqual(work(self.run, 8, self.transport)["model_calls"], 4)
        integration = self.root / "integration.md"
        integration.write_text("合成課只有一章；測試結案接口。")
        done = finish(self.run, integration, status(self.run)["revision"], "合成測試")
        self.assertEqual(done["course_status"], "complete")
        self.assertTrue(Path(report(self.run)["report"]).exists())
        self.assertEqual(self.source.read_text(), "案例班數2。")

    def test_copy_v05_evidence_reaches_controller_and_still_requires_h3(self):
        self.spec['units'][0]['profile'] = 'copy-v0.5'
        self.start()
        def with_reading(job, model, timeout, effort):
            provider = self.transport(job, model, timeout, effort)
            task = read_json(job / 'task.json')
            if task['phase'] in ('compare', 'review'):
                self.assertIn('reading_decision', response_schema(task)['required'])
                prompt = build_prompt(task, 100000)
                self.assertLess(prompt.index('"id": "' + next(k for k,v in task['allowed_inputs'].items()
                    if v['path'] == task['target']['path']) + '"'), prompt.index('"current_evaluation"'))
                answer = read_json(job / 'answer.json')
                answer['reading_decision'] = {'verdict': 'supported', 'explanation': '合成測試：說明班數與原因。',
                    'passages': [{'quote': '案例班數2。原因已補。', 'reader_understanding': '案例班數及其原因。',
                                  'remaining_gap': '', 'problem_id': None}]}
                save(job / 'answer.json', answer)
            return provider
        result = work(self.run, 8, with_reading)
        self.assertIsNone(result['last_error'])
        self.assertEqual(result['units'][0]['status'], 'waiting_human')
        self.assertEqual(result['model_calls'], 4)

    def test_copy_v05_missing_reading_evidence_cannot_reach_h3(self):
        self.spec['units'][0]['profile'] = 'copy-v0.5'
        self.start()
        result = work(self.run, 8, self.transport)
        self.assertIsNotNone(result['last_error'])
        self.assertNotEqual(result['units'][0]['status'], 'waiting_human')

    def test_copy_v06_four_checks_survive_runtime_and_still_require_h3(self):
        self.spec['units'][0]['profile'] = 'copy-v0.6'
        self.start()
        def with_reading(job, model, timeout, effort):
            provider = self.transport(job, model, timeout, effort)
            task = read_json(job / 'task.json')
            self.assertIn('plain_restatement', build_prompt(task, 100000))
            if task['phase'] in ('compare', 'review'):
                properties = response_schema(task)['properties']['reading_decision']['properties']['passages']['items']['properties']
                self.assertIn('reading_load', properties)
                answer = read_json(job / 'answer.json')
                answer['reading_decision'] = {'verdict': 'supported', 'explanation': '合成流程測試。', 'passages': [{
                    'quote': '案例班數2。原因已補。', 'reader_understanding': '班數與原因。', 'remaining_gap': '', 'problem_id': None,
                    'plain_restatement': '這個案例有兩班，後文說明原因。', 'support_quotes': ['案例班數2。原因已補。'],
                    'added_background': '', **{k: {'verdict': 'supported', 'explanation': '合成文字僅測欄位傳遞。'}
                        for k in ('referents', 'reason_placement', 'reading_load')}}]}
                save(job / 'answer.json', answer)
            return provider
        result = work(self.run, 8, with_reading)
        self.assertIsNone(result['last_error'])
        self.assertEqual(result['units'][0]['status'], 'waiting_human')
        self.assertEqual(result['model_calls'], 4)

    def test_copy_profile_keeps_registered_problem_description(self):
        self.spec["units"][0]["profile"] = "copy-v0.3"
        self.start()

        def paraphrased_compare(job, model, timeout, effort):
            provider = self.transport(job, model, timeout, effort)
            task = read_json(job / "task.json")
            if task["phase"] == "compare":
                answer = read_json(job / "answer.json")
                answer["evaluation"]["problems"][0]["description"] = "同一缺口的另一種說法"
                answer["reading_audit"] = {"sections": [{"heading": "全文", "quote": "案例班數2。原因已補。",
                    "reader_understanding": "讀者能看見班數與原因", "continuity": "原因接在班數之後",
                    "verdict": "supported"}], "overall": "supported"}
                save(job / "answer.json", answer)
            return provider

        result = work(self.run, 3, paraphrased_compare)
        self.assertIsNone(result["last_error"])
        job = self.run / "units/CH1/jobs/CH1-5-compare"
        self.assertEqual(read_json(job / "response.json")["evaluation"]["problems"][0]["description"],
                         "同一缺口的另一種說法")
        self.assertEqual(read_json(job / "controller-response.json")["evaluation"]["problems"][0]["description"],
                         "缺少原因")
        self.assertEqual(read_json(job / "identity-normalization.json")["changes"][0]["id"], "P1")
        self.assertIn("從頭連讀候選", read_json(job / "task.json")["instructions"])
        self.assertIn("reading_audit", response_schema(read_json(job / "task.json"))["required"])

    def test_v04_compare_keeps_registered_description_without_reading_audit(self):
        self.spec["units"][0]["profile"] = "copy-v0.4"
        self.start()

        def paraphrased_compare(job, model, timeout, effort):
            provider = self.transport(job, model, timeout, effort)
            task = read_json(job / "task.json")
            if task["phase"] == "compare":
                answer = read_json(job / "answer.json")
                answer["evaluation"]["problems"][0]["description"] = "同一缺口的另一種說法"
                save(job / "answer.json", answer)
            return provider

        result = work(self.run, 3, paraphrased_compare)
        self.assertIsNone(result["last_error"])
        job = self.run / "units/CH1/jobs/CH1-5-compare"
        task = read_json(job / "task.json")
        self.assertNotIn("reading_audit", response_schema(task)["required"])
        self.assertIn("完整連續段落", task["instructions"])
        self.assertEqual(read_json(job / "controller-response.json")["evaluation"]["problems"][0]["description"],
                         "缺少原因")

    def test_legacy_redundant_cap_preserves_raw_result_and_resumes(self):
        self.start()
        def legacy(job, model, timeout, effort):
            provider = self.transport(job, model, timeout, effort)
            answer = read_json(job / "answer.json")
            answer["evaluation"]["problems"][0]["core"] = True
            for grade in answer["evaluation"]["grades"].values():
                grade.update(level="L1", cap="L1")
            save(job / "answer.json", answer)
            return provider
        result = work(self.run, 1, legacy)
        self.assertIsNone(result["last_error"])
        job = next((self.run / "units/CH1/jobs").iterdir())
        self.assertEqual(read_json(job / "response.json")["evaluation"]["grades"]["A"]["cap"], "L1")
        self.assertIsNone(read_json(job / "controller-response.json")["evaluation"]["grades"]["A"]["cap"])
        self.assertEqual(read_json(job / "normalization.json")["principles"], ["A", "B", "C"])
        variants = response_schema(read_json(job / "task.json"))["properties"]["evaluation"]["properties"]["grades"]["properties"]["A"]["anyOf"]
        self.assertEqual(variants[0]["properties"]["cap"], {"type": "null"})

    def test_prepare_never_calls_models_and_activation_required(self):
        prepare(self.spec, self.run)
        self.assertFalse(status(self.run)["dispatch_enabled"])
        with self.assertRaises(LoopError):
            work(self.run, transport=self.transport)
        self.assertEqual(self.calls, [])
        self.assertFalse((self.run / "units/CH1/state.json").exists())
        with self.assertRaises(LoopError):
            prepare(self.spec, self.run)

    def test_budget_stops_before_next_model(self):
        self.spec["limits"]["max_model_calls"] = 1
        self.start()
        result = work(self.run, 8, self.transport)
        self.assertIn("額度", result["last_error"])
        self.assertEqual(result["model_calls"], 1)
        self.assertEqual(len(self.calls), 1)

    def test_receive_interruption_recovers_cache_without_call(self):
        self.start()
        with patch("src.course_loop_runtime.receive", side_effect=OSError("interrupt after model returned")):
            failed = work(self.run, 1, self.transport)
        self.assertEqual(failed["model_calls"], 1)
        recovered = work(self.run, 1, self.transport)
        self.assertEqual(recovered["model_calls"], 2)
        self.assertEqual([p for p, _ in self.calls], ["assess", "rewrite"])

    def test_failure_retries_once_without_resetting_budget(self):
        self.start()
        def broken(*args):
            raise LoopError("simulated model unavailable")
        result = work(self.run, 1, broken)
        self.assertEqual(result["model_calls"], 1)
        result = work(self.run, 1, broken)
        self.assertEqual(result["model_calls"], 1)
        result = retry(self.run, "CH1", "合成暫時錯誤，補救一次", broken)
        self.assertEqual(result["model_calls"], 2)
        with self.assertRaises(LoopError):
            retry(self.run, "CH1", "不應第三次", broken)

    def test_chapter_specific_checks_and_dependency(self):
        second = self.root / "second.md"
        second.write_text("後課")
        self.spec["units"].append({"id": "CH2", "title": "後課", "purpose": "承接班數", "source": str(second),
                                  "checks": [{"id": "meaning", "kind": "required_text", "description": "保留標題", "texts": ["後課"]}],
                                  "dependencies": [{"unit": "CH1", "reason": "依賴前章", "allow_h3_provisional": False}]})
        self.start()
        result = work(self.run, 8, self.transport)
        self.assertEqual(result["units"][1]["status"], "dependency_blocked")
        self.assertFalse((self.run / "units/CH2/state.json").exists())

    def test_source_or_spec_change_stops(self):
        self.start()
        self.source.write_text("changed")
        result = work(self.run, 3, self.transport)
        self.assertEqual(result["model_calls"], 0)
        self.assertEqual(result["units"][0]["status"], "waiting_human")
        (self.run / "spec.json").write_text("{}")
        with self.assertRaises(LoopError):
            status(self.run)

    def test_input_limit_does_not_silently_truncate_or_call_model(self):
        self.spec["limits"]["max_input_chars"] = 1000
        self.rules.write_text("完整規範" * 1000)
        self.start()
        result = work(self.run, 1, self.transport)
        self.assertIn("不截斷", result["last_error"])
        self.assertEqual(result["model_calls"], 0)

    def test_status_in_new_process_is_read_only(self):
        self.start()
        before = (self.run / "run.json").read_bytes()
        result = subprocess.run([sys.executable, "scripts/course_loop.py", "status", "--run", str(self.run)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["model_calls"], 0)
        self.assertEqual(before, (self.run / "run.json").read_bytes())

    def test_schema_requires_phase_fields_and_fresh_provider(self):
        self.start()
        result = work(self.run, 1, self.transport)
        job = next(iter(read_json(self.run / "run.json")["jobs"].values()))
        schema = read_json(Path(job["directory"]) / "schema.json")
        self.assertEqual(set(schema["required"]), {"documents", "evaluation"})
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(result["model_calls"], 1)

    def test_recover_completed_event_without_recalling_model(self):
        self.start()
        def crash(job, model, timeout, effort):
            provider = self.transport(job, model, timeout, effort)
            save(job / "invocation.json", {"model": model, "fresh_process": True})
            (job / "events.jsonl").write_text(json.dumps({"type": "thread.started", "thread_id": provider["context_id"]}) + "\n" +
                                              json.dumps({"type": "turn.completed", "usage": {}}) + "\n")
            raise OSError("parent interrupted before provider result saved")
        work(self.run, 1, crash)
        restored = recover(self.run, "CH1")
        self.assertEqual(restored["model_calls"], 1)
        self.assertEqual(restored["units"][0]["stage_phase"], "rewrite")
        self.assertEqual(len(self.calls), 1)

    def test_external_evidence_can_resume_same_unit(self):
        self.spec["units"][0]["checks"].append({"id": "operation", "kind": "external", "description": "必要實測"})
        self.start()
        def evidence_transport(job, model, timeout, effort):
            task = read_json(job / "task.json")
            ev = self.ev()
            prior = task["current_evaluation"]
            if prior and prior["questions"]:
                ev["questions"] = [{"id": "Q1", "description": "必要實測待確認", "required": True, "open": False}]
            pending = task["phase"] == "review" and any(c["status"] == "pending" for c in read_json(task["allowed_inputs"][task["checks"]]["path"])["checks"])
            if pending:
                ev["questions"] = [{"id": "Q1", "description": "必要實測待確認", "required": True, "open": True}]
                ev["grades"]["A"] = {"level": "pending", "problems": [], "questions": ["Q1"], "cap": None}
            answer = {"documents": {"report": "合成補證測試"}, "evaluation": ev}
            if task["phase"] == "assess":
                answer["documents"]["handoff"] = "合成無需改稿"
            if task["phase"] == "review":
                answer["check_resolutions"] = {"operation": "Q1"} if pending else {}
            save(job / "answer.json", answer)
            return {"model": model, "context_id": task["id"], "fresh_process": True}
        waiting = work(self.run, 5, evidence_transport)
        self.assertEqual(waiting["units"][0]["status"], "waiting_evidence")
        evidence = self.root / "actual-test.md"
        evidence.write_text("合成實測證據")
        supply_check(self.run, "CH1", "operation", "pass", evidence, artifact(self.source)["sha256"])
        done = work(self.run, 5, evidence_transport)
        self.assertEqual(done["units"][0]["status"], "complete")
        self.assertEqual(done["model_calls"], 4)

    def fake_codex(self, tool_event=False):
        path = self.root / "fake-codex"
        path.write_text("#!/usr/bin/env python3\nimport json,sys\nfrom pathlib import Path\n"
                        "args=sys.argv[1:]\nsys.stdin.read()\n"
                        "Path(args[args.index('--output-last-message')+1]).write_text('{\"ok\":\"ready\"}')\n"
                        "print(json.dumps({'type':'thread.started','thread_id':'fake-context'}))\n" +
                        ("print(json.dumps({'type':'item.completed','item':{'type':'command_execution'}}))\n" if tool_event else "") +
                        "print(json.dumps({'type':'turn.completed','usage':{'input_tokens':1}}))\n")
        path.chmod(0o700)
        job = self.root / "job"
        job.mkdir()
        (job / "prompt.txt").write_text("minimal")
        save(job / "schema.json", {"type": "object"})
        return path, job

    def test_codex_transport_is_fresh_readonly_and_records_actual_context(self):
        binary, job = self.fake_codex()
        with patch("src.course_loop_executor.shutil.which", return_value=str(binary)):
            result = execute_codex(job, "test-model", 10, "low")
        command = read_json(job / "invocation.json")["command"]
        self.assertIn("--ephemeral", command)
        self.assertIn("--ignore-user-config", command)
        self.assertEqual(command[command.index("--sandbox") + 1], "read-only")
        self.assertEqual(result["context_id"], "fake-context")

    def test_codex_transport_rejects_tool_use(self):
        binary, job = self.fake_codex(tool_event=True)
        with patch("src.course_loop_executor.shutil.which", return_value=str(binary)):
            with self.assertRaises(LoopError):
                execute_codex(job, "test-model", 10, "low")
        self.assertFalse((job / "provider-result.json").exists())


if __name__ == "__main__":
    unittest.main()
