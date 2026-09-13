# Empirical Metaphysics Bridge

This module extends the **Generative Metatheory of Physical Worlds** by adding an explicit statistical interface between a candidate physical model and measured data. It does not turn metaphysical possibility into empirical fact by definition.

## 1. Observable map

A candidate theory must provide an observational map

\[
\mathcal O:\mathcal S\to\mathbb R^k,
\]

which converts theoretical states into quantities that can in principle be measured. For the executable prototype, one scalar observable is used:

\[
D=(d,\sigma_D,u,\text{source}),
\]

where \(d\) is the measured value, \(\sigma_D\) its stated measurement uncertainty, \(u\) its unit, and `source` is a user-supplied provenance label.

The program hashes this record to produce an integrity fingerprint. A hash verifies record identity, **not** scientific provenance. Therefore it always reports `PROVENANCE_VERIFIED=false` unless an external verification system is added.

## 2. Competing hypotheses

Two hypotheses predict

\[
H_i:\quad O\sim \mathcal N(\mu_i,\sigma_i^2),\qquad i\in\{1,2\}.
\]

Under the explicitly declared assumption that measurement uncertainty and model uncertainty are independent and Gaussian,

\[
s_i^2=\sigma_D^2+\sigma_i^2.
\]

The likelihood is

\[
P(D\mid H_i)
=\frac{1}{\sqrt{2\pi s_i^2}}
\exp\!\left[-\frac{(d-\mu_i)^2}{2s_i^2}\right].
\]

The executable computes this in log space:

\[
\log P(D\mid H_i)
=-\frac12\frac{(d-\mu_i)^2}{s_i^2}-\log s_i-\frac12\log(2\pi).
\]

## 3. Bayes factor and posterior comparison

The data-only model comparison is

\[
\log BF_{12}
=\log P(D\mid H_1)-\log P(D\mid H_2).
\]

If positive prior weights \(\pi_1,\pi_2\) are supplied, the two-model posterior is

\[
P(H_i\mid D)
=\frac{P(D\mid H_i)\pi_i}{\sum_jP(D\mid H_j)\pi_j}.
\]

The posterior therefore depends on both the likelihood model and the supplied priors. It is not an automatic proof that either hypothesis is true.

If two hypotheses give identical tested predictions with identical uncertainties, then

\[
BF_{12}=1,
\]

so those data cannot empirically distinguish them. This makes empirical underdetermination executable rather than merely verbal.

## 4. Interface

```bash
python Empirical_Metaphysics_TM.py self
python Empirical_Metaphysics_TM.py omega
python Empirical_Metaphysics_TM.py compare \
  --observable x --unit arb \
  --value 10 --obs-sigma 1 \
  --h1-mu 10 --h1-sigma 1 \
  --h2-mu 14 --h2-sigma 1 \
  --p1 1 --p2 1 \
  --source synthetic-ci
```

The numerical example is synthetic and exists only to test the calculation. To perform scientific analysis, replace it with a concrete physical observable, justified model predictions, dimensional consistency, documented uncertainties, and traceable data provenance.

## 5. Interpretation boundary

The bridge implements

\[
\boxed{
\text{formal hypothesis}
\to\text{physical prediction}
\to P(D\mid H_i)
\to\text{model comparison}
}
\]

but preserves

\[
\boxed{
\text{formal possibility}
\neq
\text{physical reality}
\neq
\text{empirical confirmation}.
}
\]

The executable therefore keeps the following flags false:

```text
PROVENANCE_VERIFIED=false
EMPIRICAL_SCIENCE_VERIFIED=false
PHYSICAL_REALITY_VERIFIED=false
FORMAL_POSSIBILITY_EQUALS_PHYSICAL_REALITY=false
UNIQUE_FINAL_THEORY_VERIFIED=false
OPEN=true
FINAL=false
```

## 6. Scientific limitations

The current likelihood is deliberately minimal. Real analyses may require covariance matrices, nuisance parameters, non-Gaussian errors, selection effects, calibration uncertainty, hierarchical models, posterior predictive checks, robustness to priors, multiple-testing control, and explicit model misspecification checks.

A statistical preference inside a chosen model class is not the same as ontological proof. The empirical bridge becomes scientifically informative only when the observational map, data, uncertainty model, and competing physical hypotheses are themselves defensible.
