"""
PolicyLang Parser

Converts the token stream produced by the lexer
into a PolicyLang Abstract Syntax Tree (AST).
"""

from __future__ import annotations

from compiler.ast.nodes import Comparison, LogicalExpression, Policy, Condition
from compiler.lexer.lexer import LexerError, Token, tokenize


class ParserError(Exception):
    """Raised when the token stream does not match PolicyLang grammar."""


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.position = 0

    def current(self) -> Token | None:
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]

    def advance(self) -> Token:
        token = self.current()

        if token is None:
            raise ParserError("Unexpected end of input.")

        self.position += 1
        return token

    def expect(self, token_type: str) -> Token:
        token = self.current()

        if token is None:
            raise ParserError(
                f"Expected {token_type}, but reached end of input."
            )

        if token.type != token_type:
            raise ParserError(
                f"Expected {token_type}, got {token.type} "
                f"at line {token.line}, column {token.column}."
            )

        self.position += 1
        return token

    def parse(self) -> Policy:
        """Parse a complete PolicyLang program."""

        action = self.expect_action()
        direction = self.expect_direction()

        self.expect("WHEN")

        condition = self.parse_condition()

        if self.current() is not None:
            token = self.current()
            raise ParserError(
                f"Unexpected token {token.type} at "
                f"line {token.line}, column {token.column}."
            )

        return Policy(
            action=action,
            direction=direction,
            condition=condition,
        )

    def expect_action(self) -> str:
        token = self.current()

        if token is None:
            raise ParserError("Expected ALLOW or DENY.")

        if token.type == "ALLOW":
            self.position += 1
            return "ALLOW"

        if token.type == "DENY":
            self.position += 1
            return "DENY"

        raise ParserError(
            f"Expected ALLOW or DENY, got {token.type} "
            f"at line {token.line}, column {token.column}."
        )

    def expect_direction(self) -> str:
        token = self.current()

        if token is None:
            raise ParserError("Expected INGRESS or EGRESS.")

        if token.type == "INGRESS":
            self.position += 1
            return "INGRESS"

        if token.type == "EGRESS":
            self.position += 1
            return "EGRESS"

        raise ParserError(
            f"Expected INGRESS or EGRESS, got {token.type} "
            f"at line {token.line}, column {token.column}."
        )

    def parse_condition(self) -> Condition:
        left = self.parse_expression()

        while self.current() is not None and self.current().type in {"AND", "OR"}:
            operator = self.advance().type
            right = self.parse_expression()

            left = LogicalExpression(
                operator=operator,
                left=left,
                right=right,
            )

        return left

    def parse_expression(self) -> Comparison:
        field = self.parse_field()
        operator = self.parse_operator()
        value = self.parse_value()

        return Comparison(
            field=field,
            operator=operator,
            value=value,
        )

    def parse_field(self) -> str:
        field_tokens = {
            "SOURCE_IP": "source.ip",
            "DESTINATION_IP": "destination.ip",
            "SOURCE_PORT": "source.port",
            "DESTINATION_PORT": "destination.port",
            "PROTOCOL": "protocol",
        }

        token = self.current()

        if token is None:
            raise ParserError("Expected a field.")

        if token.type not in field_tokens:
            raise ParserError(
                f"Expected a field, got {token.type} "
                f"at line {token.line}, column {token.column}."
            )

        self.position += 1
        return field_tokens[token.type]

    def parse_operator(self) -> str:
        token = self.current()

        if token is None:
            raise ParserError("Expected comparison operator.")

        if token.type == "EQ":
            self.position += 1
            return "=="

        if token.type == "NE":
            self.position += 1
            return "!="

        raise ParserError(
            f"Expected == or !=, got {token.type} "
            f"at line {token.line}, column {token.column}."
        )

    def parse_value(self) -> str | int:
        token = self.current()

        if token is None:
            raise ParserError("Expected a value.")

        if token.type == "STRING":
            self.position += 1
            return token.value

        if token.type == "NUMBER":
            self.position += 1
            return int(token.value)

        raise ParserError(
            f"Expected STRING or NUMBER, got {token.type} "
            f"at line {token.line}, column {token.column}."
        )


def parse(source: str) -> Policy:
    """Convenience function for parsing PolicyLang source."""

    try:
        tokens = tokenize(source)
    except LexerError as exc:
        raise ParserError(str(exc)) from exc

    return Parser(tokens).parse()