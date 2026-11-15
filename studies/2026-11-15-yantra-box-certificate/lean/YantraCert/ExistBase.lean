import YantraCert.Unique4
import YantraCert.Deriv.KExAll
import YantraCert.BoxQ
import YantraCert.Frac2

/-!
# Existence: the point, the named quantities, the signs on the small box

`xs` is the zero of `F~` in the small Krawczyk box `Xs` (`KBox.exists_S`, Banach's fixed-point theorem). From it,
`u = xs 0`, `τ = xs 1`, `ρ = xs 2`, `t = u τ`, `S = (1 + ρ (1 - u) u²) / (1 + u²)`, and the named quantities are the stored
fractions `W i = N_i(u, t, S) / D_i(u, t, S)`.
-/

namespace YantraCert.Y
open YantraCert YantraCert.Deriv

noncomputable def xs : Fin 3 → ℝ := Classical.choose KBox.exists_S
lemma xs_spec : InBox KBox.cS KBox.rS xs ∧ ∀ k, KBox.F k xs = 0 := Classical.choose_spec KBox.exists_S

lemma xs_bounds : ∀ j, (KBox.LS j : ℝ) / KBox.QS ≤ xs j ∧ xs j ≤ (KBox.HS j : ℝ) / KBox.QS := KBox.inb xs_spec.1

noncomputable def eu : ℝ := xs 0
noncomputable def etau : ℝ := xs 1
noncomputable def er : ℝ := xs 2
noncomputable def et : ℝ := eu * etau
noncomputable def eS : ℝ := (1 + er * (1 - eu) * eu ^ 2) / (1 + eu ^ 2)

lemma eu_pos : 0 < xs 0 := by have := (xs_bounds 0).1; simp [KBox.LS, KBox.QS] at this; linarith
lemma eu_lt1 : xs 0 < 1 := by have := (xs_bounds 0).2; simp [KBox.HS, KBox.QS] at this; linarith
lemma etau_pos : 0 < xs 1 := by have := (xs_bounds 1).1; simp [KBox.LS, KBox.QS] at this; linarith
lemma etau_lt1 : xs 1 < 1 := by have := (xs_bounds 1).2; simp [KBox.HS, KBox.QS] at this; linarith
lemma er_pos : 0 < xs 2 := by have := (xs_bounds 2).1; simp [KBox.LS, KBox.QS] at this; linarith

/-- the substitution at the point -/
lemma subst_x (P : ZP) (d : Nat) (hd : P.zdeg d = true) :
    (ZP.substH PX PY PZn PZd d P).eval (xs 0) (xs 1) (xs 2) = P.eval eu et eS * (1 + eu ^ 2) ^ d := by
  have hd0 : PZd.eval (xs 0) (xs 1) (xs 2) ≠ 0 := by simp [PZd, ZP.eval]; positivity
  rw [ZP.eval_substH PX PY PZn PZd P d hd _ _ _ hd0]
  have ex : PX.eval (xs 0) (xs 1) (xs 2) = eu := by simp [PX, ZP.eval, eu]
  have ey : PY.eval (xs 0) (xs 1) (xs 2) = et := by simp [PY, ZP.eval, et, eu, etau]
  have ez : PZn.eval (xs 0) (xs 1) (xs 2) / PZd.eval (xs 0) (xs 1) (xs 2) = eS := by
    simp [PZn, PZd, ZP.eval, eS, eu, er]; ring
  have ezd : PZd.eval (xs 0) (xs 1) (xs 2) = 1 + eu ^ 2 := by simp [PZd, ZP.eval, eu]
  rw [ex, ey, ez, ezd]

/-- the link between the core sign check and its proved twin -/
lemma boxSignN_eq (p : SP) :
    p.boxSignN KEx.QS 1045958633310927219312709804664751888613212 630290400061572206887148711804214366640362
      4345735874637809770754784814922852658776494 1045958633310927219312709804666950911868764
      630290400061572206887148711806413389895914 4345735874637809770754784814925051682032046 =
      p.boxSign KBox.QS KBox.LS KBox.HS := rfl

lemma box_sign1 (p : SP) (hd : p.degOK = true)
    (h : p.boxSignN KEx.QS 1045958633310927219312709804664751888613212 630290400061572206887148711804214366640362
      4345735874637809770754784814922852658776494 1045958633310927219312709804666950911868764
      630290400061572206887148711806413389895914 4345735874637809770754784814925051682032046 = 1) :
    0 < p.eval (xs 0) (xs 1) (xs 2) := by
  rw [boxSignN_eq] at h
  exact (p.boxSign_sound hd KBox.QS (by decide) KBox.LS KBox.HS xs xs_bounds).1 h

lemma box_sign2 (p : SP) (hd : p.degOK = true)
    (h : p.boxSignN KEx.QS 1045958633310927219312709804664751888613212 630290400061572206887148711804214366640362
      4345735874637809770754784814922852658776494 1045958633310927219312709804666950911868764
      630290400061572206887148711806413389895914 4345735874637809770754784814925051682032046 = 2) :
    p.eval (xs 0) (xs 1) (xs 2) < 0 := by
  rw [boxSignN_eq] at h
  exact (p.boxSign_sound hd KBox.QS (by decide) KBox.LS KBox.HS xs xs_bounds).2 h

/-- the named quantities of the rebuilt figure -/
noncomputable def W (i : Nat) : ℝ := (nth (ZP.nil, ZP.one) T i).1.eval eu et eS / (nth (ZP.nil, ZP.one) T i).2.eval eu et eS

lemma inv_W (i : Nat) (h : (nth (ZP.nil, ZP.one) T i).2.eval eu et eS ≠ 0) : Inv T W eu et eS i :=
  ⟨div_mul_cancel₀ _ h, h⟩
lemma inv_W0 : Inv T W eu et eS 0 := inv_W 0 (by show D0.eval _ _ _ ≠ 0; simp [D0, ZP.eval])
lemma inv_W1 : Inv T W eu et eS 1 := inv_W 1 (by show D1.eval _ _ _ ≠ 0; simp [D1, ZP.eval])
lemma inv_W2 : Inv T W eu et eS 2 := inv_W 2 (by show D2.eval _ _ _ ≠ 0; simp [D2, ZP.eval])
lemma W0 : W 0 = eu := by show N0.eval _ _ _ / D0.eval _ _ _ = eu; simp [N0, D0, ZP.eval]
lemma W1 : W 1 = et := by show N1.eval _ _ _ / D1.eval _ _ _ = et; simp [N1, D1, ZP.eval]
lemma W2 : W 2 = eS := by show N2.eval _ _ _ / D2.eval _ _ _ = eS; simp [N2, D2, ZP.eval]
lemma W0_pos : 0 < W 0 := by rw [W0]; exact eu_pos

end YantraCert.Y
