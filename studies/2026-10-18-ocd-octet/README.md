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

### Step 3 — the key: the golden envelope's own corner (`step3_key_candidate.py` → `data/step3-key-candidate.json`) — CHOSEN by DICTO 10-18 ("tetrahedra")
- The OCD's golden envelope (RT, same frame) pokes through each joint plane as a small tetrahedron: its 3-fold corner (|x|+|y|+|z| = √5 − 1 = 2/φ) over 3 RT corners lying exactly on the plane.
- Exact: those 3 base corners lie **on the octahedron's edges** (base triangle inscribed in the face, so it covers the hexagon and part of the 3 caps); the key lies inside T+; volume (−44 + 20√5)/81 = 0.008906; height 0.0909.
- Use: bump on the 4 class −1 faces into T−, matching dent in T+ (or the reverse). DICTO chose this tetrahedral key over the earlier 20.9° hexagon key (10-18).
- 10-18 DICTO aside (outside this step): five-lobed patterns round the 12 five-fold corners → "Penrose prisms" to link OCDs. See README of the next study when started.
  - First look (float, 10-18): in the octet, each five-fold corner faces an antiparallel five-fold corner of the OCD across the shared octahedron edge (centre offset R(0,1,1)), 0.3629 apart: 0.0943 along the axis, 0.3505 sideways. The five-kite star round a corner also has radius 0.3505 → the facing corner seems to sit right over a star tip. To prove exactly; 2D drawing down the axis first (picture-first rule).

### Step 4 — the two facing five-fold stars (`step4_five_fold_stars.py` → `data/step4-stars.json`; `draw_step4.py` → `renders/step4-stars.html`)
- DICTO 10-18: "could five lobed patterns on ocd surface be built into penrose prisms to connect with each other"; picture first.
- Each five-fold corner c1 faces the neighbour OCD's corner c2 = R(0,1,1) − c1, pointing straight back (across the shared octahedron edge).
- Exact: the sideways offset of c2 equals the star's tip radius 0.350487. Exact: c2 is NOT over a gold tip (my float guess was wrong) — it sits at 180°, in line with an inner corner, between two tips. Along the axis c2 is 0.0943 nearer.
- The stars are turned a half turn (= 36° for a five-fold star) against each other. Star: 5 kites, inner corners 0.0559 and tips 0.1281 below the centre.
- Page: claude.ai/artifact/AsT1sqmf4pkdGj9v6K4ZZh. Next: DICTO's read of the drawing before any Penrose-prism search.

### Step 5 — the keyed octet (`step5_keyed_octet.py` → `data/step5-keyed-octet.json`) — DONE
- The key's base reaches the octahedron edges, so a dent inside the OCD would also cut the caps. So all 8 keys go out as bumps (OCD + 8 envelope corners = one piece) and both tetrahedra take 4 dents each.
- Exact: the 4 keys entering each tetrahedron (T+ and T−) stay inside their own face pyramids, so they never overlap. ✓
- Exact pieces: **OCD + 8 keys (−7688 + 4280√5)/1539 = 1.223113**; **cap (1108 − 316√5)/4617 = 0.086940** (×6); **tetrahedron with 4 dents 64/27 − 8√5/9 = 0.382754** (×2: T+ and T−). Sum = cell (32 + 16√5)/27 exactly. ✓
- Float: 200 000 points, every one in exactly one piece (0 gaps, 0 overlaps). ✓
- **Result: a keyed octet truss from 3 shapes: the keyed OCD, the cap, the dented tetrahedron (in two orientations).**
- Open: are T+ and T− with dents the same shape or mirror images? Renders of the pieces; Penrose-prism links (step 4) after DICTO reads the drawing.

### Step 6 — DICTO 10-18 on the stars drawing: "the stars look possible to bring into alignment"
- Fixed by the lattice (all OCDs are translates): the sideways offset (= tip radius), the 36° turn, the 0.094 axial step. So alignment has to come from a joining piece.
- Options put to DICTO: (1) a connector over the facing lobes, (2) a slanted Penrose prism from c1 to c2 (≈75° from the axis, nearly flat), (3) a shared middle piece on the half-turn centre between c1 and c2.
- **DICTO chose (3), a shared middle piece.**
- Note: the half-turn centre is m = (c1 + c2)/2 = R(0,1,1)/2, the **midpoint of the octahedron edge the two OCDs share**; m is a centre of inversion (each OCD and star maps to the other). In the octet, 2 octahedra and 2 tetrahedra meet round that edge.
