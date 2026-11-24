/-
Aequus = equal fin regions (study 2026-11-25-one-structure, Theorem A1 (a)).
DICTO, with Claude (Anthropic).
-/
import VacuusResonus.PolarLink

/-!
# The fin regions of a die (M2)

The die, its face cones and its solid angles are defined exactly as in the Lean Alexandrov study
(2026-11-22-lean-alexandrov, `Alexandrov/Dice.lean`): face normals `n j` (unit, distinct, not all in
one closed hemisphere), face distances `d j > 0`, `die n d = {x | ∀ j, ⟪n j, x⟫ ≤ d j}`, and
`solidAngle n d k = 3 * volume (faceCone n d k ∩ ball 0 1)`.

The **fin region** of face `k` is the radial projection of the face onto the unit sphere `S`: the unit
directions whose ray from `O` meets the face. Its area is measured with Mathlib's surface measure
`volume.toSphere` on `S`.

* `toSphere_finRegion` : the area of the fin region of face `k` is the solid angle of face `k`.
* `iUnion_finRegion` : the fin regions cover the sphere.
* `finRegion_inter_subset` and `toSphere_finRegion_inter` : two distinct fin regions meet only on a
  great circle (the plane through `O` and the common edge), a null set.
* `sum_toSphere_finRegion` : the areas add up to `4π`.
* `aequus_iff_finRegions` (**Theorem A1 (a)**): all faces have equal solid angle (the Aequus) if and
  only if all fin regions have equal area; and `isFair_iff_finRegions`: then each is `4π / N`.
-/

open MeasureTheory Set Metric
open scoped RealInnerProductSpace ENNReal Pointwise

namespace VacuusResonus

variable {N : ℕ}

/-- The die with face normals `n j` at distances `d j` (as in the Alexandrov study). -/
def die (n : Fin N → E3) (d : Fin N → ℝ) : Set E3 := {x | ∀ j, ⟪n j, x⟫ ≤ d j}

/-- Face `k` of the die. -/
def face (n : Fin N → E3) (d : Fin N → ℝ) (k : Fin N) : Set E3 := die n d ∩ {x | ⟪n k, x⟫ = d k}

/-- Directions whose ray from the origin leaves the die through face `k` (as in the Alexandrov
study). -/
def faceCone (n : Fin N → E3) (d : Fin N → ℝ) (k : Fin N) : Set E3 :=
  {x | ∃ t : ℝ, 0 < t ∧ t • x ∈ die n d ∧ ⟪n k, t • x⟫ = d k}

/-- The solid angle of face `k` (as in the Alexandrov study). -/
noncomputable def solidAngle (n : Fin N → E3) (d : Fin N → ℝ) (k : Fin N) : ℝ≥0∞ :=
  3 * volume (faceCone n d k ∩ ball (0 : E3) 1)

/-- A die is fair about the origin when all `N` faces have solid angle `4π / N` (as in the
Alexandrov study). -/
def IsFair (n : Fin N → E3) (d : Fin N → ℝ) : Prop :=
  ∀ k, solidAngle n d k = ENNReal.ofReal (4 * Real.pi / N)

/-- The fin region of face `k`: the radial projection of the face onto the unit sphere. -/
def finRegion (n : Fin N → E3) (d : Fin N → ℝ) (k : Fin N) : Set (sphere (0 : E3) 1) :=
  {u | ∃ t : ℝ, 0 < t ∧ t • (u : E3) ∈ face n d k}

/-- The cell of face `k`: directions in which face `k` is the first face plane reached. -/
def cellD (n : Fin N → E3) (d : Fin N → ℝ) (k : Fin N) : Set E3 :=
  {x | ∀ j, (d j)⁻¹ * ⟪n j, x⟫ ≤ (d k)⁻¹ * ⟪n k, x⟫}

theorem finRegion_eq (n : Fin N → E3) (d : Fin N → ℝ) (k : Fin N) :
    finRegion n d k = ((↑) : sphere (0 : E3) 1 → E3) ⁻¹' faceCone n d k := by
  ext u
  simp [finRegion, face, faceCone]

theorem zero_not_mem_faceCone {n : Fin N → E3} {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) (k : Fin N) :
    (0 : E3) ∉ faceCone n d k := by
  rintro ⟨t, -, -, h⟩
  simp at h
  exact (hd k).ne h

