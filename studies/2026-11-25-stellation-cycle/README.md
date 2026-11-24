# The stellation cycle: Pacioli's rectangles, the Vacuus, the Resonus, the Kepler–Poinsot stars, the Dogstar, the Sunstar, the H3 permutahedron and the Aequi (25 November 2026)

DICTO · dictospheres.com · study 2026-11-25-stellation-cycle · with Claude (Anthropic).

DICTO's proposal (25 Nov, recorded at the end of papers/2026-11-24-vacuus-resonus/PLAN.md): a cycle joining Pacioli's golden rectangles,
the Vacuus, the Resonus, the Kepler–Poinsot stars, the Dogstar and the Sunstar, with the permutahedra and the Aequi joining it, which may
close gaps between earlier cycles in the right ratios. Everything below is exact in Q(√5) unless marked otherwise.
Checks: scripts/cycle.py FINAL ok (data/cycle.log, data/cycle.json); scripts/aequi.py FINAL ok (data/aequi.json);
scripts/loose_step.py FINAL ok (data/loose-step.json). Second part (gap-closers): scan42, exact42, factor3, gaps, gapcheck, vacres, all FINAL ok.

**Verdict.**
- **(1) The cycle holds.** Pacioli's icosahedron I0 and its dual dodecahedron D0 share one midsphere. Each Kepler–Poinsot star of a
  dodecahedron D_k has the corners of I_{k+1} = φ·I_k (small stellated and great dodecahedron) or of D_{k+3} (great stellated
  dodecahedron). The great icosahedron of I_k has the corners of I_{k+3}. So the golden rectangles come back at every scale φ^k, for every
  integer k. Every one of these stars, and the Dogstar, has the 15 mirror planes as its Vacuus and keeps its core's Resonus.
- **(2) The hub holds.** The H3 permutahedron's 31 Resonus planes are exactly I's 10, D's 6 and the 15 mirrors. Its 20 hexagon centres are
  the corners of φ²·D0, which is a step of the cycle.
- **(3) The Aequi.** 4 039 of the dice checked have their Resonus inside the 31 planes. None has a depth ratio equal to a step of the cycle at
  a different scale (φ^k with k ≠ 0). **42 dice have faces lying exactly on the planes of I_k and RT_k (or D_k and RT_k) at one and the same
  scale: proved (Theorem 8, second part below).**
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
- **Same-scale dice (now Theorem 8):** 42 dice have faces on the planes of one I_k (or D_k) and of RT_k at the same k: 38 of the 4 553 and 4 of
  the extension. (The first run of aequi.py read the extension's certified depths one orbit out of place; corrected on 25 Nov. It now finds
  42 such dice, and 24 with two orbits of one axis type at equal depth; data/aequi.json `coincidences`, `equal_depth_dice`.)
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

## Second part: the station dice and the gap-closers (25 November 2026)

