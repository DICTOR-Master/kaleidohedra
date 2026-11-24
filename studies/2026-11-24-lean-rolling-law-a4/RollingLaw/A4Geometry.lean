/-
# The A4 die in ℝ⁴: convex, with exactly the 120 listed faces, and fair (M4, M7)

Coordinates: ℝ⁵, the die lies in the hyperplane `y₀ + ⋯ + y₄ = 0` (a copy of ℝ⁴).
* face `x` has normal `nR x = corner x - (3,3,3,3,3)` (a permutation of (2,1,0,-1,-2));
* the die is `Die = {y : ∑ y = 0, nR z ⬝ y ≤ 1 for every face z}` (convex: an intersection of
  half-spaces in a hyperplane);
* face `x` has the four vertices `PR x k = vZ x k / ht k` (`k = 0..3`, heights 10, 15, 15, 10):
  `vZ x k` is `4 - k` at the positions of the `k + 1` largest entries of `corner x` and `-(k+1)`
  elsewhere (5 times a fundamental weight of A4, moved to face `x`).

Proved (0 sorry, `decide +kernel` only for finite checks):
* `support`: `nR z ⬝ PR x k ≤ 1` for every face `z` and every vertex `PR x k`, with equality
  exactly when `PR x k` is the vertex of type `k` of face `z`;
* `facet`: the face of the die in the plane `nR x ⬝ y = 1` is exactly the tetrahedron
  `convexHull {PR x 0, …, PR x 3}`;
* `fair`: for any two faces `x, y` there is a permutation of the coordinates (an isometry of ℝ⁵,
  a product of reflections in the mirrors `y_j = y_(j+1)`) mapping the die onto itself, taking
  face `x` onto face `y` vertex type by vertex type, and permuting the faces by a permutation
  that commutes with every roll.

How the global inequality is reached without checking every face against every vertex
(120 × 30): the reflection in the mirror `y_j = y_(j+1)` (swap of coordinates `j, j+1`) permutes
the faces (`l`, a table checked by the kernel) and carries normals and vertices along; every face
is reached from face 0 by such reflections (`lw`). So `support` for all pairs follows from the
480 checks of the 120 faces against the 4 vertices of face 0 (`base_q`). `facet` at face 0 uses
only the four neighbours of face 0 (each neighbour plane bounds one barycentric coordinate), then
moves to every face by the same reflections.
-/
import RollingLaw.A4

namespace RollingLaw

namespace A4

open Matrix

/-! ### Data: position swaps, coordinates -/

/-- The reflection of the die in the mirror `y_j = y_(j+1)`, on faces. -/
def l (j : Fin 4) (x : Fin 120) : Fin 120 :=
  ⟨((Data.A4.lt.getD j.val []).getD x.val 0) % 120, Nat.mod_lt _ (by decide)⟩

/-- Reflections that, applied in order to face 0, give face `x`. -/
def lw (x : Fin 120) : List (Fin 4) :=
  ((Data.A4.lw.getD x.val []).map fun i => ⟨i % 4, Nat.mod_lt _ (by decide)⟩)

/-- Entry `p` of the corner of face `x`. -/
def cv (x : Fin 120) (p : Fin 5) : ℕ := (corner x).getD p.val 0

/-- The normal of face `x` (integer vector, a permutation of (2,1,0,-1,-2)). -/
def nZ (x : Fin 120) (p : Fin 5) : ℤ := (cv x p : ℤ) - 3

/-- Five times the vertex direction of type `k` of face `x`. -/
def vZ (x : Fin 120) (k : Fin 4) (p : Fin 5) : ℤ :=
  if 5 ≤ cv x p + k.val then 4 - k.val else -((k.val : ℤ) + 1)

/-- The height of the vertex of type `k`: `nZ x ⬝ vZ x k`. -/
def ht (k : Fin 4) : ℤ := ![10, 15, 15, 10] k

/-- Swapping coordinates `j` and `j + 1`. -/
def sw (j : Fin 4) : Equiv.Perm (Fin 5) := Equiv.swap j.castSucc j.succ

/-- Explicit integer dot product (for the kernel). -/
def dot5 (a b : Fin 5 → ℤ) : ℤ := a 0 * b 0 + a 1 * b 1 + a 2 * b 2 + a 3 * b 3 + a 4 * b 4

/-! ### Kernel checks -/

theorem l_cv : ∀ j x p, cv (l j x) p = cv x (sw j p) := by decide +kernel
theorem l_l : ∀ j x, l j (l j x) = x := by decide +kernel
theorem l_r : ∀ j i x, l j (r i x) = r i (l j x) := by decide +kernel
theorem lw_spec : ∀ x, (lw x).foldl (fun y j => l j y) 0 = x := by decide +kernel

