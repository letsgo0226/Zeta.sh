# Physiological Restoration Equivalence Framework

This module treats hypothetical sleep replacement as a **multisystem physiological equivalence problem**, not as a stimulant or supplement recommendation. It is a research scaffold only.

## 1. Restoration state

Normal sleep is represented by a reference recovery vector

\[
R=(R_n,R_m,R_s,R_c,R_i,R_e,R_{met},R_{cv},R_a,R_{circ}),
\]

covering neural, memory, synaptic, clearance, immune, endocrine, metabolic, cardiovascular, autonomic, and circadian domains.

A candidate intervention produces

\[
U=(U_n,\ldots,U_{circ}).
\]

The executable uses normalized values in \([0,1]\) purely as abstract research coordinates. They are **not clinical measurements** unless a future empirical pipeline supplies validated data and calibration.

## 2. Equivalence residual

For each domain,

\[
\Delta_i=|U_i-R_i|.
\]

The model computes

\[
\Delta_{max}=\max_i\Delta_i,
\]

and combines this with explicit harm and uncertainty variables:

\[
\Delta_{rest}=\max(\Delta_{max},H,U_q).
\]

A formal gate may pass only if

\[
\Delta_{rest}\le\varepsilon
\]

and a user-specified minimum number of repeated cycles has been reached. Passing this gate means only that **the supplied formal inputs satisfy the chosen tolerance**.

It does not establish that sleep has been replaced safely.

## 3. Alertness is not restoration

The framework keeps alertness as a separate field:

```text
ALERTNESS_COUNTS_AS_RESTORATION=false
```

A stimulant-like intervention can improve wakefulness while leaving one or more restoration domains impaired. Therefore alertness never contributes to equivalence by itself.

## 4. Longitudinal requirement

A true replacement claim would require repeated-cycle equivalence, because an intervention may look acceptable after one cycle while accumulating deficits later. Hence the model keeps

```text
LONGITUDINAL_EVIDENCE_REQUIRED=true
MULTISYSTEM_EQUIVALENCE_REQUIRED=true
```

Real validation would need pre-specified biomarkers and functional endpoints, adverse-event monitoring, circadian timing, repeated cycles, suitable controls, uncertainty propagation, and independent replication.

## 5. Omega boundary

The symbolic boundary is

\[
\Delta_{rest}=0,\qquad H=0,\qquad U_q=0.
\]

This is a definition of ideal equivalence, not a result obtained from finite evidence:

```text
BOUNDARY_BY_DEFINITION=true
ATTAINED_BY_FINITE_EXECUTION=false
FULL_SLEEP_REPLACEMENT_VERIFIED=false
REAL_WORLD_VERIFIED=false
```

## 6. Example

```bash
python Physiological_Restoration_Equivalence_TM.py assess \
  --reference 1,1,1,1,1,1,1,1,1,1 \
  --candidate .99,.98,.99,.98,.99,.99,.98,.99,.99,.98 \
  --harm .01 --uncertainty .02 --alertness 1 \
  --cycles 60 --min-cycles 30 --epsilon .05
```

This example uses synthetic normalized values for software testing only.

## 7. Medical boundary

The repository intentionally does not provide a supplement formula, dose, drug combination, or personal treatment plan. Current deployment status remains:

```text
FULL_SLEEP_REPLACEMENT_VERIFIED=false
REAL_WORLD_VERIFIED=false
PERSONALIZED_MEDICAL_CLAIM=false
NO_DOSING_OR_TREATMENT_ADVICE=true
FORMAL_MODEL_ONLY=true
OPEN=true
FINAL=false
```
