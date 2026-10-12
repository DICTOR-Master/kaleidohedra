# Bodhi seed gap pieces (study, 2026-10-12)

The Bodhi seed (DICTO, discovery #24): a rhombic triacontahedron RT(φ²) holding 12 copies RT(1) on its 5-fold axes (centres
φ² from the middle, touching the outer form and five neighbours each) and RT(1/φ) at the centre. Gap 70.272181 (31.8%).
The question: what are the gap's natural pieces, the analogues of the Lotus seed's AXE, FUJI and CLEO? We wanted convex pieces,
the whole decomposition invariant under the full icosahedral group (order 120), and as few congruence classes as possible.
Labels B1–B5 are neutral; naming is left to DICTO.

## Result in one paragraph
The gap splits exactly into **three convex piece types: 60 B1 (inner pocket) + 60 B2 + 60 B3 (outer pocket), 180 pieces**
("kit A"). Every corner is exact in Q(φ), and every dihedral angle is a multiple of 6° (36°, 60°, 72°, 90°, 108°, 120°, 144°).
Each piece has a mirror symmetry (stabiliser of order 2). A second exact kit with three types
also exists: **60 B1 + 20 B4 + 120 B5 (200 pieces, "kit B")**. B4 is a 3-fold piece sitting in each outer 3-fold corner, as
FUJI does in the Lotus seed. The inner pocket's volume equals RT(1) for an exact reason. The 12 copies enclose exactly a **rhombic
hexecontahedron RH(1)** (20 prolate golden rhombohedra of edge 1, one per 3-fold axis). Its volume is 20P, and
20P = RT(1) + RT(1/φ), so cavity − centre = RT(1). This is an identity, not a coincidence.

## The geometry in block coordinates (why the pieces are so simple)
All solids here are golden zonotopes: every face normal is one of the 15 two-fold axes. So separating-axis tests on those 15 axes
are exact (`scripts/bodhi_core.py`). Take an icosahedron face with 5-fold unit vectors e_a, e_b, e_c. Write
x = s e_a + t e_b + u e_c. Then the RH(1) block on that face is the unit cube 0 ≤ s, t, u ≤ 1, and one fundamental cone (chamber)
of the full group is s ≥ t ≥ u ≥ 0. In these coordinates (derived, then checked numerically):

| solid, inside the 3-fold sector | inequalities |
|---|---|
| centre RT(1/φ) | s + t + u/φ ≤ 1 (and its two permutations) |
| outer RT(φ²) | s + t + u/φ ≤ φ³ (and permutations) |
| copy on e_a, inside the chamber | s ≥ 1, t + u/φ ≤ φ, s/φ + t + u ≤ 2φ, s + t + u/φ ≤ φ³ |

The other copies do not enter the chamber's interior. So per chamber:
- **inner pocket** = {1 ≥ s ≥ t ≥ u ≥ 0, s + t + u/φ ≥ 1}, a single convex cell;
- **outer pocket** = {s ≥ 1, s ≥ t ≥ u ≥ 0, s + t + u/φ ≤ φ³} minus the copy, i.e. that region ∩ ({t + u/φ ≥ φ} ∪ {s/φ + t + u ≥ 2φ}),
  which is two convex cells, split one of two ways (by either copy face first).

Over the 120 chambers this gives 120 inner cells and 240 outer cells. They are checked to lie inside RT(φ²) and outside all 13
solids, with total volume 70.272181080 = gap. That makes them an exact cover. The bodhi_bsp.py run in the earlier study cut the
same region much finer: 74 cells per chamber, because it used every face plane of every solid.

## Search for the coarsest decomposition (`scripts/pieces.py`)
1. Take all 120 images of the chamber cells.
2. List every convex union of cells, built by repeated pairwise merging and checked by union volume = hull volume to 1e-8. This
   includes unions that cross chamber walls.
3. Group the unions into orbits under the 120 symmetries.
4. Solve an exact-cover MILP over the orbits. It minimises 1000 × (number of congruence types) + (number of pieces).

| pocket, split | cells | convex unions | orbits | optimum |
|---|---|---|---|---|
| inner | 120 | 180 (sizes 1, 2) | 2 | **60 B1**, 1 type (`logs/pieces-inner.log`) |
| outer, copy face t + u/φ = φ first | 240 | 360 (sizes 1, 2) | 4 | **60 B2 + 60 B3**, 2 types, 120 pieces (`logs/pieces-outer.log`) |
| outer, copy face s/φ + t + u = 2φ first | 240 | 500 (sizes 1, 2, 3, 6) | 6 | **20 B4 + 120 B5**, 2 types, 140 pieces (`logs/pieces-outer-H2FIRST.log`) |
| outer, both copy faces + copy b's face s/φ + u = φ | 360 | 660 | 7 | same as the first split (B2 + B3) (`logs/pieces-outer-H3.log`) |

In every case the fewest pieces regardless of types gives the same answer.

