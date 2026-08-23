import pytest

from compiler.backend.ebpf_generator import (
    EBPFGenerationError,
    generate_ebpf_c,
)
from compiler.ir.ir import (
    IRComparison,
    IRLogical,
    IRPolicy,
)


def test_generate_allow_policy():
    policy = IRPolicy(
        action="ALLOW",
        direction="INGRESS",
        condition=IRComparison(
            field="SRC_IP",
            operator="EQ",
            value="10.0.0.5",
        ),
    )

    code = generate_ebpf_c(policy)

    assert "src_ip == 0x0a000005" in code
    assert "return TC_ACT_OK;" in code
    assert "return TC_ACT_SHOT;" in code


def test_generate_deny_policy():
    policy = IRPolicy(
        action="DENY",
        direction="INGRESS",
        condition=IRComparison(
            field="SRC_IP",
            operator="EQ",
            value="10.0.0.5",
        ),
    )

    code = generate_ebpf_c(policy)

    assert "src_ip == 0x0a000005" in code
    assert "return TC_ACT_SHOT;" in code
    assert "return TC_ACT_OK;" in code


def test_generate_destination_port():
    policy = IRPolicy(
        action="ALLOW",
        direction="INGRESS",
        condition=IRComparison(
            field="DST_PORT",
            operator="EQ",
            value=443,
        ),
    )

    code = generate_ebpf_c(policy)

    assert "dst_port == 443" in code


def test_generate_not_equal():
    policy = IRPolicy(
        action="DENY",
        direction="INGRESS",
        condition=IRComparison(
            field="SRC_IP",
            operator="NE",
            value="192.168.1.10",
        ),
    )

    code = generate_ebpf_c(policy)

    assert "src_ip != 0xc0a8010a" in code


def test_generate_and_condition():
    condition = IRLogical(
        operator="AND",
        left=IRComparison(
            field="SRC_IP",
            operator="EQ",
            value="10.0.0.5",
        ),
        right=IRComparison(
            field="DST_PORT",
            operator="EQ",
            value=443,
        ),
    )

    policy = IRPolicy(
        action="ALLOW",
        direction="INGRESS",
        condition=condition,
    )

    code = generate_ebpf_c(policy)

    assert "src_ip == 0x0a000005" in code
    assert "dst_port == 443" in code
    assert "&&" in code


def test_generate_or_condition():
    condition = IRLogical(
        operator="OR",
        left=IRComparison(
            field="DST_PORT",
            operator="EQ",
            value=80,
        ),
        right=IRComparison(
            field="DST_PORT",
            operator="EQ",
            value=443,
        ),
    )

    policy = IRPolicy(
        action="ALLOW",
        direction="INGRESS",
        condition=condition,
    )

    code = generate_ebpf_c(policy)

    assert "dst_port == 80" in code
    assert "dst_port == 443" in code
    assert "||" in code


def test_generate_tcp_protocol():
    policy = IRPolicy(
        action="ALLOW",
        direction="INGRESS",
        condition=IRComparison(
            field="PROTOCOL",
            operator="EQ",
            value="tcp",
        ),
    )

    code = generate_ebpf_c(policy)

    assert "protocol == IPPROTO_TCP" in code


def test_generate_udp_protocol():
    policy = IRPolicy(
        action="ALLOW",
        direction="INGRESS",
        condition=IRComparison(
            field="PROTOCOL",
            operator="EQ",
            value="udp",
        ),
    )

    code = generate_ebpf_c(policy)

    assert "protocol == IPPROTO_UDP" in code


def test_invalid_ipv4_is_rejected():
    policy = IRPolicy(
        action="ALLOW",
        direction="INGRESS",
        condition=IRComparison(
            field="SRC_IP",
            operator="EQ",
            value="999.999.999.999",
        ),
    )

    with pytest.raises(EBPFGenerationError):
        generate_ebpf_c(policy)


def test_invalid_protocol_is_rejected():
    policy = IRPolicy(
        action="ALLOW",
        direction="INGRESS",
        condition=IRComparison(
            field="PROTOCOL",
            operator="EQ",
            value="ftp",
        ),
    )

    with pytest.raises(EBPFGenerationError):
        generate_ebpf_c(policy)