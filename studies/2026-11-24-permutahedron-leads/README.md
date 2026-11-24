# Permutahedron leads (24 Nov 2026)

DICTO · project V SF A (Vacuus, Scutoid Frusta, Aequus). DICTO's strong lead: the permutahedra. "Vacuus", "Scutoid Frusta", "Aequus",
"amber cell" and the combined method are DICTO's. "Face-parallel planes" is a working name for a separate construction, not the Vacuus.

> **Status box.** Study note, not published. Every count below is exact (number fields Q, Q(√2), Q(√5); floats only order polygon
> corners, and every float-derived combinatorics is checked exactly). Solid angles in Section 1 are 60-digit evaluations, used only to
> show inequality by a wide margin (gaps of 0.047 and more). Renders: house renderer, in the reading folder as
> RENDER-associahedron-A3/B3/H3.png. Resume: everything committed; nothing running.

**Verdict.** (1) The three generalized associahedra are found inside the permutahedra exactly as Hohlweg–Lange–Thomas say: keep 9 of 14,
12 of 26, 18 of 62 facets and the corners number 14, 20, 32 (the W-Catalan numbers), for all four Coxeter elements of each group. None of
them, and none of their polars, is a fair die: their symmetry groups have order 2, 1, 1. Their Vacuus is of the inherited heart kind,
since none is centrally symmetric. (2) Cut by its Vacuus, a permutahedron falls into 176, 1160, 7592 pyramids from the centre, each over one
convex piece of one face. Cut by its face-parallel planes it falls into 32, 96, 480 pieces, and every one has exactly three plate walls:
the three face-parallel arrangements are simplicial. A shell between a solid and a smaller copy of itself, cut by planes through the
centre, contains frusta only (Lemma 3), so scutoid frusta need two different patterns. In amber cells the A3 and B3 permutahedra give frusta
only, while the H3 permutahedron gives 62 of 62 scutoid frusta in every cubic mould. At its own s0 in bcc, the truncated octahedron is its
own mould: it tiles space alone. (3) The rolling law for the H4 die (14 400 faces) looks feasible in Lean in stages. Mathlib already has
the H₄ Coxeter matrix. Convexity of a 4D die needs a new local-to-global step (LEAD 1).

## 1. The hidden associahedra (task 1)

**Construction (credit).** C. Hohlweg, C. Lange, H. Thomas, *Permutahedra and generalized associahedra*, arXiv 0709.4241 (2007),
Adv. Math. 226 (2011) 608–640. Take a point a inside the fundamental chamber and a Coxeter element c. Write w0(c) for the c-sorting word
of the longest element (N. Reading, *Clusters, Coxeter-sortable elements and noncrossing partitions*, Trans. AMS 359 (2007)). The
c-singletons are the prefixes of w0(c) up to commutations. Keep exactly those facets of the permutahedron conv(W a) that contain a corner
w a with w a c-singleton; the intersection of their half-spaces is the c-associahedron. Earlier realizations: Loday (2004, type A),
Chapoton–Fomin–Zelevinsky (2002, all finite types). The W-Catalan numbers are due to Fomin–Zelevinsky and Reading.

**Our data.** a = a corner of the uniform permutahedron: (2,1,0) for A3 (in D3 coordinates), (1+2√2, 1+√2, 1) for B3, and
(1/φ, 1/φ, 3+φ) for H3 (the truncated icosidodecahedron, edge 2/φ). Diagram s1–s2–s3, where s1 is the end with the larger bond (B3: 4,
H3: 5). We used all four Coxeter elements: linear s1s2s3 and its inverse s3s2s1, and bipartite s2s1s3 and its inverse s1s3s2. Script
`scripts/assoc.py`, logs `logs/assoc-*.log`, data `data/assoc-*.json` (the removed facets are listed by side count and normal).

