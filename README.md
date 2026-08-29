# PolicyLang

PolicyLang is a domain-specific language and compiler for expressing
human-readable network security policies and compiling them into
explainable eBPF programs.

## Vision

PolicyLang bridges the gap between high-level security intent and
low-level eBPF execution.

It allows users to write simple network security policies and transform
them through a complete compiler pipeline into eBPF C code.

## Compiler Pipeline

```text
Policy Source
     ↓
Lexer
     ↓
Parser
     ↓
AST
     ↓
Semantic Analysis
     ↓
Policy IR
     ↓
Optimization
     ↓
eBPF Backend
     ↓
Generated eBPF C