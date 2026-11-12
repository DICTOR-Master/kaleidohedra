# Near but never on (13 Nov 2026; aim 2, candidate route to DICTO's "Canonical Law")

**Conclusion (13 Nov 2026): "never on" is false in general: on every self-dual line and on B4 the special points sit EXACTLY ON hR (Theorems A, B, proved); on the other lines they are off by -f(0)/f'(0) to first order (certified), but nearness is not a law (B_d drifts), so "Canonical Law" is not earned.**

Script `scripts/near_on.py` (log `data/near-on.log`, `data/near-on.json`; pilot `data/near-on-pilot.log`), compute node through the
job gate (jobs nearon-pilot, nearon), 2 worker processes, 669 s, 150 checks, FINAL ok. Exact arithmetic in Q(sqrt5) (field class and
pulling triangulation of pds_line.py, exact root counter of canon_unique.py, both executed from their files, not retyped). Numerical
only where marked: the s-expansion values are printed from 50-digit evaluations of exact formulas; the L1 norm in the radial bound
(Monte Carlo).

## Setting and words
Polar line S(mu) = {w.x <= 1, w the facet vectors of P} cap {v.x <= mu, v the corners of P}; turn mu -> c/mu, c = (hR)^2, fixed point
hR (the insphere point; Turn Theorem, ledger [71]). G = Sym(P), k = the first degree with a G-invariant harmonic H (one-dimensional in
every case here; Coxeter degrees). The canonical form at the centre, Omega(S(mu); y) = d! vol((S - y)°), has Taylor terms
d! C(n+d,d) INT_{S°} (x.y)^n dx (moment identity of the aim 2 paper); its first direction-dependent term is **T(mu) H(y)**: we call T the
form's tone (T = B(mu) of chunk 6 on the 600-cell line, checked equal exactly). The **corner tone** is H(corner of S(mu)) (the corners
are one G-orbit in each chamber). Special points: zeros of either tone (the roundest point and the design station of chunks 3 and 6).
Write mu = hR e^s and **f(s) = mu^lam T(mu), lam = (d+k)/2**; the turn is s -> -s.

## 1. Results per line (EXACT: zeros counted on the whole line, value at hR decided exactly)

| line | d, k | self-dual | form zero(s) | corner station(s) | hR | ON? |
|---|---|---|---|---|---|---|
| square | 2, 4 | yes (eps -1) | sqrt2 | sqrt2 | sqrt2 | ON |
| tetrahedron | 3, 3 | yes (eps -1, g = -I) | 1 (a wall) | 1 | 1 | ON (S(1) = octahedron) |
| tetrahedron, 2nd tone | 3, 4 | eps +1 | none | 0.553810, 1.805674 (product 1) | 1 | a turn PAIR |
| cube | 3, 4 | no | 1.692590 (mu^4+2mu^3+mu^2-4mu-14) | **phi = 1.618034** | 1.732051 | off |
| icosahedral | 3, 6 | no | 2.891793 (degree 12) | 2.911240 | 2.875087 | off |
| B4 | 4, 4 | no | 2 (a wall) | 2 | 2 | ON (S(2) = 24-cell) |
| 24-cell | 4, 6 | yes (eps -1) | 1/sqrt2 | 1/sqrt2 | 0.707107 | ON |
| 5-cell | 4, 3 | yes (eps -1, g = -I) | 4/5 | 4/5 | 4/5 | ON |
| B5 | 5, 4 | no | 2.306956 | 2.420861 | 2.236068 | off |
| B6 | 6, 4 | no | 2.605767 | 2.632456 | 2.449490 | off |
| 600-cell (hop) | 4, 12 | no | mu_Omega 0.921450 (deg 24) | mu* 0.924139 (deg 20) | 0.925615 | off |

Each zero is the only one of its kind on the whole line (B6 and 600-cell: on the chambers computed, 2..6 and the truncated-600-cell
hop; the 600-cell's other hops are chunk 6's exact count). New exact facts: the cube line's corner station is **mu = phi**: the 24
corners (+-1, +-1/phi, 0) are the two icosahedra of a compound, a 5-design. The 24-cell line's corners at hR are silent in degree 6
(a 7-design); the tetrahedron's second tone gives a corner pair mu, 1/mu.

