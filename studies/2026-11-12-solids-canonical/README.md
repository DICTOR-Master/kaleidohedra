# Aim 2, chunk 5: DICTO's solids as positive geometries (12 Nov 2026; `scripts/solids_canon.py`, log `data/solids-canon.log`, FINAL ok)

**Conclusion.** Every DICTO solid tested (Cleo-Icos, Antonius, Narcissus, Covenant, twisted cube, Ogdoecontahedron OG, Hecatodihedron)
passes the defining test of a positive geometry exactly (on every face the residue of its canonical form is the face's own form). DICTO's
space-filling joins are exactly pole cancellations: a shared inner face leaves no pole, a mis-fitted face does. The Mahler product
(canonical form at its minimum point times volume, over 6) is new and exact for OG ((384200 − 160400√5)/1539 = 16.5917, the roundest
of the set), Covenant and the twisted cube (both 51/4), and Narcissus (11.0787, a root of an irreducible cubic). Cleo-Icos and Antonius
add nothing new as positive geometries: up to an affine map they are the cube's corner simplex and middle octahedron.

**Question.** Chunk 5 of the aim "geometry gives laws": are DICTO's solids positive geometries, and what do their canonical forms say
(walls/joins, special points, exact numbers)? Chunk 4 checked the same tools on the textbook case (the ABHY associahedron).

**Solids (all exact, in Q or Q(√5)).** Cleo-Icos = conv(centre, one face) of the icosahedron (0, ±1, ±φ); the golden prolate
rhombohedron spanned by that face's corners a, b, c = Cleo + Antonius + Cleo (#44, study 2026-11-10-icosahedra-fill); the icosahedron
as 20 Cleo-Icos; Narcissus in the rational frame (x, √3 y, √(3/2) z) of 2026-11-04-dehn-screen (canonical forms and Mahler products
are affine-covariant, so nothing is lost); Covenant = Narcissus + Narcissus turned over on the hexagon and turned 60°; twisted cube =
the straight pair (turned over only); OG = pentakis dodecahedron with its 20 six-fold corners cut flat through the midpoints of the
six-fold-to-six-fold edges, built here from the truncated icosahedron; Hecatodihedron = polar of OG.

**Method.** Canonical form Ω(P; Y) by Warren's vertex formula (fan over the dual polygon at a corner on more than three faces), as in
chunks 3-4; independent second formula: a triangulation into positively oriented simplex forms (chunk 2). All arithmetic exact
(own Q(√5) class over fractions; sympy for the Narcissus axis). 4 cores, 16 s.

## Checks (86, all held)
- Known answers: cube Ω = ∏ 1/(x(1−x)), cube Mahler 32/3, simplex 64/9; Narcissus volume 3/4 (rational frame) and Mahler about the
  corner centroid = 34/3 (published 4 Nov); OG has 102 corners, 80 faces (20 regular hexagons, 60 kites), squared radii 4/9 and
  (170+2√5)/361 and squared edges 120 × (2/9 − 2√5/27), 60 × (86/3249 + 2√5/361), as published; Hecatodihedron 80 corners, 102 faces.
- Warren = triangulation formula at 8 generic points (4 inside, 4 outside), every solid.
- Bridge (chunk 2): Ω(P; Y) = 3!·vol(polar of P about Y) at 4 interior points, every solid; Ω(OG; 0) = 6 vol(Hecatodihedron) and back.
- **Positive geometry by residues:** on every face F (OG 80, Hecatodihedron 102, all faces of the others), Res_F Ω(P) = Ω(F), the
  canonical form of the face polygon, exact at 3 generic points of the face plane each.
- **Joins:** Ω(rhombohedron) = Ω(Cleo) + Ω(Antonius) + Ω(Cleo) PROVED as an identity of rational functions (8 planes; cleared numerator
  of degree ≤ 5 vanishes on a 6³ grid); Ω(Covenant) = Ω(Narcissus) + Ω(turned Narcissus) PROVED the same way (13 planes, degree ≤ 10,
  11³ grid); Ω(icosahedron) = sum of the 20 Cleo-Icos forms at 8 generic points; poles cancel (residue 0) on both inner cut planes of the
  rhombohedron, on all 15 inner planes of the icosahedron (each holds two opposite edges and four Cleo faces), on the hexagon plane of
  Covenant and of the twisted cube.
- Affine images: Ω(L y)·|det L| = Ω(y) for L = [a b c] taking the cube's corner simplex, middle octahedron and the cube to Cleo-Icos,
  Antonius and the rhombohedron (3 points); hence Mahler 64/9, 32/3, 32/3 (checked exactly).
- Negative controls (all caught): one Warren term dropped (OG) breaks the triangulation match; Antonius treated as simple (one fan
  triangle at its four-face corners) breaks the bridge; a mis-joined pair (second Narcissus shifted 1/7 along the hexagon) leaves a pole
  on the hexagon plane; an off-axis point separates the Covenant and twisted-cube forms.

## Results
| solid | faces / corners | corners on >3 faces | Ω at Santaló point | Mahler = Ω·vol/6 |
|---|---|---|---|---|
| Cleo-Icos | 4 / 4 | 0 | 192 − 64√5 | 64/9 = 7.1111 (affine simplex, the conjectured minimum) |
| Antonius | 8 / 6 | 6 (four faces) | 72 − 24√5 | 32/3 (affine octahedron, the symmetric minimum) |
| golden prolate rhombohedron | 6 / 8 | 0 | 48 − 16√5 | 32/3 (affine cube) |
| Narcissus | 10 / 10 | 6 | see below | **11.078716400698901373** |
| Covenant | 12 / 14 | 6 | 51 (vol 3/2, rational frame) | **51/4 = 12.75** |
| twisted cube (straight pair) | 12 / 11 | 9 | 51 | **51/4 = 12.75** |
| icosahedron (edge 2) | 20 / 12 | 12 | 300 − 132√5 | (400 − 160√5)/3 = 14.0764 (with the dodecahedron; classical) |
| OG | 80 / 102 | 42 (30 on four, 12 on five) | 2580 + 156√5 (scale of `data/`) | **(384200 − 160400√5)/1539 = 16.591745555** |
| Hecatodihedron | 102 / 80 | 80 | (2050 − 870√5)/513 | same as OG (polar pair) |

1. **Narcissus.** The Santaló point (where Ω is least, i.e. the polar body has its centroid at the point) lies on the 3-fold axis at
   depth 0.300092257 of a layer below the hexagon (apex one layer down), the root in (−1, 0) of 4z³ + 19z² + 32z + 8; the Mahler product
   there is 11.078716400698901373, the root of the irreducible 2304m³ − 25440m² − 943m − 30: below the corner-centroid value 34/3, above
   the simplex value 64/9 (the general 3D Mahler conjecture's minimum).
2. **Covenant and the twisted cube** have the same canonical form along the whole 3-fold axis (the 60° turn fixes the axis and has det 1;
   also on the hexagon's mirror planes that are not Narcissus's), hence the same Santaló point (the hexagon centre, although the twisted
   cube has no centre of symmetry) and the same Mahler product 51/4. Elsewhere their forms differ.
3. **OG** is the roundest solid of the set: Mahler 16.5917 = 94.6% of the ball's (4π/3)² = 17.5460 (icosahedron 80.2%). All three
   centrally symmetric values satisfy the proved bounds 32/3 ≤ M (Iriyeh–Shibata 2020) and M ≤ 8E/9 (Winter 2026, flag-number bound,
   E = edges) and M ≤ (4π/3)² (Blaschke–Santaló).
4. **Adjoint** (numerator of Ω over the product of face forms), degree on a generic line: OG 76 and Hecatodihedron 98 (= faces − 4,
   Warren's bound reached), icosahedron 16 (= 20 − 4), Antonius 4; lower where faces are parallel (cube 0, rhombohedron 0, Covenant 6 of
   8, Narcissus 5 of 6, twisted cube 7 of 8).

**What this gives the aim.** In the language of positive geometry the faces of a solid are the poles of its form; DICTO's joins are the
places where poles cancel, so a space-filling assembly has a form whose poles are its outer faces only (the analogue of a physical
amplitude having poles only at its physical channels). The Mahler product is Ω at its least point times volume: a single exact
roundness number per solid. No physical amplitude is claimed for any of these solids.

**Not done here.** The DICTO Yantra cones: they are bounded by circular cones (curved, not polytopes) and their numbers are algebraic
of degree 160 (#103), so they need the curved-boundary theory and a different exact method; queued as chunk 5b.

**Faults fixed on the way.** (1) Pilot: the expected number of inner icosahedron planes was 30; it is 15 (a plane through the centre and
an edge also holds the opposite edge). (2) The first off-axis control point (1/3, 1/2, z) lay on a mirror of the hexagon, where the
Covenant and twisted-cube forms agree too; replaced by (1/3, 3/7, 1/5). (3) An edit with a comment inside an open bracket failed to
compile and the launch, chained with ';', ran the old script: the launch now follows the compile-and-swap with '&&'.

Credit: canonical forms and positive geometries: Arkani-Hamed, Bai, Lam (2017); Warren's adjoint (1996); Mahler products: Mahler,
Santaló, Iriyeh–Shibata (2020), Winter (2026). The solids and their names are DICTO's (Cleo-Icos is the icosahedron's face pyramid,
classical; Antonius #44; Narcissus, Covenant 4 Nov; OG #31; the twisted cube #86; the Hecatodihedron #28).
NEXT (chunk 6): Poincaré dodecahedral space along a Hopscotch line; chunk 5b: the Yantra cones.
