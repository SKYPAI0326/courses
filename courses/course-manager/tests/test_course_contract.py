import copy
import tempfile
import unittest
from pathlib import Path

from src.course_contract import (
    ContractStateError,
    GATE_ORDER,
    GATE_STATUSES,
    approve_gate,
    block_gate,
    load_contract,
    new_contract,
    record_change,
    save_contract_atomic,
    submit_gate,
    validate_contract,
)


REQUIRED_SECTIONS = {
    "schema_version",
    "identity",
    "governance",
    "gates",
    "G0_requirements",
    "G1_research",
    "adaptation",
    "G2_architecture",
    "G3_lesson_design",
    "G4_pilot",
    "G5_production",
    "G6_release_maintenance",
    "changes",
    "evidence_index",
}

REQUIRED_GATE_FIELDS = {
    "status",
    "owner",
    "inputs",
    "deliverables",
    "evidence",
    "risks",
    "open_questions",
    "approved_by",
    "approved_at",
    "source_revision",
    "affected_downstream",
}


class CourseContractModelTests(unittest.TestCase):
    def make_contract(self):
        return new_contract(
            slug="practical-ai",
            title="實用生成式 AI",
            created_by="課程團隊",
            created_at="2026-10-18T12:00:00+08:00",
        )

    def test_new_contract_has_all_gates_and_single_state_source(self):
        contract = self.make_contract()

        self.assertEqual(GATE_ORDER, tuple(f"G{index}" for index in range(7)))
        self.assertEqual(
            GATE_STATUSES,
            frozenset({"DRAFT", "REVIEW", "APPROVED", "BLOCKED", "STALE"}),
        )
        self.assertTrue(REQUIRED_SECTIONS.issubset(contract))
        self.assertEqual(tuple(contract["gates"]), GATE_ORDER)
        self.assertTrue(
            all(set(record) == REQUIRED_GATE_FIELDS for record in contract["gates"].values())
        )
        for section_name in REQUIRED_SECTIONS - {"gates"}:
            section = contract[section_name]
            if isinstance(section, dict):
                self.assertNotIn("status", section)

    def test_validate_rejects_unknown_gate_status(self):
        contract = self.make_contract()
        contract["gates"]["G3"]["status"] = "DONE"

        issues = validate_contract(contract)

        self.assertIn("unknown_gate_status", {issue.code for issue in issues})
        self.assertIn("$.gates.G3.status", {issue.path for issue in issues})

    def test_validate_rejects_missing_required_gate_fields(self):
        contract = self.make_contract()
        del contract["gates"]["G2"]["evidence"]

        issues = validate_contract(contract)

        self.assertIn("missing_gate_field", {issue.code for issue in issues})
        self.assertIn("$.gates.G2.evidence", {issue.path for issue in issues})

    def test_validate_rejects_invalid_section_and_gate_collection_types(self):
        mutations = {
            "governance": lambda contract: contract.update(governance=None),
            "changes": lambda contract: contract.update(changes="not-a-list"),
            "evidence_index": lambda contract: contract.update(evidence_index={}),
            "payload": lambda contract: contract.update(G1_research=[]),
            "gate risks": lambda contract: contract["gates"]["G0"].update(
                risks={"blocking": True, "resolved": False}
            ),
            "gate evidence": lambda contract: contract["gates"]["G0"].update(
                evidence={}
            ),
            "gate deliverables": lambda contract: contract["gates"]["G0"].update(
                deliverables="not-a-list"
            ),
        }

        for label, mutate in mutations.items():
            with self.subTest(label=label):
                contract = self.make_contract()
                mutate(contract)
                self.assertTrue(validate_contract(contract))

    def test_validate_rejects_manually_forged_approval(self):
        contract = self.make_contract()
        contract["gates"]["G2"]["status"] = "APPROVED"

        issues = validate_contract(contract)
        codes = {issue.code for issue in issues}

        self.assertIn("approval_metadata_required", codes)
        self.assertIn("unapproved_prerequisite", codes)

    def test_new_contract_rejects_path_traversal_slug(self):
        invalid_slugs = ("../outside", "nested/course", "Uppercase", "two words", "")

        for slug in invalid_slugs:
            with self.subTest(slug=slug):
                with self.assertRaises(ValueError):
                    new_contract(slug, "課程", "作者", "2026-10-18T12:00:00+08:00")

    def test_atomic_save_round_trips_utf8_prose_without_rewriting(self):
        prose = "先看懂工作情境，再完成一份可交付、可驗收的成果。\n保留完整推理，不改成待辦清單。"
        contract = self.make_contract()
        contract["G0_requirements"]["learner_context"] = prose
        expected = copy.deepcopy(contract)

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "nested" / "course-contract.json"
            save_contract_atomic(path, contract)
            loaded = load_contract(path)

            self.assertEqual(loaded, expected)
            self.assertEqual(
                loaded["G0_requirements"]["learner_context"].encode("utf-8"),
                prose.encode("utf-8"),
            )
            serialized = path.read_text(encoding="utf-8")
            self.assertIn("先看懂工作情境", serialized)
            self.assertNotIn("\\u5148", serialized)
            self.assertEqual(list(path.parent.glob(f".{path.name}.*.tmp")), [])