## 2. Theorem A (the parity law; PROVED)
Let P be regular and self-dual by an isometry g with g(unit facet normals) = unit corner directions and back, and H o g^-1 = eps H.
Then g S(mu)° = (hR/mu) S(c/mu)°, so INT over S(mu)° of H = eps (hR/mu)^(d+k) INT over S(c/mu)° of H, i.e. **f(-s) = eps f(s) on the
whole line**, and the corner tones obey the same rule. Proof: S(mu)° = conv(W cup V/mu) = (1/h) conv(X cup (hR/mu) Y) (X, Y the two
unit orbits); apply g and change variables (the Jacobian gives (hR/mu)^(d+k)). Consequences: eps = -1 forces both tones to vanish at
hR (ON); eps = +1 makes the special points come in turn pairs mu, c/mu, never on unless f(0) = 0 by accident.
Checked exactly as polynomial identities on every chamber pair: square, tetrahedron (eps -1 for H3, +1 for H4), 24-cell (g =
(1/sqrt2)[[1,1,0,0],[1,-1,0,0],[0,0,1,1],[0,0,1,-1]], eps = -1 computed from the orbit sums), 5-cell (g = -I). Polygons in general:
the polar n-gon is the n-gon turned by pi/n and cos(n theta) changes sign, so eps = -1 and S(hR) is the regular 2n-gon: ON for every n.
Regular simplices in every dimension: g = -I and the first invariant degree is 3 (odd), so ON.

## 3. Theorem B (the exact obstruction; PROVED)
**Both tones vanish at hR whenever the symmetry group of the fixed solid S(hR) has no nonzero invariant harmonic of degree k** (average
H over Sym(S(hR)): the integral over the invariant body S(hR)° and the sum over its corners only see that average). Theorem A with
eps = -1 is the case Sym(S(hR)) = <G, g>. The second case found: **B4**, where hR = 2 is a wall and S(2) = tesseract cap 2·16-cell is
the 24-cell, whose group W(F4) has invariants of degrees 2, 6, 8, 12 only (its 24 corners are a 5-design, checked exactly).
Conversely, when Sym(S(hR)) = G (all non-self-dual lines except B4), ON would need the single algebraic number f(0) = (hR)^lam T(hR)
(the fixed solid's own tone) to vanish; it is nonzero for cube, icosahedral, B5, B6 and 600-cell (exact). A proof that it can never
vanish when Sym(S(hR)) = G is NOT found: "never on" stays a checked statement for these five lines.

## 4. Why near: the even/odd reading (exact formula, certified numerics)
f(0) is the even part at the fixed point (the odd part vanishes there) and f'(0) is pure odd part (the even part has slope 0). So the
zero sits at **s* = -f(0)/f'(0) + O((f(0)/f'(0))^2)**, with f(0), f'(0) exact invariants of the fixed solid (its tone and the tone's
rate under the turn). (The brief's phrasing "odd part over slope of the even part" is the other way round: value from the even part,
slope from the odd part.) The Kantorovich test (|f''| bounded on |s| <= 2|s1|) certifies the zero within t* in every case:

| line | f(0) | f'(0) | s1 = -f(0)/f'(0) | exact s* | rel. error | Newton s2 | certified t* |
|---|---|---|---|---|---|---|---|
| cube | -0.3708 | -15.85 | -0.023393 | -0.023046 | 1.5% | -0.0230463 | 0.02404 |
| icosahedral | 0.011305 | -1.9419 | 0.0058215 | 0.0057937 | 0.5% | 0.0057937 | 0.00587 |
| B5 | 7.752 | -253.1 | 0.030631 | 0.031210 | 1.9% | 0.0312098 | 0.03175 |
| B6 | 72.51 | -1260.6 | 0.057521 | 0.061847 | 7.0% | 0.0618257 | 0.06539 |
| 600-cell (form) | -2.3154 | -519.0 | -0.0044610 | -0.0045100 | 1.1% | -0.0045100 | 0.004526 |

So "near" means: the fixed solid's tone is small against its odd slope (|f(0)/f'(0)| from 0.0045 to 0.06). The formula explains the
size of every displacement but does not say why the ratio is small; it is not small by any proven bound.
Two candidate explanations tested and REJECTED: (i) the two-ends model mu_m = (-T_V/T_P)^(1/(d+k)) (pure powers on the outer chambers,
exact) misses badly: cube 1.7772 (wrong side), icosahedral 2.7965, B5 2.5154, 600-cell 0.8965; (ii) the radial bound |T(hR)| <=
d! C(k+d,d) ((1/h)^(d+k) - R_S^-(d+k)) ||H'||_1 / (2(d+k) |H(u1) - H(u2)|) (h/R_S = in/circumradius of the fixed solid) holds but is
14 to 60 times too large (ratios 0.016-0.068).

