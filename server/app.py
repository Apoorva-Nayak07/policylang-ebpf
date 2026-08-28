from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from compiler.parser.parser import parse
from compiler.semantic.analyzer import analyze
from compiler.ir.lower import lower_policy
from compiler.optimizer.optimizer import optimize_policy
from compiler.backend.ebpf_generator import generate_ebpf_c


app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "PolicyLang Compiler API"
    })


@app.post("/compile")
def compile_policy():
    data = request.get_json(silent=True)

    if not data or "policy" not in data:
        return jsonify({
            "success": False,
            "error": "Missing 'policy' field"
        }), 400

    source = data["policy"]

    try:
        # 1. Parsing
        policy = parse(source)

        # 2. Semantic analysis
        analyze(policy)

        # 3. IR lowering
        ir = lower_policy(policy)

        # 4. Optimization
        optimized_ir = optimize_policy(ir)

        # 5. eBPF generation
        ebpf_code = generate_ebpf_c(optimized_ir)

        # Save generated output
        output_dir = Path("build")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / "policy.bpf.c"
        output_path.write_text(
            ebpf_code,
            encoding="utf-8"
        )

        return jsonify({
            "success": True,
            "stages": {
                "lexer": "success",
                "parser": "success",
                "semantic": "success",
                "ir": "success",
                "optimizer": "success",
                "ebpf": "success"
            },
            "ir": str(optimized_ir),
            "ebpf": ebpf_code,
            "output": str(output_path)
        })

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 400


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )