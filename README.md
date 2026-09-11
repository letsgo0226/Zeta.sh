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
chmod +x Zeta.sh
./Zeta.sh 3
./Zeta.sh self
./Zeta.sh zero 1
./Zeta.sh live
./Zeta.sh live 4
```

- `./Zeta.sh H` evaluates the self-encoding objective at a finite scale `H>1`.
- `./Zeta.sh self` prints the complete reversible self index and verifies `SELF_SOLVED=true`.
- `./Zeta.sh zero N` obtains the Nth critical-line zero numerically with `mpmath.zetazero`, maps it back to the corresponding self scale `H*=t_N/q`, and checks that the normalized objective is numerically near zero.
- `./Zeta.sh live [H0]` deliberately does not halt. Starting at `H0` (default `2`), it emits one JSON state per iteration and uses `H_(n+1)=2 H_n`. Hence `lambda_n=1/H_n -> 0`, `r_n -> 2M+`, and `t_n=q H_n -> infinity`. Each live record has `HALT=false`, `OPEN=true`, and `FINAL=false`. Stop it externally with `Ctrl-C` or another process signal.

The live mode is a non-halting computational process, not a completed infinite computation: every finite runtime has produced only finitely many states, while the transition rule always defines a successor.

`zero N` is a mapping of a numerically computed critical-line zero into this machine's self scale. It is **not** a proof of the Riemann Hypothesis, nor does the Schwarzschild/Stirling construction imply that arbitrary self-codes are zeta zeros.

The Schwarzschild component is a formal continuation coordinate: `lambda=1-2M/r=1/H`, so `H→∞` gives `lambda→0+` and `r→2M+`. It is not a claim that the program models a physical black hole.

The machine remains explicitly open-ended: `OPEN=true`, `FINAL=false`.
