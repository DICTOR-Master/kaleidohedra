# Amplitude at a distance (13 Nov 2026; aim 2, test of DICTO's proposition)

**Conclusion (13 Nov 2026): NOT SUPPORTED as stated. All three pre-registered tests fail (T1 choice, T2 direction, T3 position), and the controls behave like the space-fillers wherever a signature appears. What the canonical form does carry at a distance is its pole set, the extended facet planes; where neighbours sit on it, that is Voronoi bisector geometry, not the form's values. One exact law turned up outside the plan (KNOWN: it is Theorem 4.5 of Baumbach, Freyer, Weigert and Winter, arXiv:2508.04275 (2025), proved in every dimension there; see studies/2026-11-13-zonotope-falloff): far from P, Omega decays like r^-6 for every zonotope (so every 3D parallelohedron), r^-5 for the TRD and the triangular prism, and r^-4 otherwise. It follows face symmetry, not tiling: the rhombic triacontahedron, which does not tile, also decays like r^-6.**

DICTO's proposition (13 Nov 2026, confirmed): "law giving shapes act at a distance governed by their amplitude", amplitude = the
canonical form of aim 2 (Geometry Gives Laws). Working statement tested here: a law-giving (space-filling) shape P acts at a distance
through its canonical function Omega_P; the field its faces create decides where its neighbours can sit, and so which grouping
(lattice / stacking) it forces. This is a test: a negative or partial outcome is a result.

## 0. Setting (fixed before running)

Omega_P(x) = sum over corners v of P, over the simplicial cones of a fan of the normal cone at v, of |det(n_a, n_b, n_c)| /
(f_a f_b f_c), f_i(x) = b_i - n_i.x, P = {f_i >= 0} (Warren's vertex formula; a corner on more than three faces is fanned). Inside P
it equals 3! vol((P - x)°) (Arkani-Hamed, Bai and Lam: canonical form of a positive geometry); outside P it is the same rational
function, with poles exactly on the facet planes.

Shapes (each the Voronoi cell of its own grouping, one frame; hexagonal objects have their c-axis along (1,1,1), an a-axis along
(1,-1,0)):

| shape | own grouping | facets (n.x <= b) | field |
|---|---|---|---|
| RD rhombic dodecahedron | fcc (D3, covolume 2) | (+-1,+-1,0) perms, b = 1 | Q |
| TRD trapezo-rhombic dodecahedron | hcp (ideal c/a, nearest distance sqrt2) | the 12 hcp neighbours n, b = n.n/2 = 1 | Q |
| cube | sc (Z^3) | +-e_i, b = 1/2 | Q |
| TO truncated octahedron | bcc | +-e_i, b = 1/2; (+-1,+-1,+-1), b = 3/4 | Q |
| HP hexagonal prism | simple hexagonal, c = a = sqrt2 | 6 in-plane neighbours, b = 1; +-(1,1,1), b = sqrt6/2 | Q(sqrt6) |
| control: icosahedron | none (no lattice tiling) | corners (0, +-1, +-phi) cyclic | Q(sqrt5) |
| control: dodecahedron | none | corners (+-1,+-1,+-1), (0, +-1/phi, +-phi) cyclic | Q(sqrt5) |
| control: perturbed RD | none: one facet plane (1,1,0) moved to b = 21/20, so P is not centrally symmetric and cannot tile by translations (Minkowski) | | Q |

Candidate groupings (all six for every shape), each scaled to the shape's volume per site (equal density), fixed orientation:
fcc, hcp (ABAB), dhcp (ABAC), bcc, sc, simple hexagonal (c = a). Cubic lattices on the coordinate axes; hexagonal ones with c along
(1,1,1) and a along (1,-1,0) (so for the hexagonal shapes the cubic lattices stand with [111] along c).

## 1. Pre-registered tests (written before the pilot)

**T0 method checks (must all pass, else FINAL FAIL).** Vertex formula = 3! vol(polar) exactly at interior rational points; = the
independent triangulation formula (sum of simplex forms) exactly at exterior points; the complete-fan identity (the r^-3 terms
cancel) exactly; r^4 Omega(r u) tends to the far-field profile c1(u) (float); at a generic point of a facet plane the Laurent order
is -1 (simple pole); known values Omega_cube(0) = 64, Omega_RD(0) = 40; negative method control: dropping one Warren term breaks
the polar identity.

**T1 Choice (lattice sum).** E_P(L) = sum over t in L, t != 0 of Omega_P(t).
- First, exactly: does L contain points ON a facet plane of P? (decided exactly: field degree of b/lambda, then integer membership in
  the module n.L by Hermite reduction). An on-plane point is a pole: E_P(L) is then undefined (infinite, of no sign). We report it
  and do NOT replace it by a principal value.
- C1 (primary): for every one of the five law-giving shapes, E_P(own L) is finite and is the extreme of the six by ONE common rule
  (all minimum or all maximum), with the gap larger than the stated error. Any shape whose own E is undefined fails C1.
- C1' (secondary, a stated regularisation): the same with on-plane points deleted from the sum (pole-deleted sum E').
- C2 (secondary): the own grouping is the unique candidate with points on P's facet planes.
- C3 (robustness): E' at 16 random orientations of each lattice (partial sum to radius 20 rho, rho = vol^(1/3)); if the spread over
  orientations of one lattice exceeds the gaps between lattices, the sum does not characterise a grouping.
