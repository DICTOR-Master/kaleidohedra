# Euclid–Kepler–Pacioli (EKP) cell by DICTO: two variations, symmetry and overlap

*Statement for the Zenodo record, by DICTO. Draft dated 2026-10-07; not released.*

## Summary

The EKP cell (DISCOVERIES.md #8) fills a cubic lattice of cubes with the same seven pieces in every cube: the cube, the regular dodecahedron, the regular icosahedron, the great stellated dodecahedron (the star), the octahedron, the stella octangula and three Pacioli golden rectangles (planar, so they have no volume).

This record defines two variations and gives their exact symmetry and overlap:

- **A, identical cells.** Every cube is the same and unturned. This is the cell as first recorded (DISCOVERIES #8). In the app it is the Euclid–Kepler–Pacioli Cell Network world, with the turn off.
- **B, checkerboard turn.** Odd cubes (i + j + k odd) are turned 90° about the z axis, with all their pieces. In the app it is the Turn odd cubes option of the Euclid–Kepler–Pacioli Cell Network world, switched on for this variation.

Both variations are kept; neither replaces the other. The EKP network (DISCOVERIES #8b), which puts stars on even cubes and icosahedra on odd cubes, is included for comparison.

The repeat rule of DISCOVERIES #8 is that the cell repeats by translations of 2 along x, y and z (`ROOF_FOLD_PERIOD = 2`). Variation A keeps that rule. Variation B does not: its odd cubes are rotated copies, so a one-cube translation swaps even and odd cubes. Within each cube the roof rules still hold in both variations: roofs on the cube, then reflection through its six faces. The turn rotates each odd cube as a whole, so the construction inside it is unchanged, only turned. Between cubes, B breaks the roof node rule of DISCOVERIES #8: no roof vertex of a cube meets an icosahedron vertex of a neighbour (section 5). B also has two cube orientations where DISCOVERIES #8 has one.

## Definitions

- Cube (i, j, k) has its centre at 2(i, j, k) and edge 2, in the units of `src/geometry-extensions/roof-fold.js`. One lattice step is one cube.
- Even cubes have i + j + k even; odd cubes have it odd.
- Variation A: each cube holds the seven pieces, unturned.
- Variation B: as A, but each odd cube is rotated 90° about z together with its pieces.
- Placement: the app places any of the seven pieces in any cube. Section 4 gives the exact fit for chosen pairs.

## 1. Symmetry

Each operation is a cube symmetry (signed permutation) with a cube translation, checked against the full contents of a 5 × 5 × 5 window of cubes. Counts are per 2 × 2 × 2 supercell.

| | A identical | Network (#8b) | B checkerboard |
|---|---|---|---|
| Operations | 192 | 96 | 192 |
| Point operations | 24 (m-3) | 24 (m-3) | 48 (m-3m) |
| Translation lattice | primitive (all cube vectors) | face-centred | face-centred |
| Operations exchanging even and odd cubes | 96 | 0 | 96 |
| Space group | Pm-3 (No. 200) | Fm-3 (No. 202) | Fm-3c (No. 226) |
| Symmorphic | yes | yes | no |

- Space groups come from the reflections of the operation set (determinant −1, trace 1), classed by glide type (`scripts/ekp-v2/space-group.mjs`). In A and in the network, the mirrors perpendicular to the cube axes are pure mirrors. In B those mirrors remain, and the reflections perpendicular to face diagonals are c-glides and diagonal glides, with no pure mirror.
- Repeat rule: A repeats by one cube along each axis. B and the network (#8b) do not: their translations are the face-centred ones only, so a one-cube translation is not a symmetry of either.
- B is not symmorphic. The operation R90·diag(−1, 1, 1) exchanges even and odd cubes, so every one of its translations has odd cube-sum. Moving the origin by s changes the translation by (I − O)s = (s_x + s_y, s_x + s_y, 0), which has even cube-sum. No origin makes all translations lattice vectors.
- In B the 96 exchanging operations are exactly the 90° rotation composed with the 24 pyritohedral operations.
- Under the quarter turn R90, the octahedron and the stella octangula are each mapped onto themselves (48 operations each). For the dodecahedron, icosahedron, great star and Pacioli rectangles, the original and the rotated copy share 24 operations. The 24 operations common to all six solids are unchanged by the turn.

## 2. Overlap per lattice cube (exact; volume 8)

| Pair | A | B |
|---|---|---|
| dodecahedron–dodecahedron | 6.4721 | 6.4721 |
| dodecahedron–cube | 3.2361 | 3.2361 |
| dodecahedron–stella octangula | 1.2361 | 1.2361 |
| dodecahedron–great star | 0.6950 | 0.8053 |
| dodecahedron–octahedron | 0.2918 | 0.2918 |
| dodecahedron–icosahedron | 0.1115 | 0.1305 |
| cube–great star | 0.1115 | 0.1115 |
| great star–great star | 0.2229 | 0.0077 |
| all other pairs | 0 | 0 |
| **Total** | **18.0588** (225.7% of cube volume) | **18.1021** (226.3%) |

- Per face contact: A 6.01961, B 6.03403, equal on all six faces in each variation.
- Edge neighbours (12) and corner neighbours (8) of each cube give zero overlap for every pair, in both variations. At the corners the pieces meet at most at a point: each large piece reaches circumradius √3 in the cube-corner directions, and corner neighbours sit at distance 2√3.
- Cubes two steps away are at least 4 apart, beyond 2√3 ≈ 3.46, so all overlap lies within the first shell.

## 3. Merged outer surface (3 × 3 × 3 cubes; app function `mergedDodecaSurface`)

| | A | B |
|---|---|---|
| Faces | 731 | 1945 |
| Winding or normal mismatches / faces not outward | 0 / 0 | 0 / 0 |
| Closure difference (two reference points) | 6.8 × 10⁻¹³ | 3.4 × 10⁻¹³ |
| Enclosed volume (exact, from the surface) | 274.249 | 274.249 |
| Monte Carlo estimate of the union | 272.79 ± 0.89 | 274.07 ± 0.89 |

The enclosed volume is the same to the printed precision in both variations. The Monte Carlo estimates agree with it within about two standard errors.

## 4. Alternating pieces (variation B)

A cube holds one piece in a given placement. Two pieces placed on even and odd cubes are checked exactly for every neighbour direction (6 faces, 8 corners, 12 edges):

| Even cube | Odd cube | Face | Corner | Edge |
|---|---|---|---|---|
| great star | icosahedron | 0 | 0 | 0 |
| dodecahedron | icosahedron | 0.0435 | 0 | 0 |
| stella octangula | dodecahedron | 0.412 | 0 | 0 |

So the great star and the icosahedron fit exactly when alternated. The stella octangula and the dodecahedron do not fit across faces.

## 5. Roof rules (DISCOVERIES #8)

DISCOVERIES #8 records that every roof vertex of a cube is an icosahedron vertex of a neighbouring cube. A cube has 12 roof vertices (the dodecahedron's vertices outside the cube). Counting those that coincide with an icosahedron vertex of one of the 26 neighbouring cubes:

| Cube | A identical | B checkerboard |
|---|---|---|
| even (0, 0, 0) | 12 of 12 | 0 of 12 |
| odd (1, 0, 0) | 12 of 12 | 0 of 12 |

Every even cube is a translate of (0, 0, 0) and every odd cube of (1, 0, 0), so these two cases cover all cubes. Variation B therefore has no roof node shared with a neighbour. Section 2 gives its overlaps. The construction inside each cube (roofs on the cube, reflection through its faces) holds in both variations. DISCOVERIES #8 also says every cube repeats one orientation; B has two. Script: `scripts/ekp-v2/roof-nodes.mjs`, output `RESULTS-roof-nodes.txt`.

## 6. Checks on the method

- Overlaps are exact convex intersections: each boundary face of one piece is clipped against the other. The face totals printed by the script agree in all six directions in each variation.
- Monte Carlo: the great star with the great star across a face (+y), exact 0.07430 against Monte Carlo 0.07446 ± 0.00022 (2 × 10⁷ samples).
- The two tetrahedra of the stella octangula intersect in the octahedron (volume 4/3, checked).
- Corrections since the first draft: (1) an earlier hull-based intersection depended on point order for pairs of star spikes. The identical-cell great star–great star term was 0.2018 and is now 0.2229, so the variation A total moves from 18.0377 to 18.0588. Variation B (18.1021) is unchanged. (2) The earlier glide note counted improper operations too; the classification in section 1 counts only reflections. (3) A two-origin symmorphic test is replaced by the argument in section 1.

## 7. Limits

- The pieces overlap by design. The arrangement is not a tiling; the totals measure the overlap and say nothing about physical assembly.
- Space-group symbols are derived from the glide classification above. They have not yet been compared with the printed International Tables.
- Monte Carlo values are estimates with stated standard errors; repeated runs vary within those errors.

## 8. Reproduce

From the repository root:

```
node scripts/ekp-v2/symmetry-compare.mjs      # operations (writes ops.json)
node scripts/ekp-v2/space-group.mjs           # space-group symbols
node scripts/ekp-v2/symmetry-seven.mjs        # per-solid symmetry under the quarter turn
node scripts/ekp-v2/content-symmetry.mjs      # shared subgroup
node scripts/ekp-v2/contents-totals.mjs       # overlap per lattice cube, variation B
node scripts/ekp-v2/contents-totals.mjs --unturned --mc   # variation A, corners, Monte Carlo pair check
node scripts/ekp-v2/alternate-fit.mjs         # alternating pieces
node scripts/ekp-v2/merged-orientation.mjs    # merged outer surface
node scripts/ekp-v2/roof-nodes.mjs            # roof vertices on neighbouring icosahedra
```

Outputs are in `scripts/ekp-v2/RESULTS-*.txt`.

## 9. Context

- Variation A: DISCOVERIES.md #8 (cell) and #8b (network). The v2026.10.07 release, DOI 10.5281/zenodo.23197596, already archives variation A.
- Concept DOI of the Kaleidohedra record: 10.5281/zenodo.23173809.
- Source: github.com/DICTOR-Master/kaleidohedra (MIT licence).
- Credit: DICTO.

## Suggested Zenodo fields (not released)

- **Title:** Euclid–Kepler–Pacioli (EKP) cell by DICTO: two variations, symmetry and overlap
- **Creator:** DICTO
- **Version:** v2026.10.07-alt2 (proposed; to be decided)
- **Licence:** MIT, as the repository. To confirm: whether the text should carry CC BY 4.0 instead.
- **Keywords:** Euclid–Kepler–Pacioli cell; icosahedral symmetry; space filling; space group Fm-3c; stellated dodecahedron; stella octangula
- **Related identifiers:** 10.5281/zenodo.23173809 (concept); 10.5281/zenodo.23197596 (v2026.10.07, variation A)
- **Description:** Two variations of the Euclid–Kepler–Pacioli cell, each cube holding the same seven pieces. Variation A (identical cells, space group Pm-3) and variation B (odd cubes turned 90°, space group Fm-3c, not symmorphic) are both kept. Variation B does not repeat by translation alone and breaks the roof node rule between cubes; each cube still follows the roof rules. Exact symmetry and per-cube overlaps, the closed merged outer surface and the alternating-piece fits are given with scripts that reproduce every number.
