# Scutoids as stand-in pieces for the centre pyramids? (21 Nov 2026)

**DICTO's question:** "Scutoids?" as the stand-in pieces that let centre pyramids fill space.

## The two compounds (exact; scripts/compounds.py, log.txt, data/compounds.json)
The 12:1 and 20:1 ratios are one glued piece each, with equal edges a:
- C1 = truncated icosahedron with a dodecahedron centre pyramid on each of its 12 pentagons.
- C2 = truncated dodecahedron with an icosahedron centre pyramid on each of its 20 triangles.
Neither is one of DICTO's named solids (concordance search: the TI Star puts pyramids on all 32 faces; not this). Working names C1, C2.
Basis alpha = arctan phi, beta = arccos(1/sqrt6). Packet of each compound: zero on both length classes (proved exactly by the
coefficient sums in the log; the pyramid edges 2pi/3 and 2pi/5 are rational).

| compound | edge | count | angle | degrees | ring needs (2pi - angle) | on a face needs (pi - angle) |
|---|---|---|---|---|---|---|
| C1 | hexagon-hexagon | 30 | 3pi/2 - 2beta | 138.19 | pi/2 + 2beta = 221.81 | 2beta - pi/2 = 41.81 |
| C1 | pyramid side-hexagon (reflex) | 60 | 3pi/4 + beta | 200.91 | 5pi/4 - beta = 159.09 | impossible |
| C1 | pyramid side-side | 60 | 2pi/3 | 120 | 4pi/3 | pi/3 |
| C2 | decagon-decagon | 30 | 2alpha | 116.57 | 2pi - 2alpha = 243.43 | pi - 2alpha = 63.43 |
| C2 | pyramid side-decagon (reflex) | 60 | 3pi/2 - alpha | 211.72 | pi/2 + alpha = 148.28 | impossible |
| C2 | pyramid side-side | 60 | 2pi/5 | 72 | 8pi/5 | 3pi/5 |

The reflex edges cannot lie on another piece's face: they must be closed by a full ring. Total alpha, beta, gamma coefficient
demanded at the length-a edges is 0 for both (consistent with packet zero).

## Verdict (ring/angle condition only)
Not impossible by the algebra, and the earlier theorem does not apply. That theorem rules out helpers whose dihedral angles are
all rational multiples of pi. A scutoid is not in that class: a side plane between its two parallel faces makes angle t at the
top and exactly pi - t at the bottom, so its Dehn term is (l_top - l_bottom) x t. It can carry irrational angles and still have
packet zero, which a prism cannot. So the necessary angle data are available. What a scutoid kind must supply:
- C1 reflex edge (length a): a dihedral edge pi*5/4 - beta = 159.09 deg (or several edges adding to it); its partner edge on the
  other parallel face is beta - pi/4 = 20.91 deg. C2 reflex edge: pi/2 + alpha = 148.28 deg, partner pi/2 - alpha = 31.72 deg.
- C1 hexagon-hexagon edge needs pi/2 + 2beta, over 180 deg, so at least two scutoid edges (beta-coefficient 2 in total); C2
  decagon-decagon needs 2pi - 2alpha, likewise at least two.
- The beta (alpha) coefficients supplied must balance at +2 on the 30 edges and -1 on the 60 reflex edges (C1); the top/bottom
  pairing t, pi - t gives the opposite signs needed. Its own rings must also close: not checked.
Not decided: that one scutoid kind exists, or that C1 or C2 plus it tiles. No tiling search was done.

## LEADS
1. Ask whether a scutoid with side edges of length a and top/bottom edge angles from {5pi/4 - beta, beta - pi/4, pi/4 + beta, 3pi/4 - beta} closes its own rings (first check, small).
2. 3pi/4 - beta is the icosahedron centre pyramid's base angle: test whether C1's two-edge ring pi/2 + 2beta = 2 x (pi/4 + beta) is met by tilted sides built on that pyramid.
3. Same for C2 with alpha in place of beta.

