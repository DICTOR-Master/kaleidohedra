# Polarity and inversion for the big finds: Aequus, the stellation cycle, Vacuus, Resonus, Sphericus (25 November 2026)

DICTO · dictospheres.com · study 2026-11-25-inversions · with Claude (Anthropic).

DICTO's question (25 Nov): do star polyhedra and inversions have value for the big finds (Vacuus, Resonus, Aequus, Tacitus, Sphericus)?
Four claims were tested both ways. Each ends as PROVED POSSIBLE, PROVED IMPOSSIBLE (with its exact scope) or OPEN (with its blocker).
Everything is exact in Q(√5) (pure Python, scripts/q5.py) or certified in ball arithmetic (python-flint arb), unless marked otherwise.

Checks, all FINAL ok: scripts/polar_aequi.py (logs/polar-aequi.log, data/polar-aequi.jsonl.gz), scripts/gram_check.py
(logs/gram-check.log, data/gram-check.json), scripts/uniform_faces.py (logs/uniform-faces.log), scripts/polar_cycle.py
(logs/polar-cycle.log, data/polar-cycle.json). All runs were on the compute hosts, at low priority, each under 5 minutes.

## Verdict

- **(1) The polar of an Aequus.**
  - **Theorem 1 (PROVED, with its normalisation).** Take the polar about the centre from which fairness is measured, in a sphere of any
    radius. At its corner for face k, the polar has curvature exactly equal to that face's solid angle Ω_k. So the polar of every fair die
    has curvature 4π/N at every corner. The radius of the sphere and the size of the die do not matter. The centre does.
  - **Theorem 2 (PROVED).** The polar of a die is fair exactly when the die has the same curvature at every corner. So the polar of an
    Aequus is an Aequus exactly when the die is fair and has equal curvature at every corner. Then each of the two is fair and has equal
    corners, and they form a pair.
  - **PROVED POSSIBLE.** The Platonic polyhedra qualify, and so does every disphenoid (both face- and corner-transitive). So do **exactly 24 of the
    15 192 catalogued Aequi**: all corner curvatures are equal, proved exactly. 21 have congruent corners (exact Gram matrices). The other 3
    have two kinds of corner that are not congruent but both have curvature exactly π/3 (exact identity).
  - Among the 24 are the Aequi CO-14 (Oh 1, the cube–octahedron die), CORD-26 (Oh 4), DI-32 (Ih 1) and D·I·RT-62 (Ih 4). All 24 have three
    faces at every corner, so their polars are fair dice with triangular faces only. For example, the polar of Aequus DI-32 is a fair
    pentakis-dodecahedron-shaped die with 60 faces.
  - **PROVED IMPOSSIBLE for the other 15 168** catalogued Aequi: two of their corners have curvatures certified distinct in ball arithmetic.
    The search is exhaustive over the catalogue. Since every orbit set carries exactly one fair die (aequi-uniqueness), this covers every
    fair die with these orbit sets.
  - The face-transitive Nos. 1233–1235 are the polars of the three permutahedra. Their polars are **not** fair: the permutahedra's faces
    have certified-distinct solid angles (scripts/uniform_faces.py).

- **(2) The cycle under polarity: PROVED.**
  - Polarity in a sphere of radius² φ^m maps the cycle onto itself, for every integer m. In ladder steps it is the reflection
    k ↦ m − c − k, with c = 2 for I ↔ D, c = 3 for the small stellated dodecahedron ↔ great dodecahedron, and c = 5 for the great
    stellated dodecahedron ↔ great icosahedron (Theorem 4).
  - In any other sphere (radius² not a power of φ, for example 3) the polar leaves the ladder.
  - The Vacuus (the 15 mirrors) is kept. The Resonus is exchanged with the corner planes: 10 ↔ 6 for I ↔ D and for the great icosahedron ↔
    great stellated dodecahedron; 6 ↔ 6 for the small stellated ↔ great dodecahedron.
  - Scope: "Vacuus kept" fails outside the six regular members. The compound of five cubes has 30 Vacuus planes, none of them a mirror;
    its polar, the compound of five octahedra, has the 15 mirrors.
- **(3) Stellate, then invert: PROVED, the same cycle and not a second one.** Faceting with the corners fixed gives the four Kepler–Poinsot
  stars again: the dual ladder is the stellation ladder read downwards (steps φ⁻¹ and φ⁻³), so the two meet at every station.
  - Every faceting of the icosahedron has its Vacuus inside the 15 mirrors and its Resonus inside 16 of the 31 hub planes.
  - Facetings of the dodecahedron that use its cube edges or cube face diagonals leave the mirrors (30 planes each). These include the
    compounds of five cubes and of five and ten tetrahedra.
