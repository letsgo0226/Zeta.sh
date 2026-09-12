# SDGs as a Computable Dynamical System

This repository component treats the UN Sustainable Development Goals (SDGs) as a **formal academic research model** in mathematics, physics, and information science. It does not claim that a symbolic zero-residual state means the real world has achieved the SDGs.

## 1. Mathematical state space

Let

\[
G(X)=(G_1(X),\ldots,G_{17}(X)),\qquad 0\le G_i\le 1.
\]

Define goal gaps

\[
d_i(X)=1-G_i(X).
\]

Two complementary residuals are used:

\[
\Delta_{\Sigma}(X)=\sum_{i=1}^{17} d_i(X),
\qquad
\Delta_{\infty}(X)=\max_i d_i(X).
\]

The formal SDG boundary is

\[
\Omega_{\rm SDG}=\{X:G_i(X)=1\;\forall i\},
\]

so

\[
X\in\Omega_{\rm SDG}\iff \Delta_{\Sigma}=\Delta_{\infty}=0.
\]

The sum prevents information loss about aggregate shortfall, while the maximum prevents good performance on some goals from masking a failed goal.

## 2. Exact finite path

`finite n` uses the exact rational research tolerance

\[
\epsilon_n=2^{-n}.
\]

It is emitted as the integer pair `EPS_NUM=1`, `EPS_DEN=2^n`. Every finite state has \(\epsilon_n>0\), while

\[
\lim_{n\to\infty}\epsilon_n=0.
\]

The default/`omega` output is a symbolic boundary, not a completed infinite computation.

## 3. Self encoding

`SDG_Research_TM.sh` retains the reversible program coordinate

\[
G_R=I(R),\qquad D(G_R)=R,
\]

where `R` is its canonical quine core. `SELF_SOLVED=true` certifies exact byte recovery only.

## 4. Dynamical and control interpretation

A research-scale world model may be written

\[
X_{t+1}=F(X_t,U_t,W_t),
\]

where \(U_t\) denotes policy or control actions and \(W_t\) external disturbances. A candidate Lyapunov-like objective is

\[
V(X)=\sum_i w_i d_i(X)^2.
\]

A policy is progress-making when it decreases the chosen residual or Lyapunov objective subject to feasibility constraints. If no state satisfies all goals simultaneously, the relevant mathematical object is a Pareto frontier rather than a fictitious exact optimum.

## 5. Physical constraints

SDG trajectories must remain inside a physically feasible region, for example energy, water, material, carbon, and ecological resource balances. In the compact `assess` mode this entire layer is represented only by the first evidence bit, `PHYSICAL_FEASIBLE`. It is a formal gate, not a physical simulation.

A full empirical model should replace that bit with explicit conservation and capacity constraints such as

\[
E_{\rm supply}\ge E_{\rm demand},
\qquad
W_{\rm extraction}\le W_{\rm sustainable},
\]

and material/carbon stock-flow equations.

The model's `SOLUTION_ENTROPY=0` at the symbolic boundary is **solution-space entropy by definition**, not thermodynamic entropy. No claim of \(S_{\rm thermo}=0\) is made.

## 6. Information-science constraints

An empirical indicator should carry more than a scalar value. A useful record is

\[
I_j=(v_j,\sigma_j,t_j,s_j,p_j),
\]

containing value, uncertainty, time, source, and provenance. The compact `assess` mode therefore includes three evidence bits:

1. physical feasibility,
2. provenance completeness,
3. bounded uncertainty.

`ADMISSIBLE=true` requires all 17 normalized scores to equal 100 and all three evidence bits to equal 1. Even then the program emits `REAL_WORLD_VERIFIED=false`; real-world verification requires external evidence.

## 7. Compact interfaces

```bash
./SDG_Research_TM.sh
./SDG_Research_TM.sh omega
./SDG_Research_TM.sh self
./SDG_Research_TM.sh finite 4
./SDG_Research_TM.sh check 11111111111111111
./SDG_Research_TM.sh check 11111111111111110
./SDG_Research_TM.sh assess 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100 111
```

For `check`, the 17 bits are only an abstract goal-level test vector. For `assess`, each score is an integer in `[0,100]`; the residuals are

\[
\texttt{TOTAL_GAP}=\sum_i(100-x_i),
\qquad
\texttt{BOTTLENECK}=\max_i(100-x_i).
\]

## 8. Open-system interpretation

The intended research question is:

> Can the SDGs be represented as a physically constrained, information-aware, multi-objective dynamical system whose admissible trajectories converge toward a zero-residual viability region?

The answer is not hard-coded. The compact machine supplies definitions and executable invariants; empirical data, causal models, policy effects, and uncertainty estimates must be supplied independently.

Accordingly the formal system remains

```text
FORMAL_MODEL_ONLY=true
REAL_WORLD_VERIFIED=false
OPEN=true
FINAL=false
```

Finite specified checks may be decidable, while the global socio-ecological system remains open to new data, new failure modes, and revised models.
