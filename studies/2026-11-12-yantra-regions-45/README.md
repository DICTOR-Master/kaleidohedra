# Aim 2, chunk 5c leads (a) and (b): the 45-region yantras, and the zero curve of the DICTO Yantra (12 Nov 2026)

**Conclusion.** Kulaichev's yantra and Rh345 (45 regions) have 41 triangles and 4 four-sided regions, all faces convex, the same double zeros at the 18 marmas and residue 2 at all 28 sandhis, but a positive centre value; from 43 to 45 the degree (24), the residues and the 511-term signed sum are unchanged (exact through Q3). The DICTO Yantra's zero curve N = 0 is irreducible of genus 207: its only singular points are the 18 marmas (isolated real points) and an ordinary 8-fold point at infinity where the 9 bases meet; numerically 10 real components (exact for R1, high precision for the DICTO Yantra). E1 (43 triangles, 18 double zeros, 22 sandhis of residue 2, two 4-line points, centre +343) shows "most even" not in the residues but in the forms: least form value = 27/(2 area) for every triangle, so E1 has the most equal least form values.

Scripts: `scripts/yantra_regions45.py` (lead a; log `data/yantra-regions45.log`), `scripts/zero_curve.py` (lead b; log `data/zero-curve.log`).
Both reuse the functions of chunk 5c (`studies/2026-11-12-yantra-regions-canonical/scripts/yantra_regions.py`, commit 2366ec88) unchanged.

## Lead (a): the 45-region yantras

**Question.** Chunk 5c found for the 43-region DICTO Yantra: every region a triangle, every face convex, N (numerator of the whole-yantra form
over the 27 sides) of degree 24, an order-2 zero of N at each of the 18 marmas (no point residue), residue 2 at each of the 24 sandhis,
Ω_Y = −86.08 < 0 at the centre. Kulaichev's yantra and Rh345 have 45 regions. Same questions for them:
1. Are all regions triangles, and are all faces convex? (Which regions are four-sided?)
2. Do the marmas again carry a double zero, and what residues sit at the sandhis?
3. Is the form at the centre again negative?
4. What changes between 43 and 45 regions: the form's degree, its residues, its signed-sum structure?

**Yantras (data from the sri-yantra study, 8–10 Nov).**
- *Kulaichev's yantra* (Kulaichev 1984; Rao 1998; Pustynski 2014): u = v is a root of an irreducible integer polynomial of degree 348
  (`figures/kulaichev-minpoly-u.txt`). Rebuilt here: u isolated EXACTLY by a sign change of that polynomial on an interval of width 10⁻²⁸⁰
  (10⁻⁵⁸⁰); Q, S by Newton from the two corner conditions (t1, t9 corners on the circle); Kulaichev's fourth condition (bindu centred),
  never imposed, then holds to 8.5·10⁻²⁹² (5.2·10⁻⁵⁹¹); the stored 60 digits agree to 4.6·10⁻⁶¹.
