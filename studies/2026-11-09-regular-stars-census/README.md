# The regular solids and the regular star polytopes under DICTO's growth rule: Star Cores, Star Halos, gains, core cycles and the turn, study 2026-11-09

**Verdicts (one line each).**
1. **Census: DONE, exact, 25 of 25.** All regular polytopes of 3D and 4D (5 Platonic, 4 Kepler–Poinsot, 6 convex 4-polytopes,
   10 Schläfli–Hess) come out of one mirror-chain enumeration with their exact flags. Each solid's T-gain per period is
   g = (R/h)². For the convex ones the Star Core, the Star Halo and the Polar Halo are the dual, and the core cycle has period 2 with
   two-turn radius scale t²/g. For a star polytope, the first core leaves the star world: it is the convex Platonic solid or
   4-polytope spanned by the face (cell) centres. The known #80 values (cube 3, tetrahedron 9, dodecahedron 15 − 6√5) are reproduced.
2. **The turn for stars: the identity HOLDS, the peak FAILS.** On the flag line S\*(μ) of every regular polytope, convex or not:
   - The antipol identity S\*(μ)^∨ = h⁻²S\*(h²R²/μ) holds.
   - The turn theorem holds verbatim *within one flag*: the closed form is exact at every sample, the peak is at μ = hR, and the
     curve is log-concave.
   - Across flags it fails. The whole star polytope's t_min\* is largest at the two ends for 12 of the 14 stars. For the grand 600-cell
     and the great grand stellated 120-cell (density 191) the turn is the global maximum, but the curve is not log-concave there either.
3. **Hopscotch: a new star-line theorem.** For a regular polytope P with T-gain g, the hulls of DICTO's stars
   K_t = conv(P ∪ tips at t·feet), for 1 ≤ t ≤ g, form the polar image of the dual's polar line, at μ° = R°²/t.
   - The walls are t = ρ_k²/h²: the solid at t = 1, the join at k = d − 2, and T(P) at t = g.
   - The line carries the turn t ↦ g/t. Its fixed point is t = √g = R/h, where the tips lie on the circumsphere.
   - One step of the growth rule is a jump from one end of this line to the other, and two steps make one hop with multiplier g.
     The core's two-turn hop has multiplier t²/g, so the two hop multipliers always multiply to t².
   - At t = 2 the spike sides of four polytopes lie in their own facet hyperplanes (a stellation): the 16-cell, the 24-cell, the
     icosahedral 120-cell and the great icosahedral 120-cell.
   - DICTO's doubling t = 2 is exactly the turn's fixed point for the four polytopes with g = 4: the tesseract, the 16-cell, the great
     stellated 120-cell and the grand 120-cell. It is the join wall of the cube, and the T end of the 24-cell.
4. **Non-regular Star Cores (context only):** the turn is known to fail there (dual-sweeps theorem). The census of DICTO's own solids is
   in the 2026-10-30 and 2026-11-02 studies. Nothing was recomputed here.

**Status:** DONE (exact in Q(√5); in Q for the cubic family). Every script ends FINAL ok. Nothing was committed, pushed or published.

## 0. Definitions used (exactly those of #79–#81 and the census scripts)

- **Star** (t): the solid with a pyramid over each face, its tip at t × the foot of the face perpendicular. Here t = 2 (the doubled star)
  and t = φ (the golden star). For a star-polygon face the foot is the polygon's centre.
- **Star Halo:** the hull of the tips. **Polar Halo:** the reciprocal, with corners at the poles of the face planes.
- **Star Core:** the common part of the hulls of each face family's tips (study2.core_turn), followed turn after turn.
- **T:** DICTO's growth rule, T(S) = {x : v·x ≤ v·v for every corner v} (#38; exactlib.ustep), followed until it returns.
  **Gain:** the radius factor per period, as in #80.
