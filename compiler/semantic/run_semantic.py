from compiler.parser.parser import parse
from compiler.semantic.analyzer import SemanticError, analyze


def test_policy(name: str, source: str) -> None:
    print(f"\n{name}")
    print("-" * len(name))

    try:
        policy = parse(source)
        analyze(policy)
        print("✅ VALID")
    except SemanticError as exc:
        print(f"❌ INVALID: {exc}")


valid_policy = """allow ingress
when source.ip == "10.0.0.5"
and destination.port == 443
"""


invalid_ip = """allow ingress
when source.ip == "999.999.999.999"
"""


invalid_port = """allow ingress
when destination.port == 65536
"""


invalid_protocol = """allow ingress
when protocol == "ftp"
"""


test_policy("Valid Policy", valid_policy)
test_policy("Invalid IPv4", invalid_ip)
test_policy("Invalid Port", invalid_port)
test_policy("Invalid Protocol", invalid_protocol)