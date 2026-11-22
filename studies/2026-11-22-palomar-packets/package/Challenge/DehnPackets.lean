module

public import Mathlib

@[expose] public section

/-!
# Dehn packets: two icosahedral pairs that cannot fill space

**Informal statement.** A convex polytope is a bounded intersection of finitely many closed half-spaces (`IsPoly`).
A tiling (`ConvexTiling`) covers space with convex polytopes that have interior points and pairwise disjoint
interiors, finitely many near each point; it need not be face to face. Angles are read from the set alone, as in the
Dehn Canon: at `x` the directions that stay in the set form a cone (`tcone`); where the directions `v` with `v`, `-v`
both in it span a line `K` (`linSpace`), the angle is 2π times the share of the unit disc of `Kᗮ` in the cone
(`wedgeAngle`); `EdgeAngle P θ` says that `θ` occurs so. A similar copy (`SimilarCopy`) is the image of a positive
scaling under an isometry (reflections allowed).

1. `lemma3` (**Lemma 3**): π, α = arctan φ, β = arccos(1/√6), γ = arccos √(2/3) are linearly independent over ℚ.
2. `lemma2` (**Lemma 2**): at an edge point `x` of tile `i` there are finitely many tiles, `i` among them, with angles
   `ω` summing to 2π: `ω i` is the angle of tile `i` at `x`, each `ω j` a dihedral angle of tile `j`, or π, or 2π.
3. `theorem4a_copies` (**Theorem 4 (a)**): in a tiling of ℝ³ by similar copies of the dodecahedron centre pyramid
   (`pyrDSet`), the truncated icosahedron (`tiSet`), the dodecahedron (`dhSet`), the icosahedron (`ihSet`), the
   truncated octahedron (`toSet`), the truncated cuboctahedron (`tcoSet`), and convex polytopes whose dihedral angles
   are all nonnegative rational multiples of π (`RationalAngles`), no tile is a copy of the pyramid or of the
   truncated icosahedron.
4. `theorem4b_copies` (**Theorem 4 (b)**): the same for the icosahedron centre pyramid (`pyrISet`) and the truncated
   dodecahedron (`tdSet`).

Each solid is the solution set of its face inequalities `⟪N k, x⟫ ≤ B k`, exact in ℚ(√5) or ℚ(√2) (the pyramids'
apex is the origin). The truncated icosidodecahedron of the paper's helper list is not built here.

**Sources.** DICTO, *From Dehn Packets to Scutoids: How the Fullerene Star Fills Space*, Zenodo (2026),
doi:10.5281/zenodo.24411660: Lemmas 2, 3 and Theorem 4 (a), (b). The set-defined angle is that of DICTO's *The Dehn
Canon* (Palomar PALOMAR-2026-11-20-000003). Every definition and statement is copied character for character from
the Lean library (namespaces `DehnCanon.Library`, `Packets`, `PacketsGen`; the qualifier `DehnCanon.Library.`
dropped); the comment before each group names its file.
-/

namespace DehnPackets

-- from Dehn2Poly.lean
section
open scoped RealInnerProductSpace
open Set

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The solution set of a system of linear inequalities `⟪a i, x⟫ ≤ b i`. -/
def sol {ι : Type} (a : ι → E) (b : ι → ℝ) : Set E := {x | ∀ i, ⟪a i, x⟫ ≤ b i}

/-- A convex polytope: a bounded intersection of finitely many closed half-spaces. -/
def IsPoly (P : Set E) : Prop :=
  Bornology.IsBounded P ∧ ∃ (ι : Type) (_ : Fintype ι) (a : ι → E) (b : ι → ℝ), P = sol a b

end

-- from Dehn2Local.lean
section
open scoped RealInnerProductSpace
open Set MeasureTheory Module TensorProduct

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

/-- The cone of directions that stay in `P` near the point `x` of `P` (empty when `x ∉ P`). -/
def tcone (P : Set E) (x : E) : Set E := {v | x ∈ P ∧ ∃ t : ℝ, 0 < t ∧ x + t • v ∈ P}

/-- The span of the directions `v` of a cone for which `-v` is in the cone too. -/
def linSpace (T : Set E) : Submodule ℝ E := Submodule.span ℝ {v | v ∈ T ∧ -v ∈ T}

