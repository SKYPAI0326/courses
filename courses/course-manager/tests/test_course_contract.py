import copy
import tempfile
import unittest
from pathlib import Path

from src.course_contract import (
    GATE_ORDER,
    GATE_STATUSES,
    load_contract,
    new_contract,
    save_contract_atomic,
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


if __name__ == "__main__":
    unittest.main()
