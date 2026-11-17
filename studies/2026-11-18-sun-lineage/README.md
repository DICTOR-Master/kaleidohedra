# Sun: net change of neighbours between granule lineages (18 Nov 2026)

DICTO, 18 Nov 2026: "yes do the lineage count". Follows LEADS 2 of studies/2026-11-18-sun-net-vs-d and LEADS 2 of
studies/2026-11-18-sun-net-change (aim "geometry gives laws": a natural rung of the scutoid ladder would be a number that is the
same across settings, specific to the real time order, and has a null value).

## Question

The Sun's net neighbour change per SURVIVING granule after a time tau is frame-rate free and, plotted against the survivors' rms
displacement D, the 16 settings come within 15% of one curve (D = 0.20 to 0.45). But its ratio to the moving-Voronoi null falls
from 0.73 to 0.60 over that range. Suspected cause: the survivor rule drops every contact with a cell that died or was born, and
that loss grows with time; the null has no births or deaths.

1. Counted between granule LINEAGES (a split's daughters and a merged cell carry their ancestors' contacts), so that births and
   deaths no longer drop contacts, do the 16 settings still fall onto one curve against D?
2. Against a moving-Voronoi null WITH births and deaths at the Sun's measured rates, counted the same way, is Sun / null a single
   number over D (within 10%)?
3. Is the lineage count specific to the real time order (shuffled frames, test fixed below)?

## Definition

Tracking, unchanged: tiles.match of the 15 Nov study (imported from studies/2026-11-17-sun-step-zero/scripts), mutual best
overlap between consecutive sampled frames at step s. For one transition, old map P (tracked labels) to new map Q:
- best_par(n) = the old label with the largest pixel overlap with new cell n; best_heir(o) = the new label with the largest
  overlap with old cell o (the two quantities tiles.match itself uses, ties broken the same way).
- **Ancestor links** A(n) = {best_par(n)} plus every old cell o that is nobody's best_par and whose best_heir is n.
  So a split gives the parent two descendants; a merger gives the merged cell both ancestors; a cell that keeps its label is
  linked to itself. Every old cell has at least one descendant and every new cell at least one ancestor.
- Composed over the transitions from t to t + tau: anc(c) = the start cells (at t) from which end cell c (at t + tau) descends.
  The **lineage** of start cell a is the set of end cells c with a in anc(c).
- **Lineage contacts at t + tau:** the pairs of start cells (a, b), a != b, such that some end cell of a's lineage touches some end
  cell of b's lineage, or one end cell descends from both (they fused). E0 = contact pairs at t (all cells).
- **Lineage net change per cell** = (|E0 minus lineage contacts| + |lineage contacts minus E0|) / N0, N0 = cells at t;
  pooled over starts as sum of counts / sum of N0 (the parent's pooling).
- **Reduces to the parent's definition:** if no cell is born or dies between t and t + tau (every transition a one-to-one mutual
  match), then anc(c) = {c}, the lineage contacts are the contact pairs at t + tau, every cell survives, and the count equals the
  parent's net(tau) = (survivor pairs lost + made) / survivors, and the null study's (net_lost + net_made) / N. Checked in code on
  a synthetic case and on the zero-rate null.
- D (the x-axis) is the parent's: rms periodic centroid displacement of survivors over tau, in spacings l = (box area / mean
  cells)^(1/2). The survivor counts and D are recomputed here and must equal the parent's stored rows.

## Null with births and deaths (moving.py of studies/2026-11-15-tissue-null-models, extended)

N = 20 000 periodic 2D Poisson-Voronoi seeds (contacts = Delaunay edges, nulllib.edge_keys, as moving.py), time in steps of 10 s
up to 640 s:
- **Motion, matched to each setting:** every seed moves by an independent Gaussian step each 10 s; the variance of the steps
  follows D^2(t), linear between (0, 0) and the Sun's survivor D at tau = 80, 160, ..., 640 s (that setting, step 10 s), so the
  null's survivors reach the same D at the same tau. l = N^(-1/2).
- **Rates, per setting:** births at the census rate of persistent splits, deaths at the census rate of persistent merges, per
  cell per minute at step 10 s (studies/2026-11-15-sun-granulation/results/census, step 1, rate_per_cell_per_min), drawn as
  Poisson numbers each 10 s (deaths first, then births).
- **Lineage rule:** a new seed is placed uniformly at random; its parent is the nearest alive seed (the cell it is born in). A
  dying seed is chosen uniformly among the alive ones; its heir is the nearest remaining alive seed. anc(new) = anc(parent);
  anc(heir) gains anc(dead). The lineage net change is then counted exactly as for the Sun.
