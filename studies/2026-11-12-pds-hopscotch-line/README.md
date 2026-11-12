# Aim 2, chunk 6: the Poincaré dodecahedral space along the Queens' Hopscotch line (12 Nov 2026; DICTO "go ahead with chunk 6 on node")

**Conclusion (12 Nov 2026): EXACT. On the Queens' Hopscotch line the PDS's first mode P12 picks out two stations in the truncated-600-cell
hop and neither is the turn's fixed point r = 0.925615: the corners form a 19-design exactly at μ* = 0.924138673… (degree 20 over Q;
the book's grid value 0.924165 is corrected), and the canonical form falls silent at order 12 exactly at μ_Ω = 0.921449634… (a
degree-12 factor over Q(√5)); the turn keeps neither. Every Ω(S(μ); y) on the line is isotropic through order 11 and first sounds
the PDS mode B(μ)·P12(y) at order 12 (scripts/pds_line.py, 40 checks, FINAL ok).**

## 1. What Silent Queens proved, and what "along a Hopscotch line" means here

**Silent Queens** (#107, Chapter 9 of *Alicia in Wonderland: The Red & White Queens*, v4, 7 Nov 2026; studies 2026-11-04-harmonic-4d,
-hopf-interlock, -pds-modes; ledger [28]). Proved, all classical and credited (Goethals and Seidel; Coxeter; Sadoc and Mosseri; Klein):
1. Heard as tones on the 3-sphere, the White Queen (600-cell, 120 corners) and the Red Queen (120-cell, 600 corners) are silent in every
   degree 1 to 11 and sound first at degree 12: both are spherical 11-designs.
2. Read as a group, the White Queen's corners are the 120 icosians, the group of the Poincaré dodecahedral space (PDS = S³/icosians).
   The number of degree-k harmonics invariant under the icosians equals Aurich, Lustig and Steiner's PDS mode count at every k = 0..120;
   so the Queens' silence below 12 is the PDS's missing low modes (first mode k = 12, Klein's degree-12 invariant).
3. Read as rings (Hopf map): 12 decagons, 20 hexagons, 30 squares onto the icosahedron, dodecahedron, icosidodecahedron.
Numerical only (labelled so in the book): on the path between the Queens S(μ) = 600-cell ∩ μ·120-cell, the 1440 corners of the
truncated stage form a 19-design at μ ≈ 0.924165 (degree-12 tone vanishes; classical Goethals–Seidel route; "exact μ* still to compute").

**The Hopscotch line.** The path between the Queens is the H4 polar line of the Turn Theorem (ledger [71], studies/2026-11-09-turn-theorem):
P = 600-cell with circumradius R = 1 and inradius h = r = 0.925615, S(μ) = {facet planes of P} ∩ {corner planes v·x ≤ μ}, r² ≤ μ ≤ 1.
S(1) = White Queen, S(r²) = Red Queen (scaled). Walls = squared flag radii 1, ρ1², ρ2², r² (stages truncated 600-cell, bitruncated,
truncated 120-cell between them). **The turn:** μ ↦ r²/μ (S(μ)^∨ = r⁻² S(r²/μ)), fixed point μ = r, where every facet touches one sphere.

**The family:** the H4-symmetric solids S(μ) on this line. Every one of them is invariant under W(H4), which contains left and right
multiplication by the icosians; so any harmonic quantity built from S(μ) lives on the PDS, and below degree 12 it can only be constant.

**The invariant:** the PDS's first mode, the degree-12 W(H4)-invariant harmonic P12 (Klein's degree-12 invariant, made harmonic), read
two ways along the line:
- (i) on the corners (the Silent Queens reading): the corners of S(μ) are one W(H4) orbit in each hop, so they are silent through
  degree 11 everywhere, and silent through degree 19 exactly where P12(corner) = 0 (19-design stations);
- (ii) on the canonical form (the aim 2 reading, chunks 2 to 5): Ω(S(μ); y) = 4!·vol((S − y)*) expanded at the centre is a series of
  W(H4)-invariant polynomials, hence isotropic through order 11; its first direction-dependent term is B(μ)·P12(y) at order 12, the
  PDS's lowest mode. B(μ) is the canonical form's "tone".

