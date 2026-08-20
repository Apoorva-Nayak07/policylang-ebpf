from compiler.lexer.lexer import tokenize


source = """allow ingress
when source.ip == "10.0.0.5"
and destination.port == 443
"""


print("PolicyLang Source:")
print("------------------")
print(source)

print("Tokens:")
print("------------------")

for token in tokenize(source):
    print(
        f"{token.type:<20} "
        f"value={token.value!r:<15} "
        f"line={token.line} "
        f"column={token.column}"
    )