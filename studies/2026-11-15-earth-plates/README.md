# Earth plates: counting rule settled on a fixed mesh, persistence, deforming zones, several models (One tissue, three scales, Section 1)

Follows studies/2026-11-15-event-logger (the logger, its validation and the first Müller 2016 census). DICTO, 15 Nov 2026: all
resources on the scutoid Earth, Sun and cosmos work now; this is the 17 Nov follow-up brought forward.

VERDICT (15 Nov 2026): the counting rule is settled and one swap count now holds across step sizes, models and deforming-zone
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
NEXT: (1) one more model with its own plate history (for example Young et al. 2019 or a Scotese/PALEOMAP model) to test the
agreement; (2) persistent swaps per 100 Myr against the known reorganisations (about 100 and 50 Ma); (3) the same rules on the Sun
and void tissues.

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
