# Capturing the In-betweens: a Study of Transitional Polyhedral Shells

**DICTO** · dictospheres.com

*First draft for DICTO, 13 October 2026. Not released. Computation, checking and drafting with Claude (Anthropic). The structures, their pieces and their names are DICTO's.*

---

## Abstract

Three exact icosahedral dissections by DICTO, the Chain of Karma, the Spheres of Dharma and the Bodhi Seed, each build a larger polyhedron from a small core by adding rings of congruent pieces. Between the regular, Archimedean and Catalan solids that the builds pass through lie intermediate stages, which we call transitional shells. We treat each stage as a single solid by fusing its pieces. We then identify the stages that are classical polyhedra and describe the 21 piece types technically.

On the main routes, the counts are 11 stages for the Spheres of Dharma (7 convex), 6 for the Chain of Karma's Lotus seed (2 convex) and 6 for Bodhi Seed Kit B (2 convex). Counting every combination of whole rings gives 107, 7 and 10 stages. Counting partial rings as well gives 5,569, 124 and 363.

Three classical solids occur among the intermediate stages, and one further convex stage has no name we could find; each identification was confirmed against an independent construction to within 10⁻⁴:

- **Lotus seed, stage 2** (icosahedron + 20 CLEO) is the solid bounded by Kepler's great stellated dodecahedron: 60 golden triangles and 32 corners.
- **Lotus seed, stage 3** (+ 30 AXE) is the excavated dodecahedron. Its surface is the Ef1g1 stellation of the icosahedron, and it has exactly the same 32 corners as stage 2.
- **The same two solids reappear** in the Dodecahedral Chain at the same size, and in Samsara (Chain step 2) at scales 1/φ and φ².
- **Bodhi Seed Kit B, stage 2** (rhombic triacontahedron + 60 Vajra (fine)) is the rhombic hexecontahedron.
- **Spheres of Dharma, stage 7** is a convex solid with 80 corners and faces of 12 regular pentagons, 30 rhombi and 60 isosceles triangles. It is the truncated icosahedron with a low hexagonal pyramid (Shield) on each hexagon. We found no name for it.

Three of the piece types are known solids: AXE, CLEO and t1 are Mosseri–Sadoc tiles. One piece, Cleo-low, is similar to a fourth Mosseri–Sadoc tile, t3. The caps are Johnson solids J2 and J11.

We give A4 cut-out nets, checked for overlaps, for four of the transitional shells.

---

## 1. Introduction

While scrubbing the Top-shell slider in the Kaleidohedra app's Multi-shell chains world, DICTO noticed that the in-between stages of his nested structures look very different from the solids at the start and end of each step. He picked out about 11 striking stages on Chain step 2, 5 on the Lotus seed, 4 on the Dodecahedral Chain and 6 on the other views. His proposal was that "these forms may be known about, but possibly not viewed as transitional shapes between the regular well-known solids, and there may be hidden value in analysing the transitional steps that show as the models build and change."

This paper does four things:

1. It defines the stages exactly (Section 2).
2. It describes the pieces that build them (Section 3).
3. It identifies the stages that are classical solids and checks each identification against an independent construction (Section 4).
4. It reads the result against the literature DICTO pointed to: crystal and cluster growth, virus capsids, materials science, chemistry and medicine (Section 5).

Section 6 gives our own assessment of what the transitional shells are worth, and Section 7 gives the plan for them in the apps. Section 8 describes the cut-out nets.

## 2. The structures and their stages

**The structures.** All three structures are DICTO's published findings. The Lotus seed is the icosahedron of edge φ², cut into 13 icosahedra, 60 AXE, 20 FUJI and 20 CLEO, 113 pieces in all [DICTO, Chain of Karma]. Replacing every icosahedron with a Lotus seed gives Samsara (Chain step 2, 1,569 pieces). Closing a grown core with 12 pentagonal caps gives the Dodecahedral Chain.

The Spheres of Dharma is a six-shell cycle of 237 pieces [DICTO, Spheres of Dharma]:

> icosahedron 1/φ → icosidodecahedron φ/2 → dodecahedron 1 → truncated icosahedron 1/φ → rhombic triacontahedron → icosahedron φ²

The outer icosahedron is φ³ times the inner one, so the cycle repeats. The Bodhi Seed is a rhombic triacontahedron of edge φ² holding 12 triacontahedra of edge 1 on its five-fold axes around one of edge 1/φ [DICTO, The Bodhi Seed]. Its gap is filled exactly by Kit A (Vajra (fine), Chatra, Mudra) or by Kit B (Vajra (fine), Crown Jewel, Diadem L and R).

**Stages.** Inside each structure, every piece is assigned to a ring: an orbit of congruent pieces at one distance from the centre. A *stage* is the union of a set of rings. The study counts stages in three ways:

- **Main route.** Rings are added in order of distance.
- **Whole-ring stages.** Any union of rings that touches the core.
- **Partial-ring stages.** Symmetric parts, hemispheres or caps of a ring, added to a whole-ring stage.

The app's Top-shell slider groups rings into levels slightly differently (`appstages.json`). Table 1 gives the counts. They come from the study's data (`stages.json`, `partials.json`); we did not recompute them.

**Table 1.** Stage counts.