**The questions:** exact 19-design stations on the whole line (is the book's μ ≈ 0.924165 exact, and is it the turn's fixed point
r = 0.925615, which it nearly equals?); exact B(μ) per hop, its zeros (the canonical form's "silent" points) and their place relative
to the fixed point and the design stations; does the turn keep either set of stations?

Ledger read before any test: [28] PDS modes (counts settled, never retry: not retried, only cited); [21] 600-cell slices; [71] Turn
Theorem (line, walls, turn: used, not retried); [74] census; [129], [130] H4 orbit seeds (the stages are W(H4) orbits); [166] chunk 3
(icosahedral roundest point near but not at the fixed point: the 3D analogue of question (ii)); [167]–[177] chunks 4, 5. No entry
computes the exact 19-design station, nor the canonical form of any 4D solid on this line. Nothing here retries an earlier attempt.

## 2. Method (scripts/pds_line.py; log data/pds-line.log, data/pds-line.json; pilot data/pds-line-pilot.log; compute host, 469 s, 4 cores)

Exact arithmetic in Q(√5) (own class on Fractions) and sympy over QQ<√5>. White Queen: the 120 icosians (circumradius 1); its 600
cells give the facet normals w (w·v = 1 on the cell), which are the Red Queen's corners. S(μ) = {w·x ≤ 1} ∩ {v·x ≤ μ}.
- **Corners and P12.** P12 = Σ_v (v·y)¹² − 120·E[x₁¹²]·|y|¹² (E over S³). In each hop the corners are one W(H4) orbit, so the
  corner set is silent in degree 12 iff P12(corner) = 0, and then silent through degree 19: W(H4) has no invariant harmonic in degrees
  13 to 19 (odd degrees die by −I; degrees 14, 16, 18 have none by Coxeter's basic invariants 2, 12, 20, 30). The corner x(μ) is
  affine in μ (four tight planes), so P12(x(μ)) is an exact degree-12 polynomial in μ over Q(√5), factored over Q(√5), with its norm
  to Q giving the minimal polynomial.
- **Canonical form.** Ω(S; y) = 4!·vol((S − y)*) = Σ |det(q₁..q₄)| / Π(1 − q_j·y), summed over a pulling triangulation of the
  boundary of S* = conv(q), with q = w (type 0) or v/μ (type 1). This is the chunk 2/3 formula; the triangulation is built exactly from
  the face lattice, which is fixed in each hop, so it holds for the whole hop. Along y = t·u each term is a product of geometric
  series, and the Taylor coefficients c_k(u) are exact polynomials in ν = 1/μ over Q(√5). Directions: a White Queen corner, a Red
  Queen corner and the generic (1, 2, 3, 5). Every Taylor coefficient is a W(H4)-invariant polynomial, so c_k is isotropic for k < 12
  and c₁₂(u) = A(μ)|u|¹² + B(μ)·P12(u). B is fixed by two directions and checked exactly on the third.
- Combinatorics: qhull at one rational μ per hop gives candidate faces; each tight set is then confirmed exactly (the smallest float
  margin of a non-tight plane is 0.018).

## 3. Results (EXACT unless marked)

**Line data.** r² = (7 + 3√5)/16 (r = 0.9256147934, minimal polynomial 64m⁴ − 56m² + 1). The walls are the squared flag radii 1,
(5 + √5)/8 = 0.904508, 1/2 + √5/6 = 0.872678 and r². A float scan at 41 μ finds corner changes only across the two inner walls. Hops
(sample μ: corners, facets per corner, simplices): truncated 600-cell (3809/4000: 1440, 6, 4320); middle hop, the bitruncated stage
(88859/100000: 3600, 4, 3600); truncated 120-cell (10809/12500: 2400, 4, 2400). The turn μ ↦ r²/μ has its fixed point r inside the
truncated-600-cell hop.

**(i) The corners: one 19-design station on the whole line.** P12(x(μ)) has exactly one root in the line's interior:
  μ* = 0.924138673238867458601238076667, in the truncated-600-cell hop. Its minimal polynomial over Q has degree 20:
  1048576m²⁰ − 13107200m¹⁹ + 69468160m¹⁸ − 195952640m¹⁷ + 278528000m¹⁶ − 20480000m¹⁵ − 683458560m¹⁴ + 1317437440m¹³ − 1168629760m¹²
  + 290048000m¹¹ + 501350400m¹⁰ − 656972800m⁹ + 384408320m⁸ − 117126400m⁷ + 9318400m⁶ + 6118400m⁵ − 2304080m⁴ + 318600m³ − 12000m²
  − 900m + 45.
  The middle hop and the truncated-120-cell hop have no station. **This corrects the book's numerical value 0.924165** (#107 Ch. 9 §5;
  a 400-point grid with step 2.4·10⁻⁴; the difference is −2.6·10⁻⁵, within one grid step). The 1440 corners at μ* are silent to
  10⁻¹⁶ in degrees 2 to 18, and degree 20 sounds at 8·10⁻⁸ (NUMERICAL, float moments; the 19-design property itself is exact by the
  argument above). μ* is NOT the turn's fixed point: its minimal polynomial differs from r's (exact). Its turn image r²/μ* =
  0.927093 is not a station either, since μ* is the only one.
  CREDIT: an orbit of W(H4) through a zero of the degree-12 invariant is a 19-design (Goethals and Seidel 1981, as credited in
  #107). New here: the exact algebraic station on the Queens' path, its uniqueness on the whole path, and its position against the turn.

**(ii) The canonical form: silent through order 11, PDS tone at order 12.** In every hop, along all three directions, the odd orders
vanish and orders 2 to 10 are equal (isotropic). Order 12 is exactly A + B·P12(u), and the third direction agrees. So on the whole
line Ω(S(μ); y) = f(|y|²) + B(μ)·P12(y) + O(|y|¹⁴). Its first direction-dependent term is the PDS's lowest mode: P12 is invariant
under left multiplication by the icosians (checked: they permute the corners), so it descends to S³/icosians.
- Ω(S;0) = 4!·vol(S*), one power of μ per hop: 1440(47√5 − 105)/μ, then 1800(13√5 − 29)/μ², then 600(5√5 − 11)/μ³. The degree
  rises by one at each wall, as on the 3D lines of chunks 2 and 3.
- B(μ) = (exact degree-12 polynomial over Q(√5))/μ^(13, 14, 15) per hop (data/pds-line.json). B > 0 on the middle and
  truncated-120-cell hops. In the truncated-600-cell hop B changes sign once, at
  **μ_Ω = 0.921449634428905791812131090257**, a root of a degree-12 factor irreducible over Q(√5); this is the only point of the line
  where the canonical form is silent through order 13.
- At the fixed point r: B(r) = −4.2971334197 (30-digit evaluation; nonzero by a wide margin). So μ_Ω is not the fixed point, and since
  μ_Ω is the only zero on the line while r²/μ_Ω = 0.92981 ≠ μ_Ω, the turn does not keep the canonical form's silent point either.
- Order on the line: μ_Ω = 0.921450 < μ* = 0.924139 < r = 0.925615 < r²/μ* = 0.927093. Three distinct points lie within 0.0042 of
  each other. This is the 4D twin of chunk 3, where the icosahedral canonical form was roundest at 2.891793, near the fixed point
  2.875087 but not at it.

**Reading.** On the line between the Queens the PDS's first mode is the first direction-dependent signal, both in the corners and in the
canonical form. Each reading has exactly one silent station on the whole line, and both fall in the hop that holds the turn's fixed
point, close to it but not on it. The turn μ ↦ r²/μ is a symmetry of neither. As in chunk 3, the turn's fixed point is special only as
the insphere point; the harmonic silences sit beside it. No cosmology claim is made.

## 4. Controls (40 checks, all ok)
POSITIVE: cube–octahedron line by the same code: Ω(S;0) = 48/μ³, 48/μ², 24/μ (chunk 2), c₂/c₀ = (μ² + 2μ + 7)/(3μ²), and the order-4
anisotropy/c₀ = 2(μ⁴ + 2μ³ + μ² − 4μ − 14)/(9μ⁴) (chunk 3), all exact. White Queen and Red Queen (600 normals) are exact 11-designs
(polynomial identities k = 2..10) that sound at degree 12 (Silent Queens reproduced). P12 is harmonic (Laplacian 0 exactly). Left and
right multiplication by two icosians permutes the corners. Every facet of S* has the same 3-volume in each hop (one orbit, no simplex
missing). P12 is equal at all corners (float, all; exact, 6). The order-12 form agrees on the third direction.
NEGATIVE: the B4 line (tesseract ∩ μ·16-cell, μ = 3/2) is isotropic at order 2 but not at order 4, so the code sees anisotropy where
the group allows it. Dropping one simplex breaks order-2 isotropy in every hop. μ* + 1/1000 is not a station.

## LEADS
1. #107 (Alicia book, Ch. 9 §5): the 19-design station becomes exact, μ* = 0.9241386732… (degree 20). The text's 0.924165 is a
   grid value. Destination: a book version line, DICTO's call when.
2. The degree-20 mode (P20, the PDS's second mode): stations where Q20 = 0 on the line (the book's numerical μ ≈ 0.9540), exact by the
   same route; and whether any point has Q12 = Q20 = 0 (a 29-design candidate; generically not on a one-parameter path).
3. The facet side: the area measure of S(μ) (Minkowski) read by P12. Is its silent point the turn image of the corner station? The
   antipol swaps corners and facets.
4. B(μ) at the walls: B is continuous and its derivative kinks at the walls, as Ω(S;0) does in chunk 2. Prove it and give the
   one-sided values.
5. Chunk 7 (E8 at the Golden Ladder's top rung): E8's root system is a 7-design whose first invariant harmonic has degree 8. The same
   two readings apply on an E8 polar line (the 4₂₁ ∩ μ·dual line), with H4 ⊂ E8 through the icosians (the Elser–Sloane / Moody–Patera
   projection).

## Ready Concordance ledger line

```json
{"question": "aim 2 chunk 6: the PDS's first mode (degree-12 W(H4)-invariant harmonic P12) along the Queens' Hopscotch line S(mu) = 600-cell cap mu 120-cell: exact 19-design stations of the corners, the canonical form's order-12 tone B(mu), and their place against the turn mu -> r^2/mu", "method": "studies/2026-11-12-pds-hopscotch-line/scripts/pds_line.py: exact Q(sqrt5) + sympy; corner orbit per hop, P12(x(mu)) factored over Q(sqrt5); Omega = sum |det q|/prod(1 - q.y) on an exact pulling triangulation, Taylor coefficients to order 12 along 3 directions as polynomials in nu = 1/mu; 40 checks incl. C-O line (chunks 2/3 reproduced), both Queens 11-designs, B4 negative, dropped simplex", "status": "SETTLED (exact)", "result": "one 19-design station on the whole line, mu* = 0.9241386732388674586 (degree 20 over Q; corrects the book's grid value 0.924165), in the truncated-600-cell hop; Omega isotropic through order 11 in every hop, order 12 = A + B(mu) P12 (the PDS's lowest mode); Omega(S;0) = 1440(47sqrt5-105)/mu, 1800(13sqrt5-29)/mu^2, 600(5sqrt5-11)/mu^3; B has one zero, mu_Omega = 0.9214496344 (degree-12 factor over Q(sqrt5)); neither station is the turn's fixed point r = 0.9256148 (B(r) = -4.297), and the turn keeps neither", "retry": "never for these; new questions: P20 stations, facet-measure reading, B at the walls", "study": "studies/2026-11-12-pds-hopscotch-line", "date": "2026-11-12"}
```

## Sources checked
#107 (papers/book-queens/zenodo-metadata.json v4 description; studies 2026-11-04-harmonic-4d README, 2026-11-04-pds-modes README);
studies/2026-11-09-hopscotch-rows (bridge table, lead 5); studies/2026-11-09-turn-theorem (setting, walls, turn); chunks 2–5 READMEs
(2026-11-10-canonical-sweep, 2026-11-12-solids-canonical, 2026-11-12-yantra-cones-canonical); Concordance ledger entries [21], [28],
[71], [74], [129], [130], [166]–[177]. Classical tools used and cited: Coxeter's basic invariants of H4 (2, 12, 20, 30);
Goethals–Seidel 1981 (19-designs from W(H4) orbits); the positive-geometry canonical form = volume of the polar (Arkani-Hamed, Bai,
Lam 2017), as in chunks 2–5. The reference library was not searched for a published exact value of this station. Hardin–Sloane's
design tables were not checked; check them before any paper text.

DICTO · dictospheres.com
