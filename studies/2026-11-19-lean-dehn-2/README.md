# Lean study 2 of the shape-language canon: Dehn's theorem, layer (b), the bridge (19 November 2026)

**Question (DICTO's canon, continued from study 1):** study 1 proved the arithmetic of the Dehn invariant on edge lists given as data. Does cutting a solid into pieces and moving the pieces rigidly keep the Dehn invariant? Prove it in Lean for convex polytopes in 3-space, from a definition of the invariant that uses the solid alone.

**Result:** proved. Eight Lean files (1,661 lines) compile with Lean v4.35.0-rc2 and the pinned Mathlib: no errors, no warnings, no `sorry`; every main theorem uses only the three standard axioms (`lean/compile.log`). The one file with `sorry` is `lean/DehnCanon2Gaps.lean`; it holds what remains, which is the evaluation of the invariant on concrete solids, not the bridge.

## The definition (file `Dehn2Local.lean`)
- A convex polytope (`IsPoly`, file `Dehn2Poly.lean`) is a bounded intersection of finitely many closed half-spaces.
- `tcone P x`: the directions that stay in `P` near the point `x`. `linSpace`: the span of the directions `v` with `v` and `-v` both in the cone. The point `x` is an edge point when that span is a line `K`.
- `wedgeAngle T K`: the angle of the cone around the line, measured as 2π × (area of the cone inside the unit disc of the plane perpendicular to `K`) / (area of that disc).
- `edgeAngle P x`: that angle modulo rational multiples of π at an edge point, 0 at every other point.
- `dehnSet P = Σ over angle classes θ of (1-dimensional Hausdorff measure of {x : edgeAngle P x = θ}) ⊗ θ`, in ℝ ⊗[ℚ] (ℝ/ℚπ), the space of study 1. No list of edges is given as input.

## Proved in Lean (theorem names, statements)
1. `wedgeAngle_split`: a plane through the edge line cuts the cone in two; the two angles add up to the angle of the cone, exactly.
2. `wedgeAngle_mem_ratPi_of_line`: a cone that contains a whole line of the perpendicular plane has angle 0, π or 2π. (A new edge made by a cut on a face or inside the solid: its two angles sum to π or 2π, zero in ℝ/ℚπ.)
3. `dehnSet_cut` (the core lemma, `Dehn2Cut.lean`): for every convex polytope `P` in 3-space and every plane, `dehnSet P = dehnSet (P ∩ one side) + dehnSet (P ∩ other side)`. No condition on the plane; an edge that crosses the plane is cut at a single point, of length zero (`exc_null`).
4. `dehnSet_image` (`Dehn2Motion.lean`): `dehnSet` is unchanged by every isometry of the space (rotations, translations, reflections). `IsPoly.image`: the image of a convex polytope is a convex polytope.
5. `dissection_additive` (`Dehn2Poly.lean`, the refinement argument, in any finite dimension and for any group-valued set function): additive under every single plane cut of a convex polytope ⇒ additive over every dissection of a convex polytope into finitely many convex polytopes (pieces cover it, interiors pairwise disjoint). The proof cuts along all the facet planes of the pieces. `flat_of_cut`: such a function is zero on polytopes with empty interior.
6. `dehnSet_dissection` (`DehnCanon2.lean`): `dehnSet P = Σ dehnSet (p k)` for every such dissection.
7. `dehnSet_eq_of_scissorsCongruent` (**the bridge**), `dehn_bridge_R3` (the same in coordinate ℝ³): scissors-congruent convex polytopes have the same Dehn invariant. `ScissorsCongruent P Q`: `P` is cut into finitely many convex polytopes with pairwise disjoint interiors, each piece is moved by an isometry, and the moved pieces fill `Q` with pairwise disjoint interiors.
8. `dehnSum_eq_of_same_union`, `dehnSum_eq_of_scissors`: for polyhedra that need not be convex (finite unions of convex polytopes with disjoint interiors), the total `Σ dehnSet (pieces)` does not depend on the dissection and is the same for scissors-congruent polyhedra.
9. `dehnSet_eq_dehn_edgeList` (`Dehn2Edges.lean`, the link to study 1): for a bounded polytope given by half-spaces, `dehnSet` equals study 1's `dehn` of an explicit edge list: one entry per set `A` of constraints whose common direction space is a line, with length = Hausdorff length of the points where exactly the constraints in `A` are tight, and angle = `wedgeAngle` of the cone of those constraints.
10. `isPoly_tetra`, `isPoly_cube` (`Dehn2R3.lean`): the regular tetrahedron with corners (−1,−1,−1), (1,1,−1), (1,−1,1), (−1,1,1) and the cubes [−s,s]³ are convex polytopes in this sense.
11. Optional `Dehn2Hull.lean`: `isPoly_iff_convexHull`, `dehn_bridge_convexHull`: the polytopes of this study are exactly the convex hulls of finite point sets in ℝ³, so the bridge holds for those. This borrows the Minkowski–Weyl theorem `Chapter10.isConvexPolytope_iff` of FormalBook (credited in the file at the point of use); the FormalBook file is not copied here.

## Not proved: what remains (all in `lean/DehnCanon2Gaps.lean`, each a stated theorem with `sorry`)
The bridge for convex polytopes has no gap. What is missing is the evaluation of `dehnSet` on concrete solids; until then the Lean files do not show that `dehnSet` is nonzero on any solid.
- Gap 1, `wedgeAngle_two_planes`: for two half-spaces with outward normals a₁, a₂ (not parallel), `wedgeAngle = π − angle(a₁, a₂)`. (The area of a disc sector is half its angle; Mathlib has polar coordinates but no sector area: grep of the pinned copy.)
- Gap 2, `dehnSet_cube`: `dehnSet (cubeSet s) = 0` for s > 0.
- Gap 3, `dehnSet_tetra`: `dehnSet tetraSet = dehn (tetrahedron (2√2))` (study 1's value: six edges of length 2√2 at arccos(1/3)).
- `tetra_not_scissorsCongruent_cube`: the regular tetrahedron is not scissors congruent to any cube. Its proof is written and compiles, but it rests on gaps 2 and 3 (plus this study's bridge and study 1's Niven step).

Limits of what is stated: dimension 3; pieces are convex polytopes; the solids `P`, `Q` in item 7 are convex (item 8 covers unions); isometries include reflections.

## Decision on reuse of FormalBook
Fetched FormalBook/Chapter_10.lean (2,345 lines) at merge commit 54da1ce and compiled it on our toolchain (v4.35.0-rc2; it was written for rc3): it compiles unchanged, 8 s. Its Hilbert's-third-problem theorem lives in an abstract segment-and-angle model; its geometric part defines faces, congruence, decompositions and proves Minkowski–Weyl, but has no Dehn invariant of a polytope, no plane-cut lemma and no bridge (as its description says). Nothing in it shortens the bridge, so parts A–G are independent of it. Only the optional part H borrows its Minkowski–Weyl theorem.

## Prior art (checked)
- FormalBook PR #157 (github mo271/FormalBook, merged 6 Oct 2026): as above; file read and compiled.
- Mathlib (pinned copy, grep for "Dehn invariant", "scissors", "equidecompos"): only `Algebra/Group/Action/Equidecomp.lean`, equidecomposability of sets under a group action (the Banach–Tarski setting), no polytopes, no Dehn invariant.
- Web searches (19 Nov 2026) for a Lean, Isabelle, Coq or HOL Light proof of the Dehn invariant's additivity or of the geometric bridge: none found; results were mathematical sources only (arxiv math/9712226, arxiv 1910.07112, arxiv 2502.03380, Encyclopedia of Mathematics "Dehn invariant", Wikipedia "Dehn invariant" and "Hilbert's third problem").
- A machine-checked proof that scissors-congruent convex polytopes have equal Dehn invariant, from a geometric definition: not found in the sources checked.
- Mathematics: Dehn (1901); Jessen's tensor form; the plane-cut and common-refinement argument is the textbook one.

## `#print axioms` (from `lean/compile.log`)
```
'DehnCanon.dissection_additive' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.wedgeAngle_split' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.wedgeAngle_mem_ratPi_of_line' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.dehnSet_cut' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.dehnSet_image' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.dehnSet_dissection' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.dehnSet_eq_of_scissorsCongruent' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.dehnSum_eq_of_same_union' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.dehnSum_eq_of_scissors' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.dehnSet_eq_dehn_edgeList' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.dehn_bridge_R3' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.isPoly_tetra' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.isPoly_cube' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.isPoly_iff_convexHull' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.dehn_bridge_convexHull' depends on axioms: [propext, Classical.choice, Quot.sound]
```
No `native_decide`, no added axioms.

## Files and how to compile
`lean/`: `Dehn2Poly` (A, polytopes and refinement), `Dehn2Local` (B, the definition and the angle lemmas), `Dehn2Sum` (C, sums of finitely-valued angle functions), `Dehn2Cut` (D, the core lemma), `Dehn2Motion` (E), `DehnCanon2` (main theorems), `Dehn2Edges` (F, link to study 1), `Dehn2R3` (G), `Dehn2Hull` (H, optional), `DehnCanon2Gaps` (the gaps), `Axioms2`, `compile.log`.
Compiled on the compute host in the Lean workspace of study 1, in the folder `DehnCanon/` beside `DehnCanon1.lean`, each file in the order above with
`lake env lean -o .lake/build/lib/lean/DehnCanon/<File>.olean DehnCanon/<File>.lean` (3 to 5 s each). Part H also needs FormalBook's `Chapter_10.lean` (commit 54da1ce) placed as `FormalBook/Chapter_10.lean` and compiled the same way.

## Leads
- Study 3, the evaluation layer: sector area (gap 1) from Mathlib's polar coordinates; then cube and tetrahedron (gaps 2, 3) through `dehnSet_eq_dehn_edgeList`; that closes Dehn's theorem end to end with no `sorry`.
- A short route to gap 2 without sector areas: a quadrant is half of a half-plane by a reflection (`wedgeAngleIn_image`), so its angle is rational in π.
- Then our words (AXE, CLEO, FUJI: two independent angles, beyond Niven), as planned in study 1.
