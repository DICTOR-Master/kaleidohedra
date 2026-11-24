# Paper #118, Theorem 3 (iv) in Lean: three odd edges of one wall — 2026-11-24

**Result (Lean 4 + Mathlib v4.35.0-rc2, built clean; 0 sorry, no `native_decide`, every theorem below depends only on
`[propext, Classical.choice, Quot.sound]`, `logs/axioms.log`).**

`AmberMirror.no_mirror_placement`:

```lean
theorem no_mirror_placement :
    ¬ ∃ x : ℕ → V3, ∀ w ∈ walls, x w.b = mirror w.c0 w.c1 w.c3 (x w.a)
```

There is no choice of points `x c` (one per cell `c`, anywhere in space) such that, for each of 14 walls of the patch,
the point of the cell on one side is the mirror image, in that wall's plane, of the point of the cell on the other side.
The 14 walls are the 4 walls of a tree path from the start cell 33 to cell 0 and the 11 walls round three edges of
wall 3 (cells 0 | 85); wall 1 is in both lists. Since the patch is a set of exact cells and walls, any placement of cores in the whole patch with every
two neighbours mirror images in their shared wall gives such an `x` (its core centres), so this is Theorem 3 (iv) of
paper #118 for the patch, proved from three edges instead of all 597 loops.

The algebraic core and the three conditions, exactly as `odd_edges.py` prints them (s = √5):

| edge (6D lattice points of its two ends) | cells round it | condition on the start cell's point p | Lean |
|---|---|---|---|
| (−2,0,−1,−1,0,−1) – (−1,0,−1,−1,0,−1) | 5: 0, 85, 165, 188, 26 | (−3/4 − s/4) p.x + (1/4 + s/4) p.y − 1/2 p.z = 3/2 + s/2 | `plane1`, `edge1_plane` |
| (−2,0,−1,−1,0,−1) – (−2,0,0,−1,0,−1) | 3: 0, 200, 85 | −2 p.z = 1 + s | `plane2`, `edge2_plane` |
| (−1,0,−1,−1,0,−1) – (−1,0,0,−1,0,−1) | 5: 0, 243, 351, 321, 85 | (−3/4 − s/4) p.x + (1/4 + s/4) p.y + 1/2 p.z = 3/2 + s/2 | `plane3`, `edge3_plane` |

* `plane1_plane3_z`: plane 1 and plane 3 together force p.z = 0 (subtract them; neither alone does).
* `plane2_z`: plane 2 forces p.z = −(1+√5)/2 = −φ.
* `planes_no_common_point : ¬ ∃ p, plane1 p ∧ plane2 p ∧ plane3 p` (the certificate:
  ((s−1)/2)·plane1 + ((1−s)/4)·plane2 + ((1−s)/2)·plane3 gives 1 = 0, using s² = 5).
* `edgeN_plane`: if the points are mirror images across the 4 path walls and the k walls round edge N, then
  the start cell's point lies on planeN.
* `no_mirror_placement` = the three `edgeN_plane` + `planes_no_common_point`.

Also proved: `mirror_mirror` (each reflection is an involution, so the orientation a → b of a wall in `walls` does not
matter: x b = R(x a) iff x a = R(x b)); `wK_flat` (each wall's fourth corner lies on the plane through the other three,
so `mirror` is the reflection in the wall itself); `wK_eq` (each wall's mirror written out as an affine map
u ↦ M u + t with entries in ℚ(√5)).

## From the geometry to the linear equations (why the Lean statement is the paper's claim)

1. **Mirror images ⇒ centres are mirror images.** Paper, Theorem 3 (iii)–(iv): two neighbouring cores must be mirror
   images in their shared wall. A reflection R is an isometry, so if core_b = R(core_a) then centre_b = R(centre_a).
   So any placement in the paper's sense gives points x c (the centres) with x b = R_w(x a) for every wall w = (a | b).
   The Lean statement asks only this of the 14 walls, and lets x c be any point of space (not only inside the cell) and
   ignores the size of the core. So `no_mirror_placement` implies (iv) for the patch: it is the paper's claim, not a weaker one
   (it is stronger: fewer conditions, any points).
2. **The wall's mirror.** The wall with corners c0, c1, c2, c3 (6D lattice points, projected by the rows
   e₀ = (0,1,φ), e₁ = (0,−1,φ), e₂ = (1,φ,0), e₃ = (−1,φ,0), e₄ = (φ,0,1), e₅ = (−φ,0,1) of `tiling.py`) lies in the plane
   through c0 with normal n = (c1 − c0) × (c3 − c0) (`wK_flat`). Its reflection is
   R(u) = u − 2 (n·(u − c0))/(n·n) n = M u + t, M = I − 2 n nᵀ/(n·n), t = 2 (n·c0)/(n·n) n:
   Lean's `mirror`, the same formula as `refl` in `seams_mirror.py` / `odd_edges.py`. Each relation x b = R(x a) is
   three linear equations in the coordinates of x a, x b with coefficients in ℚ(√5) (`wK_eq`, proved from the definition by
   clearing n·n, `mirror_poly`).
