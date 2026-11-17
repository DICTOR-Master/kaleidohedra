# Sun: the granule swap rate at time step 0 (17 Nov 2026)

DICTO reopened one route of the shelved scutoid study (17 Nov 2026): the Sun's swap rate extrapolated to time step 0 with the
control's efficiency (open item 3 of studies/2026-11-16-scutoid-interactions; serves the aim "geometry gives laws": a natural rung
of the scutoid ladder would be a swap rate that is stable and comparable across scales).

## Question

Does the granule swap rate per cell per unit time converge to a stable value as the time step, and with it the persistence window,
go to 0, once each step's count is corrected by the detection efficiency measured on the moving-Voronoi control at the same step and
window? If it converges: the value with an honest uncertainty and its ratio to the null model (moving Poisson-Voronoi, 3.04 ± 0.005
T1 per cell per spacing of rms seed displacement in 2D). If not: the clean negative and what blocks it.

## What was already done, and what is new here

Ledger (Concordance, 16 Nov, studies/2026-11-15-sun-granulation section "Swap rate at step 0"): COMPUTED, NOT CONFIRMED. With
the persistence window P held FIXED (20 to 240 s) and the step taken to 0 by a line, the corrected rate still fell 36 to 66% from
step 0 to 80 s and its step-0 value moved with P by up to 30%; shuffled frames gave as many swap patterns as real frames at 10 s.
Retry rule there: "not with the moving-Voronoi calibration alone; next only with ... a continuity rule (all four cells matched above
a fixed overlap share) that shuffled frames must fail". This study keeps the moving-Voronoi calibration DICTO named and adds what
was not tried:
1. **The joint limit.** P tied to the step (P = k x step, k = 1, 2, 3) and P = 0 (no persistence), so step and window go to 0
   together, beside the fixed windows of 16 Nov (P = 30, 60, 120 s).
2. **The continuity rule** of the ledger's retry rule: each swap carries the smallest frame-to-frame overlap share (overlap / union
   of the same label in the two frames) of its four cells; a swap counts at share threshold theta only if all four cells reach it.
   The control's efficiency is measured at the same step, window and theta.
3. **A false-swap floor** from shuffled frames for EVERY setting (16 Nov had the primary setting only), and a floor-subtracted fit.
4. **Hold-out by extrapolation**: the line through steps 20 to 80 s must predict the corrected rate at 10 s.
5. **A cell speed** (apparent rms centroid speed of kept cells), so that a converged rate can be put in the null model's units;
   the speed estimator is checked on the control, whose seed speeds are known exactly.

The time step cannot go below 10 s: the simulation's snapshots are 10 s apart. Convergence can therefore only be judged on steps 10
to 80 s and by extrapolation; the criteria below say what counts.

## Plan (written 17 Nov 2026 BEFORE the pilot and the runs)

- **Data, unchanged.** Bifrost en024048_hion (242 snapshots, 10 s, 40 min) and qs024048_by3363 (101 snapshots, 17 min), the
  planes fetched for the 15 Nov study; the 13 main settings of 16 Nov (en uz 0.1 Mm: thr 0, 0.25, 0.5, hmax 300, 600, 1200, smoothing
  3; en temperature at tau = 1: thr 0.25, hmax 300 K; qs uz 0.1 Mm: thr 0, 0.25, 0.5, hmax 600). Steps 10, 20, 30, 40, 60, 80 s.
  The two-step pairing window stays 60 s (census rule).
- **Chain.** census_sz.py = census.py of the 15 Nov study plus two outputs (the full swap list with times and shares; centroid
  displacements); every count of 16 Nov must reproduce exactly (primary setting 733, 626, 484, 305 at 10, 20, 40, 80 s, P = 60 s,
  theta = 0). Persistence is applied afterwards to the swap list with the census rule (persistent = elementary - 2 x swaps undone by
  the same four cells within P); at P = 60 s it must equal census.py's own count at every step and setting.
- **Windows.** Fixed: P = 30, 60, 120 s. Tied: P = 1, 2, 3 x step. None: P = 0 (elementary count). For the control, the exact
  persistent count at any (step, P) is Delaunay pairs lost between sampled frames minus twice those regained at a sampled frame
  within P (the 16 Nov rule).
- **Continuity threshold.** theta = 0 (all swaps) and theta* = the smallest of 0.3, 0.4, 0.5, 0.6, 0.7 at which the primary
  setting's shuffled count at 10 s (P = 2 x step) is at most 1/3 of its real count; chosen on the primary setting only, then applied
  to all 13. If no theta reaches it, the continuity variant is reported as failing.
