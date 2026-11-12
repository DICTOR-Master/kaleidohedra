# The residents of the Queens, exact (13 Nov 2026; Platonic book, Chapter 11; Atlas of the Chains, Observation 5)

**Conclusion (13 Nov 2026): the 600-cell's corners carry exactly 120 D, 240 I, 600 C, 3000 T and 900 O (complete enumeration over Q(sqrt5), all draft counts confirmed), and the 120-cell's 1560, 2400, 7200, 34 200, 8100. Of the four 4D reflection families only H4 houses D or I (proved by a field argument, and checked), and each of its 15 polytopes houses all five. One correction to the draft: each of the 120 dodecahedra has ALL FIVE of its Euclid cubes (and all ten tetrahedra) on the 600-cell's corners, not two; and One World's nesting holds for D, C, T only (its octahedra and icosahedron are not there).**

Script `scripts/residents.py` (stdlib Python only). Log `data/residents.log`, data `data/residents-full.json`; pilot `data/residents-pilot.log`,
`data/residents-pilot.json`. Run on the compute node through the job gate (jobs residents-pilot: 159 checks, 19 s; residents: 199 checks,
286 s, FINAL ok). Every decision uses exact integer arithmetic in Z[phi] or Z[sqrt2]; there are no floats in any test.

## What is counted
A *resident* of a polytope is a regular D, I, C, T or O, of any size and in any position, whose corners are ALL corners of the polytope.
It does not have to be a cell. Residents are counted as distinct corner sets. So the 600-cell's "3000 tetrahedra" are every regular
tetrahedron on its 120 corners: its 600 cells plus 2400 more, of three other sizes.

## Method, and why it misses nothing
1. **Polytopes.** Each Wythoff polytope is the orbit of its 0/1 seed (distance 1 from every ringed mirror), so every polytope is uniform.
   The orbit is generated exactly from the simple reflections of the root system: H3/H4 roots in Q(sqrt5) (the 600-cell's 120 corners,
   doubled), A/B/F roots in Q(sqrt2). The reflections are recorded as corner permutations, and these permutations are the group action used below.
2. **Frames.** A finite point set is fixed up to isometry by its distance matrix. A 3D solid is fixed by any 4 affinely independent
   corners: every other corner is a fixed affine combination of them, with exact coefficients over the field. Each solid gets a frame
   in a model: p0 plus its nearest affinely independent corners.
3. **Search through corner v0.** For every squared distance s from v0, the search lists every ordered tuple of corners (v0, P1, P2, P3)
   whose six squared distances equal s times the frame's ratios. Each tuple determines one candidate solid, which is kept only if all of
   its corners are polytope corners. Each kept solid's full distance matrix is then checked exactly against the model's.
   *Completeness:* label any resident with v0 as p0 and its frame is one of the listed tuples, so it is found.
4. **Totals.** The polytopes are corner-transitive, so total = (residents through v0) x corners / (corners per solid). The script
   requires this to be a whole number. For the 600-cell and the 120-cell the whole set is also built as the closure under the four
   reflections and split into orbits under [3,3,5] (order 14400) and under its rotation subgroup. Separately, and with no use of the
   group, the search is rerun from EVERY corner, and its union equals the closure exactly (both Queens, every solid type).
   The snub 24-cell and the grand antiprism are not taken as corner-transitive: for them the search runs from every corner.

## Table 1. The 600-cell (edge 1, circumradius phi): every resident, by orbit of [3,3,5]
| solid | total | orbits: size x (edge, what they are) |
|---|---|---|
| D | **120** | one orbit of 120 (stabiliser order 120): edge 1, centre at distance R/2 |
| I | **240** | 120 vertex figures (edge 1) + 120 of edge phi (centre distance^2 = (3 - sqrt5)/8 R^2) |
| C | **600** | one orbit of 600 (stabiliser 24): edge phi = the 8 cells of each of the 75 inscribed tesseracts |
| T | **3000** | 600 cells (edge 1) + 600 of edge phi + 1200 of edge phi sqrt2 (two rotation orbits, a mirror pair: the 16 cells of each of the 75 inscribed 16-cells = the two tetrahedra in each of the 600 cubes) + 600 of edge phi^2 |
| O | **900** | 600 of edge phi (the 24 cells of each of the 25 inscribed 24-cells) + 300 central, edge phi sqrt2 (4 in each of the 75 16-cells) |
| (4D) | | 25 24-cells, 75 16-cells, 75 tesseracts, no regular 5-cell |

## Table 2. The 120-cell (600 corners, edge 1)
| solid | total | orbits (size: edge^2) |
|---|---|---|
| D | **1560** | 120 cells (1) + 120 (phi^2) + 1200 (2 phi^2) + 120 (phi^4) |
| I | **2400** | 1200 (2 phi^2) + 1200 (2 phi^4) |
| C | **7200** | 600 (phi^2) + 600 (phi^4) + 4800 (2 phi^4) + 600 (2 phi^4) + 600 (phi^6) |
| T | **34 200** | 14 orbits; 600 of them are the vertex figures (edge^2 phi^2) |
| O | **8100** | 4800 + 600 (2 phi^4) + 2400 + 300 central (4 phi^4) |
| (4D) | | 225 24-cells (25 + 200), 675 16-cells (75 + 600), 675 tesseracts (75 + 600), 840 regular 5-cells (120 + 720) |
All orbit data (stabilisers, centre distances, rotation splits) are in `data/residents-full.json`, key `queens`.

