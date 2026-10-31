# Building the HexOct tiles from rings (31 October 2026)

DICTO's idea: build one c-tile and one h-tile of HexOct: Two Tiles for Every Stacking (#75) from PET-bottle-cap security
rings. Each ring is pulled into a triangle and tied at six points (two per side, at 1/4 and 3/4); two rings sharing a side
are tied at both facing points (2 zip ties per shared side). Double scale: one ring = a triangle of side 1/2 (ball spacing 1),
so a unit triangle = 4 rings and a regular hexagon of side 1 = 24 rings.

Typeset build sheet: `hexoct-ring-build.pdf` (from `paper.html`; also in ~/Documents/papers-to-read). Not for publication.

## Method

1. Tiles from the #75 engine (`tiles.py` of studies/2026-10-29-endless-stack-cell; on dicto-big-brother ~/kres-tmp/endless):
   c-tile = `tile('ABC', 1, λ)`, h-tile = `tile('AB', 0, λ)`, exact rational corners in lattice units.
2. `scripts/exactfaces.py`: exact outer faces of the union of the pieces. Facets of each convex piece found exactly; on every
   plane the facets of all pieces are cut by all their edge lines (common refinement), each cell gets +1/−1 per facing
   facet, cells with 0 are glued, the rest are merged across shared sides into faces. Replaces the approximate convex-hull
   merge of the first script `tilefaces.py`. Checks at every weight: union volume = sum of piece volumes; every side used by
   exactly two faces. Both pass at all 82 weights.
3. Ring test (exact): a face can be laid with rings iff every side runs in one of three directions 60° apart, has length a
   multiple of 1/2, and all corners lie on one triangular grid of spacing 1/2. Rings = area / area of one ring triangle.
4. `scripts/scan.py`: grid of step 1/96 over the walk −11/24 ≤ λ ≤ 3/8 (81 weights, includes all multiples of 1/24) plus 1/10.
   `scripts/angles.py`: in each open stretch between changes of the face pattern the angles are fixed; at least 6 faces of
   each tile have a corner angle other than 60°/120° in every stretch, so only the change points can work, and those were
   tested exactly.
5. `scripts/build.py` at λ = −1/8: rings of every face, nets (random spanning trees, overlap test with shapely, most compact
   kept; a non-tree side whose two copies coincide in the net is tied flat), counts, 3D drawings (z-buffer, solid faces,
   crisp edges, ring sides drawn thin; c-tile gold, h-tile blue). Ring drawing helpers from studies/2026-10-31-ring-nets.
6. `scripts/tables.py` → `out/tables.md`; `scripts/faces_at.py` → `out/faces--1_8.json` (every face, exact corners).

Run on dicto-big-brother: `TILES_DIR=~/kres-tmp/endless LOGO=<dicto-logo.png> ~/geom/bin/python <script>.py`.

## Scan

| λ | weights | c-tile faces | c: ring faces (best) | h-tile faces | h: ring faces (best) |
|---|---|---|---|---|---|
| −11/24 | 1 | 20: 18 quad, 2 hex | 0/20 | 8: 6 quad, 2 hex | 0/8 |
| −43/96 … −3/8 | 8 | 20: 18 quad, 2 hex | 0/20 | 16: 8 tri, 2 hex, 6 hept | 0/16 |
| −35/96 … −29/96 | 7 | 32: 12 tri, 12 pent, 8 hex | 0/32 | 16: 8 tri, 2 hex, 6 hept | 0/16 |
| −7/24 | 1 | 32: 12 tri, 12 quad, 8 hex | 0/32 | 16: 8 tri, 6 pent, 2 hex | 8/16 |
| −9/32 … −13/96 | 15 | 38: 12 tri, 6 quad, 12 pent, 6 hex, 2 twelve-gons | 6/38 (at −1/4) | 24: 12 tri, 4 quad, 6 hept, 2 twelve-gons | 0/24 |
| **−1/8** | 1 | **14: 6 tri, 6 pent, 2 hex** | **14/14** | **14: 4 tri, 4 quad, 4 pent, 2 hex** | **14/14** |
| −11/96 … 19/96 | 32 | 32: 12 tri, 6 quad, 14 hex | 6/32 (at 1/8) | 30: 8 tri, 6 quad, 4 pent, 12 hex | 0/30 |
| 5/24 | 1 | 32: 12 tri, 6 quad, 14 hex | 0/32 | 30: 8 tri, 10 quad, 4 pent, 8 hex | 0/30 |
| 7/32 … 35/96 | 15 | 32: 12 tri, 6 quad, 14 hex | 0/32 | 30: 8 tri, 4 quad, 10 pent, 8 hex | 0/30 |
| 3/8 | 1 | 12 squares (two cubes) | 0/12 | 12: 6 tri, 6 quad | 0/12 |

