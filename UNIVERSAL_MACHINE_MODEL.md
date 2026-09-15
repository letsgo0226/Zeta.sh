# Universal Machine — Offline Research Model

`Universal_Machine.sh` is a self-contained, offline shell/Python research model. It uses only Python's standard library and requires no network access or third-party packages.

## 1. Exact self-encoding

For source bytes `P`, the machine uses the reversible integer code

\[
E(P)=\frac{256^{|P|}-1}{255}+\operatorname{int}(P),
\]

with decoder `D` satisfying `D(E(P))=P` for the current file bytes. This is an exact syntactic identity, not a proof of semantic completeness.

## 2. Universal TM interpreter

The `simulate` mode interprets a finite deterministic single-tape Turing-machine description stored in local JSON. A machine file has the form:

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

Each transition maps `state|symbol` to `[next_state, write_symbol, direction]`, where direction is `L`, `R`, or `N`. The interpreter therefore simulates any finite deterministic single-tape TM description supplied in this representation, subject to the explicit finite `--max-steps` execution bound.

Example:

```bash
sh Universal_Machine.sh simulate --machine machine.json --input 111 --max-steps 10000
```

This is a practical universal interpreter at the model level; it does not claim that every computation halts or that the halting problem is solved.

## 3. Self-derived Riemann coordinate

The machine also retains the preceding Riemann–Quine research layer. Its own exact source code determines

\[
r=E(P)\bmod 1000003,
\qquad
X=\frac12+i\left(14+30\frac r{1000003}\right).
\]

The `point` mode evaluates a finite Euler–Maclaurin approximation to `ζ(X)` twice, at cutoffs `N` and `2N`, and reports their difference only as a convergence diagnostic. It does not label finite floating-point evaluation as exact analytic truth.

## 4. Pole normalization and formal zero

At `s=1`, `ζ` has a simple pole with residue one:

\[
\operatorname{Res}_{s=1}\zeta(s)=1,
\qquad
\lim_{s\to1}(s-1)\zeta(s)=1,
\]

so

\[
\log\left(\lim_{s\to1}(s-1)\zeta(s)\right)=\log1=0.
\]

The `pole` mode keeps this theorem-level zero distinct from finite numerical error.

The `zero` mode also records exact formal/construction-level invariants for the Schwarzschild relation `r_s=2M` and for a Stirling expansion only when its exact remainder is included. Hence

`FORMAL_ZERO_ERROR=true`

is never identified with

`NUMERICAL_ZERO_ERROR=true`.

## 5. Modes

```bash
sh Universal_Machine.sh self
sh Universal_Machine.sh point
sh Universal_Machine.sh pole
sh Universal_Machine.sh zero
sh Universal_Machine.sh simulate --machine machine.json --input 111
sh Universal_Machine.sh omega
```

The machine remains a formal research model and reports `OFFLINE=true`, `OPEN=true`, and `FINAL=false`.
