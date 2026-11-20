module

public import Mathlib

@[expose] public section

/-!
# Grünbaum's zone question at k = 10: the definitions (generated from Challenge.lean)

**Informal statement.** There is a polyhedron `P` in Euclidean 3-space with these properties.

* `P` is a polyhedron of spherical type in Grünbaum's sense (2010, p. 9): its surface is homeomorphic to a sphere and
  adjacent faces are not coplanar. Here `P` is the solid: a compact set equal to the closure of its interior, whose
  frontier is the union of its 30 parallelogram faces; the 30 faces are distinct, and two faces meet in a common side,
  a common corner, or not at all.
* `P` is rhombic and monohedral: every face is a rhombus, any two faces are congruent, and the diagonals of every face
  are in the golden ratio.
* Every zone of `P` has exactly 10 faces. A zone is a belt: start from a face and one of its side directions `w`, and
  pass repeatedly to the face across a side parallel to `w`; the zone is the set of faces reached. The statement also
  says that each belt is the set of all faces with a side parallel to `w`. Two calibration theorems check this
  definition on known solids: it gives 4 for the cube and 6 for the rhombic dodecahedron.
* `P` is a parallelohedron: its translates by the vectors of a lattice cover space and have pairwise disjoint
  interiors. The tiling is moreover face to face, in the per-face sense of `FaceToFace`: every face of `P` is also a
  face of a translate of `P` by a non-zero lattice vector.

This gives an example for `k = 10` for the question of B. Grünbaum, "The Bilinski dodecahedron, and assorted
parallelohedra, zonohedra, monohedra, isozonohedra and otherhedra", *Math. Intelligencer* 32(4) (2010) 5–15: "Given an
even integer k ≥ 4, is there a rhombic monohedral parallelohedron such that every zone has exactly k faces?" Grünbaum
defines a parallelohedron as a polyhedron that admits a tiling of space by translated copies of itself; a lattice
tiling is a special case, so the main statement here is stronger. The second theorem states the result in his terms.

**Witness (in the Solution, not part of the statement).** DICTO's Grünbaum–Escher Triacontahedron (GET B): the
rhombic triacontahedron less four oblate golden rhombohedra, the union of 16 golden rhombohedra.
-/

namespace GrunbaumK10

open Set
open scoped Pointwise

/-- Euclidean 3-space -/
abbrev Space := EuclideanSpace ℝ (Fin 3)

/-- a parallelogram `p + [0,1] u + [0,1] v` -/
structure Parallelogram where
  p : Space
  u : Space
  v : Space

namespace Parallelogram

/-- the closed parallelogram as a set -/
def carrier (F : Parallelogram) : Set Space :=
  {x | ∃ s ∈ Icc (0 : ℝ) 1, ∃ t ∈ Icc (0 : ℝ) 1, x = F.p + s • F.u + t • F.v}

/-- the four corners, in cyclic order -/
def corners (F : Parallelogram) : Fin 4 → Space :=
  ![F.p, F.p + F.u, F.p + F.u + F.v, F.p + F.v]

/-- the four sides, side `i` joining corner `i` to corner `i + 1` -/
def side (F : Parallelogram) (i : Fin 4) : Set Space :=
  segment ℝ (F.corners i) (F.corners (i + 1))

/-- the parallelogram is not degenerate -/
def Nondegenerate (F : Parallelogram) : Prop := LinearIndependent ℝ ![F.u, F.v]

/-- a rhombus: a non-degenerate parallelogram with equal sides -/
def IsRhombus (F : Parallelogram) : Prop := F.Nondegenerate ∧ ‖F.u‖ = ‖F.v‖

/-- a golden rhombus: a rhombus whose long diagonal is the golden ratio times its short diagonal -/
def IsGoldenRhombus (F : Parallelogram) : Prop :=
  F.IsRhombus ∧ (‖F.u + F.v‖ = Real.goldenRatio * ‖F.u - F.v‖ ∨ ‖F.u - F.v‖ = Real.goldenRatio * ‖F.u + F.v‖)

