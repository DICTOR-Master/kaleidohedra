# The Laves big atom on the three-layer window: the last exception of the Hexagonality Law (12 Nov 2026)
Gap row (Concordance gaps.ranked): "The Hexagonality Law for the Laves big atom (#66, #67)": "#84 shows the Swap Rule is the
condition to stay on the line; check it on the three-layer window"; goal: the last exception of the law explained.

**Conclusion:** the exception was a labelling shift, not a three-layer piece: the big atom M0 of gap k sits IN layer k, and its
piece is fixed by exactly TWO layer types, its own layer k and the layer below (k-1), on all 18 computed stackings and in every
lam-window (only the type of layer k-1 between 17/96 and 7/32). On that pair it obeys the Swap Rule as an identity in lam, so #66's
theorem covers it; the three-layer Swap defects (#84 (c), g = 3) are zero in every window. The law holds for M0 wherever the other
Laves roles hold it: proved from the pieces' locality, which for all six roles is found on the data (#64), not proved.

## Question
In the Laves phases (#64) the big atom at the foot of a gap, role M0, has a piece fixed by THREE layer types above lam = 17/96, so
#66's proof (a piece fixed by two layers + the Swap Rule) does not reach it. #66 and #67 found the law exact for M0 on every stacking
tested (up to 8 layers, 390 of 390) and left "every stacking" open. The Window Law (#84, Main Theorem (c)) says a count fixed by g
layers comes down to g - 1 layers exactly when its Swap defects
    Delta_v(F) = F(cvc) + F(hvh) - F(cvh) - F(hvc),   |v| = g - 2,
vanish. For g = 3 the law (a straight line in h) needs three numbers to vanish: Delta_c and Delta_h (three layers -> two), then the
Swap defect of the pair count that remains (two -> one). Question: does the M0 table on the three-layer window obey this three-layer
Swap Rule exactly, as an identity in lam, in every window of lam; and does the law hold or fail exactly where it does?

## Plan
1. Read the exact weight walks of #64 (run 2, studies/2026-10-27-splash-rules/run2/raw/lvw_*.json: 15 stackings up to 8 layers + 3
   Fibonacci approximants of 15, 16, 26 layers; #57's census engine, census checks must all have passed).
2. Locality: for every lam-window and role, find the shortest window of layer types (length g = 1..4, every offset round the gap)
   that fixes the exact piece volume with no clash on any stacking; record which windows of three types occur.
3. Build the table F(xyz) on the 8 three-layer words; compute exactly Delta_c, Delta_h, the remaining pair defect Delta(P), and, as
   an independent cross-check, the three short-cycle sums (stackings with c/h words ch, cch, chh) that must vanish for the line.
4. Compare prediction with observation on every stacking: the law holds on all stackings of the set iff all three defects vanish.
5. Controls. Positive: the five other Laves roles (two-layer, the law proved in #66) and M0 below 17/96 must give zero defects and the
   law; generic tables of the form one-letter + coboundary must pass on all c/h words up to 12 layers. Negative: counts made from the
   real M0 and M1 volumes restricted to one kind of window (e.g. M0 only where the window reads chc; M1 only in mixed gaps) must
   have non-zero defects and fail the line on a tested stacking; random integer tables must fail exactly when a defect is non-zero
   (all c/h words up to 12 layers).
6. Compute only on the compute machine (dbbjob, 6 GB cage, 2 cores), pilot (words up to 6 layers) first, then the full set.

What will NOT be claimed: that M0 is fixed by its three-layer window in EVERY stacking. That is a locality statement (the M0 power
cell sees no layer beyond the six round its gap), found with no clash on the computed stackings (#64) but not proved; it is a LEAD.

## Result (law3 full run on the compute machine, FINAL ok, 12 Nov 2026; out/law3_full.log, out/law3_full.json; pilot out/law3_pilot.*)
- Data: the 18 Laves walks of #64 run 2 (15 stackings up to 8 layers + Fibonacci approximants of 15, 16 and 26 layers; census
  checks all passed). Five lam-windows: (-11/32, -5/32), (-5/32, 17/96), (17/96, 7/32), (7/32, 9/32), (9/32, 11/32).
- Locality, shortest window of layer types with no clash on any of the 18 stackings (gap k between layers k and k+1):
  M0 (big atom at height 0 of gap k, i.e. in layer k): constant below 17/96 (one type, any position); (17/96, 7/32) the type of layer
  k-1 ONLY; above 7/32 the pair (layer k-1, layer k), and no other position of the pair works. #64 keyed M0 to the pair
  (layer k, layer k+1) and found clashes, hence "reads three layer types"; the third type was never needed.
  All 16 six-layer neighbourhoods of a gap (mirror-merged) occur in the data, so the table covers every neighbourhood.
- Defects (exact polynomials in lam): Delta_c = Delta_h = 0 and the remaining pair defect = 0 for every role in every window;
  cross-check: the three short-cycle sums (c/h words ch, cch, chh) vanish too. M0 tables: (17/96, 7/32) F = V_c for layer k-1 cubic,
  V_h for hexagonal; (7/32, 9/32) and (9/32, 11/32) four distinct values with F(cc) + F(hh) = F(ch) + F(hc) (out/law3_full.json).
- Law tested directly: every role, every window, 16 non-pure stackings each = 480 exact tests, all on the line (M0: 80), including
  the three Fibonacci approximants, new beyond #67's 390. Prediction (defects zero) = observation in 30 of 30 role-windows.
- Controls. Positive: the five other roles and M0 below 17/96 (two-layer pieces, #66) zero defects and the law, 30/30; the theorem on
  all 801 cyclic c/h words up to 12 layers: prediction = observation in 600/600 tables, one-letter + coboundary tables on the line
  200/200. Negative: M0 counted only where its window reads chc, M1 counted only in mixed gaps: non-zero defects and off the line, 10/10;
  lifted pair counts with a Swap defect off the line 190/190 (the other 10 random draws had defect 0).

What is proved: (i) for any count fixed by three layer types, the line in h on every stacking <=> the three defects vanish (#84 (c)
twice; checked combinatorially here); (ii) M0's table, exact on all 16 six-layer neighbourhoods, depends on two layers and obeys the
Swap Rule, so under locality M0 is on the line on every stacking (#66). Not proved: the locality itself (that the M0 power cell
reads no layer beyond the six round its gap) - the same status as the other five Laves roles.

## LEADS
1. Locality certificate for the Laves net, all six roles: exact Farkas certificates as in #61 step 2 (splash-rules/proof/locality.py)
   that no site outside the six layers round a gap cuts the M0 cell, per lam-window; that would make the law for the Laves phases a
   theorem on every stacking.
2. Errata: #66 (end of §3) and #67 (§5) call M0 "the piece the proof does not cover"; the next versions can say it is a two-layer piece
   of its own layer and the layer below, with the Swap Rule exact, and cite this study (DICTO decides the version).
3. Why the layer below: between 17/96 and 7/32 the M0 piece sees only layer k-1; a picture of the M0 cell in C14 and C15 in this
   window would show which faces come from the gap below.
