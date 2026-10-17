# Octet truss from the OCD pieces — DICTO 2026-10-18

DICTO · dictospheres.com

**Ask (DICTO):** "try and construct an octet truss system from pieces available — please save every step to study".
Pieces available: the OCD (Ogdoecontahedron), the 6 caps of its octahedron (studies/2026-10-18-ocd-octahedron-caps), regular tetrahedra, the golden key on the joint hexagons.
All numbers a + b√5 exact (Fraction pairs, `scripts/q5.py`) unless marked float.

## Stages at a glance (10-18; details in the step log below)
| Stage | Steps | Result |
|---|---|---|
| 1. Octet frame + keyed kit | 1–5 | OCD in the octahedron |x|+|y|+|z| ≤ 2φ/3; keyed kit (keyed OCD, cap, dented tetrahedron L/R) fills space exactly |
| 2. Middle pieces + Penrose | 6–17 | facing five-fold stars; middle piece; thick Penrose rhombus core (exact); full kit exact; sphericity scores; merges rejected |
| Fable review | ba28bd0, `fable-review/` | both kits PROVED EXACTLY 100%; corrections: tetrahedra chiral in both kits, step-12 reflex angles |
| 3. Keyless + three cores | 18–20 | DICTO drops the keys; flanking Penrose cores (mirror pair); keyless kit on the 3D page |
| 4. Toward a minimal golden kit | 21–22 | envelopes fill exactly 10/φ⁶; **envelope kit: golden envelope + 6 outer corners + L/R dented tetrahedra (4 shapes)** |
| App | `src/app` on research 94eb7d2 | two networks in the Icosahedral Octet world (not on master yet; to update to the keyless kit) |

Pages: 3D pieces claude.ai/artifact/Fx4WGWm6udtt6EEPKsaMua · stars AsT1sqmf4pkdGj9v6K4ZZh · middle piece Pqp34sp8zVkw7Y2kS1WLgM · slices N76HnetzU4pJpdEGETNEHD · Penrose cut 41opNbdPpZFeMa6crGpFBz.
Related: bcc golden kit `studies/2026-10-18-bcc-golden-kit` (steps 1–5: slabs, keys, G′ = 93√5/2 − 831/8 exactly, no Penrose link in bcc).

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

### Step 15 — DICTO 10-18: "1, keep the central prism trimmed"
- The middle piece splits into a **Penrose core** (central thick-rhombus prism ∩ middle piece) and the rest of the middle piece.
- Exact (`step15_penrose_core.py` → `data/step15-core.json`): core = prism ∩ H − OCD1 − OCD2; no key enters it (exact). **Penrose core (−36734 + 16658√5)/50787 = 0.010129** (13.8% of the middle piece); **rest of the middle piece (47668/50787 − 99416√5/253935) = 0.063162**. The two OCD cuts are equal (symmetric through m).
- Meshes (`step15_mesh.py` on dicto-node → `data/step15-meshes.json`): core and rest are **each one solid**; volumes equal the exact values.
- 3D page updated (same link, claude.ai/artifact/Fx4WGWm6udtt6EEPKsaMua): buttons for the Penrose core and the rest; the assembly shows each middle piece as core + rest.
- **Set now: keyed OCD, notched cap, Penrose core, middle rest, left and right tetrahedra** (6 shapes; 5 counting the mirror pair as one).

### Step 16 — how much space each piece takes (`step16_space_shares.py` → `data/step16-shares.json`, exact)
- DICTO 10-18: "how much space do these octet arrangements cover together with ocds". The set fills space completely (shares sum to exactly 1).
- Exact shares of the cell: **bare OCDs 45.886%** ((1025/114 − 145√5/38)); keys 2.838% (94/3 − 14√5); **notched caps 13.880% (exactly 2√5 − 13/3)**; Penrose cores 2.421%; middle rests 15.097%; tetrahedra 19.877%.
- So OCD + keys = 48.72%; everything else (caps, middle pieces, tetrahedra) 51.28%.
- For comparison, OCDs joined hexagon to hexagon in the bcc packing fill 77.43%: the octet spreads the OCDs out (octahedron centres on fcc, edge 2√2φ/3) and the extra space is what the caps, middle pieces and tetrahedra take.

