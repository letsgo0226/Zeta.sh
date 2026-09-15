# Riemann–Quine Turing Model

This module formalizes a self-referential computational embedding of a program into the graph of the Riemann zeta function. It deliberately distinguishes program self-reference from an analytic fixed point of zeta.

Let `P` be the exact source bytes and let

\[
e=\ulcorner P\urcorner
\]

be a reversible integer encoding. The executable verifies `decode(e)=P`. A deterministic embedding sends the program code to the critical line:

\[
r=e\bmod q,\qquad \tau(e)=14+30r/q,
\]

\[
X_P=\tfrac12+i\tau(e).
\]

The analytic image is

\[
Y_P=\zeta(X_P).
\]

Thus each program instance determines a pair

\[
Q_P=(X_P,Y_P)\in\operatorname{Graph}(\zeta)\subset\mathbb C\times\mathbb C.
\]

The `quine` mode returns the exact source text together with its reversible code and the Riemann pair. Its self-reference cycle is represented as

\[
P\to\ulcorner P\urcorner\to X_P\to\zeta(X_P)\to(\ulcorner P\urcorner,X_P,Y_P)\to P.
\]

The final arrow is source recovery from the reversible code, not inversion of the zeta function.

## Two different fixed points

The model explicitly separates a computability-theoretic fixed point from an analytic one. A Kleene-style self-reference concerns program semantics under a computable transformation. The equation

\[
\zeta(s)=s
\]

is instead an analytic fixed-point problem. The former does not prove the latter, and this implementation does not claim that the program literally equals the zeta function.

## Numerical boundary

`mpmath` evaluates \(\zeta(X_P)\) at arbitrary finite precision. If `dps=p`, the result is a finite numerical approximation \(\zeta_p(X_P)\). The mathematical limit is

\[
\lim_{p\to\infty}\zeta_p(X_P)=\zeta(X_P),
\]

but no finite run is declared to have attained infinite precision.

Examples:

```bash
python Riemann_Quine_TM.py self
python Riemann_Quine_TM.py point --dps 80
python Riemann_Quine_TM.py quine --dps 80
python Riemann_Quine_TM.py omega
```

The research boundary remains:

```text
PROGRAM_EQUALS_ZETA_FUNCTION=false
ANALYTIC_FIXED_POINT_CLAIMED=false
KLEENE_FIXED_POINT_DISTINCT_FROM_ANALYTIC_FIXED_POINT=true
ATTAINED_BY_FINITE_EXECUTION=false
FORMAL_MODEL_ONLY=true
OPEN=true
FINAL=false
```
