from compiler.parser.parser import parse
from compiler.semantic.analyzer import analyze
from compiler.ir.lower import lower_policy
from compiler.optimizer.optimizer import optimize_policy
from compiler.backend.ebpf_generator import generate_ebpf_c


SOURCE = """allow ingress
when source.ip == "10.0.0.5"
and destination.port == 443
"""


print("==================================================")
print("              PolicyLang Compiler")
print("==================================================")

print()
print("SOURCE")
print("------")
print(SOURCE)

# --------------------------------------------------
# 1. PARSE
# --------------------------------------------------

print("1. Parsing...")
policy = parse(SOURCE)
print("   ✓ Parser successful")

# --------------------------------------------------
# 2. SEMANTIC ANALYSIS
# --------------------------------------------------

print("2. Semantic analysis...")
analyze(policy)
print("   ✓ Policy is valid")

# --------------------------------------------------
# 3. LOWER TO IR
# --------------------------------------------------

print("3. Lowering to IR...")
ir = lower_policy(policy)
print("   ✓ IR generated")
print()
print(ir)

# --------------------------------------------------
# 4. OPTIMIZE
# --------------------------------------------------

print()
print("4. Optimizing IR...")
optimized_ir = optimize_policy(ir)
print("   ✓ Optimization complete")
print()
print(optimized_ir)

# --------------------------------------------------
# 5. GENERATE eBPF C
# --------------------------------------------------

print()
print("5. Generating eBPF C...")
ebpf_code = generate_ebpf_c(optimized_ir)

print("   ✓ eBPF C generated")

print()
print("==================================================")
print("                 GENERATED eBPF")
print("==================================================")
print()
print(ebpf_code)