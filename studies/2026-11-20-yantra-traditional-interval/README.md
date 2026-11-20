**Verdict: the traditional window is a theorem on 0.3364 ≤ c ≤ 0.5640.** Every yantra with Huet's conditions, Kulaichev's (b) and (c), and admissibility, whose great slopes have product c = uv with c_lo < c < c*, is unique up to the viewpoint and has the traditional form: 43 regions, all triangles, 18 marmas, 24 sandhis. Just beyond each end, out to c = 0.3364 below and c = 0.5640 above, it has 45 regions (41 triangles), 18 marmas and 28 sandhis. Every step is a certified computation, and every certificate ends FINAL ok. Kulaichev's yantra lies above c*, exactly. Outside 0.3364 ≤ c ≤ 0.5640 nothing new is certified: there the earlier scans remain computed only.

# The traditional window, certified (study 2026-11-20)

DICTO approved this study on 20 Nov 2026: "certify the traditional-form interval for #103 v8". It builds on study 2026-11-20-cleo-antonius-selection, which found the window and certified its two ends but computed the counts inside at 60 digits only (its LEADS 1). This study makes the interior a theorem and certifies a stretch beyond each end. #103 was not edited.

## 1. The proposition for #103 Version 8

Placement: directly after Proposition 13 (the rhombus threshold), which it contains and makes certified. Its number follows the paper's sequence when it is placed.

**Proposition (the traditional window).** Take a yantra in the model of §1 that meets Huet's conditions in Chiodo's form [1, 2], Kulaichev's (b) and (c) [4], and admissibility as in Theorem 1. Let c = uv be the product of its two great slopes. Let c_lo = 0.346198290229885036933… and c* = 0.556510833490959503531… be the two roots of the irreducible integer polynomial g90 of degree 90, g90(c) = f180(√c), that lie in [3461982902298850369337545579901666303262, 3461982902298850369337545579901666303265]·10⁻⁴⁰ and [5565108334909595035316398529088728582340, 5565108334909595035316398529088728582343]·10⁻⁴⁰. Here f180 is the polynomial of Proposition 13, so c* = u*².
1. **One yantra for each product.** For every c with 0.3364 ≤ c ≤ 0.5640 there is exactly one such yantra up to the viewpoint (Theorem 5).
2. **The window.** For c_lo < c < c* it has the traditional form: 43 odd regions (14, 10, 10, 8, 1), all of them triangles, 18 marmas, 24 sandhis and 74 bounded regions.
3. **Just outside.** For 0.3364 ≤ c < c_lo and for c* < c ≤ 0.5640 it has 45 odd regions (14, 10, 12, 8, 1), 41 of them triangles, 18 marmas, 28 sandhis and 78 bounded regions.
4. **The ends.** In this range, t4's right leg passes through t5's corner, where t5's base and t6's right leg meet (the corner touch (5,5,6)), at c = c_lo and c = c* and nowhere else; the mirror image does the same. These are the three lines of Proposition 13 and Figure 12.
5. **Named yantras.** The DICTO Yantra (c = 2/φ³ = 0.4721) lies inside the window, 0.599 of the way from c_lo to c*. Kulaichev's yantra (c = 0.5631579663…, Theorem 10) and Rh345 (c = 9/16) lie above c*.

