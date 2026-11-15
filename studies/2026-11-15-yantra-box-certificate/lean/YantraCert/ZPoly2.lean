import YantraCert.ZPoly

/-!
# Signed polynomials as integer polynomials, and rescaling (Lean core only)

`ZP.ofSP` turns a stored signed polynomial `P⁺ - P⁻` of the certificate into an integer polynomial (sorted by `ZP.norm`, an
insertion sort through `ZP.add`). `ZP.scaleW` substitutes `x_j ↦ (n_j / d_j) x_j` and multiplies by `∏ d_j^(D_j)`, so that it
stays integral. Soundness is in `YantraCert.ZPoly2Sound`.
-/

namespace YantraCert

noncomputable def ZP.ofNP (neg : Bool) (p : NP) : ZP :=
  NP.rec (motive := fun _ => ZP) .nil (fun c a b e _ ih => .cons (cond neg (-(c : Int)) (c : Int)) a b e ih) p

/-- insertion sort (through the merge of `ZP.add`) -/
noncomputable def ZP.norm (p : ZP) : ZP :=
  ZP.rec (motive := fun _ => ZP) .nil (fun c a b e _ ih => ZP.add (.cons c a b e .nil) ih) p

noncomputable def ZP.ofSP (p : SP) : ZP := ZP.norm (ZP.app (ZP.ofNP false p.pp) (ZP.ofNP true p.pn))

/-- `Σ c n0^a d0^(D0-a) n1^b d1^(D1-b) n2^e d2^(D2-e) x^a y^b z^e` -/
noncomputable def ZP.scaleW (n0 d0 D0 n1 d1 D1 n2 d2 D2 : Nat) (p : ZP) : ZP :=
  ZP.rec (motive := fun _ => ZP) .nil (fun c a b e _ ih =>
    .cons (c * ((n0 ^ a * d0 ^ (D0 - a) * (n1 ^ b * d1 ^ (D1 - b)) * (n2 ^ e * d2 ^ (D2 - e)) : Nat) : Int)) a b e ih) p

noncomputable def ZP.degLE (D0 D1 D2 : Nat) (p : ZP) : Bool :=
  ZP.rec (motive := fun _ => Bool) true (fun _ a b e _ ih => Nat.ble a D0 && Nat.ble b D1 && Nat.ble e D2 && ih) p

end YantraCert
