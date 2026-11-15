module
public import Mathlib
@[expose] public section

/-!
# The octahedral constant 3: proof library (paper #43 "Kyushindo Cores", Theorem 4)

Copies of the definitions of `Challenge.lean`, in the namespace `KyushindoProof`,
with proofs of its four theorems; `Solution.lean` transfers them by definitional
unfolding.

Route: (a) the 24 rotations as an explicit list, checked by `decide`; (b) the
covering lemma by the moments of `t = ⟪g u, w⟫` over the 24 rotations (sum 0, sum
of squares `8 ‖u‖² ‖w‖²`, sum of cubes 0: the orbits are spherical 3-designs,
Delsarte–Goethals–Seidel 1977, Goethals–Seidel 1981) and the cubic
`(M - t)(t + M)²` of #43's proof; the bound itself is the known diameter of
`S²/O` (Greenwald 2000; Dunbar–Greenwald–McGowan–Searle 2009, Table 2);
(c) strict separation of a point from a finite convex hull (Mathlib's
`geometric_hahn_banach_closed_point`); (d) Theorem 4: every distance is at least
`‖x‖/√3`, and every direction meets a normal at angle at most `arccos (1/√3)`,
so `x/3` lies in the foot-point hull; (e) the cube is sharp.
-/
namespace KyushindoProof
open scoped RealInnerProductSpace Pointwise
abbrev E3 := EuclideanSpace ℝ (Fin 3)
noncomputable def signedPerm (σ : Equiv.Perm (Fin 3)) (s : Fin 3 → ℤˣ) (x : E3) : E3 :=
  WithLp.toLp 2 (fun i => ((s i : ℤ) : ℝ) * x (σ i))
def IsOctahedralRotation (σ : Equiv.Perm (Fin 3)) (s : Fin 3 → ℤˣ) : Prop :=
  ((Equiv.Perm.sign σ : ℤˣ) : ℤ) * ∏ i, ((s i : ℤˣ) : ℤ) = 1

/-! ## (a) The 24 rotations, listed explicitly -/

/-- Sign vectors with product `1`. -/
def evenSigns : Fin 4 → Fin 3 → ℤˣ := ![![1, 1, 1], ![1, -1, -1], ![-1, 1, -1], ![-1, -1, 1]]
/-- Sign vectors with product `-1`. -/
def oddSigns : Fin 4 → Fin 3 → ℤˣ := ![![-1, -1, -1], ![-1, 1, 1], ![1, -1, 1], ![1, 1, -1]]

