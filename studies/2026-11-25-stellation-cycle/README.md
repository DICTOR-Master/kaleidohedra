# The stellation cycle: Pacioli's rectangles, the Vacuus, the Resonus, the Kepler–Poinsot stars, the Dogstar, the Sunstar, the H3 permutahedron and the Aequi (25 November 2026)

DICTO · dictospheres.com · study 2026-11-25-stellation-cycle · with Claude (Anthropic).

DICTO's proposal (25 Nov, recorded at the end of papers/2026-11-24-vacuus-resonus/PLAN.md): a cycle joining Pacioli's golden rectangles,
the Vacuus, the Resonus, the Kepler–Poinsot stars, the Dogstar and the Sunstar, with the permutahedra and the Aequi joining it, which may
close gaps between earlier cycles in the right ratios. Everything below is exact in Q(√5) unless marked otherwise.
Checks: scripts/cycle.py FINAL ok (data/cycle.log, data/cycle.json); scripts/aequi.py FINAL ok (data/aequi.json);
scripts/loose_step.py FINAL ok (data/loose-step.json).

**Verdict.**
- **(1) The cycle holds.** Pacioli's icosahedron I0 and its dual dodecahedron D0 share one midsphere. Each Kepler–Poinsot star of a
  dodecahedron D_k has the corners of I_{k+1} = φ·I_k (small stellated and great dodecahedron) or of D_{k+3} (great stellated
  dodecahedron). The great icosahedron of I_k has the corners of I_{k+3}. So the golden rectangles come back at every scale φ^k, for every
  integer k. Every one of these stars, and the Dogstar, has the 15 mirror planes as its Vacuus and keeps its core's Resonus.
- **(2) The hub holds.** The H3 permutahedron's 31 Resonus planes are exactly I's 10, D's 6 and the 15 mirrors. Its 20 hexagon centres are
  the corners of φ²·D0, which is a step of the cycle.
- **(3) The Aequi.** 4 039 of the dice checked have their Resonus inside the 31 planes. None has a depth ratio equal to a step of the cycle at
  a different scale (φ^k with k ≠ 0). 39 dice have face planes that lie, to every digit computed, on the planes of I_k and RT_k (or D_k and
  RT_k) at one and the same scale. That is an observation, not yet proved.
