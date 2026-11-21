# Amber-cell sweep (21 Nov 2026)

DICTO's combined method ("fill the ends in 2D, then cut the resin to fit"), first run on the Fullerene Star (DICTO's name for C1) in the
scutoid stand-in study (branch E; the whole cell there is DICTO's Fullerene-Amber Cell), swept over C2, the icosahedral solids that do not
fill space alone, and one mixed core (dodecahedron + icosahedron). Method: DICTO's. Names: Fullerene Star, Fullerene-Amber Cell are DICTO's;
C2, "dodeca-icosa compound" and the solid labels in the scripts are working names.

## Setting

- Solid at every point of a cubic lattice (sc, bcc, fcc), its T_h axes on the cube axes; mould = its Voronoi cell (cube, truncated
  octahedron, rhombic dodecahedron); resin = mould minus solid.
- s0 = smallest lattice scale with the solid inside its Voronoi cell, computed exactly (max over vertices and mould planes). Runs at s0 and 6/5 s0.
- Combined method exactly as in branch E (combi.py): inner pattern = the solid's faces; outer pattern = 3D Voronoi diagram of the face
  centroids cut by the mould; where the two patterns differ, one Y vertex per cluster (on the ray from the centre, halfway between solid and
  mould); walls pinch to it or grow from it.
- Two additions (scripts/amber.py): (1) an edge lying on the mould keeps no wall (zero area; bottom meets top along it);
  (2) "fins": where a face meets only one outer vertex of a cluster, its two walls share the triangle (v, Y, c) with opposite
  orientation; the pair cancels in that piece and its two neighbours meet across it. Both are re-verified by the same checks.
- Checks on every run: each piece a closed oriented 2-manifold; embedded (pairwise triangle tests, float64 with margin, exact Q(sqrt5)
  inside the margin); positive exact volume; every wall triangle used by exactly two pieces with opposite orientation; volumes add to
  mould - solid exactly (gap 0 in Q(sqrt5)); independent winding-number sampling (1848-6000 points, each resin point covered once).
  All coordinates exact in Q(sqrt5); embedding and sampling tests are float with exact fallback as stated.
- Kinds = congruence classes of pieces (T_h orbit members checked congruent). Scutoid = piece with a Y vertex whose neighbours on the solid
  side and on the mould side differ. 157.7612 deg tested on every dihedral of every piece.

## Table (centroid seeds; contact = solid vertices / edges / faces lying on the mould)

| solid | mould | s | contact | valid | kinds | scutoids | Y |
|---|---|---|---|---|---|---|---|
| C1 Fullerene Star | sc | s0 = (5+3√5)/2 | 12/0/0 | yes | 5 | 80/80 | 24 |
| C1 Fullerene Star | sc | 6/5 s0 | 0 | yes | 5 | 80/80 | 30 |
| C1 Fullerene Star | bcc | s0 = (10+4√5)/3 | 12/0/0 | yes | 5 | 36/80 | 6 |
| C1 Fullerene Star | bcc | 6/5 s0 (Fullerene-Amber Cell) | 0 | yes | 5 | 80/80 | 30 |
| C1 Fullerene Star | fcc | s0 = 5+2√5 | 12/0/0 | yes | 5 | 80/80 | 30 |
| C1 Fullerene Star | fcc | 6/5 s0 | 0 | yes | 5 | 80/80 | 30 |
| C2 | sc | s0 = (7+3√5)/2 | 12/0/0 | yes | 4 | 72/72 | 30 |
| C2 | sc | 6/5 s0 | 0 | yes | 4 | 72/72 | 30 |
| C2 | bcc | s0 = 4+2√5 | 8/0/0 | yes | 4 | 72/72 | 30 |
| C2 | bcc | 6/5 s0 | 0 | yes | 4 | 72/72 | 30 |
| C2 | fcc | s0 = 5+2√5 | 12/0/0 | yes | 4 | 72/72 | 30 |
| C2 | fcc | 6/5 s0 | 0 | yes | 4 | 72/72 | 30 |
| dodecahedron | sc | s0 = (3+√5)/2 | 12/6/0 | yes | 1 | 0/12 | 0 |
| dodecahedron | sc, bcc, fcc | s0 (bcc 1+√5, fcc (5+√5)/2) and 6/5 s0 | | yes (all 6) | 1 | 0/12 | 0 |
| icosahedron | sc | s0 = φ | 12/6/0 | yes | 2 | 0/20 | 0 |
| icosahedron | bcc | s0 = 1.745356 | 12/24/8 | no: 8 faces lie on the mould (zero resin over them; zero-volume pieces) | | | |
| icosahedron | sc 6/5, bcc 6/5, fcc s0, fcc 6/5 | | | yes | 2 | 0/20 | 0 |
| icosidodecahedron | sc | s0 = 1+√5 | 6/0/0 | no: Y vertex at a contact cluster falls on the solid | | | |
| icosidodecahedron | sc | 6/5 s0 | 0 | yes | 3 | 20/32 | 30 |
| icosidodecahedron | bcc | s0 | 24/24/8 | no: as sc s0 | | | |
| icosidodecahedron | bcc | 6/5 s0 | 0 | yes | 3 | 20/32 | 30 |
| icosidodecahedron | fcc | s0 = 2+√5 | 24/12/0 | no: self-intersecting pieces | | | |
| icosidodecahedron | fcc | 6/5 s0 | 0 | yes | 3 | 12/32 | 30 |
| truncated icosahedron (alone) | sc / bcc / fcc | s0 | 12/6/0, 48/48/8, 24/12/0 | no: collinear wall (sc, bcc), self-intersecting (fcc) | | | |
| truncated icosahedron (alone) | sc / bcc / fcc | 6/5 s0 | 0 | yes | 3 | 0/32 | 0 |
| rhombic triacontahedron | sc | s0 = 1+√5 (inradius 1) | 24/24/6 | no: 6 rhombi lie on the mould | | | |
| rhombic triacontahedron | sc 6/5, bcc s0 (= 4), bcc 6/5, fcc s0, fcc 6/5 | | | yes | 2 | 0/30 | 0 |
| truncated dodecahedron (alone) | sc / bcc / fcc | s0 | 12/6/0, 24/24/8, 24/12/0 | no: Y on the solid (sc), self-intersecting (bcc, fcc) | | | |
| truncated dodecahedron (alone) | sc / bcc / fcc | 6/5 s0 | 0 | yes | 3 | 32/32 | 30 |
| dodeca-icosa compound (mixed) | sc | s0, 6/5 s0 | 30/24/0, 0 | no: Y on the solid (s0), self-intersecting (6/5) | | | |
| dodeca-icosa compound (mixed) | bcc | s0 = 4 | 8/0/0 | no: self-intersecting pieces | | | |
| dodeca-icosa compound (mixed) | bcc | 6/5 s0 | 0 | yes | 6 | 60/120 | 30 |
| dodeca-icosa compound (mixed) | fcc | s0 = 3+√5 | 12/0/0 | no: self-intersecting pieces | | | |
| dodeca-icosa compound (mixed) | fcc | 6/5 s0 | 0 | yes | 6 | 60/120 | 30 |

Exact s0 for every case: logs/summary.txt (last lines). Edge 1 for all solids except the rhombic triacontahedron (polar of the
icosidodecahedron, inradius 1). Every valid run: exact volume gap 0, sampling 0 miscounted, 157.7612 absent; every valid run is a
tiling, so every edge ring closes. logs/summary.txt ends FINAL ok.

## What the sweep shows

- C2 behaves like the Fullerene Star: valid in all six moulds, every piece a true scutoid (72/72), 4 kinds (the four T_h face orbits:
  12 decagons, 24 + 24 + 12 triangles), 30 Y vertices. As for C1 the swaps sit at the big-face edges: the 30 decagon-decagon edges pinch
  (inner-only pairs) and the triangle pairs across them meet on the mould (60 outer-only pairs). The decagon pieces keep only their 5
  triangle neighbours on the mould side.
- Scutoids need the outer pattern to differ from the inner one. With centroid seeds this happens only where two large faces meet edge to
  edge (C1 hexagon-hexagon, C2 decagon-decagon, truncated dodecahedron decagon-decagon) or at 4-valent vertices (icosidodecahedron,
  compound valleys). Solids whose face pattern is already a Voronoi-like pattern from the centroids (dodecahedron, icosahedron,
  rhombic triacontahedron, truncated icosahedron alone) give valid divisions with no Y vertex and no scutoid: each piece is a frustum.
- Truncated dodecahedron alone: 32/32 scutoids at 6/5 s0 in all three moulds, 3 kinds (12 decagons, 12 + 8 triangles), 30 Y vertices.
- Icosidodecahedron: each 4-valent vertex splits into two Y-meetings on the mould side ((1 inner, 2 outer) clusters); valid at 6/5 s0
  with fins cancelled; 20/32 scutoids (sc, bcc: all 20 triangles) or 12/32 (fcc: only the 12-orbit triangles); pentagon pieces are not
  scutoids.
- Mixed core (DICTO's addition): the dual compound of a dodecahedron and an icosahedron with edges crossing at their common midpoints;
  core = their union (non-convex, star-shaped), surface 120 triangles (60 from the icosahedron's five-sided tips, 60 from the
  dodecahedron's three-sided tips), 62 vertices (12 + 20 tips, 30 crossing points). Option (a) of the request was built; (b) was not
  needed. Valid at bcc and fcc 6/5 s0: 6 kinds, 60/120 scutoids = exactly the 60 dodecahedron-tip pieces (each gains two neighbours on
  the mould across the crossing point), the icosahedron-tip pieces keep their neighbours; 30 Y vertices, one over each crossing point.
- Failures are failures of the one-Y-per-cluster cut rule, not proofs that no combined-method division exists: at s0 they come with
  contact along edges or faces (icosahedron bcc, rhombic triacontahedron sc: whole faces on the mould, zero resin over them, so those
  faces cannot carry pieces), or with Y vertices that land on or behind the solid near a contact point.

## Skipped

- DICTO's CLEO, AXE, FUJI: not run. They are single low-symmetry pieces (AXE and CLEO are the Mosseri-Sadoc tiles t6 and t4 scaled
  by 1/τ; FUJI is a gap piece of the Icosa-13), none has T_h symmetry, so there is no orientation with T_h axes on the cube axes and the
  sweep's kind count (T_h orbits) does not apply. They need their own setting (orientation choice, stabiliser group) first.

## Files

- scripts/solids.py: exact solids (C1 and C2 from the scutoid stand-in study, branch D, unchanged; hulls checked exactly; compound).
- scripts/amber.py: the generalised combined method (from branch E combi.py). `python amber.py SOLID LATTICE FACTOR cen`;
  needs RESIN_DIR pointing at ../../2026-11-21-scutoid-stand-in/tree/branch-D-resin/scripts (default path).
- scripts/summary.py: re-checks every record, prints the table; logs/summary.txt.
- data/amber_<solid>_<lattice>_<factor>_cen.json: per run (pieces, kinds, neighbours, dihedrals with basis forms, Y vertices).
- logs/run_*.log: per run, including every kind's facets, neighbours and all dihedrals; logs/reg_*.log: regression of C1 against branch E.

LEADS
1. Contact cases at s0: a rule for faces lying on the mould (no piece) and for Y vertices near contact points would decide the
   tightest moulds of the icosahedron (bcc), triacontahedron (sc) and the truncated solids.
2. Compound sc 6/5 s0 fails by self-intersection; other seeds (branch E's cproj) or tau other than 1/2 are untested here.
3. CLEO, AXE, FUJI need their own lattice setting before the sweep can include them.
