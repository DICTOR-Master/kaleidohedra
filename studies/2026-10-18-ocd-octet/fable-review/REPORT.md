# Fable review of the OCD octet truss design — 2026-10-18

DICTO · dictospheres.com — independent verification and critical review (Claude Fable 5.1) of `studies/2026-10-18-ocd-octet` (steps 1–17 + app stage). Research branch only.

Scripts: `scripts/fable_exact.py` (own exact polytope engine in Q(√5), run on the Pi, 37 s), `scripts/fable_node.py` (dicto-node: dense sampling, manifold3d meshes, handedness, improvement variants), `scripts/fable_misc.py` (side checks). Data: `data/fable-exact-checks.json`, `data/fable-node.json`, `data/fable-misc.json`.

## 1. Verdict on 100 % space filling

| Kit | Verdict | Evidence |
|---|---|---|
| **Keyed kit** (step 5: keyed OCD, cap ×6, dented tetrahedra T+ and T−) | **PROVED EXACTLY** | §1.1; sampling 2,000,000 uniform + 2,000,000 near-face points, 0 uncovered, 0 double |
| **Full kit** (step 15: keyed OCD, notched cap ×6, middle piece ×6 = Penrose core + rest, notched T+ and T−) | **PROVED EXACTLY** | §1.2; sampling 2,000,000 uniform + 2,000,000 near-face points, 0 uncovered, 0 double (same with core + rest split: 0 uncovered, 0 double) |

What "exact" means here. All geometry is in Q(√5) (pairs of Fractions). Corners of every convex body are found by solving all plane triples; a float pre-screen may discard a triple only when its float solution violates some plane by more than 1e-7 (ill-conditioned triples are always solved exactly), and every kept corner is checked exactly against every plane. Volumes come from exact corners; each qhull facet is re-proved exactly to be a supporting plane. Two convex bodies are interior-disjoint iff their exact intersection has exact volume 0. The only non-exact ingredient is the 1e-7 pre-screen on double-precision numbers of size ~1, sound by many orders of magnitude. The symmetry shortcuts of step 11 were **not** used: every volume below was computed directly.

### 1.1 Keyed kit — proof structure (all steps verified exactly)
1. **Frame tiles space.** Octahedra |x|+|y|+|z| ≤ R (R = 2φ/3) on the fcc lattice, T+ = conv(Re_x, Re_y, Re_z, R(1,1,1)), T− = −T+. 75 frame bodies round the origin, all pairs interior-disjoint (0 pairs with positive overlap); octa + T+ + T− = cell (32+16√5)/27 exactly. Closed pieces, interior-disjoint, density exactly 1 ⇒ they cover space (the uncovered set is open and of measure zero, hence empty).
2. **Octahedron = OCD + 6 caps.** The six corner cones {x_k ≥ |x_i|, |x_j|} partition R³ (largest coordinate decides); each cone ∩ octahedron has volume (32+16√5)/243, the six sum to the octahedron; OCD ⊂ octahedron (102 corners inside, 48 on it, the 8 joint hexagons on the 8 faces); the six caps are exactly equal, (1108−316√5)/4617 each, and caps + OCD = octahedron.
3. **Keys move from the tetrahedra to the OCD.** Key = conv(RT 3-fold corner, 3 RT corners on the joint plane); exactly the step-3 key; volume (−44+20√5)/81. The key lies beyond the joint plane (zero overlap with the octahedron) and entirely inside the adjacent tetrahedron (every corner satisfies all 4 tetrahedron planes). Each tetrahedron receives exactly 4 keys, each wholly inside it. 104 nearby keys tested pairwise: 0 overlapping pairs; keys vs octahedra: 0.
4. **Bookkeeping.** keyed OCD (−7688+4280√5)/1539 + 6 caps + 2 dented tetrahedra 64/27 − 8√5/9 = cell exactly.

