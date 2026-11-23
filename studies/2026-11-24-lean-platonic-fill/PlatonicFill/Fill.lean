/-
Platonic solids filling space, part 2: which Platonic solids can take part in a tiling of 3-space.

Tilings are those of the packets development (`ConvexTiling`): convex polytopes (bounded intersections of
finitely many closed half-spaces) with interior points, covering space, with pairwise disjoint interiors, finitely
many meeting a neighbourhood of each point; nothing is assumed about how tiles meet (not necessarily
face-to-face). A tile may be any similar copy of a solid (`SimilarCopy`: rigid motion, reflections allowed, and
any positive scaling; each tile its own scale).

* `aristotle_error`: **no tiling of 3-space by similar copies of the regular tetrahedron** (Aristotle, De Caelo
  III.8, said that tetrahedra fill space; see Lagarias–Zong, Notices AMS 59 (2012)). Stronger, `no_tetra`: in a
  tiling by copies of the regular tetrahedron and convex pieces whose dihedral angles are rational multiples of π,
  no tile is a tetrahedron.
* `no_octa`, `no_dodeca`, `no_icosa` and `octa_alone`, `dodeca_alone`, `icosa_alone`: the same for the regular
  octahedron, the regular dodecahedron and the regular icosahedron.
* `platonic_mix`: in a tiling by similar copies of the five Platonic solids (and convex pieces with rational
  angles), no tile is a dodecahedron or an icosahedron.

