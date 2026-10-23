# The AXE gap of the simple cubic icosahedron lattice (design study, 2026-10-23)

Credit: DICTO (design study, 2026-10-23), with Claude. Names are DICTO's: Unborn, Lotus Jewel, Tricap, AXE. The solid Unborn is
Koca, Koca, Al-Mukhaini & Al-Qanobi 2015's pseudoicosahedron (x = 1/τ); its role as the cut void of this lattice is DICTO's.

## Theorem

Put unit icosahedra (edge 1, corners the cyclic permutations of (0, ±1/2, ±φ/2)) on the simple cubic lattice of spacing φ, and in
each cell centre (φ/2)(1, 1, 1) the regular dodecahedron of edge 1/φ in the EKP orientation (its cube of edge 1 on the axes). Then:

1. Each icosahedron meets each of its 8 corner dodecahedra in exactly one **Tricap** (Mosseri–Sadoc t3, volume (3 − √5)/24), and no
   two Tricaps overlap. The icosahedron minus its 8 Tricaps is the **Lotus Jewel**, (1 + 3√5)/4; the dodecahedron minus its 8 Tricaps
   is the **Unborn**, the convex hull of the 12 points cyclic (±φ/2, ±1/(2φ), 0) round the cell centre: 8 equilateral faces of edge 1,
   12 isosceles (1/φ, 1, 1), 30 edges (6 of 1/φ), volume (3 + 7√5)/12.
2. The space the icosahedra and dodecahedra leave is exactly **6 AXE per cell** (Mosseri–Sadoc t6: five edges 1, one edge 1/φ,
   volume 1/12). One of them has corners (−1/2, φ/2, 0), (1/2, φ/2, 0), (0, φ/2 ± 1/(2φ), φ/2): its edge of 1 is the edge the
   icosahedra at 0 and (0, φ, 0) share, its edge of 1/φ the edge the Unborns of two neighbouring cells share. The other five are its
   images under the pyritohedral group m-3 about the icosahedron's centre, reduced mod the lattice: two on each cell face.
3. Hence these fill space, with nothing left over and nothing covered twice, per cell (φ³ = 2 + √5 exactly in Q(√5)):
   - icosahedron + Unborn + 6 AXE: 5(3 + √5)/12 + (3 + 7√5)/12 + 1/2;
   - Lotus Jewel + dodecahedron + 6 AXE;
   - Lotus Jewel + 8 Tricaps + Unborn + 6 AXE;
   - and any assignment of each Tricap to its icosahedron or to its dodecahedron, with the 6 AXE: for example whole dodecahedra in
     some blocks of cells and whole icosahedra in others ("Mixed blocks"), the pieces where blocks meet being an icosahedron or a
     dodecahedron that keeps 1 to 7 of its Tricaps.

Part 3's last line follows from 1 and 2: every Tricap lies in exactly one icosahedron and one dodecahedron and nowhere else in the
first two tilings, so moving it from one to the other changes nothing else.

## Checks (`axe-gap-check.py`, output in `axe-gap-check.log`, 43 checks, 0 failures)

Run from the repo root: `python3 studies/2026-10-23-axe-gap/axe-gap-check.py` (numpy, scipy).

- Unborn's 12 corners equal the earlier study's H (`../2026-10-10-icosa-networks-2/data/sc-star-H-unit.json`); faces, edge lengths,
  volume (3 + 7√5)/12; the dodecahedron (H + cube corners) has 20 corners and volume (5 + √5)/4.
- 6 distinct AXE per cell, each congruent to krp-core's KIT13_ICOSA13_AXE by corner matching, volume 1/12; each one's long edge on
  two icosahedra, its 1/φ edge on two Unborns; centroids two on each of the faces x, y, z = 0.
- 8 Tricaps, volume (3 − √5)/24, each inside its icosahedron and its dodecahedron, congruent to each other.
- Exact volumes in Q(√5) (Fraction arithmetic): icosahedron = Lotus Jewel + 8 Tricaps, dodecahedron = Unborn + 8 Tricaps, and
  all three per-cell sums equal 2 + √5.
- Point tests, 200 000 random points of one cell: 0 in no piece, 0 in more than one, for the three readings of part 3. Sample
  shares, e.g. icosahedron 0.5156 (exact 0.5150), Unborn 0.3658 (0.3669), AXE 0.1185 (0.1180).
- The app's Lotus Jewel mesh (`../2026-10-10-icosa-networks-3/data/clawed-icosahedron-unit.json`) is the icosahedron minus its
  8 Tricaps: winding numbers at 40 000 points, 0 disagree.
- Mixed blocks, 200 000 points over 6 × 6 × 6 cells, cell by cell: two random Tricap assignments; and the app's four patterns
  (layers, rods, checker, pyrochlore = fcc(8) + {(1,1,1), (1,−1,−1), (−1,1,−1), (−1,−1,1)}, 16 per 8³ blocks) at block sizes 1, 2
  and 3, each also swapped (whole icosahedra on the marked blocks of lattice points): 0 uncovered, 0 doubled in every case. (The
  app moves each pattern so a block sits on the middle; a translation, so the same.)

