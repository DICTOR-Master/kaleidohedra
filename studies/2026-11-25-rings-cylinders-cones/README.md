# Rings, cylinders and cones: what the materials of DICTO's builds add to zero-thickness geometry (25 November 2026)

DICTO · study 2026-11-25-rings-cylinders-cones · with Claude (Anthropic).

> **Status box.** Study note, not published. Every item ends PROVED POSSIBLE, PROVED IMPOSSIBLE (with its scope) or OPEN (with its
> blocker). The proofs below need no computer. The per-polyhedron tables (163 catalogue polyhedra, the Dogstar, the Sunstar and the
> 1232 numbered Aequi) are **not yet run**. The scripts are written and the job plans are filed, but the job runner's pre-flight gate
> refused the launch on a keyword match with an unrelated ledger entry (no. 235, about McCooey's catalogue files). Setting the
> override was not allowed to this agent, so it waits for DICTO's or the coordinator's word.
> Resume: add the `ledger_override` line to `~/dicto-alerts/plans/rings-pilot.plan` and `rings-all.plan`, then run the commands under
> "Runs" below.

The question (DICTO, 25 Nov): do the materials of his builds carry geometry that changes our zero-thickness assumptions? He builds
as Vacuus and hulls, skeletons, empty (DICTO 24 Nov), using bottle security rings (B1NR, rings tied at 3 points), cylinders (bottles,
struts) and cones (necks, caps). The facts used here come only from DICTO's statements and the ring-fin reading of study
2026-11-24-vacuus-build-renders. In that reading, each ring is the incircle of its fin (the triangle O, a, b of an edge ab) and lies
in the fin's plane; the cuboctahedron build has 24 rings and 12 ties. Nothing else about the builds is assumed.

## Verdict

| # | Item | Status |
|---|---|---|
| 1a | Ring lemmas: radius, tie points; in a convex build, rings never cross or link and meet only at tie points | **PROVED** |
| 1b | Every polyhedron with all edges equal and all corners equidistant from O (5 Platonic, 13 Archimedean, 20 uniform prisms and antiprisms n = 3–12) takes one ring size, and every ring touches all its neighbours at the struts: V ties, E rings | **PROVED POSSIBLE** |
| 1c | Bipyramids (the catalogue's polars of the uniform prisms): equal rings only for n = 4 (the octahedron), for every n ≥ 3 | **PROVED IMPOSSIBLE** for n ≠ 4 |
| 1d | All-tie builds need every edge to subtend the same angle at O; equal rings + all ties ⇔ r and t constant | **PROVED** (necessary condition) |
| 1e | Johnson polyhedra about their circumcentre, when it lies inside: one ring size, all ties (by 1b) | **PROVED POSSIBLE** for each such polyhedron; *which* ones: OPEN (exact check written, not run) |
| 1f | Catalan (11 not edge-transitive), trapezohedra, Johnson about the catalogue centres: equal rings or not, ratio sets | **OPEN**: job not launched (gate) |
| 1g | Kepler–Poinsot stars: the great dodecahedron uses the icosahedron's edges, so its build is the icosahedron's; in the small stellated dodecahedron, the great stellated dodecahedron and the great icosahedron, two rings pass through each other at every crossing of edges | **PROVED POSSIBLE** (GD) / **PROVED IMPOSSIBLE** (SSD, GSD, GI) |
| 1h | Dogstar, Sunstar, the 1232 Aequi | **OPEN**: job not launched |
| 2a | "Each ring, seen from the centre, is a small circle" | **PROVED IMPOSSIBLE** for fin rings: each is seen edge-on, as exactly its edge's arc |
| 2b | Tie points (= corner directions) against Tammes: tetrahedron, octahedron, **square antiprism**, icosahedron and **snub cube** builds put their ties at the proved Tammes optima (N = 4, 6, 8, 12, 24); every other uniform build falls short (table) | **PROVED** for N = 4, 6, 8, 12; N = 24 agrees to 4 decimals with Robinson's optimum (cited) |
| 2c | The cuboctahedron's 12 ties are the kissing arrangement of the face-centred cubic packing (neighbours exactly 60° apart) | **PROVED** |
| 3a | Hollow core: struts of radius r on rays at least θ apart are disjoint outside the ball of radius R = r / sin(θ/2), and this is the least such R. Flat-cut ends: a = r cot(θ/2) | **PROVED** |
| 3b | B1NR cube (8 centre struts): R = √3 r, a = √2 r | **PROVED** |
| 3c | No polyhedron does better than R = √(3/2) r, reached only by the regular tetrahedron about its centre | **PROVED** |
| 3d | Uniform frames: R/r = 2R_c/ℓ (circumdiameter over edge), a/r = 2ρ_mid/ℓ | **PROVED** |
| 4a | Round-fairness as defined (equal solid angles of the cones over the ring discs) | **PROVED** degenerate: every fin ring's cone is flat (solid angle 0), so every build is trivially round-fair and the Aequus question is empty |
| 4b | With the band height of a real ring (a short tube, as modelled in the render study), the cones are no longer flat; congruent-fin builds are then round-fair | **PROVED POSSIBLE** (1b builds); Aequi: **OPEN** |

**Conclusion.** The materials change the zero-thickness picture in two exact ways.
- Rings: one ring size forces the frame to be "all edges alike as seen from O". Every uniform polyhedron passes. Most other
  polyhedra are ruled out, the bipyramids for all n. Seen from the centre, the ring build is the edge net itself, and its ties
  are the corners. Five uniform builds put those ties exactly at the proved best spreads of 4, 6, 8, 12 and 24 points.
- Struts: a strut of radius r cannot reach the centre. Every frame has an empty core of radius r / sin(θ/2). The B1NR cube's core
  is √3 r, and nothing beats the tetrahedron's √(3/2) r.

## 1. The equal-ring rule

**Setting.** P is a convex polyhedron with O inside. For an edge ab the fin is the triangle O, a, b, and its ring is the fin's incircle
(render study). Put A = |Oa|², B = |Ob|², C = |ab|².

**Lemma 1 (ring and tie point).**
- The ring has radius r = 2·area / perimeter = √(4AB − (A+B−C)²) / (2(√A + √B + √C)).
- It touches the spoke Oa at distance t = (√A + √B − √C)/2 from O, and Ob at the same distance. This t is the tangent length from O.
- *Proof.* These are the standard incircle facts. The two tangent lengths from a vertex of a triangle are equal, and the three of
  them sum to the half-perimeter.

**Lemma 2 (convex builds: no crossing, no linking).** Two rings of a convex build meet only if their fins share a spoke Oa and have the
same t there. They then touch at the single point at distance t on Oa.
- *Proof.* The fin of ab is the union of the segments from O to the points x of the edge ab. Suppose λx = μy with x on edge e₁,
  y on edge e₂ and λ, μ > 0. The ray from O through x meets the boundary of P only once, so x = y, and this point lies on e₁ ∩ e₂,
  a common corner. So two fins meet only along a common spoke (or at O).
- A ring lies in its closed fin and stays off O, because an incircle does not reach the vertices of its triangle. So two rings can
  only meet on a common spoke.
- Each ring meets the line of that spoke only at its tangency point. So the rings meet iff the two t agree, and then in that one point.

**Theorem 1 (one ring size, all ties).** Suppose every edge has length ℓ and every corner lies at distance R from O. Then:
- all fins are congruent (sides R, R, ℓ), so all rings have one radius r = (ℓ/2)·√(4R² − ℓ²)/(2R + ℓ);
- every ring touches the spokes at t = R − ℓ/2;
- at each corner v, the deg(v) rings of the fins on Ov all touch at one point (a tie). The build has V ties, E rings and
  Σ_v C(deg v, 2) touching pairs, and by Lemma 2 there are no other contacts.
- *Proof.* Lemma 1 with A = B = R² and C = ℓ², then Lemma 2.
- *Check against the render study.* For the cuboctahedron: 12 ties, 4 rings each, 72 pairs, r = √6/6 at ℓ = √2. For the
  dodecahedron: 20 ties, 3 rings each, 60 pairs. Both agree with `check.py` there.
- *Scope.* This covers the 5 Platonic, the 13 Archimedean, the 10 uniform prisms and the 10 uniform antiprisms (n = 3–12) of the
  catalogue: 38 polyhedra. It also covers any equal-edged polyhedron built about a circumcentre inside it (1e).

**Theorem 2 (what "all ties" needs).**
- All ties (every ring touches every neighbouring ring at both of its struts) ⇔ t is the same on every edge, since the edge graph
  is connected.
- Equal rings and all ties ⇔ r and t are both constant. Then tan(∠aOb / 2) = r / t is constant, so **every edge subtends the same
  angle at O**. This is a necessary condition, easy to test. It is not sufficient for congruent fins: with r and t fixed, a can still
  slide along its spoke.

**Theorem 3 (bipyramids: equal rings only for the octahedron).** Take the n-gonal bipyramid of the catalogue: the polar, in the unit
sphere, of the uniform prism with unit edges. Its fins have equal inradius iff n = 4.
- *Setup.* Put x = π/n. The apexes are at height 2 and the equator at radius q = 2 tan x.
- *The two kinds of fin.*
  - An apex fin has a right angle at O, so r₁ = (2 + q − √(4+q²))/2 = 1 + tan x − sec x.
  - An equator fin is isosceles with legs q and apex angle 2x, so r₂ = 2 sin²x / (1 + sin x).
- *Reduction.* Put σ, κ = sin(x/2), cos(x/2). Then r₁ − r₂ has the sign of (cos x + sin x − 1)(1 + sin x) − 2 sin²x cos x, and
  this equals 2σ(κ−σ)(κ+σ)·[(κ+σ) − 4σκ²].
- *The bracket.* Divide it by κ³ and put τ = tan(x/2). It becomes τ³ + τ² − 3τ + 1 = (τ − 1)(τ² + 2τ − 1).
- *Roots.* On 0 < τ ≤ tan(π/6) the only root is τ = √2 − 1 = tan(π/8), that is x = π/4 and n = 4. ∎
- *Ties at n = 4.* The ties hold there too, as the octahedron is in Theorem 1.

**Kepler–Poinsot stars (1g).** All four stars have equal edges and all their corners on one sphere, so all their fins are congruent.
But they are not convex, and Lemma 2 fails for them.
- *Great dodecahedron.* It has the icosahedron's 12 corners and 30 edges (the shared edge arrangement), so its ring build *is* the
  icosahedron's: possible.
- *Small stellated dodecahedron, great stellated dodecahedron.* Their faces are pentagrams, so they have edges that cross at inner
  points w.
  - The reflection of the pentagram in its line through w swaps the two crossing edges. It is the restriction of a mirror plane of
    the icosahedral group, and that plane contains O and w.
  - So the mirror swaps the two fins and their rings, and it fixes the ray Ow.
  - The ray Ow runs inside both fins, so it cuts the first ring in two points. The mirror fixes these points, so they lie on the
    second ring too.
  - So the two rings meet in two points, which means they pass through each other. Closed rings cannot do this, so these builds are
    **impossible**.
- *Great icosahedron.* It shares the small stellated dodecahedron's edge arrangement, so it is impossible too.
- *Pending.* `scripts/stars.py` checks these counts exactly, and also the Dogstar and the Sunstar.

**Pending (1e, 1f, 1h).** `scripts/rings_catalogue.py` gives, for every catalogue polyhedron and centre:
- its fin classes (exact keys) and its distinct ring radii, with their ratios to the largest;
- its tangent lengths and its central angles;
- for the Johnson polyhedra, whether a sphere passes through all corners with its centre strictly inside, by an exact linear solve.
  We expect the Johnson polyhedra cut from uniform polyhedra with their centre kept (J11, J27, J34, J37, J62, J63, J72–J83). This
  list is a **conjecture** until the run.

Distinct values are certified by interval arithmetic. A tie of two non-congruent classes is reported as UNDECIDED, never claimed.
`scripts/aequi_rings.py` screens the 1232 numbered Aequi in double precision, with a stated margin.

## 2. The rings seen from the centre

**Theorem 4 (edge-on).** A fin ring lies in a plane through O. Seen from O, it covers exactly the arc of its edge ab and has zero
solid angle.
- *Proof.* The lines from O tangent to the ring are the spokes Oa and Ob, by Lemma 1. So the cone of sight lines to the ring is
  the angle aOb in the fin plane.
- *Consequences.*
  - Seen from O, the build is the radial image of the edge net, and its ties are the corner directions.
  - The reading "each ring is a small circle on the sphere" is **impossible** for fin rings. A small-circle reading would need rings
    lying across the radius, for example in hull faces. That is not one of DICTO's stated builds, so it stays a LEAD.

**Tie points against Tammes.** For a Theorem 1 build, the ties are the N corner directions. Their least angle is the edge arc
θ = 2 arcsin(ℓ/2R_c). It is the least angle between any two corners, because for points on a sphere the nearest pairs are Delaunay
edges, which are hull edges or diagonals of faces, and the diagonals of regular faces are longer than ℓ.

Comparison values:
- Tammes (1930) asked for the largest least angle of N points on the sphere. It is proved for N = 3–14 and 24:
  - Fejes Tóth (1943): N = 4, 6, 12;
  - Schütte and van der Waerden (1951): N = 5–9;
  - Danzer (1963/1986): N = 10, 11;
  - Musin and Tarasov: N = 13 (2012) and N = 14 (2015);
  - Robinson (1961): N = 24.
- Best known values for other N: Sloane's tables of spherical packings (Hardin, Sloane, Smith). The files `pack.3.N.txt` were
  downloaded and their least angles computed (`scripts/sloane_angles.py`, `data/sloane-min-angles.json`). They agree with the
  proved optima where those exist.

| build | N | tie spread θ | Tammes / best known | at the optimum? |
|---|---|---|---|---|
| tetrahedron | 4 | 109.4712° | 109.4712° (proved) | **yes** |
| octahedron (= 3-antiprism) | 6 | 90° | 90° (proved) | **yes** |
| 3-prism | 6 | 81.7868° | 90° | no |
| cube (= 4-prism) | 8 | 70.5288° | 74.8585° (proved) | no |
| **square antiprism** | 8 | 74.8585°, cos = (2√2 − 1)/7 exactly | (2√2 − 1)/7 (Schütte–van der Waerden) | **yes, exact** |
| 5-prism, 5-antiprism | 10 | 60.8928°, 63.4349° | 66.1468° (proved) | no |
| icosahedron | 12 | 63.4349° | 63.4349° (proved) | **yes** |
| cuboctahedron | 12 | 60° | 63.4349° | no, but the fcc kissing arrangement |
| truncated tetrahedron; 6-prism; 6-antiprism | 12 | 50.4788°; 53.1301°; 54.7356° | 63.4349° | no |
| dodecahedron; 10-prism; 10-antiprism | 20 | 41.8103°; 34.3441°; 34.7466° | 47.431° (best known) | no |
| **snub cube** | 24 | 43.6908° | 43.6908° (proved, Robinson) | **yes, to 4 decimals** (exact identity cited, not re-proved) |
| truncated octahedron; truncated cube; rhombicuboctahedron; 12-prism; 12-antiprism | 24 | 36.8699°; 32.6499°; 41.8820°; 29.0216°; 29.2614° | 43.6908° | no |
| icosidodecahedron | 30 | 36° | 38.5971° | no |
| truncated cuboctahedron | 48 | 24.9178° | 30.7628° | no |
| truncated icosahedron; truncated dodecahedron; rhombicosidodecahedron; snub dodecahedron | 60 | 23.2814°; 19.3874°; 25.8786°; 26.8213° | 27.1928° | no |
| truncated icosidodecahedron | 120 | 15.1121° | 19.324° | no |

- *Values.* The θ values come from the closed-form circumradii, in double precision (`data/uniform-ties.txt`). The exact versions
  come out of `rings_catalogue.py` when it runs.
- *Square antiprism, exact.* R² = 1/2 + 1/(4√2) at unit edge, so cos θ = 1 − 1/(2R²) = 1/(2√2 + 1) = (2√2 − 1)/7. This is
  Schütte and van der Waerden's optimum. The best 8 points are therefore the tie points of the uniform square antiprism ring build.
- *The "no" verdicts.* Each "no" is proved: a better arrangement exists, either a proved optimum or a coordinate file.
- *Kissing (2c).* At 60° the chords between neighbouring tie directions equal the radius of their sphere. So unit balls centred at
  twice the 12 cuboctahedron tie directions touch a central unit ball and their 4 neighbours each. This is the arrangement of the
  face-centred cubic packing, one of the configurations of the kissing number 12 (Newton–Gregory problem; proved by Schütte and van
  der Waerden 1953).
  - Every build with θ ≥ 60° gives a kissing arrangement of N balls: tetrahedron, octahedron, 3-prism, cube, square antiprism,
    5-prism, 5-antiprism, icosahedron, cuboctahedron.
  - Only the cuboctahedron has touching neighbours.
- *Gaps.* The empty part of the sphere between rings is the radial image of the faces. In the Tammes sense, the slack is the column
  "Tammes − θ".

## 3. The hollow core

**Theorem 5 (core radius).** Take two struts, solid cylinders of radius r around the rays from O in unit directions u, v at angle
θ ∈ (0, π).
- (a) Every point within r of both rays has |p| ≤ r / sin(θ/2). Equality holds on the bisector.
- (b) The same holds for the farthest extent along the axis of the region common to both cylinders: it is r·cot(θ/2), reached in the
  plane of the axes.
- Hence, for a frame whose struts are at least θ_min apart:
  - struts cut on the sphere of radius R(r) = r / sin(θ_min/2) about O are pairwise disjoint, and no smaller sphere will do;
  - struts with flat ends need ends at distance a(r) = r·cot(θ_min/2) from O.
  - The empty core is the ball of radius R (or a).

*Proof of (a).* Let p have angles α and β to the rays u and v.
- If α ≥ π/2, the distance from p to the ray u is |p|. So for |p| > r, both α and β are below π/2.
- Then |p| sin α ≤ r and |p| sin β ≤ r.
- On the sphere α + β ≥ θ, so max(α, β) ≥ θ/2, with θ/2 < π/2.
- So |p| ≤ r / sin(θ/2). The bisector point at that distance is within r of both rays.

*Proof of (b).* Put u = (1, 0, 0) and v = (cos θ, sin θ, 0), and take p = (x, y, z) with y² + z² ≤ r².
- Then dist(p, line v)² = (x sin θ − y cos θ)² + z².
- So x sin θ ≤ r + y cos θ ≤ r(1 + cos θ), that is x ≤ r cot(θ/2). Equality holds at (r cot(θ/2), r, 0). ∎

**B1NR cube (3b).** The 8 centre struts run to (±1, ±1, ±1). The least angle is between neighbouring corners, cos θ = 1/3, so
sin(θ/2) = 1/√3 and cot(θ/2) = √2. This gives **R = √3 r** (sphere-cut) and **a = √2 r** (flat ends). The two centre struts of a
long diagonal are opposite (180°) and never meet.

**Theorem 6 (the tetrahedron has the smallest core).** Any N ≥ 4 strut directions u_i have a pair with u_i·u_j ≥ −1/(N−1).
- So R ≥ r / sin(½ arccos(−1/(N−1))) ≥ √(3/2) r.
- Equality holds only for N = 4 with all u_i·u_j = −1/3: the regular tetrahedron about its centre.
- *Proof.* 0 ≤ |Σu_i|² = N + Σ_{i≠j} u_i·u_j, so the average of the u_i·u_j over the N(N−1) ordered pairs is at least −1/(N−1).
  This is the simplex bound (Rankin 1955). A polyhedron with O inside has N ≥ 4 corners. ∎

**Theorem 7 (uniform frames).** For the Theorem 1 polyhedra, θ_min is the edge arc (Section 2). So R/r = 1/sin(θ/2) = 2R_c/ℓ, the
circumdiameter in edge units, and a/r = cot(θ/2) = 2ρ_mid/ℓ, with ρ_mid the midradius.

Values (double precision, `data/uniform-ties.txt`):

| frame | R/r |
|---|---|
| tetrahedron | 1.2247 = √(3/2) |
| octahedron | 1.4142 = √2 |
| 3-prism | 1.5275 |
| square antiprism | 1.6453 |
| cube | 1.7321 = √3 |
| icosahedron | 1.9021 = √((5+√5)/2) |
| cuboctahedron | 2 |
| truncated tetrahedron | 2.3452 |
| snub cube | 2.6874 |
| dodecahedron | 2.8025 = √((9+3√5)/2) |
| icosidodecahedron | 3.2361 = 2φ |
| truncated icosidodecahedron | 7.6048 |

Prisms and antiprisms grow roughly like n/π. The core is smallest for the tetrahedron, then the octahedron, the 3-prism, the square
antiprism and the cube. Non-uniform frames (Catalan, Johnson, Aequi) come from the pending runs, using the least angle over all
pairs of corners.

## 4. Round Aequi

**Theorem 8 (degenerate as stated).** The cone from O over a fin ring's disc lies in the fin plane. So its solid angle is 0 for every
ring (Theorem 4). Equal solid angles therefore hold for every fin-ring build. "Round-fair" in this sense separates nothing, and
"is an Aequus round-fair?" is trivially yes. **Proved, degenerate.**

**4b (with thickness).** The render study models a real ring as a short tube: band height w across the fin plane, outer face the
incircle. With band height w > 0, the band's sight cone from O has positive solid angle Ω(r, w, fin).
- In a Theorem 1 build all fins are congruent and the rings identical, so all Ω are equal. These builds are round-fair:
  **proved possible**.
- For an Aequus, round-fairness would need equal Ω across its edge orbits. The 1232 numbered Aequi all have at least 2 face orbits,
  and none is edge-transitive (the edge-transitive convex polyhedra are the 5 Platonic, the cuboctahedron, the icosidodecahedron,
  and the rhombic dodecahedron and triacontahedron). So any equality would be a coincidence across orbits. **OPEN**: the pending
  Aequi run finds the dice with equal r and equal central angle first, and only those need the Ω integral.

## Runs

- `scripts/sloane_angles.py`: done here (seconds, 15 small files). FINAL ok.
- On the compute machine, through the job runner, nice, 3 free cores, after the gate override:
  - `dbbjob.sh rings-pilot 0.25 "cd ~/k-research/studies/2026-11-25-rings-cylinders-cones/scripts && PROCS=3 nice -n 10 ~/venvs/arb/bin/python rings_catalogue.py cube cuboctahedron 3 J1 J27 J84"` (JOBSYNC = this folder);
  - then `rings-all` (no names);
  - then `stars.py` and `aequi_rings.py` with the same venv.

## Sources checked (and opened)

- Render study 2026-11-24-vacuus-build-renders (README, `check.py` values).
- Catalogue study 2026-11-24-vacuus-resonus-catalogue (builders, centres).
- Stellation-cycle study 2026-11-25 (`q5.py`, `cycle.py`, `cycle.json`).
- Aequi picker data (`dice.json`).
- Wikipedia "Tammes problem" (proved N = 3–14, 24; Musin–Tarasov N = 14).
- N. J. A. Sloane, spherical packings in 3D (neilsloane.com/packings/dim3, files pack.3.N.txt; found by R. H. Hardin, N. J. A. Sloane
  and W. D. Smith, 1994, some by D. A. Kottwitz 1991).

Cited, not opened (no free copy found in this pass):
- P. M. L. Tammes (1930);
- L. Fejes Tóth (1943);
- K. Schütte and B. L. van der Waerden (1951, and 1953 for the kissing number);
- R. M. Robinson, Math. Ann. 144 (1961) (N = 24);
- O. Musin and A. Tarasov (2012, 2015);
- R. A. Rankin (1955).

## LEADS

1. Run the four scripts (blocker: gate override) and fill 1e, 1f, 1h and the non-uniform core table.
2. Hull rings: rings lying in hull faces, as face incircles, are seen from O as small circles. With regular faces and a midsphere
   they touch at the edge midpoints: a Koebe-type packing whose Tammes comparison is the face directions. Only if DICTO says his
   hulls carry rings this way.
3. Square antiprism and snub cube ring builds: the two non-Platonic builds whose ties are the proved best spreads (8 and 24 points).
   Natural next physical builds, DICTO's choice.
4. Thickness of the ties: rings of radial wall e meeting at one strut point. The dihedral angles between the fins on a spoke set how
   many rings fit at a tie before the bands collide. Exact bound pending.
5. Round-fairness with band height (4b): the Ω integral, closed form, for the dice that pass the equal-r and equal-angle screen.

Name proposals (DICTO's choice; plain descriptions used above): "tie spread" for θ; "ring-buildable" for one ring size; "all-tie
build" for constant t.
