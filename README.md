# Zeta.sh

A compact self-encoding Schwarzschild–Stirling–Riemann objective machine.

The program reconstructs its own quine core `R`, assigns it an exact reversible length-lex index

\[
G=I(R)=\frac{256^{|R|}-1}{255}+\operatorname{int}(R),\qquad D(G)=R,
\]

and defines the self scale

\[
q=\frac{\log(1+G)}{|R|}.
\]

For a continuation scale `H>1`,

\[
\lambda=\frac1H,\qquad r=\frac{2M}{1-\lambda}\;(M=1),\qquad t=qH=\frac{q}{\lambda}.
\]

The Riemann target is the completed zeta function

\[
\xi(s)=\tfrac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s),\qquad s=\tfrac12+it.
\]

`Zeta.sh` divides by a nonzero leading Stirling envelope for the Gamma/prefactor magnitude and reports

\[
J_{SELF}(H)=|\widehat\Xi(t)|^2.
\]

The normalization does not create or remove zeros, so `J=0` corresponds numerically to a critical-line zero of `xi`. `STIR_ERR` is the relative error of the leading complex Stirling Gamma approximation; as the scale grows it tends toward zero in the relevant sector.

## Usage

Requires Python 3 and `mpmath`:

```bash
python3 -m pip install mpmath
chmod +x Zeta.sh Public_Universe_TM.sh OMEGA_Limit_TM.sh
./Zeta.sh 3
./Zeta.sh self
./Zeta.sh zero 1
./Zeta.sh live
./Zeta.sh live 4
./Public_Universe_TM.sh 3
./Public_Universe_TM.sh self
./OMEGA_Limit_TM.sh
./OMEGA_Limit_TM.sh finite 1
./OMEGA_Limit_TM.sh finite 8
./OMEGA_Limit_TM.sh live 1
./OMEGA_Limit_TM.sh omega
./OMEGA_Limit_TM.sh self
```

- `./Zeta.sh H` evaluates the self-encoding objective at a finite scale `H>1`.
- `./Zeta.sh self` prints the complete reversible self index and verifies `SELF_SOLVED=true`.
- `./Zeta.sh zero N` obtains the Nth critical-line zero numerically with `mpmath.zetazero`, maps it back to the corresponding self scale `H*=t_N/q`, and checks that the normalized objective is numerically near zero.
- `./Zeta.sh live [H0]` deliberately does not halt. Starting at `H0` (default `2`), it emits one JSON state per iteration and uses `H_(n+1)=2 H_n`. Hence `lambda_n=1/H_n -> 0`, `r_n -> 2M+`, and `t_n=q H_n -> infinity`. Each live record has `HALT=false`, `OPEN=true`, and `FINAL=false`. Stop it externally with `Ctrl-C` or another process signal.

## Public account meta-machine

`Public_Universe_TM.sh` lifts the same reversible self-encoding idea to the current public GitHub repository state of `letsgo0226`.

At each run it fetches every public repository exposed by the GitHub public user-repositories endpoint, paginates to exhaustion, sorts repositories canonically by name, and constructs

\[
W_t=\operatorname{Frame}(name,default\_branch,size,pushed\_at,fork,archived)_t.
\]

It then computes the exact reversible length-lex coordinate

\[
G_t=I(W_t),\qquad D(G_t)=W_t,
\]

and reports `WORLD_INDEX`, `WORLD_REV`, `PUBLIC_REPOS`, `META_SELF`, and a deterministic `TRUTH_PATH`. The truth path contributes one observed bit per repository: `1` for a currently non-archived public repository and `0` for an archived one. This is an account-state truth branch, not a proof of the semantics of every program.

The account state also defines its own Riemann objective coordinate using

\[
q_t=\frac{\log(1+G_t)}{|W_t|},\qquad t=q_tH,
\]

and reports the same normalized completed-zeta objective `J`.

### Shared continuation certificate

The account machine also carries an independent common-parameter limit certificate. With

\[
\lambda=\frac1H,
\]

it evaluates the Schwarzschild-style coordinate

