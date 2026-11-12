# Palindromic middles: the reversal kills the first tone (13 Nov 2026; lead 4 of swaps-and-fixed-points)

**Conclusion (13 Nov 2026): CONFIRMED and PROVED: at every palindromic seed of A4 and F4 the first tone of the canonical form and of the corners is EXACTLY zero (A4 degree 3, F4 degree 6; 5 palindromic seeds each), because the seed reversal is an isometry that flips the sign of the tone (eps = -1, computed exactly on 6 reversed pairs and 6 points of the seed line); the next tone (A4 degree 4, F4 degree 8) survives, and B4 and H4 middles carry a nonzero tone, one-signed at every sampled point of the seed line (B4: t from 1/2 to 2; H4: t = 1/2, 1, 2; no zero count done), so "NEAR for B4 and H4" is NOT supported by the samples; it is not refuted.**

Script `scripts/middles.py` (logs `data/middles-pilot.log`, `data/middles.log`; data `data/middles-pilot.json`, `data/middles.json`).
Compute node through the job gate (jobs middles-pilot, middles), 4 worker processes, full run 61 s, 128 checks, 0 FAIL, FINAL ok.
**Exact arithmetic throughout**: Q(sqrt2) for A4, B4, F4 (uniform seeds need sqrt2 where root lengths differ), Q(sqrt5) for H4. No
floating point decides anything; floats are printed only as a guide (for H4 the printed differences round to 0 though the exact values are not 0).

## Setting and words
S(lam) = Wythoff polytope of a seed lam = (lam1..lam4) given by EDGE LENGTHS (the edge along node i has length lam_i), centred at 0, so a
palindromic seed (a, b, b, a) is the uniform-type polytope that the reversal of the diagram maps to itself. Polar S° = conv(n/c) over the
cells {n.z <= c}. Form moment t_k(y) = INT over S° of (x.y)^k dx: the degree-k Taylor term of the canonical form at the centre
(up to d! C(k+d, d); moment identity of the aim 2 draft). Corner moment C_k(y) = SUM over corners of (v.y)^k. Both are W-invariant
polynomials of degree k. **Isotropic in degree k** = t_k(y) (resp. C_k(y)) the same for four test vectors y of one norm lying in four
DIFFERENT W-orbits (orbit membership decided exactly); for odd k, all zero. At the first degree k with a W-invariant harmonic H_k
(A4: 3, B4: 4, F4: 6, H4: 12) the only invariants of degree k are |y|^k and H_k, so isotropic <=> the **tone** T (coefficient of H_k) is 0.
Integration: each polar facet (dual of the corner figure) is triangulated combinatorially (cells at the corner; cyclic order of the
cells round each edge read from the 2-faces), coned from the origin, and INT over a simplex of (l.x)^k = vol k! d!/(k+d)! h_k(l.v_i).

## 1. Results (exact)

| group | seeds | first tone degree | tone at the seed | next degree | there |
|---|---|---|---|---|---|
| A4 | palindromes (0,1,1,0) (1,0,0,1) (1,1,1,1) (1,2,2,1) (2,1,1,2) | 3 | **0** (form and corners); degrees 5, 7 also 0 | 4 (and 6) | nonzero |
| F4 | the same five palindromes | 6 | **0** (form and corners) | 8 (and 10, 12) | nonzero |
| A4, F4 | non-palindromes (0,1,1,1) (1,1,1,0) (1,1,0,0) (0,0,1,1) (1,2,3,4) (4,3,2,1) | 3 / 6 | nonzero, 12 of 12 | | |
| B4 | (0,1,1,0) bitruncated tesseract, (1,0,0,1), (1,1,1,1) | 4 | nonzero, 3 of 3 | | |
| H4 | (0,1,1,0) bitruncated 600-cell (3600 corners) | 12 | nonzero (degrees 2, 6 isotropic) | | |

**The reversal law (exact).** For each reversed pair lam, rev(lam) the tone flips sign: T(rev lam) = -T(lam), form and corners, A4 and F4,
on (0,1,1,1)/(1,1,1,0), (1,1,0,0)/(0,0,1,1), (1,2,3,4)/(4,3,2,1): eps = -1 in all 12 comparisons. Along the seed line (0,1,t,0):
T(t) = -t^-(4+k) T(1/t) for the form and C(t) = -t^k C(1/t) for the corners, at t = 2, 3, 3/2 (A4 k = 3, F4 k = 6; 12 comparisons), the
tone nonzero at every t != 1 tested and zero at t = 1.