- **Correction.** f(step, P, theta) = pipeline / exact persistent swaps on the seed-1 control at speed 1 (Sun-like, about 0.10 swaps
  per cell per minute), texture 0 and 1, mean of the two; half their difference is the calibration band. Corrected rate
  y(step) = rate / f. Speed 2 is a sensitivity only.
- **Fit models** (per setting, window family and theta): line through all six steps (main); parabola; short line through 10 to
  40 s; floor-subtracted line, y_fs = (real - shuffled) / f per cell-minute (shuffled frames as an upper bound on false swaps).
  Uncertainty u of the step-0 value: line standard error, line against parabola, half the calibration band, and the held-out
  control's measured calibration error at that window family, in quadrature.
- **Convergence criteria per setting** (all must pass):
  C1 plateau: the short line (10 to 40 s) changes by at most 10% from step 0 to 30 s;
  C2 models: line, parabola and short line agree within u;
  C3 windows: the step-0 values of the six window families agree pairwise within their combined u;
  C4 hold-out: the line through 20 to 80 s predicts y(10 s) within u;
  C5 specificity: at 10 s the shuffled count is at most 1/3 of the real count, or the floor-subtracted step-0 value agrees with the
  plain one within u.
  **Converges** if C1 to C5 pass in at least 10 of 13 settings (at theta = 0 or at theta*) AND the held-out control (seed 2,
  speed 1, texture 0 and 1, corrected with seed-1 fractions) recovers its exact step-0 rate within 15% in the tied family k = 2.
  Then: value = median over settings with the spread and the median u; dimensionless rate = rate x spacing / rms cell speed, against
  3.04 (spacing = (box area / mean cells)^(1/2)).
- **Cell speed.** Mean square centroid displacement of kept cells between sampled frames, d2(step); d2 = v^2 step^2 + j^2 (jitter j)
  fitted over 10 to 40 s gives v. On the control the same estimator is compared with the exact rms seed speed (from the seed paths);
  on the control the exact elementary rate per cell per spacing of rms displacement is also compared with 3.04 (its seeds move on
  smooth, locally linear paths), as a check of the unit conversion.
- **Controls with expected outcome.** (1) reproduction of 16 Nov (exact); (2) seed-2 regenerated sequences reproduce their 16 Nov
  exact totals (exact); (3) held-out control, as above; (4) shuffled frames for all 13 settings and for the control (speed 1,
  texture 0): at theta* the control's real count must keep at least 80% of its swaps (the continuity rule must not throw out real
  swaps of a clean tiling).
- **Prediction** (from 16 Nov): at theta = 0 the corrected rate still rises toward small steps (C1 fails), the tied windows give
  larger step-0 values than the fixed ones as P goes to 0 with the step, because back-and-forth swaps are no longer removed (C3
  fails), and shuffled frames fail C5. Whether a continuity threshold separates real from unrelated frames without removing most real
  swaps is open. Expected verdict: NOT CONFIRMED, unless theta* changes the picture.
- **Jobs** (compute machine, foreground chunks under 10 minutes): sz-pilot (primary setting and one control, 40 frames), sz-a
  (seed-2 sequences, shuffled copies, 13 Sun settings real, 4 seed-1 controls), sz-b (13 Sun settings shuffled, 4 held-out controls,
  1 control shuffled); fit by fit_sz.py.
- **Deviation from the plan, recorded:** none in the method. The jobs ran as foreground stages of under 5 minutes each (sz-a in
  two stages: gen, census); the 1.2 GB of regenerated image arrays (seed-2 sequences, shuffled copies) were deleted after the run
  and are rebuilt by `sz_a.sh gen`.

## Result (jobs sz-pilot, sz-a, sz-b: FINAL ok; fit_sz.py: FINAL ok)

**VERDICT: NOT CONFIRMED. The corrected Sun swap rate does not converge as the step and the window go to 0.** It passes the
criteria C1 to C5 in 0 of 13 settings, at theta = 0 and at theta* = 0.5 alike, and the held-out control fails at the tied window
k = 2. What is stable is the order of magnitude: the step-0 line gives a median of 0.11 to 0.13 persistent swaps per cell per
minute over the six judged windows (0.07 to 0.17 over settings and windows), as on 16 Nov. That is an extrapolation of a falling
line, not a plateau, and it is not quoted as a rate.