### 1.2 Full kit — additional lemmas (all exact)
Let H be the hull of the two facing five-fold stars at an octahedron edge, M = H − (its two keyed OCDs).
5. **H stays in the four cells round its edge**: vol H = 4√5/81 = Σ over the two octahedra ((5+√5)/243 each) and the two tetrahedra ((−5+5√5)/243 each); no other frame body meets H.
6. **H meets only its own two OCDs and 4 of their keys** (+++ and −++ of OCD 1, +−− and −−− of OCD 2, (−1/27 + 7√5/405) each): every other keyed OCD within reach was tested, zero overlap. So the step-10 definition M = H − keyed₁ − keyed₂ is complete; M = 994/4617 − 1466√5/23085 as claimed.
7. **Middle pieces never overlap**: 84 pairs of nearby hulls tested; **not even the hulls H overlap** (0 pairs), so the Ms are disjoint before any trimming.
8. **Pieces by direct subtraction** (no equal-share assumptions): each of the 6 notched caps = cap − Σ_e [vol(H_e ∩ cone ∩ octa) − vol(H_e ∩ cone ∩ OCD)] = (32−8√5)/243, all six equal; notched T+ = T+ − keys − Σ_e [vol(H_e ∩ T+) − Σ vol(H_e ∩ T+ ∩ key)] = 166/81 − 326√5/405, and notched T− the same volume (computed separately). 6 hulls notch each tetrahedron, 4 each cap.
9. **Core**: the prism cross-section is an exact rhombus with cos 72° = (√5−1)/4 at c1 (thick Penrose rhombus — the naming is correct), edges equal, long diagonal = tip radius; core = prism ∩ H − OCD₁ − OCD₂, no key enters it; core (−36734+16658√5)/50787, rest = M − core.
10. keyed OCD + 6 notched caps + 6 M + notched T+ + notched T− = cell exactly.

### 1.3 Sampling (dicto-node, float, one fundamental cell)
| points | kit | n | in no piece | in exactly one | in two or more |
|---|---|---|---|---|---|
| uniform | keyed kit | 2,000,000 | 0 | 2000000 | 0 |
| uniform | full kit (M whole) | 2,000,000 | 0 | 2000000 | 0 |
| uniform | full kit (core + rest) | 2,000,000 | 0 | 2000000 | 0 |
| uniform | kit B, no keys (I1) | 2,000,000 | 0 | 2000000 | 0 |
| boundary | keyed kit | 2,000,000 | 0 | 2000000 | 0 |
| boundary | full kit (M whole) | 2,000,000 | 0 | 2000000 | 0 |
| boundary | full kit (core + rest) | 2,000,000 | 0 | 2000000 | 0 |
| boundary | kit B, no keys (I1) | 2,000,000 | 0 | 2000000 | 0 |

Uniform points: uniform in the lattice cell. Boundary points: uniform points moved onto a random piece face plane and pushed off it by 10^−6…10^−2 (log-uniform), folded back into the cell. Middle pieces found overlapping each other: 0 (uniform), 0 (boundary).

### 1.4 Solidity (manifold3d meshes, dicto-node)
- bare OCD: 1 solid part(s), genus 0, 0 zero-volume sliver(s)
- keyed OCD: 1 solid part(s), genus 0, 0 zero-volume sliver(s)
- cap (keyed kit): 1 solid part(s), genus 0, 0 zero-volume sliver(s)
- dented tetrahedron (keyed kit): 1 solid part(s), genus 0, 0 zero-volume sliver(s)
- notched cap: 1 solid part(s), genus −4 as a mesh (the 4 zero-volume slivers; the solid part is genus 0), 4 zero-volume sliver(s)
- middle piece M: 1 solid part(s), genus 0, 0 zero-volume sliver(s)
- Penrose core: 1 solid part(s), genus 0, 0 zero-volume sliver(s)
- middle rest: 1 solid part(s), genus 1, 0 zero-volume sliver(s)
- notched tetrahedron: 1 solid part(s), genus 0, 0 zero-volume sliver(s)
- Handedness (mesh): dented tetrahedron chiral = True (smallest improper symmetric difference 0.0226); notched tetrahedron chiral = True (0.0628); T− = point reflection of T+: symmetric difference 0.0e+00 (dented), 3.0e-17 (notched).

## 2. Critical review

**R1 — Step 9 is wrong for the keyed kit: the dented tetrahedron is chiral.** Exact test of all 24 symmetries of the regular tetrahedron on the 4 keys inside T+: the 12 proper maps are symmetries, **none of the 12 improper maps** (6 mirrors, 6 rotoreflections) is. Mesh check: the best improper map leaves a symmetric-difference volume of 0.0226. Cause: the key is a twisted tetrahedron — its base corners split each octahedron edge in the ratio **φ : 1** (exact: (2/3, (√5−1)/3, 0) etc.), not at the midpoints, so the key has C3 but no mirror symmetry. Step 9 compared the *union* of key corner points, which is mirror-symmetric because the two keys on adjacent faces put their base corners at mirror-image golden points of the shared edge. Consequences: (a) the keyed kit also has a **left and a right tetrahedron** (4 shapes; 3 if a mirror pair counts as one) — README steps 5, 9, 10 and the app-stage list ("keyed OCD, cap, dented tetrahedron") need correcting; (b) in the app, T− must be the point reflection of T+ (as the lattice construction gives it), not a rotated copy of the same mesh, or the dents miss the keys. Dented and notched T− are exactly the point reflection of T+ (mesh symmetric difference ~1e-17).

