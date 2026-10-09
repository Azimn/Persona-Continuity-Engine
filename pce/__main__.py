"""Python -m pce entry point: offline inspection and compilation only."""
from __future__ import annotations

import argparse
import json
import pathlib

from . import STRATEGIES, SpecError, compile_packet, digest, load_spec, verify_packet
from .budget import BudgetError, compile_budget_set, load_local_tokenizer_json, verify_budget_set


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
    for command in (comp, all_cmd):
        command.add_argument("--budget-mode", choices=("natural", "matched"), default="natural")
        command.add_argument("--tokenizer-json", type=pathlib.Path, help="exact target model tokenizer.json on local disk; optional dependency")
        command.add_argument("--tokenizer-id", help="exact target model or tokenizer revision identifier")
    args = parser.parse_args(argv)
    try:
        spec = load_spec(args.spec)
    except SpecError as exc:
        parser.error(str(exc))
    if args.action == "validate":
        print(json.dumps({"status": "valid", "persona_id": spec["persona_id"], "source_spec_sha256": digest(spec)}, sort_keys=True))
        return 0
    if bool(args.tokenizer_json) != bool(args.tokenizer_id):
        parser.error("--tokenizer-json and --tokenizer-id must be supplied together")
    if args.budget_mode == "matched" and not args.tokenizer_json:
        parser.error("matched mode requires the exact target tokenizer.json and tokenizer ID")
    profile = None
    if args.tokenizer_json:
        try:
            profile = load_local_tokenizer_json(args.tokenizer_json, args.tokenizer_id)
            packets = compile_budget_set(spec, profile, mode=args.budget_mode)
        except (BudgetError, OSError, ValueError) as exc:
            parser.error(str(exc))
        if not verify_budget_set(packets, spec, profile):
            parser.error("exact tokenizer budget-set verification failed")
    else:
        packets = {s: compile_packet(spec, s) for s in STRATEGIES}
    if args.action == "compile":
        outputs = [(args.out, packets[args.strategy])]
    else:
        outputs = [(args.out_dir / f"{spec['persona_id']}.{strategy}.json", packets[strategy]) for strategy in STRATEGIES]
    for path, packet in outputs:
        if not verify_packet(packet) or (profile is None and not verify_packet(packet, spec)):
            parser.error("internal packet verification failed")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(packet, sort_keys=True, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"file": str(path), "strategy": packet["strategy"], "packet_sha256": packet["packet_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
