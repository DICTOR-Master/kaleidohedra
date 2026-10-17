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

### Step 7 — the shared middle piece, first look (float) (`step7_middle_piece.py` → `data/step7-middle.json`; `draw_step7.py` → `renders/step7-middle.html`)
- Candidate M = hull(star 1 + star 2) minus the two OCDs; inversion-symmetric through m (checked). Volume ≈ 0.0796 (hull 0.1104, 28% of it inside the OCDs).
- It straddles the octet pieces: ≈36% in the two caps, ≈64% in the two tetrahedra on the shared edge (half each).
- Clash: 4 step-5 keys (2 per OCD, on the faces beside the shared edge) reach into it, ≈8% of its volume.
- Section drawing in the mirror plane x = 0: claude.ai/artifact/Pqp34sp8zVkw7Y2kS1WLgM
- Open for DICTO: middle piece swallows the key tips or is trimmed round them? Cut from caps and tetrahedra (notching them) or replace parts of them?

### Step 8 — DICTO 10-18: "trimmed around and leave notches"
- Middle piece M = hull(two stars) minus both OCDs minus the keys (trimmed round the 4 key tips). Caps and tetrahedra keep their shape but get notches where M takes their space.
- One M on every octahedron edge (each OCD has 12 five-fold corners, one facing each edge; per cell 6 Ms).
- 2D drawing (`draw_step8.py` → `renders/step8-trimmed.html`, claude.ai/artifact/N76HnetzU4pJpdEGETNEHD): slices across the shared edge at m and 0.06, 0.12, 0.18 along it; red middle piece over blue caps / green tetrahedra = notches; purple keys stay with their OCDs. Float.