**Proof (certified computation).**
- *Reduction to the rhombus.* By Theorem 5, the viewpoint map with λ = √(v/u) takes a yantra with slopes u, v to one with u = v = √c, and keeps the conditions, admissibility and every count. So it is enough to treat the rhombus family u = v. In the census unknowns of Theorem 15 (t = b1/w1, so (b) holds by construction, and S = b9), every admissible yantra of this family solves G = 0, which is (c), and H1 = 0, the closing marma (1,4,6); the factors stripped by the divisor lemma are nonzero on admissible yantras.
- *Uniqueness (part 1).* The range 0.58 ≤ u ≤ 0.751 is cut into 684 boxes. On each box, G has exactly one root S in (R, 1), and the other root is certified outside [R, 1]. Interval Newton (Moore [24]) gives a t-box that holds exactly one root of H1 for every u and S of the box. The rest of 0 < t < u is cut into 51 205 boxes, and each one is closed by a single test: either H1 has no zero on it, or the yantra built from it breaks an admissibility condition everywhere on it.
- *The sweep (parts 2 to 4).* The arrangement of the 27 drawn sides can change only when three sides pass through one point that lies on all three closed sides. The same range of u is cut into 2375 boxes, bisected where a test needed it. On each box, ball arithmetic encloses the yantra, admissibility (strict) and the determinant of every triple of the 27 lines by the centred form, with derivatives in u carried through the whole construction. Each of the 2810 triples that are not identities is then decided in one of two ways: its determinant has a fixed sign on the box, or its meeting point is certified off one of the three sides. The 115 identities (84 triples of parallel bases and the 31 Huet conditions) are decided exactly, in the model of Proposition 11. Triples that hold both opposite sides of the rhombus never meet at a finite point, because those two sides are parallel and distinct. The six threshold triples (t4's leg with two of t5's base, t5's leg and t6's leg, and their mirror images) are excused only on the two boxes that hold an end. On those boxes the crossing determinant C = det(t4 right leg, t5 base, t6 right leg) is monotone. The other threshold triples vanish exactly where C does, because t5's base, t5's right leg and t6's right leg always meet in one point; the mirror triples follow by symmetry. So the counts are constant on [0.3364, c_lo), on (c_lo, c*) and on (c*, 0.5640].
- *The ends exactly.* At each end the Krawczyk test [14] proves that G = H1 = C = 0 has exactly one solution in a box of radius 2⁻³⁰⁰. Elimination (Singular, PARI) shows that the u of that solution is the root of f180 isolated above. On the branch, C changes sign between u_m − 2⁻³¹⁰ and u_m + 2⁻³¹⁰, and the branch over that interval lies inside the Krawczyk box. So the one zero of C on each end box is exactly √c_lo or √c*.
- *The counts.* Proposition 11's pipeline (every decision a certified sign or an exact identity) counts the arrangement at four points of the branch, enclosed to about 570 digits. It gives 43 / 18 / 24 at c = 2/φ³ (the rhombus image of the DICTO Yantra) and at c = 0.49. It gives 45 (41 triangles) / 18 / 28 at c = 0.3364 and at c = 9/16 (Rh345, matching Proposition 11 to the last margin). These points carry the counts to the three stretches.
- *Part 5.* Kulaichev's u is isolated as a root of f348 (Theorem 10), and c_K = u_K² > c* is shown by comparing rational intervals (PARI polsturm).

All of this ball arithmetic is Arb (FLINT, through python-flint), as in Proposition 11 [16]. ∎

**Remarks for the text.**
- **Proposition 13 becomes certified.** Its u* is √c*, and part 4 with parts 2 and 3 certifies "43 just below u*, 45 just above". Its "Computed, not certified" can go, and its row in Table 5 moves to the certified results.
- **§9.5, open question (2), is now answered for (b), (c) yantras on 0.3364 ≤ c ≤ 0.5640.** The 45-region rule there is one crossing, of t4's leg through the corner touch (5,5,6), at c_lo and at c*.
- **§10.1.** The observation "the two great slopes add up to about 1.49 or more" can be replaced by part 2 (2√c* = 1.49199…).
- **The ends themselves are not counted.** At c = c_lo and c = c*, E1's edge, Figure 11 counts 22 sandhis and two points where four sides meet; that count is computed, not certified here.
- **A small event outside the counts.** At u ≈ 0.74685 (c ≈ 0.5578, above c*), t5's right leg turns parallel to t3's right leg and t7's left leg. Parallel lines do not meet, so the arrangement does not change there. The sweep excuses those triples for this reason only.

**Credits at point of use.**
- Huet's conditions: Huet [1], in Chiodo's form [2]. The conditions (b) and (c), and the equal great triangles of Kulaichev's yantra: Kulaichev [4].
- The Krawczyk test: Krawczyk [14].
- Interval Newton and the centred (mean-value) form: R. E. Moore, *Interval Analysis* (Prentice-Hall, 1966). This is a new reference; it is cited as [24] above.
- Software: Singular through Sage, PARI/GP through cypari2, FLINT with Arb through python-flint, and mpmath [16].
- The sweep's structure follows the threshold certificate of study 2026-11-10-g1-e1-exact (threshold_cert.py). The census unknowns and the divisor lemma come from Theorem 15. The counting pipeline is Proposition 11's certified_counts.py, used unchanged except for a choice of the expected counts.

## 2. What is certified, and what is not

| Claim | Status | How |
|---|---|---|
| One yantra up to the viewpoint for each c in [0.3364, 0.5640] | **certified** | cert3_unique.py |
| 43 / 18 / 24 (all triangles, 74 regions) for c_lo < c < c* | **certified** | cert1 + cert0 + cert2 + cert4 |
| 45 (41 triangles) / 18 / 28 (78 regions) for 0.3364 ≤ c < c_lo and c* < c ≤ 0.5640 | **certified** | the same |
| The threshold crossing at c_lo and c* exactly, and nowhere else in the range | **certified** | cert1 (monotone, nonzero elsewhere) + cert2 (Krawczyk, elimination) |
| c* < c_K (Kulaichev), c_lo < 2/φ³ < c*, Rh345 above c* | **certified** (exact) | cert5_compare.py |
| Theorem 5's reduction (any u, v to u = v) and the divisor lemma | proved in #103 (Theorem 5) and in Theorem 15's census | cited, not recomputed |
| Counts at c = c_lo and c = c* themselves | not certified | computed in #103 (E1, Figure 11) |
| The form for c < 0.3364 or c > 0.5640, so "traditional exactly when c_lo < c < c*" over the whole range 0 < c < 0.7612 | **not certified** | computed (study 2026-11-20-cleo-antonius-selection, 2000-point scan; events at c = 0.16188 and below c = 0.0015) |