## Table 3. The Law of Residents (every 0/1 seed: 15 each of A4, B4, F4, H4; 7 each of A3, B3, H3)
| family | residents (union over the family) | per polytope |
|---|---|---|
| A4 | T, O | 4 of the 15 hold none (cantitruncated, runcitruncated, both ways) |
| B4 | C, T, O | 16-cell, truncated 16-cell, bitruncated tesseract and cantitruncated tesseract have no C |
| F4 | C, T, O | all 15 hold C, T, O |
| H4 | D, I, C, T, O | **all 15 hold all five** (counts per polytope in the json; e.g. omnitruncated 120-cell 28 800, 57 600, 144 000, 734 400, 216 000) |

**Theorem (no D or I outside the Queens' family; proof, exact).** The A4, B4 and F4 orbits have every coordinate in Q(sqrt2) (by
construction: the roots have entries in Z/2 with norms 1, 2, 4 and 8, and the seed solves a linear system whose right-hand side lies in
Q(sqrt2)), so every squared distance lies in Q(sqrt2). The dodecahedron's faces and the icosahedron's five neighbours of a corner are
regular pentagons, with diagonal^2 / side^2 = phi^2 = (3 + sqrt5)/2. This is not in Q(sqrt2): if sqrt5 = a + b sqrt2 with a, b rational,
then 2ab = 0, so sqrt5 or sqrt(5/2) would be rational. So no A4, B4 or F4 polytope (and no D4 polytope, since these are B4 or F4 ones)
has a D or I among its corners. The scan agrees.

**What was checked, precisely:** "Of all the reflection-group polytopes, only the Queens' family houses all five" is proved and checked
for the uniform polytopes of the four irreducible 4D groups A4, B4, F4, H4 (D4 included). The following were also checked, and none of
them holds all five: the 7 uniform H3 prisms (the dodecahedron prism holds D, C, T; the icosahedron prism I; the cantellated and
omnitruncated dodecahedron prisms C, T, O), the snub 24-cell (I 48, C 192, T 936, O 432, no D) and the grand antiprism (D 20, C 200,
T 1600, O 300, no I). **Not checked:** the duoprisms {p}x{q} (an infinite family, outside Q(sqrt5)). The sentence in the book should say
"of the four four-dimensional reflection groups".

## One World inside the 600-cell (with #106 Table 1, dodecahedron edge 1)
- Every one of the 120 dodecahedra has **all 5** of its Euclid cubes (edge phi, Elements XIII.17) and all 10 of their tetrahedra (edge
  phi sqrt2) on the 600-cell's corners. This is forced, since their corners are corners of the dodecahedron. Each of the 600 cubes lies
  in exactly one dodecahedron, and so does each of the 1200 tetrahedra of edge phi sqrt2: **the 600 cubes are exactly the Euclid cubes
  of the 120 dodecahedra**. The draft's "two of the five Euclid cubes" (from the float search of 11 Nov) is wrong: it is five.
- One World's other sizes: octahedra of edge phi/sqrt2 or phi^2/sqrt2: **none**. Icosahedron of edge 1/phi: **none**. Icosahedron of
  edge 1: 120 (the vertex figures), but **no icosahedron or octahedron of any size is concentric with any of the dodecahedra**.
  So the nesting D (1) ⊃ C (phi) ⊃ T (phi sqrt2) holds at One World's sizes. The octahedron and icosahedron of One World do not.

## Controls (all ok)
Group orders 24, 48, 120, 120, 384, 1152, 14400. Corners = |W| / |W_J| for all 81 polytopes, and the 15 H4 corner counts against
Coxeter's. Tetrahedron T 1; cube C 1, T 2; octahedron O 1; dodecahedron D 1, C 5, T 10; icosahedron I 1; icosidodecahedron O 5. 600-cell:
600 tetrahedral cells, 120 icosahedral vertex figures (Coxeter, Regular Polytopes), 25 inscribed 24-cells, 75 inscribed 16-cells.
120-cell: 120 dodecahedral cells, 675 inscribed 16-cells, regular 5-cells in orbits 120 (the full-stabiliser orbit) and 720.
Consistency: the 24-cell = rectified 16-cell, and the B4/F4 coincidences, give identical counts. The search from every corner equals the closure.
Remark: the "120 5-cells inscribed in the 120-cell" of the 600-cell article is the orbit with full stabiliser. All 840 together are the
regular compounds of 120 and 720 5-cells listed in the polytope-compound article (Coxeter; McMullen 2018). Likewise 25 + 200 24-cells and
75 + 600 16-cells match the listed compounds of 25 and 200 24-cells and 75 and 600 16-cells.

## Sources checked
H. S. M. Coxeter, *Regular Polytopes*, 3rd ed., Dover 1973 (cells, vertex figures, corner counts of {3,3,5}, {5,3,3}; regular compounds,
ch. 14). Wikipedia, "600-cell" (library copy, 2026): 25 inscribed 24-cells, 75 16-cells, table "inscribed: 120 in 120-cell, 675 in
120-cell". Wikipedia, "Polytope compound" (library copy, 2026): compounds of 75 16-cells, 25 24-cells, 120 and 720 5-cells, 200 24-cells,
600 16-cells. P. McMullen, New regular compounds of 4-polytopes (2018), as cited there. Koca, Koca and Al-Ajmi 2011, Branching of the H4
polytopes (library; consulted for the family, no count taken from it). Euclid, *Elements* XIII.17. DICTO: #106 One World for the Platonic
Solids (Table 1 sizes); #108 Atlas of the Chains (draft), Observation 5; study 2026-11-11-orbit-polytopes (the float search, now superseded
by this one for the counts and corrected on the Euclid cubes).
