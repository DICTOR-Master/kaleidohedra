module

public import YantraCert.Unique2
public import YantraCert.Charts

@[expose] public section

/-!
# The case split over the charts (step 3 assembled)

`pt_in_X`: the main-chart point of every admissible figure lies in the Krawczyk box `X`. The point lies in the open box
`(0,1)² × (0,6]` (`BoxBounds`). If it is in the corner `[7/8,1]²` it is covered by chart A or B; if it is in the corner
`[0,1/4] × [0,1/16]` by chart C1 or C2, and C1's hole N1 by W, Wt± or Wr± (`Charts`). Every chart's certificate (`covered`)
then says that the point is in a hole, and the chart lemmas `contra_*` (`Unique2`) leave only the main chart's hole `Krawczyk`.
-/

namespace YantraCert.Y
open YantraCert YantraCert.Deriv

section
variable {y : Yantra} (F : Facts y)
include F

lemma unit_of {C : Chart} (h : C.Covered ⟨0, 0, 0, 0, 0, 0⟩) {a b c : ℝ} (ha : 0 ≤ a ∧ a ≤ 1) (hb : 0 ≤ b ∧ b ≤ 1)
    (hc : 0 ≤ c ∧ c ≤ 1) : C.Good a b c := C.good_of_root h a b c ha hb hc

/-- the N1 hole of chart C1 is covered by the W charts -/
lemma no_N1 (s θ : ℝ) (hs : 0 < s) (hθ : 0 < θ) (hu : V y 0 = s) (hτ : tau y = s ^ 4 * θ)
    (hN : (1 : ℝ) ≤ θ * 1 / 2 * 4 ∧ θ * 1 / 2 * 4 ≤ 3 ∧ 0 ≤ s * 4 / 1 * 1 ∧ s * 4 / 1 * 4 ≤ 1 ∧
      (1 : ℝ) ≤ rho y * 1 / 6 * 12 ∧ rho y * 1 / 6 * 4 ≤ 1) : False := by
  have hr := rho_pos F
  obtain ⟨n1, n2, -, n4, n5, n6⟩ := hN
  rcases Charts.cover_N1 s θ (rho y) ⟨hs, by linarith⟩ ⟨by linarith, by linarith⟩ ⟨by linarith, by linarith⟩ with
    ⟨ζ, x, z1, z2, x1, x2, eθ, eρ⟩ | ⟨σ, a, x, hσ, hσ1, ha0, ha1, x1, x2, es, eθ, eρ⟩ | ⟨σ, a, ζ, hσ, hσ1, ha0, ha1, z1, z2, es, eθ, eρ⟩
  · -- chart W: (p, q, r) = (s, ζ + 4, x + 4)
    have hG := unit_of F YantraCert.Data.W.covered (a := s * 16 / 1) (b := (ζ + 4) * 1 / 8) (c := (x + 4) * 1 / 8)
      ⟨by positivity, by linarith⟩ ⟨by linarith, by linarith⟩ ⟨by linarith, by linarith⟩
    obtain ⟨h, hh, -⟩ := contra_W F s (ζ + 4) (x + 4) hs (by linarith) (by linarith)
      (by simp [MW_0, ZP.eval]; linarith) (by simp [MW_1, ZP.eval]; rw [hτ, eθ]; ring)
      (by simp [MW_2, ZP.eval]; rw [eρ]; ring) hG
    simp [YantraCert.Data.W.C] at hh
  · rcases eθ with eθ | eθ
    · have hG := unit_of F YantraCert.Data.Wtp.covered (a := σ * 5 / 3) (b := a * 1 / 1) (c := (x + 1) * 1 / 2)
        ⟨by positivity, by linarith⟩ ⟨by linarith, by linarith⟩ ⟨by linarith, by linarith⟩
      have ha : 0 < a := by
        rcases eq_or_lt_of_le ha0 with h | h
        · rw [← h, mul_zero] at es; linarith
        · exact h
      obtain ⟨h, hh, -⟩ := contra_Wtp F σ a (x + 1) hσ ha (by linarith)
        (by simp [MWtp_0, ZP.eval]; linarith) (by simp [MWtp_1, ZP.eval]; rw [hτ, eθ, es]; ring)
        (by simp [MWtp_2, ZP.eval]; rw [eρ, es]; ring) hG
      simp [YantraCert.Data.Wtp.C] at hh
    · have hG := unit_of F YantraCert.Data.Wtm.covered (a := σ * 5 / 3) (b := a * 1 / 1) (c := (x + 1) * 1 / 2)
        ⟨by positivity, by linarith⟩ ⟨by linarith, by linarith⟩ ⟨by linarith, by linarith⟩
      have ha : 0 < a := by
        rcases eq_or_lt_of_le ha0 with h | h
        · rw [← h, mul_zero] at es; linarith
        · exact h
      obtain ⟨h, hh, -⟩ := contra_Wtm F σ a (x + 1) hσ ha (by linarith)
        (by simp [MWtm_0, ZP.eval]; linarith) (by simp [MWtm_1, ZP.eval]; rw [hτ, eθ, es]; ring)
        (by simp [MWtm_2, ZP.eval]; rw [eρ, es]; ring) hG
      simp [YantraCert.Data.Wtm.C] at hh
  · rcases eρ with eρ | eρ
    · have hG := unit_of F YantraCert.Data.Wrp.covered (a := σ * 8 / 3) (b := a * 1 / 1) (c := (ζ + 1) * 1 / 2)
        ⟨by positivity, by linarith⟩ ⟨by linarith, by linarith⟩ ⟨by linarith, by linarith⟩
      have ha : 0 < a := by
        rcases eq_or_lt_of_le ha0 with h | h
        · rw [← h, mul_zero] at es; linarith
        · exact h
      obtain ⟨h, hh, -⟩ := contra_Wrp F σ a (ζ + 1) hσ ha.le (by linarith)
        (by simp [MWrp_0, ZP.eval]; linarith) (by simp [MWrp_1, ZP.eval]; rw [hτ, eθ, es]; ring)
        (by simp [MWrp_2, ZP.eval]; rw [eρ, es]; ring) hG
      simp [YantraCert.Data.Wrp.C] at hh
    · have hG := unit_of F YantraCert.Data.Wrm.covered (a := σ * 8 / 3) (b := a * 1 / 1) (c := (ζ + 1) * 1 / 2)
        ⟨by positivity, by linarith⟩ ⟨by linarith, by linarith⟩ ⟨by linarith, by linarith⟩
      have ha : 0 < a := by
        rcases eq_or_lt_of_le ha0 with h | h
        · rw [← h, mul_zero] at es; linarith
        · exact h
      obtain ⟨h, hh, -⟩ := contra_Wrm F σ a (ζ + 1) hσ ha.le (by linarith)
        (by simp [MWrm_0, ZP.eval]; linarith) (by simp [MWrm_1, ZP.eval]; rw [hτ, eθ, es]; ring)
        (by simp [MWrm_2, ZP.eval]; rw [eρ, es]; ring) hG
      simp [YantraCert.Data.Wrm.C] at hh

