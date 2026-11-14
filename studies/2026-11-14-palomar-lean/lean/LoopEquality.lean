module

public import Mathlib

@[expose] public section

/-!
# The Loop Equality (DICTO, paper #102, Theorem 1)

Statement surface only (every proof is `sorry`); candidate Challenge for a
Palomar entry.

Planar coordinates: the pair `(i, j) : ℤ × ℤ` stands for the point
`(i a₁ + j a₂) / 3`, where `a₁, a₂` are unit vectors at 60°. The three
close-packed positions A, B, C (`c = 0, 1, 2 : ZMod 3`) are the points with
`i ≡ j ≡ c (mod 3)`. A stacking is `σ : ℤ → ZMod 3` with `σ (k+1) ≠ σ k`,
periodic or not; `σ k = k` is diamond (3C).

The tetrahedral network `G σ`: at bilayer `k` there is a lower atom
`(k, p, 0)` and an upper atom `(k, p, 1)` at every point `p` of position
`σ k`. Each lower atom is bonded to the upper atom above it, and each upper
atom `(k, p, 1)` to the three lower atoms `(k+1, q, 0)` with `|q - p| = 1/√3`,
i.e. `q - p` one of the six vectors `shortVecs`.

A closed non-backtracking loop of length `m` at `v` is a cyclic sequence
`f : Fin m → Atom` with `f 0 = v`, consecutive atoms bonded, and
`f (i + 2) ≠ f i` for every `i` (indices mod `m`): it never turns straight back,
including across the start.
-/

namespace DictoLoopEquality

/-- A close-packed stacking: neighbouring layers in different positions. -/
def IsStacking (σ : ℤ → ZMod 3) : Prop := ∀ k, σ (k + 1) ≠ σ k

/-- Diamond (3C): the stacking ABCABC... -/
def diamond : ℤ → ZMod 3 := fun k => (k : ZMod 3)

/-- An atom label: bilayer `k`, planar point `p`, lower (`0`) or upper (`1`). -/
abbrev Atom := ℤ × (ℤ × ℤ) × Fin 2

/-- `v` is an atom of `G σ`: its planar point has the position of its bilayer. -/
def IsSite (σ : ℤ → ZMod 3) (v : Atom) : Prop :=
  ((v.2.1.1 : ZMod 3) = σ v.1) ∧ ((v.2.1.2 : ZMod 3) = σ v.1)

/-- The six planar vectors of length `1/√3`, in the coordinates above. -/
def shortVecs : Finset (ℤ × ℤ) := {(1, 1), (-2, 1), (1, -2), (-1, -1), (2, -1), (-1, 2)}

/-- The bonds of `G σ`. -/
def Bond (σ : ℤ → ZMod 3) (v w : Atom) : Prop :=
  IsSite σ v ∧ IsSite σ w ∧
    ((v.1 = w.1 ∧ v.2.1 = w.2.1 ∧ v.2.2 ≠ w.2.2) ∨
     (w.1 = v.1 + 1 ∧ v.2.2 = 1 ∧ w.2.2 = 0 ∧ w.2.1 - v.2.1 ∈ shortVecs) ∨
     (v.1 = w.1 + 1 ∧ w.2.2 = 1 ∧ v.2.2 = 0 ∧ v.2.1 - w.2.1 ∈ shortVecs))

/-- Closed non-backtracking loops of length `m` at `v` in `G σ`. -/
def nbLoops (σ : ℤ → ZMod 3) (v : Atom) (m : ℕ) [NeZero m] : Set (Fin m → Atom) :=
  {f | f 0 = v ∧ ∀ i, Bond σ (f i) (f (i + 1)) ∧ f (i + 2) ≠ f i}

/-- There are finitely many such loops. -/
theorem nbLoops_finite (σ : ℤ → ZMod 3) (v : Atom) (m : ℕ) [NeZero m] :
    (nbLoops σ v m).Finite := by
  sorry

/-- **The Loop Equality (#102, Theorem 1).** On the tetrahedral network of
every close-packed stacking, periodic or not, at every site and for every
length, the number of closed non-backtracking loops equals the number at a
site of diamond. -/
theorem loop_equality (σ : ℤ → ZMod 3) (hσ : IsStacking σ) (v : Atom) (hv : IsSite σ v)
    (m : ℕ) [NeZero m] :
    (nbLoops σ v m).ncard = (nbLoops diamond (0, (0, 0), 0) m).ncard := by
  sorry

end DictoLoopEquality
