"""
PolicyLang Lexer

Converts PolicyLang source code into a stream of tokens.

v0.1 scope:
- IPv4 only
- allow / deny
- ingress / egress
- source.ip / destination.ip
- source.port / destination.port
- protocol
- == / !=
- and / or
- tcp / udp / icmp
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterator


@dataclass(frozen=True)
class Token:
    type: str
    value: str
    line: int
    column: int


class LexerError(Exception):
    """Raised when invalid PolicyLang syntax is encountered."""


class Lexer:
    KEYWORDS = {
        "allow": "ALLOW",
        "deny": "DENY",
        "ingress": "INGRESS",
        "egress": "EGRESS",
        "when": "WHEN",
        "and": "AND",
        "or": "OR",
        "tcp": "TCP",
        "udp": "UDP",
        "icmp": "ICMP",
    }

    FIELD_TYPES = {
        "source.ip": "SOURCE_IP",
        "destination.ip": "DESTINATION_IP",
        "source.port": "SOURCE_PORT",
        "destination.port": "DESTINATION_PORT",
        "protocol": "PROTOCOL",
    }

    TOKEN_SPECIFICATION = [
        ("EQ", r"=="),
        ("NE", r"!="),
        ("STRING", r'"[^"\n]*"'),
        ("NUMBER", r"\d+"),
        (
            "FIELD",
            r"(?:source\.ip|destination\.ip|source\.port|destination\.port|protocol)",
        ),
        ("WORD", r"[A-Za-z_][A-Za-z0-9_]*"),
        ("NEWLINE", r"\n"),
        ("SKIP", r"[ \t\r]+"),
        ("MISMATCH", r"."),
    ]

    def __init__(self, source: str) -> None:
        self.source = source

        pattern = "|".join(
            f"(?P<{name}>{regex})"
            for name, regex in self.TOKEN_SPECIFICATION
        )

        self._regex = re.compile(pattern)

    def tokenize(self) -> Iterator[Token]:
        line = 1
        column = 1

        for match in self._regex.finditer(self.source):
            token_type = match.lastgroup
            value = match.group()

            if token_type == "NEWLINE":
                line += 1
                column = 1
                continue

            if token_type == "SKIP":
                column += len(value)
                continue

            if token_type == "WORD":
                token_type = self.KEYWORDS.get(value.lower())

                if token_type is None:
                    raise LexerError(
                        f"Unknown keyword '{value}' at "
                        f"line {line}, column {column}"
                    )

            elif token_type == "FIELD":
                token_type = self.FIELD_TYPES[value]

            elif token_type == "STRING":
                value = value[1:-1]

            elif token_type == "MISMATCH":
                raise LexerError(
                    f"Unexpected character '{value}' at "
                    f"line {line}, column {column}"
                )

            yield Token(
                type=token_type,
                value=value,
                line=line,
                column=column,
            )

            column += len(match.group())


def tokenize(source: str) -> list[Token]:
    """Convenience function for tokenizing PolicyLang source."""
    return list(Lexer(source).tokenize())