/-
# The fair-die property: all faces are congruent

For each die, `Die` is the solid `{ p : n z · p ≤ 1 for every face z }` (the
exact face normals of `RollingLaw.Die`). The data give for each face `x` an
exact matrix `G x` (stored as `4 G x` in ℤ[√5]). Kernel checks, transferred to ℝ:
* `G_orth`: each `G x` is orthogonal (an isometry);
* `G_transpose`: its transpose is `G (inv x)`;
* `G_roll`: `G (r i x) = G x * G (r i 0)`, and `G 0 = 1`;
* each mirror `G (r i 0)` permutes the face normals, hence maps `Die` into itself;
  so every `G x` maps `Die` into itself (`G_maps`);
* `G_vertex`: `G x` takes the vertices of face 0 to those of face `x`, type by type.
**`fair`**: for any two faces `x, y` there is an isometry `A` of space with
`A Die = Die` that takes face `x` onto face `y` (vertex of type `k` to vertex of type `k`).
So the symmetry group acts transitively on the faces: every face is congruent
to every other — the die is fair.
-/
import RollingLaw.Mirrors

namespace RollingLaw

open Matrix

namespace Fair
open Q5

/-- A 3-vector of `Q5` as a real vector. -/
noncomputable def vec (l : List Q5) : Fin 3 → ℝ := fun k => (l.getD k zero).toReal
/-- Entry `(a, b)` of a matrix given by rows. -/
def ent (g : List (List Q5)) (a b : ℕ) : Q5 := (g.getD a []).getD b zero
/-- The real matrix `g / 4`. -/
noncomputable def mat (g : List (List Q5)) : Matrix (Fin 3) (Fin 3) ℝ :=
  Matrix.of fun a b => (ent g a b).toReal / 4
/-- Column `b`. -/
def col (g : List (List Q5)) (b : ℕ) : List Q5 := [ent g 0 b, ent g 1 b, ent g 2 b]
/-- Matrix times vector. -/
def matvec (g : List (List Q5)) (v : List Q5) : List Q5 :=
  [dot (g.getD 0 []) v, dot (g.getD 1 []) v, dot (g.getD 2 []) v]
/-- Four times a vector. -/
def smul4 (v : List Q5) : List Q5 := v.map (mul ⟨4, 0⟩)
/-- Matrix product. -/
def matmul (g h : List (List Q5)) : List (List Q5) :=
  [0, 1, 2].map fun a => [0, 1, 2].map fun b => dot (g.getD a []) (col h b)

theorem toReal_four : (⟨4, 0⟩ : Q5).toReal = 4 := by simp [toReal]
theorem toReal_sixteen : (⟨16, 0⟩ : Q5).toReal = 16 := by simp [toReal]
theorem toReal_zero : Q5.zero.toReal = 0 := by simp [toReal, Q5.zero]

theorem vec_smul4 (v : List Q5) : vec (smul4 v) = (4 : ℝ) • vec v := by
  funext k
  have h0 : zero = mul ⟨4, 0⟩ zero := by decide
  simp only [vec, smul4, Pi.smul_apply, smul_eq_mul]
  rw [h0, List.getD_map, toReal_mul, toReal_four, ← h0]

theorem vec_matvec (g : List (List Q5)) (v : List Q5) :
    vec (matvec g v) = (4 : ℝ) • (mat g *ᵥ vec v) := by
  funext k
  fin_cases k <;>
  simp [vec, matvec, mat, ent, mulVec, dotProduct, Fin.sum_univ_three, toReal_dot, rdot] <;> ring

theorem apply_of {g : List (List Q5)} {v w : List Q5} (h : matvec g v = smul4 w) :
    mat g *ᵥ vec v = vec w := by
  have := congrArg vec h
  rw [vec_matvec, vec_smul4] at this
  exact smul_right_injective _ (by norm_num : (4 : ℝ) ≠ 0) this

