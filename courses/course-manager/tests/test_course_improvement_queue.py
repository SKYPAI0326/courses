import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.course_improvement_loop import LoopError, artifact, read_json
from src.course_improvement_queue import confirm_integration, dispatch, initialize_queue, queue_status
from src.course_loop_stages import confirm_h3, create_stage, next_task, receive, stage_status, supplement_evidence


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.queue = self.root / "queue.json"
        units = []
        for i in range(1, 6):
            source = self.root / f"CH{i}.md"
            source.write_text(f"source {i}")
            units.append({"id": f"CH{i}", "title": f"章{i}", "purpose": f"用途{i}", "source": artifact(source),
                          "stage_state": str(self.root / f"CH{i}" / "state.json"),
                          "dependencies": [] if i == 1 else [{"unit": f"CH{i-1}", "reason": "承接前章成果", "allow_h3_provisional": True}]})
        self.manifest = {"id": "test-course", "dispatch_enabled": True, "units": units}

    def init(self):
        initialize_queue(self.manifest, self.queue)

    def begin(self, i):
        u = self.manifest["units"][i-1]
        path = Path(u["stage_state"])
        path.parent.mkdir(parents=True, exist_ok=True)
        create_stage({"id": u["id"], "purpose": u["purpose"], "source": "source", "artifacts": {"source": u["source"]},
                      "output_root": str(path.parent)}, path)
        return path

    def output(self, state, name):
        p = state.parent / name
        p.write_text(name)
        return str(p)

    def evaluation(self, problem=False, question=False, solved=False):
        return {"problems": [{"id": "P1", "description": "局部解釋不足", "core": False, "open": not solved}] if problem else [],
                "questions": [{"id": "Q1", "description": "必要材料待查", "required": True, "open": not solved}] if question else [],
                "grades": {k: {"level": "L3" if solved or not (problem or question) else ("pending" if question else "L2"),
                               "problems": ["P1"] if problem and not solved else [],
                               "questions": ["Q1"] if question and not solved else []} for k in "ABC"},
                "regression": False, "next_fix": {"problem": "P1", "method": "補解釋"} if problem and not solved else None}

    def assess(self, state, ev, suffix=""):
        t = next_task(state)
        receive(state, {"task_id": t["id"], "outputs": {"report": self.output(state, f"assessment{suffix}.md"),
                        "handoff": self.output(state, f"handoff{suffix}.md")}, "evaluation": ev})

    def complete(self, i):
        p = self.begin(i)
        self.assess(p, self.evaluation())
        return p

    def h3(self, i):
        p = self.begin(i)
        self.assess(p, self.evaluation(problem=True))
        t = next_task(p)
        receive(p, {"task_id": t["id"], "outputs": {"candidate": self.output(p, "candidate.md"), "report": self.output(p, "changes.md")}})
        t = next_task(p)
        receive(p, {"task_id": t["id"], "outputs": {"report": self.output(p, "compare.md")}, "evaluation": self.evaluation(problem=True, solved=True)})
        return p

    def test_five_sequential_tickets_and_no_rewrite(self):
        self.init()
        for i in range(1, 6):
            result = dispatch(self.queue)
            self.assertEqual(result["ticket"]["unit"], f"CH{i}")
            before = self.queue.read_bytes()
            self.assertTrue(dispatch(self.queue)["reused"])
            self.assertEqual(self.queue.read_bytes(), before)
            self.complete(i)
        self.assertIsNone(dispatch(self.queue)["ticket"])
        self.assertEqual(queue_status(self.queue)["course_status"], "waiting_integration_review")

    def test_read_only_real_mode_cannot_dispatch(self):
        self.manifest["dispatch_enabled"] = False
        self.init()
        before = self.queue.read_bytes()
        with self.assertRaises(LoopError):
            dispatch(self.queue)
        self.assertEqual(self.queue.read_bytes(), before)
        self.assertFalse(any(Path(u["stage_state"]).exists() for u in self.manifest["units"]))

    def test_evidence_blocks_dependents_but_independent_unit_continues(self):
        self.manifest["units"][2]["dependencies"] = []
        self.init()
        dispatch(self.queue)
        p = self.begin(1)
        self.assess(p, self.evaluation(question=True))
        result = dispatch(self.queue)
        self.assertEqual(result["ticket"]["unit"], "CH3")
        rows = queue_status(self.queue)["units"]
        self.assertEqual(rows[0]["status"], "waiting_evidence")
        self.assertEqual(rows[1]["status"], "dependency_blocked")

    def test_supply_evidence_resume_without_reset(self):
        self.init()
        dispatch(self.queue)
        p = self.begin(1)
        self.assess(p, self.evaluation(question=True))
        self.assertIsNone(dispatch(self.queue)["ticket"])
        child_before = read_json(p)
        supplement_evidence(p, {"new_evidence": self.output(p, "new-evidence.md")}, child_before["revision"])
        self.assertEqual(dispatch(self.queue)["ticket"]["unit"], "CH1")
        self.assertEqual(stage_status(p)["candidate_usage"], "0/2")
        self.assess(p, self.evaluation(question=True, solved=True), "-recheck")
        self.assertEqual(dispatch(self.queue)["ticket"]["unit"], "CH2")
        self.assertEqual(len(read_json(p)["candidates"]), len(child_before["candidates"]))

    def test_h3_provisional_binding_and_confirmation(self):
        self.init()
        dispatch(self.queue)
        p = self.h3(1)
        ticket = dispatch(self.queue)["ticket"]
        self.assertEqual(ticket["unit"], "CH2")
        self.assertTrue(ticket["provisional"])
        self.complete(2)
        self.assertNotEqual(queue_status(self.queue)["course_status"], "complete")
        confirm_h3(p, self.output(p, "human.md"), artifact(p.parent / "candidate.md")["sha256"], stage_status(p)["revision"], "tester")
        self.assertEqual(queue_status(self.queue)["units"][1]["status"], "complete")

    def test_h3_not_allowed_and_h1_propagation(self):
        self.manifest["units"][1]["dependencies"][0]["allow_h3_provisional"] = False
        self.init()
        dispatch(self.queue)
        p = self.h3(1)
        self.assertIsNone(dispatch(self.queue)["ticket"])
        (p.parent / "candidate.md").write_text("changed")
        rows = queue_status(self.queue)["units"]
        self.assertEqual(rows[0]["status"], "waiting_human")
        self.assertIn("H1", rows[0]["blockers"][0])
        self.assertEqual(rows[1]["status"], "dependency_blocked")

    def test_restart_does_not_reset_active_ticket(self):
        self.init()
        ticket = dispatch(self.queue)["ticket"]
        before = self.queue.read_bytes()
        cli = Path(__file__).resolve().parents[1] / "scripts/course_improvement_queue.py"
        result = json.loads(subprocess.check_output([sys.executable, str(cli), "resume", "--state", str(self.queue)], text=True))
        self.assertEqual(result["active"], ticket)
        self.assertEqual(self.queue.read_bytes(), before)

    def test_integration_review_requires_all_chapters_complete(self):
        self.init()
        evidence = self.root / "integration.md"
        evidence.write_text("fixture evidence")
        with self.assertRaises(LoopError):
            confirm_integration(self.queue, evidence, 0, "tester")
        for i in range(1, 6):
            dispatch(self.queue)
            self.complete(i)
        dispatch(self.queue)
        result = confirm_integration(self.queue, evidence, read_json(self.queue)["revision"], "tester")
        self.assertEqual(result["course_status"], "complete")
        self.assertIsNone(dispatch(self.queue)["ticket"])

    def test_invalid_dependency_and_existing_state_rejected(self):
        self.manifest["units"][0]["dependencies"] = [{"unit": "CH5", "reason": "cycle", "allow_h3_provisional": True}]
        with self.assertRaises(LoopError):
            self.init()
        self.manifest["units"][0]["dependencies"] = []
        self.init()
        with self.assertRaises(LoopError):
            self.init()

    def test_h2_blocks_provisional_downstream(self):
        self.init()
        dispatch(self.queue)
        p = self.begin(1)
        ev = self.evaluation(problem=True)
        ev["regression"] = True
        ev["next_fix"] = None
        self.assess(p, ev)
        self.assertIn("H2", stage_status(p)["decision"]["reason"])
        self.assertIsNone(dispatch(self.queue)["ticket"])
        self.assertEqual(queue_status(self.queue)["units"][1]["status"], "dependency_blocked")


if __name__ == "__main__":
    unittest.main()