**Theorem (PROVED, given the exact sign).** Let W be A4 or F4 and phi the isometry realising the diagram reversal (A4: x -> -w0 x;
F4: the map exchanging the 24-cell and its dual). phi normalises W, so it acts on the one-dimensional space of degree-k invariant
harmonics (k = 3 for A4, 6 for F4) by a sign eps; phi maps S(lam) onto S(rev lam), hence T(rev lam) = eps T(lam) for every seed.
The computed pairs give eps = -1 (one nonzero exact example decides the sign). So T vanishes at every palindromic seed, real or not.
For A4 this is -I: every odd moment vanishes (degrees 3, 5, 7 checked); for F4 it is the outer automorphism, which kills degree 6 but
not 8. This is near-but-never-on Theorem B with Sym(S) = <W, phi>, and Theorem A (eps = -1) read on seeds instead of the polar line.

**Link to near-but-never-on.** The 5-cell line and the 24-cell line of that study (ON at hR = 4/5 and 1/sqrt2) pass through exactly these
middles: at (0,1,1,0) the two end cell families are at equal distance from the centre (checked exactly for A4 and F4), so S(hR) on each
polar line is the uniform bitruncated 5-cell / 24-cell. Its ON result is reproduced here; the new content is the whole palindromic
family (non-0/1 seeds (1,2,2,1), (2,1,1,2), the runcinated (1,0,0,1), omnitruncated (1,1,1,1)) and the sign law along the seed line.

## 2. B4 and H4: no reversal symmetry, no zero found
B4 seed line (0,1,t,0), degree-4 tone at t = 1/2, 2/3, 1, 3/2, 2: form difference -2.774, -1.195, -0.2735, -0.0437, -0.00956 (one sign);
corner difference 34560, 43680, 64800, 103680, 151200 (one sign). The parity identity fails at t = 2 and 3/2 (as it must).
H4 seed line, degree 12, t = 1/2, 1, 2: exact signs constant (form +, corners -) on three test-vector differences each; parity fails at t = 2.
So on these seed lines the tone has no sign change in the tested points: the swaps study's prediction "NEAR for B4 and H4" is not supported
here (sampled only; no claim that no zero exists elsewhere). Note: on the B4 POLAR line the fixed point is ON (the 24-cell, Theorem B of
near-but-never-on); that line meets the B4 middle at no fixed point and is a different object.

## 3. Controls (128 checks, all ok)
SHOULD PASS: cross-polytope moments exact (INT x1^2 = 2/45, INT x1^4 = 1/105, INT (x1 + x2)^4 = 1/35); degree 2 isotropic for every
polytope (form and corners); F4 degree 4 isotropic for every F4 seed (no F4 invariant of degree 4); H4 degree 6 isotropic; ends equidistant
at the A4 and F4 middles. SHOULD FAIL (and did): A4 degree 4 at all 5 palindromes; A4 degree 3 and F4 degree 6 at all 6 non-palindromes;
B4 degree 4 at 3 seeds; H4 degree 12 at the middle; the parity identity on the B4 line (t = 2, 3/2) and the H4 line (t = 2).
Fault fixed in the pilot: two F4 test vectors, (6,3,2,1) and (5,4,3,0), lie in ONE F4 orbit, so their difference saw no tone and the F4
line checks failed spuriously; test vectors are now chosen in distinct orbits by exact orbit membership.

## LEADS
1. The F4 middle's first surviving tone is degree 8: compute its zero along the 24-cell polar line (is the degree-8 silent point ON or NEAR?).
2. B4 and H4 seed lines: an exact zero count of the tone for t in (0, inf) (rational function in t per chamber); sampled one-signed here.
3. E6 (diagram reversal also a symmetry, -w0 not -I): the same law predicts the tone of the first non-reversal-invariant harmonic dies at
   palindromic seeds of E6; D4 triality gives three-fold versions.
4. Seeds by edge length vs by root label: for B4 and F4 the label seed (0,1,1,0) is not uniform; the law needs edge lengths (sqrt2 enters).

## Sources checked
studies/2026-11-13-near-but-never-on (README: Theorems A, B, the 5-cell and 24-cell lines, eps for the 24-cell); studies/2026-11-13-rosette-balance
(rosette_balance.py: root systems, Q(sqrt5) arithmetic, corner and cell construction, adapted here to Q(sqrt m)); studies/2026-11-13-swaps-and-fixed-points
(row 12, lead 4); studies/2026-11-11-orbit-polytopes (Mirror Law middles); the aim 2 draft (moment identity). Classical facts: Coxeter degrees
(A4: 2, 3, 4, 5; B4: 2, 4, 6, 8; F4: 2, 6, 8, 12; H4: 2, 12, 20, 30), diagram automorphisms of A_n and F4, the simplex moment formula with
complete homogeneous symmetric polynomials. The reference library was not searched.

## Ledger line (ready)
2026-11-13, question "palindromic middles (A4/F4 seed reversal, Theorem B)": tone exactly 0 at all palindromic seeds of A4 (deg 3) and F4 (deg 6),
eps = -1 proved/computed; next tone (4 / 8) survives; B4, H4 middles nonzero, one-signed at the sampled seed-line points (no zero count); 128 checks, FINAL ok.

DICTO · dictospheres.com
