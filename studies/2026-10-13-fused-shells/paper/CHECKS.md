# CHECKS: what was verified, and how (2026-10-13)

DICTO · dictospheres.com

## Inputs
- Six fused solids: `src/krp-core/src/polyhedra/transitional.js`. These are Polyhedraverse's "DICTO Transitional Shells". When generated, each was checked for simple faces and for volume equal to the fused pieces' volume.
- Seven more fused stages, made with the same functions (`analysis/fuse_extra.py`, run on dicto-node): `analysis/data/fused-extra.json`. Every one has fused volume equal to its pieces' volume, except Dharma stage 5 (11.922 against 12.462), which is not used in the paper.
- Pieces: `../pieces.json`. Stage facts: `../steps.json`, `../stages.json`, `../partials.json`, `../renders/index.json`. The counts 107/5,569, 7/124 and 10/363 were taken from these files, not recomputed.

## Identifications (`analysis/identify.py`, 25 PASS, 0 FAIL, `analysis/identify.log`)
Tolerance 1e-4 throughout (coordinates are stored to 5–6 decimals). Each reference solid was built from first principles; only the size and orientation of the stage's core come from the data.

| Claim | How checked | Worst error |
|---|---|---|
| Lotus 2 = great stellated dodecahedron (solid) | GSD built from the core icosahedron: 12 planes aᵢ·x = r/√5, points where three planes meet on 3-fold axes. Checked: point positions, inner corners, all 60 faces on the 12 planes, face set identical (60/60), golden triangles (ratio φ), regular pentagram in each plane (radius ratio φ²), circumradius by the Kepler–Poinsot formula, volume = icosahedron + 20 golden pyramids | 3.6e-5 |
| Lotus 3 = excavated dodecahedron | same 32 corners as Lotus 2; 60 equilateral triangles of the hull dodecahedron's edge; all faces on the core icosahedron's 20 face planes; volume = dodecahedron − 12 J2 | 1.4e-5 |
| Dodecahedral Chain stages 2 and 3 = Lotus 2 and 3 | corner sets compared | 6.3e-6 |
| Samsara (Chain step 2) stages 2 and 4 = excavated dodecahedron ×1/φ, GSD ×φ² | corner sets compared after scaling; scale factor checked as a power of φ | 5.4e-5 |
| Bodhi Kit B 2 = rhombic hexecontahedron | corners of 20 prolate golden rhombohedra (edge 1) round the centre, built from the 5-fold axes; volume = 20 prolate rhombohedra; 60 golden rhombi (diagonal ratio φ); 30 planes, all at the centre triacontahedron's inradius | 3.5e-6 |
| Dharma 7: convex 80-corner solid | hull volume = solid volume; face census; the 30 quadrilaterals are rhombi (equal sides, angles 56.68°/123.32°), **not rectangles** as the brief's lead said; corners = 60 (truncated icosahedron) + 20 (dodecahedron); all 90 non-pentagon planes at one distance (1.5) | — |
| Dharma 7 is not on deltoidal-hexecontahedron or triakis-icosahedron planes | angle of triangle normals to the nearest 3-fold axis: 20.905°, against 14.985° and 11.211° for those Catalan solids | — |
| Dharma 10 is not the great dodecahedron | its dimples reach r = 1.6057; the great dodecahedron round the same icosahedron reaches r = 1.4013; its 60 triangles lie on 60 distinct planes | — |

Not checked directly:
- The label Ef1g1 and Wenninger's model number 28 for the excavated dodecahedron come from Wikipedia, which cites *The Fifty-Nine Icosahedra*. We did not see the book.
- The rhombic hexecontahedron was not mapped to Messer's (1995) notation.
- The absence of a name for the 80-corner solid rests on our search: Archimedean, Catalan and Johnson classes excluded by its face types and two corner orbits; web and library search. It has not been checked against Conway-operator catalogues.

