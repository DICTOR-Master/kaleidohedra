/-
Alexandrov's theorem on prescribed curvature, polyhedral case: a uniform margin in Alexandrov's condition.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Functional

/-!
# A uniform margin (M9c, part 1)

`nbhd n ε I` is the open cone of directions `x` with `⟪n i, x⟫ > ε ‖x‖` for some ray `i ∈ I`;
`nbhd n 0 I` is the open `π/2`-neighbourhood of the rays in `I`.

* `exists_cover`: some `ε₀ > 0` has every direction within `⟪n j, x⟫ > ε₀ ‖x‖` of some ray (the rays
  are not in one closed hemisphere, and the unit sphere is compact).
* `exists_margin`: **Alexandrov's condition** for the corners, `Σ_{i ∈ I} κ i < area (nbhd n 0 I)`
  for every nonempty proper set `I` of rays, survives with a uniform margin `η > 0` after shrinking
  each neighbourhood to `nbhd n ε I` for one small `ε > 0`.
-/

open MeasureTheory Set Metric Finset Filter Topology
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ} [NeZero N]

/-- Directions making an angle less than `arccos ε` with some ray in `I`. -/
def nbhd (n : Fin N → E3) (ε : ℝ) (I : Finset (Fin N)) : Set E3 :=
  {x | ∃ i ∈ I, ε * ‖x‖ < ⟪n i, x⟫}

omit [NeZero N] in
lemma isOpen_nbhd (n : Fin N → E3) (ε : ℝ) (I : Finset (Fin N)) : IsOpen (nbhd n ε I) := by
  have : nbhd n ε I = ⋃ i ∈ I, {x : E3 | ε * ‖x‖ < ⟪n i, x⟫} := by ext x; simp [nbhd]
  rw [this]
  exact isOpen_biUnion fun i _ =>
    isOpen_lt (continuous_const.mul continuous_norm) (continuous_const.inner continuous_id)

