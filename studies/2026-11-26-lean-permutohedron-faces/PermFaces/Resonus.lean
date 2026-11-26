/-
Step 7: the Resonus of the permutohedron (#120): the hyperplanes through the centre parallel to the facets, their number
`2^(n-1) - 1`, and which of them are Vacuus plates.
DICTO, with Claude (Anthropic). Built on PermFaces.FacetDim (`vectorSpan_facet`), PermFaces.PlateEq and PermFaces.Count.
-/
import PermFaces.Count

/-!
# The Resonus of the permutohedron (step 7)

The Resonus plane of the facet of `S` (`∅ ≠ S ≠ univ`) is the direction space of the facet, `vectorSpan ℝ (facet S) = dirs S`,
the vectors with sum `0` over `S` and over its complement. `resonusSet n` is the set of all of them.
* `dirs_eq_plateOf`: `dirs S` is the plate of the indicator of `S`; `dirs_eq_iff`: two facets have the same Resonus plane
  exactly when `S' = S` or `S' = Sᶜ` (parallel facets share one plane).
* `card_resonusSet`: there are `2^(n-1) - 1` Resonus planes; `resonus_three … resonus_eight`: `3, 7, 15, 31, 63, 127`.
* `facet_subset_vadd`, `resonus_parallel`: each facet lies in a translate of its Resonus plane, of dimension `n - 2`.
* `dirs_eq_plate_iff`: the Resonus plane of `S` is the Vacuus plate of a ridge exactly when the outer blocks of the ridge
  have equal size and `S` is the middle block or its complement.
* `card_resonus_inter_plate`, `card_resonus_diff_plate`: `#(middles n)` planes are both; `2^(n-1) - 1 - #(middles n)` Resonus
  planes are not Vacuus plates: none for odd `n ≥ 3` (`resonusSet_subset_plateSet_of_odd`), `2^(n-2)` for even `n ≥ 4`.
-/

open Finset
open scoped Pointwise

namespace PermFaces

variable {n : ℕ}

/-! ### The Resonus plane of a facet as a plate -/

/-- The indicator of `S`. -/
noncomputable def ind (S : Finset (Fin n)) : Fin n → ℝ := fun i => if i ∈ S then 1 else 0

theorem ind_of_mem {S : Finset (Fin n)} {i : Fin n} (h : i ∈ S) : ind S i = 1 := if_pos h

theorem ind_of_not_mem {S : Finset (Fin n)} {i : Fin n} (h : i ∉ S) : ind S i = 0 := if_neg h

theorem ind_eq_iff {S : Finset (Fin n)} {i j : Fin n} : ind S i = ind S j ↔ (i ∈ S ↔ j ∈ S) := by
  by_cases hi : i ∈ S <;> by_cases hj : j ∈ S <;> simp [ind, hi, hj]

/-- The directions of the facet of `S` form the plate of the indicator of `S`. -/
theorem dirs_eq_plateOf (S : Finset (Fin n)) : dirs S = VacuusResonus.plateOf (ind S) := by
  ext y
  have e : ∑ i, ind S i * y i = ∑ i ∈ S, y i := by
    simp only [ind, ite_mul, one_mul, zero_mul, sum_ite_mem, univ_inter]
  have c := sum_add_sum_compl S y
  rw [mem_dirs]
  simp only [VacuusResonus.plateOf, Submodule.mem_inf, LinearMap.mem_ker, VacuusResonus.dotL, LinearMap.coe_mk,
    AddHom.coe_mk, one_mul]
  rw [e]
  constructor
  · rintro ⟨h1, h2⟩; exact ⟨by linarith, h1⟩
  · rintro ⟨h1, h2⟩; exact ⟨h2, by linarith⟩

/-- A set and its complement give the same directions (opposite facets are parallel). -/
theorem dirs_compl (S : Finset (Fin n)) : dirs Sᶜ = dirs S := by
  ext y; rw [mem_dirs, mem_dirs, compl_compl]; exact and_comm

/-- **Parallel facets.** For `∅ ≠ S, S' ≠ univ`, the facets of `S` and `S'` have the same directions exactly when
`S' = S` or `S' = Sᶜ`. -/
theorem dirs_eq_iff {S S' : Finset (Fin n)} (hS : S.Nonempty) (hSc : Sᶜ.Nonempty) (hS' : S'.Nonempty)
    (hSc' : S'ᶜ.Nonempty) : dirs S = dirs S' ↔ S' = S ∨ S' = Sᶜ := by
  constructor
  · intro h
    obtain ⟨l, m, hlm⟩ : ∃ l m : ℝ, ∀ i, ind S' i = l * ind S i + m :=
      VacuusResonus.affine_of_plateOf_le (by rw [← dirs_eq_plateOf, ← dirs_eq_plateOf, h])
    have key : ∀ i j, (i ∈ S ↔ j ∈ S) → (i ∈ S' ↔ j ∈ S') := fun i j hij =>
      ind_eq_iff.1 (by rw [hlm i, hlm j, ind_eq_iff.2 hij])
    obtain ⟨i0, hi0⟩ := hS; obtain ⟨j0, hj0⟩ := hSc
    have hj0' : j0 ∉ S := mem_compl.1 hj0
    have kin : ∀ i, i ∈ S → (i ∈ S' ↔ i0 ∈ S') := fun i hi => key i i0 ⟨fun _ => hi0, fun _ => hi⟩
    have kout : ∀ i, i ∉ S → (i ∈ S' ↔ j0 ∈ S') := fun i hi =>
      key i j0 ⟨fun h => absurd h hi, fun h => absurd h hj0'⟩
    by_cases a : i0 ∈ S' <;> by_cases b : j0 ∈ S'
    · exfalso; obtain ⟨k, hk⟩ := hSc'
      apply mem_compl.1 hk
      by_cases c : k ∈ S
      · exact (kin k c).2 a
      · exact (kout k c).2 b
    · left; ext i
      by_cases c : i ∈ S
      · exact ⟨fun _ => c, fun _ => (kin i c).2 a⟩
      · exact ⟨fun h => absurd ((kout i c).1 h) b, fun h => absurd h c⟩
    · right; ext i; rw [mem_compl]
      by_cases c : i ∈ S
      · exact ⟨fun h => absurd ((kin i c).1 h) a, fun h => absurd c h⟩
      · exact ⟨fun _ => c, fun _ => (kout i c).2 b⟩
    · exfalso; obtain ⟨k, hk⟩ := hS'
      by_cases c : k ∈ S
      · exact a ((kin k c).1 hk)
      · exact b ((kout k c).1 hk)
  · rintro (rfl | rfl)
    · rfl
    · exact (dirs_compl S).symm

/-! ### The Resonus -/

/-- **The Resonus of the permutohedron**: the direction spaces of its facets (the hyperplanes of the sum-zero space through
the centre parallel to a facet), parallel facets sharing one. -/
def resonusSet (n : ℕ) : Set (Submodule ℝ (Fin n → ℝ)) :=
  {D | ∃ S : Finset (Fin n), S.Nonempty ∧ Sᶜ.Nonempty ∧ vectorSpan ℝ (facet S) = D}

theorem mem_resonusSet {D : Submodule ℝ (Fin n → ℝ)} :
    D ∈ resonusSet n ↔ ∃ S : Finset (Fin n), S.Nonempty ∧ Sᶜ.Nonempty ∧ dirs S = D := by
  constructor
  · rintro ⟨S, h1, h2, rfl⟩; exact ⟨S, h1, h2, (vectorSpan_facet h1 h2).symm⟩
  · rintro ⟨S, h1, h2, rfl⟩; exact ⟨S, h1, h2, vectorSpan_facet h1 h2⟩

/-- The same two facet statements for the two sets named in `dirs_eq_iff`, in terms of the facets themselves. -/
theorem vectorSpan_facet_eq_iff {S S' : Finset (Fin n)} (hS : S.Nonempty) (hSc : Sᶜ.Nonempty) (hS' : S'.Nonempty)
    (hSc' : S'ᶜ.Nonempty) : vectorSpan ℝ (facet S) = vectorSpan ℝ (facet S') ↔ S' = S ∨ S' = Sᶜ := by
  rw [vectorSpan_facet hS hSc, vectorSpan_facet hS' hSc']; exact dirs_eq_iff hS hSc hS' hSc'

/-- One set from each pair `{S, Sᶜ}`: the nonempty sets without the coordinate `z`. -/
def reps (z : Fin n) : Finset (Finset (Fin n)) := ((univ : Finset (Fin n)).erase z).powerset.erase ∅

theorem mem_reps {z : Fin n} {S : Finset (Fin n)} : S ∈ reps z ↔ S.Nonempty ∧ z ∉ S := by
  rw [reps, mem_erase, mem_powerset, nonempty_iff_ne_empty]
  refine and_congr_right fun _ =>
    ⟨fun h hz => (mem_erase.1 (h hz)).1 rfl, fun h i hi => mem_erase.2 ⟨fun e => ?_, mem_univ _⟩⟩
  rw [e] at hi; exact h hi

theorem card_reps (z : Fin n) : (reps z).card = 2 ^ (n - 1) - 1 := by
  have h0 : (∅ : Finset (Fin n)) ∈ ((univ : Finset (Fin n)).erase z).powerset := mem_powerset.2 (empty_subset _)
  rw [reps, card_erase_of_mem h0, card_powerset, card_erase_of_mem (mem_univ z), card_univ, Fintype.card_fin]

theorem resonusSet_eq (z : Fin n) : resonusSet n = dirs '' (↑(reps z) : Set (Finset (Fin n))) := by
  ext D
  rw [mem_resonusSet, Set.mem_image]
  constructor
  · rintro ⟨S, h1, h2, rfl⟩
    by_cases hz : z ∈ S
    · exact ⟨Sᶜ, mem_coe.2 (mem_reps.2 ⟨h2, fun h => (mem_compl.1 h) hz⟩), dirs_compl S⟩
    · exact ⟨S, mem_coe.2 (mem_reps.2 ⟨h1, hz⟩), rfl⟩
  · rintro ⟨S, hS, rfl⟩
    obtain ⟨h1, hz⟩ := mem_reps.1 (mem_coe.1 hS)
    exact ⟨S, h1, ⟨z, mem_compl.2 hz⟩, rfl⟩

theorem dirs_injOn_reps (z : Fin n) : Set.InjOn dirs (↑(reps z) : Set (Finset (Fin n))) := by
  intro S hS S' hS' e
  obtain ⟨h1, hz⟩ := mem_reps.1 (mem_coe.1 hS)
  obtain ⟨h1', hz'⟩ := mem_reps.1 (mem_coe.1 hS')
  rcases (dirs_eq_iff h1 ⟨z, mem_compl.2 hz⟩ h1' ⟨z, mem_compl.2 hz'⟩).1 e with h | h
  · exact h.symm
  · exfalso; rw [h] at hz'; exact hz' (mem_compl.2 hz)

/-- **The number of Resonus planes of the permutohedron is `2^(n-1) - 1`** (all `n`; the paper's range is `n ≥ 2`). -/
theorem card_resonusSet (n : ℕ) : (resonusSet n).ncard = 2 ^ (n - 1) - 1 := by
  rcases Nat.eq_zero_or_pos n with rfl | hn
  · have h : resonusSet 0 = ∅ := by
      ext D; simp only [Set.mem_empty_iff_false, iff_false]
      rintro ⟨S, ⟨i, -⟩, -⟩; exact i.elim0
    rw [h]; simp
  · classical
    have h : dirs '' (↑(reps (⟨0, hn⟩ : Fin n)) : Set (Finset (Fin n))) = ↑((reps (⟨0, hn⟩ : Fin n)).image dirs) :=
      (coe_image ..).symm
    rw [resonusSet_eq ⟨0, hn⟩, h, Set.ncard_coe_finset, card_image_of_injOn (dirs_injOn_reps _), card_reps]

theorem resonus_three : (resonusSet 3).ncard = 3 := (card_resonusSet 3).trans (by decide +kernel)
theorem resonus_four : (resonusSet 4).ncard = 7 := (card_resonusSet 4).trans (by decide +kernel)
theorem resonus_five : (resonusSet 5).ncard = 15 := (card_resonusSet 5).trans (by decide +kernel)
theorem resonus_six : (resonusSet 6).ncard = 31 := (card_resonusSet 6).trans (by decide +kernel)
theorem resonus_seven : (resonusSet 7).ncard = 63 := (card_resonusSet 7).trans (by decide +kernel)
theorem resonus_eight : (resonusSet 8).ncard = 127 := (card_resonusSet 8).trans (by decide +kernel)

/-! ### Each Resonus plane is parallel to its facet -/

theorem facet_nonempty (S : Finset (Fin n)) : (facet S).Nonempty := by
  obtain ⟨y, hy, h⟩ := exists_top S; exact ⟨y, hy, h⟩

/-- A facet lies in the translate of its direction space through any of its points. -/
theorem facet_subset_vadd {S : Finset (Fin n)} {x : Fin n → ℝ} (hx : x ∈ facet S) :
    facet S ⊆ x +ᵥ (vectorSpan ℝ (facet S) : Set (Fin n → ℝ)) := by
  intro y hy
  exact Set.mem_vadd_set.2 ⟨y - x, vsub_mem_vectorSpan ℝ hy hx, by simp⟩

/-- **Each Resonus plane is parallel to a facet**: it is `dirs S` for a facet `S`, the facet is nonempty and lies in the
translate of the plane through any of its points, and the plane has dimension `n - 2`. -/
theorem resonus_parallel {D : Submodule ℝ (Fin n → ℝ)} (hD : D ∈ resonusSet n) :
    ∃ S : Finset (Fin n), S.Nonempty ∧ Sᶜ.Nonempty ∧ D = dirs S ∧ (facet S).Nonempty ∧
      (∀ x ∈ facet S, facet S ⊆ x +ᵥ (D : Set (Fin n → ℝ))) ∧ Module.finrank ℝ D = n - 2 := by
  obtain ⟨S, h1, h2, rfl⟩ := hD
  exact ⟨S, h1, h2, vectorSpan_facet h1 h2, facet_nonempty S, fun x hx => facet_subset_vadd hx,
    finrank_vectorSpan_facet h1 h2⟩

theorem finrank_of_mem_resonusSet {D : Submodule ℝ (Fin n → ℝ)} (hD : D ∈ resonusSet n) :
    Module.finrank ℝ D = n - 2 := by
  obtain ⟨S, h1, h2, rfl⟩ := hD
  exact finrank_vectorSpan_facet h1 h2

theorem resonusSet_finite (n : ℕ) : (resonusSet n).Finite := by
  refine (Set.finite_range (dirs : Finset (Fin n) → Submodule ℝ (Fin n → ℝ))).subset ?_
  intro D hD
  obtain ⟨S, -, -, h⟩ := mem_resonusSet.1 hD
  exact ⟨S, h⟩

/-! ### Resonus planes and Vacuus plates -/

/-- The plate weight is `0` exactly on the middle block. -/
theorem wt_eq_zero_iff {key : Fin n → Fin 3} (hk : Function.Surjective key) (i : Fin n) :
    wt key i = 0 ↔ key i = 1 := by
  have q0 := mul_pos (sz_pos hk 2) (add_pos (sz_pos hk 0) (sz_pos hk 1))
  have q2 := mul_pos (sz_pos hk 0) (add_pos (sz_pos hk 1) (sz_pos hk 2))
  rcases fin3 (key i) with h | h | h
  · rw [(wt_of key i).1 h, h]; exact ⟨fun e => absurd e q0.ne', fun e => absurd e (by decide)⟩
  · rw [(wt_of key i).2.1 h, h]; exact ⟨fun _ => rfl, fun _ => rfl⟩
  · rw [(wt_of key i).2.2 h, h]; exact ⟨fun e => absurd e q2.ne', fun e => absurd e (by decide)⟩

/-- **When a Resonus plane is a Vacuus plate.** The direction space of the facet of `S` is the plate of the ridge with blocks
`B₁, B₂, B₃` exactly when `B₁` and `B₃` have equal size and `S` is the middle block `B₂` or its complement. -/
theorem dirs_eq_plate_iff {key : Fin n → Fin 3} (hk : Function.Surjective key) (S : Finset (Fin n)) :
    dirs S = plate key ↔ bc key 0 = bc key 2 ∧ (S = block key 1 ∨ S = (block key 1)ᶜ) := by
  have pa := sz_pos hk 0; have pb := sz_pos hk 1; have pc := sz_pos hk 2
  constructor
  · intro h
    obtain ⟨l, m, hlm⟩ : ∃ l m : ℝ, ∀ i, wt key i = l * ind S i + m :=
      VacuusResonus.affine_of_plateOf_le (by rw [← dirs_eq_plateOf, h, plate, permPlate_eq_plateOf_wt])
    obtain ⟨i0, g0⟩ := hk 0; obtain ⟨i1, g1⟩ := hk 1; obtain ⟨i2, g2⟩ := hk 2
    have w0 := (wt_of key i0).1 g0; have w1 := (wt_of key i1).2.1 g1; have w2 := (wt_of key i2).2.2 g2
    have same : ∀ i j, (i ∈ S ↔ j ∈ S) → wt key i = wt key j := fun i j hij => by
      rw [hlm i, hlm j, ind_eq_iff.2 hij]
    have n01 : ¬ (i0 ∈ S ↔ i1 ∈ S) := fun hh => by
      have e := same i0 i1 hh; rw [w0, w1] at e
      exact (mul_pos pc (add_pos pa pb)).ne' e
    have n12 : ¬ (i1 ∈ S ↔ i2 ∈ S) := fun hh => by
      have e := same i1 i2 hh; rw [w1, w2] at e
      exact (mul_pos pa (add_pos pb pc)).ne' e.symm
    have hl : l ≠ 0 := by
      intro hl0
      apply n01
      have e : wt key i0 = wt key i1 := by rw [hlm i0, hlm i1, hl0, zero_mul, zero_mul]
      rw [w0, w1] at e
      exact absurd e (mul_pos pc (add_pos pa pb)).ne'
    have diff : ∀ i j, wt key i = wt key j → (i ∈ S ↔ j ∈ S) := fun i j e => by
      rw [hlm i, hlm j] at e
      exact ind_eq_iff.1 (mul_left_cancel₀ hl (by linarith))
    have h02 : (i0 ∈ S ↔ i2 ∈ S) := by
      by_cases a : i0 ∈ S <;> by_cases b : i1 ∈ S <;> by_cases c : i2 ∈ S <;> simp_all
    have e02 := same i0 i2 h02; rw [w0, w2] at e02
    have hac : sz key 0 = sz key 2 := by
      have h3 : sz key 1 * (sz key 2 - sz key 0) = 0 := by linear_combination e02
      rcases mul_eq_zero.1 h3 with h4 | h4 <;> linarith
    have hac' : bc key 0 = bc key 2 := by
      have h5 : ((bc key 0 : ℕ) : ℝ) = ((bc key 2 : ℕ) : ℝ) := hac
      exact_mod_cast h5
    refine ⟨hac', ?_⟩
    have mid : ∀ i, (i ∈ S ↔ i1 ∈ S) ↔ key i = 1 := fun i => by
      rw [← wt_eq_zero_iff hk i]
      constructor
      · intro hh; rw [same i i1 hh, w1]
      · intro e; exact diff i i1 (by rw [e, w1])
    by_cases c : i1 ∈ S
    · left; ext i; rw [mem_block, ← mid i]
      exact ⟨fun hi => ⟨fun _ => c, fun _ => hi⟩, fun hh => hh.2 c⟩
    · right; ext i; rw [mem_compl, mem_block, ← mid i]
      exact ⟨fun hi hh => c (hh.1 hi), fun hh => by
        by_contra hi; exact hh ⟨fun h' => absurd h' hi, fun h' => absurd h' c⟩⟩
  · rintro ⟨hac', hS⟩
    have hac : sz key 0 = sz key 2 := by
      show ((bc key 0 : ℕ) : ℝ) = ((bc key 2 : ℕ) : ℝ); rw [hac']
    have main : dirs (block key 1) = plate key := by
      rw [dirs_eq_plateOf, plate, permPlate_eq_plateOf_wt]
      refine (plateOf_affine (l := -(sz key 2 * (sz key 0 + sz key 1))) (m := sz key 2 * (sz key 0 + sz key 1))
        (neg_ne_zero.2 (mul_pos pc (add_pos pa pb)).ne') fun i => ?_).symm
      rw [wt_two_level hac i]
      by_cases hi : key i = 1
      · rw [if_pos hi, ind_of_mem (mem_block.2 hi)]; ring
      · rw [if_neg hi, ind_of_not_mem (fun h' => hi (mem_block.1 h'))]; ring
    rcases hS with rfl | rfl
    · exact main
    · rw [dirs_compl]; exact main

/-- **The Vacuus plates that are Resonus planes** are those of the ridges whose outer blocks have equal size. -/
theorem plate_mem_resonusSet_iff {key : Fin n → Fin 3} (hk : Function.Surjective key) :
    plate key ∈ resonusSet n ↔ bc key 0 = bc key 2 := by
  rw [mem_resonusSet]
  constructor
  · rintro ⟨S, -, -, h⟩; exact ((dirs_eq_plate_iff hk S).1 h).1
  · intro h
    obtain ⟨i1, g1⟩ := hk 1; obtain ⟨i0, g0⟩ := hk 0
    refine ⟨block key 1, ⟨i1, mem_block.2 g1⟩, ⟨i0, mem_compl.2 fun h' => ?_⟩,
      (dirs_eq_plate_iff hk _).2 ⟨h, Or.inl rfl⟩⟩
    have h2 := mem_block.1 h'; rw [g0] at h2; exact absurd h2 (by decide)

theorem resonus_inter_plate (n : ℕ) :
    resonusSet n ∩ plateSet n = plate '' (↑(keysEq n) : Set (Fin n → Fin 3)) := by
  ext D
  constructor
  · rintro ⟨hR, key, hk, rfl⟩
    exact ⟨key, mem_coe.2 (mem_keysEq.2 ⟨hk, (plate_mem_resonusSet_iff hk).1 hR⟩), rfl⟩
  · rintro ⟨key, hk, rfl⟩
    obtain ⟨hs, he⟩ := mem_keysEq.1 (mem_coe.1 hk)
    exact ⟨(plate_mem_resonusSet_iff hs).2 he, key, hs, rfl⟩

/-- **The number of planes that are both a Resonus plane and a Vacuus plate** is the number of middle-block classes. -/
theorem card_resonus_inter_plate (n : ℕ) : (resonusSet n ∩ plateSet n).ncard = (middles n).card := by
  classical
  have h : plate '' (↑(keysEq n) : Set (Fin n → Fin 3)) = ↑((keysEq n).image plate) := (coe_image ..).symm
  rw [resonus_inter_plate, h, Set.ncard_coe_finset,
    card_image_eq_of_iff (keysEq n) plate (fun key => canonMiddle (block key 1))
      (fun x hx y hy => plate_eq_iff_canon hx hy), image_canonMiddle]

/-- **The number of Resonus planes that are not Vacuus plates.** -/
theorem card_resonus_diff_plate (n : ℕ) :
    (resonusSet n \ plateSet n).ncard = 2 ^ (n - 1) - 1 - (middles n).card := by
  have h := Set.ncard_inter_add_ncard_sdiff_eq_ncard (resonusSet n) (plateSet n) (resonusSet_finite n)
  rw [card_resonus_inter_plate, card_resonusSet] at h
  rw [← h, Nat.add_sub_cancel_left]

/-- **`n` odd: every Resonus plane is a Vacuus plate.** -/
theorem resonusSet_subset_plateSet_of_odd (hn : 3 ≤ n) (ho : ¬ Even n) : resonusSet n ⊆ plateSet n := by
  have h := card_resonus_diff_plate n
  rw [card_middles_odd hn ho, Nat.sub_self] at h
  exact Set.diff_eq_empty.1 ((Set.ncard_eq_zero ((resonusSet_finite n).subset Set.diff_subset)).1 h)

/-- **`n` even: exactly `2^(n-2)` Resonus planes are not Vacuus plates** (and `2^(n-2) - 1` are). -/
theorem card_resonus_diff_plate_even (hn : 3 ≤ n) (he : Even n) :
    (resonusSet n \ plateSet n).ncard = 2 ^ (n - 2) := by
  rw [card_resonus_diff_plate, card_middles_even hn he]
  have e : 2 ^ (n - 1) = 2 * 2 ^ (n - 2) := by
    rw [← pow_succ']; congr 1; omega
  have p : 0 < 2 ^ (n - 2) := Nat.two_pow_pos _
  rw [e]; omega

end PermFaces