theorem mat_matmul_of {g h k : List (List Q5)}
    (hc : ∀ a b : Fin 3, ent (matmul g h) a b = mul ⟨4, 0⟩ (ent k a b)) : mat g * mat h = mat k := by
  ext a b
  have := congrArg toReal (hc a b)
  fin_cases a <;> fin_cases b <;>
  simp [ent, matmul, col, toReal_dot, rdot, Fin.sum_univ_three, toReal_mul, toReal_four] at this <;>
  simp [mat, ent, Matrix.mul_apply, Fin.sum_univ_three] <;> linear_combination this / 16

theorem orth_of {g : List (List Q5)}
    (hc : ∀ a b : Fin 3, dot (col g a) (col g b) = if a = b then (⟨16, 0⟩ : Q5) else Q5.zero) :
    (mat g)ᵀ * mat g = 1 := by
  ext a b
  have := congrArg toReal (hc a b)
  fin_cases a <;> fin_cases b <;>
  simp [col, ent, toReal_dot, rdot, Fin.sum_univ_three, toReal_sixteen, toReal_zero] at this <;>
  simp [mat, ent, Matrix.mul_apply, Fin.sum_univ_three] <;>
  linear_combination this / 16

theorem transpose_of {g h : List (List Q5)} (hc : ∀ a b : Fin 3, ent g a b = ent h b a) :
    mat g = (mat h)ᵀ := by
  ext a b; simp [mat, hc a b]

theorem one_of {g : List (List Q5)} (hc : ∀ a b : Fin 3, ent g a b = if a = b then (⟨4, 0⟩ : Q5) else Q5.zero) :
    mat g = 1 := by
  ext a b; rw [mat, Matrix.of_apply, hc a b]
  split_ifs with h <;> simp [h, toReal_four, toReal_zero, Matrix.one_apply]

/-- The solid bounded by the face planes `n z · p = 1`. -/
def Solid {N : ℕ} (n : Fin N → List Q5) : Set (Fin 3 → ℝ) := {p | ∀ z, vec (n z) ⬝ᵥ p ≤ 1}

theorem maps_solid {N : ℕ} {n : Fin N → List Q5} {A : Matrix (Fin 3) (Fin 3) ℝ} (σ : Fin N → Fin N)
    (hA : ∀ z, Aᵀ *ᵥ vec (n z) = vec (n (σ z))) {p : Fin 3 → ℝ} (hp : p ∈ Solid n) :
    A *ᵥ p ∈ Solid n := by
  intro z
  rw [dotProduct_mulVec, ← mulVec_transpose, hA]
  exact hp _

end Fair

/-! ## A3: the tetrakis hexahedron is fair -/
namespace A3
open Fair

/-- the symmetry taking face 0 to face `x` -/
noncomputable def G (x : Fin 24) : Matrix (Fin 3) (Fin 3) ℝ := mat (Data.A3.gm.getD x.val [])
/-- the face whose symmetry is the inverse -/
def inv (x : Fin 24) : Fin 24 := ⟨(Data.A3.inv.getD x.val 0) % 24, Nat.mod_lt _ (by decide)⟩
/-- how the mirror of edge type `i` of face 0 permutes the faces -/
def gp (i : Fin 3) (z : Fin 24) : Fin 24 :=
  ⟨((Data.A3.gperm.getD i.val []).getD z.val 0) % 24, Nat.mod_lt _ (by decide)⟩
/-- the die as a solid -/
def Die : Set (Fin 3 → ℝ) := Solid nrm

theorem G_orth (x : Fin 24) : (G x)ᵀ * G x = 1 := orth_of (by revert x; decide +kernel)

theorem G_transpose (x : Fin 24) : G (inv x) = (G x)ᵀ := transpose_of (by revert x; decide +kernel)

theorem G_zero : G 0 = 1 := one_of (by decide +kernel)

theorem G_roll (x : Fin 24) (i : Fin 3) : G (r i x) = G x * G (r i 0) :=
  (mat_matmul_of (by revert x i; decide +kernel)).symm

