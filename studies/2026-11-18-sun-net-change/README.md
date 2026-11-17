# Sun: net change of neighbours after a fixed time (18 Nov 2026)

Follows LEADS 1 of studies/2026-11-17-sun-step-zero (aim "geometry gives laws": a natural rung of the scutoid ladder would be a
number that is stable across sampling, runs, depths, smoothing and labelling, and has a null value to compare with).

## Question

The granule swap rate has no converged value as the time step goes to 0 (studies/2026-11-17-sun-step-zero), and granule centroids
move nearer to diffusion than to straight lines (mean square displacement ~ step^0.70 to 0.88). For diffusive seed motion the null
model (studies/2026-11-15-tissue-null-models) found that swap counts per unit time grow as the frame interval shrinks, and that only
the NET change of contacts after a fixed displacement is frame-rate free (3.600 per cell after one spacing of rms displacement, 2D).

1. Is the Sun's net neighbour change per cell after a fixed elapsed time tau the same at sampling steps 10, 20, 40 and 80 s?
2. Is it stable over runs, depths, smoothing and labelling?
3. How does it compare with the null model at matched displacement?

## Definition (the null study's, read from its script)

studies/2026-11-15-tissue-null-models/scripts/moving.py: E0 = contact pairs at the start, E = contact pairs at the end;
net_lost = |E0 \ E|, net_made = |E \ E0|; **net change per cell = (net_lost + net_made) / N** (N cells; each pair counted once,
not once per cell). The null value 3.600 +- 0.006 is this number after a total rms seed displacement of 1.0 spacing
(spacing = (area / N)^(1/2)), N = 20 000 periodic Poisson-Voronoi seeds. It uses only the two end configurations; the frames in
between do not enter.

For the Sun, cells are born, split, merge and die, so the null's fixed set of N cells becomes the **survivors**: the cells whose
tracked label is present at both t and t + tau. Primary quantity, per (setting, step, tau):

  net(tau) = sum over starts of (pairs of survivors touching at t and not at t + tau, plus the reverse) / sum of survivors.

Secondary (reported, not judged): (a) **share of contacts changed** = net_lost / (contacts among survivors at t); the null
equivalent is net_lost / 3N; this removes the effect of survivors losing partners that died; (b) **all labels**: the same count
over all pairs, divided by the mean cell number of the two frames.

The sampling step enters only through the tracking (each frame's segmentation and contacts are the same at every step; the label a
cell carries at t + tau depends on the chain of frame-to-frame matches). So question 1 tests whether the tracked identities are
frame-rate free; for the null, net change is frame-rate free by construction.

## Plan (written 18 Nov 2026 BEFORE the pilot and the runs)

- **Data, unchanged.** The 13 main settings of the 16 and 17 Nov studies (Bifrost en024048_hion uz at 0.1 Mm: thr 0, 0.25, 0.5,
  hmax 300, 600, 1200, smoothing 3; en temperature at tau = 1: thr 0.25, hmax 300 K; qs024048_by3363 uz at 0.1 Mm: thr 0, 0.25,
  0.5, hmax 600), plus three depth settings: en uz thr 0.25 smoothing 1.5 at 0.0 and 0.2 Mm, qs uz thr 0.25 smoothing 1.5 at 0.2 Mm (16 settings). Segmentation and frame-to-frame
  matching: tiles.py of the 15 Nov study, unchanged (imported from studies/2026-11-17-sun-step-zero/scripts).
- **Steps** 10, 20, 40, 80 s. **tau** 80, 160, 240, 320, 480, 640 s. **Starts** every 80 s (frames 0, 8, 16, ...), the same
  starts at every step, so the four steps compare the same pairs of frames.
- **Contacts** per frame: pairs of labels sharing a pixel edge (4-adjacency, periodic), the census rule; checked equal to
  tiles.graph on pilot frames.
- **Displacement.** D = rms periodic centroid displacement of survivors over tau, in spacing l = (box area / mean cells)^(1/2);
  D_rel = rms change of the separation of pairs touching at t (both survivors). For independent seeds D_rel = 2^(1/2) D, so the
  matched null displacement is reported two ways: D itself, and D_eff = D_rel / 2^(1/2) (granules move with their neighbours in
  flows; independent seeds do not). Centroid jitter (1.6 to 2.3 pixels, 17 Nov) inflates D at short tau; the bracket with
  D^2 - j^2 is reported.