## Pieces (`analysis/pieces_analysis.py`, `analysis/pieces-analysis.json`, `.log`)
- All 11 views' pieces were grouped into congruence and similarity classes by corners, faces, edge lengths, dihedrals and volume.
- For each class: corners, edges, faces, edge lengths with multiplicities, interior dihedral angles, volume, symmetry group order (proper and improper, by searching vertex permutations induced by orthogonal maps), and convexity.
- Mosseri–Sadoc check: each piece was compared with t1–t6 from the library's `shapes/mosseri-sadoc-tiles.json`, allowing for scale.
  - AXE = t6 and CLEO = t4 at the Icosa-13 scale. This confirms DICTO's earlier credit.
  - The Dharma t1 = t1 at that scale.
  - **Cleo-low is similar to t3, at 0.809 times the Icosa-13 scale, which is half the tabulated Mosseri–Sadoc size.** This had not been recorded in DICTO's earlier studies.
- Closed forms (squared lengths, cos or cos² of dihedrals in Q(√5)) were fitted to 3e-5. They are guesses for DICTO's reference, not proofs. The paper quotes only standard ones.
- Diadem L and Diadem R are congruent by measurement. Their symmetry group is C2 with no reflection, so they are a chiral pair, as the Bodhi pieces study states.

## Counting convention (finding about the study's own counts)
- `steps.py` and `renders/index.json` merge coplanar faces that touch only at a corner, and they do so unevenly.
- As a result, symmetric stages get asymmetric counts. Lotus 2, for example, is counted as 16 triangles + 12 hexagons + 4 decagons on 12 equivalent planes, and Lotus 3 as 56 triangles instead of 60.
- The paper uses the `transitional.js` convention. **Suggested fix:** never merge across a corner-only contact.

## Nets (`nets/nets.py`, `nets/nets-checks.json`; ran on dicto-node)
| Shell | Scale | Pieces | Glue pairs | Mountain / valley folds | Worst overlap | All edges folded or paired | All tabs present |
|---|---|---|---|---|---|---|---|
| Lotus 2 (GSD) | 44 mm/unit | 5 | 35 | 40 / 15 (+15 valley glue edges) | 6e-13 mm² | yes | yes |
| Lotus 3 (excavated dodecahedron) | 40 mm/unit | 6 | 36 | 18 / 36 (+24 valley glue edges) | 3e-8 mm² | yes | yes |
| Bodhi Kit B 2 (rhombic hexecontahedron) | 30 mm/unit | 6 | 66 | 31 / 23 (+37 valley glue edges) | 8e-8 mm² | yes | yes |
| Dharma 7 (80 corners) | 46 mm/unit | 6 | 84 | 96 / 0 (convex) | 3e-13 mm² | yes | yes |

How the nets were checked:
- **Congruence.** Each 2D face matches its 3D face (sides and angles) to 1e-10 mm.
- **Overlap.** No faces or tabs overlap within a piece; tabs are clipped to free paper and must keep at least 45% of the edge.
- **Page fit.** No piece leaves the printable area, and pieces do not overlap on a page (assertions in `svg_pages`).
- **Folds.** Fold kind comes from the 3D dihedral: mountain where the solid is convex, valley where it is reflex.
- **Unfolding.** Pieces never close the ring of faces round a corner whose angle defect is below 40°. For the convex 80-corner solid we used a steepest-edge cut tree (best of the random directions tried).
- **Not done.** No net has been printed and folded by hand yet. The PDF was rendered with headless Chromium on dicto-node; the pages were looked at as 45 dpi previews.

## References
- DOIs were checked against Crossref (`api.crossref.org`) on 2026-10-13.
- Messer 1995 and the Twarock–Luque and Cutler–Schulte PDFs were downloaded and their title pages read.
- Library: 26 entries added (`papers/MANIFEST.json`, category `transitions`), INDEX.html/pdf rebuilt, committed in the library's own repository.

## Not done (open)
- Tsai, Bergman and Mackay shell radius ratios were not compared stage by stage.
- The 36 distinct convex partial-ring signatures were not identified.
- Samsara stages 5–11 were not identified.
- The great stellated dodecahedron and excavated dodecahedron are classical. The novelty of the dissection routes between them rests on a non-exhaustive search.
