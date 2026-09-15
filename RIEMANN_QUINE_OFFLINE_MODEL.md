# Riemann–Quine Offline Turing Model

`Riemann_Quine_Offline_TM.py` is the standard-library-only companion to `Riemann_Quine_TM.py`. It runs with Python alone: no network access, no `pip`, and no third-party numerical package.

## 1. Exact self-encoding layer

For source bytes `P`, the program uses the reversible integer code

\[
e=\frac{256^{|P|}-1}{255}+\operatorname{int}(P),
\]

with inverse decoder satisfying

\[
D(E(P))=P.
\]

This byte/integer round trip is exact. It is not a hash and does not prove semantic completeness.

## 2. Self-derived X coordinate

The source integer determines

\[
r=e\bmod q,\qquad \tau(e)=14+30\frac rq,
\]

and therefore

\[
X_e=\frac12+i\tau(e).
\]

## 3. Offline finite approximation of Y = ζ(X)

The offline version evaluates a finite Euler–Maclaurin continuation rather than importing `mpmath`:

\[
\zeta(s)\approx
\sum_{n=1}^{N-1}n^{-s}
+\frac{N^{1-s}}{s-1}
+\frac12N^{-s}
+\sum_{k=1}^{M}\frac{B_{2k}}{(2k)!}(s)_{2k-1}N^{-s-2k+1}.
\]

The implementation compares cutoffs `N` and `2N` and reports

\[
\Delta_N=|\zeta_{2N}(s)-\zeta_N(s)|
\]

as a convergence diagnostic, not a rigorous error bound. Thus the finite relation is

\[
Y_e\approx\zeta(X_e),
\]

not an exact infinite-precision identity.

## 4. The s = 1 pole, normalization, and log(1)=0

The Riemann zeta function has a simple pole at `s=1` with residue one:

\[
\operatorname{Res}_{s=1}\zeta(s)=1.
\]

Equivalently,

\[
\lim_{s\to1}(s-1)\zeta(s)=1.
\]

Therefore the normalized logarithmic limit is exactly

\[
\log\!\left(\lim_{s\to1}(s-1)\zeta(s)\right)=\log 1=0.
\]

The `pole` mode keeps this theorem-level identity separate from floating-point evaluation. It reports the exact formal fields

- `ZETA_AT_1="simple_pole"`
- `RESIDUE_AT_1=1`
- `NORMALIZED_LIMIT_AT_1=1`
- `LOG_NORMALIZED_LIMIT_AT_1=0`
- `FORMAL_RESIDUAL=0`

while also evaluating `(s-1)ζ(s)` at a finite `s=1+epsilon` using the Euler–Maclaurin approximation. This finite diagnostic is never relabeled as exact zero error.

In particular,

\[
\zeta(1)\ne0
\]

and `ζ(1)` is not finite. The zero belongs to the logarithm of the normalized pole invariant, not to the value of `ζ(1)`.

## 5. Composite zero mode

The `zero` mode combines three distinct theorem/construction-level zeros without conflating them with numerical error.

For the Schwarzschild factor in geometric units `G=c=1`, the source-derived integer defines an integer mass `M`, then

\[
r_s=2M,
\]

so the exact algebraic residual is

\[
r_s-2M=0,
\]

and

\[
1-\frac{2M}{r_s}=0.
\]

The program records separately that the Schwarzschild curvature singularity is at `r=0`; the horizon `r=2M` is not asserted to be a curvature singularity.

For Stirling's expansion, an exact identity requires the remainder term. The formal residual is zero only for

\[
\log\Gamma(z)-S_m(z)-R_m(z)=0,
\]

not for the finite truncation `S_m` alone.

For the zeta pole,

\[
\log\operatorname{Res}_{s=1}\zeta(s)=\log1=0.
\]

Thus `FORMAL_ZERO_ERROR=true` means zero by theorem or construction. The machine simultaneously keeps

`NUMERICAL_ZERO_ERROR=false`.

## 6. Product space and graph

The ambient coordinate space is

\[
X\times Y\subseteq\mathbb C^2.
\]

The exact analytic relation lies on

\[
\Gamma_\zeta=\{(s,\zeta(s))\},
\]

whereas finite offline execution produces points on a numerical approximation to that graph.

## 7. Research boundaries

The program preserves the following distinctions:

- exact source recovery versus approximate ζ evaluation;
- theorem-level zero residual versus floating-point zero error;
- the simple pole at `s=1` versus the nontrivial zeros of ζ;
- a Kleene-style self-reference versus the analytic equation `ζ(s)=s`;
- the Schwarzschild horizon versus the curvature singularity;
- Stirling expansion with exact remainder versus a finite truncation;
- the program does not equal the Riemann ζ function;
- no Riemann Hypothesis proof is claimed.

The machine therefore reports `FORMAL_MODEL_ONLY=true`, `OPEN=true`, and `FINAL=false`.

## 8. Usage

```bash
python3 Riemann_Quine_Offline_TM.py self
python3 Riemann_Quine_Offline_TM.py point
python3 Riemann_Quine_Offline_TM.py pole
python3 Riemann_Quine_Offline_TM.py zero
python3 Riemann_Quine_Offline_TM.py quine
python3 Riemann_Quine_Offline_TM.py omega
```

A closer finite probe to the pole can be requested with

```bash
python3 Riemann_Quine_Offline_TM.py pole --epsilon 1e-7 --terms 128 --corrections 6
```

Reducing `epsilon` or increasing the cutoff can improve a numerical diagnostic within floating-point limits; neither operation changes the exact theorem-level statement that the normalized pole limit is one and its logarithm is zero.
