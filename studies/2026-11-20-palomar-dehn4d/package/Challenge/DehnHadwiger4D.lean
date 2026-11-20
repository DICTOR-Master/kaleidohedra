module

public import Mathlib

@[expose] public section

/-!
# The Dehn–Hadwiger invariant in four dimensions

**Informal statement.** Convex polytopes (`IsPoly`) are bounded intersections of finitely many closed half-spaces;
`ScissorsCongruent P Q`: `P` is cut into finitely many convex polytopes with disjoint interiors which, each moved by
an isometry (reflections allowed), fill `Q` with disjoint interiors.

The Dehn–Hadwiger invariant `dehnHadwiger P ∈ ℝ ⊗[ℚ] (ℝ / ℚπ)` is read from the set `P` alone, in any finite
dimension `n`. At a point `x` the directions that stay in `P` form a cone (`tcone`) with lineality space `linSpace`.
Where that space has codimension 2 (a ridge point), the class at `x` is the angle of the cone in the orthogonal plane
(`wedgeAngle`) modulo ℚπ (`thetaH`, `ridgeAngle`); elsewhere it is 0. `dehnHadwiger P` is the sum over classes `θ` of
((n − 2)-dimensional Hausdorff measure of the ridge points of class `θ`) ⊗ `θ`: in ℝ⁴, Hadwiger's sum of
area ⊗ dihedral angle over the 2-faces. Polytopes are cut out by facet normals `n` as `⟪n, x⟫ ≤ 1` (`sol`).

1. **The bridge**: scissors-congruent convex polytopes have the same invariant, in every finite dimension; the same
   for finite unions of convex polytopes (`dehnHadwigerSum_eq_of_scissors`).
2. The tesseract, the 16-cell, the 24-cell and the 120-cell have invariant 0; arccos(1/4) ∉ ℚπ.
3. The 5-cell's invariant is A₅ ⊗ arccos(1/4), the 600-cell's A₆₀₀ ⊗ (4π/3 − arccos(1/4)) (A: area of the ridge
   points; the 600-cell's dihedral angle is 4π/3 minus the 5-cell's); both are non-zero.
4. No similar copy (`IsSimilarCopy`) of the 5-cell or the 600-cell is scissors congruent to a similar copy of the
   tesseract, the 16-cell, the 24-cell or the 120-cell, nor a similar copy of the 5-cell to one of the 600-cell.

**Sources.** H. Hadwiger, *Math. Ann.* 127 (1954) 170–174, and *Vorlesungen über Inhalt, Oberfläche und
Isoperimetrie* (1957); M. Dehn, *Math. Ann.* 55 (1901) 465–478; B. Jessen, *Math. Scand.* 22 (1968) 241–256 and
*Nachr. Akad. Wiss. Göttingen* (1972) (the converse in ℝ⁴, not stated here).
Definitions and statements are copied character for character from the Lean development (comments name the files).
-/

namespace DehnHadwiger4D

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

section
open scoped RealInnerProductSpace Pointwise
open Set MeasureTheory Measure Module TensorProduct

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

-- from Dehn2Poly.lean
/-- The solution set of a system of linear inequalities `⟪a i, x⟫ ≤ b i`. -/
def sol {ι : Type} (a : ι → E) (b : ι → ℝ) : Set E := {x | ∀ i, ⟪a i, x⟫ ≤ b i}

/-- A convex polytope: a bounded intersection of finitely many closed half-spaces. -/
def IsPoly (P : Set E) : Prop :=
  Bornology.IsBounded P ∧ ∃ (ι : Type) (_ : Fintype ι) (a : ι → E) (b : ι → ℝ), P = sol a b

-- from Dehn2Local.lean
/-- The cone of directions that stay in `P` near the point `x` of `P` (empty when `x ∉ P`). -/
def tcone (P : Set E) (x : E) : Set E := {v | x ∈ P ∧ ∃ t : ℝ, 0 < t ∧ x + t • v ∈ P}