- Controls: icosahedron, dodecahedron and perturbed RD must NOT show the same signature as the law-giving shapes (else the criterion
  is about polytopes in general, not about laws).
Truncation: partial sums over balls of radius R = 8 .. 40 rho, extrapolated by E(R) = E_inf + a/R + b/R^2 (the tail is of order
1/R when lattice points come near facet planes: the near-plane terms behave like Res/f with Res ~ |x|^-3; proof sketch in Results);
error = disagreement of two fits + certified float rounding bound. If this cannot be certified we say so.

**T2 Direction.** (a) Far field: c1(u) = lim r^4 Omega(r u) (exact rational function). (b) The sphere through the nearest neighbours.
For each own neighbour direction: exactly decide pole / finite; if finite, whether it is critical (tangential gradient zero, exact)
and its type (Hessian on the sphere, exact sign). PASS iff in all five shapes every own neighbour direction is a finite critical
point of one common type (all local maxima or all local minima), and the controls' face directions (the would-be neighbours) do not
all have that type. Symmetry alone forces criticality on rotation axes; so every symmetry-axis class is classified too: if
non-neighbour axes have the same type, the match is symmetry, not grouping.

**T3 Position.** On the line x = s n through each facet normal (facet at s0, neighbour centre at 2 s0), exactly decide whether 2 s0 is
a pole, a zero or a critical point of Omega(s n). PASS iff one common kind holds for every facet class of all five shapes and at
none of the controls' facet classes. Exploratory: all zeros, poles and critical points on s0 < s <= 6 s0 (float), as s/s0.

**Verdict rule.** The proposition is supported only if T1-C1 (or C1', stated as regularised) passes AND at least one of T2, T3
passes, with the controls behaving differently. Otherwise the outcome is "not supported", with every partial fact stated.

## Running
Compute node through the job gate (jobs amp-pilot, amp), 2 worker processes, 4 GB cage. Script `scripts/amp_dist.py`; logs
`data/amp.log` (full, 343 s, 93 checks, FINAL ok) and `data/amp-pilot.log`; all numbers in `data/amp.json`.

**Pilot amendments (made before the full run, recorded here):** (1) the pilot showed that the r^-4 coefficient c1 of the brief is
identically 0 for the five space-fillers, so T2's far field uses the first nonzero coefficient a_k of Omega(r u) = sum a_k(u)
r^(-3-k) (exact formula: a_k = -sum d h_k(b_a/w_a, b_b/w_b, b_c/w_c)/(w_a w_b w_c), w = n.u, h_k the complete symmetric polynomial);
the criterion is unchanged. (2) First pilot faults fixed: the dodecahedron was built in the other golden orientation (wrong face
planes for the icosahedron), a tangent-vector picker looped forever for the cube, a test direction lay on a TO plane, and the
TRD was wrongly listed as centrally symmetric (it is not: it tiles hcp in two orientations). (3) A far-field decay census of ten
further solids was added (exploratory; it is not part of the verdict rule).

## 2. Results

### T0 method checks: all pass (exact unless marked)
Vertex formula = 3! vol(polar) at interior points, = triangulation formula at exterior points (all 8 shapes); complete-fan identity
(the r^-3 terms cancel); Laurent order -1 at generic points of facet planes (poles exactly on facet planes); Omega_cube(0) = 64,
Omega_RD(0) = 40; dropping one Warren term breaks the polar identity; volumes equal the covolumes of the own groupings; the float
on-plane detection agrees with the exact incidence in all 48 shape/lattice pairs. The far-field order (float, Richardson from r = 1000
and 2000, 1e-3) agrees with the exact first nonzero a_k.

**The brief's premise "Omega decays like |t|^-4" is false for the space-fillers.** First nonzero far-field coefficient (a_0 .. a_(k-1)
vanish exactly at two generic directions; the decay itself float-checked):

