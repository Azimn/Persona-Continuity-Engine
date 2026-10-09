"""Offline integrity tests for exact schema and epistemic authority."""
import copy
import json
from pathlib import Path
import unittest
from pce import SpecError, digest, load_spec, validate_spec

ROOT = Path(__file__).resolve().parents[1]


class SpecTests(unittest.TestCase):
    def setUp(self):
        self.spec = load_spec(ROOT / "examples/meridian.json")

    def test_examples_valid(self):
        self.assertEqual(load_spec(ROOT / "examples/river.json")["persona_id"], "river")

    def test_digest_independent_of_json_key_order(self):
        self.assertEqual(digest(self.spec), digest(json.loads(json.dumps(self.spec, sort_keys=True))))

    def test_unknown_top_level_rejected(self):
        spec = copy.deepcopy(self.spec)
        spec["surprise"] = 10
        with self.assertRaises(SpecError):
            validate_spec(spec)

    def test_missing_required_rejected(self):
        spec = copy.deepcopy(self.spec)
        del spec["values"]
        with self.assertRaises(SpecError):
            validate_spec(spec)

    def test_unknown_evidence_rejected(self):
        spec = copy.deepcopy(self.spec)
        spec["traits"][0]["evidence_ids"] = ["E999"]
        with self.assertRaises(SpecError):
            validate_spec(spec)

    def test_duplicate_ids_rejected(self):
        spec = copy.deepcopy(self.spec)
        spec["values"][0]["id"] = spec["traits"][0]["id"]
        with self.assertRaises(SpecError):
            validate_spec(spec)

    def test_duplicate_links_rejected(self):
        spec = copy.deepcopy(self.spec)
        spec["traits"][0]["evidence_ids"] = ["E01", "E01"]
        with self.assertRaises(SpecError):
            validate_spec(spec)

    def test_synthetic_authority_not_laundered(self):
        spec = copy.deepcopy(self.spec)
        spec["evidence"][0]["epistemic_status"] = "lived_record"
        with self.assertRaises(SpecError):
            validate_spec(spec)

    def test_no_unknown_statement_extensions(self):
        spec = copy.deepcopy(self.spec)
        spec["biography"][0]["secret_runtime_override"] = True
        with self.assertRaises(SpecError):
            validate_spec(spec)

    def test_unknown_schema_rejected(self):
        spec = copy.deepcopy(self.spec)
        spec["schema_version"] = "2.0"
        with self.assertRaises(SpecError):
            validate_spec(spec)
