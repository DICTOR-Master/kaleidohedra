# The Laves big atom on the three-layer window: the last exception of the Hexagonality Law (12 Nov 2026)
Gap row (Concordance gaps.ranked): "The Hexagonality Law for the Laves big atom (#66, #67)": "#84 shows the Swap Rule is the
condition to stay on the line; check it on the three-layer window"; goal: the last exception of the law explained.

**Conclusion:** the exception was a labelling shift, not a three-layer piece: the big atom M0 of gap k sits IN layer k, and its
piece is fixed by exactly TWO layer types, its own layer k and the layer below (k-1), on all 18 computed stackings and in every
lam-window (only the type of layer k-1 between 17/96 and 7/32). On that pair it obeys the Swap Rule as an identity in lam, so #66's
theorem covers it; the three-layer Swap defects (#84 (c), g = 3) are zero in every window. LOCALITY IS NOW PROVED (Part II below):
every Laves piece, all six roles, is fixed by the six layers round its gap, in every lam-window, by 253440 exact Farkas certificates,
each re-checked by an independent verifier. So the Hexagonality Law for the Laves phases, M0 included, is a theorem on every stacking.

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

## Part I. Result (law3 full run on the compute machine, FINAL ok, 12 Nov 2026; out/law3_full.log, out/law3_full.json; pilot out/law3_pilot.*)
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
Swap Rule, so under locality M0 is on the line on every stacking (#66). Locality was open after Part I; Part II proves it for all
six roles.

## Part II: locality certified (lavloc full run on the compute machine, FINAL ok, 12 Nov 2026; out/lavloc_full.log, out/lavloc_full.json, out/verify_full.log; pilot out/lavloc_pilot.*, out/verify_pilot.log)
Question (LEAD 1): does each Laves role's power cell read any layer beyond the six round its gap? Method of #61 step 2
(splash-rules/proof/locality.py), adapted (scripts/lavgeom.py, scripts/lavloc.py):
- Linearisation. The Laves net has the ideal spacing (layer spacing^2 = 2/3), so in z = (lam, x, y, zeta) every power-bisector
  condition pow_i <= pow_j is one linear inequality with a constant right side. A cell lifted over a closed lam-window is one convex
  polyhedron; one Farkas certificate (y >= 0, y^T M = c, y^T m <= beta, exact rationals) proves c.z <= beta for every lam of the window.
- Cases: 5 lam-windows (-11/32, -5/32), (-5/32, 17/96), (17/96, 7/32), (7/32, 9/32), (9/32, 11/32) x 6 roles (M0 M1 K1 K2 K3 T)
  x all 32 six-layer neighbourhoods (layers k-2 .. k+3; no symmetry used) = 960 cases.
- K = the cell of the role's site against every site fixed by those six layers (all sites of gaps k-2 .. k+2 and the five sites of
  gap k+3 over layer k+3). Certified per case: pow_i <= pow_j on K for every site j of gap k+3 (its single small atom, both choices of
  layer k+4), of gap k-3 (both choices of layer k-3) and of the supersets of gaps k+4 and k-4 (all six position pairs); and
  zeta <= 4, zeta >= -3 on K.
- Completeness. Lateral: the six same-level neighbours keep K within 1/sqrt3 of the site laterally, so at each level the nearest
  lattice point (within Q <= 4/3 of the site) dominates all others; the lists keep every point with Q <= 4/3. Vertical: a site of gap
  m >= k+5 is dominated by the same point at the same fraction in the gap k+4 superset when zeta < 4.5, and gap m <= k-5 by gap k-4
  when zeta > -3.625; both hold by the zeta certificates. So no site of any stacking cuts K, and each piece is a function of its
  six-layer neighbourhood alone.
- Result: 253440 certificates PASS, 0 FAIL, 0 unresolved (960 cases, 1495 s). VERDICT: local, every role, every window, every
  neighbourhood.
- Independent verification (scripts/verify_lavloc.py, no shared geometry code): site sets rebuilt from #64's net builder
  (run2/laves_net.py) on concrete periodic stackings, 16 continuations per neighbourhood; the certified rows must be sites fixed by
  the six layers, and every other site of gaps k-4 .. k+4 of every continuation must carry a certificate; each certificate re-checked
  in exact rationals from its site references with Gram-matrix rows. Result: 253440 of 253440 certificates re-checked ok, 0 bad; coverage 15360 of 15360 (case, continuation) pairs ok; FINAL ok.
- Controls. (C1) #61 step 2 reproduced by its own script: 1070 PASS, 0 FAIL (as published). (C2) negative: the M0 cell against only
  FOUR layers (k-1 .. k+2) is not local: in (17/96, 7/32) and (7/32, 9/32), on 4 neighbourhoods each, an exact cut by the big atom M1
  of gap k-2 over the other choice of layer k-2 (8/8 cases); witness (lam, x, y, zeta) = (7/32, 0, 0, -27/40) and (9/32, 0, 0, -3/4),
  in K and strictly nearer in power to that site. (C3) model cell = census engine (#64 raw walks) on ABC and AC at each window's
  midpoint: face counts 60/60, volume ratio model/engine one constant per stacking (3/sqrt2 and sqrt2, the per-layer normalisation;
  spread < 3e-15). Checker control: a tampered certificate is rejected.
- With Part I: each Laves piece is a function of its six-layer neighbourhood (proved here); the tables on all 16 neighbourhoods
  (mirror-merged; all occur in the 18 walks) depend on two layer types and obey the Swap Rule (Part I); so by #66's theorem every
  Laves role, M0 included, is on the line n_c F(c, c) + n_h F(h, h) on every stacking, periodic or not, in every lam-window.
- Certificates: out/lavloc_full_certs.jsonl.gz (3 MB, every certificate with its site references), checked by verify_lavloc.py full.

## Erratum wording for #66 and #67 (note only; DICTO decides the versions, the papers are not edited)
- #66 (The Focus), end of §3, replace "The theorem's hypothesis, that a piece is fixed by its two neighbouring layers, was checked
  in #64 for every role except the Laves foot atom above λ = 17/96, which reads three layer types. For that role the law holds in every
  test above, but the proof does not apply: it is an open problem whether it holds for every stacking." by: "The theorem's hypothesis
  holds for every Laves role. The foot atom M0 sits in the lower layer of its gap; above λ = 17/96 its piece is fixed by the types of
  that layer and the layer below (#64 keyed it to the layer above, hence 'three layer types'), and on that pair it obeys the Swap Rule
  exactly. Every Laves piece is fixed by the six layers round its gap (exact Farkas certificates, every window of λ). So the law holds
  for the Laves phases, M0 included, on every stacking."
- #67 (Random Stackings and Stacking Faults), §5 first sentence, replace "In the Laves phases (#64) the foot atom, the big atom M0,
  reads three layer types above λ = 17/96, so the proof does not apply to it; #66 found the law exact for it on every stacking up to
  six layers and left it as an open problem." by: "In the Laves phases (#64) the foot atom M0 was said to read three layer types above
  λ = 17/96; it reads two, its own layer and the layer below, obeys the Swap Rule on them, and every Laves piece is local (exact
  certificates), so the theorem covers it." The Result box (390 of 390) can stay as a check; the abstract's "every role computed except
  the Laves foot atom" becomes "every role".
- Both cite this study (studies/2026-11-12-laves-three-layer-swap, Parts I and II). #69 (Fibonacci Stacking) §4 has the same sentence ("The
  Laves foot atom M0 reads three layers above λ = 17/96, where the law is not proved"); the same correction applies there.

## LEADS
1. DONE 12 Nov 2026 (Part II): locality certificate for the Laves net, all six roles: exact Farkas certificates as in #61 step 2 (splash-rules/proof/locality.py)
   that no site outside the six layers round a gap cuts the M0 cell, per lam-window; that would make the law for the Laves phases a
   theorem on every stacking.
2. Errata: #66 (end of §3) and #67 (§5) call M0 "the piece the proof does not cover"; the next versions can say it is a two-layer piece
   of its own layer and the layer below, with the Swap Rule exact, and cite this study (DICTO decides the version).
3. Why the layer below: between 17/96 and 7/32 the M0 piece sees only layer k-1; a picture of the M0 cell in C14 and C15 in this
   window would show which faces come from the gap below.