**R2 — Step 12's face-angle lists are unreliable for non-convex faces.** 38 of 210 faces have angle sums ≠ (n−2)·180° (keyed OCD 8/110, middle 8/38, cap 4/14, notched tetrahedron 18/48). These faces are non-convex polygons; the code reports a reflex angle θ as 360° − θ. So: the middle piece's "4 quadrilaterals carrying the Penrose angles 36° and 144°" are darts with corners 18°, 36°, 90° and a **reflex 216°** (144° is not an interior angle); the "hexagon thirds (30/120/30)" are quadrilaterals 30°, 60°, 30° with a reflex 240°; the notched tetrahedron's "15 quadrilaterals with golden (8+8) and Penrose (7+7) angles" must be recounted. Triangle claims stand: the key faces are exactly half golden rhombi (apex cos² = 1/5, cos < 0 → 116.57°; 31.72°, 31.72°).

**R3 — Step 11's symmetry shortcuts are correct, with one nuance.** The two tetrahedron shares of an M are exactly equal (13/243 − 17√5/1215 each), the two octahedron shares too ((250−82√5)/4617 each), but an M's octahedron share splits **unequally between the two caps** at its edge: (−7502+3376√5)/4617 = 0.01017 and 136/81 − 182√5/243 = 0.00426 (70 : 30). Each notched cap therefore carries 4 notches of two sizes (2 + 2), consistent with its symmetry: the mirrors x → −x and y → −y hold (mesh symmetric difference ~1e-18), the 90° turn does not (0.033). The notched cap is one achiral shape; step 11's volume is right because the 6 caps are Th-equivalent.

**R4 — What was "sampled only" is now exact.** Step 8's "Ms on different edges never overlap" and "every point in exactly one piece" are proved (lemmas 5–8); the README can upgrade those statements.

**R5 — Shape facts worth stating.** H is an **oblique pentagonal antiprism**: 10 corners = the 5 tips of each star (star centres and inner corners lie inside H), 2 regular pentagons perpendicular to the five-fold axis + 10 triangles. Exact: the pentagons' centres are offset sideways by exactly their circumradius r = 0.3505 **and** axially by exactly r (a 45° shear); the half turn between the pentagons equals a 36° turn. The Penrose core is 76 % by volume of the full thick-rhombus prism between the two OCD surfaces inside the 4 cells (24 % of that prism lies outside H); step 14's "12 % of columns" is a column count, not a volume share.

**R6 — Hexagon coverage.** All 6 corners of the joint hexagon lie inside the key's base triangle (exact), so the key base covers the hexagon with an overhang onto the three caps, as step 12 says.

