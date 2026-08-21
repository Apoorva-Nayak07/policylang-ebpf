import pytest

from compiler.ast.nodes import Comparison, LogicalExpression, Policy
from compiler.parser.parser import ParserError, parse


def test_parse_basic_https_policy():
    source = """allow ingress
when source.ip == "10.0.0.5"
and destination.port == 443
"""

    policy = parse(source)

    assert isinstance(policy, Policy)
    assert policy.action == "ALLOW"
    assert policy.direction == "INGRESS"

    assert isinstance(policy.condition, LogicalExpression)
    assert policy.condition.operator == "AND"

    assert policy.condition.left == Comparison(
        field="source.ip",
        operator="==",
        value="10.0.0.5",
    )

    assert policy.condition.right == Comparison(
        field="destination.port",
        operator="==",
        value=443,
    )


def test_parse_deny_policy():
    source = """deny ingress
when source.ip == "192.168.1.10"
"""

    policy = parse(source)

    assert policy.action == "DENY"
    assert policy.direction == "INGRESS"

    assert policy.condition == Comparison(
        field="source.ip",
        operator="==",
        value="192.168.1.10",
    )


def test_parse_egress_policy():
    source = """allow egress
when destination.port == 443
"""

    policy = parse(source)

    assert policy.action == "ALLOW"
    assert policy.direction == "EGRESS"

    assert policy.condition == Comparison(
        field="destination.port",
        operator="==",
        value=443,
    )


def test_parse_not_equal_operator():
    source = """deny ingress
when source.ip != "10.0.0.5"
"""

    policy = parse(source)

    assert policy.condition == Comparison(
        field="source.ip",
        operator="!=",
        value="10.0.0.5",
    )


def test_missing_when_is_rejected():
    source = """allow ingress
source.ip == "10.0.0.5"
"""

    with pytest.raises(ParserError):
        parse(source)


def test_invalid_action_is_rejected():
    source = """permit ingress
when source.ip == "10.0.0.5"
"""

    with pytest.raises(ParserError):
        parse(source)


def test_invalid_field_is_rejected():
    source = """allow ingress
when source.mac == "AA:BB:CC:DD:EE:FF"
"""

    with pytest.raises(ParserError):
        parse(source)


def test_invalid_operator_is_rejected():
    source = """allow ingress
when source.ip = "10.0.0.5"
"""

    with pytest.raises(ParserError):
        parse(source)