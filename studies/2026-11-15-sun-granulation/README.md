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
10. **The skeleton without swap matching** (16 Nov, DICTO's framing; section "The skeleton: persistence or reappearance"): corners
   do NOT outlive the cells (half-life 220 s against 540 s for cells, NOT CONFIRMED); vanished corners re-form at the same place
   within a minute 5.6 times as often as chance (CONSISTENT), and the cells at a corner are renewed while it stays (0.64 per minute,
   CONSISTENT); no cycle of local recurrence, only a box-wide oscillation of 7 to 8 min.
11. **Space-time slicing at a tilt** (16 Nov, DICTO's question; SCOPE and pilot only, section "Space-time slicing at a tilt"): the
   corner argument of #104 Theorem 1 carries over to a simple space-time cell complex; births, swaps and deaths per volume are fixed
   in every generic direction only if the cells are convex in space-time. A space-time Poisson-Voronoi block shows it exactly
   (within 2% over 9 directions). The Sun's tracked cells are balls but not convex at a tilt, and the time direction is the
   non-generic one (2.5 times fewer swaps than the tilts); the 3D connected components of upflow percolate. Full run waits for DICTO.

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
0.1 Mm plane at snapshot 433 in the five Kaleidohedra app colours (violet, blue, green, red, yellow); rings: swaps of the 10 minutes around it confirmed at 0.05 and 0.15 Mm, 63;
grey dots: swaps seen at 0.1 Mm only, 145). Segmentations, links and track files stay on the compute machine (data/trace3d, 0.8 GB).

## The skeleton: persistence or reappearance (16 Nov 2026; DICTO's framing)

DICTO, 16 Nov 2026: "better framing can still be achieved with the sun, maybe there is a persistence, or reappearance of
structures that reappear in cycles"; sharpened the same day: "it's a reappearance that seems to be persistence". Swap counting
failed its shuffled-frame control because frame-to-frame matching of cells makes false swaps. Persistence and recurrence of the
skeleton need no swap matching: cells come and go, but the walls (downflow lanes) and corners may persist, or vanish and re-form
at the same place. Shuffled frames should show neither.

Plan and predictions (written 16 Nov 2026 BEFORE the run; only pilots on 24 and 40 frames were seen first, and their numbers
are stated in the predictions):
- Data: en024048_hion, uz at 0.1 Mm below the mean tau = 1 height first (where the census reproduces), then 0 and 0.2 Mm, all
  242 snapshots (10 s, 40 min); qs024048_by3363 at 0.1 Mm (101 snapshots) as a second run. Cells: the census label maps of the
  depth trace (threshold mean + 0.25 std, smoothing 1.5 pixels); for qs segmented with the same rule.
- Objects (scripts/skeleton.py): lanes = pixels with downflow (smoothed uz < 0); corners = junctions of the tiling (2 x 2 blocks
  where three or more cells meet, blocks within one pixel merged) with the cells that meet there; downflow sinks = local maxima
  of downflow speed (4 pixels apart, faster than 1.5 standard deviations); cells tracked by mutual largest overlap (the census
  rule) and by their centres.
- Persistence: position tracking by mutual nearest neighbours within r = 96, 144, 192 km (2, 3, 4 pixels; 144 km primary).
  Two lifetimes: number-weighted (tracks born after the first frame, Kaplan-Meier median with the end of the run as censoring)
  and time-weighted (the half-time of S(tau), the share of the objects present at a frame that are still present tau later;
  no truncation bias).
- Sites (DICTO's sharpening): corner tracks joined into one site when a new track starts within r of where the old one ended,
  at most G = 30, 60, 120 s later (60 s primary). An apparently persistent site spans at least 5 min; it is (a) continuous with
  the same cells (at least two of the cells meeting there at its first frame still meet there at its last; strict variant: the
  set never changes), (b) continuous with renewed cells (at most one kept), or (c) intermittent and re-formed (absent for at
  least one sampled frame). Reported per site: gaps, gap durations, share of the span absent, distinct cells against span.
- Recurrence: share of corner-track ends followed by a new corner within r and G, and share of new cells (overlap rule) born
  within r of a cell that died in the preceding 60 s, each against a uniform random place (same number, same times) and against
  a time-shifted null (the same places with the starts or deaths taken half the run away in time: keeps any fixed spatial
  pattern, removes continuity in time); share of a new cell's area over a place held by a corner lasting 5 min or more, against
  the share of the whole box so covered. Families of fragmenting granules (after Roudier and co-workers): a cell's descendants
  by splits (main parent share >= 0.5), family lifetime against single-cell lifetime; split-and-merge genealogy reported beside it.
  Lanes at fixed pixels: autocorrelation over lag up to 20 min, power spectrum (Hann window, mean over pixels), gaps in presence
  of pixels that are lane in at least half the frames; the uz spectrum on the same pixels for any p-mode band.
- Controls and criteria: (1) SHUFFLED frames (seed 7): the corner half-life must fall to about one frame and the re-formation
  and births-near-deaths ratios to the time-shifted null (about 1). (2) TIME-REVERSED frames must keep the position-track
  statistics within 5% (mutual nearest neighbours are symmetric, so this checks the code more than the Sun). (3) MOVING VORONOI
  (control_voronoi.py, seed 1, speeds 1 and 2, texture 0 and 1, regenerated from its seed): exact corners are the circumcentres
  of the periodic Delaunay triangles; their combinatorial lifetimes, position-tracked lifetimes and site classes are the known
  answer the pipeline must recover. (4) STABILITY: half-lives within 30% over steps 10 to 80 s and over r = 96 to 192 km.
- Verdict per quantity: ESTABLISHED if it passes (1), (2), (4) and the control (3) recovers the known answer; CONSISTENT if it
  passes (1) and (2) but not (4); NOT CONFIRMED if it fails (1) or goes against the prediction.
- Predictions: (a) the corners outlive the cells (corner half-life at r = 144 km longer than the cell half-life). (3) Of the
  apparently persistent corner sites, about 50% continuous with the same cells, 25% renewed, 25% re-formed (re-formed below one
  third), strictly unchanged cells about 10% (the 40-frame pilot gave 50 / 25 / 25 and 11%); in shuffled frames more than 90%
  re-formed; for exact Voronoi corners fewer than 5% re-formed. Re-formation and births near deaths at least twice the
  time-shifted null in real frames. The lane autocorrelation decays without a secondary maximum (no cycle); a p-mode peak near
  3 mHz, if any, shows in uz and not in the lane mask.
- Job: sun-skeleton (compute machine; 52 tasks); tables by scripts/skeleton_combine.py; figure by scripts/skeleton_fig.py.

### Result (jobs sun-skeleton and sun-skeleton2, both FINAL ok; tables by skeleton_combine.py, figure by skeleton_fig.py)

A second pass (job sun-skeleton2, plan written before it ran) was added after reading the first results: the first-pass
re-formation test was biased against re-formation at the next frame (a corner within r at the next frame is usually linked, so
it cannot count as a new start), which showed as a ratio 0.36 in shuffled frames at 80 s. The second pass counts only true
vanishings (no corner within r at the next frame) and compares with the same conditional event at the same place at least 10 min
away; it also measures families as presence, and repeats the lane statistics with a fault fixed (the gap count of lane pixels
read a byte as a flag and gave zero gaps everywhere).

VERDICT per quantity (0.1 Mm below mean tau = 1 first; r = 144 km, G = 60 s unless stated; en = en024048_hion, qs = qs024048_by3363):

1. **Corners outlive the cells: NOT CONFIRMED (against the prediction).** Time-weighted half-lives at 0.1 Mm: corners 220 s, corner
   sites (gaps up to 60 s joined) 280 s, downflow sinks 140 s, lane pixels (autocorrelation e-fold) 190 s, cell centres tracked by
   the same rule 150 s, but cells tracked by overlap (the census rule) 540 s. The skeleton's corners outlive the cell CENTRES
   (x1.5) but not the cells: a granule keeps its identity 2.5 times longer than any one of its corners keeps its place. The same at
   0 Mm (220 / 280 against 580 s), 0.2 Mm (180 / 220 against 360 s) and in qs (140 / 170 against 420 s). Number-weighted
   Kaplan-Meier medians of tracks born during the run: corners 110 s, sinks 100 s, cell centres 100 s, cells 150 s.
2. **Corner persistence itself (half-life about 3.5 min): CONSISTENT.** Shuffled frames: 10 s (one frame) at every plane, PASS;
   time reversal: half-lives identical, PASS; tolerance r = 96 / 144 / 192 km: 190 / 220 / 230 s (21%), PASS; step 10 / 20 / 40 /
   80 s: 220 / 220 / 200 / 160 s (37%), FAIL at the 30% criterion. Moving Voronoi: the pipeline gives 840 s for exact corners whose
   half-life is 970 s (speed 1, no texture) but 200 s with texture, so the Sun value is a lower bound of unknown size.
3. **Apparent persistence split (DICTO's three classes): NOT CONFIRMED as a measured split.** Of 1240 corner sites at 0.1 Mm that
   span at least 5 min (median span 550 s): (a) continuous with the same cells 32%, (b) continuous with renewed cells 33%, (c)
   intermittent and re-formed 35%; strictly unchanged cells 6%. Prediction 50 / 25 / 25 with c below one third: missed. 0 Mm 33 /
   31 / 35, 0.2 Mm 24 / 37 / 39, qs 34 / 27 / 38. The gaps of class (c) are short: median 20 s (1 to 2 frames), 0.46 gaps per site,
   2.1% of a site's span absent; with G = 120 s the gaps up to 2 min are spread evenly (166, 121, 104, 175, 147 gaps in the bins up
   to 15, 25, 35, 65, 125 s). Shuffled frames: 100% re-formed, PASS; reversal equal, PASS; but the share (c) falls from 35% to 14%
   from 10 to 80 s and moves 23 to 45% with r, and the pipeline itself makes moving-Voronoi corners look intermittent (21% at 10 s
   without texture, 76% with texture, against 1 to 7% exact). So (c) at 10 s cannot be told from detection dropouts. What holds:
   at least two thirds of apparently persistent corners are present in every frame, and the absent time is about 2%.
4. **Turnover (corners stay while their cells are renewed): CONSISTENT.** Distinct cells meeting at a persistent corner site: median
   6 over its span, 0.64 per minute at 0.1 Mm (0.63 at 0 Mm, 0.75 at 0.2 Mm, 0.76 qs); unchanged over steps 10 to 80 s (0.60 to 0.64),
   over r (0.63 to 0.65) and under reversal; shuffled frames 3.1 to 3.5 per minute. Moving Voronoi: exact 0.20 (speed 1) and 0.30
   (speed 2) per minute, pipeline 0.27 to 0.49, so the pipeline adds up to about 0.2 per minute and the control does not recover
   the known value; even so the Sun's corners renew their cells at least about 1.5 times as fast as a Voronoi tiling at a Sun-like
   swap rate. Not ESTABLISHED because the control overestimates.
5. **Re-formation at the same place after a true vanishing: CONSISTENT.** A vanished corner is back within 144 km inside 60 s in
   23% of cases, against 4.1% at the same place 10 min or more away: ratio 5.6 (0 Mm 5.2, 0.2 Mm 6.8, qs 4.8; downflow sinks 4.7).
   Shuffled frames 1.03 at every plane, PASS; reversal 4.8, PASS; r = 96 / 144 / 192 km 6.6 / 5.6 / 5.4, PASS; window 300 s 2.4;
   step 10 / 20 / 40 / 80 s 5.6 / 4.7 / 2.4 / 1.8, FAIL (falls with the step but stays above 1). So corners do re-form where they
   vanished, beyond what a fixed spatial pattern gives; most of it is within a minute.
6. **New granules born where one died: NOT CONFIRMED.** Births (overlap rule) within 144 km of a death in the preceding 60 s: 4.0%
   against 0.3% (time-shifted null) at 10 s, but 0 at 80 s at every plane; this is the labelling flicker of splits and merges,
   not recurrence. **Born at a persistent corner: NOT CONFIRMED** (share of a new cell's area over a corner place held 5 min or
   more 0.056 against 0.049 for the whole plane, x1.1). In reversed time (births become deaths) the same share is x2.6 at 10 s and
   x1.6 at 80 s: granules VANISH over long-lived corner places; they are not born there.
7. **Trees of fragmenting granules outlive single granules: CONSISTENT.** Families by splits (main parent share 0.5 or more; after
   Roudier and co-workers), counted as presence: at 0.1 Mm 93 families per frame against 226 cells; still present after 20 min:
   51% of families (half-life beyond the 20 min window) against cell half-life 540 s; 0 Mm and 0.2 Mm the same (52%); qs half-life
   600 s against 420 s. Unchanged from 10 to 80 s (51 to 52% at 20 min); shuffled frames 6% at 20 min. Reversal turns split trees
   into merge trees and changes the qs value (1000 s), and the moving-Voronoi control has no splits, so there is no known answer.
   The split-and-merge genealogy joins almost the whole plane into one family within 40 min (1 to 6 families per frame), so it says
   nothing. Tracks born during the run: families KM median 150 s against 150 s for single cells (most new cells are small split
   pieces). Roudier et al. 2003 report families living hours in an 11 h series; our 40 min run cannot reach that.
8. **A cycle in the recurrence at fixed points: NOT CONFIRMED for local structures; the only cycle is box-wide.** The lane
   autocorrelation at fixed pixels decays with e-fold 190 s (170 to 200 s at all planes, both runs) to 0.07 at 10 min and 0.03 at
   20 min. It has a small secondary maximum at 890 to 900 s (bump 0.03 to 0.09) in all four quadrants of the en planes, but it
   vanishes when the lane share of the whole plane is removed frame by frame: then the decay is monotone at every plane. The whole
   plane oscillates: the lane share of en swings between 0.26 and 0.53 (0.1 Mm) with a period of 400 to 480 s (spectral peak 2.07 to
   2.48 mHz, resolution 0.41 mHz; autocorrelation of the share -0.9 at 3.5 min, +0.8 at 7.5 min), in step with the plane-mean uz, at
   0, 0.1 and 0.2 Mm alike; qs shows it at 505 s (1.98 mHz) and weaker. A horizontally uniform oscillation is a mode of the whole
   simulated box (presumably acoustic), with a period of 7 to 8 min, below the solar 5-minute band (3.3 mHz). It is not a
   reappearance of individual structures. The uz at fixed pixels shows a mild excess at 3.7 to 5.8 mHz (x1.5 to 1.9 over a power
   law), the p-mode band; the lane mask does not (x1.1 to 1.4 at the box-mode frequency). Lane pixels that are lane in at least half
   the frames are absent 36% of the time and almost all have gaps (95% at 0.1 Mm; qs 59%): the network at a fixed pixel comes and goes.

Controls against the criteria written before the runs: (1) shuffled frames: corner, sink, site and lane half-lives fall to one
frame at every plane and step, site class (c) to 100% (85 to 94% at 80 s), re-formation ratio to 1.02 to 1.06 and births-near-deaths ratio to 0.89 to 0.98: PASS. (2) Time
reversal: half-lives equal, site classes within 1%, turnover equal: PASS (number-weighted medians within one frame). (3) Moving
Voronoi: exact corner half-lives 970 s (speed 1) and 350 s (speed 2), triangles change at 190 to 290 s (KM median); the pipeline
recovers corner persistence within 15% without texture and falls to 160 to 200 s with texture; it invents intermittency and
turnover (see items 3 and 4). (4) Stability: over r PASS for half-lives, re-formation and turnover; over the step FAIL for corner
and sink half-lives, site classes and re-formation, PASS for turnover, cell and family persistence.

Conclusion: the frame "cells come and go, the walls and corners persist" is not what this simulation shows: a granule keeps its
identity about 9 min, its corners keep their places about 3.5 min and the lanes at a fixed pixel decorrelate in about 3 min. What
DICTO's sharpened idea finds is real but short: corners that vanish come back at the same place within a minute five times more
often than chance, and the cells meeting at a corner are replaced while the corner stays (about 0.6 new cells per minute). The
reappearance that looks like persistence is mostly continuous presence with brief dropouts; a longer recurrence, and any cycle,
is not seen in 40 min, apart from an oscillation of the whole simulated box with a period of 7 to 8 minutes.

Next (decided): the families (item 7) and the box-wide oscillation (item 8) are the two leads; a longer series is needed for
both (the qs run is 17 min, en 40 min). A moving-Voronoi control with texture matched to the Sun's lanes would bound the
detection share of class (c) and of the turnover.

Files: scripts/skeleton.py (feat, anal, anal2, voro), skeleton_job.sh (job sun-skeleton), skeleton_job2.sh (job sun-skeleton2),
skeleton_combine.py, skeleton_fig.py; results/skeleton/summary.md, summary.json, anal2/, voro/; results/figures/sun_skeleton.png
(left: 12 x 12 Mm of the 0.1 Mm plane, lane share over a 10 min window, corner tracks of that window coloured by lifetime, dots on
tracks of 5 min or more; right: autocorrelation at fixed pixels with and without the box-wide lane share, and the box-wide share
itself; persistence S(lag) of corners, corner sites, cells and cell centres, corners in shuffled frames). The first-pass analysis
files (33 MB, with corner tracks) and the features stay on the compute machine (results/skeleton/anal, data/skeleton).
Prior art for this section: PRIOR_ART.md, "Persistence and recurrence of the granulation pattern" (Getling and Brandt 2002 asked
"persistence or recurrence?" of averaged intensity images; Roudier and co-workers' trees of fragmenting granules; Hoekzema and
co-workers' persistency regions).

## Space-time slicing at a tilt (16 Nov 2026; DICTO's question; SCOPE and pilot only)

DICTO, 16 Nov 2026: "are there scutoid structures that transcend persistence or recurrence, is it possible that time is not running
in a linear direction". In DICTO's #104 (Scutoid Tissues in Four Dimensions) a sweep through a simple 4-polytope gives a tissue
whose births, swaps and deaths are fixed by the h-vector, the same for every generic sweep direction; time is one sweep direction
among many. The test asked for: stack the granulation frames into one 3D space-time block, label the cells as 3D regions of the block,
cut the block by planes tilted away from the time axis, and see whether births, deaths and swaps per unit of swept volume stay fixed
across directions. This section is about the geometry of the block only; it makes no claim about physical time. DICTO approved the
scope on 16 Nov 2026; the full run waits for him.

### Theory: what carries over from #104, and on what conditions

Set-up. The block is the region (x, y, t) of the box; its cells are 3D regions that fill it. A sweep is a family of parallel planes
h = const, h(t, x) = t cos(theta) + (x / v) sin(theta), where theta is the angle between the plane's normal and the t-axis and v is a
speed that converts space into time (without it a tilt has no meaning: theta is an angle only in the coordinates (x / v, t)).

1. **#104 Theorem 1, the local part, carries over unchanged** to any *simple* 3D cell complex (four cells and four edges at every
   corner, three cells at every edge, two cells sharing at most one wall) cut by a *generic* plane family. Its proof only looks at
   one corner: when the plane passes a corner with i of its four edges below, the plane's tiling gains a three-sided cell (i = 1),
   makes one swap (i = 2) or loses a three-sided cell (i = 3), and nothing else changes. Here "generic" means: no edge lies in a
   plane of the family at a corner (no edge perpendicular to the normal), no two corners on one plane, and no plane tangent to a wall
   or an edge away from the corners.
2. **The global part (counts fixed by the h-vector) does not carry over as such.** In #104 the counts are the h-vector of the
   polytope because its boundary is a closed 3-sphere, its cells are convex (one lowest and one highest corner in every direction),
   and the Dehn-Sommerville relations hold. A space-time block has a boundary (the first and last frames, and the side walls of a
   sub-box) and no h-vector. What carries over is the counting argument of studies/2026-11-15-tissue-null-models (THEORY section 2,
   which extends #104 Theorem 1 to normal 3D tessellations): **if every cell is convex in the sweep direction** (one lowest and one
   highest point, both corners, in every direction considered), then
   births = number of cells whose lowest point lies inside the swept region, deaths = number whose highest point lies inside,
   swaps = corners inside - births - deaths.
   The corners and the cells are fixed objects of the block, so in a large block **births, deaths and swaps per unit volume tend to
   direction-independent values: births = deaths = cells per volume, swaps = corners per volume - 2 x cells per volume**, and swaps
   per birth = (corners per cell) - 2 = k/2 - 3 (k = mean number of neighbours of a 3D cell). The direction enters only through cells
   and corners cut by the block's boundary: a surface term, which falls as (block size)^-1. This is the exact analogue of #104's
   h1 = f3 - 4, h2 = f0 - 2 - 2 h1 (there the "boundary term" is the 4 cells at the lowest and highest corner). The g-theorem bound
   of #104 (swaps at least births) has no analogue here; the value for space-time Poisson-Voronoi cells is 4.77 swaps per birth.
3. **The speed scale v does not change the prediction.** Changing v is a linear map of the block; it keeps convexity, corners and the
   ratio of volumes. So for convex simple cells the densities are the same for every theta and every v. Any dependence on v in data
   is a sign that the cells are not convex in space-time, or of the sampling (below).
4. **For cells of any shape** (not convex, curved walls), stratified Morse theory gives one identity that holds in every generic
   direction: for each cell that does not touch the block's boundary and is a 3D ball, **(pieces born) - (pieces of the same cell
   that join) = 1** (its Euler characteristic; in general = Euler characteristic of the cell). A cell that is not convex in the
   sweep direction can show up in a plane as several pieces: a new piece can appear at a corner, on an edge (a two-sided lens), or
   inside a wall (an island), and pieces can join or split off. Births then include these extra pieces, and swaps are no longer
   corners - births - deaths: **for non-convex cells the counts depend on the direction**, and only the identity above, the corner
   count and the Euler formula of each plane (V - E + F = 2 with the outside as one cell) are fixed.
5. **Sampled blocks are not generic in the time direction.** The block is built from frames 10 s apart, so the plane theta = 0 sees
   every change of one frame step at once (clumps); and a cell label assigned by frame-to-frame tracking makes walls that lie exactly
   in a frame plane (where a split piece gets a new label). Tilted planes break these ties. So theta = 0 is the least generic
   direction of the block, and differences between theta = 0 and the tilts can come from this alone.
6. **Shuffled time.** A block built from frames in shuffled order is still a cell complex, so the theory predicts invariance for it
   too *if* it were simple, convex and generic. It is not: its cells are thin slabs with walls in the frame planes. So the shuffled
   block must break invariance through items 4 and 5 (direction-dependent counts, clumps at theta = 0), and a run in which it did not
   would show that the counts do not see the block's continuity at all. It is a control of the pipeline, not of the theorem.

What would count as the h-vector-like invariance in the Sun: births, deaths and swaps per volume in the core of the block equal at
theta = 0, 15 and 30 degrees and for v from half to twice the granule speed, within the spread of the Poisson-Voronoi control,
together with the Morse identity holding cell by cell. The theory says this happens only if the granules' space-time cells are
close to convex.

### Pilot plan (written 16 Nov 2026 BEFORE the pilot ran; scripts/spacetime_tilt.py, job sun-tilt-pilot)

- Sub-box 250 x 250 pixels (12 x 12 Mm) of en024048_hion, uz at 0.1 Mm below the mean tau = 1 height, all 242 snapshots (40 min).
  Core for counting: 24 pixels (1.1 Mm) in from the side walls and 30 frames (300 s) in from the first and last frame; the same core
  for every direction. Speed scale v = 3 km/s (a granule's diameter, 1.8 Mm, over its lifetime by the census, 558 s) and, at
  theta = 30 degrees, v = 1.5 and 6 km/s. Tilt in the x direction.
- Two labellings of the Sun block: (A) the task's: markers are the 3D connected components (in x, y, t) of upflow above mean + 0.25
  std (smoothing 1.5 pixels, as the census), and the block is filled by a 3D marker watershed of uz; (B) census tracks: the census
  cells with labels carried by the overlap rule (tiles.match), so a split piece gets a new label.
- Planes: one per frame step at fixed x (step 10 s cos(theta) in h); the part of a plane outside the block is one outside cell, so
  each plane is a sphere tiling. Pieces of one 3D cell keep their identity by overlap within that cell. Events by the shared logger;
  events touching the outside cell are boundary events and are not counted; counted events lie in the core. Also counted from the 3D
  identity alone (no logger): cell first appears, new piece of a present cell, piece splits off, pieces of one cell join, cell
  vanishes. Swaps undone by the same four pieces within 60 s (at fixed x) are flicker; persistent swaps are reported beside all.
- Block checks: cells that do not touch the block boundary are connected and balls (voxel Euler number 1); corners (2 x 2 x 2 voxel
  windows with four or more cells, clustered) with exactly four cells; Euler of every plane; the logger's balance; the Morse identity
  per interior cell.
- Controls (known answers): (1) a space-time Poisson-Voronoi block of the same size (seed spacing about 1.2 Mm, time scale 3 km/s,
  so cells are granule-sized and live about 7 min), voxel labels by the nearest seed; exact counts per direction from its Delaunay
  corners (corner index = edges going down, counted in the core); (2) a moving-Voronoi block (control_voronoi.py, 500 seeds, speed 1,
  seed 1: no cell is ever born or dies; every change at theta = 0 is a swap); (3) shuffled frames (seed 7) for labellings A and B.
  The #104 polytope sweeps themselves were already logged in two directions with the exact h-vector counts (event-logger study,
  validation (a)); they are the exact closed case and are not rerun.
- Predictions: (P1) Poisson-Voronoi exact: no corner of index 0 or 4; births, swaps and deaths per volume within 10% across the 3 x 3
  directions (theta 0/15/30, v 1.5/3/6), swaps per birth near 4.8. (P2) Poisson-Voronoi through the voxel pipeline: within 25% of the
  exact counts in every direction (voxel walls add flicker), Morse identity on at least 90% of interior cells. (P3) Moving Voronoi:
  interior births and deaths near 0 at theta = 0; at the tilts still few as long as the fastest seed is slower than v cot(theta).
  (P4) Sun, labelling A: the upflow markers connect through time into large families (the census found that splits and merges join
  the plane into a few families within 40 min), so the 3D cells are few, large and far from convex; we expect births per volume to
  change by more than 20% between theta = 0 and 30 degrees and with v, i.e. NO invariance; the Morse identity can still hold.
  (P5) Labelling B: walls in frame planes make theta = 0 non-generic; births at theta = 0 are mostly read as splits by the logger.
  (P6) Shuffled blocks: counts at theta = 0 dominated by clumps and very different from the tilts.
- Pilot size: 6 blocks (sunA real/shuffled, sunB real/shuffled, Poisson-Voronoi, moving Voronoi) x 5 directions = 30 slice runs,
  in parallel, cap 5 min.

### Pilot result (job sun-tilt-pilot, FINAL ok; tables by scripts/tilt_summary.py; results/tilt-pilot/)

The pilot ran twice: the first run counted a new cell twice when it first showed as two pieces in one plane (truth counts only;
the logger counts were unchanged). The second run is the one reported. Blocks took 5 to 21 s each, slice runs 2 to 58 s.
Core volume 2791 Mm^2 min in every run (10.1 x 10.1 Mm, 30.2 min). Directions: theta 0, 15, 30 degrees at v = 3 km/s, and theta
30 degrees at v = 1.5 and 6 km/s.

**Control 1, Poisson-Voronoi space-time block, exact (P1): PASS.** 2467 seeds, 927 cells. Corners in the core by index i (edges
going down), from the Delaunay tetrahedra, in all 9 directions (theta 0/15/30 x v 1.5/3/6): no corner of index 0 or 4; births
(i = 1) 285 to 291, swaps (i = 2) 1390 to 1400, deaths (i = 3) 285 to 293. Spread 2% or less; swaps per birth 4.79 to 4.91 (bulk
value for the typical cell 4.77). The corners are the same corners in every direction; only their index changes, and the counts stay.
This is the invariance the theory predicts, on a block where the answer is known.

**The voxel pipeline on the same block (P2): partly.**

| Poisson-Voronoi, core | theta 0 | 15, v 3 | 30, v 3 | 30, v 1.5 | 30, v 6 |
|---|---|---|---|---|---|
| exact births / swaps / deaths | 291 / 1394 / 287 | 287 / 1399 / 286 | 285 / 1400 / 287 | 289 / 1390 / 293 | 287 / 1400 / 285 |
| cell first appears / vanishes (3D identity) | 292 / 289 | 286 / 286 | 281 / 291 | 285 / 296 | 286 / 290 |
| logger swaps, all (persistent) | 749 (719) | 757 (716) | 812 (747) | 954 (809) | 751 (706) |
| logger births / deaths / clumps | 168 / 174 / 607 | 165 / 169 / 706 | 166 / 162 / 829 | 182 / 190 / 985 | 161 / 157 / 713 |
| Morse identity holds (of 333 interior cells) | 308 | 302 | 303 | 258 | 302 |

Births and deaths read from the 3D identity match the exact counts within 2% in every direction. The logger finds only 52 to 58%
of the swaps (69% at v = 1.5); the rest fall into clumps, because at one plane step (10 s) about nine corners pass through the core at
once. The logger's persistent swap count is stable across directions within 6% at v = 3 and 6 km/s, and 13% higher at v = 1.5,
where the plane crosses 1.4 frames per pixel and the staircase sampling adds pieces. Morse identity: 91 to 92% of interior cells
(77% at v = 1.5); the failures are cells that are not voxel balls (24 of 333 have voxel Euler number other than 1). Every plane passes
Euler; the balance holds in every step.

**Control 2, moving Voronoi (P3): PASS for births, with a detection loss at the tilts.** 500 seeds, 256 corners in the core (247
with exactly four cells). Fastest seed 2.4 km/s in x, slower than v cot(theta) in every direction run (2.6 km/s at 30 degrees and
v = 1.5). Core births + deaths: 0, 5, 9, 21, 4 (theta 0; 15; 30 at v 3, 1.5, 6). Swaps (all): 193, 181, 156, 118, 186, i.e. 75% of the
corners at theta 0 and 46 to 73% at the tilts.

**Sun, labelling A (the 3D connected components of upflow) (P4): it percolates; nothing to test.** The 55 upflow markers of the
12 x 12 Mm x 40 min block join into one that holds 66% of all upflow voxels; the block has 47 cells, 2 of them inside, 9 corners in
the core and **no swap in any direction**. Planes fail Euler in 131 to 162 of 242 to 700 (the giant cell's pieces have holes). With
shuffled frames the largest marker holds 99.9% of the upflow voxels.

**Sun, labelling B (census tracks): a block of balls, cut into non-convex pieces at a tilt.** 464 cells; all 211 cells inside the
block are connected and balls (voxel Euler number 1); 714 corners in the core, 697 (98%) with exactly four cells. Convex-cell
prediction for the swaps: corners - births - deaths = 714 - 149 - 149 = 416 (the voxel corner count finds 86% of the exact corners
in control 1, so this is a lower value).

| Sun B, core | theta 0 | 15, v 3 | 30, v 3 | 30, v 1.5 | 30, v 6 |
|---|---|---|---|---|---|
| cell first appears / vanishes (3D identity) | 149 / 149 | 147 / 145 | 146 / 142 | 150 / 354 | 148 / 144 |
| logger swaps, all (persistent) | 61 (36) | 156 (141) | 152 (135) | 172 (96) | 163 (147) |
| logger births / deaths | 23 / 41 | 89 / 104 | 90 / 108 | 161 / 177 | 90 / 102 |
| logger splits / merges / clumps / relabels | 67 / 58 / 65 / 0 | 134 / 133 / 352 / 69 | 162 / 162 / 469 / 186 | 323 / 311 / 746 / 237 | 142 / 140 / 361 / 78 |
| new pieces of a present cell / pieces joining | 0 / 0 | 185 / 58 | 358 / 69 | 508 / 112 | 198 / 61 |
| Morse identity holds (of 211) | 211 | 160 | 134 | 84 | 157 |
| planes failing Euler | 3 of 242 | 71 of 349 | 132 of 471 | 236 of 700 | 78 of 357 |

- The number of cells born and vanishing in the core is the same in every direction (146 to 150), but that holds for any block
  (each cell is counted once, at its lowest point) and is not the test.
- Swaps: theta = 0 gives 2.5 times fewer than the tilts (61 against 152 to 172). The time direction is the non-generic one here
  (theory item 5: tracking puts a split piece's new label on a wall that lies in a frame plane, and every change of a 10 s step
  lands on one plane): at theta = 0 the logger reads most births as splits (23 births against 149 cells born). Among the tilted
  directions at v = 3 and 6 km/s the swaps agree within 7% (persistent 135 to 147), about as well as in control 1; with about 150
  events each, the counting error alone is about 8%.
- The cells are not convex in space-time: a tilted plane cuts a cell into several pieces, more the larger tan(theta) / v (new pieces
  0, 185, 358 at theta 0, 15, 30 degrees at v = 3; 508 at v = 1.5, 198 at v = 6), and planes fail Euler (pieces with holes). So by
  theory item 4 the swap count is not expected to be fixed, and it is far below the convex prediction (about 150 found where 416 x
  0.55 = 230 would be detected if the cells were convex).
- The Morse identity fails beyond the control's digital baseline at the tilts (64 to 76% at v >= 3, 40% at v = 1.5, against 91% in
  control 1); at v = 1.5, 207 cells vanish from a plane and come back, i.e. the plane steps over thin parts of a cell. That is
  sampling: thin tails of shrinking granules lie between two frames.

**Control 3, shuffled frames (P6): PASS, it breaks everything.** Labelling B shuffled: 7307 cells (slabs one frame thick); cells
born in the core 2909 to 2954, but new pieces 0 at theta 0 against 32 812 to 69 064 at the tilts, logger births 75 against 352 to
1277, the Morse identity holds for 99% of cells at theta 0 and 0 to 2% at the tilts.

**Pilot verdict.** The theory carries over in the form stated (control 1: births, swaps and deaths of a convex simple space-time
complex are the same in every generic direction and for every speed scale, within 2%). The voxel pipeline reproduces the births
exactly but finds only about half the swaps, with a direction spread of about 6%. In the Sun, the 3D-connected-component cells
percolate (obstacle 1); the tracked cells are balls but not convex in space-time, so the h-vector-like invariance of swaps is not
expected and is not seen across theta = 0 and the tilts; among tilted directions at v >= 3 km/s the swap counts agree within the
counting error of this small block. Nothing here is a statement about physical time.

**Obstacles found.**
1. Percolation of 3D upflow components (labelling A as asked): one family holds two thirds of the upflow; needs markers that are
   not connected through time (higher thresholds, h-maxima, or per-frame markers linked only by mutual best overlap).
2. Units: theta is an angle only after choosing v. The theory's counts do not depend on v (control 1: identical exact counts at
   v = 1.5, 3, 6 km/s); the Sun's pieces and the pipeline's detection do (pieces x2.6 from v = 6 to 1.5 km/s), so a v-dependence in
   the Sun is a measure of non-convexity and of sampling, not a physical speed. The reference v = 3 km/s is the census granule
   diameter over lifetime; any v from 1.5 to 6 km/s should be reported.