/-- The span of the directions `v` of a cone for which `-v` is in the cone too. -/
def linSpace (T : Set E) : Submodule ℝ E := Submodule.span ℝ {v | v ∈ T ∧ -v ∈ T}

/-- The part of the cone `T` inside the open unit disc of the space perpendicular to `K`. -/
def wedgeSet (T : Set E) (K : Submodule ℝ E) : Set Kᗮ := {w | (w : E) ∈ T ∧ ‖w‖ < 1}

/-- The angle of the cone `T` around `K` (`Kᗮ` a plane): 2π × area(T ∩ unit disc of Kᗮ) / area(unit disc of Kᗮ). -/
noncomputable def wedgeAngle (T : Set E) (K : Submodule ℝ E) : ℝ :=
  2 * Real.pi * ((volume (wedgeSet T K)).toReal / (volume (Metric.ball (0 : Kᗮ) 1)).toReal)

-- from DehnCanon2.lean
/-- `P` and `Q` are scissors congruent (equidecomposable) with convex pieces: `P` is cut into finitely many
convex polytopes `p k` with pairwise disjoint interiors, each piece is moved by an isometry `g k` of the
space, and the moved pieces fill `Q`, again with pairwise disjoint interiors. -/
def ScissorsCongruent (P Q : Set E) : Prop :=
  ∃ (κ : Type) (_ : Fintype κ) (p : κ → Set E) (g : κ → E ≃ᵃⁱ[ℝ] E),
    (∀ k, IsPoly (p k)) ∧ (⋃ k, p k) = P ∧
    (Pairwise fun i j => Disjoint (interior (p i)) (interior (p j))) ∧
    (⋃ k, g k '' p k) = Q ∧
    (Pairwise fun i j => Disjoint (interior (g i '' p i)) (interior (g j '' p j)))

-- from Dehn4Similar.lean
/-- `Q` is a similar copy of `P`: `P` scaled by a factor `a > 0` and then moved by an isometry of the space
(rotation, translation, reflection). Any size, any position. -/
def IsSimilarCopy (P Q : Set E) : Prop := ∃ a : ℝ, 0 < a ∧ ∃ g : E ≃ᵃⁱ[ℝ] E, Q = g '' (a • P)

-- from DH1Def.lean
/-- The angle class in ℝ/ℚπ of a cone: its wedge angle around `linSpace` when that space has codimension 2,
else 0. -/
noncomputable def thetaH (T : Set E) : Angle :=
  if finrank ℝ (linSpace T) + 2 = finrank ℝ E then Submodule.Quotient.mk (wedgeAngle T (linSpace T)) else 0

/-- The dihedral angle class of the set `P` at the point `x` (0 unless `x` is a ridge point). -/
noncomputable def ridgeAngle (P : Set E) (x : E) : Angle := thetaH (tcone P x)

/-- **The Dehn–Hadwiger invariant of a set**, in ℝ ⊗[ℚ] (ℝ/ℚπ): Σ over angle classes θ of
((n−2)-dimensional measure of the ridge points with class θ) ⊗ θ, `n` the dimension of the space. -/
noncomputable def dehnHadwiger (P : Set E) : DehnSpace :=
  ∑ᶠ θ : Angle, (μH[(finrank ℝ E - 2 : ℕ)] {x | ridgeAngle P x = θ}).toReal ⊗ₜ[ℚ] θ

-- from DH6Cells.lean
/-- Coordinate 4-space. -/
abbrev R4 := EuclideanSpace ℝ (Fin 4)

/-- The vector of `R4` with whole-number coordinates `z`. -/
noncomputable def zvec (z : Fin 4 → ℤ) : R4 := !₂[(z 0 : ℝ), (z 1 : ℝ), (z 2 : ℝ), (z 3 : ℝ)]

/-- Facet normals of the tesseract [-1, 1]⁴: ±eᵢ. -/
def tessZ : Fin 8 → Fin 4 → ℤ :=
  ![![1, 0, 0, 0], ![-1, 0, 0, 0], ![0, 1, 0, 0], ![0, -1, 0, 0], ![0, 0, 1, 0], ![0, 0, -1, 0], ![0, 0, 0, 1], ![0, 0, 0, -1]]

