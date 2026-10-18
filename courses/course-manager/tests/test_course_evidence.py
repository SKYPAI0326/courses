import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from src.course_evidence import (
    materialize_json_evidence,
    register_evidence_file,
    verify_evidence_reference,
)


class CourseEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.temp_dir.name)
        self.root = self.base / "workspace"
        self.root.mkdir()

    def tearDown(self):
        self.temp_dir.cleanup()

    def reference(self, **overrides):
        reference = {
            "id": "g1-research",
            "gate": "G1",
            "kind": "research_record",
            "path": "evidence/research.json",
            "sha256": hashlib.sha256(b"evidence").hexdigest(),
        }
        reference.update(overrides)
        return reference

    def test_registers_regular_file_with_actual_hash_and_typed_fields(self):
        path = self.root / "evidence" / "research.json"
        path.parent.mkdir()
        path.write_bytes(b"evidence")

        reference = register_evidence_file(
            self.root,
            evidence_id="g1-research",
            gate_id="G1",
            kind="research_record",
            relative_path="evidence/research.json",
            maturity="STATIC_VALIDATED",
            metadata={"validator": "course-research"},
        )

        self.assertEqual(reference, self.reference(
            maturity="STATIC_VALIDATED",
            metadata={"validator": "course-research"},
        ))
        self.assertEqual(verify_evidence_reference(self.root, reference), [])

    def test_materializes_canonical_json_before_registering_it(self):
        value = {"z": "最後", "a": [2, 1]}

        reference = materialize_json_evidence(
            self.root,
            evidence_id="g0-requirements",
            gate_id="G0",
            kind="requirements_record",
            relative_path="evidence/requirements.json",
            value=value,
        )

        expected = '{"a":[2,1],"z":"最後"}\n'.encode("utf-8")
        self.assertEqual((self.root / reference["path"]).read_bytes(), expected)
        self.assertEqual(reference["sha256"], hashlib.sha256(expected).hexdigest())

    def test_verification_reports_missing_file(self):
        issues = verify_evidence_reference(self.root, self.reference())

        self.assertIn("missing_file", {issue.code for issue in issues})

    def test_verification_reports_wrong_hash(self):
        path = self.root / "evidence" / "research.json"
        path.parent.mkdir()
        path.write_bytes(b"changed")

        issues = verify_evidence_reference(self.root, self.reference())

        self.assertIn("hash_mismatch", {issue.code for issue in issues})

    def test_verification_reports_wrong_gate(self):
        path = self.root / "evidence" / "research.json"
        path.parent.mkdir()
        path.write_bytes(b"evidence")

        issues = verify_evidence_reference(
            self.root, self.reference(), expected_gate="G2"
        )

        self.assertIn("wrong_gate", {issue.code for issue in issues})

    def test_rejects_absolute_and_traversal_paths(self):
        for path in ("/tmp/outside.json", "../outside.json", "evidence/../../outside.json"):
            with self.subTest(path=path):
                issues = verify_evidence_reference(
                    self.root, self.reference(path=path)
                )
                self.assertIn("unsafe_path", {issue.code for issue in issues})

    def test_rejects_symlink_escape(self):
        outside = self.base / "outside.json"
        outside.write_bytes(b"evidence")
        evidence_dir = self.root / "evidence"
        evidence_dir.mkdir()
        (evidence_dir / "research.json").symlink_to(outside)

        issues = verify_evidence_reference(self.root, self.reference())

        self.assertIn("path_escape", {issue.code for issue in issues})
        with self.assertRaises(ValueError):
            register_evidence_file(
                self.root,
                evidence_id="g1-research",
                gate_id="G1",
                kind="research_record",
                relative_path="evidence/research.json",
            )

    def test_rejects_non_regular_file_and_invalid_gate_or_kind_types(self):
        directory = self.root / "evidence" / "directory"
        directory.mkdir(parents=True)
        issues = verify_evidence_reference(
            self.root, self.reference(path="evidence/directory")
        )
        self.assertIn("not_regular_file", {issue.code for issue in issues})

        for overrides, expected_code in (
            ({"gate": "G7"}, "invalid_gate"),
            ({"kind": 7}, "invalid_kind"),
        ):
            with self.subTest(overrides=overrides):
                issues = verify_evidence_reference(
                    self.root, self.reference(**overrides)
                )
                self.assertIn(expected_code, {issue.code for issue in issues})


if __name__ == "__main__":
    unittest.main()
