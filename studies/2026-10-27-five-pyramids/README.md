# Five pyramids: shared networks and new deltahedra (study, 2026-10-27)

Credit: DICTO (question and pieces), with Claude (computation). Research only, no app changes.

**One-line conclusion.** Of the five Platonic face pyramids only Q (tetrahedron) and the octahedron's pyramid can share a
face-to-face network (the octet cut from its centres); the Cleo-Icos meets another face pyramid only base to base in finite
bipyramids and shares space only with partners that are not face pyramids (Antonius, #20/#44; the #47 connectors); and
gluing DICTO's pieces gives no new deltahedron up to 4 pieces (5 pieces in the DICTO-pieces-only search): every
equilateral-surfaced gluing found is a regular solid cut up again (4 Q, 2 P) or a face-gluing of regular tetrahedra,
octahedra and icosahedra.

**Status:** steps 1–3 done (question 1 proved exactly; question 2 searched to 4 pieces, 5 for DICTO's pieces alone;
question 3 answered by an exact counting argument). Next, if wanted: a larger search with Antonius, Admiral Caps and
Tricaps around whole icosahedra (7+ pieces), and dented (excavated) forms, which gluing cannot make.

DICTO's questions: "analysis of idea looking at five pyramids — how many of these are in or could be in shared networks
based on cleo icosa etc, alternative deltahedron networks"; "new deltahedra, maybe including admiral caps etc"; "some of
the new deltahedra variants of regular deltahedra will be different".

## Method

- `scripts/pieces.py`: exact library (sympy) of every piece: regular tetrahedron, octahedron, icosahedron; the five face
  pyramids; half octahedron P; Antonius (middle third of the golden rhombohedron spanned by the Cleo-Icos rays); Admiral
  Cap (krp-core `edgeRoof.js`); the six Mosseri–Sadoc tiles from their edge tables (AXE = t6, CLEO = t4, Tricap = t3,
  Hound Tooth = t2, plus t1, t5); Weirdstone and Tadpole (study 2026-10-10-icosa-networks-3, coordinates recovered exactly
  in Q(√5) and checked planar); Penta-cleo. Data: `data/pieces-report.json` (exact face edge lengths of every piece).
- `scripts/q1_pyramids.py`: exact dihedral angles and face shapes of the five pyramids, exact face-similarity tests, and
  all edge stars (angles adding to 360°). Data: `data/q1-pyramids.json`.
- `scripts/exact_faces.py`: exact face-matching table (which pieces carry each non-equilateral face). Data:
  `data/face-matching-exact.json`.
- `scripts/enum_glue.py` (ran on dicto-big-brother, 4 processes): gluing search. A piece is glued whole face to whole
  congruent face (any face, mirror images allowed), interiors disjoint (manifold3d intersection volume), duplicates removed
  by a labelled distance signature. Pieces at the scale where their equilateral faces have edge 1, and the Mosseri–Sadoc
  tiles also at their second scale so tiles meet on their (1,1,τ) and (1,τ,τ) faces. The surface is merged into planar
  faces; a result is a **strict deltahedron** when every merged face is an equilateral triangle of one size and the surface
  is a closed 2-manifold with Euler characteristic 2 enclosing the pieces' total volume (no partial or edge-only contacts).
  Run A (all 17 pieces with an equilateral face, 25 entries with scales and mirrors): complete to 3 pieces; at 4 pieces the
  fourth is glued on a non-equilateral face whenever the 3-piece cluster has one. Counts 23, 262, 7 162, 120 020 clusters.
  Run B (DICTO's pieces only, no regular solids or P): complete to 2 pieces, then each new piece glued on a non-equilateral
  face; to 5 pieces (19, 191, 1 834, 25 683, 363 319 clusters).
- `scripts/validate.py`: known cases through the same engine: icosahedron + 6 Admiral Caps = octahedron of edge
  φ²/√2 = 1.85123 (#47); Cleo-Icos + Antonius + Cleo-Icos = 6 golden rhombi of side 0.951057 (#20, #44); 20 Cleo-Icos,
  4 Q and 8 octahedron pyramids round one centre = icosahedron, tetrahedron, octahedron. All pass.
- `scripts/classify.py`: distinct solids (corner matching, mirror images identified), compared with the 8 convex
  deltahedra by edge graph (networkx isomorphism) and corner-matching congruence. Data: `data/q2-deltahedra.json`
  (corners and faces of every solid), `data/q2-deltahedra-summary.csv`, `data/q2-deep-results.json`.
- `scripts/render.py`: the two renders.

## Question 1: the five face pyramids

Exact values (`data/q1-pyramids.json`); α = arccos(1/3), θ_D = arccos(−1/√5), θ_I = arccos(−√5/3).

| Pyramid | Faces (edge of the solid = 1) | Base-edge dihedral | Side-edge dihedral | Known networks (cited) | Shared face to face with another face pyramid | Shared in any tiling (not face to face) |
|---|---|---|---|---|---|---|
| Cube (C) | square 1; 4 isosceles (1, √3/2, √3/2), apex angle arccos(1/3) | 45° (cos √2/2) | 120° | cube tiling; #44 {C}; #47 mixes | **No.** Its square meets only another C's square; its sides match no other pyramid's | {C,T,O} (#44 slabs); with all five + connectors (#47) |
| Tetrahedron (Q, T) | equilateral 1; 3 isosceles (1, √6/4, √6/4), apex arccos(−1/3) | α/2 = 35.26° (cos √6/3) | 120° | octet cut from centres (#44); connector Q in #47 | **Yes, with O only**: Q base on O base, the octet cut from its centres; every edge star 4 Q + 4 O | {T,O}, {C,T,O} (#44) |
| Octahedron (O) | equilateral 1; 3 right isosceles (1, √2/2, √2/2) | (π−α)/2 = 54.74° (cos √3/3) | 90° | octet cut from centres (#44) | **Yes, with T only** (as above) | {T,O}, {C,T,O} (#44) |
| Dodecahedron (D) | regular pentagon 1; 5 isosceles, side/base √((9+3√5)/8), apex arccos(√5/3) | θ_D/2 = 58.28° (cos √((5−√5)/10)) | 120° | whole dodecahedra in the Dogstar/Sunstar lattice (#42); #47 mixes | **No.** Pentagon matches no other pyramid's face | Never with face pyramids only (#44); yes with the #47 connectors |
| Icosahedron (Cleo-Icos, I) | equilateral 1; 3 isosceles, side/base √((5+√5)/8), apex arccos(1/√5) | θ_I/2 = 69.09° (cos √(1/2−√5/6)) | 72° (cos (√5−1)/4) | Cleo-Icos + Antonius fill the golden rhombohedron, two to one (#20, #44); OTT's octahedral ray (#43); whole icosahedra in F21 and #47 | **Only finite**: base to base with Q or O (bipyramids, render 1); never in a face-to-face space filling | Never with face pyramids only (#44); yes with Antonius (#20, #44) and with the #47 connectors |

Proof of the face-to-face column (exact, `q1_pyramids.py`):
1. The lateral faces of different pyramids are never similar (apex-angle cosines 1/3, −1/3, 0, √5/3, 1/√5 all differ) and
   never equilateral; so a lateral face can only meet a lateral face of the same kind, and congruence then carries base
   edge to base edge and apex to apex.
2. Bases: squares (C) and pentagons (D) occur once each; the equilateral bases of T, O, I match each other at equal edge.
   So two different face pyramids can meet face to face only base to base.
3. In a face-to-face filling, round a side edge every neighbour is the same kind with the same apex, so the 360° is made
   by 3, 3, 4, 3 or 5 copies: each face pyramid lies inside its whole solid. Round a base edge, pyramids come in
   lateral-glued pairs of one kind, and a mixed star needs equal numbers of α/2 and (π−α)/2 (the angles are Q-independent of
   π, #44 Lemma 2): the only mixed star is 4 T + 4 O = 360°, the octet edge. Of the 20 angle-only mixed stars listed in
   `q1-pyramids.json`, every other one fails the face condition. Cubes never touch tetrahedra or octahedra face to face
   (round a cube edge both faces are squares, so every cell there is a cube).

So: in face-to-face networks the five pyramids behave exactly as their whole solids. The only shared face-to-face network
is Q + octahedron pyramid (the octet, and any of its layer stackings, since every triangle of a tetrahedron–octahedron
face-to-face tiling is shared by one of each). Cleo-Icos-based shared networks need a partner that is not a face pyramid:
Antonius (#20, #44), or the #47 kit (all five solids, hence all five face pyramids, in one tiling with connectors).

## Question 2: new deltahedra from DICTO's pieces

Equilateral faces (`data/pieces-report.json`): regular T, O, I (all faces); P 4; Antonius 2; Admiral Cap 2; M-S t1 2;
AXE 2 (edge τ); Tadpole 2; Q, octahedron pyramid, Cleo-Icos, Hound Tooth, CLEO, Tricap (edge τ), t5, Weirdstone 1 each;
cube and dodecahedron pyramids and Penta-cleo none (Penta-cleo's edges 0.8507, 1, 1, 0.5257, 0.5257, 0.618; excluded).

Exact face matching (`data/face-matching-exact.json`), which decides everything: the Admiral Cap's four side triangles
(1, √2/2, φ/√2) occur on no other piece; the Cleo-Icos side (1, R, R) only on Cleo-Icos and Antonius; Q's and the
octahedron pyramid's sides only on themselves; the Weirdstone and Tadpole quadrilaterals only on themselves (one shared
triangle shape between them); the Mosseri–Sadoc tiles share (1,1,τ) and (1,τ,τ) faces among themselves (and Tricap's
sides (1/φ,1/φ,1) are also the Lotus Jewel's 24 gnomon faces).

Admiral Caps on one icosahedron (exact, by hand): each cap's 4 side triangles lie in 4 faces of Pacioli's octahedron,
and an octahedron face becomes one equilateral triangle only when all 3 caps at its corners are present; a set of caps
closed under that rule is all 6. So caps on an icosahedron give a deltahedron only as the whole octahedron (#47).

**Results.** 772 distinct equilateral-surfaced solids, all checked closed, Euler 2, no self-contact:

| Class | Solid | Built from | Note |
|---|---|---|---|
| (a) congruent to a convex deltahedron | tetrahedron | 4 Q | re-cut |
| (a) | triangular bipyramid J12 | 2 tetrahedra | classical |
| (a) | octahedron | 2 P | re-cut |
| (a) | icosahedron | 1 icosahedron | (20 Cleo-Icos needs 20 pieces; checked in validate.py) |
| (b) variant of a convex deltahedron | **none** | | no gluing in range has a convex deltahedron's face pattern with another shape |
| (c) other face pattern, non-convex | 768 solids | face-gluings of regular tetrahedra, octahedra, icosahedra (with P in place of half octahedra) | e.g. 3 tetrahedra (8 faces, degrees 554433), three of 4 tetrahedra (10 faces, render 2), 2 octahedra (14 faces), up to 4 icosahedra (74 faces) |

No solid uses Antonius, Admiral Cap, AXE, CLEO, Tricap, Hound Tooth, Weirdstone, Tadpole, the Cleo-Icos or the
octahedron pyramid; the only DICTO-related ones are the re-cuts 4 Q and 2 P. Gluings of regular tetrahedra, octahedra
and icosahedra are a known infinite class (joining deltahedra face to face; prior-art.md), and the smallest are inside
Tsuruta et al.'s enumeration of deltahedral graphs up to 10 vertices; so **no shape here is claimed new and none gets a
placeholder name**. A strict deltahedron never contains a tetrahedron on an octahedron or P triangle (α + (π − α) = π
makes the faces coplanar: rhombi), which the search confirms (those gluings are recorded as not strict).

DICTO's "variants of regular deltahedra" (same face pattern, different shape, class b) do exist in the literature
(Tsuruta et al. 2014, graph 9_50: one convex and two non-convex forms), but none arises by gluing within this range;
they come from denting (pushing a corner in), which is removing material, not gluing pieces.

## Question 3: networks of the deltahedra found

Exact, by the counting map of #44 (Lemma 1 and Lemma 2, integrated as in its Corollary 2): a tile that fills space by
congruent copies must have Σ over its edges of length × h(dihedral) = 0 for every additive h with h(π) = 0. With
h(α) = 1: a solid of n_T tetrahedra, n_O octahedra and n_P half octahedra (edge 1) gives 6 n_T − 12 n_O − 6 n_P; with
h(θ_I) = 1: 30 n_I.
- Every solid with an icosahedron has 30 n_I > 0: it fills space neither alone nor with any face pyramids (none has a
  negative θ_I part; the Cleo-Icos's is positive). Antonius has a negative part, so icosahedron-plus-Antonius fillings are
  not excluded: not determined here.
- A strict solid of tetrahedra and octahedra/P has its tetrahedra touching only tetrahedra (above), so it is all
  tetrahedra or all octahedra/P, and 6 n_T − 12 n_O − 6 n_P ≠ 0: none of the 772 solids fills space alone. Tetrahedron
  gluings together with octahedron pyramids (or octahedron gluings with Q) are not excluded by this count: not determined.
- Corner-sharing networks of these (known) solids were not studied, since no new deltahedron was found.

## Renders

- `renders/shared-bipyramids.png`: the three base-to-base meetings of different face pyramids (Q + octahedron pyramid, the
  octet's shared face; Q + Cleo-Icos and octahedron pyramid + Cleo-Icos, finite only).
- `renders/small-deltahedra.png`: the 3- and 4-tetrahedron deltahedra (class c).

## Not determined, and why

- Gluings of 5+ pieces with the regular solids, and 6+ pieces of DICTO's pieces alone: the search grows about 14 times per
  piece (363 319 clusters at 5); the 4- and 5-piece levels also used the rule "glue on a non-equilateral face first", so a
  result whose non-equilateral faces are all closed by coplanar merging with faces added later could be missed there.
- Space fillings of tetrahedron gluings with octahedron pyramids, and of icosahedra with Antonius (not excluded by the
  counting map).
- Exactness: face shapes, dihedral angles, face matching and the counting arguments are exact (sympy, Q(√2, √3, √5)); the
  search, overlap tests and congruence classing are floating point (tolerance 1e-7) and are screening; the four class (a)
  results are classical identities.
