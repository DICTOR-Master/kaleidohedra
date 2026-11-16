# Scutoid interactions: one study of the scutoid streams (16 Nov 2026)

**SHELVED 16 Nov 2026 (DICTO: "yes shelve it").** The ladder that stands is rungs 1-3 (geometry, one contact at a time, exact null rates) with the compound-eye law on top; no natural rung is established (Sun: persistence, tilts, space-time scutoid tubes still running; froth law-built model gives 0.25, not 0.53, scaling state not reached; plates, clouds, eyes not confirmed). The title Microcosm and Macrocosm is kept for a later version, when a natural rung is established. Routes still open: the space-time scutoid tubes of the Sun, the larger froth run, the wasp eye.


Title (DICTO, 16 Nov 2026): **Microcosm and Macrocosm**: Scutoid studies from cells to stars, planets and the cosmos.

DICTO, 16 Nov 2026: "narrow our focus back to core study objectives and drop any avenues that are not supportive of the scutoid
interactions and pull what we have into a study that has as few loose ends to tie up as possible". Scope (DICTO): "im only talking
about scutoid matters". This study is a WRITE-UP of results already obtained: no new computation, no new data, no new jobs. Every
number is copied from the source study named in its row; each verdict is the source study's own, never upgraded.
Draft PDF: paper/DRAFT-scutoid-interactions.pdf (build: `sh build.sh`; data/results.json is the single source of the tables;
scripts/make_html.py checks that this README and the PDF carry the same rows and open items, FINAL ok).

## 1. Conclusion

**Established:** the geometry. In a generic sweep of a simple 4-polytope the slice is a tissue whose cells are born, swap neighbours
(the scutoid move) and die, counted exactly by the h-vector; in higher dimensions contacts are gained and lost one at a time (#104,
Theorems 1, 1′ and 2). The shared event logger recovers these counts exactly, and the null-model reference values for moving Voronoi
tilings are fixed exactly or by two methods that agree (2D T1 rate 3.04 ± 0.005 against the integral 3.058 ± 0.005; 3D 15.53 ± 0.07
against 15.61 ± 0.03). **Consistent, at the strength of computation:** generic moving toy foams change one contact at a time (30,758
events, none simultaneous); 3D grain growth obeys the contact identity. **Not confirmed:** the froth's macroscopic T1 per T2. A
froth built only from Plateau's and von Neumann's laws, with Rutenberg and McCurdy's own rules, gives 0.25 ± 0.02 at every cut-off,
half of their 0.53 ± 0.05 (the Potts lattice's 0.48 at rc = 1 pixel held only at that cut-off); its window is not yet in a tested
scaling state.
**Not established:** no natural tiling yet has a swap rate that is stable and comparable across scales (granules and cloud cells
depend on the time step or the settings; the plate agreement within the Müller model family does not carry over to an independent
history), and no scutoid has been observed in a real compound eye (the butterfly traces are not a test of the prediction). The
cross-scale comparison of the plan "One tissue, three scales" therefore cannot yet be made; the five open items lead to it.

## 2. One counting rule, one null model

**Counting rule** (studies/2026-11-15-event-logger: eventlog.py, pairing.py, rm_count.py). One logger and one tiling format for 2D and
3D, with Euler, triple-junction and balance checks and a negative control in every run. A swap is the 2-2 move. Three layers, fixed
before counting: *pairing* (lost contact a-b and gained c-d make one swap if the four cells are distinct, c and d both touched a and b
just before, and the times differ by at most W); *persistence* (a change counts only if the new state lasts at least P; a
back-and-forth within P cancels); *macroscopic* swaps by Rutenberg and McCurdy's own area rule (all four cells larger than
l² = rc √⟨A⟩). Pairing and persistence remove flicker but do not make raw swap counts step-independent: at a coarse step a swap falls
into the same interval as a neighbouring cell's vanishing.

