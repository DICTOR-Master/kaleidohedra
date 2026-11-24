# Certifying the 4 404 Aequi of study 2026-11-19 whose groups do not contain T (24 November 2026)

DICTO · dictospheres.com · study 2026-11-24-aequi-certify-4404 · with Claude (Anthropic).

**Verdict: all 4 404 are rigorously certified.** These are the Aequi of study 2026-11-19-aequi-complete whose full symmetry group
does not contain T (the 4 553 minus the 149 frame-group dice, which are among the 1232 certified in Part 1 of study
2026-11-24-aequi-certify-extend). For each die, ball arithmetic proves that exactly one fair depth vector lies in an explicit box
around its published 60-digit depths, that those depths are within 5.0e-60 of it, and that the face structure is constant over
the box (or, for 5 dice, constant on each side of one wall). summarize.py: **FINAL ok**. Approved by DICTO 24 Nov (item C).

**Not numbered here** (decided): they receive catalogue numbers after No. 10725 in a later batch. This study records only their
certified status.

## Result (logs/summarize.log)

| | count |
|---|---|
| dice | 4 404 (all m ≥ 2) |
| certified on a box of constant type (tight Krawczyk ok, symmetry ok, face graph ok) | 4 399 |
| certified on a split box (fair point on a wall where the type changes; split Krawczyk ok) | 5 |
| not certified | 0 |
| dice with structural corners (four or more planes through a corner for every depth vector) | 1 366; 2 195 distinct exact checks, 0 failures |
| certified with one depth per frame-map orbit (full group not made of frame maps: D2h 16, D6h 1, D8h 1) | 18 |

By group: C2h 888, D2 857, D2h 848, S6 694, D3 344, Ci 280, D3d 261, D5d 112, D5 62, D2d 27, D4h 17, S4 8, D6h 2, D10h 1,
D3h 1, D5h 1, D8h 1 (total 4 404).

- Tight boxes (r = 1e-40): every published depth vector lies within 5.0e-60 of the fair one; largest |F(x̃)| = 6.1e-59; largest
  |Ω − 4π/N| over all faces at the published depths 6.1e-59 (check of the symmetry reduction).
- Uniqueness half-widths (largest box tried with exactly one fair die, depths near 1): 1e-2: 598, 3e-3: 1 458, 1e-3: 1 548,
  3e-4: 644, 1e-4: 108, 3e-5: 28, 1e-5: 9, 3e-6: 2, 1e-6: 2, 1e-7: 1, 3e-8: 1.
- The 5 split-box dice (each with one wall h = 0 through the fair point, |h| ≤ 6e-61 there):
  - D5d: C6+RT24/10 + O8+I12/10 (4) (sid 89), split half-width 1e-2;
  - D5d: C6+RT24/10a + C6+RT24/10b + O8+I12/10a + O8+I12/10b (3) (sid 160), 3.2e-4;
  - D3d: C6+RT24/6 + I12/2 + RT24/12 (2) (sid 307), 3.2e-3;
  - D3d: O8+I12/6 + I12/2 + RT24/12 (sid 310), 3.2e-3;
  - D3d: C6+RT24/6a + C6+RT24/6b + O8+I12/6 + RT24/12 (1) (sid 417), 1e-3.
  As in the extension study, the fair point lies on the wall to 60 digits; whether it lies there exactly is open (LEAD 1).

## Method

Exactly the method of Part 1 of study 2026-11-24-aequi-certify-extend, run with its scripts unchanged (certify.py, accidental.py,
structural.py; read there for the full argument): exact face normals over Q(√5) as 320-bit arb balls; symmetry reduction to one
depth per orbit (checked against the frame maps); the combinatorial type certified constant over the box by linear slacks and the
edge-graph argument (Balinski); structural corners proved exactly in Q(√5); Krawczyk's test with an arb enclosure of the Jacobian
(forward differentiation); a split box with the hull of the two one-sided Jacobians for the dice on a wall. Solid angles:
Van Oosterom and Strackee (1983). Ball arithmetic: python-flint (arb, Johansson). Krawczyk's operator: Krawczyk (1969). No Newton
step: the 60-digit depths of study 2026-11-19 were used as published.

Run: scripts/make_dice.py writes the input list (asserts 4 553 dice in study 2026-11-19, 4 404 without T, sids distinct);
scripts/run.sh certifies; scripts/summarize.py prints FINAL ok only if every die is certified (or split-box certified), labels and
N agree, and the structural checks have no failure. A pilot of 30 dice (two per group, logs/*-pilot.log) passed first; the full run
used 16 cores on a compute host (certify step 24 s).

## Files

- scripts/make_dice.py, run.sh, summarize.py.
- data/certify4404.jsonl.gz (one record per die: status, type radius, tight and wide Krawczyk results, structural corners),
  accidental4404.json (the 5 split-box dice), structural4404.json; pilot files *-pilot.*. data/dice4404.json (input list) is not
  committed; make_dice.py rebuilds it.
- logs/: make_dice, certify4404, accidental4404, structural4404, summarize.

## LEADS

1. The 5 dice on a wall: look for exact ratios, as for row 95 of the extension study (cos 18°, cos 30°, equal depths).
2. Number the 4 404 after No. 10725 (order as in study 2026-11-24-aequi-catalogue-2: each group one block); catalogue-2 already
   shows none of its 9 490 is congruent to any of the 4 553.