## Step 2 (ring system; scripts/rings.py, scripts/box.py, data/rings.json, log.txt)
Question: does one flat-faced scutoid kind S exist that supplies C1's demands and closes all its own edge rings with C1 copies and S copies only?
Model: edge angles as (pi, X) coefficient pairs, X = beta (C1) or alpha (C2); pi and X independent, so a ring closes iff the pi-sum is 2
(1 on a face) and the X-sum is 0. Ring multisets enumerated exactly (integers, Fractions).
- C1 pieces h = hexagon-hexagon (3/2, -2), r = reflex (3/4, 1), s = (2/3, 0). Forced: the hh ring needs X-sum +2 from S edges at
  pi-sum 1/2, so at least two S edges; the reflex ring needs X-sum -1 at pi-sum 5/4.
- Smallest S pair on one side plane: T = pi/4 + beta (110.91 deg) with partner B = 3pi/4 - beta (69.09 deg, the icosahedron pyramid's
  base angle). Rings: h + 2T = 2pi exactly; r + B + one right angle = 2pi exactly; s + s + s.
- C2 mirror: d = decagon-decagon (0, 2), r = (3/2, -1). T = pi - alpha (121.72), B = alpha (58.28, the dodecahedron pyramid's base
  angle). Rings: d + 2T; r + B + one right angle; s: five at 2pi/5.
- Count balance per compound (60 hh-ring slots take 2T each = 60 T... 60 reflex slots take one B and one right angle each):
  T = 60, B = 60, right angles = 60. A piece with 4 T, 4 B and 4 right angles gives exactly 15 per compound. Balanced, nothing left over.
- Such an S exists exactly (box.py): a square tube cut by two parallel planes with unit normal (c, c, sqrt(1-2c^2)), c = cos B
  (C1: c^2 = 1/2 - sqrt5/6; C2: c^2 = 1/2 - sqrt5/10; sqrt(1-2c^2)^2 = sqrt5/3, sqrt5/5, positive). It is a slanted rhombic prism:
  four right-angled lateral edges, top and bottom rhombi with angles alternating B and pi - B on the sides, all edges equal to a by choosing
  the tube width and the height. Its Dehn invariant is zero (a x (B + pi - B) = 0).
- The wider search of rational lateral angles (k <= 4 side planes, denominators <= 12) gives 38 more ring-closing candidates in each case
  (listed in the log); the right-angled slanted prism is the only one that is count-balanced with a single lateral edge per reflex ring.

**Verdict.** Feasible at the ring/angle/count level, both for C1 (beta) and for C2 (alpha): no theorem against one-scutoid-kind
helpers. Honest limits: (1) the solution is a slanted prism, a scutoid with no Y-junction (a true scutoid adds edges and is not needed
here); (2) ring conditions and counts closing is necessary, not sufficient: no placement or tiling was searched, so "C1 plus 15 S
fill space" is not claimed; (3) each ring was matched edge to edge with equal lengths a, not with partial overlaps.
LEADS: (a) place 15 S around one C1 (reflex edge: one S edge B and one S lateral edge in the same ring) and test the vertex rings;
(b) the same for C2; (c) the faces of S (rhombi, side rectangles) must meet C1's faces: check face-to-face fit of the rhombus against
hexagons and pyramid sides.

## Step 3 (placement around one C1; scripts/place.py, data/place.json, log.txt)
The slanted prism S of step 2 is a rhombohedron with all 12 edges equal to a (face angles cos = phi^-2, phi^-2, phi^-4). Each of the 30
hexagon-hexagon edges takes wedges T,T (110.905 deg each) and each of the 60 reflex edges takes B (69.095) and Q (90) in either order,
S edge on the C1 edge at full length a, first face flush with the C1 face. All 48 isometries of S per wedge (all 12 edges, both ends,
both face orders, mirror images included) were generated and tested with the exact separating-axis test for convex polytopes
(C1 split into the truncated icosahedron and 12 pyramids; float64, tolerance 1e-9).
- Each slot alone works: no S wedge overlaps C1; 16 placements per hh slot and 32 per reflex slot survive (faces flush, wedge rings close).
- **Contradiction.** Slots at one truncated-icosahedron vertex clash: an hh slot and a reflex slot meeting at the same vertex have
  NO pair of placements (all 512 tried) whose S pieces are interior-disjoint or identical; the best achievable worst-case
  separation is -0.2432 (a forced interior overlap, far from the tolerance). The same failure holds for 30 hh/reflex pairs without a
  shared vertex and for 60 reflex/reflex pairs, so arc consistency empties the hh slots at once.
