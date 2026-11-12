# Grogan 2610.01307 v2: full-scope check, run log (12 Nov 2026)

## Lean, Theorem 1.4 (FiniteSymmetry.lean on the supported Lean 4.35.0-rc2 checkpoint)
- Toolchain: Lean 4.35.0-rc2 (commit 11acb17e, equal to the author's receipt), mathlib 06535612 (official cache, 8915 files).
- FiniteSymmetry.lean SHA-256 a3f3445311f8... equal to the paper.
- Build of SparseMonotiles.T5Monotile from source: 1331 modules, exit 0 (stronger than the author's receipt, which reused objects).
- Audit: T5_strong_aperiodic_bound : IsCompact T5 ∧ HasTiling T5 ∧ ∀ tiles, IsTiling T5 tiles → Finite (EuclideanSymmetries tiles) ∧
  Nat.card (EuclideanSymmetries tiles) ≤ 3840. All 10 axiom reports (6 printed by the source, 4 by our audit lines) are exactly
  [propext, Classical.choice, Quot.sound]; no sorryAx; no sorry/admit/native_decide/axiom in the source.
- Definitions read (Model.lean): IsTiling = images of T under arbitrary isometries (≃ᵢ), covering, pairwise disjoint interiors;
  IsPeriod preserves the tile collection; EuclideanSymmetries = isometries preserving the collection. Match the paper's Theorem 1.4.

## Faults in our own checks (none is a mismatch with the paper)
1. First evidence run: our inline shell quoting emptied the path variables; no script ran. Rerun from a script file.
2. First Lean 4.35 run: we targeted `lake build SparseMonotiles`; this checkpoint has no root file. Rerun on the module target.
3. Second Lean 4.35 run: our control demanded exactly 4 axiom lines; the source prints 6 more. All 10 standard; result passes.

## Own computations (our code, none of the author's)
- E (Proposition 3.2) for (p, g, mu) = (3,2,1), (5,2,1), (5,3,1), (5,2,4), (5,3,4), (7,6,1): counts equal formula (6); p = 5, 7 sets equal
  the author's data files contact by contact; E for mu = 1 and mu = 4 at p = 5 is the SAME SET (mu-independence).
- Lemma 2.1 dissection: children partition 2C_p at p = 3, 5, 7.
- Lemma 7.1 finite data from the two JSON specs: 160 / 896 facet triples equal the exposed facets; keys/facet {1:128, 4:32} and
  {1:768, 2:128}; 256 / 1024 keys, half bumps; h = 1/(48d); edge margins 89/320, 181/672 (> 1/4); max slope 1/2; 2 max w < 1/D.
