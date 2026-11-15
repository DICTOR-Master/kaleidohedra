**Verdict: UNIQUE (certified).** The DICTO Yantra has exactly one admissible solution under its own conditions: the one in #103 Theorem 9. The polynomial system has exactly four real solutions with u > 0, all on f160. The other three are not DICTO Yantras:
- u = 0.57120 passes every admissibility test of #103 Theorem 1. But the circle's centre lies outside the innermost triangle, at the centre of its excircle beyond the base (b5 > 1/2). So (d) fails, and the squared form of (d) cannot tell the two apart.
- u = 0.67176 and u = 0.88628 are not admissible: t4 turns over, b4 > b5, b6 > b7, and w5, w6 < 0.

Two censuses agree. They use different elimination orders (S then t, and t then S), different elimination methods (resultants, and evaluation with exact interpolation), different root isolators and different interval libraries (Arb and mpmath). Route 2 finds only f160 as a candidate.

# Uniqueness of the DICTO Yantra (study 2026-11-15)

DICTO, 15 Nov 2026: "yes start the DICTO Yantra uniqueness check". This applies the method of the Kulaichev census (studies/2026-11-15-yantra-uniqueness, the same day) to the DICTO Yantra of #103 (Theorem 9).

## Theorem (the DICTO Yantra is unique)

Take a circle of diameter 1 and nine isosceles triangles with a common vertical axis that meet Huet's conditions, in Chiodo's form (C. R. Math. 359, 2021, (i)–(iii)):
- the two great triangles are inscribed;
- seven apexes lie on bases;
- the 18 marmas and the 6 corner touches hold.

Add three of Kulaichev's four conditions (A. P. Kulaichev, *IJHS* 19.3, 1984):
- (b) the corners of the smallest top triangle lie on the circle;
- (c) the corners of the smallest bottom triangle lie on the circle;
- (d) the incircle of the innermost triangle (t1's legs and t5's base) is centred at the circle's centre.

