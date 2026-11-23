# Lean: Aristotle's error and the Platonic solids that cannot fill space (24 Nov 2026)

Lean 4 + Mathlib (toolchain and Mathlib pin `v4.35.0-rc2`, as the packets development and the Dehn Canon).
Project on the compute host, `~/lean/platonic-fill`; this folder mirrors its sources (no `.lake`).

## Status box
- Study, not published; no public repository.
- Built clean from scratch on the compute host (logs/build.log; 4 min 20 s wall over a prebuilt Mathlib, peak 3.9 GB; dbb job platonic-fill FINAL ok): 0 `sorry`, axioms only propext, Classical.choice,
  Quot.sound (logs/axioms.log).
- Reuses the packets development unchanged: `Packets/` here is a byte-identical copy of the modules needed from
  the packets Palomar entry (Dehn Canon vendored under `Packets/Canon/`, `Angles`, `Rings`, `Tiling`, `Cones`,
  `Lemma2`, `Pieces`, `Exact`, `Values`, `GenDH`, `GenIH`). New work: `PlatonicFill/`.
- Not done (outside this milestone): the positive half "the cube tiles alone" (a `ConvexTiling` by unit cubes);
  the full Dehn theorem for the five Platonic solids.

## What is proved
Tilings are `ConvexTiling` (packets development): convex polytopes (bounded intersections of finitely many closed
half-spaces) with interior points, covering 3-space, pairwise disjoint interiors, locally finite. **Not
necessarily face-to-face.** A tile is a `SimilarCopy` of a solid: a rigid motion (reflections allowed) of a
positive scaling, each tile at its own scale.

| Lean name | statement |
|---|---|
| `PlatonicFill.aristotle_error` | **no tiling of 3-space by similar copies of the regular tetrahedron** |
| `PlatonicFill.no_tetra` | in a tiling by copies of the regular tetrahedron and convex pieces whose dihedral angles are rational multiples of π (`RationalAngles`, e.g. cubes), no tile is a tetrahedron |
| `PlatonicFill.octa_alone`, `no_octa` | the same for the regular octahedron |
| `PlatonicFill.dodeca_alone`, `no_dodeca` | the same for the regular dodecahedron |
| `PlatonicFill.icosa_alone`, `no_icosa` | the same for the regular icosahedron |
| `PlatonicFill.platonic_mix` | in a tiling by similar copies of the five Platonic solids (and rational-angle pieces), no tile is a dodecahedron or an icosahedron |
| `PlatonicFill.te_edgeAngle` … `ih_edgeAngle` | the dihedral angle of each Platonic solid, read from the set: `arccos(1/3)`, `arccos(−1/3)`, `π/2`, `arccos(−1/√5)`, `arccos(−√5/3)` |
| `PlatonicFill.ring_wt_le`, `tiling_wt_le` | the ring bound with a weight on all four of π, α, β, γ |

Solids from exact coordinates (gen/gen_pieces.py, new cases `te`, `oc`, `cu`; every fact checked in Python and
again by Lean with `decide +kernel` on integer tables, `Packets/Exact.lean`): regular tetrahedron `teSet`, corners
(1,1,1), (1,−1,−1), (−1,1,−1), (−1,−1,1); regular octahedron `ocSet`, corners ±e₁, ±e₂, ±e₃; cube `cuSet`,
corners (±1,±1,±1). Dodecahedron `dhSet` and icosahedron `ihSet` are those of the packets development
(coordinates in Q(√5)).

## Method
Angles are read from the sets (`EdgeAngle`: the share of a small disc across an edge, Dehn Canon). Around an edge
point of any tile, the tiles there have angles adding up to 2π, each a dihedral angle of its tile, π (the point
lies inside a face) or 2π (`lemma2`, packets development; no face-to-face assumption). Every Platonic angle is
q·π + a·α + b·β + c·γ with α = arctan φ, β = arccos(1/√6), γ = arccos √(2/3) (2γ = arccos(1/3)), and π, α, β, γ
are linearly independent over ℚ (`lemma3`, by Niven's theorem, Mathlib `niven`; field argument of the Dehn
Canon's study 8). So the weight q + u·a + v·b + t·c is well defined; when it is nonnegative on every angle that
can occur, every angle in a ring has weight at most 2. Weights used: tetrahedron t = 2 (weight 4), octahedron
t = −1 (3), dodecahedron u = 2 (4), icosahedron v = −1 (7/2); the mixture (u, v, t) = (2, −1, 0) gives 0, 1, 1/2,
4, 7/2 to tetrahedron, octahedron, cube, dodecahedron, icosahedron.

## Files
| file | lines | content |
|---|---|---|
| PlatonicFill/GenTE.lean, GenOC.lean, GenCU.lean | 198, 249, 227 | generated edge data, boundedness, interior point, Gram values |
| PlatonicFill/Solids.lean | 150 | `*_edgeAngle` for the five solids |
| PlatonicFill/Fill.lean | 221 | weight, ring bound, the theorems |
| Packets/ | (copy) | packets development, unchanged |
| gen/gen_pieces.py | | generator (packets version plus cases te, oc, cu) |
| Axioms.lean | | `#print axioms` for the main theorems |

Largest file 1,485 lines (Packets/Canon/Dehn7CubeOct.lean).

## Reference
J. C. Lagarias, C. Zong, "Mysteries in packing regular tetrahedra", Notices AMS 59 (2012) 1540–1549: history of
Aristotle's claim (De Caelo III.8) that regular tetrahedra fill space, and its refutation.

## LEADS
- The cube tiles alone (unit cubes at integer points as a `ConvexTiling`): completes "every Platonic solid except
  the cube fails alone".
- The tetrahedron–octahedron tiling (octet) as the positive answer for mixtures.
- Prior-art check for earlier machine-checked proofs before any public use.