So the proposition says "for 0.3364 ≤ c ≤ 0.5640", and not "exactly when" over the whole family. The wider claim stays computed until LEADS 1 is done.

## 3. Method

Every certificate ran on the compute host. Nothing was computed on the interface machine.

| Script | What it does |
|---|---|
| scripts/ycert.py | The shared model in Arb ball arithmetic. It holds G, H1 and C with v = u (data/system-uv.json, copied from the selection study) and the construction of yfam.build line by line in forward-derivative numbers. It encloses the branch: S from the quadratic G, with the other root certified outside [R, 1]; t by parametric interval Newton with centred forms. It also gives the lines, determinants, the meeting parameters along the sides, and Theorem 1's admissibility quantities. |
| scripts/cert0_identities.py | At u = 7/10 and u = 29/50 (2000 bits), the triples whose determinant ball holds 0 are the candidates. Each is decided exactly in the case K model of #103's audit: the symbolic determinant is zero, or it is a multiple of the closing numerator Fc (inputs/model.py, inputs/stage2-K.json). Also: the two pairs of opposite rhombus sides are parallel identically. Writes data/identities.json. |
| scripts/cert1_sweep.py | The sweep, u in [29/50, 751/1000], 684 starting boxes, bisected up to 12 times, 22 processes, 256 bits. Writes data/sweep-29_50-751_1000.json (every box, its smallest margins, and the sign of C). |
| scripts/cert2_ends.py | A copy of the selection study's s4_endpoints.py, with step (4) added. It runs the Krawczyk test for G = H1 = C = 0 at 1200 bits and the elimination (Res_S, then Res_t, degree 1928, with the factor through each end shown to be f180). It runs polsturm and the irreducibility of f180 and g90. Then it checks that the branch's C changes sign within 2⁻³¹⁰ of the end, inside the Krawczyk box. Its outputs data/window-exact-recheck.json and data/g90-c-recheck.txt are byte-identical to the selection study's files. |
| scripts/cert3_unique.py | Uniqueness on [29/50, 751/1000]: 684 u-boxes, with t bisected up to 40 times. Writes data/unique-29_50-751_1000.json. |
| scripts/cert4_counts.py with scripts/certified_counts.py | Encloses the branch at four points (1900 bits) and writes stage5-K.json. It then runs #103's certified_counts.py (case K). The one change to that script is an argument for the expected counts, and the triangles are compared in both cases. Outputs are in data/counts/. |
| scripts/cert5_compare.py | Exact placement of Kulaichev's yantra, the DICTO Yantra, Rh345 and the sweep ends against the window (PARI polsturm, rational intervals). |
| scripts/explore/x0_solutions.py | Exploration, not a certificate: every real solution at sample u, with its admissibility slack. Besides the branch there is exactly one other solution, and it breaks admissibility by 0.5 to 2.2. This is what made the uniqueness bisection feasible. |

## 4. Checks (every certificate ends FINAL ok; logs in logs/)

- **cert0.** At both points the same 115 candidates hold 0: 84 triples of bases and 31 others. All 115 are exact identities (identically zero, or a multiple of Fc). The 31 are the 18 marma triples, the 6 corner touches and the 7 apex-on-base triples. Every other triple is certified nonzero, the smallest being 4.2·10⁻⁶ at u = 29/50. Both opposite-side pairs (R3, L7) and (L3, R7) are parallel identically.
- **cert1.**
  - The 2375 boxes cover [29/50, 751/1000] with no gap. The deepest bisection is 11, and no box fails.
  - The two end boxes are [602507/1024000, 241003/409600], which holds √c_lo, and [3055601/4096000, 1527801/2048000], which holds √c*. On both, dC/du has a fixed sign (+ at the lower end, − at the upper end), and all six threshold triples are monotone.
  - C is certified positive on every box inside the window (1899 boxes) and negative on every box outside it (474 boxes).
  - The smallest certified |det| is 4.3·10⁻¹², on the threshold triples next to the end boxes. The smallest admissibility slack is 5.3·10⁻³.
  - Two boxes near u = 0.74685 excuse the triples that hold both opposite rhombus sides (see §1, "A small event outside the counts").
