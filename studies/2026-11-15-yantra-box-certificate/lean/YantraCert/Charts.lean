import Mathlib

/-!
# The corner charts cover the corner holes (step 3 of the Lean plan, the covering lemmas)

The main chart leaves two corner holes of the box `(u, τ, ρ) ∈ [0, 1] × [0, 1] × [0, 6]`, and chart C1 leaves the hole `N1`.
These lemmas show that the blow-up charts of `scripts/b1_charts.py` cover them:
* `cover_corner1`: charts A and B (homogeneous blow-up at `(u, τ) = (1, 1)`) cover `[7/8, 1]²`;
* `cover_corner0`: charts C1 and C2 (weights `(1, 4)` at `(u, τ) = (0, 0)`) cover `[0, 1/4] × [0, 1/16]`;
* `cover_N1`: charts W, Wt± and Wr± (weights `(1, 4, 2)` along the curve `θ = 1, ρ = 1 + s`) cover `N1` minus `s = 0`.
Each is a case split on which weighted size is largest, with real square roots.
-/

namespace YantraCert.Charts

/-- **corner (1, 1)**: charts A `(x, θ) ↦ (1 - x, 1 - x θ)` and B `(y, η) ↦ (1 - y η, 1 - y)` cover `[7/8, 1]²` -/
theorem cover_corner1 (u τ : ℝ) (hu : 7 / 8 ≤ u ∧ u ≤ 1) (hτ : 7 / 8 ≤ τ ∧ τ ≤ 1) :
    (∃ x θ : ℝ, 0 ≤ x ∧ x ≤ 1 / 8 ∧ 0 ≤ θ ∧ θ ≤ 1 ∧ u = 1 - x ∧ τ = 1 - x * θ) ∨
    (∃ y η : ℝ, 0 ≤ y ∧ y ≤ 1 / 8 ∧ 0 ≤ η ∧ η ≤ 1 ∧ u = 1 - y * η ∧ τ = 1 - y) := by
  rcases le_total (1 - τ) (1 - u) with h | h
  · left
    rcases eq_or_lt_of_le (show 0 ≤ 1 - u by linarith) with h0 | h0
    · refine ⟨0, 0, le_rfl, by norm_num, le_rfl, by norm_num, by linarith, by linarith⟩
    · refine ⟨1 - u, (1 - τ) / (1 - u), h0.le, by linarith, div_nonneg (by linarith) h0.le,
        (div_le_one h0).mpr h, by ring, ?_⟩
      field_simp; ring
  · right
    rcases eq_or_lt_of_le (show 0 ≤ 1 - τ by linarith) with h0 | h0
    · refine ⟨0, 0, le_rfl, by norm_num, le_rfl, by norm_num, by linarith, by linarith⟩
    · refine ⟨1 - τ, (1 - u) / (1 - τ), h0.le, by linarith, div_nonneg (by linarith) h0.le,
        (div_le_one h0).mpr h, ?_, by ring⟩
      field_simp; ring

/-- the fourth root as two square roots -/
lemma sqrt_sqrt_pow4 {a : ℝ} (ha : 0 ≤ a) : Real.sqrt (Real.sqrt a) ^ 4 = a := by
  have h1 : Real.sqrt (Real.sqrt a) ^ 2 = Real.sqrt a := Real.sq_sqrt (Real.sqrt_nonneg a)
  calc Real.sqrt (Real.sqrt a) ^ 4 = (Real.sqrt (Real.sqrt a) ^ 2) ^ 2 := by ring
    _ = a := by rw [h1, Real.sq_sqrt ha]

lemma le_of_pow4_le {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) (h : x ^ 4 ≤ y ^ 4) : x ≤ y :=
  (pow_le_pow_iff_left₀ hx hy (by norm_num : (4 : ℕ) ≠ 0)).mp h