| solid | decay | | solid | decay |
|---|---|---|---|---|
| RD, cube, TO, HP (space-fillers, zonotopes) | r^-6 | | icosahedron, dodecahedron | r^-4 |
| TRD (space-filler, not centrally symmetric) | r^-5 | | perturbed RD | r^-4 |
| generic parallelepiped, generic 4- and 5-generator zonotopes | r^-6 | | octahedron, cuboctahedron, corner-cut cube (centrally symmetric, not zonotopes) | r^-4 |
| rhombic triacontahedron, rhombic icosahedron (zonotopes, **no tiling**) | r^-6 | | tetrahedron | r^-4 |
| triangular prism (tiles, not centrally symmetric) | r^-5 | | | |

So the fast decay marks zonotopes (every face centrally symmetric), not space-filling. Every 3D parallelohedron is a zonotope
(Minkowski, Venkov, McMullen), so all of them decay like r^-6. Several zonotopes that do not tile do the same. Reading: Omega =
A/prod f_i with the adjoint A of degree F - 4 (Warren); decay r^-(4+m) means A contains the plane at infinity m times. Parallel facets
and zones put residual intersections at infinity, which the adjoint must pass through. Central symmetry kills the odd coefficients
(a_0, a_2), so m is even there. Proved in general by Baumbach, Freyer, Weigert and Winter (arXiv:2508.04275, 2025, Theorem 4.5); not new here (LEAD 1 closed 13 Nov, studies/2026-11-13-zonotope-falloff).

### T1 Choice: FAIL (C1, C1', C2 and C3 all fail)
Exact incidence: which of the six groupings (equal density, fixed orientation) have points ON facet planes of P, where Omega has a
pole and E_P(L) is undefined (no principal value used):

| shape | groupings with points on its poles | own |
|---|---|---|
| RD | fcc, hcp, dhcp (all 12 planes) | fcc |
| TRD | fcc, hcp, dhcp (all 12 planes) | hcp |
| cube | none | sc |
| TO | bcc (the 6 square planes) | bcc |
| HP | sh (the 6 side planes) | sh |
| icosahedron, dodecahedron, perturbed RD | none | - |

Reason (exact, elementary): a lattice point t lies on the facet plane bisecting 0 and a neighbour n' iff |t| = |t - n'|, i.e. t, 0, n'
form an isosceles triangle. Close packings have such triangles (60 degrees), bcc on its square planes, sh in its layers; sc never
(2 t_i = 1 has no integer solution). The other groupings at equal density never hit, because b/lambda then has field degree 3 or 6
(a cube root), outside Q(sqrt2, sqrt3, sqrt5). So for 4 of the 5 space-fillers the own lattice sum is undefined: **C1 fails**.
**C2 fails** (RD and TRD share fcc/hcp/dhcp; the cube has no incident grouping).

Pole-deleted sums E' (on-plane points removed, a stated regularisation), extrapolated from R = 8 .. 40 rho with E_inf + a/R + b/R^2;
the +- is the disagreement of two fits plus the certified float-rounding bound. The tail was not certified (see below).

