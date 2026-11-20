**Verdict: no selection theorem.** Nothing proved here singles out the Cleo-Antonius condition (uv = 2/φ³) among the fourth conditions of #103 Table 3. Every condition of the form uv = c gives the traditional form (43 triangles, 18 marmas, 24 sandhis) for a whole interval of c, c_lo < c < c*, and 2/φ³ = 0.4721 is an ordinary point inside it. So candidates (a), (b) and (d) are refuted, and (c) is a fact about solids, not about yantras. **What the study does give** is a new rule for #103: for every yantra with (b) and (c), the traditional form holds exactly when c_lo < uv < c*. Both ends are roots of one irreducible polynomial of degree 90, and at each end the same three lines meet. This answers the open question of #103 §9.5 for yantras with (b) and (c). It does not lift the Palomar finding.

# Does a theorem single out the Cleo-Antonius? (study 2026-11-20)

DICTO approved this study on 20 Nov 2026. It looks for a theorem that singles out the Cleo-Antonius fourth condition, uv = 2/φ³, among the fourth conditions of #103 Table 3. The reason is that the blind Palomar scorers found Theorem 15's interest "not established independently" of Kulaichev's theorems (studies 2026-11-20-yantra-v2-rescore and 2026-11-20-yantra-thm15-scope). #103 and the Palomar entry were not touched.

## 1. Main result: the traditional form holds on an interval of uv

**Proposition (the traditional window).** Take a yantra in #103's model that meets Huet's conditions in Chiodo's form, Kulaichev's (b) and (c), and admissibility as in #103 Theorem 1. Let u and v be the slopes of the great triangles t7 and t3, and let c = uv.
1. **Counts depend only on c.** The yantra's counts depend only on c (by #103 Theorem 5). For each c in (0, 0.7612…) there is exactly one admissible yantra up to the viewpoint.
2. **The window.** The yantra has the traditional form exactly when c_lo < c < c*, where
   - c_lo = 0.34619829022988503693375455799016663032631948136950…
   - c* = 0.55651083349095950353163985290887285823415889856098…

   Here the traditional form means 43 odd regions (14, 10, 10, 8, 1), all triangles, 18 marmas, 24 sandhis and 74 regions in all.
3. **Outside the window.** For c just outside the window the yantra has 45 odd regions (41 triangles), 18 marmas, 28 sandhis and 78 regions in all.
4. **What happens at the ends.** At both ends, t4's right leg passes through t5's corner, where t5's base and t6's right leg already meet (the corner touch (5,5,6)). These are the three lines of #103 Proposition 13 and Figure 12. Going up through c*, t4's leg crosses the corner outwards. Going down through c_lo, it crosses back.
5. **Exact form of the ends.** c_lo and c* are the roots of one irreducible integer polynomial g90 of degree 90 (data/g90-c.txt), in the rational isolating intervals
   - [3461982902298850369337545579901666303262, …265]·10⁻⁴⁰
   - [5565108334909595035316398529088728582340, …343]·10⁻⁴⁰

   g90 is monic, and its constant term is −96.
6. **Link to #103 Proposition 13.** g90(c) = f180(√c), where f180 is the polynomial of #103 Proposition 13, so c* = u*². The lower end c_lo is a second root of the same polynomial; #103 does not know this end.
7. **Adding (d).** With (d) added, every c in the window gives exactly one Śrī Yantra meeting all of Huet's conditions, (b), (c) and (d), with the traditional form. This uses #103 Theorem 5: exactly one viewpoint centres the bindu.

**What is certified, and what is computed:**

| Part | Status | How |
|---|---|---|
| 5 and 6 (the ends are roots of g90 in the stated intervals, and the three lines meet there) | certified | Exact elimination (s4). The Krawczyk test shows that G = H1 = C = 0 has exactly one solution in a box of radius 2⁻³⁰⁰ around each end. Every other factor of the resultant is shown to be nonzero on that box by ball arithmetic. f180 has exactly one root in each u-interval (PARI polsturm). f180 and g90 are irreducible (PARI). |
| 1 (counts depend only on c) | proved in #103 (Theorem 5) | Checked here at 12 random (u, v) (s1). |
| 1 (one yantra per c), 2, 3, 7 | computed at 60 digits, not certified | See below. |

