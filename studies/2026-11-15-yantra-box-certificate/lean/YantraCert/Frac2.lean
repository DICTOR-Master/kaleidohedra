module

public import YantraCert.Frac

@[expose] public section

namespace YantraCert

/-- **a step holds for quantities that are their stored fractions** (the converse of `step_inv`) -/
theorem step_of_inv (T : List (ZP × ZP)) (V : Nat → ℝ) (x y z : ℝ) (i : Nat) (d n : Ex) (K : ZP)
    (hok : stepOK T i d n K = true) (hI : ∀ j < i + 1, Inv T V x y z j) : V i * d.ev V = n.ev V := by
  unfold stepOK at hok
  simp only [Bool.and_eq_true] at hok
  obtain ⟨⟨⟨hbd, hbn⟩, h1⟩, h2⟩ := hok
  have hI' : ∀ j < i, Inv T V x y z j := fun j hj => hI j (by omega)
  obtain ⟨d1, d2⟩ := frac_sound T V x y z i hI' d hbd
  obtain ⟨n1, n2⟩ := frac_sound T V x y z i hI' n hbn
  obtain ⟨v1, v2⟩ := hI i (by omega)
  have e1 := ZP.eq_of_eqv h1 x y z
  have e2 := ZP.eq_of_eqv h2 x y z
  rw [ZP.eval_mul, ZP.eval_mul] at e1 e2
  have key : (V i * d.ev V - n.ev V) * ((Ex.frac T d).2.eval x y z * (Ex.frac T n).2.eval x y z) = 0 := by
    linear_combination V i * (Ex.frac T n).2.eval x y z * d1 - V i * e1 + K.eval x y z * v1 + e2 -
      (Ex.frac T d).2.eval x y z * n1
  rcases mul_eq_zero.mp key with h | h
  · linarith
  · exact absurd h (mul_ne_zero d2 n2)

end YantraCert
