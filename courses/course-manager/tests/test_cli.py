import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

from manager import build_parser


class CliContractTests(unittest.TestCase):
    def test_registers_all_management_commands(self):
        parser = build_parser()
        argument_sets = (
            ["scan"],
            ["find", "ai"],
            ["inspect", "office-ai"],
            ["propose-new", "SQL Server"],
            ["propose-move", "source", "destination"],
            ["propose-merge", "source", "target"],
            ["verify"],
            ["apply", "proposal.json", "--approval", "approval.json"],
            ["rollback", "manifest.json", "--approval", "approval.json"],
        )

        for argv in argument_sets:
            namespace = parser.parse_args(argv)
            self.assertEqual(namespace.command, argv[0])


if __name__ == "__main__":
    unittest.main()
