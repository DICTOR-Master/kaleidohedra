# Kaleidohedra discoveries

*Kaleidohedra by DICTO — working notes, started 2026-10-01.*

Findings made while playing in Rhombiverse, Polyhedraverse and Kaleidohedra,
with how each one is verified and whether it appears to be new.
Every geometric claim here is checked exactly by a script that runs on every
push (`scripts/verify-kaleido.mjs` in this repo; `verify-zome-parallelohedra`
in Polyhedraverse; `verify-dicto-fcc` in Rhombiverse).

**Status** means only what a literature search on 2026-10-01 turned up
(Wikipedia, MathWorld, the Polytope Wiki, George Hart's zonohedra pages).
"Not found" is not proof of novelty; a specialist search (e.g. Fedorov /
Delone / Štogrin parallelohedra literature) is still needed before claiming
priority.

A deeper search on 2026-10-06 for #1 and #5 (Grünbaum's 2010 survey of
parallelohedra and zonohedra, Lalvani's zonohedra patents, the icosahedral
tiling literature, the contents of Hart & Picciotto's *Zome Geometry*) found
#5 known (see #5) and did not find #1. Not yet checked, as they are not
online: Fedorov's 1885 book, Lalvani's *Structures on Hyper-Structures*
(1982) and the printed chapters 14 and 16 of *Zome Geometry*.

| # | Finding | Credit | Verified | Status | First recorded |
|---|---|---|---|---|---|
| 1 | DICTO skewed rhombic dodecahedron | DICTO (found by building it) | yes | **not found** — candidate | 2026-10-01 (8420a51) |
| 2 | Equal-edge rule for sheared FCC | Kaleidohedra | yes | general idea known; this form not found | 2026-10-01 (8420a51) |
| 3 | Bain disphenoids become regular tetrahedra | — | yes | **known** (Bain, 1924) | 2026-10-01 (8420a51) |
| 4 | Bain rhombic dodecahedron (squares + 60° rhombi) | — | yes | **known** | 2026-10-01 (8420a51) |
| 5 | Regular-hexagon elongated dodecahedron | DICTO, independently (from the "hexagons and rhombi" hunch) | yes | **known** — the truncated octahedron with one zone removed (Fedorov's ED as drawn by Grünbaum 2010); DICTO's route, the Bain stretch, is new | 2026-10-01 (8420a51) |
| 6 | Exactly 9 "most regular" space-fillers | Kaleidohedra two-way search | yes | not yet searched | 2026-10-01 (547aac9) |
| 7 | DICTO skewed ED (two forms) | Kaleidohedra (extending #1) | yes | not yet searched | 2026-10-01 (e97193f) |
| 8 | Euclid–Kepler–Pacioli (EKP) cell: all five Platonic solids nested in one cubic cell, with Kepler's star and Pacioli's rectangles (Pm-3) | DICTO (built a physical cell) | yes | **not found** — candidate; a periodic approximant-type structure like α-AlMnSi (no fivefold axis) | 2026-10-06 (6636342) |
| 8b | Euclid–Kepler–Pacioli network: great stellated dodecahedra (even cells) and icosahedra (odd cells), sharing only corners | DICTO (from "the overlap belongs to the extraction") | yes | **not found** — candidate | 2026-10-06 |
| 9 | Rhombic dodecahedron sub-family: 24 sheared-FCC cells from TARGETS.md, each built from four edge directions with volume matching the table | Kaleidohedra (predicted); verified by building in Polyhedraverse (9599e14) | yes (by construction) | **candidates** — combinatorial type is Fedorov's rhombic dodecahedron (Grünbaum 2010, Fig. 2(c)); none is in Grünbaum's monohedral enumeration (Figs. 3, 10: only Kepler's K and Bilinski's B), and the paper doesn't list mixed-angle cells like these | 2026-10-06 |

## 1. DICTO skewed rhombic dodecahedron

A rhombic-dodecahedron-type space-filler whose four equal edge directions
meet at **60° three times and 72° three times**. Its faces are 60° rhombi and 72° rhombi.
It splits into DICTO's two all-rhombus blocks (volume φ/2 each) and two
flattened rhombohedra (½ each), so its volume is exactly
**2·φ/2 + 2·½ = φ²** (the golden ratio's identity φ² = φ + 1 as a volume).
It tiles a sheared FCC lattice, DICTO FCC.

- Verified: Polyhedraverse `verify-zome-parallelohedra`, Rhombiverse
  `verify-dicto-fcc`, and here (path stop 2 with Cell = 1 is exactly this cell).
- Nearest known relative: the **Bilinski dodecahedron** (1960), also an
  RD-type space-filler with golden-ratio geometry, but its twelve faces are
  congruent golden rhombi (63.43°). DICTO's has two kinds of face, 60° and
  72° rhombi.
- Full write-up: Polyhedraverse `docs/dicto-zometool-discoveries.md`.

## 2. The equal-edge rule

Shear the FCC lattice any way at all. The RD-type cells that still tile the
sheared lattice are exactly the sheared RD's four edge directions, each
shifted by one common vector w; every w keeps all 12 neighbour
translations. **Exactly one** w makes all four edges equal: the circumcentre
of the four negated directions. That one cell is the regular RD for plain
FCC, and exactly DICTO's skewed RD for DICTO FCC. This is the Cell slider.

- Verified here: "Cell = 1 always has four equal edges", "the Cell slider
  keeps the lattice", and the two exact matches.
- Status: equilateral versions of any zonohedron type are well known (Hart;
  Wikipedia "Zonohedron"). The statement for a *fixed* sheared lattice, with
  a unique equal-edge member and the circumcentre construction, was not found.

## 3. Bain disphenoids

Stretch BCC by √2 along one cube axis and it becomes FCC. Of the six BCC
disphenoid orientations, the two whose long edges lie across that axis become
**regular tetrahedra**; the other four become quarters of regular octahedra.
Along the DICTO path the disphenoids only get less regular, and plain BCC is
the most regular overall (a regular tetrahedron cannot fill space alone).

- Verified here (Towards → Bain; the Disphenoids meter).
- Status: **known** — the Bain correspondence (E. C. Bain, 1924), standard in
  metallurgy. Kaleidohedra makes it something you can slide through and see.

## 4. Bain rhombic dodecahedron

At the Bain stop the equal-edge RD cell has edge directions meeting at
60, 60, 60, 60, 90, 90 degrees: **4 squares and 8 rhombi of 60°**, all edges
equal.

- Verified here ("Bain RD").
- Status: **known** — listed on Wikipedia's rhombic dodecahedron page as the
  D4h form, "a cuboctahedron with square pyramids attached on the top and
  bottom".

## 5. Regular-hexagon elongated dodecahedron

Add a fifth edge direction to the Bain RD along an unstretched cube axis, of
the same length. Every edge is 1, and the elongation direction lies at 60° to
two pairs of RD directions in their planes, so the faces are:

- **4 regular hexagons**
- **4 squares**
- **4 rhombi of 60°** (each two equilateral triangles)

It is an elongated-dodecahedron-type zonohedron, so it fills space by
translation (Fedorov). Every face is made of regular polygons. Elongated
along the stretched axis instead, it has 8 rhombi of 60° and 4 equal-edged
hexagons with corners 135°, 135°, 90° (a square with two corners cut at 45°).

- Verified here ("Bain ED along x", "Bain ED along z").
- Not the Polyhedraverse ED sheared: that one's elongation is the RD's edge
  √3/2 before the shear, giving hexagon edges 1, 1, 0.866. The regular-hexagon
  form needs the elongation 2/√3 times longer.
- Status: **known; reached independently by DICTO by a different route.**
  It is the truncated octahedron with one of its six zones removed: the two
  squares containing that edge direction shrink to edges, the four hexagons
  containing it shrink to 60° rhombi, and 4 regular hexagons, 4 squares and
  4 60° rhombi remain. Wikipedia and the Polytope Wiki describe it as the
  "contraction of a uniform truncated octahedron" (an earlier reading here
  wrongly took that form to have no squares), and Grünbaum (2010, Fig. 2(b))
  draws it as Fedorov's representative elongated dodecahedron, "with regular
  faces". DICTO arrived at it on 2026-10-01 from the other side: the Bain
  stretch's equal-edge RD plus one unstretched cube axis. `verify-targets`
  checks that the two routes give the same cell (same edge-direction angles,
  faces and volume 4√2). The construction route is DICTO's; the shape is not
  new. It remains Kaleidohedra's symbol.

## 6. The nine most regular space-fillers

Every space-filling zonohedron with all edges equal whose faces are only
squares, regular hexagons and 60° rhombi (each two equilateral triangles):
there are **exactly 9** — four parallelepipeds (the cube, the 60°
rhombohedron, and two mixed), two hexagonal prisms (the regular one, and
one leaning with 60° rhombi), the Bain RD (#4), the regular-hexagon ED
(#5) and the regular truncated octahedron.

- Verified: `discover.py` builds every candidate exactly (top-down) and an
  independent random search over all cell shapes agrees (TARGETS.md).
  Such faces need only 60° and 90° angles, which the search covers
  exactly, so the list is complete.
- Status: not yet searched. It says #4 and #5 are the *only* RD and ED
  forms of this kind.

## 7. DICTO skewed ED

Add a fifth edge direction to DICTO's skewed RD (#1), the same recipe #5 used
on the Bain RD. Unlike the Bain RD, DICTO's RD has no 90° relationships at
all, so the new direction can't join it at 60° or 90° the way #5's did — it
meets the existing four at 36° twice and 60° or 72° twice, and the belt test
(Venkov) allows exactly two space-filling choices, both already present in
TARGETS.md's search:

| | Faces | Volume |
|---|---|---|
| **ED #16** | 4 rhombi of 60°, 4 rhombi of 72°, 2 hexagons (36°/36°/72° corners), 2 regular hexagons | **φ² + 2** |
| **ED #18** | 6 rhombi of 60°, 2 rhombi of 72°, 4 hexagons (36°/72°/72° corners) | **φ³ + ½** |

Both keep DICTO's skewed RD's own four directions unchanged as a sub-set —
found by matching `DICTO_DIRECTIONS`' Gram matrix against every ED cell's
4-direction sub-sets in `data/geometry-targets.json`; exactly these two contain it.
Neither has a square face, consistent with DICTO's RD having none.

- Verified here (`DICTO_SKEWED_ED_16`, `DICTO_SKEWED_ED_18` in
  `src/geometry-extensions/dicto-fcc.js`): equal edges, the face counts above,
  the exact volumes, and that both keep DICTO's four directions unchanged.
- `TARGETS.md` rows 16 and 18 (elongated dodecahedron section) updated from
  "to find" to built.
- Status: not yet searched (same caveat as #1 — a specialist parallelohedra
  literature search would be needed to claim priority).

## 8. Euclid–Kepler–Pacioli (EKP) cell

*Named 2026-10-06 by DICTO, whose artist name stands for Euclid's five Platonic
solids, all of which now nest in this one cell: **Euclid** for the roofs on the
cube (Elements XIII), **Kepler** for his great stellated dodecahedron, his
stella octangula and his nested solids, **Pacioli** for the three golden
rectangles the neighbouring roofs form. Short name **EKP by DICTO**. Extraction
(b) below is the **Euclid–Kepler–Pacioli network**. Code and file names keep the
working name "roof-fold".*

Put Euclid's roofs on a cube of edge 2 to make the regular dodecahedron, then
reflect the 12 roof vertices back through the six cube faces: they land on a
regular icosahedron inside the cube. Repeat the cell by translations of 2
along x, y and z.

- **Edges:** cube 2, dodecahedron 2/φ, icosahedron 2/φ² — a φ² : φ : 1 chain,
  every edge along one of the 15 two-fold axes of the icosahedron.
- **Nodes:** 13 per cell — one cube corner and the 12 icosahedron vertices.
  Every roof vertex is a vertex of a neighbouring cell's icosahedron.
- **Spikes:** over each of the icosahedron's 20 faces sits exactly one node at
  2/φ from its three corners; the 20 tips are the dodecahedron's vertices and
  the spike faces are golden triangles (36° apex).
- **Aligned symmetry** (DICTO's point, 2026-10-06: "the symmetries all
  align in every direction"). Every cell repeats one orientation, so each
  cell's solids carry the icosahedron's **31 rotation axes** (6 five-fold,
  10 three-fold, 15 two-fold; 62 directions), all parallel through the whole
  crystal. Of these, **7** are symmetries of the crystal itself (the 3 cube
  axes as two-fold, the 4 body diagonals as three-fold); the other 24 are
  local but aligned (non-crystallographic symmetry). The crystal's group m-3
  is exactly the cube's symmetries that are also the icosahedron's, the most
  icosahedral symmetry a periodic crystal can keep. Checked in CI.
- **Pacioli's golden rectangles are the neighbours' roofs** (DICTO,
  2026-10-06: "four elements of roofing structure overlap, making golden
  section rectangles"). Each roof ridge, seen from the neighbouring cell it
  pokes into, is the long side of a golden rectangle (2/φ × 2/φ²); the six
  neighbours' ridges make, inside every cube, the three mutually
  perpendicular interlocking (Borromean) golden rectangles of Pacioli's *De
  divina proportione* (1509), whose 12 corners are the icosahedron. So the
  fold is literally the neighbours' roofs meeting in the middle.
- **Kepler's chain in one cell** (DICTO, 2026-10-06, as a homage to
  Kepler's nested solids). The two regular tetrahedra on alternate cube
  corners (the stella octangula, Kepler's name) overlap in the octahedron on
  the six cube-face centres, and the icosahedron's 12 vertices lie one on
  each of the octahedron's 12 edges at the golden section (and 8 of its faces
  lie in the octahedron's 8 face planes). So all five
  Platonic solids nest exactly in one cell, **icosahedron ⊂ octahedron ⊂
  tetrahedra ⊂ cube ⊂ dodecahedron**, with Kepler's great stellated
  dodecahedron around the icosahedron. Each step is classical; the chain as
  one periodic cell has not been searched. The stella octangula keeps all
  of m-3 (one tetrahedron alone keeps only the 12 rotations, 23). The
  tetrahedra and octahedron edges lie along cube face diagonals (√2, 2√2),
  not the icosahedral axes, so a physical build needs a second rod family.
- **Not a tiling:** the dodecahedra overlap. Space is covered once (19%) or
  twice (81%), mean (5+√5)/4 ≈ 1.809, the dodecahedron's volume 10 + 2√5 over
  the cell's 8.
- **Symmetry:** exactly the 24 operations of m-3 keep the node set, each
  with a lattice translation only, so the space group is **Pm-3 (No. 200)**,
  primitive cubic — not FCC, not aperiodic, no fivefold axis. With the origin
  at the icosahedron centre the nodes are on Wyckoff **1b** (the corner) and
  **12j** (0, y, z), y = 1/(2φ) ≈ 0.309, z = 1/(2φ²) ≈ 0.191.

- **Neighbours:** face-neighbour dodecahedra overlap; edge-neighbour ones don't
  overlap but share a cube edge and touch over a small coplanar patch of
  opposite pentagons; corner neighbours share one vertex. Adding dodecahedra
  across their own faces only reaches cells of one parity, i.e. an FCC
  sublattice. *(Recorded 2026-10-06.)*
- **Colourings:** colouring the cells breaks the symmetry in exact steps:
  x+y+z parity gives **Fm-3** (No. 202), x+y gives **Cmmm** (No. 65), z gives
  **Pmmm** (No. 47), and 8 octant colours give **Pmmm** on a doubled cell.
  *(Recorded 2026-10-06.)*
- **The star is Kepler's great stellated dodecahedron** {5/2, 3} (Kepler
  1619): the icosahedron with 20 golden-triangle spikes, whose 60 visible
  triangles lie in 12 planes as 12 regular pentagrams (edge φ³ × the core
  icosahedron edge) and whose 20 tips are the dodecahedron's vertices. Volume
  ≈ 2.918 at cube edge 2; its convex hull is the dodecahedron. So one cell
  holds Euclid's dodecahedron, the icosahedron and Kepler's star, all nested
  on the same 20 + 12 points. *(Identity known; its place in this cell
  recorded 2026-10-06.)*
- **Extractions that don't overlap** (DICTO's point, 2026-10-06: the
  overlap belongs to the solids chosen, not to the vertices). From the same
  13-node set:
  - **(a)** dodecahedra on the even cells alone (an FCC lattice) touch their
    12 nearest neighbours and never overlap, density exactly
    (5+√5)/8 ≈ 0.9045 — the **optimal lattice packing** of the regular
    dodecahedron (Betke & Henk; Torquato & Jiao 2009 note it contacts 12
    neighbours and its lattice coincides with FCC). **Known**, here
    re-found inside the structure.
  - **(b)** great stellated dodecahedra on the even cells (an FCC lattice,
    touching tip to tip at shared cube corners) with icosahedra on the odd
    cells share **only corners**: every star's 12 roof tips are vertices of
    the 6 neighbouring icosahedra, and an exact separating-axis test finds no
    overlap. A corner-sharing (Kagome-like) network of Kepler stars and
    icosahedra: the **Euclid–Kepler–Pacioli network**. **Not found** — candidate
    (targeted search below).
  - Dodecahedra on even cells with icosahedra on odd cells do overlap; the
    stars are what make (b) corner-sharing.
- **Literature search (web-level, 2026-10-06).** Status of the parts:
  - Euclid's roof construction of the dodecahedron on a cube (Elements
    XIII) and the pyritohedral icosahedron inscribed in a cube are classical.
  - Periodic crystals with icosahedral or dodecahedral motifs are well known
    and do not break the crystallographic restriction: α-AlMnSi (Pm-3, the
    1/1 cubic approximant, Mackay icosahedra), skutterudites (Im-3,
    icosahedral cages on 24g (0, y, z)), type-I clathrates (Pm-3n,
    pentagonal-dodecahedral cages). This structure is of that kind: m-3, no
    fivefold axis.
  - **Not found:** the fold itself (roof vertices reflected through the
    cube faces give the regular icosahedron, each roof vertex landing on a
    neighbouring cell's icosahedron vertex), the exact φ² : φ : 1 cell as a
    13-node Pm-3 structure, and extraction (b). Koca et al. (2016,
    pyritohedral group, pseudoicosahedra and cubic lattices) is the closest
    paper found; its abstract does not describe this, but the full text was
    not read.
  - **Targeted search for (b)** (2026-10-06): great stellated dodecahedron
    packings, Kepler–Poinsot polyhedra in lattices, corner-sharing icosahedral
    frameworks. The only packing work found is de Graaf, van Roij & Dijkstra
    (PRL 107, 155501, 2011), whose densest-known packing of great stellated
    dodecahedra is a **dimer lattice of two orientations with interlocking
    spikes**, and has no icosahedra. (b) is a different arrangement (one
    orientation, FCC, corner contacts only, icosahedra in the other cells)
    and was not found.
  - **Construction-kit and maths-art search** (2026-10-06): George Hart's
    pages and Zome Geometry book, nested-Platonic-solid kit models, and the
    Bridges archive. Found only single nested objects (an icosahedron in a
    cube; the five nested Platonic solids with Euclid's roof caps; a stellated
    dodecahedron inside an icosahedron, Hildebrandt, Bridges 2006) and other
    periodic structures (Gailiunas, triply periodic links, Bridges 2022). No
    periodic arrangement of this cell or of the Euclid–Kepler–Pacioli network. The
    dodecahedral–icosahedral honeycomb that fits these solids face to face
    exists only in hyperbolic space.
  - Before claiming priority: check Koca et al. in full, approximant and
    skutterudite structure databases (Bilbao, ICSD) for a 1b + 12j set with
    y = 1/(2φ), z = 1/(2φ²), and stellated-icosahedron framework literature.
- Status: the cell and (b) **not found** — candidates; (a) **known**.

## 9. Rhombic dodecahedron sub-family (candidates)

Targets 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24 and 26 of the rhombic-dodecahedron table in TARGETS.md. Each is a zonohedron of four unit edge directions (edge 1), built in Polyhedraverse as RD_TARGET_N and checked against the table's volume. Verified by building, not by literature. Listed here as candidates until the Grünbaum 2010 tables are checked for each. Any that turn out not to appear there move to the table above as not found.

**Provenance (Grünbaum 2010, read in full):**
- Combinatorial type: each is a zonohedron of four directions, so it has the combinatorial type of Fedorov's rhombic dodecahedron (Fig. 2(c), Kepler's K). Fedorov's list of the five parallelohedron types covers this type, so no new type is involved.
- Monohedral (all faces congruent): Grünbaum's enumeration of monohedral rhombic dodecahedra (Figs. 3 and 10) gives only Kepler's K and Bilinski's B. None of the 24 is monohedral: each has two or more rhombus kinds (for example #4 has 36°, 60° and 72° rhombi), so none is one of those two.
- So the paper neither lists nor rules out these specific cells. They stay candidates until someone checks mixed-angle sheared rhombic dodecahedra in the literature.

## Attribution and dates

All findings above credited to DICTO are the work of the artist **DICTO**
(Japan), made while building physical models and playing in Rhombiverse,
Polyhedraverse and Kaleidohedra; "Kaleidohedra" credits mean found by this
project's own search, under DICTO's direction. "First recorded" is the date and
commit that first put the finding in this repository; the git history is the
timestamped record. A physical model may predate it (#1 was built in Zometool
before it was written up; #8's physical cell was built before 2026-10-06).

Please cite as: *DICTO, Kaleidohedra discoveries, #N (first recorded
YYYY-MM-DD), https://doi.org/10.5281/zenodo.23173809.*

The repository is public, so its commit history is a public timestamped record,
and it is archived on Zenodo: **DOI [10.5281/zenodo.23173809](https://doi.org/10.5281/zenodo.23173809)** (all versions);
finding #8, the Euclid–Kepler–Pacioli cell and network, is version v2026.10.06,
**DOI [10.5281/zenodo.23173810](https://doi.org/10.5281/zenodo.23173810)**, published 2026-10-06.
Renamed the Euclid–Kepler–Pacioli (EKP) cell, with Kepler's chain and Pacioli's
rectangles, as version v2026.10.06-ekp, **DOI [10.5281/zenodo.23176568](https://doi.org/10.5281/zenodo.23176568)**.

## Sources

- [The Bilinski dodecahedron and assorted parallelohedra, zonohedra, monohedra, isozonohedra and otherhedra — Grünbaum, Math. Intelligencer 32 (2010)](https://faculty.washington.edu/moishe/branko/BG285%20Bilinski%20dodecahedron.pdf) (#5 is its Fig. 2(b))
- [Elongated dodecahedron — Wikipedia](https://en.wikipedia.org/wiki/Elongated_dodecahedron)
- [Elongated Dodecahedron — MathWorld](https://mathworld.wolfram.com/ElongatedDodecahedron.html)
- [Elongated rhombic dodecahedron — Polytope Wiki](https://polytope.miraheze.org/wiki/Elongated_rhombic_dodecahedron)
- [Rhombic dodecahedron — Wikipedia](https://en.wikipedia.org/wiki/Rhombic_dodecahedron)
- [Bilinski dodecahedron — Wikipedia](https://en.wikipedia.org/wiki/Bilinski_dodecahedron)
- [Dense packings of the Platonic and Archimedean solids — Torquato & Jiao (2009)](https://arxiv.org/abs/0909.0940)
- [Quaternionic representations of the pyritohedral group, related polyhedra and lattices — Koca et al.](https://arxiv.org/abs/1506.04600)
- [Pyritohedral icosahedron — Polytope Wiki](https://polytope.miraheze.org/wiki/Pyritohedral_icosahedron)
- [Dense regular packings of irregular nonconvex particles — de Graaf, van Roij & Dijkstra, PRL 107, 155501 (2011)](https://doi.org/10.1103/PhysRevLett.107.155501)
- [Zometool icosahedron in cube — George Hart, Zome Geometry](https://www.georgehart.com/zomebook/icosa-cube.html)
- [Zome-inspired sculpture — Paul Hildebrandt, Bridges 2006](https://archive.bridgesmathart.org/2006/bridges2006-335.pdf)
- [Dodecahedral-icosahedral honeycomb (hyperbolic) — Wikipedia](https://en.wikipedia.org/wiki/Dodecahedral-icosahedral_honeycomb)
- [Great stellated dodecahedron — Wikipedia](https://en.wikipedia.org/wiki/Great_stellated_dodecahedron)
- [Icosahedral tiling with dodecahedral structures — Koca et al. (2020)](https://arxiv.org/abs/2008.00862) (aperiodic; not this structure)
- [Zonohedron — Wikipedia](https://en.wikipedia.org/wiki/Zonohedron)
- [Zonohedrification — George Hart](https://www.georgehart.com/zonohedra/zonohedrification.html)