### Step 17 — DICTO 10-18: "merge caps with middle rests" (after the comparison: octet = finished kit, not a denser packing; aim now fewer, chunkier pieces)
- A middle rest is shared by 2 octahedra and touches caps at both ends of its edge, so a whole rest can't go to one cap without breaking the symmetry (more shapes). Instead (Claude's construction): cut each rest in half by the plane through m perpendicular to its edge (the halves are congruent, swapped by the inversion through m), and merge round each octet vertex: **vertex piece = the 6 caps meeting at a lattice vertex + the 12 half-rests on the 12 edges there.** One vertex per cell, so the set becomes: keyed OCD, vertex piece, Penrose core, left + right tetrahedra.
- Chunkiness scored by sphericity ψ = π^(1/3)(6V)^(2/3)/A (1 = ball; cube 0.806, regular tetrahedron 0.671).
- Result (`step17_vertex_piece.py` on dicto-node → `data/step17-vertex.json`): **vertex piece volume 0.727404 (= 6 caps + 6 rests ✓) but it falls into 2 separate solids and is very spiky: ψ = 0.213.** Not a usable single piece; not chunkier.
- Alternative tried (`step17b_tet_plus_rests.py` → `data/step17b-tet-rests.json`): cut each rest by the mirror plane through its edge and axis, merge each tetrahedron with its 6 half-rests: **one solid, volume 0.438972 ✓, but ψ = 0.357**, less chunky than the tetrahedron alone (0.460).
- Sphericity of the current pieces: bare OCD 0.979; **keyed OCD 0.696** (the overhanging key plates cost a lot); **Penrose core 0.752** (the chunkiest new piece); notched cap 0.494; notched tetrahedron 0.460; middle rest 0.385.
- **Reading: the middle rests are thin collars round the stars; merging them into anything makes it less chunky.** The thin pieces come from the octet's spacing itself, not from how the pieces are grouped. Keep the step-15 set; do not merge.

