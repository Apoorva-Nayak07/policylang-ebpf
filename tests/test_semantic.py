import pytest

from compiler.parser.parser import parse
from compiler.semantic.analyzer import SemanticError, analyze


def test_valid_ipv4_and_port():
    source = """allow ingress
when source.ip == "10.0.0.5"
and destination.port == 443
"""

    policy = parse(source)

    assert analyze(policy) == policy


def test_valid_egress_policy():
    source = """allow egress
when destination.ip == "192.168.1.10"
"""

    policy = parse(source)

    assert analyze(policy) == policy


def test_invalid_ipv4_is_rejected():
    source = """allow ingress
when source.ip == "999.999.999.999"
"""

    policy = parse(source)

    with pytest.raises(SemanticError, match="Invalid IPv4 address"):
        analyze(policy)


def test_invalid_port_is_rejected():
    source = """allow ingress
when destination.port == 65536
"""

    policy = parse(source)

    with pytest.raises(SemanticError, match="Port must be between"):
        analyze(policy)


def test_negative_port_is_rejected_by_parser():
    source = """allow ingress
when destination.port == -1
"""

    with pytest.raises(Exception):
        parse(source)


def test_invalid_protocol_is_rejected():
    source = """allow ingress
when protocol == "ftp"
"""

    policy = parse(source)

    with pytest.raises(SemanticError, match="Unsupported protocol"):
        analyze(policy)


def test_valid_tcp_protocol():
    source = """allow ingress
when protocol == "tcp"
"""

    policy = parse(source)

    assert analyze(policy) == policy


def test_valid_udp_protocol():
    source = """allow ingress
when protocol == "udp"
"""

    policy = parse(source)

    assert analyze(policy) == policy


def test_valid_icmp_protocol():
    source = """allow ingress
when protocol == "icmp"
"""

    policy = parse(source)

    assert analyze(policy) == policy