| Structure | Main-route steps | Whole-ring stages (convex) | Partial-ring stages |
|---|---|---|---|
| Spheres of Dharma (one cycle) | 11 | 107 (8) | 5,569 |
| Chain of Karma, Lotus seed | 6 | 7 (2) | 124 |
| Bodhi Seed, Kit B | 6 | 10 (2) | 363 |

**Fusing.** We treat each stage as one solid: the outer surface of the union of its pieces. Coplanar parts of piece faces are merged, and gaps from rounding are closed. Faces pointing inward are subtracted from those pointing out, and every face is checked to be a simple polygon. The fused solid's volume must equal the sum of its pieces' volumes. Six fused stages are already in Polyhedraverse (`transitional.js`); we computed seven more in the same way (`analysis/data/fused-extra.json`).

One convention needs a warning. The study's own face counts (`steps.py`, `renders/index.json`) also merge coplanar faces that touch at only a corner, and they do this unevenly. Lotus stage 2, for example, is counted as 16 triangles, 12 hexagons and 4 decagons on 12 planes. That cannot be right for a stage with full icosahedral symmetry, where all 12 planes must look the same. In this paper we count faces as the fused polyhedra in `transitional.js` do. Under that convention Lotus stage 2 has 60 triangles, 90 edges and 32 corners.

## 3. The pieces

Table 2 lists every piece type. Lengths are in the study's own units:

- **Lotus seed:** icosahedra of edge 1, core of edge 1/φ.
- **Bodhi Seed:** copies of edge 1.
- **Spheres of Dharma:** dodecahedron of edge 1.

Dihedral angles are interior angles. Symmetry is the order of each piece's own symmetry group, counting rotations and reflections; "chiral" means the piece has no reflection symmetry.

The script `analysis/pieces_analysis.py` sorts the 11 views' pieces into congruence classes, allowing for scale. AXE, FUJI, CLEO and the icosahedra recur in Samsara at scales 1/φ, 1 and φ². Closed forms were fitted to the measured values, such as edge² = (3 − √5)/2 for edge 1/φ and cos² = 5/9 for 138.19°. They agree to 3 × 10⁻⁵, but they are fits, not proofs, so we do not quote any that are not already standard.

**Table 2.** The pieces. Where DICTO has not yet named a piece, its working label is shown in brackets.

