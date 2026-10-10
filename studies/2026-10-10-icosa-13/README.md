# DICTO Icosa-13 (study, 2026-10-10)

Research only, no app changes. Study and family name: **DICTO Icosa-13** (DICTO, 2026-10-10).

**Names (DICTO, 2026-10-10).** DICTO named each shape after seeing it as a 3D model. The sections below keep the
study's working labels; this table maps them:

| Working label | DICTO's name |
|---|---|
| wedge | **AXE** |
| hexagonal pyramid | **FUJI** |
| needle | **CLEO** |
| outer star (FUJI + 3 AXE) | **Triskelion Hex** |
| inner star (CLEO + 3 AXE) | **Triskelion** |
| core | **Inner Eye** |
| finned unit | **Hasu (lotus)** |
| filled cluster | **Lotus seed** |
| parallel cage | **DESHI** |
| DICTO's 13-cell (icosidodecahedron + 12 J11) | **UNITY** |

DICTO asked to try the Dodeca-13 moves (filled cluster, gap pieces, units, tiling) with regular icosahedra,
starting at 13 cells. He has built a 13-cell of his own (photos `~/Downloads/KPR-photos/IMG_2572`, `IMG_2573`: an
icosidodecahedron of PET caps with a mesh of cap security rings). Those materials are flexible, but the connectivity
is the same as the rigid solid, so the photos were read for topology only.

Design study with Claude (Fable), research only: no app changes, literature search
in §9. Geometry comes from krp-core v0.14.0 (`id-star.js`: icosahedron, icosidodecahedron, unit
dodecahedron). Every solid was rebuilt and checked afresh: closed, consistently wound, Euler 2, no overlap by
separating axes, volumes exact. Scale **unit** = icosahedron edge 1 (`data/*-unit.json`; `*-raw.json` are the same
solids before normalising).

