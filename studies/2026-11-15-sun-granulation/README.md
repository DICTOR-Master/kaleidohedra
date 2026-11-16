# Sun: neighbour swaps in solar granulation (One tissue, three scales, Section 2)

DICTO, 15 Nov 2026: "throw all possible resources at the new scutoid work". Plan: "One tissue, three scales" (14 Nov 2026),
Section 2. The plane of granules is a tiling with three cells at almost every corner; followed through time, each granule is a
scutoid-like cell of a tissue in space-time. Here we count how that tiling changes: swaps (two cells stop touching, two others
start: the 2-2 move), splits (one cell divides in two), merges (two cells join), births and deaths at a junction (the 1-3 and 3-1
moves). Nothing here assumes or tests any influence of one system on another.

## VERDICT

1. **Prior art (free sources).** No count of neighbour swaps in solar granulation or supergranulation was found. Granule trackers
   count fragmentation, merging and lifetimes of single cells (Malherbe, Roudier and co-workers; Lemmerer et al. 2017; DeRosa &
   Toomre 2004); network studies give single-frame side-number laws (Schrijver, Hagenaar & Title 1997). Neighbour switching in
   laboratory Bénard-Marangoni convection is described by Cerisier, Rahal & Rivier (1996), whose full text we could not read, so
   whether they give rates is open. Details and every source checked: [PRIOR_ART.md](PRIOR_ART.md).
2. **Data.** Public radiative-MHD simulations (Bifrost; Hinode Science Data Centre Europe): the enhanced-network run
   en024048_hion (242 snapshots, 10 s apart, 40 min) and the quiet-Sun run qs024048_by3363 (101 snapshots, 17 min); 24 x 24 Mm,
   periodic, 48 km pixels. We took only horizontal planes, 2.1 GB in all. Supergranules were not reached (box too small; the free
   supergranulation data route needs a registered e-mail address).
3. **The tilings are clean.** Segmentation tiles every pixel; the torus Euler formula V - E + F = 0 holds in 3109 of 3167
   frames (98.2%) over the 16 settings at the granulation planes (0 to 13 failing frames per setting; at 0.4 Mm depth, where the
   cells blur, 146 of 242 fail); 99.45% of junctions are triple, the rest four-fold. The logger's balance holds at every step and its negative control is caught in every run.
4. **Swaps are frequent and of the same order as splits.** At the finest step (10 s), over 13 settings of field, threshold
   and smoothing in the two runs, a granule takes part in a persistent swap (not undone within 60 s) at a rate of **0.07 to 0.15
   swaps per cell per minute**, and the ratio **swaps per persistent split is 0.8 to 1.9**; with the cell lifetime (Little's law,
   6 to 11 min) this is **0.6 to 1.3 swaps per cell lifetime**, i.e. each granule takes part in about 2.5 to 5 swaps in its life
   (4 cells per swap). These ranges are the spread over settings, not statistical errors.
5. **Births and deaths at junctions are almost absent.** With lineage, new granules arise by splitting (thousands) and vanish by
   merging into one neighbour (90% or more of their area goes to one cell); fewer than 1 in 100 new cells is a three-sided
   birth at a junction at 10 s. This is a property of the counting rule as much as of the Sun: a shrinking granule's last pixels
   lie in one neighbour.