## App stage — DICTO 10-18: "lets build it in the app"
Decisions (DICTO, 10-18, asked before any app edit):
- Place: the existing **DICTO Icosahedral Octet** world (#21, Admiral Caps), as new networks beside Caps / All-icosahedral / Frog Chorus / Pyrochlore / Lotus Jewel (same family, no crossover; same controls).
- Both kits, **two rows**: **"Octet with OCD"** (keyed kit, step 5: keyed OCD, cap, dented tetrahedron) and **"Octet with OCD and Penrose cores"** (full kit, step 15: + Penrose core, middle rest; notched caps; left/right tetrahedra). Name of the full kit chosen by DICTO.
- Colours as on the 3D study page: OCD gold, caps blue, middle rest red, Penrose core purple, left tetrahedra green, right teal.

## Fable review (ba28bd0, `fable-review/REPORT.md`) — verdict and corrections
- **Both kits PROVED EXACTLY to fill space 100%** (own exact Q(√5) engine, no symmetry shortcuts), backed by 4 M + 2 M sampled points (every point in exactly one piece).
- **Correction to steps 5, 9, 10:** the dented tetrahedron is **chiral** (12 proper symmetries, no improper one): the key's base corners sit at the golden-section points (φ:1) of the octahedron edges, so the key is twisted. **The keyed kit also has a left and a right tetrahedron** (4 shapes; 3 counting the mirror pair as one). In the app T− must be the point reflection of T+ (it is: `put(..., invert)`).
- **Correction to step 12:** angle lists for non-convex faces reported reflex angles θ as 360 − θ. The middle piece's "quadrilaterals with Penrose 36°/144°" are darts with a reflex 216°; "hexagon thirds (30/120/30)" are quads 30/60/30 with a reflex 240°; the notched tetrahedron's counts need recounting. Triangle claims stand (key faces exactly half golden rhombi).
- Extra exact facts: an M's octahedron share splits 70:30 between the two caps on its edge; H is an oblique pentagonal antiprism with a 45° exact shear; the middle rest is a ring (genus 1) round the core.
- Fable's tested improvements (space filling survives): (1) drop the keys in the full kit → OCD ψ 0.979, M 0.579, tetrahedron 0.517; (2) keyed kit with the key cut to the hexagonal plug (3/4 of the key) → keyed OCD ψ 0.948; (3) keep M whole unless the Penrose motif is wanted.

### Step 18 — DICTO 10-18: "I'll go with suggestion of dropping the keys" (Fable improvement 1)
- **Full kit without keys:** OCD (plain, ψ 0.979), notched cap, middle piece M₀ = H − both OCDs (or Penrose core + rest), left/right tetrahedra notched by the Ms only. Space filling survives (Fable: exact by construction, sampled 4 M points). Fable's ψ: middle 0.579, tetrahedron 0.517, rest 0.497.
- Re-run of the step-14 fit with no keys (`step18_no_keys_flanks.py` → `data/step18-fit.json`): the **flanking Penrose prisms are now clear** (nothing to hit); like the central one they are closed by both OCDs at every column, but ≈22% of their columns (central ≈12%) leave the hull, so they would be trimmed to it as the central core is. Three prisms together ≈0.021.
- App (research branch 94eb7d2) still shows keys in "Octet with OCD and Penrose cores"; to update to the keyless kit when app work resumes. The keyed kit row ("Octet with OCD") is unchanged unless DICTO says.

### Step 19 — the flanking Penrose cores, keyless kit (`step19_flank_cores.py` → `data/step19-flank-cores.json` exact; `step19_mesh.py` on dicto-node → `data/step19-mesh.json`)
- DICTO 10-18: "compute the flanking cores and check them".
- Exact: keyless middle piece **M₀ = (310 + 26√5)/4617 = 0.079735**. Cores: central (−36734 + 16658√5)/50787 = 0.010129 (unchanged, no key ever entered it); **each flanking core 4114/1539 − 9182√5/7695 = 0.004993**, the two exactly equal. The three prisms are pairwise interior-disjoint inside H (exact 0). Three cores = 25.2% of M₀; **rest = −231380/50787 + 524152√5/253935 = 0.059620**.
- Meshes: every core and the rest are **single solids**; volumes equal the exact ones. Sphericity: central core 0.752, flanking core 0.729, rest 0.377 (M₀ whole 0.579).
- **The two flanking cores are mirror images** (a left and a right): no rotation takes one onto the other; the mirror of one does.
- So with flanking cores the full keyless kit is: OCD, notched cap, central core, left + right flanking core, rest, left + right tetrahedron (7 shapes; 5 counting mirror pairs as one).

### Step 20 — the keyless kit with three cores on the 3D page (`step20_keyless_meshes.py` on dicto-node → `data/step20-keyless-meshes.json`)
- Meshes: plain OCD 1.151868, notched cap 0.058072 (unchanged: keys never entered the octahedron), **keyless notched tetrahedron 0.265776**, central core 0.010129, flanking cores 0.004993 each, rest 0.059620. Per cell 1.151868 + 6×0.058072 + 6×0.079735 + 2×0.265776 = 2.510263 = cell ✓.
- Page (same link): button "Keyless kit, 3 Penrose cores" (assembly round one OCD: 6 caps, 12 middle pieces each as central core + 2 flanking cores + rest, 4 left + 4 right tetrahedra), and single-piece buttons for the flanking cores (left, right), the rest and the keyless tetrahedron.

## Stage 3 — toward a minimal golden kit (DICTO 10-18: "develop the octet toward a minimal golden kit")
### Step 21 — the golden envelopes in the octet (`step21_envelopes_in_octet.py` → `data/step21-envelopes.json`, exact)
- Each OCD's golden envelope (RT, (−320 + 160√5)/27) placed in the octet: **neighbouring envelopes never overlap** (exact 0).
- **RT = (its part in the octahedron) + exactly its 8 keys** in the 8 tetrahedra round it: RT outside the octahedron = (−352 + 160√5)/81 = 8 × key.
- **The envelopes fill exactly 90 − 40√5 = 10/φ⁶ = 55.728% of space.**
- What is left: in each octahedron, the corners outside the envelope ((224/27 − 32√5/9) per octahedron, 6 corner pieces), and each tetrahedron minus the 4 envelope corners (64/27 − 8√5/9, the step-5 dented tetrahedron, chiral).
- So a kit **"golden envelope + 6 outer corners + left/right dented tetrahedra"** fills space with the golden envelope (a golden zonohedron, buildable from golden rhombohedra) as the big piece; the OCD sits inside it. Next: the outer corners and dented tetrahedra — can they be cut into golden/Penrose pieces?

### Step 22 — what the envelopes leave (`step22_complement.py` on dicto-node → `data/step22-complement.json`)
- The space outside the envelopes is **one connected web** (round every lattice vertex, tetrahedron and edge it runs on), so it has to be cut; the octet frame gives the cuts.
- **The octahedron minus its envelope falls into exactly 6 separate, congruent pieces**, one per octahedron corner — no cone cuts needed (cone cuts would leave two 0.00029 slivers each). Each **outer corner = 112/81 − 16√5/27 = 0.057639** (exact from step 21: (224/27 − 32√5/9)/6), non-convex, ψ 0.456.
- Each tetrahedron minus its 4 envelope corners = the step-5 dented tetrahedron (64/27 − 8√5/9 = 0.382754), chiral (left/right), ψ 0.620.
- The envelope (RT) ψ 0.961.
- **Envelope kit: golden envelope (OCD inside) + 6 outer corners + left/right dented tetrahedra — 4 shapes (3 counting the mirror pair), and 10/φ⁶ = 55.73% of space is in the golden piece.** Fills space exactly (frame + RT = octahedron part + 8 keys, step 21). The fewest shapes of any kit so far; Penrose does not appear in it (the Penrose cores straddle the envelope surfaces).

### Step 23 — the envelope kit in 3D (`step23_envelope_meshes.py` on dicto-node → `data/step23-envelope-meshes.json`)
- Meshes: envelope 1.398921, outer corner 0.057639, dented tetrahedron 0.382754, OCD 1.151868 (all = the exact values).
- 3D page (same link): "Envelope kit (4 shapes)" assembly round one OCD — glass golden envelope with the gold OCD inside, 6 outer corners (blue), 4 left + 4 right dented tetrahedra; buttons for the envelope and the outer corner alone.

### Step 24 — cutting the outer corners (DICTO 10-18: "try cutting the outer corners into golden pieces"; `step24_outer_corner_cut.py`, `step24_mesh.py` (node), `step24b_wedge.py`, `step24c_tetra.py`, `step24d_vertex_cubocta.py`)
- The +z axis is a 2-fold axis of the envelope through a face centre; that face's plane z = 2/3 cuts off a square pyramid at the octahedron's corner lying wholly outside the envelope. **Exact: the pyramid is the octahedron's corner scaled by φ⁻²** (pyramid "radius" (√5 − 1)/3 = R/φ²), volume (−32 + 16√5)/81 = 0.046631 — **80.9% of the outer corner**.
- The rest of the outer corner is **two congruent wedges** (0.005504 each, non-convex), each = two convex tetrahedra: A (−116 + 52√5)/81 (angles 90°, 45°, 120°, one half-golden 31.72°; mostly not golden) and B 188/81 − 28√5/27 (one face an **exact half golden rhombus** 31.72/31.72/116.57, two faces with the golden 63.43° angle).
- **Vertex cuboctahedron (Claude's observation, exact):** at each lattice vertex the 6 φ⁻² pyramids of the octahedra and the φ⁻² corners of the 8 tetrahedra make a **cuboctahedron scaled by φ⁻²** (the octet's vertex figure, edge R√2/φ² = 0.582688). Exact: the small tetrahedron corners lie outside every envelope and meet no key except at points (the keys' base corners sit exactly at the golden-section points, 6 of them on its corners). **Its volume (−320 + 160√5)/81 is exactly 1/3 of the envelope's**, so it fills (10/φ⁶)/3 = 18.576% of space.
- So the envelope kit refines to: **golden envelope (55.73%) + φ⁻² vertex cuboctahedron (18.58%) + 12 wedges per cell (2.63%) + left/right tetrahedra with 4 key dents and 4 corners cut off (256/81 − 104√5/81 = 0.289494 each)**. 74.3% of space is in the two golden-scaled pieces.

### Step 25 — the refined envelope kit in 3D (`step25_refined_meshes.py` on dicto-node → `data/step25-refined-meshes.json`)
- Meshes: φ⁻² vertex cuboctahedron 0.466307, wedges 0.005504 each, cut-down tetrahedron 0.289493 (= the exact values of step 24).
- 3D page (same link): "Refined envelope kit" — glass envelope with the OCD, the 6 vertex cuboctahedra at its octahedron's corners (orange; each is shared by the 6 octahedra meeting there), 12 wedges (red), 4 left + 4 right cut-down tetrahedra; single-piece buttons for the cuboctahedron, a wedge and the cut-down tetrahedron.
