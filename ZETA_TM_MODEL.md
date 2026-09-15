# Zeta_TM.sh — Offline Zeta-Represented Turing Machine

`Zeta_TM.sh` is an offline, standard-library-only research model that couples a finite deterministic single-tape Turing-machine interpreter with Riemann-zeta analytic representations and a Quine-style X/Y generator.

## 1. Discrete machine state

For a machine `M` and input `w`, let the finite configuration at step `n` be

\[
C_n=(q_n,h_n,T_n),
\]

with ordinary deterministic update

\[
C_{n+1}=\delta(C_n).
\]

`run` reports the final observed configuration inside a finite step bound. `trace` records every observed configuration from step zero through the final observed step.

## 2. Exact configuration encoding

Each configuration is serialized canonically as sorted compact JSON and encoded as

\[
E(b)=\frac{256^{|b|}-1}{255}+\operatorname{int}(b).
\]

The inverse decoder satisfies

\[
D(E(b))=b.
\]

Thus `CONFIG_CODE_EXACT=true` and `CONFIG_RECOVERED=true` refer only to the byte/integer round trip. They do not imply semantic completeness or solve undecidable problems.

## 3. Zeta spectral representation

For the exact configuration integer `e_n`, the program computes

\[
r_n=e_n\bmod q,
\qquad
\tau_n=14+30\frac{r_n}{q},
\qquad
X_n=\frac12+i\tau_n.
\]

The corresponding analytic image is

\[
Y_n\approx\zeta(X_n),
\]

using a finite Euler–Maclaurin continuation. The difference between cutoffs `N` and `2N` is a convergence diagnostic, not a rigorous certified error bound.

The modulus projection is non-injective:

\[
e_i\ne e_j\centernot\implies X_i\ne X_j.
\]

Therefore the program reports `ZETA_TRACE_REPRESENTATION=true` and `ZETA_TRACE_EMBEDDING=false`.

## 4. Quine-style X/Y cycle

The `xy-cycle` mode adds a second, independent analytic generator. A finite self-referential state carries the source index, current enumeration index, and successor rule. The implementation is file-reflective: it reads its own source bytes, so it is explicitly marked

`FILE_REFLECTIVE_QUINE=true` and `CLASSICAL_NO_INPUT_QUINE=false`.

The generator enumerates Gaussian rationals

\[
\mathbb Q(i)=\{a+ib:a,b\in\mathbb Q\}
\]

through a Cantor pairing of two signed Calkin–Wilf rational enumerations. Hence there is a computable map

\[
\phi:\mathbb N\to\mathbb Q(i)
\]

and each cycle has

\[
X_n=\phi(n),
\qquad
Y_n\approx\zeta(X_n),
\qquad
n\mapsto n+1.
\]

Operationally the phase is

\[
(P,n)\to X_n\to Y_n\to(P,n+1),
\]

where `P` is the same finite source program carried by the Quine-style state.

Because \(\mathbb Q(i)\) is dense in \(\mathbb C\),

\[
\overline{\phi(\mathbb N)}=\mathbb C.
\]

But \(\mathbb C\) is uncountable while a Turing-machine execution has only countably many steps. Therefore the machine deliberately reports

- `DENSE_GAUSSIAN_RATIONAL_ENUMERATION=true`
- `DENSE_CLOSURE_IS_COMPLEX_PLANE=true`
- `FULL_COMPLEX_SPACE_POINTWISE_ENUMERATION=false`
- `IMMEDIATE_EXHAUSTIVE_TRAVERSAL=false`
- `UNCOUNTABLE_CARDINALITY_BARRIER=true`

The finite program immediately contains the generator rule, not all complex points as already executed states.

## 5. Pole and zero branches

If the dense enumeration reaches exactly

\[
X_n=1,
\]

then `xy-cycle` does not evaluate a finite `ζ(1)`. It returns the exact pole-normalized invariants

\[
\operatorname{Res}_{s=1}\zeta(s)=1,
\qquad
\lim_{s\to1}(s-1)\zeta(s)=1,
\qquad
\log1=0.
\]

If it reaches a negative even integer,

\[
X_n=-2k,
\]

then the branch records the exact trivial zero

\[
\zeta(-2k)=0.
\]

All other `Y` values are finite floating-point Euler–Maclaurin approximations and retain `ERROR_BOUND_RIGOROUS=false`.

## 6. Zeta trace over ordinary TM configurations

The discrete execution

\[
C_0\to C_1\to\cdots\to C_N
\]

is represented as

\[
\Gamma_{M,w}^{\zeta}
=
\{(n,C_n,X_n,Y_n)\}_{n=0}^{N}.
\]

This is a representation layer over a finite observed execution trace. The program does **not** identify a Turing machine with the Riemann zeta function:

\[
\text{program}\ne\zeta.
\]

## 7. Formal zero mode

The `zero` mode preserves three theorem/construction-level identities:

\[
r_s-2M=0,
\]

for the Schwarzschild horizon relation in geometric units;

\[
\log\Gamma(z)-S_m(z)-R_m(z)=0,
\]

when the exact Stirling remainder is included; and

\[
\log\operatorname{Res}_{s=1}\zeta(s)=0.
\]

These formal zeros are not claims that finite floating-point numerical error vanishes.

## 8. Limit boundary

For a nonhalting execution, the model does not assume that

\[
\lim_{n\to\infty}(X_n,Y_n)
\]

exists. Dense enumeration means every open disk contains enumerated X-points eventually; it does not mean the sequence converges or that every complex point is visited.

The machine therefore reports `LIMIT_EXISTS="not_assumed"`, `ATTAINED_BY_FINITE_EXECUTION=false`, `OPEN=true`, and `FINAL=false`.

## 9. Usage

```bash
sh Zeta_TM.sh self
sh Zeta_TM.sh quine
sh Zeta_TM.sh point
sh Zeta_TM.sh xy-cycle --start 0 --count 8
sh Zeta_TM.sh run --machine machine.json --input 1011
sh Zeta_TM.sh trace --machine machine.json --input 1011 --max-steps 128
sh Zeta_TM.sh pole
sh Zeta_TM.sh zero
sh Zeta_TM.sh omega
```

Example machine schema:

```json
{
  "start":"q0",
  "halt":["qh"],
  "blank":"_",
  "delta":{
    "q0|1":["q0","0","R"],
    "q0|_":["qh","_","N"]
  }
}
```

The implementation is offline and requires only Python 3 standard-library modules.