Reproduction (exact):
- Every 16 Nov count is reproduced: 13 settings x 6 steps x 5 windows, the primary setting 733, 626, 484, 305 at 10, 20, 40, 80 s,
  its shuffled count 767 at 10 s, and the four seed-1 controls.
- The swap-list rule gives census.py's own persistent count at every step, window and setting.
- The regenerated seed-2 sequences give their 16 Nov exact totals (1164, 1164, 2300, 2300).

Results:
1. **The joint limit is blocked by the calibration (computed).** As the window shrinks with the step, the control's detection
   efficiency stops being a correction and starts measuring the pipeline's own flicker on textured boundaries. At 10 s the
   Sun-like f is 3.35 with no persistence, 1.51 at P = step and 1.17 at P = 2 x step, against 1.01 at P = 60 s; at 80 s it is 0.57
   to 0.69 in every window.
   The correction does not carry over to a second realisation of the same motion. The seed-2 step-0 value, divided by its exact
   value (speed 1, texture 0 and 1), is 0.28 and 1.37 with no persistence, 0.65 and 1.14 at P = step, 0.78 and 1.04 at P = 2 x step
   (criterion 15%: FAIL), 0.85 and 1.00 at P = 3 x step, and 0.88 and 0.94 at P = 60 s.
   So the step-0 value in the tied windows carries a calibration error of 15 to 35%, and with no persistence of about 70%.
2. **No plateau at the smallest steps (C1, computed).** Between 10 and 30 s the corrected rate still rises toward step 0. The short
   line (10 to 40 s) changes by a median of -11% (k = 2) and -15% (P = 60 s) from step 0 to 30 s, against the 10% allowed. From 0
   to 80 s the full line falls 36 to 68% (k = 2) and 36 to 66% (P = 60 s).
   C1 holds in all six windows in 0 of 13 settings; window by window, in 0 to 9 of 13.
3. **The windows agree, but only inside wide errors (C2 to C4, computed).** The step-0 medians at theta = 0 are k = 1: 0.108,
   k = 2: 0.123, k = 3: 0.130, P = 30 s: 0.117, P = 60 s: 0.129, P = 120 s: 0.118 (no persistence: 0.065). They agree within u, and
   so do line, parabola and short line, and the hold-out prediction of the 10 s value. All three criteria pass in 13 of 13
   settings. They pass because u is wide (median 17% at P = 60 s, 26% at k = 2, 45% at k = 1), mostly from the held-out calibration
   error. They do not show that the value is tight.
4. **The continuity rule separates real frames from unrelated ones at 10 s, but does not make the rate step-stable (computed).**
   On the primary setting at 10 s (P = 20 s), requiring all four cells of a swap to keep an overlap share of at least theta gives:

   | theta | real | shuffled | shuffled / real |
   |---|---|---|---|
   | 0 | 785 | 771 | 0.98 |
   | 0.3 | 785 | 608 | 0.77 |
   | 0.4 | 785 | 379 | 0.48 |
   | 0.5 | 780 | 240 | 0.31 |
   | 0.6 | 767 | 149 | 0.19 |
   | 0.7 | 743 | 82 | 0.11 |

   At theta* = 0.5, real frames keep 98.5 to 99.8% of their 10 s swaps in every setting, and the control keeps all of its swaps.
   Shuffled frames fall to 0.15 to 0.32 of the real count in the 8 settings of the en run with smoothing 1.5. They fall only to
   0.39 to 0.45 in the quiet-Sun run and with smoothing 3 (C5 at k = 2: 8 of 13).
   So the 16 Nov worry that the 10 s swaps might be matching errors is answered for the en run at smoothing 1.5: those swaps are
   made of cells that stay well matched, and unrelated frames mostly are not.
   But the rule removes more real swaps at coarse steps (the median share falls from 0.98 at 10 s to 0.82 at 80 s on the primary
   setting), so the corrected fall from 0 to 80 s steepens. At k = 2 the median goes from -46% to -61%.