| | A3 (truncated octahedron) | B3 (truncated cuboctahedron) | H3 (truncated icosidodecahedron) |
|---|---|---|---|
| permutahedron facets | 14 = 6 squares + 8 hexagons | 26 = 12 + 8 + 6 octagons | 62 = 30 + 20 + 12 decagons |
| kept = n + N (rank + reflections) | 9 = 3 squares + 6 hexagons | 12 = 4 squares + 4 hexagons + 4 octagons | 18 = 6 squares + 6 hexagons + 6 decagons |
| removed | 5 = 3 squares + 2 hexagons | 14 = 8 squares + 4 hexagons + 2 octagons | 44 = 24 squares + 14 hexagons + 6 decagons |
| corners (W-Catalan) | **14** | **20** | **32** |
| f-vector (V, E, F) | 14, 21, 9 | 20, 30, 12 | 32, 48, 18 |
| faces | 6 pentagons, 3 squares | 4 hexagons, 4 pentagons, 4 squares | 6 heptagons, 6 pentagons, 6 squares |
| corners shared with the permutahedron (= c-singletons) | 8 (linear c), 9 (bipartite c) | 12, 13 | 20, 21 |
| symmetry group (about the corner centroid) | order 2: a half-turn (linear c); one mirror (bipartite c) | order 1 (all c) | order 1 (all c) |
| Vacuus (edge plates, about the corner centroid) | 16 plates: 1 full, 4 shared, 11 single (linear); 14: 6 shared, 8 single, 1 on its mirror (bipartite) | 27: 3 shared, 24 single (linear); 26: 4 shared, 22 single (bipartite) | 43: 5 shared, 38 single (linear); 42: 6 shared, 36 single (bipartite) |
| Vacuus kind | inherited heart | inherited heart | inherited heart |
| fair die? (face orbits) | no (5 linear, 6 bipartite) | no (12) | no (18) |
| polar a fair die? (face orbits) | no: 14 triangles in 7 (linear) or 10 (bipartite) orbits | no: 20 triangles in 20 orbits | no: 32 triangles in 32 orbits |

Each facet of a permutahedron through corner w a has normal w ω_s, where ω_s is a fundamental weight. A facet of type s is a 2m-gon, with
m the bond between the other two nodes. Exact checks in `assoc.py`: every permutahedron facet holds exactly its 2m corners, and all others
lie strictly inside. The associahedron corners are all triple intersections of kept planes that satisfy every kept inequality. The count
must equal the W-Catalan number and the kept count must equal n + N (asserted). Faces, edges and Euler are checked exactly by the Vacuus
enumeration's `analyse()`, unchanged. Removed facets for A3, linear c (normal directions): squares (0,±1,0), (0,0,−1); hexagons
(−1,1,−1), (1,−1,−1).

**Fair dice.** A die is fair by symmetry when it is face-transitive. The orders 2, 1, 1 rule that out for all twelve associahedra and
their polars. The Aequus model also allows several face orbits with equal solid angles. Here, about the volume centroid, some face's solid angle
differs from 1/F of the sphere by 0.09 or more (A3), 0.17 or more (B3) and 0.27 or more (H3) for the associahedra, and by 0.047 or more for
the polars (largest deviation per solid, 60-digit evaluations; values in the JSON). **None is an Aequus.**

**Isometry.** For c and c⁻¹ the multisets of corner-to-corner distances are equal (exact), which fits the known isometry
Asso_c ≅ Asso_{c⁻¹} (Bergeron, Hohlweg, Lange, Thomas, *Isometry classes of generalized associahedra*, Sém. Lothar. Combin. 61A (2009)).
The linear and bipartite pairs differ. So each group gives two shapes from these four c.

**Renders** (`scripts/render_assoc.py`, house renderer and compose): for each group, (i) the associahedron with faces coloured by
side count; (ii) the permutahedron inside the see-through associahedron, at the same scale; (iii) the permutahedron close up, with
kept facets in pearl and removed facets in bronze. A pull-apart does not fit here. The permutahedron lies inside the associahedron, and
the region between them is not a set of separate pieces by itself (LEAD 2). The H3 associahedron through the uniform point is very
long: its pentagons reach far out past the removed facets. This is the true shape for this a.

## 2. V + SF on the permutahedra (task 2)

