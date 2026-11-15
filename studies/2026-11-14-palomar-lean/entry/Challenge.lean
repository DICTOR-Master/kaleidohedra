module

public import Mathlib

@[expose] public section

/-!
# The Loop Equality (DICTO, paper #102, Theorem 1), with the explicit count

This file is the statement surface: definitions and theorem statements only,
every proof `sorry`. The proofs are in the library `LoopEquality`, re-exported
by `Solution.lean`.

Source: DICTO, *Every Site Hears the Same: the Loop Equality Is a Theorem*,
Zenodo 2026, DOI 10.5281/zenodo.24127070 (version 4).

## The model

Planar coordinates: the pair `(i, j) : ℤ × ℤ` stands for the point
`(i a₁ + j a₂) / 3`, where `a₁, a₂` are unit vectors at 60°. The three
close-packed positions A, B, C (`c = 0, 1, 2 : ZMod 3`) are the points with
`i ≡ j ≡ c (mod 3)`. A close-packed stacking is `σ : ℤ → ZMod 3` with
`σ (k+1) ≠ σ k`, periodic or not; `σ k = k` is diamond (3C). The stackings
include lonsdaleite (2H), every polytype, and every aperiodic stacking.

The tetrahedral network `G σ` (the bond network of diamond, lonsdaleite, ice
Ic/Ih and their polytypes): at bilayer `k` there is a lower atom `(k, p, 0)` and
an upper atom `(k, p, 1)` at every point `p` of position `σ k`. Each lower atom
is bonded to the upper atom above it, and each upper atom `(k, p, 1)` to the
three lower atoms `(k+1, q, 0)` with `|q - p| = 1/√3`, i.e. `q - p` one of the
six vectors `shortVecs`.

A closed non-backtracking loop of length `m` at `v` is a cyclic sequence
`f : Fin m → Atom` with `f 0 = v`, consecutive atoms bonded, and
`f (i + 2) ≠ f i` for every `i` (indices mod `m`): it never turns straight back,
including across the start. These are the rooted cycles counted by the Ihara
zeta function.

## The results