class CourseContractStateTests(unittest.TestCase):
    def make_contract(self):
        return new_contract(
            slug="practical-ai",
            title="實用生成式 AI",
            created_by="課程團隊",
            created_at="2026-10-18T12:00:00+08:00",
        )

    def approve_gates_through(self, contract, final_gate):
        for gate_id in GATE_ORDER:
            submit_gate(contract, gate_id, "child-skill", "2026-10-18T13:00:00+08:00")
            approve_gate(
                contract,
                gate_id,
                "使用者",
                "2026-10-18T13:05:00+08:00",
                f"核准 {gate_id} 成果與證據",
            )
            if gate_id == final_gate:
                return

    def test_submit_requires_previous_gate_approval(self):
        contract = self.make_contract()

        with self.assertRaises(ContractStateError):
            submit_gate(contract, "G1", "course-researcher", "2026-10-18T13:00:00+08:00")

        self.assertEqual(contract["gates"]["G1"]["status"], "DRAFT")

    def test_approve_requires_review_state_and_user_approval_fields(self):
        contract = self.make_contract()
        with self.assertRaises(ContractStateError):
            approve_gate(contract, "G0", "使用者", "2026-10-18T13:00:00+08:00", "核准")

        submit_gate(contract, "G0", "course-run", "2026-10-18T13:00:00+08:00")
        for approved_by, approved_at, note in (
            ("", "2026-10-18T13:00:00+08:00", "核准"),
            ("使用者", "", "核准"),
            ("使用者", "2026-10-18T13:00:00+08:00", ""),
        ):
            with self.subTest(
                approved_by=approved_by, approved_at=approved_at, approval_note=note
            ):
                with self.assertRaises(ContractStateError):
                    approve_gate(contract, "G0", approved_by, approved_at, note)
        self.assertEqual(contract["gates"]["G0"]["status"], "REVIEW")

    def test_approve_rejects_unresolved_blockers(self):
        contract = self.make_contract()
        contract["gates"]["G0"]["risks"].append(
            {"id": "risk-1", "blocking": True, "resolved": False, "description": "時數未確認"}
        )
        submit_gate(contract, "G0", "course-run", "2026-10-18T13:00:00+08:00")

        with self.assertRaises(ContractStateError):
            approve_gate(
                contract,
                "G0",
                "使用者",
                "2026-10-18T13:05:00+08:00",
                "核准需求",
            )

        self.assertEqual(contract["gates"]["G0"]["status"], "REVIEW")

    def test_child_submission_cannot_mark_gate_approved(self):
        contract = self.make_contract()

        submit_gate(contract, "G0", "course-run", "2026-10-18T13:00:00+08:00")

        gate = contract["gates"]["G0"]
        self.assertEqual(gate["status"], "REVIEW")
        self.assertIsNone(gate["approved_by"])
        self.assertIsNone(gate["approved_at"])
        self.assertEqual(gate["source_revision"], 1)

    def test_semantic_change_resets_affected_gate_and_stales_downstream(self):
        contract = self.make_contract()
        self.approve_gates_through(contract, "G2")
        original_g0 = copy.deepcopy(contract["gates"]["G0"])

        invalidated = record_change(
            contract,
            "G1",
            "代表工具改版，研究與架構需重驗",
            "course-run",
            "2026-10-19T09:00:00+08:00",
            semantic=True,
        )

        self.assertEqual(invalidated, ["G1", "G2", "G3", "G4", "G5", "G6"])
        self.assertEqual(contract["gates"]["G0"], original_g0)
        self.assertEqual(contract["gates"]["G1"]["status"], "DRAFT")
        self.assertIsNone(contract["gates"]["G1"]["approved_by"])
        self.assertIsNone(contract["gates"]["G1"]["approved_at"])
        self.assertTrue(
            all(contract["gates"][gate_id]["status"] == "STALE" for gate_id in GATE_ORDER[2:])
        )
        self.assertEqual(contract["changes"][-1]["affected_gate"], "G1")
        self.assertTrue(contract["changes"][-1]["semantic"])

    def test_nonsemantic_change_preserves_gate_states(self):
        contract = self.make_contract()
        self.approve_gates_through(contract, "G1")
        before = {gate_id: contract["gates"][gate_id]["status"] for gate_id in GATE_ORDER}

        invalidated = record_change(
            contract,
            "G1",
            "修正錯字",
            "編輯",
            "2026-10-19T09:00:00+08:00",
            semantic=False,
        )

        self.assertEqual(invalidated, [])
        self.assertEqual(
            {gate_id: contract["gates"][gate_id]["status"] for gate_id in GATE_ORDER},
            before,
        )
        self.assertFalse(contract["changes"][-1]["semantic"])

    def test_blocked_gate_can_return_to_draft_but_cannot_skip_review(self):
        contract = self.make_contract()
        block_gate(
            contract,
            "G0",
            "缺少學員使用情境",
            "course-run",
            "2026-10-18T13:00:00+08:00",
        )
        self.assertEqual(contract["gates"]["G0"]["status"], "BLOCKED")

        record_change(
            contract,
            "G0",
            "已補齊學員使用情境",
            "course-run",
            "2026-10-18T14:00:00+08:00",
            semantic=True,
        )
        self.assertEqual(contract["gates"]["G0"]["status"], "DRAFT")
        with self.assertRaises(ContractStateError):
            approve_gate(
                contract,
                "G0",
                "使用者",
                "2026-10-18T14:05:00+08:00",
                "核准需求",
            )

        submit_gate(contract, "G0", "course-run", "2026-10-18T14:10:00+08:00")
        self.assertEqual(contract["gates"]["G0"]["status"], "REVIEW")

    def test_approve_rejects_malformed_blocking_risk_container(self):
        contract = self.make_contract()
        submit_gate(contract, "G0", "course-run", "2026-10-18T13:00:00+08:00")
        contract["gates"]["G0"]["risks"] = {
            "blocking": True,
            "resolved": False,
        }

        with self.assertRaises(ContractStateError):
            approve_gate(
                contract,
                "G0",
                "使用者",
                "2026-10-18T13:05:00+08:00",
                "核准需求",
            )

        self.assertEqual(contract["gates"]["G0"]["status"], "REVIEW")


if __name__ == "__main__":
    unittest.main()
