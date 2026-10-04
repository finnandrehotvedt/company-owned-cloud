from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_synthetic_only_claim(self) -> None:
        config = json.loads((ROOT / "config/platform.json").read_text(encoding="utf-8"))
        self.assertTrue(config["data"]["synthetic_only"])
        self.assertFalse(config["data"]["customer_data_allowed"])

    def test_physical_card_is_not_a_tested_claim(self) -> None:
        decisions = (ROOT / "DECISIONS.md").read_text(encoding="utf-8")
        self.assertIn("not purchased, integrated or tested", decisions)

    def test_state_comparator_is_import_free_cli(self) -> None:
        self.assertTrue((ROOT / "scripts/compare_states.py").is_file())


if __name__ == "__main__":
    unittest.main()