- **Null curve.** N = 20 000 periodic 2D Poisson-Voronoi seeds, each moved by an independent Gaussian displacement of rms D,
  D = 0.02 to 1.0, 4 repetitions: net per cell and share of contacts changed. Since net uses only the end positions, straight-line
  motion with Gaussian velocities and Brownian motion give the SAME end distribution, so one curve serves both. Check: D = 1.0
  reproduces 3.600 within 0.02.
- **Shuffled frames** (the 17 Nov permutation, seed 7) for every setting, step and tau: unrelated frames give the false-change
  level of the tracking.

Criteria (per setting; judged over tau = 80 to 640 s):
- **F, frame-rate free:** at every tau, net at 20, 40 and 80 s is within 5% of net at 10 s, or within 2 standard errors
  (standard error from the per-start values with an effective count n_starts x min(1, 80 s / tau)).
  **Frame-rate free** if F holds in at least 13 of 16 settings.
- **S, specific to the time order:** at every tau, real net is at most 1/2 of shuffled net, at every step.
- **Stable over settings:** at each tau (10 s step), every setting within +-15% of the median of the 16. If not, the spread is
  broken down by run, depth, smoothing and labelling.
- **Positive** (a candidate natural rung, computed, not proved) only if frame-rate free AND S in at least 13 of 16 AND stable.
- Null comparison (ratio Sun / null at D and at D_eff, per tau) is reported, not judged.

Prediction (before the pilot): the survivor count will depend strongly on the step (coarse steps lose more mutual-best matches),
while net per survivor moves less; whether it stays within 5% is open. Against the null at matched D the Sun should change fewer
neighbours (neighbouring granules move together, which independent seeds do not), so Sun / null < 1 at D and closer to 1 at D_eff.

Jobs: on the compute machine where the Bifrost planes live, foreground chunks under 5 minutes each; nothing in the background.
- **Deviations from the plan, recorded:** (1) the shuffled-frame table gives division by zero where no shuffled survivors touch
  (net 0); the ratio is then reported as infinite (S fails there). (2) Two diagnostics were added AFTER the run and are marked so:
  the step-dependence of the survivor share on shuffled frames, and the share of contacts changed on shuffled frames.
  (3) The regenerated shuffled arrays (1.2 GB) were deleted after the run and are rebuilt by `jobs.sh gen`.

## Result (jobs pilot, gen, real, shuf, null: FINAL ok; net_fit.py: FINAL ok, 18 checks, 0 failed)

**VERDICT: NOT CONFIRMED as a natural rung.** One of the three planned tests passes and two fail:
- frame-rate free: passes in 16 of 16 settings;
- shuffled-frame test: passes in 0 of 16 settings;
- stability: passes only at tau = 240 to 480 s.

What holds (computed): the Sun's net neighbour change after a fixed time does not depend on the sampling step. For tau = 80 to
320 s, steps of 20, 40 and 80 s give the 10 s value within 4.9% in every setting.

Checks (exact or within the stated tolerance):
- The null curve reproduces the null study: 3.602 +- 0.008 per cell at D = 1.0, against 3.600 +- 0.006.
- The contact pairs equal tiles.graph on the three checked frames of all 32 sequences.
- Every null configuration has exactly 3N contacts.

Results:
1. **Frame-rate free (computed).** Net per survivor at steps 10 / 20 / 40 / 80 s on the primary setting (en uz 0.1 Mm, thr 0.25):
   0.564 / 0.561 / 0.560 / 0.556 at tau = 80 s, 1.125 / 1.125 / 1.116 / 1.117 at 320 s, 1.330 / 1.334 / 1.331 / 1.342 at 640 s.
   - Over all 16 settings: the largest deviation from the 10 s value is 4.9% for tau up to 320 s.
   - At 480 and 640 s it reaches 17.4% (20 comparisons above 5%, in 8 settings: all four en h-maxima and temperature settings, the en depths 0.0 and 0.2 Mm, and qs h-maxima 600). Those
     pass only by the 2 standard error rule, because few starts are left (23 to 25 in the en run, 5 to 7 in the qs run).
   - The survivor share itself hardly depends on the step: from 10 s to 80 s it rises by 0.4 to 2.2% at tau = 80 s, and by 3 to
     19% at 640 s.