theorem G_vertex (x : Fin 24) (k : Fin 3) : G x *ᵥ vec (vtx (fv 0 k)) = vec (vtx (fv x k)) :=
  apply_of (by revert x k; decide +kernel)

theorem mirror_maps (i : Fin 3) {p : Fin 3 → ℝ} (hp : p ∈ Die) : G (r i 0) *ᵥ p ∈ Die := by
  refine maps_solid (gp i) (fun z => ?_) hp
  rw [← G_transpose]
  exact apply_of (by revert i z; decide +kernel)

/-- Every symmetry `G x` maps the die into itself. -/
theorem G_maps (x : Fin 24) {p : Fin 3 → ℝ} (hp : p ∈ Die) : G x *ᵥ p ∈ Die := by
  have key : ∀ ω : List (Fin 3), ∀ p ∈ Die, G (roll r ω 0) *ᵥ p ∈ Die := by
    intro ω
    induction ω using List.reverseRecOn with
    | nil => intro p hp; simpa [G_zero] using hp
    | append_singleton ω i ih =>
      intro p hp
      rw [roll_append, roll_singleton, G_roll, ← mulVec_mulVec]
      exact ih _ (mirror_maps i hp)
  have := key (nf x) p hp
  rwa [roll_nf] at this

/-- **The tetrakis hexahedron is fair.** For any two faces `x, y` there is an isometry `A`
mapping the die onto itself and face `x` onto face `y`, vertex type by vertex type. -/
theorem fair (x y : Fin 24) : ∃ A : Matrix (Fin 3) (Fin 3) ℝ, Aᵀ * A = 1 ∧
    (∀ p, A *ᵥ p ∈ Die ↔ p ∈ Die) ∧ ∀ k, A *ᵥ vec (vtx (fv x k)) = vec (vtx (fv y k)) := by
  refine ⟨G y * G (inv x), ?_, fun p => ⟨fun hp => ?_, fun hp => ?_⟩, fun k => ?_⟩
  · rw [transpose_mul, Matrix.mul_assoc, ← Matrix.mul_assoc (G y)ᵀ, G_orth, Matrix.one_mul,
      G_orth]
  · have h1 := G_maps x (G_maps (inv y) hp)
    rw [mulVec_mulVec, mulVec_mulVec, G_transpose, G_transpose] at h1
    have e : G x * (G y)ᵀ * (G y * (G x)ᵀ) = 1 := by
      rw [Matrix.mul_assoc, ← Matrix.mul_assoc (G y)ᵀ, G_orth, Matrix.one_mul,
        mul_eq_one_comm.mp (G_orth x)]
    rwa [e, one_mulVec] at h1
  · rw [← mulVec_mulVec]; exact G_maps y (G_maps (inv x) hp)
  · rw [← G_vertex x k, ← G_vertex y k, mulVec_mulVec, Matrix.mul_assoc, G_transpose, G_orth,
      Matrix.mul_one]

end A3

/-! ## B3: the disdyakis dodecahedron is fair -/
namespace B3
open Fair

/-- the symmetry taking face 0 to face `x` -/
noncomputable def G (x : Fin 48) : Matrix (Fin 3) (Fin 3) ℝ := mat (Data.B3.gm.getD x.val [])
/-- the face whose symmetry is the inverse -/
def inv (x : Fin 48) : Fin 48 := ⟨(Data.B3.inv.getD x.val 0) % 48, Nat.mod_lt _ (by decide)⟩
/-- how the mirror of edge type `i` of face 0 permutes the faces -/
def gp (i : Fin 3) (z : Fin 48) : Fin 48 :=
  ⟨((Data.B3.gperm.getD i.val []).getD z.val 0) % 48, Nat.mod_lt _ (by decide)⟩
/-- the die as a solid -/
def Die : Set (Fin 3 → ℝ) := Solid nrm