/-- The part of the cone `T` inside the open unit disc of the space perpendicular to `K`. -/
def wedgeSet (T : Set E) (K : Submodule ℝ E) : Set Kᗮ := {w | (w : E) ∈ T ∧ ‖w‖ < 1}

/-- The angle of the cone `T` around the line `K`: 2π × area(T ∩ unit disc of Kᗮ) / area(unit disc of Kᗮ). -/
noncomputable def wedgeAngle (T : Set E) (K : Submodule ℝ E) : ℝ :=
  2 * Real.pi * ((volume (wedgeSet T K)).toReal / (volume (Metric.ball (0 : Kᗮ) 1)).toReal)

end

-- from Dehn2R3.lean
section
open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct

/-- Coordinate 3-space. -/
abbrev R3 := EuclideanSpace ℝ (Fin 3)

end

-- from Angles.lean
section
open Real

/-- `α = arctan φ` (58.28°), half the dihedral angle of the regular dodecahedron. -/
noncomputable def α : ℝ := Real.arctan ((1 + √5) / 2)

/-- `β = arccos (1/√6)` (65.91°); `3π/4 − β` is half the dihedral angle of the regular icosahedron. -/
noncomputable def β : ℝ := Real.arccos (1 / √6)

/-- `γ = arccos √(2/3)` (35.26°); `2γ = arccos (1/3)` is the dihedral angle of the regular tetrahedron. -/
noncomputable def γ : ℝ := Real.arccos (√(2 / 3))

/-- **Lemma 3 of the paper: π, α, β and γ are linearly independent over ℚ.** -/
theorem lemma3 (q a b c : ℚ) (h : (q : ℝ) * π + a * α + b * β + c * γ = 0) :
    q = 0 ∧ a = 0 ∧ b = 0 ∧ c = 0 := by
  sorry

end

-- from Lemma2.lean
section
open Set MeasureTheory Module Filter Topology
open scoped RealInnerProductSpace

/-- **A tiling of space by convex polytopes.** -/
structure ConvexTiling (ι : Type*) (E : Type*) [NormedAddCommGroup E] [InnerProductSpace ℝ E] where
  /-- The tiles. -/
  P : ι → Set E
  poly : ∀ i, IsPoly (P i)
  nonempty_interior : ∀ i, (interior (P i)).Nonempty
  cover : ∀ x, ∃ i, x ∈ P i
  disjoint : Pairwise fun i j => Disjoint (interior (P i)) (interior (P j))
  locallyFinite : LocallyFinite P

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
variable [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] [Fact (finrank ℝ E = 3)]

/-- **Lemma 2 of the paper: angles round an edge.** -/
theorem lemma2 {ι : Type*} (T : ConvexTiling ι E) {i : ι} {x : E} (hx : x ∈ T.P i)
    (h1 : finrank ℝ (linSpace (tcone (T.P i) x)) = 1) :
    ∃ (J : Finset ι) (ω : ι → ℝ), i ∈ J ∧
      ω i = wedgeAngle (tcone (T.P i) x) (linSpace (tcone (T.P i) x)) ∧
      (∀ j ∈ J, (∃ y ∈ T.P j, finrank ℝ (linSpace (tcone (T.P j) y)) = 1 ∧
          ω j = wedgeAngle (tcone (T.P j) y) (linSpace (tcone (T.P j) y))) ∨
        ω j = Real.pi ∨ ω j = 2 * Real.pi) ∧
      ∑ j ∈ J, ω j = 2 * Real.pi := by
  sorry

/-- `θ` is a dihedral angle of `P`, read from the set at an edge point. -/
def EdgeAngle (P : Set E) (θ : ℝ) : Prop :=
  ∃ x ∈ P, finrank ℝ (linSpace (tcone P x)) = 1 ∧ wedgeAngle (tcone P x) (linSpace (tcone P x)) = θ

end

-- from Pieces.lean
section
open Set MeasureTheory Module Filter Topology
open scoped RealInnerProductSpace Pointwise

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

/-- `Q` is a similar copy of `S`: the image of a positive scaling of `S` under a rigid motion (reflections
allowed). -/
def SimilarCopy (Q S : Set E) : Prop := ∃ (g : E ≃ᵃⁱ[ℝ] E) (c : ℝ), 0 < c ∧ Q = g '' (c • S)

