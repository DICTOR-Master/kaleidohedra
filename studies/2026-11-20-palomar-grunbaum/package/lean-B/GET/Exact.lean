module

public import GET.CellVolume

@[expose] public section

/-!
# Exact vectors in `Space`

A vector with coordinates in `ℤ[φ]` is evaluated in Euclidean 3-space by `ev`. Equality, inner products, norms,
parallelism and linear independence of evaluated vectors are decided by exact computations on `ZPhi`.
-/

namespace GET

open ZPhi GrunbaumK10

/-- an exact vector as a point of `Space` -/
noncomputable def ev (x : Fin 3 → ZPhi) : Space := WithLp.toLp 2 (rv x)

theorem ev_apply (x : Fin 3 → ZPhi) (c : Fin 3) : ev x c = toReal (x c) := rfl

theorem rv_add (x y : Fin 3 → ZPhi) : rv (x + y) = rv x + rv y := by
  funext c; simp [rv, toReal_add]

theorem rv_sub (x y : Fin 3 → ZPhi) : rv (x - y) = rv x - rv y := by
  funext c; simp [rv, toReal_sub]

theorem rv_neg (x : Fin 3 → ZPhi) : rv (-x) = -rv x := by
  funext c; simp [rv, toReal_neg]

theorem rv_zero : rv (0 : Fin 3 → ZPhi) = 0 := by
  funext c; simp [rv]; exact toReal_zero

theorem ev_add (x y : Fin 3 → ZPhi) : ev (x + y) = ev x + ev y := by
  simp [ev, rv_add]

theorem ev_sub (x y : Fin 3 → ZPhi) : ev (x - y) = ev x - ev y := by
  simp [ev, rv_sub]

theorem ev_neg (x : Fin 3 → ZPhi) : ev (-x) = -ev x := by
  simp [ev, rv_neg]

theorem ev_zero : ev 0 = 0 := by
  simp [ev, rv_zero]

theorem rv_injective : Function.Injective rv := by
  intro x y h
  funext c
  exact toReal_injective (congrFun h c)

theorem ev_injective : Function.Injective ev := by
  intro x y h
  exact rv_injective (WithLp.toLp_injective 2 h)

theorem ev_eq_iff {x y : Fin 3 → ZPhi} : ev x = ev y ↔ x = y := ev_injective.eq_iff

theorem ev_eq_zero_iff {x : Fin 3 → ZPhi} : ev x = 0 ↔ x = 0 := by
  rw [← ev_zero, ev_eq_iff]

/-- inner products are exact dot products -/
theorem inner_ev (x y : Fin 3 → ZPhi) : inner ℝ (ev x) (ev y) = toReal (dot x y) := by
  simp only [PiLp.inner_apply, ev, PiLp.toLp_apply, rv, Fin.sum_univ_three, dot, toReal_add, toReal_mul,
    RCLike.inner_apply, conj_trivial]
  ring

theorem norm_ev_sq (x : Fin 3 → ZPhi) : ‖ev x‖ ^ 2 = toReal (dot x x) := by
  rw [← real_inner_self_eq_norm_sq, inner_ev]

theorem norm_ev (x : Fin 3 → ZPhi) : ‖ev x‖ = Real.sqrt (toReal (dot x x)) := by
  rw [← norm_ev_sq, Real.sqrt_sq (norm_nonneg _)]

/-! ## Cross products and parallelism -/

/-- the exact cross product -/
def xcross (u v : Fin 3 → ZPhi) : Fin 3 → ZPhi :=
  ![u 1 * v 2 - u 2 * v 1, u 2 * v 0 - u 0 * v 2, u 0 * v 1 - u 1 * v 0]

theorem rv_xcross (u v : Fin 3 → ZPhi) : rv (xcross u v) = crossProduct (rv u) (rv v) := by
  funext c
  fin_cases c <;> simp [rv, xcross, cross_apply, toReal_sub, toReal_mul]

