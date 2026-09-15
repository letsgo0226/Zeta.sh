# Zeta_TM.sh — Offline Zeta-Embedded Turing Machine

`Zeta_TM.sh` is an offline, standard-library-only research model that couples a finite deterministic single-tape Turing-machine interpreter with a Riemann-zeta analytic representation of each machine configuration.

## 1. Discrete machine state

For a machine `M` and input `w`, let the finite configuration at step `n` be

\[
C_n=(q_n,h_n,T_n),
\]

where `q_n` is the control state, `h_n` the head position, and `T_n` the finite nonblank tape support. The transition relation is the ordinary deterministic single-tape update

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

Thus `CONFIG_CODE_EXACT=true` and `CONFIG_RECOVERED=true` refer only to the byte/integer round trip. They do not imply semantic completeness or a solution to undecidable problems.

## 3. Zeta spectral projection

For the exact configuration integer `e_n`, the program computes

\[
r_n=e_n\bmod q,
\qquad
\tau_n=14+30\frac{r_n}{q},
\]

and

\[
X_n=\frac12+i\tau_n.
\]

The corresponding analytic image is

\[
Y_n\approx\zeta(X_n),
\]

where the offline implementation uses a finite Euler–Maclaurin continuation. The machine compares cutoffs `N` and `2N` and reports their difference as a convergence diagnostic, not as a rigorous certified error bound.

The modulus projection is deliberately identified as non-injective:

\[
e_i\ne e_j\centernot\implies X_i\ne X_j.
\]

Therefore the exact identity of a configuration is its full reversible code; `X` is only a deterministic spectral projection.

## 4. Zeta trace

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

This is an embedding/representation layer over the finite observed execution trace. The program does **not** identify a Turing machine with the Riemann zeta function:

\[
\text{program}\ne\zeta.
\]

## 5. Pole normalization at s = 1

The zeta function has a simple pole at `s=1` with residue one:

\[
\operatorname{Res}_{s=1}\zeta(s)=1,
\qquad
\lim_{s\to1}(s-1)\zeta(s)=1.
\]

Hence

\[
\log\left(\lim_{s\to1}(s-1)\zeta(s)\right)=\log 1=0.
\]

The `pole` mode keeps this theorem-level zero separate from finite numerical approximation and reports `NUMERICAL_ZERO_ERROR=false`.

## 6. Formal zero mode

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

## 7. Limit boundary

For a nonhalting execution, `Zeta_TM.sh` does not assume that

\[
\lim_{n\to\infty}(X_n,Y_n)
\]

exists. It therefore reports `LIMIT_EXISTS="not_assumed"`, `ATTAINED_BY_FINITE_EXECUTION=false`, `OPEN=true`, and `FINAL=false`.

A finite step limit is an observation boundary, not a halting oracle. `step_limit` means only that no halt state was reached within the requested number of simulated steps.

## 8. Usage

```bash
sh Zeta_TM.sh self
sh Zeta_TM.sh point
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
