/-
Lean study 2 of the shape-language canon (DICTO, 19 Nov 2026), optional part H: the convex polytopes of this
study (bounded intersections of finitely many half-spaces) are exactly the convex hulls of finite point sets.

BORROWED, credited here at the point of use: the Minkowski–Weyl theorem `Chapter10.isConvexPolytope_iff`
from FormalBook, file FormalBook/Chapter_10.lean (Proofs from THE BOOK ch. 10 in Lean, github mo271/FormalBook,
PR #157, merge commit 54da1cecd8f3a27faa5d46a23b273611fc4f3365, Apache 2.0). That file is not copied into this
study; to compile this part, place it in the workspace as FormalBook/Chapter_10.lean.
No `sorry`.
-/
import DehnCanon.Dehn2R3
import FormalBook.Chapter_10

open Set

namespace DehnCanon

/-- A set in ℝ³ is a convex polytope in the sense of this study iff it is the convex hull of a finite set
(Minkowski–Weyl, from FormalBook). -/
theorem isPoly_iff_convexHull {P : Set R3} :
    IsPoly P ↔ ∃ S : Finset R3, P = convexHull ℝ (S : Set R3) :=
  (Chapter10.isConvexPolytope_iff (d := 3) (P := P)).symm

/-- **Dehn's theorem, the bridge, for convex hulls of finite point sets in ℝ³.** -/
theorem dehn_bridge_convexHull (S T : Finset R3)
    (h : ScissorsCongruent (convexHull ℝ (S : Set R3)) (convexHull ℝ (T : Set R3))) :
    dehnSet (convexHull ℝ (S : Set R3)) = dehnSet (convexHull ℝ (T : Set R3)) :=
  dehn_bridge_R3 (isPoly_iff_convexHull.2 ⟨S, rfl⟩) (isPoly_iff_convexHull.2 ⟨T, rfl⟩) h

end DehnCanon

#print axioms DehnCanon.isPoly_iff_convexHull
#print axioms DehnCanon.dehn_bridge_convexHull
