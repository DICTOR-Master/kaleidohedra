# App and books premise audit (16 Nov 2026)

DICTO, 16 Nov 2026: "we need to rebuild apps built on beautiful but mistaken premises", "check the red and white queens in the apps, see what they are built in. I was thinking of the sector split or any transitional shadows could possibly be wrong", and "means a re-edit of books presumably".

**Conclusion.** The Queens' geometry in the app is right. Both Queens are built exactly. The sector split cuts along true mirrors and partitions both Queens. The five stages between the Queens are the right uniform polytopes, and every shadow count checked matches. The one fault in the geometry is in the stage slider. The inner stages are seen along the White Queen's four directions, but its Red end switches to the Red Queen's own four directions under the same names. So the last step turns the view by 22.2° (vertex- and cell-first) or 10.8° (edge- and face-first). The app does not rest on any of the corrected premises 1–6: no world claims the Vacuus needs central symmetry, that the Red Queen is built by inclusion, that the silent sets hide because of the twist, scutoid rates in nature, or element reasons for colours. The fixes are small. There is one geometry fix (the stage slider), a few wording fixes, and one new view (the three Vacuus kinds in the lens). Nothing needs a rebuild. In the books, the work is the re-edit listed in Part 3.

Status: READ-ONLY audit. Nothing in ~/k-mix or in any book was edited. App state: k-mix master at a4e82acf (16 Nov 2026). Computation: the numeric check below ran on the compute machine (pilot, under 5 min, FINAL ok, 26 checks).

---

## Part 1. The Queens: what they are built from, the sector split and the transitional shadows (checked in the geometry)

Check script: a reimplementation of the app's own constructions, read from its data files `white-queen-data.js` and `red-queen-data.js` and following `queen-sectors.js`, `queen-stages-geometry.js`, `white-queen-geometry.js` and `red-queen-geometry.js` line by line. Exact tests use sympy in Q(√5); the rest is floating point at tolerance 1e-9. Log: 26 `CHECK ok`, FINAL ok. As the brief asked, only this README is committed. The script and log are kept outside the repository (scratch), and can be filed here on request.

### 1.1 How each Queen is built

| world / file:function | what it does | verdict (numbers) |
|---|---|---|
| White Queen: `white-queen-geometry.js` `VERTICES` from `white-queen-data.js` | The 600-cell taken directly from exact coordinates: the permutations of (±2, 0, 0, 0), (±1, ±1, ±1, ±1), and the even permutations of (±φ, ±1, ±1/φ, 0). The 720 edges, 1200 triangles and 600 cells come from the source study's model. | **Correct.** 120 corners at radius 2. All 720 edges equal √5 − 1. Corner 0 is (2, 0, 0, 0). |
| Red Queen: `red-queen-geometry.js` `VERTICES_EXACT_RQ`, `EDGES`, `PENTAGONS`, `CELLS` | Built as the **dual** of the White Queen, not by inclusion. Its 600 corners are the centres of her 600 cells (exact in Q(√5)). An edge joins two cells that share a triangle. There is one pentagon round each of her edges and one dodecahedron round each of her corners. | **Correct.** The corners satisfy r² = 7/4 + 3/4√5. There are 1200 edges, all with edge² = 1/4. Nothing in the code builds the 120-cell from inscribed 600-cells, so premise 2 does not touch the app's geometry. |

### 1.2 The sector split (`queen-sectors.js`: `sectorCones`, `conesOverFaces`, `cellWedges`)

