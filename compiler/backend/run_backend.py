from pathlib import Path

from compiler.parser.parser import parse
from compiler.semantic.analyzer import analyze
from compiler.ir.lower import lower_policy
from compiler.optimizer.optimizer import optimize_policy
from compiler.backend.ebpf_generator import generate_ebpf_c


SOURCE = """allow ingress
when source.ip == "10.0.0.5"
and destination.port == 443
"""


def main() -> None:
    print("==================================================")
    print("              PolicyLang Compiler")
    print("==================================================")
    print()

    print("SOURCE")
    print("------")
    print(SOURCE)

    print("1. Parsing...")
    policy = parse(SOURCE)
    print("   ✓ Parser successful")

    print("2. Semantic analysis...")
    analyze(policy)
    print("   ✓ Policy is valid")

    print("3. Lowering to IR...")
    ir = lower_policy(policy)
    print("   ✓ IR generated")
    print()
    print(ir)

    print()
    print("4. Optimizing IR...")
    optimized_ir = optimize_policy(ir)
    print("   ✓ Optimization complete")
    print()
    print(optimized_ir)

    print()
    print("5. Generating eBPF C...")
    ebpf_code = generate_ebpf_c(optimized_ir)
    print("   ✓ eBPF C generated")

    output_path = Path("build/policy.bpf.c")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(ebpf_code, encoding="utf-8")

    print()
    print("==================================================")
    print("               COMPILATION COMPLETE")
    print("==================================================")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()