- **Flag line** (new here; it is the turn theorem's polar line extended to stars): Δ(μ) = conv(0, q₀, …, q_{d−1}) cut by q₀·x ≤ μ, and
  S\*(μ) = G·Δ(μ). The flag-wise antipol is Δ^∨(μ) = h⁻²Δ(c/μ), with c = h²R².
  t_min\*(μ) = max x·y over S\* × S\*^∨ = max over corner pairs a, b of a⁺·b⁺, where x⁺ is x folded into G's chamber.
  - For a convex P the flag simplex is a chamber, so S\*(μ) = P ∩ μP\*: the line of the turn theorem.
  - For a star P the flag simplex covers *density*-many chambers.
  - At the nodes, S\*(μ) passes through the star solid (R²), its rectification (ρ₁²: the dodecadodecahedron or the great
    icosidodecahedron) and its reciprocal star (h²).

## 1. The census table

Full table: data/census_table.csv and data/census_table.json (25 rows, 20 columns). It is built from data/flags.json, s2_census3d.json,
s3_census4d.json and s4_starturn.json. In the table, g = R²/h² is also the T-gain per period (radius), and the core cycle has period 2
with two-turn radius scale t²/g' (g' is the g of the convex core). "Join" is the star-line wall where neighbouring spike sides become
coplanar; up to it, the convex solid's star is convex. ⊛ = the turn's fixed point √g.

| Solid | {p,q(,r)} | density | g = (R/h)² | Star Core / Halo (first) | Polar Halo | join t | t = 2 | t = φ | t_min\* on the flag line |
|---|---|---|---|---|---|---|---|---|---|
| dodecahedron | {5,3} | 1 | 15 − 6√5 ≈ 1.5836 | icosahedron | icosahedron | (5 − √5)/2 | beyond g, non-convex star (new) | beyond g (new) | peak at turn |
| icosahedron | {3,5} | 1 | 15 − 6√5 | dodecahedron | dodecahedron | (9 − 3√5)/2 | beyond g (new) | beyond g (new) | peak at turn |
| cube | {4,3} | 1 | 3 | octahedron | octahedron | 2 | **= join: rhombic dodecahedron** (classical) | convex kis (new) | peak at turn |
| tetrahedron | {3,3} | 1 | 9 | tetrahedron | tetrahedron | 3 | convex kis (new) | convex kis (new) | peak at turn |
| octahedron | {3,4} | 1 | 3 | cube | cube | 3/2 | non-convex (new) | non-convex (new) | peak at turn |
| small stellated dodecahedron | {5/2,5} | 3 | 5 | icosahedron (hull of face centres) | great dodecahedron | (5 − √5)/2 | star on star faces (new) | (new) | max at ends √5; turn 15 − 6√5 is the minimum |
| great dodecahedron | {5,5/2} | 3 | 5 | icosahedron | small stellated dodecahedron | (5 + √5)/2 | (new) | (new) | the same as SSD |
| great stellated dodecahedron | {5/2,3} | 7 | 15 + 6√5 ≈ 28.416 | icosahedron | great icosahedron | (5 + √5)/2 | (new) | (new) | max at ends 2 + √5 = φ³; local max at the turn 3.7363 |
| great icosahedron | {3,5/2} | 7 | 15 + 6√5 | dodecahedron | great stellated dodecahedron | (9 + 3√5)/2 | (new) | (new) | the same as GSD |
| 120-cell | {5,3,3} | 1 | 28 − 12√5 ≈ 1.1672 | 600-cell | 600-cell | 2 − 2√5/5 ≈ 1.1056 | beyond g (new) | beyond g (new) | peak at turn |
| 600-cell | {3,3,5} | 1 | 28 − 12√5 | 120-cell | 120-cell | ≈1.0186 | beyond g (new) | beyond g (new) | peak at turn |
| tesseract | {4,3,3} | 1 | 4 | 16-cell | 16-cell | 2 | **⊛ and join: the 24-cell** (classical) | convex (new) | peak at turn |
| 5-cell | {3,3,3} | 1 | 16 | 5-cell | 5-cell | 8/3 | convex (new) | convex (new) | peak at turn |
| 16-cell | {3,3,4} | 1 | 4 | tesseract | tesseract | 4/3 | **⊛: a stellation of the 16-cell, hull the 24-cell** | non-convex (new) | peak at turn |
| 24-cell | {3,4,3} | 1 | 2 | 24-cell | 24-cell | 4/3 | **= g: a stellation, hull T(24-cell)** | non-convex (new) | peak at turn |
| icosahedral 120-cell | {3,5,5/2} | 4 | 6 − 2√5 ≈ 1.5279 | 600-cell | small stellated 120-cell | 4/3 | beyond g; spike sides in its own cell hyperplanes (new) | beyond g | max at ends √5 − 1; turn 28 − 12√5 |
| small stellated 120-cell | {5/2,5,3} | 4 | 6 − 2√5 | 600-cell | icosahedral 120-cell | ≈1.1056 | beyond g | beyond g | the same |
| great 120-cell | {5,5/2,5} | 6 | 6 − 2√5 | 600-cell | itself | ≈1.1056 | beyond g | beyond g | max at ends √5 − 1; turn 28 − 12√5 |
| grand 120-cell | {5,3,5/2} | 20 | 4 | 600-cell | great stellated 120-cell | ≈2.894 | **⊛** (new) | (new) | max at ends 2; turn 6 − 2√5 |
| great stellated 120-cell | {5/2,3,5} | 20 | 4 | 600-cell | grand 120-cell | ≈1.1056 | **⊛** (new) | (new) | the same |
| grand stellated 120-cell | {5/2,5,5/2} | 66 | 6 + 2√5 ≈ 10.472 | 600-cell | itself | ≈2.894 | (new) | (new) | max at ends 1 + √5; turn 12 − 4√5 |
| great grand 120-cell | {5,5/2,3} | 76 | 6 + 2√5 | 600-cell | great icosahedral 120-cell | ≈2.894 | (new) | (new) | max at ends 1 + √5; turn 70 − 30√5 |
| great icosahedral 120-cell | {3,5/2,5} | 76 | 6 + 2√5 | 600-cell | great grand 120-cell | 4/3 | spike sides in its own cell hyperplanes (new) | (new) | the same |
| grand 600-cell | {3,3,5/2} | 191 | 28 + 12√5 ≈ 54.83 | 120-cell (600 cell centres) | great grand stellated 120-cell | ≈6.981 | (new) | (new) | **global max at the turn 6.9964**, ends φ⁴; not log-concave |
| great grand stellated 120-cell | {5/2,3,3} | 191 | 28 + 12√5 | 600-cell | grand 600-cell | ≈2.894 | (new) | (new) | the same |