**What it splits, and by what rule.** Each Queen is cut from the centre into cones. Each cone contains the seed axis v = e₀ (the White Queen's corner (2, 0, 0, 0)) and stands over one face of the core. For the White Queen the core is the 20 cells at v, and its faces are their 20 outer triangles (the core icosahedron). For the Red Queen the core is the dodecahedron round her corner v, with 12 pentagons. In the 3D picture across v, each boundary is the plane through the picture's centre and one core edge. In 4D this is the hyperplane through the centre spanned by v and that edge. Every Shells picture maps x to (frame · x)/(x₀ − eye), a projective map with a positive denominator, so cutting in the picture is the same as cutting in 4D. The cut is exact.

| check | White Queen (20 sectors) | Red Queen (12 sectors) |
|---|---|---|
| boundaries over the core edges | 30 core edges on 15 distinct hyperplanes | 30 core edges on 15 distinct hyperplanes |
| are the boundaries true walls? | **yes, all 30 are mirrors (exact)**. Each is the plate of the edge triangle (v, a, b), as face lemma (a) of Walls of Silence predicts. | **yes, all 30 are mirrors (exact)**: the normal is parallel to a White Queen corner |
| the 15 hyperplanes | the 15 mirrors through v (the H3 mirrors of the corner's icosahedral symmetry) | the same 15 mirrors through v |
| partition | every one of 20,000 random points lies in exactly one cone | the same, 12 cones |
| cells cut | 300 of 600 tetrahedra are cut, 300 are whole, 15 whole per sector. The app's "half of the White Queen's [cells] sit on boundaries" is right. | 72 of 120 dodecahedra are cut, 48 are whole, 4 whole per sector. "Most of the Red Queen's" is right. |
| count | 20 | 12 |

**Verdict: correct.** No piece is assigned to the wrong sector, none is missing and none overlaps. Each sector is a union of whole Coxeter chambers: 720 for the White Queen and 1200 for the Red Queen.

**The same cut in two other worlds (not wrong, but not on walls).** `world-bitrunc.js` cuts the bitruncated 600-cell into 32 sectors over its core truncated icosahedron. Of its 90 core edges, only the 30 between two hexagons give mirrors. The 60 pentagon–hexagon edges give hyperplanes on no wall of the 600-cell. `perm4-geometry.js` cuts the 4D permutohedron into 14 sectors over its seed permutohedron, and none of its 36 seed-edge hyperplanes is a mirror xᵢ = xⱼ. The app's notes describe the rule correctly ("the planes through the seed axis over the core's faces") and make no claim about walls, so nothing in them is false. If DICTO wants every sector boundary to be a wall, as it is for the Queens, these two cuts would need a different rule. That is DICTO's call; it is listed under 1.4.

### 1.3 Transitional shadows: the five stages (`queen-stages-geometry.js` `BUILD`, `stage`, `stageShadowAt`)

Rule: Wythoff truncations from the White Queen's own elements. Each stage is rebuilt here exactly as the code builds it, and its edges and cells are counted with an independent 4D hull.

| stage | rule in the code | corners, edges, degree | cells (independent hull) | next distance / edge | verdict |
|---|---|---|---|---|---|
| t01 truncated 600-cell | 1/3 along each edge | 1440, 4320, 6 | 720 cells of 12 corners (120 icosahedra + 600 truncated tetrahedra) | φ | correct |
| t1 rectified 600-cell | edge midpoints | 720, 3600, 10 | 120 of 12 + 600 of 6 (icosahedra, octahedra) | √2 | correct |
| t12 bitruncated | 3/5 from edge middle to triangle centre | 3600, 7200, 4 | 120 of 60 + 600 of 12 (truncated icosahedra, truncated tetrahedra) | φ | correct |
| t2 rectified 120-cell | triangle centres | 1200, 3600, 6 | 120 of 30 + 600 of 4 | φ | correct |
| t23 truncated 120-cell | (5 − √5)/10 along each Red edge | 2400, 4800, 4 | 120 of 60 + 600 of 4 | 1.902 | correct |

All counts match `STAGE_FACTS` and the note. The cut (5 − √5)/10 = 1/(2 + φ) is the value that makes the decagons regular. Every stage is a true orthogonal shadow: `viewAt` turns a frame that stays orthonormal and perpendicular to u.

**Shadow outlines** (true corners, with points in the middle of an edge removed by a linear-programming test):

| | vertex-first | edge-first | face-first | cell-first |
|---|---|---|---|---|
| White Queen (app note: 42, 52, 56, 44) | 42 | 52 | 56 | 44 |
| Red Queen (atlas data: 158, 180, 160, 80) | 158 | 180 | 160 | 80 |

Both match. Each direction passes through the centre of its named element: a corner, an edge midpoint, a face centre or a cell centre.

**The one geometric fault: the direction names change meaning at the Red end of the stage slider.**
- File and code: `world-white-queen.js`, lines 166–168 and 308. The stages t01…t23 (slider 1–5) are drawn by `stageShadowAt(key, view.from, view.to, s)`, which uses the **White** Queen's `viewAt`. At slider 6, `M()` becomes `RQG` and `RQG.shadowAt(view.from, view.to, s)` uses the **Red** Queen's own four directions, with the same From/To names kept.
- The two sets of directions are swapped (exact): White vertex-first = Red cell-first, White edge-first = Red face-first, White face-first = Red edge-first, White cell-first = Red vertex-first. Between the same names the angle is 22.239° (vertex and cell) or 10.812° (edge and face).
- So the step from t23 to Red jumps the view direction. The outline goes from 200 corners (t23 along the White vertex-first direction, which is the Red Queen's cell axis) to 158 (Red along her own vertex-first). The truncated 120-cell is shown cell-first and the Red Queen vertex-first, under one name. Because the stages are drawn along the White directions, the inner stages read as the White Queen's views relabelled. The note, "the slider shows their shadows in the queens' four directions", hides this.
- Along the Red directions every stage count is the mirror image of its count along the White directions. For example, t12 gives 240 / 580 / 636 / 504 along the White directions and 504 / 636 / 580 / 240 along the Red ones. This confirms the swap.
- **Fix (data/geometry, S):** at slider 6 draw the Red Queen with the White Queen's `viewAt` (her corners projected along the same u and frame), so the slider is one continuous view. The direction label then needs a qualifier, such as "vertex-first (of the White Queen) = cell-first of the Red Queen". The alternative is to translate From/To by the swap when the slider crosses into Red. **Risk:** the `?open=whitequeen:` links, the saved views and the e2e tests that read `stop`/`dir` at stage 6. The tests that touch this are tests/unit/queen-stages.test.mjs, red-queen.test.mjs and white-queen.test.mjs, and tests/browser/queen-stages.mjs and white-queen.mjs. Re-run them, and smoke the slider through the UI.

**What the app does not show (no fault).** There is no Hopscotch line S(μ) = 600-cell ∩ μ·120-cell, no "Between the Queens" (#76) world and no "Silent Queens" world. The five stages are the uniform members of that line. The golden station of Walls of Silence (Proposition 6) is the truncated-600-cell member cut at 1/(1 + φ²) of each edge, whose Vacuus is exactly the 360 walls. It is not a stop. Adding it would be a new view.

### 1.4 Queens: wording and views

| world / file:line | current text | premise | now true (source) | change | effort | risk |
|---|---|---|---|---|---|---|
| White Queen stages, i18n.js:939 `wq.note.stage` (and the ja/es/fr/ko/zh/ru copies at 3028, 5116, 7204, 9292, 11380, 13468) | "120 truncated icosahedra (footballs) … the four-dimensional icosahedron with hexagons … the slider shows their shadows in the queens' four directions" | banned word; vague image; hides the direction swap | DICTO's rule against "football"; 1.3 above | Drop "(footballs)" and its translations. Drop "the four-dimensional icosahedron with hexagons". End with a sentence that matches the fix in 1.3, for example: "the slider shows every stage along the White Queen's four directions; along them the Red Queen is seen cell-, face-, edge- and vertex-first in turn" | S | none |
| Red Queen, i18n.js:1129 `rq.note` | "It is built exactly from the White Queen: its corners are the centres of her 600 cells." | (checked) | dual construction, correct | none. To meet premise 2, optionally add: "Ten White Queens fit inside her, two through every corner, but they do not make her pentagons" (Walls of Silence, Theorem B; redqueen-cats) | S (optional) | none |
| Bitruncated and 4D Permutohedron sectors, i18n.js:979; perm4 notes | "Sectors: every cell is cut by the planes through the seed axis over the core's faces" | none (true as stated) | 1.2: 60 of 90 and 36 of 36 boundaries are on no wall | keep, or (DICTO's call) re-cut along walls only | — | — |
| White Queen (new view) | — | — | Walls of Silence: the 60 mirrors and 300 cross walls, the two states of five 600-cells in the Red Queen, the golden station. Silent Running: the five S5-orbits A, −A, C3, B, −B. Both drafts say "no world shows" these. | new mode (DICTO's call, after release) | L | none to what runs |

**World verdicts (Queens).** White Queen: OK, with a wording fix (the stage note). Stage slider: fix the geometry of the Red end (S). Red Queen: OK. Sectors (White, Red): OK. Bitruncated and Permutohedron sectors: OK as stated.

---

## Part 2. The rest of the app (premises 1–7)

### 2.1 Polyhedraverse: DICTO Vacuus lens (`vacuus-geometry.js`, `vacuus-lens.js`; i18n.js:1961–1980)

- **Premise 1 (Vacuus only for centrally symmetric solids): not in the app.** `vacuusSolidOf` takes any solid whose centre O, the mean of its corners, lies strictly inside every face plane. Convexity is not needed. This is already the widened definition of Walls of Silence §2, applied in 3D with the corner centroid as O.
- **What is now too narrow is the reading.** The "Sheets" view (`finsOf`) draws one fin per edge and groups the fins by **congruence** (SSS). It never groups them by **plate**, the plane through O and an edge. So it cannot show the three kinds: heart (every plate a full sheet: an edge and its opposite), inherited heart (some plate carries two or more edges but is not full), and non-heart (every plate a single fin). Figure 1 of Walls of Silence shows the octahedron as 3 full square sheets and the tetrahedron as 6 single fins. The lens shows both as one class of congruent fins.

| item | current | now true (source) | change | effort | risk |
|---|---|---|---|---|---|
| i18n.js:1966 `poly.vac.view.sheets` | button "Sheets"; the captions (1975, 1977) say "fins" | a sheet is a plate's fins taken together; a fin is the cone over one edge (Walls of Silence §2) | rename the button "Fins" (all 7 languages) | S | none |
| `finsOf` and the Sheets view | fins coloured by congruence class | the kind is read from the plates (Lemma 1 and the index law, Walls of Silence §3) | **new mode:** group the fins by plate (normal of span(O, edge), merged under 1e-9). Colour full sheets, shared sheets and single fins as in Figure 2 of the paper (blue, pink, green), and add one caption line: "{p} plates: {kind}". Lemma 1 in 3D means a centrally symmetric solid reads heart. | M | low: a new view key. The Pyramids / Exploded / Star / Struts views are unchanged. |
| centre O | the corner mean, unstated | "the centre must be stated" (Walls of Silence §2, §8, the GET example: 2 of 54 plates on walls about the corner centroid) | caption: "seen from the mean of its corners" | S | none |

Verdict: **wording fix + one new mode** (no rebuild).

### 2.2 Premises 3–6 across the app (wording sweep of all English strings, the world files, the wizard, guide, almanac, changelog and the HTML pages)

- **3, hidden walls:** no text says that golden or silent sets hide in the walls, for any reason. The gperm "wall" captions are Postnikov's wall forms, which is correct. OK.
- **4, silence and tones:** no app text on silence, harmonics, tones, twisted classes or Sym6. The Double Vision notes (i18n.js ~1247–1400) are geometry only. OK.
- **5, scutoids:** no text claims scutoids or swap rates in Earth plates, granulation, clouds, eyes, froth, tissues or voids. Every scutoid count is #104's sweep (bitruncated 716 / 2166 / 716; permutohedron 26 / 66 / 26), and those counts stand. One precision slip:

| world / file:line | current | premise | now true | change | effort | risk |
|---|---|---|---|---|---|---|
| 4D Permutohedron, i18n.js:1007 `pm.note.sweep` | "26 births, 26 deaths and 66 scutoid swaps, as the h-vector (1, 26, 66, 26, 1) predicts in every direction" | the counts hold in every direction | one change per corner only along a **generic** direction; along special directions the changes come in batches (#104; the bitruncated note already says so) | "in every generic direction" (all languages) | S | none |

- **6, elements:** Fire, Water, Earth, Wind and Void appear only as DICTO's wizard ring headings (i18n.js 1876–1880; dimension-wizard.js 716–725, with kanji and colours). That is allowed. "void(s)" elsewhere (i18n.js 605, 608, 697, 708, 709, 1600) means packing gaps, which is geometry. render.js has an internal material key `water`, shown to the user as "Blue" (index.html:1262). Renaming the key would break saved builds, so leave it. Comments in world-platonic-mix.js:18 and world-pair-lattice.js are not visible. **No violations.**

### 2.3 Premise 7: published corrections not yet in the app

| world / file:line | current | correction (source) | change | effort | risk |
|---|---|---|---|---|---|
| Chains (Karma / Dharma / Bodhi film), world-chains.js:376 `PIECE` (`icleo`, `ccleo`, `cspike`), shown through `pieceName` at :389 | "Cleo-Ico" | one name per shape: "Cleo-Icos" (Concordance errata n = 10) | three display strings (the comments in mandala-geometry.js:120 and world-up.js:17 are cosmetic) | S | none |
| Vajrayana, i18n.js:1375 `vj.note.oh`; world-vajrayana.js:22 `VJ_NAMES O: 'O'`, :30 `OH_FULL ohO: 'O'` | "the DICTO Ogdoecontahedron O"; on tap, "O · the DICTO Ogdoecontahedron" | "OG" everywhere, since O is the octahedron (errata n = 35) | display strings 'O' → 'OG'; keep the internal keys | S | low |
| Aristotle's Pyramid, i18n.js:1564 `alm.d.aristotle.desc` | "DICTO's question: Aristotle wrote that…" | voice rule: DICTO proposes or answers (errata n = 23) | "DICTO's proposal: …" | S | none |
| 5D quasicrystal, i18n.js:385 `wiz.dim.5D`; almanac i18n.js:268 `alm.c.cutAndProject.desc` | "layers of the Penrose tiling … in a pattern that never repeats" | the world stacks Penrose layers as prisms (world-quasicrystal.js:6–7, `PRISM_HEIGHT`), so it repeats straight up and is non-periodic only across the layers. This is the same kind of fault as erratum #105 Lead 3 (non-periodic in one direction only). | "never repeats across the layers; the layers repeat straight up" | S | none |

Checked and right in the app: the TI Star core (krp-core `TI_STAR_CORE`, cut 0.408629 = (10 − √5)/19, hexagon ratio √5); the DICTO GTI (up-film-data.js, edges 1.23607 : 0.52786, ratio 2.34166 = 1 + 3√5/5). Not present in the app: the golden-slice filling, the Icosaxes Hexa volume, "finding #16", "2/3 of each roof", the polytope coinage, "capped" J11, and the #89 depth polynomial.

### 2.4 World verdicts (app)

| world | verdict |
|---|---|
| White Queen (shadow, slice, shells, halves, sectors) | OK; wording fix (stage note) |
| Stage slider (White → Red) | geometry fix at the Red end (S) |
| Red Queen | OK |
| Bitruncated 600-cell | OK (sectors not on walls: DICTO's call) |
| 4D Permutohedron | wording fix ("generic") |
| Polyhedraverse DICTO Vacuus lens | wording fix + new mode (plates and kinds) |
| Chains film | wording fix (Cleo-Icos) |
| Vajrayana | wording fix (OG) |
| Aristotle's Pyramid (almanac) | wording fix (voice) |
| 5D quasicrystal (wizard, almanac) | wording fix (repeats along the stacking) |
| every other world | OK for premises 1–7 |

No world needs a rebuild.

---

## Part 3. Books (premises 1–7, the Queens' construction, the sector split and the stages)

Read: every papers/book-* (the HTML as published), and the next-version branches where they exist. Line numbers are lines of the HTML files. DICTO's book rule applies: each corrected statement below states only the right result. Errata go only into the Concordance and the version lines.

**Overall.** No book says the Red Queen is built from White Queens by inclusion. None says that the silent shapes hide because of the twist. None claims scutoids in nature or a Sym6 silence. None uses "football". The books' account of the five stages and of the two sector splits agrees with the app and with the geometry checked in Part 1. The faults are these:
- the narrow Vacuus definition (Paradigm; Alicia v6 draft);
- one false statement in the Alicia v6 draft;
- stage tables that leave out the two rectified stages;
- element words used as labels in the Platonic Coda;
- Concordance errata still printed in the Golden Cycle, Star Cores, Quanta, the DICTOnary and their editions.

### 3.1 Alicia in Wonderland (book-queens; published v5, draft v6 on branch next-version/book-queens)

| place | current text | now true (source) | statement to use |
|---|---|---|---|
| Opening, paper.html:75, front.html:21 | "the word polytope for them is credited to her" | Hoppe coined "Polytop" (1882) (erratum 46) | "The word polytope is Reinhold Hoppe's (German Polytop, 1882); Alicia Boole Stott brought it into English." **Done in v6.** |
| Ch 7 abstract :695; Ch 8 abstract :757, §2 heading :762, conclusion :802; Epilogue :997 (and epilogue.html:4; still in v6); Golden Ladder Ch 5 :626, :631 | "built exactly from the White Queen" | the construction is duality, which is correct, but the wording invites the inclusion reading. Inclusion does not build her pentagons, while the duals of the S5-orbit solids do: Q = A* ∩ (−A)* ∩ C3* ∩ B* ∩ (−B)* (Walls of Silence, Theorems B and B′; redqueen-cats) | Ch 8 abstract: "The 120-cell, named the Red Queen by DICTO, is the White Queen's dual: her 600 corners are the White Queen's 600 cell centres, her edges join cells that share a triangle, her 720 pentagons ring the White Queen's 720 edges, and her 120 dodecahedra ring the White Queen's 120 corners." §2 heading: "The Red Queen, the White Queen's dual". |
| Ch 7, five stages :702–717 | five stages with cuts 1/3, ½, 3/5, centre, (5 − √5)/10 | matches the app and the exact check (Part 1.3) | no change |
| Ch 8, sectors :757–765, Plates 14, 35 | 20 Cleo-Icos round a corner (real cells); 12 pentagonal pyramids from the 4D centre (not cells) | matches the app; the boundaries are mirrors (Part 1.2) | no change. Optionally add: "The 15 planes that cut the sectors are mirrors of both Queens." |
| Ch 9, Silent Queens :933–987 | 11-designs; the station μ* ≈ 0.924165 | consistent with Silent Running | no change. If extended, keep μ* apart from the golden station of Walls Prop. 6 (cut 1/(1 + φ²)) |
| **v6 draft** Ch 10, "The Vacuus of the Queens", ~line 999 | "the cube's edges lie on no such slice at all." | false: each cube edge lies with its opposite on one of 6 diagonal planes (Platonic Ch 4 table) | "Each edge spans one plate through the centre. The octahedron's twelve edges lie four to a plate on three square sheets; the cube's twelve lie two to a plate, an edge and its opposite, on six diagonal planes; the tetrahedron's six lie one to a plate on six planes." |
| v6 Ch 10, same paragraph | "the set of flat slices through its centre that carry its faces" | widened definition with three kinds (Walls of Silence §2–3) | "Let X be a polytope and O a chosen point inside it. Each ridge spans with O one hyperplane, its plate; the Vacuus of (X, O) is the set of plates with the ridges on each. It is of the heart kind when every plate carries a ridge and its opposite (X centrally symmetric about O), of the non-heart kind when every plate carries one ridge, and of the inherited heart kind otherwise; the ridges of one orbit on a plate H number \|G_H\|/\|G_f\|. The centre must be stated." |
| v6 Ch 10, path line ~1000 and Table 10.1 | three stages (truncated 600, bitruncated, truncated 120) | Ch 7 and the app have five; the rectified 600-cell and the rectified 120-cell have faces on all 60 mirrors and 1200 plates on no wall (Walls §7) | add the two rectified rows |

Chapters to revise at the next version: Opening (done in v6); Ch 7 (abstract wording); Ch 8 (abstract, §2 heading, conclusion; add the ten inscribed 600-cells and the dual cats); Ch 9 (twisted silence); Ch 10 of v6 (the three rows above); Epilogue (wording and the new results). Ch 1–6 and the plates need no change.

### 3.2 The Permutohedron Paradigm (book-permutohedron-paradigm, v1)

| place | current text | now true | statement to use |
|---|---|---|---|
| chapters/00-open.html:33 (glossary), paper.html:86 | "the hyperplanes through the centre spanned by the ridges of a centrally symmetric polytope (#87)" | any polytope with a chosen centre; three kinds (Walls of Silence §2–3) | the definition in 3.1, cited "(#87, #105; Walls of Silence)" |
| chapters/07-web.html:11 | "The Vacuus of a centrally symmetric polytope is the set of hyperplanes …" | as above | the definition, then: "The 4D permutohedron is centrally symmetric, so its Vacuus is of the heart kind: 60 plates carry a face and its opposite, and 5 carry six faces each" (non-heart-vacuus control) |
| chapters/12-everyn.html:22 | "The fillings by permutohedra repeat; cut at a golden tilt, they do not." | non-periodic in one direction only (Concordance erratum, #105 Lead 3) | "cut at a golden tilt, they repeat along a plane and never across it." |
| chapters/07-web.html:36, table :51–57 | three stages | five stages | add the two rectified rows |
| 07-web.html:23–32, 01-three.html:26, epilogue.html:9 | "heart slices" (the five 1:2 slices) | "heart" is now also a Vacuus kind | tell the two apart at first use (DICTO's call; no rename proposed) |

Chapters: Opening (glossary), Ch 7, Ch 12 (closing line). The scutoid passages cite epithelia (Gómez-Gálvez 2018) and rosettes (Blankenship 2006) only, which is fine.

### 3.3 The Platonic Solids (book-platonic, v1)

| place | current text | now true | statement to use |
|---|---|---|---|
| chapters/coda.html:10–11 (and paper.html) | "The tetrahedron and the octahedron, fire and air, fill space together …; the cube, earth, fills space alone; the icosahedron, water, …"; "Water and the heavens, the two solids that would not fill the room" | element words used as labels inside mathematical claims (rule: elements only as history or heading). Also, Plato's interchange groups T, O and I against C, which is not the book's grouping. | "Plato's elements could change into one another (Timaeus 56d–57c). This book groups the solids by how they fill: the tetrahedron and the octahedron fill space together, and their face pyramids rebuild them face to face (Chapter 3); the cube fills space alone; the icosahedron fills space only with help; and the dodecahedron holds all the others." Line 11: "The icosahedron and the dodecahedron, the two solids that would not fill the room, …" |
| chapters/ch04.html:26–33 (§4.3 table) | edges and plates, right but narrow | three kinds | optional: "About the centre, the dodecahedron, icosahedron, cube and octahedron are of the heart kind (each plate carries an edge and its opposite; the octahedron four), the tetrahedron of the non-heart kind (six single fins)." |

The same Coda text sits in papers/book-arcs-2026-11-13/paper.html:87, a planning document. Chapters: Coda; Ch 4 (optional).

### 3.4 Concordance errata still in books

| book | place | current | statement to use | state |
|---|---|---|---|---|
| Golden Cycle | paper.html:56, 1378, 1423, 1453, 1465, 1473, 1478, 1633, 1643; front.html:21; epilogue.html:4, 14 | TI Star core "1/φ³" | "the icosahedron truncated at (10 − √5)/19 of each edge" (:1423: "its hexagons have alternating edges in the ratio √5, its pentagon sides the long ones, so it is the icosahedron truncated at (10 − √5)/19 of each edge") | fixed on next-version branch |
| Golden Cycle (#38 chapter) | paper.html:1053, 1068, 1101 | "hexagon sides 1 : φ", "cut at 1/(2+φ)" | "DICTO GTI: 12 regular pentagons and 20 hexagons whose sides alternate √5 − 1 and 5 − 2√5 (long : short = 1 + 3√5/5 ≈ 2.342); the icosahedron (edge 1) cut at (5 − √5)/12 ≈ 0.2303 of each edge." | **still wrong on the branch** |
| Star Cores | paper.html:48, 75, 120, 150, 162, 170, 171, 179, 184, 714, 733; front.html:19; epilogue.html:13 | "1/φ³" | as above | fixed in the v3 draft. Check that cards_data.py generates the plates with the new value |
| Quanta of Space, ja / zh / ar / fa | ja :1350, zh :1669, ar :1675, fa :1677 | TI Star core "1/φ³" | as above | English fixed on the branch; the four editions not |
| Quanta, ja / zh (ar, fa likely) | ja :242, zh :260 | the Jewel keeps "two-thirds of each roof" | "1/φ (about 0.618) of each roof by volume" | English fixed on the branch |
| Quanta, four editions | the Alice note | polytope "credited to her" | Hoppe's word, as in 3.1 | English fixed |
| DICTOnary of Atoms (and ar, fa, ja, zh) | paper.html:1303 | GTI "sides 1 : φ (cut at 1/(2 + φ))" | "hexagon sides √5 − 1 and 5 − 2√5 in turn, ratio 1 : (1 + 3√5/5) ≈ 2.342 (icosahedron cut at (5 − √5)/12 of each edge)" | **still wrong on the v1.4 branch and in all editions** |
| DICTOnary (and ar :395, zh :385) | paper.html:386 | "keeps the whole cube and 2/3 of each of its six roofs: volume exactly 12" | "keeps the whole cube and, of each of its six roofs, a carved roof of volume 2/3, which is 1/φ of the Euclid roof: volume exactly 12." | **still wrong** |
| Golden Ladder | paper.html:937 | "their depths share the minimal polynomial z⁴ − 8z³ + 4z − 1" | "their remaining sides 1 − 2x share the minimal polynomial z⁴ − 8z³ + 4z − 1, and their depths x ≈ 0.347943 and 0.233196 the minimal polynomial 4z⁴ + 8z³ − 18z² + 8z − 1." | fixed on the branch |
| Centre Pyramids (unpublished drafts) | drafts/ch1-plato.html:6, 25 | "Plato described the universe using five perfect shapes, which he called the elements" | "In the Timaeus Plato gives four of the five solids to the four elements, the tetrahedron to fire, and the fifth, the dodecahedron, to the whole (53c–56c)." | draft |

Clean: Bonds, Laws of Stacking and Space-Fillers. In each, the 1/φ³ values are other quantities (Lotus Jewel, layer frequencies, Dogstar core). The DICTOnary's Vacuus entries are already general, and its D105 already has (10 − √5)/19.

### 3.5 Per book: chapters to revise at the next version

- **Alicia (book-queens):** Ch 7 abstract; Ch 8 abstract, §2 heading and conclusion (dual wording, ten inscribed 600-cells, dual cats); Ch 9 (twisted silence); v6 Ch 10 (false cube line, general definition, five-stage table); Epilogue.
- **Permutohedron Paradigm:** Opening glossary; Ch 7 (definition, kind, five-stage table); Ch 12 closing line.
- **Platonic Solids:** Coda (element labels); Ch 4 (optional kinds sentence).
- **Golden Cycle:** the #38 chapter (GTI, still open on the branch); the #78 chapter, front and epilogue (done on the branch).
- **Star Cores:** done in the v3 draft (check the cards' generator).
- **Quanta of Space:** ja, zh, ar, fa editions (TI Star core, Jewel roof, Hoppe).
- **DICTOnary of Atoms:** the GTI row and the Jewel entry, in English and all four editions.
- **Golden Ladder:** :937 (done on the branch); Ch 5 dual wording.
- **Centre Pyramids drafts:** Ch 1 history sentence.

### 3.6 The Alicia next-version plan (papers/plan-alicia-v2/paper.html)

Already covered by the plan: the three Vacuus kinds; A and B in the walls; the White Queen as A + (−A) + C3 + B + (−B) by corners, with the solids overlapping; the ten White Queens, the two states, the 1200 + 1200 copies and the 1560 walls; twisted silence in Ch 9; the shadows' wall lattice; the rules (right statements only, elements as history, colours as colours).

To add to the plan:
1. The v6 draft already has a Ch 10, "The Vacuus of the Queens" (#107 retold), and it contains the three faults in 3.1. Decide whether the walls-and-cats material becomes Ch 11 or merges into that Ch 10.
2. The general definition, with the centre stated. Example: measured from its own centroid, the 600-cell less one corner has 915 plates, 900 of them single fins. Also the index law, C3 as heart and the special cuts as inherited heart.
3. Hidden is not silent. The arc line ("their plates are her walls") and the Ch 9 hand-on imply a cause. State the face lemmas, and that A and B are hidden because their faces are edge triangles, golden rectangles and radius triangles. Add that the snub 24-cell, the grand antiprism and the special cuts are hidden too and are not silent (Walls §4, §8).
4. The dual cats (Theorem B′): Q = A* ∩ (−A)* ∩ C3* ∩ B* ∩ (−B)*. The copies inside never reach her pentagons. The A* fins (or the B* fins) cover every pentagon and edge, and the fewest copies that do so are 16 A*, 16 B* or 22 C3*. Ch 8 must call her "her dual" and must not suggest that inclusion builds her.
5. Replace "the shapes and the structure weigh the same" with the three exact answers. By corners, the five orbits are the White Queen. By walls, A and B carry all 60 mirrors, and B carries 40 of the 300 cross walls. By solids, the hulls overlap and cover 65.0% of her; they are unions of chambers, never chambers.
6. Missing results: the B copies split her 1200 triangles exactly (Theorem B(d)); the chamber counts 4,291,200 and 593,236,800. Optionally put the golden station (Walls Prop. 6) in Ch 7, kept apart from Ch 9's μ*.
7. Five stages everywhere, including the two rectified ones.
8. Credits by name: A and B as orbits are Koca et al.'s; their description as solids and their Vacuus are DICTO's; the compound of ten 600-cells is Coxeter's; the special cuts are Dutour Sikirić and Myrvold's.
9. Figure colours: the Silent Running Fig. 2 orbit colours and the Walls Fig. 7 colours (16) are still pending. Print colour names only.
10. Add one line: the 15 hyperplanes that cut the sectors (Plates 14, 35) are mirrors, so the sector figures are true symmetric pieces (Part 1.2).

---

## Prioritised plan

1. **Stage slider, Red end (app, geometry, S):** draw the Red Queen with the White Queen's view at slider 6, or translate From/To by the swap, and fix the wording of the stage note in the same change (Part 1.3, 1.4). This is the only fault in the app geometry. Re-run the queen-stages / white-queen / red-queen tests and smoke the slider through the UI.
2. **Books with live wrong statements (re-edit):**
   - Alicia v6 Ch 10: the false cube line, the general definition and the five-stage table.
   - Paradigm: the glossary and Ch 7 definition, and the Ch 12 golden-tilt line.
   - DICTOnary and Golden Cycle: the GTI and the Jewel roof (still wrong on their branches).
   - Platonic Coda: the element labels.
   - The Quanta and DICTOnary editions.
   - Add the plan items in 3.6 to plan-alicia-v2.
3. **App wording batch (S, no risk):**
   - "(footballs)" out, in all 7 languages;
   - Cleo-Icos;
   - OG;
   - "DICTO's proposal";
   - "generic direction";
   - the 5D "never repeats" scope;
   - the Vacuus button "Fins" and "seen from the mean of its corners".
   This is one deploy-queue push.
4. **New view (M):** the Vacuus lens grouped by plate, with the three kinds (heart / inherited heart / non-heart). This is the app's form of the corrected #105.
5. **Later (L, DICTO's call, after Walls of Silence and Silent Running are released):** a Queens mode for the 360 walls, the two states of five 600-cells, the five S5-orbits and the golden station. Optionally re-cut the bitruncated and permutohedron sectors along walls only.

DICTO · dictospheres.com
