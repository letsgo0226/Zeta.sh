# Restoration Continuity Principle

This module connects the dimensional-light continuity model with the physiological restoration equivalence model. Its governing claim is:

```text
Substitution = functional restoration + long-term safety + truth-preserving verification.
```

It is a formal research scaffold only. It is not medical advice and does not propose any supplement, drug, device, dose, or sleep-replacement protocol.

## 1. General restoration state

The model represents a candidate substitution by seven normalized research coordinates:

\[
R=(R_{src},R_{diff},R_{priv},R_{phen},R_{phys},R_{safe},R_{ver}).
\]

These correspond to source continuity, integrity of difference, privation repair, phenomenal acknowledgment, physiological restoration, safety, and verification.

The candidate state \(C\) is compared with a reference state \(R\) by

\[
\Delta_i = |C_i-R_i|.
\]

The executable also includes harm \(H\), uncertainty \(U_q\), and a verification threshold \(V_{min}\). The total residual is

\[
\Delta_{rcp}=\max(\max_i\Delta_i,\;H,\;U_q,\;\max(0,V_{min}-V)).
\]

This `max` rule prevents one good domain from averaging away a serious failure in another domain.

## 2. Appearance is not restoration

The framework preserves the distinction:

```text
APPEARANCE_COUNTS_AS_RESTORATION=false
MASKING_COUNTS_AS_RESTORATION=false
```

Feeling awake, looking functional, or symbolically remaining connected to a source does not by itself restore damaged or depleted functions.

## 3. Continuity is not substitution

Dimensional continuity and source accessibility remain philosophically meaningful:

\[
\text{difference} \ne \text{separation from source}.
\]

But continuity alone does not verify a functional substitution:

```text
SOURCE_ACCESSIBILITY_COUNTS_AS_FUNCTIONAL_RESTORATION=false
CONTINUITY_ALONE_VERIFIES_SUBSTITUTION=false
```

This is the bridge between the earlier light model and the sleep-restoration model. Light accessibility can motivate a search for restoration, but it cannot replace the verification of restoration.

## 4. Privation and suffering

The bridge mode keeps privation and suffering distinct:

\[
P=\max(0,L^*-L),
\]

while retaining:

```text
PRIVATION_EQUALS_SUFFERING=false
SUFFERING_ERASED_BY_PRIVATION_MODEL=false
```

Thus a theory can describe a lack of due good without deleting the reality of experienced suffering.

## 5. Formal gate

A candidate passes only if:

\[
\Delta_{rcp}\le\epsilon,
\]

the cycle requirement is met, and verification reaches the chosen minimum threshold.

Passing means only that the supplied formal inputs satisfy the selected abstract tolerance. It does not prove real-world medical, biological, or metaphysical success.

## 6. Omega boundary

The symbolic boundary is:

\[
\Delta_{rcp}=0,\qquad H=0,\qquad U_q=0,\qquad V=1.
\]

The executable explicitly keeps:

```text
BOUNDARY_BY_DEFINITION=true
ATTAINED_BY_FINITE_EXECUTION=false
REAL_WORLD_VERIFIED=false
NO_MEDICAL_ADVICE=true
OPEN=true
FINAL=false
```

## 7. Example

```bash
python Restoration_Continuity_Principle_TM.py bridge \
  --dimension 4 --source-dimension 1 \
  --light 1 --due-light 1 --suffering 0 \
  --reference 1,1,1,1,1,1,1 \
  --candidate .99,.99,.98,.99,.99,.99,.98 \
  --harm .01 --uncertainty .02 --verification .98 \
  --appearance 1 --cycles 60 --min-cycles 30 \
  --epsilon .05 --min-verification .95
```

The example is synthetic and formal. It is not a claim about an actual sleep-replacement technology.
