**Verdict: UNIQUE (certified).** Kulaichev's yantra has exactly one admissible solution, the one in #103 Theorem 10. No second yantra exists. The polynomial system has exactly one other real solution with 0 < u < 1, at u = 0.66866 (a root of f348), and it is not a Śrī Yantra: t4 turns over, b6 > b7, and w5, w6 < 0. Two censuses agree. They use different elimination orders, different root isolators and different interval libraries.

# Uniqueness of Kulaichev's Śrī Yantra (study 2026-11-15)

DICTO, 15 Nov 2026: "yes start the yantra uniqueness check". This answers the question Kulaichev asked in 1984 (A. P. Kulaichev, *IJHS* 19.3, p. 285). Chiodo (*C. R. Math.* 359, 2021, p. 384) calls it "toujours ouverte", still open. Pustynski (*IJHS* 49.3, 2014, pp. 273–274) argued for uniqueness from residual plots on dense grids, which is numerical evidence only. Huet's conditions are used in Chiodo's form.

## Theorem (Kulaichev's question answered)

Take a circle of diameter 1 and nine isosceles triangles with a common vertical axis that meet Huet's conditions:
- the two great triangles are inscribed;
- seven apexes lie on bases;
- the 18 marmas and the 6 corner touches hold.

Add Kulaichev's four conditions:
- (a) the two great triangles are congruent;
- (b) the corners of the smallest top triangle lie on the circle;
- (c) the corners of the smallest bottom triangle lie on the circle;
- (d) the incircle of the innermost triangle is centred at the circle's centre.

Admissibility is as in #103 Theorem 1: bases strictly ordered, half-widths positive, apexes on the correct side, corners in the closed disc. Then there is **exactly one** such figure, up to the normalisation (the scale, and the labelling with t1–t5 pointing down). It is the yantra of #103 Theorem 10:
- slope u = 0.7504385160222140244060846…, a root of the irreducible f348;
- b1 = 0.10327007530820…, Q = b6 = 0.55070523297544…, S = b9 = 0.92006014590959….

Its count of 45 regions (Proposition 11) therefore belongs to the unique Kulaichev yantra.

## Exact problem formulation (as in #103: model.py, natural.py)

- **Frame.** Depth d is measured below the top point O, so the circle is x² + d² − d = 0. Triangle ti has base depth b_i, half-width w_i and apex depth a_i.
- **Coordinates.**
  - u = w7/b7, so b7 = R = 1/(1+u²).
  - v = w3/(1−b3), so b3 = P = v²/(1+v²).
  - Condition (a) is u = v, because inscribed isosceles triangles with apex on the circle are congruent exactly when their slopes are equal.
  - t = b1/w1, so condition (b) holds by construction: t1's corner is (t, t²)/(1+t²).
  - S = b9.
- **The construction is forced.** Every other quantity is the meeting point of two lines (scripts/s1_system.py, line by line, each line naming the marma or touch it uses). Q follows from the marma (1,3,8), which is linear in Q.
- **Equations.** Every admissible yantra satisfies:
  - G(u, S) = 0, which is (c);
  - H1(u, t, S) = 0, the closing equation from the marma (1,4,6);
  - D(u, t, S) = 0, which is (d) squared.
- **These are #103's polynomials.** They equal the published ones (audit stage 4, appendix H) up to constants and factors that are nonzero at any admissible yantra.

## Proof structure

1. **Divisor lemma (exact, s1).**
   - Every divisor met in the construction is nonzero at an admissible yantra. The 14 step divisors are differences of distinct base depths, or sums of two positive slopes. One is the marma (1,3,8) coefficient, which is nonzero because otherwise w1(R − b1)(b1 − P) = 0.
   - The check runs by induction in Singular: the denominator of each step divisor factors into polynomials already proved nonzero. That gives 23 such factors, among them u, u ± 1, t ± u, ut ± 1 and (1+u²)S − 1.
   - So the numerators of G, H1 and D vanish, and only the following factors are dropped: (t ∓ u) (b1 = b3), (ut ∓ 1) (b1 = b7), u, and (S − R)².
