/-
Lean study 9 of the shape-language canon (DICTO, 19 Nov 2026), part AC: volumes.

* `volume_iUnion_poly`, `volume_eq_of_scissorsCongruent`: **scissors congruence keeps volume** (study 2's
  definition: convex pieces with disjoint interiors; a convex set has a boundary of volume zero).
* `volume_similarCopy`: a similar copy at scale `a` has `a³` times the volume.
* `volume_oct`: the octahedron |x| + |y| + |z| ≤ 1 has volume 4/3.
* `volume_tetra`: the regular tetrahedron of study 3 (corners (1, 1, −1), (1, −1, 1), (−1, 1, 1),
  (−1, −1, −1), edge 2√2) has volume 8/3.
* `volume_co`: the cube ∩ octahedron solid `coSet t` (1 ≤ t < 2) has volume (4/3)(t³ − 3(t − 1)³).

Method. Mathlib gives the volume of the ball of the sum norm (`volume_sum_rpow_le`, `volume_sum_rpow_lt`,
from the Gamma function): (4/3) r³ in 3-space. Everything else is cut from it:
- reflecting one coordinate keeps volume (`measurePreserving_pi` with `Measure.measurePreserving_neg`), and a
  coordinate plane has volume zero (`Measure.pi_hyperplane`), so a set symmetric in one coordinate has half its
  volume on each side (`vol_half`); three halvings give the corner simplex {u ≥ 0, u₀ + u₁ + u₂ < 2}: 4/3;
- the octahedron is the ball of radius 1;
- the cube ∩ octahedron solid is the ball of radius t less six caps {x_i > 1} (t < 2: the caps are disjoint);
  each cap is a translate of half a ball of radius t − 1;
- the tetrahedron is the cube [−1, 1]³ less four corner simplices (each the corner simplex above, moved by
  x ↦ (1 − v_i x_i)).
The sets of 3-space (`EuclideanSpace ℝ (Fin 3)`) are moved to `Fin 3 → ℝ` by `PiLp.volume_preserving_ofLp`.

Credits: Mathlib `MeasureTheory.volume_sum_rpow_le`, `MeasureTheory.volume_sum_rpow_lt` (volume of the ℓᵖ
ball), `Real.Gamma_two`, `Real.Gamma_nat_eq_factorial`, `Measure.pi_hyperplane`, `measurePreserving_pi`,
`Measure.measurePreserving_neg`, `Measure.measurePreserving_sub_left`, `measurePreserving_add_left`,
`measure_preimage_add_right`, `Real.volume_Icc_pi`, `PiLp.volume_preserving_ofLp`, `measure_iUnion`,
`measure_inter_add_sdiff`, `Convex.addHaar_frontier` (the boundary of a convex set is null),
`LinearIsometryEquiv.measurePreserving`, `Measure.addHaar_smul`, `AffineIsometryEquiv.map_vadd`.
No `sorry`.
-/
import DehnCanon.Dehn8Cross

open scoped RealInnerProductSpace Real Pointwise
open Set MeasureTheory Measure Module

namespace DehnCanon

/-! ### Scissors congruence keeps volume -/

lemma vol_eq_of_sub_null {X : Type*} [MeasurableSpace X] {μ : Measure X} {s t z : Set X}
    (h1 : s ⊆ t) (h2 : t ⊆ s ∪ z) (hz : μ z = 0) : μ s = μ t :=
  le_antisymm (measure_mono h1)
    ((measure_mono h2).trans ((measure_union_le _ _).trans (by rw [hz, add_zero])))

/-- **Volume is additive over a dissection into convex polytopes** (pairwise disjoint interiors). -/
theorem volume_iUnion_poly {κ : Type} [Fintype κ] {p : κ → Set R3} (hp : ∀ k, IsPoly (p k))
    (hd : Pairwise fun i j => Disjoint (interior (p i)) (interior (p j))) :
    volume (⋃ k, p k) = ∑ k, volume (p k) := by
  have hfr : ∀ k, volume (frontier (p k)) = 0 := fun k => Convex.addHaar_frontier volume (hp k).convex
  have hsub : ∀ k, p k ⊆ interior (p k) ∪ frontier (p k) := fun k =>
    subset_closure.trans (closure_eq_interior_union_frontier (p k)).subset
  have hint : ∀ k, volume (interior (p k)) = volume (p k) := fun k =>
    vol_eq_of_sub_null interior_subset (hsub k) (hfr k)
  have hU : volume (⋃ k, interior (p k)) = ∑ k, volume (interior (p k)) := by
    rw [measure_iUnion (fun i j hij => hd hij) (fun k => isOpen_interior.measurableSet), tsum_fintype]
  rw [← vol_eq_of_sub_null (iUnion_mono fun k => interior_subset)
    (t := ⋃ k, p k) (z := ⋃ k, frontier (p k)) ?_ (measure_iUnion_null hfr), hU]
  · exact Finset.sum_congr rfl fun k _ => hint k
  · intro x hx
    obtain ⟨k, hk⟩ := mem_iUnion.1 hx
    rcases hsub k hk with h | h
    · exact Or.inl (mem_iUnion.2 ⟨k, h⟩)
    · exact Or.inr (mem_iUnion.2 ⟨k, h⟩)