**Setting.** P is the uniform permutahedron, with centre O = its symmetry centre. (a) The Vacuus: one plane through O and each edge,
equal planes merged (#110). (b) The face-parallel planes: one plane through O parallel to each pair of opposite faces. P is cut by all the
planes of (a), or all those of (b). Every plane goes through O, so each piece is the cone from O over one patch of P's surface. Method
(`scripts/cut.py`): every face polygon is clipped exactly by every plane. Each sub-polygon gets its sign vector, and sub-polygons with
equal sign vectors form one patch. Checks: the sub-polygon areas of each face add up to the face area exactly, and the cone volumes add up
to vol P exactly. Each patch is connected with one boundary cycle, and holds at most one sub-polygon per face.

| | A3 | B3 | H3 |
|---|---|---|---|
| Vacuus plates | 15 | 36 | 90 |
| pieces, Vacuus | **176**, all pyramids from O over one convex polygon in one face | **1160**, all pyramids | **7592**, all pyramids |
| their bases (sides: count) | 3: 120, 4: 24, 5: 24, 6: 8 | 3: 456, 4: 528, 5: 120, 6: 8, 7: 48 | 3: 2880, 4: 2880, 5: 1440, 6: 320, 8: 60, 10: 12 |
| face-parallel planes (on Coxeter mirrors) | 7 (0) | 13 (9) | 31 (15) |
| pieces, face-parallel | **32**: 8 pyramids over a triangle in a hexagon; 24 cones over a bent patch (square + hexagon, 5 corners) | **96**: 48 cones over square + hexagon + octagon, each holding one corner of P; 48 over square + hexagon | **480**: 120 cones over square + hexagon + decagon, each holding one corner of P; 120 over square + hexagon; 120 over square + decagon; 120 pyramids over a triangle in a decagon |
| plate walls per piece, face-parallel | 3 for every piece | 3 for every piece | 3 for every piece |

In the Vacuus cut every edge of P lies on a plate. So no patch crosses an edge, and every piece is a pyramid over part of one face.
In the face-parallel cut every piece has exactly three plate walls, so these three central arrangements (7, 13, 31 planes) are
**simplicial**. For H3 the 15 mirrors give the 120 chambers, one corner in each (#110 item checked again), and the 10 hexagon and 6 decagon
planes split each chamber into 4 pieces.

**Classification under the proposed definition** (study 2026-11-24-scutoid-frusta-enumeration, convex tier):
- A cone piece has its apex at O and only one end. It is **not** a scutoid frustum of either tier: "other (pyramid from the centre)".
- The shell variant: the region between P and λP (0 < λ < 1), cut by the same planes. A piece over a one-face patch is a truncated
  pyramid. It is simple, its ends are the patch and λ times the patch, and every lateral face meets both ends, so it is a **convex frustum
  SF n-n-0**. A piece over a bent patch has bent ends, and its inner end is reflex, so it is not convex. It is a **frustum of the general
  tier** (bent ends, no Y-corner). Counts: Vacuus 176 / 1160 / 7592 convex frusta. Face-parallel: 8 / 0 / 120 convex frusta and
  24 / 96 / 360 general-tier frusta.
- **No piece changes its side count.**

**Lemma 3 (homothetic shells give frusta only).** Cut the shell between a star-shaped solid P and λP by any planes through the centre.
Every piece is a frustum: no piece has a Y-corner. *Proof.* The cut pattern on λP is λ times the pattern on P. So each piece is the set
{t x : x in a patch, λ ≤ t ≤ 1}. Its walls are cones over the boundary edges of the patch, and every vertex lies on one of the two ends. ∎
So scutoid frusta in a shell need **two different patterns**, inside and outside. The combined method gets them by using the solid's
faces inside and the Voronoi pattern of the mould outside.

**Amber cells with the permutahedron as core** (combined method, DICTO's; the amber-cell sweep's `amber.py` unchanged except for the
solid, as `scripts/amber_perm.py` + `scripts/perm_solid.py`; table `data/amber-summary.md`, logs `logs/amber_*`). The cores are the
truncated octahedron, the B3 permutahedron through (1,2,3), and the uniform truncated icosidodecahedron. The B3 core is rational because
the uniform truncated cuboctahedron needs √2, which lies outside the code's field Q(√5). It has the same faces and symmetry. Moulds:
sc, bcc, fcc Voronoi cells, at s0 and 6/5 s0.

| core | s0 (sc / bcc / fcc) | at s0 | at 6/5 s0 (all three moulds valid) |
|---|---|---|---|
| truncated octahedron | 4 / 4 / 6 | **bcc: the core is its own Voronoi cell** (all 14 faces on the mould, resin volume 0): it tiles space alone. sc: self-intersecting; fcc: a collinear wall | 14 pieces, 2 kinds, **all frusta** (0 Y): every face keeps its neighbours (4/4, 6/6) |
| B3 permutahedron (1,2,3) | 6 / 8 / 10 | self-intersecting in all three | 26 pieces, 3 kinds, **all frusta** (4/4, 6/6, 8/8) |
| truncated icosidodecahedron | 7+√5 / 6+2√5 / 4+4√5 | self-intersecting in all three | 62 pieces, 5 kinds, **62 scutoid frusta**; Y vertices 60 (sc, bcc), 48 (fcc); squares 4 → 8 (or 7) mould-side neighbours, hexagons 6 → 3 (or 4), decagons 10 → 5 (or 6) |

The octahedral permutahedra fit the cubic moulds. Their face pattern already matches the mould's Voronoi pattern, so the combined
method needs no Y. The icosahedral one does not fit, and every piece changes its neighbours. In the earlier sweep the icosidodecahedron
and the truncated dodecahedron also gave scutoid frusta, while the dodecahedron, icosahedron and truncated icosahedron gave none.

## 3. LEADS

1. **Rolling law in 4D: the H4 die (feasibility only).** The die is the polar of the H4 permutahedron (the omnitruncated 120-cell): 14 400
   tetrahedral faces, one per element of W(H4). Rolling goes across the 4 face types of triangle, with 60 mirrors, and a longest shortest
   roll of 60 rolls. Corner moves come from rank-2 pairs with m = 5, 3, 3 and three commuting pairs. Mathlib has `CoxeterMatrix.H₄`
   (checked in its source). The 3D proof splits into general theorems (`RollModel`, independent of size) and kernel-checked finite
   tables. Sizes against H3: roll tables 57 600 entries against 360 (160 times), and the corner condition is checked per face and per pair
   (14 400 × 6). Feasible in stages, with care over the encoding (arrays, `decide +kernel`). **The geometric step M4 does not scale as it
   stands.** Checking every face against every corner would mean 14 400 × 2 640 exact dot products in ℤ[√5]. It needs a local-to-global
   lemma instead: a closed, locally convex surface that is star-shaped about O bounds a convex body, so only face–neighbour checks remain.
   Proposed stepping stones, with the same code: A4 (120 faces), D4 (192), B4 (384), F4 (1152), then H4. Fairness (M7) needs only the 4
   generating reflections plus transitivity from the roll tables.
2. **Associahedron shell (V + SF meets task 1).** The region between the associahedron and the permutahedron inside it. Use the
   permutahedron's faces (or Vacuus) as the inner pattern and the associahedron's as the outer pattern. The two patterns differ, which
   Lemma 3 shows is needed for scutoid frusta. A natural amber-type cell whose mould is not a Voronoi cell.
3. **The three simplicial arrangements** (7, 13, 31 central planes; 16, 48, 240 triangles in the projective plane). They should be the
   known simplicial arrangements of Grünbaum's catalogue (B. Grünbaum, *A catalogue of simplicial arrangements in the real projective
   plane*, Ars Math. Contemp. 2 (2009)). The entry names are still to be matched; we have not checked them.
4. **Fair associahedra?** a ranges over a 3-parameter family (the chamber), and c over 4 choices. With symmetry of order 2 at most, an
   associahedron die would need equal solid angles across 5 to 18 orbits, which is far more equations than parameters. A search would
   only look for something that cannot be expected. Not proposed.
5. **4D Vacuus cut**: the 4D pilot of the Vacuus enumeration (`four_d.py`) already has the omnitruncations of A4, B4, H4. The cone counts
   of Section 2 in 4D come next if wanted.
6. **B3 uniform core**: extending the amber code from Q(√5) to Q(√2) would give the uniform truncated cuboctahedron cell. We expect the same
   frusta-only result, since the combinatorics is the same, but this is not checked.

## 4. Questions for DICTO

1. **Which hidden associahedron?** Each group gives two shapes, linear c and bipartite c. For A3 the bipartite one has a mirror and the
   linear one (Loday's) a half-turn. Keep both, or pick one?
2. **"Pieces between the solid and its Vacuus"**: are these the cones from the centre (Section 2, not scutoid frusta), or the shell
   pieces (frusta)?
3. **A name for the face-parallel planes?** They are now known to form simplicial arrangements for all three permutahedra.
4. **LEAD 1 or LEAD 2 next?**

## Files

`scripts/assoc.py` (task 1), `scripts/cut.py` (task 2 cuts), `scripts/perm_solid.py` + `scripts/amber_perm.py` + `scripts/amber_summary.py`
(amber cells), `scripts/render_assoc.py` + `scripts/shots.mjs` (renders); `data/`, `logs/`, `renders/`. Reused unchanged:
`vacuus_exact.py`, `perm_checks.py` (study 2026-11-24-vacuus-enumeration), `amber.py`, `solids.py` (2026-11-21-amber-cell-sweep), render3d.py,
compose.py, shots.mjs (2026-11-21-scutoid-stand-in).

## Decisions (24 Nov; DICTO: "make decisions instead of questions")
1. Keep both associahedra (linear c and bipartite c) for each group.
2. "Pieces between the solid and its Vacuus" = the shell pieces (frusta), not the cones.
3. Name: keep the plain description "face-parallel planes" (placeholder until DICTO names them).
4. LEAD 2 next (associahedron shell, V + SF, the main priority); LEAD 1 (H4 rolling law) in small steps later, A4 first.

- 24 Nov: DICTO named the face-parallel planes **Resonus** (plural Resoni).