**DICTO's conjecture (25 Nov).** A further related shape fills the remaining gaps of the cycle. Filling the gap and building its Vacuus and
Resonus are part of one construction, and the shape lies among the Aequi. The gaps: (a) the loose step O ⊂ rTI; (b) Double Vision's
factor 3; (c) the DICTO-Star (#14); (d) the Sunstar, whose Vacuus has 69 planes.

**Verdict (second part).**
- **Theorem 8 (proved, all 42).** Every same-scale coincidence of the Aequi is exact: 42 dice have one orbit of faces lying exactly on face
  planes of one icosahedron I_k (one die: of one dodecahedron D_k), with the faces next to them on the rhombus planes of RT_k at the same k.
- **(a) not closed.** Two Aequi fit strictly inside O ⊂ rTI, but neither touches both: Yo (No.4) and Goi (No.51).
- **(b) cannot be closed by φ-steps** (3 is not a power of φ; proof in #33). The factor is carried exactly by 41 of the station dice:
  their depth ratio r satisfies φ²r² = 3.
- **(c) a fit that touches both (exact).** A D5d station die fits between the DICTO-Star's icosidodecahedron and the star's hull, touching
  both. It sits at step 0 of the ladder. Its Resonus is inside the 31 planes, but its Vacuus is not inside the 15 mirrors (15 planes, 10 of
  them mirrors).
- **(d) a fit that touches both (exact).** The regular octahedron |x| + |y| + |z| ≤ 3 fits between D0 and the Sunstar's hull, touching
  both. Its Vacuus (the 3 coordinate mirrors) and Resonus (4 three-fold planes) lie inside the cycle's planes. Its size is off the φ
  ladder: its faces lie on the planes of (3/φ²)·I0, so the factor 3 of gap (b) shows up here too. It is a fair die (face-transitive), but it
  is not in the numbered Aequi catalogue.
- **The conjecture.** One part holds: Aequi touch both sides of gaps (c) and (d), with Resonus inside the 31. No single shape closes every gap:
  - in (c), the Vacuus leaves the 15 mirrors;
  - in (d), the closer is off the φ ladder;
  - (a) stays loose;
  - (b) cannot close.

### Theorem 8 (the station dice)

**Theorem 8.** For each of the 42 dice listed in data/exact42.json, the following holds in the fair die itself. Take the orbit S of
three-fold faces (for one die, the five-fold pair D12/2) and the orbit B of two-fold faces next to it. Then:
- the faces of S lie exactly on face planes of one I_k (of D_k), and the faces of B lie exactly on rhombus planes of RT_k at the same k;
- the depths satisfy d(B)/d(S) = √3/φ exactly (for the D12/2 die, d(S)/d(B) = φ/√(φ + 2) = √((5 + √5)/10));
- each face of S is a whole face triangle of I_k (a whole pentagon of D_k). It covers 6 (10) of the 120 mirror triangles, that is
  4π/20 (4π/12), so the die has N = 20 faces (N = 12).

Station offsets used (unnormalised normal q, plane q·x = h, scale k = 0):
- three-fold O8 (1, 1, 1) and I12 (0, 1/φ, φ): h = φ² (I0's faces);
- five-fold D12 (0, φ, 1): h = φ² (D0's faces);
- two-fold C6 (1, 0, 0): h = φ; RT24 (1, φ, 1/φ): h = 2φ (RT0's rhombi, depth φ, through the midsphere points).
All of these are in Q(√5).

**Lemma 9 (monotone cells).** Let S be a set of face orbits of a fair die P with depths d*. Let d(s) be d* with every S depth multiplied by
s. Then the solid angle Ω_S(s) of all S faces together is strictly decreasing in s.
*Proof.* Let p_i = u_i/d_i. The central projection of the S faces is U(s) = {x : max_S p·x / s ≥ max_rest p·x}. On U(s) the S maximum is
positive (the centre is inside), so U(s′) ⊂ U(s) for s′ > s. A point on an arc of U(s) bordering a non-S face fails the inequality at s′,
and so do nearby points inside U(s). Such arcs exist, since the non-S faces have positive area. So the area drops strictly. ∎
This is the elementary monotonicity behind Alexandrov's uniqueness theorem; it is used here only as stated.

**Proof of Theorem 8.**
1. *The station point.* Let s0 be the factor that puts the S planes onto the station planes paired with B (B kept at its certified depth).
2. *An exact polytope.* Let Q be the polytope cut out by the S and B planes alone, at the station offsets. It is exact in Q(√5)
   (scripts/exact42.py; corners by Cramer's rule, every incidence exact).
3. *The other faces stay away.* Every corner of every S face of Q lies strictly inside every plane of the other orbits, at their certified
   depths. This is checked in ball arithmetic on the certified enclosures (studies 2026-11-24-aequi-certify-4404 and -certify-extend:
   Krawczyk boxes of radius 1e-40, or the tight split box for the dice on a wall). The smallest slack is 0.0023 (sid 365). So at s0
   the S faces of P are exactly the S faces of Q.
4. *A shadow count.* Every side of every S face of Q lies in a mirror plane, and every corner lies on a rotation axis (exact). By the
   shadow-dice theorem (study 2026-11-24-aequi-exact-dice, Theorem 2(a)), each S face projects onto a whole number of the 120 mirror
   triangles. Ball arithmetic pins the number: 6 per face (10 for the pentagons), and the S faces together cover exactly 120·|S|/N.
   So Ω_S(s0) = 4π|S|/N.
5. *Conclusion.* The fair die has Ω_S(1) = 4π|S|/N too. By Lemma 9, s0 = 1. ∎

The station ratio agrees with the certified depth ratio to better than 1e-25 for every die. Die 310 (D3d: O8+I12/6 + I12/2 + RT24/12) has
an RT24 plane through corners of its I12/2 faces, so step 3 cannot be strict there. It is proved whole instead:
- all three orbits are put on station planes at one scale, and the whole polytope is exact;
- each orbit's faces together are bounded by mirror arcs and cover 36, 12 and 72 triangles (= 120·|orbit|/20);
- faces of one orbit are congruent under the die's group, so the polytope is fair;
- by Alexandrov's uniqueness (prescribed normals and solid angles, used through polarity as in the aequi-exact-dice study) it is the
  catalogue die.

Its three scale checks agree to 30 digits.

**Classification (data/exact42.json).**

| group | dice | S (on I_k or D_k) | B (on RT_k) | whole die exact? |
|---|---|---|---|---|
| D5d | sid 77 | D12/2: two opposite pentagons of D_k | C6+RT24/10 | yes (2 orbits) |
| D5d | sids 87, 89 | O8+I12/10: ten triangles of I_k | C6+RT24/10 | yes (2 orbits; 89 is also a shadow die) |
| D3d | sids 301, 302, 360, 361, 362, 364, 365, 366, 367 | I12/2: two opposite triangles | a C6+RT24/6 orbit | no: other orbits stay free |
| D3d | sid 310 | O8+I12/6 and I12/2 | RT24/12 | yes (proved whole) |
| D3 | sids 2197, 2198, 2199, 2200, 2202, 2203, 2213, 2215; Yaonani (No.8072), Yaonayo (No.8074) | O8/2: two opposite triangles | an RT24/6 orbit | no |
| S6 | sids 2631, 2635, 2639, 2640, 2661, 2662, 2663, 2664, 2671, 2672 | O8/2 | an RT24/6 orbit | no |
| D2h | sids 1037, 1039, 1040, 1483, 1506, 1507; Gonayamu (No.5786), Gonakuna (No.5797) | I12/4: four triangles | an RT24/8 orbit | no |
| T | Muna (No.67) = Aequus ORT-20, T 9 | O8/4a: four triangles | RT24/12 | no |

"sid" is the record number of study 2026-11-19-aequi-complete. Those dice have no catalogue number yet (they follow No. 10725). Names
from studies 2026-11-24-aequi-numberings and 2026-11-24-aequi-catalogue-2.

What the theorem shows: a face that is a whole face of a station (a triangle of I_k or a pentagon of D_k) has its fair share exactly when
N = 20 (or 12). It is held there by RT_k's rhombus planes, which pass through its edges. So these dice are where the Aequi meet the cycle's
stations. The shadow dice of the earlier study are the case where every face is held this way.

### The gaps tested (step 2)

Screen (scripts/gaps.py, double precision) over all 4 039 dice with Resonus in the 31 planes, in the dice frame, which is the Dharma frame
here. For a gap X_in ⊂ X_out:
- s1 is the least size of the die that holds X_in;
- t1 is how far the die at that size reaches toward X_out.
The die fits iff t1 ≤ 1, and touches both iff t1 = 1. Every hit was then checked exactly or in ball arithmetic (scripts/gapcheck.py).

| gap | X_in ⊂ X_out | screen | checked result |
|---|---|---|---|
| (a) | O ⊂ rTI (Progenitors' stations, exact) | 2 fit, 0 touch both | Yo (No.4) = Aequus D·I·RT-62, Ih 4: t1 = 0.95002 (ball arithmetic on certified depths); Goi (No.51) = Aequus D·I·RT-56, Th 40: t1 = 0.99707. Both fit strictly inside and touch O only. **Not closed.** |
| (b) | factor 3 (scripts/factor3.py: r² = 3φ^k or φ^k/3, \|k\| ≤ 12, 60 digits) | 41 dice | exactly the 41 three-fold station dice of Theorem 8, all with r² = 3/φ² for r = d(RT)/d(I). **Exact, by Theorem 8.** The factor is named, but a φ-step cannot produce it. |
| (c) | the DICTO-Star's icosidodecahedron ⊂ the hull of the star (#14 data, coordinates recognised in Q(√5), every piece edge exactly 1) | 3 301 fit, 1 touches both | the D5d station die sid 77 at its station size (D0's two pentagon planes and ten RT0 rhombus planes): s1 = t1 = 1 exactly. 10 of the icosidodecahedron's corners lie on its faces, and 10 of its 20 corners lie on the star's hull (not on star corners). **Touches both, exact.** |
| (d) | D0 ⊂ the hull of the Sunstar (D0 with six Dogstars; 5 placements per die, since the Sunstar has only Th) | 12 548 fit, 131 touch both | all 131 touch for one reason. Their three-fold faces pass through D0's cube corners (planes ±x ± y ± z = 3), and two such planes meet in a line on a square face of the hull (x + y + z = 3 and x − y − z = 3 meet in x = 3, y = −z). The polyhedron behind it is the **regular octahedron \|x\| + \|y\| + \|z\| ≤ 3**: D0's 8 cube corners lie on its 8 faces, and its 6 corners (±3, 0, 0) are the centres of the hull's 6 square faces x = ±3 (the hull corners with x = 3 are the Dogstar corners (3, ±1, ±1); every other corner has \|x\| < 3). **Touches both, exact.** |

**Vacuus and Resonus of the hits (scripts/vacres.py; step 3).**

| polyhedron | corners, edges | Vacuus | Resonus | joins the cycle? |
|---|---|---|---|---|
| D5d station die sid 77 (gap c), exact | 20, 30 | 15 planes: 10 mirrors + 5 others (exact) | 6 planes, inside the 31 | Resonus yes; Vacuus needs 5 planes beyond the 15 |
| regular octahedron \|x\|+\|y\|+\|z\| ≤ 3 (gap d), exact | 6, 12 | the 3 coordinate mirrors, inside the 15 | 4 three-fold planes, inside the 31 | yes, but its size is (3/φ²)·I0's face planes: off the φ ladder |
| Yo (No.4) (gap a, loose) | 120 corners | 90 planes, none a mirror (other planes ≥ 0.15 from every mirror) | 31 | Resonus is the full 31; Vacuus leaves |
| Goi (No.51) (gap a, loose) | 108 corners | 75 planes, 3 of them mirrors | 28 | Resonus yes; Vacuus leaves |

**Observation (exact numbers, no reason claimed).** The number 3/φ² appears twice:
- as (d(RT_k)/d(I_k))² for the station dice of gap (b);
- as the linear size of the octahedron of gap (d) against I0's face planes, since its faces are x + y + z = 3 while I0's are x + y + z = φ².

### Where each gap-closer sits (updated cycle table)

| step | polyhedron | scale on the ladder | Vacuus | Resonus | gap |
|---|---|---|---|---|---|
| 1 | I_k | φ^k·I0 | 15 mirrors | 10 | – |
| 1s | **station dice (Theorem 8)**: whole faces of I_k (or D_k) held by RT_k's planes | step k (same k for both) | varies | inside the 31 | carry (b): φ²r² = 3 |
| 2 | D_k | φ^k·D0 | 15 | 6 | – |
| 2c | **D5d station die sid 77**: D_k's two pentagon planes + ten RT_k planes | step k | 15 planes, 10 mirrors | 6 | touches both sides of (c) at k = 0 |
| 2d | **regular octahedron** on D_k's cube corners | (3/φ²)·φ^k: off the ladder | 3 mirrors | 4 | touches both sides of (d) |
| 3–4′ | Kepler–Poinsot stars | ×φ, ×φ³ | 15 | inherited | – |
| 5 | Dogstar | tips I_{k−2} | 15 (3 its own) | 6 | – |
| 6 | Sunstar | 92 corners | 69 planes | 6 | (d) |
| hub | uniform H3 permutahedron | hexagon centres D_2 | – | 31 | – |
| Dharma | O ⊂ rTI | – | – | – | (a): Yo (No.4), Goi (No.51) fit loosely only |
| return | I_{k+1} | ×φ | 15 | 10 | – |

## Sources checked

papers/2026-11-24-vacuus-resonus/PLAN.md (end); papers/names-audit.md (Dogstar row); papers/2026-10-20-dicto-sunstar/paper.html (#42: Dogstar,
Sunstar, Star Chain Reaction); papers/2026-10-19-kepler-poinsot-pitet/paper.html (#38a); papers/book-golden-cycle/paper.html (Chs 1, 6–10,
open problems: #22, #32, #33, #34, #35a, #35b, #38); papers/consolidation-map.md (Book Four); studies 2026-11-24-resonus,
2026-11-24-permutahedron-leads, 2026-11-19-aequi-complete, 2026-11-20-aequi-two-placements, 2026-11-24-aequi-catalogue-2,
2026-11-24-aequi-certify-extend, 2026-11-24-aequi-table, 2026-10-16-progenitors. Second part: studies 2026-11-24-aequi-exact-dice (shadow-dice
theorem, Alexandrov uniqueness as used there), 2026-11-24-aequi-certify-4404 (certified boxes, split boxes), 2026-11-24-aequi-numberings
and 2026-11-24-aequi-vacuus-scutoids (names, picker numbers), papers/dicto-star (data/dicto-star.json, the #14 pieces). Methods credited:
Alexandrov, Convex Polyhedra (2005), uniqueness and the cell monotonicity behind it; Krawczyk (1969) through the certifying studies;
Van Oosterom and Strackee (1983) for solid angles; arb ball arithmetic (Johansson) through python-flint. No outside source was searched for
this study. The "new"
status of the Vacuus/Resonus statements for stars rests on the prior-art search of the Vacuus–Resonus paper, still to be done.

## LEADS

1. Done: Theorem 8 (42 station dice). Lemma 9 with the shadow count is general. Screen all 15 192 Aequi for an orbit whose faces together are
   bounded by mirror arcs at the fair point; each one gives an exact depth relation.
2. Done for (a): no Aequus of the 31 closes O ⊂ rTI; Yo (No.4) and Goi (No.51) fit loosely. Next: the free-depth families (certify-extend
   LEAD 4), where t1 moves continuously and may cross 1 at a member that touches both.
2b. The 24 equal-depth dice (after the aequi.py fix, 8 of them new): try Lemma 9 plus a mirror swap, as for CIRT-30.
2c. Gap (c): is the D5d station die (sid 77) inside the DICTO-Star itself (the non-convex star), not only inside its hull? Its 5 Vacuus
   planes that are not mirrors: which edges give them, and does a stated extension of the 15 hold them?
2d. Gap (d): is there a polyhedron at a φ-step that touches both D0 and the Sunstar's hull? The octahedron sits at 3/φ². The number 3/φ²
   also appears in gap (b) (Observation above); find the reason or close it as a coincidence.
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
- scripts/aequi.py: corrected 25 Nov (it read the extension's enclosures one orbit out of place); rerun, data/aequi.log.
- scripts/scan42.py → data/scan42.json, scan42.log: screen of the 42 (mirror edges, unions of orbits bounded by mirrors).
- scripts/exact42.py → data/exact42.json, exact42.log: Theorem 8 (exact Q(√5) and ball arithmetic).
- scripts/factor3.py → data/factor3.json, factor3.log: gap (b).
- scripts/dump_stations.py → data/stations.json: O, rTI, I, ID of the Dharma (run from inside study 2026-10-16-progenitors).
- scripts/gaps.py → data/gaps.json, gaps.log: gaps (a), (c), (d), screen.
- scripts/gapcheck.py → data/gapcheck.json, gapcheck.log: the hits, exact or ball arithmetic.
- scripts/vacres.py → data/vacres.json, vacres.log: Vacuus and Resonus of the hits.
- Second part needs python-flint (arb), numpy and scipy, and reads studies 2026-11-24-aequi-exact-dice, -certify-4404, -certify-extend,
  2026-11-19-aequi-complete and papers/dicto-star. Every run took under five minutes on a compute host.
