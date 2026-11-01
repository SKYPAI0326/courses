import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.course_improvement_loop import (
    LoopError, artifact, checkpoint, decide, initialize, load, report, save, validate_unit,
)


class LoopTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.state = self.root / "state.json"
        self.refs = {}
        for name in ("original", "v1", "v2", "evidence", "feedback", "new_evidence"):
            p = self.root / (name + ".md")
            p.write_text(name, encoding="utf-8")
            self.refs[name] = artifact(p)

    def unit(self, kind="complete"):
        u = {"id": "CH1-2", "purpose": "理解工具分工", "historical_rules": "v0.9",
             "assessment_basis": "evidence", "assessed_version": "v1",
             "candidate_limit": 2, "artifacts": copy.deepcopy(self.refs), "source": "original",
             "candidates": ["v1"], "problems": [], "questions": [],
             "grades": {k: {"level": "L3", "problems": [], "questions": []} for k in "ABC"},
             "human": {"decision": None, "h3": "confirmed", "version": "v1", "basis": "feedback"},
             "failures": {}, "attempts": [], "restrictions": [], "regression": False, "next_fix": None}
        if kind == "h3":
            u.update(id="CH1-1", candidates=["v1", "v2"], assessed_version="v2")
            u["human"] = {"decision": None, "h3": "pending"}
        if kind in ("repair", "evidence"):
            u["problems"] = [{"id": "P1", "description": "缺少登入入口", "core": True, "open": True, "basis": "evidence"}]
            u["grades"]["B"] = {"level": "L1", "problems": ["P1"], "questions": []}
            u["human"] = {"decision": None, "h3": "pending"}
            u["next_fix"] = {"problem": "P1", "method": "補入已確認入口", "basis": "evidence"}
        if kind == "evidence":
            u.update(id="CH1-3", candidates=["v1", "v2"], assessed_version="v2", next_fix=None,
                     restrictions=["使用者暫不下載"])
            u["questions"] = [{"id": "Q1", "description": "指定包尚未實測", "required": True, "open": True, "basis": "evidence"}]
            u["grades"]["B"] = {"level": "pending", "cap": "L1", "problems": ["P1"], "questions": ["Q1"]}
        return u

    def start(self, kind="complete"):
        u = self.unit(kind)
        initialize({"units": [u]}, self.state)
        return u

    def test_three_record_shapes_and_parallel_constraints(self):
        self.assertEqual(decide(self.unit("h3"))["status"], "waiting_human")
        self.assertEqual(decide(self.unit())["status"], "complete")
        result = decide(self.unit("evidence"))
        self.assertEqual(result["status"], "waiting_evidence")
        self.assertEqual(result["candidate_usage"], "2/2")
        self.assertEqual(len(result["constraints"]), 3)
        self.assertFalse(result["can_register_candidate"])

    def test_restart_cli_is_read_only(self):
        self.start("evidence")
        before = self.state.read_bytes()
        script = Path(__file__).resolve().parents[1] / "scripts/course_improvement_loop.py"
        output = subprocess.check_output([sys.executable, str(script), "resume", "--state", str(self.state)], text=True)
        self.assertEqual(json.loads(output)["units"][0]["status"], "waiting_evidence")
        self.assertEqual(self.state.read_bytes(), before)

    def test_reinitialization_and_candidate_reset_rejected(self):
        u = self.start("h3")
        with self.assertRaises(LoopError):
            initialize({"units": [u]}, self.state)
        u["candidates"] = ["v2"]
        with self.assertRaises(LoopError):
            checkpoint(self.state, u, 0, "tester", "不可重置")

    def test_complete_unit_cannot_add_candidate(self):
        u = self.start()
        u.update(candidates=["v1", "v2"], assessed_version="v2", assessment_basis="new_evidence")
        u["human"] = {"decision": None, "h3": "pending"}
        with self.assertRaises(LoopError):
            checkpoint(self.state, u, 0, "tester", "不應改稿")

    def test_third_candidate_and_failure_reset_rejected(self):
        u = self.start("evidence")
        u["candidates"].append("new_evidence")
        u["assessed_version"] = "new_evidence"
        with self.assertRaises(LoopError):
            checkpoint(self.state, u, 0, "tester", "第三版")
        u = self.unit("repair")
        u["failures"] = {"P1": 2}
        self.assertEqual(decide(u)["status"], "waiting_human")
        other = self.root / "other.json"
        initialize({"units": [u]}, other)
        u["failures"] = {}
        with self.assertRaises(LoopError):
            checkpoint(other, u, 0, "tester", "不能重置失敗")

    def test_untested_does_not_imply_low_grade(self):
        u = self.unit("evidence")
        u["problems"] = []
        u["grades"]["B"] = {"level": "pending", "questions": ["Q1"], "problems": []}
        self.assertEqual(decide(u)["status"], "waiting_evidence")
        u["grades"]["B"]["cap"] = "L1"
        with self.assertRaises(LoopError):
            validate_unit(u)

    def test_out_of_scope_question_does_not_block_concept(self):
        u = self.unit()
        u["questions"] = [{"id": "Q1", "description": "後課部署未測", "required": False, "open": True, "basis": "evidence"}]
        self.assertEqual(decide(u)["status"], "complete")

    def test_source_drift_stops_and_checkpoint_cannot_accept_it(self):
        u = self.start()
        (self.root / "original.md").write_text("changed")
        self.assertEqual(report(self.state)["units"][0]["status"], "waiting_human")
        with self.assertRaises(LoopError):
            checkpoint(self.state, u, 0, "tester", "舊來源已改")

    def test_h3_version_and_existing_requirement(self):
        u = self.unit("h3")
        u["human"] = {"decision": None, "h3": "confirmed", "version": "v1", "basis": "feedback"}
        with self.assertRaises(LoopError):
            validate_unit(u)
        u = self.start("h3")
        u["human"]["h3"] = "not_required"
        with self.assertRaises(LoopError):
            checkpoint(self.state, u, 0, "tester", "不能略過H3")

    def test_atomic_write_failure_keeps_previous_checkpoint(self):
        self.start()
        before = self.state.read_bytes()
        with patch("src.course_improvement_loop.os.replace", side_effect=OSError("simulated interruption")):
            with self.assertRaises(OSError):
                save(self.state, {"bad": "incomplete"})
        self.assertEqual(self.state.read_bytes(), before)
        self.assertEqual(report(self.state)["revision"], 0)

    def test_feedback_checkpoint_and_stale_revision(self):
        u = self.start("h3")
        u["human"] = {"decision": None, "h3": "confirmed", "version": "v2", "basis": "feedback"}
        result = checkpoint(self.state, u, 0, "tester", "模擬新回饋，僅臨時測試")
        self.assertEqual(result["units"][0]["status"], "complete")
        self.assertEqual(len(load(self.state)["history"]), 2)
        with self.assertRaises(LoopError):
            checkpoint(self.state, u, 0, "tester", "舊revision")

    def test_permitted_candidate_registration_and_second_failure(self):
        u = self.start("repair")
        u.update(candidates=["v1", "v2"], assessed_version="v2", assessment_basis="new_evidence")
        u["attempts"] = [{"problem": "P1", "method": "補入已確認入口"}]
        result = checkpoint(self.state, u, 0, "tester", "只登記已存在候選")
        self.assertEqual(result["units"][0]["status"], "limited_stop")

    def test_new_evidence_required_and_restrictions_preserved(self):
        u = self.start("evidence")
        u["questions"][0]["open"] = False
        u["grades"]["B"] = {"level": "L1", "problems": ["P1"], "questions": []}
        u["assessment_basis"] = "new_evidence"
        with self.assertRaises(LoopError):
            checkpoint(self.state, u, 0, "tester", "沒有新的Q依據")
        u = self.unit("evidence")
        u["restrictions"] = []
        with self.assertRaises(LoopError):
            checkpoint(self.state, u, 0, "tester", "不能解除使用者限制")

    def test_evidence_resolution_does_not_restore_budget(self):
        u = self.start("evidence")
        u["questions"][0].update(open=False, basis="new_evidence")
        u["assessment_basis"] = "new_evidence"
        u["grades"]["B"] = {"level": "L1", "problems": ["P1"], "questions": []}
        result = checkpoint(self.state, u, 0, "tester", "僅測試證據登記，不操作課程")
        self.assertEqual(result["units"][0]["status"], "limited_stop")
        self.assertEqual(result["units"][0]["candidate_usage"], "2/2")
        self.assertFalse(result["units"][0]["can_register_candidate"])

    def test_completed_last_version_and_h1_priority(self):
        u = self.unit("h3")
        u["human"] = {"decision": None, "h3": "confirmed", "version": "v2", "basis": "feedback"}
        self.assertEqual(decide(u)["status"], "complete")
        u = self.unit("evidence")
        u["human"]["decision"] = "H1"
        self.assertEqual(decide(u)["status"], "waiting_human")

    def test_failed_method_cannot_be_retried_unchanged(self):
        u = self.unit("repair")
        u["failures"] = {"P1": 1}
        u["attempts"] = [{"problem": "P1", "method": u["next_fix"]["method"]}]
        with self.assertRaises(LoopError):
            validate_unit(u)


if __name__ == "__main__":
    unittest.main()