/-- **the main-chart point of an admissible figure lies in the Krawczyk box** -/
theorem pt_in_X : ∀ j, (KBox.LX j : ℝ) / KBox.QX ≤ pt y j ∧ pt y j ≤ (KBox.HX j : ℝ) / KBox.QX := by
  have hu := u_pos F; have hu1 := u_lt1 F; have ht := tau_pos F; have ht1 := tau_lt1 F
  have hr := rho_pos F; have hr6 := rho_le6 F
  by_cases h1 : 7 / 8 ≤ V y 0 ∧ 7 / 8 ≤ tau y
  · exfalso
    rcases Charts.cover_corner1 (V y 0) (tau y) ⟨h1.1, hu1.le⟩ ⟨h1.2, ht1.le⟩ with
      ⟨x, θ, x0, x1, θ0, θ1, ex, eθ⟩ | ⟨x, η, x0, x1, η0, η1, ex, eη⟩
    · have hx : 0 < x := by linarith
      have hθ : 0 < θ := by
        rcases eq_or_lt_of_le θ0 with h | h
        · rw [← h, mul_zero] at eθ; linarith
        · exact h
      have hG := unit_of F YantraCert.Data.A.covered (a := x * 8 / 1) (b := θ * 1 / 1) (c := rho y * 1 / 6)
        ⟨by positivity, by linarith⟩ ⟨by linarith, by linarith⟩ ⟨by positivity, by linarith⟩
      obtain ⟨h, hh, -⟩ := contra_A F x θ (rho y) hx hθ.le hr.le (by simp [MA_0, ZP.eval]; linarith)
        (by simp [MA_1, ZP.eval]; linarith) (by simp [MA_2, ZP.eval]) hG
      simp [YantraCert.Data.A.C] at hh
    · have hx : 0 < x := by linarith
      have hη : 0 < η := by
        rcases eq_or_lt_of_le η0 with h | h
        · rw [← h, mul_zero] at ex; linarith
        · exact h
      have hG := unit_of F YantraCert.Data.B.covered (a := x * 8 / 1) (b := η * 1 / 1) (c := rho y * 1 / 6)
        ⟨by positivity, by linarith⟩ ⟨by linarith, by linarith⟩ ⟨by positivity, by linarith⟩
      obtain ⟨h, hh, -⟩ := contra_B F x η (rho y) hx hη.le hr.le (by simp [MB_0, ZP.eval]; linarith)
        (by simp [MB_1, ZP.eval]; linarith) (by simp [MB_2, ZP.eval]) hG
      simp [YantraCert.Data.B.C] at hh
  by_cases h0 : V y 0 ≤ 1 / 4 ∧ tau y ≤ 1 / 16
  · exfalso
    rcases Charts.cover_corner0 (V y 0) (tau y) ⟨hu.le, h0.1⟩ ⟨ht.le, h0.2⟩ with
      ⟨s, θ, s0, s1, θ0, θ1, es, eθ⟩ | ⟨s, η, s0, s1, η0, η1, eu, es⟩
    · have hs : 0 < s := by linarith
      have hθ : 0 < θ := by
        rcases eq_or_lt_of_le θ0 with h | h
        · rw [← h, mul_zero] at eθ; linarith
        · exact h
      have hG := unit_of F YantraCert.Data.C1.covered (a := s * 4 / 1) (b := θ * 1 / 2) (c := rho y * 1 / 6)
        ⟨by positivity, by linarith⟩ ⟨by positivity, by linarith⟩ ⟨by positivity, by linarith⟩
      obtain ⟨h, hh, hm⟩ := contra_C1 F s θ (rho y) hs hθ.le hr.le (by simp [MC1_0, ZP.eval]; linarith)
        (by simp [MC1_1, ZP.eval]; rw [eθ]) (by simp [MC1_2, ZP.eval]) hG
      simp only [YantraCert.Data.C1.C, List.mem_cons, List.not_mem_nil, or_false] at hh
      subst hh
      simp only [HB.Mem] at hm
      push_cast at hm
      exact no_N1 F s θ hs hθ (by linarith) eθ (by obtain ⟨m1, m2, m3, m4, m5, m6⟩ := hm; exact ⟨by linarith, by linarith,
        by linarith, by linarith, by linarith, by linarith⟩)
    · have hs : 0 < s := by
        rcases eq_or_lt_of_le s0 with h | h
        · rw [← h] at es; norm_num at es; linarith
        · exact h
      have hη : 0 < η := by
        rcases eq_or_lt_of_le η0 with h | h
        · rw [← h, mul_zero] at eu; linarith
        · exact h
      have hG := unit_of F YantraCert.Data.C2.covered (a := s * 2 / 1) (b := η * 32 / 27) (c := rho y * 1 / 6)
        ⟨by positivity, by linarith⟩ ⟨by positivity, by linarith⟩ ⟨by positivity, by linarith⟩
      obtain ⟨h, hh, -⟩ := contra_C2 F s η (rho y) hs hη.le hr.le (by simp [MC2_0, ZP.eval]; linarith)
        (by simp [MC2_1, ZP.eval]; linarith) (by simp [MC2_2, ZP.eval]) hG
      simp [YantraCert.Data.C2.C] at hh
  -- the main chart
  have hG := unit_of F YantraCert.Data.Main.covered (a := V y 0) (b := tau y) (c := rho y / 6)
    ⟨hu.le, hu1.le⟩ ⟨ht.le, ht1.le⟩ ⟨by positivity, by linarith⟩
  obtain ⟨h, hh, hm⟩ := contra_Main F hG
  simp only [YantraCert.Data.Main.C, List.mem_cons, List.not_mem_nil, or_false] at hh
  rcases hh with rfl | rfl | rfl <;> simp only [HB.Mem] at hm <;> push_cast at hm
  · obtain ⟨m1, m2, m3, m4, m5, m6⟩ := hm
    intro j; fin_cases j <;> simp [pt, KBox.LX, KBox.HX, KBox.QX] <;> constructor <;> linarith
  · exfalso; obtain ⟨m1, m2, m3, m4, m5, m6⟩ := hm; exact h0 ⟨by linarith, by linarith⟩
  · exfalso; obtain ⟨m1, m2, m3, m4, m5, m6⟩ := hm; exact h1 ⟨by linarith, by linarith⟩

end

end YantraCert.Y