/-- **The 480 base checks**: every face against the four vertices of face 0. -/
theorem base_q : ∀ (x : Fin 120) (k : Fin 4), dot5 (nZ x) (vZ 0 k) ≤ ht k ∧
    (dot5 (nZ x) (vZ 0 k) = ht k ↔ ∀ p, vZ 0 k p = vZ x k p) := by decide +kernel

theorem ht_pos : ∀ k, 0 < ht k := by decide +kernel
theorem vZ_sum : ∀ x k, ∑ p, vZ x k p = 0 := by
  intro x k; rw [Fin.sum_univ_five]; revert x k; decide +kernel
theorem n0 : ∀ p, nZ 0 p = ![2, 1, 0, -1, -2] p := by decide +kernel
theorem nr00 : ∀ p, nZ (r 0 0) p = ![1, 2, 0, -1, -2] p := by decide +kernel
theorem nr10 : ∀ p, nZ (r 1 0) p = ![2, 0, 1, -1, -2] p := by decide +kernel
theorem nr20 : ∀ p, nZ (r 2 0) p = ![2, 1, -1, 0, -2] p := by decide +kernel
theorem nr30 : ∀ p, nZ (r 3 0) p = ![2, 1, 0, -2, -1] p := by decide +kernel
theorem v0 : ∀ k p, vZ 0 k p = if p.val ≤ k.val then 4 - (k.val : ℤ) else -((k.val : ℤ) + 1) := by
  decide +kernel

/-! ### Symmetries: face permutations carried by coordinate permutations -/

/-- `σ` permutes the faces as the coordinate permutation `τ` permutes normals and vertices. -/
def Sym (σ : Equiv.Perm (Fin 120)) (τ : Equiv.Perm (Fin 5)) : Prop :=
  ∀ z, nZ (σ z) = nZ z ∘ τ ∧ ∀ k, vZ (σ z) k = vZ z k ∘ τ

/-- `σ` commutes with every roll. -/
def Comm (σ : Equiv.Perm (Fin 120)) : Prop := ∀ i z, σ (r i z) = r i (σ z)

