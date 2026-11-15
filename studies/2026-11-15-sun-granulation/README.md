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
3. Emergent intensity (the observable) instead of velocity planes: the archive's synthetic images, or a radiative transfer pass.
4. A real observation: Hinode SOT/BFI G-band quiet-Sun series (free, needs calibration), with the patch edge rule.
5. Supergranules: SDO/HMI flow maps (needs a registered account; ask DICTO) or a larger simulation box.
6. Ratio to compare with #104: swaps per birth there (h2/h1, e.g. 366/116 = 3.2); here births are absent and splits stand in.