2. **The planned shuffled-frame test fails, and does not work as a floor for this measure (computed).**
   - Planned test, real at most half of shuffled: holds in 0 of 16 settings. At tau = 80 s (10 s step) the ratio real / shuffled is
     0.74 to 1.63. At longer tau it grows without bound: in shuffled frames only 0 to 14% of cells survive, and they rarely touch
     each other (0 to 85 survivor contacts at 640 s), so their net per survivor falls towards 0.
   - After the run, not in the plan: the time order shows elsewhere. At tau = 80 s, 81 to 88% of real cells survive against 13 to
     27% in shuffled frames. Changing the step from 10 s to 80 s moves the real survivor share by 0.4 to 2.2%, but the shuffled one by
     +135 to +386%. The share of survivor contacts changed is 0.10 to 0.16 in real frames against 0.29 to 0.56 in shuffled ones.
   - From tau = 240 s on, too few shuffled survivor contacts are left to compare (100 or more in 8, 6, 3 and 0 settings at 240,
     320, 480 and 640 s).
   - So the step-independence is specific to the real time order, but by a test chosen after the run. The planned criterion fails.
3. **Not stable over settings at short and long tau (computed).** At the 10 s step, the largest deviation from the median of the 16
   settings is:

   | tau | 80 s | 160 s | 240 s | 320 s | 480 s | 640 s |
   |---|---|---|---|---|---|---|
   | median net per survivor | 0.622 | 0.911 | 1.064 | 1.159 | 1.249 | 1.270 |
   | largest deviation | 37% | 21% | 14% | 9% | 13% | 18% |

   The spread comes from the labelling. At tau = 320 s:
   - depth (en 0.0 / 0.1 / 0.2 Mm): 1.128 / 1.125 / 1.117; qs 0.1 / 0.2 Mm: 1.154 / 1.181;
   - smoothing 1.5 / 3: 1.125 / 1.147;
   - run en / qs (thr 0.25): 1.125 / 1.154; field uz / temperature (thr 0.25): 1.125 / 1.096;
   - labelling: thr 0 / 0.25 / 0.5: 1.164 / 1.125 / 1.121; h-maxima 300 / 600 / 1200: 1.262 / 1.263 / 1.165.

   At tau = 80 s the threshold settings give 0.537 to 0.653 (qs thr 0.5: 0.747), and h-maxima 300 and 600 and the temperature
   settings give 0.722 to 0.851. (h-maxima 1200: 0.623). Those four high settings also move further per spacing in the same time: D = 0.175 to 0.204, against 0.143 to
   0.169 for the threshold settings at 0.1 Mm.
4. **Against the null at matched displacement (computed; not a constant).** The null net per cell rises from 0.574 at D = 0.1 to
   3.602 at D = 1.0. The Sun's rms survivor displacement is D = 0.14 to 0.20 spacings at tau = 80 s and 0.47 to 0.68 at 640 s.
   Sun / null at the same D (median over settings, range):

   | tau | 80 s | 160 s | 240 s | 320 s | 480 s | 640 s |
   |---|---|---|---|---|---|---|
   | Sun / null(D) | 0.73 (0.62 to 0.80) | 0.74 (0.67 to 0.80) | 0.71 | 0.67 | 0.60 | 0.54 (0.39 to 0.59) |
   | Sun / null(D_eff) | 0.70 | 0.73 | 0.70 | 0.68 | 0.64 | 0.56 |
   | share of contacts changed / null share (D) | 0.82 (0.71 to 0.90) | 0.90 | 0.93 | 0.95 (0.86 to 1.03) | 0.99 | 1.01 (0.81 to 1.09) |

   - At matched displacement the Sun changes about 0.7 of the null's neighbours at tau = 80 to 240 s, and the ratio then falls.
     The fall follows the survivor rule: survivor contacts per survivor drop from 2.65 to 2.80 at 80 s to 1.13 to 1.81 at 640 s
     (null: 3 per cell), because contacts with cells that died are not counted.
   - Per contact (the planned secondary, reported, not judged) the Sun moves from 0.82 of the null at 80 s to about 1.0 at 480 to
     640 s. There the survivors are the long-lived cells and no shuffled floor is left.
   - Matching, stated honestly: the null's net change uses only the end positions. Its seeds end Gaussian-distributed for
     straight-line and Brownian motion alike, so the straight-line against diffusive question does not change the null value.
   - What differs from the null: the Sun's cells are not Voronoi cells of their centroids; their displacements need not be
     Gaussian or independent; survivors replace a fixed set of cells; and centroid jitter inflates D at short tau.
   - Pairs of neighbours separate about as much as independent seeds would (D_eff / D = 0.90 to 1.09). Subtracting the 17 Nov
     jitter raises the ratio by up to 0.06 at 80 s and by 0.01 or less from 320 s.

