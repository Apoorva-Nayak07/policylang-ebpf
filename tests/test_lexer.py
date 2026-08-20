import pytest

from compiler.lexer.lexer import LexerError, tokenize


def test_https_policy():
    source = """allow ingress
when source.ip == "10.0.0.5"
and destination.port == 443
"""

    tokens = tokenize(source)

    assert [token.type for token in tokens] == [
        "ALLOW",
        "INGRESS",
        "WHEN",
        "SOURCE_IP",
        "EQ",
        "STRING",
        "AND",
        "DESTINATION_PORT",
        "EQ",
        "NUMBER",
    ]


def test_deny_ip_policy():
    source = """deny ingress
when source.ip == "192.168.1.10"
"""

    tokens = tokenize(source)

    assert [token.type for token in tokens] == [
        "DENY",
        "INGRESS",
        "WHEN",
        "SOURCE_IP",
        "EQ",
        "STRING",
    ]


def test_ssh_policy():
    source = """allow ingress
when protocol == "tcp"
and destination.port == 22
"""

    tokens = tokenize(source)

    assert [token.type for token in tokens] == [
        "ALLOW",
        "INGRESS",
        "WHEN",
        "PROTOCOL",
        "EQ",
        "STRING",
        "AND",
        "DESTINATION_PORT",
        "EQ",
        "NUMBER",
    ]


def test_unknown_keyword_is_rejected():
    source = """permit ingress
when source.ip == "10.0.0.5"
"""

    with pytest.raises(LexerError):
        tokenize(source)


def test_invalid_character_is_rejected():
    source = """allow ingress
when source.ip @ "10.0.0.5"
"""

    with pytest.raises(LexerError):
        tokenize(source)


def test_unknown_field_is_rejected():
    source = """allow ingress
when source.mac == "AA:BB:CC:DD:EE:FF"
"""

    with pytest.raises(LexerError):
        tokenize(source)