The book's weight λ = 1/10: c 32 faces, h 30 faces, none ring-buildable.

## Findings

- **λ = −1/8 is the only weight of the walk where every face of both tiles can be built from rings**, and it has the fewest
  faces inside the walk (14 + 14). No face needs to be left open or forced.
- At λ = −1/8 the pieces are the classical ones: unit tetrahedra and halves of unit octahedra (from −3/8 to −1/8 the
  tetrahedral piece is a regular tetrahedron of edge 4(λ + 3/8)). The octahedron halves are cut by the layer mid-plane,
  parallel to two faces: the cut is a regular hexagon of side 1/2, not a square; these hexagons are outer faces (top and
  bottom of the tile). No square faces.
- The c-tile is never one solid: at every weight tested its pieces form two parts (half-octahedron + tetrahedron each) that
  touch only at the centre of layer L's ball. At −1/8 the two parts are congruent towers (exact: part 2 = −part 1, and part 1
  has a mirror). The h-tile is one solid at every weight.
- Counts at λ = −1/8 (s = side of one ring triangle):
  - c-tile: 2 towers × 30 rings = 60 rings; faces per tower 3 pentagons (7 rings: unit triangle on a trapezoid), 1 hexagon
    (6), 3 small triangles (1); shared sides 54 inside faces + 36 on edges = 90; 180 zip ties. Net: 35 sides tied flat,
    10 when closing, per tower. Tower height 2.45s.
  - h-tile: 48 rings; 4 pentagons (5 rings: unit triangle + one small triangle), 4 trapezoids (3), 2 hexagons (6), 4 small
    triangles (1); shared sides 36 + 36 = 72; 144 zip ties. Net: 56 tied flat, 16 when closing. Height 3.27s.
  - Together 108 rings, 324 zip ties.
- Difference in one sentence: the c-tile is two identical 30-ring towers that touch only at one corner, one upside down
  beside the other, while the h-tile is one 48-ring solid in which a double pyramid of two tetrahedra leans on a
  hexagon-topped slab of two octahedron halves.

## Conclusion and status

Conclusion: build both tiles at λ = −1/8 (classical tetrahedra + octahedron halves); every face is a sheet of ring triangles.
Status: done, exact; build sheet printed (not for publication), awaiting DICTO's read.

## Files

- `paper.html`, `hexoct-ring-build.pdf` — the build sheet.
- `out/scan.txt`, `out/scan.json` — full scan; `out/angles.txt` — angle check per stretch; `out/tables.md` — tables.
- `out/faces--1_8.json` — every face at λ = −1/8, exact; `out/counts.json` — counts; `out/build.log`.
- `scripts/mockup.py` → `out/mockup-sheet.png`, `out/mockup-c.png`, `out/mockup-h.png`: ring mock-up (translucent rounded-triangle bands, zip ties as dark bars, three views per tile; DICTO 10-31).
- `out/net-c-solid1.png` (one tower, make twice), `out/net-h-solid1.png`, `out/tile3d-*.png`.