- *Rh345* (DICTO's 3-4-5 rhombus, u = v = 3/4, field of degree 20): Q, S by Newton; S agrees with the exact (21464 + 56√56869)/37825 to
  8.5·10⁻³⁰²; Q = b6 and b1 isolated EXACTLY by sign changes of their degree-20 minimal polynomials (`data/rhombus345-exact-data.txt`);
  the bindu misses the centre by 2.36·10⁻⁵, as recorded.
- *Q3*, the exact 45-region instance (the role R1 plays for 43): u = v = 3/4, Q = 11/20, S = 11/12, every coordinate in ℚ(√Δ)
  (`data/quadratic-examples.json`). Computed here in EXACT arithmetic of ℚ(√Δ) (numbers a + b√Δ with rational a, b; signs decided exactly
  by comparing a² with b²Δ), the grid lemma proving every polynomial identity as for R1.

**Method.** Exactly chunk 5c's: arrangement of the 27 sides, faces by half-edge walk, containment count c, regions = faces with c odd;
forms by the vertex formula, by fan triangulation and as 2 × polar area; the whole-yantra form Ω_Y = sum of the regions, its numerator N
by interpolation on the 26 × 26 grid; at every crossing of side lines the order k of N and the point residue. Kulaichev and Rh345 at 300 and
600 digits; Q3 and R1 exact. "Ring" below is the count c of triangles covering a region (c = 1, 3, 5, 7, 9: the fourteen, the outer ten,
the inner ten, the eight, the innermost triangle).

**Controls.** Positive: the sector lemmas and plain cases of 5c (rerun); the known counts (45 for Kulaichev, Rh345, Q3; 43 for the rhombus
yantra just below the threshold slope u* = 0.745996…, where the two tiny regions are born, sri-yantra study 10 Nov); the faces in each of the
nine triangles sum to its form; vertex = fan (for the four-sided regions also with the other diagonal). Negative: one region's sign flipped
breaks the valuation identity; a flipped normal breaks vertex = fan; a wall moved 1/1000 leaves a pole (exponent 1.000 against 0.000).
All held (`data/yantra-regions45.log`, FINAL ok).

**Results.**

1. **Regions.** All three 45-region yantras (Kulaichev, Rh345, Q3, and the rhombus yantra just above u*) have one and the same crossing
   pattern: 78 faces, all **convex**; 45 regions by ring 14, 10, **12**, 8, 1: **41 triangles and 4 four-sided regions**; 33 even faces
   (12 triangles, 21 four-sided). The four-sided regions are two mirror pairs:
   - in the inner ten-ring (c = 5, covered by t2, t3, t6, t7, t8): sides on t4's leg, t5's leg, t6's leg, t6's base;
   - in the eight-ring (c = 7, covered by t2–t8): sides on t4's leg, t5's base, t5's leg, t9's leg.
   The two extra regions are the two tiny **triangles** of the inner ten-ring (sides on t4's leg, t5's base, t6's leg; area 5.8·10⁻⁸ for
   Kulaichev, 4.7·10⁻⁸ for Rh345, 2.6·10⁻⁶ for Q3). Going from 43 to 45, on each side: t4's leg cuts a corner off one region of the eight
   (triangle → four-sided) and off one region of the inner ten (triangle → four-sided), and the tiny triangle is new; among the even faces
   one triangle is new, one four-sided face becomes a triangle and one triangle becomes four-sided. Each region is still a positive
   geometry (convex polygon; vertex = fan = 2 × polar area); no two regions share a wall (parity lemma, 0 exceptions).
2. **Points.** Point table for the drawn sides (identical for Q3 exact, Kulaichev and Rh345 at both precisions):

   | point | 43 (DICTO Yantra, R1) | 45 (Kulaichev, Rh345, Q3) | m | k | point residue |
   |---|---|---|---|---|---|
   | marma | 18 | 18 | 3 | **2** | none |
   | sandhi | 24 | **28** | 2 | 0 | **2** (all) |
   | triangle corner (free) | 14 | 14 | 2 | 0 | 1 |
   | tip on a base | 7 | 7 | 3 | 1 | |
   | corner touch | 6 | 6 | 3 | 1 | |
   | crossing of extended lines off the drawn sides | 162 (R1) | 156 | 2 | 1 | 0 |

   The marmas again carry the double zero of N (order exactly 2, no point residue); every sandhi again carries residue 2, the four new
   ones (two on each side) included. The only change in the point table on the drawn sides is 24 → 28 sandhis.
3. **Centre.** Ω_Y at the circle centre (0, 1/2), inside the bindu region, is **positive** for all 45-region yantras: Kulaichev +27.45,
   Rh345 +26.17, Q3 +83.37 (exact value in ℚ(√Δ)). It is also positive for the 43-region rhombus yantra just below u* (+14.64) and for R1
   (+1649.8). The DICTO Yantra's −86.08 is so far the only negative centre: the sign at the centre is not fixed by the crossing pattern;
   it depends on where the lines sit.
4. **43 against 45.** Unchanged: N has degree 24 and is even in x (mirror symmetry); all 27 sides are pole lines; all 511 intersections
   of the nine triangles are nonempty (9, 36, 84, 126, 126, 84, 36, 9, 1), so the signed-sum structure
   Ω_Y = Σ_{I≠∅} (−2)^{|I|−1} Ω(∩_{i∈I} T_i) is the same formula with the same 511 terms; the residues are the same values (marmas 0,
   sandhis 2, free corners 1, off-figure crossings 0). Changed: 2 more regions (45 = 41 triangles + 4 four-sided against 43 triangles),
   2 more even faces, 4 more sandhis, and the sign of Ω_Y at the centre against the DICTO Yantra. So the whole 45-region yantra is again a
   signed sum of 45 positive geometries and not a positive geometry itself (residue 2 at all 28 sandhis).

**Precision, stated plainly.** Exact: Q3 (ℚ(√Δ)), R1 (ℚ), the lemmas, the isolation of u (Kulaichev), Q and b1 (Rh345). Kulaichev and Rh345
themselves: high precision only (300 and 600 digits; values agree to 2.6·10⁻²⁸⁸, residues to 5.3·10⁻²⁷⁸); their structure is proved
through Q3, which has the same crossing pattern and point table (checked).

## Lead (b): the zero curve N = 0 of the DICTO Yantra (degree 24)

**Question.** Ω_Y = N / (product of the 27 side lines). What is the curve N = 0: its genus, its real components, and does it pass
through the marmas (and through the bindu centre or along the circle)?

**Method (`scripts/zero_curve.py`).** N is even in x (mirror symmetry), N(x, y) = M(x², y). Singular points: off the axis they are the
common zeros of M, M_s, M_y; on the axis x = 0 the double roots of N(0, y); at infinity, the repeated factors of the top form.
- *R1 (same crossing pattern as the DICTO Yantra), EXACT:* PARI resultants Res_y(M, M_y) (degree 248) and Res_y(M_s, M_y) (degree 225),
  their gcd over ℚ (degree 9, nine linear factors), and at each root the gcd in y; N(0, y) squarefree by an exact gcd; the tangent cone at
  infinity squarefree by an exact gcd.
- *DICTO Yantra, high precision only (300 and 600 digits):* starting points from the exact resultants of M rounded to 60 digits (3043
  candidates), each refined by Newton on (M_s, M_y) = 0 with M itself at full precision; a point counts as singular only if M, M_s, M_y
  all vanish below 10⁻ᵈⁱᵍⁱᵗˢ/³ of their scale. Positive control: R1 sent through this same numerical route gives exactly the exact answer.
- *Real picture (numerical, 120 digits, not certified):* real branches over the critical x values (real roots of Res_y(M, M_y), refined),
  joined through each critical point, through the simple points at infinity (same asymptotic direction at both ends) and through the
  point (1:0:0) (all horizontal asymptotes); no count mismatch between neighbouring critical values (0 of 62).
- *Circle:* N on x² + y² = y through x = t/(1 + t²), y = t²/(1 + t²), a polynomial of degree 48 in t, real roots counted.

**Results.**
1. **Singular points.** Exactly the 18 marmas (each an ordinary double point; the tangent cone is definite, so each marma is an
   **isolated real point** of the curve: two complex-conjugate branches cross there, no real branch) and one point at infinity,
   (1:0:0), the direction in which the 9 parallel bases meet. There N = 0 has an **ordinary 8-fold point**: 9 lines meet in one point
   and the alternate sectors cancel, the 5c marma lemma (k lines, order k − 1) at infinity. Its 8 tangents are real horizontal lines,
   the curve's 8 horizontal asymptotes. Nothing else, real or complex, affine or at infinity (16 further simple points at infinity, all
   real for the DICTO Yantra, 12 real for R1). No singular point on the axis.