The app side is checked too: `scripts/build-octet-data.py` asserts the cells it writes (Unborn = the void dodecahedron's 12 non-cube
corners, Tricap apexes and bases, Lotus Jewel corners, 2 AXE per face); `tests/unit/octet-axe.test.mjs` counts the pieces per cell
(6 AXE, 8 Tricaps), adds their volumes to φ³, point-tests the convex network and, for Mixed blocks, checks every piece closed with
its kind's volume and every test point near the middle in exactly one piece (winding numbers); krp-core's
`tests/unit/unborn.test.mjs` and `scripts/verify-icosa.mjs` check the Unborn shape.

## Data

Scale **unit** = icosahedron edge 1 (krp-core POLYHEDRA scale); **raw** = unit / (φ/2), the EKP frame of the earlier studies.

- `data/unborn-{unit,raw}.json`: the Unborn, centred, faces outward, exact volume.
- `data/axe-cell-parts-{unit,raw}.json`: one cell: the icosahedron at the origin (role `ico`), its 8 Tricaps (role `tricap`, with
  their direction), the Unborn at (φ/2)(1, 1, 1) (role `unborn`) and the cell's 6 AXE (role `axe`, with `faceAxis`).

## Prior use (library check, and web search 2026-10-23)

What the sources say; "not found" is not the same as "new".

- **Unborn's shape, the pseudoicosahedron.** Koca, Koca, Al-Mukhaini & Al-Qanobi 2015 (arXiv 1506.04600, in the library) derive it
  from the pyritohedral group as the orbit of (1 + x)e₁ + x e₂ (cyclic, signs; the earlier study, §7 of
  `../2026-10-10-icosa-networks-2/README.md`, identified this solid in their family as x = 1/τ); with integer or rational x the
  corners lie in the simple cubic lattice, and they ask whether a pyrite crystal (their Fig. 18) has this form. Their remark that "the truncated octahedron … splits into two pseudoicosahedra
  which are mirror images" is, on reading §4.3 of the library PDF, about **vertices**: the 24 corners of the truncated octahedron
  are the union of the corners of two mirror pseudoicosahedra (x = 1), not a cutting of its volume. Also: "Symmetry of the
  Pyritohedron and Lattices" (SQU J. Sci. 21(2), 2016, doi 10.24200/squjs.vol21iss2pp139-149) and arXiv 1606.02445 (4D
  pyritohedral symmetry, polytopes and lattices), not read in full. No source found uses pseudoicosahedra as a space filler, in a
  honeycomb, or between regular icosahedra.
- **AXE (Mosseri–Sadoc t6).** The six tetrahedra of Mosseri & Sadoc 1982 and Kramer 1982 build aperiodic icosahedral (3D Penrose
  type) tilings; Papadopolos & Ogievetsky give inflation rules and Dehn invariants (arXiv math-ph/9911005, math-ph/9910006); Koca et
  al. 2020 dissect the dodecahedron and related solids with them (arXiv 2009.07048, Acta Cryst. A, in the library) and build
  icosahedral tilings with dodecahedral structures (arXiv 2008.00862); Al-Siyabi, Koca & Koca 2020 relate them to D6 and Danzer's
  ABCK (arXiv 2003.13449); Al Raisi et al. 2026 modify them from D6 (arXiv 2604.03988, in the library). Every use found is
  aperiodic; none fills the gap of a periodic packing.
- **Edge-sharing regular icosahedra on a simple cubic net:** the Cs₈Sn₄₆ clathrate and Dewar 2024 (both in
  `../2026-10-10-icosa-networks-2/README.md` §7); neither gives the void piece or the density.
- The library (`~/Documents/kaleidohedra-references`, papers/MANIFEST.json) has nothing on icosahedron + dodecahedron packings
  beyond these.

So the three ingredients are each known: the icosahedron net, the pseudoicosahedron, and AXE as a tile of aperiodic tilings. Unborn
+ 6 AXE closing the simple cubic icosahedron lattice, its Lotus Jewel twin, the four-kind tiling and the free Tricap assignment were
not found in the library or these searches. The crystal-chemistry literature (clathrates, intermetallics with icosahedral and
dodecahedral cages) is the most likely place for prior use not found here.

## In the app

DICTO → 3D+ → DICTO Icosahedral Octet: the **Lotus Jewel network** (now with its AXE), **Icosahedra and Unborn**, **Icosahedra,
dodecahedra and AXE** (Lotus Jewel green, Tricap purple, Unborn gold, AXE cyan) and **Mixed blocks** (whole icosahedra green, Lotus
Jewels dark green, whole dodecahedra gold, Unborns orange, transition pieces pink, AXE cyan; Pattern, Block size, Swap). The AXE
button hides and shows the AXE. The first three are also in the Icosahedral Octet Lattice to build cell by cell. The Unborn is a
piece in Polyhedraverse's DICTO's pieces.
