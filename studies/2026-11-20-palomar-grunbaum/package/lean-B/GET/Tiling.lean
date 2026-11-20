module

public import GET.Solid

@[expose] public section

/-!
# GET B, its lattice, and the disjointness of its translates

`PB` is the union of the 16 cells `cellSet (CB i)`; the lattice is spanned by `bB`. Every lattice vector is `lat x`
for an integer vector `x`. Two distinct cells of `PB`, and a cell of `PB` and a cell of a translate `lat x + PB`
(`x ≠ 0`), meet inside a plane: the exact checks give a separating normal for the 26 vectors `x ∈ {-1,0,1}³ \ 0`,
and the dual normals `mB` show that no other translate meets `PB` at all. Hence `PB ∩ (t + PB)` is null for every
non-zero lattice vector `t`, and the interiors of distinct translates are disjoint. The volume of `PB` is
`20 + 32 φ`, the covolume of the lattice.
-/

namespace GET

open ZPhi GrunbaumK10 Set MeasureTheory
open scoped Pointwise

/-! ## Positions -/

theorem rv_posn (p : Fin 6 → ℤ) : rv (posn p) = ∑ i, (p i : ℝ) • rv (axis i) := by
  funext c
  simp only [rv, posn, toReal_lsum, List.map_map, Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  rw [Fin.sum_univ_def]
  congr 1
  apply List.map_congr_left
  intro i _
  simp [toReal_mul, toReal_ofInt]

theorem ev_posn (p : Fin 6 → ℤ) : ev (posn p) = ∑ i, (p i : ℝ) • ax i := by
  unfold ev ax ev
  rw [rv_posn]
  simp only [Fin.sum_univ_six, WithLp.toLp_add, WithLp.toLp_smul]

/-! ## The lattice -/

/-- the lattice basis of GET B in `ℤ⁶` -/
def BB : Fin 3 → Fin 6 → ℤ := ![![1, 0, 0, -1, 0, -1], ![0, -1, 0, 0, 1, -1], ![0, 0, 1, 1, 1, 0]]

theorem BB_eq : basisB = [BB 0, BB 1, BB 2] := by decide +kernel

/-- the lattice basis in `Space` -/
noncomputable def bB (r : Fin 3) : Space := ev (posn (BB r))

/-- the lattice vector with integer coordinates `x` -/
noncomputable def lat (x : Fin 3 → ℤ) : Space := ∑ r, (x r : ℝ) • bB r

/-- the same vector in `ℤ⁶` -/
def lv (x : Fin 3 → ℤ) : Fin 6 → ℤ := fun c => x 0 * BB 0 c + x 1 * BB 1 c + x 2 * BB 2 c

theorem ev_posn_add_lv (p : Fin 6 → ℤ) (x : Fin 3 → ℤ) : ev (posn (p + lv x)) = ev (posn p) + lat x := by
  simp only [ev_posn, lat, bB, Fin.sum_univ_six, Fin.sum_univ_three, Pi.add_apply, lv]
  push_cast
  module

theorem lat_add (x y : Fin 3 → ℤ) : lat (x + y) = lat x + lat y := by
  simp only [lat, Fin.sum_univ_three, Pi.add_apply]; push_cast; module

theorem lat_sub (x y : Fin 3 → ℤ) : lat (x - y) = lat x - lat y := by
  simp only [lat, Fin.sum_univ_three, Pi.sub_apply]; push_cast; module

theorem mem_lattice {t : Space} : t ∈ lattice bB ↔ ∃ x, t = lat x := by
  unfold lattice lat
  rw [SetLike.mem_coe, AddSubgroup.mem_closure_range_iff_of_fintype]
  simp only [Int.cast_smul_eq_zsmul]

theorem lat_mem (x : Fin 3 → ℤ) : lat x ∈ lattice bB := mem_lattice.mpr ⟨x, rfl⟩

/-! ## The cells -/

/-- the 16 cells of GET B -/
def CB (i : Fin 16) : Cell := cellsB.getD i ⟨fun _ => 0, 0, 0, 0⟩

/-- the solid GET B -/
noncomputable def PB : Set Space := ⋃ i, cellSet (CB i)

theorem cellSet_shift (c : Cell) (x : Fin 3 → ℤ) : cellSet (c.shift (lv x)) = lat x +ᵥ cellSet c := by
  unfold cellSet Cell.shift
  simp only [ev_posn_add_lv, vadd_vadd]
  rw [add_comm]

/-! ## Separation -/

/-- the normal `eₓ × e_y` -/
def nrm (x y : Fin 6) : Fin 3 → ZPhi := xcross (axis x) (axis y)

/-- the normal `n` separates the cells `c` and `d` (weakly) -/
def sepN (n : Fin 3 → ZPhi) (c d : Cell) : Bool :=
  nonneg (cellLo n d - cellHi n c) || nonneg (cellLo n c - cellHi n d)

/-- one of the 15 normals separates the cells -/
def sep (c d : Cell) : Bool := pairs15.any fun xy => sepN (nrm xy.1 xy.2) c d

theorem pairs15_nrm : ∀ xy ∈ pairs15, nrm xy.1 xy.2 ≠ 0 := by decide +kernel

theorem sepN_sound {n : Fin 3 → ZPhi} (hn : n ≠ 0) {c d : Cell} (h : sepN n c d = true) :
    ∃ N : Space, N ≠ 0 ∧ ∃ k, cellSet c ∩ cellSet d ⊆ plane N k := by
  refine ⟨ev n, fun h0 => hn (ev_eq_zero_iff.mp h0), ?_⟩
  simp only [sepN, Bool.or_eq_true] at h
  rcases h with h | h
  · refine ⟨toReal (cellHi n c), ?_⟩
    rintro z ⟨hc, hd⟩
    have h1 := cell_bounds n c hc
    have h2 := cell_bounds n d hd
    have h3 := nonneg_sound h
    rw [toReal_sub] at h3
    show inner ℝ (ev n) z = _
    linarith [h1.2, h2.1]
  · refine ⟨toReal (cellLo n c), ?_⟩
    rintro z ⟨hc, hd⟩
    have h1 := cell_bounds n c hc
    have h2 := cell_bounds n d hd
    have h3 := nonneg_sound h
    rw [toReal_sub] at h3
    show inner ℝ (ev n) z = _
    linarith [h1.1, h2.2]

theorem sep_sound {c d : Cell} (h : sep c d = true) :
    ∃ N : Space, N ≠ 0 ∧ ∃ k, cellSet c ∩ cellSet d ⊆ plane N k := by
  simp only [sep, List.any_eq_true] at h
  obtain ⟨xy, hxy, h⟩ := h
  exact sepN_sound (pairs15_nrm xy hxy) h

theorem null_of_sep {c d : Cell} (h : sep c d = true) : volume (cellSet c ∩ cellSet d) = 0 := by
  obtain ⟨N, hN, k, hk⟩ := sep_sound h
  exact measure_mono_null hk (volume_plane hN k)

/-- the 16 cells pairwise do not cross -/
theorem B_cells_sep : ∀ i j : Fin 16, i ≠ j → sep (CB i) (CB j) = true := by decide +kernel

/-- the coefficients `-1, 0, 1` -/
def L3 : List ℤ := [-1, 0, 1]

/-- no cell of `PB` crosses a cell of `lat x + PB`, for the 26 vectors `x ∈ {-1,0,1}³ \ 0` -/
theorem B_trans_sep : ∀ a ∈ L3, ∀ b ∈ L3, ∀ c ∈ L3, ¬ (a = 0 ∧ b = 0 ∧ c = 0) →
    ∀ i j : Fin 16, sep (CB i) ((CB j).shift (lv ![a, b, c])) = true := by decide +kernel

/-! ## Only the 26 neighbours can touch -/

/-- the dual normals: `mB r · b_{r'} = δ` if `r = r'`, else `0` -/
def mB : Fin 3 → Fin 3 → ZPhi :=
  ![![⟨2, 3⟩, ⟨5, 8⟩, ⟨-1, -1⟩], ![⟨3, 5⟩, ⟨-4, -7⟩, ⟨-1, -2⟩], ![⟨1, 2⟩, ⟨3, 5⟩, ⟨4, 7⟩]]

/-- `δ = 20 + 32 φ` -/
def δB : ZPhi := ⟨20, 32⟩

theorem mB_dual : ∀ r r' : Fin 3, dot (mB r) (posn (BB r')) = if r = r' then δB else 0 := by decide +kernel

