module

public import GET.Checks

@[expose] public section

/-! Pilot bridge from the exact checks to `ℝ`: volume = covolume as an identity of real determinants (GET B). -/

namespace GET

open ZPhi

/-- a `ZPhi` vector evaluated in `ℝ³` -/
noncomputable def rv (v : Fin 3 → ZPhi) : Fin 3 → ℝ := fun c => toReal (v c)

/-- the real 3 × 3 matrix with rows `u, v, w` -/
noncomputable def rmat (u v w : Fin 3 → ZPhi) : Matrix (Fin 3) (Fin 3) ℝ := Matrix.of ![rv u, rv v, rv w]

theorem toReal_det3 (u v w : Fin 3 → ZPhi) : (rmat u v w).det = toReal (det3 u v w) := by
  simp only [rmat, rv, Matrix.det_fin_three, Matrix.of_apply, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.cons_val_two, Matrix.head_cons, Matrix.tail_cons, det3, toReal_add, toReal_sub, toReal_mul]
  ring

theorem toReal_lsum (l : List ZPhi) : toReal (lsum l) = (l.map toReal).sum := by
  induction l with
  | nil => exact toReal_zero
  | cons x l ih => simp only [lsum, List.foldr_cons, List.map_cons, List.sum_cons] at *; rw [toReal_add, ih]

theorem toReal_zabs {x : ZPhi} (h : pos x = true ∨ pos (-x) = true) : toReal (zabs x) = |toReal x| := by
  unfold zabs
  split_ifs with hx
  · rw [abs_of_pos (pos_sound hx)]
  · have h' := pos_sound (h.resolve_left hx)
    rw [toReal_neg] at h'
    rw [toReal_neg, abs_of_neg (by linarith)]

/-- every cell of GET B has a non-zero determinant of decided sign -/
theorem B_cell_signs : cellsB.all (fun c => pos (D c.i c.j c.k) || pos (-(D c.i c.j c.k))) = true := by
  decide +kernel

theorem B_basis_shape : basisB = [basisB[0]!, basisB[1]!, basisB[2]!] := by decide +kernel

theorem B_basis_sign :
    pos (det3 (posn basisB[0]!) (posn basisB[1]!) (posn basisB[2]!)) = true ∨
    pos (-(det3 (posn basisB[0]!) (posn basisB[1]!) (posn basisB[2]!))) = true := by
  right; decide +kernel

/-- **volume = covolume for GET B, over `ℝ`**: the sum of `|det(eᵢ, eⱼ, eₖ)|` over the 16 cells equals
`|det|` of the lattice basis (both are `20 + 32 φ`). -/
theorem B_volume_eq_covolume_real :
    (cellsB.map fun c => |(rmat (axis c.i) (axis c.j) (axis c.k)).det|).sum =
      |(rmat (posn basisB[0]!) (posn basisB[1]!) (posn basisB[2]!)).det| := by
  have hv := B_vol
  simp only [volEqCovol, beq_iff_eq] at hv
  have hcov : covol basisB = zabs (det3 (posn basisB[0]!) (posn basisB[1]!) (posn basisB[2]!)) := by
    rw [B_basis_shape]; rfl
  rw [toReal_det3, ← toReal_zabs B_basis_sign, ← hcov, ← hv, toReal_lsum, List.map_map]
  congr 1
  apply List.map_congr_left
  intro c hc
  have h : pos (D c.i c.j c.k) = true ∨ pos (-(D c.i c.j c.k)) = true := by
    have := B_cell_signs
    rw [List.all_eq_true] at this
    simpa using this c hc
  simp only [Function.comp_apply, cellVol]
  rw [toReal_zabs h, toReal_det3]
  rfl

/-- the common value, `20 + 32 φ` -/
theorem B_covolume_value :
    |(rmat (posn basisB[0]!) (posn basisB[1]!) (posn basisB[2]!)).det| = 20 + 32 * Real.goldenRatio := by
  rw [toReal_det3, ← toReal_zabs B_basis_sign]
  have : zabs (det3 (posn basisB[0]!) (posn basisB[1]!) (posn basisB[2]!)) = ⟨20, 32⟩ := by decide +kernel
  rw [this]; simp [toReal]

end GET