/-- `ev d` is a non-zero multiple of `ev w` exactly when `d ≠ 0` and `d × w = 0` (for `w ≠ 0`) -/
theorem parallel_iff {d w : Fin 3 → ZPhi} (hw : w ≠ 0) :
    (∃ c : ℝ, c ≠ 0 ∧ ev d = c • ev w) ↔ (d ≠ 0 ∧ xcross d w = 0) := by
  have hw' : rv w ≠ 0 := by
    intro h; apply hw; apply rv_injective; rw [h, rv_zero]
  constructor
  · rintro ⟨c, hc, h⟩
    have h' : rv d = c • rv w := WithLp.toLp_injective 2 (by rw [WithLp.toLp_smul]; exact h)
    refine ⟨?_, ?_⟩
    · rintro rfl
      rw [rv_zero] at h'
      exact hw' ((smul_eq_zero.mp h'.symm).resolve_left hc)
    · apply rv_injective
      rw [rv_xcross, rv_zero, h', LinearMap.map_smul_of_tower, LinearMap.smul_apply, cross_self, smul_zero]
  · rintro ⟨hd, hx⟩
    have hd' : rv d ≠ 0 := by
      intro h; apply hd; apply rv_injective; rw [h, rv_zero]
    have hdep : ¬ LinearIndependent ℝ ![rv d, rv w] := by
      rw [← crossProduct_ne_zero_iff_linearIndependent, ← rv_xcross, hx, rv_zero]
      exact fun h => h rfl
    rw [LinearIndependent.pair_iff] at hdep
    push_neg at hdep
    obtain ⟨s, t, hst, hne⟩ := hdep
    have hs : s ≠ 0 := by
      intro hs
      rw [hs, zero_smul, zero_add] at hst
      exact hne hs ((smul_eq_zero.mp hst).resolve_right hw')
    refine ⟨-t / s, ?_, ?_⟩
    · intro h
      have ht : t = 0 := by
        rcases div_eq_zero_iff.mp h with h | h
        · exact neg_eq_zero.mp h
        · exact absurd h hs
      rw [ht, zero_smul, add_zero] at hst
      exact hd' ((smul_eq_zero.mp hst).resolve_left hs)
    · have : rv d = (-t / s) • rv w := by
        have h2 : s • rv d = -(t • rv w) := eq_neg_of_add_eq_zero_left hst
        rw [div_eq_inv_mul, mul_smul, neg_smul, ← h2, smul_smul, inv_mul_cancel₀ hs, one_smul]
      show WithLp.toLp 2 (rv d) = (-t / s) • WithLp.toLp 2 (rv w)
      rw [this, WithLp.toLp_smul]

/-! ## Linear independence from determinants -/

theorem rmat_rows (u v w : Fin 3 → ZPhi) : (fun r => (rmat u v w) r) = ![rv u, rv v, rv w] := by
  funext r; fin_cases r <;> rfl

/-- three exact vectors with non-zero determinant are linearly independent in `Space` -/
theorem linearIndependent_ev3 {u v w : Fin 3 → ZPhi} (h : det3 u v w ≠ 0) :
    LinearIndependent ℝ ![ev u, ev v, ev w] := by
  have hdet : (rmat u v w).det ≠ 0 := by
    rw [toReal_det3]
    intro h0; apply h; apply toReal_injective; rw [h0, toReal_zero]
  have hrows := Matrix.linearIndependent_rows_of_det_ne_zero hdet
  have h3 : LinearIndependent ℝ ![rv u, rv v, rv w] := by
    have := hrows
    rwa [show (fun r => (rmat u v w) r) = ![rv u, rv v, rv w] from rmat_rows u v w] at this
  have := h3.map' (WithLp.linearEquiv 2 ℝ (Fin 3 → ℝ)).symm.toLinearMap
    (LinearEquiv.ker _)
  convert this using 1
  funext r; fin_cases r <;> rfl

/-- two exact vectors with non-zero cross product are linearly independent in `Space` -/
theorem linearIndependent_ev2 {u v : Fin 3 → ZPhi} (h : xcross u v ≠ 0) :
    LinearIndependent ℝ ![ev u, ev v] := by
  have h2 : LinearIndependent ℝ ![rv u, rv v] := by
    rw [← crossProduct_ne_zero_iff_linearIndependent, ← rv_xcross]
    intro h0; apply h; apply rv_injective; rw [h0, rv_zero]
  have := h2.map' (WithLp.linearEquiv 2 ℝ (Fin 3 → ℝ)).symm.toLinearMap (LinearEquiv.ker _)
  convert this using 1
  funext r; fin_cases r <;> rfl

end GET