2. **Irreducible, genus 207.** Two components of degrees a + b = 24 would meet in ab points, all singular: at most 18 from the nodes and
   at most m_A·m_B ≤ 16 from (1:0:0), so ab ≤ 34, which leaves only a line; a slanted line would need 23 nodes, a horizontal one gets at most
   2 marmas (mirror pairs) + 7 = 9 < 23. So N = 0 is irreducible over ℂ and its genus is (23·22)/2 − 18 − 28 = 253 − 18 − 28 = **207**.
   Exact for R1; for the DICTO Yantra high precision only (300 = 600 digits), same answer.
3. **Real components (numerical).** DICTO Yantra: in the plane 31 real pieces, 7 closed ovals and 24 running to infinity; in the
   projective plane **10 real one-dimensional components** (the 16 horizontal ends all meet at (1:0:0)), plus the 18 marmas as isolated real
   points. R1: 27 pieces, 7 ovals, 11 projective components. Far below Harnack's bound (208).
4. **Marmas, bindu, circle.** The curve passes through every marma, but only as an isolated real point: the real curve never runs
   through a marma. It passes through the 7 tips on bases, the 6 corner touches and every crossing of extended lines off the figure
   (order 1, 5c table), and not through the sandhis or free corners. It misses the bindu centre (N(0, 1/2) ≠ 0) and meets the circle in
   26 real points, all simple (degree 48 in the circle parameter), the same number for R1.