In place of Kulaichev's (a), equal great triangles, take DICTO's Cleo-Antonius condition (#103 §9.1):
- the great slopes satisfy u·v = 2/φ³ = 2√5 − 4. Here u is the slope of the upper great triangle t7 and v that of the lower one, t3.

Admissibility is as in #103 Theorem 1: bases strictly ordered, half-widths positive, apexes on the correct side, corners in the closed disc. Then there is **exactly one** such figure, up to the normalisation (the scale, and the labelling with t1–t5 pointing down). It is the DICTO Yantra of #103 Theorem 9:
- u = 0.6793185887067746573886503103907545526887…, a root of the irreducible f160 (#103's data file, here inputs/f160-u.txt);
- v = (2√5 − 4)/u = 0.69501403737293…;
- t = 0.2144778165096741112408695537…, so b1 = t²/(1+t²) = 0.043977726104218…;
- S = b9 = 0.9682686074586943741422847787…;
- Q = b6 = 0.5765103217078404…, P = b3 = 0.3257114052811785…, R = b7 = 0.6842408243369539….

So its 43 triangles, 18 marmas and 24 sandhis (#103 Proposition 11, certified there) belong to the only figure that meets these conditions.

## Exact problem formulation

- **Frame and construction.** These are the Kulaichev census's (model.py and natural.py of #103, copied in inputs/), with the slope v left free.
  - u = w7/b7, so b7 = R = 1/(1+u²).
  - v = w3/(1−b3), so b3 = P = v²/(1+v²).
  - t = b1/w1, so condition (b) holds by construction.
  - S = b9.
  - Every other quantity is the meeting point of two lines (scripts/s1_system.py, line by line, each line naming its marma or touch).
- **Equations.** Every admissible figure satisfies:
  - G = 0, which is (c);
  - H1 = 0, the closing equation from the marma (1,4,6);
  - D = 0, which is (d) squared.
- **Field.** The Cleo-Antonius enters as v = c/u with c = 2√5 − 4. Since u > 0, powers of u may be cleared. All further work is exact over K = ℚ(√5), with s = √5.
  - The two conjugate choices of c are kept apart, so no norm is taken before the last step.
  - Only for root isolation is each kept factor over K replaced by its norm in ℚ[u] (the factor times its conjugate). That step can add roots but cannot lose any.
- **These are #103's polynomials.** After substitution, G, H1 and D equal the system of the #103 v3 certificate (audit stage 4, case D, inputs/stage4-D-system.txt). They agree up to constants and factors that are nonzero at any admissible figure.

## Proof structure

1. **Divisor lemma (exact, s1).**
   - The lemma is done over ℚ with u and v free, so it holds for every pair of great slopes, not only the Cleo-Antonius. The 14 step divisors are as in the Kulaichev census: differences of distinct base depths, sums of two positive slopes, and the marma (1,3,8) coefficient.
   - Singular proves by induction that each denominator factors into polynomials already known to be nonzero. That gives 26 such factors over ℚ.
   - After substituting v = c/u, each is factored over K. Its 23 distinct factors over K are nonzero wherever the original factor is.
   - Only these factors are dropped:
     - u t ± c, that is t = ±v (b1 = b3);
     - u t ± 1, that is b1 = b7;
     - u;
     - (1+u²)S − 1, that is b9 = b7.
2. **Full elimination over K (exact, no factor chosen numerically).**
   - R1 = Res_S(G, H1) = u¹⁰·A, with A of degree (20, 20) in (u, t).
   - R2 = Res_S(G, D) = u⁸·B, with B of degree (28, 20).
   - A and B have no common factor.
   - E = Res_t(A, B), computed in PARI with coefficients in ℚ[s]/(s² − 5), has degree 560. Its factorisation over K (PARI nffactor) is u⁴⁰⁰ · g80 · g80′.
   - The norms of the two degree-80 factors are f160 (Theorem 9) and one other irreducible polynomial of degree 160, called **h160** here.
   - Resultants lie in the ideal, so no solution is lost.
   - u is not confined to (0, 1) here: b3 < b7 only says uv < 1, which always holds. So the census covers the whole half-line u > 0.
3. **Root census (s2): 30 + 29 positive real roots.**
   - Each polynomial is bounded by an exact Cauchy bound, 2¹⁸⁰ and 2¹⁸², and isolated on f(2^k x) for x in (0, 1).
   - Three independent isolators agree:
     - Vincent–Collins–Akritas bisection (Descartes' rule; pure-Python integers);
     - PARI/GP polsturm (Sturm count 1 on each interval, 0 on each gap) and polrootsreal on [0, +∞);
     - FLINT/Arb complex root enclosures.
   - f160 has 30 positive roots (60 real roots, as #103 says), and h160 has 29.
   - Each root is held in a dyadic interval of width about 2⁻¹⁴⁰⁰, certified by exact signs at the endpoints.
4. **Back-solving (s3, Arb balls, 2400 bits, √5 as a ball).** For each of the 59 roots:
   - all 20 roots of A(t, u) are isolated, and those with 0 < t < v (from 0 < b1 < b3) are certified real;
   - that gives 177 roots (3 for each u). B is evaluated at each of them: 165 are rejected because B ≠ 0, with certified margins down to 3.0·10⁻⁷;
   - for the 12 that are left, S is taken from G with R < S < 1, then H1 and D are tested: 8 are rejected (H1 ≠ 0 or D ≠ 0, margins down to 7.3·10⁻⁵);
   - **4 true solutions** remain, all roots of f160. Each is certified by the Krawczyk test (exactly one solution in a box of radius 10⁻³⁰⁰), and each figure is rebuilt in balls:

| u | t | S | outcome (every inequality certified) |
|---|---|---|---|
| 0.571195314832 | 0.255076965509 | 0.977355225771 | Theorem 1 admissible, but b5 > 1/2: the centre is the excentre of the bindu triangle, not its incentre, so (d) fails |
| 0.671758400623 | 0.147508983833 | 0.968949150846 | not admissible: b4 > b5, b6 > b7, w5, w6 < 0, t4's apex on the wrong side, corners of t4 and t6 outside the disc (and b5 > 1/2) |
| **0.679318588707** | **0.214477816510** | **0.968268607459** | **admissible, every inequality strict: Theorem 9's root** |
| 0.886279995316 | 0.111804846754 | 0.947165909639 | not admissible: as for u = 0.67176 (b5 < 1/2 holds) |

   - h160 carries no real solution. Like f396 in the Kulaichev census, it is an artefact of the elimination order.
   - Every (u, t, S) fixes the whole figure, because the construction is forced. Hence there is exactly one DICTO Yantra.
5. **Independent census (s4, second compute machine; job dyuniq-route2 FINAL ok).**
   - **Elimination order: t first, then S.** Direct Res_t(H1, D) over K[u, S] did not finish within the 5-minute pilot in any of four systems: Singular over K, Singular over ℚ[s], PARI with polmod coefficients, and FLINT. So the eliminant is built from values instead.
   - **Values at 869 integers u0 = 1 … 869 (735 s).** For each u0:
     - R3(u0, S) = Res_t(H1(u0), D(u0)) in K[S];
     - E2(u0) = Res_S(R3(u0, S), G(u0, S)) in K.
     - A value is used only when every degree keeps its generic value: t-degrees 10 and 10, S-degree 2 for G, S-degree 50 for R3. No point had to be skipped.
   - **Degree bound.** The Sylvester bounds give deg_u R3 ≤ 10·15 + 10·18 = 330, so deg_u E2 ≤ 2·330 + 50·4 = 860.
   - **Interpolation (PARI polinterpolate, exact, 463 s).** 861 points fix E2, and the 8 extra points agree.
   - **Result.** E2 has degree 460 = u³⁸⁰ · g80 over K, and the norm of g80 is **f160**. It is the only candidate: h160 does not appear in this order.
   - **Root census.** PARI Sturm bisection on [0, 2¹⁸⁰] finds 30 positive roots.
   - **Back-solving in mpmath interval arithmetic:**
     - S by the quadratic formula;
     - t by a 1-D branch and bound with interval Newton on H1 over (0, v);
     - then D, Krawczyk and the admissibility rebuild.
   - **Same result:** 0 undecided. The same four real solutions are found, and only Theorem 9's is admissible. The excentre figure (u = 0.57120) and the two inverted figures are found again.

**Controls.**
- Positive: Theorem 9's root passes every step. Its 40-digit isolating interval (audit stage 1) holds exactly one root of f160.
- Negative:
  - B + 1 at the true u is rejected;
  - u + 2⁻²⁰⁰ is rejected;
  - f160 + a0/10¹⁰, with a0 the constant term, has no root in Theorem 9's interval. Adding 1 would be too small to move a root out of the interval, since f160's coefficients have about 200 digits.
- **Near miss caught.** This is the undistorted Cleo-Antonius: u = 2/φ² = 3 − √5 exactly, v = 1/φ, the Cleo-Icos cone above and the Antonius side below (#103 §9.1 with β = 0). It meets Huet's conditions, (b) and (c). A(t, 3 − √5) has three real roots in (0, v), and B rejects all three.
  - Two of them lie on the closing curve: t = 0.1907, which is Theorem 1 admissible, and t = 0.1297, which is not.
  - At the admissible one, the bindu's incircle centre is 0.058 of the diameter above the circle's centre.
  - The excentre solution at u = 0.57120 is a second near miss that the census catches: it meets every equation and every shape condition, and fails only the side of the centre.

## Credits (at point of use)

- **Problem and sources.**
  - Huet (2002) gave the conditions. Chiodo (*C. R. Math.* 359, 2021) gave their form (i)–(iii) and the statement that the uniqueness question is open for Kulaichev's yantra.
  - Kulaichev (1984) gave conditions (b), (c) and (d), and condition (a), which is replaced here.
  - DICTO gave the Cleo-Antonius condition u·v = 2/φ³ and the DICTO Yantra (#103, #44 for the Cleo-Icos and Antonius).
- **Software.**
  - Singular, through passagemath/Sage: resultants and factorisation over ℚ and over ℚ(√5).
  - PARI/GP, through cypari2: resultants with polmod coefficients, nffactor, norms, polsturm, polrootsreal and polinterpolate.
  - FLINT/Arb, through python-flint: root enclosures and ball arithmetic.
  - mpmath: interval arithmetic (iv).
- **Methods.**
  - Krawczyk test: R. Krawczyk (1969).
  - Vincent–Collins–Akritas root isolation: Collins and Akritas (1976).
  - Sturm's theorem and Cauchy's root bound.
  - Lagrange interpolation, used with the Sylvester degree bounds.
- **Pipeline.** The pipeline is the Kulaichev census's, adapted here: scripts s1–s4 of studies/2026-11-15-yantra-uniqueness.

## For #103 v5 (note only; #103 is not edited here)

Possible addition next to Theorem 9: "**Theorem (uniqueness).** Under Huet's conditions, Kulaichev's (b), (c), (d), u·v = 2/φ³ and the admissibility of Theorem 1, the DICTO Yantra is the only solution."
- Proof: as above, by a certified computation over ℚ(√5) with two independent censuses.
- Worth one sentence: the excentre figure at u = 0.57120 is the only other real solution in admissible shape. Condition (d) must be read as incircle, not as "equidistant from the three sides".
- Ledger entry: concordance.json, 2026-11-15, "Uniqueness of the DICTO Yantra".

## Files

- `scripts/s1_system.py`: the construction, the divisor lemma (generic u, v), the substitution v = c/u over ℚ(√5), the match with #103's system, and the full elimination. Writes data/system-D.txt, nz-factors.txt, R1-/R2-/E-factors.txt, candidates.txt and polys-D.json.
- `scripts/s2_isolate.py`: the three isolators on u > 0. Writes data/roots-D.json.
- `scripts/s3_backsolve.py`: the census in Arb, Krawczyk, admissibility and the controls. Writes data/census-D.json.
- `scripts/s4_route2.py`: the independent census by evaluation and interpolation. Writes data/route2-E2.txt (E2 in full), route2-E2-factors.txt and route2-candidates.txt.
- `scripts/run_census.sh`: runs steps 1–3 as one job.
- `logs/`: the pilot logs (s1–s4); s1_system.log, s2_isolate.log and s3_backsolve.log from job dyuniq-main (FINAL ok); job-dyuniq-main.log; job-dyuniq-route2.log (the full s4 output, job dyuniq-route2, FINAL ok).
- `inputs/`: model.py, natural.py and golden_family.json (#103); f160 (#103's dicto-yantra-exact-u.txt); the audit's stage1/4/5 outputs for case D.
