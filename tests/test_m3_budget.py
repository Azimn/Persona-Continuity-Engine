"""Exact-budget compilation and M3 preregistration integrity tests."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from pce import load_spec, verify_packet
from pce.budget import BudgetError, TokenizerProfile, compile_budget_set, verify_budget_set, PADDING_PREFIX, PADDING_UNIT

ROOT = Path(__file__).resolve().parents[1]
MOCK_DIGEST = "a" * 64


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.spec = load_spec(ROOT / "examples/meridian.json")
        self.words = TokenizerProfile("synthetic-word-counter-NOT-a-model", MOCK_DIGEST, lambda x: len(x.split()))
        self.chars = TokenizerProfile("synthetic-char-counter-NOT-a-model", "b" * 64, lambda x: len(x))

    def test_natural_and_matched_both_supported(self):
        for mode in ("natural", "matched"):
            set_ = compile_budget_set(self.spec, self.words, mode=mode)
            self.assertEqual(set(set_), {"factual", "narrative", "symbolic", "hybrid"})
            self.assertTrue(verify_budget_set(set_, self.spec, self.words))
            target = max(p["natural_tokens"] for p in set_.values())
            for packet in set_.values():
                self.assertEqual(packet["target_tokens"], target)
                self.assertEqual(packet["final_tokens"], self.words.tokens(packet["content"]))
                self.assertTrue(verify_packet(packet))
                if mode == "matched":
                    self.assertGreaterEqual(packet["final_tokens"], .95 * target)
                    self.assertLessEqual(packet["final_tokens"], target)
                else:
                    self.assertEqual(packet["final_tokens"], packet["natural_tokens"])
                    self.assertEqual(packet["padding_text"], "")

    def test_actual_filler_verbatim_not_character_facts(self):
        packets = compile_budget_set(self.spec, self.words, mode="matched")
        for packet in packets.values():
            filler = packet["padding_text"]
            self.assertTrue(not filler or filler.startswith(PADDING_PREFIX))
            self.assertTrue(not filler or filler[len(PADDING_PREFIX):].replace(PADDING_UNIT, "") == "")
            self.assertNotIn("Meridian", filler)
            self.assertTrue(packet["content"].endswith(filler))
            self.assertEqual(packet["padding_utf8_bytes"], len(filler.encode("utf-8")))

    def test_another_tokenizer_means_separate_results(self):
        a = compile_budget_set(self.spec, self.words, mode="matched")
        b = compile_budget_set(self.spec, self.chars, mode="matched")
        self.assertNotEqual(a["factual"]["tokenizer_sha256"], b["factual"]["tokenizer_sha256"])
        self.assertFalse(verify_budget_set(a, self.spec, self.chars))

    def test_determinism(self):
        self.assertEqual(compile_budget_set(self.spec, self.words, mode="matched"),
                         compile_budget_set(copy.deepcopy(self.spec), self.words, mode="matched"))

    def test_mutation_and_filler_removal_rejected(self):
        packets = compile_budget_set(self.spec, self.words, mode="matched")
        corrupted = copy.deepcopy(packets)
        corrupted["factual"]["content"] += "unapproved"
        self.assertFalse(verify_budget_set(corrupted, self.spec, self.words))
        corrupted = copy.deepcopy(packets)
        corrupted["symbolic"]["padding_text"] += "SECRET"
        self.assertFalse(verify_budget_set(corrupted, self.spec, self.words))

    def test_requires_real_exact_token_count_contract(self):
        invalid = TokenizerProfile("mock", "a"*64, lambda _: 0.5)
        with self.assertRaises(BudgetError):
            compile_budget_set(self.spec, invalid, mode="matched")
        bad_fingerprint = TokenizerProfile("mock", "not-a-digest", lambda s: len(s.split()))
        with self.assertRaises(BudgetError):
            compile_budget_set(self.spec, bad_fingerprint, mode="matched")

    def test_tolerance_ceiling(self):
        with self.assertRaises(BudgetError):
            compile_budget_set(self.spec, self.words, mode="matched", tolerance=.07)

    def test_cli_rejects_matched_without_tokenizer(self):
        process = subprocess.run([sys.executable, "-m", "pce", "compile-all",
                                  "examples/river.json", "--out-dir", "ignored",
                                  "--budget-mode", "matched"], cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("tokenizer", process.stderr)


class PreregisteredBatteryTests(unittest.TestCase):
    def test_probe_classes_and_source_links(self):
        battery = json.loads((ROOT / "m3/probes.v1.json").read_text())
        self.assertEqual(len(battery["probes"]), 24)
        self.assertEqual(len({q["id"] for q in battery["probes"]}), 24)
        for persona in ("meridian", "river"):
            spec = load_spec(ROOT / f"examples/{persona}.json")
            groups = {row["id"]: group for group in ("traits", "values", "relationships", "commitments", "biography", "symbols", "style") for row in spec[group]}
            probes = [q for q in battery["probes"] if q["persona_id"] == persona]
            self.assertEqual(len(probes), 12)
            for kind in ("retrieval", "integration", "conflict"):
                items = [q for q in probes if q["probe_class"] == kind]
                self.assertEqual(len(items), 4)
                for q in items:
                    self.assertTrue(q["expected_resolution"])
                    self.assertTrue(set(q["source_field_ids"]) <= set(groups))
                    if kind == "retrieval":
                        self.assertEqual(len(q["source_field_ids"]), 1)
                        self.assertNotIn("factual_only_failure_mode", q)
                    else:
                        self.assertGreaterEqual(len({groups[v] for v in q["source_field_ids"]}), 2)
                        self.assertGreater(len(q["factual_only_failure_mode"]), 20)
                    if kind == "conflict":
                        self.assertEqual(len(q["tension_field_ids"]), 2)
                        self.assertTrue(set(q["tension_field_ids"]) <= set(q["source_field_ids"]))
                        self.assertTrue(set(q["priority_rule_ids"]) <= set(q["source_field_ids"]))
                        self.assertTrue(all(groups[i] == "values" for i in q["priority_rule_ids"]))

    def test_predeclared_anchors_comparisons_and_counts(self):
        rub = json.loads((ROOT / "m3/rubric.v1.json").read_text())
        pre = json.loads((ROOT / "m3/preregistration.v1.json").read_text())
        self.assertEqual(pre["design"]["response_slots_per_budget_mode"], 576)
        self.assertEqual(pre["design"]["total_response_slots"], 1152)
        self.assertEqual(len(pre["primary_comparisons"]), 2)
        for name, dimension in rub["dimensions"].items():
            self.assertEqual(set(dimension["anchors"]), {"0","2","4"}, name)
            self.assertTrue(all(dimension["anchors"][k] for k in ("0","2","4")))
