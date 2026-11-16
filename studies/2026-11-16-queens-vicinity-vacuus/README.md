# The shapes round the Queens, read as Vacuus (16 Nov 2026)

> **Correction (16 Nov 2026, after the Walls of Silence review):** "heart" here means centrally symmetric about the Queens' centre (the host centre), not about a shape's own centroid. Under the three kinds of the paper (heart, inherited heart, non-heart), the diminished 600-cells (special cuts) that are not antipodal are of the inherited heart kind, not non-heart (paper, Proposition 4). The cross-wall law and its stations go to the next version of #107.

**Conclusion (exact in Q(√5)): every shape built from the Queens' own corners is a Vacuus, and most of them are hidden in the Queens' walls. Five kinds of shape have every plate on a wall: the snub 24-cell, the grand antiprism, every diminished 600-cell, the 24-cell inscribed in the 600-cell, and the 600-cell inscribed in the 120-cell. The 24-cell and the inscribed 600-cell sit entirely on cross walls. The 15 uniform members of the H4 family are never fully hidden, except the two Queens. One new shape on the Queens' Hopscotch line has a Vacuus that is exactly the whole wall system, all 360 walls: the truncated 600-cell cut at the golden station μ = 1/2 + √5/5.** None of these Vacuus readings was stated by the shape's finder. The Vacuus is DICTO's notion (#87, #105). Before this study only the Queens and their stages had been read for mirrors (#107).

DICTO's idea (16 Nov 2026), in his words: "I think anybodys shape found in the vicinity of queens shape needs to be reevaluated as a vacuus, but also if these are the shapes where is the structure, and if these are the structure where are the shapes". This study answers the first half. The reverse question is in `studies/2026-11-16-queens-chambers`.

## Test
- **Walls of the Queens (the structure):** the 60 mirror hyperplanes of H4, which the 600-cell and the 120-cell share, plus the 300 cross walls. A cross wall is the central section parallel to a pair of opposite tetrahedral cells of the 600-cell; its normal points to a corner of the 120-cell. DICTO ruled on 16 Nov that "cross walls also count". The 120-cell adds no cell-parallel walls of its own: its cell centres point along the 600-cell's corners, so its cell-parallel sections are the 60 mirrors.
- **Plates:** for a 4D shape, each plate is the central hyperplane spanned by one of its 2-faces. For a 3D slice or shadow taken across a direction n, each plate is the central plane spanned by one edge, lifted to the 4D hyperplane span(n, edge). The lifted plate is a wall exactly when that wall contains the slicing axis and the edge.
- **Heart / non-heart:** a shape is of the heart kind when it is centrally symmetric about the Queens' centre, so that opposite 2-faces share plates; otherwise it is non-heart. The histogram of 2-faces per plate is in the data.
- **Verdict per shape:** *hidden* (every plate is a wall), *partly hidden*, or *not hidden* (no plate is a wall).
- **Exactness:** frame = the 600-cell of radius 2 in Q(√5) (the source frame of study 2026-10-27-4d-shadows; its q5.py and polytopes.py are reused). The face lattice is proposed in floating point (Qhull). Every 2-face is then checked exactly to lie in its plate, and every plate normal is put in canonical form and matched exactly against the 60 + 300 wall normals.

## Controls (all pass, `data/study1.log`, 45 checks, FINAL ok)
| control | plates | kind | mirror / cross / none |
|---|---|---|---|
| 600-cell (positive) | 60 (20 triangles each) | heart | 60 / 0 / 0 |
| 120-cell (positive) | 60 (12 pentagons each) | heart | 60 / 0 / 0 |
| 600-cell with every corner moved by an exact rational step of at most 0.04 (negative) | 1200 | non-heart | 0 / 0 / 1200 |
| 600-cell turned by a generic exact rational rotation (negative) | 60 | heart | 0 / 0 / 60 |