## DICTO's extra case: E1, the most even exact yantra (#103 §10/§12; `scripts/e1_regions.py`, log `data/e1-regions.log`, FINAL ok)

**Question (DICTO).** E1 keeps the traditional 43 regions but leaves the circle (t1, t9 corners inside). Same analysis: region types,
marma double zeros, sandhi residues, centre value; compared with the DICTO Yantra and Kulaichev's yantra: does "most even" show in the formula?

**Data and precision, stated plainly.** E1 has no exact form (studies/2026-11-10-g1-e1-exact: it is fixed by one incidence, t4's right
leg through t5's corner, and three stationarity equations of the area spread; open). Used here: u, v, Q from its 90-digit refinement, S
re-solved at 300 and at 600 digits so that the incidence holds to working precision (to 3·10⁻³⁰³ and exactly 0 at 600 digits); all Huet
conditions to 10⁻³⁰¹. So the yantra analysed lies exactly on E1's edge and agrees with E1 to the refinement's accuracy; the results are
high precision only (300 and 600 digits agree to 9·10⁻²⁹⁹, same faces and point table). There is no exact instance like R1 or Q3 for
E1's pattern. Controls: the DICTO Yantra recomputed gives 5c's answer (43 triangles, 18 order-2 marmas, 24 sandhis, −86.08); E1 gives
43 regions and spread 0.614193120241 as in #103; per-yantra region sums, valuation identity, sign flip, flipped normal and wall controls held.

**Results.**
1. **Regions.** 43 regions (14, 10, 10, 8, 1), **all triangles**; all 74 faces convex; even faces 12 triangles + 19 four-sided (DICTO
   Yantra 10 + 21).
2. **Points.** 18 marmas, each an order-2 zero of N with no point residue (isolated real points of N = 0, as for the DICTO Yantra);
   **22 sandhis, every one with residue 2**; free corners residue 1. New for E1: its defining incidence makes **two 4-line points**
   (t5's corner touch with t4's right leg through it, and its mirror): N vanishes there to order 2 (one more than at an ordinary
   corner touch), and the sandhi count drops by two (24 → 22), consistent with t4's leg now crossing at the corner instead of beside it. (#103 lists 28 two-line crossings for E1, counted at double
   precision where this meeting is split by 2·10⁻¹⁰; on the edge itself the count is 22 + the two 4-line points.)
3. **Centre.** Ω_Y(0, 1/2) = **+343.29** (bindu region alone 3598.37): positive, like Kulaichev (+27.45), unlike the DICTO Yantra (−86.08).
4. **Does "most even" show in the formula?** In the residues: **no.** Residues are fixed by the crossing pattern (marmas 0, sandhis 2,
   free corners 1) and are the same numbers for E1, the DICTO Yantra and Kulaichev; E1 differs only in which points exist (22 sandhis
   and two 4-line points). In the forms of the regions: **yes, exactly.** For every triangle the least value of its form is
   Ω_min = 27/(2·area) (checked: Ω_min × area = 27/2 for all 43), so the spread of the 1/Ω_min over the regions IS the area spread E1
   minimises: 0.614 for E1 against 0.866 for the DICTO Yantra (Kulaichev 0.782, its four-sided regions giving Ω_min × area = 13.545 and
   13.550, not 27/2). E1's range of least form values is the narrowest: Ω_min from 983 to 49 030 (ratio 49.9), DICTO Yantra 606 to 53 570
   (88.4), Kulaichev 747 to 2.3·10⁸ (3.1·10⁵, the tiny triangles). So "most even" = most equal least form values (in the reciprocal
   sense); the spread of Ω_min itself (not its reciprocal) is not smaller for E1 (1.886 against 1.824), because the smallest regions
   dominate it.



**Faults fixed on the way (lead b).** (1) The first numerical route (resultants by evaluation at roots of unity) missed marmas and
critical values; the positive control (R1 through the numerical route must give the exact answer) caught it; replaced by exact
resultants of M rounded to 60 digits as starting points plus Newton on M itself. (2) Critical-x offsets of 10⁻²⁰ were taken in double
precision (lost); now in PARI. (3) An unpicklable PARI error hung the pool; tasks now return errors as text. (4) The first full run missed
the point (1:0:0) at infinity (the top form has the factor y⁸): it gave genus 235; with the 8-fold point analysed the genus is 207.