- **(4) Sphere inversion about the centre: PROVED; constant width PROVED IMPOSSIBLE.**
  - Planes through the centre are fixed, so the Vacuus, the Resonus and their Sphericus great circles are unchanged.
  - Each face goes to the sphere on the diameter from the centre to that face's polar corner. Each edge goes to a circle through the
    centre, lying in its Vacuus plate.
  - The inverted body of a convex polyhedron is the union of those balls, which is the pedal body of the polar.
  - It is never convex, so never of constant width. The same holds for the Kepler–Poinsot stars and every star-shaped polyhedral body.
  - The clean property is the link with polarity: at the centre, the inverted body's spheres touch exactly the Resonus planes.

## Frame and words

- Frame of study 2026-11-25-stellation-cycle:
  - I0 = cyclic (0, ±φ, ±1) and D0 = (±1, ±1, ±1), cyclic (0, ±1/φ, ±φ);
  - I_k = φ^k·I0 and D_k = φ^k·D0;
  - SSD(k), GD(k) and GSD(k) are the small stellated, great and great stellated dodecahedra of D_k, and GI(k) is the great icosahedron of
    I_k (corners I_{k+1}, I_{k+1}, D_{k+3}, I_{k+3}).
- **Polar** in the sphere |x|² = R about O: a face plane n·x = h goes to the corner (R/h)·n, a corner v goes to the plane v·x = R, and the
  edge where faces F and G meet goes to the edge joining their two corners. For star polyhedra this is Coxeter's reciprocation (Regular
  Polytopes §6.2; cited, not opened). Wenninger's *Dual Models* builds all of them (cited, not opened).
- **Corner planes** of P: the planes through O at right angles to the lines from O to the corners. **Curvature** of a convex polyhedron at a
  corner: 2π minus the sum of the face angles there (Descartes's angle defect).
- Vacuus, Resonus and Sphericus are as in studies 2026-11-24-resonus and 2026-11-25-plate-harmony. Sphericus is DICTO's name (25 Nov) for
  the spherical view of a plate set: its great circles, plus small circles where the construction has them, and how they cross. Its
  exact definition is still to be fixed with DICTO; the working measures of the plate-harmony study are used.

## (1) The polar of an Aequus

**Setting.** P = {x : u_k·x ≤ d_k}, with unit normals u_k, depths d_k > 0, every face present, and O = 0 inside. Ω_k is the solid angle of
face k seen from O. The polar in the sphere of radius ρ about O is P*_ρ = {y : y·x ≤ ρ² for all x ∈ P} = conv{p_k = ρ² u_k/d_k}.

**Theorem 1 (equal curvature of the polar).** The curvature of P*_ρ at the corner p_k equals Ω_k. If P is fair about O (Ω_k = 4π/N for all
k), every corner of P*_ρ has curvature exactly 4π/N.

*Proof.*
- The curvature of a convex polyhedron at a corner is the area of the set of unit outer normals there, that is, of its normal cone. This is
  the polar spherical polygon of the corner figure: its area is 2π minus the sum of the face angles.
- The normal cone of P*_ρ at p_k is {x : x·p_k ≥ x·p_j for all j}.
- A point x ≠ 0 lies on the cone over face k exactly when x·p_k = max_j x·p_j > 0, because x ∈ F_k means max_j x·u_j/d_j = 1 = x·u_k/d_k.
- Since O is inside P*_ρ, max_j x·p_j > 0 for every x ≠ 0. So the normal cone is exactly the cone over F_k, and its spherical area is Ω_k. ∎

*Normalisation.*
- ρ is free, and so is the scale of P: curvature does not change under scaling.
- The centre is not free. Polarity about any other point changes the corners of the polar and their curvatures, while fairness is
  measured from O (the centroid, which is the centre for every catalogued Aequus).

This is Lemma 1 of #112, formalised in Lean as `solidAngle_eq_curvature` (study 2026-11-22-lean-alexandrov). It is credited there; the
normalisation is stated here. Alexandrov's uniqueness theorem for prescribed normals and curvatures is applied to this polar in
study 2026-11-24-aequi-uniqueness.

*Control.* For all 15 192 dice the polar's curvature at every corner was computed from the polar's own face angles:
- for the 5 636 dice with 60-digit depths, a ball containing 4π/N, of radius below 1e-30;
- for the others (double-precision depths), within 1e-9 of 4π/N.
The die's curvatures add to 4π every time (logs/polar-aequi.log).

**Theorem 2 (when the polar is fair).** P*_ρ is fair about O exactly when P has equal curvature at all its V corners (each 4π/V).
*Proof.* (P*_ρ)*_ρ = P. Apply Theorem 1 to P*_ρ: the solid angle of the face of P*_ρ belonging to the corner v of P is the curvature of P
at v. ∎

So "the polar of an Aequus is an Aequus" means the die is fair **and** has equal curvature at every corner. By Theorem 1 the polar then has
the same two properties.
- Equal curvature holds when the corners form one symmetry orbit, or more generally when their normal cones are congruent.
- Both properties hold for the convex polyhedra that are face- and corner-transitive: the Platonic polyhedra and the disphenoids (Bruckner;
  Grünbaum and Shephard, "noble polyhedra"; cited, not opened). So the class is not empty outside the catalogue either.

**The catalogue of polars (scripts/polar_aequi.py, data/polar-aequi.jsonl.gz).** The sources are the 15 192 certified Aequi:
- the 1232 (Part 1 of aequi-certify-extend);
- the 4 404 of study 2026-11-19 (aequi-certify-4404);
- 5 935 + 336 + 1 375 + 1 910 (Parts 2a and 2b, caps 1–3).

For each die the file records: the polar's corners (N, curvature 4π/N each), its faces (one per corner of the die, with sides = the
corner's degree), its corner radii 1/d per orbit, the number of distinct face distances, its Resonus count (the die's corner lines,
floating point), and the die's curvature classes in ball arithmetic.
- The curvature at a corner of the die is the solid angle of the cone on the unit face normals there. It depends only on the exact
  normals (over Q(√5)) and on the combinatorics. The combinatorics are certified constant on a box round the fair depths by the certify
  studies; here they are rebuilt, and the corner count matches the certified one for every die.