/-- Facet normals of the regular 16-cell: the sixteen vectors (±1, ±1, ±1, ±1). -/
def cell16Z : Fin 16 → Fin 4 → ℤ :=
  ![![1, 1, 1, 1], ![1, 1, 1, -1], ![1, 1, -1, 1], ![1, 1, -1, -1], ![1, -1, 1, 1], ![1, -1, 1, -1], ![1, -1, -1, 1], ![1, -1, -1, -1],
    ![-1, 1, 1, 1], ![-1, 1, 1, -1], ![-1, 1, -1, 1], ![-1, 1, -1, -1], ![-1, -1, 1, 1], ![-1, -1, 1, -1], ![-1, -1, -1, 1], ![-1, -1, -1, -1]]

/-- Facet normals of a regular 24-cell: the twenty-four vectors ±eᵢ ± eⱼ (i < j). -/
def cell24Z : Fin 24 → Fin 4 → ℤ :=
  ![![1, 1, 0, 0], ![1, -1, 0, 0], ![-1, 1, 0, 0], ![-1, -1, 0, 0], ![1, 0, 1, 0], ![1, 0, -1, 0], ![-1, 0, 1, 0], ![-1, 0, -1, 0],
    ![1, 0, 0, 1], ![1, 0, 0, -1], ![-1, 0, 0, 1], ![-1, 0, 0, -1], ![0, 1, 1, 0], ![0, 1, -1, 0], ![0, -1, 1, 0], ![0, -1, -1, 0],
    ![0, 1, 0, 1], ![0, 1, 0, -1], ![0, -1, 0, 1], ![0, -1, 0, -1], ![0, 0, 1, 1], ![0, 0, 1, -1], ![0, 0, -1, 1], ![0, 0, -1, -1]]

/-- The tesseract (4-cube) [-1, 1]⁴. -/
def tesseract : Set R4 := sol (fun i => zvec (tessZ i)) (fun _ => 1)

/-- The regular 16-cell |x₀| + |x₁| + |x₂| + |x₃| ≤ 1. -/
def cell16 : Set R4 := sol (fun i => zvec (cell16Z i)) (fun _ => 1)

/-- A regular 24-cell: |xᵢ| + |xⱼ| ≤ 1 for all i < j. -/
def cell24 : Set R4 := sol (fun i => zvec (cell24Z i)) (fun _ => 1)

-- from DH7Cell5.lean
/-- The five facet normals of the regular 5-cell. -/
noncomputable def fiveN : Fin 5 → R4 :=
  ![!₂[√5, √5, √5, 1], !₂[√5, -√5, -√5, 1], !₂[-√5, √5, -√5, 1], !₂[-√5, -√5, √5, 1], !₂[0, 0, 0, -4]]

/-- The regular 5-cell: the points with `⟪fiveN i, x⟫ ≤ 1` for the five facet normals. -/
def cell5 : Set R4 := sol fiveN (fun _ => 1)

-- from DH8Cell120.lean
/-- The real number `a + b φ` coded by `(a, b)`. -/
noncomputable def gval (c : ℤ × ℤ) : ℝ := c.1 + c.2 * Real.goldenRatio

/-- The vector of `R4` with coordinates in ℤ[φ]. -/
noncomputable def gvec (z : Fin 4 → ℤ × ℤ) : R4 := !₂[gval (z 0), gval (z 1), gval (z 2), gval (z 3)]