3. **Round an edge.** Let cells c1, …, ck surround an interior edge in order, joined by walls W1, …, Wk (all containing the
   edge). The relations give x c1 = Wk ∘ … ∘ W1 (x c1). With x c1 = g(x0), where x0 = x 33 is the start cell's point and g
   is the product of the reflections along the tree path 33 → 273 → 229 → 243 → 0 (the BFS frame of `odd_edges.py`), x0 is
   fixed by the holonomy h = g⁻¹ Wk⋯W1 g = (M, t): (M − I) x0 = −t. For odd k, h is a product of an odd number of reflections
   in planes through the edge, i.e. a reflection; M − I has rank 1 and the three equations are one plane a·x0 = b.
   `odd_edges.py` takes the first non-zero row; these are `plane1..3`, copied verbatim from its log (the generator
   finds each printed row as a combination of the mirror equations; Lean checks that combination).
4. **What Lean proves of step 3.** Lean does not form h; it proves directly that the 3(4 + k) coordinate equations of
   step 2 imply a·x0 = b, by an explicit linear combination with coefficients in ℚ(√5) (`edgeN_plane`). So the plane condition is
   a proved consequence of the mirror relations, which is the direction the impossibility needs. (That the fixed set of h is
   exactly the plane, and not smaller, is not needed and not formalised; the script checks it exactly: h is a reflection,
   rank(M − I) = 1, h fixes both ends of the edge.)
5. **No common point** (`planes_no_common_point`), hence no placement.

## Where the line falls

Formalised: everything from the wall corners (as 6D integer lattice points) to the contradiction: the projection, the
wall planes, the reflections, the mirror relations, their consequences round each edge and through the tree path, and
the inconsistency. Not formalised (data, trusted from the study): that these 12 cells and 14 walls, with these corners, are
cells and walls of the exact patch `data/patch.json` of study 2026-11-21-amber-ammann (export: `gen/export.py`, which runs
`odd_edges.py` unchanged), and that the patch is a piece of every 3D Penrose tiling (cited in the paper). Lean does not
need that the edges are interior or odd, or that the listed walls surround them: the implication holds for whatever walls are
listed; those facts only explain why these walls were chosen (checked exactly in `odd_edges.py`).

## Method

* `gen/export.py` (run with the study's Python environment) runs `odd_edges.py` of the amber-ammann study and writes
  `gen/cert.json`: the three edges of its certificate, the cells and walls round each, the tree path, each wall's two cells and four 6D corners,
  and the three printed planes.
* `gen/make_lean.py` (plain Python, exact fractions) writes `AmberMirror/Data.lean`, `Walls.lean`, `Main.lean`. It proposes
  the matrices and the coefficients of every linear combination (Gaussian elimination over ℚ(√5); residues divided exactly by
  s² − 5). Nothing in it is trusted: each step is checked by Mathlib's `linear_combination` (ring normalisation) with
  `hs : √5 ^ 2 = 5`; non-zero denominators n·n by `linarith` from 2.236 < √5 < 2.237 (`s_lo`, `s_hi`, by `nlinarith`).
* `AmberMirror/Basic.lean`: √5, φ, vectors, `proj`, `mirror`, `mirror_poly`, `mirror_mirror` (hand-written, general).
* Build: `lake build` (about 25 s after Mathlib), `lake env lean Axioms.lean`; logs in `logs/`.

## Sources checked

Paper #118 (`papers/2026-11-22-amber-ammann/paper.html`, Theorem 3 and proof); its audit of 2026-11-24 (items 1, 2);
study 2026-11-21-amber-ammann (`scripts/odd_edges.py`, `seams_mirror.py`, `tiling.py`, `logs/odd_edges.log`);
study 2026-11-24-lean-rolling-law (toolchain and build pattern). Mathlib at this pin: `linear_combination`, `Real.sq_sqrt`,
`field_simp`. The holonomy method (carry a point through walls; consistency iff every loop fixes it) is the standard
flat-connection argument used in `seams_mirror.py`; the odd-edge reduction is from `odd_edges.py`.

## LEADS

1. Formalise the converse of step 4 (fixed set of h = the plane) if the paper's text is to quote it from Lean.
2. Lean check of the data link: that the 14 walls' corners are faces of the listed cells (cells as 6D lattice
   rhombohedra n + span of three eᵢ) — combinatorial, cheap.
3. The paper's next version can cite this certificate (three edges of wall 3) in place of the 597-loop elimination.
