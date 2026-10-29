import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from src.course_improvement_loop import LoopError, artifact
from src.course_loop_stages import confirm_h3, create_stage, next_task, receive, recheck_comparison, stage_status, supplement_evidence


class StageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "source.md"
        self.source.write_text("original")
        self.state = self.root / "state.json"
        create_stage({"id": "trial", "purpose": "概念理解", "source": "original",
                      "artifacts": {"original": artifact(self.source)}, "output_root": str(self.root)}, self.state)

    def output(self, name):
        p = self.root / name
        p.write_text(name)
        return str(p)

    def evaluation(self, solved=False):
        return {"problems": [{"id": "P1", "description": "說明不足", "core": False, "open": not solved}],
                "questions": [], "grades": {k: {"level": "L3" if solved else "L2", "problems": [] if solved else ["P1"], "questions": []} for k in "ABC"},
                "regression": False, "next_fix": None if solved else {"problem": "P1", "method": "補解釋"}}

    def assess(self):
        task = next_task(self.state)
        response = {"task_id": task["id"], "outputs": {"report": self.output("assessment.md"), "handoff": self.output("handoff.md")}, "evaluation": self.evaluation()}
        receive(self.state, response)

    def rewrite(self):
        self.assess()
        task = next_task(self.state)
        response = {"task_id": task["id"], "outputs": {"candidate": self.output("v1.md"), "report": self.output("changes.md")}}
        receive(self.state, response)
        return response

    def test_resume_task_and_duplicate_candidate(self):
        first = next_task(self.state)
        before = self.state.read_bytes()
        self.assertEqual(next_task(self.state), first)
        self.assertEqual(self.state.read_bytes(), before)
        self.assess()
        task = next_task(self.state)
        response = {"task_id": task["id"], "outputs": {"candidate": self.output("v1.md"), "report": self.output("changes.md")}}
        receive(self.state, response)
        before = self.state.read_bytes()
        self.assertTrue(receive(self.state, response)["duplicate"])
        self.assertEqual(self.state.read_bytes(), before)
        self.assertEqual(stage_status(self.state)["candidate_usage"], "1/2")
        self.assertEqual(stage_status(self.state)["phase"], "compare")

    def test_compare_stops_at_h3(self):
        self.rewrite()
        task = next_task(self.state)
        receive(self.state, {"task_id": task["id"], "outputs": {"report": self.output("compare.md")}, "evaluation": self.evaluation(True)})
        self.assertEqual(stage_status(self.state)["decision"]["status"], "waiting_human")
        self.assertTrue(next_task(self.state)["stopped"])

    def test_failed_save_can_retry_once_without_double_count(self):
        self.assess()
        task = next_task(self.state)
        response = {"task_id": task["id"], "outputs": {"candidate": self.output("v1.md"), "report": self.output("changes.md")}}
        before = self.state.read_bytes()
        with patch("src.course_improvement_loop.os.replace", side_effect=OSError("interrupted")):
            with self.assertRaises(OSError):
                receive(self.state, response)
        self.assertEqual(self.state.read_bytes(), before)
        receive(self.state, response)
        self.assertEqual(stage_status(self.state)["candidate_usage"], "1/2")

    def test_h3_recheck_preserves_history_and_uses_remaining_version(self):
        self.rewrite()
        task = next_task(self.state)
        receive(self.state, {"task_id": task["id"], "outputs": {"report": self.output("compare.md")}, "evaluation": self.evaluation(True)})
        before = json.loads(self.state.read_text())
        evidence = self.output("broken-link.md")
        with self.assertRaises(LoopError):
            recheck_comparison(self.state, evidence, before["revision"] - 1)
        recheck_comparison(self.state, evidence, before["revision"])
        reopened = json.loads(self.state.read_text())
        self.assertEqual(reopened["candidates"], before["candidates"])
        self.assertEqual(reopened["receipts"], before["receipts"])
        self.assertEqual(reopened["history"][:-1], before["history"])
        task = next_task(self.state)
        ev = self.evaluation(True)
        ev["problems"].append({"id": "P2", "description": "新增失效連結", "core": False, "open": True})
        ev["grades"]["B"] = {"level": "L2", "problems": ["P2"], "questions": []}
        ev["regression"] = True
        ev["next_fix"] = {"problem": "P2", "method": "修正路徑"}
        receive(self.state, {"task_id": task["id"], "outputs": {"report": self.output("recheck.md")}, "evaluation": ev})
        self.assertEqual(stage_status(self.state)["phase"], "rewrite")
        self.assertEqual(json.loads(self.state.read_text())["unit"]["failures"], before["unit"]["failures"])
        task = next_task(self.state)
        receive(self.state, {"task_id": task["id"], "outputs": {"candidate": self.output("v2.md"), "report": self.output("v2-changes.md")}})
        task = next_task(self.state)
        ev["next_fix"] = {"problem": "P2", "method": "改用核對過的路徑"}
        receive(self.state, {"task_id": task["id"], "outputs": {"report": self.output("v2-compare.md")}, "evaluation": ev})
        self.assertEqual(stage_status(self.state)["candidate_usage"], "2/2")
        self.assertEqual(stage_status(self.state)["decision"]["status"], "limited_stop")
        self.assertTrue(next_task(self.state)["stopped"])
        with self.assertRaises(LoopError):
            recheck_comparison(self.state, self.output("again.md"), stage_status(self.state)["revision"])

    def test_recheck_rejects_confirmed_h3_and_bound_evidence(self):
        self.rewrite()
        task = next_task(self.state)
        receive(self.state, {"task_id": task["id"], "outputs": {"report": self.output("compare.md")}, "evaluation": self.evaluation(True)})
        s = json.loads(self.state.read_text())
        with self.assertRaises(LoopError):
            recheck_comparison(self.state, self.source, s["revision"])
        candidate = s["artifacts"][s["candidates"][-1]]
        confirm_h3(self.state, self.output("human.md"), candidate["sha256"], s["revision"], "使用者")
        with self.assertRaises(LoopError):
            recheck_comparison(self.state, self.output("new.md"), stage_status(self.state)["revision"])

    def test_different_resend_rejected(self):
        response = self.rewrite()
        response["outputs"]["report"] = self.output("other.md")
        with self.assertRaises(LoopError):
            receive(self.state, response)

    def test_source_change_rejects_accept(self):
        task = next_task(self.state)
        self.source.write_text("changed")
        with self.assertRaises(LoopError):
            receive(self.state, {"task_id": task["id"], "outputs": {}})

    def test_ai_cannot_confirm_h3_or_use_external_output(self):
        task = next_task(self.state)
        response = {"task_id": task["id"], "outputs": {"report": self.output("assessment.md"), "handoff": self.output("handoff.md")}, "evaluation": self.evaluation()}
        response["evaluation"]["human"] = {"h3": "confirmed"}
        with self.assertRaises(LoopError):
            receive(self.state, response)
        del response["evaluation"]["human"]
        response["outputs"]["report"] = str(self.source)
        with self.assertRaises(LoopError):
            receive(self.state, response)

    def test_new_process_resumes_waiting_comparison(self):
        self.rewrite()
        cli = Path(__file__).resolve().parents[1] / "scripts/course_improvement_loop.py"
        result = json.loads(subprocess.check_output([sys.executable, str(cli), "resume", "--state", str(self.state)], text=True))
        self.assertEqual(result["phase"], "compare")
        self.assertEqual(result["candidate_usage"], "1/2")

    def test_second_candidate_no_third(self):
        self.rewrite()
        task = next_task(self.state)
        ev = self.evaluation()
        ev["next_fix"]["method"] = "改用對照例解釋"
        receive(self.state, {"task_id": task["id"], "outputs": {"report": self.output("compare1.md")}, "evaluation": ev})
        task = next_task(self.state)
        receive(self.state, {"task_id": task["id"], "outputs": {"candidate": self.output("v2.md"), "report": self.output("changes2.md")}})
        task = next_task(self.state)
        ev["next_fix"] = None
        receive(self.state, {"task_id": task["id"], "outputs": {"report": self.output("compare2.md")}, "evaluation": ev})
        self.assertTrue(next_task(self.state)["stopped"])
        self.assertEqual(stage_status(self.state)["candidate_usage"], "2/2")

    def finished_comparison(self):
        self.rewrite()
        task = next_task(self.state)
        receive(self.state, {"task_id": task["id"], "outputs": {"report": self.output("compare.md")}, "evaluation": self.evaluation(True)})
        return artifact(self.root / "v1.md")["sha256"]

    def test_h3_confirm_restart_no_rewrite_and_idempotence(self):
        version = self.finished_comparison()
        feedback = self.output("human.md")
        rev = stage_status(self.state)["revision"]
        result = confirm_h3(self.state, feedback, version, rev, "human tester")
        self.assertEqual(result["status"], "complete")
        before = self.state.read_bytes()
        self.assertTrue(confirm_h3(self.state, feedback, version, rev, "human tester")["duplicate"])
        cli = Path(__file__).resolve().parents[1] / "scripts/course_improvement_loop.py"
        resumed = json.loads(subprocess.check_output([sys.executable, str(cli), "resume", "--state", str(self.state)], text=True))
        self.assertEqual(resumed["decision"]["status"], "complete")
        self.assertTrue(next_task(self.state)["stopped"])
        self.assertEqual(self.state.read_bytes(), before)

    def test_h3_wrong_version_stale_revision_and_before_compare_rejected(self):
        self.rewrite()
        feedback = self.output("human.md")
        with self.assertRaises(LoopError):
            confirm_h3(self.state, feedback, "bad", 4, "human tester")
        task = next_task(self.state)
        receive(self.state, {"task_id": task["id"], "outputs": {"report": self.output("compare.md")}, "evaluation": self.evaluation(True)})
        version = artifact(self.root / "v1.md")["sha256"]
        with self.assertRaises(LoopError):
            confirm_h3(self.state, feedback, "bad", 6, "human tester")
        with self.assertRaises(LoopError):
            confirm_h3(self.state, feedback, version, 0, "human tester")

    def test_h3_does_not_clear_required_evidence(self):
        self.rewrite()
        task = next_task(self.state)
        ev = self.evaluation(True)
        ev["questions"] = [{"id": "Q1", "description": "需要查核資料", "required": True, "open": True}]
        ev["grades"]["A"] = {"level": "pending", "questions": ["Q1"], "problems": []}
        receive(self.state, {"task_id": task["id"], "outputs": {"report": self.output("compare.md")}, "evaluation": ev})
        result = confirm_h3(self.state, self.output("human.md"), artifact(self.root / "v1.md")["sha256"], 6, "human tester")
        self.assertEqual(result["status"], "waiting_evidence")
        self.assertTrue(next_task(self.state)["stopped"])

    def test_supplement_preserves_candidate_h3_and_failure_count(self):
        self.rewrite()
        task = next_task(self.state)
        ev = self.evaluation(True)
        ev["questions"] = [{"id": "Q1", "description": "必要資料待查", "required": True, "open": True}]
        ev["grades"]["A"] = {"level": "pending", "questions": ["Q1"], "problems": []}
        receive(self.state, {"task_id": task["id"], "outputs": {"report": self.output("compare.md")}, "evaluation": ev})
        confirm_h3(self.state, self.output("human.md"), artifact(self.root / "v1.md")["sha256"], 6, "human tester")
        evidence = {"new": self.output("evidence.md")}
        with self.assertRaises(LoopError):
            supplement_evidence(self.state, evidence, 0)
        supplement_evidence(self.state, evidence, 7)
        self.assertEqual(stage_status(self.state)["candidate_usage"], "1/2")
        task = next_task(self.state)
        self.assertEqual(task["phase"], "compare")
        ev["questions"][0]["open"] = False
        ev["grades"]["A"] = {"level": "L3", "questions": [], "problems": []}
        receive(self.state, {"task_id": task["id"], "outputs": {"report": self.output("compare-new.md")}, "evaluation": ev})
        state = json.loads(self.state.read_text())
        self.assertEqual(stage_status(self.state)["decision"]["status"], "complete")
        self.assertEqual(state["unit"]["failures"], {})
        self.assertEqual(len(state["candidates"]), 1)


if __name__ == "__main__":
    unittest.main()