### Step 9 — left and right tetrahedra? (`step9_tet_handedness.py` → `data/step9-handedness.json`, float)
- T− is T+ turned inside out through the OCD centre, so they are the same piece exactly when T+ (with its dents and notches) has a mirror symmetry.
- With the 4 key dents only (step 5 set): all 6 tetrahedron mirrors hold → **T+ and T− are the same piece**; the step-5 keyed octet needs just 3 shapes.
- With the 6 middle-piece notches as well (step 8 set): no mirror holds (the stars' 36° twist makes the notches twist), only the 3-fold turns → **T+ and T− are mirror images**, a left and a right tetrahedron.
- Step 8 check done (`data/step8-trimmed.json`, 300 000 samples in one cell): Ms on different edges never overlap (0); every point assigned exactly once (0 unassigned, 0 twice); M is one piece (one big component, the rest single-voxel specks). Per cell: keyed OCD 1.2214, 6 M 0.4417 (one ≈0.0736), 6 notched caps 0.3496 (one ≈0.0583), 2 notched tetrahedra 0.4975 (one ≈0.2488).

### Step 10 — the pieces as solid meshes and a 3D page (`step10_piece_meshes.py` on dicto-node with manifold3d → `data/step10-meshes.json`; `draw_step10.py` + `step10_template.html` → `renders/step10-pieces.html`)
- Mesh volumes: keyed OCD 1.223113 and dented tetrahedron 0.382754 (both = the exact step-5 values), unnotched cap 0.086940 (= exact step 2); middle piece 0.073291, notched cap 0.058072, notched tetrahedron 0.249486 — agree with the step-8 sampling.
- All pieces are single solids without holes (the notched cap shows 4 zero-volume boolean slivers, ignored). Per cell 1.2231 + 6×0.0581 + 6×0.0733 + 2×0.2495 = 2.5102 ≈ cell 2.5103.
- **Final set with middle pieces: keyed OCD, notched cap, middle piece, left tetrahedron, right tetrahedron** (5 shapes; 4 if a mirror-image pair counts as one).
- Page: claude.ai/artifact/Fx4WGWm6udtt6EEPKsaMua (gallery + exploded assembly round one OCD: 1 OCD, 6 caps, 12 middle pieces, 4 left + 4 right tetrahedra).

## Development stage 2 — exact pieces (DICTO 10-18: "next development stage")
### Step 11 — exact volumes of the trimmed set (`exactpoly.py`, `step11_exact_pieces.py` → `data/step11-exact.json`)
- Exact convex polytopes in Q(√5) (`exactpoly.py`: float only picks which planes meet; every corner solved and checked exactly).
- Middle piece by convex parts: vol M = vol H − 2 vol(H∩OCD) − Σ vol(H∩key); H = hull of the two stars.
- Exact: **hull of the two facing stars = 4√5/81**; H∩OCD = (−155 + 101√5)/4617; each of the 4 key tips in H = −1/27 + 7√5/405.
- Exact pieces: **middle piece 994/4617 − 1466√5/23085 = 0.073291**; **notched cap (32 − 8√5)/243 = 0.058072**; **notched tetrahedron 166/81 − 326√5/405 = 0.249486**; keyed OCD (−7688 + 4280√5)/1539 (step 5).
- Exact: keyed OCD + 6 caps + 6 middle pieces + 2 tetrahedra = cell (32 + 16√5)/27. ✓  Mesh volumes (step 10) agree to 1e-16.
- Shares used (by symmetry): each M meets each of its 2 octahedra in (250 − 82√5)/4617 and each of its 2 tetrahedra equally (inversion through m); the 6 caps are equal (Th), the 6 edges of a tetrahedron equivalent (its 12 turns).

### Step 12 — every face, and which are golden / Penrose (`step12_exact_faces.py` → `data/step12-faces.json`, log `data/step12.log`; `step12b_key_in_hull_planes.py`)
- Faces from the step-10 meshes, each matched to its exact source plane(s); corners snapped to exact 3-plane points; exact squared edges and exact cos² name the angles (golden 63.43/116.57, Penrose 36/72/108/144, 60/90/120).
- **Keyed OCD:** 60 kites, 12 free hexagons, and **24 key faces that are exact half golden rhombi** (31.72°, 31.72°, 116.57°); the key bases overhang the hexagons (undersides lie on the joint planes, against the caps).
- **Middle piece:** **no golden or Penrose rhombus.** Faces: the 10 kites of the two stars, hexagon thirds (30/120/30), key faces cut to quarter golden rhombi (right triangles 90/31.72/58.28), 45-45-90 and 69.3/41.4 triangles, and **4 quadrilaterals carrying the Penrose angles 36° and 144°** (with 90° and 18°). Edge ratios include φ (0.3505/0.2166, 0.6667/0.4120), √3 (0.4120/0.2379) and √2.
- **Notched cap:** no golden or Penrose angles at all.
- **Notched tetrahedron:** golden (8+8) and Penrose (7+7) angles occur in 15 quadrilaterals, none a full rhombus.
- Exact (12b): each of the 4 keys beside a shared edge has one face lying exactly in a facing-star hull plane (of a neighbouring edge's hull).
- **So the middle piece is not made of Penrose rhombi;** Penrose angles appear only in 4 of its faces. A true Penrose-prism link would need a different cut (open, for DICTO).
- Caveat: some mesh loops are degenerate (0-gons, a few "?" where a corner did not snap); they are boolean slivers, not real faces.

### Step 13 — a Penrose cut between the facing stars, in 2D (`step13_penrose_cut.py` → `data/step13-penrose.json`; `draw_step13.py` → `renders/step13-penrose.html`) — PROPOSAL (Claude), awaiting DICTO
- DICTO 10-18: "1, draw the Penrose cut in 2D". Seen down the five-fold axis (projection exact in Q(√5)).
- Exact: c1 → c2 is the long diagonal of a **thick Penrose rhombus** (72° at c1, c2; 108° at the sides), edge = tip radius ÷ φ = 0.2166; its edges run **along the stars' own spokes**.
- Exact: at each side corner a **thick Penrose rhombus one φ-step smaller** (edge 0.1339, 108° at the side corner) reaches one tip of each star.
- So three thick Penrose rhombi in φ-scaled sizes join the two stars tip to tip, symmetric about m. Each would become a Penrose prism along the axis, closed by the two OCD surfaces.
- Open: do the prisms fit inside the middle region in 3D (between the OCDs, clear of the keys)? Page: claude.ai/artifact/41opNbdPpZFeMa6crGpFBz

### Step 14 — 3D fit of the Penrose prisms (`step14_penrose_fit.py` → `data/step14-fit.json`, float sampling, 4000 columns per prism)
- Each prism = rhombus footprint run along the five-fold axis from OCD 1's surface to OCD 2's surface.
- **Central thick prism:** closed by both OCDs at every column ✓; **clear of all keys** ✓; column height 0.198–0.273; but **12% of its columns poke out of the star hull** (beyond the middle region, into caps/tetrahedra). Volume ≈ 0.0104.
- **Two flanking prisms:** closed at both ends ✓, but **every column runs into a key** ✗, and ≈22% poke out of the hull. Height 0.254–0.412. Volume ≈ 0.0052 each.
- Together the three fill ≈28% of the middle piece (0.0209 of 0.0733).
- Reading: the central Penrose prism is a real candidate link (needs either clipping to the hull or a slightly larger middle region); the flanking prisms clash with the chosen tetrahedral keys.
