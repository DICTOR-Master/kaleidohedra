# Sun: net change of neighbours against displacement (18 Nov 2026)

Follows LEADS 1 and 3 of studies/2026-11-18-sun-net-change (aim "geometry gives laws"). Re-reading of stored data only: no new
segmentation, tracking or null runs.

## Question

The Sun's net neighbour change per surviving granule after a fixed time tau is frame-rate free, but it spreads over the 16
settings (up to 37% from the median at tau = 80 s, 9% at 320 s), the spread comes from the labelling, and finer segmentations move
further per spacing in the same time. Its ratio to the null at matched displacement falls with tau (0.73 at 80 s to 0.54 at 640 s).

1. Plotted against the survivors' rms displacement D (in spacings) instead of tau, do the 16 settings fall onto one curve net(D)?
2. How does that curve compare with the null curve net_null(D)? Is Sun / null a single number over D?
3. (Lead 3) Does the survivor-share step test, with a threshold fixed here, separate real from shuffled frames?

## Data (unchanged, from studies/2026-11-18-sun-net-change)

- data/net/TAG.json and TAG-shuf.json: for every setting, step (10, 20, 40, 80 s) and tau (80 to 640 s), one row per start with
  survivors, survivor contacts lost and made, and d2_px2 = sum over survivors of the squared periodic centroid displacement.
  D = (sum of d2_px2 / sum of survivors)^(1/2) / spacing, exactly as net_fit.py of that study. So D per (setting, step, tau) is
  computed from the stored per-start rows; nothing has to be re-run.
- data/null/null_net.json: the null curve (N = 20 000 periodic Poisson-Voronoi seeds, independent Gaussian displacement of rms D,
  D = 0.02 to 1.0, 4 repetitions; null_net.py, built on moving.py of studies/2026-11-15-tissue-null-models). Between grid points
  net_null(D) is interpolated linearly, as in net_fit.py.

## Plan (written 18 Nov 2026 BEFORE the re-reading)

Step 10 s throughout unless stated (the parent study found the measure frame-rate free); step 80 s is repeated as a check.