Histogram of the number of certified-distinct curvature values per die: 1: 24, 2: 323, 3: 1 438, 4: 2 698, 5: 2 923, 6: 3 658, 7: 1 812,
8: 1 299, 9: 471, 10: 338, 11: 113, 12: 65, 13: 29, 14: 1.

**Theorem 3 (the catalogue, exhaustive).** Among the 15 192 catalogued Aequi, the polar is fair for exactly these 24. For each of the other
15 168, two corners have certified-distinct curvature, so the polar is not fair.

| source | die (study row) | name | N faces | corners = polar faces (all triangles) | why the curvatures are equal |
|---|---|---|---|---|---|
| 1232 | Ih: O8+I12/20 + D12 (3) | Aequus DI-32, Ih 1 | 32 | 60 | one orbit |
| 1232 | Ih: C6+RT24/30 + O8+I12/20 + D12 (6) | Aequus D·I·RT-62, Ih 4 | 62 | 120 | one orbit |
| 1232 | Oh: C6 + O8 (10) | Aequus CO-14, Oh 1 | 14 | 24 | one orbit |
| 1232 | Oh: C6 + O8 + RD12 (13) | Aequus CORD-26, Oh 4 | 26 | 48 | one orbit |
| 4404 | D10h: C6+RT24/10 + D12/2 (14) | – | 12 | 20 | congruent |
| 4404 | D8h: C6+RD12/8 + C6/2 (15) | – | 10 | 16 | congruent |
| 4404 | D6h: O8/2 + RD12/6 (16) | – | 8 | 12 | congruent |
| 4404 | D5d: C6+RT24/10 + D12/10 + D12/2 (3) (108) | – | 22 | 40 | congruent |
| 4404 | D5h: C6+RT24/5 + D12/2 (188) | – | 7 | 10 | congruent |
| 4404 | D3d: D12/6 + I12/2 (2) (222) | – | 8 | 12 | congruent |
| 4404 | D3h: O8/2 + RD12/3 (477) | – | 5 | 6 | congruent (prism-like; its polar is a fair three-sided bipyramid) |
| 4404 | D2d: C6/2 + O8/4 (784) | – | 6 | 8 | congruent |
| 4404 | D2d: C6/2 + RD12/4 (785) | – | 6 | 8 | congruent |
| 4404 | D2d: C6/4 + C6/2 + RD12/4 (793) | – | 10 | 16 | congruent |
| 4404 | D3: O8+I12/6 + O8/2 (2009) | – | 8 | 12 | two kinds, both exactly π/3 |
| 2a | D2d: C6/2 + D12+D12p/4 (1938, 1939) | – | 6 | 8 | congruent |
| 2a | D2d: C6/2 + I12+I12p/4 (1940, 1941) | – | 6 | 8 | congruent |
| 2a | D2d: C6/2 + RT24+RT24p/4 (1942, 1943, 1944) | – | 6 | 8 | congruent |
| 2a | D2d: I12+I12p/4a + I12+I12p/4b (1967) | – | 8 | 12 | two kinds, both exactly π/3 |
| 2a | D3: O8/2 + I12+I12p/6 (4289) | – | 8 | 12 | two kinds, both exactly π/3 |