- Verdict: one S kind (the slanted rhombic prism of step 2) placed edge to edge at length a cannot be placed around C1: the edge rings
  close in angle and count but the pieces overlap at the vertices. Not excluded: other S kinds in the 38 further ring-closing
  candidates (laterals of other angles), edges meeting at partial length, or other ring splits. C2 not run, since C1 failed.
- LEAD: repeat place.py for one of the 38 other candidates, or allow S edges shorter than a (partial overlap along the edge).

## Step 4 (true scutoids at a TI vertex; scripts/scutoid.py, data/scutoid.json): bounded, undecided
Vertex ledger at a truncated-icosahedron vertex v (exact; spherical vertex figures, area = angle sum - (n-2) pi):
- C1 seen from v is a spherical quadrilateral with corners 138.19, 200.91, 200.91, 120 degrees: solid angle exactly 5pi/3 (alpha and
  beta cancel). What C1 leaves at v is the quadrilateral X with corners 221.81 (hh), 159.09, 159.09 (reflex), 240 (ss): 7pi/3.
- A pyramid apex cone is 5 x 2pi/3 - 3pi = pi/3.
- New exact constraint on the ss ring (not used by the ring theorem): if all three pyramids round one ss edge had their truncated
  icosahedron at the same end, three cones of 5pi/3 would meet there (5pi > 4pi). Only the mixed orientations k = 1, 2 survive
  (k pyramids with base end at v): they leave 5pi/3 at one end of the ss edge and pi/3 at the other, for K pieces and any further C1.
- So a K at v lives in the 5pi/3 end (or fits in pi/3 at the other end) and its vertex figure must tile what X leaves, with corners
  T,T at the hh direction and B,Q at both reflex directions, flush with the four C1 faces. A thin spherical polygon can carry any corner
  angle, so the ledger alone gives no contradiction and no K.
- Verdict (3), undecided. Obstacle: a spherical tiling search of X (area 7pi/3 or 5pi/3) by apex pentagons (pi/3, corners 120), C1
  quadrilaterals (5pi/3) and K polygons, then a 3D K from it. Not done; step 3 already shows that the prism K cannot be that K.

## Status box
Study note, not published. Exact run on the compute host (sympy Fractions in the basis pi, alpha, beta, gamma). No tiling search.

## Proper round (scripts/round_local.py, scripts/round_trivial.py, data/round_local.json, data/round_trivial.json, log_round.txt)
DICTO's question: can a TRUE SCUTOID be the stand-in piece that lets dodecahedron centre pyramids and truncated icosahedra (12:1) fill
space? Unit: C1 (edge 1). Helper: one kind K, mirror images allowed. All claims below are exact (sympy; angles as p*pi + b*beta with
pi, beta independent) or certified at 50 digits with the margin printed. Controls pass: octet ring and octet vertex (8 tetrahedra +
6 octahedra = 4pi); the dodecahedron (known non-filler) fails (2cos 2alpha has minimal polynomial 5x^2 - 4, so 2alpha/pi is irrational).

**1. Without a shape restriction the answer is yes, trivially (round_trivial.py).** Stand C1 on a 5-fold axis. Its top spike rises
1.1135 above the pentagon (zA = 3.4410, pentagon at 2.3274; every other point of C1 is at most 2.3274). Let D be the slab between a
surface S and S - h, where S is the plane z = zc = (2.3274 + 3.4410)/2 with the spike tip above zc added over every lattice point
(period W = 2RA + 1, h = 2RA + 1, RA = 3.4410 the apex distance). D tiles space by translations, C1 lies inside D, and only the
spike tip touches the top. So K = D minus C1 is one flat-faced solid (a ball; its face in the plane zc has a pentagonal hole) and
C1 + K tile space periodically, 1 K per C1 (vol C1 = 62.9509, vol K = 426.7088). A box with a C1-shaped cavity also works. So "one
helper kind" is no obstacle by itself, and packets never stop it (C1 has packet zero, so K needs packet zero, which any such cell
remainder has). The real question is the SHAPE: a true scutoid (two parallel end faces, all other faces lateral, at least one
Y-junction vertex). K above is not a scutoid.

