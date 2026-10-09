# Kaleidohedra discoveries

*Kaleidohedra by DICTO — working notes, started 2026-10-01.*

Findings made while playing in Rhombiverse, Polyhedraverse and Kaleidohedra,
with how each one is verified and whether it appears to be new.
Every geometric claim here is checked exactly by a script that runs on every
push (`src/krp-core/scripts/verify-kaleido.mjs`, krp-core; `verify-zome-parallelohedra`
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
| 1 | DICTO skewed rhombic dodecahedron | DICTO (found by building it) | yes | **not found** as this member — the family (skewed RD parallelohedra) is known (Fedorov; Lalvani 1997) | 2026-10-01 (8420a51) |
| 2 | Equal-edge rule for sheared FCC | Kaleidohedra | yes | general idea known; this form not found | 2026-10-01 (8420a51) |
| 3 | Bain disphenoids become regular tetrahedra | — | yes | **known** (Bain, 1924) | 2026-10-01 (8420a51) |
| 4 | Bain rhombic dodecahedron (squares + 60° rhombi) | — | yes | **known** | 2026-10-01 (8420a51) |
| 5 | Regular-hexagon elongated dodecahedron | DICTO, independently (from the "hexagons and rhombi" hunch) | yes | **known** — the truncated octahedron with one zone removed (Fedorov's ED as drawn by Grünbaum 2010); DICTO's route, the Bain stretch, is new | 2026-10-01 (8420a51) |
| 6 | Exactly 9 "most regular" space-fillers | Kaleidohedra two-way search (its regular-hexagon elongated dodecahedron member: DICTO, independently, by lattice shearing) | yes | not yet searched as a set; that member is **known** (Grünbaum 2010, Fig. 2(b); see #5) | 2026-10-01 (547aac9) |
| 7 | DICTO skewed ED (two forms) | Kaleidohedra (extending #1) | yes | **not found** as these members — the family is known (Fedorov; Lalvani 1997) | 2026-10-01 (e97193f) |
| 8 | Euclid–Kepler–Pacioli (EKP) cell: all five Platonic solids nested in one cubic cell, with Kepler's star and Pacioli's rectangles (Pm-3) | DICTO (built a physical cell) | yes | **not found** — candidate; a periodic approximant-type structure like α-AlMnSi (no fivefold axis) | 2026-10-06 (6636342) |
| 8b | Euclid–Kepler–Pacioli network: great stellated dodecahedra (even cells) and icosahedra (odd cells), sharing only corners | DICTO (from "the overlap belongs to the extraction") | yes | **not found** — candidate | 2026-10-06 |
| 9 | Rhombic dodecahedron sub-family: 24 sheared-FCC cells from TARGETS.md, each built from four edge directions with volume matching the table | Kaleidohedra (predicted); verified by building in Polyhedraverse (9599e14) | yes (by construction) | **candidates** — combinatorial type is Fedorov's rhombic dodecahedron (Grünbaum 2010, Fig. 2(c)); none is in Grünbaum's monohedral enumeration (Figs. 3, 10: only Kepler's K and Bilinski's B), and the paper doesn't list mixed-angle cells like these | 2026-10-06 |
| 10 | EKP windows: the dodecahedron with its six face-neighbours' stella octangulas carved out shows exactly 12 Penrose thick rhombi (72°/108°, edge 2/φ), one on each cube edge, at the dodecahedron's own face angles; 48 triangles wall the cut-away; volume exactly 12 | DICTO (spotted 12 diamond windows between six stellas and the dodecahedron) | yes | **not found** — candidate (web-level search) | 2026-10-08 (fb9de6b) |
| 10a | Study of #10, the windows made convex: the 12 window rhombi pushed straight out by √(7 − 4φ), keeping size and orientation, hull into a 74-face solid with 12 Penrose thick rhombi, 6 golden rhombi on the cube faces, 8 equilateral triangles and 48 triangles; three edge lengths; has a flat net (recorded as #12 in Zenodo v2026.10.08-convex) | DICTO (asked to make the windows convex by expanding from the centre) | yes | study of #10, not a separate claim | 2026-10-08 |
| 10b | Study of #10, windows and stellas in a checkerboard: the windows (even cells) and stella octangulas (odd cells) fill space exactly, each odd cube being its stella plus its six neighbours' carved roofs; volumes 12 + 4 = two cubes | DICTO (asked for "a male counterpart to window" fitting the faces the stellas leave) | yes | study of #10, not a separate claim | 2026-10-08 (ac203df) |
| 11 | Dodecahedron stretched along a cube-face axis: 8 regular pentagons, 4 hexagons (108° × 4, 144° × 2), 2 rectangles at any stretch; squares at one edge (2/φ); at the lattice spacing 2 it is the hull of two EKP face-neighbour dodecahedra | DICTO (the "pentagon caps and hexagons" hunch, from overlapped dodecahedra) | yes | **not found** — candidate (web-level search; a simple construction, so likely to appear somewhere, e.g. crystal habits) | 2026-10-08 (fb9de6b) |
| 12 | Star Chain Reaction: the EKP great star is exactly the great stellated dodecahedron of the Dogstar's core (a dodecahedron 1/φ³ the cell's), and a whole Sunstar 1/φ³ the size fits inside it with no room to grow, so dodecahedron ⊃ great star ⊃ Sunstar(1/φ³) ⊃ great star(1/φ³) ⊃ … nests forever, each step touching, scale ratio φ³ | DICTO (asked for a Sunstar cell network and to search nestings; named it); found by Kaleidohedra's search under DICTO's direction. The Dogstar itself is George W. Hart's stellation 8 of the dodecahedron (1996) | yes | **not found** — candidate (web-level search, 2026-10-08) | 2026-10-08 (79448e3) |
| 12a | Study of #12, the Jewel chain: DICTO Jewel ⊃ cube ⊃ stella octangula ⊃ Dogstar ⊃ dodecahedron(1/φ³) ⊃ DICTO Jewel(1/φ³) ⊃ …, every step touching; the EKP cell recurs inside its own stella, through the Dogstar | DICTO (asked whether "another cell network" was buried in the DICTO Jewel); found by Kaleidohedra's search | yes | study of #12, not a separate claim | 2026-10-08 |
| 13 | The 13-dodecahedron cluster made solid: a regular dodecahedron with one on each face leaves gaps of exactly two kinds, 30 wedges (two pentagons hinged at 10.3048°, volume φ³/20) and 20 needles (volume (45 − 19√5)/600), and the filled cluster comes apart into 12 finned units | DICTO (designed the cluster; asked for its gaps as pieces, separable once built) | yes | **not found** — candidate (the 10.3° gap itself is well known) | 2026-10-09 |
| 14 | DICTO-Star: an icosidodecahedron with a regular dodecahedron on each pentagon and a tridiminished icosahedron (J63) on each triangle; 33 regular-faced pieces, every contact a whole face, every edge and corner closed, no filler, volume (195 + 89√5)/3 | DICTO (the centre of DICTO's builds, by 2026-10-04); confirmed exactly by the search DICTO asked for | yes | **not found** — candidate (the version with whole icosahedra, which overlaps, is Robert Austin's 2014 model) | 2026-10-09 |
| 15 | DICTO Jewel clusters: four DICTO Jewels in a tetrahedron (pairwise face to face, touching at one point in the middle) and six in an octahedron round a stella octangula, which fits them face for face (a solid piece); each a shape of its own, and each fills space with stella octangulas | DICTO (built the tetrahedral cluster in the app, asked for the octahedral, saw that both fill space with stellas) | yes | **not found** — candidate (made only of the DICTO Jewel, #10, itself not found) | 2026-10-09 |
| 16 | Sunstar clusters: the octet structure of #15 in the Sunstar Lattice; four dodecahedra round a cell corner, and six round an odd cell with its Dogstar inside, a solid piece (a Dogstar with its 6 dodecahedra: a Sunstar turned inside out); each fills space with Dogstars, and shared they form the octet network | DICTO (asked whether the octet network held for the Sunstars and Dogstars) | yes | **not found** — candidate (the honeycomb itself is Hart's, 1996) | 2026-10-09 |

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
- Literature check (2026-10-09, using the reading library): the **family** is known. Any rhombic
  dodecahedron spanned by four directions tiles space (Fedorov's parallelohedra), and Lalvani's
  US 5,623,790 (1997) draws a "4-zonohedron … a rhombic dodecahedron" of three kinds of
  parallelogram and a periodic space-filling of "tilted rhombic dodecahedra". Lalvani's
  US 4,723,382 (1988) builds space-fillers whose edges all run along the 15 icosahedral 2-fold axes,
  DICTO's directions, from pieces that also make DICTO's faces (two equilateral triangles make a 60°
  rhombus; two 36°–108°–36° triangles a 72° one) and from rhombohedra and parallelepipeds like
  DICTO's blocks; it names sheared truncated octahedra and cuboctahedra, but no rhombic
  dodecahedron. Grünbaum (2010) classifies only the rhombic monohedra (all faces congruent:
  Kepler's, Bilinski's, …), so a two-faced equilateral one is outside it. This **member**, equal
  edges, 60° and 72° rhombi, volume exactly φ², splitting into two all-rhombus blocks and two
  flattened rhombohedra, was **not found**: a new member of a known family.

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
- Literature check (2026-10-09): elongated dodecahedra spanned by five directions are Fedorov's
  fifth parallelohedron type, and Lalvani (US 5,623,790) treats skewed 5-zonohedra in general;
  equilateral regular-hexagon versions are known (#5, Grünbaum 2010). These two equal-edge members on
  DICTO's directions (36°, 60° and 72° relations; volumes φ² + 2 and φ³ + ½) were **not found**:
  new members of a known family, like #1.

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

## 10. EKP windows (DICTO, 2026-10-08)

*Its study 10a is a construction on these windows, recorded with its exact results but not claimed as a separate finding.*

Take the EKP cell's dodecahedron (cube edge 2) and the stella octangula in each of its six
face-neighbour cells, and carve the twelve tetrahedra out of the dodecahedron.

- What remains of the dodecahedron's surface is exactly **12 rhombi**, one on each edge of the
  cube, each lying in one of the dodecahedron's own face planes (the face whose diagonal is that
  cube edge). Each rhombus has edge 2/φ (the dodecahedron's edge), long diagonal 2 (the cube
  edge), short diagonal 2·0.7265 and angles **72° and 108°: Penrose's thick rhombus**. Two of its
  sides are dodecahedron edges; the other two are where the neighbour's two tetrahedra cut the face.
- The rhombic dodecahedron's 12 rhombi sit on the same cube edges, but there the cube edge is the
  short diagonal (angles 70.53°/109.47°), and they are turned about 13° about that edge: the windows
  are its icosahedral near-twin. (Corrected 2026-10-08: an earlier wording said the cube edge was the
  windows' short diagonal; it is their long one.) The Studies world morphs one into the other.
- The cut-away is walled by **48 triangles** in the stellas' face planes, 24 with sides
  √2/φ, 2/φ, √2 (cube corner, roof vertex, cube-face centre) and 24 with sides √2/φ², 2/φ, √2
  (cube-face centre, a rhombus's inner corner, cube corner); the 8 over each cube face meet at its
  centre, an octahedron vertex. The cube itself is untouched.
- The carved solid closes and encloses exactly **12**: the cube's 8 plus 2/3 from each of the six
  roofs. A roof is 2φ/3, so each roof keeps exactly **1/φ** of itself.
- Any convex solid that keeps all 12 rhombi in their planes is the dodecahedron itself (the rhombi's
  corners are its vertices and points on its faces), so these windows only appear by carving.
- Why it matters: an aperiodic tile (the thick rhombus) appearing, at its icosahedral orientation,
  on a periodic cubic lattice — a bridge between the two.
- Verified: `src/krp-core/scripts/verify-roof-fold.mjs` §13(a), every push. Shown in the Studies world (Wizard → 3D+ → Studies), Windows.
- Status: **not found** at web level (2026-10-08); not yet searched in the faceting/compound literature.
- Checked against Lalvani, US 4,723,382 (1988), on 2026-10-09: his building system has every edge on
  the 15 icosahedral 2-fold axes, and his ten pieces include the 72°/108° rhombus, so the window
  rhombus itself is one of his pieces. The windows solid is not: its 48 walls lie in the stella
  octangulas' planes, and all their edges run along the cube's face diagonals, 22.24° off every
  icosahedral 2-fold axis (checked from the solid's 165 edges). The patent has no stella octangula,
  no carving and no cube–dodecahedron construction. Not prior art for #10.

### 10a. Study: the windows made convex (DICTO, 2026-10-08)

*Recorded as #12 in Zenodo version v2026.10.08-convex; regrouped under #10 as a study the same day (DICTO's decision).*

Any convex solid that keeps the 12 window rhombi (#10) where they are is the dodecahedron itself.
DICTO's question: expand from the centre instead. Push each rhombus straight out along its own
normal by t, keeping its size, angles and orientation, and take the convex hull.

- For every t > 0 the hull has 80 faces: the 12 rhombi, 8 equilateral triangles where the cube
  corners open, and 60 joining triangles (each gap between rhombi is twisted, so it splits in two).
- At exactly **t = √(7 − 4φ) ≈ 0.7265** (half the rhombi's short diagonal), and nowhere else on
  0 < t ≤ 3 (scanned), the six gaps over the cube faces flatten. Each becomes a **golden rhombus**
  (angles 63.43° and 116.57°, diagonals in ratio exactly φ), square on a cube face. The solid has
  **74 faces**:
  - 12 Penrose thick rhombi (72°/108°, edge 2/φ), the windows, unchanged;
  - 6 golden rhombi (edge 2√(7 − 4φ), the windows' short diagonal);
  - 8 equilateral triangles (edge 2/φ²) at the cube corners;
  - 24 isosceles triangles (2/φ, 2t, 2t) and 24 triangles (2/φ², 2/φ, 2t).
  Only three edge lengths occur: 2/φ², 2/φ and 2√(7 − 4φ).
- It carries the 2D aperiodic rhombus (Penrose's thick rhombus) and the 3D one (the golden rhombus,
  the face of Ammann's golden rhombohedra and of the rhombic triacontahedron) together, on cubic
  symmetry: a convex bridge between periodic and aperiodic.
- **Buildable:** it unfolds into a flat net of all 74 faces with no two faces overlapping, which
  folds closed (found by the Nets code, 76 taps).
- Verified: `src/krp-core/scripts/verify-roof-fold.mjs` §13(c) (faces, golden ratio, edge lengths, closure, the
  80-face case elsewhere) and `src/krp-core/scripts/verify-nets.mjs` (the net), every push. Shown in the Studies world, Windows made convex, with a push slider that snaps at the golden point.
- Status: a study of #10, not a separate claim (not found at web level, 2026-10-08).

### 10b. Study: windows and stellas fill space (DICTO, 2026-10-08)

DICTO's question: is there a "male counterpart to window", with stars pushing out to fit the faces
the stella octangulas leave? There is, and it is the stella octangula itself.

- Put the windows solid (#10) in every even cell of the cubic lattice (cell parity, x + y + z
  even) and the cell's own stella octangula in every odd cell. Every neighbour of an even cell is
  odd, so each windows solid keeps its whole cube, and its six roofs reach into six odd cubes.
- Each odd cube is then exactly its stella octangula plus the six carved roofs reaching into it,
  with **no gap and no overlap**: the six inward roofs never overlap one another (each roof's
  trapezoid lies in the same plane as the next roof's triangle), and what each roof loses to the
  stella is exactly what the windows carve away.
- Exact volumes, cube edge 2: dodecahedron 14.472136, each roof 2φ/3 = 1.078689, each roof's carved
  part 0.412023, so each roof keeps 2/3 and six of them fill 4 = cube − stella. The windows (12) and
  the stella (4) make 16, two cubes.
- So the windows tile space together with the stella octangula in the rock-salt arrangement: a
  periodic packing whose even pieces carry 12 Penrose thick rhombi at their icosahedral orientation.
- Prior art checked: Lalvani, US 4,723,382 (1988), the closest system found (polygons and polyhedra
  filling space periodically or not), requires every edge to lie along the 15 icosahedral two-fold
  axes. The windows' rhombi meet that (all 48 edges), but 96 of the windows' 144 wall edges and every
  stella edge (the cube-face diagonals) do not; nor does it describe a cube, a stella octangula or
  these windows.
- Verified: `src/krp-core/scripts/verify-roof-fold.mjs` §13(f): the volumes exactly, and a 40³ grid of points in
  an odd cube, every one in exactly one piece (a 60³ grid, 216,000 points, was also checked by hand).
  Shown in the Studies world, Windows and stellas, checkerboard, with an Apart slider.
- Named by DICTO (2026-10-08): the windows solid on its own is the **DICTO Jewel** (DJ; first named the Dragon Jewel, renamed by DICTO on 2026-10-09); the
  checkerboard is the **Stella–Jewel Lattice** (the face-centred cubic lattice with two pieces per
  point), a world of its own in the app. On its own, the DICTO Jewels on the even cells meet face to
  face on all 12 rhombi (each rhombus is coplanar with, and the same as, a neighbour's), leaving
  stella-shaped holes. Five-fold: each window lies in a dodecahedron face, facing a five-fold axis;
  each face has five window positions, one per pentagon diagonal, and the cube picks the one on a
  cube edge. Verified: `src/krp-core/scripts/verify-roof-fold.mjs` §13(g).
- Status: a study of #10, not a separate claim (not found at web level, 2026-10-08).

## 11. The stretched dodecahedron (DICTO, 2026-10-08)

The hull of the dodecahedron and a copy moved s along a cube-face axis (one of its 2-fold axes,
the same axis along which the rhombic dodecahedron stretches into the elongated dodecahedron).

- For **every** s > 0: 8 regular pentagons (4 at each end), 4 hexagons with angles 108°, 108°,
  108°, 108°, 144°, 144°, and 2 rectangles: 14 faces. At s = 2/φ, one edge, the rectangles are
  **squares**; at s = 2, the EKP lattice spacing, it is the hull of two face-neighbour dodecahedra.
- Volume = the dodecahedron's + s × 7.236068 (its shadow across the axis), as for any segment
  sweep.
- The dodecahedral counterpart of the elongated (rhombic) dodecahedron: 4 pentagons at each end where
  that has 4 rhombi, and a hexagon belt, plus the two rectangles that the dodecahedron's own roof
  ridges force. A pentagon-capped, hexagon-belted solid without them needs another construction.
- Verified: `src/krp-core/scripts/verify-roof-fold.mjs` §13(b), every push. Shown in the Studies world,
  Stretched dodecahedron, with a stretch slider.
- Status: **not found** at web level (2026-10-08). Simple enough that it probably appears somewhere
  (crystal habits, Minkowski sums); a targeted search is still needed before claiming priority.

## 12. Star Chain Reaction (DICTO, 2026-10-08)

*Named by DICTO, "like solar radiation": each star sets off the next, smaller one inside it.*

Regular dodecahedra on the even cells of the EKP cubic lattice (cube edge 2) are the dodecahedron's
densest lattice packing (density (5 + √5)/8; Betke–Henk 2000). Each odd cell's hole is a **Dogstar**
(DICTO's name): the solid George W. Hart listed in 1996 as stellation 8 of the dodecahedron, noting
that it fills space alternated with regular dodecahedra (credit: Hart; also Polyhedra-World, and Hans Walser, whose “semi-regular dodecahedron” is this solid as a cube with its six hip roofs cut away, checkerboarded with regular dodecahedra). New
here is where it sits and what nests in it:

- The Dogstar is a partial stellation of a regular dodecahedron 1/φ³ the size of the lattice's,
  same centre and orientation: its core, all 12 first-layer pyramids, 24 of the 30 second-layer
  wedges (all but the 6 on the cube axes) and the 8 great-stellated spikes aimed at the cube
  corners, whose tips are the cube corners. Its edges are only 2/φ⁴, 2/φ³, 2/φ² and 2/φ, and its
  volume is 16 − (the dodecahedron) = 1.527864, exactly **φ/2 at dodecahedron edge 1**.
- A dodecahedron with the 6 Dogstars on its faces is a **Sunstar** (DICTO's name: the sun with its
  sun dogs).
- **The chain.** The EKP cell's great star (Kepler's great stellated dodecahedron, the icosahedron
  with 20 spikes to the dodecahedron's vertices) is *exactly* the great stellated dodecahedron of
  the Dogstar's 1/φ³ core: all 60 of its faces lie on the core's 12 face planes. So the Dogstar is
  that great star trimmed to the cube (12 spikes and 6 wedges removed).
- Inside the great star sits a **whole Sunstar 1/φ³ the size** (the core with its own 6 Dogstars
  at 1/φ³), with no room to grow: the largest scale at which it fits is exactly 1/φ³. Its
  dodecahedron is the core, which holds the next great star (1/φ³), which holds the next Sunstar
  (1/φ⁶), and so on: dodecahedron ⊃ great star ⊃ Sunstar(1/φ³) ⊃ great star(1/φ³) ⊃ Sunstar(1/φ⁶) ⊃
  …, each step touching. The ratio φ³ is the inflation factor of icosahedral quasicrystals, so the
  chain joins the periodic packing to an aperiodic, self-similar one.
- Related, on the same cell (verified, not separate claims): the Dogstars alone form a
  corner-sharing network in the spirit of the Kagome and pyrochlore lattices, but **four** Dogstars
  share each cube corner (pyrochlore's tetrahedra share theirs in pairs); this is the known tiling with
  the dodecahedra hidden, framed by DICTO as a corner-sharing lattice. A Dogstar also fits wholly
  inside its own cell's dodecahedron, touching (Dogstar ⊂ stella octangula ⊂ cube ⊂ dodecahedron),
  which the tiling does not give: so Dogstars can fill every cell, **eight** sharing each cube corner
  (this nesting is also the step into study 12a). And a Sunstar fits a cube exactly 1/3 its size (it
  spans 3 lattice cells).
- Verified: `src/krp-core/scripts/verify-roof-fold.mjs` §13(h) (the Dogstar: closure, golden edges, volume,
  fill with the dodecahedra), §13(i) (the lattice's point tests), §13(j) (Dogstars in every cell)
  and §13(k) (the chain: the great star on the core's planes, and the zero-slack fit, largest
  scale 1.000000000 of the 1/φ³ Sunstar), every push. Shown in the Sunstar Lattice world (in
  Kaleidohedra and Rhombiverse), view Star Chain Reaction; the pieces are in Polyhedraverse's
  Space-Filling Pairs (a dodecahedron seamed where Dogstars meet it, and the Dogstar).
- Status: the nesting chain was **not found** in a web-level search on 2026-10-08 (Hart's
  stellation pages, Polyhedra-World, Torquato–Jiao and Betke–Henk on the packing, Koca et al. on
  icosahedral inflation). The Dogstar solid and its tiling with dodecahedra are known (Hart 1996; Walser),
  and credited as such. Not proof of novelty; a specialist search (stellation and quasicrystal
  cluster literature) is still worth doing before claiming priority.

### 12a. Study: the Jewel chain (DICTO, 2026-10-08; first called the Dragon chain, renamed by DICTO on 2026-10-09)

DICTO's question: is "another cell network buried in the Dragon's claw"? There is, through the
same bridge. Inside the DICTO Jewel (#10, the windows solid), every step touching, with no room to
grow (the largest scale at which each fits inside the one before is exactly 1):

- DICTO Jewel ⊃ cube (its cube is untouched by the carving) ⊃ stella octangula (on the cube's
  corners) ⊃ Dogstar (its 8 tips are the cube corners) ⊃ the Dogstar's core, a dodecahedron 1/φ³ the
  cell's (it reaches the Dogstar's surface where the 6 axial wedges are missing) ⊃ DICTO Jewel
  1/φ³ the size (its rhombi lie on the core's faces) ⊃ … , ratio φ³ per round.
- So the EKP cell's own chain (… ⊂ stella ⊂ cube ⊂ dodecahedron) carries on downward through the
  Dogstar into the next cell, 1/φ³ smaller. The Dogstar is the bridge between scales in both this
  chain and #12's.
- Several steps touch only at the shared cube corners, which the cube, the stella and the Dogstar
  all reach; the link that is not obvious is the Dogstar touching its own core.
- Verified: `src/krp-core/scripts/verify-roof-fold.mjs` §13(l), every push. Shown in the Stella–Jewel Lattice
  (Kaleidohedra and Rhombiverse), view Jewel chain.
- Status: a study of #12, not a separate claim (not found at web level, 2026-10-08).

## 13. The 13-dodecahedron cluster made solid (DICTO, 2026-10-09)

*DICTO's cluster: "one dodecahedron at the center of a cluster", built in layers down a 3-fold axis:
a snowflake belt of six, three in the dimples on top, turned over, three more. Its earlier basis is
DICTO's exhibition piece, a 12-dodecahedron cluster of PET bottle caps and their security rings,
shown at a sculpture exhibition.*

A regular dodecahedron with a regular dodecahedron on **each of its 12 faces**. A dodecahedron that
shares a whole face with another is its mirror image across that face (opposite faces are turned
36°, so no shift fits), so the cluster is unique: the first shell of the 120-cell, laid flat. The
12 never overlap; they touch each other only along the centre's 30 edges, where three dodecahedra
leave 360° − 3 × 116.565° = **10.3048°**. The gaps are exactly two kinds of piece (edge 1):

- **Wedge** (30, one on each edge of the centre, congruent): two regular pentagons, the two
  neighbours' faces, hinged on the centre's edge at 10.3048°, closed by two end triangles and two
  outer trapezoids (sides 1, 1/(φ²√5), 1, 1/(φ√5)). Volume exactly **φ³/20**.
- **Needle** (20, one at each corner of the centre, congruent): a tetrahedron whose three long edges
  are the three neighbours' outer edges (length 1) and whose base is an equilateral triangle of
  side 1/(φ²√5). Volume exactly **(45 − 19√5)/600**. Its three sides are the end triangles of the
  three wedges at that corner: three wedges and a needle lock into a three-armed **star**.
- Together, 13 dodecahedra, 30 wedges and 20 needles are one closed solid with no gap inside,
  volume 13(15 + 7√5)/4 + 30φ³/20 + 20(45 − 19√5)/600; outside, 72 pentagons, 60 thin trapezoids
  and 20 small triangles.
- **Separable once built** (DICTO's requirement): each wedge is symmetric across the mirror plane
  through the centre's edge, and each needle 3-fold about the line through its corner, so the
  wedges halve and the needles split in thirds along the same planes. Every outer dodecahedron
  carries 5 half-wedges and 5 needle-thirds as fins and lifts straight out; the centre carries none.
- Beyond the cluster (studied, not claimed): a second shell puts 12 copies of the centre, same
  orientation, at 4 × the inradius along the six 5-fold axes, the projected basis of the 6D cubic
  lattice, so the centres follow the golden-rhombohedron (Ammann–Kramer) tiling with that edge.
  Decorated with dodecahedra at its corners and edge midpoints it fills about 68% at most while
  keeping every contact a whole face (the oblate rhombohedron's short diagonal is where it must
  split); the rest are cage-sized voids, not stars. In the cubic 1/1 approximant (exact golden tiles,
  period 15.155 at dodecahedron edge √5 − 1) the decoration is 32 corner + 96 edge dodecahedra per
  cell, 8 corners dropped on the oblate short diagonals; filled face to face as far as it goes it
  saturates at 162 per cell, 67.35%, and what is left is one connected, thin labyrinth (deepest point
  1.356, just under the inradius 1.376, so no further dodecahedron fits in any orientation). Shared
  out by nearest centre it gives dozens of unit shapes, since the approximant's sites all differ:
  clean finned units need a truly periodic arrangement, not an approximant.
  For comparison, the A15 (Weaire–Phelan, clathrate I) pattern: the largest regular dodecahedron in
  each 12-faced site cell (EKP orientation, the body site turned 90°) fills 85.4% of it, leaving thin
  fins; the six 14-faced cages per cube take 75.6% of space, so regular dodecahedra fill only 20.9%,
  with no face contacts: tidy, periodic, but essentially the known clathrate structure.
  Grown fins: the filled cluster's densest translation-only packing (searched over 54 406 lattices
  from its contact distances, the winner checked independently) is **body-centred cubic**, its 8
  nearest neighbours along its 3-fold axes, density 0.7154. So one block shape, the cluster plus its
  share of the leftover 28.5% as grown fins, fills space by bcc translations; the cluster pokes up to
  0.23 (dodecahedron edge √5 − 1) outside its truncated-octahedron cell at 48 corners, so the units'
  boundaries zigzag around the truncated octahedron's faces and interlock. Exact, but the fins are
  chunky, not slim stars.
- Build plan: [BUILD-13-BLOCK.md](BUILD-13-BLOCK.md) (pieces with dimensions, the separable units,
  DICTO's assembly order, and the tentative bcc stacking with grown fins).
- Verified: `src/krp-core/scripts/verify-dodeca-cluster.mjs` (krp-core v0.7.2), every push:
  congruence, exact volumes, no overlap among the 63 solids (separating axes), every gap face
  accounted for, and the halving and thirds.
- Status: the 10.3° gap of three dodecahedra round an edge is well known (the 120-cell and
  frustration literature, which closes it by curving space or twisting, e.g. Sadoc and Mosseri;
  Fang, Irwin et al. 2018), and Jenczyk (2024) builds networks of regular dodecahedra joined by
  icosahedron-based binders. The cluster's gaps as two exact solid pieces, and the separable finned
  units, were **not found** in a web-level search on 2026-10-09. Not proof of novelty.

## 14. DICTO-Star (2026-10-09)

*DICTO's own pattern: it is the centre of DICTO's builds, in Polyhedraverse (by 4 October 2026) and
from PET bottle caps and their security rings, made as a 3D analogue of the 4D fold of the
13-dodecahedron cluster (#13: in the 120-cell the 12 outer dodecahedra fold round the centre and
close the gaps; in 3D the J63s close them instead). Having it at the centre of the build is why
DICTO asked for a search: Kaleidohedra's search (testing DICTO's idea that bi- and tri-diminished
icosahedra, J62 and J63, close the gaps between dodecahedra) confirmed DICTO's pattern exactly,
showed it is forced, and checked how far it continues with regular pieces.*

An **icosidodecahedron** with a regular **dodecahedron** on each of its 12 pentagons and a
**tridiminished icosahedron** (Johnson solid J63) on each of its 20 triangles, each J63 by its one
triangle that borders only pentagons. 33 regular-faced pieces, edge 1:

- **Every contact is a whole face and nothing overlaps.** At each of the icosidodecahedron's 60 edges
  142.6226° + 116.5651° + 100.8123° = 360° exactly (icosidodecahedron, dodecahedron, J63), and the
  dodecahedron's face there is exactly a pentagon of the J63: the edge is closed with no gap. Every
  corner of the icosidodecahedron is filled.
- **No filler is needed**, unlike the 13-dodecahedron cluster (#13). The J63s sit like caps in the 20
  three-fold dimples between the dodecahedra.
- Volume exactly **(195 + 89√5)/3** ≈ 131.3367 (icosidodecahedron (45 + 17√5)/6, 12 dodecahedra,
  20 J63 of 5(3 + √5)/12 − (5 + √5)/8 each).
- **Why J63 and not the whole icosahedron:** with whole icosahedra on the triangles (Robert Austin's
  2014 virtual model) each icosahedron's three pentagonal pyramids run into the neighbouring
  dodecahedra; J63 is the icosahedron with exactly those three removed. In curved (hyperbolic) space
  the whole-icosahedron version is a cell of the dodecahedral-icosahedral honeycomb; J63 is what lets
  it exist, exactly, in ordinary space.
- **What it does not do (studied, not claimed):** it does not continue into a space-filling of these
  pieces. Each edge of an icosidodecahedron closes only with a dodecahedron and a J63, which forces
  the star round every icosidodecahedron, and each J63 keeps a cap of four triangles that no regular
  piece closes; the pockets over the caps widen outward, so in packings the gaps join into one
  labyrinth (about 26%). Two stars can share a dodecahedron along a 5-fold axis (centres 4.97980
  apart), which gives columns, but no lattice of them fits.
- **How far DICTO went (DICTO's evidence: Polyhedraverse screenshots, 3–4 October 2026):** DICTO had
  the star and grew it outward before this search, with stellation pieces, which are not
  regular-faced, so the result above (no closure with regular pieces) does not rule these out:
  - 4 October, 20:12: icosidodecahedron + 12 dodecahedra + 20 tridiminished icosahedra (the star,
    no stellation pieces, no gaps), then 72 dodecahedron first stellations (flat: rhombic
    triacontahedron pieces) + 60 square pyramids + 60 cube first stellations (flat: rhombic
    dodecahedron pieces) + 20 tetrahedron first stellations (flat: cube pieces): the
    triangle-covered shell. It looked good, but DICTO knew small gaps and overlaps were hidden
    under an accurate-looking outer build.
  - 4 October, 12:44: icosidodecahedron + 24 dodecahedra + 20 tridiminished icosahedra + 120
    dodecahedron second stellations (small stellated dodecahedron pieces) + 8 tall triangular
    pyramids + 4 tetrahedra, a second stack of dodecahedra outward, likewise closed to the eye with
    hidden overlaps and gaps.
  - 3 October: the related "heart", an augmented tridiminished icosahedron + 3 gyroelongated
    pentagonal pyramids + 52 icosahedron third stellations.
  Its precursor is DICTO's physical build: PET bottle caps and security rings with an
  icosidodecahedron at its centre (DICTO's photos).
  An exact rebuild of the 4 October shell from the same pieces (pentagonal pyramids on the
  dodecahedra's 72 free faces, cube corners on the 20 bottom triangles of the tridiminished
  icosahedra, square pyramids on their other 60 triangles, each with a rhombic-dodecahedron pyramid
  on its square) fits all 245 pieces without overlap, in every orientation of the square pyramids,
  but no two added pieces meet face to face: they leave hidden gaps 0.0067, 0.046, 0.053, 0.066 and
  0.263 of an edge wide (the smallest, on 120 faces, about 0.3 mm at a 40 mm edge, invisible), and
  fill 76.2% of the convex hull. So it confirms what DICTO knew: it looks right, but is not closed
  exactly. (This reading has no overlaps; DICTO's build had some, so its placements differ slightly.)
- Verified: `src/krp-core/scripts/verify-id-star.mjs` (krp-core v0.7.4), every push: no overlap
  among the 33 solids (separating axes), all 60 edges closed, every corner filled, exact volumes, and
  that whole icosahedra overlap.
- Status: **not found** in a web-level and reading-library search on 2026-10-09. Closest: Robert
  Austin's *Icosidodecahedra, Icosahedra, and Dodecahedra* (2014), the same arrangement with whole
  icosahedra, built in Stella 4D as a virtual model in which the pieces overlap; the
  dodecahedral-icosahedral honeycomb of hyperbolic space; J63 as the vertex figure of the snub
  24-cell (Koca et al., in the library); Klitzing's 4D segmentochora (e.g. dodecahedron atop
  icosidodecahedron, K-4.77) use the same pieces as cells but not this cluster. Simple enough that it
  may be known somewhere unindexed; not proof of novelty.
- Extended search (2026-10-09, at DICTO's request), still **not found**:
  - **No convex 4D polytope can contain it:** at every edge of the icosidodecahedron the three
    angles add to exactly 360°, so the star is flat, while a convex 4D polytope's cells need less
    than 360° round every edge to fold. That rules out all of Klitzing's CRF polychora at once.
  - Robert Austin's cluster posts (2013 dodecahedral cluster of icosidodecahedra, 2014, 2015
    greatly augmented icosidodecahedron, 2023 clusters round a dodecahedron): whole icosahedra,
    great stellations or icosidodecahedra on the faces, never tridiminished icosahedra.
  - George Hart's polyhedra clusters; Klitzing's tridiminished-icosahedron page (it occurs in the
    snub 24-cell's vertex figure and related CRF and blends, not in this cluster); a Stewart toroid
    of genus 11 built from 20 tridiminished icosahedra, 30 metabidiminished icosahedra and 60
    pentagonal antiprisms (no icosidodecahedron or dodecahedra).
  - The Elser–Sloane quasicrystal's 3D slice (icosidodecahedron, dodecahedron, icosahedron and
    golden tetrahedron tiles; Fang et al., arXiv 1311.3994; Baake & Gähler 1998, in the library):
    whole icosahedra, no tridiminished ones, so not this configuration; a neighbour worth noting for
    the lattice-to-quasicrystal bridge.
  - Not reached: the post before Austin's 2013 cluster (archive offline that day), the Stella forum,
    printed books (Stewart's *Adventures Among the Toroids*), and non-English sources.
- Archived: Zenodo [10.5281/zenodo.23256623](https://doi.org/10.5281/zenodo.23256623) (v2026.10.09-octet, 2026-10-09).

## 15. DICTO Jewel clusters (DICTO, 2026-10-09)

*DICTO built the tetrahedral cluster in the app, asked for the octahedral one beside it, and saw that
both fill space with stella octangulas (the cube of eight Jewels was left out: so far it exists only
sheared).*

Groups of DICTO Jewels (#10) from the Stella–Jewel Lattice, each touching pair meeting face to face on
a whole rhombus, each group a shape of its own (krp-core `DJ_TETRAHEDRAL_CLUSTER`,
`DJ_OCTAHEDRAL_CLUSTER`):

- **Tetrahedral cluster:** four Jewels at the corners of a regular tetrahedron of cells, 6 shared
  rhombi. Surface 228 faces (192 triangles, 36 rhombi), closed; the four lobes also touch at **one
  point**, the cell corner in the middle where all four Jewels meet. Volume exactly 4 Jewels.
- **Octahedral cluster:** the six Jewels round one odd cell, at the corners of an octahedron, 12 shared
  rhombi, and **that cell's stella octangula inside**: the six close round exactly a stella's space
  (sealed but for its 8 spike tips, which reach the outside at a point), and the stella fits them face
  for face, every one of its 48 faces against a Jewel's. **A solid piece** (DICTO: "it's a solid";
  else someone could say they don't perfectly fill space). Surface 288 faces. Volume exactly 6 Jewels
  and a stella.
- **Both fill space with stella octangulas.** Tetrahedral clusters at every cell with all coordinates
  even take every Jewel exactly once; octahedral clusters round the odd cells (1, 0, 0) + the lattice
  of (2, 1, −1), (2, −1, 1), (1, 2, 1) do too (12 cells per cluster: its 6 Jewels, its own stella and
  5 more), one of 12 such lattices, found by exact cover. Stellas fill the cells between, as in the
  Stella–Jewel Lattice.
- **The octet network** (DICTO's idea): sharing Jewels instead of keeping them apart, the clusters are
  the cells of the **octet truss** on the Jewels' lattice: tetrahedral clusters at every cell corner
  (the tetrahedral holes), octahedral ones at every odd cell (the octahedral holes), each Jewel in 8
  of one and 6 of the other as each truss vertex is, neighbours meeting on 3 Jewels (a face). Every
  stella is then inside exactly one octahedral cluster, so the network of solid clusters fills all
  of space with no separate Jewels or stellas. (Not a tiling of separate pieces:
  neighbours share Jewels.) Shown in the Stella–Jewel world's Octet network view.
- **The Kagome network** (DICTO's idea, "Kagome-style reversing tetrahedrons"): up tetrahedral clusters
  on a face-centred cubic set of anchors (all coordinates even, summing to a multiple of 4), down
  clusters forming between them. Every Jewel held is in one up and one down cluster, neighbouring
  clusters share a single Jewel at a corner, as Kagome triangles do, and it holds half the Jewel
  cells; single Jewels take the other half and stellas the odd cells, so it fills space too. The
  pyrochlore lattice itself is well known (corner-sharing tetrahedra in frustrated magnets and
  pyrochlore minerals, stacked Kagome layers); its cells as solid DICTO Jewel clusters were not found.
- Not a pairing with Dogstars: between clusters the gaps are whole stella octangulas, and a Dogstar
  (0.8090 at this size) fills only 38% of one (2.1180), leaving the spike tips open.
- In the apps: Stella–Jewel views that place a whole cluster per tap, and DICTO's pieces in
  Polyhedraverse's list. Their nets wait for an unfolding of 228 and 288 faces that does not overlap
  itself (searching).
- Verified: `src/krp-core/scripts/verify-dicto-jewel-cluster.mjs` (krp-core v0.9.1), every push, 26
  checks: the shared rhombi, no overlap (point tests), closed and consistently wound surfaces, the
  pinch point, the stella inside the octahedral cluster (fitting face for face, reaching the outside
  only at its 8 spike tips), the volumes, and both space-fillings (every Jewel cell in a box of 3,429 in
  exactly one cluster), the octet network (8 and 6 clusters per Jewel, faces of 3, every stella
  inside one octahedral cluster), and the Kagome network (one up and one down cluster per Jewel held,
  single shared corners, half the Jewel cells).
- Status: **not found**, a candidate, resting on #10: the clusters are made only of the DICTO Jewel,
  which itself was not found.
- Archived: Zenodo [10.5281/zenodo.23256623](https://doi.org/10.5281/zenodo.23256623) (v2026.10.09-octet, 2026-10-09). The Kagome network: [10.5281/zenodo.23257393](https://doi.org/10.5281/zenodo.23257393) (v2026.10.09-kagome).

## 16. Sunstar clusters (DICTO, 2026-10-09)

*DICTO asked whether the octet network of #15 held for the Sunstars and Dogstars. It does: the
Sunstar Lattice has the same cells, dodecahedra on the even ones and Dogstars on the odd.*

- **Tetrahedral cluster:** four regular dodecahedra round a cell corner, neighbours meeting flat on
  parts of faces (the seamed Sunstar dodecahedra make the contacts whole matching cells); in the
  middle, where the Jewels touched at a point, four Dogstar tips meet. Volume 4 dodecahedra.
- **Octahedral cluster:** the six dodecahedra round an odd cell **and its Dogstar inside**: the six
  close round exactly the Dogstar's space (every point just outside it lies in one of the six, none
  in the 8 corner dodecahedra; its 8 tips reach the cell corners), and the Dogstar fits them face for
  face. A solid piece. Volume 6 dodecahedra and a Dogstar. **A Sunstar is a dodecahedron with its 6
  Dogstars; this is a Dogstar with its 6 dodecahedra**, the Sunstar turned inside out.
- **Both fill space with Dogstars**, on the same packings as #15 (tetrahedral at all-even anchors,
  octahedral on the lattice of 12 cells per cluster), and **shared they form the octet network**,
  every Dogstar inside one octahedral cluster.
- **The Kagome network** holds for them too, on the same cells: up and down clusters of dodecahedra
  sharing single dodecahedra at their corners, single dodecahedra and Dogstars filling the rest.
- In the apps: the Sunstar world's Tetrahedral clusters, Octahedral clusters and Octet network
  views, and both shapes in Polyhedraverse's DICTO's pieces.
- Verified: `src/krp-core/scripts/verify-sunstar-cluster.mjs` (krp-core v0.9.0), every push, 12 checks:
  no overlap, closed and consistently wound surfaces, volumes 4 dodecahedra and 6 dodecahedra with a
  Dogstar, the Dogstar inside and walled in, and the shared packings.
- Status: **not found** in a web search on 2026-10-09 (with #15's). Known, and credited: the
  honeycomb of dodecahedra and Dogstars (George W. Hart's stellation 8, 1996; Hans Walser), the octet
  truss (Buckminster Fuller; the tetrahedral-octahedral honeycomb), and new tilings by regular
  tetrahedra and octahedra (MRSEC highlight). The clusters, the Dogstar-with-its-dodecahedra and the
  octet network of dodecahedra are DICTO's.
- Archived: Zenodo [10.5281/zenodo.23256623](https://doi.org/10.5281/zenodo.23256623) (v2026.10.09-octet, 2026-10-09). The Kagome network: [10.5281/zenodo.23257393](https://doi.org/10.5281/zenodo.23257393) (v2026.10.09-kagome).

## 17. Kagome hulls (DICTO, 2026-10-09)

*DICTO has worked with hulls for months: how they transform, and how they repeat according to how
they are built. Here DICTO tested whether those hulls (rhombi, cuboctahedra, RD hulls) behave as
expected with the DICTO Jewel and the Sunstar, giving Kagome configurations as the tetrahedral
clusters of #15 and #16 do. They do, and all six keep to one rule.*

- Both lattices have the same rock-salt cells (DICTO Jewels or dodecahedra on the even cells,
  stellas or Dogstars on the odd), so a configuration is a cluster of even cells and a lattice of
  anchors in which **any two clusters share at most one piece and every shared piece is in exactly
  two clusters**, corner to corner as in the Kagome and pyrochlore nets.
- Six hulls work, each in both lattices:
  - **Rhombohedron** (8 pieces at the corners of the FCC primitive cell, its odd cell inside),
    anchors on a BCC pattern: a **perfect Kagome**, every piece in exactly two blocks, none left
    over; a quarter of the odd cells sealed inside, the rest free. 8⅓ Jewels.
  - **Cuboctahedron**, hollow (the 12 round an even cell, a cage with a central hole) or solid
    (13), on the anchors of today's Kagome network (FCC): 12 neighbours each.
  - **Cube** (the 14 of the FCC conventional cell round an odd cell), on BCC: 8 neighbours; many
    single pieces and open pockets, the least Kagome-like.
  - **Rhombic dodecahedron** (19 even pieces and 14 odd, its corners partly stellas), on BCC with
    its second neighbours: 14 neighbours, no single pieces.
  - **Octahedron** (the octahedral cluster of #15), on a simple cubic pattern: the corner-sharing
    octahedra of the perovskite structure.
- **The rule: a hull with n corners sits on a network where each cluster has n neighbours**
  (tetrahedron and diamond, octahedron and simple cubic, cube and rhombohedron and BCC, cuboctahedron
  and FCC, rhombic dodecahedron and BCC with its second neighbours).
- Verified in the design study of 2026-10-09 (exact checks on a 13³ window in both lattices: each
  cluster closed, consistently wound, no overlap, volumes exact, sharing as stated). Not yet in
  krp-core or the apps (DICTO 2026-10-09: keep all six).
- Status: **not found** in a web search on 2026-10-09 for the rhombohedral, cuboctahedral and
  rhombic dodecahedral nets as regroupings of a space filling. Known, and credited: corner-sharing
  octahedra (the ReO₃ and perovskite structures), corner-sharing tetrahedra (the pyrochlore
  lattice), corner-coalesced cube nets in framework chemistry (Molecules 24(7):1221, 2019), and the
  FCC primitive cell as a rhombohedron (standard crystallography). The clusters of DICTO Jewels and
  dodecahedra and the rule across the six are DICTO's.

## 18. The DICTO Hexa (DICTO, 2026-10-09)

*DICTO saw a cube in Kaleidohedra's Studies (Windows, shear as copies) "beautiful and solid, like
carved out of wood", about eight Jewels in volume. Names by DICTO.*

- **The DICTO Hexa:** eight exact DICTO Jewels on a 2 × 2 × 2 block of cells, unsheared, passing
  through each other inside. As one solid it is a cube of edge 4 with the 24 outward roofs on its
  faces (volume **80 = 6⅔ Jewels**; the eight Jewels overlap by 16). Inside, two tetrahedral clusters
  of #15 interpenetrate.
- **No shear makes eight exact Jewels meet face to face as a cube**: the shear is symmetric and no
  symmetric map takes the cube's edges to the Jewels' contact directions (even two of three fail). The
  Hexa exists only as DICTO saw it. Shearing the Jewels themselves (a 3-fold squash) loses the 72°
  windows, and was not kept.
- **The DICTO Hexa-Key:** the gap between Hexas. Hexas mate only window to window (two whole
  windows per neighbour); at the FCC pattern of spacing 4, each has 12 neighbours and 24 whole
  windows shared, and the gap is one solid: **8 stella octangulas and 12 double roofs, volume 48 = 4
  Jewels**. **Hexas and Hexa-Keys fill space like a checkerboard, 5 : 3**, the Stella–Jewel Lattice
  one level up (there Jewel : stella = 3 : 1). The Hexa is 8 cubes with 24 outward roofs; the
  Hexa-Key is 8 stellas with the same 24 roofs turned inward.
- **Parts:** the Hexa splits without overlap into 8 cubes and 24 roofs, or into 4 whole Jewels and
  4 **trimmed Jewels** (3 roofs gone, 3 dents, volume exactly one cube); the Hexa-Key into 8 stellas
  and 24 roofs; every part face-matches its neighbours.
- **Clusters of eight Hexas:** rhombohedral (window to window, 36 whole windows shared, a Hexa-Key
  sealed inside, **57⅓ Jewels**: the Jewel rhombohedron of #17 one level up) and diamond (Hexas sharing
  7 corner Jewels).
- **Hexas Kagome style:** every Jewel in exactly two Hexas is impossible (corner neighbours force
  overlapping blocks); the best is the **diamond network**, each Hexa sharing 4 of its 8 corner Jewels
  with 4 neighbours, and **stella octangulas filling every cell between them exactly**: Hexas and
  stellas fill space with no single Jewels.
- **Nothing turns:** no join in these packings can be turned by its face's symmetry and still fit;
  turns exist only for a piece hanging on one neighbour (a window: 180° and one flip).
- In the apps: the whole family heads Polyhedraverse's DICTO's pieces, with a Parts view (as Jewels,
  or split A or B); the Stella–Jewel world's DICTO Hexa diamond network.
- Verified: `src/krp-core/scripts/verify-hexa.mjs` (krp-core v0.10.0), every push, 16 checks:
  closed and outward surfaces, exact volumes (Hexa 80, Hexa-Key 48, clusters 688 and 556, trimmed
  Jewel 8, roof ⅔), 24 whole Jewel windows and stella-matching walls on the Hexa, and every parts view
  adding up. The network, packing and turning results come from the design study of 2026-10-09.
- Status: **not found** in a web search on 2026-10-09 for a cube built from carved dodecahedra, or
  this block of eight. Known, and credited: the space filling by stella octangulas and octahedra, the
  cube, octahedron and stella inscribed in the rhombic dodecahedron, and the FCC primitive cell as a
  cube squashed along a diagonal. The Hexa, the Hexa-Key, their 5 : 3 filling and the clusters are
  DICTO's.

Since 2026-10-08 the geometry and its checks live in [krp-core](https://github.com/DICTOR-Master/krp-core),
the geometry shared by Kaleidohedra and Rhombiverse, pinned here at `src/krp-core`.

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
Findings #10 and #11 are version v2026.10.08, **DOI [10.5281/zenodo.23220273](https://doi.org/10.5281/zenodo.23220273)**
(published 2026-10-08 Japan time; Zenodo shows 2026-10-07, UTC).
Study 10a (recorded there as #12) is version v2026.10.08-convex, **DOI [10.5281/zenodo.23220833](https://doi.org/10.5281/zenodo.23220833)**.
Study 10b, and 10a under its new label, are version v2026.10.08-checkerboard, **DOI [10.5281/zenodo.23223555](https://doi.org/10.5281/zenodo.23223555)**.
Finding #12, the Star Chain Reaction, and its study 12a are version v2026.10.08-star-chain, **DOI [10.5281/zenodo.23226716](https://doi.org/10.5281/zenodo.23226716)**.
Finding #13, the 13-dodecahedron cluster made solid, is version v2026.10.09-cluster, **DOI [10.5281/zenodo.23247392](https://doi.org/10.5281/zenodo.23247392)** (published 2026-10-09 Japan time; Zenodo shows 2026-10-08, UTC).

## Sources

- [Icosidodecahedra, Icosahedra, and Dodecahedra — R. Austin (RobertLovesPi), 2014](https://web.archive.org/web/2020/https://robertlovespi.net/2014/11/13/icosidodecahedra-icosahedra-and-dodecahedra/) (#14)
- [Dodecahedral-icosahedral honeycomb (hyperbolic) — Wikipedia](https://en.wikipedia.org/wiki/Dodecahedral-icosahedral_honeycomb) (#14)
- [Building systems with non-regular polyhedra based on subdivisions of zonohedra — H. Lalvani, US 5,623,790 (1997)](https://patents.google.com/patent/US5623790A/en) (#1, #7)
- [Building structures based on polygonal members and icosahedral symmetry — H. Lalvani, US 4,723,382 (1988)](https://patents.google.com/patent/US4723382A/en) (#1, #10)
- [Regular Dodecahedron-Based Network Structures — J. Jenczyk, Symmetry 16 (2024) 1509](https://doi.org/10.3390/sym16111509) (#13)
- [Closing gaps in geometrically frustrated symmetric clusters — Fang, Irwin et al., Mathematics 6 (2018) 89](https://doi.org/10.3390/math6060089) (#13)
- [Tetrahedral cluster of dodecahedra (120-cell) — S. Vorthmann, vZome, 2014](https://www.vzome.com/geometry/2014/10/04/dodecTetra-11-09-35.html) (#13)
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
- [Stella octangula — MathWorld](https://mathworld.wolfram.com/StellaOctangula.html) (#10 search)
- [Compound polyhedra — George Hart](https://www.georgehart.com/virtual-polyhedra/compounds-info.html) (#10 search)
- [Regular and semi-regular dodecahedra fill space — Hans Walser](https://walser-h-m.ch/hans/Vortraege/20170627/script.htm) (the Dogstar as the cube minus its hip roofs)
