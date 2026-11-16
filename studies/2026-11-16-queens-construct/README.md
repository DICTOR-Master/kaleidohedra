# Building the Queens from polytopes, and taking them apart (16 Nov 2026)

**Conclusion: by corners, the White Queen (600-cell) is exactly A + (−A) + C3 + B + (−B), five S5 orbits. By walls, A and B together use all 60 mirrors (30 + 40, sharing the 10 S5 mirrors) and 40 of the 300 cross walls. By solids, the five orbit hulls do not assemble the Queen: they all contain the centre, no hull contains another, and together they cover only 65.0% of it. Their common core is a uniform bitruncated 5-cell, and A ∩ B is a golden cantitruncated 5-cell. Every check is exact in Q(√5).**

DICTO's proposal (16 Nov 2026): "construct/deconstruct the queens from/into polytopes, as far as possible". He asked the question as "if this is the steak, where is the cat; if this is the cat, where is the steak". Here this means: can the shapes A and B, which hide in the Queen's walls, also build the Queen itself? The White Queen is the 600-cell P and the Red Queen is the 120-cell Q, dual to P and aligned with it, in sum-zero R⁵, where S5 permutes the coordinates. Computation was done with Claude (Anthropic).

Related studies: `2026-11-16-600cell-walls` (A's and B's plates are walls), `2026-11-16-queens-vicinity-vacuus` (the shapes round the Queens read as Vacuus) and `2026-11-16-queens-chambers` (the 360 walls cut each Queen into 4,291,200 chambers). This study does not repeat the chambers.

## Table