/-- An isometry of 3-space keeps volume. -/
lemma volume_image_isometry (g : R3 ≃ᵃⁱ[ℝ] R3) (s : Set R3) : volume (g '' s) = volume s := by
  set L := g.linearIsometryEquiv
  have hg : ∀ x, g x = L x + g 0 := by
    intro x
    have := g.map_vadd (0 : R3) x
    rw [vadd_eq_add, vadd_eq_add, add_zero] at this
    exact this
  have himg : g '' s = (fun y => y + g 0) '' (L '' s) := by
    rw [Set.image_image]; exact Set.image_congr (fun x _ => hg x)
  rw [himg, Set.image_add_right, measure_preimage_add_right, L.image_eq_preimage_symm]
  exact (L.symm.measurePreserving).measure_preimage_equiv (f := L.symm.toMeasurableEquiv) s

/-- **Scissors-congruent sets have the same volume.** -/
theorem volume_eq_of_scissorsCongruent {P Q : Set R3} (h : ScissorsCongruent P Q) :
    volume P = volume Q := by
  obtain ⟨κ, _, p, g, hp, hUP, hdP, hUQ, hdQ⟩ := h
  rw [← hUP, ← hUQ, volume_iUnion_poly hp hdP,
    volume_iUnion_poly (fun k => (hp k).image (g k)) hdQ]
  exact Finset.sum_congr rfl fun k _ => (volume_image_isometry (g k) (p k)).symm

/-- A copy scaled by `a > 0` and moved by an isometry has `a³` times the volume. -/
lemma volume_similar {a : ℝ} (ha : 0 < a) (g : R3 ≃ᵃⁱ[ℝ] R3) (P : Set R3) :
    volume (g '' (a • P)) = ENNReal.ofReal (a ^ 3) * volume P := by
  rw [volume_image_isometry, Measure.addHaar_smul, finrank_euclideanSpace_fin,
    abs_of_pos (pow_pos ha 3)]

/-! ### Volumes in `Fin 3 → ℝ` -/

/-- The sum norm |y₀| + |y₁| + |y₂|. -/
def l1 (y : Fin 3 → ℝ) : ℝ := |y 0| + |y 1| + |y 2|

lemma continuous_l1 : Continuous l1 := by unfold l1; fun_prop

lemma plane_null (i : Fin 3) (c : ℝ) : volume {y : Fin 3 → ℝ | y i = c} = 0 := by
  rw [volume_pi]; exact Measure.pi_hyperplane (fun _ : Fin 3 => (volume : Measure ℝ)) i c

lemma l1_rpow (y : Fin 3 → ℝ) : (∑ i, |y i| ^ (1 : ℝ)) ^ (1 / (1 : ℝ)) = l1 y := by
  simp [Real.rpow_one, Fin.sum_univ_three, l1]

lemma gamma_four : Real.Gamma 4 = 6 := by
  rw [show (4 : ℝ) = ((3 : ℕ) : ℝ) + 1 by norm_num, Real.Gamma_nat_eq_factorial]
  norm_num [Nat.factorial]