Research scripts (kept with the study's working copy, not in the repo): `arrangements.mjs` (§1),
`build.mjs` (§2, §3, writes `data/`), `networks.mjs` (§4), `gaps.py` (§5, numpy/scipy, peaks about
1.3 GB), `render-ico.mjs` (renders). Renders: `renders/*.jpg` (icosahedra in the EKP icosahedron
green, wedges cyan, pyramids and needles purple, the icosidodecahedron gold).

## Summary

1. **Icosahedra can't do what dodecahedra do round an edge.** Two icosahedra leave 83.62° (two gaps of 41.81°), and
   three would need 414.57°. So every 13-cluster has gaps, and the question is which pieces close them.
2. **There are two natural 13-cell cages, both on the 12 five-fold axes:**
   - **Parallel:** outers parallel to the centre, slid in until they meet. They share 30 whole edges, and their
     inner rings are the 12 faces of a dodecahedron of edge 1. **Filled, it is exactly a regular icosahedron of edge
     φ²**, cut into 12 I(1) + a small centre I(1/φ) + 60 wedges + 20 hexagonal pyramids + 20 needles (113 pieces, no
     overlap, 100% fill). This is the direct analogue of the DICTO Dodeca-13. **DICTO's simpler build (§10):** a
     dodecahedron with a J11 on each pentagon, then 30 AXE + 20 FUJI, makes the same solid from 63 pieces.
   - **Turned 36° (DICTO's 13-cell):** the outers' inner rings land on the 12 pentagons of an icosidodecahedron of
     edge 1, and the 12 outers touch each other only at its 30 vertices. Built as icosidodecahedron + 12 J11, it fills
     64.26% of its hull, and the rest is **one connected gap, open to the outside**.
3. **Vertex to vertex** (unit centre, 12 outers touching it tip to tip): **fill exactly 13/27** (proof in §6).
4. **Neither cluster tiles space.** The filled parallel cage is an icosahedron, and icosahedra don't tile. Two
   clusters sharing an outer overlap. Best simple lattice packings found are lower bounds only (§4).

## 1. Ways to put 12 icosahedra round one

| Contact | Positions | Most without overlap | Note |
|---|---|---|---|
| face to face (mirror copy across a face) | 20 | 8 (the octahedral set of faces) | neighbours on edge-adjacent faces always overlap; on vertex-adjacent faces they touch at one point |
| edge to edge (parallel copy at 2 × midradius = φ) | 30 | 10 | shares the whole edge |
| vertex to vertex (at 2 × circumradius along the 5-fold axes) | 12 | **12** | parallel: neighbouring outers 1/φ² apart; turned 36°: 0.1056 apart |

Only the 5-fold axes take all 12, so both cages live there. Sliding the 12 outers inward:

| Cage | First contact (centre distance) | Exact | Outers meet | Inner rings lie on | Centre that fits tip to tip |
|---|---|---|---|---|---|
| parallel | 1.538842 | φR (R = circumradius 0.951057) | 30 shared whole edges | the 12 faces of the dodecahedron of edge 1 | I(1/φ), edge 0.618034 |
| turned 36° | 1.801707 | pentagon distance of the icosidodecahedron (1.376382) + ring height (0.425325) | 30 single points | the 12 pentagons of the icosidodecahedron of edge 1 | I(2/√5), edge 0.894427 |

A unit-edge centre fits neither cage: the tips poke into it by 0.3633 (parallel) and 0.1004 (turned).

**DICTO's observation, made exact.** In the vertex-to-vertex cluster, turned outers sit 0.100406 too far out along
each axis. Sliding them in by exactly that amount puts the 12 rings on the icosidodecahedron's pentagons and makes the
60 ring vertices meet in pairs at its 30 vertices. That is DICTO's 13-cell: the vertex cluster with its unit centre
replaced by the icosidodecahedron.

![parallel cage](renders/ico13-cage.jpg) ![DICTO's 13-cell as 12 whole icosahedra + small centre](renders/dicto13-outers.jpg)

## 2. The parallel cage, filled (analogue of the Dodeca-13)

Checks: each dodecahedron vertex is a ring vertex of exactly 3 outers; each dodecahedron edge lies in exactly 2 outers;
113 pieces with no overlapping pair; all wedges, pyramids and needles congruent within their kind.

| Piece | Count | Faces | Exact volume (edge 1) | File |
|---|---|---|---|---|
| outer icosahedron | 12 | 20 triangles | 5(3+√5)/12 = 2.181695 | — |
| small centre, icosahedron of edge 1/φ | 1 | 20 triangles | 5(√5−1)/12 = 0.515028 | `ico13-small-centre` |
| wedge (tetrahedron: five edges 1, one edge 1/φ; the same piece fills outer and inner edge gaps) | 30 + 30 | 4 triangles | **1/12** | `ico13-wedge` |
| hexagonal pyramid (outer corner; apex at a dodecahedron vertex) | 20 | 6 triangles + 1 hexagon | (1+3√5)/24 = 0.321175 | `ico13-hex-pyramid` |
| needle (inner corner; base a face of the small centre) | 20 | 4 triangles | (√5−1)/24 = 0.051503 | `ico13-needle` |
| **filled cluster**, one solid | 1 | 60 triangles + 20 hexagons (V 72, E 150) | (235+105√5)/12 = 39.148928 = φ⁶ × V(I) | `ico13-filled` |

- **The filled cluster is the icosahedron of edge φ².** Its 20 big faces each consist of 3 outer-icosahedron
  triangles and one hexagonal-pyramid base. Its convex hull is regular (20 triangles of edge 2.618034 at inradius
  1.978609), and the fill is 100.00%. The far tips sit at radius φ²R = 2.489898, the same distance as the DICTO-Star's
  dodecahedra.
- The wedge's dihedral at the unit edge opposite its short edge (where its two equilateral faces meet) is 41.8103°
  (cos = √5/3), exactly the gap two icosahedra leave round a shared edge. Its short edge has 63.4349° (cos = 1/√5).
- The hexagonal pyramid's base is equiangular (all 120°) with edges 1 and 1/φ alternating. Its area is
  √3(1+3√5)/8 = 1.668875 and its height is 1/√3. (The script printed these two as long rational fits, which are
  wrong; these are the exact forms, and they agree with the volume above.)
- **Core:** the unit dodecahedron minus the 12 caps (the J2 pentagonal pyramids of the outers that reach inside it) =
  5φ/2 = small centre + 30 wedges + 20 needles (`ico13-core`). The caps + core rebuild the dodecahedron exactly.

**Stars**, what sits at each of the 20 dodecahedron corners:

| Star | Made of | Faces | Exact volume | File |
|---|---|---|---|---|
| outer star | hexagonal pyramid + its 3 wedges | 12 triangles + 1 hexagon | (7+3√5)/24 = 0.571175 | `ico13-outer-star` |
| inner star | needle + its 3 inner wedges | 10 | (5+√5)/24 = 0.301503 | `ico13-inner-star` |

The inner star's volume equals the J2 cap's exactly: (1/24)(√5−1) + 3/12 = (5+√5)/24. This is a numerical identity;
no geometric reason has been found for it. As in the Dodeca-13, each wedge belongs to two stars, so the stars view
overlaps and doesn't add up to the solid.

![filled](renders/ico13-filled.jpg) ![down a 5-fold axis](renders/ico13-filled-5fold.jpg)
![pieces exploded](renders/ico13-parts-exploded.jpg) ![hull over the cage](renders/ico13-hull-over-cage.jpg)
![wedge](renders/ico13-wedge.jpg) ![hexagonal pyramid](renders/ico13-hex-pyramid.jpg) ![needle](renders/ico13-needle.jpg)
![outer star](renders/ico13-outer-star.jpg) ![inner star](renders/ico13-inner-star.jpg) ![core](renders/ico13-core.jpg)

### Finned units (the separable build)

Each outer icosahedron takes 5 half outer wedges, 5 half inner wedges, 5 pyramid thirds and 5 needle thirds: the
**finned unit**, 21 parts, 45 faces (35 triangles, 5 quadrilaterals, 5 pentagons), Euler 2, volume
(60+25√5)/36 = 3.219492 (`ico13-finned-unit`). **12 finned units + the small centre rebuild the filled cluster with no
overlap**, and a unit lifts straight out along its axis with no collision at shifts 0.01, 0.1, 0.5 and 2.

![finned unit](renders/ico13-finned-unit.jpg) ![units exploded](renders/ico13-units-exploded.jpg)

## 3. DICTO's 13-cell (turned cage): icosidodecahedron + 12 J11

- Each outer icosahedron minus its cap inside the icosidodecahedron is a **J11** (gyroelongated pentagonal pyramid).
  The 13 pieces don't overlap, and the 12 J11 touch each other only at the icosidodecahedron's 30 vertices.
- As one solid: 200 triangles, closed, Euler 2, volume **(60+22√5)/3 = 36.397832** (`dicto13-filled`;
  parts in `dicto13-idd-j11`).
- Other volumes: J11 = (25+9√5)/24 = 1.880192; the icosidodecahedron core (minus 12 caps) = (15+7√5)/3 = 10.217492.
  Seen as 12 whole icosahedra + a small centre of edge 2/√5 ((10+6√5)/15 = 1.561094), it is the same solid with an
  inner void of 8.656398 round the small centre.
- **Round each icosidodecahedron edge:** icosidodecahedron 142.6226° + J11 100.8123° = 243.4349°, leaving
  **116.5651°, the dodecahedron's dihedral angle**. Compare the DICTO-Star, where icosidodecahedron + dodecahedron +
  J63 = 142.6226 + 116.5651 + 100.8123 = 360°.
- Convex hull of the 12 outers: 80 faces (20 triangles + 60 quadrilaterals), volume 56.643419. The 13-cell fills
  64.26% of it, and the gap is one connected region (§5).

![DICTO's 13-cell](renders/dicto13-idd-j11.jpg) ![exploded](renders/dicto13-idd-j11-exploded.jpg)

## 4. Joining and tiling

**Parallel cage (I(φ²)):**
- Two clusters sharing an outer (centres 2φR = 3.077684 apart along an axis) overlap in 20 piece pairs: two
  icosahedra overlapping by a corner, so this is a covering, not a packing.
- Mirrored across one big face: no overlap; the contact is the whole big face.
- Lattice packings by translation in the natural frame (2-fold axes on x, y, z), found by bisection:

| Lattice | Cell parameter | Density |
|---|---|---|
| simple cubic | 4.236068 | 0.51503 |
| bcc | 4.569401 | 0.82068 |
| fcc | 6.130495 | 0.67966 |

  These are lower bounds only. The densest known lattice packing of icosahedra is 0.836357 (Betke & Henk 2000)
  and needs a lattice not aligned with the cube axes. The filled cluster *is* an icosahedron, so its best packing is
  the icosahedron's.

**DICTO's 13-cell:**
- Two on one 5-fold axis (centres 3.603415 apart) overlap in 3 pairs.
- Mirrored across a far-cap triangle: 1 overlapping pair.
- Mirrored across a lower or upper J11 band triangle: 40 and 15 overlapping pairs.
- Lattice packings: simple cubic 4.683282 (density 0.35434), bcc 4.683282 (0.70869), fcc 6.981424 (0.42786). These
  are lower bounds by the same method. The bcc cell equals the simple cubic one, so the body-centre copy fits
  without enlarging the cell.

## 5. Gap connectivity

`gaps.py`: voxel flood fill of the space inside each cluster's
convex hull, at two grid sizes, checked against exact volumes (hull minus the sum of the pieces).

| Cluster | Gap | Sealed pockets | Exact fill |
|---|---|---|---|
| Turned (DICTO 13-cell: icosidodecahedron + 12 J11) | one connected region, open to the outside | 0 | 0.642578 (pieces 36.397832 / hull 56.643419) |
| Parallel (Icosa-13 filled) | none | 0 | 1 (solid) |
| Vertex to vertex (13 icosahedra) | one connected region, open | 0 | **13/27** (proof below) |

Checks:
- **Turned:** the voxel gap volume matches the exact one (20.2472 at h = 0.025, 20.2472 at h = 0.0125; exact 20.2456).
  One component holds 99.8% at h = 0.025, and its volume grows towards the exact value as the grid gets finer
  (20.2044, then 20.2353). The thousands of other "components" are grid slivers where faces meet: the largest of them
  shrinks 8× when h halves (1.7e-4, then 2.1e-5), so they are not real gaps.
- **Vertex to vertex:** measured against the cluster's own convex hull (the hull of the 13 icosahedra).

## 6. Vertex-to-vertex fill is exactly 13/27

**Setup.** `I` is the central icosahedron, centred at the origin, with circumradius R and volume V. Its vertices are
R·u for the 12 unit vertex directions u. Each outer icosahedron is `I` moved by 2R·u, so it touches the central one
vertex to vertex at R·u.

**1. The pieces don't overlap, so their volume is 13V.** Each icosahedron lies inside a ball of radius R around its
centre, so two copies can overlap only if their centres are less than 2R apart.
- Central to outer: the centres are exactly 2R apart, so the two touch only at the shared vertex.
- Outer to outer: neighbouring vertex directions satisfy |u − v| = 4/√(10 + 2√5) ≈ 1.0515, so the nearest centres
  are about 2.103R apart, more than 2R.

**2. The hull volume is 27V.** For any convex body K and finite set T of translations, conv(⋃(t + K)) = conv(T) + K
(Minkowski sum). Here T is 0 plus the 12 points 2R·u, the vertices of 2I. The origin lies inside 2I, so
conv(T) = 2I. For convex K, aK + bK = (a + b)K, so the hull is 2I + I = 3I, with volume 3³V = 27V.

**3. Fill = 13V / 27V = 13/27**; the gap is exactly 14V. Neither depends on the edge length.

**Numerical check** (unit edge, V = 5(3 + √5)/12 = 2.1816950): hull 58.9057647 = 27V; pieces 28.3620349 = 13V.

**Possible generalisation (not checked):** for any centrally symmetric convex polytope with n vertices, a copy placed
vertex to vertex at every vertex gives hull 3P, so the fill would be (n + 1)/27, provided the copies don't overlap.
The non-overlap has to be checked for each shape.

## 7. Gap fillers: what plays the Dogstar's role

In the Sunstar Lattice the Dogstar is the piece that fills the hole between dodecahedra. The pieces doing the same
job in the icosahedron clusters are:

| Cluster | Gap filler | Status |
|---|---|---|
| parallel cage | the **outer star** (outer corner) and **inner star** (inner corner), or the wedge, hexagonal pyramid and needle separately | built and checked (§2) |
| DICTO's 13-cell | the 20 dimples over the icosidodecahedron's triangles, each bounded at the dodecahedron's dihedral angle 116.5651° | **open**: a dodecahedron-type filler is suggested by the angle, as in the DICTO-Star, but no piece was built or checked |
| vertex to vertex | one connected gap of 14 V(I) inside the hull | open; no natural piece found |

None of these is a stellation the way the Dogstar is a stellation of the dodecahedron.

## 8. Recommendation and questions for DICTO

**Recommendation (as for the Dodeca-13):** Polyhedraverse pieces in a **DICTO Icosa-13** family with a Parts view:
- **pieces:** 12 icosahedra + centre + wedges + pyramids + needles;
- **units:** the centre + 12 finned units, the separable build;
- **stars:** icosahedra + 20 outer and 20 inner stars, overlapping as in the Dodeca-13;
- **DICTO's 13-cell** as its own entry, with icosidodecahedron + 12 J11 parts.

A world isn't recommended: neither cluster tiles space (§4).

Questions:
1. ~~Names~~: answered, see the table at the top.
2. Which to build in Polyhedraverse, and which are attachable? The filled parallel cluster is a plain icosahedron of
   edge φ², so it attaches wherever an icosahedron of that size does.
3. Scale: icosahedron edge 1, as built here?
4. Should the open item in §7 be studied next: what fills DICTO's 13-cell dimples (116.57°)?
5. Record in DISCOVERIES: the filled parallel cage = I(φ²) dissection, DICTO's 13-cell = slid vertex cluster, and the
   13/27 fill? The literature search is in §9.

## 9. Literature search (2026-10-10)

Searched: the private references library (82 references, full text of every PDF), arXiv, the Bridges archive,
patents (Lalvani, Hogan), the Polytope Wiki and Wikipedia, and George Hart's pages. Scope: the pieces and clusters
above at any scale. **Not finding something is not proof it is new**; a specialist check would still be needed.

| Item | Result |
|---|---|
| **AXE** (five edges 1, one 1/φ) | **Known.** It is the Mosseri–Sadoc tile *t6* (Mosseri–Sadoc *D*, Kramer *A*), which has five edges τ and one edge 1, scaled by 1/τ (volume τ³/12 → 1/12). Sadoc & Mosseri 1982; Kramer 1982; Koca, Koc, Koca & Al-Siyabi 2020 (arXiv 2009.07048), Table 1. |
| **CLEO** (equilateral base 1/φ, side edges 1) | **Known.** It is Mosseri–Sadoc *t4* (*F*) scaled by 1/τ (volume τ²/12 → (√5−1)/24). Same sources. |
| **FUJI** (hexagonal pyramid) | Not found as a named piece, and **not a union of Mosseri–Sadoc tiles at the Icosa-13 scale** (proof below). Two tests: the mix 3 AXE + CLEO + t1′ has FUJI's volume but not its Dehn invariant; the mix t1′ + t2′ + 2 CLEO + 2 AXE has both, but fails the base-hexagon argument. Mixes that use smaller tiles (scale τ⁻² and below) are still open. |
| **Lotus seed**: the icosahedron of edge φ² cut into 12 icosahedra + I(1/φ) + 60 AXE + 20 FUJI + 20 CLEO | **Not found** as a dissection (the arrangement inside it is Gray's, above). Koca et al. 2020 state that, with the Mosseri–Sadoc tiles alone, the icosahedron cannot be inflated past edge τ. This dissection gets to φ² by using whole icosahedra as pieces, which those tilings don't. Lalvani (US 4,723,382, 1988) builds the icosahedron of edge φ from 20 tetrahedra and 4 octahedra, a different dissection. |
| **DESHI**, the 12 parallel icosahedra sharing 30 edges round I(1/φ) | **Known arrangement.** R. W. Gray, "More Icosahedron Scaling and Packing" (web, 2002-01-12) places icosahedra on the 12 pentagons of a dodecahedron, touching a central icosahedron at a vertex, and notes that all 12 define a larger icosahedron: an icosahedron of scale φⁿ holds a centre of scale φⁿ⁻³ and 12 icosahedra of scale φⁿ⁻², which is DESHI inside I(φ²). Gray does not discuss or fill the gaps. Kabai (Bridges 2010) and Hogan (US 3,953,948) have related rings, not this cage. |
| **UNITY**, icosidodecahedron + 12 J11 on its pentagons | Not found as a named compound. J11 itself (the diminished icosahedron) is a standard Johnson solid. |
| **Inner Eye** (60 triangles, volume 5φ/2) | Not identified. It may be a known stellation-type solid; not checked further. |
| 13/27 vertex-to-vertex fill | Not found stated, but the proof (§6) is elementary. Context only. |
| Lattice packings (§4) | Lower bounds only. The densest known lattice packing of icosahedra is 0.836357 (Betke & Henk 2000; Torquato & Jiao 2009). |

**FUJI and the Dehn invariant.** Two solids of equal volume can be cut into each other only if their Dehn invariants
(the sum over edges of length ⊗ dihedral angle, angles taken modulo rational multiples of π) are equal. All the
angles involved reduce to two, α = arccos(√5/3) = 41.81° and δ = 37.38° (FUJI's base angle on its short edges):
63.43° = π − α − 2δ, 79.19° = α + δ, 116.57° = α + 2δ, 138.19° = π − α, 142.62° = π − δ. These relations were found by
integer-relation search (PSLQ) and hold to 120 digits. Writing each length as a + b√5:

| | 1-part (α, δ) | √5-part (α, δ) |
|---|---|---|
| FUJI | (3, −15/2) | (0, 3/2) |
| 3 AXE + CLEO + t1′ | (27/2, 15/2) | (−1/2, 1/2) |

The √5-parts differ by (α + 2δ)/2 = (π − arctan 2)/2. arctan 2 is not a rational multiple of π, because cos²(arctan 2)
= 1/5, and an angle that is a rational multiple of π with rational cos² must have cos² equal to 0, 1/4, 1/2, 3/4 or 1.
So the invariants differ and no dissection into those five pieces exists.

**FUJI and all six Mosseri–Sadoc tiles.** An integer linear program over the six tiles at four scales (τ⁰ to τ⁻³)
finds mixes with FUJI's exact volume and Dehn invariant, e.g. t1′ + t2′ + 2 CLEO + 2 AXE at the Icosa-13 scale, so
the Dehn invariant alone cannot decide. (CLEO does fit inside FUJI: up to 1.023 × its size, found by optimising over
rotations.) A face argument settles every mix whose tiles are at the Icosa-13 scale or larger:
- FUJI's base is a hexagon with all angles 120°. Mosseri–Sadoc faces are triangles with angles 60° (equilateral),
  36°/72° or 36°/108°, and 120° can only be made as 60° + 60°. So each hexagon corner is the corner of two
  equilateral tile faces lying in the base, one along each hexagon edge.
- At these scales the equilateral faces have side 1 or 1/τ. On a long edge (length 1), two triangles started from
  both ends would overlap unless one face spans the whole edge; a side-1 face cannot start on a short edge (it would
  stick out). So the base holds an equilateral face of side 1 on each long edge and one of side 1/τ on each short edge.
- Those six triangles have total area 3·(√3/4) + 3·(√3/4)/τ² = 1.795, more than the hexagon's 1.669, so two of them
  overlap. Contradiction: no such dissection exists.

**Where this leaves the finding:** the pieces AXE and CLEO must be credited to Mosseri & Sadoc, and the DESHI
arrangement inside I(φ²) to Gray (2002). What has not been found is the *filling*: Lotus seed (whole icosahedra + AXE + FUJI + CLEO filling I(φ²) exactly), its separable
build into Hasu units, and UNITY as the slid vertex cluster. Added to the library: Koca et al. 2020 (Mosseri–Sadoc
tiles), Hogan 1976, Kabai 2010 (link).

## 10. DICTO's simpler build: dodecahedron + 12 J11

DICTO built this in Polyhedraverse on 2026-10-05, while working on a dodecahedron problem, before this study
existed. He put a J11 (gyroelongated pentagonal pyramid) on each of the 12 pentagons of a dodecahedron of edge 1. On
2026-10-10 he recognised it as the Icosa-13.

**Why it is the same cluster.** A J11 is an icosahedron with one pentagonal-pyramid cap removed. On a dodecahedron
face, each J11 plus the cap hidden inside the dodecahedron is exactly one outer icosahedron of DESHI. §2 already
showed that the dodecahedron is exactly the 12 caps + Inner Eye. So the dodecahedron + 12 J11 is DESHI with its
inside filled, and

**Lotus seed = dodecahedron + 12 J11 + 30 AXE + 20 FUJI**: 63 pieces instead of 113. Inner Eye, CLEO, the small
centre and the 30 inner AXE all merge into the one dodecahedron.

Checks (`ico13-dodeca-j11-parts`, rebuilt from krp-core):
- each J11's base is a face of the dodecahedron (12/12); J11 has 16 faces and volume (25+9√5)/24;
- 63 pieces, no overlapping pair (separating axes);
- joined into one solid: closed, consistently wound, Euler 2, 80 faces (60 triangles + 20 hexagons), the same
  outer vertices as the Lotus seed file;
- volume exactly the Lotus seed's: (15+7√5)/4 + 12 · (25+9√5)/24 + 30 · 1/12 + 20 · (1+3√5)/24 = (235+105√5)/12.

**The twin of UNITY.** UNITY is an icosidodecahedron + 12 J11 on its pentagons (the turned cage); this is a
dodecahedron + 12 J11 (the parallel cage). The same move, "a J11 on every unit pentagon", works on both cores. It is
also the easiest way to build the Lotus seed by hand: two standard solids, then the two gap pieces.

Data: `ico13-dodeca-j11` (dodecahedron + 12 J11), `ico13-dodeca-j11-parts` (all 63 pieces).
Literature (2026-10-10): no named solid "dodecahedron + 12 J11" was found (the Johnson augmented dodecahedra J58-J61
use plain pentagonal pyramids on at most three faces). The arrangement is Gray's (2002, §9): his icosahedra "just fit
the pentagon of the dodecahedron", which is the J11 + hidden cap. What is new here is filling it: the 30 AXE + 20 FUJI
that close it into the Lotus seed, and seeing it as the twin of UNITY.

**Why it looks open.** The 12 J11 meet each other only along 30 edges. Between them are 30 wedge-shaped grooves
(one per dodecahedron edge, each filled by an AXE) and 20 hexagonal dents, one at each dodecahedron corner, where
the corner of the dodecahedron itself shows at the bottom (each filled by a FUJI, whose apex is that corner). So the
build is complete with 12 J11; the openings are the gap pieces' places, not missing J11s.

![dodecahedron + 12 J11](renders/ico13-dodeca-j11.jpg) ![63 pieces, pulled apart](renders/ico13-dodeca-j11-parts-exploded.jpg)