**R7 — Topology of the rest.** The middle rest has genus 1: it is a closed ring round the Penrose core (the rhombus footprint lies strictly inside H's footprint). Core and rest are each one solid, as step 15 says, but the core can only be inserted or removed along the five-fold axis, i.e. before the second OCD is placed. Kit B's rest has genus 1 too.

**R8 — Mesh artefacts.** manifold3d booleans leave zero-volume sheets (the notched cap decomposes into 1 real + 4 zero-volume parts; the notched T+ and T− meshes differ in raw area by up to 3 % although they are exact mirror images). Volumes are unaffected; areas and hence ψ are, so the ψ values below use a cleaned area (coincident triangle pairs removed; for the mirror pair the smaller of the two meshes, since sheets only add area) and should be read as ±0.02. Step 17's ψ values carry the same uncertainty.

## 3. Improvement suggestions (ranked)

Sphericity ψ = π^(1/3)(6V)^(2/3)/A (mesh, cleaned area):

| piece | volume | ψ | solid parts (>1e-9) | genus |
|---|---|---|---|---|
| bare OCD | 1.151868 | 0.979 | 1 | 0 |
| keyed OCD | 1.223113 | 0.696 | 1 | 0 |
| cap (keyed kit) | 0.086940 | 0.471 | 1 | 0 |
| dented tetrahedron (keyed kit) | 0.382754 | 0.620 | 1 | 0 |
| notched cap | 0.058072 | 0.548 | 1 | −4 (sliver artefact; the solid part is genus 0) |
| middle piece M | 0.073291 | 0.447 | 1 | 0 |
| Penrose core | 0.010129 | 0.752 | 1 | 0 |
| middle rest | 0.063162 | 0.385 | 1 | 1 |
| notched tetrahedron | 0.249486 | 0.474 | 1 | 0 |
| A: OCD + 8 hexagonal-plug keys | 1.205302 | 0.948 | 1 | 0 |
| A: plug key alone | 0.006679 | 0.509 | 1 | 0 |
| A: tetrahedron with 4 plug dents | 0.391660 | 0.616 | 1 | 0 |
| B: middle piece M₀ (no keys) | 0.079735 | 0.579 | 1 | 0 |
| B: rest (no keys) | 0.069606 | 0.497 | 1 | 1 |
| B: notched tetrahedron (no dents) | 0.265776 | 0.517 | 1 | 0 |

Penrose core is unchanged in kit B (no key enters it). Step 17 gave 0.494 for the notched cap from a mesh carrying more sliver area (R8); 0.548 is the lower-area (better) estimate.

**I1 — Drop the keys in the full kit (kit B).** The 12 middle pieces already register every OCD (their ends are the star dimples) and the caps and tetrahedra register on the Ms through their notches, so the keys are redundant for space filling and for positioning. Exact by construction: the keys return to the tetrahedra; M₀ = H − OCD₁ − OCD₂ = (310+26√5)/4617 = 0.07974; hull–hull disjointness (lemma 7) keeps the M₀s disjoint; the notched cap is unchanged (keys lie outside the octahedra). Sampled: 2,000,000 uniform + 2,000,000 near-face points, 0 uncovered, 0 double. Sphericity: OCD 0.979 instead of 0.696, middle piece 0.579 instead of 0.447, tetrahedron 0.517 instead of 0.474, rest 0.497 instead of 0.385. Shapes: OCD, notched cap, M₀ (or core + rest), left and right tetrahedron — 5 (4 with the mirror pair as one). Bonus: the flanking Penrose prisms of step 14 failed only because they ran into keys; without keys they become possible again (they still poke out of H by ≈22 % — not tested here).

**I2 — In the keyed kit, cut the key down to the hexagonal plug (kit A).** key′ = key ∩ (prism over the joint hexagon) has exactly 3/4 of the key's volume, (−11+5√5)/27; the overhang stays with the tetrahedron. Exact by construction (key′ ⊂ key ⊂ T). Sphericity of the keyed OCD rises from 0.696 to 0.948 (bare OCD 0.979); the dented tetrahedron 0.616 (was 0.620). The tetrahedron remains chiral. Note: the trimmed keys still reach the middle hulls (4 keys, 2/243 − 4√5/1215 = 0.00087 each), so this does not simplify the full kit.

**I3 — Keep M whole unless the Penrose motif is the point.** Splitting M into core (ψ 0.75) and rest (ψ 0.385, a ring round the core — R7) adds a piece and makes the rest the least chunky piece of the set; as one piece in kit B the middle piece scores 0.579.

**I4 — Golden facts for the periodic↔aperiodic story (exact, new in this review).** The two key base corners on every octahedron edge are its two golden-section points (φ : 1 and 1 : φ); the facing tip pentagons are offset by exactly (r, r) — a 45° shear of a pentagonal antiprism; c1→c2 is the long diagonal of a thick Penrose rhombus whose edges run along the star spokes (step 13, confirmed).

**I5 — Kit practicalities.** Both kits need a left and a right tetrahedron (two STL files, two colours; the app's keyed row should match the full row). Caps are achiral and identical. Step 17's merging attempts are rightly rejected; the thin piece that remains is the rest ring, which kit B thickens (ψ 0.385 → 0.497).

## 4. Open questions for DICTO
1. Keep the keys in the full kit for feel/locking, or drop them (I1)? In the full kit the twisted notches make the tetrahedra chiral anyway.
2. In the keyed kit, hexagonal plug (I2) or overhanging key? The overhang gives the OCD a collar resting on the three caps round each hexagon; the plug does not touch the caps.
3. Core + rest (a ring that assembles along the axis only) or one middle piece?
4. Correct the README's step-9 conclusion and the app's keyed row now (left/right tetrahedra in both kits)?