theorem smul_mem_faceCone {n : Fin N → E3} {d : Fin N → ℝ} {k : Fin N} {x : E3}
    (hx : x ∈ faceCone n d k) {c : ℝ} (hc : 0 < c) : c • x ∈ faceCone n d k := by
  obtain ⟨t, ht, h1, h2⟩ := hx
  refine ⟨t / c, div_pos ht hc, ?_, ?_⟩ <;> rwa [smul_smul, div_mul_cancel₀ _ hc.ne']

/-- The face cone is the cell without the origin (the argument of the Alexandrov study,
`solidAngle_eq_curvature`). -/
theorem faceCone_eq {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) (k : Fin N) :
    faceCone n d k = cellD n d k \ {0} := by
  ext x
  constructor
  · intro hx
    refine ⟨?_, fun h => zero_not_mem_faceCone hd k (by rw [mem_singleton_iff.1 h] at hx; exact hx)⟩
    obtain ⟨t, ht, hdie, hface⟩ := hx
    intro j
    have h1 := hdie j
    rw [real_inner_smul_right] at h1 hface
    have key : t * (⟪n j, x⟫ * d k) ≤ t * (⟪n k, x⟫ * d j) := by
      have e : d j * d k = t * (⟪n k, x⟫ * d j) := by rw [← hface]; ring
      have := mul_le_mul_of_nonneg_right h1 (hd k).le
      linarith
    have key' := le_of_mul_le_mul_left key ht
    have hdj := (hd j).ne'
    have hdk := (hd k).ne'
    have e1 : (d j)⁻¹ * ⟪n j, x⟫ = (⟪n j, x⟫ * d k) * ((d j)⁻¹ * (d k)⁻¹) := by field_simp
    have e2 : (d k)⁻¹ * ⟪n k, x⟫ = (⟪n k, x⟫ * d j) * ((d j)⁻¹ * (d k)⁻¹) := by field_simp
    rw [e1, e2]
    exact mul_le_mul_of_nonneg_right key' (by have := hd j; have := hd k; positivity)
  · rintro ⟨hx, hx0⟩
    have hx0 : x ≠ 0 := hx0
    obtain ⟨m, hm⟩ := hspan x hx0
    have hcm := hx m
    have hb : 0 < ⟪n k, x⟫ := by
      have : 0 < (d m)⁻¹ * ⟪n m, x⟫ := mul_pos (inv_pos.2 (hd m)) hm
      have : 0 < (d k)⁻¹ * ⟪n k, x⟫ := lt_of_lt_of_le this hcm
      exact pos_of_mul_pos_right this (inv_pos.2 (hd k)).le
    refine ⟨d k / ⟪n k, x⟫, div_pos (hd k) hb, fun j => ?_, ?_⟩
    · rw [real_inner_smul_right, div_mul_eq_mul_div, div_le_iff₀ hb]
      have hc : (d j)⁻¹ * ⟪n j, x⟫ ≤ (d k)⁻¹ * ⟪n k, x⟫ := hx j
      have h' := (inv_mul_le_iff₀ (hd j)).1 hc
      have hdk := (hd k).ne'
      calc d k * ⟪n j, x⟫ ≤ d k * (d j * ((d k)⁻¹ * ⟪n k, x⟫)) :=
            mul_le_mul_of_nonneg_left h' (hd k).le
        _ = d j * ⟪n k, x⟫ := by field_simp
    · rw [real_inner_smul_right, div_mul_cancel₀ _ hb.ne']

theorem isClosed_cellD (n : Fin N → E3) (d : Fin N → ℝ) (k : Fin N) : IsClosed (cellD n d k) := by
  have : cellD n d k = ⋂ j, {x | (d j)⁻¹ * ⟪n j, x⟫ ≤ (d k)⁻¹ * ⟪n k, x⟫} := by
    ext; simp [cellD]
  rw [this]
  exact isClosed_iInter fun j => isClosed_le (continuous_const.mul (continuous_const.inner
    continuous_id)) (continuous_const.mul (continuous_const.inner continuous_id))

theorem measurableSet_faceCone {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) (k : Fin N) : MeasurableSet (faceCone n d k) := by
  rw [faceCone_eq hspan hd]
  exact (isClosed_cellD n d k).measurableSet.diff (measurableSet_singleton 0)

theorem measurableSet_finRegion {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) (k : Fin N) : MeasurableSet (finRegion n d k) := by
  rw [finRegion_eq]
  exact measurable_subtype_coe (measurableSet_faceCone hspan hd k)

/-- A cone without its apex, restricted to the unit sphere and swept by `(0, 1)`, is the cone inside
the unit ball. -/
theorem Ioo_smul_cone {C : Set E3} (hC : ∀ x ∈ C, ∀ c : ℝ, 0 < c → c • x ∈ C)
    (h0 : (0 : E3) ∉ C) :
    Ioo (0 : ℝ) 1 • ((↑) '' (((↑) : sphere (0 : E3) 1 → E3) ⁻¹' C)) = C ∩ ball 0 1 := by
  ext x
  constructor
  · rintro ⟨c, ⟨hc0, hc1⟩, _, ⟨⟨u, hu⟩, huC, rfl⟩, rfl⟩
    refine ⟨hC u huC c hc0, ?_⟩
    rw [mem_sphere_zero_iff_norm] at hu
    rw [mem_ball_zero_iff, norm_smul, hu, mul_one, Real.norm_eq_abs, abs_of_pos hc0]
    exact hc1
  · rintro ⟨hxC, hxb⟩
    have hx0 : x ≠ 0 := fun h => h0 (h ▸ hxC)
    have hn : 0 < ‖x‖ := norm_pos_iff.2 hx0
    rw [mem_ball_zero_iff] at hxb
    refine ⟨‖x‖, ⟨hn, hxb⟩, _, ⟨⟨‖x‖⁻¹ • x, ?_⟩, hC x hxC _ (inv_pos.2 hn), rfl⟩, ?_⟩
    · rw [mem_sphere_zero_iff_norm, norm_smul, norm_inv, norm_norm, inv_mul_cancel₀ hn.ne']
    · simp only
      rw [smul_smul, mul_inv_cancel₀ hn.ne', one_smul]

/-- **The area of a fin region is the solid angle of its face.** -/
theorem toSphere_finRegion {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) (k : Fin N) :
    volume.toSphere (finRegion n d k) = solidAngle n d k := by
  rw [Measure.toSphere_apply' _ (measurableSet_finRegion hspan hd k), finRegion_eq,
    Ioo_smul_cone (fun x hx c hc => smul_mem_faceCone hx hc) (zero_not_mem_faceCone hd k),
    solidAngle, finrank_euclideanSpace_fin]
  norm_num

/-- **The fin regions cover the sphere.** -/
theorem iUnion_finRegion {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) : ⋃ k, finRegion n d k = univ := by
  refine eq_univ_of_forall fun u => ?_
  have hu0 : (u : E3) ≠ 0 := by
    intro h
    have := u.2
    rw [h, mem_sphere_zero_iff_norm, norm_zero] at this
    exact zero_ne_one this
  obtain ⟨i, -⟩ := hspan u hu0
  obtain ⟨k, -, hk⟩ := Finset.exists_max_image Finset.univ
    (fun j => (d j)⁻¹ * ⟪n j, (u : E3)⟫) ⟨i, Finset.mem_univ i⟩
  refine mem_iUnion.2 ⟨k, ?_⟩
  rw [finRegion_eq, mem_preimage, faceCone_eq hspan hd]
  exact ⟨fun j => hk j (Finset.mem_univ j), hu0⟩

/-- **Two distinct fin regions meet only on a great circle**: the plane through `O` with normal
`d k • n j - d j • n k`, which is nonzero. -/
theorem finRegion_inter_subset {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) (j k : Fin N) :
    ((↑) : sphere (0 : E3) 1 → E3) '' (finRegion n d j ∩ finRegion n d k) ⊆
      {x | ⟪d k • n j - d j • n k, x⟫ = 0} := by
  rintro _ ⟨u, ⟨hj, hk⟩, rfl⟩
  rw [finRegion_eq, mem_preimage, faceCone_eq hspan hd] at hj hk
  have h1 := hj.1 k
  have h2 := hk.1 j
  have hdj := (hd j).ne'
  have hdk := (hd k).ne'
  have he : (d j)⁻¹ * ⟪n j, (u : E3)⟫ = (d k)⁻¹ * ⟪n k, (u : E3)⟫ := le_antisymm h2 h1
  simp only [mem_ofPred_eq, inner_sub_left, real_inner_smul_left]
  field_simp at he
  linarith

theorem normal_ne_zero {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1) (hinj : Function.Injective n)
    {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) {j k : Fin N} (hjk : j ≠ k) :
    d k • n j - d j • n k ≠ 0 := by
  intro h
  have h' : d k • n j = d j • n k := sub_eq_zero.1 h
  have hn' := congrArg norm h'
  rw [norm_smul, norm_smul, hn, hn, Real.norm_eq_abs, Real.norm_eq_abs, abs_of_pos (hd k),
    abs_of_pos (hd j), mul_one, mul_one] at hn'
  rw [hn'] at h'
  exact hjk (hinj (smul_right_injective E3 (hd j).ne' h'))

/-- A plane through the origin has volume zero (as in the Alexandrov study). -/
theorem volume_plane {w : E3} (hw : w ≠ 0) : volume {x : E3 | ⟪w, x⟫ = 0} = 0 := by
  have hs : (LinearMap.ker (innerₛₗ ℝ w)) ≠ ⊤ := by
    intro h
    have : w ∈ LinearMap.ker (innerₛₗ ℝ w) := h ▸ Submodule.mem_top
    rw [LinearMap.mem_ker] at this
    have hww : ⟪w, w⟫ = 0 := this
    exact hw (inner_self_eq_zero.1 hww)
  have := Measure.addHaar_submodule volume _ hs
  convert this using 2
  ext x
  exact Iff.rfl

/-- **Distinct fin regions overlap in a null set.** -/
theorem toSphere_finRegion_inter {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) {j k : Fin N} (hjk : j ≠ k) :
    volume.toSphere (finRegion n d j ∩ finRegion n d k) = 0 := by
  have hm := (measurableSet_finRegion hspan hd j).inter (measurableSet_finRegion hspan hd k)
  rw [Measure.toSphere_apply' _ hm]
  have hsub : Ioo (0 : ℝ) 1 • ((↑) '' (finRegion n d j ∩ finRegion n d k)) ⊆
      {x : E3 | ⟪d k • n j - d j • n k, x⟫ = 0} := by
    rintro _ ⟨c, -, x, hx, rfl⟩
    have := finRegion_inter_subset hspan hd j k hx
    simp only [mem_ofPred_eq] at this ⊢
    rw [real_inner_smul_right, this, mul_zero]
  rw [measure_mono_null hsub (volume_plane (normal_ne_zero hn hinj hd hjk)), mul_zero]

/-- The whole unit sphere has area `4π`. -/
theorem toSphere_univ : volume.toSphere (univ : Set (sphere (0 : E3) 1)) =
    ENNReal.ofReal (4 * Real.pi) := by
  rw [Measure.toSphere_apply_univ, finrank_euclideanSpace_fin,
    EuclideanSpace.volume_ball_fin_three]
  rw [ENNReal.ofReal_one, one_pow, one_mul]
  rw [show ((3 : ℕ) : ℝ≥0∞) = ENNReal.ofReal 3 by simp, ← ENNReal.ofReal_mul (by norm_num)]
  congr 1
  ring

/-- **The fin areas add up to `4π`.** -/
theorem sum_toSphere_finRegion {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) :
    ∑ k, volume.toSphere (finRegion n d k) = ENNReal.ofReal (4 * Real.pi) := by
  rw [← toSphere_univ, ← iUnion_finRegion hspan hd,
    measure_iUnion₀ (fun j k hjk => toSphere_finRegion_inter hn hinj hspan hd hjk)
      (fun k => (measurableSet_finRegion hspan hd k).nullMeasurableSet), tsum_fintype]

/-- **Theorem A1 (a).** All faces have equal solid angle (the Aequus) if and only if all fin regions
have equal area. -/
theorem aequus_iff_finRegions {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) :
    (∀ j k, solidAngle n d j = solidAngle n d k) ↔
      ∀ j k, volume.toSphere (finRegion n d j) = volume.toSphere (finRegion n d k) := by
  simp only [toSphere_finRegion hspan hd]

/-- **Theorem A1 (a), with the value.** The die is fair (every solid angle `4π / N`) if and only if
every fin region has area `4π / N`. -/
theorem isFair_iff_finRegions {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) :
    IsFair n d ↔ ∀ k, volume.toSphere (finRegion n d k) = ENNReal.ofReal (4 * Real.pi / N) := by
  simp only [IsFair, toSphere_finRegion hspan hd]

/-- **Theorem A1 (a), the value.** Equal solid angles (equivalently, equal fin areas) force the value
`4π / N`: the Aequus condition and fairness coincide. -/
theorem aequus_iff_isFair [NeZero N] {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) :
    (∀ j k, solidAngle n d j = solidAngle n d k) ↔ IsFair n d := by
  constructor
  · intro h k
    have hs := sum_toSphere_finRegion hn hinj hspan hd
    simp only [toSphere_finRegion hspan hd] at hs
    rw [Finset.sum_congr rfl (fun j _ => h j k), Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, nsmul_eq_mul] at hs
    have hN : (0 : ℝ) < N := Nat.cast_pos.2 (Nat.pos_of_ne_zero (NeZero.ne N))
    rw [ENNReal.ofReal_div_of_pos hN, ENNReal.ofReal_natCast, ← hs, mul_comm,
      ENNReal.mul_div_cancel_right]
    · exact_mod_cast NeZero.ne N
    · exact ENNReal.natCast_ne_top N
  · intro h j k
    rw [h j, h k]

end VacuusResonus
