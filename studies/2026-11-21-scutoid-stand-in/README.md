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

## Status box
Study note, not published. Exact run on the compute host (sympy Fractions in the basis pi, alpha, beta, gamma). No tiling search.
