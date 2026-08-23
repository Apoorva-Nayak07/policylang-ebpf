"""
PolicyLang command-line compiler.

Usage:
    python -m policylang <policy-file>
"""

from __future__ import annotations

import sys
from pathlib import Path

from compiler.backend.ebpf_generator import generate_ebpf_c
from compiler.ir.lower import lower_policy
from compiler.optimizer.optimizer import optimize_policy
from compiler.parser.parser import parse
from compiler.semantic.analyzer import analyze


def compile_policy(input_path: Path) -> Path:
    source = input_path.read_text(encoding="utf-8")

    print("=" * 60)
    print("                PolicyLang Compiler v0.1")
    print("=" * 60)
    print()
    print(f"Input: {input_path}")
    print()

    print("[1/6] Lexing              ✓")
    print("[2/6] Parsing...")
    policy = parse(source)
    print("       ✓")

    print("[3/6] Semantic Analysis...")
    analyze(policy)
    print("       ✓")

    print("[4/6] IR Lowering...")
    ir = lower_policy(policy)
    print("       ✓")

    print("[5/6] Optimization...")
    optimized_ir = optimize_policy(ir)
    print("       ✓")

    print("[6/6] eBPF Generation...")
    ebpf_code = generate_ebpf_c(optimized_ir)
    print("       ✓")

    output_dir = Path("build")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{input_path.stem}.bpf.c"
    output_path.write_text(ebpf_code, encoding="utf-8")

    print()
    print("Compilation successful.")
    print(f"Output: {output_path}")

    return output_path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m policylang <policy-file>")
        return 1

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: input file not found: {input_path}")
        return 1

    try:
        compile_policy(input_path)
    except Exception as exc:
        print()
        print(f"Compilation failed: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())