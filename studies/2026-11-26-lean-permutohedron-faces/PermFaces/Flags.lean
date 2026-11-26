/-
Every face of the permutohedron given by an ordered set partition (step 3, general form; 26 Nov 2026).
DICTO, with Claude (Anthropic). Built on TauCeti (Rado's theorem) and PermFaces.Facets / FacetDim.
-/
import PermFaces.FacetDim

/-!
# Faces of the permutohedron from ordered set partitions

An ordered set partition of the coordinates into `m` nonempty blocks is a surjective `key : Fin n → Fin m` (`key i` = the
block of `i`). Its face is the set of points of `P n` for which, for every `t`, the coordinates in blocks `≤ t` sum to the
largest possible value `top n |{i | key i ≤ t}|`.
* `exists_vertex_flag`: a corner of `P n` lies on it (sort the coordinates by block).
* `flagFace_isExposed`: it is an exposed face of `P n`.
* `vectorSpan_flagFace`: its directions are the vectors summing to `0` on every block.
* `finrank_vectorSpan_flagFace`: **its dimension is `n - m`.** (Facets: `m = 2`, dimension `n - 2`; ridges: `m = 3`,
  dimension `n - 3`; corners: `m = n`.)
-/

open Finset

namespace PermFaces

variable {n m : ℕ}

/-- The coordinates in blocks `≤ t`. -/
def low (key : Fin n → Fin m) (t : ℕ) : Finset (Fin n) := univ.filter fun i => (key i : ℕ) ≤ t

/-- The coordinates in block `b`. -/
def block (key : Fin n → Fin m) (b : Fin m) : Finset (Fin n) := univ.filter fun i => key i = b

/-- The face of the ordered set partition `key`. -/
def flagFace (key : Fin n → Fin m) : Set (Fin n → ℝ) :=
  {x | x ∈ P n ∧ ∀ t : Fin m, ∑ i ∈ low key t, x i = top n (low key t).card}

/-- A downward-closed set of positions is an initial segment. -/
theorem eq_initial_of_down {A : Finset (Fin n)} (hA : ∀ j ∈ A, ∀ j' : Fin n, j' ≤ j → j' ∈ A) :
    A = univ.filter fun j : Fin n => (j : ℕ) < A.card := by
  ext j
  simp only [mem_filter, mem_univ, true_and]
  constructor
  · intro hj
    have hsub : (univ.filter fun j' : Fin n => j' ≤ j) ⊆ A := fun j' hj' => hA j hj j' (by simpa using hj')
    have := card_le_card hsub
    have hc : (univ.filter fun j' : Fin n => j' ≤ j).card = (j : ℕ) + 1 := by
      rw [← Fin.card_Iic]; congr 1; ext; simp
    omega
  · intro hlt
    by_contra hj
    have hsub : A ⊆ univ.filter fun j' : Fin n => j' < j := by
      intro a ha; simp only [mem_filter, mem_univ, true_and]
      by_contra hge; push_neg at hge; exact hj (hA a ha j hge)
    have := card_le_card hsub
    have hc : (univ.filter fun j' : Fin n => j' < j).card = (j : ℕ) := by
      rw [← Fin.card_Iio]; congr 1; ext; simp
    omega

/-- **A corner on the face**: sort the coordinates by block. -/
theorem exists_vertex_flag (key : Fin n → Fin m) :
    ∃ π : Equiv.Perm (Fin n), ∀ t : ℕ, ∑ i ∈ low key t, (w n ∘ π) i = top n (low key t).card := by
  classical
  set σ := Tuple.sort (fun i => (key i : ℕ))
  have hmono : Monotone ((fun i => (key i : ℕ)) ∘ σ) := Tuple.monotone_sort _
  refine ⟨σ.symm, fun t => ?_⟩
  set A := (low key t).map σ.symm.toEmbedding
  have hdown : ∀ j ∈ A, ∀ j' : Fin n, j' ≤ j → j' ∈ A := by
    intro j hj j' hle
    simp only [A, mem_map, Equiv.toEmbedding_apply, low, mem_filter, mem_univ, true_and] at hj ⊢
    obtain ⟨i, hi, rfl⟩ := hj
    refine ⟨σ j', ?_, by simp⟩
    have := hmono hle
    simp only [Function.comp_apply, Equiv.apply_symm_apply] at this
    omega
  have hA := eq_initial_of_down hdown
  have hcard : A.card = (low key t).card := card_map _
  have := sum_map (low key t) σ.symm.toEmbedding (w n)
  simp only [Equiv.toEmbedding_apply] at this
  simp only [Function.comp_apply]
  rw [← this, top, TauCeti.prefixSum_def, ← hcard]
  conv_lhs => rw [show (low key t).map σ.symm.toEmbedding = A from rfl, hA]

/-- **The face of an ordered set partition is an exposed face of the permutohedron.** -/
theorem flagFace_isExposed (key : Fin n → Fin m) : IsExposed ℝ (P n) (flagFace key) := by
  classical
  intro _
  let l : StrongDual ℝ (Fin n → ℝ) :=
    { toFun := fun x => ∑ t : Fin m, ∑ i ∈ low key t, x i,
      map_add' := by intro x y; simp [sum_add_distrib],
      map_smul' := by intro c x; simp [mul_sum], cont := by fun_prop }
  refine ⟨l, ?_⟩
  obtain ⟨π, hπ⟩ := exists_vertex_flag key
  have hvP : w n ∘ π ∈ P n := subset_convexHull ℝ _ ⟨π, rfl⟩
  ext x
  simp only [flagFace, Set.mem_ofPred_eq, l, ContinuousLinearMap.coe_mk', LinearMap.coe_mk, AddHom.coe_mk]
  constructor
  · rintro ⟨hx, heq⟩
    refine ⟨hx, fun y hy => ?_⟩
    rw [sum_congr rfl (fun t _ => heq t)]
    exact sum_le_sum fun t _ => sum_le_top hy _
  · rintro ⟨hx, hmax⟩
    refine ⟨hx, fun t => ?_⟩
    have hle : ∀ s ∈ (univ : Finset (Fin m)), ∑ i ∈ low key s, x i ≤ top n (low key s).card :=
      fun s _ => sum_le_top hx _
    have hge : ∑ s : Fin m, top n (low key s).card ≤ ∑ s : Fin m, ∑ i ∈ low key s, x i := by
      exact (sum_congr rfl (fun (s : Fin m) _ => (hπ (s : ℕ)).symm)).le.trans (hmax _ hvP)
    exact (sum_eq_sum_iff_of_le hle).1 (le_antisymm (sum_le_sum hle) hge) t (mem_univ t)

/-- The predicted directions: sum `0` on every block. -/
def blockL (key : Fin n → Fin m) : (Fin n → ℝ) →ₗ[ℝ] (Fin m → ℝ) where
  toFun v b := ∑ i ∈ block key b, v i
  map_add' x y := by ext b; simp [sum_add_distrib]
  map_smul' c x := by ext b; simp [mul_sum]

theorem mem_ker_blockL {key : Fin n → Fin m} {v : Fin n → ℝ} :
    v ∈ LinearMap.ker (blockL key) ↔ ∀ b, ∑ i ∈ block key b, v i = 0 := by
  simp [blockL, funext_iff]

/-- Sum over blocks `≤ t` splits as the sum over blocks `< t` plus block `t`. -/
theorem sum_low_eq (key : Fin n → Fin m) (b : Fin m) (v : Fin n → ℝ) :
    ∑ i ∈ low key b, v i = ∑ i ∈ low key b with (key i : ℕ) < b, v i + ∑ i ∈ block key b, v i := by
  classical
  rw [← sum_filter_add_sum_filter_not (low key b) (fun i => (key i : ℕ) < b)]
  congr 1
  apply sum_congr _ (fun _ _ => rfl)
  ext i; simp only [low, block, mem_filter, mem_univ, true_and, not_lt]
  constructor
  · rintro ⟨h1, h2⟩; exact Fin.ext (by omega)
  · rintro rfl; omega

/-- Directions of the face lie in the kernel of the block sums. -/
theorem vectorSpan_flagFace_le (key : Fin n → Fin m) :
    vectorSpan ℝ (flagFace key) ≤ LinearMap.ker (blockL key) := by
  classical
  rw [vectorSpan_def, Submodule.span_le]
  rintro _ ⟨x, ⟨hx, hxS⟩, y, ⟨hy, hyS⟩, rfl⟩
  rw [SetLike.mem_coe, mem_ker_blockL]
  -- every chain sum of x - y vanishes
  have hz : ∀ t : ℕ, ∑ i ∈ low key t, (x - y) i = 0 := by
    intro t
    by_cases ht : t < m
    · have := hxS ⟨t, ht⟩; have := hyS ⟨t, ht⟩
      simp only [Pi.sub_apply, sum_sub_distrib]; simp_all
    · have hlow : low key t = univ := by
        ext i; simp only [low, mem_filter, mem_univ, true_and, iff_true]; have := (key i).isLt; omega
      have tx := TauCeti.sum_eq_of_mem_convexHull_range_comp_perm hx
      have ty := TauCeti.sum_eq_of_mem_convexHull_range_comp_perm hy
      simp only [hlow, Pi.sub_apply, sum_sub_distrib, vsub_eq_sub] at *; linarith
  intro b
  have hb := sum_low_eq key b (x -ᵥ y)
  rcases Nat.eq_zero_or_pos (b : ℕ) with h0 | hpos
  · have hempty : (low key b).filter (fun i => (key i : ℕ) < b) = ∅ := by
      ext i; simp [low, h0]
    rw [hempty, sum_empty, zero_add] at hb
    rw [← hb]; exact hz b
  · have hprev : (low key b).filter (fun i => (key i : ℕ) < b) = low key ((b : ℕ) - 1) := by
      ext i; simp only [low, mem_filter, mem_univ, true_and]; omega
    rw [hprev] at hb
    have h1 := hz b; have h2 := hz ((b : ℕ) - 1)
    simp only [vsub_eq_sub] at hb ⊢
    linarith

/-- `eᵢ - eⱼ` is a direction of the face when `i, j` share a block. -/
theorem single_sub_mem_flag {key : Fin n → Fin m} {i j : Fin n} (hij : i ≠ j) (hk : key i = key j) :
    (Pi.single i 1 - Pi.single j 1 : Fin n → ℝ) ∈ vectorSpan ℝ (flagFace key) := by
  classical
  obtain ⟨π, hπ⟩ := exists_vertex_flag key
  set y : Fin n → ℝ := w n ∘ π
  have hyP : y ∈ P n := subset_convexHull ℝ _ ⟨π, rfl⟩
  set s := Equiv.swap i j
  have hys : y ∘ s ∈ P n := (Equiv.Perm.comp_perm_mem_convexHull_range_comp_perm_iff s).2 hyP
  have hkey : ∀ k, key (s k) = key k := by
    intro k
    rcases eq_or_ne k i with rfl | hki
    · simp [s, Equiv.swap_apply_left, hk]
    rcases eq_or_ne k j with rfl | hkj
    · simp [s, Equiv.swap_apply_right, hk]
    simp [s, Equiv.swap_apply_of_ne_of_ne hki hkj]
  have hmap : ∀ t, (low key t).map s.toEmbedding = low key t := by
    intro t; ext k; simp only [mem_map, Equiv.toEmbedding_apply, low, mem_filter, mem_univ, true_and]
    constructor
    · rintro ⟨a, ha, rfl⟩; rwa [hkey]
    · intro hk'; exact ⟨s k, by rwa [hkey], by simp [s]⟩
  have hsum : ∀ t, ∑ k ∈ low key t, (y ∘ s) k = ∑ k ∈ low key t, y k := by
    intro t
    calc ∑ k ∈ low key t, (y ∘ s) k = ∑ k ∈ (low key t).map s.toEmbedding, y k := by rw [sum_map]; rfl
      _ = ∑ k ∈ low key t, y k := by rw [hmap]
  have h1 : y ∈ flagFace key := ⟨hyP, fun t => hπ t⟩
  have h2 : y ∘ s ∈ flagFace key := ⟨hys, fun t => (hsum t).trans (hπ t)⟩
  have hd : y -ᵥ y ∘ s = (y i - y j) • (Pi.single i 1 - Pi.single j 1 : Fin n → ℝ) := by
    funext k
    simp only [vsub_eq_sub, Pi.sub_apply, Function.comp_apply, Pi.smul_apply, smul_eq_mul]
    rcases eq_or_ne k i with rfl | hki
    · simp [s, Equiv.swap_apply_left, hij]
    rcases eq_or_ne k j with rfl | hkj
    · simp [s, Equiv.swap_apply_right, hij.symm]
    simp [s, Equiv.swap_apply_of_ne_of_ne hki hkj, hki, hkj]
  have hne : y i - y j ≠ 0 := sub_ne_zero.2 (fun h => hij (π.injective (w_injective h)))
  have := Submodule.smul_mem _ (y i - y j)⁻¹ (vsub_mem_vectorSpan ℝ h1 h2)
  rwa [hd, smul_smul, inv_mul_cancel₀ hne, one_smul] at this

/-- **The directions of the face** of an ordered set partition into nonempty blocks. -/
theorem vectorSpan_flagFace {key : Fin n → Fin m} (hkey : Function.Surjective key) :
    vectorSpan ℝ (flagFace key) = LinearMap.ker (blockL key) := by
  classical
  refine le_antisymm (vectorSpan_flagFace_le key) ?_
  choose rep hrep using hkey
  intro v hv
  rw [mem_ker_blockL] at hv
  have hrepr : v = ∑ i, v i • (Pi.single i 1 - Pi.single (rep (key i)) 1 : Fin n → ℝ) := by
    funext k
    simp only [Finset.sum_apply, Pi.smul_apply, Pi.sub_apply, smul_eq_mul, mul_sub, sum_sub_distrib, Pi.single_apply,
      mul_ite, mul_one, mul_zero, sum_ite_eq', mem_univ, if_true]
    have : ∑ i, (if k = rep (key i) then v i else 0) = 0 := by
      by_cases hk : ∃ b, rep b = k
      · obtain ⟨b, rfl⟩ := hk
        have hinj : ∀ i, (rep b = rep (key i) ↔ key i = b) := fun i =>
          ⟨fun h => by have := congrArg key h; rw [hrep, hrep] at this; exact this.symm, fun h => by rw [h]⟩
        simp only [hinj]; rw [← sum_filter]; exact hv b
      · push_neg at hk
        exact sum_eq_zero fun i _ => by rw [if_neg (fun h => hk _ h.symm)]
    rw [this, sub_zero, Finset.sum_ite_eq]; simp
  rw [hrepr]
  refine Submodule.sum_mem _ fun i _ => ?_
  rcases eq_or_ne i (rep (key i)) with h | h
  · rw [← h, sub_self, smul_zero]; exact Submodule.zero_mem _
  · exact Submodule.smul_mem _ _ (single_sub_mem_flag h (hrep _).symm)

/-- **The face of an ordered set partition into `m` nonempty blocks has dimension `n - m`.** -/
theorem finrank_vectorSpan_flagFace {key : Fin n → Fin m} (hkey : Function.Surjective key) :
    Module.finrank ℝ (vectorSpan ℝ (flagFace key)) = n - m := by
  classical
  rw [vectorSpan_flagFace hkey]
  choose rep hrep using hkey
  have hsurj : LinearMap.range (blockL key) = ⊤ := by
    rw [LinearMap.range_eq_top]
    intro c
    refine ⟨∑ b, c b • Pi.single (rep b) 1, ?_⟩
    ext b
    simp only [blockL, LinearMap.coe_mk, AddHom.coe_mk, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.single_apply,
      mul_ite, mul_one, mul_zero]
    rw [sum_comm]
    rw [sum_eq_single b]
    · rw [sum_ite_eq']; simp [block, hrep]
    · intro b' _ hb'
      apply sum_eq_zero; intro i hi
      simp only [block, mem_filter, mem_univ, true_and] at hi
      rw [if_neg]; intro h; apply hb'; rw [← hrep b', ← h, hi]
    · simp
  have := LinearMap.finrank_range_add_finrank_ker (blockL key)
  rw [hsurj, finrank_top, Module.finrank_fin_fun, Module.finrank_fin_fun] at this
  omega

end PermFaces