end

-- from GenPyrD.lean
section
open scoped RealInnerProductSpace Real
open Set Module

/-- Outward face normals. -/
noncomputable def pyrDN : Fin 6 → R3 :=
  ![!₂[0, 2, (1 + √5)], !₂[4, (-2 + 2 * √5), (-2 - 2 * √5)], !₂[(2 + 2 * √5), (-4), (2 - 2 * √5)], !₂[(-4), (-2 + 2 * √5), (-2 - 2 * √5)],
    !₂[(-2 - 2 * √5), (-4), (2 - 2 * √5)], !₂[0, (-8), 0]]

/-- Offsets. -/
noncomputable def pyrDB : Fin 6 → ℝ := ![(6 + 2 * √5), 0, 0, 0, 0, 0]

def pyrDSet : Set R3 := sol pyrDN pyrDB

-- from GenTI.lean
/-- Outward face normals. -/
noncomputable def tiN : Fin 32 → R3 :=
  ![!₂[0, 2, (1 + √5)], !₂[0, 2, (-1 - √5)], !₂[0, (-2), (1 + √5)], !₂[0, (-2), (-1 - √5)],
    !₂[(1 + √5), 0, 2], !₂[(1 + √5), 0, (-2)], !₂[(-1 - √5), 0, 2], !₂[(-1 - √5), 0, (-2)],
    !₂[2, (1 + √5), 0], !₂[2, (-1 - √5), 0], !₂[(-2), (1 + √5), 0], !₂[(-2), (-1 - √5), 0],
    !₂[2, 2, 2], !₂[2, 2, (-2)], !₂[2, (-2), 2], !₂[2, (-2), (-2)],
    !₂[(-2), 2, 2], !₂[(-2), 2, (-2)], !₂[(-2), (-2), 2], !₂[(-2), (-2), (-2)],
    !₂[0, (1 + √5), (-1 + √5)], !₂[0, (1 + √5), (1 - √5)], !₂[0, (-1 - √5), (-1 + √5)], !₂[0, (-1 - √5), (1 - √5)],
    !₂[(-1 + √5), 0, (1 + √5)], !₂[(-1 + √5), 0, (-1 - √5)], !₂[(1 - √5), 0, (1 + √5)], !₂[(1 - √5), 0, (-1 - √5)],
    !₂[(1 + √5), (-1 + √5), 0], !₂[(1 + √5), (1 - √5), 0], !₂[(-1 - √5), (-1 + √5), 0], !₂[(-1 - √5), (1 - √5), 0]]

/-- Offsets. -/
noncomputable def tiB : Fin 32 → ℝ := ![(22 + 6 * √5), (22 + 6 * √5), (22 + 6 * √5), (22 + 6 * √5), (22 + 6 * √5), (22 + 6 * √5), (22 + 6 * √5), (22 + 6 * √5), (22 + 6 * √5), (22 + 6 * √5), (22 + 6 * √5), (22 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5), (18 + 6 * √5)]

def tiSet : Set R3 := sol tiN tiB

-- from GenPyrI.lean
/-- Outward face normals. -/
noncomputable def pyrIN : Fin 4 → R3 :=
  ![!₂[2, 2, 2], !₂[(-4), (-6 - 2 * √5), (2 + 2 * √5)], !₂[(-6 - 2 * √5), (2 + 2 * √5), (-4)], !₂[(2 + 2 * √5), (-4), (-6 - 2 * √5)]]

/-- Offsets. -/
noncomputable def pyrIB : Fin 4 → ℝ := ![(6 + 2 * √5), 0, 0, 0]

def pyrISet : Set R3 := sol pyrIN pyrIB

-- from GenTD.lean
/-- Outward face normals. -/
noncomputable def tdN : Fin 32 → R3 :=
  ![!₂[0, 2, (1 + √5)], !₂[0, 2, (-1 - √5)], !₂[0, (-2), (1 + √5)], !₂[0, (-2), (-1 - √5)],
    !₂[(1 + √5), 0, 2], !₂[(1 + √5), 0, (-2)], !₂[(-1 - √5), 0, 2], !₂[(-1 - √5), 0, (-2)],
    !₂[2, (1 + √5), 0], !₂[2, (-1 - √5), 0], !₂[(-2), (1 + √5), 0], !₂[(-2), (-1 - √5), 0],
    !₂[2, 2, 2], !₂[2, 2, (-2)], !₂[2, (-2), 2], !₂[2, (-2), (-2)],
    !₂[(-2), 2, 2], !₂[(-2), 2, (-2)], !₂[(-2), (-2), 2], !₂[(-2), (-2), (-2)],
    !₂[0, (1 + √5), (-1 + √5)], !₂[0, (1 + √5), (1 - √5)], !₂[0, (-1 - √5), (-1 + √5)], !₂[0, (-1 - √5), (1 - √5)],
    !₂[(-1 + √5), 0, (1 + √5)], !₂[(-1 + √5), 0, (-1 - √5)], !₂[(1 - √5), 0, (1 + √5)], !₂[(1 - √5), 0, (-1 - √5)],
    !₂[(1 + √5), (-1 + √5), 0], !₂[(1 + √5), (1 - √5), 0], !₂[(-1 - √5), (-1 + √5), 0], !₂[(-1 - √5), (1 - √5), 0]]

/-- Offsets. -/
noncomputable def tdB : Fin 32 → ℝ := ![(10 + 6 * √5), (10 + 6 * √5), (10 + 6 * √5), (10 + 6 * √5), (10 + 6 * √5), (10 + 6 * √5), (10 + 6 * √5), (10 + 6 * √5), (10 + 6 * √5), (10 + 6 * √5), (10 + 6 * √5), (10 + 6 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5), (16 + 4 * √5)]

def tdSet : Set R3 := sol tdN tdB

-- from GenDH.lean
/-- Outward face normals. -/
noncomputable def dhN : Fin 12 → R3 :=
  ![!₂[0, 2, (1 + √5)], !₂[0, 2, (-1 - √5)], !₂[0, (-2), (1 + √5)], !₂[0, (-2), (-1 - √5)],
    !₂[(1 + √5), 0, 2], !₂[(1 + √5), 0, (-2)], !₂[(-1 - √5), 0, 2], !₂[(-1 - √5), 0, (-2)],
    !₂[2, (1 + √5), 0], !₂[2, (-1 - √5), 0], !₂[(-2), (1 + √5), 0], !₂[(-2), (-1 - √5), 0]]

/-- Offsets. -/
noncomputable def dhB : Fin 12 → ℝ := ![(6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5)]

def dhSet : Set R3 := sol dhN dhB

-- from GenIH.lean
/-- Outward face normals. -/
noncomputable def ihN : Fin 20 → R3 :=
  ![!₂[2, 2, 2], !₂[2, 2, (-2)], !₂[2, (-2), 2], !₂[2, (-2), (-2)],
    !₂[(-2), 2, 2], !₂[(-2), 2, (-2)], !₂[(-2), (-2), 2], !₂[(-2), (-2), (-2)],
    !₂[0, (1 + √5), (-1 + √5)], !₂[0, (1 + √5), (1 - √5)], !₂[0, (-1 - √5), (-1 + √5)], !₂[0, (-1 - √5), (1 - √5)],
    !₂[(-1 + √5), 0, (1 + √5)], !₂[(-1 + √5), 0, (-1 - √5)], !₂[(1 - √5), 0, (1 + √5)], !₂[(1 - √5), 0, (-1 - √5)],
    !₂[(1 + √5), (-1 + √5), 0], !₂[(1 + √5), (1 - √5), 0], !₂[(-1 - √5), (-1 + √5), 0], !₂[(-1 - √5), (1 - √5), 0]]

/-- Offsets. -/
noncomputable def ihB : Fin 20 → ℝ := ![(6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5), (6 + 2 * √5)]

def ihSet : Set R3 := sol ihN ihB

