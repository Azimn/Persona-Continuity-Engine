"""Read-only packet determinism, provenance and CLI smoke tests."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from pce import STRATEGIES, compile_packet, digest, load_spec, verify_packet
from pce.spec import GROUPS

ROOT = Path(__file__).resolve().parents[1]


class CompilerTests(unittest.TestCase):
    def setUp(self):
        self.spec = load_spec(ROOT / "examples/meridian.json")

    def test_all_four_strategies_have_all_evidence_content(self):
        for strategy in STRATEGIES:
            packet = compile_packet(self.spec, strategy)
            for group in GROUPS:
                for item in self.spec[group]:
                    self.assertIn(item["text"], packet["content"])
            for item in self.spec["symbols"]:
                self.assertIn(item["cue"], packet["content"])
                self.assertIn(item["meaning"], packet["content"])
            self.assertTrue(verify_packet(packet, self.spec))

    def test_determinism_and_provenance(self):
        for strategy in STRATEGIES:
            self.assertEqual(compile_packet(self.spec, strategy), compile_packet(copy.deepcopy(self.spec), strategy))
            self.assertEqual(compile_packet(self.spec, strategy)["source_spec_sha256"], digest(self.spec))

    def test_source_mutation_changes_packet_and_rejects_old_spec(self):
        old = compile_packet(self.spec, "factual")
        changed = copy.deepcopy(self.spec)
        changed["values"][0]["text"] += " However, it can be costly."
        new = compile_packet(changed, "factual")
        self.assertNotEqual(old["packet_sha256"], new["packet_sha256"])
        self.assertFalse(verify_packet(old, changed))

    def test_packet_corruption_detected(self):
        packet = compile_packet(self.spec, "hybrid")
        packet["content"] += "tampered"
        self.assertFalse(verify_packet(packet))

    def test_undefined_strategy_fails(self):
        with self.assertRaises(ValueError):
            compile_packet(self.spec, "neural")

    def test_compile_is_read_only(self):
        before = digest(self.spec)
        compile_packet(self.spec, "narrative")
        self.assertEqual(digest(self.spec), before)

    def test_cli_validate(self):
        proc = subprocess.run([sys.executable, "-m", "pce", "validate", "examples/river.json"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["status"], "valid")

    def test_cli_compile_all(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run([sys.executable, "-m", "pce", "compile-all", "examples/meridian.json", "--out-dir", tmp], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(len(list(Path(tmp).glob("*.json"))), 4)
            packet = json.loads((Path(tmp) / "meridian.symbolic.json").read_text(encoding="utf-8"))
            self.assertTrue(verify_packet(packet, self.spec))

    def test_cli_invalid_spec_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text('{"schema_version": "1.0"}')
            proc = subprocess.run([sys.executable, "-m", "pce", "validate", str(path)], cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)

    def test_bytes_are_actual_utf8(self):
        pkt = compile_packet(self.spec, "symbolic")
        self.assertEqual(pkt["content_utf8_bytes"], len(pkt["content"].encode("utf-8")))
        self.assertEqual(pkt["content_sha256"], hashlib.sha256(pkt["content"].encode("utf-8")).hexdigest())