**2. Vertex figures at a truncated-icosahedron vertex v (round_local.py).** What C1 leaves at v is the spherical quadrilateral X:
corners 221.81, 159.09, 240, 159.09 degrees, sides 120 (hexagon), 69.09, 69.09 (spike triangle), 120; area 7pi/3. The spike
triangle has base angle exactly 3pi/4 - beta (cos = 1/(sqrt3 phi), the icosahedron pyramid's base dihedral) and apex angle exactly
2beta - pi/2. Ring alphabet (scope): K dihedrals p*pi + b*beta with b in {-1, 0, 1}; for b = +-1, p in Z/4 (the side-plane angles
T, B, t' = beta - pi/4, pi - t' and their pi-shifts, the ring-closing set of step 2); for b = 0, p in Z/12. Ring fillings at the
corners of X: reflex edge 29 (when the hexagon beside it is a K face), hexagon-hexagon edge 32, spike edge 97 for convex K (29, 33,
106 for non-convex K). So rings and areas alone decide nothing, as in step 4.

**3. Face-to-face tilings (faces meet in whole faces): exact lemmas.**
- B1. Two C1 never share a spike triangle (the base edges coincide: 2(3pi/4 + beta) > 2pi). So every one of the 60 spike triangles
  of every C1 is a face of K: K must have a face congruent to the spike triangle (legs sqrt3 phi/2, base 1).
- B2. Two C1 can share a hexagon only with edge types swapped (hexagon-hexagon edge on reflex edge); then each of the six edges keeps
  a wedge of exactly t' = beta - pi/4 = 20.91 degrees.
- B3. The two hexagons at a hexagon-hexagon edge are never both shared with C1 copies. The hexagon graph is the dodecahedral graph;
  its largest independent set is 8, so at least 12 of the 20 hexagons of each C1 are faces of K: K has a regular hexagon face.
- FORCED. Each wedge t' is ONE edge of ONE K (no other filling in the alphabet). So where a hexagon is shared, K has an edge of length
  1 between its spike-triangle face and a regular-hexagon face at dihedral exactly t'. Since t' carries beta, it is not a lateral
  (rational) angle in the scope: one of these two faces is an end face of the scutoid.
- At v the leftover is then the hexagon L: corners 159.09, 240, 20.91, 159.09, 240, 20.91; sides 69.09, 69.09, 120, 69.09, 69.09, 120;
  area 2pi/3. L is not one scutoid vertex figure: it is not a triangle (Y-vertex) and it lies in no closed hemisphere bounded by any of
  its six sides (end-face vertex; margins >= 0.309). So at least two K meet there.

**Verdict.** Not decided for true scutoids; not proved impossible; no stand-in constructed. Exact so far: (1) unrestricted, one
helper kind always exists, periodic, 1 per C1, so the whole content is the scutoid shape; (2) in a face-to-face tiling a scutoid
helper must carry a face congruent to the spike triangle and a regular-hexagon face, and at every shared hexagon an edge triangle-hexagon
at exactly beta - pi/4 with one of the two as an end face. Obstacle: the remaining search is over scutoid combinatorial types
(end polygons, Y positions) with these forced faces; not run. The step 3 overlap test (float) is not relied on here. Not a
periodic search either: no scutoid K survived to be placed.

LEADS (proper round)
1. Two concrete scutoid cases from the forced edge: (a) end face = the hexagon, the spike triangle a lateral face falling 0.467 to its
   apex; (b) end face = the spike triangle, the hexagon lateral, its two middle vertices Y-vertices, height 0.618. Build each with its
   other faces fitted to X at v and test around one C1 (exact).
2. Case "no hexagon shared" (all 20 hexagons are K faces): K then has both forced faces at every vertex; count faces per C1 (60
   triangles + 20 hexagons) against the faces of one scutoid.
3. The same lemmas for C2 (beta replaced by alpha) are a direct rerun.
