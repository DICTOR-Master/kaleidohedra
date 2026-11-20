# Hall's Dimpled Rhombic Triacontahedron (2016) against candidate 2, GET A and GET B (20 November 2026)

**Verdict: D. Hall's "Dimpled Rhombic Triacontahedron" (Sketchfab, 28 June 2016) is candidate 2 exactly, the solid of Inchbald and the DICTOnary's "indented rhombic triacontahedron". His description allows ten choices of the four corners; each gives candidate 2, five in the same hand and five in the mirror hand, as Hall says ("left handed" or "right handed"). It is not GET A and not GET B. Found on the way: J. Kostick's "concavo-convex triacon array" (3 April 2022) shows GET A, 19 translates on GET A's own lattice.**

The finding came from the pre-score study 2026-11-20-palomar-grunbaum-prescore (LEADS 1 to 3).

## Sources seen

| Source | Date | What was seen |
|---|---|---|
| D. Hall, "Dimpled Rhombic Triacontahedron – Construction", Sketchfab, sketchfab.com/3d-models/dimpled-rhombic-triacontahedron-construction-9e2be3ccfe7b480c846f4d431441ac19 | published 28 June 2016 | Page description and metadata from the public Sketchfab API, and the thumbnail (`sources/`). The model is marked downloadable under CC BY 4.0, but Sketchfab downloads need an account, so the model file was not taken. |
| D. Hall, "Lattice of Dimpled Rhombic Triacontahedra" (82ecc6e45827421e8908db5520575003) | 29 June 2016 | Description only: one DRT with 6 neighbours along ±X, ±Y, ±Z and 4 + 4 along the two tetrahedral sets of axes. |
| D. Hall, "DRT with Positive Tetrahedral Translation" (0ccb9676d36148189af82c77ae4bb8d8), "… Negative Tetrahedral Translation" (95eb8e5da3d04754b807ea3e06113370), "… Orthogonal Translations" (21252d4c53054480802932db2215f87a) | 11 July 2016 | Descriptions, and the thumbnail of the first: partial lattices of the same DRT. |
| D. Hall, all his public models as listed by the API | 2016–2020 | These five are his only dimpled-triacontahedron models. |
| J. Kostick, "Triacon arrays", john-kostick.github.io/vzome-sharing/2022/04/03/Triacon-array-2-part-11-46-35.html | 3 April 2022 | The post source, and the exact panel exports (`*.shapes.json`, from his public vzome-sharing repository) of its three arrays. The sha256 of each export is in `sources/`. The post links Hall's collection for the tetrahedral DRT. |

## What Hall's description fixes

- "The four dimples result from removing one golden rhombohedron from each of four vertices having tetrahedral symmetry."
- "The DRT is chiral": the hand depends on which tetrahedral set of vertices is chosen.
- A lattice "with tetrahedral, octahedral or cubic symmetries"; "Fourteen such DRTs will completely enclose one in their center."
- "32 balls and 60 red struts", made with vZome. Red struts lie on the six 5-fold axes, which are the edges of the rhombic triacontahedron T.
- The thumbnail shows T with a three-face corner in front and the removed rhombohedra drawn pulled out.

The hand of the model actually posted cannot be read from the thumbnail. Hall states that both hands exist, so both are tested.

## Method (exact, in ℤ[φ])

`scripts/hall_check.py` uses numbers x + yφ with rational x, y, and no floating point anywhere.

1. **Build T.** T is built from the six axes (1, φ, 0), (−1, φ, 0), (0, 1, φ), (0, −1, φ), (φ, 0, 1), (−φ, 0, 1). It has 30 faces, 32 corners and 60 edges: 20 corners where 3 faces meet and 12 where 5 meet.
2. **Find the corner sets.** Every 4-set of corners of T that forms a regular tetrahedron centred at T's centre is listed. There are exactly 10, all made of 3-face corners: the alternate corners of the five inscribed cubes.
3. **Build Hall's solid.** For each set, the rhombohedron spanned by the three edges at each chosen corner is removed, and the three faces at that corner are replaced by the three faces at its opposite corner. Each result has F, V, E = 30, 32, 60 (Hall's 32 balls and 60 struts). Each dimple moves the corner inward. Each solid has 12 symmetries, all rotations, and none is a reflection, so it is chiral, as Hall says.
4. **House congruence test.** This is corner matching in both hands (memory rule feedback-congruence-test). Each solid is centred at its corner centroid. Three independent corners of X are taken, and every triple of corners of Y with equal inner products is tried. The map M with M(xᵢ) = yᵢ is kept only if M is exactly orthogonal and maps all 32 corners and all 30 faces of X onto Y. The determinant of M gives the hand.

Results (`data/hall_check.json`, `data/hall_check.log`):

| | GET A (cand. 0) | GET B (cand. 1) | candidate 2 |
|---|---|---|---|
| F, V, E | 30, 32, 60 | 30, 32, 60 | 30, 32, 60 |
| symmetries (rotations + reflections) | 2 + 2 | 3 + 0 | 12 + 0 |
| maps from Hall's solid, 10 corner sets | 0 | 0 | 12 for each set: sets 0, 2, 4, 7, 9 by rotations (same hand); sets 1, 3, 5, 6, 8 by reflections only (mirror hand) |