Method: every angle is written as `q·π + a·α + b·β + c·γ` (`Co`, packets development), and `π, α, β, γ` are
linearly independent over ℚ (`lemma3`, by Niven's theorem; `2γ = arccos (1/3)`). Around an edge point of a tile
the angles of the tiles there add up to `2π`, each a dihedral angle of its tile, or `π`, or `2π` (`lemma2`). A
weight `q + u·a + v·b + t·c` is then well defined on angles; if it is nonnegative on every angle that can occur,
the ring bound `ring_wt_le` gives weight at most 2 for each angle of the ring. A solid with an angle of weight
above 2 cannot occur. Weights: tetrahedron (t = 2: weight 4), octahedron (t = −1: 3), dodecahedron (u = 2: 4),
icosahedron (v = −1: 7/2); the mixture (u, v, t) = (2, −1, 0) gives weights 0, 1, 1/2, 4, 7/2 to the
tetrahedron, octahedron, cube, dodecahedron, icosahedron.
No `sorry`.
-/
module

public import PlatonicFill.Solids

@[expose] public section

open Set Module Real

namespace PlatonicFill

open Packets PacketsGen
open DehnCanon.Library (R3)

/-! ### The weight and the ring bound -/

/-- The weight `q + u·a + v·b + t·c` of an angle `q·π + a·α + b·β + c·γ`. -/
def wt (u v t : ℚ) (x : Co) : ℚ := x.q + u * x.a + v * x.b + t * x.c

/-- `θ` has coordinates of nonnegative weight. -/
def Light3 (u v t : ℚ) (θ : ℝ) : Prop := ∃ x : Co, θ = x.val ∧ 0 ≤ wt u v t x

lemma light3_zero {u v t : ℚ} : Light3 u v t 0 := ⟨⟨0, 0, 0, 0⟩, by simp [Co.val], by simp [wt]⟩

lemma Light3.add {u v t : ℚ} {θ φ : ℝ} (h1 : Light3 u v t θ) (h2 : Light3 u v t φ) :
    Light3 u v t (θ + φ) := by
  obtain ⟨x, hx, hx0⟩ := h1
  obtain ⟨y, hy, hy0⟩ := h2
  refine ⟨⟨x.q + y.q, x.a + y.a, x.b + y.b, x.c + y.c⟩, ?_, ?_⟩
  · rw [hx, hy]; simp only [Co.val]; push_cast; ring
  · have : wt u v t ⟨x.q + y.q, x.a + y.a, x.b + y.b, x.c + y.c⟩ = wt u v t x + wt u v t y := by
      simp only [wt]; ring
    rw [this]; linarith

lemma light3_sum {ι : Type*} {u v t : ℚ} (J : Finset ι) (ω : ι → ℝ) (h : ∀ j ∈ J, Light3 u v t (ω j)) :
    Light3 u v t (∑ j ∈ J, ω j) :=
  Finset.sum_induction ω (Light3 u v t) (fun _ _ h1 h2 => h1.add h2) light3_zero h

/-- **The ring bound.** If every angle of a ring adding up to `2π` has coordinates of nonnegative weight, every
angle of the ring has weight at most 2 (`lemma3` makes the coordinates add up exactly). -/
theorem ring_wt_le {ι : Type*} {u v t : ℚ} {J : Finset ι} {ω : ι → ℝ} (hL : ∀ j ∈ J, Light3 u v t (ω j))
    (hsum : ∑ j ∈ J, ω j = 2 * π) {i : ι} (hi : i ∈ J) {x : Co} (hx : ω i = x.val) : wt u v t x ≤ 2 := by
  classical
  obtain ⟨y, hy, hy0⟩ := light3_sum (J.erase i) ω (fun j hj => hL j (Finset.mem_of_mem_erase hj))
  rw [← Finset.add_sum_erase J ω hi, hx, hy] at hsum
  obtain ⟨h1, h2, h3, h4⟩ := lemma3 (x.q + y.q - 2) (x.a + y.a) (x.b + y.b) (x.c + y.c) (by
    simp only [Co.val] at hsum; push_cast; linear_combination hsum)
  have hw : wt u v t x + wt u v t y = (x.q + y.q) + u * (x.a + y.a) + v * (x.b + y.b) + t * (x.c + y.c) := by
    simp only [wt]; ring
  rw [h2, h3, h4] at hw
  linarith

/-- **The ring bound in a tiling** (from Lemma 2 of the packets development). -/
theorem tiling_wt_le {ι : Type*} (T : ConvexTiling ι R3) {u v t : ℚ}
    (hg : ∀ j θ, EdgeAngle (T.P j) θ → Light3 u v t θ) {i : ι} {x : Co} (hx : EdgeAngle (T.P i) x.val) :
    wt u v t x ≤ 2 := by
  obtain ⟨p, hp, h1, hθ⟩ := hx
  obtain ⟨J, ω, hiJ, hωi, hcl, hsum⟩ := lemma2 T hp h1
  refine ring_wt_le (fun j hj => ?_) hsum hiJ (hωi.trans hθ)
  rcases hcl j hj with ⟨y, hy, hy1, hωj⟩ | h | h
  · exact hg j _ ⟨y, hy, hy1, hωj.symm⟩
  · rw [h]; exact ⟨⟨1, 0, 0, 0⟩, by simp [Co.val], by simp [wt]⟩
  · rw [h]; exact ⟨⟨2, 0, 0, 0⟩, by simp [Co.val], by simp [wt]⟩

/-! ### Pieces -/

/-- A convex piece whose dihedral angles, read from the set, are nonnegative rational multiples of π. -/
def RationalAngles (P : Set R3) : Prop := ∀ θ, EdgeAngle P θ → ∃ q : ℚ, 0 ≤ q ∧ θ = q * π

lemma light3_of_rational {P : Set R3} (h : RationalAngles P) (u v t : ℚ) :
    ∀ θ, EdgeAngle P θ → Light3 u v t θ := by
  intro θ hθ
  obtain ⟨q, hq, rfl⟩ := h θ hθ
  exact ⟨⟨q, 0, 0, 0⟩, by simp [Co.val], by simpa [wt] using hq⟩

/-- The angles of a similar copy of a solid with one dihedral angle `x.val`. -/
lemma light3_of_copy {Q S : Set R3} {x : Co} (hc : SimilarCopy Q S) (hS : ∀ θ, EdgeAngle S θ ↔ θ = x.val)
    {u v t : ℚ} (hw : 0 ≤ wt u v t x) : ∀ θ, EdgeAngle Q θ → Light3 u v t θ :=
  fun θ h => ⟨x, (hS θ).1 ((hc.edgeAngle_iff θ).1 h), hw⟩

lemma edgeAngle_of_copy {Q S : Set R3} {x : Co} (hc : SimilarCopy Q S) (hS : ∀ θ, EdgeAngle S θ ↔ θ = x.val) :
    EdgeAngle Q x.val :=
  (hc.edgeAngle_iff _).2 ((hS _).2 rfl)

/-- The five dihedral angles as coordinates. -/
def teCo : Co := ⟨0, 0, 0, 2⟩
def ocCo : Co := ⟨1, 0, 0, -2⟩
def cuCo : Co := ⟨1 / 2, 0, 0, 0⟩
def dhCo : Co := ⟨0, 2, 0, 0⟩
def ihCo : Co := ⟨3 / 2, 0, -2, 0⟩

lemma te_co (θ : ℝ) : EdgeAngle teSet θ ↔ θ = teCo.val := by
  rw [te_edgeAngle]; simp [teCo, Co.val]

lemma oc_co (θ : ℝ) : EdgeAngle ocSet θ ↔ θ = ocCo.val := by
  rw [oc_edgeAngle]; simp only [ocCo, Co.val]; push_cast; constructor <;> intro h <;> rw [h] <;> ring

lemma cu_co (θ : ℝ) : EdgeAngle cuSet θ ↔ θ = cuCo.val := by
  rw [cu_edgeAngle]; simp only [cuCo, Co.val]; push_cast; constructor <;> intro h <;> rw [h] <;> ring

lemma dh_co (θ : ℝ) : EdgeAngle dhSet θ ↔ θ = dhCo.val := by
  rw [dh_edgeAngle]; simp [dhCo, Co.val]

lemma ih_co (θ : ℝ) : EdgeAngle ihSet θ ↔ θ = ihCo.val := by
  rw [ih_edgeAngle]; simp only [ihCo, Co.val]; push_cast; constructor <;> intro h <;> rw [h] <;> ring

/-- One solid `S` with heavy angle `x` (weight above 2), together with rational-angle pieces: no tile is a
copy of `S`. -/
theorem no_copy {ι : Type*} (T : ConvexTiling ι R3) {S : Set R3} {x : Co}
    (hS : ∀ θ, EdgeAngle S θ ↔ θ = x.val) {u v t : ℚ} (hpos : 0 ≤ wt u v t x) (hbig : 2 < wt u v t x)
    (hk : ∀ i, SimilarCopy (T.P i) S ∨ RationalAngles (T.P i)) (i : ι) : ¬ SimilarCopy (T.P i) S := by
  intro hi
  have hg : ∀ j θ, EdgeAngle (T.P j) θ → Light3 u v t θ := by
    intro j
    rcases hk j with h | h
    · exact light3_of_copy h hS hpos
    · exact light3_of_rational h u v t
  have := tiling_wt_le T hg (edgeAngle_of_copy hi hS)
  linarith

/-- A tiling has a tile (it covers the origin). -/
lemma exists_tile {ι : Type*} (T : ConvexTiling ι R3) : Nonempty ι := ⟨(T.cover 0).choose⟩

/-! ### The tetrahedron: Aristotle's error -/

/-- In a tiling of 3-space by similar copies of the regular tetrahedron and convex pieces with rational
dihedral angles (cubes, for instance), no tile is a tetrahedron. -/
theorem no_tetra {ι : Type*} (T : ConvexTiling ι R3)
    (hk : ∀ i, SimilarCopy (T.P i) teSet ∨ RationalAngles (T.P i)) (i : ι) : ¬ SimilarCopy (T.P i) teSet :=
  no_copy T te_co (u := 0) (v := 0) (t := 2) (by norm_num [wt, teCo]) (by norm_num [wt, teCo]) hk i

/-- **Aristotle's error.** There is no tiling of 3-space by similar copies of the regular tetrahedron (any
sizes, reflections allowed, not necessarily face-to-face). -/
theorem aristotle_error {ι : Type*} (T : ConvexTiling ι R3) : ¬ ∀ i, SimilarCopy (T.P i) teSet := by
  intro h
  obtain ⟨i⟩ := exists_tile T
  exact no_tetra T (fun j => Or.inl (h j)) i (h i)

