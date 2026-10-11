# Spheres and ripples on the Lotus seed (DICTO, 2026-10-11)

DICTO's classical parallels to the resin method, tested on the Lotus seed (DICTO Icosa-13; its 113-piece division:
13 icosahedra, 20 FUJI, 60 AXE, 20 CLEO). Scripts in `scripts/`, run on dicto-node.

## 1. Golden-ladder spheres (`spheres2.py`, data `lotus-spheres.json`)
Spheres placed where there is most room, with all 120 icosahedral copies, each level φ times smaller.

| Level | Radius | Spheres | Centres in |
|---|---|---|---|
| 0 | 0.245808 | 20 | one per FUJI |
| 1 | 0.151918 | 80 | one per AXE (60) and CLEO (20) |
| 2 | 0.093890 | 470 | AXE 210, FUJI 240, CLEO 20 |
| 3 | 0.058027 | 770 | AXE 450, FUJI 240, CLEO 80 |

The first two levels find the 100 gap pieces one for one. Not yet tangent; 50 of the 80 level-1 spheres overhang a cut.

## 2. Round ripples (trilateration)
Every one of the 92 gap-piece corners lies on ripples from at least 3 of the 13 icosahedron centres, using 10 radii
whose squares are all (a + b√5)/8: (5−√5)/8, (5+√5)/8, (13+√5)/8, (9+3√5)/8, (17+5√5)/8, (25+5√5)/8, (21+7√5)/8,
(21+9√5)/8, (29+9√5)/8, (33+13√5)/8. (Radii read off the corners, so a fit, not yet a prediction.)

## 3. Icosahedral ripples (`ripples_ico.py`, `ripples_fwd.py`, `ripples_mult.py`, `ripples_extra.py`)
DICTO's idea: ripples shaped as icosahedra, sizes r_in·φ^k. Flat faces make every crossing exact (planes meeting).
- All 92 corners lie on ≥ 3 independent ripple faces, in both orientations (parallel, and every ripple turned 36°).
- Forward test (parallel, k = −3, −2, 0, 1): 244 planes, 108,450 crossings in the gap, all 92 corners among them.
  The corners are the strongest resonances: 48, 70 or 81 ripple faces each, from 12–13 centres. Only 519 points
  reach ≥ 48: the 92 corners, 303 points on icosahedron edges, 12 icosahedron corners, one point inside each CLEO
  (barycentric ((7−3√5)/4, (√5−1)/4 ×3)) and 92 inside the AXEs, at golden points.
- Every ripple turned 36° (`ripples_fwd2.py`): resonance lost (corners on only 3, 6 or 20 faces; 10.27 million crossings).

## Next
Per-ripple independent turns (DICTO: "the axes can rotate"); whether the inner resonance points match the sphere
centres; tangent spheres and their power-diagram cells against the resin cuts.
