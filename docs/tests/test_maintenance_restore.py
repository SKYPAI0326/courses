import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("maintenance_restore", Path(__file__).resolve().parents[1] / "restore-maintenance.py")
restore = importlib.util.module_from_spec(spec)
spec.loader.exec_module(restore)

class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / "repo"
        self.root.mkdir()
        self.archive = self.root.parent / "archive"
        self.archive.mkdir()
        self.source = self.archive / "tool.sh"
        self.source.write_text("#!/bin/sh\nexit 0\n")
        self.source.chmod(0o755)
        self.target = self.root / "_tools/tool.sh"
        self.manifest = self.root / "manifest.json"
        self.data = {"archive_root_relative_to_repo":"../archive", "archived":[
            {"path":"_tools/tool.sh", "archive_path":"tool.sh", "sha256":restore.digest(self.source)}]}
        self.save()
    def save(self):
        self.manifest.write_text(json.dumps(self.data))
    def test_dry_run_apply_and_idempotence(self):
        self.assertEqual(restore.restore(self.root,self.manifest),1)
        self.assertFalse(self.target.exists())
        self.assertEqual(restore.restore(self.root,self.manifest,True),1)
        self.assertEqual(self.target.read_bytes(),self.source.read_bytes())
        self.assertEqual(self.target.stat().st_mode & 0o777,0o755)
        self.assertEqual(restore.restore(self.root,self.manifest,True),0)
    def test_refuses_changed_target(self):
        self.target.parent.mkdir()
        self.target.write_text("new work")
        with self.assertRaises(ValueError): restore.restore(self.root,self.manifest,True)
        self.assertEqual(self.target.read_text(),"new work")
    def test_refuses_corrupted_archive(self):
        self.source.write_text("corrupted")
        with self.assertRaises(ValueError): restore.restore(self.root,self.manifest,True)
        self.assertFalse(self.target.exists())
    def test_refuses_path_escape(self):
        self.data['archived'][0]['path']='../escape.sh'
        self.save()
        with self.assertRaises(ValueError): restore.restore(self.root,self.manifest,True)

if __name__ == "__main__": unittest.main()