-- from GenTO.lean
/-- Outward face normals. -/
noncomputable def toN : Fin 14 → R3 :=
  ![!₂[1, 0, 0], !₂[(-1), 0, 0], !₂[0, 1, 0], !₂[0, (-1), 0],
    !₂[0, 0, 1], !₂[0, 0, (-1)], !₂[1, 1, 1], !₂[1, 1, (-1)],
    !₂[1, (-1), 1], !₂[1, (-1), (-1)], !₂[(-1), 1, 1], !₂[(-1), 1, (-1)],
    !₂[(-1), (-1), 1], !₂[(-1), (-1), (-1)]]

/-- Offsets. -/
noncomputable def toB : Fin 14 → ℝ := ![2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3]

def toSet : Set R3 := sol toN toB

-- from GenTCO.lean
/-- Outward face normals. -/
noncomputable def tcoN : Fin 26 → R3 :=
  ![!₂[1, 1, 0], !₂[1, (-1), 0], !₂[(-1), 1, 0], !₂[(-1), (-1), 0],
    !₂[0, 1, 1], !₂[0, 1, (-1)], !₂[0, (-1), 1], !₂[0, (-1), (-1)],
    !₂[1, 0, 1], !₂[1, 0, (-1)], !₂[(-1), 0, 1], !₂[(-1), 0, (-1)],
    !₂[1, 1, 1], !₂[1, 1, (-1)], !₂[1, (-1), 1], !₂[1, (-1), (-1)],
    !₂[(-1), 1, 1], !₂[(-1), 1, (-1)], !₂[(-1), (-1), 1], !₂[(-1), (-1), (-1)],
    !₂[1, 0, 0], !₂[(-1), 0, 0], !₂[0, 1, 0], !₂[0, (-1), 0],
    !₂[0, 0, 1], !₂[0, 0, (-1)]]

/-- Offsets. -/
noncomputable def tcoB : Fin 26 → ℝ := ![(2 + 3 * √2), (2 + 3 * √2), (2 + 3 * √2), (2 + 3 * √2), (2 + 3 * √2), (2 + 3 * √2), (2 + 3 * √2), (2 + 3 * √2), (2 + 3 * √2), (2 + 3 * √2), (2 + 3 * √2), (2 + 3 * √2), (3 + 3 * √2), (3 + 3 * √2), (3 + 3 * √2), (3 + 3 * √2), (3 + 3 * √2), (3 + 3 * √2), (3 + 3 * √2), (3 + 3 * √2), (1 + 2 * √2), (1 + 2 * √2), (1 + 2 * √2), (1 + 2 * √2), (1 + 2 * √2), (1 + 2 * √2)]

def tcoSet : Set R3 := sol tcoN tcoB

end

-- from Copies.lean
section
open Set Module

/-- A convex piece whose dihedral angles, read from the set, are nonnegative rational multiples of π. -/
def RationalAngles (P : Set R3) : Prop := ∀ θ, EdgeAngle P θ → ∃ q : ℚ, 0 ≤ q ∧ θ = q * Real.pi

/-- **Theorem 4 (a)** for tilings by copies, with no hypothesis. -/
theorem theorem4a_copies {ι : Type*} (T : ConvexTiling ι R3)
    (hk : ∀ i, SimilarCopy (T.P i) pyrDSet ∨ SimilarCopy (T.P i) tiSet ∨ SimilarCopy (T.P i) dhSet ∨
      SimilarCopy (T.P i) ihSet ∨ SimilarCopy (T.P i) toSet ∨ SimilarCopy (T.P i) tcoSet ∨
      RationalAngles (T.P i)) (i : ι) :
    ¬ SimilarCopy (T.P i) pyrDSet ∧ ¬ SimilarCopy (T.P i) tiSet := by
  sorry

/-- **Theorem 4 (b)** for tilings by copies, with no hypothesis. -/
theorem theorem4b_copies {ι : Type*} (T : ConvexTiling ι R3)
    (hk : ∀ i, SimilarCopy (T.P i) pyrISet ∨ SimilarCopy (T.P i) tdSet ∨ SimilarCopy (T.P i) dhSet ∨
      SimilarCopy (T.P i) ihSet ∨ SimilarCopy (T.P i) toSet ∨ SimilarCopy (T.P i) tcoSet ∨
      RationalAngles (T.P i)) (i : ι) :
    ¬ SimilarCopy (T.P i) pyrISet ∧ ¬ SimilarCopy (T.P i) tdSet := by
  sorry

end

end DehnPackets
