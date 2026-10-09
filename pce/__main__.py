"""Python -m pce entry point: offline inspection and compilation only."""
from __future__ import annotations

import argparse
import json
import pathlib

from . import STRATEGIES, SpecError, compile_packet, digest, load_spec, verify_packet


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pce", description="Offline persona spec validator and conditioning compiler")
    commands = parser.add_subparsers(dest="action", required=True)
    valid = commands.add_parser("validate", help="Check an authoritatively supplied PersonaSpec")
    valid.add_argument("spec", type=pathlib.Path)
    comp = commands.add_parser("compile", help="Create one versioned conditioning packet")
    comp.add_argument("spec", type=pathlib.Path)
    comp.add_argument("--strategy", choices=STRATEGIES, required=True)
    comp.add_argument("--out", type=pathlib.Path, required=True)
    all_cmd = commands.add_parser("compile-all", help="Compile all four conditioning packets")
    all_cmd.add_argument("spec", type=pathlib.Path)
    all_cmd.add_argument("--out-dir", type=pathlib.Path, required=True)
    args = parser.parse_args(argv)
    try:
        spec = load_spec(args.spec)
    except SpecError as exc:
        parser.error(str(exc))
    if args.action == "validate":
        print(json.dumps({"status": "valid", "persona_id": spec["persona_id"], "source_spec_sha256": digest(spec)}, sort_keys=True))
        return 0
    if args.action == "compile":
        outputs = [(args.out, compile_packet(spec, args.strategy))]
    else:
        outputs = [(args.out_dir / f"{spec['persona_id']}.{strategy}.json", compile_packet(spec, strategy)) for strategy in STRATEGIES]
    for path, packet in outputs:
        if not verify_packet(packet, spec):
            parser.error("internal packet verification failed")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(packet, sort_keys=True, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"file": str(path), "strategy": packet["strategy"], "packet_sha256": packet["packet_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