3. Sampling: one plane per frame step at fixed x; at tan(theta) / v large, a plane jumps more than one frame per pixel (1.4 at
   30 degrees and 1.5 km/s) and steps over thin parts. Swaps that fall within one step become clumps (half of them in control 1).
4. Non-genericity of theta = 0 (frames, tracking walls in frame planes): theta = 0 is not a fair member of the comparison; the test
   is among tilted directions, with theta = 0 reported beside.
5. A sub-box is needed (a tilted plane is not periodic), and the core must stay far enough from the first and last frames that a
   plane's cut edge is at least one cell away: margin in time >= (1.5 Mm) tan(theta) / v. The pilot's 300 s meets this at v = 3
   and 6 km/s (289 s needed at 30 degrees and 3 km/s) but not at v = 1.5 km/s (577 s), which adds to the v = 1.5 differences above.
6. The tracked cells' count of corners (714) gives a convex prediction (416 swaps) that the data cannot reach while cells are
   non-convex; the swap count is then a property of the shapes, not of the h-vector.

### Full-run plan (not started; waits for DICTO)

- Job sun-tilt (plan file in the job system, written 16 Nov 2026); scripts/spacetime_tilt.py and scripts/tilt_pilot.sh extended
  to a task list. All four 12 x 12 Mm quadrants of the 24 x 24 Mm box as independent blocks (4 times the pilot volume), depths 0,
  0.1, 0.2 Mm below the mean tau = 1 height, en024048_hion (242 snapshots) and qs024048_by3363 (101 snapshots, 0.1 Mm, second run).