| shape | fcc | hcp | dhcp | bcc | sc | sh | own extreme? |
|---|---|---|---|---|---|---|---|
| RD | P -8.43(9) | P -41.9(3) | P -22.3(5) | -145.4(1) | -1110.3 | -5070(180) | fcc = max |
| TRD | P -34.7(2) | P -33.2(3) | P -43.0(3) | -2354(4) | -740.1 | -5070(180) | hcp = max |
| cube | 237.8(1.2) | -1268(60) | -1014(77) | -3326(6) | **-64.0(1)** | -2984(330) | no (max fcc, min bcc) |
| TO | -664.2 | -171.2(2) | -465.7(4) | P **-653.6(8)** | -48619(56) | -3584(6) | no (max hcp, min sc) |
| HP | -3188.6(3) | -2815.4(1.2) | -2815.4(1.2) | -24.46(3) | -645.5(7) | P **-29.31(1)** | no (max bcc, min fcc) |
| icosahedron | -13.4(1.2) | -325.2(1) | -196.9(8) | 22.6(3.6) | -10662(15) | 83.3(1.5) | (max sh, min sc) |
| dodecahedron | -3.46(36) | -71.4(3) | -141.6(1.2) | 18.0(2.4) | 14.0(3.4) | 198(46) | (max sh, min dhcp) |
| perturbed RD | -2.00e6 | -1.56e6 | -1.75e6 | -141.9(1) | -1088.3 | -10866(1100) | (min fcc) |