| Piece (DICTO's name) | Where, how many | Kind (technical) | Corners / edges / faces | Edge lengths (count) | Interior dihedrals | Symmetry | Volume | Known as |
|---|---|---|---|---|---|---|---|---|
| **AXE** | Lotus 60 | tetrahedron with five edges 1 and one 1/φ | 4 / 6 / 4 triangles | 1 (5), 1/φ (1) | 41.81°, 63.43°, 79.19° | C2v (4) | 1/12 | Mosseri–Sadoc t6 scaled by 1/τ (checked) |
| **CLEO** | Lotus 20 | trigonal pyramid: base equilateral 1/φ, sides 1 | 4 / 6 / 4 | 1/φ (3), 1 (3) | 63.43°, 79.19° | C3v (6) | (√5 − 1)/24 | Mosseri–Sadoc t4 scaled by 1/τ (checked); the spike of the great stellated dodecahedron |
| **FUJI** | Lotus 20 | hexagonal pyramid, base hexagon with all angles 120° and sides 1, 1/φ alternating | 7 / 12 / 6 triangles + 1 hexagon | 1 (9), 1/φ (3) | 37.38°, 41.81°, 142.62° | C3v (6) | (1 + 3√5)/24 | not a union of Mosseri–Sadoc tiles at this scale [DICTO, Icosa-13 study] |
| icosahedra | Lotus 1 + 12 | regular | | | 138.19° | Ih (120) | | |
| pentagonal cap | Dodecahedral Chain 12 (edge 1); Dharma 12 (edge 1/φ) | Johnson solid J2 (equilateral pentagonal pyramid) | 6 / 10 / 6 | all equal | 37.38°, 138.19° | C5v (10) | | J2 |
| **Stupa** (pentagonal pyramid, npyr5) | Dharma 12 | pentagonal pyramid, base 0.809 (= φ/2), sides √3/2, apex pointing in | 6 / 10 / 6 | φ/2 (5), √3/2 (5) | 43.36°, 132.40° | C5v (10) | 0.19734 | not J2 (sides longer than base) |
| **Vajra (twist)** (nfru3) | Dharma 20 | trigonal antiprismoid ("twisted triangular frustum"): parallel equilateral triangles 1/φ and φ/2, six side triangles | 6 / 12 / 8 triangles | 1/φ (3), φ/2 (3), √3/2 (6) | 99.26°, 110.91°, 113.80° | C3v (6) | 0.22215 | none found |
| **Cleo-low** (npyr3) | Dharma 20 | trigonal pyramid: base equilateral φ/2, sides 1/2; the dodecahedron's corner over the icosidodecahedron | 4 / 6 / 4 | φ/2 (3), 1/2 (3) | 37.38°, 116.57° | C3v (6) | 0.016855 | similar to Mosseri–Sadoc t3 (half its tabulated size; checked) |
| **Monkey Staff** (twisted pentagonal frustum, nfru5) | Dharma 12 | pentagonal antiprismoid: pentagons 1/φ and 1; 5 equilateral and 5 obtuse golden side triangles | 10 / 20 / 10 triangles + 2 pentagons | 1/φ (15), 1 (5) | 63.43°, 142.62° | C5v (10) | (11√5 − 15)/24 | none found |
| t1 (nt1) | Dharma 30 | tetrahedron | 4 / 6 / 4 | 1/φ (5), 1 (1) | 37.38°, 116.57°, 138.19° | C2v (4) | (√5 − 2)/12 | Mosseri–Sadoc t1 scaled by 1/τ (checked) |
| **Shield** (hexagonal cap) | Dharma 20 | very low regular-hexagon pyramid on the truncated icosahedron's hexagon | 7 / 12 / 6 triangles + 1 hexagon | 1/φ (6), 0.651 (6) | 20.91°, 159.45° | C6v (12) | 0.06763 | none found |
| **Vajra-blade** (wedge) | Dharma 60 | tetrahedron (one mirror) | 4 / 6 / 4 | 1/φ (3), 0.651 (2), 1.0898 (1) | 20.55°, 20.91°, 144°, 159.10° | Cs (2) | 0.011271 | none found |
| **Sevenfold-blade** (edge piece) | Dharma 30 | 6-corner solid, 6 triangles + 1 quadrilateral | 6 / 11 / 7 | 0.7265 (2), 1.0898 (4), 1.5568 (4), φ² (1) | 72°, 85.66°, 108°, 112.53° | C2v (4) | 5 − 2√5 | none found |
| **Cleo-low 2** (face piece) | Dharma 20 | trigonal pyramid: base equilateral φ² (the outer icosahedron's face), sides 1.5568 | 4 / 6 / 4 | φ² (3), 1.5568 (3) | 26.26°, 134.93° | C3v (6) | 0.36892 | none found |
| J11 (Dharma hinge) | hinge 12 | gyroelongated pentagonal pyramid, edge 1 | 11 / 25 / 15 triangles + 1 pentagon | all 1 | 100.81°, 138.19° | C5v (10) | (25 + 9√5)/24 | Johnson solid J11 |
| **Vajra (fine)** (B1) | Bodhi kits A and B, 60 | irregular triangular bipyramid | 5 / 9 / 6 | 1/φ (2), 1 (3), 1.0515 (1), 1.4734 (1), 1.7013 (2) | 72°, 90°, 108°, 120° | Cs (2) | RT(1)/60 = 0.20518 | none found [Bodhi pieces study] |
| **Chatra** (B2) | Kit A 60 | 7-corner solid: 3 triangles, 2 quadrilaterals, 1 pentagon | 7 / 11 / 6 | 0.9106 (2), 1 (5), 1.0515, 1.4734, φ (2) | 60°, 72°, 90°, 108°, 120° | Cs (2) | 0.86915 | none found |
| **Mudra** (B3) | Kit A 60 | quadrilateral pyramid | 5 / 8 / 5 | 1/φ (2), 0.9106 (2), 1 (4) | 36°, 120°, 144° | C2v (4) | 0.09687 | none found |
| **Crown Jewel** (B4) | Kit B 20 | 14-corner solid: 3 triangles, 3 pentagons, 3 hexagons | 14 / 21 / 9 | 0.5628 (6), 1 (6), 1.0515 (3), 2/φ (3), φ (3) | 36°, 90°, 120°, 144° | C3v (6) | 1.95764 | none found |
| **Diadem L / Diadem R** (B5) | Kit B 60 + 60 | 6-corner solid: 2 triangles, 3 quadrilaterals; L and R are mirror images | 6 / 9 / 5 | 0.5628 (2), 0.6498 (2), 1 (4), 2/φ (1) | 36°, 60°, 90°, 108° | C2 (2), chiral | 0.15674 | none found |
| rhombic triacontahedra | Bodhi 1 + 12 (+ outer) | Catalan solid | | 1/φ, 1, φ² | 144° | Ih (120) | | |

Three observations about the pieces:

- **The Bodhi pieces have simple angles.** Every dihedral angle of every Bodhi piece is a multiple of 6°, as the Bodhi pieces study already found [DICTO, Bodhi pieces study]. The Dharma and Lotus pieces instead show the characteristic icosahedral angles: arccos(√5/3) = 41.81°, arccos(1/√5) = 63.43°, 116.57°, 138.19°, and J2's base angle 37.38°.
- **Many pieces are pyramids.** The pyramids and pyramid-like pieces (CLEO, Cleo-low, Cleo-low 2, Shield, FUJI, the caps) each sit over one face of the solid beneath them. The pieces that are not pyramids (AXE, t1, Vajra-blade, Sevenfold-blade, Diadem) sit along edges.
- **One Mosseri–Sadoc similarity is new here.** Cleo-low has the shape of the Mosseri–Sadoc tile t3 at half its tabulated size. This had not been recorded in DICTO's earlier studies, which credit only AXE (t6), CLEO (t4) and t1.

**What each piece does in the transitions.** The main routes (Figures 1 to 3) show the role of each piece:

- **Lotus seed.**
  - CLEO stands on each face of the core icosahedron and turns it into a star (stage 2).
  - AXE fills the 30 grooves between the star's points (stage 3).
  - The 12 outer icosahedra and the outer AXE then build a spiky 180-triangle stage.
  - FUJI fills each three-fold corner last and closes the large icosahedron.
- **Spheres of Dharma.**
  - Vajra (twist) makes an icosidodecahedron with 12 pentagonal dimples, and the 12 Stupas fill the dimples.
  - Cleo-low closes the dodecahedron.
  - The 12 Monkey Staffs and t1 make the truncated icosahedron.
  - Shield turns it into the 80-corner solid; the pentagonal caps and Vajra-blade then complete the rhombic triacontahedron.
  - Sevenfold-blade gives an icosahedron with 20 dimples, and Cleo-low 2 fills them.
- **Bodhi Seed Kit B.** Vajra (fine) turns the centre triacontahedron into a rhombic hexecontahedron. The 12 copies, the two Diadems and the Crown Jewels then close the large triacontahedron.

## 4. Classical solids among the in-betweens

Every claim in this section was checked by `analysis/identify.py`, which recorded 25 checks, all passing (`analysis/identify.log`). Each stage is compared with a solid built independently of the stage's data. Only the size and orientation of the stage's core are taken from the data. The tolerance is 10⁻⁴, because the coordinates are stored to 5–6 decimals.

**4.1 Lotus seed stage 2 is Kepler's great stellated dodecahedron.** We built the great stellated dodecahedron (GSD) from the core icosahedron alone (core circumradius r). Its 12 pentagram faces lie in the planes aᵢ·x = r/√5, one for each five-fold axis aᵢ; each plane holds the five neighbours of the opposite corner. Its 20 points lie where three of these planes meet on a three-fold axis. Lotus stage 2 matches this construction in every respect:

- Its 20 outer corners are the GSD's 20 points (worst error 3.6 × 10⁻⁵).
- Its 12 inner corners are the core's corners.
- Its 60 faces lie in the 12 GSD planes.
- Its faces are exactly the GSD's 60 visible triangles, each a point plus one edge of the core.
- Every triangle is golden: sides 1, 1 and 1/φ, apex angle 36°.
- Each plane carries a regular pentagram (ratio of outer to inner radius = φ²).
- The circumradius equals the GSD formula (√3/4)(√5 − 1)·a with chord a = φ².
- The volume, 1.545098, equals the icosahedron plus 20 golden pyramids.

The stage therefore is the solid bounded by the GSD's outer surface, with 60 faces, 90 edges and 32 corners, as Polyhedraverse shows. As a star polyhedron in Kepler's sense, the GSD has 12 pentagram faces, 30 edges and 20 corners. The GSD first appears in Kepler's *Harmonices mundi* (1619). A by-product of the check: each CLEO (Mosseri–Sadoc t4/τ) is exactly one point of the star, so **GSD = icosahedron + 20 CLEO**. This follows directly from the geometry and is not claimed as new.

**4.2 Lotus seed stage 3 is the excavated dodecahedron.** The checks:

- Stage 3 has the same 32 corners as stage 2 (worst error 1.4 × 10⁻⁵).
- Its 60 faces are equilateral triangles of edge 1, equal to the edge of the dodecahedron formed by its outer corners.
- Every face lies in one of the 20 face planes of the core icosahedron.
- Its volume equals the dodecahedron minus 12 J2 pyramids (4.045117).

This is the excavated dodecahedron. Its surface is the Ef1g1 stellation of the icosahedron in *The Fifty-Nine Icosahedra* (Coxeter et al. 1938) and model 28 in Wenninger (1971). We took the label Ef1g1 from the Wikipedia article, which cites the book; we did not check it in the book. Adding 30 AXE therefore turns the great stellated dodecahedron into the excavated dodecahedron without moving any corner. Only the faces change, from 12 dodecahedron planes to 20 icosahedron planes.

**4.3 The Dodecahedral Chain: icosahedron → great stellated dodecahedron → excavated dodecahedron → dodecahedron.** The Dodecahedral Chain's own stages 2 and 3 are the same two solids at the same size. Stage 2 matches to 1.6 × 10⁻⁷ and stage 3 to 6.3 × 10⁻⁶. Stage 4 adds 12 J2 caps and closes the regular dodecahedron. In four steps, then, the build goes from an icosahedron to its dual dodecahedron through two classical non-convex solids, and the final dodecahedron's corners are the star's points. We have not found this sequence described as a dissection path. The solids themselves are of course classical.

**4.4 Samsara (Chain step 2).** In the app's grouping, Samsara's stage 2 is the excavated dodecahedron at scale 1/φ, and its stage 4 is the great stellated dodecahedron at scale φ². The checks give scale factors φ^−1.000 and φ^+2.000, with corners matching to 1 × 10⁻⁵ and 5.4 × 10⁻⁵. Its other stages (Figure 5) lie on 20 to 144 planes. We did not identify them.

**4.5 Bodhi Seed Kit B stage 2 is the rhombic hexecontahedron.** The checks:

- Its 62 corners are exactly the outer corners of 20 prolate golden rhombohedra of edge 1, one on each three-fold axis around the centre (worst error 3.5 × 10⁻⁶).
- Its volume equals 20 prolate rhombohedra (15.2169).
- Its 60 faces are golden rhombi (diagonal ratio φ) lying on the 30 face planes of the centre triacontahedron.

This is the rhombic hexecontahedron, described by Unkelbach (1940). It is one of the fully supported stellations of the rhombic triacontahedron enumerated by Messer (1995); we did not map it to Messer's notation. The Bodhi pieces study had already shown that the 12 copies enclose this solid [DICTO, Bodhi pieces study]. The new point is that it is also reached from inside, as the centre plus 60 Vajra (fine). The rhombic hexecontahedron and triacontahedron built from golden rhombohedra are standard objects in icosahedral tiling work (Senechal 2004; Kabai).

**4.6 The convex 80-corner stage of the Spheres of Dharma.** Stage 7 is convex: its hull volume equals its volume, 14.40420. Its faces are 12 regular pentagons, 30 quadrilaterals and 60 isosceles triangles.

The brief's lead called the quadrilaterals rectangles. They are **rhombi**, with all sides 0.65097 and angles 56.68° and 123.32°. They are not golden rhombi, whose acute angle is 63.43°.

Its corners are the 60 corners of the stage-6 truncated icosahedron and 20 corners on the three-fold axes, which form a regular dodecahedron. The solid is the convex hull of these two. Equivalently, it is the truncated icosahedron with a Shield on each hexagon. The Shields are so low that a triangle of one Shield and a triangle of its neighbour across a hexagon–hexagon edge lie in one plane, and each such pair is one rhombus. All 90 triangle and rhombus planes are tangent to one sphere, of radius 1.5.

The triangle normals lie in mirror planes, 20.905° from the nearest three-fold axis. That rules out the deltoidal hexecontahedron's planes (14.985°) and the triakis icosahedron's (11.211°). With two corner orbits, three kinds of face and non-regular faces, the solid is not Archimedean, Catalan or Johnson. We found no name for it. It may still appear in Conway-operator catalogues, and DICTO may want to check there before naming it.

**4.7 Two more Dharma stages.**

- **Stage 2** (core + 20 Vajra (twist)) is the icosidodecahedron with 12 inward pentagonal pyramids, each reaching a corner of the core. Its 80 triangles lie on 80 planes.
- **Stage 10** (+ 30 Sevenfold-blade) is the outer icosahedron (edge φ²) with 20 inward triangular pyramids. Their apices are the Shields' apices from stage 7, at radius 1.6057. Its 60 triangles lie on 60 different planes. It is not the great dodecahedron: round the same icosahedron, the great dodecahedron's dimples would reach radius 1.4013, so these dimples are shallower. The brief's lead that stage 10 was a stellation of one 60-faced solid is therefore not supported.

**4.8 Convex stages among the partial rings.** On complete shells, 45 of the Spheres of Dharma's partial-ring stages are convex (`renders/index.json`). They have 36 distinct face signatures, with 17 to 86 faces built from triangles, quadrilaterals, pentagons and hexagons (Figure 6). None has the full icosahedral symmetry, and we have not tried to identify them. They are the "slices" between two closed shells: a truncated icosahedron partly capped, a dodecahedron partly truncated, and so on.

## 5. The literature, field by field

We searched DICTO's reference library first and added every new source to it. Twenty-six entries went into a new "Transitions" section of `INDEX`.

**5.1 Stellation and the history of nested solids.** The identifications in Section 4 put three of the transitional shells into the classical stellation literature: Kepler (1619), Poinsot (1810), Cauchy (1813), Coxeter et al. (1938), Wenninger (1971), Messer (1995) and Cutler and Schulte (2011). Kepler's *Mysterium cosmographicum* (1596) nests the five Platonic solids with spheres in the gaps; Jamnitzer (1568) and Pacioli (1509) drew nested and stellated solids. DICTO's structures are filled versions of such nests, with every gap filled by a few congruent piece types. Stellation adds cells of a fixed plane arrangement. The transitional shells are different: they arise from adding solid pieces, and the planes in use change from stage to stage (12, then 20, then 60 in the Lotus seed). That some stages land exactly on stellations is a fact about these particular golden dissections. It is not true of stages in general.

**5.2 Crystal and cluster growth.** This connection is real at the level of shell types. Atom clusters grow in concentric icosahedral shells, and the shells take the same forms that appear in DICTO's routes:

- **Mackay** (1962): icosahedral shells.
- **Bergman et al.** (1957): icosahedron, then dodecahedron with icosahedron, then a truncated-icosahedral 60-atom shell.
- **Tsai-type quasicrystal clusters** (Takakura et al. 2007): dodecahedron, icosahedron, icosidodecahedron, rhombic triacontahedron.

Magic numbers mark the closed shells (Echt et al. 1981; Martin 1996; Teo and Sloane 1985). The sizes in between are less stable, and growth does pass through them: Baletto, Mottet and Ferrando (2000) follow silver clusters through intermediate morphologies, Baletto and Ferrando (2005) review the subject, and Rossi et al. (2004) describe core–shell clusters.

The match is only structural. In clusters the shells are sets of atom positions with radius ratios set by bonding. DICTO's shells are space-filling solids with golden radius ratios. For example, the 12 + 20 corners shared by Lotus stages 2 and 3 have a radius ratio of 2.384. The 12 + 20 corners of a rhombic triacontahedron, the form usually given for the Bergman cluster's second shell, have a ratio of 0.911. Nothing we found shows that the specific transitional solids occur as cluster shells. The useful, testable step is to compare the stages' corner sets with tabulated cluster shells, radius by radius.

**5.3 Materials and quasicrystals.** The Bodhi result is the strongest material link. The rhombic hexecontahedron (stage 2) is a union of 20 prolate golden rhombohedra, which are the Ammann tiles of 3D Penrose tilings. Clusters of rhombic triacontahedra and hexecontahedra are an established description of icosahedral quasicrystal structure (Kabai; Senechal 2004; Dietl and Eschenburg 2016; Fujita et al. 2013). AXE, CLEO, t1 and now Cleo-low are Mosseri–Sadoc tiles, which build icosahedral tilings (Mosseri and Sadoc 1982; Koca et al. 2020). The transitional shells are therefore made of tiles from the quasicrystal toolbox. Whether any stage is a cluster seen in a real quasicrystal or approximant is open.

**5.4 Virus capsids.** Capsids are single icosahedral shells (Caspar and Klug 1962; Twarock and Luque 2019), and they assemble through partial shells (Zlotnick 1994; Hagan and Chandler 2006; Perlmutter and Hagan 2015). Some mature through observed transitional shells; the HK97 capsid is one (Lata et al. 2000). Concentric organisation (capsid with genome) has been modelled as nested icosahedral point sets (Keef and Twarock 2009). The transitions between icosahedral arrangements have been modelled through 6D lattices (Indelicato et al. 2012; Salthouse et al. 2015), the closest mathematical analogue to "transitional shells" that we found.

Two connections hold:

- Assembly is a sequence of in-between shells, and the in-betweens matter.
- Nested icosahedral shells with golden ratios do occur in capsid models.

One does not: capsid intermediates are partial surfaces of one shell, not solids filling the space between two shells. DICTO's partial-ring stages are the nearer analogue.

**5.5 Chemistry.** Coordination cages self-assemble as polyhedra, among them an M₃₀L₆₀ icosidodecahedron (Fujita et al. 2016), one of the Spheres of Dharma's shells. These systems also give the counter-evidence. Sun et al. (2010) found that M₁₂L₂₄ and M₂₄L₄₈ cages switch sharply between polyhedra with no stable in-between. In chemistry the transitional forms are usually transient and unseen, so the transitional shells cannot claim chemical relevance without a specific system where one is observed.

**5.6 Medicine.** The link is indirect. Some antivirals act on capsid assembly, on intermediates and misassembly, rather than on the finished shell (Stray et al. 2005). Designed icosahedral protein cages built from two or more components (King et al. 2014; Hsia et al. 2016) are studied as scaffolds for vaccines and delivery. DICTO's kits are multi-component, exactly space-filling icosahedral systems, and could serve as geometric templates for multi-shell cage design. We found no evidence that any has been, or that the shapes have a medical use. We record this as a speculative lead, not a finding.

**5.7 Design, building and teaching.** Pearce's "minimum inventory, maximum diversity" building system (1976) is a direct design precedent. A few piece types (AXE, CLEO, FUJI; or the Dharma's ten) produce a long sequence of distinct, exactly fitting forms, including famous ones. Fuller's jitterbug and Verheyen's (1989) jitterbug transformers move continuously between polyhedra by rotating rigid faces. DICTO's transitions are discrete and additive, so the two are complementary rather than alike. For teaching, the shells give a physical route to stellations: the great stellated dodecahedron and excavated dodecahedron become stages one builds by adding pieces, rather than figures obtained by extending planes. Models and nets are the established medium for this (Wenninger 1971; Cundy and Rollett 1951).

## 6. Assessment: what the transitional shells are worth

Our conclusion, separated from the checks above:

1. **Mathematical value, shown.** Exact few-piece dissections pass through named classical solids at intermediate stages: the great stellated dodecahedron, the excavated dodecahedron and the rhombic hexecontahedron. The great stellated dodecahedron and the excavated dodecahedron share all 32 corners and are joined by adding 30 AXE. So the stages give constructive, buildable links between regular, Archimedean, Catalan and stellated forms. These identities are verified. The individual solids are classical; the routes between them, built from DICTO's pieces, we did not find in the literature, although the search was not exhaustive.
2. **One new-looking convex solid, unconfirmed.** The 80-corner Dharma stage has no name we could find. Whether it is new is open until Conway-operator and near-miss catalogues are checked.
3. **Thin value as individual shapes.** Thousands of other stages, including the 45 convex partial-ring stages, have no known name and no demonstrated use. Their value is visual and for design, not as findings. Some of their face counts also depend on the merging convention (Section 2).
4. **Analogy, not evidence, across fields.** Concentric icosahedral shells and growth through non-closed intermediates are real in metal clusters, quasicrystal clusters and virus capsids. Nothing we found shows these particular polyhedra occurring there, and chemistry's cages switch without stable in-betweens. The connection worth testing is a quantitative comparison of stage corner sets and radius ratios with known cluster shells and capsid point arrays.
5. **Clear value for teaching and making.** A movie of the transitions and cut-out models make stellation and duality tangible as growth. This is the most immediate use.

## 7. Next steps (the plan)

The transitional shells are being added to Polyhedraverse as their own group, **"DICTO Transitional Shells"**. The first six are already in (`src/krp-core/src/polyhedra/transitional.js`):

1. Lotus seed stage 2 (the great stellated dodecahedron)
2. Lotus seed stage 3 (the excavated dodecahedron)
3. Lotus seed stage 4
4. Lotus seed stage 5
5. Bodhi Seed Kit B stage 2 (the rhombic hexecontahedron)
6. the Spheres of Dharma's convex 80-corner stage

The app is to get a **movie slider** that plays the transitions a build goes through.

Further work suggested by this draft:

- Make the face-merging convention in `steps.py` symmetric, so that corner-touching coplanar faces are either always or never merged.
- Check the Ef1g1 label in *The Fifty-Nine Icosahedra*, and map the rhombic hexecontahedron to Messer's notation.
- Search the Conway-operator and near-miss catalogues for the 80-corner solid before naming it.
- Compare stage corner sets with tabulated cluster shells (Bergman, Mackay, Tsai) and with capsid point arrays.
- Consider adding the Dodecahedral Chain route (icosahedron → great stellated dodecahedron → excavated dodecahedron → dodecahedron) to the group, as its clearest teaching sequence.

## 8. Cut-out nets

`nets/transitional-shells-nets.pdf` has 12 A4 pages with nets for four shells:

- Lotus stage 2 (great stellated dodecahedron): 44 mm per unit, 5 pieces.
- Lotus stage 3 (excavated dodecahedron): 40 mm per unit, 6 pieces.
- Bodhi Kit B stage 2 (rhombic hexecontahedron): 30 mm per unit, 6 pieces.
- Dharma stage 7 (80 corners): 46 mm per unit, 6 pieces.

On every page:

- Glue tabs are numbered in pairs.
- Mountain folds are dashed blue and valley folds dash-dot red. Three of the four shells are non-convex and need valley folds.
- Pieces are lettered A, B, and so on.
- Each page carries the DICTO mark.

Each net was checked by `nets/nets.py` (`nets/nets-checks.json`):

- Every face is placed once, congruent to its 3D face to 10⁻¹⁰ mm.
- Every edge of the solid is either a fold within a piece or a numbered pair of cut edges, and every pair has a tab.
- No two faces or tabs overlap (worst overlap 10⁻⁷ mm²).
- No piece leaves the page, and no two pieces overlap on a page.

The fold pattern, mountain or valley from the 3D dihedral, together with the glue pairs, reproduces the solid's edge graph exactly. For the convex 80-corner solid this fixes the folded shape (Cauchy's rigidity theorem). For the three star-like solids it fixes the shape once the marked valley folds are used. The nets have not yet been built in paper.

