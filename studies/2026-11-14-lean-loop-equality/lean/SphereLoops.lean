module

public import Mathlib
public import LoopEquality.Defs

@[expose] public section

/-!
# Companion statement (not proved): #102 Corollary 3, sphere packings

Scouting file for COMPANIONS.md. The proof is `sorry`; this file only checks
that the statement typechecks. It is NOT part of the `LoopEquality` library.

In the packing of equal spheres of a close-packed stacking `σ`, the sphere
centres are `(k, p)` with `p` in position `σ k` (one level per close-packed
layer). Two spheres touch when they lie in the same layer at distance 1, i.e.
`q - p` is one of the six shortest vectors of `Λ` (`latVecs`), or in neighbouring
layers with `q - p` one of the six `shortVecs`. #102 Corollary 3: at every sphere
of every stacking, the closed non-backtracking loops of every length number
those of fcc (the stacking `diamond`, ABCABC…).
-/

namespace DictoLoopEquality

/-- The six shortest vectors of `Λ` (unit length), in the coordinates of `Defs`. -/
def latVecs : Finset (ℤ × ℤ) := {(3, 0), (0, 3), (3, -3), (-3, 0), (0, -3), (-3, 3)}

/-- A sphere of the packing of `σ`: layer `k`, planar point `p` in position `σ k`. -/
def IsSphere (σ : ℤ → ZMod 3) (v : ℤ × (ℤ × ℤ)) : Prop :=
  ((v.2.1 : ZMod 3) = σ v.1) ∧ ((v.2.2 : ZMod 3) = σ v.1)

/-- Touching spheres. -/
def Touch (σ : ℤ → ZMod 3) (v w : ℤ × (ℤ × ℤ)) : Prop :=
  IsSphere σ v ∧ IsSphere σ w ∧
    ((v.1 = w.1 ∧ w.2 - v.2 ∈ latVecs) ∨
     ((w.1 = v.1 + 1 ∨ v.1 = w.1 + 1) ∧ w.2 - v.2 ∈ shortVecs))

/-- Closed non-backtracking loops of length `m` at the sphere `v`. -/
def sphereLoops (σ : ℤ → ZMod 3) (v : ℤ × (ℤ × ℤ)) (m : ℕ) [NeZero m] :
    Set (Fin m → ℤ × (ℤ × ℤ)) :=
  {f | f 0 = v ∧ ∀ i, Touch σ (f i) (f (i + 1)) ∧ f (i + 2) ≠ f i}

/-- **#102 Corollary 3** (statement only). -/
theorem sphere_loop_equality (σ : ℤ → ZMod 3) (hσ : IsStacking σ) (v : ℤ × (ℤ × ℤ))
    (hv : IsSphere σ v) (m : ℕ) [NeZero m] :
    (sphereLoops σ v m).ncard = (sphereLoops diamond (0, (0, 0)) m).ncard := by
  sorry

end DictoLoopEquality
