# PolicyLang

### A Domain-Specific Language and Compiler for Explainable eBPF Security Policies

PolicyLang is a domain-specific language (DSL) and compiler designed to express
network security policies using a simple, human-readable syntax and translate
them into efficient eBPF programs.

The project bridges the gap between high-level security intent and low-level
Linux programmable networking through a complete compiler pipeline consisting
of lexical analysis, parsing, semantic analysis, intermediate representation,
optimization, and eBPF code generation.

---

## Project Overview

Traditional eBPF programs require knowledge of low-level C programming and
Linux networking internals.

PolicyLang provides a simpler approach by allowing users to write policies
in a readable declarative syntax.

```text
Human-readable Policy
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