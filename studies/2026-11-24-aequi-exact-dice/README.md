# Two exactness theorems for the Aequi (24 November 2026)

DICTO · dictospheres.com · study 2026-11-24-aequi-exact-dice · with Claude (Anthropic).

**Verdict.**
1. **Aequus CIRT-30, T 26.** Its C6 faces and its RT24/12a faces are at exactly the same depth. The new proof is a mirror. On the line d(C6) = d(RT24/12a) = 1, the identity 2Ω(RT24/12a) − Ω(C6) = 4π/30 holds for **every** depth t ≥ (7/4)/√3 ≈ 1.0104 of the I12 faces. This closes LEAD 1 of study 2026-11-24-aequi-certify-extend. It is a second proof of the equality, independent of the algebraic certificate (resultants) in study 2026-11-24-aequi-vacuus-scutoids, and it shows *why* the depths are equal.
2. **Shadow dice.** A die is fair exactly when its faces project from the centre onto unions of mirror triangles of the cube group (48 triangles) or the icosahedron group (120), with equally many triangles under each face. We screened all 15 192 catalogued fair dice. **Exactly 14 are of this kind** (10 cube, 4 icosahedron), and each of the 14 is proved fair exactly, with its depths in closed form. Row 95 of the two-placement study is one of them. So are the D2h dice "on walls" at cos 18° and cos 30° of Part 2 of the certify-extend study (LEAD 3 there), and the ten-wall D3d die.

## Theorem 1 (CIRT-30)

