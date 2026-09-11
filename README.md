# Zeta.sh

A compact family of self-encoding Schwarzschild–Stirling–Riemann formal machines.

The core self map uses the exact reversible length-lex coordinate

\[
G=I(R)=\frac{256^{|R|}-1}{255}+\operatorname{int}(R),\qquad D(G)=R,
\]

where `R` is the canonical quine core. `SELF_SOLVED=true` means the machine has decoded its own integer coordinate byte-for-byte back to `R`.

## Usage

Requires Python 3 and `mpmath`:

```bash
python3 -m pip install mpmath
chmod +x Zeta.sh Public_Universe_TM.sh OMEGA_Limit_TM.sh

./Zeta.sh 3
./Zeta.sh self
./Zeta.sh zero 1
./Zeta.sh live

./Public_Universe_TM.sh 3
./Public_Universe_TM.sh self

./OMEGA_Limit_TM.sh
./OMEGA_Limit_TM.sh omega
./OMEGA_Limit_TM.sh self
./OMEGA_Limit_TM.sh finite 1
./OMEGA_Limit_TM.sh finite 8
./OMEGA_Limit_TM.sh live 1
```

## Zeta self objective

For a continuation scale `H>1`, `Zeta.sh` sets

\[
\lambda=\frac1H,\qquad r=\frac{2M}{1-\lambda}\;(M=1),\qquad t=qH,
\]

with

\[
q=\frac{\log(1+G)}{|R|}.
\]

It evaluates the completed zeta expression

\[
\xi(s)=\tfrac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s),\qquad s=\tfrac12+it,
\]

and normalizes by a nonzero leading Stirling envelope. `zero N` maps an `mpmath.zetazero(N)` critical-line zero back to this machine's self scale; it is a numerical mapping, not a proof of the Riemann Hypothesis. `live` repeatedly doubles `H`, so every emitted state is finite while the successor rule remains open-ended.

## Public account meta-machine

`Public_Universe_TM.sh` lifts the reversible encoding idea to the current public GitHub repository metadata of `letsgo0226`. It canonically frames public repository metadata into bytes `W_t`, then computes

\[
G_t=I(W_t),\qquad D(G_t)=W_t.
\]

It reports `WORLD_INDEX`, `WORLD_REV`, `PUBLIC_REPOS`, `META_SELF`, and a deterministic `TRUTH_PATH`. This is a defined account-state encoding, not a proof of the semantics of every repository and not a claim that repositories are physical universes.

The account mode also carries a shared continuation certificate. With

\[
\lambda=\frac1H,
\]

it evaluates

\[
r(\lambda)=\frac{2}{1-\lambda},\qquad 1-\frac2r=\lambda,
\]

the real Stirling remainder

\[
e(H)=\log\Gamma(H+1)-\left[(H+\tfrac12)\log H-H+\tfrac12\log(2\pi)\right],
\]

for which

\[
12e(H)\sim\frac1H=\lambda,
\]

and the genuine zeta pole at `s=1` through

\[
E_\zeta(\lambda)=\left|\lambda\zeta(1+\lambda)-1\right|\to0.
\]

Thus

\[
X(H)=\left(\lambda,12e(H),1-\frac2r,E_\zeta(\lambda)\right)\to(0,0,0,0)
\]

as `H -> infinity`, while every actual finite evaluation keeps `H<infinity` and `lambda>0`.

## Exact self-omega recursive machine

`OMEGA_Limit_TM.sh` now makes **Self and Omega simultaneous in the default state**.

The no-argument invocation

```bash
./OMEGA_Limit_TM.sh
```

and the explicit invocation

```bash
./OMEGA_Limit_TM.sh omega
```

both return `MODE="omega-self"`. The boundary JSON includes the same exact self certificate exposed by diagnostic `self` mode:

- `SELF_LEN=|R|`
- `SELF_INDEX=I(R)`
- `SELF_SOLVED=true`, meaning `D(I(R))=R`
- `SELF_OMEGA=true`

At the same time it returns the symbolic compactified boundary

\[
\Omega_{\mathrm{SELF}}=
\left(R,I(R),H=\infty,\lambda=0,r=2,S=0,E_\zeta=0\right).
\]

So the default state satisfies the formal conjunction

\[
\boxed{\mathrm{SELF}\land\Omega}
\]

rather than treating self encoding and the limit boundary as mutually exclusive modes. The self coordinate is an invariant identity component, while the continuation coordinates are the components that evolve toward the boundary.

The machine explicitly reports

```text
BOUNDARY_BY_DEFINITION=true
ATTAINED_BY_FINITE_EXECUTION=false
OPEN=true
FINAL=false
```

so `H="Infinity"` and `LAMBDA="0"` are exact symbols in the extended state space, not a claim that a Turing process completed infinitely many execution steps.

### Finite approximants

Finite states are requested explicitly:

```bash
./OMEGA_Limit_TM.sh finite n
```

for integer `n>=1`, with

\[
H_n=2^n,\qquad \lambda_n=2^{-n},\qquad H_n\lambda_n=1.
\]

The reciprocal identity is represented exactly by integer fields `LAMBDA_NUM=1` and `LAMBDA_DEN=H`. The Schwarzschild-style coordinate is also preserved as the exact rational pair

\[
r_n=\frac{2H_n}{H_n-1},
\]

through `SCH_NUM=2H` and `SCH_DEN=H-1`.

The invariant self coordinate does not evolve:

\[
I(R)_{n+1}=I(R)_n=I(R),
\]

while

\[
H_n\to\infty,\qquad \lambda_n\to0^+,\qquad r_n\to2.
\]

Thus a useful formal state is

\[
X_n=\left(I(R),H_n,\lambda_n,r_n,S_n,E_{\zeta,n}\right),
\]

with ideal compactified boundary

\[
\lim_{n\to\infty}X_n=\Omega_{\mathrm{SELF}}.
\]

### Live continuation

```bash
./OMEGA_Limit_TM.sh live 1
```

executes

\[
n\mapsto n+1,\qquad H\mapsto2H,\qquad\lambda\mapsto\lambda/2
\]

without an internal halting state. Every emitted live record is finite and has `OMEGA=false`, `HALT=false`, `OPEN=true`, and `FINAL=false`.

### Self diagnostic

```bash
./OMEGA_Limit_TM.sh self
```

remains a compact diagnostic that prints only `SELF_LEN`, `SELF_INDEX`, and `SELF_SOLVED`. The default `omega-self` state must contain exactly the same `SELF_LEN` and `SELF_INDEX`; GitHub Actions verifies this identity directly.

## Interpretation and limits

These programs are formal computational models. The Schwarzschild quantity is a continuation coordinate, not a physical black-hole simulation. The Stirling, zeta-pole, and Schwarzschild objects are connected here by an explicitly defined common parameter; the construction does not establish that those theories have one physical mechanism. A symbolic `Omega` boundary is a mathematical extension of the state space, not a completed infinite computation.

Scheduled GitHub Actions run every five minutes and on push, pull request, manual dispatch, and `zeta-evolve` repository dispatch. The machines remain explicitly open-ended:

\[
\boxed{OPEN=true,\qquad FINAL=false.}
