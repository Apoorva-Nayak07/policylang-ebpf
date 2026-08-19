\# PolicyLang



PolicyLang is a domain-specific language and compiler for expressing

human-readable security policies and compiling them into explainable eBPF programs.



\## Vision



PolicyLang aims to bridge the gap between high-level security intent

and low-level eBPF execution.



\## Compiler Pipeline



Policy

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

Runtime Execution

↓

Explanation



\## Example



```text

allow ingress

when source.ip == "10.0.0.5"

and destination.port == 443