/-- The closed ball of the sum norm: (4/3) r³ (Mathlib's ℓᵖ ball with p = 1). -/
lemma vol_l1_le {r : ℝ} (hr : 0 ≤ r) :
    volume {y : Fin 3 → ℝ | l1 y ≤ r} = ENNReal.ofReal (4 / 3 * r ^ 3) := by
  have h := MeasureTheory.volume_sum_rpow_le (Fin 3) (p := 1) le_rfl r
  simp only [l1_rpow, Fintype.card_fin] at h
  rw [h, ← ENNReal.ofReal_pow hr, ← ENNReal.ofReal_mul (by positivity)]
  congr 1
  norm_num [Real.Gamma_two, gamma_four]
  ring

/-- The open ball of the sum norm: (4/3) r³. -/
lemma vol_l1_lt {r : ℝ} (hr : 0 ≤ r) :
    volume {y : Fin 3 → ℝ | l1 y < r} = ENNReal.ofReal (4 / 3 * r ^ 3) := by
  have h := MeasureTheory.volume_sum_rpow_lt (Fin 3) (p := 1) le_rfl r
  simp only [l1_rpow, Fintype.card_fin] at h
  rw [h, ← ENNReal.ofReal_pow hr, ← ENNReal.ofReal_mul (by positivity)]
  congr 1
  norm_num [Real.Gamma_two, gamma_four]
  ring

/-- Reflection in the coordinate plane `y i = 0`. -/
def refl (i : Fin 3) (y : Fin 3 → ℝ) : Fin 3 → ℝ := fun j => if j = i then -y j else y j

lemma mp_refl (i : Fin 3) : MeasurePreserving (refl i) := by
  have h := measurePreserving_pi (fun _ : Fin 3 => (volume : Measure ℝ)) (fun _ => volume)
    (f := fun j => if j = i then (Neg.neg : ℝ → ℝ) else id)
    (fun j => by
      split_ifs
      · exact Measure.measurePreserving_neg _
      · exact MeasurePreserving.id _)
  have he : refl i = fun a j => (if j = i then (Neg.neg : ℝ → ℝ) else id) (a j) := by
    funext y j; unfold refl; split_ifs <;> rfl
  rw [he, volume_pi]; exact h

/-- **Half by symmetry.** A measurable set symmetric in the coordinate `i` has half its volume where
`y i > 0`. -/
lemma vol_half (i : Fin 3) {S : Set (Fin 3 → ℝ)} (hS : MeasurableSet S)
    (hinv : ∀ y, refl i y ∈ S ↔ y ∈ S) :
    2 * volume (S ∩ {y | 0 < y i}) = volume S := by
  have hm : MeasurableSet {y : Fin 3 → ℝ | 0 < y i} :=
    measurableSet_lt measurable_const (measurable_pi_apply i)
  have h1 := measure_inter_add_sdiff (μ := volume) S hm
  have hneg : refl i ⁻¹' (S ∩ {y | 0 < y i}) = S ∩ {y | y i < 0} := by
    ext y; simp [refl, hinv]
  have h2 : volume (S ∩ {y | y i < 0}) = volume (S ∩ {y | 0 < y i}) := by
    rw [← hneg]; exact (mp_refl i).measure_preimage (hS.inter hm).nullMeasurableSet
  have h3 : volume (S ∩ {y | y i < 0}) = volume (S \ {y | 0 < y i}) := by
    apply vol_eq_of_sub_null (z := {y | y i = 0})
    · intro y hy
      simp only [mem_inter_iff, mem_sdiff, mem_ofPred_eq] at hy ⊢
      exact ⟨hy.1, fun h => lt_asymm hy.2 h⟩
    · intro y hy
      simp only [mem_sdiff, mem_ofPred_eq, not_lt] at hy
      rcases lt_or_eq_of_le hy.2 with h | h
      · exact Or.inl ⟨hy.1, h⟩
      · exact Or.inr h
    · exact plane_null i 0
  rw [← h1, ← h3, h2, two_mul]

lemma l1_refl (i : Fin 3) (y : Fin 3 → ℝ) : l1 (refl i y) = l1 y := by
  fin_cases i <;> simp [l1, refl]

lemma refl_apply_ne {i j : Fin 3} (h : j ≠ i) (y : Fin 3 → ℝ) : refl i y j = y j := by
  simp [refl, h]

lemma refl_apply_self (i : Fin 3) (y : Fin 3 → ℝ) : refl i y i = -y i := by
  simp [refl]

lemma ennreal_half {x : ENNReal} {c : ℝ} (_hc : 0 ≤ c) (h : 2 * x = ENNReal.ofReal (2 * c)) :
    x = ENNReal.ofReal c := by
  rw [ENNReal.ofReal_mul (by norm_num), ENNReal.ofReal_ofNat] at h
  exact (ENNReal.mul_right_inj (by norm_num) (by norm_num)).1 h

/-- Half a closed ball: {y i > 0, l1 y ≤ r} has volume (2/3) r³. -/
lemma vol_halfBall (i : Fin 3) {r : ℝ} (hr : 0 ≤ r) :
    volume ({y : Fin 3 → ℝ | l1 y ≤ r} ∩ {y | 0 < y i}) = ENNReal.ofReal (2 / 3 * r ^ 3) := by
  apply ennreal_half (by positivity)
  rw [vol_half i (measurableSet_le continuous_l1.measurable measurable_const)
    (fun y => by simp [l1_refl]), vol_l1_le hr]
  ring_nf

/-- **The corner simplex** {u ≥ 0, u₀ + u₁ + u₂ < 2} has volume 4/3. -/
lemma vol_corner :
    volume {u : Fin 3 → ℝ | 0 ≤ u 0 ∧ 0 ≤ u 1 ∧ 0 ≤ u 2 ∧ u 0 + u 1 + u 2 < 2} =
      ENNReal.ofReal (4 / 3) := by
  set S0 := {y : Fin 3 → ℝ | l1 y < 2}
  set S1 := S0 ∩ {y | 0 < y 0}
  set S2 := S1 ∩ {y | 0 < y 1}
  set S3 := S2 ∩ {y | 0 < y 2}
  have m0 : MeasurableSet S0 := measurableSet_lt continuous_l1.measurable measurable_const
  have mi : ∀ i : Fin 3, MeasurableSet {y : Fin 3 → ℝ | 0 < y i} := fun i =>
    measurableSet_lt measurable_const (measurable_pi_apply i)
  have m1 : MeasurableSet S1 := m0.inter (mi 0)
  have m2 : MeasurableSet S2 := m1.inter (mi 1)
  have e1 := vol_half 0 m0 (fun y => by simp [S0, l1_refl])
  have e2 := vol_half 1 m1 (fun y => by
    simp only [S1, S0, mem_inter_iff, mem_ofPred_eq, l1_refl, refl_apply_ne (by decide : (0 : Fin 3) ≠ 1)])
  have e3 := vol_half 2 m2 (fun y => by
    simp only [S2, S1, S0, mem_inter_iff, mem_ofPred_eq, l1_refl,
      refl_apply_ne (by decide : (0 : Fin 3) ≠ 2), refl_apply_ne (by decide : (1 : Fin 3) ≠ 2)])
  have hS0 : volume S0 = ENNReal.ofReal (32 / 3) := by
    rw [vol_l1_lt (by norm_num : (0 : ℝ) ≤ 2)]; norm_num
  have h3 : volume S3 = ENNReal.ofReal (4 / 3) := by
    rw [hS0] at e1
    have v1 := ennreal_half (by norm_num) (show 2 * volume S1 = ENNReal.ofReal (2 * (16 / 3)) by
      rw [e1]; norm_num)
    rw [v1] at e2
    have v2 := ennreal_half (by norm_num) (show 2 * volume S2 = ENNReal.ofReal (2 * (8 / 3)) by
      rw [e2]; norm_num)
    rw [v2] at e3
    exact ennreal_half (by norm_num) (show 2 * volume S3 = ENNReal.ofReal (2 * (4 / 3)) by
      rw [e3]; norm_num)
  rw [← h3]
  symm
  apply vol_eq_of_sub_null (z := {y | y 0 = 0} ∪ {y | y 1 = 0} ∪ {y | y 2 = 0})
  · rintro y ⟨⟨⟨h0, ha⟩, hb⟩, hc⟩
    simp only [S0, l1, mem_ofPred_eq] at h0 ha hb hc
    rw [abs_of_pos ha, abs_of_pos hb, abs_of_pos hc] at h0
    exact ⟨ha.le, hb.le, hc.le, h0⟩
  · rintro y ⟨ha, hb, hc, hs⟩
    by_cases h0 : y 0 = 0
    · exact Or.inr (Or.inl (Or.inl h0))
    by_cases h1 : y 1 = 0
    · exact Or.inr (Or.inl (Or.inr h1))
    by_cases h2 : y 2 = 0
    · exact Or.inr (Or.inr h2)
    have ha' := lt_of_le_of_ne ha (Ne.symm h0)
    have hb' := lt_of_le_of_ne hb (Ne.symm h1)
    have hc' := lt_of_le_of_ne hc (Ne.symm h2)
    refine Or.inl ⟨⟨⟨?_, ha'⟩, hb'⟩, hc'⟩
    simp only [S0, l1, mem_ofPred_eq]
    rw [abs_of_pos ha', abs_of_pos hb', abs_of_pos hc']; exact hs
  · exact measure_union_null (measure_union_null (plane_null 0 0) (plane_null 1 0)) (plane_null 2 0)

lemma ennreal_sub {x : ENNReal} {c d : ℝ} (hc : 0 ≤ c) (hcd : c ≤ d)
    (h : x + ENNReal.ofReal c = ENNReal.ofReal d) : x = ENNReal.ofReal (d - c) := by
  have hx : x ≠ ⊤ := by
    intro hx; rw [hx] at h; simp at h
  rw [← ENNReal.ofReal_toReal hx, ← ENNReal.ofReal_add ENNReal.toReal_nonneg hc,
    ENNReal.ofReal_eq_ofReal_iff (by positivity) (by linarith)] at h
  rw [← ENNReal.ofReal_toReal hx]
  congr 1; linarith

/-! ### The octahedron -/

lemma octSet_eq : octSet = WithLp.ofLp ⁻¹' {y : Fin 3 → ℝ | l1 y ≤ 1} := by
  ext x
  simp only [mem_preimage, mem_ofPred_eq, l1]
  constructor
  · intro hx
    obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8⟩ := oct_ineqs hx
    show |x 0| + |x 1| + |x 2| ≤ 1
    rcases abs_cases (x 0) with ⟨a0, -⟩ | ⟨a0, -⟩ <;> rcases abs_cases (x 1) with ⟨a1, -⟩ | ⟨a1, -⟩ <;>
      rcases abs_cases (x 2) with ⟨a2, -⟩ | ⟨a2, -⟩ <;> rw [a0, a1, a2] <;> linarith
  · intro h
    have h' : |x 0| + |x 1| + |x 2| ≤ 1 := h
    have b0 := le_abs_self (x 0); have c0 := neg_abs_le (x 0)
    have b1 := le_abs_self (x 1); have c1 := neg_abs_le (x 1)
    have b2 := le_abs_self (x 2); have c2 := neg_abs_le (x 2)
    intro m
    fin_cases m <;> simp [octN, octB, inner3] <;> linarith

/-- **The octahedron |x| + |y| + |z| ≤ 1 has volume 4/3.** -/
theorem volume_oct : volume octSet = ENNReal.ofReal (4 / 3) := by
  rw [octSet_eq, (PiLp.volume_preserving_ofLp (Fin 3)).measure_preimage
    (measurableSet_le continuous_l1.measurable measurable_const).nullMeasurableSet, vol_l1_le zero_le_one]
  norm_num

/-! ### Coordinate maps that keep volume -/

/-- Shift one coordinate by −1. -/
def shiftDown (i : Fin 3) (y : Fin 3 → ℝ) : Fin 3 → ℝ := fun j => if j = i then y j - 1 else y j

lemma mp_shiftDown (i : Fin 3) : MeasurePreserving (shiftDown i) := by
  have h := measurePreserving_pi (fun _ : Fin 3 => (volume : Measure ℝ)) (fun _ => volume)
    (f := fun j => if j = i then (fun a : ℝ => a - 1) else id)
    (fun j => by
      split_ifs
      · exact measurePreserving_sub_right _ 1
      · exact MeasurePreserving.id _)
  have he : shiftDown i = fun a j => (if j = i then (fun a : ℝ => a - 1) else id) (a j) := by
    funext y j; unfold shiftDown; split_ifs <;> rfl
  rw [he, volume_pi]; exact h

/-- The map y ↦ (1 − v_j y_j)_j for a sign vector v. -/
def flipShift (v : Fin 3 → ℝ) (y : Fin 3 → ℝ) : Fin 3 → ℝ := fun j => 1 - v j * y j

lemma mp_flipShift (v : Fin 3 → ℝ) (hv : ∀ j, v j = 1 ∨ v j = -1) : MeasurePreserving (flipShift v) := by
  have h := measurePreserving_pi (fun _ : Fin 3 => (volume : Measure ℝ)) (fun _ => volume)
    (f := fun j => fun a : ℝ => 1 - v j * a)
    (fun j => by
      rcases hv j with h | h <;> rw [h]
      · convert measurePreserving_sub_left (volume : Measure ℝ) 1 using 1
        funext a; ring
      · convert measurePreserving_add_left (volume : Measure ℝ) 1 using 1
        funext a; ring)
  rw [show flipShift v = fun a j => (fun a : ℝ => 1 - v j * a) (a j) from rfl, volume_pi]; exact h

/-! ### The cube ∩ octahedron line -/

/-- The cube ∩ octahedron solid in coordinates. -/
def coF (t : ℝ) : Set (Fin 3 → ℝ) := {y | |y 0| ≤ 1 ∧ |y 1| ≤ 1 ∧ |y 2| ≤ 1 ∧ l1 y ≤ t}

lemma coSet_eq (t : ℝ) : coSet t = WithLp.ofLp ⁻¹' coF t := by
  ext x
  simp only [mem_preimage, coF, mem_ofPred_eq]
  constructor
  · intro hx
    obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14⟩ := co_ineqs hx
    refine ⟨show |x 0| ≤ 1 from abs_le.2 ⟨by linarith, by linarith⟩,
      show |x 1| ≤ 1 from abs_le.2 ⟨by linarith, by linarith⟩,
      show |x 2| ≤ 1 from abs_le.2 ⟨by linarith, by linarith⟩, ?_⟩
    show |x 0| + |x 1| + |x 2| ≤ t
    rcases abs_cases (x 0) with ⟨a0, -⟩ | ⟨a0, -⟩ <;> rcases abs_cases (x 1) with ⟨a1, -⟩ | ⟨a1, -⟩ <;>
      rcases abs_cases (x 2) with ⟨a2, -⟩ | ⟨a2, -⟩ <;> rw [a0, a1, a2] <;> linarith
  · rintro ⟨a, b, c, h⟩
    have h' : |x 0| + |x 1| + |x 2| ≤ t := h
    obtain ⟨a', a''⟩ := abs_le.1 (show |x 0| ≤ 1 from a)
    obtain ⟨b', b''⟩ := abs_le.1 (show |x 1| ≤ 1 from b)
    obtain ⟨c', c''⟩ := abs_le.1 (show |x 2| ≤ 1 from c)
    have b0 := le_abs_self (x 0); have c0 := neg_abs_le (x 0)
    have b1 := le_abs_self (x 1); have c1 := neg_abs_le (x 1)
    have b2 := le_abs_self (x 2); have c2 := neg_abs_le (x 2)
    intro m
    fin_cases m <;> simp [coN, coB, inner3] <;> linarith

/-- The six caps {±y_i > 1} of the ball of radius t. -/
def capF (t : ℝ) (p : Fin 3 × Bool) : Set (Fin 3 → ℝ) :=
  {y | 1 < (if p.2 then y p.1 else -y p.1) ∧ l1 y ≤ t}

lemma measurableSet_capF (t : ℝ) (p : Fin 3 × Bool) : MeasurableSet (capF t p) := by
  rcases p with ⟨i, b⟩
  cases b
  · exact (measurableSet_lt measurable_const (measurable_pi_apply i).neg).inter
      (measurableSet_le continuous_l1.measurable measurable_const)
  · exact (measurableSet_lt measurable_const (measurable_pi_apply i)).inter
      (measurableSet_le continuous_l1.measurable measurable_const)

lemma capF_true (t : ℝ) (i : Fin 3) :
    capF t (i, true) = shiftDown i ⁻¹' ({y | l1 y ≤ t - 1} ∩ {y | 0 < y i}) := by
  ext y
  simp only [capF, mem_preimage, mem_inter_iff, mem_ofPred_eq, ite_true]
  fin_cases i <;> simp [shiftDown, l1]
  · constructor <;> rintro ⟨h1, h2⟩
    · rw [abs_of_pos (by linarith : (0 : ℝ) < y 0 - 1)]
      rw [abs_of_pos (by linarith : (0 : ℝ) < y 0)] at h2
      exact ⟨by linarith, h1⟩
    · rw [abs_of_pos (by linarith : (0 : ℝ) < y 0 - 1)] at h1
      rw [abs_of_pos (by linarith : (0 : ℝ) < y 0)]
      exact ⟨h2, by linarith⟩
  · constructor <;> rintro ⟨h1, h2⟩
    · rw [abs_of_pos (by linarith : (0 : ℝ) < y 1 - 1)]
      rw [abs_of_pos (by linarith : (0 : ℝ) < y 1)] at h2
      exact ⟨by linarith, h1⟩
    · rw [abs_of_pos (by linarith : (0 : ℝ) < y 1 - 1)] at h1
      rw [abs_of_pos (by linarith : (0 : ℝ) < y 1)]
      exact ⟨h2, by linarith⟩
  · constructor <;> rintro ⟨h1, h2⟩
    · rw [abs_of_pos (by linarith : (0 : ℝ) < y 2 - 1)]
      rw [abs_of_pos (by linarith : (0 : ℝ) < y 2)] at h2
      exact ⟨by linarith, h1⟩
    · rw [abs_of_pos (by linarith : (0 : ℝ) < y 2 - 1)] at h1
      rw [abs_of_pos (by linarith : (0 : ℝ) < y 2)]
      exact ⟨h2, by linarith⟩

lemma capF_false (t : ℝ) (i : Fin 3) : capF t (i, false) = refl i ⁻¹' capF t (i, true) := by
  ext y
  simp [capF, refl_apply_self, l1_refl]

lemma vol_capF (t : ℝ) (ht : 1 ≤ t) (p : Fin 3 × Bool) :
    volume (capF t p) = ENNReal.ofReal (2 / 3 * (t - 1) ^ 3) := by
  have htrue : ∀ i, volume (capF t (i, true)) = ENNReal.ofReal (2 / 3 * (t - 1) ^ 3) := fun i => by
    rw [capF_true, (mp_shiftDown i).measure_preimage
      ((measurableSet_le continuous_l1.measurable measurable_const).inter
        (measurableSet_lt measurable_const (measurable_pi_apply i))).nullMeasurableSet,
      vol_halfBall i (by linarith)]
  rcases p with ⟨i, b⟩
  cases b
  · rw [capF_false, (mp_refl i).measure_preimage (measurableSet_capF t _).nullMeasurableSet, htrue]
  · exact htrue i

lemma capF_disj {t : ℝ} (ht : t < 2) : Pairwise (Function.onFun Disjoint (capF t)) := by
  rintro ⟨i, b⟩ ⟨j, c⟩ hij
  rw [Function.onFun, Set.disjoint_left]
  rintro y ⟨h1, hl⟩ ⟨h2, -⟩
  simp only [l1] at hl
  have b0 := le_abs_self (y 0); have c0 := neg_abs_le (y 0)
  have b1 := le_abs_self (y 1); have c1 := neg_abs_le (y 1)
  have b2 := le_abs_self (y 2); have c2 := neg_abs_le (y 2)
  have d0 := abs_nonneg (y 0); have d1 := abs_nonneg (y 1); have d2 := abs_nonneg (y 2)
  fin_cases i <;> fin_cases j <;> cases b <;> cases c <;> simp at hij h1 h2 <;> linarith

lemma ball_diff_coF (t : ℝ) : {y : Fin 3 → ℝ | l1 y ≤ t} \ coF t = ⋃ p, capF t p := by
  ext y
  simp only [mem_sdiff, mem_ofPred_eq, coF, mem_iUnion]
  constructor
  · rintro ⟨hl, hn⟩
    by_cases h0 : |y 0| ≤ 1
    · by_cases h1 : |y 1| ≤ 1
      · by_cases h2 : |y 2| ≤ 1
        · exact absurd ⟨h0, h1, h2, hl⟩ hn
        · rcases lt_abs.1 (not_le.1 h2) with h | h
          · exact ⟨(2, true), h, hl⟩
          · exact ⟨(2, false), h, hl⟩
      · rcases lt_abs.1 (not_le.1 h1) with h | h
        · exact ⟨(1, true), h, hl⟩
        · exact ⟨(1, false), h, hl⟩
    · rcases lt_abs.1 (not_le.1 h0) with h | h
      · exact ⟨(0, true), h, hl⟩
      · exact ⟨(0, false), h, hl⟩
  · rintro ⟨⟨i, b⟩, h, hl⟩
    refine ⟨hl, fun ⟨a0, a1, a2, _⟩ => ?_⟩
    have := abs_le.1 a0; have := abs_le.1 a1; have := abs_le.1 a2
    fin_cases i <;> cases b <;> simp at h <;> linarith

lemma measurableSet_coF (t : ℝ) : MeasurableSet (coF t) := by
  have hc : ∀ i : Fin 3, MeasurableSet {y : Fin 3 → ℝ | |y i| ≤ 1} := fun i =>
    measurableSet_le (measurable_pi_apply i).abs measurable_const
  have : coF t = {y | |y 0| ≤ 1} ∩ ({y | |y 1| ≤ 1} ∩ ({y | |y 2| ≤ 1} ∩ {y | l1 y ≤ t})) := by
    ext y; simp [coF]
  rw [this]
  exact (hc 0).inter ((hc 1).inter ((hc 2).inter
    (measurableSet_le continuous_l1.measurable measurable_const)))

/-- **The volume of the cube ∩ octahedron solid**: for 1 ≤ t < 2 it is (4/3)(t³ − 3(t − 1)³). -/
theorem volume_co {t : ℝ} (ht1 : 1 ≤ t) (ht2 : t < 2) :
    volume (coSet t) = ENNReal.ofReal (4 / 3 * (t ^ 3 - 3 * (t - 1) ^ 3)) := by
  rw [coSet_eq, (PiLp.volume_preserving_ofLp (Fin 3)).measure_preimage
    (measurableSet_coF t).nullMeasurableSet]
  have h := measure_inter_add_sdiff (μ := volume) {y : Fin 3 → ℝ | l1 y ≤ t} (measurableSet_coF t)
  have hsub : {y : Fin 3 → ℝ | l1 y ≤ t} ∩ coF t = coF t :=
    inter_eq_right.2 fun y hy => hy.2.2.2
  rw [hsub, ball_diff_coF, measure_iUnion (capF_disj ht2) (measurableSet_capF t), tsum_fintype,
    Finset.sum_congr rfl (fun p _ => vol_capF t ht1 p), Finset.sum_const, Finset.card_univ,
    Fintype.card_prod, Fintype.card_fin, Fintype.card_bool, vol_l1_le (by linarith), nsmul_eq_mul,
    show ((3 * 2 : ℕ) : ENNReal) = ENNReal.ofReal 6 by norm_num,
    ← ENNReal.ofReal_mul (by norm_num)] at h
  have h1 : 0 ≤ (t - 1) ^ 3 := pow_nonneg (by linarith) 3
  rw [ennreal_sub (by positivity) (by nlinarith [sq_nonneg (t - 1), sq_nonneg t]) h]
  congr 1; ring

/-! ### The regular tetrahedron -/

def cubeF : Set (Fin 3 → ℝ) := {y | |y 0| ≤ 1 ∧ |y 1| ≤ 1 ∧ |y 2| ≤ 1}

def tetF : Set (Fin 3 → ℝ) :=
  {y | y 0 + y 1 + y 2 ≤ 1 ∧ -y 0 - y 1 + y 2 ≤ 1 ∧ -y 0 + y 1 - y 2 ≤ 1 ∧ y 0 - y 1 - y 2 ≤ 1}

/-- The four corner directions of the cube cut off by the tetrahedron's faces. -/
def cornerV : Fin 4 → (Fin 3 → ℝ) := ![![1, 1, 1], ![-1, -1, 1], ![-1, 1, -1], ![1, -1, -1]]

def cornerF (v : Fin 3 → ℝ) : Set (Fin 3 → ℝ) :=
  {y | |y 0| ≤ 1 ∧ |y 1| ≤ 1 ∧ |y 2| ≤ 1 ∧ 1 < v 0 * y 0 + v 1 * y 1 + v 2 * y 2}

def octant : Set (Fin 3 → ℝ) := {u | 0 ≤ u 0 ∧ 0 ≤ u 1 ∧ 0 ≤ u 2 ∧ u 0 + u 1 + u 2 < 2}

lemma cornerV_sign (k : Fin 4) : ∀ j, cornerV k j = 1 ∨ cornerV k j = -1 := by
  intro j; fin_cases k <;> fin_cases j <;> simp [cornerV]

lemma cornerF_eq (v : Fin 3 → ℝ) (hv : ∀ j, v j = 1 ∨ v j = -1) :
    cornerF v = flipShift v ⁻¹' octant := by
  ext y
  simp only [cornerF, octant, flipShift, mem_preimage, mem_ofPred_eq]
  rcases hv 0 with h0 | h0 <;> rcases hv 1 with h1 | h1 <;> rcases hv 2 with h2 | h2 <;>
  rw [h0, h1, h2] <;>
  rcases abs_cases (y 0) with ⟨a0, s0⟩ | ⟨a0, s0⟩ <;> rcases abs_cases (y 1) with ⟨a1, s1⟩ | ⟨a1, s1⟩ <;>
  rcases abs_cases (y 2) with ⟨a2, s2⟩ | ⟨a2, s2⟩ <;> rw [a0, a1, a2] <;>
  constructor <;> rintro ⟨b0, b1, b2, b3⟩ <;> refine ⟨?_, ?_, ?_, ?_⟩ <;> linarith

lemma measurableSet_octant : MeasurableSet octant := by
  have hc : ∀ i : Fin 3, MeasurableSet {y : Fin 3 → ℝ | 0 ≤ y i} := fun i =>
    measurableSet_le measurable_const (measurable_pi_apply i)
  have : octant = {y | 0 ≤ y 0} ∩ ({y | 0 ≤ y 1} ∩ ({y | 0 ≤ y 2} ∩ {y | y 0 + y 1 + y 2 < 2})) := by
    ext y; simp [octant]
  rw [this]
  exact (hc 0).inter ((hc 1).inter ((hc 2).inter (measurableSet_lt (by fun_prop) measurable_const)))

lemma vol_cornerF (k : Fin 4) : volume (cornerF (cornerV k)) = ENNReal.ofReal (4 / 3) := by
  rw [cornerF_eq _ (cornerV_sign k), (mp_flipShift _ (cornerV_sign k)).measure_preimage
    measurableSet_octant.nullMeasurableSet]
  exact vol_corner

lemma measurableSet_cornerF (k : Fin 4) : MeasurableSet (cornerF (cornerV k)) := by
  rw [cornerF_eq _ (cornerV_sign k)]
  exact (mp_flipShift _ (cornerV_sign k)).measurable measurableSet_octant

lemma cornerF_disj : Pairwise (Function.onFun Disjoint fun k : Fin 4 => cornerF (cornerV k)) := by
  intro i j hij
  rw [Function.onFun, Set.disjoint_left]
  rintro y ⟨a0, a1, a2, h1⟩ ⟨-, -, -, h2⟩
  have := abs_le.1 a0; have := abs_le.1 a1; have := abs_le.1 a2
  fin_cases i <;> fin_cases j <;> simp [cornerV] at hij h1 h2 <;> linarith

lemma cube_diff_tet : cubeF \ tetF = ⋃ k : Fin 4, cornerF (cornerV k) := by
  ext y
  simp only [mem_sdiff, mem_iUnion, cubeF, tetF, cornerF, mem_ofPred_eq]
  constructor
  · rintro ⟨⟨a0, a1, a2⟩, hn⟩
    by_cases hA : y 0 + y 1 + y 2 ≤ 1
    · by_cases hB : -y 0 - y 1 + y 2 ≤ 1
      · by_cases hC : -y 0 + y 1 - y 2 ≤ 1
        · by_cases hD : y 0 - y 1 - y 2 ≤ 1
          · exact absurd ⟨hA, hB, hC, hD⟩ hn
          · exact ⟨3, a0, a1, a2, by simp [cornerV]; linarith⟩
        · exact ⟨2, a0, a1, a2, by simp [cornerV]; linarith⟩
      · exact ⟨1, a0, a1, a2, by simp [cornerV]; linarith⟩
    · exact ⟨0, a0, a1, a2, by simp [cornerV]; linarith⟩
  · rintro ⟨k, a0, a1, a2, h⟩
    refine ⟨⟨a0, a1, a2⟩, fun ⟨hA, hB, hC, hD⟩ => ?_⟩
    fin_cases k <;> simp [cornerV] at h <;> linarith

lemma tetF_sub_cubeF : tetF ⊆ cubeF := by
  rintro y ⟨hA, hB, hC, hD⟩
  exact ⟨abs_le.2 ⟨by linarith, by linarith⟩, abs_le.2 ⟨by linarith, by linarith⟩,
    abs_le.2 ⟨by linarith, by linarith⟩⟩

lemma measurableSet_tetF : MeasurableSet tetF := by
  have : tetF = {y : Fin 3 → ℝ | y 0 + y 1 + y 2 ≤ 1} ∩ ({y | -y 0 - y 1 + y 2 ≤ 1} ∩
      ({y | -y 0 + y 1 - y 2 ≤ 1} ∩ {y | y 0 - y 1 - y 2 ≤ 1})) := by
    ext y; simp [tetF]
  rw [this]
  exact (measurableSet_le (by fun_prop) measurable_const).inter
    ((measurableSet_le (by fun_prop) measurable_const).inter
      ((measurableSet_le (by fun_prop) measurable_const).inter
        (measurableSet_le (by fun_prop) measurable_const)))

lemma vol_cubeF : volume cubeF = ENNReal.ofReal 8 := by
  have : cubeF = Icc (fun _ => -1) (fun _ => 1) := by
    ext y
    simp only [cubeF, mem_ofPred_eq, mem_Icc, Pi.le_def, abs_le, Fin.forall_fin_succ,
      IsEmpty.forall_iff]
    simp only [Fin.succ_zero_eq_one, Fin.succ_one_eq_two]
    tauto
  rw [this, Real.volume_Icc_pi, Fin.prod_univ_three]
  rw [← ENNReal.ofReal_mul (by norm_num), ← ENNReal.ofReal_mul (by norm_num)]
  norm_num

lemma tetraSet_eq : tetraSet = WithLp.ofLp ⁻¹' tetF := by
  ext x
  simp only [mem_preimage, tetF, mem_ofPred_eq]
  constructor
  · intro hx
    have h0 := hx 0; have h1 := hx 1; have h2 := hx 2; have h3 := hx 3
    simp [tetN, inner3] at h0 h1 h2 h3
    exact ⟨by linarith, by linarith, by linarith, by linarith⟩
  · rintro ⟨hA, hB, hC, hD⟩ m
    fin_cases m <;> simp [tetN, inner3] <;> linarith

/-- **The regular tetrahedron of study 3 (edge 2√2) has volume 8/3.** -/
theorem volume_tetra : volume tetraSet = ENNReal.ofReal (8 / 3) := by
  rw [tetraSet_eq, (PiLp.volume_preserving_ofLp (Fin 3)).measure_preimage
    measurableSet_tetF.nullMeasurableSet]
  have h := measure_inter_add_sdiff (μ := volume) cubeF measurableSet_tetF
  rw [inter_eq_right.2 tetF_sub_cubeF, cube_diff_tet,
    measure_iUnion cornerF_disj measurableSet_cornerF, tsum_fintype,
    Finset.sum_congr rfl (fun k _ => vol_cornerF k), Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul, vol_cubeF,
    show ((4 : ℕ) : ENNReal) = ENNReal.ofReal 4 by norm_num,
    ← ENNReal.ofReal_mul (by norm_num)] at h
  rw [ennreal_sub (by norm_num) (by norm_num) h]
  norm_num

end DehnCanon