/-- **corner (0, 0)**: charts C1 `(s, θ) ↦ (s, s⁴ θ)` and C2 `(s, η) ↦ (s η, s⁴)` cover `[0, 1/4] × [0, 1/16]` -/
theorem cover_corner0 (u τ : ℝ) (hu : 0 ≤ u ∧ u ≤ 1 / 4) (hτ : 0 ≤ τ ∧ τ ≤ 1 / 16) :
    (∃ s θ : ℝ, 0 ≤ s ∧ s ≤ 1 / 4 ∧ 0 ≤ θ ∧ θ ≤ 2 ∧ u = s ∧ τ = s ^ 4 * θ) ∨
    (∃ s η : ℝ, 0 ≤ s ∧ s ≤ 1 / 2 ∧ 0 ≤ η ∧ η ≤ 27 / 32 ∧ u = s * η ∧ τ = s ^ 4) := by
  rcases le_or_gt τ (2 * u ^ 4) with h | h
  · left
    rcases eq_or_lt_of_le hu.1 with h0 | h0
    · subst h0
      refine ⟨0, 0, le_rfl, by norm_num, le_rfl, by norm_num, rfl, ?_⟩
      have : τ = 0 := le_antisymm (by simpa using h) hτ.1
      simp [this]
    · refine ⟨u, τ / u ^ 4, hu.1, hu.2, div_nonneg hτ.1 (by positivity), ?_, rfl, ?_⟩
      · rw [div_le_iff₀ (by positivity)]; linarith
      · field_simp
  · right
    have hτ0 : 0 < τ := lt_of_le_of_lt (by positivity) h
    set s := Real.sqrt (Real.sqrt τ) with hs
    have s4 : s ^ 4 = τ := sqrt_sqrt_pow4 hτ.1
    have s0 : 0 < s := Real.sqrt_pos.mpr (Real.sqrt_pos.mpr hτ0)
    refine ⟨s, u / s, s0.le, ?_, div_nonneg hu.1 s0.le, ?_, by field_simp, s4.symm⟩
    · apply le_of_pow4_le s0.le (by norm_num); rw [s4]; linarith [hτ.2]
    · apply le_of_pow4_le (div_nonneg hu.1 s0.le) (by norm_num)
      rw [div_pow, s4, div_le_iff₀ hτ0]
      nlinarith [h]