/-! ### The octahedron, the dodecahedron, the icosahedron -/

theorem no_octa {ι : Type*} (T : ConvexTiling ι R3)
    (hk : ∀ i, SimilarCopy (T.P i) ocSet ∨ RationalAngles (T.P i)) (i : ι) : ¬ SimilarCopy (T.P i) ocSet :=
  no_copy T oc_co (u := 0) (v := 0) (t := -1) (by norm_num [wt, ocCo]) (by norm_num [wt, ocCo]) hk i

theorem no_dodeca {ι : Type*} (T : ConvexTiling ι R3)
    (hk : ∀ i, SimilarCopy (T.P i) dhSet ∨ RationalAngles (T.P i)) (i : ι) : ¬ SimilarCopy (T.P i) dhSet :=
  no_copy T dh_co (u := 2) (v := 0) (t := 0) (by norm_num [wt, dhCo]) (by norm_num [wt, dhCo]) hk i

theorem no_icosa {ι : Type*} (T : ConvexTiling ι R3)
    (hk : ∀ i, SimilarCopy (T.P i) ihSet ∨ RationalAngles (T.P i)) (i : ι) : ¬ SimilarCopy (T.P i) ihSet :=
  no_copy T ih_co (u := 0) (v := -1) (t := 0) (by norm_num [wt, ihCo]) (by norm_num [wt, ihCo]) hk i

