# Riemann–Quine Offline Turing Model

`Riemann_Quine_Offline_TM.py` is the standard-library-only companion to `Riemann_Quine_TM.py`.
It is designed to run with Python alone: no network access, no `pip`, and no third-party numerical package.

## 1. Exact self-encoding layer

For source bytes `P`, the program uses the reversible integer code

\[
e=\frac{256^{|P|}-1}{255}+\operatorname{int}(P),
\]

with an inverse decoder satisfying, for the current source bytes,

\[
D(E(P))=P.
\]

This is an exact byte/integer round trip. It is not a hash and does not prove semantic completeness.

## 2. Self-derived X coordinate

The source code integer determines

\[
r=e\bmod q,\qquad
\tau(e)=14+30\frac rq,
\]

and therefore

\[
X_e=\frac12+i\tau(e).
\]

Thus the X coordinate is reproducibly derived from the program's own bytes.

## 3. Offline approximation of Y = ζ(X)

The offline version does **not** import `mpmath`. It evaluates a finite Euler–Maclaurin continuation:

\[
\zeta(s)\approx
\sum_{n=1}^{N-1}n^{-s}
+\frac{N^{1-s}}{s-1}
+\frac12N^{-s}
+\sum_{k=1}^{M}\frac{B_{2k}}{(2k)!}(s)_{2k-1}N^{-s-2k+1}.
\]

The implementation uses six Bernoulli correction coefficients at most. It computes the approximation at `N` and `2N` and reports

\[
\Delta_N=|\zeta_{2N}(s)-\zeta_N(s)|
\]

as a convergence **diagnostic**, not as a rigorous error bound.

Therefore the actual relation is

\[
Y_e\approx\zeta(X_e),
\]

not an exact finite-precision identity.

## 4. Product space and graph

The ambient coordinate space is

\[
X\times Y\subseteq\mathbb C^2.
\]

The exact analytic relation would lie on the graph

\[
\Gamma_\zeta=\{(s,\zeta(s))\},
\]

whereas this offline finite-float implementation produces points on an approximation to that graph.

## 5. Research boundaries

The program explicitly keeps the following distinctions:

- source recovery is exact; ζ evaluation is approximate;
- a Kleene-style self-reference is not the analytic equation `ζ(s)=s`;
- the program does not equal the Riemann ζ function;
- finite floating-point execution does not attain an exact infinite-precision ζ value;
- formal self-reference does not imply physical or metaphysical truth.

The machine therefore reports `FORMAL_MODEL_ONLY=true`, `OPEN=true`, and `FINAL=false`.

## 6. Usage

```bash
python3 Riemann_Quine_Offline_TM.py self
python3 Riemann_Quine_Offline_TM.py point
python3 Riemann_Quine_Offline_TM.py quine
python3 Riemann_Quine_Offline_TM.py omega
```

Optional controls:

```bash
python3 Riemann_Quine_Offline_TM.py point --terms 128 --corrections 6 --modulus 1000003
```

`--terms` controls the first Euler–Maclaurin cutoff; the returned Y value is computed with twice that number of terms. Increasing it can improve stability but does not convert the finite computation into an exact analytic value.
