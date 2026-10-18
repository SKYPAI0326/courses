import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from src.course_contract import (
    GATE_ORDER,
    authorize_external_action,
    begin_gate,
    new_contract,
    propose_external_action,
    save_contract_atomic,
)
from tests.gate_test_support import _commit_gate_pass
from src.course_release import (
    ReleaseAuthorizationError,
    apply_release_proposal,
    build_release_proposal,
    scan_course_freshness,
    validate_release_record,
)


class CourseReleaseTests(unittest.TestCase):
    def sha(self, value):
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def make_course_root(self, root: Path):
        (root / "staged").mkdir(parents=True)
        (root / "public").mkdir()
        (root / "staged" / "index.html").write_text(
            "<html>new course</html>", encoding="utf-8"
        )
        (root / "staged" / "search-index.json").write_text(
            '{"course":"new"}\n', encoding="utf-8"
        )
        (root / "public" / "index.html").write_text(
            "<html>old course</html>", encoding="utf-8"
        )
        (root / "untouched.txt").write_text("preserve me", encoding="utf-8")

    def valid_release_record(self):
        checks = []
        for name in (
            "technical",
            "links",
            "registration",
            "access",
            "rollback",
            "maintenance",
        ):
            checks.append(
                {
                    "id": name,
                    "result": "PASS",
                    "evidence": {
                        "path": f"evidence/{name}.json",
                        "sha256": self.sha(name),
                    },
                }
            )
        return {
            "schema_version": 1,
            "course_id": "demo-course",
            "g5_status": "PASS",
            "g6_state": "READY_TO_PUBLISH",
            "published": False,
            "checks": checks,
            "changes": [
                {
                    "source_path": "staged/index.html",
                    "target_path": "public/index.html",
                },
                {
                    "source_path": "staged/search-index.json",
                    "target_path": "public/search-index.json",
                },
            ],
            "maintenance": {
                "owner": "course-ops",
                "cadence": "quarterly",
                "freshness_sources": ["official release notes", "learner reports"],
                "next_review": "2027-01-18",
            },
        }

    def write_authorized_contract(self, path: Path, proposal):
        contract = new_contract(
            "demo-course",
            "示範課程",
            "course-run",
            "2026-10-18T12:00:00+08:00",
        )
        for gate_id in GATE_ORDER:
            begin_gate(
                contract, gate_id, "course-run", "2026-10-18T17:00:00+08:00"
            )
            evidence_id = f"{gate_id.casefold()}-evidence"
            contract["evidence_index"].append(
                {
                    "id": evidence_id,
                    "gate": gate_id,
                    "kind": "test_record",
                    "path": f"evidence/{evidence_id}.json",
                    "sha256": self.sha(evidence_id),
                }
            )
            _commit_gate_pass(
                contract,
                gate_id,
                [evidence_id],
                f"{gate_id.casefold()}-validator",
                "course-run",
                "2026-10-18T17:05:00+08:00",
            )
        propose_external_action(
            contract,
            proposal["action_id"],
            "course-release",
            str(path.parent / "release-proposal.json"),
            proposal["manifest_sha256"],
            "course-ops",
            "2026-10-18T18:00:00+08:00",
        )
        authorize_external_action(
            contract,
            proposal["action_id"],
            "course-owner",
            "2026-10-18T18:05:00+08:00",
            "核准這份精確發布 manifest。",
        )
        save_contract_atomic(path, contract)

    def test_g6_pass_means_ready_not_published(self):
        record = self.valid_release_record()

        self.assertEqual(validate_release_record(record), [])
        self.assertEqual(record["g6_state"], "READY_TO_PUBLISH")
        self.assertFalse(record["published"])

        published = copy.deepcopy(record)
        published["published"] = True
        codes = {issue.code for issue in validate_release_record(published)}
        self.assertIn("g6_cannot_claim_published", codes)

    def test_release_proposal_lists_exact_targets_hashes_backup_and_rollback(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)

            proposal = build_release_proposal(root, self.valid_release_record())

            self.assertEqual(proposal["status"], "PENDING_AUTHORIZATION")
            self.assertEqual(len(proposal["manifest"]["targets"]), 2)
            target = proposal["manifest"]["targets"][0]
            self.assertEqual(target["before_sha256"], self.sha("<html>old course</html>"))
            self.assertEqual(target["after_sha256"], self.sha("<html>new course</html>"))
            self.assertTrue(target["backup_path"].startswith(".release-backups/"))
            self.assertEqual(
                proposal["manifest_sha256"],
                self.sha(
                    json.dumps(
                        proposal["manifest"],
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    )
                ),
            )
            self.assertEqual(
                {item["target_path"] for item in proposal["manifest"]["rollback"]["targets"]},
                {"public/index.html", "public/search-index.json"},
            )

    def test_apply_refuses_missing_mismatched_or_consumed_authorization(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            save_contract_atomic(
                contract_path,
                new_contract(
                    "demo-course",
                    "示範課程",
                    "course-run",
                    "2026-10-18T12:00:00+08:00",
                ),
            )
            with self.assertRaises(ReleaseAuthorizationError):
                apply_release_proposal(proposal_path, contract_path)

            self.write_authorized_contract(contract_path, proposal)
            mismatched = json.loads(proposal_path.read_text(encoding="utf-8"))
            mismatched["manifest"]["targets"][0]["after_sha256"] = "0" * 64
            proposal_path.write_text(json.dumps(mismatched), encoding="utf-8")
            with self.assertRaises(ReleaseAuthorizationError):
                apply_release_proposal(proposal_path, contract_path)

            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            apply_release_proposal(proposal_path, contract_path)
            with self.assertRaises(ReleaseAuthorizationError):
                apply_release_proposal(proposal_path, contract_path)

    def test_apply_modifies_only_manifest_targets_and_records_result(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)
            untouched_before = (root / "untouched.txt").read_bytes()

            apply_release_proposal(proposal_path, contract_path)

            self.assertEqual(
                (root / "public" / "index.html").read_text(encoding="utf-8"),
                "<html>new course</html>",
            )
            self.assertEqual(
                (root / "public" / "search-index.json").read_text(encoding="utf-8"),
                '{"course":"new"}\n',
            )
            self.assertEqual((root / "untouched.txt").read_bytes(), untouched_before)
            applied = json.loads(proposal_path.read_text(encoding="utf-8"))
            self.assertEqual(applied["status"], "APPLIED")
            self.assertEqual(applied["result"]["outcome"], "PASS")
            self.assertEqual(
                set(applied["result"]["modified_targets"]),
                {"public/index.html", "public/search-index.json"},
            )
            for target in proposal["manifest"]["targets"]:
                if target["before_sha256"] is not None:
                    self.assertTrue((root / target["backup_path"]).is_file())

    def test_register_compatibility_entry_dispatches_to_course_ops(self):
        project_root = Path(__file__).resolve().parents[1]
        text = (project_root / "skill-packages/course-register/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("相容入口", text)
        self.assertIn("course-ops", text)
        self.assertNotIn("Step 6：更新 `inject_gate.py`", text)

    def test_refresh_scan_is_read_only_and_routes_stale_items_to_gate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            html = root / "unit-1.html"
            html.write_text(
                '<main data-platform-version="tool-v1" data-built-at="2026-01-01">課程</main>',
                encoding="utf-8",
            )
            before = html.read_bytes()

            report = scan_course_freshness(root, "2026-10-18")

            self.assertEqual(html.read_bytes(), before)
            self.assertEqual(report["items"][0]["severity"], "STALE")
            self.assertEqual(report["items"][0]["affected_gate"], "G1")
            self.assertIn("recommended_action", report["items"][0])

    def test_refresh_never_edits_metadata_or_republishes(self):
        project_root = Path(__file__).resolve().parents[1]
        skill = (project_root / "skill-packages/course-refresh/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertNotIn("Edit", skill.split("---", 2)[1])
        self.assertNotIn("Write", skill.split("---", 2)[1])
        self.assertNotIn("bump-metadata", skill)
        self.assertNotIn("git commit", skill)
        self.assertIn("affected_gate", skill)


if __name__ == "__main__":
    unittest.main()
