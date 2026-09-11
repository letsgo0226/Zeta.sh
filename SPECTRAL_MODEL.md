# Self-Encoded Analytically-Continued Spectral Turing Machine

`Spectral_TM.sh` is a formal computational model that combines reversible self-encoding, a computable successor path, a Riemann spectral coordinate, exact Stirling remainder bounds, and a Schwarzschild-form compactification.

## Self encoding

For canonical quine core `R`,

\[
G=I(R)=\frac{256^{|R|}-1}{255}+\operatorname{int}(R),\qquad D(G)=R.
\]

`SELF_SOLVED=true` means the integer coordinate decodes byte-for-byte back to the same core.

## Finite Turing path

For integer `n>=1`,

\[
H_n=2^n,\qquad \lambda_n=2^{-n},\qquad r_n=\frac{2H_n}{H_n-1}.
\]

These are represented exactly by integer numerator/denominator fields. The spectral coordinate is

\[
t_n=q_GH_n,\qquad q_G=\frac{\log(1+G)}{|R|}.
\]

The real Stirling remainder `e(H)` is not rounded to zero. Instead the machine carries the exact rational certificate

\[
\frac{12}{12H+1}<12e(H)<\frac1H.
\]

Thus every finite state has strictly positive Stirling residual while the upper bound tends to zero as `H -> infinity`.

## Spectral solutions

`solution N` (alias `zero N`) calls `mpmath.zetazero(N)` and evaluates the completed xi expression numerically at the corresponding critical-line coordinate. For a zero `rho`, the formal logarithmic derivative `xi'/xi` has a pole at `rho`; the JSON field `LOG_DERIV_POLE=true` records that mathematical representation. `ZERO_ENTROPY_BY_MODEL=true` and `INFO_H=0` mean that this model assigns one admissible solved branch to a selected zero. This is formal branching entropy, not thermodynamic entropy.

Numerically computed zeros are not a proof of the Riemann Hypothesis.

## Spectral compactification

The default state and explicit `omega` mode use the ideal extension

\[
H=\infty,\qquad \lambda=0,\qquad r=2,\qquad t=\infty.
\]

This is interpreted as spectral infinity compactified to a finite Schwarzschild-form boundary coordinate. `STIR_BOUND=0` is the boundary value of the exact finite remainder bounds. The machine reports

```text
BOUNDARY_BY_DEFINITION=true
ATTAINED_BY_FINITE_EXECUTION=false
OPEN=true
FINAL=false
```

so no finite execution is claimed to complete infinitely many steps.

## Modes

```bash
./Spectral_TM.sh
./Spectral_TM.sh omega
./Spectral_TM.sh self
./Spectral_TM.sh finite 4
./Spectral_TM.sh solution 1
./Spectral_TM.sh live 1
```

The `live` mode implements the open successor path

\[
n\mapsto n+1,\qquad H\mapsto2H,\qquad\lambda\mapsto\lambda/2,
\]

while the self coordinate remains invariant.

The construction is a formal cross-domain model. It does not assert that Riemann zeros, black-hole horizons, Stirling asymptotics, and physical entropy are literally one physical mechanism.