- **(4) Earlier cycles.** The Chain of Karma and the Kepler–Poinsot–UP cycle (#38a) are this same ladder. Double Vision's factor 3 is exactly
  the great stellated dodecahedron's spike ratio: this names the gap but does not close it, because 3 is not a power of φ. The
  Palintriacontahedron's 3/√5 is now exact. The uniform H3 permutahedron does **not** close the loose step O ⊂ rTI.

## Frame

I0 = cyclic (0, ±φ, ±1): Pacioli's three golden rectangles, 2 × 2φ, in the coordinate planes. D0 = (±1, ±1, ±1) and cyclic (0, ±1/φ, ±φ).
This is the frame of the Aequi (study 2026-11-19-aequi-complete). I_k = φ^k·I0 and D_k = φ^k·D0. Squared values: I0 edge 4,
D0 edge 6 − 2√5, I0 circumradius (5 + √5)/2, D0 circumradius 3, I0 inradius (7 + 3√5)/6, D0 inradius φ⁴/(φ + 2).
The 15 mirror planes are the planes at right angles to the 15 two-fold axes (checked: each one maps I0 to itself).

## Theorems

**Theorem 1 (the dual pair).** I0 and D0 share the midsphere of radius φ. Each is the polar of the other in it:
I0 = {x : w·x ≤ φ² for all w in D0} and D0 = {x : n·x ≤ φ² for all n in I0}. So I_k and D_k are polar in the sphere of radius φ^{k+1}.
*Proof.* Every edge midpoint of both has squared radius φ². Each corner w of D0 gives a plane w·x = φ² through exactly 3 corners of I0, with
all others below it. Each corner n of I0 gives a plane through exactly 5 corners of D0. (cycle.py, exact asserts.)

**Theorem 2 (vertex return; the stellation ladder).** Stellate D_k in its own face planes n·x = φ^{k+2} (n in I0). Then:
- the small stellated dodecahedron {5/2, 5} and the great dodecahedron {5, 5/2} both have the 12 corners of **I_{k+1} = φ·I_k**;
- the great stellated dodecahedron {5/2, 3} has the 20 corners of **D_{k+3} = φ³·D_k**, and the inner corners of its visible surface are
  those of I_{k+1}.

Stellate I_k in its face planes. Then the great icosahedron {3, 5/2} has the 12 corners of **I_{k+3} = φ³·I_k**.
Hence the cycle I_k → D_k → (small stellated / great dodecahedron) → I_{k+1} returns Pacioli's rectangles at scale φ, for every integer k.
I_{k+1}'s rectangles are 2φ^{k+1} × 2φ^{k+2}. The great stellated dodecahedron and the great icosahedron make three steps at once (φ³).
D_k's own 12 non-cube corners form rectangles of ratio φ², not φ.

*Proof.* The scales are exact: they are the triple points of the 12 (or 20) face planes, grouped by radius and axis (data/cycle.log).
- D0's planes meet in 3 shells: the 20 corners of D0, the 12 corners of φ·I0 and the 20 corners of φ³·D0.
- For each star, the face of a plane is the set of shell corners on it: 5 corners for the dodecahedral stars and 3 for the great
  icosahedron. Its sides are the longest pairs (pentagram) or the shortest pairs (pentagon, triangle).
- Each star has V, E, F = 12, 30, 12 (Euler characteristic −6) or 20, 30, 12 or 12, 30, 20 (Euler characteristic 2). Each edge lies in
  exactly two faces. The vertex degrees are 5, 5, 3 and 5.
- Scale invariance carries the result from k = 0 to every k.

The vertex sets and edge sets are classical (Coxeter, Regular Polytopes; cited, not opened); what is checked here is the exact scale in this
frame.

**Lemma 3 (stellation planes).** If all face planes are n_i·x = d, then the plane through O and the line where faces i and j meet is
(n_i − n_j)·x = 0. For the dodecahedron's 12 face normals, n_i − n_j always lies on a two-fold axis, for every non-opposite pair (squared
distances 4 and 6 + 2√5). For the icosahedron's 20 face normals the same holds for the pairs at squared distances 6 − 2√5, 4 and 6 + 2√5. It
fails only for the pairs at squared distance 8, whose difference lies along a cube's face diagonal, (1, 1, 0) up to symmetry.
*Proof.* If n_i·x = n_j·x = d, then (n_i − n_j)·x = 0, and O lies on that plane too. The pair classes are listed exactly in data/cycle.log.

**Theorem 4 (Vacuus and Resonus along the cycle).**
- (a) **Every stellation of the dodecahedron has its Vacuus inside the 15 mirror planes.** This holds for every union of cells of its 12
  face planes, as a star polyhedron or as a visible surface, and so for every polyhedron whose edges all lie on lines where two of those
  planes meet. It follows from Lemma 3.
- (b) Computed exactly:
  - For the four Kepler–Poinsot stars with their true edges (the 30 star edges), and for I0 and D0, the Vacuus is **exactly the 15 mirror
    planes**.
  - The small stellated dodecahedron, the great dodecahedron and the great stellated dodecahedron as visible surfaces (90 edges each) also
    give exactly the 15.
  - **The Dogstar** (Hart's stellation 8 of the dodecahedron) gives exactly the 15. Only 3 of them, the coordinate planes, are mirrors of the
    Dogstar's own symmetry (Th). The other 12 are mirrors of the icosahedral frame it was cut from, not of the Dogstar itself.
- (c) **Every stellation keeps the Resonus of its core**: 6 planes (five-fold) for the dodecahedral stars and the Dogstar, 10 planes (three-fold)
  for the great icosahedron. A stellation only extends the core's face planes, and each of those planes still carries a face (checked on
  every surface).
