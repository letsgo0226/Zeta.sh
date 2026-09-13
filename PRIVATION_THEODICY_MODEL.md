# Privation, Innocent Suffering, and Non-Compensation

This module formalizes a philosophical distinction rather than proving a theological doctrine.

Let \(G^*(x)\) be a due good and \(G(x)\) the realized good. Define privation

\[
E_{priv}(x)=\max(0,G^*(x)-G(x)).
\]

Under a privation theory, evil need not be modeled as an independently created substance. This does **not** imply that suffering, injury, injustice, or loss are unreal.

The central distinction is:

\[
Q_1:\;\text{Must evil be an independently created substance?}
\]

versus

\[
Q_2:\;\text{Why is severe innocent suffering permitted?}
\]

A privation theory may answer \(Q_1\) negatively while leaving \(Q_2\) unresolved.

For an individual \(i\), let \(S_i\ge0\) denote suffering and \(C_i\in\{0,1\}\) culpability. Innocent suffering is represented as

\[
C_i=0\land S_i>0.
\]

To prevent aggregate benefit from simply canceling severe harm to an innocent person, introduce a non-compensation constraint. For a chosen formal threshold \(S_{max}\),

\[
C_i=0\Rightarrow S_i\le S_{max}.
\]

This is a normative modeling device, not a claim that one universal numerical suffering threshold exists in moral reality.

The executable prototype `Privation_Theodicy_TM.py` has three modes:

```bash
python Privation_Theodicy_TM.py logic
python Privation_Theodicy_TM.py assess 10 6 8 0 5
python Privation_Theodicy_TM.py omega
```

`assess` reports privation, whether suffering is innocent under the supplied culpability bit, and whether the supplied non-compensation threshold is violated. It always keeps:

```text
PRIVATION_ERASES_SUFFERING=false
THEODICY_RESOLVED=false
EMPIRICAL_GOD_CLAIM=false
FORMAL_MODEL_ONLY=true
OPEN=true
FINAL=false
```

The `omega` mode is only a formal boundary in which modeled privation and innocent suffering approach zero. It does not prove that such a world is physically attainable, that a theodicy is successful, or that God exists or does not exist.

This module is intended to preserve three levels:

\[
\text{ontology of evil}\neq\text{ethics of suffering}\neq\text{theology of permission}.
\]

Its purpose is to prevent a metaphysical account of evil as privation from being used to erase or trivialize the moral reality of innocent suffering.
