from compiler.parser.parser import parse


source = """allow ingress
when source.ip == "10.0.0.5"
and destination.port == 443
"""


print("PolicyLang Source")
print("------------------")
print(source)

print("AST")
print("------------------")

policy = parse(source)

print(policy)