*Proof.*
- *Inequality.* The balls of distinct values are disjoint (arb, 200 bits, exact directions), so the inequality is certified.
- *Equality.*
  - "One orbit": the corners form one orbit of the die's frame symmetries.
  - "Congruent" (scripts/gram_check.py): at every corner the Gram matrix of the face normals, taken in cyclic order up to rotation and
    reflection, is the same exact matrix over Q(√5). Congruent cones have equal solid angles.
  - "Two kinds, exactly π/3" (scripts/angles_exact.py): all normals at a corner have squared length 3. So the Van Oosterom–Strackee
    identity tan(E/2) = |a·(b×c)| / (1 + a·b + b·c + c·a) becomes the exact identity 3·T² = D² with D > 0, that is, E = π/3 = 4π/12.
    (The face angles themselves are not rational multiples of π.) ∎

For the four named dice, the polar is a face-transitive fair die of a Catalan type: the tetrakis hexahedron (24 faces), the disdyakis
dodecahedron (48), the pentakis dodecahedron (60) and the disdyakis triacontahedron (120). It is **not** the Catalan polyhedron itself.
- For example, the polar of CO-14 has its apex-to-cube-corner coordinate ratio √3·d(O8)/d(C6) = 1.7566…, where the Catalan tetrakis
  hexahedron has 3/2.
- The Catalans are the polars of the uniform permutahedra. Those are not fair (next paragraph), so by Theorem 2 the Catalans do not have
  equal corners.

**The face-transitive Aequi Nos. 1233–1235** (duals of the three permutahedra; ball arithmetic, scripts/uniform_faces.py). Their polars are
the uniform truncated octahedron, truncated cuboctahedron and truncated icosidodecahedron. In each, the face kinds subtend different solid
angles, each certified distinct from 4π/N:
- truncated octahedron: squares 0.44536, hexagons 1.23677, against 4π/14 = 0.89760;
- truncated cuboctahedron: 0.19534, 0.52101, 1.00903, against 4π/26;
- truncated icosidodecahedron: 0.07039, 0.18452, 0.56369, against 4π/62.
So the polars of Nos. 1233–1235 are not Aequi, and those three dice do not have equal curvature at their corners.
Theorem 1 is confirmed exactly there: the permutahedra's corner curvatures are π/6, π/12 and π/30, that is 4π/24, 4π/48 and 4π/120.

## (2) The stellation cycle under polarity

**Lemma 3 (the polar link holds for star polyhedra).** Let P be a polyhedron, star or convex, with no face plane and no edge line through O.
Let P* be its polar in any sphere about O. Then:
- the Vacuus of P* is the set of planes at right angles to the edge directions of P, and the Vacuus of P is the set of planes at right
  angles to the edge directions of P*;
- the Resonus of P* is the set of corner planes of P, and the corner planes of P* are the Resonus of P.

*Proof.* Let faces F (n_F·x = h_F) and G meet in the edge line L. The polar edge joins the poles (R/h_F)n_F and (R/h_G)n_G. The plane through
O and that edge has normal n_F × n_G, which is the direction of L. Exchanging P and P* gives the second half. A face of P* lies in v·x = R
for a corner v of P. Its Resonus plane is v·x = 0, the corner plane of v. ∎ For convex P this is Theorem 1 of study 2026-11-24-resonus;
convexity is not used.

**Theorem 4 (closure, with exact scales).** For every integer m, polarity in the sphere of radius² φ^m maps:

| member | its polar |
|---|---|
| I_k | D_{m−2−k} |
| D_k | I_{m−2−k} |
| SSD(k) | GD(m−3−k) |
| GD(k) | SSD(m−3−k) |
| GSD(k) | GI(m−5−k) |
| GI(k) | GSD(m−5−k) |

Hence the cycle (all six members at all integer k) is closed under polarity exactly when R ∈ φ^ℤ. The Vacuus of every member and of its
polar is the 15 mirror planes. The Resonus and the corner planes are exchanged.