/-- `w` is parallel to a side of the parallelogram -/
def HasSideParallel (F : Parallelogram) (w : Space) : Prop :=
  (∃ c : ℝ, c ≠ 0 ∧ F.u = c • w) ∨ (∃ c : ℝ, c ≠ 0 ∧ F.v = c • w)

end Parallelogram

/-- Two parallelograms are congruent: their corners are congruent point sets (Mathlib's `Congruent`, after some
relabelling of the corners). -/
def FacesCongruent (F G : Parallelogram) : Prop :=
  ∃ σ : Equiv.Perm (Fin 4), Congruent (F.corners ∘ σ) G.corners

/-- the faces `F i` and `F j` share a side -/
def Adjacent {m : ℕ} (F : Fin m → Parallelogram) (i j : Fin m) : Prop :=
  ∃ a b : Fin 4, (F i).side a = (F j).side b

/-- two faces meet in a common side, in a common corner, or not at all -/
def MeetProperly (F G : Parallelogram) : Prop :=
  F.carrier ∩ G.carrier = ∅ ∨
  (∃ a b : Fin 4, F.corners a = G.corners b ∧ F.carrier ∩ G.carrier = {F.corners a}) ∨
  (∃ a b : Fin 4, F.side a = G.side b ∧ F.carrier ∩ G.carrier = F.side a)

/-- `P` is a polyhedron of spherical type with the faces `F`: a compact solid, the closure of its interior, whose
frontier is the union of the faces and is homeomorphic to a sphere; the faces are non-degenerate and distinct, meet
properly, and adjacent faces are not coplanar (Grünbaum 2010, p. 9). -/
structure IsSphericalPolyhedron {m : ℕ} (P : Set Space) (F : Fin m → Parallelogram) : Prop where
  compact : IsCompact P
  closure_interior : closure (interior P) = P
  frontier_eq : frontier P = ⋃ i, (F i).carrier
  nondegenerate : ∀ i, (F i).Nondegenerate
  distinct : ∀ i j, (F i).carrier = (F j).carrier → i = j
  meet : ∀ i j, i ≠ j → MeetProperly (F i) (F j)
  sphere : Nonempty (frontier P ≃ₜ Metric.sphere (0 : Space) 1)
  not_coplanar : ∀ i j, i ≠ j → Adjacent F i j →
    ¬ Coplanar ℝ (range (F i).corners ∪ range (F j).corners)

/-- rhombic and monohedral: every face is a rhombus and any two faces are congruent -/
def IsRhombicMonohedral {m : ℕ} (F : Fin m → Parallelogram) : Prop :=
  (∀ i, (F i).IsRhombus) ∧ ∀ i j, FacesCongruent (F i) (F j)

/-- faces `i` and `j` share a side parallel to `w` -/
def AcrossSideParallel {m : ℕ} (F : Fin m → Parallelogram) (w : Space) (i j : Fin m) : Prop :=
  ∃ a b : Fin 4, (F i).side a = (F j).side b ∧
    ∃ c : ℝ, c ≠ 0 ∧ (F i).corners (a + 1) - (F i).corners a = c • w

/-- the zone (belt) through face `i` in the direction `w`: the faces reached from `i` by crossing sides parallel
to `w` -/
def zone {m : ℕ} (F : Fin m → Parallelogram) (i : Fin m) (w : Space) : Set (Fin m) :=
  {j | Relation.ReflTransGen (AcrossSideParallel F w) i j}

/-- every zone has exactly `k` faces, and it consists of all faces with a side parallel to its direction -/
def EveryZoneHas {m : ℕ} (F : Fin m → Parallelogram) (k : ℕ) : Prop :=
  ∀ i, ∀ w ∈ ({(F i).u, (F i).v} : Set Space),
    (zone F i w).ncard = k ∧ zone F i w = {j | (F j).HasSideParallel w}

