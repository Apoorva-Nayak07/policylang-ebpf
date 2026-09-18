# 🛡️ PolicyLang

### 🚀 A Human-Readable Security Policy Language & Explainable eBPF Compiler

<p align="center">

**Write security intent in simple language → Compile it → Generate eBPF → Inspect the result**

</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![eBPF](https://img.shields.io/badge/eBPF-Linux-orange?logo=linux)
![LLVM](https://img.shields.io/badge/LLVM%2FClang-eBPF-purple?logo=llvm)
![Flask](https://img.shields.io/badge/API-Flask-black?logo=flask)
![pytest](https://img.shields.io/badge/tests-49%20passed-brightgreen?logo=pytest)
![License](https://img.shields.io/badge/license-Educational%2FResearch-lightgrey)

</p>

---

## 🎯 What is PolicyLang?

**PolicyLang** is a domain-specific language (DSL) and compiler designed
to make **network security policy development simpler, more transparent,
and explainable**.

Instead of manually writing low-level eBPF networking code, a user can
express a security requirement using a simple policy syntax.

### 👨‍💻 Traditional Approach

A developer may need to understand:

```text
Linux networking
      +
Packet structures
      +
TCP / UDP headers
      +
C programming
      +
eBPF
      +
Kernel networking
```

### 🚀 PolicyLang Approach

The user writes:

```text
allow ingress
when destination.port == 443
```

PolicyLang transforms this high-level policy through a compiler pipeline
and produces corresponding eBPF-compatible C code.

```text
┌──────────────────────────────────────┐
│      Human-Readable Security Rule    │
└──────────────────┬───────────────────┘
                   ↓
              🔤 Lexer
                   ↓
              🧩 Parser
                   ↓
              🌳 AST
                   ↓
          🔍 Semantic Analysis
                   ↓
              📦 Policy IR
                   ↓
             ⚡ Optimizer
                   ↓
             🐝 eBPF Backend
                   ↓
          📝 Generated eBPF C
                   ↓
             LLVM / Clang
                   ↓
            📦 eBPF ELF Object
                   ↓
          🐧 Linux eBPF Runtime
```

---

# 💡 Why PolicyLang?

eBPF provides powerful programmable networking capabilities inside the
Linux kernel.

However, writing eBPF programs directly can require low-level knowledge
of packet processing and kernel networking.

PolicyLang introduces a higher-level abstraction:

> **Security engineers describe WHAT they want.  
> The compiler handles HOW it is implemented.**

This creates a clear separation between:

```text
Security Intent
       ↓
Compiler
       ↓
Low-Level Network Enforcement
```

---

# 🌍 Real-World Example

Imagine a company has a Linux server.

The security administrator wants:

> "Allow incoming HTTPS traffic."

Instead of manually implementing packet parsing and port checking in
eBPF C, the administrator can express the intent as:

```text
allow ingress
when destination.port == 443
```

Here:

| Policy Element | Meaning |
|---|---|
| `allow` | Permit matching traffic |
| `ingress` | Incoming traffic |
| `destination.port` | Destination network port |
| `== 443` | Match HTTPS port |

PolicyLang then converts this policy into lower-level packet-processing
logic.

---

# ✨ Key Features

## 📝 1. Human-Readable DSL

Security policies are written using a concise and understandable syntax.

Example:

```text
allow ingress
when destination.port == 443
```

---

## 🔤 2. Custom Lexer

The lexer converts the policy source into tokens that can be processed by
the compiler.

Conceptually:

```text
allow
ingress
when
destination.port
==
443
```

---

## 🧩 3. Parser & AST

The parser validates the policy structure and creates an
**Abstract Syntax Tree (AST)**.

Conceptually:

```text
             ALLOW
               |
            INGRESS
               |
        DST_PORT == 443
```

---

## 🔍 4. Semantic Analysis

PolicyLang validates whether the policy values and fields are meaningful.

Validation includes concepts such as:

- IPv4 addresses
- Network ports
- Protocol values
- Supported fields
- Supported operators
- Actions
- Directions

Invalid policies are rejected before backend generation.

---

## 📦 5. Intermediate Representation

The compiler converts the validated policy into an intermediate
representation (IR).

Example:

```text
IRPolicy(
    action=ALLOW,
    direction=INGRESS,
    condition=
        IRComparison(
            field=DST_PORT,
            operator=EQ,
            value=443
        )
)
```

The IR provides a clean boundary between the policy language and the
backend.

---

## ⚡ 6. Optimization Stage

The intermediate representation passes through an optimization stage
before code generation.

This allows compiler transformations to remain independent of the
front-end policy syntax.

---

## 🐝 7. Explainable eBPF Backend

The backend generates eBPF-compatible C code.

For example, generated code can contain packet-processing logic such as:

```c
dst_port = bpf_ntohs(tcp->dest);
```

The generated C source can be inspected by the developer rather than
being hidden behind the compiler.

---

## 🐧 8. eBPF Object Generation

The generated C program can be compiled using LLVM/Clang into an
eBPF ELF relocatable object.

Example:

```text
build/api_policy.bpf.o
```

---

## 🔬 9. eBPF Inspection

The generated program can be inspected using `bpftool`.

Example:

```bash
sudo bpftool prog show
```

and:

```bash
sudo bpftool prog dump xlated
```

This provides visibility into the resulting eBPF program.

---

## 🌐 10. Compiler API

A Flask API exposes the compiler to the frontend.

Example endpoint:

```text
POST /compile
```

The API returns information about the compilation stages,
intermediate representation, generated eBPF code, and compilation status.

---

## 🖥️ 11. Interactive Policy Editor

The project includes a frontend policy editor where users can:

- Enter a policy
- Select example policies
- Compile the policy
- View compilation results
- Inspect generated output

---

## 🧪 12. Automated Testing

The project contains automated tests for the compiler components.

Current verification:

```text
49 tests passed
```

Coverage includes:

```text
AST
Lexer
Parser
Semantic Analysis
Intermediate Representation
Optimizer
Backend
API
```

---

# 🏗️ System Architecture

```text
                         ┌───────────────────────┐
                         │   👨‍💻 User / Admin     │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │    📝 Policy Editor    │
                         │      Frontend          │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      🌐 Flask API      │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      🔤 Lexer          │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      🧩 Parser         │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │       🌳 AST           │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ 🔍 Semantic Analysis  │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      📦 Policy IR      │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      ⚡ Optimizer       │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │    🐝 eBPF Backend     │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │  📝 Generated eBPF C  │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │     LLVM / Clang      │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   📦 eBPF ELF Object  │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ 🐧 Linux eBPF System  │
                         └───────────────────────┘
```

---

# 🔄 Complete Compiler Pipeline

PolicyLang follows a compiler-oriented architecture.

## 1️⃣ Source Policy

```text
allow ingress
when destination.port == 443
```

⬇️

## 2️⃣ Lexical Analysis

The source is converted into tokens.

⬇️

## 3️⃣ Parsing

The tokens are converted into a structured AST.

⬇️

## 4️⃣ Semantic Analysis

The compiler validates the policy.

⬇️

## 5️⃣ Intermediate Representation

The policy is converted into a backend-independent representation.

⬇️

## 6️⃣ Optimization

The IR passes through the optimization stage.

⬇️

## 7️⃣ eBPF Code Generation

The backend produces eBPF-compatible C code.

⬇️

## 8️⃣ LLVM / Clang Compilation

The generated C can be compiled into an eBPF ELF object.

⬇️

## 9️⃣ Linux eBPF Inspection

The resulting eBPF program can be inspected using Linux eBPF tooling.

---

# 📋 Example Policies

## 🔐 HTTPS Allow

```text
allow ingress
when destination.port == 443
```

Meaning:

```text
Allow incoming traffic
when destination port is 443.
```

---

## 🌐 HTTP or HTTPS

```text
allow ingress
when destination.port == 80
or destination.port == 443
```

---

## 🎯 Source IP Matching

```text
allow ingress
when source.ip == "10.0.0.5"
```

---

## 🚫 SSH Denial

```text
deny ingress
when destination.port == 22
```

> The exact supported policy syntax is determined by the grammar
> implemented in the current compiler.

---

# 🧠 Intermediate Representation

PolicyLang does not directly convert source text into eBPF code.

Instead, it introduces an intermediate representation.

For example:

```text
Source Policy
     │
     ▼
┌──────────────────────────────┐
│         IRPolicy              │
│                              │
│ action    = ALLOW            │
│ direction = INGRESS           │
│                              │
│ condition:                   │
│   field    = DST_PORT        │
│   operator = EQ              │
│   value    = 443             │
└──────────────────────────────┘
     │
     ▼
 eBPF Backend
```

This design makes the compiler easier to extend with additional
backends and policy constructs.

---

# 🐝 Generated eBPF Code

Example generated code includes packet parsing and protocol-specific
port extraction.

For TCP:

```c
struct tcphdr *tcp = (void *)ip + (ip->ihl * 4);

src_port = bpf_ntohs(tcp->source);
dst_port = bpf_ntohs(tcp->dest);
```

For UDP:

```c
struct udphdr *udp = (void *)ip + (ip->ihl * 4);

src_port = bpf_ntohs(udp->source);
dst_port = bpf_ntohs(udp->dest);
```

The generated program then evaluates the condition represented by the
original PolicyLang rule.

---

# 🌐 API

PolicyLang exposes the compiler through a Flask API.

## ❤️ Health Check

### Request

```text
GET /health
```

Example:

```bash
curl http://127.0.0.1:5000/health
```

Example response:

```json
{
  "service": "PolicyLang Compiler API",
  "status": "ok",
  "version": "0.1"
}
```

---

# 🚀 Compile Endpoint

### Request

```text
POST /compile
```

Example:

```json
{
  "source": "allow ingress\nwhen destination.port == 443"
}
```

The API processes the policy through:

```text
Lexer
  ↓
Parser
  ↓
Semantic Analysis
  ↓
IR Lowering
  ↓
Optimization
  ↓
eBPF Generation
```

The response contains information such as:

```text
success
policy
stages
IR
explanation
generated eBPF C
output file
```

---

# 🖥️ Frontend Workflow

The frontend provides an interactive interface for the compiler.

```text
┌───────────────────────┐
│   📝 Enter Policy     │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│   ▶ Compile Policy    │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│     🌐 Compiler API   │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│   ⚙️ Compiler Pipeline │
└───────────┬───────────┘
            ↓
     ┌──────┴──────┐
     ↓             ↓
┌─────────┐   ┌──────────────┐
│  IR     │   │ eBPF C Code  │
└─────────┘   └──────────────┘
```

---

# 📁 Project Structure

```text
policylang-ebpf/
│
├── 📂 api/
│   └── server.py
│
├── 📂 compiler/
│   ├── ast/
│   ├── backend/
│   ├── ir/
│   ├── lexer/
│   ├── optimizer/
│   ├── parser/
│   └── semantic/
│
├── 📂 docs/
│
├── 📂 examples/
│
├── 📂 frontend/
│
├── 📂 policylang/
│
├── 📂 tests/
│   ├── test_api.py
│   ├── test_ast.py
│   ├── test_backend.py
│   ├── test_ir.py
│   ├── test_lexer.py
│   ├── test_optimizer.py
│   ├── test_parser.py
│   └── test_semantic.py
│
├── 📂 build/
│   ├── api_policy.bpf.c
│   ├── api_policy.bpf.o
│   ├── basic_policy.bpf.c
│   └── policy.bpf.c
│
├── 📄 requirements.txt
├── 📄 README.md
└── 📄 .gitignore
```

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| 🧠 Compiler | Python |
| 🔤 Lexer | Custom implementation |
| 🧩 Parser | Custom implementation |
| 🌳 AST | Custom compiler representation |
| 🔍 Semantic Analysis | Python |
| 📦 IR | Custom intermediate representation |
| ⚡ Optimization | Custom optimization stage |
| 🐝 eBPF Backend | Python → eBPF C |
| 🐧 Runtime Environment | Linux / WSL2 |
| ⚙️ Compiler Toolchain | LLVM / Clang |
| 🔬 eBPF Tooling | bpftool |
| 🌐 API | Flask |
| 🖥️ Frontend | Web-based interface |
| 🧪 Testing | pytest |
| 🔧 Version Control | Git / GitHub |

---

# 🧪 Testing & Verification

PolicyLang includes automated tests across multiple compiler stages.

Run:

```powershell
python -m pytest -v
```

Current result:

```text
==============================
49 passed
==============================
```

The tests validate:

```text
              🧪 TEST SUITE
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
     Lexer       Parser       AST
       │           │           │
       └───────────┼───────────┘
                   ↓
          Semantic Analysis
                   ↓
                  IR
                   ↓
              Optimizer
                   ↓
                Backend
                   ↓
                  API
```

---

# 🐧 Building the eBPF Object

On Linux / WSL2:

```bash
clang -O2 -g -target bpf \
-I/usr/include/x86_64-linux-gnu \
-c build/api_policy.bpf.c \
-o build/api_policy.bpf.o
```

Verify the generated object:

```bash
file build/api_policy.bpf.o
```

Expected format:

```text
ELF 64-bit LSB relocatable, eBPF
```

This verifies that the generated C source has been compiled into an
eBPF relocatable object.

---

# 🔬 Inspecting the eBPF Object

Inspect ELF sections:

```bash
llvm-objdump -h build/api_policy.bpf.o
```

The generated object contains an eBPF classifier section.

You can also inspect the generated source:

```bash
head -40 build/api_policy.bpf.c
```

Search for destination-port handling:

```bash
grep -n "dst_port" build/api_policy.bpf.c
```

---

# 🧰 Loading & Inspecting eBPF

On a Linux environment with the required privileges and eBPF support:

```bash
sudo ~/bpftool/src/bpftool prog load \
build/api_policy.bpf.o \
/sys/fs/bpf/policylang_test
```

Inspect the pinned program:

```bash
sudo ~/bpftool/src/bpftool prog show pinned \
/sys/fs/bpf/policylang_test
```

Inspect translated eBPF instructions:

```bash
sudo ~/bpftool/src/bpftool prog dump xlated pinned \
/sys/fs/bpf/policylang_test
```

A loaded PolicyLang program can appear as a `sched_cls` program with the
generated function name:

```text
policylang_filter
```

> eBPF loading and attachment depend on the Linux kernel, WSL2
> configuration, privileges, networking setup, and available eBPF
> capabilities.

---

# ⚙️ Installation

## 1. Clone

```bash
git clone https://github.com/Apoorva-Nayak07/policylang-ebpf.git
```

```bash
cd policylang-ebpf
```

---

## 2. Create Virtual Environment

### Windows PowerShell

```powershell
python -m venv .venv
```

Activate:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Run Tests

```powershell
python -m pytest -v
```

Expected:

```text
49 passed
```

---

# 🚀 Running the API

From the project root:

```powershell
python -m api.server
```

The API runs at:

```text
http://127.0.0.1:5000
```

Test:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/health
```

Expected:

```text
service : PolicyLang Compiler API
status  : ok
version : 0.1
```

---

# 🧪 Test the Compiler API

Create a request:

```powershell
$body = @{
    source = "allow ingress`nwhen destination.port == 443"
} | ConvertTo-Json
```

Send it:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/compile" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

A successful response contains:

```text
success : True
```

along with compilation stages and generated output.

---

# 🔍 Verification Levels

PolicyLang provides multiple levels of verification.

### 🧪 Level 1 — Unit Tests

```text
49 tests passed
```

### 📝 Level 2 — Generated C

```text
build/api_policy.bpf.c
```

### 📦 Level 3 — eBPF Object

```text
build/api_policy.bpf.o
```

### 🔬 Level 4 — ELF Inspection

```bash
llvm-objdump -h build/api_policy.bpf.o
```

### 🐧 Level 5 — Kernel-Level Inspection

```bash
sudo bpftool prog show
```

and:

```bash
sudo bpftool prog dump xlated
```

This creates a verification chain:

```text
Policy
  ↓
Compiler
  ↓
Generated C
  ↓
eBPF ELF Object
  ↓
Loaded eBPF Program
  ↓
Kernel-Level Inspection
```

---

# 🏆 What Makes the Project Different?

PolicyLang focuses on the connection between:

```text
👨‍💻 Human Security Intent
           +
🧠 Compiler Technology
           +
🐝 eBPF
           +
🐧 Linux Networking
```

Instead of treating eBPF code generation as a black box, the project
exposes the compiler stages and generated artifacts.

The user can inspect:

```text
Source Policy
      ↓
Tokens
      ↓
AST
      ↓
Semantic Result
      ↓
IR
      ↓
Optimized Representation
      ↓
Generated eBPF C
      ↓
eBPF Object
      ↓
Kernel-Level Program
```

---

# 🔐 Design Principles

## 🟢 Simplicity

Make common network security intent easier to express.

## 🔵 Separation of Concerns

Keep the language, compiler stages, IR, and backend modular.

## 🟣 Explainability

Expose compilation stages and generated eBPF code.

## 🟠 Verifiability

Provide automated tests and inspectable generated artifacts.

## ⚫ Extensibility

Keep the compiler architecture open for additional policy constructs,
fields, operators, and backends.

---

# 📊 Current Implementation Status

| Component | Status |
|---|---|
| 📝 Policy DSL | ✅ Implemented |
| 🔤 Lexer | ✅ Implemented |
| 🧩 Parser | ✅ Implemented |
| 🌳 AST | ✅ Implemented |
| 🔍 Semantic Analysis | ✅ Implemented |
| 📦 Intermediate Representation | ✅ Implemented |
| ⚡ Optimization Stage | ✅ Implemented |
| 🐝 eBPF Backend | ✅ Implemented |
| 🌐 Flask API | ✅ Implemented |
| 🖥️ Frontend | ✅ Implemented |
| 🧪 Automated Tests | ✅ 49 tests passing |
| 📄 eBPF C Generation | ✅ Implemented |
| 📦 eBPF Object Compilation | ✅ Verified |
| 🔬 eBPF Inspection | ✅ Verified in supported Linux/WSL2 environment |

---

# 🚧 Future Scope

PolicyLang can be extended with:

### 🔹 Advanced Policy Expressions

- More comparison operators
- Logical expressions
- More network fields
- CIDR-based matching
- More protocol conditions

### 🔹 Advanced Compiler Features

- More optimization passes
- Better error diagnostics
- Policy conflict detection
- Policy dependency analysis
- More sophisticated IR transformations

### 🔹 eBPF Extensions

- Additional eBPF program types
- Automated TC attachment
- Runtime observability
- Performance benchmarking
- Traffic statistics
- Policy monitoring

### 🔹 Security Features

- Stateful policies
- Rate limiting
- Connection tracking
- Security event logging
- Policy auditing

---

# 🎥 Demo

The project demonstration shows the complete workflow:

```text
📝 Write Policy
      ↓
▶️ Compile
      ↓
🔤 Lexer
      ↓
🧩 Parser
      ↓
🔍 Semantic Analysis
      ↓
📦 IR
      ↓
⚡ Optimization
      ↓
🐝 eBPF Generation
      ↓
📄 Generated C
      ↓
📦 eBPF Object
      ↓
🐧 Linux / eBPF Inspection
```

### 🎬 Demo Highlights

The demonstration covers:

- Human-readable policy creation
- Policy compilation
- Compilation-stage results
- Generated eBPF C code
- Automated test results
- eBPF ELF object verification
- bpftool-based eBPF inspection

📌 **Demo Video:** Add your unlisted YouTube link here.

---

# 📸 Project Screenshots

Add screenshots here to showcase the project interface.

Recommended screenshots:

### 🖥️ Policy Editor

```text
docs/screenshots/policy-editor.png
```

### ⚙️ Compilation Result

```text
docs/screenshots/compile-result.png
```

### 📝 Generated eBPF Code

```text
docs/screenshots/generated-ebpf.png
```

### 🧪 Test Results

```text
docs/screenshots/tests.png
```

### 🐧 eBPF Inspection

```text
docs/screenshots/bpftool.png
```

---

# 👥 Team

## 🛡️ Team SegFault

**Project:** PolicyLang

**Focus:**

```text
Compiler Design
+
Network Security
+
eBPF
+
Linux Networking
```

---

# 🌟 Project Vision

PolicyLang aims to demonstrate how compiler technology can bridge the gap
between **high-level security intent** and **low-level programmable
networking**.

The long-term vision is:

```text
        HUMAN SECURITY INTENT
                 │
                 ▼
          SIMPLE POLICY DSL
                 │
                 ▼
             COMPILER
                 │
        ┌────────┴────────┐
        ▼                 ▼
    ANALYSIS          EXPLANATION
        │                 │
        └────────┬────────┘
                 ▼
            eBPF PROGRAM
                 │
                 ▼
        LINUX NETWORK STACK
```

---

# ⭐ Final Summary

**PolicyLang transforms human-readable network security policies into
explainable eBPF programs through a complete compiler pipeline.**

```text
╔══════════════════════════════════════════════╗
║              🛡️ POLICYLANG                  ║
╠══════════════════════════════════════════════╣
║                                              ║
║  📝 Human Policy                             ║
║          ↓                                   ║
║  🔤 Lexer                                    ║
║          ↓                                   ║
║  🧩 Parser                                   ║
║          ↓                                   ║
║  🌳 AST                                      ║
║          ↓                                   ║
║  🔍 Semantic Analysis                        ║
║          ↓                                   ║
║  📦 Intermediate Representation              ║
║          ↓                                   ║
║  ⚡ Optimization                              ║
║          ↓                                   ║
║  🐝 eBPF Backend                              ║
║          ↓                                   ║
║  📝 Generated eBPF C                         ║
║          ↓                                   ║
║  ⚙️ LLVM / Clang                              ║
║          ↓                                   ║
║  📦 eBPF ELF Object                          ║
║          ↓                                   ║
║  🐧 Linux eBPF Infrastructure                ║
║                                              ║
╚══════════════════════════════════════════════╝
```

> **PolicyLang — From Security Intent to Programmable Networking. 🚀**
