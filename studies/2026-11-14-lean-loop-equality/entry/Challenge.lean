module

public import Mathlib

@[expose] public section

/-!
# The Loop Equality (DICTO, paper #102, Theorem 1), with the explicit count, Corollary A and the flip formula

This file is the statement surface: definitions and theorem statements only,
every proof `sorry`. The proofs are in the library `LoopEquality`, re-exported
by `Solution.lean`.

Source: DICTO, *Every Site Hears the Same: the Loop Equality Is a Theorem*,
Zenodo 2026, DOI 10.5281/zenodo.24127070 (version 4). Corollary A and Theorem B (the flip formula, here
in counting form): #102 Version 6, DOI 10.5281/zenodo.24241321, §5; their machine-checked proofs: DICTO,
paper #125, *Loops and Polygons on Close-Packed Stackings* (Zenodo, DOI given at release).

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
* `corollaryA1`, `polysAtMostTwice_finite`, `corollaryA_everySite`,
  `polysAtMostTwice_diamond_six_pos`: a polygon is a minimal nonempty set of
  bonds with every atom of even degree. The polygons through a site with `l`
  edges that cross every bilayer at most twice are finitely many, are as many at
  every site of every stacking as at diamond's site `(0, (0, 0), 0)`, and there
  is at least one at `l = 6` (a hexagon) (Corollary A of #102).
* `theoremB`: the flip formula. Flipping bilayer `k` (every letter above it
  reflected through its letter) changes the number of polygons through a site
  below the cut by a finite sum over crossing sets, each term counted in the
  stacking before the flip: pairs of linkages below and above the cut that close
  into one cycle, with the upper linkage half-turned or not.
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

/-! ## Where the stackings differ: polygons crossing every bilayer at most twice

A polygon is a nonempty finite set of bonds in which every atom has even degree and
no nonempty proper subset has that property (a cycle). The cut at bilayer `k`
separates the upper atoms of bilayer `k` and everything above from the rest; an
edge crosses it when one end lies on each side. -/

open Classical in
/-- The number of edges of `E` at the atom `x`. -/
noncomputable def edgeDeg (E : Finset (Sym2 Atom)) (x : Atom) : ℕ := (E.filter (fun e => x ∈ e)).card

/-- A polygon of `G σ`. -/
def IsPolygon (σ : ℤ → ZMod 3) (E : Finset (Sym2 Atom)) : Prop :=
  E.Nonempty ∧ (∀ e ∈ E, ∃ a b, e = s(a, b) ∧ Bond σ a b) ∧ (∀ x, Even (edgeDeg E x)) ∧
    ∀ F ⊆ E, F.Nonempty → (∀ x, Even (edgeDeg F x)) → F = E

/-- The far side of the cut at bilayer `k`: the upper atom of bilayer `k` and everything above. -/
def IsAbove (k : ℤ) (v : Atom) : Prop := k < v.1 ∨ (v.1 = k ∧ v.2.2 = 1)

/-- The edge `e` crosses the cut at bilayer `k`. -/
def Crosses (k : ℤ) (e : Sym2 Atom) : Prop := ∃ a b, e = s(a, b) ∧ IsAbove k a ∧ ¬ IsAbove k b

open Classical in
/-- The number of edges of `E` crossing the cut at bilayer `k`. -/
noncomputable def crossings (E : Finset (Sym2 Atom)) (k : ℤ) : ℕ := (E.filter (Crosses k)).card

/-- The polygons of `G σ` through `v` with `l` edges that cross every bilayer at most twice. -/
def polysAtMostTwice (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) : Set (Finset (Sym2 Atom)) :=
  {E | IsPolygon σ E ∧ 0 < edgeDeg E v ∧ E.card = l ∧ ∀ k, crossings E k ≤ 2}

/-- **Corollary A1 (the half-turn surgery, every stacking).** For any two stackings
and an atom `v` that is a site of both, the number of polygons through `v` with `l`
edges crossing every bilayer at most twice is the same, for every `l`. -/
theorem corollaryA1 {σ τ : ℤ → ZMod 3} (hσ : IsStacking σ) (hτ : IsStacking τ) {v : Atom}
    (hvσ : IsSite σ v) (hvτ : IsSite τ v) (l : ℕ) :
    (polysAtMostTwice σ v l).ncard = (polysAtMostTwice τ v l).ncard := by
  sorry

/-- **Finiteness.** The polygons through `v` with `l` edges crossing every bilayer at
most twice form a finite set, so the counts in `corollaryA1` are genuine counts. -/
theorem polysAtMostTwice_finite (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) : (polysAtMostTwice σ v l).Finite := by
  sorry

/-- **Every site counts the same (Corollary A of #102, Version 6).** For every
stacking and every site `v` of it, the polygons through `v` with `l` edges crossing
every bilayer at most twice are as many as at diamond's site `(0, (0, 0), 0)`. -/
theorem corollaryA_everySite {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v : Atom} (hv : IsSite σ v) (l : ℕ) :
    (polysAtMostTwice σ v l).ncard = (polysAtMostTwice diamond (0, (0, 0), 0) l).ncard := by
  sorry

/-! ### Theorem B: the flip formula -/

/-- Flip bilayer `k`: every letter above bilayer `k` is reflected through the letter of bilayer `k`. -/
def flip (σ : ℤ → ZMod 3) (k : ℤ) (j : ℤ) : ZMod 3 := if j ≤ k then σ j else 2 * σ k - σ j

/-- The half-turn `p ↦ c - p` of the planar position of an atom. -/
def halfTurn (c : ℤ × ℤ) (a : Atom) : Atom := (a.1, c - a.2.1, a.2.2)

/-- The lower atom at position `p` of bilayer `k`. -/
def lower (k : ℤ) (p : ℤ × ℤ) : Atom := (k, p, 0)

/-- The upper atom at position `p` of bilayer `k`. -/
def upper (k : ℤ) (p : ℤ × ℤ) : Atom := (k, p, 1)

/-- `a` and `b` are joined by a path of edges of `L`. -/
def Joined (L : Finset (Sym2 Atom)) : Atom → Atom → Prop :=
  Relation.ReflTransGen (fun a b => s(a, b) ∈ L ∧ a ≠ b)

/-- `L` is a linkage with ends `B`: degree 1 at each end, 0 or 2 at every other atom, no nonempty subset of
`L` with every degree even, and no loops. -/
def IsLinkage (L : Finset (Sym2 Atom)) (B : Finset Atom) : Prop :=
  (∀ w ∈ B, edgeDeg L w = 1) ∧ (∀ w ∉ B, edgeDeg L w = 0 ∨ edgeDeg L w = 2) ∧
    (∀ G ⊆ L, G.Nonempty → ¬ ∀ x, Even (edgeDeg G x)) ∧ (∀ e ∈ L, ¬ e.IsDiag)

/-- A linkage of `G σ` below the cut at bilayer `k`, ending at the lower atoms of `P`. -/
def rootLinkage (σ : ℤ → ZMod 3) (k : ℤ) (P : Finset (ℤ × ℤ)) (R : Finset (Sym2 Atom)) : Prop :=
  IsLinkage R (P.image (lower k)) ∧ (∀ e ∈ R, ∀ w ∈ e, ¬ IsAbove k w) ∧
    ∀ e ∈ R, ∃ a b, e = s(a, b) ∧ Bond σ a b

/-- A linkage of `G σ` above the cut at bilayer `k`, ending at the upper atoms of `P`. -/
def farLinkage (σ : ℤ → ZMod 3) (k : ℤ) (P : Finset (ℤ × ℤ)) (F : Finset (Sym2 Atom)) : Prop :=
  IsLinkage F (P.image (upper k)) ∧ (∀ e ∈ F, ∀ w ∈ e, IsAbove k w) ∧
    ∀ e ∈ F, ∃ a b, e = s(a, b) ∧ Bond σ a b

/-- The pairings of the ends by `R` (below) and `F` (above) close into a single cycle: no nonempty proper
subset of `P` is closed under both. -/
def OneCycle (k : ℤ) (P : Finset (ℤ × ℤ)) (R F : Finset (Sym2 Atom)) : Prop :=
  ∀ Q ⊆ P, Q.Nonempty → (∀ p ∈ Q, ∀ q ∈ P, Joined R (lower k p) (lower k q) → q ∈ Q) →
    (∀ p ∈ Q, ∀ q ∈ P, Joined F (upper k p) (upper k q) → q ∈ Q) → Q = P

/-- The polygons of `G σ` through `v` with `l` edges. -/
def polysThrough (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) : Set (Finset (Sym2 Atom)) :=
  {E | IsPolygon σ E ∧ 0 < edgeDeg E v ∧ E.card = l}

/-- Pairs (linkage below through `v`, linkage above) of `G σ`, both ending at `P`, closing into one cycle,
with `l` edges in all (counting the vertical bonds at `P`). -/
def stayPairs (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) (k : ℤ) (P : Finset (ℤ × ℤ)) :
    Set (Finset (Sym2 Atom) × Finset (Sym2 Atom)) :=
  {RF | rootLinkage σ k P RF.1 ∧ farLinkage σ k P RF.2 ∧ 0 < edgeDeg RF.1 v ∧
    RF.1.card + P.card + RF.2.card = l ∧ OneCycle k P RF.1 RF.2}

/-- Pairs (linkage below through `v` ending at `P`, linkage above ending at `c - P`) of `G σ` whose
half-turned upper part closes the lower part into one cycle, with `l` edges in all. -/
def flipPairs (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) (k : ℤ) (P : Finset (ℤ × ℤ)) (c : ℤ × ℤ) :
    Set (Finset (Sym2 Atom) × Finset (Sym2 Atom)) :=
  {RF | rootLinkage σ k P RF.1 ∧ farLinkage σ k (P.image (fun p => c - p)) RF.2 ∧ 0 < edgeDeg RF.1 v ∧
    RF.1.card + P.card + RF.2.card = l ∧ OneCycle k P RF.1 (RF.2.image (Sym2.map (halfTurn c)))}

/-- The planar positions within `2l` of `v` in both coordinates. -/
def window (v : Atom) (l : ℕ) : Finset (ℤ × ℤ) :=
  Finset.Icc (v.2.1.1 - 2 * l) (v.2.1.1 + 2 * l) ×ˢ Finset.Icc (v.2.1.2 - 2 * l) (v.2.1.2 + 2 * l)

open Classical in
/-- **Theorem B (the flip formula).** Flip bilayer `k` of any stacking, with `c ≡ 2·σ k` in both
coordinates, mod 3. For every atom `v` below the cut at bilayer `k`, the polygons through `v` with `l` edges
after the flip are as many as before, plus the sum over the nonempty sets `P` of crossing positions (with
vertical bonds) of `#flipPairs − #stayPairs`: every term is counted in the stacking before the flip. -/
theorem theoremB {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {c : ℤ × ℤ}
    (hc : (c.1 : ZMod 3) = 2 * σ k ∧ (c.2 : ZMod 3) = 2 * σ k) (hv : ¬ IsAbove k v) :
    ((polysThrough (flip σ k) v l).ncard : ℤ) = (polysThrough σ v l).ncard +
      ∑ P ∈ (window v l).powerset.filter (fun P => P.Nonempty ∧ ∀ p ∈ P, Bond σ (lower k p) (upper k p)),
        (((flipPairs σ v l k P c).ncard : ℤ) - (stayPairs σ v l k P).ncard) := by
  sorry

/-- **The count is not empty.** Diamond has a polygon through its site `(0, (0, 0), 0)` with 6 edges crossing
every bilayer at most twice (a hexagon), so the counts compared by Corollary A are not all zero. -/
theorem polysAtMostTwice_diamond_six_pos : 0 < (polysAtMostTwice diamond (0, (0, 0), 0) 6).ncard := by
  sorry

/-- The polygons of `G σ` through `v` with `l` edges whose crossing profile is `π`: exactly `π j` edges
cross the cut at bilayer `j`, for every `j`. -/
def polysWithProfile (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) (π : ℤ → ℕ) : Set (Finset (Sym2 Atom)) :=
  {E | IsPolygon σ E ∧ 0 < edgeDeg E v ∧ E.card = l ∧ ∀ j, crossings E j = π j}

/-- **Corollary A of #102, profile by profile.** Fix a length `l` and a crossing profile `π` with every entry
at most 2. For any two stackings and an atom `v` that is a site of both, the polygons through `v` with `l`
edges and exactly that profile are equally many. -/
theorem corollaryA_profile {σ τ : ℤ → ZMod 3} (hσ : IsStacking σ) (hτ : IsStacking τ) {v : Atom}
    (hvσ : IsSite σ v) (hvτ : IsSite τ v) (l : ℕ) (π : ℤ → ℕ) (hπ : ∀ j, π j ≤ 2) :
    (polysWithProfile σ v l π).ncard = (polysWithProfile τ v l π).ncard := by
  sorry

/-- The profile `π` read from the bilayer of `v`: upward from a lower atom, downward from an upper atom. -/
def profileFrom (v : Atom) (π : ℤ → ℕ) : ℤ → ℕ := fun i => if v.2.2 = 0 then π (v.1 + i) else π (v.1 - i)

/-- **Every site counts the same, profile by profile.** For every stacking `σ`, every site `v` of it and every
crossing profile `π` with entries at most 2, the polygons through `v` with `l` edges and profile `π` are as many
as at diamond's site `(0, (0, 0), 0)` with the profile read from `v`'s bilayer. -/
theorem corollaryA_everySite_profile {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v : Atom} (hv : IsSite σ v) (l : ℕ)
    (π : ℤ → ℕ) (hπ : ∀ j, π j ≤ 2) :
    (polysWithProfile σ v l π).ncard = (polysWithProfile diamond (0, (0, 0), 0) l (profileFrom v π)).ncard := by
  sorry

end DictoLoopEquality
