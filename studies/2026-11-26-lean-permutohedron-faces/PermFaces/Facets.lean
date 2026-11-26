/-
The facets of the permutohedron as exposed faces (step 3a of the restructured Vacuus entry, 26 Nov 2026).
DICTO, with Claude (Anthropic). Built on TauCeti's formalization of Rado's theorem (TauCeti/Analysis/Convex/PermutationOrbit.lean).
-/
import TauCeti.Analysis.Convex.PermutationOrbit
import Mathlib.Analysis.Convex.Exposed

/-!
# Permutohedron facets (step 3a)

`P n` is the convex hull of the rearrangements of `w = (n, n-1, …, 1)`. For a set `S` of coordinates with `|S| = k`:
* `sum_le_top`: every point of `P n` has `∑_{i ∈ S} xᵢ ≤ top k` (the sum of the `k` largest entries of `w`);
* `facet_isExposed`: the points where equality holds form an exposed face of `P n` (the facet of `S` when `∅ ≠ S ≠ univ`).
The proof moves `S` onto the first `k` coordinates by a permutation and applies TauCeti's prefix-sum bound (the easy half of
Rado's theorem) to the permuted point, which stays in `P n` by TauCeti's permutation invariance.
-/

open Finset

namespace PermFaces

variable {n : ℕ}

/-- `w = (n, n-1, …, 1)`. -/
def w (n : ℕ) : Fin n → ℝ := fun i => ((n - (i : ℕ) : ℕ) : ℝ)

theorem w_antitone : Antitone (w n) := by
  intro i j hij
  simp only [w]
  exact_mod_cast Nat.sub_le_sub_left (Fin.le_def.1 hij) n

/-- The permutohedron: the convex hull of the rearrangements of `w`. -/
def P (n : ℕ) : Set (Fin n → ℝ) := convexHull ℝ (Set.range fun σ : Equiv.Perm (Fin n) => w n ∘ σ)

/-- The sum of the `k` largest entries of `w`. -/
def top (n k : ℕ) : ℝ := TauCeti.prefixSum k (w n)

/-- For antitone `v`, the sum over any `k` coordinates is at most the sum over the first `k`. -/
theorem sum_le_prefixSum_of_antitone {v : Fin n → ℝ} (hv : Antitone v) (T : Finset (Fin n)) :
    ∑ j ∈ T, v j ≤ TauCeti.prefixSum T.card v := by
  classical
  rw [TauCeti.prefixSum_def]
  set F : Finset (Fin n) := univ.filter fun j : Fin n => (j : ℕ) < T.card
  have hF : F.card = T.card := by
    have hk : T.card ≤ n := by simpa using T.card_le_univ
    simp only [F]; rw [Fin.card_filter_val_lt]; omega
  -- split both sums along T ∩ F
  rw [← sum_sdiff (inter_subset_left : T ∩ F ⊆ T), ← sum_sdiff (inter_subset_right : T ∩ F ⊆ F)]
  gcongr ?_ + _
  have hc : (T \ (T ∩ F)).card = (F \ (T ∩ F)).card := by
    rw [card_sdiff_of_subset inter_subset_left, card_sdiff_of_subset inter_subset_right, hF]
  rcases Nat.eq_zero_or_pos T.card with h0 | hpos
  · have : T = ∅ := card_eq_zero.1 h0
    subst this; simp [F]
  · have hk : T.card - 1 < n := by have := T.card_le_univ; simp at this; omega
    set c := v ⟨T.card - 1, hk⟩
    have h1 : ∑ j ∈ T \ (T ∩ F), v j ≤ (T \ (T ∩ F)).card • c := by
      apply sum_le_card_nsmul; intro j hj
      have : ¬ (j : ℕ) < T.card := by
        intro hlt; simp only [mem_sdiff, mem_inter, F, mem_filter, mem_univ, true_and] at hj; exact hj.2 ⟨hj.1, hlt⟩
      exact hv (Fin.le_def.2 (by simp; omega))
    have h2 : (F \ (T ∩ F)).card • c ≤ ∑ j ∈ F \ (T ∩ F), v j := by
      apply card_nsmul_le_sum; intro j hj
      have : (j : ℕ) < T.card := by simp only [mem_sdiff, F, mem_filter, mem_univ, true_and] at hj; exact hj.1
      exact hv (Fin.le_def.2 (by simp; omega))
    rw [hc] at h1; exact h1.trans h2