theorem G_orth (x : Fin 48) : (G x)ᵀ * G x = 1 := orth_of (by revert x; decide +kernel)

theorem G_transpose (x : Fin 48) : G (inv x) = (G x)ᵀ := transpose_of (by revert x; decide +kernel)

theorem G_zero : G 0 = 1 := one_of (by decide +kernel)

theorem G_roll (x : Fin 48) (i : Fin 3) : G (r i x) = G x * G (r i 0) :=
  (mat_matmul_of (by revert x i; decide +kernel)).symm

theorem G_vertex (x : Fin 48) (k : Fin 3) : G x *ᵥ vec (vtx (fv 0 k)) = vec (vtx (fv x k)) :=
  apply_of (by revert x k; decide +kernel)

theorem mirror_maps (i : Fin 3) {p : Fin 3 → ℝ} (hp : p ∈ Die) : G (r i 0) *ᵥ p ∈ Die := by
  refine maps_solid (gp i) (fun z => ?_) hp
  rw [← G_transpose]
  exact apply_of (by revert i z; decide +kernel)

/-- Every symmetry `G x` maps the die into itself. -/
theorem G_maps (x : Fin 48) {p : Fin 3 → ℝ} (hp : p ∈ Die) : G x *ᵥ p ∈ Die := by
  have key : ∀ ω : List (Fin 3), ∀ p ∈ Die, G (roll r ω 0) *ᵥ p ∈ Die := by
    intro ω
    induction ω using List.reverseRecOn with
    | nil => intro p hp; simpa [G_zero] using hp
    | append_singleton ω i ih =>
      intro p hp
      rw [roll_append, roll_singleton, G_roll, ← mulVec_mulVec]
      exact ih _ (mirror_maps i hp)
  have := key (nf x) p hp
  rwa [roll_nf] at this

/-- **The disdyakis dodecahedron is fair.** For any two faces `x, y` there is an isometry `A`
mapping the die onto itself and face `x` onto face `y`, vertex type by vertex type. -/
theorem fair (x y : Fin 48) : ∃ A : Matrix (Fin 3) (Fin 3) ℝ, Aᵀ * A = 1 ∧
    (∀ p, A *ᵥ p ∈ Die ↔ p ∈ Die) ∧ ∀ k, A *ᵥ vec (vtx (fv x k)) = vec (vtx (fv y k)) := by
  refine ⟨G y * G (inv x), ?_, fun p => ⟨fun hp => ?_, fun hp => ?_⟩, fun k => ?_⟩
  · rw [transpose_mul, Matrix.mul_assoc, ← Matrix.mul_assoc (G y)ᵀ, G_orth, Matrix.one_mul,
      G_orth]
  · have h1 := G_maps x (G_maps (inv y) hp)
    rw [mulVec_mulVec, mulVec_mulVec, G_transpose, G_transpose] at h1
    have e : G x * (G y)ᵀ * (G y * (G x)ᵀ) = 1 := by
      rw [Matrix.mul_assoc, ← Matrix.mul_assoc (G y)ᵀ, G_orth, Matrix.one_mul,
        mul_eq_one_comm.mp (G_orth x)]
    rwa [e, one_mulVec] at h1
  · rw [← mulVec_mulVec]; exact G_maps y (G_maps (inv x) hp)
  · rw [← G_vertex x k, ← G_vertex y k, mulVec_mulVec, Matrix.mul_assoc, G_transpose, G_orth,
      Matrix.mul_one]

end B3

/-! ## H3: the disdyakis triacontahedron is fair -/
namespace H3
open Fair

/-- the symmetry taking face 0 to face `x` -/
noncomputable def G (x : Fin 120) : Matrix (Fin 3) (Fin 3) ℝ := mat (Data.H3.gm.getD x.val [])
/-- the face whose symmetry is the inverse -/
def inv (x : Fin 120) : Fin 120 := ⟨(Data.H3.inv.getD x.val 0) % 120, Nat.mod_lt _ (by decide)⟩
/-- how the mirror of edge type `i` of face 0 permutes the faces -/
def gp (i : Fin 3) (z : Fin 120) : Fin 120 :=
  ⟨((Data.H3.gperm.getD i.val []).getD z.val 0) % 120, Nat.mod_lt _ (by decide)⟩
