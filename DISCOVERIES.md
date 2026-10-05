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

| # | Finding | Credit | Verified | Status | First recorded |
|---|---|---|---|---|---|
| 1 | DICTO skewed rhombic dodecahedron | DICTO (found by building it) | yes | **not found** — candidate | 2026-10-01 (8420a51) |
| 2 | Equal-edge rule for sheared FCC | Kaleidohedra | yes | general idea known; this form not found | 2026-10-01 (8420a51) |
| 3 | Bain disphenoids become regular tetrahedra | — | yes | **known** (Bain, 1924) | 2026-10-01 (8420a51) |
| 4 | Bain rhombic dodecahedron (squares + 60° rhombi) | — | yes | **known** | 2026-10-01 (8420a51) |
| 5 | Regular-hexagon elongated dodecahedron | DICTO (from the "hexagons and rhombi" hunch) | yes | **not found** — candidate | 2026-10-01 (8420a51) |
| 6 | Exactly 9 "most regular" space-fillers | Kaleidohedra two-way search | yes | not yet searched | 2026-10-01 (547aac9) |
| 7 | DICTO skewed ED (two forms) | Kaleidohedra (extending #1) | yes | not yet searched | 2026-10-01 (e97193f) |
| 8 | Roof-fold cell: cube, dodecahedron and folded icosahedron (Pm-3) | DICTO (built a physical cell) | yes | not yet searched; same space group as known icosahedral approximants | 2026-10-06 (6636342) |

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
- Status: **not found.** Known ED forms: the standard one (MathWorld: 80.4°
  rhombi, equilateral hexagons with 131.8° corners), the contracted truncated
  octahedron (60° rhombi, no squares), and cube-volume and concave variants.
  None has regular hexagons with squares.

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
4-direction sub-sets in `geometry-targets.json`; exactly these two contain it.
Neither has a square face, consistent with DICTO's RD having none.

- Verified here (`DICTO_SKEWED_ED_16`, `DICTO_SKEWED_ED_18` in
  `src/geometry-extensions/dicto-fcc.js`): equal edges, the face counts above,
  the exact volumes, and that both keep DICTO's four directions unchanged.
- `TARGETS.md` rows 16 and 18 (elongated dodecahedron section) updated from
  "to find" to built.
- Status: not yet searched (same caveat as #1 — a specialist parallelohedra
  literature search would be needed to claim priority).

## 8. Roof-fold cell

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
- **Not a tiling:** the dodecahedra overlap. Space is covered once (19%) or
  twice (81%), mean (5+√5)/4 ≈ 1.809, the dodecahedron's volume 10 + 2√5 over
  the cell's 8.
- **Symmetry:** exactly the 24 operations of m-3 keep the node set, each
  with a lattice translation only, so the space group is **Pm-3 (No. 200)**,
  primitive cubic — not FCC, not aperiodic, no fivefold axis. With the origin
  at the icosahedron centre the nodes are on Wyckoff **1b** (the corner) and
  **12j** (0, y, z), y = 1/(2φ) ≈ 0.309, z = 1/(2φ²) ≈ 0.191.

Verified here by `scripts/verify-roof-fold.mjs` (geometry in
`src/geometry-extensions/roof-fold.js`). The original notes labelled the
icosahedron site 12i; the stabiliser check shows (0, y, z) with a single
mirror, which is 12j in the International Tables' list for Pm-3.

- Status: not yet searched. α-AlMnSi (Pm-3, the 1/1 cubic approximant of
  the icosahedral phase, 138 atoms per cell built from Mackay icosahedra)
  shares the space group and an icosahedral motif; whether its positions
  match this 13-node set has not been checked.

## Attribution and dates

All findings above credited to DICTO are the work of the artist **DICTO**
(Japan), made while building physical models and playing in Rhombiverse,
Polyhedraverse and Kaleidohedra; "Kaleidohedra" credits mean found by this
project's own search, under DICTO's direction. "First recorded" is the date and
commit that first put the finding in this repository; the git history is the
timestamped record. A physical model may predate it (#1 was built in Zometool
before it was written up; #8's physical cell was built before 2026-10-06).

Please cite as: *DICTO, Kaleidohedra discoveries, #N (first recorded
YYYY-MM-DD), github.com/DICTOR-Master/kaleidohedra.*

The repository is public, so its commit history is a public timestamped record.
An archived, citable snapshot (e.g. a Zenodo DOI, as for RHOMBITURE) would make it permanent.

## Sources

- [Elongated dodecahedron — Wikipedia](https://en.wikipedia.org/wiki/Elongated_dodecahedron)
- [Elongated Dodecahedron — MathWorld](https://mathworld.wolfram.com/ElongatedDodecahedron.html)
- [Elongated rhombic dodecahedron — Polytope Wiki](https://polytope.miraheze.org/wiki/Elongated_rhombic_dodecahedron)
- [Rhombic dodecahedron — Wikipedia](https://en.wikipedia.org/wiki/Rhombic_dodecahedron)
- [Bilinski dodecahedron — Wikipedia](https://en.wikipedia.org/wiki/Bilinski_dodecahedron)
- [Zonohedron — Wikipedia](https://en.wikipedia.org/wiki/Zonohedron)
- [Zonohedrification — George Hart](https://www.georgehart.com/zonohedra/zonohedrification.html)