(P = grouping with points on the poles; value shown is the pole-deleted E'.) **C1' fails**: own = max for RD and TRD only; cube,
TO and HP have their own grouping in the middle. The perturbed RD shows what the poles do: moving one plane by 1/20 turns the
deleted pole points into near-pole points worth about -2 million. **C3 fails by orders of magnitude**: at 16 random orientations
the same lattice gives E'(20 rho) between, e.g., -1.6e4 and 5.4e4 (RD/fcc) or -5.8e6 and 1.4e5 (TO/fcc), far wider than any gap
between lattices. A lattice point near any extended facet plane dominates the sum. So the sum measures how lattice rows meet the
extended facet planes, not a grouping, and no common min/max rule exists.

Tail (proved part): off the facet planes |Omega| = O(r^-(3+k)) (table above); near a facet plane Omega ~ Res_F/f with Res_F the
facet polygon's canonical function (decay |y|^-3 or faster), so with a uniform gap g > 0 from the planes the tail is O(1/(g R)) and
the sum converges absolutely. A lattice point on a plane gives an infinite term. A certified explicit tail constant was NOT obtained:
the slab terms resisted a clean bound, so the extrapolated values are estimates, not certified.

### T2 Direction: FAIL
Own neighbour directions, exact classification (far field = first nonzero a_k on the sphere; sphere = Omega on the sphere through the
neighbours; type by the exact Hessian sign):

| shape | far field at neighbour directions | sphere through neighbours |
|---|---|---|
| RD | 12 poles (order 2) | 12 poles (order 2: 4 facet planes meet there) |
| TRD | 12 poles | 12 poles |
| cube | 6 poles (order 4) | 6 local maxima |
| TO | 6 square: poles; 8 hexagon: local maxima | 6 square: maxima; 8 hexagon: poles |
| HP | 8 poles | 8 local maxima |
| icosahedron (face directions) | 20 local maxima | 20 local maxima |
| dodecahedron (face directions) | 12 local maxima | 12 local maxima |
| perturbed RD | 4 maxima, 8 poles | 1 maximum, 11 poles |

No common type across the five shapes. Where neighbour directions are maxima (cube, HP and TO on the sphere), the non-tiling
icosahedron and dodecahedron show exactly the same thing at their face directions. Symmetry alone forces criticality on those axes,
and the far-field profile also has maxima on non-neighbour axes (cube and TO: the 3-fold axis). So the match is symmetry, not
grouping.

### T3 Position: FAIL
Along each facet normal, at the neighbour centre 2 s0 (exact):

| shape | at 2 s0 |
|---|---|
| RD | pole (order 2) on all 12 lines: the neighbour centre lies on 4 other facet planes |
| TRD | pole on all 12 lines |
| cube | regular (no zero, pole or critical point; along the line Omega is the segment's 1/((1/2 - s)(1/2 + s)) times constants) |
| TO | square lines regular; hexagon lines pole (3 square planes meet there) |
| HP | side lines pole; top lines regular |
| icosahedron, dodecahedron | regular |
| perturbed RD | pole on 11 of 12 lines, regular on the moved one |

No common kind across the five, and the perturbed RD (no tiling) keeps the RD's poles. The pole at 2 s0 is exactly the bisector
condition 2 n.n' = |n'|^2 (two neighbours at 60 degrees, or a square/hexagon pair in bcc), a fact about the facet-plane arrangement.
Exploratory scan (float, s0 < s <= 6 s0, as s/s0): RD zero at 3.1622 (sqrt10 to the printed digits), critical points 1.4449 and
3.6623; TO square line pole 1.5, zero 3.6742; cube line nothing at all; icosahedron poles 1.3416 (3/sqrt5) and 3, zero 1.8278;
dodecahedron pole sqrt5. Nothing sits at 2 apart from the poles above.

## 3. What holds (exact)
1. Omega's influence at a distance is concentrated on the extended facet planes (simple poles there, decay r^-(3+k) elsewhere);
   the "field" is the facet-plane arrangement, weighted by the facet polygons' own canonical forms (residues).
2. Own lattice points lie on these poles iff the grouping has isosceles neighbour triangles (RD, TRD, TO, HP yes; cube no). This
   is Voronoi geometry (bisector planes), so the canonical form adds nothing to it.
3. Far-field decay r^-6 for zonotopes, r^-5 for the TRD and the triangular prism, r^-4 otherwise (exact at two generic directions
   per solid; KNOWN, proved by Baumbach-Freyer-Weigert-Winter 2025, Thm 4.5). This is the one place where the form tells space-fillers from the icosahedron, dodecahedron and perturbed
   RD, but it is a zonotope law, not a tiling law: the rhombic triacontahedron does not tile and decays like r^-6.

**Verdict by the pre-registered rule: not supported** (T1 fails, T2 fails, T3 fails; the controls share every signature found).

## 4. Credits and sources checked
Known mathematics used: Voronoi (cells of lattices, bisector facets); Delone, Dolbilin, Shtogrin and Galiulin 1976 (the local
theorem: local rules determine a regular system; the proposition is a field-theoretic cousin of it, which this test does not
support); Arkani-Hamed, Bai and Lam (positive geometries, canonical forms); Warren (adjoint and vertex formula); Minkowski (a
translation tile is centrally symmetric); Minkowski, Venkov, McMullen (3D parallelohedra are the five zonotope types).
Checked: studies 2026-11-12-solids-canonical (solids_canon.py: Warren and triangulation formulas, re-implemented here over
Q(sqrt D)), 2026-11-10-canonical-sweep (canon_sweep.py), 2026-11-13-aim2-review-checks (README, R2 moment identity),
2026-11-13-near-but-never-on (README, near_on.py, its job-gate pattern), the paper papers/2026-11-12-geometry-gives-laws
(paper.html: bridge, Warren's vertex formula, credits). Reference library manifests (papers, expansion, gaps, cited) searched for
positive geometry, canonical form, amplituhedron, Delone, local theorem, Epstein, lattice sum, Warren, adjoint, Voronoi. Hits read by
title: "The amplituhedron", "Canonical Forms as Dual Volumes", "The canonical form, scissors congruence and adjoint degrees of
polytopes", "Perfect, strongly eutactic lattices are periodic extreme", the Voronoi-conjecture parallelohedra papers. None treats
lattice sums of canonical functions or the far-field decay order. Concordance ledger read: [71], [166], [168], [179], [193] and the
2026-11-13 entries; none covers Omega outside P.

## LEADS
1. Prove: the adjoint of a 3D zonotope contains the plane at infinity twice (decay r^-6); characterise the r^-5 class (TRD and
   triangular prism: some parallel facet pairs and zones, not all). Does the order count the zones or the parallel pairs? Higher d?
2. The extended facet planes as the real "field": count, per grouping, the lattice points on P's planes (an incidence law). Exact
   so far: own lattice on the poles iff it has isosceles neighbour triangles.
3. A different regularisation of T1 (e.g. Omega integrated over the neighbour's body, or the residues Omega_F summed over the lattice
   rows inside each extended plane) could give a finite, orientation-stable quantity. Not tried here; it would be a new hypothesis.
4. The RD line's zero at s/s0 = sqrt10 (float) and the TO line's 3.6742: exact values and meaning.
5. A certified tail constant for the near-plane slab terms.