**Setting.** We use orbits under the frame rotation group T:
- C6 = (±1, 0, 0) cyclic;
- I12 = (0, ±1/φ, ±φ)/√3 cyclic;
- RT24 = (±1, ±φ, ±1/φ)/2 cyclic, split into RT24/12a (the half with the die's representative (φ, 1/φ, 1)/2, i.e. the sign product of that representative) and RT24/12b (the other half, absent from the die).

Put the C6 and RT24/12a planes at depth 1 and the I12 planes at depth t. Let Ω_C, Ω_R, Ω_I be the solid angles of one face of each orbit, seen from the centre.

**Theorem 1.** For every t ≥ t₀ = (7/4)/√3: 6 Ω_C − 12 Ω_R = −4π/5, that is 2 Ω_R − Ω_C = 4π/30. There is a t* in ((7/4)/√3, (1.76)/√3) with Ω_I(t*) = 4π/30. At t*, Ω_C = Ω_R = Ω_I = 4π/30. So the fair die Aequus CIRT-30, T 26 has d(C6) = d(RT24/12a) **exactly**.

**Proof.**
- *Cells.* Write p_i = u_i/d_i, where u_i is the unit normal and d_i the depth. The ray from the centre in direction x meets face i first exactly when p_i·x is largest. So Ω_i is the area of the cell {x on the unit sphere : p_i·x ≥ p_j·x for all j}. This holds whether or not the face is present: an absent face has area 0.
- *Comparison die.* Compare with the rhombic triacontahedron RT30 = C6 + RT24/12a + RT24/12b, all at depth 1. It is face-transitive, so each of its cells has area 4π/30.
- *Around one axis.* Fix the O8 axis b = −(1, 1, 1). Near b lie:
  - the three RT24/12b directions nearest b (20.9°);
  - the three I12 directions nearest b (41.8°);
  - three C6 and three RT24/12a directions, all at 54.7°.
  Call this set M_b. One mirror σ of the icosahedron group passes through b (unit normal an RT24 direction orthogonal to b). It maps M_b to itself: it permutes the I12 triple, it permutes the RT24/12b triple, and it **swaps the three C6 with the three RT24/12a**. Since C6 and RT24/12a have the same depth, σ maps each point p of M_b to another point of M_b, with the C and R labels swapped.
- *The region W_b.* W_b = E_I ∪ E_R, where:
  - E_I is where some member of the I12 triple (at t₀) beats all of the I12 triple and the six C6/RT24a points;
  - E_R is the same with the RT24/12b triple in place of the I12 triple.
  Both are defined from σ-invariant point sets, so σ(W_b) = W_b. Exact tests in Q(√5) (scripts/cirt30_mirror.py, logs/cirt30_mirror.log) show:
  - (A1) on W_b, every other C6 or RT24/12a point loses to the maximum over the six near ones;
  - (A2) on W_b, every other I12 point at t₀ loses to the maximum over the I12 triple and the six;
  - (A3) on W_b, every other RT24/12b point loses to the maximum over the RT24/12b triple and the six;
  - E_I lies in the cap of radius 60° about b, and E_R in the cap of radius 45°;
  - the four T-images of b are pairwise 109.47° apart, which is more than 60° + 45°, so the four regions g·W_b have disjoint interiors;
  - the T-images of the two triples are all 12 I12 and all 12 RT24/12b, each once.
- *All t ≥ t₀ at once.* Every I12 value p·x = u·x/t falls as t grows, so the I12 cells shrink with t. By (A2), each other I12 point beats neither the triple nor the six for any t ≥ t₀ (if it lost to the six at t₀, it still does at larger t). So for every t ≥ t₀:
  - the I12 cells lie in ∪ g·W_b;
  - on W_b, the cells of the die are decided by M_b alone, and so are the cells of RT30 (A1, A3).
  Hence σ carries the die's cell pattern on W_b onto itself with C ↔ R, and the same holds for RT30. On W_b: area(C cells) = area(R cells), for the die and for RT30.
- *Outside the regions.* Outside ∪ g·W_b, no I12 and no RT24/12b point wins. So there the die's C and R cells are exactly those of RT30.
- *Adding up.* [6Ω_C − 12Ω_R](die) = [area C − area R outside the regions](RT30) + 0 = (6 − 12)·4π/30 − 0 = −4π/5.
- *Intermediate value step.* Ω_I is continuous in t. In ball arithmetic, Ω_I(t₀) − 4π/30 = +0.019890 and Ω_I(1.76/√3) − 4π/30 = −0.005134 (rigorous enclosures). So some t* between them has Ω_I(t*) = 4π/30.
- *Solving.* With 6Ω_C + 12Ω_R + 12Ω_I = 4π, this gives 12Ω_C = 12·4π/30. So Ω_C = 4π/30, and then Ω_R = 4π/30.
- *Uniqueness.* The fair die with these 30 normals is unique up to scale. This is Alexandrov's theorem on polyhedra with prescribed vertex directions and curvatures, applied to the polar polytope: the polar's vertices are p_i, and the curvature at a vertex is the area of the cell of face i. So the fair CIRT-30 is this die, and its C6 and RT24/12a depths are equal. ∎

**Checks.** The script also evaluates 2Ω_R − Ω_C − 4π/30 at t = 1.75, 1.758, 1.76 and 2.0 (each over √3). All four values are 0 to within 7e-57 (ball arithmetic). t* lies in (1.75, 1.76)/√3, which agrees with the vacuus-scutoids value x/√3, where x ≈ 1.7579 is the root of 16x⁴ − 40x³ − 100x² + 130x + 145. This also matches the certified t* = 1.01493580273976… of certify-extend.

**What the mirror shows.** The die is RT30 with its twelve RT24/12b faces taken away and twelve I12 faces put in. Both changes happen in four separate patches, one around each axis of the O8/4 orbit of b. A mirror of the icosahedron through the axis exchanges the C6 and RT24/12a faces of each patch. So each patch gives equal area to C6 and to RT24/12a. The six C6 faces therefore gain exactly as much as the twelve RT24/12a faces. When the I12 faces take their fair share, each C6 face and each RT24/12a face ends with 4π/30.

**Scope.** The identity is proved for t ≥ (7/4)/√3. Below that, the I12 cells grow past the 60° cap (67° at t = 1.7/√3), and this argument does not cover them. Nothing below t₀ is needed for the theorem.

## Theorem 2 (shadow dice)

**Theorem 2.** Let G be a finite reflection group of space. Its mirrors cut the sphere into |G| congruent triangles, each of area 4π/|G| (|G| = 48 for the cube group Oh, 120 for the icosahedron group Ih). Let P be a convex polytope with the centre inside and N faces.
- (a) The central projection of every face of P is a union of these triangles **if and only if** every edge of P lies in a mirror plane of G. Equivalently: every corner lies on a rotation axis of G, and the two ends of each edge lie on a common mirror.
- (b) In that case Ω_i = k_i·4π/|G|, where k_i is the number of triangles under face i. So P is fair from the centre if and only if k_i = |G|/N for every face. In particular N divides |G|.

**Proof of (a), "if".** Each edge projects to a great-circle arc inside a mirror. So the boundary of each projected face lies in the union of the mirrors. Each triangle is a connected piece of the sphere minus the mirrors, so it lies wholly inside or wholly outside the face's projection.

**Proof of (a), "only if".** The boundary of a union of triangles lies in the mirrors. So each edge projects into a mirror, and the plane through the edge and the centre is that mirror. At a corner, at least three edges meet, and not all of them lie in one plane through the centre. So the corner lies on two different mirrors, that is, on a rotation axis. Conversely, if both ends of an edge lie on one mirror plane through the centre, the whole edge lies in it.

**Proof of (b).** It is immediate from the areas. (This is how the disdyakis dodecahedron and the disdyakis triacontahedron, the solids whose faces *are* the triangles, are fair; Theorem 2 lets each face cover several triangles.) ∎

**Classification in the catalogue (scripts/scan_shadow.py, logs/scan_shadow.log).**
- *Screen.* All 15 192 fair dice on record were screened: 4553 of study 2026-11-19-aequi-complete, 1083 of study 2026-11-20-aequi-two-placements, and 9556 of study 2026-11-24-aequi-certify-extend (aequi2a, aequi2caps, aequi2caps2, aequi2caps3). The test was condition (a) for G = Oh and for Ih in both icosahedron placements, in double precision with tolerance 1e-7. The mirrors of every other reflection group on these frames (D2h, Td, D3d, D5d, …) are among these mirrors, so this covers them too.
- *Hits.* 14 dice pass.
- *Margin.* Every other die misses by at least 9.2e-3: either a corner is that far from the nearest axis, or an edge is that far from the nearest mirror. The closest misses are T: O8/4 + D12 (9.2e-3) and Th: C6 + D12 (1.6e-2). That margin is ten orders of magnitude above the depth accuracy (1e-12 or better), so the negative result is safe. It is still a double-precision screen, not an exact proof of the negative.

**Exact proof of each hit (scripts/prove_shadow.py, data/shadow_proved.json, logs/prove_shadow.log: proved 14 of 14, FINAL ok).** All of it is exact in Q(√5) except the triangle counts, which are rigorous by ball arithmetic.
1. *Corners on axes.* Each corner is put on its axis direction a_v. The corner radii λ_v and the plane offsets h_i then solve the linear incidence equations exactly in Q(√5).
2. *Face structure.* Every incidence holds exactly, and every corner is strictly inside every other plane. Each face has at least 3 corners, and in cyclic order every side is a supporting line. Each side is shared by exactly two faces. So the faces form the closed boundary of conv(corners), and conv(corners) = P.
3. *Mirrors.* Every side lies in a mirror (n·a_v = n·a_w = 0).
4. *Triangle counts.* The projected area divided by 4π/|G| is enclosed (ball arithmetic) within 1/4 of a single integer k_i. By (a) the area is an exact multiple of 4π/|G|, so k_i is exact.
5. *Fairness and identity.* Each die is fair with k = |G|/N. By Alexandrov's uniqueness it is the catalogue die. The closed-form depths agree with the catalogue to 1e-11 or better.

| die (source, row) | solid's group | N | projection onto | triangles per face | corners (axes) | depth ratios (first orbit = 1), exact |
|---|---|---|---|---|---|---|
| D5d: C6+RT24/10a + C6+RT24/10b (3) (11-19, 83) | D5d | 20 | Ih, 120 | 6 | 22 (C6, D12, RT24) | 1, 1 |
| D5d: C6+RT24/10 + O8+I12/10 (4) (11-19, 89) | D5d | 20 | Ih, 120 | 6 | 12 (D12) | 1, φ/√3 |
| D2d: RD12/4a + RD12/4b (11-19, 787) | D2d | 8 | Oh, 48 | 6 | 8 (C6, RD12) | 1, 1 |
| D2h: C6/2 + RT24/8 (1) (11-19, 844) | D2h | 10 | Ih, 120 | 12 | 12 (C6, D12) | 1, 1 |
| Td: D12+D12′/24 + RT24+RT24′/24 (11-20, 95) | Td | 48 | Oh, 48 | 1 | 26 (C6, O8, RD12) | 1, cos 18° = √(10+2√5)/4 |
| D4h: RD12/8 + D12+D12′/8a + D12+D12′/8b (2a, 272) | D4h | 24 | Oh, 48 | 2 | 14 (C6, O8) | 1, √((5+2√5)/10), √((5+2√5)/10) |
| D4h: RD12/8 + I12+I12′/8a + I12+I12′/8b (2a, 273) | D4h | 24 | Oh, 48 | 2 | 14 (C6, O8) | 1, √(5/6), √(5/6) |
| D4h: D12+D12′/8a + D12+D12′/8b + I12+I12′/8 (2a, 274) | D4h | 24 | Oh, 48 | 2 | 14 (C6, O8) | 1, 1, √((25−10√5)/3) |
| D4h: D12+D12′/8 + I12+I12′/8a + I12+I12′/8b (2a, 275 and 276: two dice) | D4h | 24 | Oh, 48 | 2 | 14 (C6, O8) | 1, √((25−10√5)/3), same |
| D3d: D12+D12′/12 + RT24+RT24′/12a, /12b, /12c (2a, 1509; the ten-wall die) | D3d | 48 | Oh, 48 | 1 | 26 (C6, O8, RD12) | 1, cos 18°, cos 18°, cos 18° |
| D2h: D12+D12′/8 + RT24+RT24′/8 (2a, 3268 and 3269: two dice) | D2h | 16 | Oh, 48 | 3 | 10 (C6, RD12) | 1, cos 18° |
| D2h: I12+I12′/8 + RT24+RT24′/8 (2a, 3270) | D2h | 16 | Oh, 48 | 3 | 10 (C6, RD12) | 1, cos 30° = √3/2 |

Here √((25−10√5)/3) = √(5/3)·tan 36°.

**What the table shows.**
- *Two kinds.*
  - (i) *Depths all equal* (rows 83, 787, 844). These are face-transitive solids with faces taken away: the rhombic triacontahedron keeping 20 or 10 of its 30 faces, and the rhombic dodecahedron keeping 8 of its 12. Each kept face's cell is its old rhombus plus an equal share of the removed ones, and the shares are whole triangles.
  - (ii) *Depths at the ratios that put every corner on an axis* (cos 18°, cos 30°, φ/√3, √(5/6), and so on).
- *More symmetry in the shadow.* In every case the projection has more symmetry than the solid, for example a D2h solid with an Oh shadow.
- *The equal-depth S6 dice are not shadow dice.* The two S6 dice "at equal depth" of certify-extend (D12/6 + D12′/6 and I12/6 + I12′/6) fail the test: 6 of their 14 corners are off the frame axes. Their normals have only the symmetry S6 (two orbits), and their two kinds of face cell are not congruent (scripts/s6_check.py, logs/s6_check.log). Their exact status stays open (LEAD 2).
- *Row 124 is not a shadow die* either (LEAD 2 of certify-extend stays open).

## Sources checked

- Study 2026-11-24-aequi-vacuus-scutoids (README, scripts/cirt30_exact.py). Its exact certificate for CIRT-30 at the fair point (resultants in PARI, Cauchy root bound) is a different method; Theorem 1 does not use it.
- Study 2026-11-24-aequi-certify-extend (README Part 1, "Row 95, exact"; Part 2 walls; LEADS 1 and 3; its prior-art list in Part 3, still valid for these dice).
- Alexandrov, *Convex Polyhedra* (English ed. 2005), the theorem on polyhedra with prescribed vertex directions and curvatures (uniqueness up to similarity), used through polarity, as in the vacuus-scutoids study.
- Coxeter, *Regular Polytopes*: finite reflection groups and their fundamental triangles; the disdyakis dodecahedron and triacontahedron as the solids on those triangles.
- Diaconis and Keller, "Fair dice" (Amer. Math. Monthly 1989): fair by symmetry (face-transitive). Theorem 2 is a "fair by shadow" criterion for dice that are not face-transitive. We did not find it stated in the sources checked; this is a search record, not a priority claim.
- Methods credited at their point of use: Van Oosterom and Strackee (1983) for triangle solid angles; arb ball arithmetic (Johansson) through python-flint.

## LEADS

1. Theorem 1 below t₀: a finer σ-invariant region (not a cap) would extend the identity to all t where the I12 cells stay apart.
2. The S6 equal-depth dice (certify-extend Part 2 rows 5169, 5170): their two kinds of cell have equal area but are not congruent. Find the mechanism (a rearrangement of the RT24-type patches, as in Theorem 1?). Then try Row 124.
3. The mirror argument of Theorem 1 is general. It applies when a die is a face-transitive die with some faces removed or added in patches, and each patch has a mirror of the big group that swaps the kept orbits. Search the catalogue for more dice proved fair this way (two orbits at equal depth is the signature).
4. Off-axis families (certify-extend LEAD 4): the shadow condition gives isolated exact members wherever a family's corners all reach axes.

## Files

- scripts/: qsqrt5.py (exact Q(√5) arithmetic and exact spherical polygons), cirt30_mirror.py (Theorem 1), scan_shadow.py (screen), prove_shadow.py (exact proofs), symgroup.py and s6_check.py (the S6 dice), groups.py (copy, 122 directions).
- data/: shadow_hits.json (the 14 screen hits), shadow_proved.json (proof record per die: exact depth ratios, triangle counts, checks).
- logs/: cirt30_mirror.log, scan_shadow.log, prove_shadow.log, s6_check.log (all FINAL ok).

Run time: each script takes under five minutes on one core (run on a compute host). Software: python-flint 0.9.0 (arb), numpy, scipy, sympy.
