import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.course_improvement_loop import LoopError, artifact
from src.course_improvement_queue import dispatch, initialize_queue, queue_status
from src.course_loop_review import local_links, run_checks
from src.course_loop_stages import (confirm_h3, create_stage, next_task, receive,
                                    recheck_comparison, stage_status, supplement_evidence)


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "source.md"
        self.source.write_text("安2、柏1\n原稿")
        self.state = self.root / "state.json"
        self.policy = {"roles": {"assessor": "evaluation-model", "writer": "writing-model", "reviewer": "evaluation-model"},
                       "checks": [{"id": "links", "kind": "local_links", "description": "教材連結存在"},
                                  {"id": "facts", "kind": "required_text", "description": "保留案例班數", "texts": ["安2、柏1"]}]}
        self.config = {"id": "unit", "purpose": "案例理解", "source": "source", "artifacts": {"source": artifact(self.source)},
                       "output_root": str(self.root), "review_policy": self.policy}
        self.serial = 0

    def init(self):
        create_stage(self.config, self.state)

    def output(self, name, content=None):
        p = self.root / name
        p.write_text(content or name)
        return str(p)

    def ev(self, issue=False, solved=False, method="補足原因"):
        return {"problems": [{"id": "P1", "description": "缺少原因", "core": False, "open": not solved}] if issue else [],
                "questions": [], "grades": {k: {"level": "L2" if issue and not solved else "L3",
                                                   "problems": ["P1"] if issue and not solved else [], "questions": []} for k in "ABC"},
                "regression": False, "next_fix": {"problem": "P1", "method": method} if issue and not solved else None}

    def make_response(self, task, ev=None, candidate=None, resolutions=None):
        self.serial += 1
        prefix = str(self.serial)
        outputs = {"report": self.output(prefix + "-report.md")}
        response = {"task_id": task["id"], "outputs": outputs}
        if task["phase"] == "assess":
            outputs["handoff"] = self.output(prefix + "-handoff.md")
        if task["phase"] == "rewrite":
            outputs["candidate"] = self.output(prefix + "-candidate.md", candidate or "安2、柏1\n補足原因")
        else:
            response["evaluation"] = ev
        if task["phase"] == "review":
            response["check_resolutions"] = resolutions or {}
        return response

    def execution(self, task):
        return {"role": task["assignment"]["role"], "model": task["assignment"]["model"], "context_id": task["id"]}

    def accept(self, ev=None, candidate=None, resolutions=None):
        task = next_task(self.state)
        response = self.make_response(task, ev, candidate, resolutions)
        result = receive(self.state, response, self.execution(task))
        return result, response, task

    def checks(self, evidence=None):
        return run_checks(self.state, stage_status(self.state)["revision"], evidence)

    def candidate_ready(self, candidate=None):
        self.init()
        self.accept(self.ev(True))
        self.accept(candidate=candidate)
        self.accept(self.ev(True, True))

    def test_no_change_requires_checks_and_fresh_review(self):
        self.init()
        _, _, assessment = self.accept(self.ev())
        self.assertEqual(stage_status(self.state)["decision"]["status"], "waiting_checks")
        before = self.state.read_bytes()
        self.assertTrue(next_task(self.state)["waiting_checks"])
        self.assertEqual(before, self.state.read_bytes())
        self.checks()
        review = next_task(self.state)
        self.assertEqual(review["assignment"]["role"], "reviewer")
        self.assertNotIn("grades", review["current_evaluation"])
        self.assertFalse(any(k.endswith(":report") for k in review["allowed_inputs"]))
        response = self.make_response(review, self.ev())
        wrong = self.execution(review)
        wrong["context_id"] = assessment["id"]
        with self.assertRaises(LoopError):
            receive(self.state, response, wrong)
        receive(self.state, response, self.execution(review))
        self.assertEqual(stage_status(self.state)["decision"]["status"], "complete")
        self.assertEqual(stage_status(self.state)["candidate_usage"], "0/2")

    def test_reviewer_catches_assessor_omission(self):
        self.init()
        self.accept(self.ev())
        self.checks()
        self.accept(self.ev(True))
        self.assertEqual(stage_status(self.state)["phase"], "rewrite")
        self.assertEqual(next_task(self.state)["assignment"]["role"], "writer")

    def test_role_mismatch_and_old_checks_cannot_pass(self):
        self.init()
        task = next_task(self.state)
        response = self.make_response(task, self.ev())
        before = self.state.read_bytes()
        for identity in (None, {"role": "writer", "model": "writing-model", "context_id": "x"},
                         {"role": "assessor", "model": "writing-model", "context_id": "x"}):
            with self.assertRaises(LoopError):
                receive(self.state, response, identity)
        self.assertEqual(before, self.state.read_bytes())
        with self.assertRaises(LoopError):
            run_checks(self.state, 1)
        receive(self.state, response, self.execution(task))
        with self.assertRaises(LoopError):
            run_checks(self.state, 1)

    def test_broken_link_cannot_be_ignored_by_reviewer(self):
        self.candidate_ready("安2、柏1\n[附件](missing.md)")
        self.checks()
        task = next_task(self.state)
        with self.assertRaises(LoopError):
            receive(self.state, self.make_response(task, self.ev(True, True)), self.execution(task))
        ev = self.ev(True, True)
        ev["problems"].append({"id": "P2", "description": "新增失效連結", "core": False, "open": True})
        ev["grades"]["B"] = {"level": "L2", "problems": ["P2"], "questions": []}
        ev["regression"] = True
        ev["next_fix"] = {"problem": "P2", "method": "更正連結"}
        response = self.make_response(task, ev, resolutions={"links": "P2"})
        receive(self.state, response, self.execution(task))
        self.assertEqual(stage_status(self.state)["phase"], "rewrite")
        self.assertEqual(stage_status(self.state)["candidate_usage"], "1/2")

    def test_h3_requires_review_then_restart_stays_complete(self):
        self.candidate_ready()
        s = json.loads(self.state.read_text())
        candidate = s["artifacts"][s["candidates"][-1]]
        feedback = self.output("human.md", "使用者認可此版本閱讀")
        with self.assertRaises(LoopError):
            confirm_h3(self.state, feedback, candidate["sha256"], s["revision"], "使用者")
        self.checks()
        self.accept(self.ev(True, True))
        self.assertEqual(stage_status(self.state)["decision"]["status"], "waiting_human")
        confirm_h3(self.state, feedback, candidate["sha256"], stage_status(self.state)["revision"], "使用者")
        before = self.state.read_bytes()
        for command in ("resume", "next"):
            r = subprocess.run([sys.executable, "scripts/course_improvement_loop.py", command, "--state", str(self.state)], text=True, capture_output=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(json.loads(r.stdout)["decision"]["status"], "complete")
        self.assertEqual(before, self.state.read_bytes())

    def test_candidate_replay_and_pending_review_resume(self):
        self.init()
        self.accept(self.ev(True))
        _, response, task = self.accept()
        before = self.state.read_bytes()
        self.assertTrue(receive(self.state, response, self.execution(task))["duplicate"])
        self.assertEqual(before, self.state.read_bytes())
        self.accept(self.ev(True, True))
        self.checks()
        pending = next_task(self.state)
        r = subprocess.run([sys.executable, "scripts/course_improvement_loop.py", "next", "--state", str(self.state)], text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), pending)
        self.assertEqual(stage_status(self.state)["candidate_usage"], "1/2")

    def test_two_versions_still_stop_and_failure_count_is_not_doubled(self):
        self.init()
        self.accept(self.ev(True))
        for n in (1, 2):
            self.accept()
            self.accept(self.ev(True, method=f"下一修法{n}"))
            self.checks()
            self.accept(self.ev(True, method=f"下一修法{n}"))
            s = json.loads(self.state.read_text())
            self.assertEqual(s["unit"]["failures"]["P1"], n)
        result = next_task(self.state)
        self.assertTrue(result["stopped"])
        self.assertEqual(result["decision"]["candidate_usage"], "2/2")
        self.assertEqual(result["decision"]["status"], "waiting_human")

    def test_external_unknown_blocks_completion_and_rechecks_after_evidence(self):
        self.policy["checks"].append({"id": "operation", "kind": "external", "description": "指定操作成功紀錄"})
        self.init()
        self.accept(self.ev())
        self.checks()
        task = next_task(self.state)
        with self.assertRaises(LoopError):
            receive(self.state, self.make_response(task, self.ev()), self.execution(task))
        ev = self.ev()
        ev["questions"] = [{"id": "Q1", "description": "必要操作待補證", "required": True, "open": True}]
        ev["grades"]["A"] = {"level": "pending", "problems": [], "questions": ["Q1"]}
        receive(self.state, self.make_response(task, ev, resolutions={"operation": "Q1"}), self.execution(task))
        self.assertEqual(stage_status(self.state)["decision"]["status"], "waiting_evidence")
        report = self.output("new-evidence.md", "隔離測試的操作證據")
        supplement_evidence(self.state, {"new-evidence": report}, stage_status(self.state)["revision"])
        ev["questions"][0]["open"] = False
        ev["grades"]["A"] = {"level": "L3", "problems": [], "questions": []}
        self.accept(ev)
        with self.assertRaises(LoopError):
            self.checks({"operation": {"target": {"path": "wrong", "sha256": "wrong"}, "status": "pass", "report": report}})
        self.checks({"operation": {"target": artifact(self.source), "status": "pass", "report": report}})
        self.accept(ev)
        self.assertEqual(stage_status(self.state)["decision"]["status"], "complete")

    def test_changed_check_report_is_rejected(self):
        self.init()
        self.accept(self.ev())
        self.checks()
        s = json.loads(self.state.read_text())
        Path(s["artifacts"][s["latest_checks"]]["path"]).write_text("{}")
        with self.assertRaises(LoopError):
            next_task(self.state)

    def test_checks_interruption_recovers_without_overwrite(self):
        self.init()
        self.accept(self.ev())
        from src.course_loop_review import save as real_save
        def interrupted(path, data):
            if Path(path) == self.state:
                raise OSError("state write interrupted")
            real_save(path, data)
        before = self.state.read_bytes()
        with patch("src.course_loop_review.save", side_effect=interrupted):
            with self.assertRaises(OSError):
                self.checks()
        self.assertEqual(before, self.state.read_bytes())
        self.checks()
        self.assertEqual(stage_status(self.state)["phase"], "review")

    def test_recheck_after_h3_pending_still_requires_new_review(self):
        self.candidate_ready()
        self.checks()
        self.accept(self.ev(True, True))
        recheck_comparison(self.state, self.output("recheck.md"), stage_status(self.state)["revision"])
        self.accept(self.ev(True, True))
        self.assertEqual(stage_status(self.state)["phase"], "checks")
        self.assertIsNone(json.loads(self.state.read_text())["review_gate"])
        self.checks()
        self.accept(self.ev(True, True))
        self.assertEqual(stage_status(self.state)["candidate_usage"], "1/2")

    def test_queue_cannot_use_unreviewed_or_legacy_child(self):
        # 佇列建立在同一暫存目錄，實際教材與既有佇列均不接觸。
        manifest = {"id": "course", "dispatch_enabled": True, "review_policy": self.policy,
                    "units": [{"id": "unit", "title": "章1", "purpose": "案例理解", "source": artifact(self.source),
                               "stage_state": str(self.state), "dependencies": []}]}
        queue = self.root / "queue.json"
        initialize_queue(manifest, queue)
        self.assertEqual(dispatch(queue)["ticket"]["review_policy"], self.policy)
        self.init()
        self.accept(self.ev())
        self.assertEqual(queue_status(queue)["units"][0]["status"], "in_progress")
        self.checks()
        self.assertEqual(queue_status(queue)["units"][0]["stage_phase"], "review")
        self.accept(self.ev())
        self.assertEqual(queue_status(queue)["course_status"], "waiting_integration_review")
        # 模擬既有格式的相同來源狀態：不允許拿它抵充指定新版覆核。
        old = json.loads(self.state.read_text())
        old["schema_version"] = "stages-1"
        del old["config"]["review_policy"]
        self.state.write_text(json.dumps(old))
        self.assertEqual(queue_status(queue)["units"][0]["status"], "waiting_human")

    def test_local_link_check_handles_encoded_spaces_html_and_references(self):
        self.output("a b.md")
        path = self.output("links.md", "[a](a%20b.md)\n[x][ref]\n[ref]: <a b.md>\n<a href='a%20b.md'>a</a>\n[remote](https://example.test)\n")
        result = local_links(path)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(len(result["observations"]), 3)
        self.assertEqual(result["not_checked"], ["https://example.test"])

    def test_cli_new_trial_cannot_omit_review_policy(self):
        config = copy.deepcopy(self.config)
        del config["review_policy"]
        filename = self.output("config.json", json.dumps(config))
        r = subprocess.run([sys.executable, "scripts/course_improvement_loop.py", "stage-init", "--config", filename,
                            "--state", str(self.state)], text=True, capture_output=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("review_policy", r.stderr)
        self.assertFalse(self.state.exists())


if __name__ == "__main__":
    unittest.main()