/-- Facet normals of the regular 120-cell: the 120 vertices of the 600-cell, doubled, in ℤ[φ]. -/
def cell120Z : Fin 120 → Fin 4 → ℤ × ℤ :=
  ![![(2, 0), (0, 0), (0, 0), (0, 0)], ![(-2, 0), (0, 0), (0, 0), (0, 0)], ![(0, 0), (2, 0), (0, 0), (0, 0)], ![(0, 0), (-2, 0), (0, 0), (0, 0)], ![(0, 0), (0, 0), (2, 0), (0, 0)],
    ![(0, 0), (0, 0), (-2, 0), (0, 0)], ![(0, 0), (0, 0), (0, 0), (2, 0)], ![(0, 0), (0, 0), (0, 0), (-2, 0)], ![(1, 0), (1, 0), (1, 0), (1, 0)], ![(1, 0), (1, 0), (1, 0), (-1, 0)],
    ![(1, 0), (1, 0), (-1, 0), (1, 0)], ![(1, 0), (1, 0), (-1, 0), (-1, 0)], ![(1, 0), (-1, 0), (1, 0), (1, 0)], ![(1, 0), (-1, 0), (1, 0), (-1, 0)], ![(1, 0), (-1, 0), (-1, 0), (1, 0)],
    ![(1, 0), (-1, 0), (-1, 0), (-1, 0)], ![(-1, 0), (1, 0), (1, 0), (1, 0)], ![(-1, 0), (1, 0), (1, 0), (-1, 0)], ![(-1, 0), (1, 0), (-1, 0), (1, 0)], ![(-1, 0), (1, 0), (-1, 0), (-1, 0)],
    ![(-1, 0), (-1, 0), (1, 0), (1, 0)], ![(-1, 0), (-1, 0), (1, 0), (-1, 0)], ![(-1, 0), (-1, 0), (-1, 0), (1, 0)], ![(-1, 0), (-1, 0), (-1, 0), (-1, 0)], ![(0, 1), (1, 0), (-1, 1), (0, 0)],
    ![(0, 1), (1, 0), (1, -1), (0, 0)], ![(0, 1), (-1, 0), (-1, 1), (0, 0)], ![(0, 1), (-1, 0), (1, -1), (0, 0)], ![(0, -1), (1, 0), (-1, 1), (0, 0)], ![(0, -1), (1, 0), (1, -1), (0, 0)],
    ![(0, -1), (-1, 0), (-1, 1), (0, 0)], ![(0, -1), (-1, 0), (1, -1), (0, 0)], ![(0, 1), (-1, 1), (0, 0), (1, 0)], ![(0, 1), (-1, 1), (0, 0), (-1, 0)], ![(0, 1), (1, -1), (0, 0), (1, 0)],
    ![(0, 1), (1, -1), (0, 0), (-1, 0)], ![(0, -1), (-1, 1), (0, 0), (1, 0)], ![(0, -1), (-1, 1), (0, 0), (-1, 0)], ![(0, -1), (1, -1), (0, 0), (1, 0)], ![(0, -1), (1, -1), (0, 0), (-1, 0)],
    ![(0, 1), (0, 0), (1, 0), (-1, 1)], ![(0, 1), (0, 0), (1, 0), (1, -1)], ![(0, 1), (0, 0), (-1, 0), (-1, 1)], ![(0, 1), (0, 0), (-1, 0), (1, -1)], ![(0, -1), (0, 0), (1, 0), (-1, 1)],
    ![(0, -1), (0, 0), (1, 0), (1, -1)], ![(0, -1), (0, 0), (-1, 0), (-1, 1)], ![(0, -1), (0, 0), (-1, 0), (1, -1)], ![(1, 0), (0, 1), (0, 0), (-1, 1)], ![(1, 0), (0, 1), (0, 0), (1, -1)],
    ![(1, 0), (0, -1), (0, 0), (-1, 1)], ![(1, 0), (0, -1), (0, 0), (1, -1)], ![(-1, 0), (0, 1), (0, 0), (-1, 1)], ![(-1, 0), (0, 1), (0, 0), (1, -1)], ![(-1, 0), (0, -1), (0, 0), (-1, 1)],
    ![(-1, 0), (0, -1), (0, 0), (1, -1)], ![(1, 0), (-1, 1), (0, 1), (0, 0)], ![(1, 0), (-1, 1), (0, -1), (0, 0)], ![(1, 0), (1, -1), (0, 1), (0, 0)], ![(1, 0), (1, -1), (0, -1), (0, 0)],
    ![(-1, 0), (-1, 1), (0, 1), (0, 0)], ![(-1, 0), (-1, 1), (0, -1), (0, 0)], ![(-1, 0), (1, -1), (0, 1), (0, 0)], ![(-1, 0), (1, -1), (0, -1), (0, 0)], ![(1, 0), (0, 0), (-1, 1), (0, 1)],
    ![(1, 0), (0, 0), (-1, 1), (0, -1)], ![(1, 0), (0, 0), (1, -1), (0, 1)], ![(1, 0), (0, 0), (1, -1), (0, -1)], ![(-1, 0), (0, 0), (-1, 1), (0, 1)], ![(-1, 0), (0, 0), (-1, 1), (0, -1)],
    ![(-1, 0), (0, 0), (1, -1), (0, 1)], ![(-1, 0), (0, 0), (1, -1), (0, -1)], ![(-1, 1), (0, 1), (1, 0), (0, 0)], ![(-1, 1), (0, 1), (-1, 0), (0, 0)], ![(-1, 1), (0, -1), (1, 0), (0, 0)],
    ![(-1, 1), (0, -1), (-1, 0), (0, 0)], ![(1, -1), (0, 1), (1, 0), (0, 0)], ![(1, -1), (0, 1), (-1, 0), (0, 0)], ![(1, -1), (0, -1), (1, 0), (0, 0)], ![(1, -1), (0, -1), (-1, 0), (0, 0)],
    ![(-1, 1), (1, 0), (0, 0), (0, 1)], ![(-1, 1), (1, 0), (0, 0), (0, -1)], ![(-1, 1), (-1, 0), (0, 0), (0, 1)], ![(-1, 1), (-1, 0), (0, 0), (0, -1)], ![(1, -1), (1, 0), (0, 0), (0, 1)],
    ![(1, -1), (1, 0), (0, 0), (0, -1)], ![(1, -1), (-1, 0), (0, 0), (0, 1)], ![(1, -1), (-1, 0), (0, 0), (0, -1)], ![(-1, 1), (0, 0), (0, 1), (1, 0)], ![(-1, 1), (0, 0), (0, 1), (-1, 0)],
    ![(-1, 1), (0, 0), (0, -1), (1, 0)], ![(-1, 1), (0, 0), (0, -1), (-1, 0)], ![(1, -1), (0, 0), (0, 1), (1, 0)], ![(1, -1), (0, 0), (0, 1), (-1, 0)], ![(1, -1), (0, 0), (0, -1), (1, 0)],
    ![(1, -1), (0, 0), (0, -1), (-1, 0)], ![(0, 0), (0, 1), (-1, 1), (1, 0)], ![(0, 0), (0, 1), (-1, 1), (-1, 0)], ![(0, 0), (0, 1), (1, -1), (1, 0)], ![(0, 0), (0, 1), (1, -1), (-1, 0)],
    ![(0, 0), (0, -1), (-1, 1), (1, 0)], ![(0, 0), (0, -1), (-1, 1), (-1, 0)], ![(0, 0), (0, -1), (1, -1), (1, 0)], ![(0, 0), (0, -1), (1, -1), (-1, 0)], ![(0, 0), (1, 0), (0, 1), (-1, 1)],
    ![(0, 0), (1, 0), (0, 1), (1, -1)], ![(0, 0), (1, 0), (0, -1), (-1, 1)], ![(0, 0), (1, 0), (0, -1), (1, -1)], ![(0, 0), (-1, 0), (0, 1), (-1, 1)], ![(0, 0), (-1, 0), (0, 1), (1, -1)],
    ![(0, 0), (-1, 0), (0, -1), (-1, 1)], ![(0, 0), (-1, 0), (0, -1), (1, -1)], ![(0, 0), (-1, 1), (1, 0), (0, 1)], ![(0, 0), (-1, 1), (1, 0), (0, -1)], ![(0, 0), (-1, 1), (-1, 0), (0, 1)],
    ![(0, 0), (-1, 1), (-1, 0), (0, -1)], ![(0, 0), (1, -1), (1, 0), (0, 1)], ![(0, 0), (1, -1), (1, 0), (0, -1)], ![(0, 0), (1, -1), (-1, 0), (0, 1)], ![(0, 0), (1, -1), (-1, 0), (0, -1)]]