How the computed parts were found:
- The members were scanned at 2000 and at 400 values of c.
- All 2925 triples of the 27 lines and all 351 pairs were checked at 300 and at 1500 values of c. The same 202 sign changes appear at both densities. Only 3 of them have their meeting point on all three drawn sides.
- The (d) curve was scanned at 189 values of c.

How this sits beside #103:
- **It replaces an observation.** #103 §10.1 has the observation "the two great slopes add up to about 1.49 or more". The rule is in the product, not in the sum. On the rhombus, 2√c* = 1.49199…, which is where the 1.49 came from.
- **It predicts a lower end.** None of #103's yantras goes below the lower end: the smallest product in Table 3 is the DICTO Yantra's, 0.472.
- **It explains Kulaichev's yantra.** Kulaichev's equal great triangles with (d) land at c = 0.56316, just above c* = 0.55651. That is why Kulaichev's yantra has the two extra triangles (Theorem 14, Proposition 11).

Other events along c, for the record (computed):
- At c = 0.16187611565517789114… the left and right legs of t4 and t5 meet t9's leg on t6's base. Below it, 42 of the 45 odd regions are triangles; above it, 41.
- Another change happens below c = 0.0015. The 2000-point scan sees 40 triangles at c ≤ 0.001.
- No admissible (b), (c) yantra exists above c ≈ 0.7612.

## 2. The candidates, one by one

**(a) "Only uv = 2/φ³ gives the traditional form, among c in a natural family": refuted.**
The traditional form holds on the whole open interval (c_lo, c*). So it holds for infinitely many c in ℚ(√5) and for rational c. Below, every product of two slopes from the solids used in #103 Table 3 is shown with its yantra. Each yantra meets (b), (c) and (d) with uv equal to the product (s3, 50 digits).

| Product of slopes | c | u, v of the yantra with (d) | Form |
|---|---|---|---|
| Antonius × Antonius (golden rhombus) | 1/φ² = 0.38197 | 0.59776, 0.63900 | 43 / 18 / 24 |
| Antonius × stella | 0.43702 | 0.64878, 0.67360 | 43 / 18 / 24 |
| Antonius × 3/4 | 0.46353 | 0.67199, 0.68978 | 43 / 18 / 24 |
| **Cleo-Icos × Antonius (Cleo-Antonius)** | **2/φ³ = 0.47214** | **0.67932, 0.69501 (DICTO Yantra)** | **43 / 18 / 24** |
| stella × stella; Antonius × φ/2 | 1/2 | 0.70232, 0.71192 | 43 / 18 / 24 |
| stella × 3/4 | 0.53033 | 0.72611, 0.73037 | 43 / 18 / 24 |
| Cleo-Icos × stella (Cleo-Octangula, V1) | 0.54018 | 0.73356, 0.73638 | 43 / 18 / 24 |
| 3/4 × 3/4 | 0.5625 | 0.74996, 0.75004 | 45 / 18 / 28 |
| stella × φ/2, Cleo × 3/4, Cleo × Cleo, φ/2 × 3/4, Cleo × φ/2, φ/2 × φ/2 | 0.572 to 0.655 | | 45 / 18 / 28 |

In the Form column, 43 / 18 / 24 means 43 regions (all triangles), 18 marmas and 24 sandhis; 45 / 18 / 28 means 45 regions (41 triangles), 18 marmas and 28 sandhis.

Eight products of two slopes fall in the window (seven values of c), and four of them lie in ℚ(√5):
- 1/φ², the Antonius side above and below;
- 3/(4φ), the Antonius side with 3/4;
- 1/2, the Antonius side with φ/2 (1/2 is also the stella pair);
- 2/φ³, the Cleo-Antonius.

Two of them are simpler than 2/φ³ by any height measure: 1/2 is rational, and 1/φ² is a unit. So no "only one in the family" statement holds for the field ℚ(√5), for products of slopes of pieces, or for small height.