**Null model** (studies/2026-11-15-tissue-null-models). Poisson-Voronoi throughout: moving seeds with linear motion for rates (2D T1
per cell per spacing 3.058 ± 0.005, simulated 3.04; 3D contact changes 15.61 ± 0.03, simulated 15.53), swept Poisson-Voronoi for
swaps per birth (24π²/35 − 2 = 4.7677; for sections of any normal 3D tessellation k̄/2 − 3). Coarsening froths: the literature value
0.53 ± 0.05 macroscopic T1 per T2 (Rutenberg and McCurdy, arXiv cond-mat/0502287) and 3/2 with side-shedding (Herdtle and Aref 1992).
Brownian seed motion gives no rate (counts scale as 1/δ); only the net change, which saturates, is frame-rate free.

**Streams with a different setting.** Earth: contacts counted per boundary on a fixed 15 km mesh, two-sided persistence 5 Myr (its own
scripts/swaps.py). Sun: persistence 60 s at 10 s steps. Clouds: two-sided persistence 10 min. 2D grains: exact events of the vertex
model, persistence by area fraction q. Void toy: exact event times. Compound eyes: Delaunay neighbour sets compared between depths, not
the logger. Jupiter: cyclic order of the published cyclone centres per epoch. Yew: the logger through an adapter (one section).

## 3. Results (one row per system)