theorem Sym.trans {σ σ' τ τ'} (h : Sym σ τ) (h' : Sym σ' τ') : Sym (σ.trans σ') (τ'.trans τ) := by
  intro z
  refine ⟨?_, fun k => ?_⟩
  · simp only [Equiv.trans_apply, (h' _).1, (h z).1]; rfl
  · simp only [Equiv.trans_apply, (h' _).2, (h z).2]; rfl

theorem Sym.symm {σ τ} (h : Sym σ τ) : Sym σ.symm τ.symm := by
  intro z
  have e := h (σ.symm z)
  rw [Equiv.apply_symm_apply] at e
  refine ⟨?_, fun k => ?_⟩
  · funext p; simp [e.1]
  · funext p; simp [e.2 k]

theorem Comm.trans {σ σ'} (h : Comm σ) (h' : Comm σ') : Comm (σ.trans σ') := by
  intro i z; simp [h i z, h' i]

theorem Comm.symm {σ} (h : Comm σ) : Comm σ.symm := by
  intro i z
  apply σ.injective
  rw [h, Equiv.apply_symm_apply, Equiv.apply_symm_apply]

/-- The reflection in the mirror `y_j = y_(j+1)`, as a permutation of the faces. -/
def le (j : Fin 4) : Equiv.Perm (Fin 120) := Function.Involutive.toPerm (l j) (l_l j)

theorem sym_le (j : Fin 4) : Sym (le j) (sw j) := by
  intro z
  refine ⟨?_, fun k => ?_⟩
  · funext p; exact congrArg (fun c : ℕ => (c : ℤ) - 3) (l_cv j z p)
  · funext p; simp only [vZ, Function.comp]; rw [← l_cv]; rfl

theorem comm_le (j : Fin 4) : Comm (le j) := fun i z => l_r j i z

/-- Reflections applied in order. -/
def Le : List (Fin 4) → Equiv.Perm (Fin 120)
  | [] => Equiv.refl _
  | j :: ω => (le j).trans (Le ω)

/-- The matching coordinate permutation. -/
def TT : List (Fin 4) → Equiv.Perm (Fin 5)
  | [] => Equiv.refl _
  | j :: ω => (TT ω).trans (sw j)

theorem sym_Le : ∀ ω, Sym (Le ω) (TT ω)
  | [] => fun _ => ⟨rfl, fun _ => rfl⟩
  | j :: ω => (sym_le j).trans (sym_Le ω)

theorem comm_Le : ∀ ω, Comm (Le ω)
  | [] => fun _ _ => rfl
  | j :: ω => (comm_le j).trans (comm_Le ω)

theorem Le_apply : ∀ (ω : List (Fin 4)) (x : Fin 120), Le ω x = ω.foldl (fun y j => l j y) x
  | [], _ => rfl
  | j :: ω, x => by simp only [Le, Equiv.trans_apply, List.foldl_cons]; rw [Le_apply ω]; rfl

/-- For every face `x`: a product of mirror reflections taking face 0 to face `x`. -/
theorem to_face (x : Fin 120) : ∃ σ τ, Sym σ τ ∧ Comm σ ∧ σ 0 = x :=
  ⟨Le (lw x), TT (lw x), sym_Le _, comm_Le _, by rw [Le_apply, lw_spec]⟩

/-! ### Support: every face against every vertex, from the 480 base checks -/

theorem dot_comp (a b : Fin 5 → ℤ) (τ : Equiv.Perm (Fin 5)) :
    ∑ p, (a ∘ τ) p * (b ∘ τ) p = ∑ p, a p * b p :=
  Equiv.sum_comp τ (fun p => a p * b p)

theorem comp_eq_iff {a b : Fin 5 → ℤ} (τ : Equiv.Perm (Fin 5)) : a ∘ τ = b ∘ τ ↔ a = b := by
  refine ⟨fun h => funext fun p => ?_, fun h => h ▸ rfl⟩
  simpa using congrFun h (τ.symm p)

theorem dot5_eq (a b : Fin 5 → ℤ) : dot5 a b = ∑ p, a p * b p := by
  rw [Fin.sum_univ_five]; rfl

/-- Integer form of `support`. -/
theorem support_int (z x : Fin 120) (k : Fin 4) :
    ∑ p, nZ z p * vZ x k p ≤ ht k ∧ (∑ p, nZ z p * vZ x k p = ht k ↔ vZ x k = vZ z k) := by
  obtain ⟨σ, τ, hS, -, hx⟩ := to_face x
  have hz := (hS (σ.symm z)).1
  rw [Equiv.apply_symm_apply] at hz
  have hv : vZ x k = vZ 0 k ∘ τ := hx ▸ (hS 0).2 k
  have hv' := (hS (σ.symm z)).2 k
  rw [Equiv.apply_symm_apply] at hv'
  rw [hz, hv, hv', dot_comp, comp_eq_iff, ← dot5_eq, funext_iff]
  exact base_q _ k

/-! ### Real statements -/

/-- The normal of face `x` in ℝ⁵. -/
def nR (x : Fin 120) : Fin 5 → ℝ := fun p => (nZ x p : ℝ)

/-- The vertex of type `k` of face `x`. -/
noncomputable def PR (x : Fin 120) (k : Fin 4) : Fin 5 → ℝ := fun p => (vZ x k p : ℝ) / (ht k : ℝ)

/-- **The A4 die**: in the hyperplane `∑ y = 0` of ℝ⁵, bounded by the 120 face planes. -/
def Die : Set (Fin 5 → ℝ) := {y | ∑ p, y p = 0 ∧ ∀ z, nR z ⬝ᵥ y ≤ 1}

theorem convex_die : Convex ℝ Die := by
  intro y hy y' hy' a b ha hb hab
  refine ⟨?_, fun z => ?_⟩
  · simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, Finset.sum_add_distrib, ← Finset.mul_sum,
      hy.1, hy'.1]; ring
  · rw [dotProduct_add, dotProduct_smul, dotProduct_smul, smul_eq_mul, smul_eq_mul]
    nlinarith [hy.2 z, hy'.2 z]

theorem dot_PR (z x : Fin 120) (k : Fin 4) :
    nR z ⬝ᵥ PR x k = ((∑ p, nZ z p * vZ x k p : ℤ) : ℝ) / ht k := by
  simp only [dotProduct, nR, PR]; push_cast; rw [Finset.sum_div]
  exact Finset.sum_congr rfl fun p _ => by ring

theorem PR_eq_iff (x z : Fin 120) (k : Fin 4) : PR x k = PR z k ↔ vZ x k = vZ z k := by
  have h' : (ht k : ℝ) ≠ 0 := by exact_mod_cast (ht_pos k).ne'
  constructor
  · intro e; funext p
    have := congrFun e p
    simp only [PR] at this
    rw [div_left_inj' h'] at this; exact_mod_cast this
  · intro e; unfold PR; rw [e]

/-- **Support (M4)**: every face plane `nR z ⬝ y = 1` has every vertex of the die on its inner
side, and passes through the vertex `PR x k` exactly when that is the vertex of type `k` of
face `z`. -/
theorem support (z x : Fin 120) (k : Fin 4) :
    nR z ⬝ᵥ PR x k ≤ 1 ∧ (nR z ⬝ᵥ PR x k = 1 ↔ PR x k = PR z k) := by
  obtain ⟨h1, h2⟩ := support_int z x k
  have hp : (0 : ℝ) < ht k := by exact_mod_cast ht_pos k
  rw [dot_PR, PR_eq_iff, ← h2, div_le_one hp, div_eq_one_iff_eq hp.ne']
  exact ⟨by exact_mod_cast h1, Int.cast_inj⟩

theorem PR_mem (x : Fin 120) (k : Fin 4) : PR x k ∈ Die := by
  refine ⟨?_, fun z => (support z x k).1⟩
  simp only [PR]; rw [← Finset.sum_div, div_eq_zero_iff]; left; exact_mod_cast vZ_sum x k

/-- At face 0, the face of the die is the tetrahedron, using only the four neighbours of face 0:
the plane of neighbour `r k 0` bounds the `k`-th barycentric coordinate. -/
theorem facet0 {y : Fin 5 → ℝ} (hy : y ∈ Die) (h1 : nR 0 ⬝ᵥ y = 1) :
    y ∈ convexHull ℝ (Set.range (PR 0)) := by
  obtain ⟨hs, hz⟩ := hy
  have e0 := hz (r 0 0); have e1 := hz (r 1 0); have e2 := hz (r 2 0); have e3 := hz (r 3 0)
  simp only [dotProduct, Fin.sum_univ_five, nR, nr00, nr10, nr20, nr30, n0] at e0 e1 e2 e3 h1
  simp at e0 e1 e2 e3 h1
  rw [Fin.sum_univ_five] at hs
  set w : Fin 4 → ℝ := ![(y 0 - y 1) * 2, (y 1 - y 2) * 3, (y 2 - y 3) * 3, (y 3 - y 4) * 2]
  have hw : ∀ k, 0 ≤ w k := by intro k; fin_cases k <;> simp [w] <;> linarith
  have hsum : ∑ k, w k = 1 := by simp [w, Fin.sum_univ_four]; linarith
  have hmem : (∑ k, w k • PR 0 k) ∈ convexHull ℝ (Set.range (PR 0)) :=
    (convex_convexHull ℝ _).sum_mem (fun k _ => hw k) hsum
      (fun k _ => subset_convexHull ℝ _ (Set.mem_range_self k))
  convert hmem using 1
  funext p
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Fin.sum_univ_four, PR, v0, ht, w]
  fin_cases p <;> simp <;> linarith

/-! ### Transport by the mirror reflections -/

theorem Sym.nR' {σ τ} (h : Sym σ τ) (z : Fin 120) : nR (σ z) = nR z ∘ τ := by
  funext p; simp [nR, (h z).1]

theorem Sym.PR' {σ τ} (h : Sym σ τ) (z : Fin 120) (k : Fin 4) : PR (σ z) k = PR z k ∘ τ := by
  funext p; simp [PR, (h z).2 k]

/-- A permutation of the coordinates is an isometry. -/
theorem dotR_comp (a b : Fin 5 → ℝ) (τ : Equiv.Perm (Fin 5)) : (a ∘ τ) ⬝ᵥ (b ∘ τ) = a ⬝ᵥ b := by
  simp only [dotProduct]; exact Equiv.sum_comp τ (fun p => a p * b p)

theorem Sym.die {σ τ} (h : Sym σ τ) (v : Fin 5 → ℝ) : v ∘ τ ∈ Die ↔ v ∈ Die := by
  have hs : ∑ p, (v ∘ τ) p = ∑ p, v p := Equiv.sum_comp τ v
  have hd : ∀ z, nR (σ z) ⬝ᵥ (v ∘ τ) = nR z ⬝ᵥ v := fun z => by rw [h.nR', dotR_comp]
  simp only [Die, Set.mem_ofPred_eq, hs]
  refine and_congr_right fun _ => ⟨fun H z => ?_, fun H z => ?_⟩
  · rw [← hd]; exact H _
  · rw [← Equiv.apply_symm_apply σ z, hd]; exact H _

/-- **Facets (M4)**: the face of the die in the plane of face `x` is exactly the tetrahedron
on the four listed vertices of `x`. -/
theorem facet (x : Fin 120) : {y ∈ Die | nR x ⬝ᵥ y = 1} = convexHull ℝ (Set.range (PR x)) := by
  apply Set.Subset.antisymm
  · rintro y ⟨hy, h1⟩
    obtain ⟨σ, τ, hS, -, hx⟩ := to_face x
    set y0 : Fin 5 → ℝ := y ∘ τ.symm
    have hy0 : y0 ∘ τ = y := by funext p; simp [y0]
    have m0 : y0 ∈ Die := (hS.die y0).mp (hy0 ▸ hy)
    have d0 : nR 0 ⬝ᵥ y0 = 1 := by rw [← dotR_comp _ _ τ, ← hS.nR', hx, hy0, h1]
    have := facet0 m0 d0
    have hA := Set.mem_image_of_mem (LinearMap.funLeft ℝ ℝ τ) this
    rw [LinearMap.image_convexHull, ← Set.range_comp] at hA
    have e : (LinearMap.funLeft ℝ ℝ τ) ∘ PR 0 = PR x := by
      funext k; rw [← hx, hS.PR']; rfl
    rw [e] at hA
    simpa [LinearMap.funLeft, hy0] using hA
  · refine convexHull_min ?_ ?_
    · rintro _ ⟨k, rfl⟩; exact ⟨PR_mem x k, (support x x k).2.mpr rfl⟩
    · intro a ha b hb s t hs ht hst
      refine ⟨convex_die ha.1 hb.1 hs ht hst, ?_⟩
      show nR x ⬝ᵥ (s • a + t • b) = 1
      rw [dotProduct_add, dotProduct_smul, dotProduct_smul, smul_eq_mul, smul_eq_mul, ha.2, hb.2]
      linarith

/-! ### Fairness (M7) -/

/-- **The A4 die is fair.** For any two faces `x, y` there is a permutation `τ` of the
coordinates (a product of reflections in the mirrors `y_j = y_(j+1)`; an isometry) that maps
the die onto itself and takes face `x` onto face `y`, vertex type by vertex type; on the faces
it acts by a permutation `σ` that commutes with every roll. -/
theorem fair (x y : Fin 120) : ∃ τ : Equiv.Perm (Fin 5), ∃ σ : Equiv.Perm (Fin 120),
    σ x = y ∧ (∀ i z, σ (r i z) = r i (σ z)) ∧
    (∀ a b : Fin 5 → ℝ, (a ∘ τ) ⬝ᵥ (b ∘ τ) = a ⬝ᵥ b) ∧
    (∀ v, v ∘ τ ∈ Die ↔ v ∈ Die) ∧
    (∀ z, nR (σ z) = nR z ∘ τ) ∧ (∀ z k, PR (σ z) k = PR z k ∘ τ) := by
  obtain ⟨σ₁, τ₁, h₁, c₁, e₁⟩ := to_face x
  obtain ⟨σ₂, τ₂, h₂, c₂, e₂⟩ := to_face y
  have h := h₁.symm.trans h₂
  refine ⟨τ₂.trans τ₁.symm, σ₁.symm.trans σ₂, ?_, c₁.symm.trans c₂, fun a b => dotR_comp a b _,
    h.die, h.nR', h.PR'⟩
  rw [Equiv.trans_apply, ← e₁, Equiv.symm_apply_apply, e₂]

/-- **Every roll-preserving permutation of the faces is an isometry of the die**: it is
realised by a permutation of the coordinates that maps the die onto itself and carries the
normal and the vertices of each face to those of its image. -/
theorem roll_symmetry_isometry (σ' : Fin 120 → Fin 120)
    (hσ' : ∀ i z, σ' (r i z) = r i (σ' z)) : ∃ τ : Equiv.Perm (Fin 5),
    (∀ a b : Fin 5 → ℝ, (a ∘ τ) ⬝ᵥ (b ∘ τ) = a ⬝ᵥ b) ∧ (∀ v, v ∘ τ ∈ Die ↔ v ∈ Die) ∧
    (∀ z, nR (σ' z) = nR z ∘ τ) ∧ (∀ z k, PR (σ' z) k = PR z k ∘ τ) := by
  obtain ⟨τ, σ, h0, hc, hi, hd, hn, hp⟩ := fair 0 (σ' 0)
  have e : (σ : Fin 120 → Fin 120) = σ' := transitive_unique σ σ' hc hσ' 0 h0
  exact ⟨τ, hi, hd, e ▸ hn, e ▸ hp⟩

end A4

end RollingLaw