The run also checks: the f-vectors of all 15 uniform H4 polytopes; W(H4) of order 14400; the orders 240, 240, 576, 400 and 144 of Koca et al.'s maximal subgroups; the 62 slice types of #63 and the 124 slice patterns of the Red Queen atlas, both reproduced; the Mirror Law of #107 Theorem 1, reproduced for every face type of the 15; and A and B as reported by the 600-cell walls study (30 mirror plates; 40 mirror + 40 cross).

## Results
Notation: plates M / C / N = mirror walls / cross walls / no wall.

**The 15 uniform H4 polytopes** (Wythoff 1907 construction. Schläfli found the 600-cell and 120-cell (manuscript 1852). Gosset (1900) found the rectified 600-cell. Boole Stott (1910) and Elte (1912) listed further members, and Conway and Guy (1965) gave the complete list, proved complete by Möller (2004). The sources checked do not credit each member separately.)

| shape (seed) | plates | kind | M / C / N | verdict |
|---|---|---|---|---|
| 600-cell (0001), 120-cell (1000) | 60 | heart | 60 / 0 / 0 | hidden |
| rectified 600-cell (0010), rectified 120-cell (0100), truncated 600-cell (0011), truncated 120-cell (1100), bitruncated (0110) | 1260 | heart | 60 / 0 / 1200 | partly hidden |
| cantellated 120-cell (1010), cantitruncated 120-cell (1110) | 4260 | heart | 60 / 0 / 4200 | partly hidden |
| cantellated 600-cell (0101), cantitruncated 600-cell (0111) | 3780 | heart | 60 / 0 / 3720 | partly hidden |
| runcinated (1001) | 3720 | heart | 0 / 0 / 3720 | **not hidden** |
| runcitruncated 120-cell (1101), runcitruncated 600-cell (1011) | 6720 | heart | 0 / 0 / 6720 | **not hidden** |
| omnitruncated (1111) | 8520 | heart | 0 / 0 / 8520 | **not hidden** |

No uniform member has a 2-face on a cross wall. The off-mirror faces lie two to a plate, as #107 found for the stages.

**The cross-wall law for the whole family (exact, every seed).** A face of type J (two nodes) has the plate span(x, α_J). A wall with normal w contains it exactly when w ⟂ α_J and Σ_{ringed i} λ_i (w·ω_i) = 0. Roots have coefficients of one sign, which gives #107's Mirror Law. Cross-wall normals have mixed signs, so they give **stations**: seeds at which a face type that is off the mirrors lands on cross walls. Only face type {2,3} has stations, and only in these families:
- the truncated 600-cell family (0, 0, λ3, λ4) at **λ3 : λ4 = 1/φ**;
- the cantellated 600-cell family (0, λ2, 0, λ4) at **λ2 : λ4 = √5 − 2**;
- a one-parameter family of seeds in each of the runcitruncated 120-cell, runcitruncated 600-cell, cantitruncated 600-cell and omnitruncated families.

No uniform seed sits at a station.

**The golden station on the Queens' Hopscotch line (new shape, flagged).** The Hopscotch line is S(μ) = 600-cell ∩ μ·120-cell (studies/2026-11-12-pds-hopscotch-line). The truncated-600-cell hop passes the station at **μ = 1/2 + √5/5 = 0.947213595** exactly. There each corner sits on a 600-cell edge at fraction t = 1/2 − √5/10 = 1/(1+φ²) from the nearer corner, the edges come in two lengths in the ratio φ, and the hexagons are golden (sides alternating in the ratio 1 : φ). Its 1440 corners, 720 cells, 2400 triangles and 1200 hexagons put **20 hexagons on each of the 60 mirrors and 8 triangles on each of the 300 cross walls: 360 plates = the whole wall system of the Queens, and nothing else** (heart kind; `scripts/station.py`, `data/station.log`, FINAL ok). Its Vacuus *is* the Queens' structure. This station is not μ* = 0.924139 (the 19-design), μ_Ω = 0.921450 (the canonical-form silence) or the turn r = 0.925615. Elsewhere on the line S(μ) behaves like its stage: 60 mirror plates + 1200 plates on no wall (9 seeds tested across the three hops). The cantellated station, at the same μ value, has 60 M + 300 C + 2520 N, so it is partly hidden.