| Queen | method | pieces | exact check | status |
|---|---|---|---|---|
| 600 | corners: S5 orbits | C1 = A (golden truncated 5-cell, gaps 1, φ; f 20/40/30/10), C2 = −A, C3 = uniform expanded (runcinated) 5-cell (f 20/60/70/30), C4 = B (golden cantellated 5-cell, gaps φ, 1; f 30/90/80/20), C5 = −B | disjoint, cover all 120; hull volumes (1+3φ)/40, (14+7φ)/60 and (3+5φ)/24 of P | split known (Koca, Koca, Al-Ajmi 2011/12). Our computation names the hulls from their coordinate blocks; we did not check whether that paper names them. C3 is R of the walls study |
| 600 | corners: 24-cells | 25 inscribed; two of them share 0 or 6 corners; exactly 10 ways to choose 5 disjoint ones | exact closure and inner-product profile | known: Schoute 1905; Coxeter, Regular Polytopes p. 270; proved by Denney et al. 2019 |
| 600 | corners: 24-cell + snub 24-cell | 24 + 96; snub f = 96/432/480/144, 24 icosahedra + 120 tetrahedra, one edge length | exact | known (Gosset 1900; Coxeter) |
| 600 | corners: great polygons | 72 decagons, 200 hexagons, 450 squares. There are 84 covers by 12 disjoint decagons, and 12 of them are Hopf (pairwise Clifford parallel) | exact isoclinic test | Hopf covers known (Sadoc–Mosseri). The 72 non-Hopf covers were not found in the sources checked |
| 600 | corners: layers | vertex axis: point, icosahedron, dodecahedron, icosahedron, icosidodecahedron, ... (1, 12, 20, 12, 30, 12, 20, 12, 1). Cell axis: 4, 4, 6, 12, 12, 12, 4, 12, 4, ... (tetrahedra, octahedra, cuboctahedra, truncated tetrahedra) | counts exact | known (Coxeter, Table V; Boole Stott 1900) |
| 600 | solids: cell pyramids (control) | 600 congruent pieces | sum = 25φ³a⁴/4 exactly | control passes |
| 600 | solids: snub 24-cell + 24 icosahedral pyramids | snub (1+2φ)/5 of P; each pyramid (1/30 − φ/60) of P | sum exact. Control: the same split with the apex at the centre **fails** | known (Conway–Guy; Coxeter) |
| 600 | solids: grand antiprism + its complement | GA = 17/30 + φ/5 of P (f 100/500/720/320, 300 tetrahedra + 20 pentagonal antiprisms) + 20 pentagonal-antiprism pyramids + 20 edge joins (segment ∗ pentagon) | sum exact. The 20 icosahedral caps overlap, and the overlap is exactly the 20 edge joins counted twice | GA known (Conway–Guy 1965). The two-piece split of its complement was **not found in the sources checked** |
| 600 | solids: rings | 240 Boerdijk–Coxeter rings of 30 tetrahedra, each holding 3 decagons. The cells split into 20 disjoint rings in 828 ways; the rings of one split are congruent | sum exact; each ring = V/20 (a pyramid from the centre, not convex) | 20 rings known (Coxeter 1985; Sadoc 2001). The count 828 was not found in the sources checked |
| 600 | solids: caps over an inscribed 24-cell | 24 caps of 50 corners each | **fails**: the caps overlap (sum exceeds by (−111/2 + 43φ)V) | fails |
| 600 | cat/steak: solids | the hulls of the five orbits | all contain the centre, so they overlap and cannot tile. Union = 0.6504 of P (inclusion–exclusion over 31 exact intersections). Core of all five = uniform bitruncated 5-cell, (23/750 + 23φ/1500) of P. A ∩ B = golden cantitruncated 5-cell (one S5 orbit), 0.1308 of P. Caps of P over A's facets overlap (0.161 V), and over B's (0.107 V) | does not tile (the core and A ∩ B **not found in the sources checked**) |
| 600 | cat/steak: A's and B's 30 facet hyperplanes | 686 regions in 23 S5 classes | Σ (orbit size × volume) = V exactly | new (computed) |
| 600 | cat/steak: all 90 facet hyperplanes of the five hulls | 17,371 regions in 300 S5 classes. 14,290 regions (205 classes) lie outside every hull and fill 0.34959 of P, which matches 1 − union independently. The central region is the bitruncated core, and it is the only region inside all five hulls | Σ (orbit size × volume) = V exactly (job qconstruct-all, FINAL ok, 5 min) | new (computed) |
| 600 | cat/steak: walls | A: 30 mirrors. B: 40 mirrors + 40 cross walls. They share the 10 S5 mirrors. **A ∪ B = all 60 mirrors + 40 cross walls**; C3 adds 5 cross walls. Left over: 255 cross walls (S5 orbits 15 + 60 + 60 + 120) | exact; control: an ordinary orbit (t = 3/2) has plates in no wall | **new**: A and B together rebuild the whole mirror system |
| 120 | corners: 600-cells | 10 inscribed, each corner in 2; 2 splits into 5 disjoint ones (5 × 120). Control: 5·vol(600-cell) ≠ vol(120-cell) | exact closure | known (Coxeter's compounds; Wikipedia "120-cell") |
| 120 | corners: 24-cells | 225 inscribed, each corner in 9; at least 1000 splits into 25 disjoint ones (search capped). Each lies in 1 or 2 of the 600-cells | exact | 225 and 25 known (Denney et al. 2019; Wikipedia). The split count is open |
| 120 | corners: S5 orbits | 13 orbits: 5 + 5 (two regular 5-cells, 5/144 of Q each), 20 + 20 (expanded 5-cells), 20 + 20 (truncated 5-cells), 30 (antipodal bitruncated 5-cell, 23/72 of Q), 60 + 60 (runcitruncated), 60 + 60 (cantitruncated), 120 + 120 (permutohedra) | exact, sum 600 | 120 inscribed 5-cells known (Wikipedia). The full S5 orbit table was **not found in the sources checked** |
| 120 | solids: pyramids (control) and Hopf rings | 120 dodecahedral pyramids; 12 rings of 10 dodecahedra over a Hopf cover, neighbours sharing a pentagon | volume = (15/4)(105 + 47√5)a⁴ exactly | known (Coxeter; Sadoc–Mosseri) |
| 120 | solids: caps over an inscribed 600-cell / 24-cell | 480 congruent caps / 24 caps | **fails**: overlap 0.081 V / 0.191 V | fails |
| 120 | walls: S5-orbit hulls | Only the two 5-cells have every plate a wall (10 mirrors each). All 13 hulls together reach 40 mirrors + 45 cross walls, and have 270 plates in no wall | exact | cat/steak fails for the Red Queen's orbits |

**Answer to DICTO's question.** For the corners and the walls, the cat and the steak weigh the same:
- **Corners:** A, B, their mirror images and C3 are exactly the 600-cell's corners.
- **Walls:** A and B alone carry all 60 of its mirrors.

For the solids, they do not. The five hulls pile up at a common bitruncated 5-cell core and leave 35% of the Queen uncovered. To fill the Queen, the facet hyperplanes of A and B must cut it into 686 pieces of 23 kinds.

## Files

- `scripts/qlib.py`: exact tools. Q5 arithmetic (copied from the echo-shapes study), certified hulls, face lattice, exact volumes, caps, halfspace intersection.
- `s1_corners600.py`, `s2_solids600.py`, `s3_catsteak.py`, `s3b_arrangement.py` (mode AB), `s4_redqueen.py`, `fig_orbits.py`. Each log in `data/` ends FINAL ok. Every run except one was a pilot of under 5 min on the compute machine. The 90-plane arrangement (`data/s3b_arrangement_all.*`) ran as a monitored job.
- Figure: `data/queens-construct-orbits.png` (the five orbit hulls in the A4 Coxeter plane, in element colours).

## Sources checked (16 Nov 2026)

- Denney, Hooker, Johnson, Robinson, Butler, Claiborne, "The geometry of H4 polytopes", arXiv:1912.06156, https://arxiv.org/abs/1912.06156. Read: Facts 2 and 5 (25 24-cells, 10 partitions; Schoute 1905; Coxeter's correction) and §3 (25 disjoint 24-cells in the 120-cell).
- Wikipedia, "120-cell", https://en.wikipedia.org/wiki/120-cell, read 16 Nov 2026: 225 24-cells / 25 disjoint; ten 600-cells, two splits into five; 12 rings of 10; 120 5-cells.
- Library (bridges/):
  - Koca, Al-Ajmi, Koca 2009, "Grand antiprism and quaternions" (arXiv:0906.2117). Searched for pyramids or a dissection of the complement: none found.
  - Koca, Koca, Al-Ajmi 2011, "Branching of the W(H4) polytopes ..." (arXiv:1106.2957).
  - Koca et al. 2009 and 2011, the snub 24-cell papers.
- Not opened: Coxeter, Regular Polytopes (Dover 1973; cited through Denney et al. and the library index); Conway–Guy 1965; Sadoc–Mosseri, Geometrical Frustration (1999); Sadoc 2001 on helices; Elser–Sloane 1987.

## LEADS

1. Reduce the 300 classes of the 90-plane arrangement by S5 × {±1}, because the plane set is centrally symmetric. Then name the classes that touch a corner of P (2,420 regions do).
2. Check in the literature whether the two-piece split of the grand antiprism's complement, the core bitruncated 5-cell and A ∩ B are known, in particular in Koca, Koca, Al-Ajmi 2011, section on the W(A4) orbits.
3. The 120-cell's 13 S5 orbits as Vacuus: which golden twist, if any, makes a Red-Queen orbit all-wall, as A and B are for the White Queen.
4. Count all splits of the 120-cell into 25 disjoint 24-cells (the search stopped at its cap of 1000) and all 20-ring splits of the 600-cell up to symmetry (828 in all).
5. The 72 non-Hopf decagon covers of the 600-cell: are they unions of partial Hopf fibres (mixed left and right)?
6. A dissection of the 120-cell around an inscribed 600-cell does not come from caps (they overlap by 0.081 V). Try caps over the 600-cell's facets cut back by the neighbouring facet planes. This is the 120-cell version of the grand-antiprism repair.