*Proof.* The face planes of D_k are n·x = φ^{k+2} with n ∈ I0, so their poles are φ^{m−k−2}·I0, the corners of I_{m−2−k}.
- The corners of SSD(k) are φ^{k+1}·I0. Their polar planes are v·x = φ^{m−k−1}, the face planes of D_{m−k−3}. So the polar has the
  corners and the face planes of the stars of D_{m−3−k}.
- Its edges are the poles of the edge pairs. They are the long pairs (pentagram) for the great dodecahedron's reciprocal and the short pairs
  for the small stellated one's, so SSD and GD are exchanged.
- The same computation gives the other rows.
- For R ∉ φ^ℤ, the polar of I_k is (R/φ^{k+2})·D0. That is a ladder member only if R/φ^{k+2} is a power of φ.

Exact check (scripts/polar_cycle.py):
- every row holds as an identity of corner sets, face-plane sets and edge sets, for k = −3…3 and m = −3…5;
- polarity is an involution on every member;
- Lemma 3 holds on every pair, and Vacuus(P) = Vacuus(P*) = the 15 mirrors;
- R = 3 gives the polar of I0 as (3/φ²)·D0, off the ladder (3/φ² is not a power of φ; see #33).
Scale invariance carries the result to all k and m. ∎

**The proper reciprocal (sphere = the member's own midsphere).** Every member's edges touch one sphere, and its radius² is a power of φ:

| member | midsphere radius² | reciprocal in it | corners: member → reciprocal | Resonus · corner planes → polar's |
|---|---|---|---|---|
| I_k | φ^{2k+2} | D_k | I_k → D_k | 10 · 6 → 6 · 10 |
| SSD(k) | φ^{2k+2} | GD(k−1) | I_{k+1} → I_k (×φ⁻¹) | 6 · 6 → 6 · 6 |
| GD(k) | φ^{2k+4} | SSD(k+1) | I_{k+1} → I_{k+2} (×φ) | 6 · 6 → 6 · 6 |
| GSD(k) | φ^{2k+4} | GI(k−1) | D_{k+3} → I_{k+2} | 6 · 10 → 10 · 6 |
| GI(k) | φ^{2k+6} | GSD(k+1) | I_{k+3} → D_{k+4} | 10 · 6 → 6 · 10 |

Every reciprocal pair shares its midsphere (checked). So the classical pairs SSD ↔ GD and GI ↔ GSD come out with exact ladder steps:
- the great dodecahedron reciprocal to the small stellated dodecahedron of D_k is the great dodecahedron of D_{k−1}, its corners shrunk by φ;
- the great icosahedron reciprocal to the great stellated dodecahedron of D_k is the great icosahedron of I_{k−1}.

**Scope: Vacuus kept only where edges and Vacuus normals agree.** By Lemma 3 the Vacuus is kept under polarity exactly when the set of edge
directions of P equals the set of normals of P's Vacuus planes. This holds for the six regular members: their edges run along the 15 two-fold
axes, and the Vacuus normals are those axes. It fails for the compound of five cubes, a faceting of D0 (its five cubes found exactly among
D0's corners):
- five cubes: Vacuus 30 planes, none a mirror (each cube's six diagonal planes); Resonus 15 (two-fold);
- its polar in the sphere φ², the compound of five octahedra (a stellation of the icosahedron; corners the 30 points φ²·(two-fold
  directions), radius² φ⁴): Vacuus the 15 mirrors, Resonus 10 (three-fold).

So the claim, as stated for the cycle, is proved, with its scope: it holds for the regular members and not for the compounds.

**The Dogstar under polarity (partial).** The Dogstar's 12 face planes are those of its core D_{k−3}. So its polar is a faceting of the
icosahedron I_{m+1−k} (sphere radius² φ^m), with 12 face planes on the five-fold axes and 8 on the cube diagonals (Th).
- By Lemma 3, the polar's Resonus is the Dogstar's corner planes: 6 five-fold and 4 three-fold, 10 planes.
- Its Vacuus lies inside the 15 mirrors. Every Dogstar edge lies on a line where two of the core's planes meet, and all such lines run
  along two-fold axes (the I0 chord table below, read through Lemma 3).
- Whether it is all 15 is **OPEN**: the Dogstar's edge list was not kept by the cycle study.

## (3) Stellate, then invert: the faceting ladder

Polarity turns the cells of the face-plane arrangement of D_k (its stellations) into polyhedra on the corners of its polar I_{m−2−k} (its
facetings), and back. The tables list every chord and every plane available to a faceting with the corners fixed (exact, data/polar-cycle.json).

**Facetings of I0** (12 corners):

| chord² | chords | Vacuus plates (normal a × b) | edge directions |
|---|---|---|---|
| 4 (edges) | 30 | 15, all mirrors | two-fold |
| 6 + 2√5 (second neighbours) | 30 | 15, all mirrors | two-fold |

| plane | distance² | corners on it | planes |
|---|---|---|---|
| three-fold (the faces) | (3 − √5)/6 | 3 | 20 |
| five-fold (pentagons) | (5 + √5)/10 | 5 | 12 |
| three-fold (great icosahedron triangles) | (7 + 3√5)/6 | 3 | 20 |

The antipodal chords pass through O and carry no Vacuus plate.

**Theorem 5 (I).** Every faceting of the icosahedron (corners those of I_k) has its Vacuus inside the 15 mirrors and its Resonus inside
the 10 three-fold and 6 five-fold planes, so inside the 31 hub planes. *Proof:* the two tables are complete (all pairs and all triples of
the 12 corners). ∎

**Facetings of D0** (20 corners):

| chord² | chords | Vacuus plates | edge directions |
|---|---|---|---|
| 6 − 2√5 (edges) | 30 | 15, all mirrors | two-fold |
| 4 (cube edges) | 60 | 30, **none a mirror** | two-fold |
| 8 (cube face diagonals) | 60 | 30, **none a mirror** | not on an axis |
| 6 + 2√5 | 30 | 15, all mirrors | two-fold |

Plane classes: 12 + 12 five-fold, 20 + 20 three-fold, 30 two-fold (4 corners: the cube faces), and three classes of 60 planes in general
position (3 corners each).

**Theorem 5 (D).** A faceting of the dodecahedron has its Vacuus inside the 15 mirrors exactly when it uses no cube edge and no cube face
diagonal. The compounds of five cubes (cube edges) and of five and ten tetrahedra (face diagonals) leave the mirrors. A faceting that uses
a general-position plane has a Resonus plane outside the 31.

**Theorem 6 (the dual ladder is the cycle read downwards).** With the corners fixed:
- the icosahedron I_k is faceted by the small stellated and great dodecahedra (face planes of D_{k−1}) and by the great icosahedron (face
  planes of I_{k−3});
- the dodecahedron D_k is faceted by the great stellated dodecahedron (face planes of D_{k−3}).

These are SSD(k−1), GD(k−1), GI(k−3) and GSD(k−3), the same polyhedra as the stellation ladder (checked exactly, k = −2…2). Stellation climbs
φ and φ³ and faceting descends φ⁻¹ and φ⁻³. Polarity (Theorem 4) carries one onto the other, with the order reversed.
So **there is no second cycle**: the faceting ladder is the stellation cycle traversed backwards. The two meet at every station, with the
same Vacuus (15 mirrors), the same Resonus and the same φ-scales. New stations appear only off the regular members, among the compounds
above, and those leave the Vacuus. ∎

## (4) Sphere inversion about the centre

ι(x) = R·x/|x|², the inversion in the sphere |x|² = R about O.

**Theorem 7.**
- (a) *Central planes are fixed.* ι(x) is a positive multiple of x, so every plane through O is mapped onto itself. Hence every Vacuus
  plate and every Resonus plane is unchanged, the image of each edge lies in that edge's own Vacuus plate, and the Sphericus of the plate
  sets (their great circles) is unchanged.
- (b) *Faces.* The face plane n·x = h (h > 0) goes to the sphere |x|² = (R/h)·n·x through O. Its centre is (R/2h)·n, **half of the face's
  polar corner** (R/h)·n, and its diameter is the segment from O to that corner. Its tangent plane at O is n·x = 0, **the face's Resonus
  plane**.
- (c) *Edges.* An edge line at distance δ from O, with foot f, goes to the circle through O and ι(f), of diameter R/δ. It lies in the
  edge's Vacuus plate, and its tangent at O is parallel to the edge.
  - Parallel edges give circles that touch at O.
  - Edge lines that meet at a point x give circles that cross again at ι(x), at the same angle (inversion keeps angles).
- (d) *The body.* For a convex polyhedron P with O inside, the inverted body K = ι(outside of P) ∪ {O} is the union of the closed balls
  on the diameters [O, p_k], one for each corner p_k of the polar P* in the same sphere. Its radial function is the support function of P*,
  so K is the pedal body of P*.
- (e) *Not convex, so never of constant width.* At an interior point of the image of an edge, two distinct face spheres cross
  transversally, and K's angle there is 2π − α > π, where α is P's dihedral angle. So K is not convex, and a body of constant width is
  convex.
  - The same holds for every polyhedral body that is star-shaped about an interior point O, the visible surfaces of the Kepler–Poinsot stars
    included. Any convex edge of the body gives such a crease, and every polyhedral body has one: at a corner of its convex hull, the corner
    figure is a spherical polygon in an open hemisphere, and such a polygon has a convex corner.

*Proof.*
- (a) is immediate.
- (b): substituting x = R·y/|y|² into n·x = h gives |y|² = (R/h)·n·y.
- (c): the line is the meet of two face planes, so its image is the meet of two spheres through O inside the plane through O and the line.
  The nearest point f goes to the farthest point ι(f).
- (d): the open half-space n_k·x > h_k goes to the open ball on [O, (R/h_k)n_k]. The outside of P is the union of these half-spaces. For a
  unit vector u, the boundary of K in direction u is at distance R/r_P(u) = R·max_k(n_k·u/h_k) = max_k p_k·u = h_{P*}(u).
- (e): two distinct spheres through O and a common point q ≠ O cannot touch at q. Their centres would lie both on the common normal at q
  and on the plane bisecting O and q, and that line meets that plane once. So the crossing is transversal. A point inside an edge of P is
  in no open half-space n_k·x > h_k, so its image lies on ∂K. Near it, K is the union of two balls crossing at angle π − α (conformality),
  so its inner angle is 2π − α > π. A convex set has inner angles ≤ π. ∎

The pedal identity was checked exactly at every corner direction of the tetrahedron, cube, octahedron, icosahedron and dodecahedron. The
link between inversion and polarity through pedal curves is classical in the plane (the pedal of a curve is the inverse of its polar
reciprocal: Salmon, *Higher Plane Curves*; Lockwood, *A Book of Curves*; cited, not opened).

**The Sphericus of the inverted bodies (exact; each inverted in its own midsphere, so every edge midpoint is fixed).** Every face sphere passes
through O, with its centre at half the reciprocal's corner. Every edge circle passes through O with diameter² = R, on the diameter from O to an
edge midpoint. Crossing angles are given by cos², with 1/4, (3 + √5)/8 and (3 − √5)/8 for 60°, 36° and 72°.

| polyhedron | R | face spheres (radius²) | edge circles / planes (= Vacuus) | lines at O (circles each) | crossings besides O | crossing angles cos² | sphere-to-sphere cos² |
|---|---|---|---|---|---|---|---|
| tetrahedron | 1 | 4 (3/4) | 6 / 6 | 6 (1) | 4 corner images, 3 arcs each | 1/4 | 1/9 |
| cube | 2 | 6 (1) | 12 / 6 | 3 (4) | 8 corner images, 3 arcs | 0 | 0 |
| octahedron | 1/2 | 8 (3/16) | 12 / 3 | 6 (2) | 6 corner images, 4 arcs | 0, 1/4 | 1/9 |
| icosahedron | φ² | 20 (3/4) | 30 / 15 | 15 (2) | 12 corner images (5 arcs); 20 points where 3 full circles cross, no arcs | 1/4, (3 ± √5)/8 | 5/9 |
| dodecahedron | φ² | 12 ((5 + √5)/8) | 30 / 15 | 15 (2) | 20 corner images (3 arcs); 12 points of 5 full circles, no arcs | same | 1/5 |
| small stellated dodecahedron | φ² | 12 ((5 + √5)/8) | 30 / 15 | 15 (2) | 12 corner images (5 arcs); **20 points where 3 arcs cross** (D0's corners) | same | 1/5 |
| great dodecahedron | φ⁴ | 12 ((25 + 11√5)/8) | 30 / 15 | 15 (2) | 12 corner images (5 arcs); 20 points of 3 full circles, no arcs | same | 1/5 |
| great stellated dodecahedron | φ⁴ | 12 ((25 + 11√5)/8) | 30 / 15 | 15 (2) | 20 corner images (3 arcs); **12 points where 5 arcs cross** | same | 1/5 |
| great icosahedron | φ⁶ | 20 ((141 + 63√5)/8) | 30 / 15 | 15 (2) | 12 corner images (5 arcs); **20 points where 3 arcs cross** | same | 5/9 |

What the inverted Sphericus adds, exactly:
- Opposite edges give two circles in one Vacuus plate that touch at O. So the 30 circles meet at O along the 15 two-fold lines, two by two.
- The four stars and their cores share one set of crossing angles (60°, 36°, 72°).
- The stars differ from their cores only in the extra crossing points. There the arcs themselves cross: these are the false corners of the
  star faces, mapped by ι.
- The inverted icosahedron and the inverted dodecahedron (the dual pair, one midsphere) have the same 30 circle diameters. Each I edge and
  the D edge crossing it at a midpoint m give two equal circles on the one diameter [O, m], in two planes at right angles.

**Tacitus and Sphericus under inversion.** Both are measured on central plates or on directions from O. Inversion fixes every direction
from O, so it leaves both unchanged (Theorem 7(a)). Inversion adds nothing new to them; what it adds is the small circles of item (4).

## Sources checked

- Studies:
  - 2026-11-24-resonus (Theorem 1, polar link);
  - 2026-11-25-stellation-cycle (frame, stars, Theorems 1–8);
  - 2026-11-24-vacuus-resonus-catalogue;
  - 2026-11-24-aequi-uniqueness and #112 (Lemma 1, polar identity; Lean `solidAngle_eq_curvature`);
  - 2026-11-24-aequi-certify-extend and -certify-4404 (data, certified boxes, combinatorics);
  - 2026-11-24-aequi-exact-dice (shadow dice);
  - 2026-11-25-plate-harmony (Sphericus measures).
- Literature, cited, not opened:
  - Coxeter, *Regular Polytopes* (reciprocation, Kepler–Poinsot pairs);
  - Wenninger, *Dual Models* (1983);
  - Bruckner (1906) and Grünbaum & Shephard on noble polyhedra (Platonic polyhedra and disphenoids are the convex polyhedra both
    face- and corner-transitive);
  - Salmon and Lockwood (pedal = inverse of polar reciprocal);
  - Descartes (angle defect, total 4π);
  - Alexandrov (uniqueness for prescribed normals and curvatures).
- Method credits: Van Oosterom–Strackee solid-angle formula (as in the certify study); Krawczyk certification (earlier studies).

## LEADS

1. **Equal curvature beyond symmetry and congruence.** In 453 dice two corners have curvatures equal to 1e-50 in ball arithmetic but
   non-congruent normal cones. Every such die also has certified-distinct values elsewhere, so Theorem 3 does not depend on them.
   - Find the exact reason, as the π/3 identity did for the three dice: mirror-triangle counts, or tan(E/2) identities.
   - Status: OPEN; blocker: an exact identity for each pair (data/gram-check.json `undecided`).
2. **The 24 polar pairs as dice.** The polars of the 24 are new fair dice (face-transitive for the four named ones, triangle-faced for all).
   They are not in the numbered catalogue. Their Vacuus and Resonus follow from Lemma 3: Resonus = the die's corner lines, Vacuus = planes
   at right angles to the die's edges. Status: OPEN (not computed exactly here).
3. **Equal-curvature fair dice outside the catalogue.** Are there any besides the noble polyhedra and polars of the 24, for example in the
   continuous off-axis families? Status: OPEN; blocker: an equal-curvature condition along each family (one equation per corner class).
4. **The Dogstar's polar:** its exact Vacuus count. It lies inside the 15 mirrors; equality is OPEN, blocked by the Dogstar's edge list
   (rerun cycle.py's arrangement and keep its edges).
5. **The compound branch of the faceting ladder.** Five cubes, five and ten tetrahedra, and their polars (five octahedra, five and ten
   tetrahedra as stellations of I) are stations off the regular cycle. Their Vacuus leaves the mirrors. Do they make a cycle of their own
   under stellate-and-facet? Status: OPEN.
6. **Inversion about other points.** With O outside the body, the image is bounded by spheres through O, some convex and some concave. The
   constant-width question is OPEN there; this study proved impossibility only for an interior centre.
7. **Sphericus with small circles.** The inverted bodies give exact small-circle networks (item 4 table). Fixing the exact definition of
   Sphericus with DICTO decides whether they belong to it.

## Proposals for DICTO (names are his; nothing here is named)

- A word for a polyhedron that is both fair (equal solid angles of its faces) and has equal curvature at every corner, so that its polar
  is fair too. 24 Aequi, the Platonic polyhedra and the disphenoids are of this kind.
- A word for the polar die of such an Aequus (for example the 60-face polar of Aequus DI-32, and the 24-face polar of Aequus CO-14).
- A word for the inverted body: the union of the balls on the diameters from the centre to the polar's corners (the pedal body of the
  polar).