/-- the width of `PB` along each dual normal is less than `2 δ` -/
theorem B_bound : ∀ r : Fin 3, ∀ i j : Fin 16,
    pos (⟨2, 0⟩ * δB - (cellHi (mB r) (CB i) - cellLo (mB r) (CB j))) = true := by decide +kernel

theorem δB_pos : 0 < toReal δB := pos_sound (by decide +kernel)

theorem inner_mB_lat (r : Fin 3) (x : Fin 3 → ℤ) : inner ℝ (ev (mB r)) (lat x) = x r * toReal δB := by
  simp only [lat, Fin.sum_univ_three, inner_add_right, inner_smul_right, bB, inner_ev, mB_dual]
  fin_cases r <;> simp [toReal_zero]

theorem coeff_bound {i j : Fin 16} {x : Fin 3 → ℤ} (h : (cellSet (CB i) ∩ (lat x +ᵥ cellSet (CB j))).Nonempty)
    (r : Fin 3) : -1 ≤ x r ∧ x r ≤ 1 := by
  obtain ⟨z, hz1, hz2⟩ := h
  obtain ⟨w, hw, rfl⟩ := Set.mem_vadd_set.mp hz2
  have b1 := cell_bounds (mB r) _ hz1
  have b2 := cell_bounds (mB r) _ hw
  have e : inner ℝ (ev (mB r)) (lat x +ᵥ w) = x r * toReal δB + inner ℝ (ev (mB r)) w := by
    rw [vadd_eq_add, inner_add_right, inner_mB_lat]
  have c1 := pos_sound (B_bound r i j)
  have c2 := pos_sound (B_bound r j i)
  rw [toReal_sub, toReal_mul, toReal_sub] at c1 c2
  have h2 : toReal (⟨2, 0⟩ : ZPhi) = 2 := by simp [toReal]
  rw [h2] at c1 c2
  have hδ := δB_pos
  have u1 : (x r : ℝ) * toReal δB < 2 * toReal δB := by linarith [b1.2, b2.1]
  have u2 : -(2 * toReal δB) < (x r : ℝ) * toReal δB := by linarith [b1.1, b2.2]
  have v1 : (x r : ℝ) < 2 := by nlinarith
  have v2 : (-2 : ℝ) < x r := by nlinarith
  constructor
  · have : (-2 : ℤ) < x r := by exact_mod_cast v2
    omega
  · have : x r < 2 := by exact_mod_cast v1
    omega

