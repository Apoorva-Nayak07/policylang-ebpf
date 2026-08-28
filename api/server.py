from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from compiler.backend.ebpf_generator import generate_ebpf_c
from compiler.ir.lower import lower_policy
from compiler.optimizer.optimizer import optimize_policy
from compiler.parser.parser import parse
from compiler.semantic.analyzer import analyze


app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "PolicyLang Compiler API",
        "version": "0.1",
    })


@app.post("/compile")
def compile_policy():
    data = request.get_json(silent=True)

    if not data or "source" not in data:
        return jsonify({
            "success": False,
            "error": "Missing 'source' in request body",
        }), 400

    source = data["source"]

    if not isinstance(source, str) or not source.strip():
        return jsonify({
            "success": False,
            "error": "Policy source cannot be empty",
        }), 400

    try:
        # ---------------------------------------------------------
        # 1. Parse
        # ---------------------------------------------------------
        policy = parse(source)

        # ---------------------------------------------------------
        # 2. Semantic analysis
        # ---------------------------------------------------------
        analyze(policy)

        # ---------------------------------------------------------
        # 3. Lower AST -> IR
        # ---------------------------------------------------------
        ir = lower_policy(policy)

        # ---------------------------------------------------------
        # 4. Optimize IR
        # ---------------------------------------------------------
        optimized_ir = optimize_policy(ir)

        # ---------------------------------------------------------
        # 5. Generate eBPF C
        # ---------------------------------------------------------
        ebpf_code = generate_ebpf_c(optimized_ir)

        # ---------------------------------------------------------
        # Save generated C
        # ---------------------------------------------------------
        output_dir = Path("build")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / "api_policy.bpf.c"

        output_path.write_text(
            ebpf_code,
            encoding="utf-8",
        )

        # ---------------------------------------------------------
        # Return compiler result
        # ---------------------------------------------------------
        return jsonify({
            "success": True,

            "policy": {
                "action": policy.action,
                "direction": policy.direction,
            },

            "stages": {
                "lexer": "success",
                "parser": "success",
                "semantic_analysis": "success",
                "ir_lowering": "success",
                "optimization": "success",
                "ebpf_generation": "success",
            },

            "ir": repr(optimized_ir),

            "output_file": str(output_path),

            "ebpf_code": ebpf_code,
        })

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": str(exc),
        }), 400


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )