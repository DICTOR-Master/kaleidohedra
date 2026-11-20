module

public import Mathlib

@[expose] public section

/-!
# Hilbert's third problem, with the Dehn invariant of a set

**Informal statement.** In Euclidean 3-space, a convex polytope is a bounded intersection of finitely many closed
half-spaces (`IsPoly`). Two sets are *scissors congruent* (`ScissorsCongruent`) when the first is the union of
finitely many convex polytopes with pairwise disjoint interiors that, each moved by an isometry of the space
(reflections allowed), fill the second, again with pairwise disjoint interiors. They are *equicomplementable*
(`EquiComplementable`) when congruent sets of convex polytopes can be added to both, with disjoint interiors, so that
the two enlarged solids are scissors congruent.

The Dehn invariant `dehnSet P` is defined from the set `P` alone, in `ℝ ⊗[ℚ] (ℝ / ℚπ)`. At a point `x` of `P` the
directions that stay in `P` form a cone (`tcone`); the directions `v` with `v` and `-v` both in it span a space
(`linSpace`). Where that space is a line `K`, the angle at `x` is `2π · area(cone ∩ unit disc of K^⊥) / area(unit disc
of K^⊥)` (`wedgeAngle`), taken modulo rational multiples of `π`; elsewhere the class is `0` (`theta`, `edgeAngle`).
Then `dehnSet P` is the sum over the angle classes `θ` of (1-dimensional Hausdorff measure of the points with class
`θ`) ⊗ `θ`. The edges (`IsEdge`: exposed faces that are segments with two different ends), the outward unit normals of
the facets through an edge (`facetNormals`) and the interior dihedral angle (`dihedral`) are also defined from the set.

1. `hilbert_third_problem`: **Hilbert's third problem in Hilbert's words.** There are two tetrahedra `A B C D` and
   `A B C D'` on one and the same base triangle, with apexes at the same distance 1 from its plane and the same
   volume 1/6, that are neither scissors congruent nor equicomplementable.
2. `dehnSet_eq_edge_sum`: for every convex polytope with interior points, `dehnSet P` is the classical sum over the
   edges of (length) ⊗ (interior dihedral angle modulo ℚπ): Dehn's invariant in Jessen's tensor form.
3. `dehnSet_eq_of_scissorsCongruent`: **the bridge.** Scissors-congruent convex polytopes have the same `dehnSet`
   (in every 3-dimensional real inner product space).
4. `dehnSum_eq_of_scissors`: the bridge for finite unions of convex polytopes (polyhedra that need not be convex):
   the total invariant over the pieces does not depend on the dissection and is kept by scissors congruence.
5. `similarTetra_not_scissorsCongruent_similarCube`: **Dehn's theorem.** No similar copy of the regular tetrahedron
   `tetraSet` is scissors congruent to a similar copy of the cube `cubeSet 1`.

**Sources.** D. Hilbert, Mathematische Probleme, *Nachr. Ges. Wiss. Göttingen* (1900) 253–297, problem 3 (English by
M. W. Newson, *Bull. Amer. Math. Soc.* 8 (1902) 437–479); M. Dehn, Ueber den Rauminhalt, *Math. Ann.* 55 (1901)
465–478; B. Jessen, *Math. Scand.* 22 (1968) 241–256 (the tensor form). The pair of tetrahedra is that of M. Aigner and
G. M. Ziegler, *Proofs from THE BOOK*, chapter "Hilbert's third problem" (their T₁ and T₂), placed on one base.

**Scope.** Dimension 3. The pieces of a dissection are convex polytopes, finitely many, moved by isometries
(reflections included). The edge sum is for convex polytopes with interior points. Sydler's converse is not stated.

Every definition and statement below is copied, character for character, from the Lean development (studies
2026-11-19-lean-dehn-1 to -10; in this entry its namespace is `DehnCanon.Library`); the comment before each group
names its file.
-/

namespace DehnCanon

-- from DehnCanon1.lean
section
open Real TensorProduct

/-- The rational multiples of π, a ℚ-subspace of ℝ. -/
noncomputable def ratPi : Submodule ℚ ℝ := Submodule.span ℚ {π}

/-- Angles modulo rational multiples of π. -/
abbrev Angle := ℝ ⧸ ratPi

/-- Where Dehn invariants live. -/
abbrev DehnSpace := ℝ ⊗[ℚ] Angle

end

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

/-- The angle class in ℝ/ℚπ of a cone: its angle around `linSpace` when that is a line, else 0. -/
noncomputable def theta (T : Set E) : Angle :=
  if finrank ℝ (linSpace T) = 1 then Submodule.Quotient.mk (wedgeAngle T (linSpace T)) else 0

/-- The dihedral angle class of the set `P` at the point `x` (0 unless `x` is an edge point). -/
noncomputable def edgeAngle (P : Set E) (x : E) : Angle := theta (tcone P x)

/-- **The Dehn invariant of a set**, in ℝ ⊗[ℚ] (ℝ/ℚπ): Σ over angle classes θ of length{edge points with class θ} ⊗ θ. -/
noncomputable def dehnSet (P : Set E) : DehnSpace :=
  ∑ᶠ θ : Angle, (μH[1] {x | edgeAngle P x = θ}).toReal ⊗ₜ[ℚ] θ

end

-- from DehnCanon2.lean
section
open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E] [Fact (finrank ℝ E = 3)]

/-- `P` and `Q` are scissors congruent (equidecomposable) with convex pieces: `P` is cut into finitely many
convex polytopes `p k` with pairwise disjoint interiors, each piece is moved by an isometry `g k` of the
space, and the moved pieces fill `Q`, again with pairwise disjoint interiors. -/
def ScissorsCongruent (P Q : Set E) : Prop :=
  ∃ (κ : Type) (_ : Fintype κ) (p : κ → Set E) (g : κ → E ≃ᵃⁱ[ℝ] E),
    (∀ k, IsPoly (p k)) ∧ (⋃ k, p k) = P ∧
    (Pairwise fun i j => Disjoint (interior (p i)) (interior (p j))) ∧
    (⋃ k, g k '' p k) = Q ∧
    (Pairwise fun i j => Disjoint (interior (g i '' p i)) (interior (g j '' p j)))

end

-- from Dehn2R3.lean
section
open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct

/-- Coordinate 3-space. -/
abbrev R3 := EuclideanSpace ℝ (Fin 3)

instance : Fact (finrank ℝ R3 = 3) := ⟨by simp⟩

/-- Outward face normals of the regular tetrahedron with corners (−1,−1,−1), (1,1,−1), (1,−1,1), (−1,1,1). -/
def tetN : Fin 4 → R3 := ![!₂[1, 1, 1], !₂[-1, -1, 1], !₂[-1, 1, -1], !₂[1, -1, -1]]

/-- The regular tetrahedron with corners (−1,−1,−1), (1,1,−1), (1,−1,1), (−1,1,1) (edge 2√2). -/
def tetraSet : Set R3 := sol tetN (fun _ => 1)

/-- Outward face normals of a cube: ± the three coordinate directions. -/
noncomputable def cubeN : Fin 3 × Bool → R3 :=
  fun p => if p.2 then EuclideanSpace.single p.1 1 else -EuclideanSpace.single p.1 1

/-- The cube `[-s, s]³` (edge 2s). -/
def cubeSet (s : ℝ) : Set R3 := sol cubeN (fun _ => s)

end

-- from Dehn4Similar.lean
section
open scoped RealInnerProductSpace Pointwise
open Set MeasureTheory Measure Module TensorProduct

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

/-- `Q` is a similar copy of `P`: `P` scaled by a factor `a > 0` and then moved by an isometry of the space
(rotation, translation, reflection). Any size, any position. -/
def IsSimilarCopy (P Q : Set E) : Prop := ∃ a : ℝ, 0 < a ∧ ∃ g : E ≃ᵃⁱ[ℝ] E, Q = g '' (a • P)

end

-- from Dehn10Edges.lean
section
open scoped RealInnerProductSpace Real
open Set MeasureTheory Measure Module TensorProduct

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The face of `P` in the direction `n`: the points of `P` where ⟪n, ·⟫ is largest. -/
def faceIn (P : Set E) (n : E) : Set E := {x | x ∈ P ∧ ∀ y ∈ P, ⟪n, y⟫ ≤ ⟪n, x⟫}

/-- **An edge** of `P`: an exposed face of `P` that is a segment with two different ends. -/
def IsEdge (P F : Set E) : Prop := IsExposed ℝ P F ∧ ∃ u v : E, u ≠ v ∧ F = segment ℝ u v

/-- The set of the edges of `P`. -/
def edges (P : Set E) : Set (Set E) := {F | IsEdge P F}

/-- **The outward unit normals of the facets of `P` through `F`**: the unit vectors `n` whose face contains
`F` and is not contained in a line. -/
def facetNormals (P F : Set E) : Set E :=
  {n | ‖n‖ = 1 ∧ F ⊆ faceIn P n ∧ ¬ Collinear ℝ (faceIn P n)}

/-- **The interior dihedral angle of `P` at `F`**: π minus the largest angle between two outward unit normals
of facets through `F`. -/
noncomputable def dihedral (P F : Set E) : ℝ :=
  π - sSup ((fun p : E × E => InnerProductGeometry.angle p.1 p.2) ''
    (facetNormals P F ×ˢ facetNormals P F))

end

-- from Dehn10Hilbert.lean
section
open scoped RealInnerProductSpace Real Pointwise
open Set MeasureTheory Measure Module TensorProduct

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

/-- `P` and `Q` are equicomplementable: finitely many convex polytopes `c k` can be added to `P`, and
congruent copies `g k '' c k` of the same pieces to `Q` (interiors disjoint from each other and from `P`,
from `Q`), so that the two enlarged solids are scissors congruent. -/
def EquiComplementable (P Q : Set E) : Prop :=
  ∃ (κ : Type) (_ : Fintype κ) (c : κ → Set E) (g : κ → E ≃ᵃⁱ[ℝ] E),
    (∀ k, IsPoly (c k)) ∧
    (∀ k, Disjoint (interior P) (interior (c k))) ∧
    (Pairwise fun i j => Disjoint (interior (c i)) (interior (c j))) ∧
    (∀ k, Disjoint (interior Q) (interior (g k '' c k))) ∧
    (Pairwise fun i j => Disjoint (interior (g i '' c i)) (interior (g j '' c j))) ∧
    ScissorsCongruent (P ∪ ⋃ k, c k) (Q ∪ ⋃ k, g k '' c k)

end

-- from Dehn10Hilbert.lean
section
open scoped RealInnerProductSpace Real Pointwise
open Set MeasureTheory Measure Module TensorProduct

/-- **Hilbert's third problem, in Hilbert's words.** "Two tetrahedra of equal bases and equal altitudes which
can in no way be split up into congruent tetrahedra, and which cannot be combined with congruent tetrahedra to
form two polyhedra which themselves could be split up into congruent tetrahedra" (Hilbert 1900, problem 3;
English by Newson 1902). Solved by Dehn (1901).

There are two tetrahedra `A B C D` and `A B C D'` on one and the same base triangle `A B C`, with the same
altitude 1 over it (hence the same volume, 1/6), which are not scissors congruent and not equicomplementable.
Here the pieces may be any convex polytopes, and they are moved by any isometries.
The pair: `A = (0,0,0)`, `B = (1,0,0)`, `C = (0,1,0)`, `D = (0,0,1)`, `D' = (0,1,1)` (Aigner–Ziegler,
Proofs from THE BOOK, the tetrahedra T₁ and T₂ of the chapter on Hilbert's third problem). -/
theorem hilbert_third_problem :
    ∃ A B C D D' : R3,
      Metric.infDist D (affineSpan ℝ ({A, B, C} : Set R3) : Set R3) = 1 ∧
      Metric.infDist D' (affineSpan ℝ ({A, B, C} : Set R3) : Set R3) = 1 ∧
      volume (convexHull ℝ ({A, B, C, D} : Set R3)) = ENNReal.ofReal (1 / 6) ∧
      volume (convexHull ℝ ({A, B, C, D'} : Set R3)) = ENNReal.ofReal (1 / 6) ∧
      ¬ ScissorsCongruent (convexHull ℝ ({A, B, C, D} : Set R3)) (convexHull ℝ ({A, B, C, D'} : Set R3)) ∧
      ¬ EquiComplementable (convexHull ℝ ({A, B, C, D} : Set R3))
        (convexHull ℝ ({A, B, C, D'} : Set R3)) := by
  sorry

end

-- from Dehn10Edges.lean
section
open scoped RealInnerProductSpace Real
open Set MeasureTheory Measure Module TensorProduct

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
variable {ι : Type} {a : ι → E} {b : ι → ℝ}
variable [FiniteDimensional ℝ E] [Fact (finrank ℝ E = 3)]
variable [MeasurableSpace E] [BorelSpace E]

/-- **The set-defined Dehn invariant is the classical edge sum** (Dehn 1901, in Jessen's tensor form). For
every convex polytope `P` in 3-space (a bounded intersection of finitely many closed half-spaces) with
interior points, the Dehn invariant `dehnSet P`, defined from the set `P` by cones of directions and
sector areas, is the sum over the edges `F` of `P` of

  (length of `F`) ⊗ (interior dihedral angle of `P` at `F`, modulo rational multiples of π).

The edges (`edges`, `IsEdge`: the exposed faces that are segments) and the dihedral angle (`dihedral`: π minus
the angle between the outward unit normals of the two facets through the edge,
`IsEdge.facetNormals_eq_pair`) are defined from `P` alone. The sum is finite (`edges_finite`). -/
theorem dehnSet_eq_edge_sum {P : Set E} (hP : IsPoly P) (hint : (interior P).Nonempty) :
    dehnSet P = ∑ᶠ F ∈ edges P,
      (μH[1] F).toReal ⊗ₜ[ℚ] (Submodule.Quotient.mk (dihedral P F) : Angle) := by
  sorry

end

-- from DehnCanon2.lean
section
open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E] [Fact (finrank ℝ E = 3)]

/-- **Dehn's theorem, the bridge.** Scissors-congruent convex polytopes in 3-space have the same Dehn
invariant. -/
theorem dehnSet_eq_of_scissorsCongruent {P Q : Set E} (hP : IsPoly P) (hQ : IsPoly Q)
    (h : ScissorsCongruent P Q) : dehnSet P = dehnSet Q := by
  sorry

/-- **Dehn's theorem for polyhedra that need not be convex.** Let the polyhedron `⋃ k, p k` be cut into the
convex pieces `p k`, and let the moved pieces `g k '' p k` fill a second polyhedron. Then every dissection
`p₁` of the first polyhedron into convex polytopes and every dissection `p₂` of the second have the same
total Dehn invariant. -/
theorem dehnSum_eq_of_scissors {κ κ₁ κ₂ : Type} [Fintype κ] [Fintype κ₁] [Fintype κ₂]
    {p : κ → Set E} {g : κ → E ≃ᵃⁱ[ℝ] E} {p₁ : κ₁ → Set E} {p₂ : κ₂ → Set E}
    (hp : ∀ k, IsPoly (p k))
    (hdp : Pairwise fun i j => Disjoint (interior (p i)) (interior (p j)))
    (hdg : Pairwise fun i j => Disjoint (interior (g i '' p i)) (interior (g j '' p j)))
    (hp₁ : ∀ k, IsPoly (p₁ k))
    (hd₁ : Pairwise fun i j => Disjoint (interior (p₁ i)) (interior (p₁ j)))
    (hU₁ : (⋃ k, p₁ k) = ⋃ k, p k)
    (hp₂ : ∀ k, IsPoly (p₂ k))
    (hd₂ : Pairwise fun i j => Disjoint (interior (p₂ i)) (interior (p₂ j)))
    (hU₂ : (⋃ k, p₂ k) = ⋃ k, g k '' p k) :
    ∑ k, dehnSet (p₁ k) = ∑ k, dehnSet (p₂ k) := by
  sorry

end

-- from Dehn4Similar.lean
section
open scoped RealInnerProductSpace Pointwise
open Set MeasureTheory Measure Module TensorProduct

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

/-- **Dehn's theorem, any size and any position.** No similar copy of the regular tetrahedron `tetraSet`
(corners (−1,−1,−1), (1,1,−1), (1,−1,1), (−1,1,1)) is scissors congruent to a similar copy of the cube
`[-1, 1]³`. Here "a regular tetrahedron" and "a cube" mean: a similar copy of these two models. -/
theorem similarTetra_not_scissorsCongruent_similarCube {T Q : Set R3}
    (hT : IsSimilarCopy tetraSet T) (hQ : IsSimilarCopy (cubeSet 1) Q) : ¬ ScissorsCongruent T Q := by
  sorry

end

end DehnCanon