* `nbLoops_finite`, `loop_equality`: at every site of every stacking the number
  of closed non-backtracking loops of each length equals the number at a site of
  diamond (#102, Theorem 1).
* `loop_count_eq`: that number is `loopCount m`, an explicit computable integer
  (#102, "Explicitly"); `loopCount_values` and `loopCount_values_34` give the
  values for `m ≤ 34` listed in #102; `closedWalks_domb_small` and
  `loopCount_eq_iharaBass_small` compare the formula with the Domb numbers and
  with #102's Ihara–Bass series for small lengths.
* `W_closed`, `bond_iff`: the number of closed walks at every atom of every
  stacking is `closedWalks i` (Thorpe 1972 for periodic polytypes; #102 Lemma 2
  (a) and Proposition); the neighbour function `nbr` used there is the bond
  relation at every site.
* `Graph.loops_ncard_eq_FD`: the general local loop formula behind
  `loop_count_eq`. In any graph, finite or infinite, in which every vertex has
  `q + 1` neighbours and the same closed-walk counts `w i`, the closed
  non-backtracking loops of length `m ≥ 3` at a vertex are finitely many and
  number `FD (dataW q w) m false false`.
* `fibonacci_isStacking`, `fibonacci_zero`, `fibonacci_one`,
  `fibonacci_layer_type`, `isH_eq_word`, `fibonacci_not_periodic`,
  `fibonacci_loop_equality`: the Fibonacci stacking is an aperiodic close-packed
  stacking whose hexagonal layers follow the Fibonacci word, and the Loop
  Equality holds on it with the same explicit count.
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

end DictoLoopEquality

/-! ## Graphs given by neighbour sets -/

namespace DictoLoopEquality.Graph

open Finset Polynomial

variable {V : Type*} [DecidableEq V] (nbr : V → Finset V)

/-- Walks of length `i` from `x` to `y` in the graph with neighbour sets `nbr`. -/
def W : ℕ → V → V → ℕ
  | 0, x, y => if x = y then 1 else 0
  | i + 1, x, y => ∑ z ∈ nbr x, W i z y

/-- A symmetric loopless graph in which every vertex has `q + 1` neighbours. -/
structure IsRegular (q : ℕ) : Prop where
  symm : ∀ x y, y ∈ nbr x → x ∈ nbr y
  irrefl : ∀ x, x ∉ nbr x
  card : ∀ x, (nbr x).card = q + 1

variable {nbr}

variable (nbr) in
/-- Closed non-backtracking loops of length `m` at `v` (the same shape as `nbLoops`). -/
def loops (v : V) (m : ℕ) [NeZero m] : Set (Fin m → V) :=
  {f | f 0 = v ∧ ∀ i, f (i + 1) ∈ nbr (f i) ∧ f (i + 2) ≠ f i}

end DictoLoopEquality.Graph

namespace DictoLoopEquality.Graph

open Finset

variable {V : Type*} [DecidableEq V] {nbr : V → Finset V}

/-- Integer coefficients with `A j = Σ_i cA q j i · W i` for the non-backtracking
walk counts `A j` in a graph with `q + 1` neighbours everywhere (the standard
recursion `A₂ = A·A₁ − (q+1)A₀`, `A_{j+2} = A·A_{j+1} − q A_j`). -/
def cA (q : ℕ) : ℕ → ℕ → ℤ
  | 0, i => if i = 0 then 1 else 0
  | 1, i => if i = 1 then 1 else 0
  | 2, i => (if i = 2 then 1 else 0) - ((q : ℤ) + 1) * (if i = 0 then 1 else 0)
  | j + 3, i => (if i = 0 then 0 else cA q (j + 2) (i - 1)) - (q : ℤ) * cA q (j + 1) i

/-- Walk data on the two ends of a bond: `d s t j` stands for the number of
non-backtracking walks of length `j` between the ends selected by `s` and `t`. -/
abbrev Data := Bool → Bool → ℕ → ℤ

/-- The bond recursion for non-backtracking walks whose first step is forbidden
(Hashimoto 1989; Bass 1992; #102, Lemma 3), with the walk counts as data. -/
def nbD (d : Data) : ℕ → Bool → Bool → ℤ
  | 0, s, t => d (!s) t 0
  | k + 1, s, t => d (!s) t (k + 1) - nbD d k (!s) t

/-- The bond recursion for non-backtracking edge sequences (entries of the powers
of Hashimoto's edge matrix; #102, Lemma 3), with the walk counts as data. -/
def FD (d : Data) : ℕ → Bool → Bool → ℤ
  | 0, s, t => d s t 0
  | k + 1, s, t => nbD d k s t - FD d k s (!t)

/-- The bond data summed over the `q + 1` bonds at a vertex, when every vertex
has closed-walk counts `w`. -/
def dataW (q : ℕ) (w : ℕ → ℤ) : Data := fun s t j =>
  if s = t then ((q : ℤ) + 1) * ∑ i ∈ range (j + 1), cA q j i * w i
  else ∑ i ∈ range (j + 1), cA q j i * w (i + 1)

/-- **Local loop formula.** In a symmetric loopless graph (finite or infinite)
in which every vertex has `q + 1` neighbours and the same closed-walk counts
`w i`, the closed non-backtracking loops of length `m ≥ 3` at any vertex are
finitely many and number `FD (dataW q w) m false false`. -/
theorem loops_ncard_eq_FD {q : ℕ} (hr : IsRegular nbr q) (w : ℕ → ℤ)
    (hw : ∀ x i, (W nbr i x x : ℤ) = w i) (v : V) (m : ℕ) [NeZero m] (hm : 3 ≤ m) :
    (loops nbr v m).Finite ∧ ((loops nbr v m).ncard : ℤ) = FD (dataW q w) m false false := by
  sorry

end DictoLoopEquality.Graph

/-! ## The neighbours of an atom -/

namespace DictoLoopEquality

open Finset

/-- The triangle `D` of the three shortest vectors of `Λ + t`. -/
def triD : Finset (ℤ × ℤ) := {(1, 1), (-2, 1), (1, -2)}

/-- `d` if `σ (k+1) - σ k = 1`, and `-d` otherwise. -/
def sd (σ : ℤ → ZMod 3) (k : ℤ) (d : ℤ × ℤ) : ℤ × ℤ :=
  if σ (k + 1) - σ k = 1 then d else -d

/-- The four neighbours of an atom. The formula is used at every atom; at a site
of a stacking it is exactly the bond relation (`bond_iff`). -/
def nbr (σ : ℤ → ZMod 3) (v : Atom) : Finset Atom :=
  if v.2.2 = 0 then
    insert (v.1, v.2.1, 1) (triD.image fun d => (v.1 - 1, v.2.1 - sd σ (v.1 - 1) d, 1))
  else
    insert (v.1, v.2.1, 0) (triD.image fun d => (v.1 + 1, v.2.1 + sd σ v.1 d, 0))

/-- At a site of a stacking, the bonds are exactly the neighbours `nbr`. -/
theorem bond_iff {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v w : Atom} (hv : IsSite σ v) :
    Bond σ v w ↔ w ∈ nbr σ v := by
  sorry

end DictoLoopEquality

/-! ## The closed walks -/

namespace DictoLoopEquality

open Finset AddMonoidAlgebra

/-- `H(a)`: closed walks of length `2a` on the honeycomb net (OEIS A002893),
written with multinomials `C(a, i) C(a - i, j) = a! / (i! j! (a-i-j)!)`. -/
def honeycomb (a : ℕ) : ℕ :=
  ∑ i ∈ range (a + 1), ∑ j ∈ range (a - i + 1), (a.choose i * (a - i).choose j) ^ 2

/-- The chain formula of #102: `Σ_{a ≤ n} C(n, a)² H(a)`. -/
def chainWalks (n : ℕ) : ℕ := ∑ a ∈ range (n + 1), n.choose a ^ 2 * honeycomb a

/-- Closed walks of length `i` at a site: `0` for odd `i`, `chainWalks (i/2)` for even `i`. -/
def closedWalks (i : ℕ) : ℕ := if i % 2 = 0 then chainWalks (i / 2) else 0

/-- The Domb numbers, OEIS A002895: `Σ_k C(n,k)² C(2k,k) C(2n-2k,n-k)`. -/
def domb (n : ℕ) : ℕ :=
  ∑ k ∈ range (n + 1), n.choose k ^ 2 * (2 * k).choose k * (2 * (n - k)).choose (n - k)

/-- **Closed walks at every atom of every stacking** (#102, Lemma 2 (a) and the
Proposition; Thorpe 1972 for periodic polytypes, Nagle 1966 for ice): the
number of closed walks of length `i` at any atom is `closedWalks i`. -/
theorem W_closed (σ : ℤ → ZMod 3) (x : Atom) (i : ℕ) :
    Graph.W (nbr σ) i x x = closedWalks i := by
  sorry

end DictoLoopEquality

/-! ## The Loop Equality and the explicit count -/

namespace DictoLoopEquality

open Finset

/-- There are finitely many closed non-backtracking loops of each length. -/
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

/-- The explicit number of closed non-backtracking loops of length `m` at a site:
the local loop formula with `q = 3` applied to the closed-walk counts. -/
def loopCount (m : ℕ) : ℤ :=
  Graph.FD (Graph.dataW 3 (fun i => (closedWalks i : ℤ))) m false false

/-- **The Loop Equality, explicit form.** For every stacking `σ`, every site `v`
of its tetrahedral network and every `m ≥ 1`, the number of closed
non-backtracking loops of length `m` at `v` is `loopCount m`. -/
theorem loop_count_eq (σ : ℤ → ZMod 3) (hσ : IsStacking σ) (v : Atom) (hv : IsSite σ v)
    (m : ℕ) [NeZero m] : ((nbLoops σ v m).ncard : ℤ) = loopCount m := by
  sorry

/-- The first values (#102: 24, 48, 480, 3432 for m = 6, 8, 10, 12). -/
theorem loopCount_values :
    loopCount 3 = 0 ∧ loopCount 4 = 0 ∧ loopCount 5 = 0 ∧ loopCount 6 = 24 ∧ loopCount 7 = 0 ∧
      loopCount 8 = 48 ∧ loopCount 10 = 480 ∧ loopCount 12 = 3432 := by
  sorry

/-- #102's values for `m = 14, …, 34`. -/
theorem loopCount_values_34 :
    loopCount 14 = 25704 ∧ loopCount 16 = 194256 ∧ loopCount 18 = 1509072 ∧
      loopCount 20 = 11820000 ∧ loopCount 22 = 93722376 ∧ loopCount 24 = 750276792 ∧
      loopCount 26 = 6056400480 ∧ loopCount 28 = 49241424120 ∧ loopCount 30 = 402912569544 ∧
      loopCount 32 = 3315331754256 ∧ loopCount 34 = 27416593190640 := by
  sorry

/-- The closed walks at a site are the Domb numbers for `i = 2n`, `n < 10`.
The identity for all `n` (Bala's comment on OEIS A002895) is not stated here. -/
theorem closedWalks_domb_small : ∀ n < 10, closedWalks (2 * n) = domb n := by
  sorry

/-- The coefficient of `u^m` in #102's Ihara–Bass series, times `m`. -/
def iharaBass (m : ℕ) : ℚ :=
  (if m % 2 = 0 then 2 else 0) +
    ∑ j ∈ Icc 1 m, if m ≤ 2 * j then
      (m : ℚ) / j * (j.choose (2 * j - m) : ℚ) * (closedWalks (2 * j - m) : ℚ) * (-3) ^ (m - j)
    else 0

/-- `loopCount` agrees with #102's Ihara–Bass coefficients for `1 ≤ m ≤ 12`.
The identity for all `m` is not stated here. -/
theorem loopCount_eq_iharaBass_small : ∀ m ∈ Icc 1 12, (loopCount m : ℚ) = iharaBass m := by
  sorry

end DictoLoopEquality

/-! ## The aperiodic Fibonacci stacking -/

namespace DictoLoopEquality

open Finset

/-- `α = 1/φ² = (3 − √5)/2`, the frequency of `h` in the Fibonacci word. -/
noncomputable def fibAlpha : ℝ := (3 - Real.sqrt 5) / 2

/-- `⌊(k+2)α⌋`: the number of `h` letters at positions `1, …, k` (for `k ≥ 0`). -/
noncomputable def fibFlip (k : ℤ) : ℤ := ⌊((k : ℝ) + 2) * fibAlpha⌋

/-- The Fibonacci letter at position `k` is `h` (cut-and-project form of the
Sturmian word of slope `α`; Morse–Hedlund 1940; Lothaire 2002, Ch. 2). -/
def IsH (k : ℤ) : Prop := fibFlip k ≠ fibFlip (k - 1)

/-- The step `σ(k+1) − σ(k)`: `+1` or `−1`, that is `(−1)^⌊(k+2)α⌋`
(Jagodzinski's rule: the step keeps its direction at a `c` layer and reverses at
an `h` layer). -/
noncomputable def fibStep (k : ℤ) : ZMod 3 := if Even (fibFlip k) then 1 else -1

/-- The Fibonacci stacking: `σ 0 = A` and the steps `fibStep`. -/
noncomputable def fibonacci (k : ℤ) : ZMod 3 :=
  if 0 ≤ k then ∑ n ∈ range k.toNat, fibStep n
  else -∑ n ∈ range (-k).toNat, fibStep (-1 - n)

/-- The Fibonacci stacking is a close-packed stacking. -/
theorem fibonacci_isStacking : IsStacking fibonacci := by
  sorry

/-- `σ 0 = A`. -/
theorem fibonacci_zero : fibonacci 0 = 0 := by
  sorry

/-- `σ 1 = B`. -/
theorem fibonacci_one : fibonacci 1 = 1 := by
  sorry

/-- **Jagodzinski's rule.** Layer `k` is hexagonal (its two neighbours are in the
same position) exactly when the Fibonacci letter at `k` is `h`. -/
theorem fibonacci_layer_type (k : ℤ) : fibonacci (k - 1) = fibonacci (k + 1) ↔ IsH k := by
  sorry

/-- One application of the Fibonacci substitution `c ↦ ch`, `h ↦ c`
(`false` = c, `true` = h). -/
def fibSubst (w : List Bool) : List Bool := w.flatMap fun b => if b then [false] else [false, true]

/-- The substitution applied `n` times to `c`. -/
def fibWord (n : ℕ) : List Bool := (fibSubst)^[n] [false]

/-- The cut-and-project letters agree with the substitution word at positions
`0, …, 99`. Equality at every position is the classical Sturmian
characterisation and is not stated here. -/
theorem isH_eq_word (k : ℕ) (hk : k < 100) : IsH k ↔ (fibWord 10).getD k false = true := by
  sorry

/-- **The Fibonacci stacking is not periodic.** -/
theorem fibonacci_not_periodic (p : ℤ) (hp : p ≠ 0) : ¬ ∀ k, fibonacci (k + p) = fibonacci k := by
  sorry

/-- **Corollary (aperiodic case).** At every site of the aperiodic Fibonacci
stacking, the number of closed non-backtracking loops of length `m` equals
diamond's, and equals the explicit `loopCount m`. -/
theorem fibonacci_loop_equality (v : Atom) (hv : IsSite fibonacci v) (m : ℕ) [NeZero m] :
    (nbLoops fibonacci v m).ncard = (nbLoops diamond (0, (0, 0), 0) m).ncard ∧
      ((nbLoops fibonacci v m).ncard : ℤ) = loopCount m := by
  sorry

end DictoLoopEquality