- (d) The icosahedron's other stellations can have Vacuus planes that are not mirrors, but only along lines from face pairs at squared
  distance 8 (Lemma 3). The great icosahedron uses none of them.

**Theorem 5 (the Dogstar and the Sunstar in the cycle).** Take the Sunstar Lattice of paper #42 with cells of edge 2. The cell dodecahedron is
D0 and the Dogstar's core is D_{−3} = φ⁻³·D0, as #42 states; here that is checked again and the edges are found.
- **The Dogstar** has 20 corners and 30 edges. Its 12 five-fold tips are the corners of **I_{−2}** about its own centre: the tips of the small
  stellated dodecahedron of its core. Its 8 three-fold tips are the cube corners of D0, the tips of the great stellated dodecahedron of its
  core. Two independent constructions give the same corners, edges and Vacuus:
  - the cells of the core's planes (core, 12 pyramids, 24 wedges, 8 spikes);
  - Hart's tiling (the cube minus the six neighbouring dodecahedra).
- **The Sunstar** (D0 with six Dogstars) has 92 corners and 150 edges. Its Resonus is D0's 6 planes. Its Vacuus about the centre of D0 has
  **69 planes**, and only 3 of them (the coordinate planes) are among the 15 mirrors. So the Sunstar keeps the cycle's Resonus but leaves its
  Vacuus.
- Placement: the Star Chain Reaction of #42 (×φ³) is one turn of the ladder: D_{−3} → great stellated dodecahedron → D0.
- The Dogstar's tips I_{−2} are the inner icosahedron of the Chain of Karma for the cell dodecahedron (Theorem 7).

**Theorem 6 (the hub: the H3 permutahedron).** Take the uniform truncated icosidodecahedron, edge 2/φ = D0's edge (coordinates as study
2026-11-24-permutahedron-leads).
- Its 62 face planes are found exactly: 30 squares, 20 hexagons and 12 decagons, on the 15 two-fold, 10 three-fold and 6 five-fold axes. Its
  180 edges each lie in exactly two of them, so these are all its faces.
- Hence **its Resonus is exactly 31 planes: I's Resonus (10), D's Resonus (6) and the 15 mirrors, which are the Vacuus of I, D and every
  star above.**
- Squared face distances: squares (27 + 7√5)/2, hexagons (21 + 9√5)/2, decagons (25 + 5√5)/2. Squared circumradius (33 + 5√5)/2.
- **Hexagon distance = 3 × the inradius of I0, exactly (squared ratio 9).** It is also the circumradius of φ²·D0. So **the 20 hexagon
  centres are the corners of D_2 = φ²·D0**, the largest copy of D0 inside the permutahedron.
- The decagon centres are √5·I0, and √5 is not a power of φ. The square centres are ((3√5 − 1)/2)·ID0, where ID0 is the icosidodecahedron of
  I0's edge midpoints; that scale is not a power of φ either.

