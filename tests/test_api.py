from api.server import app


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"
    assert data["service"] == "PolicyLang Compiler API"


def test_compile_valid_policy():
    client = app.test_client()

    source = """allow ingress
when source.ip == "10.0.0.5"
and destination.port == 443"""

    response = client.post(
        "/compile",
        json={"source": source},
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True

    assert data["policy"]["action"] == "ALLOW"
    assert data["policy"]["direction"] == "INGRESS"

    assert data["stages"]["lexer"] == "success"
    assert data["stages"]["parser"] == "success"
    assert data["stages"]["semantic_analysis"] == "success"
    assert data["stages"]["ir_lowering"] == "success"
    assert data["stages"]["optimization"] == "success"
    assert data["stages"]["ebpf_generation"] == "success"

    assert "IRPolicy(" in data["ir"]
    assert "#include <linux/bpf.h>" in data["ebpf_code"]
    assert "TC_ACT_OK" in data["ebpf_code"]


def test_compile_invalid_ipv4():
    client = app.test_client()

    source = """allow ingress
when source.ip == "999.999.999.999" """

    response = client.post(
        "/compile",
        json={"source": source},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert "999.999.999.999" in data["error"]


def test_compile_empty_policy():
    client = app.test_client()

    response = client.post(
        "/compile",
        json={"source": ""},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert "empty" in data["error"].lower()


def test_compile_missing_source():
    client = app.test_client()

    response = client.post(
        "/compile",
        json={},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert "source" in data["error"].lower()


def test_compile_deny_policy():
    client = app.test_client()

    source = """deny ingress
when destination.port == 22"""

    response = client.post(
        "/compile",
        json={"source": source},
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["policy"]["action"] == "DENY"
    assert "TC_ACT_SHOT" in data["ebpf_code"]


def test_compile_or_policy():
    client = app.test_client()

    source = """allow ingress
when destination.port == 80
or destination.port == 443"""

    response = client.post(
        "/compile",
        json={"source": source},
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert "||" in data["ebpf_code"]