/-- the lattice spanned by `b` -/
def lattice (b : Fin 3 → Space) : Set Space := AddSubgroup.closure (range b)

/-- the translates `t + P`, `t ∈ T`, cover space and have pairwise disjoint interiors -/
def TilesByTranslates (P : Set Space) (T : Set Space) : Prop :=
  (⋃ t ∈ T, t +ᵥ P) = univ ∧ T.Pairwise fun s t => Disjoint (interior (s +ᵥ P)) (interior (t +ᵥ P))

/-- Grünbaum's parallelohedron: some set of translates of `P` tiles space -/
def IsParallelohedron (P : Set Space) : Prop := ∃ T : Set Space, TilesByTranslates P T

/-- face to face, per face: every face of `P` is also a face of a translate of `P` by a non-zero vector of `T`
(together with `MeetProperly`, the frontier condition and disjoint interiors this gives the usual notion) -/
def FaceToFace {m : ℕ} (F : Fin m → Parallelogram) (T : Set Space) : Prop :=
  ∀ i, ∃ t ∈ T, t ≠ 0 ∧ ∃ j, t +ᵥ (F j).carrier = (F i).carrier

/-- the six faces of the unit cube `[0,1]³` (calibration of `EveryZoneHas`) -/
def cubeFaces : Fin 6 → Parallelogram := ![
  ⟨!₂[0, 0, 0], !₂[0, 1, 0], !₂[0, 0, 1]⟩,
  ⟨!₂[1, 0, 0], !₂[0, 1, 0], !₂[0, 0, 1]⟩,
  ⟨!₂[0, 0, 0], !₂[1, 0, 0], !₂[0, 0, 1]⟩,
  ⟨!₂[0, 1, 0], !₂[1, 0, 0], !₂[0, 0, 1]⟩,
  ⟨!₂[0, 0, 0], !₂[1, 0, 0], !₂[0, 1, 0]⟩,
  ⟨!₂[0, 0, 1], !₂[1, 0, 0], !₂[0, 1, 0]⟩]

/-- the twelve faces of the rhombic dodecahedron with vertices `(±1, ±1, ±1)` and `(±2, 0, 0)`, `(0, ±2, 0)`,
`(0, 0, ±2)` (calibration of `EveryZoneHas`) -/
def rhombicDodecahedronFaces : Fin 12 → Parallelogram := ![
  ⟨!₂[1, 1, -1], !₂[1, -1, 1], !₂[-1, 1, 1]⟩,
  ⟨!₂[1, -1, -1], !₂[1, 1, 1], !₂[-1, -1, 1]⟩,
  ⟨!₂[-1, 1, -1], !₂[-1, -1, 1], !₂[1, 1, 1]⟩,
  ⟨!₂[-1, -1, -1], !₂[-1, 1, 1], !₂[1, -1, 1]⟩,
  ⟨!₂[1, -1, 1], !₂[1, 1, -1], !₂[-1, 1, 1]⟩,
  ⟨!₂[1, -1, -1], !₂[1, 1, 1], !₂[-1, 1, -1]⟩,
  ⟨!₂[-1, -1, 1], !₂[-1, 1, -1], !₂[1, 1, 1]⟩,
  ⟨!₂[-1, -1, -1], !₂[-1, 1, 1], !₂[1, 1, -1]⟩,
  ⟨!₂[-1, 1, 1], !₂[1, 1, -1], !₂[1, -1, 1]⟩,
  ⟨!₂[-1, 1, -1], !₂[1, 1, 1], !₂[1, -1, -1]⟩,
  ⟨!₂[-1, -1, 1], !₂[1, -1, -1], !₂[1, 1, 1]⟩,
  ⟨!₂[-1, -1, -1], !₂[1, -1, 1], !₂[1, 1, -1]⟩]

end GrunbaumK10