## Figures

![Figure 1](figures/fig1-karma-route.jpg)

**Figure 1.** Chain of Karma, Lotus seed main route: (a) core icosahedron; (b) + 20 CLEO, the great stellated dodecahedron; (c) + 30 AXE, the excavated dodecahedron; (d) + 12 icosahedra; (e) + 30 AXE; (f) + 20 FUJI, the icosahedron of edge φ². Orange: the pieces added at that step. One scale throughout.

![Figure 2](figures/fig2-dharma-route.jpg)

**Figure 2.** Spheres of Dharma, one cycle: (a) icosahedron 1/φ; (b) + 20 Vajra (twist), the dimpled icosidodecahedron; (c) + 12 Stupa, icosidodecahedron; (d) + 20 Cleo-low, dodecahedron; (e) + 12 Monkey Staff; (f) + 30 t1, truncated icosahedron; (g) + 20 Shield, the convex 80-corner solid; (h) + 12 pentagonal caps; (i) + 60 Vajra-blade, rhombic triacontahedron; (j) + 30 Sevenfold-blade, the dimpled icosahedron; (k) + 20 Cleo-low 2, icosahedron φ².

![Figure 3](figures/fig3-bodhi-route.jpg)

**Figure 3.** Bodhi Seed Kit B: (a) centre triacontahedron; (b) + 60 Vajra (fine), the rhombic hexecontahedron; (c) + 12 triacontahedra; (d) + 60 Diadem L; (e) + 60 Diadem R; (f) + 20 Crown Jewel, the triacontahedron of edge φ².

