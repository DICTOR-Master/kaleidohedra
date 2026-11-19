# The complete family of the Aequi: fair dice on the axes of the cube and the icosahedron (19–20 November 2026)

**Verdict: for the seven frame groups the family is complete (every orbit set searched, one fair die found in each within the search box): 149 Aequi** (Ih 4, Oh 4, Td 3, Th 47, T 91 in two hands each; O 0, I 0), by number of face orbits m = 2: 26, m = 3: 41, m = 4: 42, m = 5: 27, m = 6: 11, m = 7: 2. **Crossing every subgroup of Oh and Ih (DICTO: "cross all possible symmetry groups, see what falls out") gives 4553 Aequi in all**, complete for every subgroup class with one fixed point and at most 8 orbits, and capped at m ≤ 3 or m ≤ 4 for the rest (table below). Every one of the 4553 is confirmed to 80 digits (largest |Ω − 4π/N| = 6.9e-100). Every orbit set searched for a group with one fixed point (6684 sets) gave **exactly one** fair die; none gave 0 and none gave 2 or more. All controls pass: Equanimity's twelve with their symmetry (the 16-face tetrahedron–dodecahedron die under T, two hands), D191, and the 13 single-frame sets of the pilot.

Aequi by full symmetry group and m (every die counted once, under its full symmetry group; a chiral die counts once for its two hands):

| group | order | m=2 | m=3 | m=4 | m=5 | m=6 | m=7 | total |
|---|---|---|---|---|---|---|---|---|
| Ih | 120 | 3 | 1 |  |  |  |  | 4 |
| Oh | 48 | 3 | 1 |  |  |  |  | 4 |
| D10h | 40 | 1 |  |  |  |  |  | 1 |
| D8h | 32 | 1 |  |  |  |  |  | 1 |
| D6h | 24 | 2 |  |  |  |  |  | 2 |
| Td | 24 | 2 | 1 |  |  |  |  | 3 |
| Th | 24 | 10 | 17 | 14 | 5 | 1 |  | 47 |
| D5d | 20 | 18 | 34 | 34 | 19 | 7 |  | 112 |
| D5h | 20 | 1 |  |  |  |  |  | 1 |
| D4h | 16 | 6 | 7 | 4 |  |  |  | 17 |
| D3d | 12 | 41 | 91 | 129 |  |  |  | 261 |
| D3h | 12 | 1 |  |  |  |  |  | 1 |
| T | 12 | 8 | 21 | 28 | 22 | 10 | 2 | 91 |
| D5 | 10 | 5 | 15 | 20 | 15 | 6 | 1 | 62 |
| D2d | 8 | 8 | 10 | 8 | 1 |  |  | 27 |
| D2h | 8 | 49 | 183 | 606 | 8 | 2 |  | 848 |
| D3 | 6 | 26 | 97 | 220 | 1 |  |  | 344 |
| S6 | 6 | 27 | 166 | 501 |  |  |  | 694 |
| C2h | 4 | 77 | 766 | 45 |  |  |  | 888 |
| D2 | 4 | 20 | 147 | 682 | 6 | 2 |  | 857 |
| S4 | 4 | 1 | 3 | 3 | 1 |  |  | 8 |
| Ci | 2 |  | 280 |  |  |  |  | 280 |
| all | | 310 | 1840 | 2294 | 78 | 28 | 3 | 4553 |

Five groups in this list lie outside both frames: D3h, D5h, D6h (twice), D8h and D10h. These dice are prisms (triangular, pentagonal, hexagonal, octagonal, decagonal, and a 12-sided prism whose sides are not evenly spaced). Their caps and sides lie on frame axes, but the turn about the prism's axis is not a frame map. They were found under frame subgroups (for example the octagonal prism under D4h, D4, D2d and seven more; the 12-sided prism only under S6).

## Definition (fixed for this study)

An **Aequus** is a convex polyhedron S = {x : n·x ≤ d_k for n in O_k, k = 1..m}, where each O_k is a full orbit, under a point group G, of directions along symmetry axes of the cube frame or the icosahedron frame, one depth d_k per orbit, m ≥ 2, every face present, and fair under the solid-angle model: from the centre (the centroid) every face subtends 4π/N, N the number of faces. A die is listed once, under its full symmetry group, with m = the number of its face orbits under that group; a die with one orbit (face-transitive, fair by symmetry) is excluded.