Conclusion: NOT CONFIRMED. A natural rung needs a number that is the same at every step, specific to the real time order, stable
across settings, and has a null value.
- The net neighbour change per surviving granule after a fixed time meets the first (computed): within 4.9% over steps 10 to 80 s
  for tau up to 320 s, in all 16 settings.
- It fails the planned shuffled-frame test. Per-survivor counts in shuffled frames are not a usable floor.
- It fails stability at short and long tau, where the segmentation's marker rule moves it by up to 37%. Depth, smoothing, run and
  field move it by 3% or less at 320 s.
- Against the null at matched displacement it is about 0.7 at tau = 80 to 240 s and falls with tau. So there is no single ratio.

## LEADS

1. **Net change against displacement instead of time (re-analysis of data/net, no new census).** The labelling spread at short tau
   goes with D: finer segmentations move further per spacing. Plot net per survivor and share of contacts changed against D for all
   16 settings. If they fall onto one curve, the labelling spread is a time-scale effect, and Sun / null(D) at fixed D is the
   number to judge (0.62 to 0.80 at tau = 80 s, against 0.537 to 0.851 for net itself).
2. **A survivor-free count.** The fall of Sun / null with tau follows the survivor rule (fewer counted contacts per survivor). Count
   instead the contacts lost and made per cell-lineage: a split's daughters inherit the parent's contacts. Or compare with a null
   that has births and deaths: the swept Poisson-Voronoi of the null study, or the scaling-state froth.
3. **A specificity test fixed in advance for this measure.** The survivor share's step-dependence separates real from shuffled
   frames by a factor of 60 or more at tau = 80 s (0.4 to 2.2% against 135 to 386%). Fix that as the test before the next run.
4. **Longer runs for tau of 480 s and more.** The qs run gives only 5 to 7 starts there, and the en run 23 to 25 overlapping
   ones. The 17 min qs run cannot settle the long-tau values.

## Files

- scripts/net_sz.py: segmentation (tiles.py of the 15 Nov study, imported unchanged from studies/2026-11-17-sun-step-zero/scripts),
  tracking at each step, survivors, net counts, displacements; one JSON per setting with every start's counts.
- scripts/null_net.py: the null curve (nulllib.py of studies/2026-11-15-tissue-null-models, imported unchanged).
- scripts/settings.txt (the 16 settings), scripts/jobs.sh (stages pilot, gen, real, shuf, null), scripts/net_fit.py (tables,
  criteria, verdict).
- data/net/TAG.json and TAG-shuf.json: raw per-start counts (the raw data). data/null/null_net.json: the null runs.
- results/summary.md: every table. results/summary.json: the same as numbers. results/logs/, results/pilot/.
- Bifrost planes are read from the 15 Nov study's data folder; the shuffled arrays are not kept (work/ is ignored).

Credits: Bifrost (Gudiksen et al. 2011, A&A 531, A154); run en024048_hion of Carlsson, Hansteen, Gudiksen, Leenaarts and
De Pontieu 2016 (A&A 585, A4) and qs024048_by3363, Hinode Science Data Centre Europe. "Hinode is a Japanese mission developed and
launched by ISAS/JAXA, with NAOJ as domestic partner and NASA and STFC (UK) as international partners. It is operated by these
agencies in co-operation with ESA and NSC (Norway)." scikit-image (van der Walt et al. 2014). Qhull (Barber, Dobkin and Huhdanpaa
1996) through scipy.spatial for the null's Delaunay contacts.

DICTO: the question and the route. Computation, checks and drafting with Claude (Anthropic).