/-- The regular 120-cell: `⟪n, x⟫ ≤ 1` for its 120 facet normals `n`. -/
def cell120 : Set R4 := sol (fun i => gvec (cell120Z i)) (fun _ => 1)

-- from DH11Cell600Defs.lean
/-- The 24 orderings of four coordinates (coordinate `i` of the new vector is coordinate `σ i` of the old one);
the first 12 are the even ones. -/
def orders : List (Fin 4 → Fin 4) :=
  [![0, 1, 2, 3], ![0, 2, 3, 1], ![0, 3, 1, 2], ![1, 0, 3, 2], ![1, 2, 0, 3], ![1, 3, 2, 0], ![2, 0, 1, 3],
    ![2, 1, 3, 0], ![2, 3, 0, 1], ![3, 0, 2, 1], ![3, 1, 0, 2], ![3, 2, 1, 0], ![0, 1, 3, 2], ![0, 2, 1, 3],
    ![0, 3, 2, 1], ![1, 0, 2, 3], ![1, 2, 3, 0], ![1, 3, 0, 2], ![2, 0, 3, 1], ![2, 1, 0, 3], ![2, 3, 1, 0],
    ![3, 0, 1, 2], ![3, 1, 2, 0], ![3, 2, 0, 1]]

/-- All 16 sign changes of all orderings of `z` (`n = 24`), or of its even orderings only (`n = 12`). -/
def orbit (n : ℕ) (z : Fin 4 → ℤ × ℤ) : List (Fin 4 → ℤ × ℤ) :=
  (orders.take n).flatMap fun σ => (List.range 16).map fun s i => if s.testBit i then -z (σ i) else z (σ i)