2. **Full elimination (exact, no factor chosen numerically).**
   - R1 = Res_S(G, H1) = (u−1)⁶u⁶(u+1)⁶(u²+1)⁴·A, with A of degree (50, 20) in (u, t).
   - R2 = Res_S(G, D) = (u−1)⁴u⁴(u+1)⁴(u²+1)⁴·B, with B of degree (44, 20).
   - A and B have no common factor.
   - E = Res_t(A, B) has degree 1744: (u−1)¹⁷⁸ u²⁷⁴ (u+1)¹⁷⁸ (u²+1)¹⁸⁵ · **f348** · f396.
   - Resultants lie in the ideal, so no division occurs here. Leading coefficients and components at infinity cannot lose a real solution in this direction.
   - Admissibility forces 0 < u < 1 (from b3 < b7). So u is a root of f348 or f396 in (0, 1).
   - The degree-1744 eliminant of the audit is this E. This study recomputes it in full and checks that nothing was set aside.
3. **Root census (s2): 8 + 8 real roots in (0, 1).** Three independent isolators agree:
   - Vincent–Collins–Akritas bisection (Descartes' rule, pure-Python integers, written here);
   - PARI/GP polsturm (exact Sturm counts: 1 on each interval, 0 on each gap) and polrootsreal;
   - FLINT/Arb complex root enclosures (python-flint).
   - Each root is held in a dyadic interval of width 2⁻¹⁴⁰⁰, certified by exact signs at the endpoints.
4. **Back-solving (s3, Arb ball arithmetic, 2400 bits).** For each of the 16 roots:
   - all 20 roots of A(t, u) are isolated, and those with 0 < t < u (from 0 < b1 < b3) are certified real;
   - B is evaluated at each of them: 45 are rejected because B ≠ 0, with certified margins (the smallest |B| is 3.1·10⁻¹⁰, at a root of f396);
   - for the 3 that are left, S is taken from G with R < S < 1, then H1 and D are tested: 1 is rejected (D ≠ 0);
   - **2 true solutions** remain. Each is certified by the Krawczyk test (exactly one solution in a box of radius 10⁻³⁰⁰), and each yantra is rebuilt in balls:
     - u = 0.66866: **not admissible**. b4 > b5, b6 > b7, w5 < 0, w6 < 0, t4's apex is on the wrong side, two corners lie outside the disc, and b5 > 1/2. Every one of these is certified.
     - u = 0.750438…: **admissible**, with every inequality strict and certified. It is Theorem 10's root.
   - Every (u, t, S) fixes the whole yantra, because the construction is forced. Hence there is exactly one admissible yantra.
5. **Independent census (s4, second compute machine).**
   - Elimination in the other order: Res_t(H1, D), degree (434, 50), then Res_S with G. Its only non-trivial factor is **f348** (f396 is an artefact of the first order).
   - The 8 roots are isolated by PARI Sturm bisection.
   - Back-solving uses mpmath interval arithmetic (iv): S by the quadratic formula; t by a 1-D branch and bound with interval Newton on H1; then D, Krawczyk and the admissibility rebuild.
   - Same result: one admissible solution (Theorem 10's), and the u = 0.66866 solution found again, not admissible.

**Controls.**
- Positive: Theorem 10's root passes every step.
- Negative:
  - B + 1 at the true u is rejected;
  - u + 2⁻²⁰⁰ is rejected;
  - f348 + 1 has no root in Theorem 10's interval;
  - Rh345 (DICTO's 3-4-5 rhombus, u = 3/4 exactly, which meets (a), (b) and (c) but not (d)): A has three real t-roots in (0, 3/4), and B rejects all three. So the census does catch a yantra that misses (d) by only 2.4·10⁻⁵.

## The two tiny extra triangles measured (DICTO, 15 Nov 2026: "yes measure them")

`scripts/s5_tiny_triangles.py` (job ytiny, FINAL ok; pilot ytiny-pilot) rebuilds Theorem 10's yantra as s3 does: f348's root in Theorem 10's interval, the t-root of A with B = 0, S from G, the Krawczyk box of radius 1e-300 (one solution certified), then the whole yantra in Arb balls at 2400 bits. The arrangement's combinatorics is read from a double-precision copy of it (the face walk of studies/2026-11-08-sri-yantra/scripts/figure.py, copied). That is the arrangement certified in #103 Proposition 11. Every corner is then recomputed in Arb as the meeting point of its two lines; the largest corner ball has radius 4.2e-591.

Checks (all hold): 45 odd regions (14, 10, 12, 8, 1), 41 triangles, 4 four-sided; the two smallest regions are the mirror pair in ring 3 and are certified smaller than every other region; the bounded regions' areas add up to the area of the union of the nine triangles, integrated slab by slab (0.532851924 both ways, no enclosed gap); the two great triangles have equal area; t5's corner lies on the far side of t4's right leg (certified sign).

Values (r = the circle's radius = 1/2 in #103's units; certified bounds, rounded outward; the log prints "+/- 1.98e-12" on the signed distance only because Arb's 8-digit display adds its rounding to the radius):

| quantity | certified value |
|---|---|
| tiny triangle (p, r, c) area | [2.312, 2.313]e-7 r² = [5.782, 5.783]e-8 D² |
| / great triangle (1.228 r²) | [1.882, 1.883]e-7 |
| / circle | [7.361, 7.362]e-8 |
| / smallest other triangle (ring 4, at t4 right leg, t5 right leg, t6 base, t9 right leg) | [2.570, 2.571]e-4 (about 1/3890) |
| its sides | [7.076, 7.077]e-4, [7.208, 7.209]e-4, [7.682, 7.683]e-4 r |
| its inradius | [2.105, 2.106]e-4 r |
| mirror image | same area (difference certified 0 to the ball width) |
| white sliver (p, q, c), an even region | area [8.228, 8.229]e-7 r²; sides 7.077e-4, 2.565e-3, 2.934e-3 r; inradius 2.651e-4 r |
| four-sided A (ring 3) | area [0.01115, 0.01116] of a great triangle = 15.22 x smallest other triangle; short side q-c [2.934, 2.935]e-3 r; longest 0.1862 r |
| four-sided B (ring 4) | area [0.007417, 0.007418] of a great triangle = 10.13 x smallest other triangle; short side p-q [2.564, 2.565]e-3 r; longest 0.1505 r |
| smallest other triangle | area [8.999, 9.000]e-4 r² = [7.325, 7.326]e-4 of a great triangle |
| overshoot: signed distance of t5's corner c from t4's right leg | [-6.417, -6.416]e-4 r (= -0.000320824 D) |
| overshoot along t5's base, c-p | [7.076, 7.077]e-4 r |

Drawing scale (pen line 0.1 mm):

| radius | tiny triangle sides | inradius | area | overshoot | A short side | B short side |
|---|---|---|---|---|---|---|
| 10 cm | 70.8, 72.1, 76.8 µm | 21.1 µm | 2313 µm² | 64.2 µm | 293 µm | 256 µm |
| 1 m | 0.708, 0.721, 0.768 mm | 0.211 mm | 0.2313 mm² | 0.642 mm | 2.93 mm | 2.56 mm |

So at a radius of 10 cm the whole tiny triangle is narrower than the pen line and t4's leg passes the corner by less than the line's width: invisible. The triangle's inside first shows when its inradius exceeds half the line width, at a radius of about 24 cm (0.05 mm / 2.1056e-4 = 237 mm); at a radius of 1 m it is a speck with sides of about 0.7 mm. In #103 v5 these numbers are Table 6 and the paragraph after the list of deviations (§10.1).

Files: `scripts/s5_tiny_triangles.py`, `data/tiny-triangles.json`, `logs/s5_tiny.log`, `logs/s5-pilot.log` (pilot: the same script before the union-area check was made exact; same values).

Note for #103: Proposition 11 calls its smallest certified value 5.8e-8 "the doubled area of one of the two tiny triangles". The certified area itself is 5.782e-8 (doubled area 1.156e-7), so that phrase needs checking against certified_counts.py; it was not changed here.

## Credits (at point of use)

- **Problem and sources.** Kulaichev (1984) posed the problem. Pustynski (2014) gave the numerical solution and the remark on the extra triangles. Chiodo (2021) gave the form of Huet's conditions and the statement that uniqueness is open. Huet (2002) gave the conditions themselves. Rao (1998) is credited as in #103.
- **Software.**
  - Singular, through passagemath/Sage: resultants and factorisation.
  - PARI/GP, through cypari2: resultants, factorisation, polsturm, polrootsreal.
  - FLINT/Arb, through python-flint: complex root isolation and ball arithmetic.
  - mpmath: interval arithmetic (iv).
- **Methods.**
  - The Krawczyk test is due to R. Krawczyk (1969).
  - The root isolation method is the Vincent–Collins–Akritas method (Collins and Akritas 1976).
  - Sturm's theorem.

## Lean / Palomar assessment

- **Statement.** It is small: the 27 coordinates, 31 incidences as determinants, 4 conditions and 30-odd strict inequalities. The conclusion says the admissible set is a singleton, given by f348 and an isolating interval. That is about 150 lines of definitions.
- **Certificate, part by part:**
  - **(i) Divisor lemma and derivation.** These are field_simp, ring and positivity steps of moderate size. Feasible.
  - **(ii) The two resultant identities in S.** These are R = αG + βH1, with G quadratic and H1 cubic in S. The cofactors come from a 5×5 Sylvester matrix and have about 10³–10⁴ terms. This is at the edge for `linear_combination`.
  - **(iii) The identity E = αA + βB.** Here A and B have degree 20 in t, so the Sylvester matrix is 40×40, and E has degree 1744 with coefficients of hundreds of digits. The cofactors are far beyond `ring` or `decide` in the kernel.
  - **(iv) Descartes certificates for f348 and f396 on (0, 1).** These need Taylor shifts of degree about 400. They are plausible with a reflective checker on Nat/Int, which the kernel computes with GMP.
  - **(v) Back-solve and Krawczyk.** Dyadic-interval reflective checkers are feasible. About 200–400 bits suffice, given margins of 3·10⁻¹⁰ and more.
- **Bottleneck and how to remove it.** Part (iii) is the bottleneck. It can be removed by using route 2's eliminant as well: gcd(E, E2) = f348. Better, replace the Res_t identity by a subresultant or a verified polynomial-arithmetic checker, proved correct once and run by `decide` without native_decide.
- **Assessment.** This is a real project: a verified sparse-polynomial normaliser plus an interval evaluator. It is not a one-file proof. Everything except (iii) is within reach today.

## Files

- `scripts/s1_system.py`: the construction, the divisor lemma, the match with #103's system, and the full elimination. Writes data/system-K.txt, nz-factors.txt, R1-/R2-/E-factors.txt, candidates.txt and polys-K.json.
- `scripts/s2_isolate.py`: the three isolators. Writes data/roots-K.json, which holds the certified dyadic intervals.
- `scripts/s3_backsolve.py`: the census in Arb, Krawczyk, admissibility and the controls. Writes data/census-K.json.
- `scripts/s4_route2.py`: the independent census. Writes data/route2-*.txt.
- `scripts/run_census.sh`: runs steps 1–3 as one job.
- `logs/`: the job logs. Job yuniq-main ended FINAL ok (s1–s3), and job yuniq-route2 ran s4. The pilot logs are kept.
- `inputs/`: model.py and natural.py (#103), f348 (kulaichev-minpoly-u.txt), and the audit's stage1/4/5 outputs for case K.