**Theorem 7 (the earlier cycles are this ladder).**
- **Chain of Karma** (#22): I(1/φ) ⊂ D(1) ⊂ I(φ²) ⊂ D(φ³), edges relative to D(1). In this frame that is I_{k−2} ⊂ D_k ⊂ I_{k+1} ⊂ D_{k+3}
  (edge ratios 1/φ, φ², φ³, from the exact edges of Theorem 2). Each station is the corner set of a Kepler–Poinsot star:
  - I_{k−2} is the small stellated dodecahedron of D_{k−3}, and D_k is its great stellated dodecahedron;
  - I_{k+1} is the small stellated dodecahedron of D_k, and D_{k+3} is its great stellated dodecahedron.
- **The Kepler–Poinsot–UP cycle** (#38a): one turn is I_{k+1} (kernel) → great stellated dodecahedron of D_k → D_{k+3} (its hull) →
  small stellated dodecahedron → I_{k+4}. Edge steps are ×φ, then ×φ²; one turn is ×φ³, as #38a states.
- **The spike ratio 3:** the circumradius of D_{k+2} is exactly 3 × the inradius of I_k. This is #38a's "spikes to 3× the face distance",
  now tied to the ladder.

## The earlier cycles: which gaps close (step 4)

| earlier cycle and its open point | what this study finds | closes? |
|---|---|---|
| #22 Chain of Karma, ×φ³ per round | its stations are the corner sets of the Kepler–Poinsot stars of D_{k−3} and D_k (Theorem 7) | nothing was open; now explained by stellation |
| #38a Kepler–Poinsot–UP cycle, ×φ³ | the same ladder; spike ratio 3 = R(D_{k+2}) / r(I_k) | nothing was open; identified |
| #33 Double Vision: the two settings differ by 3, not a power of φ | 3 is exactly the great stellated dodecahedron's spike ratio, and exactly the uniform H3 permutahedron's hexagon distance over I0's inradius | **does not close**: 3 ≠ φ^k for every k ≠ 0 (proof in #33). The gap has an exact geometric name, but it is a circumradius-to-inradius step, not a similarity between stations |
| #34/#35a: the same number 9/φ⁴ as Progenitors' tightest 3-cycle gain and the Metaxyhexecontahedron's edge ratio ("coincidence noted without explanation") | 9/φ⁴ = (R(D0)/r(I0))² exactly, where R(D0)/r(I0) = 3/φ² for the midsphere dual pair (cycle.json) | **observation only**: both numbers equal the square of the dual pair's radius ratio; why each construction produces it is not proved here |
| #35b Palintriacontahedron: "the first stellation of the icosahedron puts its tips at 3/√5 times the face distance" (float observation in the book) | exact: tip ÷ face distance = \|w0\|²/(w·w0) = 3/√5 for neighbouring face normals w0, w (squared ratio 9/5) | **closed (made exact)**. This is equality of the number 3/√5 only; the first stellation's tip hull is not the Palintriacontahedron |
| Golden Cycle book, open problem (1): the loose step O ⊂ rTI | uniform H3 permutahedron, exact, Dharma frame (loose_step.py): scaled to hold O (12 corners of O touching) it reaches 1.0386 of the way out of rTI; scaled to touch rTI from inside (scale (√5 − 1)/4) it does not hold O | **does not close**. The Aequi were not tested here (LEAD) |
| #14 DICTO-Star: "missing the exact closure" | this is a missing exact write-up (icosidodecahedron, 12 dodecahedra, 20 tridiminished icosahedra), not a ratio gap | not addressed |
| #32 Inverted Shells | the reversed cycle; its shared stations with the original are those of #33 above | as #33 |

## The Aequi (step 3)

Sources: the 4 553 dice of study 2026-11-19-aequi-complete (depths to 60 digits) and the 9 545 certified records of study
2026-11-24-aequi-certify-extend (enclosures of radius 1e-44). The 1 083 dice of study 2026-11-20-aequi-two-placements use both icosahedron
placements by definition, so no one set of 31 planes holds their Resonus. The three face-transitive Nos. 1233–1235 have normals in general
position (TO-24, TCO-48, TID-120 duals); their normals lie on no axis, so they are not inside the 31 either.

- **Resonus inside the 31 planes**: the condition is face directions only from C6, O8, D12, I12, RT24 (no RD12, and one icosahedron placement).
  - 2 343 of the 4 553: all 4 Ih dice, 112 D5d, 62 D5, 244 D3d, 330 D3, 190 S6, 358 D2h, 466 C2h, 456 D2, 49 Ci, 45 T, 19 Th, 1 Oh, 1 Td,
    2 D2d, 2 D4h, 1 D5h, 1 D10h.
  - 1 696 of the extension.
  - Total **4 039**.
  - The rest use RD12 (cube two-fold axes, 2 210 + 3 830) or both placements (4 019).
- So the rule "every icosahedral-axis Aequus has its Resonus in the 31" holds: those are exactly the 4 039 (by construction of the frames).
- **Depths at a cycle step (φ^k with k ≠ 0)**: for every pair of orbits, the depth ratio was compared with φ^k times the ratio of the station
  depths of I, D, RT (the hull of I_k ∪ D_k, rhombi at the midsphere) and the H3 permutahedron along those axis types. **No die has such a
  ratio at k ≠ 0** (to 1e-30, against data good to 1e-44 or better). Refuted for the catalogue as given.
- **Observation (same-scale coincidences, not proved):**
  - 37 dice have a two-fold orbit and a three-fold orbit with depth ratio exactly √3/φ, to every digit computed. That is the ratio of RT_k's
    rhombus planes to I_k's face planes at the same k, so these faces lie on the face planes of one icosahedron and its triacontahedron.
  - One die (D5d, sid 77 of the 4 553) has the same with D_k and RT_k.
  - One extension die (caps batch 2, id 29) has a three-fold to two-fold ratio of √3/φ.
  - 16 dice have two orbits of the same axis type at equal depth.
  - These ratios are algebraic, while Aequus depths solve transcendental equations, so each must have a structural reason (probably
    corners where four planes meet). Listed in data/aequi.json as `coincidences` and `equal_depth_dice`.
  - None of them is a vertex set equal to I_k, D_k or a star. A die with m ≥ 2 orbits is not face-transitive, so it is never one of these
    polyhedra itself.

## Diagram-ready table of the cycle (k any integer; scales relative to I0, D0)

| step | polyhedron | corners / scale | Vacuus | Resonus |
|---|---|---|---|---|
| 0 | Pacioli's 3 golden rectangles | in I_k: 2φ^k × 2φ^{k+1} | – | – |
| 1 | icosahedron I_k | φ^k·I0 | 15 mirrors | 10 (three-fold) |
| 2 | dodecahedron D_k (polar of I_k in the midsphere φ^{k+1}) | φ^k·D0 | 15 mirrors | 6 (five-fold) |
| 3 | small stellated dodecahedron of D_k | corners I_{k+1} (×φ) | 15 mirrors (star edges and surface) | 6, inherited |
| 3′ | great dodecahedron of D_k | corners I_{k+1} (×φ) | 15 mirrors | 6, inherited |
| 4 | great stellated dodecahedron of D_k | corners D_{k+3} (×φ³), kernel I_{k+1} | 15 mirrors | 6, inherited |
| 4′ | great icosahedron of I_k | corners I_{k+3} (×φ³) | 15 mirrors | 10, inherited |
| 5 | Dogstar (core D_{k−3}, cell dodecahedron D_k) | tips I_{k−2} (12) + 8 cube corners of D_k | 15 mirrors (3 its own) | 6, inherited |
| 6 | Sunstar (D_k + six Dogstars) | 92 corners | 69 planes (3 mirrors) | 6 |
| hub | uniform H3 permutahedron (edge = D0 edge) | hexagon centres = D_2; decagon centres √5·I0 | – | 31 = 10 + 6 + 15 |
| return | I_{k+1} | rectangles ×φ | 15 | 10 |

## Method

- Pure-Python exact arithmetic in Q(√5): scripts/q5.py.
- Star polyhedra:
  - from the triple points of the face planes;
  - faces = shell corners on each plane, with sides by distance class.
- Visible surfaces (scripts/arrangement.py): each polyhedron is a union of cells of a plane arrangement, given by an exact membership
  rule on the sign vector.
  - Every line where two planes meet is cut at all other planes.
  - At each piece, the sectors round the line are sampled exactly: sector sums of the plane traces, no ε.
  - A piece is an edge when the in/out pattern is neither constant nor a single flat split.
- Vacuus = planes through O and each edge line (normal p × u); Resonus = planes through O parallel to the face-carrying planes. This
  follows the definitions and the projective-key and mirror tests of study 2026-11-24-resonus (resonus_3d.py), rewritten without dependencies.
- The Dogstar's two constructions are compared corner by corner.
- The Aequi test uses Python's decimal module at 70 digits.
- The loose-step test rebuilds O and rTI with the Progenitors study's own code.
- All runs were on the compute hosts, each under 20 s.

Credit:
- Kepler–Poinsot stars and their vertex/edge sets: Kepler, Poinsot; Coxeter, Regular Polytopes (cited, not opened).
- The Dogstar as stellation 8 of the dodecahedron and its tiling: G. W. Hart (1996), also Walser and Polyhedra-World, as credited in #42.
- Pacioli's golden rectangles: Pacioli, De divina proportione (1509; cited, not opened).
- The 31 planes as Fuller's 31 great circles: as recorded in PLAN.md (Fuller, Synergetics; cited, not opened).

## Sources checked

papers/2026-11-24-vacuus-resonus/PLAN.md (end); papers/names-audit.md (Dogstar row); papers/2026-10-20-dicto-sunstar/paper.html (#42: Dogstar,
Sunstar, Star Chain Reaction); papers/2026-10-19-kepler-poinsot-pitet/paper.html (#38a); papers/book-golden-cycle/paper.html (Chs 1, 6–10,
open problems: #22, #32, #33, #34, #35a, #35b, #38); papers/consolidation-map.md (Book Four); studies 2026-11-24-resonus,
2026-11-24-permutahedron-leads, 2026-11-19-aequi-complete, 2026-11-20-aequi-two-placements, 2026-11-24-aequi-catalogue-2,
2026-11-24-aequi-certify-extend, 2026-11-24-aequi-table, 2026-10-16-progenitors. No outside source was searched for this study. The "new"
status of the Vacuus/Resonus statements for stars rests on the prior-art search of the Vacuus–Resonus paper, still to be done.

## LEADS

1. Prove the 39 same-scale coincidences of the Aequi structurally (expected: corners where a two-fold plane meets an I_k edge line); then
   these dice are the gap-closers in DICTO's sense: Aequi whose faces lie on one cycle station's planes.
2. Test the Ih Aequi (4) and the D5d/D3d dice of the 31 for the loose step O ⊂ rTI (exact for the ones whose depths are provably algebraic).
3. The icosahedron's 59 stellations: which ones use the squared-distance-8 face pairs (Lemma 3) and so have Vacuus planes that are not mirrors.
4. The Sunstar's 69 Vacuus planes: their orbit structure under Th, and the Sunstar Lattice's Vacuus about other centres.
5. The decagon (√5·I0) and square ((3√5 − 1)/2·ID0) centres of the H3 permutahedron: is there a uniform-like H3 permutahedron whose three
   centre sets all lie on the ladder (a free-depth member of the family)?
6. Into the Vacuus–Resonus paper (§8 "Where V meets SF and A"): Theorem 4 (stars keep the Resonus; dodecahedral stellations have the 15
   mirrors as Vacuus), Theorem 6 (hub), and the Dogstar's 12 non-own mirrors. To ask DICTO where it goes.

## Files

- scripts/q5.py: exact Q(√5).
- scripts/arrangement.py: surface edges of a union of cells.
- scripts/cycle.py → data/cycle.log, data/cycle.json: Theorems 1–7.
- scripts/aequi.py → data/aequi.json: step 3.
- scripts/loose_step.py → data/loose-step.json: the O ⊂ rTI test. Run it from inside study 2026-10-16-progenitors; it reads
  2026-10-16-polar-dharma and 2026-10-15-icosa-star-hollow.