5. **The comparison with the null model is not like for like (computed, NOT CONFIRMED).** The cell centroids move between
   diffusion and straight-line motion: their mean square displacement grows as step^0.70 to step^0.88 over 10 to 40 s, where
   straight-line motion would give step^2.
   On that reading the apparent rms speed is 0.057 to 0.074 pixels per second (2.7 to 3.5 km/s, with a jitter of 1.6 to 2.3
   pixels) at a cell spacing of 24 to 39 pixels (1.1 to 1.8 Mm). The step-0 rate (k = 2) is then 0.68 to 1.18 swaps per cell per
   spacing of rms displacement, that is 0.22 to 0.39 of the null 3.04.
   Three things stop this from being a rung:
   - the rate has not converged;
   - the speed estimator reads 0.96 to 1.50 of the true seed speed on the control;
   - the null assumes straight-line seed motion, which the granule centroids do not follow.
   Units check on the control (computed): its exact count is 2.74 to 2.85 T1 per cell per spacing of rms displacement against
   3.04. Its seeds move on smooth curved paths, not straight lines.

Conclusion: NOT CONFIRMED. Taking the step and the window to 0 together, with the moving-Voronoi efficiency measured at the same
step, window and continuity threshold, does not give a converged Sun swap rate.
- **The value is not stable at the smallest steps.** The corrected rate still rises toward step 0 below 30 s.
- **The calibration breaks as the window shrinks.** The control's efficiency then measures its own flicker and does not carry over
  to a second realisation (errors of 15 to 70%).
- **The sampling sets a floor.** The steps cannot go below the simulation's 10 s.
- **Order of magnitude.** The step-0 extrapolation stays at 0.11 to 0.13 per cell per minute (median over settings), about 0.2 to
  0.4 of the null rate in its units. That is not a natural rung.

What is new and holds: the continuity rule at share 0.5 keeps 99% of the real 10 s swaps and removes 68 to 85% of the swaps found in
unrelated frames in the en run at smoothing 1.5 (computed). And the granule centroids do not move in straight lines (msd exponent
0.70 to 0.88, computed).

## LEADS

1. **Measure the net neighbour change over a fixed time instead of a rate (outside this route).** The null-model study found that
   with diffusive seed motion, counts per unit time grow as the frame interval shrinks. There, only the net change of contacts
   after a fixed displacement does not depend on the frame rate (3.600 per cell per spacing after one spacing in 2D, for straight
   and diffusive motion alike).
   The granule centroids here move closer to diffusion than to straight lines. So a step-independent swap rate may not exist for
   granulation at all. The net change of neighbours against elapsed time can be read from the census tracks already kept, and it
   has a null value.
2. **A calibration control with Sun-like boundaries, if the rate route is reopened.** Use a moving tiling whose cells move with
   the Sun's measured msd(t), and splits and merges: the scaling-state froth drawn as images, the 16 Nov decided next. The
   held-out test at P = 2 x step must pass within 15% before any joint limit is fitted again.
3. **A continuity threshold set per step.** Shares fall with the step, so a fixed theta removes real swaps at coarse steps. Set
   the threshold at each step from the shuffled-frame share distribution, for example the share that shuffled frames exceed only
   5% of the time. That keeps specificity constant across steps.
4. **The quiet-Sun run and the smoothing-3 setting do not pass the shuffled test at theta = 0.5** (0.39 to 0.45). Report them
   separately, or raise theta for them, before using any quiet-Sun number.

## Files

- scripts/census_sz.py: census.py of the 15 Nov study plus the swap list with shares and the centroid displacements. tiles.py,
  control_voronoi.py, run_matrix.py and prep_order.py (= stepcal_prep.py) are copied unchanged.
- scripts/make_configs.py: the configurations. sz_pilot.sh, sz_a.sh (stages gen, census) and sz_b.sh: the jobs.
- scripts/fit_sz.py: windows, theta, efficiency, held-out control, fits, criteria, speeds and tables.
- data/sun, data/control, data/holdout, data/order: census JSON with full swap lists, the raw data.
- data/configs_*.jsonl.
- results/summary.md: every table, per setting, window and theta. results/summary.json: the same as numbers.
- results/logs/, results/pilot/.
- Planes are read from the 15 Nov study's data folder. The regenerated arrays are not kept (work/ is ignored).

Credits: Bifrost (Gudiksen et al. 2011, A&A 531, A154); run en024048_hion of Carlsson, Hansteen, Gudiksen, Leenaarts and
De Pontieu 2016 (A&A 585, A4) and qs024048_by3363, Hinode Science Data Centre Europe. "Hinode is a Japanese mission developed and
launched by ISAS/JAXA, with NAOJ as domestic partner and NASA and STFC (UK) as international partners. It is operated by these
agencies in co-operation with ESA and NSC (Norway)." scikit-image (van der Walt et al. 2014). The shared event logger
(studies/2026-11-15-event-logger).

DICTO: the question and the route. Computation, checks and drafting with Claude (Anthropic).