Launch: the compute machine, 4 cores, memory cages 3–4 GB, through the job gate; pilots 40 s, 166 s, 38 s; full runs 296 s, 335 s, about 2 min.

**LEADS.** (a) An exact yantra with E1's crossing pattern (rational u, v, Q on E1's edge) to make the E1 results exact. (b) The 8-fold point
at infinity is the 5c lemma for parallel lines: does every family of k parallel sides give a (k − 1)-fold point, so that the genus is a
pattern count (253 − marmas − Σ C(k − 1, 2))? (c) Why the centre sign is negative only for the DICTO Yantra among the yantras tested (R1, Q3, Rh345, Kulaichev, the rhombus below u*, E1 all positive).

Credit: positive geometries and canonical forms: Arkani-Hamed, Bai, Lam (2017); the Śrī Yantra conditions: Huet (2002), Chiodo (2021);
Kulaichev's yantra: Kulaichev (1984), Rao (1998), Pustynski (2014); Rh345, the DICTO Yantra and its name are DICTO's; R1, Q3 from the
sri-yantra study (8 Nov 2026).

## #103's E1 sandhi count settled (`scripts/e1_sandhi.py`, logs `data/e1-sandhi-pilot.log`, `data/e1-sandhi.log`, FINAL ok)

**Question.** #103 (Proposition 3, Table 3, §10) lists 28 two-line crossings (sandhis) for E1; above, on E1's exact edge, the count is
22 sandhis plus two 4-line points. Which counting gives 28, and what should #103 Version 5 say?

**Method.** #103's own rule (counts.py: points where exactly two drawn sides cross, corners left out), run (1) with counts.py itself on
#103's stored E1 (`figures/even.json`, 16 digits); (2) at 300 digits on E1's exact edge (S re-solved from the incidence, as in
e1_regions.py); (3) at 300 digits just off the edge, S → S ± δ with δ = 10⁻¹⁰, 10⁻³⁰, 10⁻⁶⁰, listing the clusters at each 4-line point and
recounting the odd regions. Controls: counts.py's own K1 row (4, 5, 18, 24) and the DICTO Yantra (24 sandhis) by the same rule (positive);
off the edge the split points must not merge into 4-line points (negative). All held.

**Result.**
1. **The 4-line points.** On the exact edge the two points are t4's right leg + t5's base + t5's right leg + t6's right leg, and the mirror
   image (left legs): t5's corner touch (5,5,6) with t4's leg through it. They are corners, so #103's rule counts neither.
2. **The 28 counts each 4-line point as 3 sandhis.** counts.py as written (tolerance 10⁻³⁰, meant for 40-digit data) gives 0 marmas and
   86 sandhis on the 16-digit even.json, i.e. nothing merges; with a tolerance that fits 16 digits (10⁻¹²) it gives exactly #103's
   18 marmas and **28** sandhis. The stored E1 lies just across the edge, on the side where t4's leg cuts off t5's corner: each 4-line point
   splits into the corner touch (3 sides, a corner) plus three separate crossings of t4's leg with t5's base, t5's leg and t6's leg, so
   22 + 2 × 3 = **28**; on that side the two tiny extra triangles also appear (45 odd regions, 41 triangles + 4 four-sided). On the other
   side t4's leg passes outside t5's corner and crosses only t6's leg: 22 + 2 × 1 = **24**, 43 regions. Same at δ = 10⁻¹⁰, 10⁻³⁰, 10⁻⁶⁰.
3. **On the edge (E1 itself): 22 sandhis, two 4-line points, 43 regions, all triangles.** E1 sits exactly where the count jumps 24 → 28
   and the regions 43 → 45.

**Correct wording for #103 Version 5:** "E1 keeps 43 regions and 18 marmas; it has 22 sandhis and two points where four sides meet (t4's
leg through the corner touch (5,5,6), and its mirror image)." Proposition 3 ("the sandhis number 24 in all of them except E1"), Table 3
(E1 row: 22 + two 4-line points) and §10 to be changed to match; the answer is recorded in #103's status box (To check for Version 5).
Precision: E1 itself has no exact form, so items 1 and 3 are high precision (300 digits, incidence to 3·10⁻³⁰³); item 2 for #103's
stored data is exact (Fractions).