/-- The 24 rotations of the octahedral group as signed permutations. -/
def rot : Fin 24 → Equiv.Perm (Fin 3) × (Fin 3 → ℤˣ) :=
  ![((1 : Equiv.Perm (Fin 3)), evenSigns 0),
    ((1 : Equiv.Perm (Fin 3)), evenSigns 1),
    ((1 : Equiv.Perm (Fin 3)), evenSigns 2),
    ((1 : Equiv.Perm (Fin 3)), evenSigns 3),
    ((Equiv.swap 0 1 : Equiv.Perm (Fin 3)), oddSigns 0),
    ((Equiv.swap 0 1 : Equiv.Perm (Fin 3)), oddSigns 1),
    ((Equiv.swap 0 1 : Equiv.Perm (Fin 3)), oddSigns 2),
    ((Equiv.swap 0 1 : Equiv.Perm (Fin 3)), oddSigns 3),
    ((Equiv.swap 0 2 : Equiv.Perm (Fin 3)), oddSigns 0),
    ((Equiv.swap 0 2 : Equiv.Perm (Fin 3)), oddSigns 1),
    ((Equiv.swap 0 2 : Equiv.Perm (Fin 3)), oddSigns 2),
    ((Equiv.swap 0 2 : Equiv.Perm (Fin 3)), oddSigns 3),
    ((Equiv.swap 1 2 : Equiv.Perm (Fin 3)), oddSigns 0),
    ((Equiv.swap 1 2 : Equiv.Perm (Fin 3)), oddSigns 1),
    ((Equiv.swap 1 2 : Equiv.Perm (Fin 3)), oddSigns 2),
    ((Equiv.swap 1 2 : Equiv.Perm (Fin 3)), oddSigns 3),
    ((Equiv.swap 0 1 * Equiv.swap 1 2 : Equiv.Perm (Fin 3)), evenSigns 0),
    ((Equiv.swap 0 1 * Equiv.swap 1 2 : Equiv.Perm (Fin 3)), evenSigns 1),
    ((Equiv.swap 0 1 * Equiv.swap 1 2 : Equiv.Perm (Fin 3)), evenSigns 2),
    ((Equiv.swap 0 1 * Equiv.swap 1 2 : Equiv.Perm (Fin 3)), evenSigns 3),
    ((Equiv.swap 1 2 * Equiv.swap 0 1 : Equiv.Perm (Fin 3)), evenSigns 0),
    ((Equiv.swap 1 2 * Equiv.swap 0 1 : Equiv.Perm (Fin 3)), evenSigns 1),
    ((Equiv.swap 1 2 * Equiv.swap 0 1 : Equiv.Perm (Fin 3)), evenSigns 2),
    ((Equiv.swap 1 2 * Equiv.swap 0 1 : Equiv.Perm (Fin 3)), evenSigns 3)]

theorem rot_isOctahedralRotation : ∀ k, IsOctahedralRotation (rot k).1 (rot k).2 := by
  unfold IsOctahedralRotation; decide

theorem rot_injective : Function.Injective rot := by
  unfold Function.Injective; decide

/-- The list is the whole rotation group. -/
theorem rot_surjective (σ : Equiv.Perm (Fin 3)) (s : Fin 3 → ℤˣ)
    (h : IsOctahedralRotation σ s) : ∃ k, rot k = (σ, s) := by
  revert σ s; unfold IsOctahedralRotation; decide


/-! ## (b) The covering lemma -/

theorem inner_signedPerm (σ : Equiv.Perm (Fin 3)) (s : Fin 3 → ℤˣ) (x y : E3) :
    ⟪signedPerm σ s x, y⟫ = ∑ i, ((s i : ℤ) : ℝ) * x (σ i) * y i := by
  simp [PiLp.inner_apply, signedPerm, mul_comm, mul_left_comm]

theorem norm_sq_eq (x : E3) : ‖x‖ ^ 2 = x 0 ^ 2 + x 1 ^ 2 + x 2 ^ 2 := by
  rw [← real_inner_self_eq_norm_sq, PiLp.inner_apply, Fin.sum_univ_three]; simp [sq]