## The pieces (exact; `logs/verify_kit_A.log`, `logs/verify_kit_B.log`, data in `data/`)
Volumes are in units of the oblate golden rhombohedron of edge 1, O = √(10 − 2√5)/5 = 0.470228202. The prolate one is
P = φ O = 0.760845213. Corner coordinates (s, t, u) are given in the block basis above (e_a, e_b, e_c = `blockBasis` in the JSON).
Edge-length values: 1.051462 = √(2 − 2/√5) (two 5-fold unit vectors apart); 1.473370 = RT(1)'s 3-fold corner radius;
1.701302 = √(2 + 2/√5); 0.910593 = √(9/5 − 3φ/5); 0.618034 = 1/φ; 1.618034 = φ; 1.236068 = 2/φ; 0.562777 = √(21/5 − 12φ/5);
0.649839 = √(28/5 − 16φ/5).

### B1 (inner pocket) × 60, volume φ²/6 · O = RT(1)/60 = 0.205178902
- **Shape:** triangular bipyramid (5 corners, 9 edges, 6 triangular faces).
- **Corners:** (1,1,0) on a 2-fold axis; (1,1,1), the RH(1) 3-fold point; (1,0,0) and (0,1,0), the centre's 5-fold corners;
  (2−φ)(1,1,1), the centre's 3-fold corner.
- **Faces:** the middle triangle is (1,1,1), (1,0,0), (0,1,0), sides 1.7013, 1.7013, 1.0515. The two apices are (1,1,0) and
  (2−φ)(1,1,1). Two faces lie on copies: these are halves of RH faces, triangles 1, 1, 1.7013. One face lies on the centre:
  triangle 0.618, 0.618, 1.0515.
- **Edges:** 1 (×3), 1/φ (×2), 1.0515, 1.4734, 1.7013 (×2).
- **Dihedral angles:** 72°, 90°, 108°, 120°.
- **Where it sits:** each RH(1) block minus the centre is 3 B1. That union is not convex (hull 0.634 vs 0.616,
  `logs/inner_pocket.log`), so no single 3-fold inner piece exists.

### B2 (outer pocket, kit A) × 60, volume (3 + 5φ)/6 · O = 0.869151778
- **Shape:** 7 corners, 11 edges, 6 faces.
- **Corners:** (1+φ,1,1), (φ,φ,φ) (the outer 3-fold corner), (1,1,1), (1+φ,φ,0), (1,1+φ,1), (φ,1+φ,0), (φ,φ,0).
- **Faces:** one pentagon on the outer RT(φ²) (sides 0.9106, 1, 1, 0.9106, 1.0515; area φ); two quadrilaterals on two copies
  (0.9106, 1, 1, φ; area 1.1708); three cut triangles.
- **Edges:** 1 (×5), φ (×2), 0.9106 (×2), 1.0515, 1.4734.
- **Dihedral angles:** 60°, 72°, 90°, 108°, 120°.

### B3 (outer pocket, kit A) × 60, volume (φ − 1)/3 · O = O/(3φ) = 0.096872337
- **Shape:** a pyramid on a golden rhombus (the RT face, edge 1), lying flat on a copy's face.
- **Corners:** apex (1+φ,1,1) on the outer surface; base (2φ, φ−1, φ−1), (1+φ, φ, 0), (2,1,1), (1+φ, 0, φ).
- **Faces:** two triangles on the outer RT(φ²), two cut triangles; all four are 0.618, 0.9106, 1.
- **Dihedral angles:** 36°, 120°, 144°.

### B4 (outer pocket, kit B) × 20, volume (7φ − 3)/2 · O = 1.957615943
- **Shape:** a 3-fold piece in each outer 3-fold corner, with 3-fold rotation and mirror symmetry (stabiliser order 6).
  14 corners, 21 edges, 9 faces.
- **Faces:** three pentagons on the outer RT(φ²) (area 2.1708) meeting at the corner (φ,φ,φ); three hexagons, one on each of the
  three copies round that axis (area 2.1305); three small cut triangles (0.5628, 0.5628, 1.0515).
- **Dihedral angles:** 36°, 90°, 120°, 144°.

### B5 (outer pocket, kit B) × 120, volume O/3 = 0.156742734
- **Shape:** 6 corners, 9 edges, 5 faces: a wedge whose rhombus face (edge 1) lies on a copy.
- **Corners:** (1+φ, φ, 0), (2,2,0), (φ,φ,0), (2,1,1), (2φ−2)(1,1,1), (1,1,1).
- **Chirality:** it has no mirror symmetry, so kit B uses 60 left-handed and 60 right-handed B5
  (`logs/render.log`, exhaustive check).
- **Dihedral angles:** 36°, 60°, 90°, 108°.

