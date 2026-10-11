# Network versions (DICTO, 2026-10-12)

DICTO: "at least 3 further versions of Network … any and all possibilities … the real one will stand up, or the false may
eliminate themselves or reveal further missing pieces"; the icosidodecahedron (ID) as the hybrid "twin" of the two-form version;
fullerene cages as transition figures; the three golden rectangles; the great icosahedron.

All forms are built from one icosahedron so that they share its turn (`scripts/network_screen.py`).

## Verified
- **The ID plays the stella octangula's role** (`scripts/dual_compound.py`, `logs/dual_compound.log`). With the icosahedron and
  dodecahedron in dual position (equal midradius), their 30 edge pairs cross at the same 30 points, which are the corners of an
  icosidodecahedron, and the hull of the two is the rhombic triacontahedron (30 faces). As the two tetrahedra of the stella octangula
  cross at an octahedron's corners inside a cube: tetrahedron + tetrahedron → octahedron, cube; icosahedron + dodecahedron → ID, RT.
- **Pacioli's rectangles.** Icosahedron: 12 corners = three golden rectangles (ratio φ). Dodecahedron: cube (8) + 12 corners on
  three rectangles of ratio φ². The great icosahedron has the icosahedron's 12 corners, so the same rectangles.
- **The 600-cell's shells** seen down a vertex run point, I, D, I, **ID (the equator)**, I, D, I, point (study 2026-10-11).
- **Every form has a Lotus seed** (`logs/network_screen.log`): for each of I, D, ID, RT and TI, the form at edge φ² holds copies
  of itself at edge 1 at all its corners, touching their neighbours, and leaves room for a centred copy of exactly edge 1/φ.

  | Form | corner copies | centred form that fits exactly |
  |---|---|---|
  | icosahedron | 12, touching | icosahedron 1/φ (the Lotus seed) |
  | dodecahedron | 20, touching | dodecahedron 1/φ; also a truncated icosahedron of edge φ⁻² |
  | icosidodecahedron | 30, touching | icosidodecahedron 1/φ |
  | rhombic triacontahedron | 32, touching | triacontahedron 1/φ |
  | truncated icosahedron | 60, touching | truncated icosahedron 1/φ |

  At edge φ³ the corner copies of ID, RT and TI still touch, and the inner fits are multiples of √5 (√5, 2√5, 3√5).
- **Prior art, as point shells:** the Tsai cluster of real quasicrystals has concentric dodecahedron, icosahedron and
  icosidodecahedron shells in a triacontahedral envelope (Takakura et al. 2007); nested icosahedral point arrays model viruses
  (Keef and Twarock 2009; Twarock et al. 2015). See the Chain of Karma paper, section 9.

## The shared core (DICTO's dual arrangement)
DICTO (2026-10-12): the Lotus shell is an icosahedron that separates into pentagonal elements at its 12 corners; look for the dual,
a dodecahedron with triangular structures at its 20 corners. `scripts/dual_caps.py`, `logs/dual_caps.log`:
- Icosahedron (edge 1) = icosidodecahedron (edge 1/2) + 12 pentagonal pyramids (all edges 1/2). Volumes 1.729441 + 0.452254 =
  2.181695.
- Dodecahedron (edge 1) = icosidodecahedron (edge φ/2) + 20 triangular pyramids (base φ/2, side edges 1/2). Volumes 7.326029 +
  0.337090 = 7.663119.
- So an icosahedron of edge φ and a dodecahedron of edge 1 share one icosidodecahedral core (edge φ/2), and their dual compound is
  exactly that core + 12 pentagonal pyramids + 20 triangular pyramids. The ID is the body both forms share; only their corner pieces
  differ. In DICTO's ring models these corner pieces are the vertex gaps (pentagonal or triangular, by the reading).

## The other pair: rhombic triacontahedron and fullerene cage (DICTO: "the triangles of rhombi mirroring the hexagons")
`scripts/rt_ti.py`, `logs/rt_ti.log`. The cage's 12 pentagons face the triacontahedron's 12 five-fold corners and its 20 hexagons
the 20 three-fold corners (three rhombi). With the cage at edge 0.567101 (triacontahedron edge 1) all 60 cage corners lie on the
triacontahedron's faces, and exactly:
**rhombic triacontahedron = fullerene cage + 12 pentagonal caps + 20 hexagonal caps + 60 tetrahedral wedges**,
volumes 10.083445 + 1.704813 + 60 × 0.008708 = 12.310734. Each cap has its apex at the triacontahedron corner over its cage face;
each wedge lies along a pentagon–hexagon edge of the cage (edges 0.567101 ×3, 0.597322 ×2, 1 ×1); the cage's hexagon–hexagon edges
lie in the triacontahedron's faces. The pattern resonates with the Lotus seed (20 FUJI on hexagonal bases with apex at a three-fold
corner, 60 AXE along edges); that link is not yet shown.

## Touching nestings (midsphere screen, after DICTO's ring models)
`scripts/touch_screen.py`, `logs/touch_screen.log`. DICTO's ring models are canonical (midsphere) polyhedra: rings = faces,
touches = edges, gaps = vertices (the Koebe–Andreev–Thurston circle packing gives one shape per face pattern). Every pair of forms,
same turn, at the size where the inner one touches the outer one naturally:
- **Golden step: the dodecahedron inside the fullerene cage (truncated icosahedron)**, its 20 corners on the cage's 20 hexagon
  centres, cage edge = dodecahedron edge / φ exactly.
- Exact but not golden: ID in the icosahedron (corners at edge midpoints, edge ratio 2); ID in the dodecahedron (2/φ); the
  dodecahedron in the icosahedron, corners on face centres (3/φ); the icosahedron in the dodecahedron, corners on face centres
  (0.854102).
- So plain touching does not give golden steps (except the cage round the dodecahedron): the Chain's golden steps come from filled
  shells, and the gap pieces decide the other versions.

## Icosidodecahedral network, test 1: no clean shell inside the Lotus seed
`scripts/clean_shells.py`, `logs/clean_shells.log` (DICTO: "try both, the geometry will tell"). Scanning the size of a centred ID
and a fullerene cage (TI), same turn, and sampling inside every Lotus piece: no size at which the shell's surface runs only between
pieces, either with all 113 pieces whole or with the corner icosahedra allowed to split (the only "clean" sizes are trivial: inside
the centre icosahedron, or enclosing the whole seed). So an icosidodecahedral network is not a re-reading of the Lotus seed; it needs
its own pieces. Next: build the ID shell directly at the dual compound's midsphere and look for its gap pieces. (The dodecahedron's
scan range in this script was too small to reach D(1); D(1) is known to separate the 63-piece build cleanly, study 2026-10-11.)

## Not yet done
- **The gap pieces of the new Lotus seeds.** Cutting each gap along all extended face planes gives the right volume but far too many
  pieces (1,730 for the icosahedron), and merging them back, even symmetrically, does not recover AXE, FUJI and CLEO; that method is
  set aside. Next: build the gap pieces from the solids' own corners (as AXE, FUJI and CLEO are), with DICTO's eye on candidates.
- Chaining: whether the outer form of one version can be the inner form of the next (I → ID → D …) at golden sizes.
- Comparing shell ratios with measured Tsai-cluster and virus shell radii (future study).
