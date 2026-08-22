from compiler.parser.parser import parse
from compiler.semantic.analyzer import analyze
from compiler.ir.lower import lower_policy


source = """allow ingress
when source.ip == "10.0.0.5"
and destination.port == 443
"""


print("PolicyLang Source")
print("-----------------")
print(source)

policy = parse(source)
analyze(policy)

ir = lower_policy(policy)

print("Policy IR")
print("-----------------")
print(ir)