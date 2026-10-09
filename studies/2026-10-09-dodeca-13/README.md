# The DICTO Dodeca-13: best use, and its hulls (DICTO, 2026-10-09)

**Built:** krp-core v0.12.0 as the **DICTO Dodeca-13** family (names by DICTO): DICTO Dodeca-13 (the
filled cluster), Star, Unit (the finned unit), Wedge, Needle, all attachable, at edge 1, with parts
views pieces / units / stars (wedges cyan, needles purple). The working names below (13-cluster,
finned unit) are the study's own. Renders are JPG copies of the study's PNGs.


DISCOVERIES.md #13. DICTO asked to "look at the 13-dodecahedron cluster to get best use out of it in
the most appropriate way, and then work on building hulls." Design study with Claude (Fable), research
only: nothing committed, no app changes. All geometry is DICTO's cluster from krp-core
(`src/geometry-extensions/dodeca-cluster.js`); every solid here was rebuilt and checked afresh.
Scales: **unit** = dodecahedron edge 1 (krp-core's POLYHEDRA scale, `*-unit.json`); **raw** = cube edge 2,
dodecahedron edge √5 − 1 (the EKP / Sunstar frame, `*-raw.json`, raw = unit ÷ φ/2, same orientation as
`ekp/dodecahedron`, so the cluster's centre sits exactly on a Sunstar dodecahedron).

## 1. Recommendation: best use

**Polyhedraverse pieces (a "DICTO 13-cluster" group in DICTO's pieces), with a Parts view.** The
cluster is a *set of pieces that comes apart*, which is what the Parts view is for; it is not a lattice
and (see §3) it makes no Kagome network, so a world would show little the pieces do not. Proposed set,
all built and checked here:

| Shape | Faces | Exact volume (edge 1) | File |
|---|---|---|---|
| the filled cluster, one solid | 152 (72 pentagons, 60 trapezoids, 20 triangles), V 180, E 330 | 13(15+7√5)/4 + 30φ³/20 + 20(45−19√5)/600 = 106.058472 | `c13-filled` |
| wedge | 2 pentagons, 2 triangles, 2 trapezoids | φ³/20 | `c13-wedge` |
| needle | 4 triangles | (45−19√5)/600 | `c13-needle` |
| star (3 wedges + needle, what sits at each corner of the centre) | 16 (6 pentagons, 6 trapezoids, 4 triangles) | 3φ³/20 + (45−19√5)/600 | `c13-star` |
| half-wedge (a fin) | 6 | φ³/40 | `c13-half-wedge` |
| needle-third (a fin) | 5 | (45−19√5)/1800 | `c13-needle-third` |
| finned unit (outer dodecahedron + 5 half-wedges + 5 needle-thirds) | 37 | (15+7√5)/4 + φ³/8 + (45−19√5)/360 = 8.199613 | `c13-finned-unit` |

Parts views (as the DICTO Hexa has): **pieces** (13 dodecahedra + 30 wedges + 20 needles,
`c13-parts-pieces`), **units** (the bare centre + 12 finned units, `c13-parts-units`, DICTO's separable
build), **stars** (13 dodecahedra + 20 stars, `c13-parts-stars`). The pieces and units views add up to the
filled solid with no overlap (checked). The stars view overlaps: each of the 30 wedges sits in two of
the 20 stars, so it adds up to 13 dodecahedra + 20 stars = 112.412574 (correction 2026-10-09,
krp-core verify-dodeca13). The wedge, needle and star are the ones to catalogue as attachable
pieces; the two fins are halves of them and matter for the build, less as pieces.

Which to catalogue as *attachable* pieces (clicked onto other shapes) is DICTO's call: the filled
cluster's outer faces are 72 regular pentagons of edge 1, so it attaches to any pentagon piece.

**Not recommended:** a Sunstar-style world (it does not sit in any lattice as pieces, §3) or a
"Space-Filling Pair" (there is no partner piece, §3.4). The bcc stacking is best shown, if at all, as one
arrangement ("bcc stack") in a 3D+ study view, since the grown fins are a convex-decomposed shape,
not a clean piece.

### How it relates to the other DICTO shapes
- **DICTO-Star (#14) is this cluster opened up.** Its 12 dodecahedra sit on the same 12 five-fold axes
  at 2.489898 = 2 r_in + 0.262866 from the centre (r_in = φ²/(2√(3−φ)) = 1.113516 the dodecahedron's
  inradius; 0.262866 = the icosidodecahedron's pentagon distance 1.376382 minus r_in), and they are
  **parallel copies of the centre dodecahedron** (12/12 match), not the cluster's mirror-image outers
  (0/12): so going from the 13-cluster to the DICTO-Star, each outer dodecahedron turns 36° about its
  own axis and moves out 0.2629; the 30 wedges and 20 needles become the 20 three-fold dimples, each
  closed by one J63, and the centre becomes the icosidodecahedron. Same 12 axes, same symmetry (Ih),
  two different closures: wedges+needles (flat, face-sharing) or J63s (parallel, no filler).
- **Sunstar / Dogstar:** no direct relation as a packing. The Sunstar Lattice has all dodecahedra
  parallel; the cluster's 12 outers are mirror images of the centre (turned 36°). In the raw frame the
  cluster's centre *is* the Sunstar dodecahedron at the origin, but none of its 12 outers is on a
  Sunstar site. The wedge+needle set is this cluster's analogue of the Dogstar: the exact gap pieces.
- **Icosahedral symmetry:** the cluster's hull of piece centres is a regular icosahedron of edge
  2 r_in · 2 sin 31.72° = 2.341641 (the 12 outers); its 60 outer-shell vertices lie on four shells
  (radii 1.401259, 2.398412, 2.844999, 3.447155, 20/60/60/60 vertices).
- **120-cell:** the cluster is the 120-cell's first shell laid flat (known); the 10.3048° wedges are the
  folding angle that closes it in 4D.

## 2. The cluster's convex hull

The hull of the 12 outer dodecahedra is a **truncated icosahedron in topology** (60 vertices, 90 edges,
32 faces: 12 pentagons + 20 hexagons, all 60 vertices being the outer dodecahedra's far-face corners),
but **not the Archimedean one**: the 12 pentagons are the outer dodecahedra's far faces (regular, edge
1, on the 5-fold axes) and the 20 hexagons (on the 3-fold axes, each spanning three outer dodecahedra)
have edges alternating **1 and √((27+7√5)/10) = 2.065248**. Volume 142.955323; the filled cluster fills
74.19% of it, the bare 13 dodecahedra 69.69%. Files `c13-convex-hull`, renders `c13-convex-hull`,
`c13-hull-over-cluster`.

## 3. Hull networks (as #17 did for the Jewel and Sunstar clusters)

The hull of the cluster's piece centres is the icosahedron, 12 corners; #17's rule would ask for a
12-neighbour network. Checked exactly (every pair of clusters tested piece by piece with separating
axes, 63 × 63):

### 3.1 Corner sharing (two clusters sharing one outer dodecahedron D)
The second cluster's centre must sit on a face of D other than the shared one: 11 ways, three kinds.
- **5 faces adjacent to the shared face:** the new centre is 2.3416 from the old, 151 overlapping piece
  pairs. Impossible.
- **5 second-ring faces:** the new cluster is the old one rotated 126.870° (two mirrors, not a
  crystallographic angle); 20 overlapping pairs. Impossible.
- **1 opposite face:** the new cluster is a **translation by 4 r_in = 4.454065 along the 5-fold axis**,
  clean. This is the only corner-sharing hop.
So corner-sharing networks are built only of 5-fold translations. A cluster has 12 such slots, but
**neighbours on adjacent axes (63.43°, centres 4.6833 apart) always overlap** (30/30 pairs), while those
on 116.57° axes (7.5777 apart) never do. **The most neighbours one cluster can share dodecahedra with
at once is 3**, on three axes at mutual 116.57° (20 such sets, one per 3-fold direction: the edges of
an oblate golden rhombohedron). Render `c13-corner-sharing-3`; the impossible full star
`c13-star12-overlapping`.
- **No lattice:** all 20 lattices generated by three 5-fold translations overlap (their shortest
  vectors 4.6833 or 2.5066, the oblate rhombohedron's short diagonal, which is the "8 corners dropped"
  of #13's Ammann–Kramer decoration); even two directions fail (|n₁ + n₂| = 4.6833). The only periodic
  corner-sharing structure is the **chain** along one 5-fold axis (period 4 r_in, 2 neighbours each);
  anything with 3 neighbours per cluster is a branching, aperiodic network on the 6D (Z⁶-projected)
  vertex set.
- So **#17's rule breaks for the icosahedral hull**: 12 corners, but at most 3 neighbours in flat
  space, and never a lattice. This is the icosahedral frustration itself (the 13-cluster's full
  12-neighbour star exists only in the 120-cell / curved space), and it is where the periodic ↔
  aperiodic bridge sits: the cubocta13 hull of #17 (13 pieces, 12 neighbours, FCC) is the periodic
  twin of this cluster (13 pieces, 12 slots, no lattice).

### 3.2 Face to face (two clusters meeting on a whole pentagon)
Two dodecahedra meeting on a whole face are mirror images, so face-to-face neighbours are the cluster
**mirrored across a free pentagon** of an outer dodecahedron (parallel copies can never meet whole
face to whole face: every face contact turns the next cluster 36°, as BUILD-13-BLOCK.md says).
- **5 second-ring pentagons:** 50 overlapping pairs. Impossible.
- **the pentagon opposite the shared face (⊥ the 5-fold axis):** clean; the mirror-image cluster's
  centre is 6 r_in = 6.681098 away, meeting on exactly **one whole pentagon** plus 5 point contacts.
  Repeating gives the **column**: clusters along a 5-fold axis alternating mirror images (turned 36°),
  spacing 6 r_in, period 12 r_in = 13.362196. Render `c13-column`.
The mirror planes are at dodecahedral angles, so no face-to-face network beyond the column closes up
periodically.

### 3.3 The periodic packing: bcc (the 2026-10-09 stacking study, now checked exactly)
- The densest lattice packing of the filled cluster is **body-centred cubic**, same orientation
  everywhere, cube edge **a = 6.668296** (= 5.988503 r_in; contact spacing found by bisection, 0 of 14
  reaching shifts overlapping), nearest neighbours **5.774914** apart along the cluster's 3-fold axes;
  **density 0.71537** (gap 28.46%).
- **Contacts are only edge–edge crossings:** with each 3-fold neighbour, 6 outer-dodecahedron edges
  cross 6 of the neighbour's (no face lies on a face, no vertex on a face); with the 6 cube-axis
  neighbours there is no contact at all. Blocks never meet on a face.
- The block pokes out of its truncated-octahedron Voronoi cell by **0.184900** at 48 outer-dodecahedron
  vertices (its reach along a 3-fold axis is 3.0724 against the cell's hexagon at 2.8875); 1.501% of
  its volume lies in the 8 neighbouring cells.

### 3.4 Can filled clusters tile space, alone or with a partner?
- **Alone: no** (71.5% at best by translations; no whole-face contact is possible between copies).
- **With a partner piece, as Hexa + Hexa-Key: no.** In the bcc packing the gap is **one connected
  labyrinth** (64³ periodic grid: 28.51% free, a single component through the whole cell), because the
  blocks touch only on crossing edges; there are no sealed pockets to be a Key. A partner can only be
  made by *cutting* the labyrinth by convention.
- **The grown unit (cut by the Voronoi walls):** block + its share of the gap = its truncated-octahedron
  cell with 48 pokes out and 48 dents in, volume exactly a³/2 = 148.256814; it fills space by the bcc
  translations by construction. Computed here as the block's 63 pieces plus a convex decomposition of
  the fins: 87 block pieces reach into the cell (its own 63 and 24 from the 8 three-fold neighbours),
  and cutting the cell by their faces leaves **696 convex fin pieces**, disjoint (scipy: no sample point
  in two pieces), total **42.04** against the exact 42.198 = a³/2 − 104.466 (block inside its cell) −
  1.592 (neighbours' pokes); the 0.4% missing is slivers thinner than the tolerance, dropped. The fins
  are 28.5% of the unit, in one connected region inside the cell: chunky, as #13 says, not slim stars.
  Render `c13-grown-unit` (`data/c13-grown-unit`, `c13-grown-fins`, `c13-grown-fins-points`;
  `results-grown.json`). (krp-core's O(n³) hull mis-measures some slivers, 44.10 in Node; the scipy
  figures are the ones to trust.)
- **Separability of the bcc stack:** a bare block (no fins) cannot be lifted straight out of its 14
  neighbours along a cube axis, a 3-fold axis or a face diagonal: the interlocking pokes catch it.
  With fins the units are the Voronoi cells with the same pokes, so they interlock the same way; the
  stack is not separable by straight pulls in those directions (other directions untested).

## 4. Data (`data/`)
Each shape in `-unit` and `-raw` scale, with `credit`, `name`, `vertices`, `faces` (outward),
`faceTags` (dodeca / wedge / needle / fin / hull), `volume`, `checks`. Parts files carry `parts[]` with
`role`. Arrangements (unit only): `c13-star-clean` (cluster + 3 corner-sharing neighbours),
`c13-star12-network` (all 12, for the impossible-star render), `c13-column`, `c13-bcc-9` (cluster + 8
bcc neighbours), `c13-grown-unit`, `c13-grown-fins`. Numbers: `results-build.json`,
`results-hulls.json`, `results-grown.json`; scripts `lib.mjs`, `build.mjs`, `hulls.mjs`, `grown.mjs`,
`render.mjs` (all research, reading krp-core, writing nothing into the repos).

## 5. Checks
- No overlap among the 63 pieces, and among the 133 convex parts of the units view (separating axes).
- Filled cluster, star, finned unit, all parts views: closed, consistently wound, Euler 2, exact volumes
  (to 1e-9), union faces cancel exactly in pairs (132 pairs), no triple faces.
- Wedge halves and needle thirds by the mirror planes: volumes φ³/40 and (45−19√5)/1800; 12 finned
  units + centre rebuild the filled cluster exactly.
- Hull: 60/90/32 with 12 regular pentagons and 20 hexagons of edges 1 / 2.065248 (exact (27+7√5)/10).
- DICTO-Star: 12/12 of its dodecahedra are parallel copies of the centre on the cluster's axes.
- Hops, star, lattices, mirror hops, column, bcc: pairwise separating-axis tests on all 63 pieces of
  each cluster; bcc spacing by bisection; gap connectivity by periodic flood fill on a 64³ grid.
- krp-core's `verify-dodeca-cluster.mjs` (congruence, exact volumes, separability) still stands beneath
  all of this.

## 6. Renders (`renders/`, app colours: dodecahedra EKP gold 0xffc857, wedges 0x4dd0e1, needles stella
0xc792ea, fins cube-grey 0x9fb4c8; neighbouring clusters in the arrangement palette)
`c13-filled`, `c13-filled-5fold`, `c13-parts-exploded`, `c13-units-exploded`, `c13-stars-exploded`,
`c13-wedge`, `c13-needle`, `c13-star`, `c13-finned-unit`, `c13-convex-hull`, `c13-hull-over-cluster`,
`c13-corner-sharing-3`, `c13-star12-overlapping`, `c13-column`, `c13-bcc-9`, `c13-grown-unit`.

## 7. Prior art (web, 2026-10-09; quick)
- The 13-dodecahedron face-sharing cluster is the 120-cell's first shell and the 10.3048° gap is the
  classic frustration angle (Sadoc & Mosseri; Fang, Irwin et al. 2018; Koca, Koc, Koca & Al-Siyabi,
  *Dodecahedral structures with Mosseri–Sadoc tiles*, Acta Cryst. 2021 — tetrahedral golden tiles that
  decompose dodecahedra/icosidodecahedra and tile space "with maximal face coverage", not this
  cluster's gaps). Kabai (*Mathematica Journal* 14, 2012) places rhombic triacontahedra and
  dodecahedra at the vertices of icosahedra/icosidodecahedra ("when dodecahedra are used … they are
  attached to each other along their edges"), with icosahedral clusters of 13 / 55 / 147 sites: the
  13-site icosahedral cluster is standard (Mackay / Frank), but with parallel pieces at icosahedron
  vertices, not face-sharing mirror images. George Hart's polyhedra clusters: stellated and great
  dodecahedra in icosahedral arrangements, no face-sharing dodecahedra. Robert Austin: rings and
  icosidodecahedra on dodecahedron faces, not this.
- **Not found:** the cluster's convex hull as the non-regular truncated icosahedron (edges 1 and
  2.0652), the "at most 3 corner-sharing neighbours, at 116.57°" result, the mirror column, the
  edge-crossing bcc contacts and the one-labyrinth gap. The bcc packing of the block and the 13-atom
  icosahedral cluster frustration are known ideas in other guises (icosahedral cluster packings in
  quasicrystal approximants, e.g. the 2/1 AlPdMnSi dodecahedral clusters, are *atomic* clusters
  packed on cubic lattices, not solid clusters). Not proof of novelty.

## 8. Questions for DICTO
1. **Names.** Proposed only, nothing fixed: "DICTO 13-cluster" for the filled solid; "wedge", "needle",
   "star" (3 wedges + needle), "finned unit"; the hull "the 13-cluster hull". Keep #13's words, or
   name them as the Hexa family was named?
2. **Which to build into the apps:** (a) the pieces + Parts view in Polyhedraverse (recommended);
   (b) also the arrangements (corner-sharing trio, column, bcc stack) as a study view in Kaleidohedra
   3D+; (c) the grown unit as a piece (it is exact but ugly: 696 fin fragments).
3. **Scale:** catalogue at krp-core's dodecahedron edge 1 (unit, so it attaches to every pentagon piece
   and the DICTO-Star), or the raw EKP frame (so its centre is the Sunstar dodecahedron)? Both are
   written; the unit one is what POLYHEDRA uses.
4. **Attachable pieces:** which should be attachable in the picker: the filled cluster (72 pentagons),
   wedge, needle, star? The finned unit's fins have odd faces (trapezoid halves); attach by pentagon
   only?
5. **Colours:** wedges cyan and needles stella-purple here, to tell them apart from the gold
   dodecahedra; the app's choice is open.
6. **DICTO-Star relation:** worth recording in #13/#14 (the star is the cluster opened 0.2629 with each
   outer turned 36°)? It is a clean statement, checked exactly.
7. **#17's rule:** record the icosahedral exception (12 corners, at most 3 neighbours, no lattice) as a
   note under #17, or as its own finding?
