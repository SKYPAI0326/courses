import hashlib
import json
import os
import re
import tempfile
import unittest
from pathlib import Path

from src.course_evidence import (
    canonical_json_bytes,
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
        self.assertEqual(canonical_json_bytes(value), expected)

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

        self.assertIn("symlink_path", {issue.code for issue in issues})
        with self.assertRaises(ValueError):
            register_evidence_file(
                self.root,
                evidence_id="g1-research",
                gate_id="G1",
                kind="research_record",
                relative_path="evidence/research.json",
            )

    @unittest.skipUnless(os.name == "posix", "POSIX dirfd security contract")
    def test_materialize_rejects_parent_symlink_before_external_side_effect(self):
        outside = self.base / "outside"
        outside.mkdir()
        (self.root / "evidence").symlink_to(outside, target_is_directory=True)

        with self.assertRaises(ValueError):
            materialize_json_evidence(
                self.root,
                evidence_id="g0-requirements",
                gate_id="G0",
                kind="requirements_record",
                relative_path="evidence/new/requirements.json",
                value={"outcome": "artifact"},
            )

        self.assertFalse((outside / "new").exists())

    @unittest.skipUnless(os.name == "posix", "POSIX dirfd security contract")
    def test_register_and_verify_reject_final_and_parent_symlinks(self):
        evidence_dir = self.root / "evidence"
        evidence_dir.mkdir()
        actual = evidence_dir / "actual.json"
        actual.write_bytes(b"evidence")
        (evidence_dir / "linked.json").symlink_to(actual)

        linked_reference = self.reference(path="evidence/linked.json")
        issues = verify_evidence_reference(self.root, linked_reference)
        self.assertIn("symlink_path", {issue.code for issue in issues})
        with self.assertRaises(ValueError):
            register_evidence_file(
                self.root,
                evidence_id="g1-linked",
                gate_id="G1",
                kind="research_record",
                relative_path="evidence/linked.json",
            )

        nested = evidence_dir / "nested"
        nested.mkdir()
        (self.root / "linked-parent").symlink_to(nested, target_is_directory=True)
        parent_reference = self.reference(path="linked-parent/actual.json")
        issues = verify_evidence_reference(self.root, parent_reference)
        self.assertIn("symlink_path", {issue.code for issue in issues})

    def test_schema_and_runtime_use_the_same_scalar_reference_corpus(self):
        schema = json.loads(
            (
                Path(__file__).resolve().parents[1]
                / "contracts"
                / "course-evidence-reference.schema.json"
            ).read_text(encoding="utf-8")
        )
        properties = schema["properties"]
        corpus = (
            ("id", "evidence-1", True, None),
            ("id", "   ", False, "invalid_id"),
            ("kind", "research_record", True, None),
            ("kind", "\t", False, "invalid_kind"),
            ("maturity", "STATIC_VALIDATED", True, None),
            ("maturity", " ", False, "invalid_maturity"),
            ("path", "evidence/item.json", True, None),
            ("path", ".", False, "unsafe_path"),
            ("path", "../item.json", False, "unsafe_path"),
            ("path", "evidence\\item.json", False, "unsafe_path"),
        )

        for field, value, expected_valid, runtime_code in corpus:
            with self.subTest(field=field, value=value):
                field_schema = properties[field]
                schema_valid = isinstance(value, str) and len(value) >= field_schema.get(
                    "minLength", 0
                )
                if schema_valid and "pattern" in field_schema:
                    schema_valid = re.search(field_schema["pattern"], value) is not None
                reference = self.reference(**{field: value})
                runtime_codes = {
                    issue.code
                    for issue in verify_evidence_reference(self.root, reference)
                }
                runtime_valid = runtime_code not in runtime_codes if runtime_code else True
                self.assertEqual(schema_valid, expected_valid)
                self.assertEqual(runtime_valid, expected_valid)

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
