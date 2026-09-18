# PolicyLang

### A Domain-Specific Language and Compiler for Explainable eBPF Security Policies

PolicyLang is a domain-specific language (DSL) and compiler for expressing
network security policies using a simple, human-readable syntax and
translating them into explainable eBPF C programs.

The project provides a complete compiler pipeline:

```text
Human-Readable Security Policy
            |
            v
          Lexer
            |
            v
          Parser
            |
            v
           AST
            |
            v
    Semantic Analysis
            |
            v
       Policy IR
            |
            v
       Optimization
            |
            v
       eBPF Backend
            |
            v
     Generated eBPF C
            |
            v
      LLVM / Clang
            |
            v
       eBPF Object
            |
            v
       Linux / eBPF