![Figure 4](figures/fig4-named-inbetweens.jpg)

**Figure 4.** The in-betweens identified in Section 4, each at its own scale: (a) the great stellated dodecahedron (Lotus 2); (b) the excavated dodecahedron (Lotus 3); (c) the rhombic hexecontahedron (Bodhi Kit B 2); (d) the convex 80-corner solid (Dharma 7; the rhombi appear as pairs of triangles, because the render shows each piece's faces); (e) the icosahedron with 20 shallow dimples (Dharma 10); (f) the icosidodecahedron with 12 pentagonal dimples (Dharma 2).

![Figure 5](figures/fig5-samsara-stages.jpg)

**Figure 5.** Samsara (Chain step 2), the app's 11 Top-shell stages, one scale: (b) is the excavated dodecahedron at 1/φ and (d) the great stellated dodecahedron at φ².

![Figure 6](figures/fig6-convex-partials.jpg)

**Figure 6.** Twelve of the 45 convex partial-ring stages of the Spheres of Dharma (catalogue stages 62, 38, 29, 84, 31, 85, 86, 88, 83, 89, 69, 76), each with a different face signature; orange marks the partial ring.

## Data, scripts and checks

Everything is in this folder:

- `analysis/identify.py` (log and JSON): the 25 identification checks.
- `analysis/pieces_analysis.py` (log and JSON): the piece table.
- `analysis/fuse_extra.py` with `analysis/data/fused-extra.json`: the extra fused stages, run on dicto-node.
- `figures/compose.py`: the plates, from the study's `renders/`.
- `nets/nets.py`: the nets and their checks.
- `CHECKS.md`: what was verified and how.
- `REFERENCES.md`: the reference list.

## Credits

DICTO: the structures, the pieces and all piece and structure names, the observation that started this study, and the plan for the app. Classical solids are credited to their sources. The Mosseri–Sadoc tiles are due to Mosseri and Sadoc (1982), as tabulated by Koca et al. (2020).

## References

See `REFERENCES.md` for the full list with DOIs. Cited above:

- DICTO, The Chain of Karma (2026), doi:10.5281/zenodo.23310541.
- DICTO, Spheres of Dharma (2026), doi:10.5281/zenodo.23310833.
- DICTO, The Bodhi Seed (2026), doi:10.5281/zenodo.23311353.
- DICTO, Icosa-13 study and Bodhi pieces study, Kaleidohedra repository (studies/2026-10-10-icosa-13, studies/2026-10-12-bodhi-pieces).
- J. Kepler, *Mysterium cosmographicum* (1596); *Harmonices mundi* (1619).
- L. Pacioli, *Divina proportione* (1509); W. Jamnitzer, *Perspectiva corporum regularium* (1568).
- L. Poinsot (1810); A.-L. Cauchy (1813).
- H. S. M. Coxeter, P. Du Val, H. T. Flather, J. F. Petrie, *The Fifty-Nine Icosahedra* (1938; reprint 1982), doi:10.1007/978-1-4613-8216-4.
- M. J. Wenninger, *Polyhedron Models* (1971), doi:10.1017/CBO9780511569746.
- H. M. Cundy, A. P. Rollett, *Mathematical Models* (1951).
- H. Unkelbach, Deutsche Math. 5 (1940) 306–316.
- P. W. Messer, Structural Topology 21 (1995) 25–46.
- A. M. Cutler, E. Schulte, Beitr. Algebra Geom. 52 (2011) 133–161, doi:10.1007/s13366-011-0015-0.
- R. Mosseri, J. F. Sadoc (1982); N. O. Koca et al., Dodecahedral structures with Mosseri–Sadoc tiles (2020).
- A. L. Mackay, Acta Cryst. 15 (1962) 916, doi:10.1107/S0365110X6200239X.
- G. Bergman, J. L. T. Waugh, L. Pauling, Acta Cryst. 10 (1957) 254, doi:10.1107/S0365110X57000808.
- H. Takakura et al., Nature Mater. 6 (2007) 58.
- O. Echt, K. Sattler, E. Recknagel, PRL 47 (1981) 1121, doi:10.1103/PhysRevLett.47.1121.
- T. P. Martin, Phys. Rep. 273 (1996) 199, doi:10.1016/0370-1573(95)00083-6.
- B. K. Teo, N. J. A. Sloane, Inorg. Chem. 24 (1985) 4545, doi:10.1021/ic00220a025.
- F. Baletto, C. Mottet, R. Ferrando, PRL 84 (2000) 5544, doi:10.1103/PhysRevLett.84.5544.
- F. Baletto, R. Ferrando, Rev. Mod. Phys. 77 (2005) 371, doi:10.1103/RevModPhys.77.371.
- G. Rossi et al., PRL 93 (2004) 105503, doi:10.1103/PhysRevLett.93.105503.
- M. Senechal, Donald and the golden rhombohedra (2004).
- S. Kabai, clusters of rhombic triacontahedra and hexecontahedra (Wolfram Demonstrations; Bridges 2011).
- R. M. K. Dietl, J.-H. Eschenburg (2016); N. Fujita et al. (2013).
- D. L. D. Caspar, A. Klug, Cold Spring Harb. Symp. Quant. Biol. 27 (1962) 1.
- R. Twarock, A. Luque, Nat. Commun. 10 (2019) 4414, doi:10.1038/s41467-019-12367-3.
- A. Zlotnick, J. Mol. Biol. 241 (1994) 59, doi:10.1006/jmbi.1994.1473.
- M. F. Hagan, D. Chandler, Biophys. J. 91 (2006) 42, doi:10.1529/biophysj.105.076851.
- J. D. Perlmutter, M. F. Hagan, Annu. Rev. Phys. Chem. 66 (2015) 217, doi:10.1146/annurev-physchem-040214-121637.
- R. Lata et al., Cell 100 (2000) 253, doi:10.1016/S0092-8674(00)81563-9.
- T. Keef, R. Twarock, J. Math. Biol. 59 (2009) 287, doi:10.1007/s00285-008-0228-5.
- G. Indelicato et al., J. Math. Biol. 64 (2012) 745, doi:10.1007/s00285-011-0425-5.
- D. G. Salthouse et al., Acta Cryst. A 71 (2015) 410, doi:10.1107/S2053273315006701.
- Q.-F. Sun et al., Science 328 (2010) 1144, doi:10.1126/science.1188605.
- D. Fujita et al., Chem 1 (2016) 91, doi:10.1016/j.chempr.2016.06.007.
- S. J. Stray et al., PNAS 102 (2005) 8138, doi:10.1073/pnas.0409732102.
- N. P. King et al., Nature 510 (2014) 103, doi:10.1038/nature13404.
- Y. Hsia et al., Nature 535 (2016) 136, doi:10.1038/nature18010.
- P. Pearce, US 3,974,600 (1976); R. B. Fuller, *Synergetics* (1975).
- R. Verheyen, Comput. Math. Appl. 17 (1989) 203, doi:10.1016/B978-0-08-037237-2.50023-4.

DICTO · dictospheres.com