## 5. Nearness is not a law (B_d family, exact)
On the B_d line the corner (1^m, t, 0, ..) gives the station equation (d+2)(m + t^4) = 3(m + t^2)^2: the station sits near
(d+2)/3 while hR = sqrt d; they agree only for d = 1, 4 ((d+2)/3 = sqrt d iff d^2 - 5d + 4 = 0). Stations d = 3..16: phi, 2, 2.4209,
2.6325, 3, 3.4233, 3.6379, 4, 4.4245, 4.6408, 5, 5.4253, 5.6426, 6 against sqrt d (B16: 6 vs 4). The form's zero drifts too: relative
offset -2.3% (B3), 0 (B4), +3.2% (B5), +6.4% (B6). The low-dimensional nearness of chunks 3 and 6 is a small-dimension effect, not a
general law.

## 6. Answers to the brief
1. Why near: Section 4 (exact first-order formula from the even/odd split; certified). 2. Quantitative: |log(mu_special/hR)| <= t*
(Kantorovich, explicit from the chamber's exact tone; values above); asymptotically -f(0)/f'(0). 3. "Never on" is FALSE in general:
exact obstruction = Theorem B (symmetry of the fixed solid killing H); for lines without it, ON needs f(0) = 0, nonzero in all five
cases, unproved in general. 4. New lines: self-dual tetrahedron, 24-cell, 5-cell, square: exactly ON; B4: ON (24-cell at the
fixed point); B5, B6: off. 5. A law emerges in the form of Theorems A and B (when ON is forced) and the first-order displacement
formula; nearness itself is not a law.

## 7. Controls (150 checks, all ok)
POSITIVE: the four known stations exactly: cube 1.692590 (quartic factor), icosahedral 2.891793 (degree 12), 600-cell mu* (degree 20)
and mu_Omega (degree 24); our tone equals chunk 6's B exactly; counter synthetic controls; in every chamber the tone is one number (a
third axis agrees exactly), lower orders isotropic, one corner orbit, equal facet volumes; tone continuous at every wall; H harmonic.
NEGATIVE: a perturbed, non-regular tetrahedron (centred): order-3 term at mu = 1 nonzero (-29.62) and the parity identity broken; on
the cube line f(s) is neither +f(-s) nor -f(-s).
Faults fixed on the way (pilot, 4 runs): the fixed-point chamber was picked by a wrong index (cube used the (2,3) formula); counting
zeros in mu stalled 15 min in the icosahedral chamber 1 (counting in nu = 1/mu, the canon_unique path, takes 1 s; the stalled
polynomial was not diagnosed); a missing d! in the radial bound; a waiter loop that matched its own command line.

## LEADS
1. Prove or refute: Sym(S(hR)) = G implies f(0) != 0 (the converse of Theorem B). A counterexample would be a non-self-dual line ON
   by accident.
2. Why |f(0)/f'(0)| is small in 3D and 4D: a weighted-design reading (the hull of the two unit orbits X cup Y is near a weighted
   design: the 6 + 8 points of the cube line carry the classical 14-point degree-5 cubature).
3. Star polytopes (ledger [74] census) and quasi-regular lines: self-dual stars (great dodecahedron / small stellated dodecahedron
   pair is not self-dual; check the 4D self-dual stars) under Theorems A and B.
4. B_d for d = 9, 16 (hR on a wall, no symmetry jump expected): is the form tone off there, as Theorem B predicts nothing?
5. The cube line's corner station at phi (two icosahedra) as a figure: the golden ratio on the cube-octahedron line.

## Ledger line (ready)
See the Concordance ledger entry dated 2026-11-13 (question "near but never on").

## Sources checked
studies/2026-11-10-canonical-sweep (canon_turn.py, canon_closed.py, canon_unique.py; README chunk 3), studies/2026-11-12-pds-hopscotch-line
(pds_line.py, pds_exact.py, data/pds-line.json, README), the aim 2 paper draft papers/2026-11-12-geometry-gives-laws (paper.html:
Proposition 4, the moment identity, B(mu) as a P12-moment, the Turn Theorem normalisation); Concordance ledger [58], [68], [71], [74],
[166], [168], [179], [193]. Classical facts used: Coxeter degrees of the groups; orbits of W(F4) are 5-designs; Kantorovich's theorem.
The reference library was not searched for this question.

DICTO · dictospheres.com