theorem pair_null (i j : Fin 16) {x : Fin 3 → ℤ} (hx : x ≠ 0) :
    volume (cellSet (CB i) ∩ (lat x +ᵥ cellSet (CB j))) = 0 := by
  by_cases h : (cellSet (CB i) ∩ (lat x +ᵥ cellSet (CB j))).Nonempty
  · have hb := coeff_bound h
    have hx3 : x = ![x 0, x 1, x 2] := by funext k; fin_cases k <;> rfl
    have m : ∀ r, x r ∈ L3 := by
      intro r; have := hb r; simp only [L3, List.mem_cons, List.not_mem_nil, or_false]; omega
    have hnz : ¬ (x 0 = 0 ∧ x 1 = 0 ∧ x 2 = 0) := by
      rintro ⟨h0, h1, h2⟩; apply hx; rw [hx3, h0, h1, h2]; funext k; fin_cases k <;> rfl
    have hs := B_trans_sep _ (m 0) _ (m 1) _ (m 2) hnz i j
    rw [← hx3] at hs
    have := null_of_sep hs
    rwa [cellSet_shift] at this
  · rw [Set.not_nonempty_iff_eq_empty] at h
    rw [h, measure_empty]

theorem PB_inter_null {x : Fin 3 → ℤ} (hx : x ≠ 0) : volume (PB ∩ (lat x +ᵥ PB)) = 0 := by
  apply measure_mono_null (t := ⋃ i, ⋃ j, cellSet (CB i) ∩ (lat x +ᵥ cellSet (CB j)))
  · rintro z ⟨hz1, hz2⟩
    obtain ⟨w, hw, rfl⟩ := Set.mem_vadd_set.mp hz2
    simp only [PB, mem_iUnion] at hz1 hw ⊢
    obtain ⟨i, hi⟩ := hz1
    obtain ⟨j, hj⟩ := hw
    exact ⟨i, j, hi, Set.vadd_mem_vadd_set hj⟩
  · exact measure_iUnion_null fun i => measure_iUnion_null fun j => pair_null i j hx

/-- **the interiors of distinct lattice translates of GET B are disjoint** -/
theorem PB_disjoint : (lattice bB).Pairwise fun s t => Disjoint (interior (s +ᵥ PB)) (interior (t +ᵥ PB)) := by
  intro s hs t ht hst
  obtain ⟨xs, rfl⟩ := mem_lattice.mp hs
  obtain ⟨xt, rfl⟩ := mem_lattice.mp ht
  rw [Set.disjoint_iff_inter_eq_empty, ← interior_inter]
  apply interior_eq_empty_of_null
  have e : (lat xs +ᵥ PB) ∩ (lat xt +ᵥ PB) = lat xs +ᵥ (PB ∩ (lat (xt - xs) +ᵥ PB)) := by
    rw [Set.vadd_set_inter, vadd_vadd, lat_sub, add_sub_cancel]
  rw [e, measure_vadd]
  apply PB_inter_null
  intro h0
  apply hst
  rw [show xt = xs by rw [← sub_eq_zero]; exact h0]

theorem PB_cells_null {i j : Fin 16} (h : i ≠ j) : volume (cellSet (CB i) ∩ cellSet (CB j)) = 0 :=
  null_of_sep (B_cells_sep i j h)

end GET
