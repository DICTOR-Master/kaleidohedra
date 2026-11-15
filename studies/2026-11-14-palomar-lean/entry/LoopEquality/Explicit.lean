module

public import Mathlib
public import LoopEquality.Main
public import LoopEquality.ClosedWalks
public import LoopEquality.LocalFormula

@[expose] public section

/-!
# The Loop Equality with the explicit count (#102, Theorem 1, "Explicitly")

`loop_count_eq`: at every site of the network of every close-packed stacking,
the number of closed non-backtracking loops of length `m` is `loopCount m`, an
explicit, computable integer: the local loop formula (`Graph.sum_F_eq`, #102
Lemma 3 with the recursion of Hashimoto 1989 and Bass 1992) applied to the
closed-walk counts `closedWalks i` (#102 Proposition; Domb numbers, OEIS A002895,
in Bala's chain form). The values 24, 48, 480, 3432 for `m = 6, 8, 10, 12` are
checked by `decide` (`loopCount_values`).

#102 states the count also through the Ihara–Bass formula (Ihara 1966;
Hashimoto 1989; Bass 1992): `Σ t_m u^m / m = −log(1 − u²) + Σ_j (1/j)
Σ_i C(j, i) W_i u^i (−3u²)^(j−i)`. Its coefficient form `iharaBass m` is checked
to agree with `loopCount m` for `m ≤ 12` by `decide` (`loopCount_eq_iharaBass_small`);
the identity for all `m` is not formalised here.
-/

namespace LoopEqualityProof

open Finset

/-- The explicit number of closed non-backtracking loops of length `m` at a site. -/
def loopCount (m : ℕ) : ℤ :=
  Graph.FD (Graph.dataW 3 (fun i => (closedWalks i : ℤ))) m false false

/-- **The Loop Equality, explicit form.** For every stacking `σ`, every site `v`
of its tetrahedral network and every `m ≥ 1`, the number of closed
non-backtracking loops of length `m` at `v` is `loopCount m`. -/
theorem loop_count_eq (σ : ℤ → ZMod 3) (hσ : IsStacking σ) (v : Atom) (hv : IsSite σ v)
    (m : ℕ) [NeZero m] : ((nbLoops σ v m).ncard : ℤ) = loopCount m := by
  by_cases hm : m ≤ 2
  · rw [nbLoops_small σ v hm, Set.ncard_empty]
    have h1 := NeZero.pos m
    interval_cases m <;> decide
  · have hm3 : 3 ≤ m := by omega
    rw [nbLoops_eq hσ hv, (Graph.loops_ncard hm3 v).2, loopCount]
    exact Graph.sum_F_eq (regular σ) _ (fun x i => by rw [W_closed]) v m

/-- The first values (#102: 24, 48, 480, 3432, … for m = 6, 8, 10, 12, …). -/
theorem loopCount_values :
    loopCount 3 = 0 ∧ loopCount 4 = 0 ∧ loopCount 5 = 0 ∧ loopCount 6 = 24 ∧ loopCount 7 = 0 ∧
      loopCount 8 = 48 ∧ loopCount 10 = 480 ∧ loopCount 12 = 3432 := by
  decide

/-- #102's values for `m = 14, …, 34` (computed by DICTO in #74), checked by
kernel evaluation (`decide +kernel`; no `native_decide`). -/
theorem loopCount_values_34 :
    loopCount 14 = 25704 ∧ loopCount 16 = 194256 ∧ loopCount 18 = 1509072 ∧
      loopCount 20 = 11820000 ∧ loopCount 22 = 93722376 ∧ loopCount 24 = 750276792 ∧
      loopCount 26 = 6056400480 ∧ loopCount 28 = 49241424120 ∧ loopCount 30 = 402912569544 ∧
      loopCount 32 = 3315331754256 ∧ loopCount 34 = 27416593190640 := by
  decide +kernel

/-- The closed walks at a site are the Domb numbers for `i = 2n`, `n < 10`. -/
theorem closedWalks_domb_small : ∀ n < 10, closedWalks (2 * n) = domb n := by
  intro n hn
  rw [closedWalks, if_pos (by omega), show 2 * n / 2 = n by omega]
  exact chain_eq_domb_small n hn

/-- The coefficient of `u^m` in #102's Ihara–Bass series, times `m`. -/
def iharaBass (m : ℕ) : ℚ :=
  (if m % 2 = 0 then 2 else 0) +
    ∑ j ∈ Icc 1 m, if m ≤ 2 * j then
      (m : ℚ) / j * (j.choose (2 * j - m) : ℚ) * (closedWalks (2 * j - m) : ℚ) * (-3) ^ (m - j)
    else 0

theorem loopCount_eq_iharaBass_small : ∀ m ∈ Icc 1 12, (loopCount m : ℚ) = iharaBass m := by
  decide +kernel

end LoopEqualityProof