/-- Moment argument: 24 reals with moments `0, 24 M², 0` reach `M`. -/
theorem exists_ge_of_moments (t : Fin 24 → ℝ) (M : ℝ)
    (h1 : ∑ k, t k = 0) (h2 : ∑ k, t k ^ 2 = 24 * M ^ 2) (h3 : ∑ k, t k ^ 3 = 0) :
    ∃ k, M ≤ t k := by
  by_contra hcon
  push Not at hcon
  have hsum : ∑ k, (M - t k) * (t k + M) ^ 2 = 0 := by
    have : ∀ k, (M - t k) * (t k + M) ^ 2
        = M ^ 3 + M ^ 2 * t k - M * t k ^ 2 - t k ^ 3 := fun k => by ring
    simp only [this, Finset.sum_sub_distrib, Finset.sum_add_distrib, ← Finset.mul_sum,
      h1, h2, h3, Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    push_cast; ring
  have hne : ∃ k, t k + M ≠ 0 := by
    by_contra hall
    push Not at hall
    have : ∑ k, t k = ∑ _k : Fin 24, (-M) := Finset.sum_congr rfl fun k _ => by
      linarith [hall k]
    rw [h1] at this
    simp at this
    have h0 := hcon 0
    linarith [hall 0]
  obtain ⟨k0, hk0⟩ := hne
  have hpos : 0 < ∑ k, (M - t k) * (t k + M) ^ 2 := by
    apply Finset.sum_pos'
    · intro k _
      exact mul_nonneg (by linarith [hcon k]) (sq_nonneg _)
    · exact ⟨k0, Finset.mem_univ _, mul_pos (by linarith [hcon k0]) (by positivity)⟩
  linarith

/-- The covering lemma, general form: for all `u, w` some rotation `g` has
`‖u‖ ‖w‖ / √3 ≤ ⟪g u, w⟫`. -/
theorem covering_general (u w : E3) :
    ∃ σ s, IsOctahedralRotation σ s ∧ ‖u‖ * ‖w‖ / Real.sqrt 3 ≤ ⟪signedPerm σ s u, w⟫ := by
  set t : Fin 24 → ℝ := fun k => ⟪signedPerm (rot k).1 (rot k).2 u, w⟫ with ht
  have hs3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hs3p : 0 < Real.sqrt 3 := by positivity
  set M := ‖u‖ * ‖w‖ / Real.sqrt 3 with hMdef
  have hM2 : 24 * M ^ 2 = 8 * (‖u‖ ^ 2 * ‖w‖ ^ 2) := by
    rw [hMdef, div_pow, hs3]; ring
  have hu := norm_sq_eq u
  have hw := norm_sq_eq w
  have h1 : ∑ k, t k = 0 := by
    simp [ht, inner_signedPerm, Fin.sum_univ_succ, rot, evenSigns, oddSigns,
      Equiv.swap_apply_of_ne_of_ne, Equiv.Perm.mul_apply]
    ring
  have h2 : ∑ k, t k ^ 2 = 24 * M ^ 2 := by
    rw [hM2, hu, hw]
    simp [ht, inner_signedPerm, Fin.sum_univ_succ, rot, evenSigns, oddSigns,
      Equiv.swap_apply_of_ne_of_ne, Equiv.Perm.mul_apply]
    ring
  have h3 : ∑ k, t k ^ 3 = 0 := by
    simp [ht, inner_signedPerm, Fin.sum_univ_succ, rot, evenSigns, oddSigns,
      Equiv.swap_apply_of_ne_of_ne, Equiv.Perm.mul_apply]
    ring
  obtain ⟨k, hk⟩ := exists_ge_of_moments t M h1 h2 h3
  exact ⟨(rot k).1, (rot k).2, rot_isOctahedralRotation k, hk⟩

/-- The covering lemma behind Theorem 4. -/
theorem covering (u w : E3) (hu : ‖u‖ = 1) (hw : ‖w‖ = 1) :
    ∃ σ s, IsOctahedralRotation σ s ∧ 1 / Real.sqrt 3 ≤ ⟪signedPerm σ s u, w⟫ := by
  simpa [hu, hw] using covering_general u w


/-! ## Definitions of the body and the foot-point hull -/

def halfspaceBody {ι : Type*} (n : ι → E3) (h : ι → ℝ) : Set E3 :=
  {x | ∀ i, ⟪n i, x⟫ ≤ h i}

noncomputable def footHull {ι : Type*} (n : ι → E3) (h : ι → ℝ) : Set E3 :=
  convexHull ℝ (Set.range fun i => h i • n i)

def OctahedrallySymmetric {ι : Type*} (n : ι → E3) (h : ι → ℝ) : Prop :=
  ∀ σ s, IsOctahedralRotation σ s → ∀ i, ∃ j, n j = signedPerm σ s (n i) ∧ h j = h i

/-! ## (c) Separation -/

/-- A point outside a finite convex hull is strictly separated from it by a
direction `v`: every point of the hull has smaller inner product with `v`. -/
theorem separation {ι : Type*} [Finite ι] (p : ι → E3) (y : E3)
    (hy : y ∉ convexHull ℝ (Set.range p)) : ∃ v : E3, ∀ i, ⟪v, p i⟫ < ⟪v, y⟫ := by
  have hc : IsClosed (convexHull ℝ (Set.range p)) :=
    ((Set.finite_range p).isCompact_convexHull ℝ).isClosed
  obtain ⟨f, u, hf, hu⟩ := geometric_hahn_banach_closed_point (convex_convexHull ℝ _) hc hy
  refine ⟨(InnerProductSpace.toDual ℝ E3).symm f, fun i => ?_⟩
  rw [InnerProductSpace.toDual_symm_apply, InnerProductSpace.toDual_symm_apply]
  exact (hf _ (subset_convexHull ℝ _ ⟨i, rfl⟩)).trans hu

/-- Each distance is at least `‖x‖/√3` for a point `x` of the body. -/
theorem le_dist {ι : Type*} (n : ι → E3) (h : ι → ℝ) (hn : ∀ i, ‖n i‖ = 1)
    (hsym : OctahedrallySymmetric n h) {x : E3} (hx : x ∈ halfspaceBody n h) (i : ι) :
    ‖x‖ / Real.sqrt 3 ≤ h i := by
  obtain ⟨σ, s, hrot, hle⟩ := covering_general (n i) x
  obtain ⟨j, hnj, hhj⟩ := hsym σ s hrot i
  rw [hn i, one_mul, ← hnj] at hle
  linarith [hx j]

/-- Every direction `v` is reached by a foot point up to the factor 3. -/
theorem exists_foot {ι : Type*} [Nonempty ι] (n : ι → E3) (h : ι → ℝ) (hn : ∀ i, ‖n i‖ = 1)
    (hsym : OctahedrallySymmetric n h) {x : E3} (hx : x ∈ halfspaceBody n h) (v : E3) :
    ∃ j, ⟪v, x⟫ / 3 ≤ ⟪v, h j • n j⟫ := by
  obtain ⟨i0⟩ := ‹Nonempty ι›
  obtain ⟨σ, s, hrot, hle⟩ := covering_general (n i0) v
  obtain ⟨j, hnj, hhj⟩ := hsym σ s hrot i0
  rw [hn i0, one_mul, ← hnj, real_inner_comm] at hle
  refine ⟨j, ?_⟩
  have hd := le_dist n h hn hsym hx j
  have hs3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hs3p : 0 < Real.sqrt 3 := by positivity
  have hcs : ⟪v, x⟫ ≤ ‖v‖ * ‖x‖ := real_inner_le_norm v x
  rw [real_inner_smul_right]
  have h0 : 0 ≤ ‖x‖ / Real.sqrt 3 := by positivity
  have h0' : 0 ≤ ‖v‖ / Real.sqrt 3 := by positivity
  have key : (‖x‖ / Real.sqrt 3) * (‖v‖ / Real.sqrt 3) ≤ h j * ⟪v, n j⟫ :=
    mul_le_mul hd hle h0' (h0.trans hd)
  have : (‖x‖ / Real.sqrt 3) * (‖v‖ / Real.sqrt 3) = ‖v‖ * ‖x‖ / 3 := by
    rw [div_mul_div_comm, ← sq, hs3]; ring
  linarith

/-! ## (d) Theorem 4 -/

theorem octahedral_nesting {ι : Type*} [Fintype ι] [Nonempty ι]
    (n : ι → E3) (h : ι → ℝ) (hn : ∀ i, ‖n i‖ = 1) (hh : ∀ i, 0 < h i)
    (hsym : OctahedrallySymmetric n h) :
    halfspaceBody n h ⊆ (3 : ℝ) • footHull n h := by
  -- the positivity hypothesis `hh` is not needed by this proof
  intro x hx
  refine Set.mem_smul_set.mpr ⟨(1 / 3 : ℝ) • x, ?_, by
    rw [smul_smul]; norm_num⟩
  by_contra hy
  obtain ⟨v, hv⟩ := separation (fun i => h i • n i) _ hy
  obtain ⟨j, hj⟩ := exists_foot n h hn hsym hx v
  have := hv j
  simp only [real_inner_smul_right] at this hj
  linarith


/-! ## (e) Sharpness: the cube -/

noncomputable def cubeNormal : Fin 3 × Bool → E3 :=
  fun k => (if k.2 then (1 : ℝ) else -1) • EuclideanSpace.single k.1 1

theorem inner_cubeNormal (k : Fin 3 × Bool) (y : E3) :
    ⟪cubeNormal k, y⟫ = (if k.2 then (1 : ℝ) else -1) * y k.1 := by
  rcases k with ⟨k, b⟩
  cases b <;> simp [cubeNormal, inner_neg_left, EuclideanSpace.inner_single_left]

theorem cube_admissible :
    (∀ k, ‖cubeNormal k‖ = 1) ∧ OctahedrallySymmetric cubeNormal (fun _ => 1) := by
  refine ⟨fun k => ?_, fun σ s _ k => ?_⟩
  · rcases k with ⟨k, b⟩
    cases b <;> simp [cubeNormal]
  · rcases k with ⟨k, b⟩
    rcases Int.units_eq_one_or (s (σ.symm k)) with hs | hs
    · refine ⟨(σ.symm k, b), ?_, rfl⟩
      ext m
      by_cases hm : m = σ.symm k
      · subst hm; cases b <;> simp [cubeNormal, signedPerm, hs]
      · have : σ m ≠ k := fun h => hm (by rw [← h]; simp)
        cases b <;> simp [cubeNormal, signedPerm, hm, this]
    · refine ⟨(σ.symm k, !b), ?_, rfl⟩
      ext m
      by_cases hm : m = σ.symm k
      · subst hm; cases b <;> simp [cubeNormal, signedPerm, hs]
      · have : σ m ≠ k := fun h => hm (by rw [← h]; simp)
        cases b <;> simp [cubeNormal, signedPerm, hm, this]

/-- **Sharpness.** For the cube no constant `c` with `0 ≤ c < 3` works. -/
theorem octahedral_nesting_sharp (c : ℝ) (hc0 : 0 ≤ c) (hc : c < 3) :
    ¬ halfspaceBody cubeNormal (fun _ => 1) ⊆ c • footHull cubeNormal (fun _ => 1) := by
  intro hsub
  set x : E3 := WithLp.toLp 2 (fun _ => (1 : ℝ)) with hxdef
  have hxk : ∀ k : Fin 3 × Bool, ⟪cubeNormal k, x⟫ ≤ 1 := by
    rintro ⟨k, b⟩; cases b <;> simp [inner_cubeNormal, hxdef]
  obtain ⟨z, hz, hzx⟩ := Set.mem_smul_set.mp (hsub hxk)
  have hconv : Convex ℝ {y : E3 | ⟪x, y⟫ ≤ 1} :=
    convex_halfSpace_le ⟨fun a b => inner_add_right _ _ _,
      fun r a => real_inner_smul_right _ _ _⟩ 1
  have hhull : footHull cubeNormal (fun _ => 1) ⊆ {y : E3 | ⟪x, y⟫ ≤ 1} := by
    refine convexHull_min ?_ hconv
    rintro _ ⟨k, rfl⟩
    simpa [real_inner_comm] using hxk k
  have h1 : ⟪x, z⟫ ≤ 1 := hhull hz
  have hxx : ⟪x, x⟫ = 3 := by
    simp only [hxdef, PiLp.inner_apply, Fin.sum_univ_three]; norm_num
  have : ⟪x, x⟫ = c * ⟪x, z⟫ := by
    rw [← hzx, real_inner_smul_right]
  nlinarith

end KyushindoProof