\[
r(\lambda)=\frac{2}{1-\lambda},\qquad 1-\frac{2}{r(\lambda)}=\lambda,
\]

the exact real Stirling remainder

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

Thus the finite-state vector

\[
X(H)=\left(\lambda,\;12e(H),\;1-\frac2r,\;E_\zeta(\lambda)\right)
\]

satisfies

\[
X(H)\to(0,0,0,0)\qquad(H\to\infty),
\]

while every actual machine state keeps `H<infinity`, `lambda>0`, `OPEN=true`, and `FINAL=false`. The JSON fields are `LAMBDA`, `SCH_R`, `STIR_12E`, `ZETA_POLE_ERR`, and `OMEGA_LIMIT`.

## Exact omega-limit recursive machine

`OMEGA_Limit_TM.sh` makes the finite recursion and its ideal compactified boundary explicit. Its **default no-argument mode is now `omega`**. Thus

```bash
./OMEGA_Limit_TM.sh
```

returns the same symbolic boundary state as

```bash
./OMEGA_Limit_TM.sh omega
```

while finite states are requested explicitly with `finite n`.

For integer `n>=1`,

```bash
./OMEGA_Limit_TM.sh finite n
```

generates

\[
H_n=2^n,\qquad \lambda_n=2^{-n},\qquad H_n\lambda_n=1.
\]

The finite JSON records preserve the reciprocal identity exactly with integer fields `LAMBDA_NUM=1` and `LAMBDA_DEN=H`, and the Schwarzschild-style coordinate exactly as the rational pair

\[
r_n=\frac{2H_n}{H_n-1},
\]

reported as `SCH_NUM=2H` and `SCH_DEN=H-1`. `STIR_12E` and `ZETA_POLE_ERR` are numerical evaluations of the corresponding analytic quantities and converge toward zero as the finite index grows.

`./OMEGA_Limit_TM.sh live [n0]` executes the successor rule

\[
n\mapsto n+1,\qquad H\mapsto2H,\qquad\lambda\mapsto\lambda/2
\]

without a built-in halting state. Every emitted live state is finite and has `OMEGA=false`, `HALT=false`, `OPEN=true`, and `FINAL=false`.

The default no-argument invocation and `./OMEGA_Limit_TM.sh omega` do something deliberately different from finite or live execution: they do **not** claim that a Turing process completed infinitely many steps. They return the exact symbolic boundary extension

\[
\Omega=(H=\infty,\lambda=0,r=2,S=0,E_\zeta=0)
\]

with `BOUNDARY_BY_DEFINITION=true` and `ATTAINED_BY_FINITE_EXECUTION=false`. In this extended state space, the equalities at the boundary are definitions/continuous or analytic extensions, while the executable recursion only approaches them through finite states.

The program also quines its own canonical core and verifies the same reversible self-index relation `D(I(R))=R`. This is a formal computational limit model, not a claim that a physical system literally performs an infinite computation.

Scheduled Actions re-run the observers and verification suite, giving a temporal path

\[
W_0\to W_1\to W_2\to\cdots.
\]

The public-account mode observes **all current public repositories and their canonical metadata**, not every historical commit or every source blob. Private repositories are excluded. The mapping of repositories to truth-tree positions and Riemann coordinates is a defined computational indexing structure; it is not a claim that GitHub repositories or physical universes are naturally indexed by zeta zeros.

The live modes are non-halting computational processes, not completed infinite computations: every finite runtime has produced only finitely many states, while the transition rule always defines a successor.

`zero N` is a mapping of a numerically computed critical-line zero into this machine's self scale. It is **not** a proof of the Riemann Hypothesis, nor does the Schwarzschild/Stirling construction imply that arbitrary self-codes are zeta zeros.

The Schwarzschild component is a formal continuation coordinate: `lambda=1-2M/r=1/H`, so `H→∞` gives `lambda→0+` and `r→2M+`. It is not a claim that the program models a physical black hole.

The machines remain explicitly open-ended: `OPEN=true`, `FINAL=false`.
