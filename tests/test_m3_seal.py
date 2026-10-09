"""Detect mutations to frozen design and published source-pins."""
from pathlib import Path
import json
import unittest
from scripts.verify_m3_freeze import verify, ROOT

class M3SealTests(unittest.TestCase):
    def test_frozen_sha256_and_bytes(self):
        verify()

    def test_24_probes_refer_to_registered_design(self):
        probes = json.loads((ROOT / "m3/probes.v1.json").read_text())["probes"]
        design = json.loads((ROOT / "m3/preregistration.v1.json").read_text())["design"]
        self.assertEqual(len(probes), design["personas"] * design["probes_per_persona"])
        self.assertEqual(design["total_response_slots"], 2 * design["response_slots_per_budget_mode"])