**(b) "Exact ends, and is 2/φ³ special inside?": the ends are proved; 2/φ³ is not special.**
- The ends are c_lo and c* of §1, exact and certified.
- 2/φ³ is not a root of g90: g90(2/φ³) = −0.0570 ≠ 0. Since 2/φ³ has degree 2 and g90 is irreducible of degree 90, it cannot be.
- 2/φ³ is neither the midpoint of the window (0.4514) nor its geometric mean (0.4389). It sits 60 % of the way from c_lo to c*.
- The other roots of g90 in (0, 1) are not events of the admissible yantra: there the three lines miss by 0.0019 to 0.0038, or no yantra exists (t1_tangency.py).

**(c) "Only Cleo + Antonius come from one solid split": not a theorem about the yantra.**
"Cleo + Antonius + Cleo = golden rhombohedron" is a true fact about the two solids (#103 §9.1). A selection theorem would need a precise class of "splits" and a search of every solid in it. The yantra plays no part in such a statement. The window also holds other pairs that come from one figure:
- the two tetrahedra of the stella octangula (c = 1/2);
- the Antonius side twice (c = 1/φ²).

A definition of "split" that kept the Cleo-Antonius and excluded these would be a forced construction. **Not attempted, and not recommended.**

**(d) "The Cleo-Antonius yantra is extremal among the traditional yantras": refuted for the quantities tested.**
Along the curve of yantras that meet (b), (c) and (d) in the window (s3; values at the DICTO Yantra agree with #103: k = 0.0549838, spread/mean 0.866):
- **Nesting ratio k** (#103 §9.4, incircle radius over circle radius): its maximum is inside the window, at c ≈ 0.5348 (k = 0.0575234), not at 2/φ³ (0.0549838).
- **Spread/mean of the 43 areas** (#103 §9.6): it falls across the whole window, so its least value is at the upper end c*, not inside.
- **Smallest over largest of the 43 areas:** its maximum is at c ≈ 0.528 (0.01408), against 0.01132 at 2/φ³.
- **Smallest gap to any change of the arrangement** (least |det| over the triples that are not identities): no clean extremum, and nothing at 2/φ³.

These maxima are located on a grid only, to about 2·10⁻⁴ in c. None of them is near 2/φ³.

## 3. What this means for #103 v7 and for Palomar Version 2

**For #103 v7.** The traditional window is worth adding, for example as a proposition after Proposition 13 or in §10.1:
- It replaces the "about 1.49" observation with a rule.
- It shows that Kulaichev's yantra falls just outside the window.
- It places the DICTO Yantra inside, as the point c = 2/φ³ of a one-parameter arc of traditional yantras that meet every condition.

The certified part is the exact ends. The interior counts are computed, the same status as Proposition 13. It also makes §10.1's sentence "the family cannot single out 'the' yantra by itself" exact: the traditional form singles out an interval, not a point.

**For Palomar Version 2.** No result here meets the build rule. The scorers' finding was that Theorem 15's interest is not independent of Kulaichev's. The window theorem confirms that the choice of c inside the window is free. Theorem 15 is the uniqueness at one value of that free choice. Presenting the window would answer "why this condition?" with "any c in (c_lo, c*) gives a traditional yantra; DICTO chose the Cleo-Antonius". That is honest, but it is a reason from the pieces, not a theorem. **The verdict of study 2026-11-20-yantra-v2-rescore stands: do not build Version 2 on Theorem 15 alone.**

A separate possibility, outside the plan: the window theorem with its two certified ends, once its interior is certified too (LEADS 1), stands on its own. It is about every (b), (c) yantra, not about Kulaichev's conditions. It could be scored as its own statement. It should not be presented as a selection of the Cleo-Antonius.

## 4. Method

All work ran on the compute host. Nothing was computed on the interface machine.
- **s0_generic.py (Sage/Singular over ℚ).** The construction of #103 Theorem 15's census (studies/2026-11-15-dicto-yantra-uniqueness, s1_system.py), copied line by line with both slopes free. The divisor lemma closes for generic u and v: 26 nonzero factors. G, H1 and D are stripped as there. The crossing C = det(t4 right leg, t5 base, t6 right leg) is added. Output: data/system-uv.json.
- **yfam.py.** The numeric model (mpmath):
  - the same construction;
  - all admissible members for given (u, v): S from G (quadratic), t from H1 (degree 10 in t), all real roots;
  - admissibility as in Theorem 1;
  - the 27 lines and their triple determinants;
  - counts by #103's counts.py rule (marmas and sandhis);
  - regions by yarr.py (study 2026-11-17-yantra-sequence, copied). One change to the copy: it also returns the odd regions' areas.
- **s1_scan.py.** The counts of the rhombus member u = v = √c along c, plus the check of Theorem 5's reduction at 12 random (u, v).
- **s2_events.py.** Every sign change of a line triple (full lines) along c. It keeps those whose meeting point lies on all three drawn sides, solves each to 55 digits, and takes the counts 10⁻⁸ below and above.
- **s3_dcurve.py.** The (d) member for each c (root of the bindu offset in u). The named products of slopes. k, spread/mean and smallest/largest area, with their extrema located on a fine grid.
- **s4_endpoints.py.** The exact ends:
  1. elimination with v = u: Res_S, then Res_t (PARI), degree 1928, which equals threshold_exact.py's degree in study 2026-11-10-g1-e1-exact;
  2. Krawczyk boxes in Arb at 1200 bits;
  3. the factor through each end, shown to be #103's f180;
  4. g90, its irreducibility and the isolating intervals.
- **t1_tangency.py.** The other roots of g90 in (0, 1) are not events.

## 5. Checks (every job ended FINAL ok; logs in logs/)

- **s0.** Divisor lemma closes (generic u, v). G, H1 and D have the expected degrees: H1 has degree 10 in t, as in #103 Theorem 6.
- **Smoke test (t0).** The four reference yantras below reproduce #103's counts. At each of them exactly one admissible member is found.
  - DICTO Yantra: 43 (all triangles), 18 marmas, 24 sandhis, (d) residual 3·10⁻⁴¹.
  - Kulaichev's yantra: 45, 41 triangles, 18, 28.
  - Stella rhombus: 43, 18, 24.
  - Rhombus at 2/φ³: 43, 18, 24.
- **s1.** The reduction check passes: at 12 random (u, v), the number of members and every count equal those of the rhombus member with the same product. The 400-point and 2000-point scans agree on every run boundary.
- **s2.** 300 and 1500 scan points give the same 202 sign changes and the same 3 events on the drawn sides. The upper end agrees with #103 Proposition 13's u* (0.74599653718429518158…) to all its digits.
- **s3.** Exactly one (d) member at every grid c < 0.7. These values agree with #103:
  - k at the DICTO Yantra (0.0549838) and V1 (0.0575055);
  - spread/mean at the DICTO Yantra (0.866);
  - V1's u and v (0.73356, 0.73638).
- **s4.**
  - Both Krawczyk tests pass.
  - At each end, the only factor of E that can vanish is f180, identical to #103's file (inputs/threshold-minpoly-u.txt).
  - polsturm gives exactly 1 root in each interval, for f180 in u and for g90 in c.
  - f180 and g90 are irreducible.

## LEADS

1. **Certify the interior of the window.** Do a one-dimensional certified sweep over c ∈ [c_lo, c*] in Arb:
   - enclose the member over each c-interval (S from the quadratic G, t by interval Newton on H1);
   - enclose all 2925 triple determinants;
   - show that each one has a fixed sign, or cannot meet on the drawn sides;
   - certify the counts at one point (the DICTO Yantra's count is already certified, #103 Proposition 11).

   The 2-D tool threshold_cert.py (study 2026-11-10-g1-e1-exact) has the right structure. The 1-D version is smaller. This would make §1's parts 1 to 3 and 7 a certified theorem.
2. **Uniqueness of the (d) member for every c in the window.** The census of Theorem 15, with c as a parameter, would make §1 part 7 a theorem. Today it is proved only at 2/φ³ (Theorem 15) and computed elsewhere.
3. **#103 v7 wording.** A proposition for the window, and the "about 1.49" observation replaced by the product rule. DICTO decides where it goes.
4. **The event at c = 0.1619** (42 → 41 triangles below the window) and the one below 0.0015 can go in the same proposition as a remark, or be left out (Occam).

FINAL ok