6. **NOT STABLE with the time step.** Every count falls as the step grows: swaps per cell lifetime fall by 12 to 26% from 10 to
   20 s and by 50 to 70% from 10 to 80 s, in every setting. Part of this is real merging of events into clumps (the clump count
   stays high), part is detection. By the plan's own rule, no swap rate from this study is yet a stable number to compare across
   scales. What is stable: the order of magnitude (swaps comparable to splits; about one swap per cell lifetime), the near
   absence of junction births, and the cell statistics below.
   16 Nov: dividing out the detection loss measured on the moving-Voronoi control does not remove it (section "Swap rate at
   step 0": the corrected rate still halves from step 0 to 80 s and moves with P; NOT CONFIRMED).
   16 Nov: counting only swaps seen at the same place on the neighbouring depth planes does not remove it either, and
   real frames give only 1.2 to 1.7 times as many as shuffled frames at 10 s (section "Swaps traced through depth"; NOT CONFIRMED).
7. **Cell statistics are robust.** The granular tiling is far from the Voronoi tiling of its own cell centres: side-number
   variance mu2 = 2.7 to 3.8 (en) and 3.3 to 4.9 (qs) against 1.0 to 1.2 for the centroid Voronoi tiling; p6 = 0.19 to 0.24 (en)
   and 0.16 to 0.21 (qs) against 0.35 to 0.40. Aboav-Weaire holds: n m(n) is linear in n with a = 0.85 to 0.90 (en), 0.67 to 0.77 (qs), and the fitted
   intercept agrees with 6a + mu2 within 0.15 to 0.35 (always a little below). Lewis's law (mean area linear in n) holds with R2 0.94 to 0.99 (en).
   (Aboav 1970; Weaire 1974; Lewis 1928; earlier granulation work: the A&A 1994 statistical-crystallography paper and Schrijver
   et al. 1997, abstracts only.)
8. **Through the layers.** Slicing the same simulation deeper (0, 0.1, 0.2 Mm below the mean tau = 1 height) gives fewer, larger
   cells (270, 226, 182) and fewer swaps per cell lifetime (0.88, 0.75, 0.50 at the same threshold): the tissue coarsens with
   depth. At 0.4 Mm the segmentation fails Euler in 60% of frames and is not used.
9. **Positive control** (moving periodic Voronoi seeds drawn as images, through the same chain, against exact counts): the true
   swap count does not change with the step (within 2%), the pipeline's does (87% found at 10 s, 62% at 80 s, at the Sun-like
   rate). Much of the Sun's step dependence is therefore detection loss; at 10 s the detection factor lies between about 0.8 and
   1.15, so the Sun's 10 s rates stand to about 20% on top of the spread over settings. The control also logs false splits and
   merges, so those Sun counts carry an artefact share of unknown size.

## Method

- **Data** (credit at the point of use): Bifrost code, Gudiksen et al. 2011, A&A 531, A154; public run en024048_hion, Carlsson,
  Hansteen, Gudiksen, Leenaarts & De Pontieu 2016, A&A 585, A4; qs024048_by3363 listed by the same archive (sdc.uio.no). Planes
  fetched by HTTP range requests (scripts/fetch_bifrost.py): vertical velocity uz at the mean tau(500 nm) = 1 height (header
  ZTAU51 = 0.059 Mm) and 0.1, 0.2, 0.4 Mm below it; temperature at the top two planes. The qs headers lack ZTAU51; the en value
  was used and the plane's mean temperature (5150 K against 6930 K in en) shows that the qs planes sit higher in the atmosphere
  than the en planes of the same name; the qs "0.2 Mm" plane is therefore also counted.