So Hall's solid is candidate 2 in one hand and its mirror image in the other. Each match uses 12 maps, the full symmetry group, and every match was checked on all 32 corners and all 30 faces. `FINAL ok`.

## Kostick's arrays: is GET A or GET B among them?

`scripts/kostick_check.py` and `scripts/kostick_cells.py` read the three panel exports. Their panel coordinates are floats with 7 digits.

1. **Snap the panels to exact values.** Each coordinate is snapped to (a + bφ)/2 with |b| ≤ 400. The largest residual is 1.1·10⁻⁶ (concavo array).
2. **Check the panels exactly.** x and y are swapped, because vZome's icosahedral frame is the mirror of ours, and the coordinates are divided by the strut scale φ³. In the concavo array all 354 panels are then checked exactly to be golden rhombi with their edges on the six axes. In the other two arrays, the panels used are those that equal a face of a T placement exactly.
3. **Read the cells.** All three GET-family solids are T with four of its 3-face corners dimpled (18 faces of T kept, 12 dimple faces), checked exactly. So every translate of T fixed by some panel is read corner by corner: a corner is plain if its three faces of T are shown, dimpled if its three inward faces are shown, and unseen otherwise.

Results (`data/kostick_cells.json`, `data/kostick_check.json`):

- **"concavo-convex triacon array"** has 19 cells. Each shows 25 or 26 of its 30 faces; the rest are left out of the display.
  - Every cell has the same four dimples (the four corners of a square face of an inscribed cube), and all 19 cells are translates of one another.
  - That dimple set is GET A's, exactly. The solid T with those four dimples is congruent to GET A by the corner test (4 maps), and to no other rank-3 candidate of search6.
  - All differences between the cells lie in GET A's lattice, in either hand, and they generate it with index 1.
  - No cell can be GET B or candidate 2 (no symmetry fits their dimple sets to what is shown).
  - Kostick says the array "fill[s] space in a directional way". Read as T with corner dimples, a cell with any further dimple would have a smaller volume than GET A's covolume and could not fill that lattice. **So his cell is GET A.**
- **"Triacon-array-2-part"**:
  - 8 cells show 7 dimples each: 7 of the 8 corners of an inscribed cube. These are Kostick's "octahedrally dimpled" cells.
  - One cell shows all 30 faces of plain T.
  - 6 further cells show only 8 plain corners. These are partial views of the convex T cells his text describes, and the panels alone do not decide them.
  - No cell shows the dimples of GET A, GET B or candidate 2.
- **"Triacon-concentric-array-3"**:
  - 20 cells show 4 dimples and 12 cells show 5, all in patterns that differ from GET A, GET B and candidate 2. These are his cells "dimpled on 3-fold axes".
  - The 12 convex T cells show 15 plain corners and none dimpled.
  - No dimpled cell is GET A, GET B or candidate 2. For the 12 convex cells, 5 corners each are unseen, so the panels alone do not rule out hidden dimples; Kostick's text calls them convex.
- **GET B was not seen** in any of Kostick's arrays or in Hall's models.

## Changes made (DICTO approved, 20 Nov)

- DICTOnary v1.4 draft (papers/book-quanta-dictonary: paper.html, atoms-catalogue-known.html, atoms-catalogue.html):
  - The known atom is renamed from "(Inchbald / Senechal–Taylor, c. 2023)" to "(Hall, 2016; Inchbald; Senechal–Taylor, c. 2023)". Its note now says Hall showed it first, gives the one-line reason (earliest dated source; the same solid exactly, this study) and the Sketchfab source.
  - The same name is used where D192 and D193 refer to it.
  - One sentence is added to the status box, and the change is logged in names-changes.md.
  - Rebuilt with print.mjs; figcheck is OK; the draft now has 129 pages. The reading-folder draft was replaced, and the old one was moved to read-earlier.
- GET study README (2026-11-15-grunbaum-k10): rows for Hall 2016, Inchbald and Kostick 2022 were added to the prior-art table, with an update under the novelty verdict.
- **D192 GET A (DICTO's decision, 20 Nov):** name and number kept; note added at its first use: "* First shown by J. Kostick in a vZome array (“concavo-convex triacon array”, 3 April 2022), without proof; rediscovered by DICTO as GET A." Its "not found in the sources checked" now covers only the zone property and the proof of tiling. D193 GET B unchanged. Status box and names-changes.md updated; rebuilt (129 pages, figcheck OK); reading-folder draft replaced, previous copy kept in read-earlier.
- **Still open:** the Palomar entry's witness is GET A, so its literature section must credit Kostick 2022 too.

## Files

- `scripts/hall_check.py`: Hall's solid against candidates 0–2.
- `scripts/kostick_check.py`: direct placement of the four solids in all 120 orientations against the panels (concavo array).
- `scripts/kostick_cells.py`: corner-by-corner reading of the cells, their lattice, and the concavo cell's congruence.
- `data/`: the outputs and logs.
- `sources/`: Hall's metadata and thumbnail, Kostick's concavo image, and the sha256 of each export.

All computation ran on a compute host, in the foreground, under 285 s each. Nothing is left running.

FINAL ok