**Shapes from the Queens' corners**
| shape | finder | 2-faces | plates | kind | M / C / N | verdict |
|---|---|---|---|---|---|---|
| snub 24-cell = 600-cell − inscribed 24-cell | Gosset 1900 | 480 | 60 (8 each) | heart | 60 / 0 / 0 | hidden |
| grand antiprism = 600-cell − two orthogonal decagons | Conway and Guy 1965 | 720 (700 triangles + 20 pentagons) | 60 (12 each) | heart | 60 / 0 / 0 | hidden |
| diminished 600-cells (independent sets removed; 314,248,344 of them) | Dutour Sikirić and Myrvold 2008 | e.g. 1170 (one removed) | 60 | non-heart (heart if the removed set is antipodal) | 60 / 0 / 0 | hidden (12 tested: 1, 2, 6, 12, 18 removed, and an antipodal pair) |
| 24-cell inscribed in the 600-cell (one of 25) | classical (the 25 are in Wikipedia's 600-cell article; first finder not traced) | 96 | 12 (8 each) | heart | **0 / 12 / 0** | hidden, **on cross walls only** |
| 600-cell inscribed in the 120-cell (on 120 of its 600 corners) | classical (first finder not traced) | 1200 | 60 | heart | **0 / 60 / 0** | hidden, **on cross walls only** |
| runcinated 5-cell = hull of an A4 root system in the 600-cell (W(A4) orbit of 20) | classical; orbit listed by Koca et al. 2006 | 70 | **5** (14 each) | heart | **0 / 5 / 0** | hidden, on cross walls only |
| solid A (W(A4) orbits 20+ and 20−) | DICTO 2026 (orbit sets listed by Koca et al. 2006) | 30 | 30 | non-heart | 30 / 0 / 0 | hidden |
| solid B (W(A4) orbits 30+ and 30−) | DICTO 2026 (orbit sets listed by Koca et al. 2006) | 80 | 80 | non-heart | 40 / 40 / 0 | hidden |

**The diminished 600-cells, in general (proof).** Removing an independent set of corners leaves cells of two kinds: the tetrahedra that survive, and the icosahedra of the removed corners' neighbours. All their triangles are triangles of the 600-cell, so every 2-face is a 600-cell triangle on one of the 60 mirrors. All 314,248,344 diminished 600-cells are therefore hidden in the mirrors. Each one is heart kind exactly when its removed set is antipodal.

**A and B were already listed by Koca et al.** In their paper (2006, last section), the 120 roots of H4 split under W(A4) into 20 + 20+ + 20− + 30+ + 30−. Computed here: the two 20-orbits that are not centred on themselves are congruent to solid A, and the 30-orbits to solid B (Gram spectra). The third 20-orbit is the A4 root system. Koca et al. give these as orbit sets, not as solids, and do not describe their hulls; DICTO found A and B as solids.

**Orbits of the maximal subgroups of W(H4)** (Koca, Al-Barwani, Al-Farsi and Koç 2006; each subgroup built as the stabiliser named below; hulls of every full-dimensional orbit on the 600-cell's and the 120-cell's corners, and one generic orbit as a negative case):
| subgroup | orbits on 600-cell corners | on 120-cell corners | hulls hidden / tested | generic orbit |
|---|---|---|---|---|
| W(H3)×Z2 (240), stabiliser of a corner pair | 2, 24, 24, 30, 40 | 40, 40, 40, 60, 60, 120, 120, 120 | 5 / 10 | not hidden |
| Aut(A4) (240), stabiliser of an A4 root system | 20, 40, 60 | 10, 30, 40, 40, 120, 120, 240 | 4 / 10 | not hidden |
| W(D4):C3 (576), stabiliser of an inscribed 24-cell | 24, 96 | 24, 96, 192, 288 | 3 / 6 | not hidden |
| [W(H2)×W(H2)]:Z4 (400), stabiliser of two orthogonal decagons | 20, 100 | 100, 100, 200, 200 | 1 / 6 | not hidden |
| [W(A2)×W(A2)]:Z4 (144), stabiliser of two orthogonal hexagons | 12, 36, 72 | 24, 36, 36, 72, 72, 72, 144, 144 | 2 / 11 | not hidden |

Every orbit hull made only of the 600-cell's corners is hidden, except two: the 12-corner and 20-corner hulls of two orthogonal polygons (duopyramids), which are not hidden. Hidden examples: the two 24-corner orbits of W(H3)×Z2, with 35 plates (35 M, and 15 M + 20 C); the 40 and 60 orbits of Aut(A4), with 80 plates each (20 M + 60 C, and 40 M + 40 C); the 36 and 72 orbits of the order-144 group, with 96 plates (24 M + 72 C) and 66 plates (54 M + 12 C). Orbits on the 120-cell's corners are mostly partly hidden or not hidden. Every generic orbit has no plate on any wall. Full per-orbit lists are in `data/study1-all.json` (`koca`).

**DICTO's slice atlases (#63 White Queen and the Red Queen atlas): 3D shapes.** These are 62 + 124 slice types and 8 shadows, with plates lifted along the slicing axis. Of all their edge plates, the 600-cell's slices and shadows put 413 on mirrors, 57 on cross walls and 9640 on no wall. For the 120-cell the counts are 638, 93 and 9384. The fully hidden ones:
- in the 600-cell: the vertex-first slices at h = 2 (32 corners) and at h = 1 + √5 and 5/2 + √5/2 (12 corners), with 15 mirror plates each; and the cell-first tip tetrahedron;
- in the 120-cell: the vertex-first slices at h = 1 + √5/2 (60 corners: 15 M + 30 C), 5/4 + 3√5/4, 3/2 + 3√5/4 and 7/4 + 3√5/4 (20 corners each, 15 M), and two cell-first tetrahedra.

Seven 120-cell slices have no plate on any wall. All other slices and all 8 shadows are partly hidden. Humpty Dumpty, the 48-corner cell-first slice, is partly hidden. Most slices are non-heart, since a slice off the centre is not centrally symmetric in 4D. Per-slice data are in `atlas600` and `atlas120` of `data/study1-all.json`.

## Flags: Vacuus status not stated by the finder (DICTO's point)
No finder outside DICTO's work could have stated it, since the Vacuus is DICTO's notion. #107 (DICTO) stated the mirror reading for the Queens, their stages and every Wythoff seed of zeros and ones. These shapes are now read as Vacuus for the first time:
1. **the golden-station truncated 600-cell (μ = 1/2 + √5/5)**: a new shape whose Vacuus is the entire wall system (60 + 300);
2. **the inscribed 24-cell** (classical), **the inscribed 600-cell in the 120-cell** (classical) and **the runcinated 5-cell inside the 600-cell** (A4 roots): hidden entirely in the *cross* walls;
3. **the snub 24-cell** (Gosset), **the grand antiprism** (Conway–Guy) and **all diminished 600-cells** (Dutour Sikirić–Myrvold): hidden entirely in the mirrors;
4. **A and B** were orbit sets in Koca et al. 2006 before DICTO found them as solids. Their Vacuus was first stated by DICTO, in the non-heart Vacuus study of 16 Nov;
5. the Koca orbit hulls listed above as hidden;
6. the #63 / Red Queen slices that are hidden (listed above);
7. the cross-wall stations of the runci-, canti- and omnitruncated families: seed families where some faces lie on cross walls.

## Files
- `scripts/qv_lib.py`: frame, walls, H4 simple roots and weights, Wythoff orbits, face lattices, exact plate tests (4D and 3D).
- `scripts/study1.py`: all parts (controls, wythoff, stations, special, koca, atlas600, atlas120, hopscotch, ab). The job `qvvacuus` ran on the compute machine in 75 s; `data/study1.log` and `data/study1-all.json` are the output (FINAL ok, 45 checks). In the first run, two checks failed on reference cell counts mis-typed as 1920. The true 1440 (Wikipedia, *Cantellated 600-cell*) matches the construction.
- `scripts/station.py`, `data/station.log`: the golden station (FINAL ok).

## Sources checked (16 Nov 2026)
- Wikipedia, *Uniform 4-polytope*, https://en.wikipedia.org/wiki/Uniform_4-polytope (history: Schläfli 1852, Gosset 1900, Boole Stott 1910, Schoute 1911, Elte 1912, Coxeter 1940, Conway–Guy 1965, Möller 2004). Read 16 Nov 2026, first 100,000 characters only.
- Wikipedia, *600-cell*, https://en.wikipedia.org/wiki/600-cell (snub 24-cell as a diminished 600-cell; 25 inscribed 24-cells; grand antiprism as the 600-cell minus two 150-cell tori, citing Dechant 2021). Read 16 Nov 2026, first 100,000 characters.
- Wikipedia, *Cantellated 600-cell*, https://en.wikipedia.org/wiki/Cantellated_600-cell (cell counts 1440 for the cantellated and cantitruncated 600-cell), 16 Nov 2026.
- M. Dutour Sikirić and W. Myrvold, "The special cuts of the 600-cell", Beiträge zur Algebra und Geometrie 49(1) (2008) 269–275, https://emis.univie.ac.at/journals/BAG/vol.49/no.1/22.html, arXiv 0708.3443. The PDF returned HTTP 503 on 16 Nov; the count 314,248,344 and the definition are from the abstract and the search snippets.
- M. Koca, M. Al-Barwani, S. Al-Farsi and R. Koç, "Maximal subgroups of the Coxeter group W(H4) and quaternions", Linear Algebra Appl. 412 (2006) 441–452, arXiv hep-th/0510191. The library copy (`cited/`) was read in full text for the subgroups and orbit decompositions.
- Library entries listed but not read in full: Koca, Al-Ajmi and Koca 2009 on the snub 24-cell from E8 and on the grand antiprism with quaternions (`bridges/`).
- DICTO's own work: #107 *The Vacuus of the Queens* (papers/2026-11-11-queens-vacuus/paper.html, the Mirror Law); studies 2026-10-27-white-queen-600 (#63 atlas), 2026-10-27-white-queen-polar (Red Queen atlas), 2026-11-12-pds-hopscotch-line, 2026-11-16-600cell-walls, 2026-11-16-non-heart-vacuus, 2026-10-30-queen-stages.
- Web search "diminished 600-cell number of diminishings" and "Beiträge zur Algebra und Geometrie 2008 49 diminished 600-cell independent sets Myrvold", 16 Nov 2026.

## LEADS
1. The golden station shape: does its Vacuus = wall-system property single it out in the whole H4 family? The exact law says it is the only two-ring seed with no plate on no wall. Its golden truncated tetrahedra look like the golden truncated tetrahedra of solid A; check for congruence.
2. Seed families in the runci-, canti- and omnitruncated families where every face type lands on a wall: solve the station equations jointly for all face types.
3. Cross-only shapes (the 24-cell, the inscribed 600-cell, the runcinated 5-cell): is every polytope on the cross walls alone made from a 120-cell sub-structure? Test the 225 inscribed 24-cells of the 120-cell.
4. The Red Queen slices that are hidden (60 corners: 15 M + 30 C) belong in the next version of the Red Queen atlas.
5. The other agent's GET, echo shapes and twisted classes are not in this study, by its brief.

DICTO · dictospheres.com