**A. Collapse.** For each setting, net(D) is the broken line through its six (D(tau), net(tau)) points. On the grid
D = 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50 it is interpolated linearly (no extrapolation: a setting enters at D only if D lies
between its tau = 80 s and 640 s values). A grid D is judged only if at least 12 of the 16 settings cover it.
- Spread at matched D = largest |net / median - 1| over the covering settings.
- Spread at matched tau = the same over the 16 settings at each tau (recomputed here; the parent gave 37, 21, 14, 9, 13, 18%).
- **Collapse: yes** if at every judged D every covering setting is within +-15% of the median (the parent's stability rule), and
  the largest spread at matched D is below the largest spread at matched tau over the taus whose median D lies in the judged range.
  Otherwise no.
- Reported, not judged: the same for the share of survivor contacts changed (lost / survivor contacts at t) against the null
  share; and the collapse at step 80 s.

**B. Sun / null as a function of D.** At each judged grid D: ratio = net(D) / net_null(D) per covering setting; median and range.
- **Single number: yes** if (i) the median ratio over the judged D varies by at most 10% (largest / smallest - 1 <= 0.10) and
  (ii) at every judged D every covering setting is within +-15% of that D's median ratio.
- **Candidate rung (computed, not proved)** only if collapse is yes and single number is yes.

**C. Survivor-share step test (Lead 3), threshold fixed here.** For each setting and tau: dev = (survivor share at step 80 s) /
(survivor share at step 10 s) - 1, on real and on shuffled frames (the parent's 17 Nov permutation, seed 7).
- Passes for a setting if at **every** tau 80 to 640 s: real |dev| < 5% and shuffled dev > +50% (a shuffled share of 0 at the
  10 s step counts as passing the shuffled side, since any survivor at 80 s is then an unbounded rise; if both are 0 the tau
  fails).
- **Specific to the time order** if it passes in at least 13 of 16 settings (the parent's count rule).
- Also reported, not judged: the same at tau = 80 s alone.
- Stated before the re-reading: the parent's summary already printed these survivor shares (rounded to 0.01), and its text gave
  the tau = 80 s values (real 0.4 to 2.2%, shuffled +135 to +386%) and real rises of 3 to 19% at 640 s. So this is a rule fixed
  in advance of the computation, not a blind test: the 80 s part can only confirm what was seen. The every-tau rule is the stricter
  reading and is judged.

Checks (FINAL ok only if all pass): every one of the 32 files read; for every setting, step and tau, D and net recomputed here
equal the parent's results/summary.json to 1e-9; D increases with tau in every setting at the 10 s step (else the broken line
is not a function of D, and that is reported); net_null(1.0) = 3.602 +- 0.01.

Prediction (before the re-reading): the threshold settings and the h-maxima settings will come closer at matched D than at
matched tau, but the h-maxima and temperature curves bend down at long tau (their net falls after 320 s while D keeps growing),
so the collapse holds at small D and fails at large D; and Sun / null(D) still falls with D, because the survivor rule removes
contacts with cells that died, which grows with tau and not with D alone.

Jobs: on the compute machine where the parent's data lives, one foreground run of scripts/net_vs_d.py (seconds); nothing in the
background.

## Result (net_vs_d.py: FINAL ok, 5 checks, 0 failed)

**VERDICT: the collapse holds (computed, narrowly); Sun / null is NOT a single number over D; the step test is NOT specific by
the every-tau rule. Not a candidate rung.**

Checks: all 32 files read; D, net, share and survivor share recomputed here equal the parent's summary.json to 1e-9 at every
setting, step and tau; D increases with tau in every setting; the null curve gives 3.602 at D = 1.0. No deviations from the plan.

1. **Collapse onto one curve net(D): yes, by the planned rule (computed).** Step 10 s, grid D judged where at least 12 of 16
   settings cover it (D = 0.20 to 0.45):

   | D | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 | 0.45 |
   |---|---|---|---|---|---|---|
   | settings | 13 | 16 | 16 | 16 | 16 | 16 |
   | net median | 0.785 | 0.955 | 1.089 | 1.169 | 1.227 | 1.262 |
   | largest deviation from the median | 12% | 9% | 10% | 9% | 11% | 14% |

   - At matched tau over the same range (tau = 160 to 480 s, median D 0.23 to 0.45) the largest deviation is 21, 14, 9, 13%. So
     the largest spread falls from 21% to 14%, and every setting is within 15% at every judged D. The margin is small: 14%
     against the 15% limit at D = 0.45.
   - The gain is at short tau. At tau = 320 s (D about 0.34) the spread is already 9% at matched tau, and 9 to 10% at matched D.
   - The largest spread of the parent (37% at tau = 80 s) lies at D = 0.14 to 0.20, below the judged range: only 3 settings reach
     D = 0.15 at tau = 80 s. That part is not tested by this re-reading.
   - What is left after matching D is no longer the labelling rule (threshold and h-maxima curves mix): at D = 0.20 the en run at
     0.2 Mm and thr 0 are lowest (0.69, 0.70) and qs is highest (0.86); at D = 0.45 the temperature settings and en 0.2 Mm are
     lowest (1.09 to 1.13) and qs is highest (1.30). So the remainder follows run and field.
   - Check at step 80 s (reported, not judged): every judged D within 8% (against 20% at matched tau), so the collapse is not an
     artefact of the 10 s step.
2. **Sun / null against D: not a single number (computed).** Median over the covering settings (range):

   | D | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 | 0.45 |
   |---|---|---|---|---|---|---|
   | Sun / null(D) | 0.73 (0.64 to 0.80) | 0.73 (0.66 to 0.79) | 0.72 (0.65 to 0.75) | 0.68 (0.62 to 0.71) | 0.64 (0.57 to 0.67) | 0.60 (0.52 to 0.62) |
   | share of contacts changed / null share | 0.86 | 0.90 | 0.93 | 0.96 | 0.98 | 1.00 |

   - The median ratio varies by 22% over the judged D (limit 10%), so the planned single-number test fails. Each D's settings lie
     within 15% of its median.
   - The ratio falls with D just as it fell with tau. Matching displacement does not remove the fall, as predicted: the survivor
     rule drops contacts with cells that died, and that loss grows with time.
   - After the run, not in the plan: from D = 0.20 to 0.30 the median ratio stays at 0.72 to 0.73 (1.4% variation). This range
     was not chosen in advance and is not judged.
   - Per contact (the share of survivor contacts changed against the null share) the Sun moves from 0.86 to 1.00 of the null over
     the same D: also not constant.
3. **Survivor-share step test (Lead 3): not specific by the fixed rule (computed).**
   - Rule fixed before the run: at every tau, real survivor share moves by less than 5% from step 10 s to 80 s, and shuffled by
     more than +50%; needed in 13 of 16 settings.
   - It passes in 6 of 16 settings. The shuffled side passes everywhere: +78% to unbounded rises. The real side fails at long tau:
     real shares rise by up to 5.0 to 19.4% at tau = 240 to 640 s. It fails in 10 settings (thr 0, smoothing 3, the three en h-maxima, both
     temperature settings, en 0.2 Mm, qs thr 0, qs h-maxima 600); it passes in en thr 0.25 and 0.5, en 0.0 Mm, qs thr 0.25 and
     0.5, and qs 0.2 Mm.
   - At tau = 80 s alone (reported, not judged) it passes in 16 of 16 settings: real +0.4 to +2.2%, shuffled +135 to +386%. These
     values were seen in the parent study before the threshold was set, so this part confirms nothing new.

Conclusion: re-read against displacement, the 16 settings come within 15% of one curve net(D) for D = 0.20 to 0.45 (computed,
narrowly: 14% at the edge), and the labelling spread at matched tau is largely a time-scale effect there. The Sun / null ratio
still falls with D (0.73 to 0.60), so it is not a single number, and the shuffled-frame specificity rule fixed in advance holds
only at short tau. No candidate rung.

## LEADS

1. **Short displacements.** The parent's largest spread (tau = 80 s) lies at D = 0.14 to 0.20, outside the judged range. Reaching
   it needs a new census with tau = 20 to 70 s (outside this re-reading, which used only stored data). It would test whether the collapse extends to small D, where the ratio and its spread were largest.
2. **The fall of Sun / null with D is the survivor rule.** A survivor-free count (the parent's Lead 2: lineage contacts, or a null
   with births and deaths) is the next test of whether a single ratio exists. On the present data, the plateau 0.72 to 0.73 at
   D = 0.20 to 0.30 is a post-run observation only.
3. **Run and field remain after matching D.** qs runs above en, temperature and the 0.2 Mm depth below at large D. A third run
   would show whether this is a difference between simulations or noise from the qs run's few starts (5 to 12).
4. **A specificity rule for short tau only**, fixed now for the next census: real |dev| < 5% and shuffled > +50% at tau up to
   160 s, where both sides were met in 16 of 16 settings here.

## Files

- scripts/net_vs_d.py: re-reading, criteria, tables, figure. Usage: net_vs_d.py (from this folder).
- data/net_vs_d.json: every number (per setting, step and tau: D, net, share, ratio; grid interpolations; spreads; step test).
- results/summary.md: tables. results/net_vs_d.png: net(D) for the 16 settings with the null curve, and Sun / null(D).

Credits: as studies/2026-11-18-sun-net-change (Bifrost, Gudiksen et al. 2011, A&A 531, A154; run en024048_hion of Carlsson,
Hansteen, Gudiksen, Leenaarts and De Pontieu 2016, A&A 585, A4, and qs024048_by3363, Hinode Science Data Centre Europe;
scikit-image; Qhull through scipy.spatial). Matplotlib (Hunter 2007) for the figure.

DICTO: the question and the route. Computation, checks and drafting with Claude (Anthropic).