T-chains of the star polytopes: T reads only the corners, so the chain is that of the convex hull. The hull is the icosahedron or the
dodecahedron in 3D (gain 15 − 6√5) and the 600-cell (the 120-cell for {5/2,3,3}) in 4D (gain 28 − 12√5). Read flag-wise instead
(reciprocation in the circumsphere, star to reciprocal star), the gain per period is the star's own g: 5, 15 + 6√5, 6 ± 2√5, 4 or
28 + 12√5.

**What is new and what is known.**
- **Known.** The polytopes and their densities (Coxeter; the densities 1, 3, 7 and 4, 6, 20, 66, 76, 191 come out of the run). The
  Star Halo, Polar Halo and first Star Core are always a dual or the hull of a reciprocal: classical. The 3D T-gains are #80. The
  doubled cube is the rhombic dodecahedron, and the doubled tesseract is the 24-cell: classical. The edge-tangent kis solids are the
  Catalan solids and Wenninger's star duals. The stellations: Kepler's small stellated dodecahedron (dodecahedron at t = √5), the
  great stellated dodecahedron (icosahedron at t = 3, as in DICTO's Kepler–Poinsot–UP Cycle), the stella octangula (octahedron at
  t = 3 = g), the small triambic icosahedron (icosahedron at 3√5/5), and the small stellated 120-cell (the 120-cell at t = √5 − 1 = 2/φ,
  checked exactly).