- **cert2.**
  - Both Krawczyk tests pass.
  - At each end, the only factor of the eliminant that can vanish is f180. polsturm finds exactly 1 root of f180 in each u-interval and of g90 in each c-interval. f180 and g90 are irreducible.
  - On the branch, C at u_m ∓ 2⁻³¹⁰ is ∓4.93·10⁻¹⁰⁰ at the lower end and ±1.95·10⁻⁹⁷ at the upper end, so it changes sign at both. The branch over that interval lies inside the Krawczyk box.
- **cert3.** The 684 u-boxes cover the range and none fails. The 51 205 t-boxes are closed as follows:
  - H1 nonzero: 46 187;
  - b6 < b7 broken: 2883;
  - b3 < b4 broken: 1189;
  - b5 < b6 broken: 476;
  - t1's apex on the wrong side: 349;
  - t6's corner outside the disc: 121.
- **cert4.** Every count has Euler characteristic 2. The 31 concurrencies and the 38 parallel pairs are decided exactly.

  | Point | c | Odd regions (triangles) | Rings | Marmas | Sandhis | Bounded regions | Smallest margin |
  |---|---|---|---|---|---|---|---|
  | u = 29/50 | 0.3364 | 45 (41) | 14, 10, 12, 8, 1 | 18 | 28 | 78 | 1.1·10⁻⁷ |
  | u = √(2/φ³) | 0.47214 | 43 (43) | 14, 10, 10, 8, 1 | 18 | 24 | 74 | 5.2·10⁻⁶ |
  | u = 7/10 | 0.49 | 43 (43) | 14, 10, 10, 8, 1 | 18 | 24 | 74 | 3.4·10⁻⁵ |
  | u = 3/4 (Rh345) | 0.5625 | 45 (41) | 14, 10, 12, 8, 1 | 18 | 28 | 78 | 4.672·10⁻⁸ |

  - At u = √(2/φ³) the smallest margin is the same near-concurrency of t6's and t8's left legs with t5's right leg that Proposition 11 reports for the DICTO Yantra.
  - At u = 3/4 the margin of 4.672·10⁻⁸ and the 5965 certified signs are exactly #103's Rh345 numbers.
- **cert5.**
  - f348 is irreducible and has exactly one root in [0.7504385160222140, 0.7504385160222141].
  - c_K is in [0.56315796632962, 0.56315796632963], so c_K − c* > 6.6·10⁻³.
  - c_lo < 2/φ³ < c*.
  - Rh345 (9/16) is above c*. u = 29/50 is below c_lo, and 751/1000 is above c*.
  - c_K < (751/1000)², so Kulaichev's yantra lies inside the certified stretch above the window. Its certified count (Proposition 11: 45 / 41 triangles / 18 / 28) agrees with part 3.

## 5. Sources checked

- #103 (paper.html, Version 7 text): Theorem 1, Theorem 5, Proposition 11, Proposition 13, Table 5 and the references [1], [2], [4], [14], [16].
- Study 2026-11-20-cleo-antonius-selection: the README, data/window-exact.json, data/g90-c.txt, data/system-uv.json, scripts/s0_generic.py, s4_endpoints.py and yfam.py.
- Study 2026-11-10-g1-e1-exact: threshold_cert.py.
- The #103 audit (study 2026-11-09-yantra-audit): certificates/piece_counts/certified_counts.py, certificates/rh345/rh345_certify.py and its log, and common/stage2_symbolic.py. model.py and stage2-K.json were taken from the audit's working copy.
- Study 2026-11-15-yantra-box-certificate: the README (its box coordinates and the bound t < u).

## LEADS

1. **Make "exactly when" global.** Extend the sweep and the uniqueness bisection to all of 0 < c < 0.7612…. The new work is:
   - the event at c = 0.16188 (t4's and t5's legs with t9's leg on t6's base);
   - the change below c = 0.0015, near the degenerate corner u → 0, which needs blow-up charts as in study 2026-11-15-yantra-box-certificate;
   - the end of admissibility near c = 0.7612.

   Then the proposition can say "exactly when c_lo < c < c*" without a range.
2. **Certify the counts at the two ends** (E1's edge: 22 sandhis and two points where four sides meet). Use the Krawczyk box of cert2 as the enclosure, and decide the threshold triple exactly as zero by the f180 identity.
3. **Edit #103 for Version 8** when DICTO says so:
   - place the proposition after Proposition 13;
   - drop "Computed, not certified" from Proposition 13 and move its row in Table 5;
   - narrow §9.5's open question (2) and the open list in §13;
   - add Moore (1966) to the references;
   - replace §10.1's "about 1.49" sentence.
4. **Outside the plan.** The window theorem holds for every (b), (c) yantra and does not depend on Kulaichev's (a) or (d). Study 2026-11-20-cleo-antonius-selection noted that it could be scored on its own. It is still not a selection of the Cleo-Antonius.

FINAL ok