### Volume bookkeeping (exact)
- Gap = 80P + 20O = 70.272181080.
- Inner pocket = 60 × B1 = 10P + 10O = RT(1).
- Outer pocket = 70P + 10O:
  - kit A: 60 × (3+5φ)/6 + 60 × (φ−1)/3 = 10 + 70φ (in units of O);
  - kit B: 20 × (7φ−3)/2 + 120 × 1/3 = 10 + 70φ.

### Checks (both kits)
- Every piece is convex, lies inside RT(φ²), and is clear of all 12 copies and the centre. Pieces were tested pairwise by
  separating axes using all face normals and edge-pair cross products; there are 0 overlapping pairs among the 180 (kit A) and
  200 (kit B) pieces.
- Total piece volume = gap to 6e-14. Together with the clearance and containment checks, this makes the pieces plus the 13 solids
  an exact filling of RT(φ²): 220.907160976 both ways.
- Sampled cover: 236,269 random points in RT(φ²) each lie in exactly one solid or piece (0 in none, 0 in two).
- All copies of a type are congruent: equal corner count and volume, and all pairwise distances agree to 1e-7.
- The kit is invariant under all 120 symmetries.
- Every corner's block coordinates are exact elements of Q(φ) and reproduce the float corners to 1e-9.

## Why the inner pocket equals one RT(1) (exact)
`scripts/inner_pocket.py`, `logs/inner_pocket.log`.
- The 20 golden rhombohedra of RH(1) lie in the gap's closure. They are clear of all 12 copies, inside the outer form, and do not
  overlap each other.
- Every inner-pocket cell, and the centre, lies in the RH(1) block of its chamber. Their volumes add to exactly 20P. So the cavity
  the 12 copies enclose is exactly RH(1): its 60 rhombic faces lie on the copies' faces.
- Each RH(1) block's faces lie either through the middle or at distance 0.850650808 from it, which equals the inradius of
  RT(1/φ). So the far faces of the blocks (the ones on the copies) are coplanar with the centre's faces. This is why the
  copies, the centre and RH(1) share so few planes.
- Volumes, with P = φO, RT(1) = 10P + 10O = 10φ²O and RT(1/φ) = RT(1)/φ³ = 10O/φ:
  **inner pocket = RH(1) − RT(1/φ) = 20φ O − 10 O/φ = 10 O (2φ − 1/φ) = 10 φ² O = RT(1)**, because 2φ − 1/φ = φ + 1 = φ².
  Equivalently, RH(1) = RT(1) + RT(1/φ) by volume. RH(1) is the classical rhombic hexecontahedron (20 prolate rhombohedra);
  that the copies close exactly on it is what this study adds.

## What was tried and what did not work
- **Earlier study** (`../2026-10-12-network-versions`):
  - grouping the BSP cells by nearest axis gives non-convex parts;
  - golden rhombohedra of edge 1 and 1/φ do not tile the gap (MILP infeasible).
- **Block minus centre as one 3-fold inner piece:** not convex, so ruled out.
- **Extra cut plane in the outer pocket** (copy b's face): no gain; the optimum is still B2 + B3.

## Open questions
- **Global minimality.** The search is exact and complete only over pieces that are unions of the chamber cells, i.e. pieces cut
  by the 15 mirror planes and the solids' own face planes. Within that space, 3 types is the minimum. At least 2 types are always
  needed, since the two pockets are disjoint. Whether a decomposition with arbitrary cut planes could fill the outer pocket with a
  single convex type is not proved either way.
- **Which kit is "natural".** Kit A has fewer pieces (180) and every piece has a mirror symmetry. Kit B has a FUJI-like 3-fold piece
  (B4, 20) but needs a chiral pair (B5). DICTO's choice.
- **Links to the Lotus kit.** AXE, FUJI and CLEO have edges 1 and 1/φ with 3- and 6-sided faces. B1–B5 use golden rhombus,
  pentagon and hexagon faces. No direct dissection relation was tested.

## Files
- `scripts/bodhi_core.py`: shared geometry, the group, exact separating-axis tests, the descriptor.
- `scripts/inner_pocket.py`: the RH(1) cavity proof.
- `scripts/pieces.py`: chamber cells, convex-union enumeration and MILP. Run with `inner` / `outer`, plus env `EXTRA=H2FIRST|H3`.
- `scripts/verify_kit.py A|B`: independent checks, exact corners, JSON output.
- `scripts/render.py`: renders and the chirality check.
- `data/bodhi-B*-raw.json`: corners (seed frame, RT edge 1), exact block coordinates, faces, dihedral angles, all copies, checks.
  `data/bodhi-B*-unit.json`: the same piece scaled to shortest edge 1.
- `data/bodhi-kit-{A,B}-all-pieces.json`: every piece of each kit. `data/bodhi-seed-solids.json`: the 14 solids.
  `data/pieces-*.pkl`: MILP output.
- `renders/`: piece-types, inner-cavity, kit-A, kit-B (assembled cut-away + exploded), outer-pocket-3fold.
- Heavy runs were done on dicto-node (`~/bodhi`).