/-- the die as a solid -/
def Die : Set (Fin 3 → ℝ) := Solid nrm

theorem G_orth (x : Fin 120) : (G x)ᵀ * G x = 1 := orth_of (by revert x; decide +kernel)

theorem G_transpose (x : Fin 120) : G (inv x) = (G x)ᵀ := transpose_of (by revert x; decide +kernel)

theorem G_zero : G 0 = 1 := one_of (by decide +kernel)

theorem G_roll (x : Fin 120) (i : Fin 3) : G (r i x) = G x * G (r i 0) :=
  (mat_matmul_of (by revert x i; decide +kernel)).symm

theorem G_vertex (x : Fin 120) (k : Fin 3) : G x *ᵥ vec (vtx (fv 0 k)) = vec (vtx (fv x k)) :=
  apply_of (by revert x k; decide +kernel)

theorem mirror_maps (i : Fin 3) {p : Fin 3 → ℝ} (hp : p ∈ Die) : G (r i 0) *ᵥ p ∈ Die := by
  refine maps_solid (gp i) (fun z => ?_) hp
  rw [← G_transpose]
  exact apply_of (by revert i z; decide +kernel)

/-- Every symmetry `G x` maps the die into itself. -/
theorem G_maps (x : Fin 120) {p : Fin 3 → ℝ} (hp : p ∈ Die) : G x *ᵥ p ∈ Die := by
  have key : ∀ ω : List (Fin 3), ∀ p ∈ Die, G (roll r ω 0) *ᵥ p ∈ Die := by
    intro ω
    induction ω using List.reverseRecOn with
    | nil => intro p hp; simpa [G_zero] using hp
    | append_singleton ω i ih =>
      intro p hp
      rw [roll_append, roll_singleton, G_roll, ← mulVec_mulVec]
      exact ih _ (mirror_maps i hp)
  have := key (nf x) p hp
  rwa [roll_nf] at this

/-- **The disdyakis triacontahedron is fair.** For any two faces `x, y` there is an isometry `A`
mapping the die onto itself and face `x` onto face `y`, vertex type by vertex type. -/
theorem fair (x y : Fin 120) : ∃ A : Matrix (Fin 3) (Fin 3) ℝ, Aᵀ * A = 1 ∧
    (∀ p, A *ᵥ p ∈ Die ↔ p ∈ Die) ∧ ∀ k, A *ᵥ vec (vtx (fv x k)) = vec (vtx (fv y k)) := by
  refine ⟨G y * G (inv x), ?_, fun p => ⟨fun hp => ?_, fun hp => ?_⟩, fun k => ?_⟩
  · rw [transpose_mul, Matrix.mul_assoc, ← Matrix.mul_assoc (G y)ᵀ, G_orth, Matrix.one_mul,
      G_orth]
  · have h1 := G_maps x (G_maps (inv y) hp)
    rw [mulVec_mulVec, mulVec_mulVec, G_transpose, G_transpose] at h1
    have e : G x * (G y)ᵀ * (G y * (G x)ᵀ) = 1 := by
      rw [Matrix.mul_assoc, ← Matrix.mul_assoc (G y)ᵀ, G_orth, Matrix.one_mul,
        mul_eq_one_comm.mp (G_orth x)]
    rwa [e, one_mulVec] at h1
  · rw [← mulVec_mulVec]; exact G_maps y (G_maps (inv x) hp)
  · rw [← G_vertex x k, ← G_vertex y k, mulVec_mulVec, Matrix.mul_assoc, G_transpose, G_orth,
      Matrix.mul_one]

end H3

end RollingLaw
