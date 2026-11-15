# Earth plates: counting rule settled on a fixed mesh, persistence, deforming zones, several models (One tissue, three scales, Section 1)

Follows studies/2026-11-15-event-logger (the logger, its validation and the first Müller 2016 census). DICTO, 15 Nov 2026: all
resources on the scutoid Earth, Sun and cosmos work now; this is the 17 Nov follow-up brought forward.

VERDICT, second round (15 Nov 2026, sections 7-10): the plate-scale agreement found in the first round does NOT carry over to an
independent plate history, events do NOT cluster at the known reorganisations beyond chance, and the neighbour numbers are far
broader than random.
- Independent history: GPlately offers only one model with plate boundaries outside the Müller (EarthByte) family, Scotese & Wright
  2018 (C. R. Scotese's PALEOMAP rotations), and its boundaries cover only 100 Ma to now with 12 to 17 plates. Every frame passes
  Euler (101 of 101), but it has 1 persistent swap in 100 Myr (5 raw), 4 splits, 3 merges, 3 births, deaths 0: per plate and per
  100 Myr 0.07 persistent swaps against 0.44 to 0.58 in the rigid Müller-family readings. So the family's 23-35 persistent swaps
  measure how finely those models divide the plates, not a rate the two histories share. Young 2018 reads as the Müller 2016 map
  today (46 / 88 / 132) and was not run; Domeier & Torsvik 2014 (410-250 Ma, Matthews 2016's source there) passes Euler in all 160
  frames and gives 15 persistent swaps at 1 Myr steps against 26 in Matthews 2016 over the same window (28 at 5 Myr steps).
- Reorganisations (105-100 Ma and about 50 Ma; circular-shift test stated before the runs): in all six Müller-family readings the
  event rate in the windows is 1.3 to 2.0 times the rate outside, but p = 0.12 to 0.28 (none below 0.05); persistent swaps alone
  p = 0.35 to 0.79; Scotese & Wright 2018 rate ratio 0.73, p = 0.84. Claim rule not met: no clustering beyond chance is shown.
  The 10 Myr series peak at 20-40 Ma in the family (8 to 11 events per 10 Myr) and are thin before 150 Ma.
- Neighbour numbers: mean sides equals 6 - 12/F exactly in every frame without island loops (2169 frames), as Euler demands; the
  spread is not random: variance of sides 3 to 11 times spherical Poisson-Voronoi's at the same F (medians per model; at least 1.5
  times at every 50 Myr epoch of every model, below it in 33 of 2657 frames), three-sided plates 4.7 to 11 times more common (medians), and the
  largest plate (24 sides today in Müller 2016) beyond Poisson-Voronoi's 99th percentile in 67% of frames.
NEXT: the Sun and void tissues with the same rules; for the Earth, rates per plate (not totals) and a model-resolution control
(merge the family's microplates to Scotese-size plates and recount) before any rate is compared across histories.

VERDICT, first round (15 Nov 2026): the counting rule is settled and one swap count now holds across step sizes, models and deforming-zone
rules; the raw counts do not.
- Single-contact clumps EXPLAINED: they were swaps in which one pair shares a second boundary elsewhere; counted per boundary they
  are swaps (Müller 2016 on the mesh: 18 such clumps under the pair rule, 1 left; swaps 48 -> 62). The 33 failing frames came from
  reading overlapping, duplicated and gapped polygon pieces as a network; the map is now read on a fixed 15 km mesh (stated rules
  R1-R5), and every frame of every run passes Euler: 2396 frames in 6 runs, balance exact at every step, negative control caught in
  all 78 censuses.
- STEP-INDEPENDENT: swaps that persist (old and new contact each last 5 Myr or more). At steps of 1 and 5 Myr: Müller 2016 26 / 19,
  Müller 2019 (rule A) 37 / 36, Matthews 2016 54 / 49, Merdith 2021 64 / 66 (0-1000 Ma). Raw swaps fall 62 -> 19 -> 11 (1, 5, 10 Myr);
  at 10 Myr the persistent count halves too (events within 10 Myr cancel). Splits, merges, relabels and clumps stay step-dependent;
  births are steady at steps 1 to 5 only in Müller 2016 (8, 8, 8) and Matthews 2016 (8, 8, 9). A hard cut of short boundaries (50 or 150 km) makes events of its own and
  does not help; a length filter on swaps (150 km) changes the 1 Myr persistent counts by 0 to 3% in the rigid readings and by
  12 to 17% under rules B and C.
- Müller 2019 seam CLOSED three ways (A: zones to the nearest rigid plate, 46 cells today; B: every network a cell, 183; C: network
  cells only where no rigid plate lies, 104): all 251 frames pass Euler under each rule. Raw swaps differ threefold (73, 190, 139);
  persistent swaps agree (37, 35, 32).
- WHAT THE MODELS AGREE ON (0-230 Ma, 1 Myr; Müller 2016, Müller 2019 A/B/C, Matthews 2016, Merdith 2021): persistent swaps 23 to
  35 (10 to 15 per 100 Myr); splits 26 to 47, outnumbering births at junctions (8 to 15) two to four times; persistent swaps about
  equal to splits (ratio 0.7 to 1.1); no three-sided cell ever dies (deaths 0: plates end by merging). Raw swaps (58 to 188), relabels
  and clumps disagree by factors of three to ten. The models are related (Merdith 2021 and Matthews 2016 share the Müller 2016
  map today), so agreement is among kin, not independent proof; and every count describes the models, not the Earth itself.
NEXT (first round; (1) and (2) done in the second round): (1) one more model with its own plate history; (2) persistent swaps
against the known reorganisations (about 100 and 50 Ma); (3) the same rules on the Sun and void tissues.

## Predictions (written 15 Nov 2026 BEFORE the runs below; only the diagnosis of the old frames and the earth-pilot frames ran first)

Diagnosis already done on the old Müller 2016 run (no new computation): the single-contact clumps on clean steps are swaps in
which the new pair already touched elsewhere (or the old pair still touches elsewhere); the pair-based logger cannot see them.

New rule (R1 to R5 in scripts/earth_mesh.py): the map is read from a fixed mesh of about 15 km spacing, so every junction is triple
and every frame is a closed map; Euler is then a check of the extraction, and the data quality is reported as gap and overlap areas.

(1) Müller 2016, 230 Ma to now, 1 Myr, Lmin = 0:
- every frame passes Euler and the triple-junction formulas (231 of 231); present day 46 / 88 / 132 as in the vector reading;
- with contacts counted per boundary (by_segment), at least 5 of the old single-contact clumps become swaps (the five clean-step
  cases at 205, 148, 128, 22 and 17 Ma); swaps at 1 Myr: 50 to 70;
- births stay step-independent (within 1 of each other at steps 1, 2, 5, 10).
(2) Persistence and tolerance (same model):
- k = 1 (no rule): swaps fall by more than 50% from step 1 to step 10, as before;
- k = 5: at least the 18 back-and-forth swaps drop out; swaps at step 1 with k = 5 lie within 30% of swaps at step 5 (where k = 5
  is automatic), so the persistent swap count becomes step-independent from step 1 to step 5; step 10 still loses some;
- Lmin = 150 km: four-fold meetings appear and some swaps pass through them (joined by the rule); the k = 5 swap count changes by
  less than 20% from Lmin = 0;
- splits and merges remain step-dependent (more than 20% change from step 1 to step 10): neighbouring events fall together.
(2b) Added after the pipeline pilot (earth-pilot3, 12 Ma to now; before any full run): a hard cut of boundaries shorter than Lmin
makes events of its own (a contact "appears" when its boundary grows past Lmin), so the pilot's swaps fell and one-contact clumps
rose at Lmin 50 and 150 km. A length FILTER on swaps is added instead (R4' in scripts/swaps.py): a swap counts only when both
the old and the new boundary reach Lmin during their runs. Predictions: the hard cut does NOT make any count step-independent
(it raises clumps at every step); with the filter, persistent swaps (k = 5, filter 150 km) agree within 20% between steps 1 and 5.
(3) Müller 2019:
- rule A (zones to the nearest rigid plate), rule B (each network a cell wherever it lies, networks before rigid plates, as
  GPlates orders them) and rule C (network cells only where no rigid plate lies) all pass Euler in every frame (251 of 251);
  the earth-pilot frames already showed present day: A 46 cells / 88 / 132 (the rigid polygons alone, overlaps 0.09%, zones 6.6%
  of the sphere), B 187 cells with 32 island loops, C 103 cells with 13 islands;
- B and C have more swaps than A (more than 20% more), because the network pieces add contacts that change often; A is the rule
  comparable with the rigid models.
(4) Other models (Merdith et al. 2021 to 1000 Ma; Matthews et al. 2016 to 410 Ma). Clennett et al. 2020 is not run: its
present-day map equals Müller 2019 (rule B 189 cells against 187), so it adds no independent check. Note from earth-pilot: Merdith
2021 at present day gives exactly the Müller 2016 map (46 / 88 / 132) and Matthews 2016 nearly so (47 / 90 / 135), so for the
recent past these models share their plate boundaries; agreement there is not independent evidence.
- every frame passes Euler;
- Matthews 2016 is built on Müller 2016 for the last 230 Myr, so the two agree within 20% per event class there (not an
  independent check);
- across all models in their common window (0 to 230 Ma): splits outnumber births at junctions in every model; persistent swaps
  (k = 5) per 100 Myr agree within a factor of 2; exact counts per class differ by more than 30% between at least two models;
- Merdith 2021 before 250 Ma has fewer plates and fewer events per 100 Myr than after.

## 1. Why the old frames failed and where the single-contact clumps came from (diagnosis of the 15 Nov run, no new computation)
- The 13 "one contact lost only" and 11 "one contact gained only" clumps: on clean steps (both frames pass every check) each one is
  a swap in which one of the two pairs shares a second boundary elsewhere. Example, 205 to 204 Ma: plates 131 and 301 stop touching
  and plates 101 and 902, which already touched, gain a second boundary there. The same at 148, 128, 22 and 17 Ma. The logger
  compared neighbour PAIRS, so it saw only one side of the swap. The rest fall in steps with large reorganisations or failing frames.
- The 33 failing frames (Müller 2016): all come from reading the model's boundary pieces as a network. Causes found per frame:
  a boundary piece used by one, three or four polygons (overlapping polygons; 18 frames), two copies of one boundary of which one
  was dropped as a duplicate (20 frames), a point where three plates meet but two or four pieces end (24 frames), a cell whose
  boundary came out in two pieces (4 frames), and uncovered gaps (4 failing frames; 12 frames from 60 to 26 Ma carry a gap cell);
  most frames have more than one cause, and 2 frames show none of these marks (cause not identified). Not the dateline: the
  reading is in 3D coordinates throughout.
- Fix 1 (counting): eventlog.py has an opt-in option by_segment: a contact is lost or gained when the NUMBER of boundaries shared
  by two cells falls or rises. Fix 2 (resolution): the map is read from a fixed mesh (rules R1 to R5 in scripts/earth_mesh.py):
  every mesh point gets the polygon the GPlates partitioner puts it in, so overlaps are decided by the partitioner's own order,
  slivers narrower than the mesh spacing vanish, gaps go to the nearest plate (or become cells, rules B and C), and every frame is
  a closed map with triple junctions.
- Checks of the fix: the mesh map of Müller 2016 at present day is 46 cells, 88 junctions, 132 boundaries, 126 neighbour pairs at
  mesh spacings of 30 km and 15 km, exactly the vector reading; synthetic Voronoi maps (30 cells: 56 junctions, 84 boundaries) and
  island cells pass; tests: eventlog 33/33 (10 new: by_segment swap, its reverse, unchanged plain cases, islands, negative controls),
  swaps.py 12/12 (persistence, censoring, four-fold join and its negative, length filter).

## 2. Software, models and credits
pyGPlates 1.0 (GPlates project, GPL-2.0; Müller et al. 2018, G-cubed 19, 2243-2261, doi:10.1029/2018GC007584) resolves the plate
polygons and deforming networks and its PlatePartitioner assigns the mesh points; GPlately 2.0 and its PlateModelManager (GPL-2.0;
Mather et al. 2024, Geoscience Data Journal 11, 3-10, doi:10.1002/gdj3.185) download the models; SciPy (cKDTree, connected
components). We call their code and copy none of it. Plate models, each by its authors, downloaded through GPlately:
- Müller et al. 2016, Annu. Rev. Earth Planet. Sci. 44, 107-138 (230-0 Ma, rigid plates);
- Müller et al. 2019, Tectonics 38, 1884-1907, doi:10.1029/2018TC005462 (250-0 Ma, with deforming networks; CC BY 4.0);
- Matthews et al. 2016, Global and Planetary Change 146, 226-250, doi:10.1016/j.gloplacha.2016.10.002 (410-0 Ma);
- Merdith et al. 2021, Earth-Science Reviews 214, 103477, doi:10.1016/j.earscirev.2020.103477 (1000-0 Ma).
- Clennett et al. 2020 (G-cubed 21) was read at present day only (earth-pilot) and not run: its map equals Müller 2019's.
The persistence idea (count a neighbour exchange only if it lasts) follows the stopping rule of the plan; Bird 2003's formulas
(junctions = 2(plates - 2), boundaries = 3(plates - 2)) are the per-frame check, as in the event-logger study.

## 3. Results (scripts/earth_mesh.py, swaps.py, window.py, compare.py; results/)
Mesh level 9 (2 621 442 points, mean spacing 15.0 km). Sliver rule R3: a detached piece under 5000 km2 joins its main neighbour.
Every census: frames failing 0, balance failures 0, negative control caught (78 of 78).

Data quality reported per frame (results/*.json, "infos"): Müller 2016 has no overlap or gap above 1% in any frame. Müller 2019's
rigid polygons leave 1% to 8.3% of the sphere uncovered in 229 of 251 frames (the deforming zones) and overlap by more than 1%
in 5 frames (103 to 49 Ma, at most 11.7%). Matthews 2016 overlaps by more than 1% in 16 frames (365 to 13 Ma, at most 14.1%) and
has 2 frames with gaps above 1%; Merdith 2021 overlaps by more than 1% in 15 frames (475 to 100 Ma, at most 20.3%). Overlaps are
decided by the GPlates partitioner (rule R1); no frame is excluded. Under rules B and C some network labels are smaller than the
mesh in 31 and 201 frames (they vanish from the map).

### 3a. Step dependence (whole runs, Lmin 0; persistent = two-sided k = 5 Myr; filter = both boundaries reach 150 km)
| run | raw swaps at step 1 / 2 / 5 / 10 Myr | persistent swaps | persistent + filter | births | splits | merges | clumps |
|---|---|---|---|---|---|---|---|
| Müller 2016 (230 Ma) | 62 / 46 / 19 / 11 | 26 / 23 / 19 / 11 | 26 / 23 / 18 / 8 | 8 / 8 / 8 / 6 | 29 / 23 / 16 / 9 | 17 / 18 / 11 / 10 | 86 / 80 / 73 / 44 |
| Müller 2019 A (250) | 73 / 54 / 36 / 13 | 37 / 29 / 36 / 13 | 36 / 27 / 23 / 10 | 15 / 12 / 12 / 9 | 34 / 30 / 19 / 9 | 25 / 19 / 13 / 6 | 116 / 109 / 86 / 58 |
| Müller 2019 B | 190 / 95 / 35 / 14 | 35 / 27 / 35 / 14 | 29 / 20 / 18 / 10 | 11 / 11 / 7 / 3 | 47 / 30 / 16 / 9 | 35 / 16 / 10 / 7 | 818 / 478 / 216 / 97 |
| Müller 2019 C | 139 / 71 / 39 / 12 | 32 / 27 / 39 / 12 | 28 / 22 / 20 / 9 | 12 / 9 / 6 / 4 | 36 / 23 / 12 / 5 | 34 / 21 / 11 / 4 | 364 / 266 / 145 / 66 |
| Matthews 2016 (410) | 103 / 78 / 49 / 24 | 54 / 45 / 49 / 24 | 53 / 43 / 41 / 20 | 8 / 8 / 9 / 4 | 42 / 33 / 22 / 13 | 23 / 23 / 16 / 13 | 124 / 119 / 107 / 78 |
| Merdith 2021 (1000) | 140 / 111 / 66 / 34 | 64 / 60 / 66 / 34 | 63 / 56 / 53 / 25 | 15 / 12 / 7 / 7 | 51 / 41 / 32 / 18 | 40 / 31 / 24 / 20 | 301 / 251 / 194 / 153 |
- At step 5 the rule k = 5 is automatic (one frame lasts 5 Myr), so "persistent at step 1 = raw at step 5" is the test. It holds
  within 3% for Müller 2019 A and B and Merdith 2021, 9% for Matthews 2016, 22% for rule C and 27% for Müller 2016. At step 2 the
  rule needs 3 frames (6 Myr), hence its lower values.
- Relabels 15 to 109 at step 1, mostly under rules B and C (network pieces renumbered by size).
- Deaths (a three-sided cell vanishing) are 0 in every run: with lineage, a vanishing plate's area goes mostly to one neighbour,
  which is a merge.
- Hard cut of short boundaries (R4; Lmin 50 and 150 km, full tables in compare.py output): raw swaps fall and clumps rise at every
  step (Müller 2016 at 150 km: clumps 206 / 172 / 116 / 63), so the cut adds threshold-crossing events; the swaps joined through
  four-fold meetings (21 at step 1) do not restore the count (persistent 17 against 26).
- Old pair rule on the same mesh frames (Müller 2016, step 1): 48 swaps and 18 one-contact clumps; by boundary: 62 swaps and 1.

### 3b. Models compared on common windows (step 1, Lmin 0; results/windows.jsonl)
| run | 0-230 Ma: raw swaps | persistent swaps (k 5; with 150 km filter) | births | splits | merges | relabels | clumps | persistent swaps 0-100 / 100-200 Ma |
|---|---|---|---|---|---|---|---|---|
| Müller 2016 | 62 | 26 (26) | 8 | 29 | 17 | 15 | 86 | 17 / 8 |
| Müller 2019 A | 71 | 35 (34) | 15 | 33 | 25 | 18 | 114 | 19 / 15 |
| Müller 2019 B | 188 | 33 (27) | 11 | 47 | 35 | 108 | 815 | 19 / 13 |
| Müller 2019 C | 137 | 30 (26) | 12 | 36 | 34 | 84 | 361 | 17 / 12 |
| Matthews 2016 | 63 | 27 (27) | 8 | 27 | 20 | 15 | 84 | 15 / 9 |
| Merdith 2021 | 58 | 23 (23) | 11 | 26 | 21 | 18 | 97 | 14 / 8 |
- Agreed: persistent swaps 23 to 35 (spread 1.5 fold); in 0-100 Ma 14 to 19, in 100-200 Ma 8 to 15 (more persistent swaps in the
  younger window in every run); splits more than births (2.2 to 4.3 times); persistent swaps / splits 0.70 to 1.06; deaths 0.
- Not agreed: raw swaps (58 to 188), relabels (15 to 108), clumps (84 to 815); births (8 to 15).
- Merdith 2021 before 230 Ma: 82 raw and 41 persistent swaps in 770 Myr (5 persistent per 100 Myr against 10 in 0-230 Ma), with
  11 to 22 plates against up to 46.
- Kinship: Merdith 2021 at present day is the Müller 2016 map, Matthews 2016 nearly so (47 / 90 / 135), Matthews 2016 agrees with
  Müller 2016 within 18% in every class over 0-230 Ma. The three Müller 2019 rules read one model. So the agreement is within one
  family of reconstructions.

## 4. Predictions checked
(1) 231 of 231 frames pass, present day 46 / 88 / 132: HELD. Swaps 50 to 70: HELD (62). At least 5 old clumps become swaps: HELD
(17 of 18). Births within 1 at all steps: FAILED at step 10 (8, 8, 8, 6).
(2) k = 1 swaps fall by more than half from step 1 to 10: HELD (62 to 11). k = 5 removes the back-and-forth swaps: HELD (62 to 26).
Step 1 with k = 5 within 30% of step 5: HELD (26 against 19, 27%; in the other runs 0 to 22%). Hard cut at 150 km changes the
k = 5 count by less than 20%: FAILED (26 to 17). Splits and merges step-dependent: HELD.
(2b) Hard cut does not make any count step-independent and raises clumps: HELD. Filter (150 km) with k = 5 within 20% from step 1
to step 5: FAILED in four of six runs (Müller 2016 26 against 18; it holds for Merdith 2021, 63 against 53, and nearly for
Matthews 2016, 23%). The filter reduces step-5 counts more than step-1 counts.
(3) All three rules pass Euler in every frame: HELD. B and C have more than 20% more swaps than A: HELD for raw swaps (190, 139
against 73), FAILED for persistent swaps (35, 32 against 37).
(4) Every frame passes: HELD. Matthews 2016 within 20% of Müller 2016 in every class: HELD. Splits more than births in every model:
HELD. Persistent swaps within a factor 2: HELD (1.5). Some class differs by more than 30%: HELD. Merdith 2021 fewer plates and
events before 250 Ma: HELD.

## 5. Runs (all FINAL ok unless stated; nothing left running)
earth-pilot (present day and oldest frame of each model, mesh spacing 30 km; FINAL FAIL: rule B and Clennett 2020 failed Euler at
Lmin 50 and 150 because a contraction closed a two-sided lens; fixed by the lens rule in R4, then both passed), earth-pilot2 (FAIL:
a pyGPlates rotation call that does not exist in version 1.0; fixed), earth-pilot3 (full pipeline, 12-0 Ma, two runs), earth-m16,
earth-m19 (three rules in parallel), earth-mat16, earth-mer21; the four series ran in parallel on the two compute machines.

## 6. Files and recounts
results/frames_MODEL_RULE_L{0,50,150}.jsonl are the raw 1 Myr tilings (cells, boundaries per segment, junctions, loops,
components; the L0 files also carry every boundary's length in km), results/events_*.json the step-1 event logs, results/*.json the
censuses, results/windows.jsonl the window counts. The frame files of these runs do not carry lineage (it was used in memory);
earth_mesh.py now writes parents and heirs into the frame files, so later runs can be recounted without the plate models. The
swap rules here (scripts/swaps.py: joins through four-fold meetings, two-sided persistence, length filter) are local to this study;
a shared pairing and persistence rule for the logger is being added in studies/2026-11-15-event-logger/pairing/, and these frames
are kept so they can be recounted with it.

## 7. Second round: an independent plate history, events against reorganisations, neighbour numbers (predictions written 15 Nov 2026 BEFORE the runs)

Models chosen (provenance read from the files GPlately downloads; nothing run yet). Of the 32 models GPlately's PlateModelManager
lists, those with topological plate boundaries outside the Müller (EarthByte) family are few. Young et al. 2018/2019 (Geoscience
Frontiers 10, 989-1013, doi:10.1016/j.gsf.2018.05.011) is by the same group and described as building on previous work; whether
its last 230 Myr is Müller 2016 is checked in the pilot (present-day and 200 Ma maps against Müller 2016) before it is counted as
kin. Clennett 2020, Zahirovic 2022, Cao 2024, Alfonso 2024, Müller 2022/2025 and Shirmard 2025 are later models of the same group,
Seton 2012, Shephard 2013 and Gurnis 2012 earlier ones; none is treated as independent. PALEOMAP, Scotese 2016, Torsvik & Cocks
2017, Golonka and Li 2008 carry rotations and static polygons only (no plate boundaries), so the rules cannot read them.
Two are run:
- Scotese & Wright 2018 (0-540 Ma; GPlately name scotese_and_wright2018, Zenodo doi:10.5281/zenodo.5348491, version
  10.5281/zenodo.5460860): its rotation file is C. R. Scotese's PALEOMAP plate model (header: "PALEOMAP Plate Model m15g60_v2d3 ...
  by CR Scotese 02/01/2016"), with 524 topological plate polygons and no deforming networks. Its plate history is Scotese's own, not
  derived from the Müller family (both use the same public sea-floor magnetic data in the young oceans, so they are not blind to each
  other). Who digitised the topological boundaries is not stated in the downloaded files; the record names Scotese and Wright.
- Domeier & Torsvik 2014 (410-250 Ma; Geoscience Frontiers 5, 303-350, doi:10.1016/j.gsf.2014.01.002; GPlately name domeier2014):
  "Plate tectonics in the Late Paleozoic", the original Late Paleozoic topological model; Matthews 2016 builds its 410-250 Ma on it,
  so in that window it is Matthews 2016's source, not an independent check (Merdith 2021's link to it is not checked here); it is
  run as the parent against which the later models' Paleozoic is read.

Rules: exactly as in sections 1 to 6 (rule A, mesh level 9, step 1 Myr, Lmin 0, persistence k = 5 two-sided).

Predictions for the runs:
(P1) Scotese & Wright 2018 and Domeier & Torsvik 2014: every frame passes Euler, balance exact, negative control caught.
(P2) Scotese & Wright 2018 in 0-230 Ma agrees with the Müller family on the agreed points: persistent swaps within a factor 2 of
     the family's 23-35 (that is 12 to 70), splits more than births, deaths 0, persistent swaps / splits between 0.5 and 1.5, and more
     persistent swaps in 0-100 than in 100-200 Ma. Its raw swaps, clumps and relabels lie outside the family's ranges (they are
     reading-dependent).
(P3) Domeier & Torsvik 2014 vs Matthews 2016 and Merdith 2021 in 250-410 Ma: persistent swaps within 30% of Matthews 2016 (its
     direct descendant there).

Time series and reorganisations (scripts/timeseries.py; step-1 events and Lmin 0 frames of every run). Classes: persistent swaps
(k = 5), splits, merges, births; counts in 5 and 10 Myr bins over each model's span. Reorganisations fixed before looking, from the
literature: 105-100 Ma (Matthews, Seton and Müller 2012, "A global-scale plate reorganization event at 105-100 Ma", Earth Planet.
Sci. Lett. 355-356, 283-298) and about 50 Ma (Hawaiian-Emperor bend 50-47 Ma, Sharp and Clague 2006, Science 313, 1281-1284;
Australian-Antarctic reorganisation at the bend's time, Whittaker et al. 2007, Science 318, 83-86; India's collision with Asia
about 50-55 Ma). The kinematic synthesis of these models is Matthews et al. 2016, "Global plate boundary evolution and kinematics
since the late Paleozoic" (Global Planet. Change 146, 226-250; the reorganisation list in Müller et al. 2016 is used the same way).
Windows W = [98, 108) and [45, 55) Ma (20 Myr in all); an event between frames t0 and t0 - 1 has age t0 - 0.5.
Test (stated now): statistic = number of events (persistent swaps + splits + merges + births) with age in W, in 0-230 Ma; null =
the same event series shifted in a circle by a whole number of Myr drawn uniformly from 0..229 (keeps every cluster and the total,
destroys only the alignment with W); 10 000 shifts, fixed seed; one-sided p = share of shifts with a count at least the observed.
Also reported: rate in W / rate outside W, the same test for persistent swaps alone, and (exploratory, not part of the claim) the
Farallon breakup window [20, 26) Ma (Lonsdale 2005, Tectonophysics 404, 237-264).
Claim rule (stated now): "events cluster at reorganisations beyond chance" only if p < 0.05 in Scotese & Wright 2018 AND in at least
4 of the 6 Müller-family readings. Caveat stated now: the Müller-family models were built by the authors who described the 105-100
Ma event, so their test is partly circular; Scotese & Wright 2018 is the check.
(P4) Combined events: p < 0.05 in at least 4 of 6 Müller-family readings (rate in W about 1.5 to 2 times the rate outside).
(P5) Scotese & Wright 2018: rate in W above the rate outside, but p > 0.05 (claim not met).
(P6) Persistent swaps alone (about 25 per model): p > 0.05 in most readings (too few events for the test).

Neighbour numbers (same script; every 1 Myr frame; epochs reported every 50 Myr). n = number of boundaries of a cell (sides,
counted per boundary) and the number of distinct neighbours. Reference: studies/2026-11-15-tissue-null-models (mean sides 6 - 12/F
exactly for a triple-junction map of F cells on the sphere; 2D Poisson-Voronoi variance mu2 = 1.781, Hinde and Miles 1980);
Poisson-Voronoi on the sphere with the same F simulated here (2000 maps per F; uniform random points, Voronoi from the convex hull).
(P7) Mean sides equals 6 - 12/F exactly in every frame without island loops and with one connected boundary network (Euler).
(P8) The plates' variance of sides mu2 is larger than spherical Poisson-Voronoi's at the same F, by at least 1.5 times, at every
     50 Myr epoch of every model (a few large plates with many sides and many small three- and four-sided plates).
(P9) Three-sided plates are more common than in Poisson-Voronoi at the same F (fraction at least twice), and the largest side
     number exceeds Poisson-Voronoi's 99th percentile at the same F in most frames.

Pilot (earth-indep-pilot, single frames at mesh level 9; FINAL FAIL, read before any full run): Scotese & Wright 2018's topological
plate polygons exist only from 100 Ma to now (12 polygons at 100 Ma, 17 today, none at 105 Ma or older; the rotations reach 540 Ma
but the boundaries do not); Domeier & Torsvik 2014 has none at exactly 410 Ma (16 at 400, 17 at 250). The frames that exist pass
Euler (Scotese & Wright today 17 cells / 30 junctions / 45 boundaries; Domeier & Torsvik at 250 Ma 17 / 30 / 45). Young 2018 today
reads 46 / 88 / 132 with 126 neighbour pairs, the Müller 2016 map (boundary length 300 065 km against 300 218 km), so it is kin and
not run. Its 200 Ma frame failed in the pilot (model files were still downloading in a parallel process) and is not needed.

Predictions AMENDED after the pilot, before the full runs (the claim rule above cannot be met as written, because Scotese & Wright
2018 has no boundaries before 100 Ma):
- Runs: Scotese & Wright 2018 100-0 Ma; Domeier & Torsvik 2014 409-250 Ma.
- (P2') Scotese & Wright 2018 with 12-17 plates (against 30-46 in the Müller family over 0-100 Ma): persistent swaps in 0-100 Ma
  between 3 and 19 (family 14-19); splits at least births; deaths 0; per plate and per 100 Myr, persistent swaps within a factor 2 of
  the family's.
- Reorganisation test for Scotese & Wright 2018: span 0-100 Ma, windows [45, 55) and [98, 100) (the part of [98, 108) inside its
  record), same circular-shift null over 0..99. Claim rule amended: "events cluster at reorganisations beyond chance" only if p <
  0.05 in at least 4 of the 6 Müller-family readings over 0-230 Ma AND p < 0.05 in Scotese & Wright 2018 over 0-100 Ma; the 50 Ma
  window alone is also tested in every model ([45, 55), spans as above) and reported separately.
- (P5') Scotese & Wright 2018: rate in the windows above the rate outside, p > 0.05.

## 8. Second-round results (scripts/earth_mesh.py with an optional youngest age, timeseries.py; results/)

### 8a. The two new runs (rule A, mesh level 9, Lmin 0; every census: frames failing 0, balance failures 0, negative control caught)
| run | frames | plates | raw swaps at step 1 / 2 / 5 / 10 Myr | persistent swaps (k 5) at the same steps | births | splits | merges | clumps (step 1) |
|---|---|---|---|---|---|---|---|---|
| Scotese & Wright 2018 (100-0 Ma) | 101 | 12-19 | 5 / 5 / 3 / 2 | 1 / 1 / 3 / 2 | 3 / 1 / 1 / 2 | 4 / 5 / 5 / 5 | 3 / 2 / 2 / 0 | 6 |
| Domeier & Torsvik 2014 (409-250 Ma) | 160 | 15-21 | 31 / 27 / 28 / 15 | 15 / 13 / 28 / 15 | 0 / 0 / 0 / 0 | 5 / 5 / 4 / 3 | 4 / 6 / 2 / 1 | 55 |
- Data quality: Scotese & Wright 2018 has no gap or overlap of its plate polygons in any frame; Domeier & Torsvik 2014 gaps at most
  0.01% and no overlap above 1%.
- Scotese & Wright 2018 against the family over 0-100 Ma (persistent swaps / splits / merges / births; mean plates): Müller 2016
  17 / 16 / 12 / 7 (31.8 plates), Müller 2019 A 19 / 18 / 15 / 13 (32.6), Matthews 2016 15 / 16 / 15 / 7 (31.8), Merdith 2021
  14 / 16 / 14 / 9 (31.8), Scotese & Wright 2018 1 / 4 / 3 / 3 (15.2). All four classes per plate: family 1.6 to 2.0 per 100 Myr in
  the rigid readings, Scotese & Wright 0.72; persistent swaps per plate 0.44 to 0.58 against 0.07.
- Domeier & Torsvik 2014 against its descendants over 409-250 Ma (persistent swaps / splits / merges / births): Matthews 2016
  26 / 13 / 2 / 0 (17.3 plates), Merdith 2021 16 / 6 / 5 / 2 (19.4), Domeier & Torsvik 2014 15 / 5 / 4 / 0 (17.4). Its persistent
  count is step-dependent (15 at 1 Myr, 28 at 5 Myr; the first-round runs agreed within 3 to 27%): contacts in this model often last
  under 5 Myr. Births 0 and deaths 0: its plates arise only by splitting.

### 8b. Events in 10 Myr bins, 0-230 Ma (persistent swaps + splits + merges + births; persistent swaps in brackets; results/timeseries*.json also hold 5 Myr bins, each class, and Domeier & Torsvik 2014 and Merdith 2021 to their ends)
| age (Ma) | M16 | M19 A | M19 B | M19 C | Mat16 | Mer21 | SW18 |
|---|---|---|---|---|---|---|---|
| 0-10 | 4 (0) | 11 (2) | 18 (6) | 13 (3) | 4 (0) | 4 (0) | 1 (0) |
| 10-20 | 4 (2) | 4 (3) | 6 (1) | 3 (1) | 4 (2) | 2 (0) | 2 (1) |
| 20-30 | 8 (3) | 9 (2) | 8 (0) | 9 (1) | 8 (3) | 10 (3) | 2 (0) |
| 30-40 | 10 (4) | 10 (2) | 11 (2) | 11 (2) | 10 (4) | 10 (4) | 1 (0) |
| 40-50 | 9 (1) | 8 (1) | 6 (1) | 7 (1) | 9 (1) | 8 (0) | 0 (0) |
| 50-60 | 3 (0) | 4 (1) | 10 (1) | 9 (1) | 3 (0) | 3 (0) | 1 (0) |
| 60-70 | 3 (2) | 3 (0) | 6 (0) | 7 (0) | 3 (2) | 4 (2) | 2 (0) |
| 70-80 | 4 (3) | 6 (3) | 5 (3) | 6 (3) | 3 (1) | 3 (2) | 0 (0) |
| 80-90 | 5 (1) | 5 (0) | 6 (0) | 5 (0) | 7 (1) | 6 (1) | 1 (0) |
| 90-100 | 2 (1) | 5 (5) | 6 (5) | 5 (5) | 2 (1) | 3 (2) | 1 (0) |
| 100-110 | 6 (2) | 5 (2) | 7 (1) | 5 (1) | 3 (1) | 3 (1) | - |
| 110-120 | 1 (1) | 8 (3) | 11 (4) | 8 (3) | 2 (1) | 1 (1) | - |
| 120-130 | 5 (2) | 5 (1) | 3 (1) | 3 (0) | 4 (2) | 4 (2) | - |
| 130-140 | 4 (1) | 6 (3) | 2 (2) | 4 (2) | 4 (1) | 5 (1) | - |
| 140-150 | 2 (0) | 4 (2) | 5 (2) | 4 (2) | 4 (2) | 6 (3) | - |
| 150-160 | 1 (0) | 4 (0) | 6 (0) | 3 (0) | 2 (0) | 1 (0) | - |
| 160-170 | 2 (1) | 3 (2) | 3 (1) | 3 (2) | 2 (1) | 3 (0) | - |
| 170-180 | 1 (0) | 3 (1) | 1 (1) | 1 (1) | 3 (1) | 2 (0) | - |
| 180-190 | 1 (1) | 1 (1) | 3 (1) | 3 (1) | 0 (0) | 0 (0) | - |
| 190-200 | 2 (0) | 1 (0) | 0 (0) | 0 (0) | 2 (0) | 2 (0) | - |
| 200-210 | 3 (1) | 1 (0) | 1 (0) | 1 (0) | 0 (0) | 0 (0) | - |
| 210-220 | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 1 (1) | 0 (0) | - |
| 220-230 | 0 (0) | 2 (1) | 2 (1) | 2 (1) | 2 (2) | 1 (1) | - |

### 8c. Reorganisation test (rules in section 7; 10 000 circular shifts, seed 20261115)
| run (span) | events | in windows (expected) | rate ratio | p | persistent swaps only: in (exp.), p | 105-100 Ma window only, p | 50 Ma window only, p | exploratory 20-26 Ma, p |
|---|---|---|---|---|---|---|---|---|
| Müller 2016 (0-230) | 80 | 13 (6.96) | 2.04 | 0.115 | 3 (2.26), 0.349 | 0.196 | 0.154 | 0.130 |
| Müller 2019 A | 108 | 12 (9.39) | 1.31 | 0.279 | 3 (3.04), 0.665 | 0.470 | 0.248 | 0.519 |
| Müller 2019 B | 126 | 18 (10.96) | 1.75 | 0.135 | 3 (2.87), 0.524 | 0.355 | 0.126 | 0.188 |
| Müller 2019 C | 112 | 14 (9.74) | 1.50 | 0.214 | 2 (2.61), 0.795 | 0.504 | 0.155 | 0.135 |
| Matthews 2016 | 82 | 11 (7.13) | 1.63 | 0.181 | 3 (2.35), 0.438 | 0.350 | 0.150 | 0.109 |
| Merdith 2021 | 81 | 10 (7.04) | 1.48 | 0.240 | 2 (2.00), 0.556 | 0.390 | 0.210 | 0.118 |
| Scotese & Wright 2018 (0-100) | 11 | 1 (1.32) | 0.73 | 0.840 | 0 (0.12), 1.0 | 1.0 | 0.769 | 0.091 |
- Every family reading has more events in the windows than expected, none significantly; the excess is about 3 to 7 events, which
  the circular shifts (keeping the series' own clusters) reproduce in 12 to 28% of shifts. The family's Müller 2019 readings carry 5
  persistent swaps at 96-90 Ma, just younger than the 105-100 Ma window; the 50 Ma window holds 6 to 11 events of the 11 to 16
  found in 40-60 Ma. The series also rise toward the present with the number of plates, which the circular null does not remove;
  a per-plate rate would be the next test, not part of this claim.

### 8d. Neighbour numbers (sides counted per boundary; spherical Poisson-Voronoi with the same F, 2000 maps per F)
| run | frames | frames without island loops: mean = 6 - 12/F | variance of sides / Poisson-Voronoi: median (min) | three-sided share / PV: median | largest side number above PV 99th percentile |
|---|---|---|---|---|---|
| Müller 2016 | 231 | 231 of 231 | 5.4 (1.6) | 9.7 | 126 frames |
| Müller 2019 A | 251 | 240 of 240 | 5.4 (1.7) | 11.4 | 185 |
| Müller 2019 B | 251 | 10 of 10 | 11.1 (3.6) | 7.7 | 217 |
| Müller 2019 C | 251 | 58 of 58 | 8.5 (3.4) | 11.2 | 214 |
| Matthews 2016 | 411 | 411 of 411 | 4.5 (1.4) | 7.8 | 238 |
| Merdith 2021 | 1001 | 958 of 958 | 4.7 (1.3) | 6.9 | 669 |
| Scotese & Wright 2018 | 101 | 101 of 101 | 4.6 (4.1) | 6.9 | 53 |
| Domeier & Torsvik 2014 | 160 | 160 of 160 | 3.2 (0.8) | 4.7 | 77 |
- Epochs (F, variance of sides, PV variance, three-sided share): Müller 2016 today 46, 22.6, 1.51, 28%; 50 Ma 27, 9.7, 1.35, 19%;
  100 Ma 26, 2.3, 1.34, 12%; 150 Ma 22, 10.7, 1.28, 32%; 200 Ma 13, 3.9, 1.00, 23%. Spherical PV has 1.5 to 3.6% three-sided cells
  at these F. The 100 Ma maps are the most even in every rigid family reading (variance 2.1 to 3.0, against 9.7 to 23 at 50 Ma and today).
- Frames below 1.5 times PV: Matthews 2016 7 (336-330 Ma, 1.42), Merdith 2021 11 (near 940 Ma, 1.30), Domeier & Torsvik 2014 15
  (399-330 Ma, down to 0.80, where its 16 plates are nearly even); at the 50 Myr epochs every model stays at or above 1.58.

## 9. Second-round predictions checked
(P1) Every frame passes, balance exact, control caught: HELD (101 of 101 and 160 of 160).
(P2) As first written (0-230 Ma) it could not be tested: the model has no boundaries before 100 Ma (amended before the runs).
(P2') Persistent swaps in 0-100 Ma between 3 and 19: FAILED (1; 3 at 5 Myr steps). Splits at least births: HELD (4, 3). Deaths 0:
HELD. Per plate within a factor 2 of the family: FAILED (0.07 against 0.44-0.58, about 7 times lower).
(P3) Domeier & Torsvik 2014 within 30% of Matthews 2016 in 250-410 Ma: FAILED at 1 Myr steps (15 against 26); at 5 Myr steps 28.
(P4) Combined events p < 0.05 in at least 4 of 6 family readings: FAILED (0 of 6; rate ratios 1.3 to 2.0 did appear).
(P5') Scotese & Wright 2018 rate in windows above outside: FAILED (0.73); p > 0.05: HELD (0.84).
(P6) Persistent swaps alone p > 0.05 in most readings: HELD (all seven).
(P7) Mean sides 6 - 12/F in every frame without islands: HELD (2169 of 2169).
(P8) Variance of sides at least 1.5 times PV at every 50 Myr epoch: HELD (minimum 1.58); in single frames it fails in 33 of 2657.
(P9) Three-sided share at least twice PV: HELD in 2534 of 2657 frames; largest side number above PV's 99th percentile in most
frames: HELD (1779 of 2657, 67%).

## 10. Second-round runs, files and credits
Runs (FINAL ok unless stated; nothing left running): earth-indep-pilot (single frames; FINAL FAIL, which found the Scotese & Wright
record limit and a download race, read in section 7), earth-sw18, earth-dt14 (stopped deliberately at 24 of 160 frames: under
shared load it ran at 71 s per frame; rerun as earth-dt14b), earth-dt14b, earth-ts-pilot, earth-ts6, earth-ts-sw18, earth-ts-dt14;
on the two compute machines. Files: results/frames_, events_ and census files of scotese_and_wright2018_rigid and domeier2014_rigid
(the frame files now carry lineage), results/timeseries6.json, timeseries_sw18.json, timeseries_dt14.json (every event with its age,
5 and 10 Myr bins, tests, per-frame neighbour statistics and the PV reference per F).
Credits, in addition to section 2: Scotese & Wright 2018, PALEOMAP Paleodigital Elevation Models (PaleoDEMS) for the Phanerozoic,
Zenodo doi:10.5281/zenodo.5348491, with C. R. Scotese's PALEOMAP plate model (rotations) and its topological plate boundaries;
Domeier & Torsvik 2014, Plate tectonics in the Late Paleozoic, Geoscience Frontiers 5, 303-350; Young et al. 2019 (read at present
day only); both new models downloaded through GPlately's PlateModelManager and resolved with pyGPlates. Reorganisation dates:
Matthews, Seton & Müller 2012 (EPSL 355-356, 283-298), Sharp & Clague 2006 (Science 313, 1281-1284), Whittaker et al. 2007
(Science 318, 83-86), Lonsdale 2005 (Tectonophysics 404, 237-264); kinematic context Matthews et al. 2016 (Global Planet. Change
146, 226-250; the title "Global plate boundary evolution and kinematics since the late Paleozoic" belongs to this 2016 paper) and
Müller et al. 2016. Poisson-Voronoi variance reference: Hinde & Miles 1980 via studies/2026-11-15-tissue-null-models; SciPy
ConvexHull (Qhull) for the spherical Voronoi maps.