- Labellings: B (census tracks); A at marker thresholds 0.5, 1.0, 1.5 std, kept only where the largest marker holds under 5% of the
  upflow voxels (the percolation gate); A2: per-frame census markers linked through time by mutual best overlap only (no split or
  merge links), filled by a 3D watershed.
- Directions: theta 0, 10, 20, 30, 45 degrees; tilt towards +x, -x and +y; v = 3 km/s; at 30 degrees also v = 1.5 and 6 km/s
  (15 directions). Core margin in t raised to 60 frames (600 s) so that the plane's cut edge stays at least 1.5 Mm away at 45 degrees
  and v = 3 km/s; plane step dt cos(theta) and, as a sampling check, half that.
- Counts per core volume: cells born and vanishing (3D identity), new pieces and joins, logger swaps (all, persistent), births,
  deaths, splits, merges, clumps; corners; Morse identity per interior cell; Euler of every plane; balance.
- Controls that must PASS: (1) Poisson-Voronoi blocks, 5 seeds x seed time scale 1.5, 3, 6 km/s: exact corner counts invariant
  within 3% over all 15 directions; pipeline persistent swaps invariant within its own spread, which becomes the yardstick s_PV;
  (2) moving Voronoi (seeds 1 and 2): births and deaths at most 2% of swaps whenever the fastest seed is slower than v cot(theta);
  (3) time-reversed blocks: identical swap counts, births and deaths exchanged (a code check: reversal maps the block onto itself);
  (4) the #104 polytope sweeps (120-cell, truncated 120-cell, bitruncated 600-cell) logged in three more generic directions:
  exact h-vector counts (the closed, exact case). Controls that must FAIL: (5) shuffled frames (seeds 7 and 8), both labellings:
  the spread of swaps and births over the tilted directions must exceed 3 s_PV, and the Morse identity must fall below half its
  real-block rate.