- **Frames** (as in Equanimity): cube axes on the coordinate axes, 26 directions: C6 (±x, ±y, ±z), O8 (±1, ±1, ±1), RD12 (±1, ±1, 0 cyclic). Icosahedron with a 2-fold axis on each coordinate axis and vertices (0, ±φ, ±1) cyclic (the placement of Equanimity and D191), 62 directions: D12 (0, ±φ, ±1), I20 = O8 + I12 with I12 (0, ±1/φ, ±φ), RT30 = C6 + RT24 with RT24 (±1, ±φ, ±1/φ), all cyclic. Union: 74 directions. Counts checked in scripts/groups.py.
- **Groups**: all 98 subgroups of Oh and all 164 of Ih on these frames (236 different subgroups), each acting on the 74 directions; an orbit is admissible when it lies wholly in the frames. Subgroups were grouped into classes by conjugation with frame maps that carry the admissible directions onto each other (43 classes; a class whose admissible directions map into a larger class of the same group is searched there). The seven frame groups Oh, O, Td, Th, T, Ih, I are one class each.
- **Orbit names**: a family name alone (C6, O8, RD12, D12, I12, RT24) is that whole family; "X/k" is an orbit of k directions of family X; "X+Y/k" is an orbit of k directions taken from both X and Y (for example C6+RT24/30 is the triacontahedron's 30, O8+I12/20 the icosahedron's 20, C6+RT24/10 ten of them under D5d). When two dice of one group share a label, (1), (2), … tell them apart; the table gives a representative direction for every orbit, and data/dice/*.json the full list of face directions (indices into the 74 of scripts/groups.py).
- **Hands**: a die whose symmetry group has no mirror and no rotary reflection (T, D5 here) comes in a left and a right hand; it is listed once, "two hands". Repeats are removed by congruence (mirror images included), so the two hands are one entry.
- **Full symmetry group**: every isometry fixing the centroid that maps the face planes onto themselves (not only the 144 frame maps; this is how the prisms show symmetry outside the frames), named by its elements (scripts/groups.py, schoenflies).

## Method

1. **Orbits and subsets** (scripts/classes.py, log logs/classes.log, data/classes.json): for each class, the admissible orbits; orbit subsets with m ≥ 2 reduced by the class's normaliser (frame maps) and kept only when the face directions bound a solid.
2. **Double precision** (scripts/solve.py, driven by scripts/run.sh): first orbit at depth 1; the m − 1 equations "mean solid angle of orbit k = 4π/N" (k = 2..m) in the m − 1 free log-depths, solved by scipy's hybrid Powell method from a grid of starts on depth ratios 0.65–1.7 (21 starts for m = 2; 9², 6³, 4⁴, 3⁵ grids plus the centre for m = 3..6; 256 Sobol points plus the centre for m ≥ 7), search box depth ratios e^±1.5; a solution is kept when every face is within 1e-10 of 4π/N (then every face is present). Solid angles by Van Oosterom and Strackee's formula for a triangle (1983) on a fan from the face centre, as in Equanimity; corners by half-space intersection (qhull). The work ran in short chunks on two compute hosts (raw results data/raw/sol-*.jsonl).
3. **Classification** (scripts/collect.py, log logs/collect.log): centroid, full symmetry group, face orbits under it; depths averaged over each full orbit, solid rebuilt; repeats removed by congruence (scale-free depths and corner distances to 1e-6 within the same N, corner count, group and face sides). 11303 solutions → 8137 distinct solids: 4553 Aequi, 30 face-transitive, 3554 fair only about the frame centre (below).
4. **80 digits** (scripts/exact.py, logs/exact-summary.log, data/raw/exact.jsonl.gz): each Aequus re-solved with one depth per full orbit by mpmath's findroot at 100 working digits, corners by Cramer's rule from a triple of face planes at each corner (as in study 2026-11-19-aequus-rd-ico, rd_ico_exact.py); checks: every face |Ω − 4π/N| < 1e-50 (largest 6.9e-100), every corner on all its planes and inside all others to 1e-50 (largest 1.6e-100), and the symmetry group, corner count and orbit count recomputed from the refined depths (0 mismatches).
5. **Tables and controls** (scripts/make_table.py): data/table.csv and data/table.md (all 4553), data/table-frame-groups.md, data/counts.md, data/dice/*.json (one file per die: orbits, representative directions, faces by orbit, corners, depths to 60 digits, residuals, the groups and m under which the search met it), data/controls.log.
6. **Pictures** (scripts/render.py, from the refined corners): for each die a solid render (solid faces, crisp edges, neutral label tones per face orbit; colours are labels only) and its Vacuus (one plate from the centre to each edge; slate = sloping, pale sand = on a mirror plane of the die's own symmetry group), in the style of study 2026-11-19-aequus-rd-ico (panels a and b of its sheet). Contact sheets by group in figures/sheet-<group>[-p<page>].png (129 sheets, 40 dice per page). The 9106 single-die images (data/figures/, 43 MB) are not in git (.gitignore); render.py remakes them from data/raw/exact.jsonl.gz in about a minute on 22 cores.

Credit: the solid-angle formula is Van Oosterom and Strackee's (IEEE Trans. Biomed. Eng. BME-30 (1983) 125–126); the fairness model, the orbit-depth construction and the exact-check pattern are Equanimity's (paper #111 draft, after Rawlins and Diaconis–Keller as cited there).

## Search coverage (what is complete, what is capped)

| group | order | polar | conjugates | orbits | m searched | sets searched | sets with 0 fair dice | sets with 2 or more |
|---|---|---|---|---|---|---|---|---|
| Ih | 120 | no | 1 | 3 | 2–3 (all) | 4 | 0 | 0 |
| I | 60 | no | 1 | 3 | 2–3 (all) | 4 | 0 | 0 |
| Oh | 48 | no | 1 | 3 | 2–3 (all) | 4 | 0 | 0 |
| O | 24 | no | 1 | 3 | 2–3 (all) | 4 | 0 | 0 |
| Td | 24 | no | 1 | 4 | 2–4 (all) | 8 | 0 | 0 |
| Th | 24 | no | 1 | 6 | 2–6 (all) | 57 | 0 | 0 |
| D5d | 20 | no | 6 | 7 | 2–7 (all) | 120 | 0 | 0 |
| D4h | 16 | no | 3 | 5 | 2–5 (all) | 25 | 0 | 0 |
| D3d | 12 | no | 4 | 5 | 2–5 (all) | 26 | 0 | 0 |
| D3d | 12 | no | 10 | 9 | 2–4 (cap) | 246 | 0 | 0 |
| T | 12 | no | 1 | 8 | 2–8 (all) | 153 | 0 | 0 |
| C5v | 10 | yes | 6 | 13 | 2–3 (cap) | 131 | 10 | 0 |
| D5 | 10 | no | 6 | 8 | 2–8 (all) | 183 | 0 | 0 |
| S10 | 10 | no | 6 | 7 | 2–7 (all) | 120 | 0 | 0 |
| C4h | 8 | no | 3 | 5 | 2–5 (all) | 25 | 0 | 0 |
| C4v | 8 | yes | 3 | 8 | 2–4 (cap) | 59 | 4 | 0 |
| D2d | 8 | no | 3 | 6 | 2–6 (all) | 41 | 0 | 0 |
| D2d | 8 | no | 3 | 6 | 2–6 (all) | 41 | 0 | 0 |
| D2h | 8 | no | 3 | 7 | 2–7 (all) | 67 | 0 | 0 |
| D2h | 8 | no | 1 | 16 | 2–4 (cap) | 815 | 0 | 0 |
| D4 | 8 | no | 3 | 5 | 2–5 (all) | 25 | 0 | 0 |
| C3v | 6 | yes | 4 | 9 | 2–4 (cap) | 104 | 5 | 0 |
| C3v | 6 | yes | 10 | 17 | 2–3 (cap) | 295 | 18 | 0 |
| D3 | 6 | no | 4 | 6 | 2–6 (all) | 41 | 0 | 0 |
| D3 | 6 | no | 10 | 12 | 2–4 (cap) | 449 | 0 | 0 |
| S6 | 6 | no | 4 | 13 | 2–4 (cap) | 1078 | 0 | 0 |
| C5 | 5 | yes | 6 | 14 | 2–3 (cap) | 131 | 10 | 0 |
| C2h | 4 | no | 3 | 23 | 2–3 (cap) | 1009 | 0 | 0 |
| C2h | 4 | no | 6 | 9 | 2–4 (cap) | 134 | 0 | 0 |
| C2v | 4 | yes | 3 | 11 | 2–4 (cap) | 105 | 6 | 0 |
| C2v | 4 | yes | 3 | 27 | 2–3 (cap) | 914 | 70 | 0 |
| C2v | 4 | yes | 6 | 11 | 2–4 (cap) | 182 | 8 | 0 |
| C4 | 4 | yes | 3 | 8 | 2–4 (cap) | 59 | 4 | 0 |
| D2 | 4 | no | 3 | 8 | 2–8 (all) | 107 | 0 | 0 |
| D2 | 4 | no | 1 | 20 | 2–4 (cap) | 1196 | 0 | 0 |
| S4 | 4 | no | 3 | 7 | 2–7 (all) | 65 | 0 | 0 |
| C3 | 3 | yes | 4 | 26 | 2–3 (cap) | 912 | 42 | 0 |
| C2 | 2 | yes | 3 | 38 | 2–3 (cap) | 1349 | 60 | 0 |
| C2 | 2 | yes | 6 | 14 | 2–3 (cap) | 59 | 2 | 0 |
| Ci | 2 | no | 1 | 37 | 2–3 (cap) | 637 | 0 | 0 |
| Cs | 2 | yes | 3 | 45 | 2–3 (cap) | 615 | 77 | 0 |
| Cs | 2 | yes | 6 | 17 | 2–3 (cap) | 23 | 3 | 0 |
| C1 | 1 | yes | 1 | 74 | 2–3 (cap) | 0 | 0 | 0 |

"Polar" groups (C_n, C_nv, C_s, C_1) fix a whole line or plane, so their centroid need not be the frame centre. The search there solves fairness about the frame centre. A solution is an Aequus only when its centroid is the centre, and that happened only for dice whose full symmetry has one fixed point (they are counted under that group: for example the prisms, also met under C5, C4v and C3v). The other 3554 solids have their centroid off the centre (smallest offset 6.1e-5), so they are not Aequi; 319 polar sets have no frame-centre solution in the box. This is what counting predicts: a translation along the polar axis keeps one depth per orbit, so the shape has m − 2 (C_n, C_nv) or fewer free parameters against m − 1 fairness equations. They are listed in data/not-aequi.csv with the 30 face-transitive solids. C1 needs m ≥ 4 to bound a solid, so under the cap m ≤ 3 it was not searched at all.

Caps, exactly: complete (every m) for Ih, I, Oh, O, Td, Th, T, D5d, D4h, D3d (5 orbits), D5, S10, C4h, D2d (both classes), D2h (7 orbits), D4, D3 (6 orbits), D2 (8 orbits), S4; m ≤ 4 for D3d (9 orbits), C4v, D2h (16 orbits), C3v (9 orbits), D3 (12 orbits), S6, C2h (9 orbits), C2v (11 orbits, both classes), C4, D2 (20 orbits); m ≤ 3 for C5v, C3v (17 orbits), C5, C2h (23 orbits), C2v (27 orbits), C3, C2 (both classes), Ci, Cs (both classes), C1. A die whose full group is one of the capped classes can have more orbits than the cap; those are not covered. The low groups are large because almost every orbit set gives a die: under Ci alone there are 2^37 sets of antipodal pairs.

## Controls

- **Equanimity's twelve** (paper #111 draft, Table 1), each found under its own group, μ_f (the larger family's depth over the smaller's) to 10 digits: T ∩ C 1.0659165951 (Td), C ∩ O 1.0141631690 (Oh), T ∩ RD 1.0692105364 (Td), T ∩ D 1.0603736500 (T, two hands), C ∩ RD 1.0312505091 (Oh), C ∩ D 1.0384442830 (Th), O ∩ RD 1.0370247603 (Oh), O ∩ D 1.0265315223 (Th), RD ∩ D 0.9991525381 (Th), D ∩ I 1.0043619497 (Ih), D ∩ RT 1.0072683224 (Ih), I ∩ RT 1.0155843036 (Ih): all PASS.
- **D191** (study 2026-11-19-aequus-rd-ico): Th: O8 + RD12 + I12, with RD at 1: m1 = 1.0027592509652673651138588224943292169120, m2 = 1.0106639425964276013947211797925550524897, equal to that study's 100-digit values in all 40 digits shown: PASS.
- **The pilot** (study 2026-11-19-aequi-three-families, run1.log): all 13 of its 20 sets that lie in one icosahedron placement agree to 9 digits (one, C6 + O8 + RD12, has the full symmetry Oh). Its other 7 sets (C6+D12+I12, C6+D12+RT24, O8+D12+I12, O8+D12+RT24, RD12+D12+I12, RD12+D12+RT24, D12+I12+RT24) are **not comparable**: the pilot's D12 = (0, ±1, ±φ) cyclic belongs to the other placement of the icosahedron (turned a quarter turn about z), while its I12 and RT24 belong to this one, so those 7 dice mix the two placements and lie outside this definition (here the same seven labels give other depths, e.g. Th: C6 + D12 + I12 at 1, 1.0669683174, 1.0361157931 against the pilot's 1, 1.035081866, 1.008326858). Details in data/controls.log.

## What stood out

- Every searched set for a group with a single fixed point had exactly one fair die (6684 sets), as on Equanimity's lines; this is observed in the search box, not proved.
- No die has exactly the symmetry O, I, S10, C4h or D4: every fair die of their orbit sets has more symmetry (for O and I always Oh and Ih).
- Chiral dice: T (91) and D5 (62), two hands each; none for O or I, since the axis orbits of O and I are those of Oh and Ih.
- Fair prisms with symmetry beyond the frames (D3h, D5h, D6h twice, D8h, D10h).
- Under the low groups many dice are very long or flat (a sliver parallelepiped when three axis pairs are nearly coplanar); on the sheets these look small because every die is framed by its circumsphere.

## Not covered

- Face directions off the symmetry axes (infinite families), and frames other than these two placed this way.
- The other icosahedron placement together with this one: Th and T keep both, which would add the orbits D12′, I12′, RT24′ (the pilot's 7 cross-frame sets live there).
- Orbit sets above the caps listed above; dice with depth ratios outside e^±1.5 of the first orbit; more than one fair die per set outside the grid of starts (none was seen inside it).
- Other fairness models (face areas, rolling dynamics, non-uniform density); here only the solid-angle model about the centroid.
- Closed forms: the values are numerical to 80 digits, not exact algebraic numbers.
- Whether any of these dice appears in earlier catalogues was not checked here; nothing here is a priority claim.

## Files

scripts/: groups.py (frames, groups, naming), classes.py, solve.py + run.sh, collect.py, exact.py + run_exact.sh, make_table.py, render.py. data/: classes.json, plan.json (the (class, m) pairs searched), search-status.json, table.csv, table.md, table-frame-groups.md, counts.md, controls.log, not-aequi.csv, dice/ (4553 files), raw/ (double-precision solutions, 80-digit records). figures/: contact sheets. logs/: classes.log, collect.log, exact-summary.log.

## The 155 Aequi with a frame-group or prism symmetry

| row | group | orbits (representative direction) | N | faces by orbit | corners | depths (first orbit = 1) | hands |
|---|---|---|---|---|---|---|---|
| 3 | Ih | O8+I12/20 (φ, 0, 1/φ) + D12 (φ, 1, 0) | 32 | 20×6-gon; 12×5-gon | 60 | 1.0, 0.9956569942691 | one |
| 4 | Ih | C6+RT24/30 (1, 0, 0) + D12 (φ, 1, 0) | 42 | 30×6-gon; 12×5-gon | 80 | 1.0, 0.9927841249484 | one |
| 5 | Ih | C6+RT24/30 (1, 0, 0) + O8+I12/20 (φ, 0, 1/φ) | 50 | 30×6-gon; 20×3-gon | 72 | 1.0, 0.9846548399995 | one |
| 6 | Ih | C6+RT24/30 (1, 0, 0) + O8+I12/20 (φ, 0, 1/φ) + D12 (φ, 1, 0) | 62 | 30×4-gon; 20×6-gon; 12×10-gon | 120 | 1.0, 0.9931733996341, 1.022360768955 | one |
| 10 | Oh | C6 (1, 0, 0) + O8 (1, 1, 1) | 14 | 6×4-gon; 8×6-gon | 24 | 1.0, 1.014163169042 | one |
| 11 | Oh | C6 (1, 0, 0) + RD12 (1, 1, 0) | 18 | 6×4-gon; 12×6-gon | 32 | 1.0, 1.03125050913 | one |
| 12 | Oh | O8 (1, 1, 1) + RD12 (1, 1, 0) | 20 | 8×3-gon; 12×6-gon | 30 | 1.0, 1.037024760344 | one |
| 13 | Oh | C6 (1, 0, 0) + O8 (1, 1, 1) + RD12 (1, 1, 0) | 26 | 6×8-gon; 8×6-gon; 12×4-gon | 48 | 1.0, 0.9638135278296, 0.9716263726608 | one |
| 14 | D10h | C6+RT24/10 (1, φ, 1/φ) + D12/2 (φ, -1, 0) | 12 | 10×4-gon; 2×10-gon | 20 | 1.0, 1.532998628936 | one |
| 15 | D8h | C6+RD12/8 (1, 0, 0) + C6/2 (0, 0, 1) | 10 | 8×4-gon; 2×8-gon | 16 | 1.0, 1.368952902366 | one |
| 16 | D6h | O8/2 (1, 1, -1) + RD12/6 (1, 0, 1) | 8 | 2×6-gon; 6×4-gon | 12 | 1.0, 0.8408964152537 | one |
| 17 | D6h | O8/2 (1, 1, 1) + RD12+RT24/12 (φ, -1/φ, -1) | 14 | 2×12-gon; 12×4-gon | 24 | 1.0, 0.5925816042604 | one |
| 19 | Td | C6 (1, 0, 0) + O8/4 (1, 1, 1) | 10 | 6×6-gon; 4×3-gon | 16 | 1.0, 0.9381597064759 | one |
| 20 | Td | O8/4 (1, 1, 1) + RD12 (1, 1, 0) | 16 | 4×3-gon; 12×5-gon | 22 | 1.0, 1.069210536393 | one |
| 21 | Td | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) | 22 | 6×6-gon; 4×6-gon; 12×5-gon | 40 | 1.0, 0.967692280769, 0.9998555457545 | one |
| 24 | Th | C6 (1, 0, 0) + D12 (φ, 1, 0) | 18 | 6×4-gon; 12×6-gon | 32 | 1.0, 1.038444283009 | one |
| 25 | Th | C6 (1, 0, 0) + I12 (φ, 0, 1/φ) | 18 | 6×4-gon; 12×6-gon | 32 | 1.0, 1.043588041409 | one |
| 26 | Th | O8 (1, 1, 1) + D12 (φ, 1, 0) | 20 | 8×3-gon; 12×7-gon | 36 | 1.0, 1.026531522328 | one |
| 27 | Th | RD12 (1, 1, 0) + D12 (φ, 1, 0) | 24 | 12×7-gon; 12×4-gon | 44 | 1.0, 0.9991525380596 | one |
| 28 | Th | RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) | 24 | 12×7-gon; 12×4-gon | 44 | 1.0, 0.9836977002664 | one |
| 29 | Th | D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) | 24 | 12×7-gon; 12×4-gon | 44 | 1.0, 0.9863823179596 | one |
| 30 | Th | O8 (1, 1, 1) + RT24 (φ, 1/φ, 1) | 32 | 8×3-gon; 24×5-gon | 42 | 1.0, 1.038109322973 | one |
| 31 | Th | RD12 (1, 1, 0) + RT24 (φ, 1/φ, 1) | 36 | 12×4-gon; 24×6-gon | 62 | 1.0, 1.015846031373 | one |
| 32 | Th | D12 (φ, 1, 0) + RT24 (φ, 1/φ, 1) | 36 | 12×5-gon; 24×5-gon | 56 | 1.0, 0.9993600650237 | one |
| 33 | Th | I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 36 | 12×3-gon; 24×5-gon | 44 | 1.0, 1.013149939243 | one |
| 34 | Th | C6 (1, 0, 0) + O8 (1, 1, 1) + D12 (φ, 1, 0) | 26 | 6×8-gon; 8×6-gon; 12×4-gon | 48 | 1.0, 0.9942933280562, 0.9904224888752 | one |
| 35 | Th | C6 (1, 0, 0) + O8 (1, 1, 1) + I12 (φ, 0, 1/φ) | 26 | 6×8-gon; 8×6-gon; 12×4-gon | 48 | 1.0, 1.04848769982, 1.012801305898 | one |
| 36 | Th | C6 (1, 0, 0) + RD12 (1, 1, 0) + D12 (φ, 1, 0) | 30 | 6×4-gon; 12×8-gon; 12×4-gon | 56 | 1.0, 1.007009288647, 0.9967240546433 | one |
| 37 | Th | C6 (1, 0, 0) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) | 30 | 6×4-gon; 12×8-gon; 12×4-gon | 56 | 1.0, 1.060203478247, 1.020043217505 | one |
| 38 | Th | C6 (1, 0, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) | 30 | 6×4-gon; 12×8-gon; 12×4-gon | 56 | 1.0, 1.066968317429, 1.036115793084 | one |
| 39 | Th | O8 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) | 32 | 8×6-gon; 12×5-gon; 12×6-gon | 60 | 1.0, 0.9967875911895, 1.007795782095 | one |
| 40 | Th | O8 (1, 1, 1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) | 32 | 8×6-gon; 12×5-gon; 12×6-gon | 60 | 1.0, 0.997248341551, 1.00788294062 | one |
| 41 | Th | RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) | 36 | 12×8-gon; 12×5-gon; 12×4-gon | 68 | 1.0, 0.9984588810196, 1.003655968904 | one |
| 42 | Th | C6 (1, 0, 0) + O8 (1, 1, 1) + RT24 (φ, 1/φ, 1) | 38 | 6×4-gon; 8×3-gon; 24×6-gon | 60 | 1.0, 0.9493302174968, 0.9765456150849 | one |
| 43 | Th | C6 (1, 0, 0) + RD12 (1, 1, 0) + RT24 (φ, 1/φ, 1) | 42 | 6×6-gon; 12×5-gon; 24×6-gon | 80 | 1.0, 0.9683433597944, 0.9754146002513 | one |
| 44 | Th | C6 (1, 0, 0) + I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 42 | 6×10-gon; 12×3-gon; 24×6-gon | 80 | 1.0, 0.9901271969565, 1.020424343074 | one |
| 45 | Th | O8 (1, 1, 1) + RD12 (1, 1, 0) + RT24 (φ, 1/φ, 1) | 44 | 8×6-gon; 12×6-gon; 24×5-gon | 78 | 1.0, 1.021684478821, 1.025098978348 | one |
| 46 | Th | O8 (1, 1, 1) + D12 (φ, 1, 0) + RT24 (φ, 1/φ, 1) | 44 | 8×6-gon; 12×7-gon; 24×4-gon | 72 | 1.0, 1.041053816844, 1.023328015147 | one |
| 47 | Th | O8 (1, 1, 1) + I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 44 | 8×3-gon; 12×3-gon; 24×6-gon | 60 | 1.0, 1.022982967657, 1.02140047185 | one |
| 48 | Th | RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24 (φ, 1/φ, 1) | 48 | 12×5-gon; 12×4-gon; 24×6-gon | 80 | 1.0, 1.015653709281, 1.025675653606 | one |
| 49 | Th | RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 48 | 12×7-gon; 12×6-gon; 24×5-gon | 92 | 1.0, 1.0023723013, 0.9988038972191 | one |
| 50 | Th | D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 48 | 12×7-gon; 12×6-gon; 24×5-gon | 92 | 1.0, 0.9881711268513, 0.9907277193236 | one |
| 51 | Th | C6 (1, 0, 0) + O8 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) | 38 | 6×4-gon; 8×6-gon; 12×6-gon; 12×6-gon | 72 | 1.0, 0.9930534440236, 0.9775211063955, 0.9755781388101 | one |
| 52 | Th | C6 (1, 0, 0) + O8 (1, 1, 1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) | 38 | 6×4-gon; 8×6-gon; 12×6-gon; 12×6-gon | 72 | 1.0, 1.038275917962, 1.024923205746, 1.007552986778 | one |
| 53 | Th | C6 (1, 0, 0) + O8 (1, 1, 1) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) | 38 | 6×4-gon; 8×6-gon; 12×6-gon; 12×6-gon | 72 | 1.0, 1.057237914651, 1.039301164735, 1.024146088379 | one |
| 54 | Th | C6 (1, 0, 0) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) | 42 | 6×4-gon; 12×8-gon; 12×6-gon; 12×4-gon | 80 | 1.0, 1.033671624228, 1.029471560543, 1.01930314372 | one |
| 55 | Th | O8 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) | 44 | 8×9-gon; 12×4-gon; 12×5-gon; 12×6-gon | 84 | 1.0, 0.9690215557093, 0.9759397165013, 0.992010775406 | one |
| 56 | Th | C6 (1, 0, 0) + O8 (1, 1, 1) + RD12 (1, 1, 0) + RT24 (φ, 1/φ, 1) | 50 | 6×6-gon; 8×6-gon; 12×7-gon; 24×5-gon | 96 | 1.0, 0.9415500592052, 0.9621274064435, 0.9577896743151 | one |
| 57 | Th | C6 (1, 0, 0) + O8 (1, 1, 1) + D12 (φ, 1, 0) + RT24 (φ, 1/φ, 1) | 50 | 6×6-gon; 8×6-gon; 12×7-gon; 24×5-gon | 96 | 1.0, 0.9611215105601, 0.9876172990901, 0.9776093741754 | one |
| 58 | Th | C6 (1, 0, 0) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24 (φ, 1/φ, 1) | 54 | 6×6-gon; 12×5-gon; 12×4-gon; 24×7-gon | 104 | 1.0, 0.9599579510647, 0.9666820005446, 0.983126597182 | one |
| 59 | Th | C6 (1, 0, 0) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 54 | 6×8-gon; 12×6-gon; 12×4-gon; 24×6-gon | 104 | 1.0, 1.008371651487, 0.9879540525928, 1.005539345908 | one |
| 60 | Th | C6 (1, 0, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 54 | 6×4-gon; 12×8-gon; 12×6-gon; 24×5-gon | 104 | 1.0, 1.028012082231, 1.000177815479, 1.020424515335 | one |
| 61 | Th | O8 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24 (φ, 1/φ, 1) | 56 | 8×6-gon; 12×7-gon; 12×4-gon; 24×5-gon | 96 | 1.0, 0.9997648718391, 1.018172420447, 1.01363171666 | one |
| 62 | Th | O8 (1, 1, 1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 56 | 8×6-gon; 12×9-gon; 12×6-gon; 24×4-gon | 108 | 1.0, 1.024081449797, 1.027511805662, 1.011306439634 | one |
| 63 | Th | O8 (1, 1, 1) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 56 | 8×6-gon; 12×8-gon; 12×5-gon; 24×5-gon | 108 | 1.0, 1.035329885107, 1.021033889892, 1.011094262805 | one |
| 64 | Th | RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 60 | 12×6-gon; 12×5-gon; 12×6-gon; 24×6-gon | 116 | 1.0, 1.011336762076, 1.021265331892, 1.01777507761 | one |
| 65 | Th | C6 (1, 0, 0) + O8 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) | 50 | 6×4-gon; 8×9-gon; 12×4-gon; 12×6-gon; 12×6-gon | 96 | 1.0, 1.049311936327, 1.008532768053, 1.01186927297, 1.012408393888 | one |
| 66 | Th | C6 (1, 0, 0) + O8 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24 (φ, 1/φ, 1) | 62 | 6×6-gon; 8×9-gon; 12×5-gon; 12×6-gon; 24×5-gon | 120 | 1.0, 0.9576962463915, 0.9539451887428, 0.9640174037018, 0.9659972683458 | one |
| 67 | Th | C6 (1, 0, 0) + O8 (1, 1, 1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 62 | 6×8-gon; 8×6-gon; 12×8-gon; 12×4-gon; 24×5-gon | 120 | 1.0, 0.9794702966212, 1.000992651576, 0.9825580937355, 0.9862383919143 | one |
| 68 | Th | C6 (1, 0, 0) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 66 | 6×4-gon; 12×6-gon; 12×6-gon; 12×6-gon; 24×6-gon | 128 | 1.0, 0.9938000038986, 1.001996180591, 0.9964737575115, 1.011390165389 | one |
| 69 | Th | O8 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 68 | 8×6-gon; 12×8-gon; 12×5-gon; 12×6-gon; 24×5-gon | 132 | 1.0, 0.9985789439037, 1.012199589392, 1.020595847824, 1.004088174853 | one |
| 70 | Th | C6 (1, 0, 0) + O8 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24 (φ, 1/φ, 1) | 74 | 6×4-gon; 8×6-gon; 12×8-gon; 12×6-gon; 12×6-gon; 24×5-gon | 144 | 1.0, 0.9915698110406, 0.9873288586034, 0.9977625508798, 0.9910812526312, 0.9923057117338 | one |
| 188 | D5h | C6+RT24/5 (1, 0, 0) + D12/2 (0, φ, 1) | 7 | 5×4-gon; 2×5-gon | 10 | 1.0, 1.094200283706 | one |
| 477 | D3h | O8/2 (1, 1, 1) + RD12/3 (1, -1, 0) | 5 | 2×3-gon; 3×4-gon | 6 | 1.0, 1.082044543099 | one |
| 479 | T | O8/4 (1, 1, 1) + D12 (φ, 1, 0) | 16 | 4×3-gon; 12×6-gon | 28 | 1.0, 1.060373650001 | two |
| 480 | T | O8/4 (1, 1, 1) + RT24/12 (φ, 1/φ, 1) | 16 | 4×3-gon; 12×6-gon | 28 | 1.0, 1.090358172872 | two |
| 481 | T | O8/4 (1, 1, 1) + I12 (φ, 0, 1/φ) | 16 | 4×6-gon; 12×5-gon | 28 | 1.0, 1.038136605181 | two |
| 482 | T | O8/4 (1, 1, 1) + RT24/12 (φ, 1/φ, -1) | 16 | 4×6-gon; 12×5-gon | 28 | 1.0, 0.9481107974245 | two |
| 483 | T | C6 (1, 0, 0) + RT24/12 (φ, 1/φ, 1) | 18 | 6×4-gon; 12×6-gon | 32 | 1.0, 0.9708071293056 | two |
| 484 | T | RD12 (1, 1, 0) + RT24/12 (φ, 1/φ, 1) | 24 | 12×5-gon; 12×6-gon | 44 | 1.0, 0.9741904636653 | two |
| 485 | T | D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, 1) | 24 | 12×6-gon; 12×5-gon | 44 | 1.0, 0.9640246727327 | two |
| 486 | T | I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 24 | 12×6-gon; 12×5-gon | 44 | 1.0, 0.9629476633152 | two |
| 487 | T | O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + RT24/12 (φ, 1/φ, 1) | 20 | 4×3-gon; 4×6-gon; 12×6-gon | 36 | 1.0, 1.193412439274, 1.070466269319 | two |
| 488 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + D12 (φ, 1, 0) | 22 | 6×6-gon; 4×6-gon; 12×5-gon | 40 | 1.0, 0.9914853472052, 1.012986578826 | two |
| 489 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + I12 (φ, 0, 1/φ) | 22 | 6×6-gon; 4×6-gon; 12×5-gon | 40 | 1.0, 1.035214301594, 1.027191022687 | two |
| 490 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RT24/12 (φ, 1/φ, -1) | 22 | 6×6-gon; 4×6-gon; 12×5-gon | 40 | 1.0, 1.063379673548, 0.9783637701025 | two |
| 491 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RT24/12 (φ, 1/φ, 1) | 22 | 6×4-gon; 4×3-gon; 12×7-gon | 40 | 1.0, 0.8881113570984, 0.9440449399819 | two |
| 492 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) | 28 | 4×6-gon; 12×6-gon; 12×5-gon | 52 | 1.0, 1.014172379288, 1.018501357565 | two |
| 493 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) | 28 | 4×6-gon; 12×6-gon; 12×5-gon | 52 | 1.0, 1.017519123317, 1.013468053749 | two |
| 494 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + RT24/12 (φ, 1/φ, 1) | 28 | 4×6-gon; 12×6-gon; 12×5-gon | 52 | 1.0, 1.103200398997, 1.047987371641 | two |
| 495 | T | O8/4 (1, 1, 1) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) | 28 | 4×6-gon; 12×6-gon; 12×5-gon | 52 | 1.0, 1.01659169785, 1.010869290088 | two |
| 496 | T | O8/4 (1, 1, 1) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, 1) | 28 | 4×6-gon; 12×6-gon; 12×5-gon | 52 | 1.0, 1.11631552686, 1.048143659627 | two |
| 497 | T | O8/4 (1, 1, 1) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, -1) | 28 | 4×6-gon; 12×5-gon; 12×6-gon | 52 | 1.0, 0.9887981098129, 0.9779721855922 | two |
| 498 | T | O8/4 (1, 1, 1) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, -1) | 28 | 4×6-gon; 12×5-gon; 12×6-gon | 52 | 1.0, 0.956373316697, 0.9429514567961 | two |
| 499 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + RT24/12 (φ, 1/φ, -1) | 28 | 4×3-gon; 12×6-gon; 12×6-gon | 52 | 1.0, 0.9978127172269, 0.9963493715034 | two |
| 500 | T | O8/4 (1, 1, 1) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 28 | 4×3-gon; 12×6-gon; 12×6-gon | 52 | 1.0, 1.113309983072, 1.046231893904 | two |
| 501 | T | O8/4 (1, 1, 1) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 28 | 4×3-gon; 12×7-gon; 12×5-gon | 52 | 1.0, 1.046231893904, 1.087749749422 | two |
| 502 | T | C6 (1, 0, 0) + RD12 (1, 1, 0) + RT24/12 (φ, 1/φ, 1) | 30 | 6×6-gon; 12×6-gon; 12×5-gon | 56 | 1.0, 1.00266817557, 0.9618304932137 | two |
| 503 | T | C6 (1, 0, 0) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, 1) | 30 | 6×4-gon; 12×6-gon; 12×6-gon | 56 | 1.0, 1.023547669489, 0.9894898732471 | two |
| 504 | T | C6 (1, 0, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 30 | 6×6-gon; 12×4-gon; 12×5-gon | 44 | 1.0, 1.01493580274, 1.0 | two |
| 505 | T | RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, 1) | 36 | 12×6-gon; 12×5-gon; 12×6-gon | 68 | 1.0, 1.007840272833, 0.9990709623729 | two |
| 506 | T | RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 36 | 12×6-gon; 12×5-gon; 12×6-gon | 68 | 1.0, 0.9899506508053, 0.96587255231 | two |
| 507 | T | D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 36 | 12×7-gon; 12×5-gon; 12×5-gon | 68 | 1.0, 0.9849891906651, 0.9601750629592 | two |
| 508 | T | C6 (1, 0, 0) + O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + RT24/12 (φ, 1/φ, 1) | 26 | 6×6-gon; 4×3-gon; 4×6-gon; 12×6-gon | 48 | 1.0, 0.9013208673444, 1.080841143139, 0.9473548590179 | two |
| 509 | T | O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + RD12 (1, 1, 0) + RT24/12 (φ, 1/φ, 1) | 32 | 4×6-gon; 4×3-gon; 12×7-gon; 12×5-gon | 60 | 1.0, 1.084088139948, 1.067469200353, 1.041391517164 | two |
| 510 | T | O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 32 | 4×3-gon; 4×6-gon; 12×5-gon; 12×7-gon | 60 | 1.0, 1.145394821267, 1.079271082799, 1.038109322973 | two |
| 511 | T | O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, 1) | 32 | 4×6-gon; 4×6-gon; 12×6-gon; 12×5-gon | 60 | 1.0, 1.106962578243, 1.080229971195, 1.041073980791 | two |
| 512 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) | 34 | 6×4-gon; 4×6-gon; 12×7-gon; 12×5-gon | 64 | 1.0, 0.993976051661, 0.9914816416209, 0.9848242180176 | two |
| 513 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) | 34 | 6×4-gon; 4×6-gon; 12×7-gon; 12×5-gon | 64 | 1.0, 1.038791572109, 1.042545934188, 1.012832540961 | two |
| 514 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) | 34 | 6×4-gon; 4×6-gon; 12×7-gon; 12×5-gon | 64 | 1.0, 1.053572803691, 1.052909373512, 1.029050938702 | two |
| 515 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, 1) | 34 | 6×4-gon; 4×6-gon; 12×7-gon; 12×5-gon | 64 | 1.0, 0.931704933621, 1.025341651396, 0.9646747016755 | two |
| 516 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + RT24/12 (φ, 1/φ, 1) | 34 | 6×6-gon; 4×6-gon; 12×7-gon; 12×4-gon | 64 | 1.0, 0.9076958560999, 1.002912143728, 0.9392522635954 | two |
| 517 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + RT24/12 (φ, 1/φ, -1) | 34 | 6×8-gon; 4×6-gon; 12×5-gon; 12×5-gon | 64 | 1.0, 0.9947755938152, 0.9744464930043, 0.9581885395027 | two |
| 518 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, -1) | 34 | 6×6-gon; 4×9-gon; 12×4-gon; 12×6-gon | 64 | 1.0, 1.033665971764, 0.9995287745779, 0.9914659084366 | two |
| 519 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 34 | 6×6-gon; 4×3-gon; 12×5-gon; 12×7-gon | 64 | 1.0, 0.9407270633548, 1.012707577198, 0.9733291299734 | two |
| 520 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, -1) | 34 | 6×10-gon; 4×6-gon; 12×4-gon; 12×5-gon | 64 | 1.0, 1.073835553726, 1.002092684464, 1.007204094229 | two |
| 521 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 34 | 6×4-gon; 4×3-gon; 12×7-gon; 12×6-gon | 64 | 1.0, 0.9357013381501, 0.9681292320099, 1.008936628208 | two |
| 522 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) | 40 | 4×9-gon; 12×6-gon; 12×5-gon; 12×5-gon | 76 | 1.0, 0.9808694083227, 0.9830766900278, 0.9939084789288 | two |
| 523 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, 1) | 40 | 4×9-gon; 12×6-gon; 12×6-gon; 12×4-gon | 76 | 1.0, 1.049873599146, 1.059382468363, 1.027936112762 | two |
| 524 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, -1) | 40 | 4×6-gon; 12×5-gon; 12×6-gon; 12×6-gon | 76 | 1.0, 0.973925496699, 0.9875236178282, 0.9858177330775 | two |
| 525 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, -1) | 40 | 4×6-gon; 12×6-gon; 12×6-gon; 12×5-gon | 76 | 1.0, 0.9755302251402, 0.9803106822316, 0.9594858643403 | two |
| 526 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 40 | 4×6-gon; 12×5-gon; 12×6-gon; 12×6-gon | 76 | 1.0, 1.034107283911, 1.029662179558, 1.057506970478 | two |
| 527 | T | O8/4 (1, 1, 1) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, -1) | 40 | 4×6-gon; 12×6-gon; 12×6-gon; 12×5-gon | 76 | 1.0, 0.9738570618471, 0.9686922003208, 0.9509947619847 | two |
| 528 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 40 | 4×6-gon; 12×7-gon; 12×5-gon; 12×5-gon | 76 | 1.0, 1.08506460669, 1.073127194602, 1.026081148742 | two |
| 529 | T | O8/4 (1, 1, 1) + D12 (φ, 1, 0) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 40 | 4×6-gon; 12×7-gon; 12×5-gon; 12×5-gon | 76 | 1.0, 1.052540538456, 1.028203541478, 1.057638349151 | two |
| 530 | T | O8/4 (1, 1, 1) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 40 | 4×6-gon; 12×8-gon; 12×5-gon; 12×4-gon | 76 | 1.0, 1.093330605141, 1.07471841514, 1.026158297522 | two |
| 531 | T | O8/4 (1, 1, 1) + I12 (φ, 0, 1/φ) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 40 | 4×3-gon; 12×4-gon; 12×8-gon; 12×6-gon | 76 | 1.0, 1.037217261457, 1.02604809979, 1.060269763919 | two |
| 532 | T | C6 (1, 0, 0) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, 1) | 42 | 6×6-gon; 12×6-gon; 12×5-gon; 12×6-gon | 80 | 1.0, 0.9842367396838, 0.9831376652091, 0.9790365243364 | two |
| 533 | T | C6 (1, 0, 0) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 42 | 6×6-gon; 12×7-gon; 12×4-gon; 12×6-gon | 80 | 1.0, 1.033411682106, 1.001170151458, 0.9996746099753 | two |
| 534 | T | C6 (1, 0, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 42 | 6×6-gon; 12×7-gon; 12×4-gon; 12×6-gon | 80 | 1.0, 1.044809609123, 1.013843902362, 1.010434799703 | two |
| 535 | T | RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 48 | 12×7-gon; 12×5-gon; 12×5-gon; 12×6-gon | 92 | 1.0, 1.004482514279, 1.010267530121, 0.9936572083486 | two |
| 536 | T | C6 (1, 0, 0) + O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + RD12 (1, 1, 0) + RT24/12 (φ, 1/φ, 1) | 38 | 6×8-gon; 4×6-gon; 4×6-gon; 12×6-gon; 12×4-gon | 72 | 1.0, 0.9103806982044, 1.005662910848, 0.9749989017551, 0.9370981098648 | two |
| 537 | T | C6 (1, 0, 0) + O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, 1) | 38 | 6×4-gon; 4×6-gon; 4×6-gon; 12×6-gon; 12×6-gon | 72 | 1.0, 0.9394121250094, 1.046060476477, 1.001582025241, 0.9679124690621 | two |
| 538 | T | C6 (1, 0, 0) + O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 38 | 6×6-gon; 4×3-gon; 4×6-gon; 12×4-gon; 12×8-gon | 72 | 1.0, 0.9539802910377, 1.084744616583, 1.000297218757, 0.9813289969287 | two |
| 539 | T | O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, 1) | 44 | 4×9-gon; 4×6-gon; 12×5-gon; 12×7-gon; 12×4-gon | 84 | 1.0, 1.068009149759, 1.03069360779, 1.046706076587, 1.023823836337 | two |
| 540 | T | O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 44 | 4×6-gon; 4×6-gon; 12×6-gon; 12×6-gon; 12×5-gon | 84 | 1.0, 1.096307585933, 1.059907551245, 1.064260672146, 1.021677241594 | two |
| 541 | T | O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 44 | 4×6-gon; 4×6-gon; 12×7-gon; 12×6-gon; 12×4-gon | 84 | 1.0, 1.109012720477, 1.06997336644, 1.062073582398, 1.021693196357 | two |
| 542 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) | 46 | 6×4-gon; 4×9-gon; 12×6-gon; 12×6-gon; 12×5-gon | 88 | 1.0, 1.051081172861, 1.021139582323, 1.020285208309, 1.015504230185 | two |
| 543 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, 1) | 46 | 6×6-gon; 4×9-gon; 12×7-gon; 12×5-gon; 12×4-gon | 88 | 1.0, 0.9389331870817, 0.983220655597, 0.9839083796359, 0.9579777713695 | two |
| 544 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, -1) | 46 | 6×6-gon; 4×6-gon; 12×6-gon; 12×5-gon; 12×6-gon | 88 | 1.0, 1.005087500612, 0.9699593920182, 0.9733610642667, 0.977189855114 | two |
| 545 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, -1) | 46 | 6×6-gon; 4×6-gon; 12×6-gon; 12×5-gon; 12×6-gon | 88 | 1.0, 1.048941890608, 1.016752642831, 0.9970353403228, 0.9994952135672 | two |
| 546 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 46 | 6×6-gon; 4×6-gon; 12×6-gon; 12×5-gon; 12×6-gon | 88 | 1.0, 0.9330466869543, 0.9657296236496, 0.9523626493964, 0.9812038151515 | two |
| 547 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, -1) | 46 | 6×6-gon; 4×6-gon; 12×6-gon; 12×5-gon; 12×6-gon | 88 | 1.0, 1.069240795836, 1.032980433169, 1.010293640107, 1.013219112486 | two |
| 548 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + D12 (φ, 1, 0) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 46 | 6×6-gon; 4×6-gon; 12×6-gon; 12×5-gon; 12×6-gon | 88 | 1.0, 0.9536377659581, 0.9907057239378, 0.9735735987395, 1.004371751675 | two |
| 549 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 46 | 6×6-gon; 4×3-gon; 12×7-gon; 12×4-gon; 12×7-gon | 88 | 1.0, 0.9568559414828, 1.030395109028, 0.9983512021562, 0.9753479655008 | two |
| 550 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 46 | 6×6-gon; 4×6-gon; 12×8-gon; 12×4-gon; 12×5-gon | 88 | 1.0, 0.9658323212915, 1.041858317513, 1.009562347165, 0.9845165315463 | two |
| 551 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + I12 (φ, 0, 1/φ) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 46 | 6×8-gon; 4×3-gon; 12×3-gon; 12×8-gon; 12×6-gon | 88 | 1.0, 0.9752419844752, 0.9875655468131, 0.9940893338185, 1.026405684067 | two |
| 552 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 52 | 4×9-gon; 12×7-gon; 12×6-gon; 12×5-gon; 12×4-gon | 100 | 1.0, 1.041053671831, 1.046618966752, 1.050825319017, 1.014157382666 | two |
| 553 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, -1) | 52 | 4×9-gon; 12×5-gon; 12×5-gon; 12×6-gon; 12×6-gon | 100 | 1.0, 0.954173012239, 0.9631077866076, 0.974676768915, 0.9596914494039 | two |
| 554 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 52 | 4×6-gon; 12×6-gon; 12×5-gon; 12×6-gon; 12×6-gon | 100 | 1.0, 1.008245730115, 1.025435341429, 1.016663261381, 1.039182620369 | two |
| 555 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 52 | 4×6-gon; 12×8-gon; 12×6-gon; 12×4-gon; 12×5-gon | 100 | 1.0, 1.034802000295, 1.037557846859, 1.014308097365, 1.040686538085 | two |
| 556 | T | O8/4 (1, 1, 1) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 52 | 4×6-gon; 12×7-gon; 12×5-gon; 12×5-gon; 12×6-gon | 100 | 1.0, 1.045780748766, 1.032186822702, 1.01417685048, 1.043051099011 | two |
| 557 | T | C6 (1, 0, 0) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 54 | 6×4-gon; 12×6-gon; 12×7-gon; 12×5-gon; 12×6-gon | 104 | 1.0, 1.01281274996, 1.014531171944, 1.005259012614, 1.008821600608 | two |
| 558 | T | C6 (1, 0, 0) + O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24/12 (φ, 1/φ, 1) | 50 | 6×6-gon; 4×9-gon; 4×6-gon; 12×6-gon; 12×6-gon; 12×4-gon | 96 | 1.0, 0.9412431906964, 1.011688124317, 0.9686456135901, 0.9741419768921, 0.9570314512294 | two |
| 559 | T | C6 (1, 0, 0) + O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 50 | 6×6-gon; 4×6-gon; 4×6-gon; 12×7-gon; 12×5-gon; 12×5-gon | 96 | 1.0, 0.9610438410368, 1.054024683402, 1.013717898631, 0.9943735051804, 0.9760468419917 | two |
| 560 | T | C6 (1, 0, 0) + O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 50 | 6×6-gon; 4×6-gon; 4×6-gon; 12×7-gon; 12×5-gon; 12×5-gon | 96 | 1.0, 0.9727905674007, 1.074586502606, 1.030132002554, 1.006025310388, 0.9880549676101 | two |
| 561 | T | O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 56 | 4×9-gon; 4×9-gon; 12×5-gon; 12×6-gon; 12×6-gon; 12×4-gon | 108 | 1.0, 1.080854796676, 1.024699106839, 1.035422435649, 1.046093961984, 1.011276494164 | two |
| 562 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 58 | 6×6-gon; 4×6-gon; 12×6-gon; 12×7-gon; 12×4-gon; 12×6-gon | 112 | 1.0, 0.9765936036449, 1.009365143689, 1.012018727692, 1.001417879343, 0.9858961722561 | two |
| 563 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, -1) | 58 | 6×4-gon; 4×9-gon; 12×5-gon; 12×6-gon; 12×6-gon; 12×6-gon | 112 | 1.0, 1.055313664773, 1.000770041756, 1.006718455506, 1.003316578187, 1.007789506712 | two |
| 564 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 58 | 6×6-gon; 4×9-gon; 12×5-gon; 12×5-gon; 12×5-gon; 12×7-gon | 112 | 1.0, 0.9523603200932, 0.9573049975838, 0.9657330003541, 0.9629097654033, 0.986466370116 | two |
| 565 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 58 | 6×8-gon; 4×6-gon; 12×7-gon; 12×4-gon; 12×5-gon; 12×6-gon | 112 | 1.0, 0.9739029587864, 1.00488487624, 0.9853797573154, 0.9831292190454, 1.008403996582 | two |
| 566 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 58 | 6×6-gon; 4×6-gon; 12×8-gon; 12×5-gon; 12×5-gon; 12×5-gon | 112 | 1.0, 0.987118145371, 1.025069031877, 0.9964573540424, 0.9964777041746, 1.023348291382 | two |
| 567 | T | O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 64 | 4×6-gon; 12×7-gon; 12×5-gon; 12×6-gon; 12×5-gon; 12×6-gon | 124 | 1.0, 1.006445621635, 1.018984564147, 1.028066463116, 1.006229099689, 1.029657404836 | two |
| 568 | T | C6 (1, 0, 0) + O8/4a (1, 1, 1) + O8/4b (1, 1, -1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12 (φ, 1/φ, 1) | 62 | 6×6-gon; 4×9-gon; 4×9-gon; 12×5-gon; 12×6-gon; 12×5-gon; 12×5-gon | 120 | 1.0, 0.9788453195354, 1.057715970315, 0.9973372999266, 1.0044176386, 0.9996814820793, 0.9857082142231 | two |
| 569 | T | C6 (1, 0, 0) + O8/4 (1, 1, 1) + RD12 (1, 1, 0) + D12 (φ, 1, 0) + I12 (φ, 0, 1/φ) + RT24/12a (φ, 1/φ, 1) + RT24/12b (φ, 1/φ, -1) | 70 | 6×4-gon; 4×6-gon; 12×7-gon; 12×6-gon; 12×6-gon; 12×5-gon; 12×6-gon | 136 | 1.0, 0.9877870158233, 0.9905416181023, 0.9998403003505, 0.9936216608338, 0.9903828072578, 1.012833601658 | two |

## LEADS

- Names and numbers for these dice are DICTO's; the labels here are group + orbit set only.
- Exact forms on the frame-group dice (149), as Equanimity did for its twelve (Corollary 7: regular faces fix the cut; many Th and T dice here have regular-looking faces worth testing).
- The two icosahedron placements together under Th and T (the pilot's 7 cross-frame dice are the first members).
- A proof (or a counterexample) that each orbit set with a single fixed point carries exactly one fair die.
- Raise the caps (m ≥ 4 or 5) on the capped classes; centroid-fair polar dice by solving with the centroid as the viewpoint (the counting argument says generically none).
- The Vacuus of the 149: which hide a regular polygon (Equanimity Theorem 6) and which turn without a mirror like D191.
