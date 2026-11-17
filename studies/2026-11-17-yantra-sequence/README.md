# The DICTO Yantra with n triangles: a sequence from #103? (17 Nov 2026)

**Conclusion.** The definition DICTO approved does not yet give one integer sequence. (1) Going down from nine
triangles it is exact: there is exactly one way to take off one up-and-down pair at a time. Inside every
yantra with the traditional pattern, the 3-, 5-, 7- and 9-triangle figures have **7, 16, 29, 43** odd regions
(4 terms). (2) Going up past nine, DICTO chose to repeat the 7 → 9 step exactly (decision 1, 17 Nov). That
step cannot be repeated: done once more, it puts the new up triangle's base on the line of t6's base, because
of the corner touch (2,6,6) (§2.1, checked exactly). Each repetition would also add 6 conditions for 4 new
unknowns, so the family would be rigid at 13 and overdetermined from 15. Under decision 1 the family stops at
nine, and no sequence of 6 or more terms exists. (3) Even where the
pattern is fixed, the count depends on the free parameters. In Chiodo's 4-parameter family of nine-triangle
yantras (#103 Theorem 1) the admissible yantras have 43, 45, 47 or 49 odd regions. The values for n = 3, 5, 7
are given in §4. So a(9) = 43 holds for the DICTO Yantra and the traditional pattern, not for the whole family.
**OEIS:** 7, 16, 29, 43 has no real match, and there is no candidate with 6 or more terms to search. A growth
rule that can go on must add exactly 4 conditions per pair, as the 5 → 7 step does (§6).

Status: computed and checked as described. Not a reproduction of anyone's result. Nothing in #103 is changed.

## 1. The question

DICTO's definition (approved 17 Nov 2026), unchanged: "Take the Yantra's own construction from #103
(triangles alternating up and down along one axis, each apex resting on another triangle's base, the two
great triangles inscribed in the circle) with n triangles instead of nine, and count the regions that lie
inside an odd number of the triangles (#103 Proposition 3's parity rule). For nine triangles the count is
43. Keep the traditional pattern of which apex rests on which base, growing it one up-and-down pair at a
time."

Added the same day (DICTO): also count by Chapati and Chapati's star-point rule (G. D. Chapati and
R. Chapati, *Verified Reconstruction of the Śrī Yantra*, Zenodo 2026, doi:10.5281/zenodo.23188650, credited in
#103 §2 and §10). Their rule takes one star point per convex corner of each āvaraṇa outline (8, 10, 10 and 14
for nine triangles) and adds the trikoṇa, each tip capping one region. Also give the total number of bounded
regions, split into triangles and four-sided regions.

## 2. The traditional pattern, and what it fixes

#103's model (§1): t1–t5 point down and t6–t9 point up. Bases run from top to bottom in the order t1 … t9.
t7 (apex at the top point O) and t3 (apex at the bottom point T) are the great triangles, inscribed in the
circle. Apex on base (i): a8 = b1, a6 = b2, a9 = b3, a1 = b6, a5 = b7, a4 = b8, a2 = b9.

**The apex-on-base relation is two alternating chains.** Each arrow below means "its apex rests on the base of":

    t4 (down) → t8 (up) → t1 (down) → t6 (up) → t2 (down) → t9 (up) → t3 (down, great) → T
    t5 (down) → t7 (up, great) → O

**Taking off one pair at a time.** The rule is to remove one down and one up triangle, keep both great
triangles, and leave every remaining apex on a remaining base. The only free end is t4, since no apex rests
on t4's base; t5's partner is the great t7. So the removals are forced: first (t4, t8), then (t1, t6), then
(t2, t9). Each step has exactly one choice. This gives:

| n | triangles | apex on base | marmas and corner touches of #103 kept (those among these triangles) | free parameters |
|---|---|---|---|---|
| 3 | t3, t5, t7 | t5 on t7 | none | u, v, b5, w5 |
| 5 | + t2, t9 | + t9 on t3, t2 on t9 | (2,3,7), (2,7,9) | u, v, S, b2, b5, w5 |
| 7 | + t1, t6 | + t6 on t2, t1 on t6 | + (1,2,7), (1,5,9); corner touches (5,5,6), (2,6,6) | u, v, Q, S, b1, b2 |
| 9 | + t4, t8 | + t8 on t1, t4 on t8 | all 9 marma pairs and 3 corner-touch pairs | u, v, Q, S (Chiodo) |

In every case the bases keep the order they have in the nine. The great triangles are inscribed: P = v²/(1+v²)
and R = 1/(1+u²). Admissibility is as in #103 Theorem 1: bases strictly ordered, half-widths positive, apexes
on the right side, every corner in the closed disc.

**Even n.** Even n does not fit. The pattern changes by one down and one up triangle at a time, and the
smallest member, t3, t5, t7, cannot lose another pair without losing a great triangle. Taking off t5 alone
would leave the two great triangles, the hexagram (n = 2), but that is not a step of the stated growth.

**Going up from nine.** The chain can be extended in only one way: a new up triangle with its apex on t4's
base, then a new down triangle with its apex on the new up triangle's base, and so on. The chain does not
say at which depth the new bases lie, or which new triple meetings (marmas) the new pair must make. The steps
that are known do not repeat a rule. Going from 5 to 7, the new down base became the top base. Going from 7 to
9, t4's base went in below t3's. Without such a rule every n ≥ 11 has free parameters, and the count is not
one number (§4 shows this already for n ≤ 9). This is the choice in §6.

### 2.1 DICTO's decision 1: repeat the 7 → 9 step (17 Nov 2026)

**The step, stated by chain roles.** Write the end of the chain as …, C5, C4, C3, C2, C1, with C1 the free
end (a down triangle). For 7 → 9: C5 = t3, C4 = t9, C3 = t2, C2 = t6, C1 = t1. Let G be the triangle whose
base lies just above the new up triangle's base (t7 for 7 → 9).

- New up triangle U (t8). Its apex rests on C1's base. Its base lies on the level where C5's leg meets C4's
  leg, marma (C5, U, C4) = (3,8,9). Its leg passes through the point where C5's leg meets G's base, marma
  (C5, G, U) = (3,7,8). C1's leg, C5's base and U's leg must meet in one point, marma (C1, C5, U) = (1,3,8).
- New down triangle D (t4). Its apex rests on U's base. Its base lies on the level where C1's leg meets C2's
  leg, marma (C1, D, C2) = (1,4,6). Its leg passes through the point where C4's leg meets C2's base, marma
  (D, C2, C4) = (4,6,9). Its corner must lie on U's leg, corner touch (D, D, U) = (4,4,8).

`scripts/step_check.py` checks the rule with exact arithmetic on R1 (ℚ) and Q3 (ℚ(√Δ)). From the
seven-triangle yantra it rebuilds t8 and t4 exactly, and both closing conditions vanish (`data/step-check.log`,
FINAL ok).

**Repeating it fails at once.** For 9 → 11 the roles shift by one pair: C5 = t2, C4 = t6, C3 = t1, C2 = t8,
C1 = t4. The new up triangle's base must lie where t2's leg meets t6's leg. The corner touch (2,6,6) puts t6's
corner on t2's leg, so that point is t6's corner. The new base therefore lies on the line of t6's base, two
bases at one depth. Bases must be strictly ordered, so the figure is not admissible. The check is exact on R1
and Q3, and it holds on the whole family, because (2,6,6) is one of its conditions. In the 7 → 9 step the
pair (C5, C4) = (t3, t9) has no corner touch, which is why the step works once.

**Even without that, the parameters run out.** Each repetition adds 4 unknowns (two depths and two
half-widths; the apexes are fixed by the chain) and 6 conditions. Nine has 4 free parameters, so eleven would
have 2, thirteen 0 (finitely many yantras), and fifteen and beyond more conditions than unknowns. For
comparison, the 3 → 5 step adds 2 conditions (4 → 6 parameters), the 5 → 7 step adds 4 (6 → 6) and the 7 → 9
step adds 6 (6 → 4). Only a step with exactly 4 conditions, like 5 → 7, can be repeated without end.

**What decision 1 settles, by item.**
- (a) Under decision 1 the family is n = 3, 5, 7, 9. Its odd-region counts are those of §4.2.
- (b) "Meets every condition" (Kulaichev's (b), (c), (d) with uv = 2/φ³, as the DICTO Yantra) picks out one
  yantra only at nine. That is the DICTO Yantra, with 43 = 14, 10, 10, 8, 1, certified (#103 Theorem 15,
  Proposition 11). At seven the same four conditions, on 6 parameters, leave a 2-parameter set by the count of
  conditions (not computed), not one member. At five t1 is missing, and at three t1 and t9 are, so (b) and
  (d) are not defined there.
- (c) Counts with all odd regions triangles, among the samples: n = 3: 7 (6, 1); n = 5: none; n = 7: 31
  (14, 9, 7, 1), 17 of 1500 samples; n = 9: 43 (14, 10, 10, 8, 1). The sub-yantras of §4.1 (7, 16, 29, 43) have
  this property only at 3 and 9.
- (d) Star points (outline version), alongside (c): 7, —, 25, 43.

## 3. Calibration (passed)

The counter is `scripts/yarr.py`. It builds the arrangement of all 3n sides and the regions by a half-edge
walk. The depth of each region is the number of triangles containing it. The counter checks itself on every
figure: Euler V − E + F = 2; one depth from every side of a region; every edge on exactly one side, changing
the depth by one; and Σ depth × area equal to the sum of the triangles' areas. True corners are counted as in
study 2026-11-15-chapati-vs-103: a point where a line only ends on a side is not a corner. Arithmetic is exact,
in ℚ or in ℚ(√Δ) with the exact `QF` class of study 2026-11-12-yantra-regions-45. The two yantras stored as
decimals (40 and 60 digits) have their points merged within 10⁻²⁵.

| yantra | odd regions (parity) | odd: triangles / four-sided | all bounded regions | star points, outline from the arrangement | star points, Chapati and Chapati's own code |
|---|---|---|---|---|---|
| R1 (exact, ℚ) | 43 = 14, 10, 10, 8, 1 | 43 / 0 | 74 = 53 + 21 | 43 = 14, 10, 10, 8, 1 | — |
| DICTO Yantra | 43 = 14, 10, 10, 8, 1 | 43 / 0 | 74 = 53 + 21 | 43 = 14, 10, 10, 8, 1 | 43 = 1, 8, 10, 10, 14 |
| Q3 (exact, ℚ(√Δ)) | 45 = 14, 10, 12, 8, 1 | 41 / 4 | 78 = 53 + 25 | 45 = 14, 10, 10, **10**, 1 | — |
| Kulaichev's yantra | 45 = 14, 10, 12, 8, 1 | 41 / 4 | 78 = 53 + 25 | 45 = 14, 10, 10, **10**, 1 | 43 = 1, 8, 10, 10, 14 |

All the targets are met: 43 and 45 with their rings, 74 = 53 + 21, 78 = 53 + 25, and 43 star points by
Chapati and Chapati's code on both the DICTO Yantra and Kulaichev's yantra. Logs: `data/calibration.log`,
`data/chapati-cross.log`, both FINAL ok.

**The star-point rule for n triangles.** Chapati and Chapati's code does not compute its outlines from the
figure. It reads them from Huet's appendix as polygons through named points of the nine-triangle
construction, so it exists only for nine. The only version that works for any n takes the outline of the
part covered at least c times (c = 1, 3, 5, …), counts its convex corners, and adds the regions at the
deepest level (the trikoṇa counted once). On the traditional pattern the two versions agree circuit by
circuit (14, 10, 10, 8, 1). On Kulaichev's yantra and Q3 they part. The actual outline of the eight-cornered
circuit there has two more convex corners, so the outline version gives 45, while Huet's transcribed
outline still gives 43. **No version that works for any n can give 43 for Kulaichev's yantra.** Their 43
there comes from drawing the traditional outline, not from the figure.

## 4. Results

### 4.1 The yantras inside the traditional one (the descending sequence)

Pairs are taken off the actual nine-triangle yantras (`scripts/subyantras.py`, `data/subyantras.log`, FINAL ok):

| n | odd regions (parity) | by depth 1, 3, 5, … | odd: triangles / four-sided / more corners | all bounded regions = triangles + four-sided + more | star points (outline) |
|---|---|---|---|---|---|
| 3 | **7** | 6, 1 | 7 / 0 / 0 | 8 = 7 + 0 + 1 | 7 |
| 5 | **16** | 12, 3, 1 | 13 / 0 / 3 | 26 = 18 + 5 + 3 | 14 |
| 7 | **29** | 14, 7, 7, 1 | 23 / 6 / 0 | 48 = 31 + 17 + 0 | 27 (R1, Q3) or 29 (DICTO Yantra, Kulaichev) |
| 9 | **43** (R1, DICTO Yantra); 45 (Q3, Kulaichev) | 14, 10, 10, 8, 1 | 43 / 0 / 0 | 74 = 53 + 21 + 0 | 43; 45 |

For n = 3, 5, 7 the parity counts are the same on all four yantras. The star count at n = 7 is not: two
convex corners come and go with the yantra.

### 4.2 The counts depend on the parameters

For each n = 3, 5, 7, 9, `scripts/family.py` drew 1500 admissible yantras of §2's pattern with rational
parameters, in the box u, v ∈ [0.45, 1.1], Q ∈ [0.40, 0.75], S ∈ [0.75, 0.999], with the other free depths and
widths inside their admissible ranges. It used exact arithmetic and checked every retained condition exactly.
Log `data/family-run.log`, raw data `data/family-n3-9-seed20261117.json`, FINAL ok.

| n | odd-region counts found | star-point counts (outline) found | all bounded regions found | distinct count patterns |
|---|---|---|---|---|
| 3 | 7, 9, 11 | 7, 9 | 8, 12, 16 | 6 |
| 5 | 12, 16, 18, 20, 22, 24 | 12, 14, 16, 18, 20, 22 | 18, 22, 26, 30, 32, 34, 38 | 17 |
| 7 | 23, 25, 27, 29, 31 | 23, 25, 27, 29 | 44, 48 | 8 |
| 9 | **43, 45, 47, 49** | 43, 45, 47 | 74, 78, 82, 86 | 6 |

Nine triangles, Chiodo's family (#103 Theorem 1, all 18 marmas and 6 corner touches exact). The share of
samples is a property of the sampling box, not of the yantra:

| odd regions, by depth 1, 3, 5, 7, 9 | odd: triangles / four-sided | all regions | samples | star (outline) | star (Chapati's code) |
|---|---|---|---|---|---|
| 43 = 14, 10, 10, 8, 1 | 43 / 0 | 74 = 53 + 21 | 572 | 43 | 43 |
| 45 = 14, 10, 14, 6, 1 | 42 / 2 | 78 = 54 + 23 + 1 | 506 | 43 | 43 (one sample: 42) |
| 45 = 14, 10, 12, 8, 1 (Kulaichev's pattern) | 41 / 4 | 78 = 53 + 25 | 330 | 45 | 43 (two samples: 41) |
| 49 = 14, 12, 16, 6, 1 | 42 / 6 | 86 = 58 + 23 + 5 | 60 | 47 | 43 (one: 41) |
| 47 = 14, 12, 14, 6, 1 | 40 / 6 | 82 = 56 + 23 + 3 | 21 | 45 | 43 (two: 41) |
| 45 = 14, 12, 10, 8, 1 | 41 / 4 | 78 = 53 + 25 | 11 | 45 | 43 (one: 39) |

Chapati and Chapati's code returns 43 on 1492 of the 1500 samples (`data/chapati-cross.log`). Its outline is
the traditional one by construction, so it returns 43 whatever the figure does. Its 8 other values (39–42)
come where its double-precision tolerances miss a tip.

**Where each pattern lies.** `data/regions-n9.log` gives the ranges. The six patterns overlap in every
coordinate (u, v, Q, S, uv, u/v), so no box or single threshold separates them. Their borders are walls
where three sides meet, of the kind in #103 Proposition 13 (the rhombus threshold u*). One of those walls
separates 43 from Kulaichev's 45, and the region of the DICTO Yantra is the 43 one. Four of the six patterns
are not in #103, which reports only 43 = 14, 10, 10, 8, 1 and 45 = 14, 10, 12, 8, 1: 45 = 14, 10, 14, 6, 1;
45 = 14, 12, 10, 8, 1; 47; and 49.

## 5. OEIS check (search only, 17 Nov 2026)

| searched | hits | verdict |
|---|---|---|
| 7, 16, 29, 43 (parity, inside the traditional yantra) | A386386 (a permutation of the integers; the four terms occur by chance in its data) | no real match |
| 7, 16, 29, 45 (the same inside Kulaichev's yantra) | A398857 (a midsequence of triangular and pentagonal numbers), A211784 (n² + ⌊n²/2⌋ + ⌊n²/3⌋) | chance agreement of 4 small terms; no relation known |
| 7, 14, 27, 43 / 7, 14, 29, 43 (star points, outline) | none | — |
| 7, 14, 27, 45 | A227016, A019459 | chance |
| 8, 26, 48, 74 (all bounded regions) | none | — |

Four terms are too few for an OEIS entry in any case.

## 6. Open questions for DICTO

1. **How does the yantra grow past nine?** Decision 1 (repeat 7 → 9) cannot be carried out (§2.1). A step
   that can go on must add exactly 4 conditions per pair, and its two new legs must not meet at an old
   corner. The traditional pattern has one such step, 5 → 7 (marmas (1,2,7), (1,5,9) and corner touches
   (5,5,6), (2,6,6)). Repeating it would keep 6 free parameters at every n. The alternative is to drop
   conditions from the 7 → 9 step (two of its six) so that it keeps 4. Either way it is DICTO's choice, and
   §4.2 shows that the count will still depend on the parameters.
2. **Which member counts?** For n = 9 the family gives 43, 45, 47 and 49. A sequence needs one member per n,
   for example "the member that meets every condition" (as the DICTO Yantra does for nine: (b), (c), (d) and
   uv = 2/φ³). It could also be "the traditional crossing pattern" (all odd regions triangles, which picks 43
   for nine. Among the samples, n = 3 has it at 7 and n = 7 at 31, and n = 5 has no sample with it).
3. **Which star-point rule?** Only the version that takes the outline from the figure exists for n ≠ 9. It
   agrees with Chapati and Chapati on every traditional-pattern yantra and parts from them on Kulaichev's
   (45 against 43).

## 7. LEADS

1. Describe the walls between the six nine-triangle patterns exactly. Each is one concurrency of three
   sides, as in Proposition 13. Then give the exact admissible region of each count (open in #103: "a
   description of the whole admissible region is open"). This would be a result for #103's line of work, not
   a new paper. Placement: ask DICTO.
2. The four nine-triangle patterns not in #103 (45 = 14, 10, 14, 6, 1; 45 = 14, 12, 10, 8, 1; 47; 49) are
   already exact rational samples in the raw data. Check whether any of them can meet (b), (c), (d).
3. The descending numbers 7, 16, 29, 43 hold on four yantras. Prove that they hold on the whole region where
   the nine-triangle count is 43 (the same parity count on a cell of the parameter space).
4. Once DICTO picks a growth rule that can be repeated (§6.1), compute n = 11, 13, … with `family.py`, adding
   one builder per n. The counter `yarr.py` already takes any n, and the role form of `step_check.py` is the
   template for a builder.

## 8. Files and how to rerun

- `scripts/yarr.py` is the counter (arrangement, parity, true corners, star points from the outline, self-checks). The `QF` class is copied from study 2026-11-12-yantra-regions-45.
- `scripts/model.py` is copied unchanged from study 2026-11-08-sri-yantra (Chiodo's construction, #103's model).
- `scripts/calibrate.py` and `scripts/calibrate_loaders.py` run §3 (`data/calibration.log`, `data/calibration.json`).
- `scripts/subyantras.py` runs §4.1 (`data/subyantras.log`, `data/subyantras.json`).
- `scripts/family.py` runs §4.2: `python3 family.py <study dir> 1500` (`data/family-run.log`, `data/family-n3-9-seed20261117.json`).
- `scripts/regions_n9.py` gives the parameter ranges of each nine-triangle pattern (`data/regions-n9.log`, `data/regions-n9.json`).
- `scripts/chapati_cross.py` runs Chapati and Chapati's own enumerator (MIT licence, their `src/` from the Zenodo zip, imported unchanged and not copied here) on the nine-triangle samples (`data/chapati-cross.log`, `data/chapati-cross-n9.json`).
- `scripts/step_check.py` runs §2.1, decision 1 (`data/step-check.log`).
- `data/input/` holds copies of the stored yantras (quadratic-examples.json, golden_family.json, kulaichev-numeric-data.txt) from study 2026-11-08-sri-yantra.

All of it was run on the compute host. Every script ends in a checked FINAL line, and all of them read FINAL ok.

DICTO: the definition, the question and the request for both rules. Computation and drafting with Claude (Anthropic).