/-- The 600 vertices of the regular 120-cell of radius √8 (the standard coordinates), as pairs
`(a, b) = a + b φ` (`gval`): all sign changes of all orderings of (0, 0, 2, 2), (1, 1, 1, √5), (φ⁻², φ, φ, φ) and
(φ⁻¹, φ⁻¹, φ⁻¹, φ²), and of the even orderings of (0, φ⁻², 1, φ²), (0, φ⁻¹, φ, √5) and (φ⁻¹, 1, φ, 2)
(√5 = 2φ − 1, φ⁻¹ = φ − 1, φ⁻² = 2 − φ, φ² = φ + 1). The list repeats some vectors. -/
def cell600Z : List (Fin 4 → ℤ × ℤ) :=
  orbit 24 ![(0, 0), (0, 0), (2, 0), (2, 0)] ++ orbit 24 ![(1, 0), (1, 0), (1, 0), (-1, 2)] ++
    orbit 24 ![(2, -1), (0, 1), (0, 1), (0, 1)] ++ orbit 24 ![(-1, 1), (-1, 1), (-1, 1), (1, 1)] ++
    orbit 12 ![(0, 0), (2, -1), (1, 0), (1, 1)] ++ orbit 12 ![(0, 0), (-1, 1), (0, 1), (-1, 2)] ++
    orbit 12 ![(-1, 1), (1, 0), (0, 1), (2, 0)]

