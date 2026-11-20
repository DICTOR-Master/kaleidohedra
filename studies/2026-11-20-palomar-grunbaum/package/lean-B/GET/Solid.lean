module

public import GET.Faces

@[expose] public section

/-!
# The solid GET B in `Space`

`PB` is the union of the 16 golden rhombohedra `cellSet (CB i)`. This module proves the generic facts used for the
solid: cells as sets, slab bounds of a cell along an exact normal, thin sets (inside finitely many planes) are null and
have empty interior, `PB` is compact and the closure of its interior.
-/

namespace GET

open ZPhi GrunbaumK10 Set MeasureTheory
open scoped Pointwise

/-! ## Sign tests -/

/-- completeness of the sign test: a positive number is recognised -/
theorem pos_complete {x : ZPhi} (h : 0 < toReal x) : pos x = true := by
  rw [toReal_eq] at h
  have s0 : (0 : ℝ) < Real.sqrt 5 := by positivity
  have s2 : Real.sqrt 5 * Real.sqrt 5 = 5 := Real.mul_self_sqrt (by norm_num)
  unfold pos
  generalize hu : 2 * x.a + x.b = u at h ⊢
  generalize hv : x.b = v at h ⊢
  rcases lt_trichotomy u 0 with h1 | h1 | h1 <;> rcases lt_trichotomy v 0 with h2 | h2 | h2
  · exfalso
    have : (u : ℝ) < 0 := by exact_mod_cast h1
    have : (v : ℝ) < 0 := by exact_mod_cast h2
    nlinarith
  · exfalso
    have : (u : ℝ) < 0 := by exact_mod_cast h1
    subst h2; simp at h; linarith
  · have hu' : (u : ℝ) < 0 := by exact_mod_cast h1
    have hq : u * u < 5 * v * v := by
      have := mul_self_lt_mul_self (by linarith : (0 : ℝ) ≤ -u) (by linarith : -(u : ℝ) < v * Real.sqrt 5)
      have : (u : ℝ) * u < 5 * v * v := by nlinarith
      exact_mod_cast this
    simp [h1, h2, hq, h1.not_ge, h2.le, h2.ne']
  · exfalso
    have : (v : ℝ) < 0 := by exact_mod_cast h2
    subst h1; simp at h; nlinarith
  · exfalso; subst h1; subst h2; simp at h
  · simp [h1, h2, h2.le, h2.ne']
  · have hu' : (0 : ℝ) < u := by exact_mod_cast h1
    have hv' : (v : ℝ) < 0 := by exact_mod_cast h2
    have hq : 5 * v * v < u * u := by
      have := mul_self_lt_mul_self (by nlinarith : (0 : ℝ) ≤ -v * Real.sqrt 5)
        (by linarith : -(v : ℝ) * Real.sqrt 5 < u)
      have : (5 : ℝ) * v * v < u * u := by nlinarith
      exact_mod_cast this
    simp [h1, h2, hq, h1.le, h2.not_ge, h1.ne']
  · subst h2; simp [h1, h1.le, h1.ne']
  · simp [h1, h2, h1.le, h2.le, h1.ne']

theorem not_pos_le {x : ZPhi} (h : pos x = false) : toReal x ≤ 0 := by
  by_contra hc
  push Not at hc
  rw [pos_complete hc] at h
  exact Bool.noConfusion h

/-! ## Cells -/

/-- the axis `eᵢ` in `Space` -/
noncomputable def ax (i : Fin 6) : Space := ev (axis i)

/-- the golden rhombohedron of a cell -/
noncomputable def cellSet (c : Cell) : Set Space :=
  ev (posn c.p) +ᵥ parallelepiped ![ax c.i, ax c.j, ax c.k]

theorem mem_cellSet {c : Cell} {z : Space} : z ∈ cellSet c ↔
    ∃ t : Fin 3 → ℝ, (∀ k, t k ∈ Icc (0 : ℝ) 1) ∧
      z = ev (posn c.p) + (t 0 • ax c.i + t 1 • ax c.j + t 2 • ax c.k) := by
  rw [cellSet, Set.mem_vadd_set]
  simp only [mem_parallelepiped_iff, vadd_eq_add, Fin.sum_univ_three, Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.cons_val_two, Matrix.head_cons, Matrix.tail_cons]
  constructor
  · rintro ⟨s, ⟨t, ht, rfl⟩, rfl⟩
    exact ⟨t, fun k => ⟨ht.1 k, ht.2 k⟩, rfl⟩
  · rintro ⟨t, ht, rfl⟩
    exact ⟨_, ⟨t, ⟨fun k => (ht k).1, fun k => (ht k).2⟩, rfl⟩, rfl⟩

theorem cellSet_eq_image (c : Cell) : cellSet c =
    (fun t : Fin 3 → ℝ => ev (posn c.p) + (t 0 • ax c.i + t 1 • ax c.j + t 2 • ax c.k)) '' Icc 0 1 := by
  ext z
  rw [mem_cellSet]
  constructor
  · rintro ⟨t, ht, rfl⟩
    exact ⟨t, ⟨fun k => (ht k).1, fun k => (ht k).2⟩, rfl⟩
  · rintro ⟨t, ht, rfl⟩
    exact ⟨t, fun k => ⟨ht.1 k, ht.2 k⟩, rfl⟩

theorem isCompact_cellSet (c : Cell) : IsCompact (cellSet c) := by
  rw [cellSet_eq_image]
  exact isCompact_Icc.image (by fun_prop)

theorem mem_cellSet_of (c : Cell) (t : Fin 3 → ℝ) (ht : ∀ k, t k ∈ Icc (0 : ℝ) 1) :
    ev (posn c.p) + (t 0 • ax c.i + t 1 • ax c.j + t 2 • ax c.k) ∈ cellSet c :=
  mem_cellSet.mpr ⟨t, ht, rfl⟩

/-- a cell with independent axes is the closure of its interior -/
theorem closure_interior_cellSet (c : Cell) (h : det3 (axis c.i) (axis c.j) (axis c.k) ≠ 0) :
    closure (interior (cellSet c)) = cellSet c := by
  have hconv : Convex ℝ (cellSet c) := (convex_parallelepiped _).vadd _
  have hli := linearIndependent_ev3 h
  have hint : (interior (cellSet c)).Nonempty := by
    rw [hconv.interior_nonempty_iff_affineSpan_eq_top]
    have hq : ev (posn c.p) ∈ cellSet c := by
      simpa using mem_cellSet_of c 0 (fun k => ⟨le_refl _, zero_le_one⟩)
    rw [AffineSubspace.affineSpan_eq_top_iff_vectorSpan_eq_top_of_nonempty ℝ Space Space ⟨_, hq⟩]
    have hv : ∀ k : Fin 3, (![ax c.i, ax c.j, ax c.k] : Fin 3 → Space) k ∈ vectorSpan ℝ (cellSet c) := by
      intro k
      have hk : ev (posn c.p) + (![ax c.i, ax c.j, ax c.k] : Fin 3 → Space) k ∈ cellSet c := by
        have := mem_cellSet_of c (Pi.single k 1) (fun l => by
          by_cases hl : l = k
          · subst hl; simp
          · simp [Pi.single_apply, hl])
        fin_cases k <;> simpa using this
      have := vsub_mem_vectorSpan ℝ hk hq
      simpa using this
    have htop : Submodule.span ℝ (range ![ax c.i, ax c.j, ax c.k]) = ⊤ :=
      hli.span_eq_top_of_card_eq_finrank (by simp)
    rw [eq_top_iff, ← htop, Submodule.span_le]
    rintro _ ⟨k, rfl⟩
    exact hv k
  rw [hconv.closure_interior_eq_closure_of_nonempty_interior hint, (isCompact_cellSet c).isClosed.closure_eq]

/-! ## Slab bounds of a cell along an exact normal -/

/-- the negative part, decided exactly -/
def negPart (a : ZPhi) : ZPhi := if pos a then 0 else a
/-- the positive part, decided exactly -/
def posPart (a : ZPhi) : ZPhi := if pos a then a else 0

/-- lower and upper bounds of `n · x` over a cell -/
def cellLo (n : Fin 3 → ZPhi) (c : Cell) : ZPhi :=
  dot n (posn c.p) + negPart (dot n (axis c.i)) + negPart (dot n (axis c.j)) + negPart (dot n (axis c.k))
def cellHi (n : Fin 3 → ZPhi) (c : Cell) : ZPhi :=
  dot n (posn c.p) + posPart (dot n (axis c.i)) + posPart (dot n (axis c.j)) + posPart (dot n (axis c.k))

theorem part_bounds (a : ZPhi) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) 1) :
    toReal (negPart a) ≤ t * toReal a ∧ t * toReal a ≤ toReal (posPart a) := by
  obtain ⟨h0, h1⟩ := ht
  unfold negPart posPart
  split_ifs with h
  · have := pos_sound h
    rw [toReal_zero]; constructor <;> nlinarith
  · have := not_pos_le (Bool.eq_false_iff.mpr h)
    rw [toReal_zero]; constructor <;> nlinarith

theorem cell_bounds (n : Fin 3 → ZPhi) (c : Cell) {z : Space} (hz : z ∈ cellSet c) :
    toReal (cellLo n c) ≤ inner ℝ (ev n) z ∧ inner ℝ (ev n) z ≤ toReal (cellHi n c) := by
  obtain ⟨t, ht, rfl⟩ := mem_cellSet.mp hz
  simp only [inner_add_right, inner_smul_right, ax, inner_ev, cellLo, cellHi, toReal_add]
  have h0 := part_bounds (dot n (axis c.i)) (ht 0)
  have h1 := part_bounds (dot n (axis c.j)) (ht 1)
  have h2 := part_bounds (dot n (axis c.k)) (ht 2)
  constructor <;> linarith [h0.1, h0.2, h1.1, h1.2, h2.1, h2.2]

/-! ## Thin sets -/

/-- a plane `{z | N · z = c}` -/
def plane (N : Space) (c : ℝ) : Set Space := {z | inner ℝ N z = c}

theorem volume_plane {N : Space} (hN : N ≠ 0) (c : ℝ) : volume (plane N c) = 0 := by
  let A : AffineSubspace ℝ Space := AffineSubspace.mk' ((c / ‖N‖ ^ 2) • N) (LinearMap.ker (innerₛₗ ℝ N))
  have hNN : inner ℝ N N = ‖N‖ ^ 2 := real_inner_self_eq_norm_sq N
  have hN2 : ‖N‖ ^ 2 ≠ 0 := by positivity
  have hsub : plane N c ⊆ A := by
    intro z hz
    simp only [plane, mem_ofPred_eq] at hz
    rw [SetLike.mem_coe, AffineSubspace.mem_mk', LinearMap.mem_ker, innerₛₗ_apply_apply, vsub_eq_sub,
      inner_sub_right, inner_smul_right, hNN, hz, div_mul_cancel₀ _ hN2, sub_self]
  have hA : A ≠ ⊤ := by
    intro htop
    have : (c / ‖N‖ ^ 2) • N + N ∈ A := by rw [htop]; exact AffineSubspace.mem_top ℝ Space _
    rw [AffineSubspace.mem_mk', LinearMap.mem_ker, innerₛₗ_apply_apply, vsub_eq_sub, add_sub_cancel_left,
      hNN] at this
    exact hN2 this
  exact measure_mono_null hsub (Measure.addHaar_affineSubspace volume A hA)

theorem interior_eq_empty_of_null {S : Set Space} (h : volume S = 0) : interior S = ∅ := by
  by_contra hne
  have := Measure.measure_pos_of_nonempty_interior volume (Set.nonempty_iff_ne_empty.mpr hne)
  rw [h] at this
  exact lt_irrefl _ this

end GET