- 4 repetitions per setting (seeds 18100 + 10 x setting index + repetition).
- Reported variants (not judged): (V1) **matched survival**: births = deaths = -ln(s)/320 s per cell, s = the Sun's survivor share
  at tau = 320 s (step 10 s), so the null loses identities as fast as the tracking does; (V2) **split births**: the daughter is
  placed at its parent's seed plus 0.25 l in a random direction (a split rather than a birth anywhere in the cell).
- **Calibration:** zero birth and death rates, D^2 linear up to 1.0 at the end, outputs at D = 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 4
  repetitions: the lineage count must equal the plain count in every run, and give 3.600 +- 0.02 at D = 1.0 (parent 3.602 +- 0.008).

## Plan (written 18 Nov 2026 BEFORE the pilot and the runs)

- **Data, unchanged:** the 16 settings of studies/2026-11-18-sun-net-change (scripts/settings.txt copied), same frames, steps
  10 s (judged) and 80 s (reported), tau = 80, 160, 240, 320, 480, 640 s, starts every 80 s (the parent's starts).
- **Shuffled frames:** the 17 Nov permutation (seed 7), regenerated by the parent's prep_order.py; step 10 s.

Criteria (step 10 s):
- **A. Collapse** (the rule of studies/2026-11-18-sun-net-vs-d, applied to the lineage net change): each setting's broken line
  through its six (D, lineage net) points, interpolated on D = 0.20, 0.25, ..., 0.50 (no extrapolation), a grid D judged where at
  least 12 of 16 settings cover it. **Collapse: yes** if at every judged D every covering setting is within +-15% of the median,
  and the largest spread at matched D is below the largest spread at matched tau (over the taus whose median D lies in the judged
  range).
- **B. Single number:** ratio R = Sun lineage net / null lineage net, each setting against its own null (its rates and its D(tau)),
  both interpolated on the grid. **Single number: yes** if (i) the median R over the judged D varies by at most 10%
  (largest / smallest - 1 <= 0.10) and (ii) at every judged D every covering setting is within +-15% of that D's median R.
- **C. Specificity, fixed now:** at every tau 80 to 640 s, the real lineage net change is at most 1/2 of the shuffled one (step
  10 s, per start cell). **Specific** if this holds in at least 13 of 16 settings.
- **Candidate rung (computed, not proved)** only if A, B and C all hold. Otherwise NOT CONFIRMED.
- Reported, not judged: step 80 s against 10 s; Sun lineage net against the parent's null without births; variants V1 and V2;
  the survivor share of the null against the Sun's; mean lineage size (end cells per start cell) and fused pairs; the share of
  start contacts lost (|E0 minus lineage contacts| / |E0|) against the null's.

Checks (FINAL ok only if all pass): survivors, survivor pairs lost and made, and d2 at steps 10 and 80 s equal the parent's stored
rows (real, 16 settings; shuffled at 10 s); the identity case of the lineage count equals the plain count (synthetic test); the
zero-rate null: lineage = plain in every run and 3.600 +- 0.02 at D = 1.0; every null configuration has 3 x (alive seeds)
contacts; every start cell has a descendant and every end cell an ancestor.

Prediction (before the pilot): the lineage count is larger than the survivor count per cell at the same tau (contacts made with
daughters now count, and lost contacts with dying cells are kept through heirs only when the heir touches), and Sun / null with
births falls less with D than 0.73 to 0.60, because the null now loses identities too. Whether it stays within 10% is open: the
10 s tracking flickers (231 of 991 splits undone at once in the primary setting), and a flicker can join two lineages that the
null, with no flicker, never joins. The shuffled frames join lineages at random, so their lineage net change should be several
times the real one (C passes).

Jobs: on the compute machine where the Bifrost planes live, foreground stages of under 5 minutes; nothing in the background.
Stages (scripts/jobs.sh): pilot, gen, real, shuf, null, fit.
- **Deviations from the plan, recorded:** (1) The null check "every configuration has exactly 3 x (alive seeds) contacts" failed
  in 4 of 1176 configurations, each by one contact (3N + 1: a nearly cocircular quadrilateral split by different diagonals in two
  periodic copies of the replicated Delaunay). The check was replaced by "within 1 of 3N", which holds in all 1176. The effect on
  the net change is at most 2 pairs in 20 000 cells (0.0001 per cell). (2) Two diagnostics were added to lin_fit.py before it
  ran but are not in the plan, and are reported only: the parent's survivor ratio, and the same survivor rule applied to the null
  with births and deaths. (3) The regenerated shuffled arrays (1.2 GB) were deleted after the run; `jobs.sh gen` rebuilds them.

## Result (jobs pilot, real, gen, shuf, null: FINAL ok; lin_fit.py: FINAL ok, 9 checks, 0 failed)

**VERDICT: NOT CONFIRMED as a natural rung (computed).** One of the three planned tests passes and two fail:
- specificity: passes in 16 of 16 settings;
- collapse: fails, with a spread of 51 to 73% at matched D;
- single number: fails, because Sun / null with births rises from 0.95 to 1.26 over D = 0.20 to 0.45 (32%).

The lineage count is mostly a count of lineages SPREADING, not of neighbours exchanged. The Sun's lineages spread faster than the
null's, by an amount that depends on the segmentation.

Pilot (primary setting, 80 snapshots, 12 s; FINAL ok): at tau = 80 s the lineage net change per cell was 1.12, against 0.54 per
survivor for the parent's count. The null with births gave 1.35. The survivor columns equalled the parent's rows.

Checks (exact or within the stated tolerance):
- Survivors, survivor pairs lost and made, d2 and rel2: every row (real at 10 and 80 s, shuffled at 10 s; 16 settings) equals
  the parent's stored row. So the tracking is the parent's, unchanged.
- D and the survivor net change equal the parent's summary.json to 1e-9.
- The identity case of the lineage count equals the plain count (synthetic test).
- Zero-rate null: lineage count = plain count in every run. At D = 1.0 it gives **3.605 +- 0.004** against 3.600 (parent
  3.602 +- 0.008).
- Every start cell has a descendant and every end cell an ancestor, in every Sun transition and every null configuration.
- Null contacts within 1 of 3N in all 1176 configurations (deviation 1).

Results (step 10 s):
1. **Made pairs carry the count (computed).** At tau = 320 s:
   - per start cell, lineages lose 0.11 to 0.31 of their start contacts but make 2.8 to 5.9 new ones;
   - a start cell's lineage holds 1.59 to 2.65 end cells (null with births: 1.38 to 1.58);
   - the share of start contacts lost between lineages is 0.02 to 0.11 over all settings and tau (null: 0.14 to 0.28).
   A merger joins two lineages, so the joined lineage touches the neighbours of both. A split's daughter carries its parent's
   lineage into new contacts. So after a few hundred seconds the count is ruled by how far lineages have grown, not by exchanges.
2. **No collapse against D (computed).** At D = 0.20 to 0.45 (13 to 16 settings) the largest deviation from the median is 51,
   55, 55, 57, 64 and 73%. At matched tau it is 29% at 80 s and 30, 45, 55 and 72% at 160 to 480 s.
   - The survivor count of the parent collapsed within 14%; the lineage count does not.
   - Highest: qs thr 0 and en 0.2 Mm (14.3 per cell at 640 s), temperature thr 0.25 (10.1).
   - Lowest: en 0.0 Mm (5.7), en thr 0.5 (6.0).
   - en 0.2 Mm also has the highest census rates (0.108 splits and 0.110 merges per cell per minute). But the rates do not order
     the rest: qs h-maxima 600 has the lowest (0.070 and 0.074) and gives 8.65.
3. **Sun / null with births and deaths is not a single number (computed).** Each setting against its own null (its census rates,
   its D(tau)), median over settings (range):

   | D | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 | 0.45 |
   |---|---|---|---|---|---|---|
   | Sun / null with births (main) | 0.95 (0.84 to 1.27) | 1.06 (0.93 to 1.41) | 1.12 (1.00 to 1.55) | 1.17 (1.05 to 1.71) | 1.19 (1.09 to 1.90) | 1.26 (1.14 to 2.08) |
   | V1, matched survival (reported) | 0.89 | 0.97 | 1.01 | 1.06 | 1.11 | 1.15 |
   | V2, split births (reported) | 0.97 | 1.07 | 1.13 | 1.19 | 1.22 | 1.27 |
   | Sun / null without births (reported) | 1.56 | 1.76 | 2.00 | 2.25 | 2.46 | 2.64 |

   - The median varies by 32% (limit 10%), and the settings spread up to 66% from the median.
   - The ratio now RISES with D, where the survivor count's ratio fell (0.73 to 0.60).
   - The null's lineage rule and its kind of birth hardly matter: V2 is within 0.03 of main, and V1 lowers it by 0.06 to 0.11.
4. **Specific to the time order (computed; passes as fixed).** Real lineage net is 0.06 to 0.18 of the shuffled one at every
   tau, in 16 of 16 settings.
   - Shuffled frames give 12.8 to 223 per cell: random matches join lineages across the whole box.
   - The test passes by a wide margin and says only that the real lineages are not random.
5. **Not frame-rate free (computed, reported).** Step 80 s gives 5 to 16% less than 10 s at tau = 80 s, 4 to 25% less up to
   320 s, and up to 35.5% less at 640 s. Coarser steps see fewer brief splits and mergers, so lineages join less often. The
   parent's survivor count moved by 4.9% or less up to 320 s.
6. **The survivor rule on the null (after the plan, reported only).** The null with births and deaths, counted by the parent's
   survivor rule against the null without births, gives medians 1.15, 1.05, 0.94, 0.83, 0.71 and 0.62 at D = 0.20 to 0.45. The Sun gave
   0.73 to 0.60 by the same rule.
   - So at the Sun's birth and death rates, the survivor rule alone makes the ratio fall with D, and by more than the Sun's fall.
   - This supports the suspected cause of the parent's fall. It does not give a single ratio: the ratio of the two medians runs
     from 0.63 to 0.97.

Conclusion: NOT CONFIRMED.
- Counting between lineages removes the survivor rule. But it puts in a quantity that grows with every split and merger the
  tracking sees, including brief ones.
- That quantity does not collapse over settings (51 to 73% spread at matched D) and depends on the step (up to 35.5%).
- Against a null with births and deaths at the Sun's census rates, its ratio rises from 0.95 to 1.26 with D. So it is not a
  single number.
- The fall of the parent's survivor ratio is of the size the survivor rule itself produces in a null with births and deaths
  (computed, after the plan).

Prediction against outcome: lineage count above the survivor count, as predicted. Ratio to the null with births no longer
falling, as predicted. But it rises instead of holding, and the spread over settings grew from 14% to 73%. C passed, as
predicted.

## LEADS

1. **Lineages from persistent events only.** Link lineages only through splits and mergers that the census counts as
   persistent (not undone within 60 s). If the excess lineage growth of the Sun over the null (1.59 to 2.65 against 1.38 to 1.58
   end cells per lineage at 320 s) is brief splits and mergers of the 10 s tracking, the spread over settings and the step
   dependence should both shrink. This is the direct test of item 5.
2. **The lost half alone.** The share of start contacts lost between lineages is small and changes slowly (0.02 to 0.11; the
   null's is 0.14 to 0.28). It does not grow with lineage size the way made pairs do. Whether its ratio to the null is one
   number over settings was not tested. It would need its own rule, fixed before the run.
3. **Same rule on both sides (survivor count).** Item 6 compares the Sun's survivor count with the null's survivor count under
   births and deaths. A planned test of that ratio (Sun survivor net / null-with-births survivor net, per setting, at matched D)
   would show whether the parent's survivor measure has a stable ratio once the null loses cells at the Sun's rates. The medians
   run from 0.63 to 0.97 here, so a single number is not expected. That has not been tested.

## Files

- scripts/lineage_lib.py: the lineage count (sparse matrices) and its identity test.
- scripts/lin_sun.py: segmentation and tracking (net_sz.py of the parent and tiles.py of the 15 Nov study, imported
  unchanged), ancestor links, lineage counts per start and tau; checks the survivor columns against the parent's rows.
- scripts/lin_null.py: the moving Poisson-Voronoi null with births and deaths (nulllib.py of
  studies/2026-11-15-tissue-null-models, moving.py's method), main, V1, V2 and calibration.
- scripts/lin_fit.py: tables, criteria, checks, figure. scripts/jobs.sh: stages pilot, gen, real, shuf, null, fit.
  scripts/settings.txt: the 16 settings (copied from the parent).
- data/lin/TAG.json, TAG-shuf.json: raw per-start rows (the raw data). data/null/TAG_VARIANT.json, calib_calib.json: null runs.
  data/lin_summary.json: every number of the tables.
- results/summary.md: all tables. results/lin_vs_d.png: lineage net against D for the 16 settings with each setting's null with
  births (grey) and the null without births (black); right: Sun / null with births against D, with the parent's survivor ratio.
  results/logs/, results/pilot/.

Credits: Bifrost (Gudiksen et al. 2011, A&A 531, A154); run en024048_hion of Carlsson, Hansteen, Gudiksen, Leenaarts and
De Pontieu 2016 (A&A 585, A4) and qs024048_by3363, Hinode Science Data Centre Europe. "Hinode is a Japanese mission developed and
launched by ISAS/JAXA, with NAOJ as domestic partner and NASA and STFC (UK) as international partners. It is operated by these
agencies in co-operation with ESA and NSC (Norway)." scikit-image (van der Walt et al. 2014). Qhull (Barber, Dobkin and Huhdanpaa
1996) through scipy.spatial for the null's Delaunay contacts and nearest-seed queries (cKDTree). Matplotlib (Hunter 2007).

DICTO: the question and the route. Computation, checks and drafting with Claude (Anthropic).
