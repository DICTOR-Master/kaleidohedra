# The Loop Equality in Lean

A Lean 4 / Mathlib formalisation of **Theorem 1 of DICTO's paper #102**,
*Every Site Hears the Same: the Loop Equality Is a Theorem* (Zenodo 2026,
[doi:10.5281/zenodo.24127070](https://doi.org/10.5281/zenodo.24127070)),
with its explicit count and an aperiodic companion.

Author and maintainer: DICTO. The Lean code was written with an AI agent
(Claude Code, Opus); see `formalization.yaml`, section `automation`.

## The result

Take any close-packed stacking σ : ℤ → ZMod 3 (neighbouring layers in different
positions; periodic or not) and its tetrahedral bond network: the network of
diamond, lonsdaleite, ice Ic/Ih, and every polytype and aperiodic stacking of
them. Then:

* **Loop Equality** (`loop_equality`, `nbLoops_finite`). At every site, the
  number of closed non-backtracking loops of length m equals the number at a
  site of diamond, for every m.
* **Explicit count** (`loop_count_eq`). That number is `loopCount m`, an
  explicit computable integer: 0 for odd m, and 24, 48, 480, 3432, 25704, …,
  27416593190640 for m = 6, 8, …, 34 (`loopCount_values`, `loopCount_values_34`).
* **Closed walks** (`W_closed`, with `bond_iff`). At every atom of every stacking
  the closed walks of length 2n number Σ_a C(n,a)² H(a), with H(a) the
  honeycomb closed-walk numbers: the Domb numbers 1, 4, 28, 256, 2716, …
  (`closedWalks_domb_small` for n < 10).
* **Local loop formula** (`Graph.loops_ncard_eq_FD`). In any graph, finite or
  infinite, in which every vertex has q + 1 neighbours and the same closed-walk
  counts, the closed non-backtracking loops at a vertex are an explicit integer
  combination of those counts.
* **Fibonacci stacking** (`fibonacci_isStacking`, `fibonacci_layer_type`,
  `isH_eq_word`, `fibonacci_not_periodic`, `fibonacci_loop_equality`). The
  stacking whose hexagonal layers follow the Fibonacci word is an aperiodic
  close-packed stacking, and the Loop Equality holds on it with the same count.

The non-backtracking loops are the rooted cycles counted by the Ihara zeta
function. For finite or periodic graphs, loop counts are usually reached through
the Ihara–Bass determinant formula; here the network is aperiodic in general,
and the count is proved at every single site, not on average.

## Files

- `Challenge.lean`: the statement surface (definitions and statements, every
  proof `sorry`), 17 compared theorems; read this first.
- `Solution.lean`: the same definitions and statements with proofs. Each proof
  transfers a theorem of the proof library (namespace `LoopEqualityProof`, whose
  definitions are copies of the Challenge's) by definitional unfolding, with
  small transfer lemmas for the recursive definitions; the values are checked
  again by kernel evaluation.
- `LoopEquality/`: the proof library, in 11 modules (Defs, Graph, Levels,
  Network, Counts, Main, ClosedWalks, LocalFormula, Explicit, Fibonacci, Axioms).
- `comparator.json`: the 17 compared theorems and the permitted axioms.
- `formalization.yaml`: metadata (v0.4).

## Proof account

The proof follows #102, Section 2, with two changes.

1. **Walks as coefficients** (`Levels`, `Counts`). A walk's planar displacement
   is the exponent of a monomial in the group ring ℤ[ℤ²], so the number of walks
   from x to y is a coefficient of a level generating function Q_i (this replaces
   #102's torus integral, Lemma 1). A gauge lemma (`Levels.Q_eq`) writes
   Q_i = H·E_i, where E_i depends only on N = up·dn, and N does not depend on
   the stacking (#102 fact (i); the layer gauge of He–Wilson–Ganesh 2024). With
   the conjugation and the order-3 rotation of ℤ² (`E_inv`), the walk counts at
   a site and along each kind of bond are the same for every stacking
   (`W_site`, `W_vert`, `W_cross`; #102 Lemma 2 (a), (b)).
2. **Loops from walks** (`Graph`). Non-backtracking walks are integer
   combinations of walks (the standard recursion, Hashimoto 1989, Bass 1992).
   The loops through a bond are determined by the walk counts on its four end
   pairs (`Graph.transfer`, #102 Lemma 3), and the loops at a vertex are edge
   sequences (`Graph.loops_ncard`). Each bond is compared with a reference bond
   of diamond of the same kind, so diamond's symmetry group is not needed.
3. **The count** (`Main`, `LocalFormula`, `Explicit`). Every site has one
   vertical and three slanted bonds, which gives `loop_equality`. Summing the
   bond recursions over the bonds at a vertex leaves only closed-walk counts
   (`Graph.sum_F_eq`), which gives the local loop formula and, with `W_closed`,
   `loop_count_eq`.
4. **Closed walks** (`ClosedWalks`). On diamond two steps from an even level give
   (1 + gY)(1 + ḡY⁻¹) in ℤ[ℤ²][Y, Y⁻¹]; its n-th power's constant term is
   Σ_a C(n,a)² (gḡ)^a, and the constant term of (gḡ)^a is H(a).
5. **Fibonacci** (`Fibonacci`). The letter at k is h iff ⌊(k+2)α⌋ ≠ ⌊(k+1)α⌋,
   α = (3 − √5)/2; steps follow Jagodzinski's rule. If the stacking had a period
   p, then ⌊(np+2)α⌋ = nc for all n, forcing pα = c and √5 rational.

Computational components: the values for m ≤ 34, the Domb comparison for n < 10,
the Ihara–Bass comparison for m ≤ 12 and the word check for positions < 100 are
kernel evaluations (`decide`, `decide +kernel`). No `native_decide`, no `sorry`
outside `Challenge.lean`; `#print axioms` gives only `propext`,
`Classical.choice` and `Quot.sound` (module `LoopEquality.Axioms`).

## Correspondence with #102

| #102 | Lean (`DictoLoopEquality.`) |
|---|---|
| network of a stacking, loops | `IsStacking`, `diamond`, `Atom`, `IsSite`, `shortVecs`, `Bond`, `nbLoops` |
| Theorem 1 | `loop_equality`, `nbLoops_finite` |
| Theorem 1, "Explicitly", and the table of t_m | `loopCount`, `loop_count_eq`, `loopCount_values`, `loopCount_values_34` |
| Ihara–Bass series | `iharaBass`, `loopCount_eq_iharaBass_small` (m ≤ 12 only) |
| Lemma 2 (a), Proposition | `W_closed`, `closedWalks`, `closedWalks_domb_small` (n < 10 only) |
| Lemma 3 | `Graph.transfer`; summed: `Graph.loops_ncard_eq_FD` |
| Fibonacci stacking (#102 checks) | `fibonacci`, `fibonacci_*`, `isH_eq_word` |

**Not formalised:** the Ihara–Bass series for all m; Bala's identity for all n;
the cut-and-project = substitution identity of the Fibonacci word at every
position (classical, Morse–Hedlund 1940, Lothaire 2002); #102 Corollaries 1–3
and Lemma 2 (c); equality of the vertical and slanted bond walk counts (not
needed).

## Literature and novelty

Known and credited: equal **closed-walk** counts in cubic and hexagonal ice
(Nagle 1966) and in periodic polytypes (Thorpe 1972); equal band structures of
all close-packed stackings through a layer gauge (He–Wilson–Ganesh 2024);
the non-backtracking recursion and the Ihara–Bass formula (Ihara 1966,
Hashimoto 1989, Bass 1992); for periodic stackings, the **site-averaged** loop
counts follow from Thorpe together with the Bass formula for periodic graphs
(Guido–Isola–Lapidus 2008); the Domb numbers (Domb 1960; OEIS A002895, with
Bala's chain form); Sturmian words (Morse–Hedlund 1940; Lothaire 2002).

A literature search (web and arXiv queries on non-backtracking walks, Ihara zeta
functions, walk-regular infinite graphs and polytypes; the 17 works citing
Thorpe 1972, by title; the Palomar database; the author's reference library)
found no earlier statement of the loop equality at every site, or for
aperiodic stackings. It is close to known results, and we claim no more than
this:

* the formal proof of `loop_count_eq` uses only the closed-walk counts
  (`W_closed`, Thorpe's equality extended to all stackings) and the local loop
  formula for (q+1)-regular graphs with equal closed-walk counts, which is a
  short consequence of the Hashimoto–Bass recursion; `loop_equality` follows
  from it;
* a loop of length m at a site sees only a bounded window of layers, and every
  such window occurs in a periodic polytype, so the aperiodic case reduces to
  the periodic one by locality;
* per-vertex and rooted Ihara zeta functions of infinite graphs are studied by
  Grigorchuk–Żuk (2004) and Lenz–Pogorzelski–Schmidt (2019).

What the entry adds is the explicit per-site statement for every close-packed
stacking, the explicit count, and a complete machine-checked proof. The
Fibonacci stacking and its aperiodicity are classical; only the loop statement
on it is new, as an instance of the main theorem. We know of no earlier Lean
formalisation of these statements.

Research context: polytypes and stacking disorder in close-packed materials,
spin ice and the residual entropy of ice polytypes (Isaev–McKay–Zhang 2024;
Xu–Lin–Zhang 2025; Chen–Ran 2026), and zeta functions of infinite and
aperiodic graphs (Clair–Mokhtari-Sharghi 2001; Guido–Isola–Lapidus 2008).

## Build and check

```text
lake exe cache get
lake build
python3 scripts/check-lean-sources.py
./scripts/verify-comparator.sh
```

Toolchain `leanprover/lean4:v4.35.0-rc2`, Mathlib `v4.35.0-rc2`.

Submission, when the author decides: <https://submit.palomar-registry.org/>.

## Licence

Apache-2.0 (`LICENSE`). The cited papers keep their own licences (DICTO's papers:
CC BY-SA 4.0).