theorem exists_cover {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫) :
    ∃ ε₀ > 0, ∀ x : E3, x ≠ 0 → ∃ j, ε₀ * ‖x‖ < ⟪n j, x⟫ := by
  set f : E3 → ℝ := fun x => univ.sup' univ_nonempty' (fun j => (1 : Fin N → ℝ) j * ⟪n j, x⟫)
    with hfdef
  have hf : Continuous f := continuous_sup' univ univ_nonempty' 1 n
  obtain ⟨u, hu, hmin⟩ := (isCompact_sphere (0 : E3) 1).exists_isMinOn
    (NormedSpace.sphere_nonempty.2 zero_le_one) hf.continuousOn
  have hu0 : u ≠ 0 := by rintro rfl; simp at hu
  have hm : 0 < f u := supp_pos hspan (r := 1) (fun _ => by simp) hu0
  refine ⟨f u / 2, by positivity, fun x hx => ?_⟩
  have hxn : 0 < ‖x‖ := norm_pos_iff.2 hx
  set y : E3 := ‖x‖⁻¹ • x with hydef
  have hy : y ∈ sphere (0 : E3) 1 := by
    rw [mem_sphere_zero_iff_norm, hydef, norm_smul, norm_inv, norm_norm, inv_mul_cancel₀ hxn.ne']
  have h1 : f u ≤ f y := isMinOn_iff.1 hmin y hy
  have hxy : x = ‖x‖ • y := by rw [hydef, smul_smul, mul_inv_cancel₀ hxn.ne', one_smul]
  have h2 : f x = ‖x‖ * f y := by
    have := sup'_smul univ univ_nonempty' 1 n (norm_nonneg x) y
    rw [← hxy] at this
    exact this
  obtain ⟨j, -, hj⟩ := exists_mem_eq_sup' univ_nonempty' (fun j => (1 : Fin N → ℝ) j * ⟪n j, x⟫)
  refine ⟨j, ?_⟩
  have h3 : f x = ⟪n j, x⟫ := by
    have : f x = (1 : Fin N → ℝ) j * ⟪n j, x⟫ := hj
    rw [this, Pi.one_apply, one_mul]
  nlinarith [mul_le_mul_of_nonneg_left h1 hxn.le]

theorem exists_margin {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {κ : Fin N → ℝ}
    (hA : ∀ I : Finset (Fin N), I.Nonempty → I ≠ Finset.univ →
      ∑ i ∈ I, κ i < 3 * (volume (nbhd n 0 I ∩ ball (0 : E3) 1)).toReal) :
    ∃ ε > 0, ∃ η > 0, (∀ x : E3, x ≠ 0 → ∃ j, ε * ‖x‖ < ⟪n j, x⟫) ∧
      ∀ I : Finset (Fin N), I.Nonempty → I ≠ Finset.univ →
        ∑ i ∈ I, κ i + η ≤ 3 * (volume (nbhd n ε I ∩ ball (0 : E3) 1)).toReal := by
  classical
  obtain ⟨ε₀, hε₀, hcov⟩ := exists_cover hspan
  set e : ℕ → ℝ := fun k => ε₀ / (k + 2) with hedef
  have hepos : ∀ k, 0 < e k := fun k => by positivity
  have hele : ∀ k, e k ≤ ε₀ := fun k =>
    div_le_self hε₀.le (by have : (0 : ℝ) ≤ k := Nat.cast_nonneg k; linarith)
  have hfin : ∀ S : Set E3, volume (S ∩ ball (0 : E3) 1) ≠ ∞ := fun S =>
    (measure_mono Set.inter_subset_right |>.trans_lt measure_ball_lt_top).ne
  have hlim : ∀ I : Finset (Fin N), Tendsto (fun k => 3 * (volume (nbhd n (e k) I ∩
      ball (0 : E3) 1)).toReal) atTop (𝓝 (3 * (volume (nbhd n 0 I ∩ ball (0 : E3) 1)).toReal)) := by
    intro I
    have hmono : Monotone fun k => nbhd n (e k) I ∩ ball (0 : E3) 1 := by
      intro k l hkl x ⟨⟨i, hi, hx⟩, hb⟩
      refine ⟨⟨i, hi, lt_of_le_of_lt ?_ hx⟩, hb⟩
      have : e l ≤ e k := div_le_div_of_nonneg_left hε₀.le (by positivity)
        (by have : (k : ℝ) ≤ l := Nat.cast_le.2 hkl; linarith)
      exact mul_le_mul_of_nonneg_right this (norm_nonneg x)
    have hunion : (⋃ k, nbhd n (e k) I ∩ ball (0 : E3) 1) = nbhd n 0 I ∩ ball (0 : E3) 1 := by
      ext x
      simp only [mem_iUnion, mem_inter_iff, nbhd, mem_ofPred_eq, zero_mul]
      constructor
      · rintro ⟨k, ⟨i, hi, hx⟩, hb⟩
        exact ⟨⟨i, hi, lt_of_le_of_lt (mul_nonneg (hepos k).le (norm_nonneg x)) hx⟩, hb⟩
      · rintro ⟨⟨i, hi, hx⟩, hb⟩
        obtain ⟨k, hk⟩ := exists_nat_gt (ε₀ * ‖x‖ / ⟪n i, x⟫)
        refine ⟨k, ⟨i, hi, ?_⟩, hb⟩
        rw [div_lt_iff₀ hx] at hk
        rw [hedef, div_mul_eq_mul_div, div_lt_iff₀ (by positivity)]
        nlinarith
    have := tendsto_measure_iUnion_atTop (μ := volume) hmono
    rw [hunion] at this
    exact ((ENNReal.tendsto_toReal (hfin _)).comp this).const_mul 3
  have hev : ∀ᶠ k in atTop, ∀ I : Finset (Fin N), I.Nonempty → I ≠ Finset.univ →
      ∑ i ∈ I, κ i < 3 * (volume (nbhd n (e k) I ∩ ball (0 : E3) 1)).toReal := by
    refine eventually_all.2 fun I => ?_
    by_cases hI : I.Nonempty ∧ I ≠ Finset.univ
    · exact ((hlim I).eventually (lt_mem_nhds (hA I hI.1 hI.2))).mono fun k hk _ _ => hk
    · exact Eventually.of_forall fun k h1 h2 => absurd ⟨h1, h2⟩ hI
  obtain ⟨k, hk⟩ := hev.exists
  set ε := e k
  refine ⟨ε, hepos k, ?_⟩
  set P := (univ : Finset (Finset (Fin N))).filter (fun I => I.Nonempty ∧ I ≠ Finset.univ) with hP
  set d : Finset (Fin N) → ℝ := fun I =>
    3 * (volume (nbhd n ε I ∩ ball (0 : E3) 1)).toReal - ∑ i ∈ I, κ i with hd
  have hcov' : ∀ x : E3, x ≠ 0 → ∃ j, ε * ‖x‖ < ⟪n j, x⟫ := fun x hx => by
    obtain ⟨j, hj⟩ := hcov x hx
    exact ⟨j, lt_of_le_of_lt (mul_le_mul_of_nonneg_right (hele k) (norm_nonneg x)) hj⟩
  by_cases hPne : P.Nonempty
  · refine ⟨P.inf' hPne d, (Finset.lt_inf'_iff hPne).2 fun I hI => ?_, hcov', fun I h1 h2 => ?_⟩
    · have := (Finset.mem_filter.1 hI).2
      exact sub_pos.2 (hk I this.1 this.2)
    · have hIP : I ∈ P := Finset.mem_filter.2 ⟨Finset.mem_univ I, h1, h2⟩
      have := Finset.inf'_le d hIP
      simp only [hd] at this
      linarith
  · exact ⟨1, one_pos, hcov', fun I h1 h2 =>
      (hPne ⟨I, (Finset.mem_filter.2 ⟨Finset.mem_univ I, h1, h2⟩ : I ∈ P)⟩).elim⟩

end Alexandrov