/-- No tiling of 3-space by similar copies of the regular octahedron. -/
theorem octa_alone {ι : Type*} (T : ConvexTiling ι R3) : ¬ ∀ i, SimilarCopy (T.P i) ocSet := by
  intro h
  obtain ⟨i⟩ := exists_tile T
  exact no_octa T (fun j => Or.inl (h j)) i (h i)

/-- No tiling of 3-space by similar copies of the regular dodecahedron. -/
theorem dodeca_alone {ι : Type*} (T : ConvexTiling ι R3) : ¬ ∀ i, SimilarCopy (T.P i) dhSet := by
  intro h
  obtain ⟨i⟩ := exists_tile T
  exact no_dodeca T (fun j => Or.inl (h j)) i (h i)

/-- No tiling of 3-space by similar copies of the regular icosahedron. -/
theorem icosa_alone {ι : Type*} (T : ConvexTiling ι R3) : ¬ ∀ i, SimilarCopy (T.P i) ihSet := by
  intro h
  obtain ⟨i⟩ := exists_tile T
  exact no_icosa T (fun j => Or.inl (h j)) i (h i)

/-! ### Mixtures of Platonic solids -/

/-- **In a tiling of 3-space by similar copies of the five Platonic solids** (and convex pieces with rational
dihedral angles), **no tile is a dodecahedron or an icosahedron.** -/
theorem platonic_mix {ι : Type*} (T : ConvexTiling ι R3)
    (hk : ∀ i, SimilarCopy (T.P i) teSet ∨ SimilarCopy (T.P i) ocSet ∨ SimilarCopy (T.P i) cuSet ∨
      SimilarCopy (T.P i) dhSet ∨ SimilarCopy (T.P i) ihSet ∨ RationalAngles (T.P i)) (i : ι) :
    ¬ SimilarCopy (T.P i) dhSet ∧ ¬ SimilarCopy (T.P i) ihSet := by
  have hg : ∀ j θ, EdgeAngle (T.P j) θ → Light3 2 (-1) 0 θ := by
    intro j
    rcases hk j with h | h | h | h | h | h
    · exact light3_of_copy h te_co (by norm_num [wt, teCo])
    · exact light3_of_copy h oc_co (by norm_num [wt, ocCo])
    · exact light3_of_copy h cu_co (by norm_num [wt, cuCo])
    · exact light3_of_copy h dh_co (by norm_num [wt, dhCo])
    · exact light3_of_copy h ih_co (by norm_num [wt, ihCo])
    · exact light3_of_rational h _ _ _
  refine ⟨fun hi => ?_, fun hi => ?_⟩
  · have := tiling_wt_le T hg (edgeAngle_of_copy hi dh_co)
    norm_num [wt, dhCo] at this
  · have := tiling_wt_le T hg (edgeAngle_of_copy hi ih_co)
    norm_num [wt, ihCo] at this

end PlatonicFill