/-- **Facet inequality.** -/
theorem sum_le_top {x : Fin n → ℝ} (hx : x ∈ P n) (S : Finset (Fin n)) : ∑ i ∈ S, x i ≤ top n S.card := by
  classical
  refine convexHull_min (t := {x | ∑ i ∈ S, x i ≤ top n S.card}) ?_ ?_ hx
  · rintro _ ⟨σ, rfl⟩
    simp only [Set.mem_ofPred_eq, Function.comp_apply, top]
    have := sum_le_prefixSum_of_antitone (w_antitone (n := n)) (S.map σ.toEmbedding)
    simpa [sum_map, card_map] using this
  · intro x hx y hy a b ha hb hab
    simp only [Set.mem_ofPred_eq, Pi.add_apply, Pi.smul_apply, smul_eq_mul, sum_add_distrib, ← mul_sum] at hx hy ⊢
    calc a * ∑ i ∈ S, x i + b * ∑ i ∈ S, y i ≤ a * top n S.card + b * top n S.card := by gcongr
      _ = top n S.card := by rw [← add_mul, hab, one_mul]

/-- A permutation of the coordinates carrying the first `|S|` positions onto `S`, so the bound is attained. -/
theorem exists_top (S : Finset (Fin n)) : ∃ y ∈ P n, ∑ i ∈ S, y i = top n S.card := by
  classical
  set F : Finset (Fin n) := univ.filter fun j : Fin n => (j : ℕ) < S.card
  have hF : F.card = S.card := by
    have hk : S.card ≤ n := by simpa using S.card_le_univ
    simp only [F]; rw [Fin.card_filter_val_lt]; omega
  let e : {x // x ∈ F} ≃ {x // x ∈ S} := Fintype.equivOfCardEq (by simp [hF])
  let f : {x // x ∉ F} ≃ {x // x ∉ S} := Fintype.equivOfCardEq (by
    rw [Fintype.card_subtype_compl, Fintype.card_subtype_compl]; simp [hF])
  let τ : Equiv.Perm (Fin n) := Equiv.subtypeCongr e f
  have hin : ∀ j ∈ F, τ j ∈ S := fun j hj => by
    simp only [τ, Equiv.subtypeCongr, Equiv.trans_apply, Equiv.sumCompl_symm_apply_of_pos hj, Equiv.sumCongr_apply,
      Sum.map_inl, Equiv.sumCompl_apply_inl]; exact (e ⟨j, hj⟩).2
  have hout : ∀ j ∉ F, τ j ∉ S := fun j hj => by
    simp only [τ, Equiv.subtypeCongr, Equiv.trans_apply, Equiv.sumCompl_symm_apply_of_neg hj, Equiv.sumCongr_apply,
      Sum.map_inr, Equiv.sumCompl_apply_inr]; exact (f ⟨j, hj⟩).2
  have hmap : S.map τ.symm.toEmbedding = F := by
    apply eq_of_subset_of_card_le
    · intro j hj
      simp only [mem_map, Equiv.toEmbedding_apply] at hj
      obtain ⟨i, hi, rfl⟩ := hj
      by_contra h; exact hout _ h (by simpa using hi)
    · simp [hF]
  refine ⟨w n ∘ τ.symm, subset_convexHull ℝ _ ⟨τ.symm, rfl⟩, ?_⟩
  have := sum_map S τ.symm.toEmbedding (w n)
  simp only [Equiv.toEmbedding_apply] at this
  rw [Function.comp_def]; simp only; rw [← this, hmap, top, TauCeti.prefixSum_def]

/-- The face of `S`: the points of `P n` where the facet inequality of `S` is an equality. -/
def facet (S : Finset (Fin n)) : Set (Fin n → ℝ) := {x | x ∈ P n ∧ ∑ i ∈ S, x i = top n S.card}

/-- **Each face of `S` is an exposed face of the permutohedron.** -/
theorem facet_isExposed (S : Finset (Fin n)) : IsExposed ℝ (P n) (facet S) := by
  intro _
  let l : StrongDual ℝ (Fin n → ℝ) :=
    { toFun := fun x => ∑ i ∈ S, x i, map_add' := by intro x y; simp [sum_add_distrib],
      map_smul' := by intro c x; simp [mul_sum], cont := by fun_prop }
  refine ⟨l, ?_⟩
  ext x
  simp only [facet, Set.mem_ofPred_eq, l, ContinuousLinearMap.coe_mk', LinearMap.coe_mk, AddHom.coe_mk]
  constructor
  · rintro ⟨hx, heq⟩
    exact ⟨hx, fun y hy => heq ▸ sum_le_top hy S⟩
  · rintro ⟨hx, hmax⟩
    refine ⟨hx, le_antisymm (sum_le_top hx S) ?_⟩
    obtain ⟨y, hyP, hy⟩ := exists_top S
    exact hy ▸ hmax y hyP

end PermFaces