/-- The regular 600-cell: `⟪n, x⟫ ≤ 1` for the 600 vertices `n` of the 120-cell (the 600-cell is its polar). -/
def cell600 : Set R4 := sol (fun z : {z // z ∈ cell600Z} => gvec z.1) (fun _ => 1)

-- from DH3Bridge.lean
/-- **The bridge.** Scissors-congruent convex polytopes have the same Dehn–Hadwiger invariant. -/
theorem dehnHadwiger_eq_of_scissorsCongruent {P Q : Set E} (hP : IsPoly P) (hQ : IsPoly Q)
    (h : ScissorsCongruent P Q) : dehnHadwiger P = dehnHadwiger Q := by
  sorry

/-- **The bridge for finite unions of convex polytopes.** Let the set `⋃ k, p k` be cut into the convex pieces
`p k`, and let the moved pieces `g k '' p k` fill a second set. Then every dissection `p₁` of the first set
into convex polytopes and every dissection `p₂` of the second have the same total invariant. -/
theorem dehnHadwigerSum_eq_of_scissors {κ κ₁ κ₂ : Type} [Fintype κ] [Fintype κ₁] [Fintype κ₂]
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
    ∑ k, dehnHadwiger (p₁ k) = ∑ k, dehnHadwiger (p₂ k) := by
  sorry

-- from DH6Cells.lean
theorem dehnHadwiger_tesseract : dehnHadwiger tesseract = 0 := by
  sorry

theorem dehnHadwiger_cell16 : dehnHadwiger cell16 = 0 := by
  sorry

theorem dehnHadwiger_cell24 : dehnHadwiger cell24 = 0 := by
  sorry

-- from DH7Cell5.lean
/-- **arccos(1/4) is not a rational multiple of π** (Niven's theorem). -/
theorem arccos_quarter_not_ratPi : Real.arccos (1 / 4) ∉ ratPi := by
  sorry

/-- **The invariant of the 5-cell**: (area of its ridge points) ⊗ arccos(1/4). -/
theorem dehnHadwiger_cell5_eq : dehnHadwiger cell5 =
    (μH[(finrank ℝ R4 - 2 : ℕ)] {x | ridgeAngle cell5 x = Submodule.Quotient.mk (Real.arccos (1 / 4))}).toReal
      ⊗ₜ[ℚ] (Submodule.Quotient.mk (Real.arccos (1 / 4)) : Angle) := by
  sorry

/-- **The regular 5-cell has non-zero Dehn–Hadwiger invariant.** -/
theorem dehnHadwiger_cell5_ne_zero : dehnHadwiger cell5 ≠ 0 := by
  sorry

-- from DH8Cell120.lean
theorem dehnHadwiger_cell120 : dehnHadwiger cell120 = 0 := by
  sorry

-- from DH13Cell600.lean
/-- **The invariant of the regular 600-cell**: (area of its ridge points) ⊗ (4π/3 − arccos(1/4)). -/
theorem dehnHadwiger_cell600_eq : dehnHadwiger cell600 =
    (μH[(finrank ℝ R4 - 2 : ℕ)]
      {x | ridgeAngle cell600 x = Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4))}).toReal
      ⊗ₜ[ℚ] (Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4)) : Angle) := by
  sorry

-- from DH14Cell600Area.lean
/-- **The regular 600-cell has non-zero Dehn–Hadwiger invariant.** -/
theorem dehnHadwiger_cell600_ne_zero : dehnHadwiger cell600 ≠ 0 := by
  sorry

-- from DH9Results.lean
/-- **The 5-cell against the four regular 4-polytopes with invariant zero**, any size and any position. -/
theorem similarCell5_not_scissorsCongruent {T Q : Set R4} (hT : IsSimilarCopy cell5 T)
    (hQ : IsSimilarCopy tesseract Q ∨ IsSimilarCopy cell16 Q ∨ IsSimilarCopy cell24 Q ∨
      IsSimilarCopy cell120 Q) : ¬ ScissorsCongruent T Q := by
  sorry

-- from DH15Results600.lean
/-- **The 600-cell against the four regular 4-polytopes with invariant zero**, any size and any position. -/
theorem similarCell600_not_scissorsCongruent {T Q : Set R4} (hT : IsSimilarCopy cell600 T)
    (hQ : IsSimilarCopy tesseract Q ∨ IsSimilarCopy cell16 Q ∨ IsSimilarCopy cell24 Q ∨
      IsSimilarCopy cell120 Q) : ¬ ScissorsCongruent T Q := by
  sorry

/-- **The 5-cell against the 600-cell.** No similar copy of the regular 5-cell is scissors congruent to a similar
copy of the regular 600-cell. -/
theorem similarCell5_not_scissorsCongruent_similarCell600 {T Q : Set R4} (hT : IsSimilarCopy cell5 T)
    (hQ : IsSimilarCopy cell600 Q) : ¬ ScissorsCongruent T Q := by
  sorry

end

end DehnHadwiger4D