- **New as values of DICTO's rules.** The 4D T-gains 16, 4, 4, 2 and 28 − 12√5, and the star gains. The other doubled and golden
  stars are not named in any source checked. They are Kleetopes at height (t − 1)h, a family that is classical as an operation (as
  the 2 November census found for DICTO's own solids).
- **New as structure.** The star-line theorem (Section 3), the turn for stars (Section 2), and the place of t = 2 and t = φ in every
  line.
- **Galois conjugation.** The great stellated dodecahedron and the great icosahedron are the conjugates (√5 ↦ −√5) of the dodecahedron
  and the icosahedron, and the small stellated dodecahedron and the great dodecahedron are conjugate to each other. So every exact
  number of their lines is the conjugate of the partner's: 15 ± 6√5, the joins (5 ∓ √5)/2 and (9 ∓ 3√5)/2, and the edge-tangent kis
  roots (30 ∓ 3√5)/19, (±12√5 − 15)/11 and ±5√5 − 10. The same holds in 4D (28 ± 12√5, 6 ± 2√5). The conjugacy is classical. t_min\*
  is *not* conjugate, because it is a maximum, and conjugation does not keep order.

## 2. The turn for stars (task 2)

**Definition.** The flag line S\*(μ) = G·Δ(μ) and its flag-wise antipol (Section 0). For a convex P this is P ∩ μP\* and its antipol.

**Results (s4_starturn.py; 25 lines, 13–22 exact samples each plus a 4001-point scan; FINAL ok).**
1. **Antipol identity: holds for all 25.** S\*(μ)^∨ = h⁻²S\*(c/μ), checked on the corner sets at every sample. So
   t_min\*(μ) = t_min\*(c/μ) exactly, everywhere. The proof is the same two lines as for convex P: the antipol keeps the plane
   families and inverts the distances.
2. **Flag-local turn theorem: holds for all 25.** Pair x and y within one flag, as in the convex proof, and the value is
   E min(U_μ, U'_{c/μ})/h². It is exact at every sample, peaks at μ = hR, and is log-concave in log μ. The proof carries over
   unchanged: the flag Gram identity q_j·q_k = ρ²_{max(j,k)} (Lemma 2), the chamber slice (Lemma 3), the probability form (Lemma 4)
   and convex order all hold for star flags. **Only Lemma 1 (dominance) fails.**
3. **Global t_min\*: the peak at the turn fails for all 14 stars.** Folding pairs a corner of one flag with the reciprocal corner of
   another.
   - The ends are exact: t_min\*(R²) = q₀⁺·q_{d−1}⁺/h². This is √5 for SSD and GD, φ³ for GSD and GI, √5 − 1 for {3,5,5/2},
     {5/2,5,3} and {5,5/2,5}, 1 + √5 for densities 66 and 76, 2 for density 20, and φ⁴ for density 191.
   - These exceed the turn value, except for density 191.
   - At the turn, t_min\* = R(S\*)²/h² still holds: the tangent star. Its value equals the flag-local peak, for example 15 − 6√5 for
     SSD and GD, 28 − 12√5 for densities 4 and 6, 6 − 2√5 for density 20, and the root 3.736318 of x⁴ − 48x³ + 474x² − 1512x + 1341
     for GSD and GI.
   - The shapes of the curves differ:
     - SSD and GD: U-shaped, with the turn the minimum.
     - GSD and GI: W-shaped, with a local maximum at the turn.
     - Density 191: W-shaped, with the turn the global maximum, 6.996416, the root of x⁴ − 152x³ + 4080x² − 24704x + 22784.
   - log-concavity fails on all 14 star lines.
4. **Coincidences of values, recorded, not explained.** The turn value of SSD and GD equals the T-gain of the dodecahedron and the
   icosahedron, 15 − 6√5. The turn value of the density-4 and density-6 polychora equals that of the 600-cell and the 120-cell,
   28 − 12√5. The turn value of density 20 equals the g of density 4, 6 − 2√5.

**Convex-shadow reading (checked by hand from the flags).** The turn theorem's own construction applied to a star's planes (face
planes ∩ corner planes as half-spaces) leaves the stars:
- For SSD and GD, the corner and face axes coincide (both 5-fold), so the line collapses to one solid.
- For GSD and GI, it is the dodecahedron–icosahedron line itself, with the same turn d ↦ h²/d (d the corner-plane distance).

So the flag line is the proper analogue, and on it the peak does not survive.

## 3. Hopscotch events (task 3)

**Star-line theorem.** Let P be a regular polytope, convex or star, with feet (face centres) c_f at distance h and corners at R.
Put g = R²/h². For t ≥ 1, K_t = conv(corners ∪ {t·c_f}) is the polar of S_{P°}(R°²/t), the polar line of the reciprocal P°. The
reason: the polar of conv(A ∪ B) is A° ∩ B°.

So on 1 ≤ t ≤ g:
- (i) the walls are t = ρ_k²/h² (ρ_k the flag radii): t = 1 is P, t = ρ_{d−2}²/h² is the join, and t = g gives T(P). The tips
  are then the corners of T(P), and the hull of the star is T(P).
- (ii) the antipol turn of the dual's line becomes t ↦ g/t on the star line, with fixed point t = √g = R/h, where the tips lie on
  P's circumsphere. This is the polar of the "all faces tangent" solid of the turn theorem.
- (iii) beyond t = g, the hull is the scaled dual and only the star itself changes.

The kis–truncation duality behind it is classical (Wikipedia, Kleetope: the Kleetope is the dual of the truncation of the dual). The
statement as a line with walls, ends T(P) and the turn t ↦ g/t is not stated in any source checked.

**Events per line** (exact, data/s2_census3d.log and s3_census4d.log; the 3D list is complete for every incidence of a spike side
with a corner or a tip):

| line | incidence (walls, coplanarities) | metric | stationary | DICTO's values |
|---|---|---|---|---|
| tetrahedron | 1, 3 (join = ⊛ = the cube), 9 = g | 9/5 triakis tetrahedron (Catalan) | ⊛ 3 | 2, φ in hop (1, 3); turned to 9/2 and 9/φ |
| cube | 1, 2 (join: rhombic dodecahedron), 3 = g | 3/2 tetrakis hexahedron | ⊛ √3 | **2 = join**; φ in (1, 2) |
| octahedron | 1, 3/2 (join), 3 = g = stella octangula (stellation) | 3√2 − 3 triakis octahedron; −3 − 3√2 great triakis octahedron | ⊛ √3 | 2, φ in (3/2, 3); 2 ↔ 3/2 = join |
| dodecahedron | 1, (5 − √5)/2 (join), 15 − 6√5 = g, √5 = small stellated dodecahedron, 5 + 2√5 | (30 − 3√5)/19 pentakis dodecahedron; √5 (the SSD again) | ⊛ (15 − 6√5)^½ ≈ 1.2584 | 2 and φ beyond g |
| icosahedron | 1, (9 − 3√5)/2 (join), 3√5/5 = small triambic icosahedron, g, 3 = great stellated dodecahedron | (12√5 − 15)/11 triakis icosahedron; 3 (the GSD again) | ⊛ ≈ 1.2584 | 2 and φ beyond g |
| SSD / GD | joins (5 ∓ √5)/2, g = 5; √5 = ⊛ = tips on the corners; GD 5 + 2√5 | 5√5 − 10 (SSD: small stellapentakis dodecahedron); −5√5 − 10 (GD: great pentakis dodecahedron) | ⊛ √5 | 2, φ in (1, g) |
| GSD / GI | joins (5 + √5)/2, (9 + 3√5)/2; g = 15 + 6√5; GSD √5, 5 + 2√5; GI 3, 6√5/5 + 3 | (30 + 3√5)/19 (GSD: great stellapentakis dodecahedron); −(12√5 + 15)/11 (GI: great triakis icosahedron) | ⊛ (15 + 6√5)^½ | 2, φ in (1, join) |
| 4D convex | walls ρ_k²/h²: 5-cell 1, 8/3, 6, 16; tesseract 1, 2, 3, 4; 16-cell 1, 4/3, 2, 4; 24-cell 1, 4/3, 3/2, 2; 600-cell up to 28 − 12√5 | stellations: 16-cell at 2, 24-cell at 2, 600-cell at (6√5 − 2)/11, 120-cell at √5 − 1 (= the small stellated 120-cell) | ⊛ √g: 4, **2, 2**, √2 | 2 = ⊛ (tesseract, 16-cell), 2 = g (24-cell) |
| 4D stars | walls from the flags (table); many incidences (s3 log) | spike sides in the polychoron's own cell hyperplanes at √5 − 1 ({5/2,5,3}, {5,5/2,5}, {5/2,3,5}) and **at t = 2 ({3,5,5/2}, {3,5/2,5})** | ⊛ √g; **2 for the two g = 4 polychora** | |

Edge-tangent kis roots: at each root every edge of the kis is tangent to the midsphere, and the polar of the kis in that sphere has all
edges equal: a uniform polyhedron (s2b_kis_check.py, 17 roots, FINAL ok). A root t < 1 puts the apex beyond the centre, the dual of a
quasi-truncation. Roots where the apex lands on a corner are degenerate (tetrahedron −3, SSD −√5, GD √5). The names in the table are
the classical duals (Catalan; Wenninger's stellapentakis and triakis duals), identified through this uniform polar. They are not
checked face by face.

**Turned pairs.** On every star line, wall t_k ↔ g/t_k:
- cube: join 2 ↔ 3/2, the Catalan kis. The Catalan kis and the join are turned partners on the cube line.
- octahedron: 3/2 ↔ 2.
- tetrahedron: 3 is self-turned.
- tesseract and 16-cell: 2 is self-turned.
- 24-cell: 2 ↔ 1.

On the flag lines the turned pairs are those of the turn theorem, for every one of the 25 (walls c/ρ_k²).

**Are the growth steps hops?** Yes, in two layers.
- One step of T maps the star line's end t = 1 to its other end t = g, and the core step maps the flag line's end R² to its end h². In
  both cases every face of the old solid gives way at once to the faces of the new one, so a single step is a **jump** in the
  Paradigm's sense, made at the turned pair of ends (the ends are each other's turns: 1·g = g, R²·h² = c).
- Two steps return to the same shape: one **hop**, from a value to its return, with multiplier g (T) or t²/g (core). The product is
  t² for every regular polytope.
- For the stars, the T hop leaves the star world at once (corners only). The flag-wise hop stays among stars, star ↔ reciprocal star,
  with multiplier the star's own g.

## 4. Non-regular Star Cores (context only)

DICTO's own solids (studies 2026-10-30-star-cores-exact and 2026-11-02-halo-census) have two or more face families. Their core cycles
have period 2 with scale t²cos²θ (#81). Their T-chains have period 4 or never close (#80), and the turn exists only locally
(dual-sweeps theorem, ledger 60). The hop-product t² of Section 3 is special to one face family. For example, TI's core scale is
t²(5 + 2√5)/15, against a T period of 4. This study did not recompute them.

## 5. Prior art: every source checked (9 November 2026)

- **Library** (ask-library, 5 queries):
  - "stellation of a regular polytope pyramids on the faces Kleetope height"
  - "Kepler-Poinsot polyhedra Galois conjugate of the Platonic solids"
  - "Schlafli-Hess star polychora small stellated 120-cell stellation of the 120-cell"
  - "polar reciprocal of the convex hull of a polytope and its dual"
  - "uniform star polyhedra Wythoff construction Schwarz triangle density"

  Hits:
  - McMullen–Schulte 2005; Devadoss–Harvey–Richter 2026; Kunnen–Schlicker 1998; Leppmeier 2019
  - Richter-Gebert 2026 ("An almost trivial observation about the icosahedron"); Wikipedia "Goldberg polyhedron"; Messer 1995;
    Kerckhoff–Storm 2008
  - Hart 1996; Kaida Shi 2009
  - Cunningham–Mixer 2016; Matteo 2014; Baumbach et al. 2025; Berestovskii–Nikonorov 2023
  - Torquato–Jiao 2009; the pages Wikipedia Tetrahedral-octahedral honeycomb p. 13 (citing Coxeter 1940) and arXiv:1206.3716 p. 21

  None states the star-line theorem, the turn on it, or a t_min for star polytopes.
- **Web** (3 searches):
  - Wikipedia "Small stellated 120-cell" (the first stellation of the 120-cell, {5/2,5,3}) and "Great grand stellated 120-cell"; Polytope
    Wiki "Great grand hecatonicosachoron" (density 76, which matches the run)
  - Wikipedia "Kepler–Poinsot polyhedron"; blog posts on Galois conjugation of pentagons to pentagrams (informal; the conjugacy is used
    here only as checked in the exact data)
  - Wikipedia "Kleetope" (the Kleetope as the dual of the truncation of the dual); arXiv 1402.1660; Polytope Wiki "Polytope operations"
- **Earlier DICTO work used:**
  - #79–#81 (Star Cores, DICTO DOI 10.5281/zenodo.23867732, the book)
  - The DICTO Kepler–Poinsot–UP Cycle (DICTO DOI 10.5281/zenodo.23464021: the great stellated dodecahedron as the icosahedron's star at
    3, and the small stellated dodecahedron as the dodecahedron's star at √5, both reproduced here as stellation events)
  - studies/2026-11-09-turn-theorem
- **Classical, named and not re-read:** Coxeter, Regular Polytopes (densities, Wythoff construction); Coxeter, Longuet-Higgins and
  Miller 1954 (uniform polyhedra); Wenninger, Dual Models 1983 (the star duals).

## 6. LEADS

1. **The ends of the star flag line.** t_min\*(R²) = q₀⁺·q_{d−1}⁺/h² = (R/h)·cos∠(corner axis, face axis in one chamber). Prove the
   general rule for when the ends beat the turn. Only density 191 has the turn on top. Why that one?
2. **The coincidences of Section 2.4.** The turn values equal convex gains: 15 − 6√5 for SSD and GD, 28 − 12√5 for densities 4 and 6.
   Look for a reason, perhaps the tangent star's hull being a known regular solid.
3. **Uniform truncations as metric events on the flag lines.** They are polar to the edge-tangent kis of the dual star line, which
   gives μ° = R°²/t_C. List them exactly for all 25 lines, including the 4D uniform polychora of the Schläfli–Hess flags.
4. **4D edge-tangent kis.** The analogue of the Catalan event, with all ridges tangent, was not computed in 4D.
5. **Golden star φ.** It is never a wall in 3D. In 4D, φ appears as an incidence ("side through another tip") on the {3,5,5/2} and
   600-cell-type lines. Check whether that is a stellation of any named polychoron.
6. **A star T★ that stays among stars.** Corner-wise T loses the star at once. Write the flag-wise rule as DICTO's growth rule for
   stars, and test it on DICTO's non-convex pieces (Kagemusha).

## 7. Files and method

Scripts (scripts/, run on dicto-big-brother with ~/geom/bin/python -u, in the foreground, each under 2 minutes; logs in data/):
- regstar.py: the library. Mirrors from a corner set, mirror chains to flags, folding into the chamber, the flag line, t_min\*.
- s1_flags.py → flags.json: all 25 regular polytopes. Known-case check: exactly Coxeter's list and densities.
- s2_census3d.py → s2_census3d.json: the 3D census with exactlib (T, core, halos, stars, star-line events). Reproduces #80.
- s2b_kis_check.py → s2b_kis.json.
- s3_census4d.py → s3_census4d.json: the 4D census.
  - T² = gP exactly for the six convex polytopes.
  - Two core turns = P/g exactly.
  - The tesseract at t = 2 gives the 24-cell; the small stellated 120-cell is the 120-cell at t = 2/φ.
- s4_starturn.py → s4_starturn.json: the turn for stars.
  - The convex closed form is exact for all 11 convex polytopes; the flag-local closed form is exact for all 25.
- s5_table.py → census_table.csv and census_table.json.
- s6_plate.py → figures/regular-stars-plate.png: the nine solids with their doubled stars in their halos, and the five flag-line curves.
  It carries the DICTO mark.

Copied in: q5.py and turnlib.py from studies/2026-11-09-turn-theorem. exactlib is the dataset v7 library.

## 8. Concordance ledger lines

{"question": "Census: Star Core, Star Halo, gains and core cycles of all regular polytopes (5 Platonic, 4 Kepler-Poinsot, 6 convex 4D, 10 Schlafli-Hess), with known vs new", "method": "exact Q(sqrt5): all 25 regular polytopes from mirror chains (Wythoff) of Td, Oh, Ih, A4, B4, F4, H4, densities by chamber count; exactlib T-chains and core_turn (#79-#81 definitions), 4D exact T^2 = gP and two core turns = P/g; star-line events by exact incidence solving; edge-tangent kis checked uniform (studies/2026-11-09-regular-stars-census)", "status": "SETTLED", "result": "all 25 found (Coxeter list and densities reproduced); T gain per period g = (R/h)^2: 9, 3, 3, 15-6sqrt5 (x2), 16, 4, 4, 2, 28-12sqrt5 (x2); stars: T reads corners only, so hull chain (15-6sqrt5 or 28-12sqrt5); flag-wise star gain = own g (5, 15+6sqrt5, 6+-2sqrt5, 4, 28+12sqrt5); Star Core/Halo/Polar Halo = dual (convex) or hull of face centres / reciprocal star (stars); core cycle period 2, two-turn scale t^2/g; known: RD = cube at 2, 24-cell = tesseract at 2, SSD = D at sqrt5, GSD = I at 3, small stellated 120-cell = 120-cell at sqrt5-1; other doubled/golden stars not named in sources checked; KP numbers Galois-conjugate to the Platonic ones", "retry": "never; only LEADS 3-5 (uniform truncations as flag-line events, 4D edge-tangent kis, golden incidences in 4D)", "study": "studies/2026-11-09-regular-stars-census", "date": "2026-11-09"}

{"question": "Turn for stars: on the flag line S*(mu) = G.Delta(mu) of a regular star polytope (Kepler-Poinsot, Schlafli-Hess), does the antipol identity hold and is t_min* largest at the turn mu = hR", "method": "flag line from the exact flag; t_min* = max a+.b+ by folding into the chamber (dominance), exact Q(sqrt5) at 13-22 samples per line + 4001-point scans, 25 lines; flag-local closed form checked exactly (studies/2026-11-09-regular-stars-census, s4_starturn.py)", "status": "SETTLED", "result": "antipol identity S*(mu)^v = h^-2 S*(c/mu) and turn symmetry hold for all 25; the turn theorem holds verbatim within one flag for all 25 (only Lemma 1, dominance, fails for stars); globally the peak at the turn FAILS for all 14 stars: max at the ends (q0+.q_{d-1}+/h^2 = sqrt5, phi^3, sqrt5-1, 1+sqrt5, 2) for 12, turn = global max but not log-concave for the two density-191 polychora (6.996416); SSD/GD: turn is the minimum 15-6sqrt5; log-concavity fails on all 14 star lines", "retry": "never; only LEAD 1 (rule for when the ends beat the turn) or LEAD 2 (turn values = convex gains)", "study": "studies/2026-11-09-regular-stars-census", "date": "2026-11-09"}

{"question": "Hopscotch star line: the hulls of DICTO's stars K_t = conv(P u t.feet) as a polar line with a turn; are growth steps hops", "method": "proof (polar of conv(A u B) = A° ∩ B°) + exact walls and incidences on 9 3D and 16 4D lines (studies/2026-11-09-regular-stars-census)", "status": "SETTLED", "result": "for regular P, K_t (1 <= t <= g) is the polar of the dual's polar line at mu° = R°^2/t; walls t = rho_k^2/h^2 (1, join, g = T(P)); turn t -> g/t, fixed point sqrt g = R/h (tips on the circumsphere); one T step = jump end to end, two steps = one hop x g; core hop x t^2/g; product t^2; DICTO's t = 2 is the turn's fixed point for g = 4 (tesseract, 16-cell, great stellated 120-cell, grand 120-cell), the join of the cube, the T end of the 24-cell", "retry": "never", "study": "studies/2026-11-09-regular-stars-census", "date": "2026-11-09"}