- **Segmentation that tiles** (scripts/tiles.py): smoothed field, markers, then a marker watershed (scikit-image; van der Walt
  et al. 2014) with the dark downflow lanes as the boundaries; periodic in both directions. Markers either the connected regions
  where the field exceeds mean + h std ("thr", h = 0, 0.25, 0.5) or regional maxima of prominence h ("hmax", h = 300, 600,
  1200 in the field's units; 300 K for temperature). Smoothing 1.5 or 3 pixels.
- **Graph, checks.** Contacts by shared pixel edges; junctions from 2 x 2 pixel blocks; segments per pair from junction ends;
  torus Euler per frame.
- **Matching.** Overlap-based: a new cell keeps an old label when each is the other's largest overlap; lineage shares are kept
  for newcomers (parents) and for vanished cells (heirs), in the logger's format.
- **Events** by the shared event logger (studies/2026-11-15-event-logger, imported unchanged). Elementary swaps are read inside
  every logged event (a lost contact a-b and a gained contact c-d of the same four cells), and as two-step swaps through a
  four-fold junction (lost, then gained within 60 s). Flicker: a swap undone by the same four cells within W seconds, and a split
  whose piece vanishes again within W, are removed ("persistent"). W = 60 s; W = 20 to 240 s is also recorded.
- **Rates.** Per cell per minute; cell lifetime by Little's law (mean number of cells / rate of persistent new cells); swaps
  per persistent split; swaps per cell lifetime. The box is periodic, so every event is inside: there is no patch edge.
- **Settings run** (17): en: uz 0.1 Mm with thr 0, 0.25, 0.5 and hmax 300, 600, 1200, smoothing 1.5; thr 0.25 with smoothing 3;
  temperature at tau = 1 (thr 0.25, hmax 300 K); depths 0, 0.2, 0.4 Mm; qs: uz 0.1 Mm with thr 0, 0.25, 0.5, hmax 600; uz 0.2 Mm
  thr 0.25. Each at time steps 10, 20, 40, 80 s.

## Results

Full tables: results/summary.md (generated by scripts/aggregate.py from results/census/*.json and results/control/*.json).
Figure: results/figures/sun_swaps.png (left: one snapshot, cells in a swap in the next 10 s in red, split or merge in blue;
right: swaps per cell lifetime against the time step for every setting).

### Primary setting (en, uz 0.1 Mm below tau = 1, thr 0.25, smoothing 1.5; 226 cells, 40 min)

| step | persistent swaps | per cell per min | persistent splits | persistent merges | births / deaths | lifetime (s) | swaps per split | swaps per cell lifetime |
|---|---|---|---|---|---|---|---|---|
| 10 s | 733 | 0.081 | 760 | 716 | 0 / 0 | 558 | 0.96 | 0.75 |
| 20 s | 626 | 0.069 | 652 | 418 | 3 / 0 | 539 | 0.96 | 0.62 |
| 40 s | 484 | 0.054 | 462 | 192 | 5 / 0 | 537 | 1.05 | 0.48 |
| 80 s | 305 | 0.034 | 201 | 69 | 13 / 0 | 588 | 1.52 | 0.33 |

At 10 s: 1077 elementary swaps (127 of them two-step through a four-fold junction), 908 inside events the logger itself types
as swaps; persistent swaps by window W = 20, 30, 60, 120, 240 s: 785, 763, 733, 703, 685 (levelling off). Not resolved:
253 contacts lost and 243 gained that do not pair into a swap within 60 s (they would raise the swap count by up to a third if
they are slow swaps); clumps (more than one change at one place) 936, mostly these single lost or gained contacts.

### Swaps per cell lifetime at 10 s, all settings

| run, field | thr 0 | thr 0.25 | thr 0.5 | hmax low | hmax mid | hmax high | smoothing 3 |
|---|---|---|---|---|---|---|---|
| en, uz 0.1 Mm | 0.63 | 0.75 | 0.77 | 1.04 (300) | 0.98 (600) | 0.94 (1200) | 0.86 |
| en, temperature at tau = 1 | | 0.77 | | 0.98 (300 K) | | | |
| en, uz at tau = 1 / 0.2 Mm / 0.4 Mm | | 0.88 / 0.50 / 0.17 | | | | | |
| qs, uz 0.1 Mm | 0.75 | 0.91 | 0.91 | | 1.26 (600) | | |
| qs, uz 0.2 Mm | | 1.02 | | | | | |

More markers (hmax) give more, smaller cells and more swaps per cell; the quiet-Sun run swaps more per cell than the
enhanced-network run at the same setting (0.91 against 0.75 at thr 0.25; 1.26 against 0.98 at hmax 600), but the qs planes sit
higher (see Method), so this is not yet a clean comparison of magnetic environments.

## Positive control: moving Voronoi tilings drawn as images (known answer)

500 seeds move on smooth random paths in a periodic 504 x 504 pixel box (the Bifrost grid, about 22 pixels per cell as for the
granules); the image is minus the distance to the nearest seed, optionally with smooth texture (noise 1 = boundaries shifted by
about one pixel, spurious maxima). The exact Delaunay neighbour sets are computed at every frame (and at 20 substeps); every change
of a Voronoi tiling with fixed seeds is a swap. Exact persistent = pairs lost between sampled frames minus twice those regained
within 60 s, the same rule as for the Sun. 120 frames, 10 s apart. Speed 1 gives about 0.10 swaps per cell per minute, close to
the Sun's 0.07 to 0.15.

| speed | texture | exact persistent swaps, step 10 / 20 / 40 / 80 s | pipeline persistent / exact, step 10 / 20 / 40 / 80 s |
|---|---|---|---|
| 1 | none | 1013 / 997 / 1006 / 1000 | 0.87 / 0.84 / 0.76 / 0.62 |
| 1 | 1 | same | 1.15 / 0.76 / 0.69 / 0.70 |
| 2 | none | 1999 / 1969 / 1961 / 1959 | 0.83 / 0.78 / 0.66 / 0.48 |
| 2 | 1 | same | 0.79 / 0.60 / 0.50 / 0.43 |
| 4 | none | 3626 / 3545 / 3605 / 3698 | 0.80 / 0.71 / 0.52 / 0.29 |
| 4 | 1 | same | 0.57 / 0.47 / 0.37 / 0.24 |

- **The true count does not depend on the step** (exact persistent swaps change by 2% or less from 10 to 80 s at speeds 1 and
  2), but **the pipeline's count does**: at the Sun-like speed it finds 87% of the swaps at 10 s and 62% at 80 s (no texture).
  So much of the step dependence in the Sun is detection loss, not physics: changes that fall into one step become clumps or
  unpaired lost/gained contacts.
- The Sun falls faster than the control (primary setting: 1, 0.83, 0.64, 0.44 of its 10 s value at 10, 20, 40, 80 s, against
  1, 0.94, 0.87, 0.70 for the control at speed 1, no texture). The remainder is either real short back-and-forth swaps in the Sun (undone
  within 80 s) or the Sun's texture; the control cannot tell which.
- Texture can push the count either way at 10 s (1.15 at speed 1, 0.79 at speed 2): the detection factor at the finest step lies
  between about 0.8 and 1.15 for Sun-like rates. So the Sun's 10 s rates in the verdict are good to about 20% from detection alone,
  on top of the spread over settings.
- The control's tilings have no real splits or merges, yet the pipeline logs 64 to 240 (no texture) and up to 1418 (texture) at
  10 s: false splits and merges from marker loss and texture. Of the Sun's split and merge counts, some part is this kind of
  artefact; the control gives its scale, not its exact share. (The control ran before the heir fix noted under Version; the fix
  does not touch swap counting, but the control's split/merge split may shift.)

## Wording kept

"The plane of granules has the combinatorics of a simple tiling; its history is a scutoid tissue." No claim that one body
imposes rules on another. Event names plain first (swap, split, merge), #104 names second.

## Files

- scripts/fetch_bifrost.py (range download), tiles.py (segmentation, graph, matching, logger frames), census.py (one setting),
  run_matrix.py (settings in parallel), control_voronoi.py (positive control), aggregate.py (tables), figures.py, render_pilot.py,
  pilot*.sh, control*.sh, sun_matrix.jsonl (the 17 settings).
- results/census/*.json (one per setting), results/control/*.json, results/summary.md, results/figures/, results/pilot*/.
- PRIOR_ART.md. Data (planes) are not in the repository (data/ is ignored); fetch_bifrost.py fetches them again.

## Version

Study of 15 Nov 2026 (Claude for DICTO). Faults met and fixed on the way (recorded per the ledger rule): the archive's IPv6 route
stalled 30 s per request (forced IPv4); FITS header lengths differ between snapshots (read per file); the heirs (shares of a
vanished cell) were first attached to the later frame, so every vanishing cell read as unlineaged; fixed before the counts above.

## Leads

1. Resolve the unpaired lost/gained contacts (slow four-fold passages or real non-swap changes) before quoting a rate.
2. Make the step dependence the measured object: rate against step, extrapolated to step 0, with the control's efficiency.
   Done 16 Nov (section "Swap rate at step 0"): NOT CONFIRMED; next there: a control with splits and merges, a continuity test.
3. Emergent intensity (the observable) instead of velocity planes: the archive's synthetic images, or a radiative transfer pass.
4. A real observation: Hinode SOT/BFI G-band quiet-Sun series (free, needs calibration), with the patch edge rule.
5. Supergranules: SDO/HMI flow maps (needs a registered account; ask DICTO) or a larger simulation box.
6. Ratio to compare with #104: swaps per birth there (h2/h1, e.g. 366/116 = 3.2); here births are absent and splits stand in.

## Swap rate at step 0 (16 Nov 2026; open item 3 of studies/2026-11-16-scutoid-interactions)

Question: is there a Sun swap rate that does not depend on the time step, once the pipeline's detection loss is measured on a
tiling with a known answer and divided out?

Plan and predictions (written 16 Nov 2026 BEFORE the runs; only a 23 s pilot of the scripts on 13 to 40 frames was seen first:
it reproduced the stored exact control count, 119 swaps in 12 frames, and ran the reversed and shuffled copies through census.py):
- Data and chain unchanged: the fetched Bifrost planes, the 17 settings, census.py, tiles.py, the event logger. Steps 10, 20, 30,
  40, 60, 80 s; persistence windows P = 20, 30, 60, 120, 240 s (census.py's flicker window, measured in seconds; the two-step
  pairing window stays 60 s). For P below the step no reversal can be seen, so the count is the elementary count.
- Calibration: the moving-Voronoi control (seed 1, the 15 Nov sequences regenerated from their seed; the exact totals must agree
  with the 15 Nov logs) through the same chain at the same steps and P. Detection fraction f(step, P) = pipeline persistent swaps /
  exact persistent swaps (exact: Delaunay pairs lost between sampled frames, minus twice those regained at a sampled frame within P).
  Sun-like calibration: speed 1 (about 0.10 swaps per cell per minute), texture 0 and 1, mean of the two; the half-difference is the
  calibration uncertainty. Speed 2 is reported as a sensitivity.
- Corrected Sun rate R/f at each step, fitted against the step by a straight line and by a parabola; the intercept is the rate at
  step 0. Uncertainty per setting: fit standard error, line against parabola, and the calibration band, added in quadrature; the
  spread over the 13 field, threshold and smoothing settings is reported beside it and not folded in.
- Stability across P: the step-0 rates at P = 30, 60, 120, 240 s agree within their uncertainty (P = 20 has only two steps with a
  usable window and is reported, not judged).
- Controls, with the expected outcome:
  1. Held out: four new control sequences (seed 2, speeds 1 and 2, texture 0 and 1) corrected with the seed-1 fractions must give
     their exact step-0 rate within 10%. Expected to PASS at speed 1; speed 2 with the speed-1 calibration may miss (rate transfer).
  2. Time-reversed frames: a swap run backwards is a swap, so the persistent swap count must agree with the forward count within
     10% at every step (Sun primary setting and the speed-1 control; for the control the exact count of the reversed sequence is
     also computed). Splits and merges must exchange roles (reversed splits near forward merges).
  3. Shuffled frames (fixed permutation): the tracking breaks, so the swap count must change by more than a factor of 2 (expected
     to collapse, with births, deaths and clumps rising); the control's exact count of the shuffled sequence rises steeply (every
     frame pair far apart in time), so the pipeline must fall far below it.
- Expected outcome: the corrected Sun rate still falls with the step (the 15 Nov run found the Sun falling faster than the
  control); if so, the extrapolated value depends on the model and the verdict stays NOT CONFIRMED.
- Jobs: sun-stepcal (all settings and controls, compute machine), sun-holdout (seed-2 control, side machine); fit by
  stepcal_fit.py on the compute machine.

### Result (jobs sun-stepcal and sun-holdout, both FINAL ok; fit by stepcal_fit.py on the compute machine, FINAL ok)

VERDICT: **NOT CONFIRMED.** Dividing out the measured detection loss does not make the Sun swap rate step-independent: the
corrected rate still falls by 36 to 66% (median 51%) from step 0 to 80 s at P = 60 s, in every one of the 13 main settings, and
its step-0 value moves with P (0 of 13 settings agree across P = 30 to 240 s within their uncertainty). A straight line through
the corrected rates gives, at P = 60 s, **0.083 to 0.161 persistent swaps per cell per minute at step 0 (median 0.129) over the 13
settings, each +-9 to 15% (fit, line against parabola, calibration band), with a further 10 to 15% calibration error shown by the
held-out control**. This is an extrapolation of a falling line, not a plateau, so it is not quoted as a stable rate.

- **Reproduction.** The six seed-1 control sequences, regenerated from their seed, give exactly the 15 Nov exact totals (1071,
  1071, 2225, 2225, 4466, 4466). At 10, 20, 40, 80 s the Sun counts equal the 15 Nov census (primary setting 733, 626, 484, 305).
- **Detection fraction** f (Sun-like control, speed 1, P = 60 s), steps 10 / 20 / 30 / 40 / 60 / 80 s: texture 0: 0.87, 0.84,
  0.82, 0.76, 0.77, 0.62; texture 1: 1.15, 0.76, 0.72, 0.69, 0.59, 0.70. Full table for every speed, texture and P:
  results/stepcal/summary.md.
- **The Sun falls faster than the control.** Raw Sun rate at P = 60 s falls by a factor 2.1 to 3.7 from 10 to 80 s; the Sun-like f falls by a
  factor 1.5 (1.4 and 1.6 for the two textures). So most of the Sun's step dependence is not the detection loss measured on moving Voronoi tilings. The fits
  describe it: line R2 0.84 to 0.97 (relative rms 4 to 7%); the parabola's intercept differs from the line's by 0 to 11%.
- **Across P** (median step-0 rate of the 13 settings): P = 20 s 0.108, 30 s 0.117, 60 s 0.129, 120 s 0.118, 240 s 0.096 per cell
  per minute. The values rise and fall with P by up to 30%, more than the per-setting uncertainty (median 12 to 14% at P >= 60 s, 23% at
  30 s, 37% at 20 s). NOT stable across P.
- **Depth settings** (not in the 13): 0.103 at tau = 1, 0.082 at 0.2 Mm, 0.059 at 0.4 Mm (en, P = 60 s); the coarsening with
  depth found on 15 Nov stands after correction.

Controls against the criteria written before the runs:
1. **Held out (seed 2): FAIL at the 10% criterion.** Corrected with the matched seed-1 fractions, the step-0 rate comes out at
   0.90 and 0.93 of the exact value at speed 1 (P = 60 s; 0.86 to 0.93 over all P), 0.99 and 0.85 at speed 2. With the Sun-like
   calibration (speed-1 mean): 0.88, 0.94 (speed 1), 0.95, 0.66 (speed 2, line). The detection fraction itself varies by 5 to 15%
   between two realisations of the same tiling motion, so the calibration is good to about 15%, not 10%, and it does not carry
   from one rate to another with textured boundaries.
2. **Time reversal: PASS.** Persistent swaps reversed / forward 0.96 to 1.00 for the Sun and 0.98 to 1.01 for the control at every
   step; splits and merges exchange roles (Sun 10 s: forward 991 splits, 947 merges; reversed 947, 991). The exact count of the
   reversed control sequence equals the forward one within 3%.
3. **Shuffled frames: FAIL at the factor-2 criterion, and the reason matters.** At steps 20 to 80 s the Sun count falls to 0.34 to
   0.54 of the true-order count, but at 10 s it is 767 against 733. In shuffled frames the pipeline finds about 3 swap patterns per
   frame pair at every step (767 / 241, 339 / 120, ..., 103 / 30), while in true order the count per frame pair grows with the step
   (3.0 at 10 s to 10 at 80 s). Overlap matching of unrelated frames keeps some labels and the 2-2 pattern is then found among
   them; the clumps rise fourfold (3891 against 936). So the 2-2 detector alone is not specific to continuity: at 10 s, real
   frames and unrelated frames give the same number. This does not measure the false share in real frames (there matching holds for
   almost every cell), but it means the 10 s count has no independent bound on false swaps. For the control the exact count of a
   shuffled sequence is undefined by our persistence rule (regains exceed half the losses, so "lost - 2 x regained" goes negative),
   and the pipeline count changes by 0.82 to 2.09; not a usable control.

Conclusion: NOT CONFIRMED: correcting the Sun swap count by the moving-Voronoi detection fraction leaves a rate that still halves
from step 0 to 80 s and moves with P by up to 30%; the step-0 line value (0.08 to 0.16 per cell per minute, median 0.13 at P = 60 s,
+-9 to 15% per setting plus about 15% calibration) is an extrapolation, not a stable rate.

Next (decided): the Sun loses more swaps with the step than a moving Voronoi tiling does, so the missing ones are short-lived
swaps or swaps absorbed into splits and merges, both of which the Voronoi control lacks. The calibration needs a control that has
splits and merges (the scaling-state froth of the event-logger study drawn as images, with its exact T1 list), and the counting
needs a continuity test that unrelated frames fail (a swap counts only if all four cells are matched with overlap above a fixed
share). The unpaired lost and gained contacts (lead 1) are still unresolved.

Files: scripts/stepcal_prep.py (reversed and shuffled copies), stepcal_matrix.sh (job sun-stepcal), stepcal_holdout.sh (job
sun-holdout), stepcal_fit.py (fits, controls, tables, figure); results/stepcal/ (census JSON per setting and control, summary.md,
summary.json, logs), results/figures/sun_stepcal.png (left: raw Sun rate; middle: corrected rate with the line to step 0; right:
detection fractions, held-out sequences as crosses).

## Swaps traced through depth (16 Nov 2026; DICTO's diagnosis, open item 3 of studies/2026-11-16-scutoid-interactions)

DICTO, 16 Nov 2026: "the same initial problem as the shadows of the queens". A picture of the surface is a shadow of a 3D flow; as
in the Queens' shadows, only cell walls that run along the line of sight (upright walls) stay sharp, and tilted walls smear and
make false neighbour changes. The shuffled-frame control above (unrelated frames gave as many 2-2 patterns as real ones at 10 s)
says the detector reads something other than continuity. Test: count a swap only when the same 2-2 change is seen at the
adjacent depths of the 3D simulation, i.e. only between cells whose walls stand upright through the layers.

What the data are (checked 16 Nov at the archive, before any run). The run en024048_hion is public in full 3D: 242 snapshots
(303 to 544, 10 s apart, 40 min), 17 variables per snapshot (ux, uy, uz, lg T, lg rho, lg p, lg e, three field components,
electron and hydrogen populations), one FITS file of 504 x 504 x 496 float32 (504 MB) per variable and snapshot, so 122 GB for
uz alone and about 2 TB for everything. Grid 48 km horizontally, 19 km vertically near the surface (19 to 100 km over the box).
The archive gives free access; it asks users to acknowledge the Hinode mission ("Hinode is a Japanese mission developed and
launched by ISAS/JAXA, with NAOJ as domestic partner and NASA and STFC (UK) as international partners. It is operated by these
agencies in co-operation with ESA and NSC (Norway).") and the run is cited as Carlsson et al. 2016, A&A 585, A4, the code as
Gudiksen et al. 2011, A&A 531, A154. No other licence text was found on the archive's pages. Planes are read by HTTP range
requests (one plane = 1 MB), so the whole horizontal box and the whole 40 min can be kept and only the depth range is cut:
226 cells over 40 min with a lifetime of about 9 min is about 1000 cell lifetimes, well over the 200 asked for.

A fact that matters for the diagnosis: the census above did not use emergent intensity. Its cells were already cut from the
vertical velocity uz on horizontal planes of the 3D cube at fixed depths (0, 0.1, 0.2, 0.4 Mm below the mean tau = 1 height), and
the shuffled-frame failure was measured on the 0.1 Mm plane. So the projection smear of a shadow is not what the earlier
detector read; what the depth trace can still test is whether requiring the same change at neighbouring depths removes the
false swaps.

Plan (written before the runs; only a pilot of the scripts on 40 frames and one reproduction run was seen first):
- Depths: 0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4 Mm below the mean tau = 1 height (grid planes 82, 79, 77, 74, 72, 66, 61; spacing
  50 km in the top 200 km, then 100 km); 0.05, 0.15 and 0.3 Mm are fetched new (scripts/fetch_depths.py, 726 planes, 0.7 GB).
- Cells: upflow cells bounded by downflow lanes in uz (the 15 Nov primary setting: threshold mean + 0.25 std, smoothing 1.5
  pixels, periodic marker watershed), tracked through time at each depth with the census.py rule unchanged (pairing, two-step
  swaps, persistence P = 60 s). Reproduction: at 0.1 Mm the per-depth counts must equal the census (733, 626, 484, 305 at 10, 20,
  40, 80 s; 767 for the shuffled frames at 10 s).
- Linking across depth at every frame: mutual largest pixel overlap of the label maps of adjacent depths. Walls standing upright:
  the share of contacts at one depth whose linked pair also touches at the next depth.
- Counted swap ("upright"): a persistent swap at depth d whose same 2-2 change (lost pair and gained pair of the linked cells) is
  a persistent swap at every adjacent depth in the set, within max(30 s, one step) in time. Also reported: the plain per-depth
  counts, the counts confirmed at each neighbour, a looser 'near' match (any swap within 10 pixels and the time tolerance), and
  how deep a swap of the top plane reaches by chains of confirmations.
- Steps 10, 20, 30, 40, 60, 80 s; frame orders real and shuffled (the same permutation as the step-0 section, seed 7, applied to
  every depth alike).
- Controls and criteria: (1) SHUFFLED: the upright count of real frames must exceed that of shuffled frames by at least a factor
  of 3 at every step; (2) STEP: the upright rate from 10 to 80 s must change much less than the plain rate did (plain at 0.1 Mm:
  -58%); we call it flatter only if the change is within 20%; (3) the moving-Voronoi detection fraction (Sun-like, P = 60 s, from
  results/stepcal/summary.json) is applied to the plain per-depth counts as before.
- Prediction: adjacent planes 50 km apart are strongly alike, so a false 2-2 pattern from overlap matching of unrelated frames at
  one depth is likely to appear at the next depth too: we expect the shuffled control still to FAIL the factor-3 criterion at
  10 s, while the depth rule removes part of the real swaps as well; the verdict would then stay NOT CONFIRMED.
- Jobs: sun-3d-fetch (planes), sun-3d-trace (segmentation, links, tracks, combine), compute machine.

### Result (job sun-3d-trace, FINAL ok; figure by fig3d.py on the compute machine, FINAL ok)

VERDICT: **NOT CONFIRMED.** Requiring the same 2-2 change at the adjacent depths does not separate real swaps from false ones:
at 10 s, real frames give only 1.2 to 1.7 times as many upright swaps as shuffled frames in the top 0.2 Mm (criterion: 3), and the
upright rate falls with the step as steeply as the plain rate (-54 to -63% from 10 to 80 s, against -57 to -59%).

- **Reproduction.** At 0.1 Mm the per-depth counts equal the census: 733, 626, 484, 305 at 10, 20, 40, 80 s; shuffled 767 at 10 s.
- **Data used.** en024048_hion, uz on 7 planes (0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4 Mm below the mean tau = 1 height), the whole
  24 x 24 Mm box, all 242 snapshots (40 min, 10 s); 0.7 GB fetched new. Cells per plane 270, 247, 226, 199, 182, 143, 121.
- **Walls standing upright.** Between adjacent planes in the top 0.2 Mm, 86 to 90% of cells are linked (mutual overlap) and 78 to
  83% of contacts keep their linked pair in contact one plane down; from 0.2 to 0.4 Mm only 69 to 71% and 51 to 55%. Below 0.2 Mm
  the tiling itself fails (torus Euler bad in 41 of 242 frames at 0.3 Mm, 146 of 242 at 0.4 Mm), so the deep planes count little.
- **Swaps at depth (10 s, P = 60 s).** Plain persistent swaps per plane 988, 838, 733, 617, 540, 373, 257 (0.091 down to 0.053 per
  cell per minute; corrected by the moving-Voronoi detection fraction 0.090 to 0.052). Confirmed one plane down: 442 of 988 at the
  top; at 0.1 Mm, 463 confirmed above and 317 below; upright (confirmed at both neighbours) 283, 232, 181 at 0.05, 0.1, 0.15 Mm,
  i.e. 0.026 per cell per minute at 0.1 Mm, a third of the plain rate. Of the 988 top-plane swaps, 442 reach 0.05 Mm, 281 reach
  0.1 Mm, 151 reach 0.15 Mm and 95 reach 0.2 Mm by chains of confirmations.
- **Control 1, shuffled frames: FAIL.** Upright swaps real / shuffled at 10, 20, 30, 40, 60, 80 s: at 0.1 Mm 1.69, 2.42, 3.57, 2.62,
  3.41, 3.31; at the top plane 1.22, 2.09, 2.94, 3.05, 3.11, 3.06 (plain counts: 0.96, 1.85, 2.30, 2.23, 2.25, 2.96 at 0.1 Mm). The
  depth rule raises the ratio by about a factor 1.5 to 1.8 at every step but does not reach 3 at 10 and 20 s. Unrelated frames are
  confirmed across depth almost as often as real ones (363 of 1041 shuffled top-plane swaps against 442 of 988 real), as
  predicted: a false 2-2 pattern from overlap matching of unrelated frames repeats on the next plane, 50 km down, because the
  planes are alike.
- **Control 2, time step: FAIL.** Upright rate from 10 to 80 s: -55% (top), -62% (0.05), -63% (0.1), -54% (0.15), -57% (0.2);
  the plain rate falls -57 to -59% at the same depths. Not flatter.
- **Control 3, moving-Voronoi calibration** on the plain per-depth counts: the corrected rate still falls 34 to 37% from 10 to 80 s
  in the top 0.2 Mm (43% and 63% at 0.3 and 0.4 Mm), as in the step-0 section.
- A looser rule (any swap within 10 pixels and the time tolerance on the neighbouring planes) gives counts about 20 to 40% above
  the strict rule (544 against 442 at the top plane, 325 against 232 at 0.1 Mm, 10 s) and real / shuffled 1.3 and 1.8:
  the same failure.

The diagnosis from shadows does not fit these data: the cells were never cut from a picture of the surface but from velocity on
horizontal planes of the cube, and four of five walls do stand upright through the top 0.2 Mm. What makes unrelated frames give
swaps is the overlap matching between frames, and that error is the same on neighbouring planes.

Conclusion: NOT CONFIRMED: a swap seen at the same place on the neighbouring planes is still found almost as often in shuffled
frames at 10 s (real / shuffled 1.2 to 1.7, criterion 3), and its rate halves from 10 to 80 s like the plain count; the upright
rate at 0.1 Mm, 10 s (0.026 per cell per minute) is not a stable number.

Next (decided): the depth rule tests the walls, the shuffled control tests the time matching, so the time matching has to be made
specific first: a swap counts only if all four cells are matched frame to frame with overlap above a fixed share (unrelated frames
must fail it), calibrated on a control with splits and merges (the scaling-state froth drawn as images with its exact T1 list).
The depth rule can be added on top once that passes.

Files: scripts/fetch_depths.py (planes 0.05, 0.15, 0.3 Mm), trace3d.py (seg, link, track, combine), trace3d_job.sh (job
sun-3d-trace), fig3d.py; results/trace3d/ (summary.md, summary.json, tracks.jsonl, logs), results/figures/sun_3d_trace.png (the
0.1 Mm plane at snapshot 433 in the element colours; rings: swaps of the 10 minutes around it confirmed at 0.05 and 0.15 Mm, 63;
grey dots: swaps seen at 0.1 Mm only, 145). Segmentations, links and track files stay on the compute machine (data/trace3d, 0.8 GB).
