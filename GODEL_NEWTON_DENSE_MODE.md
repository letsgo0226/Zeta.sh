# Gödel-indexed Gaussian Rationals and Newton Dynamics of ζ(s)

This note formalizes the `newton` mode in `Zeta_TM.sh`. It is an offline research model, not a proof of the Riemann hypothesis and not a claim that the Riemann zeta function is literally identical to a Turing machine.

## 1. Countable dense initial states

The program uses a computable enumeration

\[
\phi:\mathbb N\to\mathbb Q(i),
\qquad
\mathbb Q(i)=\{a+ib:a,b\in\mathbb Q\}.
\]

The set \(\mathbb Q(i)\) is countable and dense in \(\mathbb C\):

\[
\overline{\mathbb Q(i)}=\mathbb C.
\]

This does **not** mean that a finite or countable computation visits every complex point. It means every nonempty open disk in \(\mathbb C\) contains a Gaussian-rational point.

## 2. Gödel-indexed self start

Let \(P\) denote the current program and let \(E(P)\) be its exact reversible byte/integer code. With modulus \(M\),

\[
i_P=E(P)\bmod M,
\qquad
X_P=\phi(i_P).
\]

Running

```bash
sh Zeta_TM.sh newton
```

uses this self-derived index. Running

```bash
sh Zeta_TM.sh newton --index 0
```

uses an explicit Gaussian-rational starting point instead.

The modulus projection is non-injective, so \(X_P\) does not uniquely determine the full program code.

## 3. Newton map for ζ zeros

The ideal analytic Newton map is

\[
N_\zeta(s)=s-\frac{\zeta(s)}{\zeta'(s)}.
\]

The implemented finite computation uses the same finite Euler–Maclaurin zeta approximation as the rest of `Zeta_TM.sh` and a centered finite-difference derivative,

\[
\zeta'(s)\approx
\frac{\zeta_N(s+h)-\zeta_N(s-h)}{2h}.
\]

Hence an observed numerical orbit is

\[
X_0,\ X_1,\ldots,\ X_k,
\qquad
X_{j+1}=X_j-\frac{\zeta_N(X_j)}
{[\zeta_N(X_j+h)-\zeta_N(X_j-h)]/(2h)}.
\]

The output trace records each iterate and its numerical residual \(|\zeta_N(X_j)|\).

## 4. Program-to-zero chain

The self-indexed construction is

\[
P
\longrightarrow
E(P)
\longrightarrow
i_P=E(P)\bmod M
\longrightarrow
X_P=\phi(i_P)
\longrightarrow
N_{\zeta,N}^{\,k}(X_P).
\]

If the numerical orbit reaches the requested tolerance, the mode reports `CONVERGED=true`. This is a finite numerical convergence result for the chosen approximation and starting point, not a global theorem about Newton dynamics.

## 5. Exact theorem branches

If the enumerated start is an exact negative even integer,

\[
X=-2m,\qquad m\ge1,
\]

the program uses the theorem

\[
\zeta(-2m)=0
\]

and reports an exact trivial zero without numerical Newton steps.

If the start is \(X=1\), the program does not evaluate a finite value of \(\zeta(1)\), because \(s=1\) is the simple pole of the zeta function.

## 6. Boundaries

The mode deliberately reports:

- `GLOBAL_CONVERGENCE_GUARANTEED=false`;
- `ERROR_BOUND_RIGOROUS=false`;
- `RIEMANN_HYPOTHESIS_PROVED=false`;
- `INDEX_PROJECTION_INJECTIVE=false`;
- `PROGRAM_EQUALS_ZETA=false`;
- `OPEN=true`;
- `FINAL=false`.

Newton iteration may converge to different zeros from different initial states, fail to converge, or encounter an unstable/near-critical derivative. Therefore this construction is a Gödel-indexed numerical dynamical system over a countable dense set of initial states, not a single-valued global inverse \(\zeta^{-1}\).

## 7. Usage

```bash
# self-Gödel-derived Gaussian-rational start
sh Zeta_TM.sh newton

# deterministic dense start X_0 = 0
sh Zeta_TM.sh newton --index 0 --terms 32 --max-steps 20 --tolerance 1e-8

# exact trivial-zero branch X_21 = -2
sh Zeta_TM.sh newton --index 21 --terms 16
```

The mathematically precise summary is

\[
\boxed{
\mathbb N
\xrightarrow{\phi}
\mathbb Q(i)
\subset\mathbb C
\xrightarrow{N_\zeta}
\text{Newton orbits toward zeros of }\zeta
}
\]

with the self-referential specialization

\[
\boxed{
P\to E(P)\to E(P)\bmod M\to\phi(i_P)\to N_{\zeta,N}^{\,k}(\phi(i_P)).
}
\]
