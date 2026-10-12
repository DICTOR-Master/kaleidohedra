# Network versions (DICTO, 2026-10-12)

The φ³ cycle found here was named **Spheres of Dharma** by DICTO (2026-10-12), discovery #23. Its six-beat cycle is **Ritsudō** (律動), its concentric growth **Nenrin** (年輪), and the
triacontahedron's multiplying seed (see "Which forms multiply?") the **Bodhi seed** (names by DICTO).

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

## Dodecahedron to fullerene cage (the step linking the two pairs)
`scripts/d_in_ti.py`, `logs/d_in_ti.log`. The cage of edge 1/φ wraps the dodecahedron of edge 1, its 20 corners on the cage's 20
hexagon centres. The gap (5.388544, 41.3% of the cage) is filled exactly by
**12 twisted pentagonal frusta** (each between a cage pentagon, edge 1/φ, and the dodecahedron face below, edge 1, turned 36°:
2 pentagons + 10 triangles, height 0.324920, volume 0.399864) and **30 edge wedges**, tetrahedra with five edges 1/φ and one edge 1
(the dodecahedron's edge), i.e. the Mosseri–Sadoc tile t1 at scale 1/φ (volume 0.019672). Total 5.388544.
So a chain of verified steps now runs: ID core → (+20 triangular pyramids) dodecahedron → (+12 frusta, +30 t1) fullerene cage →
(+12 + 20 caps, +60 wedges) rhombic triacontahedron. Whether it continues outward at golden steps is the next question.

## The icosidodecahedral network closes inside the Lotus seed (2026-10-12)
`scripts/relink.py`, `logs/relink.log`. All four shells sit inside the Lotus seed's outer icosahedron I(φ²) (dodecahedron edge 1 =
the Lotus seed's own D(1)), and the last layer, between the triacontahedron (edge 1.089814) and I(φ²), is filled exactly by
**30 edge pieces** (each triacontahedron rhombus joined to the icosahedron edge it faces, volume 0.527864) and **20 face pieces**
(each icosahedron face joined to the three-fold corner below it, volume 0.368922): 23.214379 = the gap, and 40,000 sample points in
the gap are each covered exactly once.

So the complete network, every layer exact (237 pieces per cycle):

| Shell | edge | filled from the one inside by |
|---|---|---|
| small icosahedron (the Lotus seed's centre) | 1/φ | — |
| icosidodecahedron | φ/2 | 12 pentagonal pyramids + 20 twisted triangular frusta |
| dodecahedron | 1 | 20 triangular pyramids |
| fullerene cage | 1/φ | 12 twisted pentagonal frusta + 30 Mosseri–Sadoc t1 wedges |
| rhombic triacontahedron | 1.089814 | 12 pentagonal + 20 hexagonal caps + 60 tetrahedral wedges |
| icosahedron (the Lotus seed's outer) | φ² | 30 edge pieces + 20 face pieces |

**The last missing piece (DICTO: "one more missing piece?")** — `scripts/core_layer.py`, `logs/core_layer.log`: the ID core of
edge φ/2 is exactly the small icosahedron I(1/φ) + 12 pentagonal pyramids (ID pentagon to the corner below, 0.197336) + 20 twisted
triangular frusta (ID triangle, edge φ/2, to the icosahedron face below, edge 1/φ, side edges √3/2; 8 triangular faces; 0.222148):
6.811000 = the gap, sampled exact cover. I(1/φ) is φ³ smaller than I(φ²), so **the network is a complete φ³ cycle of its own,
I(φ²) ⊃ RT ⊃ cage ⊃ D ⊃ ID ⊃ I(1/φ), repeating inward and outward without end, independent of the Lotus seed.**

The icosahedron of edge φ² therefore has two exact inner structures: the Lotus seed (113 pieces) and this five-shell network around
the icosidodecahedral core. Since the Chain of Karma makes every icosahedron a Lotus seed of its own size, either can be chosen in
every icosahedron at every scale. The four combinations are exact fillings, but the Lotus seed's 12 corner icosahedra straddle the dodecahedron (a J2 cap inside, a J11 outside), so they are whole only when both halves are the Lotus seed's: only the pure Lotus seed branches (13 icosahedra per φ² step); the Spheres of Dharma grow concentrically (one centre icosahedron per φ³ step). The shells are the family of the Tsai cluster of real quasicrystals (as solid, exactly filled
shells; the order differs).

## The cube family in the Spheres of Dharma (DICTO: "are there missing forms like octahedra?")
`scripts/periodic_forms.py`, `logs/periodic_forms.log`. The cube family enters the icosahedral shells as compounds of five:
- **5 cubes** on the dodecahedron's 20 corners: all 60 edges lie on piece surfaces (24 along piece edges, 36 across piece faces):
  Euclid's cubes are drawn into the network's seams and cut no piece.
- **5 octahedra** on the icosidodecahedron's 30 corners (the compound of five octahedra): all 60 edges pass through pieces.
- **10 tetrahedra** on the dodecahedron's 20 corners (two in each cube): all 60 edges pass through pieces.
- So only the cube is woven into the network's seams; the octahedra and tetrahedra are present through their corners only.
- Elsewhere: icosahedron + 6 Admiral Caps = octahedron (#21, the periodic frame); Pacioli's icosahedron in the octahedron.

## Strict check of the cycle (`scripts/sod_overlap.py`, `logs/sod_overlap.log`)
All 237 pieces of one cycle: no overlapping pair (separating axes over all face normals and edge-pair cross products), all inside
I(φ²), total volume = I(φ²) to 1e-12. This check found that the triacontahedron's edge had been used rounded (1.089813, from
0.5671010), which left overlaps of 1e-6 and a volume excess of 1.7e-5; the exact edge is ½√(45 − 18√5) = 1.0898138, now used in
gen_twin.py, relink.py and outward.py.

## Octahedral variant, first finding (Pacioli in the core)
`scripts/pacioli_core.py`, `logs/pacioli_core.log`. The five octahedra on the twin core's 30 corners (octahedron edge 1.851230) each
hold Pacioli's golden icosahedron, and it is one and the same icosahedron for all five: edge exactly 1 (= φ × the centre's 1/φ), in the
network's own turn, each of its 12 corners on an edge of every one of the five octahedra, and inside the core. (The compound of five
octahedra around an icosahedron is classical; its place in the network's core is the point.) Skeleton for an octahedral variant:
icosahedron 1/φ ⊂ icosahedron 1 ⊂ five octahedra ⊂ icosidodecahedron φ/2 ⊂ dodecahedron 1 ⊂ … Filled (`scripts/oct_variant.py`, `logs/oct_variant.log`): I(1/φ) → I(1) by 20 triangular frusta (the gap is exactly
5/3); I(1) → ID(φ/2) by 12 pentagonal pyramids + 20 twisted triangular frusta; both sampled exact covers. So the network refines to
icosahedron 1/φ → icosahedron 1 → ID → D → cage → RT → icosahedron φ². I(1) is concentric with the centre, so it is a finer layer,
not a branch: unlike the Lotus seed's 12 corner icosahedra, it starts no new centre.

## A branch into the 3D Penrose tiling (DICTO: "maybe a golden ratio rhombohedron")
The rhombic triacontahedron is 10 prolate + 10 oblate golden rhombohedra (classical); with edge 1, 10 × 0.760845 + 10 × 0.470228 =
12.310734, and prolate / oblate = φ. So the network's triacontahedron shell can be filled either by the rest of the network (cage,
dodecahedron, core, centre icosahedron) or by 20 golden rhombohedra, the tiles of the Ammann–Kowalewski 3D Penrose tiling, which
continue aperiodically through space. A seeding of another kind (into the quasicrystal tiling rather than into more icosahedra), and a
direct link to the periodic ↔ aperiodic aim. To study: how the network's other shells meet that tiling.

## Which forms multiply? (seeding test)
`scripts/seeding.py`, `logs/seeding.log`. Copies X(1) pushed out along the 12, 20 or 30 symmetry axes until they touch X(φᵏ), k = 1..4;
kept when they do not overlap, then the largest centred copy. Exact golden closes (copies fit and the centre is exactly a power of φ):
- icosahedron, 12 copies on the 5-fold axes, outer φ², centre 1/φ: the Lotus seed (the check).
- **rhombic triacontahedron, 12 copies on the 5-fold axes, outer φ², centre 1/φ** (copies 147.729 of 220.907): the same pattern and
  ratios as the Lotus seed, so the same fractal dimension (2.6063). Its gap has not yet been divided into pieces.
- everything else: copies overlap at φ and φ² (dodecahedron, icosidodecahedron, fullerene cage on every axis; icosahedron and
  triacontahedron on the 3- and 2-fold axes), and at φ³, φ⁴ the centre is √5 or 3φ... (not a power of φ), so no golden cycle.
So two forms multiply, the icosahedron and the triacontahedron (the earlier statement "only the icosahedron" is corrected).

## Bodhi seed gap, first survey (`scripts/bodhi_gap.py`, `scripts/bodhi_parts.py`)
Gap 70.272181 (31.8%, as in the Lotus seed) in two connected pockets: inner (around the centre) ~12.3, outer ~57.5. The space
enclosed by the 12 (centre + inner pocket) is 15.26-15.29 on finer grids (15.287, 15.269, 15.265): it does not match 17 prolate +
5 oblate (15.285), so no rhombohedra filling is indicated. Split by nearest symmetry axis, the 5-fold parts are tiny (the copies
sit on those axes) and the gap is carried by 20 three-fold and 30 two-fold parts on each side: inner ~0.287 (convex) and ~0.189,
outer ~1.508 and ~0.886 (nearly convex). The same pattern as the Lotus seed (CLEO/FUJI on the 3-fold axes, AXE on the 2-fold).
Next: the exact pieces.

## DICTO's Bodhi seed build (Polyhedraverse, 2026-10-12)
`data/dicto-bodhi-build-2026-10-12.json`, `scripts/read_polyhedraverse_build.py` (shape vertices from krp-core, app edge 1/φ).
21 prolate, 8 oblate, 12 RT. 11 of the 12 RT centres lie exactly φ from a common middle (φ² at edge 1): the Bodhi seed's positions,
found by hand with face attachments. The 12th sits at distance 1 on the right axis (should be φ) and overlaps its 5 neighbours; 3
oblate and 1 prolate also overlap RTs. 16 prolate lie in the core (2.874 of the 3.607 enclosed, app units).
Rebuilt with triacontahedra only ("Perfect RT", `data/dicto-bodhi-perfect-2026-10-12.json`, `scripts/check_bodhi_build.py`): 12 RT,
all in one orientation, every centre exactly φ from the middle, 30 face-to-face contacts (5 each), no overlaps: the Bodhi seed's
outer twelve, exact, built by DICTO.

## Transitional spheres (DICTO: "the transitional ring/sphere structure between the solids")
`logs/transition_spheres.log` (computed inline with the network_screen forms). Inner (face), mid (edge) and outer (corner) spheres of
each shell, dodecahedron edge 1. Shared: ID inner = D inner 1.113516; ID outer = D mid 1.309017; D outer = TI inner 1.401259; TI mid
= RT inner 1.500000 (the cage's hexagon-hexagon edges lie on the RT faces). So ID -> D -> TI -> RT are linked by touching spheres;
I(1/phi) -> ID and RT -> I(phi^2) share none (the pyramid/frustum and cap layers). Next idea: a ring view, each shared sphere with
the circles the two solids draw on it (DICTO's ring models).

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