| system (data) | swaps observed | null or expectation | verdict: source study's own wording | source (studies/) |
|---|---|---|---|---|
| Sweeps of simple 4-polytopes (theory check) (120-cell, truncated 120-cell, bitruncated 600-cell swept as tiling sequences; two generic directions) | births / swaps / deaths 116 / 366 / 116; 716 / 966 / 716; 716 / 2166 / 716, exact; truncated 600-cell: no pure swap | h1 / h2 / h3 of #104 Theorems 1 and 2 (same numbers) | **ESTABLISHED**: logger built and validated; all predictions held | 2026-11-15-event-logger (validation a); #104 |
| Null model: moving Poisson-Voronoi seeds, linear motion (2D and 3D periodic Voronoi, simulated and integrated) | 2D: 3.04 +- 0.005 T1 per cell per spacing (finest step); 3D: 15.53 +- 0.07 contact changes per cell per spacing; swaps per birth in a swept 3D Poisson-Voronoi 4.7669 +- 0.0006 | integrals 3.058 +- 0.005 and 15.61 +- 0.03; exact 24 pi^2/35 - 2 = 4.7677 | **ESTABLISHED**: SETTLED; two methods agree (simulation converges from below, 0.7% and 0.5% short at the finest step) | 2026-11-15-tissue-null-models |
| Space-time cell complexes with convex cells, swept at a tilt (theory and check) (theorem with proof (sun-granulation study, section 'The convex-cell theorem'); 15 space-time Poisson-Voronoi blocks (5 seeds x 3 time scales), 15 directions each (tilts 0 to 45 degrees towards three sides, speed scale 1.5 to 6 km/s), exact corners from the Delaunay tetrahedra; #104 sweeps in 3 more directions) | no corner of index 0 or 4 in any of 225 block-directions; births and deaths in every direction between the cells wholly inside the core and that number plus the cells straddling its boundary (15 of 15 blocks); swaps vary by at most 2.7% over the directions, births and deaths by 3.5 to 11.4% (small cores: 1 to 213 cells inside against 220 to 471 straddling); swaps per birth 4.03 to 5.06; the #104 sweeps exact in 9 of 9 | theorem (extends #104 Theorem 1): per unit volume births = deaths = cells and swaps = corners - 2 x cells, in every generic direction and for every speed scale v; swaps per birth k/2 - 3 = 4.77 for Poisson-Voronoi | **ESTABLISHED**: proved; the exact parts (corner indices 1 to 3, the boundary bound) hold in every block and direction; the planned 3% invariance of births and deaths fails in these small cores because of the boundary term the theorem bounds | 2026-11-15-sun-granulation (section: space-time slicing at a tilt); #104 |
| Toy moving 3D foams (Voronoi, power diagrams) (N = 512 cells, three generic motions, two time steps) | 30,758 contact changes, 0 simultaneous at a 1e-9 time floor, 0 clumps; lattice control caught (10 simultaneous) | one contact at a time (#104 Theorem 1' read for moving 3D tilings) | **CONSISTENT**: a computation, not a proof: checks the generic statement on these motions | 2026-11-15-cosmic-voids (item 1) |
| 2D dry froth: Potts lattice and law-built vertex froth (Potts 2048^2 torus (seed 2, scaling test passed); off-lattice froth from Plateau's 120 degrees, Laplace arcs and von Neumann's law with Rutenberg-McCurdy's rules (N0 = 1000, 8 seeds; laws held to 1e-9 degrees and 1e-10)) | Potts: 0.48 +- 0.02 macroscopic T1 per T2 at rc = 1 pixel, 0.64 / 0.32 at rc = 0.5 / 2; law-built: 0.25 +- 0.02 at all cut-offs (0.26 / 0.25 / 0.24 at c = 0.5 / 1 / 2) | Rutenberg-McCurdy 0.53 +- 0.05, independent of rc | **NOT CONFIRMED**: off the lattice the count is cut-off free (the Potts rc dependence was a lattice artefact) but half of 0.53; window not yet in a tested scaling state (mu2 1.58 against 1.24); one size so far | 2026-11-15-event-logger (scaling-state froth); law-built froth |
| 2D grain growth (curved-boundary vertex model) (6 runs, 3 seeds, 1001 to 2500 vanishings per window) | 1.22 to 1.27 swaps per vanished grain; macroscopic 0.06 to 0.14 | about 1.34 (Sprague et al. 2009, unverified) and 3/2 with side-shedding; macroscopic 0.53 | **NOT CONFIRMED**: macroscopic count does NOT agree with 0.53; control partly failed (von Neumann slope 0.76, mu2 1.9 to 2.0 against 1.620) | 2026-11-15-grains-polycrystals |
| 3D grain growth (threshold dynamics) (steady windows, two runs) | mean faces 13.65 to 13.85; survivors' net contact change per vanished grain e.g. -1.49, -1.66, -2.18 | Mason et al. 2015: 13.766; identity f_v - <F>/2: -1.43, -1.60, -2.21 | **CONSISTENT**: control passes; the identity holds in the steady windows | 2026-11-15-grains-polycrystals |
| Earth: plate reconstructions, 230 Ma to now (Müller 2016, Müller 2019 (three readings), Matthews 2016, Merdith 2021; independent history Scotese & Wright 2018) | persistent swaps 23 to 35 (10 to 15 per 100 Myr), step-independent at 1 to 5 Myr; per plate per 100 Myr 0.44 to 0.58 (Müller family) against 0.07 (Scotese & Wright) | no null rate; test: agreement across independent histories, clustering at reorganisations | **NOT CONFIRMED**: agreement does NOT carry over to an independent history; no clustering beyond chance (p 0.12 to 0.28); counts describe the models, not the Earth | 2026-11-15-earth-plates (rounds 1 and 2) |
| Sun: granulation (radiative-MHD simulation) (Bifrost runs en024048_hion and qs024048_by3363, 13 settings, steps 10 to 80 s) | 0.07 to 0.15 persistent swaps per cell per minute at 10 s; 0.6 to 1.3 per cell lifetime; 0.8 to 1.9 per persistent split (spread over settings); corrected by the control's detection fraction and fitted to step 0: 0.08 to 0.16 (median 0.13) at P = 60 s, +-9 to 15% per setting plus about 15% calibration, but the corrected rate still halves from step 0 to 80 s and moves by up to 30% with P | no null rate (births at junctions almost absent, so swaps per birth is undefined) | **NOT CONFIRMED**: corrected rate still step-dependent and P-dependent; the step-0 value is an extrapolation, not a stable rate; order of magnitude stable; space-time slicing at a tilt (full run, 16 Nov): swaps, births and deaths per volume differ over tilted directions by 1.2 to 3.6 times the Poisson-Voronoi spread in every labelling and depth (NOT CONFIRMED, as predicted) | 2026-11-15-sun-granulation |
| Sun: the skeleton of granulation, persistence or reappearance (radiative-MHD simulation) (Bifrost en024048_hion, vertical velocity at 0, 0.1 and 0.2 Mm below the surface (40 min, 10 s), and qs024048_by3363 at 0.1 Mm; no swap matching: corners, downflow sinks and lanes followed by position within 96 to 192 km) | half-lives at 0.1 Mm: corners 220 s, corner sites 280 s, lanes at a fixed point 190 s, cells 540 s; corner sites lasting 5 min or more: 32% continuous with the same cells, 33% continuous with renewed cells (0.64 new cells per minute), 35% with brief gaps (median 20 s, 2% of the span); a vanished corner is back at the same place within 60 s 5.6 times as often as at a far time; families of fragmenting granules: 51% still present after 20 min; no local cycle, only an oscillation of the whole box with a period of 400 to 480 s | prediction written before the run: corners outlive cells; shuffled frames give one-frame lifetimes and chance re-formation (both seen); moving Voronoi: exact corner half-life 970 s, re-formed sites 1 to 7% | **NOT CONFIRMED**: corners do not outlive the cells (220 s against 540 s); CONSISTENT: re-formation at the same place (x5.6 at 10 s, falls to x1.8 at 80 s), renewal of the cells at a persistent corner, families outlive single granules; NOT CONFIRMED: the three-class split (gaps not separable from detection dropouts) and any cycle of local recurrence; DICTO's reading of the dark patches of its lane stack as granule tubes in space-time: next row | 2026-11-15-sun-granulation (section: the skeleton) |
| Sun: granule tubes in space-time, prisms or scutoids (radiative-MHD simulation) (Bifrost en024048_hion at 0, 0.1 and 0.2 Mm and qs024048_by3363 at 0.1 Mm; census tracks on the whole periodic box, tubes wholly inside the 40-min block, 3 min or more; steps 10 to 80 s, tracking tolerance 0 to 0.7; nulls: space-time Poisson-Voronoi (exact), moving Voronoi windows (exact), shuffled and reversed frames) | share of scutoid tubes (neighbours change along t) 0.89 at 0.1 Mm and 10 s (393 tubes), 0.87 to 0.98 over all settings; 0.07 / 0.79 / 1.00 / 1.00 for lives 0-3 / 3-6 / 6-10 / 10+ min; prisms short and small (3.6 min, 0.75 Mm2); lateral extra corners per tube mean 12.6, median 8 at 10 s, falling to 5.3 at 80 s; changes rise with lifetime (Spearman 0.83) and size (0.62); shuffled frames still leave 254 to 274 long tubes (large static regions) with share 0.95 to 0.97 | Poisson-Voronoi: every cell a scutoid (exact share 1), 25.07 lateral corners per cell exact (pipeline 17 to 22); moving Voronoi windows: pipeline within 0.015 of exact | **CONSISTENT**: CONSISTENT: most tubes are scutoids, and the share is stable within 0.06 over depth, run, tolerance and steps 10 to 40 s (0.105 with 80 s); NOT CONFIRMED: corners and changes per tube stable (-58% with the step, +45% with tolerance); the shuffled control fails, so the share is not specific to the real time order; ESTABLISHED by the rule: rise with lifetime and size | 2026-11-15-sun-granulation (section: granule tubes in space-time) |
| Atmosphere: open-cell convection (satellite) (Himawari-9, 5 Feb 2025, 6 h, 2.5 min frames) | 0.03 to 0.15 persistent swaps per cell-hour; within about 30% over 2.5 to 10 min steps, threefold over settings | no null rate | **NOT CONFIRMED**: FEASIBLE; rates NOT yet stable; no rate goes into the comparison table | 2026-11-15-atmosphere-seaice |
| Sea ice floes; ice-wedge polygons (Himawari-9 Okhotsk pilot; literature) | 0 to 33 usable cells; no event time series for polygons | - | **NOT A TEST**: NOT feasible from the geostationary images; no usable time series | 2026-11-15-atmosphere-seaice |
| Cosmic void basins (N-body simulation) (pmwd, 256^3 particles in 256 Mpc/h, watershed basins R = 3 to 6 Mpc/h, two seeds, down to Delta a = 1/512) | share of contact changes that come alone 0.60 at the finest spacing (about 0.65 to 0.7 extrapolated); about 25 contact changes per merged basin (23 to 27) | all single (Theorem 1') for generic tilings; voxel tilings are not generic | **NOT A TEST**: cannot test Theorem 1' in its exact form; residual clumping DECIDED to be the discreteness of the units (falls with finer voxels and tracers), zero in the continuum an extrapolation | 2026-11-15-cosmic-voids |
| Interstellar bubbles (toy, rung 5 of the foam ladder) (2D toy slice; public ISM data single-epoch or about 10 Myr apart) | Euler fails in 223 of 240 frames; swaps 0.01 per vanished cell (flicker) | - | **NOT A TEST**: toy rule FAILS as a tiling; real data give no usable time series | 2026-11-15-interstellar-bubbles |
| Compound eyes: geometric law (perfect hexagonal mosaic; four open micro-CT mosaics (ODA-3D)) | one edge family flips when anisotropy A reaches sqrt 3 across the rows (1024 of 3039 edges at A = 1.74, none at 1.72), never along rows; real mosaics: swaps start well below sqrt 3 (0.2% for A < 1.2 to 33% at 2.5 to 3) | prediction stated before data (commit 2bf1098a): swaps in oval eyes, about none in near-spherical ones | **ESTABLISHED**: law proved for the perfect mosaic and calibrated on four real mosaics; no scutoid observed | 2026-11-16-compound-eye-scutoids |
| Compound eyes: depth traces (butterfly gw05, gw16) (Paukner et al. 2024 X-ray volumes, 0.6 um voxels) | gw05 cone layer 10 of about 1330 pairs change against 4.2 +- 2.1; gw16 retina 799 of 4786 against null 809 +- 34; 0 of 1505 flagged changes a true exchange | about 1% scattered changes for these nearly evenly curved eyes, below the method's resolution | **NOT A TEST**: NOT A TEST OF THE PREDICTION (relabelled 16 Nov with DICTO); kept as method development | 2026-11-16-compound-eye-scutoids (gw05, survey, gw16) |
| Jupiter: south polar cyclone ring (Juno) (cyclone centres PJ4 to PJ30 (Mura et al. 2021 via Gavriel & Kaspi 2022)) | 0 swaps: cyclic order 1-2-3-4-5 in all 19 of 22 epochs where all five were seen; one sixth cyclone formed in Sep 2019 and was gone by Feb 2020 (an insertion, not a 2-2 move) | no rate possible (6 cells, one event in 9 years) | **NOT A TEST**: event catalogue, never a rate; scope SETTLED | 2026-11-16-planet-cells |
| Spectacle hole arrays (model) (hole columns between lens surfaces of 0 to 10 D base curve) | uneven stretch at most 1.15 : 1; 0 swaps for regular layouts; 1 to 4 in about 175 edges for spiral and random holes | sqrt 3 = 1.73 : 1 needed before a hexagonal lattice swaps | **ESTABLISHED**: one negative: no scutoids in spectacle lenses (computed, 7 controls passed) | 2026-11-15-scutoid-lenses |
| Yew and conifer cambium (CoLuS conifer patches (one cross-section)) | swaps not observable in one section; file starts plus ends 0.021 per file per cell (manual outlines) | - | **PARKED**: PARKED (DICTO 16 Nov: 'forget the yew sample unless available online') | 2026-11-15-yew-cambium |

Figure reused (one, with the DICTO mark): studies/2026-11-15-sun-granulation/results/figures/sun_swaps.png.

## 4. Open (five; the ones that matter most for scutoid interactions)

1. **Compound eye with strongly uneven curvature.** The one direct test of a scutoid prediction in living tissue; the prediction is stated and timestamped, the law proved. Next: find an open volume of an unevenly curved eye with a published cell segmentation (acute-zone or flattened eyes: dragonflies, robber flies, mantises, mantis shrimp; the 29-ommatidium oval wasp eye of Makarova et al. 2025 as the small first case), then trace with the gw16 pipeline and the contact-length restriction.
2. **Serial-section test of swaps per birth = <F>/2 - 3 in a real 3D grain map.** An exact law of the #104 kind, tested on real data with no time series and no tracking error: 3.883 predicted for steady grain growth against 4.768 for Poisson-Voronoi. Next: fetch one public 3D EBSD or DCT grain volume, sweep it by planes with the shared logger, compare swaps per birth with <F>/2 - 3 of the same volume.
3. **Sun: a swap rate stable under the time step.** The only natural 2D tiling with thousands of swaps; neither the step-0 fit with the moving-Voronoi detection fraction nor counting only swaps seen on the neighbouring depth planes (16 Nov) gives a step-stable rate, and shuffled frames still give nearly as many swaps as real ones at 10 s: the false swaps come from the frame-to-frame matching, which repeats on planes 50 km apart; measured without swap matching (16 Nov), the skeleton passes the shuffled control: corners vanish and come back at the same place within a minute five times as often as chance and their cells are renewed while they stay, but corners do not outlive the cells and no cycle of local recurrence is seen. Next: for swaps: make the time matching specific (all four cells matched by overlap above a fixed share), calibrate with a control that has splits and merges, then refit to step 0; for the skeleton: a moving-Voronoi control with texture matched to the Sun's lanes, to bound the detection share of re-formation and renewal, and a longer series for the families and the box-wide oscillation.
4. **Froth: the law-built count in a tested scaling state.** Decides whether the law-built value 0.25 or Rutenberg-McCurdy's 0.53 is the macroscopic T1 per T2 of a froth that obeys the laws; the two law-built derivations differ by a factor 2, perhaps through the film-relaxation speed, which no law fixes. Next: Add the running N0 = 2500 and rc x 4 counts (same rules), then run N0 >= 10^4 to a window that passes the fixed scaling test, with a local solver.
5. **Earth: per-plate rates with a resolution control.** Decides whether the Müller-family swap count is plate resolution or a rate shared with an independent history. Next: merge the family's microplates to Scotese-size plates and recount persistent swaps per plate per 100 Myr.

## 5. Closed (every lead of every source study)

| source study | lead | closed: done, or dropped and why |
|---|---|---|
| event-logger | NEXT 1: explain the single-contact clumps | done (earth-plates round 1: swaps where one pair shares a second boundary) |
| event-logger | NEXT 2: persistence rule for swaps | done (pairing.py; earth-plates two-sided k = 5 Myr) |
| event-logger | NEXT 3: close the Müller 2019 seam, second model | done (earth-plates: rules A, B, C; four models) |
| event-logger | macroscopic count against 0.53 | done (froth row: Potts lattice and law-built froth); the scaling-state value moves to open item 4 |
| tissue-null-models | power diagrams with non-linear weights | dropped: DICTO's narrowing (linear-motion values suffice for the table) |
| tissue-null-models | curved-film vertex model of coarsening | moved to open item 4 |
| earth-plates | round 1 NEXT 1 and 2: independent model, reorganisations | done (round 2: NOT CONFIRMED) |
| earth-plates | round 1 NEXT 3 and round 2: Sun and void tissues with the same rules | done (sun-granulation, cosmic-voids) |
| earth-plates | round 2: per-plate rates and resolution control | open item 5 |
| sun-granulation | lead 1: unpaired lost and gained contacts | open item 3 |
| sun-granulation | lead 2: rate against step, extrapolated to step 0 | done 16 Nov (step-0 fit: NOT CONFIRMED); the follow-up stays in open item 3 |
| sun-granulation | lead 3: emergent intensity instead of velocity planes | dropped: DICTO's narrowing (a second observable of the same simulation) |
| sun-granulation | lead 4: Hinode SOT/BFI G-band real series | dropped: DICTO's narrowing (needs calibration before any swap; reopen after open item 3) |
| sun-granulation | lead 5 and planet-cells lead 4: supergranules (HMI) | dropped: DICTO's narrowing (box too small or account needed) |
| sun-granulation | lead 6: ratio to #104 swaps per birth | closed: births at junctions are almost absent, so the ratio is undefined for granulation |
| cosmic-voids | third voxel size (768^3) | dropped: cause already decided (discreteness); a third size refines an extrapolation only |
| cosmic-voids | comparison-table numbers | done (this table) |
| interstellar-bubbles | NEXT 1: pairing rule | done (event-logger pairing section) |
| interstellar-bubbles | NEXT 2: rung 1 at 1024^2 | done (scaling-state froth at 2048^2); rung 3 at 96^3 dropped: DICTO's narrowing |
| interstellar-bubbles | NEXT 3: rung 5 new cell rule; TIGRESS at 1 Myr | dropped: toy fails as a tiling and real data have no time series |
| atmosphere-seaice | NEXT 1 to 3: pure cell scenes, two-sided splits, image control | dropped: DICTO's narrowing (rates threefold setting-dependent; the Sun carries the natural 2D rate, open item 3) |
| atmosphere-seaice | NEXT 4: sea ice (SubZero, MODIS), ice-wedge polygons | dropped: not feasible or no time series |
| grains-polycrystals | Next 1: Ni correspondences from the authors' face table | dropped: DICTO's narrowing (grain matching too noisy; open item 2 tests a law without matching) |
| grains-polycrystals | Next 2: more accurate 2D scheme | dropped: DICTO's narrowing (froth benchmark, open item 4, covers the 2D count) |
| grains-polycrystals | Next 3: serial-section test of <F>/2 - 3 | open item 2 |
| grains-polycrystals | Next 4: OCP movie count by hand | dropped: tens of grains, low resolution |
| compound-eye-scutoids | next 1: butterfly volume trace | done (gw05, gw16: NOT A TEST) |
| compound-eye-scutoids | next 2: D. elpenor negative control | folded into open item 1 (a control for the first positive test) |
| compound-eye-scutoids | next 3: wasp eye (29 ommatidia) | folded into open item 1 |
| compound-eye-scutoids | next 4: orient the bee scan | dropped: names model regions only, no new swap data |
| compound-eye-scutoids | set-aside (DICTO): find unevenly curved eye data | open item 1 |
| planet-cells | lead 1: Jupiter south ring through the logger | closed: the light check already gives 0 swaps; the logger would only classify the 2019 insertion, which is not a swap |
| planet-cells | lead 2: JIRAM PJ31 to PJ77 and north insertions | dropped: DICTO's narrowing (insertions, no rate) |
| planet-cells | lead 3: Pluto side-number statistics | dropped: static, no swaps |
| yew-cambium | multi-ring or serial tangential sections | PARKED by DICTO until an online serial-section data set turns up |
| scutoid-lenses | next 1: camera hole-array or lenslet cap | dropped: DICTO's narrowing (optics, no bearing on swaps) |
| scutoid-lenses | next 2: compound-eye scutoids | done (became the compound-eye study) |
| scutoid-lenses | next 3: exact exactly-one optimum | dropped: DICTO's narrowing (covering geometry, no bearing on swaps) |

## 6. Theory cited (not restated beyond what is proved there)

- DICTO, *Scutoid Tissues in Four Dimensions*, Paper #104, Version 3 (11 Nov 2026), DICTO DOI 10.5281/zenodo.24111864 (all versions):
  Theorem 1 (generic sweep of a simple 4-polytope: births, swaps, deaths = h1, h2, h3), Theorem 1′ (simple d-polytope, d ≥ 4: a
  corner changes the facets' contacts only by a birth, one contact gained, one lost, or a death; for d = 4 gain and loss together as
  the swap; for d = 5 separate moves), Theorem 2 (the three polytope counts). Moving 3D tilings are read as slices of a 5D sweep; the
  toy row checks that reading by computation, not proof. Source: papers/2026-11-10-scutoids-4d.
- DICTO, *The Permutohedron Paradigm: Every Possible Order*, DICTO DOI 10.5281/zenodo.24239019, Part Two "Swaps inside cells: scutoid
  tissues" (the neighbour-swap spine): Chapter 6 (the swap of neighbours in a tissue is the scutoid), Chapter 8 (the 4D permutohedron
  swept: 26 births, 66 swaps, 26 deaths). Source: papers/book-permutohedron-paradigm.
- Scutoids: Gómez-Gálvez et al. 2018 (Nat. Commun. 9, 2960); foams between concentric surfaces: Mughal, Cox, Weaire, Burke and
  Hutzler 2018.

## 7. Credits

Credited by name at the point of use in each source study; collected here by row. Froth: cellular Potts model of Glazier, Gross and
Stavans 1987; Stavans and Glazier 1989. Grains: Mason et al. 2015; Sprague, Patterson and Grandhi 2009; Wakai et al. 2001. Earth:
Müller et al. 2016 and 2019, Matthews et al. 2016, Merdith et al. 2021, Scotese and Wright 2018 (PALEOMAP), Domeier and Torsvik 2014,
read with pyGPlates (Müller et al. 2018) and GPlately (Mather et al. 2024); Bird 2003. Sun: Bifrost (Gudiksen et al. 2011), runs of
Carlsson, Hansteen, Gudiksen, Leenaarts and De Pontieu 2016 (Hinode Science Data Centre Europe); scikit-image (van der Walt et al.).
Clouds: Himawari-9 (Japan Meteorological Agency; NOAA mirror). Voids: pmwd (Li, Lanusse, Modi et al. 2022); basin tracking after
Wojtak, Powell and Abel 2016; Meijering 1953. Eyes: ODA-3D (Currea, Sondhi, Kawahara and Theobald 2023, CC BY 4.0; bee stack Taylor
et al.); Paukner et al. 2024 (BossDB, no licence stated: no images of these volumes are reproduced); Makarova et al. 2025; Kim et al.
2016. Jupiter: Mura et al. 2021 via Gavriel and Kaspi 2022 (Zenodo 6611745, CC BY 4.0); Adriani et al. 2020. Cambium: CoLuS
(Katzenmaier and co-workers, CC BY 4.0). Null values: Miles 1970, Møller 1989, Hinde and Miles 1980, Rutenberg and McCurdy, Herdtle
and Aref 1992.

DICTO: ideas, names, constructions and direction, including the scutoid tissue, the swap theorem and the compound-eye prediction.
Computation, proofs, verification and drafting with Claude (Anthropic).

## Files

data/results.json (rows, open, closed), scripts/make_html.py (tables + checks), build.sh (PDF on the print host with figcheck and the
print.mjs guards), paper/paper.html, paper/figures/sun_swaps.png, paper/DRAFT-scutoid-interactions.pdf.