- Size: about 120 blocks (Sun B 24, A and A2 up to 96 before the percolation gate, qs 8, Poisson-Voronoi 15, moving Voronoi 2) x 15
  directions = 1800 slice runs at 3 to 60 s each (pilot rate), about 6 CPU hours, 20 at a time: about 30 min wall, cap 1.5 h,
  memory under 10 GB.
- Predictions (from the pilot): Poisson-Voronoi exact invariant (PASS); Sun B: swaps per core volume equal over the tilted
  directions at v >= 3 km/s within s_PV, but not at theta = 0 or v = 1.5 km/s, and new pieces rising with tan(theta) / v: the cells
  are not convex in space-time, so no h-vector-like invariance; labelling A percolates up to at least 1.0 std.
- Verdict criteria (for the Sun's swap count, per labelling and depth): **ESTABLISHED** if swaps, births and deaths per core volume
  agree within s_PV over all tilted directions and all v from 1.5 to 6 km/s, in all four quadrants, the Morse identity holds at
  least at the control-1 rate, controls 1 to 4 pass and the shuffled control fails; **CONSISTENT** if they agree over the tilted
  directions at v >= 3 km/s only (or in some quadrants only), controls passing; **NOT CONFIRMED** if the tilted directions differ by
  more than 2 s_PV, or the shuffled control does not break the invariance.

Files: scripts/spacetime_tilt.py (blocks, checks, exact Poisson-Voronoi corners, tilted slicing and logging), scripts/tilt_pilot.sh
(job sun-tilt-pilot), scripts/tilt_summary.py (tables); results/tilt-pilot/ (blocks.jsonl, one JSON per block and direction, logs).
The blocks themselves (data/tilt/*.npz) stay on the compute machine.
