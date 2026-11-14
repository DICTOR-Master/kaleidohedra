module

public import Mathlib

@[expose] public section

/-!
# The octahedral constant 3 (DICTO, paper #43 "Kyushindo Cores", Theorem 4)

Statement surface only (every proof is `sorry`); candidate Challenge for a
Palomar entry.

A convex polytope `S` containing the origin `O` is written as the intersection
of finitely many half-spaces `⟪n i, x⟫ ≤ h i` with unit normals `n i` and
positive distances `h i`. The *foot point* of the face plane `i` is `h i • n i`,
the point of the plane nearest to `O`, and `P(S)` is the convex hull of the
foot points. Theorem 4 of #43 says: if `S` has octahedral rotational symmetry
about `O`, then `S ⊆ 3 • P(S)`, and 3 is sharp (cube, octahedron).

The octahedral rotation group is written in the standard frame as the 24
signed permutation matrices of determinant 1: `x ↦ (s i * x (σ i))ᵢ` with
`sign σ * ∏ s i = 1`.
-/

namespace DictoKyushindo

open scoped RealInnerProductSpace Pointwise

/-- Euclidean 3-space. -/
abbrev E3 := EuclideanSpace ℝ (Fin 3)

/-- The signed permutation `x ↦ (s i * x (σ i))ᵢ` of the coordinates of `x`. -/
noncomputable def signedPerm (σ : Equiv.Perm (Fin 3)) (s : Fin 3 → ℤˣ) (x : E3) : E3 :=
  WithLp.toLp 2 (fun i => ((s i : ℤ) : ℝ) * x (σ i))

/-- `(σ, s)` is one of the 24 rotations of the octahedral group: its signed
permutation matrix has determinant `sign σ * ∏ s i = 1`. -/
def IsOctahedralRotation (σ : Equiv.Perm (Fin 3)) (s : Fin 3 → ℤˣ) : Prop :=
  ((Equiv.Perm.sign σ : ℤˣ) : ℤ) * ∏ i, ((s i : ℤˣ) : ℤ) = 1

/-- The polytope cut out by the half-spaces `⟪n i, x⟫ ≤ h i`. -/
def halfspaceBody {ι : Type*} (n : ι → E3) (h : ι → ℝ) : Set E3 :=
  {x | ∀ i, ⟪n i, x⟫ ≤ h i}

/-- `P(S)`: the convex hull of the foot points `h i • n i` of the face planes. -/
noncomputable def footHull {ι : Type*} (n : ι → E3) (h : ι → ℝ) : Set E3 :=
  convexHull ℝ (Set.range fun i => h i • n i)

/-- The family of face planes is carried to itself by every octahedral rotation. -/
def OctahedrallySymmetric {ι : Type*} (n : ι → E3) (h : ι → ℝ) : Prop :=
  ∀ σ s, IsOctahedralRotation σ s → ∀ i, ∃ j, n j = signedPerm σ s (n i) ∧ h j = h i

/-- The covering lemma behind Theorem 4: every orbit of the octahedral rotation
group on the unit sphere comes within angle `arccos (1/√3)` of every direction. -/
theorem covering (u w : E3) (hu : ‖u‖ = 1) (hw : ‖w‖ = 1) :
    ∃ σ s, IsOctahedralRotation σ s ∧ 1 / Real.sqrt 3 ≤ ⟪signedPerm σ s u, w⟫ := by
  sorry

/-- **Theorem 4 of #43 (the octahedral constant 3).** A polytope given by a
nonempty finite octahedrally symmetric family of half-spaces with positive
distances lies inside 3 times the hull of its foot points. -/
theorem octahedral_nesting {ι : Type*} [Fintype ι] [Nonempty ι]
    (n : ι → E3) (h : ι → ℝ) (hn : ∀ i, ‖n i‖ = 1) (hh : ∀ i, 0 < h i)
    (hsym : OctahedrallySymmetric n h) :
    halfspaceBody n h ⊆ (3 : ℝ) • footHull n h := by
  sorry

/-- The six face normals `±eᵢ` of the cube `[-1, 1]³`. -/
noncomputable def cubeNormal : Fin 3 × Bool → E3 :=
  fun k => (if k.2 then (1 : ℝ) else -1) • EuclideanSpace.single k.1 1

/-- The cube is an admissible input: unit normals, distance 1, octahedral symmetry. -/
theorem cube_admissible :
    (∀ k, ‖cubeNormal k‖ = 1) ∧ OctahedrallySymmetric cubeNormal (fun _ => 1) := by
  sorry

/-- **Sharpness.** For the cube no constant below 3 works. -/
theorem octahedral_nesting_sharp (c : ℝ) (hc : c < 3) :
    ¬ halfspaceBody cubeNormal (fun _ => 1) ⊆ c • footHull cubeNormal (fun _ => 1) := by
  sorry

end DictoKyushindo
