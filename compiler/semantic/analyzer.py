"""
PolicyLang Semantic Analyzer

Validates the meaning of a parsed PolicyLang AST.

Responsibilities:
- Validate IPv4 addresses.
- Validate port ranges.
- Validate supported protocols.
- Validate field/value compatibility.
"""

from __future__ import annotations

import ipaddress

from compiler.ast.nodes import Comparison, LogicalExpression, Policy, Condition


class SemanticError(Exception):
    """Raised when a PolicyLang program is semantically invalid."""


SUPPORTED_PROTOCOLS = {"tcp", "udp", "icmp"}

IP_FIELDS = {
    "source.ip",
    "destination.ip",
}

PORT_FIELDS = {
    "source.port",
    "destination.port",
}


def validate_ipv4(value: object) -> None:
    if not isinstance(value, str):
        raise SemanticError(
            f"IPv4 address must be a string, got {type(value).__name__}."
        )

    try:
        address = ipaddress.ip_address(value)
    except ValueError as exc:
        raise SemanticError(f"Invalid IPv4 address: {value}") from exc

    if address.version != 4:
        raise SemanticError(f"Only IPv4 is supported in PolicyLang v0.1: {value}")


def validate_port(value: object) -> None:
    if not isinstance(value, int):
        raise SemanticError(
            f"Port must be an integer, got {type(value).__name__}."
        )

    if not 0 <= value <= 65535:
        raise SemanticError(
            f"Port must be between 0 and 65535: {value}"
        )


def validate_protocol(value: object) -> None:
    if not isinstance(value, str):
        raise SemanticError(
            f"Protocol must be a string, got {type(value).__name__}."
        )

    if value.lower() not in SUPPORTED_PROTOCOLS:
        raise SemanticError(
            f"Unsupported protocol '{value}'. "
            f"Supported protocols: tcp, udp, icmp."
        )


def validate_comparison(comparison: Comparison) -> None:
    if comparison.operator not in {"==", "!="}:
        raise SemanticError(
            f"Unsupported operator: {comparison.operator}"
        )

    field = comparison.field
    value = comparison.value

    if field in IP_FIELDS:
        validate_ipv4(value)
        return

    if field in PORT_FIELDS:
        validate_port(value)
        return

    if field == "protocol":
        validate_protocol(value)
        return

    raise SemanticError(f"Unsupported field: {field}")


def validate_condition(condition: Condition) -> None:
    if isinstance(condition, Comparison):
        validate_comparison(condition)
        return

    if isinstance(condition, LogicalExpression):
        if condition.operator not in {"AND", "OR"}:
            raise SemanticError(
                f"Unsupported logical operator: {condition.operator}"
            )

        validate_condition(condition.left)
        validate_condition(condition.right)
        return

    raise SemanticError(
        f"Unknown condition node: {type(condition).__name__}"
    )


def analyze(policy: Policy) -> Policy:
    """Validate a complete PolicyLang AST and return it unchanged."""

    if policy.action not in {"ALLOW", "DENY"}:
        raise SemanticError(f"Unsupported action: {policy.action}")

    if policy.direction not in {"INGRESS", "EGRESS"}:
        raise SemanticError(f"Unsupported direction: {policy.direction}")

    validate_condition(policy.condition)

    return policy