/-- **the hole `N1` of chart C1**: charts W, Wt± and Wr± cover `(0, 1/16] × [1/2, 3/2] × [1/2, 3/2]` in `(s, θ, ρ)`.
* W: `θ = 1 + s⁴ ζ`, `ρ = 1 + s + s² x` with `ζ, x ∈ [-4, 4]` (the weighted size is `s`);
* Wt±: `s = σ a`, `θ = 1 ± 4 σ⁴`, `ρ = 1 + s + 4 σ² x` with `σ ≤ 3/5`, `a ∈ [0, 1]`, `x ∈ [-1, 1]`;
* Wr±: `s = σ a`, `θ = 1 + 4 σ⁴ ζ`, `ρ = 1 + s ± 4 σ²` with `σ ≤ 3/8`, `a ∈ [0, 1]`, `ζ ∈ [-1, 1]`. -/
theorem cover_N1 (s θ ρ : ℝ) (hs : 0 < s ∧ s ≤ 1 / 16) (hθ : 1 / 2 ≤ θ ∧ θ ≤ 3 / 2) (hρ : 1 / 2 ≤ ρ ∧ ρ ≤ 3 / 2) :
    (∃ ζ x : ℝ, -4 ≤ ζ ∧ ζ ≤ 4 ∧ -4 ≤ x ∧ x ≤ 4 ∧ θ = 1 + s ^ 4 * ζ ∧ ρ = 1 + s + s ^ 2 * x) ∨
    (∃ σ a x : ℝ, 0 < σ ∧ σ ≤ 3 / 5 ∧ 0 ≤ a ∧ a ≤ 1 ∧ -1 ≤ x ∧ x ≤ 1 ∧ s = σ * a ∧
      (θ = 1 + 4 * σ ^ 4 ∨ θ = 1 - 4 * σ ^ 4) ∧ ρ = 1 + s + 4 * σ ^ 2 * x) ∨
    (∃ σ a ζ : ℝ, 0 < σ ∧ σ ≤ 3 / 8 ∧ 0 ≤ a ∧ a ≤ 1 ∧ -1 ≤ ζ ∧ ζ ≤ 1 ∧ s = σ * a ∧
      θ = 1 + 4 * σ ^ 4 * ζ ∧ (ρ = 1 + s + 4 * σ ^ 2 ∨ ρ = 1 + s - 4 * σ ^ 2)) := by
  set A := |θ - 1| / 4 with hA
  set B := |ρ - 1 - s| / 4 with hB
  have A0 : 0 ≤ A := by positivity
  have B0 : 0 ≤ B := by positivity
  have s0 := hs.1
  have Ale : A ≤ 1 / 8 := by rw [hA, div_le_iff₀ (by norm_num)]; rw [abs_le]; constructor <;> linarith
  have Ble : B ≤ 9 / 64 := by rw [hB, div_le_iff₀ (by norm_num)]; rw [abs_le]; constructor <;> linarith
  by_cases c1 : A ≤ s ^ 4 ∧ B ≤ s ^ 2
  · left
    refine ⟨(θ - 1) / s ^ 4, (ρ - 1 - s) / s ^ 2, ?_, ?_, ?_, ?_, by field_simp; ring, by field_simp; ring⟩
    · rw [le_div_iff₀ (by positivity)]; have := neg_abs_le (θ - 1); linarith [c1.1]
    · rw [div_le_iff₀ (by positivity)]; have := le_abs_self (θ - 1); linarith [c1.1]
    · rw [le_div_iff₀ (by positivity)]; have := neg_abs_le (ρ - 1 - s); linarith [c1.2]
    · rw [div_le_iff₀ (by positivity)]; have := le_abs_self (ρ - 1 - s); linarith [c1.2]
  rcases le_total (B ^ 2) A with c2 | c2
  · -- the weighted size comes from θ
    right; left
    have As : s ^ 4 ≤ A := by
      by_contra hh; push Not at hh
      have hB2 : s ^ 2 < B := by
        by_contra hh2; push Not at hh2; exact c1 ⟨hh.le, hh2⟩
      nlinarith [hB2, sq_nonneg (B - s ^ 2), pow_pos s0 2]
    have Apos : 0 < A := lt_of_lt_of_le (by positivity) As
    set σ := Real.sqrt (Real.sqrt A) with hσ
    have σ4 : σ ^ 4 = A := sqrt_sqrt_pow4 A0
    have σ0 : 0 < σ := Real.sqrt_pos.mpr (Real.sqrt_pos.mpr Apos)
    have σ2B : B ≤ σ ^ 2 := by
      have : B ^ 2 ≤ (σ ^ 2) ^ 2 := by rw [← pow_mul]; simpa [σ4] using c2
      exact (pow_le_pow_iff_left₀ B0 (by positivity) (by norm_num : (2 : ℕ) ≠ 0)).mp this
    refine ⟨σ, s / σ, (ρ - 1 - s) / (4 * σ ^ 2), σ0, ?_, div_nonneg s0.le σ0.le, ?_, ?_, ?_, by field_simp, ?_, ?_⟩
    · apply le_of_pow4_le σ0.le (by norm_num); rw [σ4]; linarith
    · rw [div_le_one σ0]; apply le_of_pow4_le s0.le σ0.le; rw [σ4]; exact As
    · rw [le_div_iff₀ (by positivity)]; have := neg_abs_le (ρ - 1 - s); linarith
    · rw [div_le_iff₀ (by positivity)]; have := le_abs_self (ρ - 1 - s); linarith
    · rcases abs_cases (θ - 1) with ⟨h1, _⟩ | ⟨h1, _⟩
      · left; rw [σ4, hA, h1]; ring
      · right; rw [σ4, hA, h1]; ring
    · field_simp; ring
  · -- the weighted size comes from ρ
    right; right
    have Bs : s ^ 2 ≤ B := by
      by_contra hh; push Not at hh
      have hA4 : s ^ 4 < A := by
        by_contra hh2; push Not at hh2; exact c1 ⟨hh2, hh.le⟩
      nlinarith [hA4, pow_pos s0 2, mul_le_mul hh.le hh.le B0 (by positivity)]
    have Bpos : 0 < B := lt_of_lt_of_le (by positivity) Bs
    set σ := Real.sqrt B with hσ
    have σ2 : σ ^ 2 = B := Real.sq_sqrt B0
    have σ0 : 0 < σ := Real.sqrt_pos.mpr Bpos
    have σ4 : σ ^ 4 = B ^ 2 := by rw [show σ ^ 4 = (σ ^ 2) ^ 2 by ring, σ2]
    refine ⟨σ, s / σ, (θ - 1) / (4 * σ ^ 4), σ0, ?_, div_nonneg s0.le σ0.le, ?_, ?_, ?_, by field_simp, ?_, ?_⟩
    · apply (pow_le_pow_iff_left₀ σ0.le (by norm_num) (by norm_num : (2 : ℕ) ≠ 0)).mp; rw [σ2]; linarith
    · rw [div_le_one σ0]
      apply (pow_le_pow_iff_left₀ s0.le σ0.le (by norm_num : (2 : ℕ) ≠ 0)).mp; rw [σ2]; exact Bs
    · rw [le_div_iff₀ (by positivity)]; have := neg_abs_le (θ - 1); rw [σ4]; linarith
    · rw [div_le_iff₀ (by positivity)]; have := le_abs_self (θ - 1); rw [σ4]; linarith
    · field_simp; ring
    · rcases abs_cases (ρ - 1 - s) with ⟨h1, _⟩ | ⟨h1, _⟩
      · left; rw [σ2, hB, h1]; ring
      · right; rw [σ2, hB, h1]; ring

end YantraCert.Charts
