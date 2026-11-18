/-
Lean study 2 of the shape-language canon (DICTO, 19 Nov 2026): WHAT REMAINS. Every `sorry` of the study is in
this file and nowhere else.

The bridge itself (files Dehn2Poly, Dehn2Local, Dehn2Sum, Dehn2Cut, Dehn2Motion, DehnCanon2, Dehn2Edges,
Dehn2R3) has no `sorry`. What is not yet proved is the EVALUATION of the set invariant `dehnSet` on concrete
solids: that the angle measured by area is the usual dihedral angle (gap 1), and the edge data of the cube
and of the regular tetrahedron (gaps 2, 3). The last theorem here is proved, but from gaps 2 and 3.
-/
import DehnCanon.Dehn2R3

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct

namespace DehnCanon

/-- GAP 1 (angle evaluation). Two half-spaces with outward normals `a₁`, `a₂` (not parallel) meet in a wedge
whose angle, as measured by `wedgeAngle` (area of a disc sector), is π minus the angle between the normals. -/
theorem wedgeAngle_two_planes {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] [Fact (finrank ℝ E = 3)]
    (a₁ a₂ : E) (h : LinearIndependent ℝ ![a₁, a₂]) :
    wedgeAngle (cone ![a₁, a₂] Set.univ) (linCone ![a₁, a₂] Set.univ) =
      Real.pi - InnerProductGeometry.angle a₁ a₂ := by
  sorry

/-- GAP 2 (cube). The Dehn invariant of the cube `[-s, s]³`, as a set, is zero. -/
theorem dehnSet_cube (s : ℝ) (hs : 0 < s) : dehnSet (cubeSet s) = 0 := by
  sorry

/-- GAP 3 (tetrahedron). The Dehn invariant of the regular tetrahedron with corners (−1,−1,−1), (1,1,−1),
(1,−1,1), (−1,1,1), as a set, is study 1's edge-list value for six edges of length 2√2 at arccos(1/3). -/
theorem dehnSet_tetra : dehnSet tetraSet = dehn (tetrahedron (2 * √2)) := by
  sorry

/-- Proved FROM gaps 2 and 3 (with the bridge of this study and Niven's theorem via study 1):
the regular tetrahedron is not scissors congruent to any cube. -/
theorem tetra_not_scissorsCongruent_cube (s : ℝ) (hs : 0 < s) :
    ¬ ScissorsCongruent tetraSet (cubeSet s) := by
  apply not_scissorsCongruent_of_dehnSet_ne isPoly_tetra (isPoly_cube s)
  rw [dehnSet_tetra, dehnSet_cube s hs]
  exact dehn_tetrahedron_ne_zero (by positivity)

end DehnCanon
