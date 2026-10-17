# Octet truss from the OCD pieces — DICTO 2026-10-18

DICTO · dictospheres.com

**Ask (DICTO):** "try and construct an octet truss system from pieces available — please save every step to study".
Pieces available: the OCD (Ogdoecontahedron), the 6 caps of its octahedron (studies/2026-10-18-ocd-octahedron-caps), regular tetrahedra, the golden key on the joint hexagons.
All numbers a + b√5 exact (Fraction pairs, `scripts/q5.py`) unless marked float.

## Step log
### Step 1 — the OCD and its octahedron, exact (`step1_ocd_in_octahedron.py` → `data/step1-ocd-exact.json`)
- OCD taken exactly from the polar-dharma study (102 corners, 80 faces, 20 hexagons).
- The 8 joint hexagons lie exactly on the octahedron |x|+|y|+|z| = R, **R = 2φ/3** (edge 2√2φ/3 = 1.5255); every corner is inside or on it (48 on it = 8 × 6).

### Step 2 — the octet frame, exact (`step2_octet_frame.py` → `data/step2-octet-frame.json`)
- Octahedra on the fcc lattice R(1,1,0)-type; tetrahedra T+ = conv(Re_x, Re_y, Re_z, R(1,1,1)) and T− = −T+.
- Exact: octahedron (64+32√5)/81 + 2 × tetrahedron (16+8√5)/81 = cell (32+16√5)/27. ✓
- Exact: every face of T+ lies on an octahedron face of sign class +1 (the (1,1,1) class), every face of T− on class −1. So **each OCD meets 4 T+ on one tetrahedral set of joint hexagons and 4 T− on the other** — exactly the bump/dent split.
- Exact OCD volume (−1000 + 1240√5)/1539 = 1.151868 (68.83% of the octahedron). Shell (2216 − 632√5)/1539; **each cap (1108 − 316√5)/4617 = 0.086940** (corrects the sampled 0.0865 of the caps study).
- Float check: 200 000 random points, each in exactly one of OCD / shell / T+ / T− (0 gaps, 0 overlaps).
- **So the octet set already works with plain pieces: 1 OCD + 6 caps + T+ + T−** (per lattice cell: 1 + 6 + 1 + 1).

### Step 3 — candidate key: the golden envelope's own corner (`step3_key_candidate.py` → `data/step3-key-candidate.json`) — AWAITING DICTO
- The OCD's golden envelope (RT, same frame) pokes through each joint plane as a small tetrahedron: its 3-fold corner (|x|+|y|+|z| = √5 − 1 = 2/φ) over 3 RT corners lying exactly on the plane.
- Exact: those 3 base corners lie **on the octahedron's edges** (base triangle inscribed in the face, so it covers the hexagon and part of the 3 caps); the key lies inside T+; volume (−44 + 20√5)/81 = 0.008906; height 0.0909.
- Use: bump on the 4 class −1 faces into T−, matching dent in T+ (or the reverse). Not adopted: the key choice is DICTO's (this one vs the earlier 20.9° hexagon key).
- 10-18 DICTO aside (outside this step): five-lobed patterns round the 12 five-fold corners → "Penrose prisms" to link OCDs. See README of the next study when started.
