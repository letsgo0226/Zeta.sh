# Peace Proposal Machine

`Peace_Action_TM.sh` is a compact formal proposal generator. It does **not** claim that a GitHub Action can stop a war by itself.

The target state is a seven-condition peace kernel:

1. verified ceasefire
2. civilian protection
3. humanitarian access
4. independent monitoring
5. inclusive negotiation
6. security arrangements
7. dispute resolution

The script defines `TARGET_ERROR` as the number of missing target conditions. The emitted proposal has `TARGET_ERROR=0` and `INFO_H=0` only in the internal model: there is one fully specified target branch. This is a formal zero-branch-entropy target, not evidence that a real conflict has ended.

`REAL_WORLD_VERIFIED=false` and `CLAIM="proposal-not-outcome"` are intentional. Real peace requires adoption, consent, diplomacy, verification, institutions, and continuing human judgment.

The machine keeps the prior reversible self-encoding idea: `SELF_SOLVED=true` means its canonical quine core decodes from its exact integer index back to itself.

The workflow `.github/workflows/peace.yml` runs every five minutes nominally, on pushes and pull requests, by manual dispatch, and through `repository_dispatch` type `peace-evolve`. A manual or dispatch event can supply a conflict label; scheduled runs default to `GLOBAL`. Each run verifies the one-liner is under 2048 bytes and uploads `peace.json` as an artifact.
