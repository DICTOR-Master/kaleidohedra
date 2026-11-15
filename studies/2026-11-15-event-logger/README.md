# Event logger for changing tilings: One tissue, three scales, Step 0 and the first part of Step 1

DICTO, 15 Nov 2026: "I want to start on the new scutoid Earth, Sun and cosmos work ASAP." The plan is "One tissue, three scales"
(14 Nov 2026), which follows #104 (Scutoid Tissues in Four Dimensions). The question: do the Sun's convection cells, the Earth's
plates and the cosmic voids share statistics of births, swaps (neighbour exchanges), splits, merges and deaths? Each system makes
its tiling for its own physical reasons. Nothing here assumes or tests any influence of one on another. If the same ratios appear
at all three scales, the common cause would be geometry. The plate mosaic has the combinatorics of a simple tiling; its history is
a scutoid tissue.

VERDICT (15 Nov 2026): the event logger is built and validated. The Earth present-day check passes on one model. The first plate
event census runs, but its rates are not yet stable.
- Logger: one tool and one tiling format for 2D and 3D, with built-in Euler, triple-junction and balance checks; 23/23 tests,
  negative controls included.
- Validation (a): the #104 sweeps logged as tiling sequences give exactly births 116 / swaps 366 / deaths 116 (120-cell),
  716 / 966 / 716 (truncated 120-cell) and 716 / 2166 / 716 (bitruncated 600-cell), in two directions, all frames passing. The
  truncated 600-cell gives no swap, as predicted. Coarser sampling distorts the counts (swaps down by up to 14% at step 5).
- Validation (b): sphere Voronoi and power diagrams with moving seeds. Every event is a swap, birth or death, equal to the flip count
  found independently, and the same at three time steps (4 runs). One prediction failed: the coarse step gave no clumps.
- Earth, present day: Müller et al. 2016 has 46 plates, 88 junctions (all triple) and 132 boundaries. Euler gives 2, and
  88 = 2 x 44, 132 = 3 x 44 hold exactly (Bird 2003: 52, 100, 150, verified in the paper). Müller et al. 2019 fails Euler (0) in our
  reading: its rigid plates leave 6.5% of the sphere to deforming zones, and one seam (Nazca-Andes) does not close.
- Earth, 230 Ma to the present (Müller 2016), at 1 Myr: 48 swaps, 39 splits, 24 merges, 8 births at junctions, 12 relabels and
  100 clumps; the balance is exact. The counts are strongly step-dependent: swaps fall from 48 to 14 to 10 at 1, 5 and 10 Myr.
  18 of the 48 swaps are back-and-forth pairs. Plates are added and removed by the modellers' choice, so these counts describe the
  model, not the Earth.
- Prior art: no paper found that counts swaps (neighbour exchanges) in solar granulation or in plate reconstructions. The Janin et
  al. plate graph (Zenodo 15863930) has no event classification.
CONTINUED (15 Nov 2026) in studies/2026-11-15-earth-plates: the counting rule, persistence, the Müller 2019 seam and more models.
eventlog.py gained two opt-in options there (contacts counted per boundary; boundary networks in several pieces); with the options
off its behaviour is unchanged, and the tests are now 33/33 (the 23 below plus 10 for the options).
PAIRING RULE (15 Nov 2026, section at the end; scripts/pairing.py): the shared rule pairs split swaps and removes flicker, and it
leaves exact counts unchanged. Swap counts stay step-dependent, because at coarse steps swaps merge with neighbouring cell changes.
NEXT (as it stood): settle the Earth counting rule before any rate is quoted. First, explain the single-contact clumps. Second, a persistence
rule for swaps (fix the tolerance first). Third, close the Müller 2019 seam and run a second model, then compare the two.

## Predictions (written 15 Nov 2026 before any event-logging run; only the present-day plate check below was run first)

(a) Slicing sweeps of the #104 polytopes, generic directions, frames at every corner gap (step 1):
- bitruncated 600-cell: births 716, swaps 2166, deaths 716, nothing else; Euler and the triple-junction formulas hold in every frame;
- 120-cell: 116, 366, 116; truncated 120-cell: 716, 966, 716 (the h-vectors of #104); the same counts for a second direction;
- truncated 600-cell (not simple: six cells at a corner): no swap; frames with junctions of five cells, so the triple-junction
  formulas do not apply there while Euler still holds; events are births, deaths and clumps; balance holds;
- coarser step (every 2nd corner gap): counts change (neighbouring events fall into one step and become clumps): the sampling
  artefact the plan warns of.

(b) Moving seeds on the sphere (300 cells):
- Voronoi (all weights equal): no births or deaths, every event a swap at the fine steps; the swap count is the same at dt and dt/2
  and equals the count of 2-2 flips of the Delaunay triangulation found directly from the triangles;
- power diagram (slowly changing weights): every event a swap, birth or death at the fine steps; logger = flips (2-2, 1-3, 3-1);
  the same counts at dt and dt/2; a coarse step (10 dt) gives clumps.

Earth, present day (any GPlately model): Euler V - E + F = 2 when the plate polygons tile the sphere; a model that is not Bird's
will not have 52 plates. Bird 2003 (PB2002): 52 plates, 100 triple junctions, 150 boundaries (verified in the paper, section 6,
paragraphs 110-112: "There are 100 triple-junction points ... There are no quadruple or higher-order junctions"; "There are 150
plate boundaries"), which satisfy 100 = 2(52 - 2) and 150 = 3(52 - 2).

Earth, time series (written before running any time series; one model, back as far as it goes, 1 Myr steps and a coarser step):
- the balance holds exactly at every step (births + splits - deaths - merges + clump net = change in plates);
- the number of plates grows towards the present (the plan's source: about 10 at 200 Ma against 31 today in one model), so births +
  splits exceed deaths + merges by roughly that difference; this growth is largely the modellers' loss of information back in
  time, not history;
- splits outnumber births at junctions (most new plates arise by splitting);
- swaps: tens per 100 Myr (10 to 60);
- many changes fall together because modelled boundaries switch at the times the modellers chose, so clumps are at least 20% of
  events even at 1 Myr; relabels (a plate ID replaced, nothing else) occur;
- at the coarser step at least one event class changes by more than 20% (swaps fewer, clumps more): the counts are step-dependent
  until shown otherwise.

## Tiling format and logger (scripts/eventlog.py; tests scripts/test_eventlog.py)

One frame per line (JSON): cells (persistent labels), boundaries (one entry per boundary segment; a pair may share several),
optional junctions (cells meeting at each map corner), loops (closed boundaries without junction), optional lineage (parents:
share of a new cell's area from each old cell; heirs: share of an old cell's area going to each new cell). 3D frames: contacts,
optional edges (cells round each edge) and corners (cells at each corner).
Events (plain terms first, #104 names after): swap (two cells stop touching, two others start: the 2-2 move), birth (a three-sided
cell appears at a junction: 1-3), death (3-1), split (one cell divides in two), merge (two cells join), relabel (label change only),
clump (any other local change; logged with its pattern: the rosette events of #104 Lemma 5). In space: contact gained and contact
lost as separate events, birth (1-4), death (4-1), split, merge, relabel, clump. "One place" = the changed cells all touch one
another before or after. Split vs birth and merge vs death come from lineage when given (one parent or heir with 90% or more of
the area); without lineage a three-sided newcomer at a former junction is a birth, a larger newcomer that touches only one old
cell's neighbours is a split. Without lineage, a death next to a swap in the same step can read as a merge: lineage is needed for
real data at coarse steps.
Built-in checks: Euler per frame (sphere V - E + F = 2; 3-sphere V - E + F - C = 0); with all junctions triple, junctions = 2(cells - 2)
and boundaries = 3(cells - 2); balance per step recomputed from the event types (a retyped or deleted event is caught).
Tests: 23/23 pass (birth, death, swap, split and merge with and without lineage, relabel, clump, two separate events in one step,
3D birth / death / contact gained / contact lost on triangulated 3-spheres; NEGATIVE: a birth retyped as swap and a deleted event
row are caught by the balance; a frame missing one boundary fails Euler; a four-fold junction passes Euler and is marked "triple
formulas do not apply").

## Validation (a): polytope sweeps of #104 (job elog-sweep, FINAL ok; scripts/sweep_tilings.py, results/sweep/)
Each sweep is turned into a tiling sequence: one frame midway between consecutive corner heights. A frame is the slice: cells = 3D
cells crossing the hyperplane, boundaries = shared 2D faces crossing it, junctions = polytope edges crossing it. The polytopes are built
as in studies/2026-11-10-t600-scutoid (code copied unchanged). Two generic directions (seeds 7 and 11). All predictions held.

| polytope | frames | step 1 (every corner gap), both directions | Euler / triple formulas | step 2 (seed 7) | step 5 (seed 7) |
|---|---|---|---|---|---|
| 120-cell | 599 | births 116, swaps 366, deaths 116, nothing else | every frame / every frame | 113, 336, 113 + 12 clumps, 3 splits, 3 merges | 98 births, 297 swaps, 104 deaths, 23 clumps, 13 splits, 10 merges |
| truncated 120-cell | 2399 | 716, 966, 716 | every frame / every frame | 703, 924, 703 + 8 clumps, 13 splits, 13 merges | 671, 827, 674 + 31 clumps, 39 splits, 38 merges, 1 relabel |
| bitruncated 600-cell | 3599 | 716, 2166, 716 | every frame / every frame | 696, 2078, 696 + 24 clumps, 20 splits, 20 merges | 670, 1980, 662 + 47 clumps, 40 splits, 51 merges |
| truncated 600-cell (not simple) | 1439 | no swap; 2634 clumps | every frame / do not apply (junctions of five cells) | 2522 clumps, 7 splits, 7 merges | 2431 clumps, 11 splits, 11 merges |

- The exact counts are the h-vectors (1, 116, 366, 116, 1), (1, 716, 966, 716, 1), (1, 716, 2166, 716, 1) of #104, now recovered by a
  general tool that knows nothing of polytopes. The negative control (one event retyped as a swap) was caught in all 8 runs.
- Truncated 600-cell: the clumps have exactly the patterns of the earlier study (cells appear 714 and vanish 714; 2 lost / 0 gained
  371; 1 / 0 227; 3 / 0 118, and mirrors). The logger groups by "all touching", so a corner event of the form 1 lost / 3 gained
  is logged as two clumps (1438 corners give 2634 clumps); the counts per corner are unchanged.
- Coarser steps: neighbouring events fall into one step. Some become clumps, and others are read as splits or merges, because
  without lineage a death next to a swap looks like a merge. The step-5 counts differ from the true ones by up to 14% for swaps.
  This is the sampling artefact the plan warns of, measured on a case where the truth is known.

## Validation (b): moving seeds on the sphere (jobs elog-sphere, elog-sphere2; scripts/voronoi_sphere.py; results/sphere/)
Cell i is the face of the solid {x : n_i . x <= h_i}, projected onto the sphere. Its seed n_i moves slowly; its weight is h_i = 1
for Voronoi, and varies slowly for the power diagram. The combinatorics are those of the convex hull of the points n_i / h_i: the
weighted Delaunay triangulation of #52. 100 seeds, t from 0 to 0.5. We used 100 seeds, not the 300 of the prediction, because
the pilot showed 300 seeds need a far finer time step. Steps dt = 5e-6, 1e-5 and the coarse 1e-4, two random seeds per mode.

| run | cells first -> last | logger at dt 5e-6 = 1e-5 = 1e-4 | independent flip count (all three steps) | Euler / triple formulas |
|---|---|---|---|---|
| Voronoi, seed 1 | 100 -> 100 | swaps 238, nothing else | 2-2 flips 238 | every frame (100001) |
| Voronoi, seed 2 | 100 -> 100 | swaps 168 | 168 | every frame |
| power, seed 1 | 51 -> 63 | swaps 126, births 38, deaths 26 | 2-2: 126, 1-3: 38, 3-1: 26 | every frame |
| power, seed 2 | 62 -> 59 | swaps 108, births 24, deaths 27 | 108, 24, 27 | every frame |

- Every event is a swap, birth or death. The logger agrees with the flip count exactly, and the counts are the same at all three
  steps. Births - deaths = change in cells (38 - 26 = 12; 24 - 27 = -3). The negative control (one event retyped) was caught in
  both power runs. The Voronoi runs have no cell change to retype.
- One prediction FAILED: the coarse step (10 dt) gave no clumps. The logger separates events that fall in one step but at
  different places, so on this system its counts are already step-independent at 1e-4.
- The first run (elog-sphere, results/sphere-run1/) ended FINAL FAIL by its own check. The logger's counts were already identical
  at all steps. The fault was in the reference count, which treated two flips at different places in one step as one change (power
  seed 1, dt 1e-5: logger 126 swaps, reference 125 + one "several at once"). The reference now splits a step's change into groups
  of edge-sharing triangles (elog-sphere2, FINAL ok).

## Earth, present day (scripts/plates.py; results/plates/plates_present_*.json)
Software and data, credited where they are used: pyGPlates 1.0 (GPlates project, GPL-2.0; cite Müller et al. 2018, G-cubed 19,
2243-2261, doi:10.1029/2018GC007584) and GPlately 2.0 with its PlateModelManager (GPL-2.0; Mather et al., Geoscience Data Journal
11 (2024) 3-10, doi:10.1002/gdj3.185). Both were installed in a separate user-space environment on the compute machine. We call
their functions and copy none of their code. Plate models: Müller et al. 2016, Annu. Rev. Earth Planet. Sci. 44, 107-138 (230-0 Ma,
rigid plates); Müller et al. 2019, Tectonics 38, 1884-1907, doi:10.1029/2018TC005462 (250-0 Ma, with deforming zones; CC BY 4.0).
Both were downloaded through GPlately.
Rules, fixed before counting:
- cells = the model's resolved plate polygons; polygons with one plate ID that share a boundary count as one cell;
- a junction = a point where three or more cells meet;
- a boundary = a maximal stretch between junctions shared by one pair of cells. Where one polygon's boundary ends on another's
  side, that side is split at the meeting point. Points within 640 m of each other are one point;
- in Müller 2019, regions covered by no rigid plate (the deforming zones) are cells too, one per connected region.

| model | cells | junctions | boundaries | neighbour pairs | Euler V - E + F | 2(F - 2), 3(F - 2) | mean boundaries per cell |
|---|---|---|---|---|---|---|---|
| Bird 2003 (PB2002; from the paper) | 52 | 100, all triple | 150 | 141 (9 pairs share two boundaries) | 2 | 100, 150: hold | 5.77 |
| Müller et al. 2016, present day | 46 | 88, all triple | 132 | 126 | 2 | 88, 132: hold exactly | 5.739 (= 6 - 12/46) |
| Müller et al. 2019, present day | 63 (52 polygons merged to 50 + 13 deforming zones) | 124 (one four-fold) | 188 | 165 | 0: FAILS | do not apply | 5.97 |

- Müller 2016 passes every check. Like Bird's model, every junction is triple. The pairs that share two separate boundaries
  (132 boundaries against 126 neighbour pairs) are as in Bird's model.
- Müller 2019 does not yet pass. Its rigid plate polygons cover 93.5% of the sphere, and deforming zones fill the rest, so the
  rigid plates alone do not tile. Our reading of the zones as cells leaves Euler at 0 instead of 2. The fault is local: four cells have boundaries in two pieces (Nazca,
  Australia, plate 824 (named NFB in the model) and the Northern Andes flat-slab polygon). The Nazca-Andes seam is where the polygons overlap.
  Until that is resolved, the 2019 model is not used for event counts.
- Neighbour numbers in Müller 2016 (count: plates): 2: 4, 3: 13, 4: 10, 5: 6, 6: 2, 7: 4, 9: 2, 10: 2, 16, 20, 21: one each.

## Earth, first event census: Müller et al. 2016, 230 Ma to the present (jobs elog-plates1, elog-plates10: FINAL ok)
Frames are resolved at 1, 5 and 10 Myr steps, oldest first, so events run forward in time. The lineage for splits and merges uses
40 000 points: each newcomer's points are rotated back with its own plate rotation, and each vanished plate's points forward.
Plates: 10 at 230 Ma, 15 at 184, 26 at 138, 29 at 69, 32 at 23, 46 today. The growth is mostly the reconstruction losing
information back in time. The modellers add and remove plates at times they chose, so every count below describes this model,
not the Earth's own history.
The balance holds at every step (0 failures in all three runs), and the negative control was caught in all three.
33 of 231 frames fail a check (Euler or the triple-junction formulas). These frames have slivers or four-fold meetings in our
reading of the polygons, so the table also gives "clean steps": steps whose two frames both pass every check.

| step | frames passing / all | swaps | births (at a junction) | splits | merges | relabels | clumps |
|---|---|---|---|---|---|---|---|
| 1 Myr, all steps | 198 / 231 | 48 | 8 | 39 | 24 | 12 | 100 |
| 1 Myr, clean steps (178 of 230) | | 39 | 8 | 32 | 15 | 10 | 68 |
| 5 Myr, all steps | 42 / 47 | 14 | 8 | 26 | 18 | 5 | 77 |
| 10 Myr, all steps | 20 / 24 | 10 | 8 | 17 | 14 | 3 | 50 |

Per 100 Myr (1 Myr, all steps): 0-100 Ma: 33 swaps, 22 splits, 17 merges, 7 births, 11 relabels, 73 clumps. 100-200 Ma: 13 swaps,
16 splits, 7 merges, 0 births, 1 relabel, 25 clumps. 200-230 Ma: 2 swaps, 1 split, 1 birth, 2 clumps.
How the findings compare with the predictions:
- The balance held exactly, as predicted.
- Splits outnumber births at junctions (39 to 8), as predicted.
- Swaps: 33 and 13 per 100 Myr. This is inside the predicted range of 10 to 60.
- Clumps are 43% of events at 1 Myr (predicted at least 20%).
- STEP DEPENDENCE, predicted and found strong: swaps fall from 48 to 14 to 10 as the step grows from 1 to 5 to 10 Myr. 18 of the
  48 swaps at 1 Myr are back-and-forth: 9 sets of four plates swap and swap back. A coarser step cancels these pairs. Clumps do not
  stand in for the lost swaps; their number falls too (100, 77, 50).
- Births (8) are the same at every step. They are the only count that did not change with the step.
- Not yet explained: 13 "one contact lost, nothing else" and 11 "one contact gained" clumps. A clean triple map cannot have them
  (8 and 4 remain on clean steps). They may be swaps whose two pairs of plates do not all touch, or four-fold meetings. To examine
  before any rate is quoted.
- So no event rate from this model is yet stable enough to compare across systems. The plan's stopping rule applies: decide a
  tolerance, and resolve the flicker (for example, count only swaps that persist for 3 Myr or more) before counting again.

Runs: elog-pilot (sweep and sphere parts passed; the plate part first failed on a pyGPlates call signature, which was fixed and
the plate pilot rerun: 4 frames in 7.4 s), elog-sweep, elog-sphere (FAIL, see above), elog-sphere2, elog-plates1, elog-plates10.
Nothing is left running.

## Prior art (free sources only; 15 Nov 2026; "abstract only" = full text not read)
- Swaps in solar granulation: none found. Papers that track cells count births, deaths, splits and merges of single cells:
  - DeRosa & Toomre 2004, ApJ 616, 1242, doi:10.1086/424920 (abstract only): more than 3000 supergranules; merging and fragmentation
    shape the histories of more than half of them;
  - Malherbe, Roudier, Stein & Frank 2018, arXiv:1804.01870 (abstract only): trees of fragmenting granules;
  - Solar Phys. 221 (2004) 23-32 (snippet only): mean supergranule lifetime about 22 h.
  Cell-network statistics of single frames exist without time events:
  - Schrijver, Hagenaar & Title 1997, ApJ 475, 328 (abstract only): granules and the supergranular network are close to Voronoi
    foams;
  - A&A 282 (1994), "Solar granulation and statistical crystallography" (snippet only): the Aboav-Weaire law holds for granules;
  - Berrilli et al. 2004, Solar Phys. 221, 33 (abstract only): pair correlations;
  - Del Moro et al. 2015, arXiv:1501.05444 (abstract only): a deforming Voronoi network of granules.
  Counting neighbour exchanges in granulation looks open.
- Janin, Coltice, Tierny & Chamot-Rooke. Zenodo record 15863930 (read in full) is the supplement to Janin et al. 2025, Nature
  Geoscience, doi:10.1038/s41561-025-01772-7 (paywalled, not read): a plate graph of 474 Myr of the Coltice et al. 2019 convection
  model, in .dot and .jpg, CC BY 4.0, with no README. It gives no event classification and no counts. EGU23-12628 (abstract read)
  describes plate tracking with the Topology ToolKit and reorganisations in words only. The .dot file could be parsed for splits
  and merges (a lead).
- Domokos, Jerolmack, Kun & Török 2020, PNAS, doi:10.1073/pnas.2001037117, arXiv:1912.04628 (read). The plates meet "almost
  exclusively at 'Y' junctions", with mean nodal degree 3.0 and 5.8 corners per cell, close to a Voronoi mosaic. Their SI uses Bird
  2003: 52 plates, 100 triple junctions, 150 boundaries, 5.769 corners per cell. No time evolution.
- Morra, Seton, Quevedo & Müller 2013, EPSL 373, 93-101, doi:10.1016/j.epsl.2013.04.020 (free EarthByte copy read). Plate-size
  distributions at 1 Myr steps, 200-0 Ma; the mosaic swings between heterogeneous and homogeneous states over about 100 Myr; at
  least 8 plates at any time. Splits and merges appear only as annotated events. No neighbour statistics, no event counts.
- Bird 2003, G-cubed 4(3) 1027, doi:10.1029/2001GC000252 (free copy read). Section 6, paragraphs 110-112: 52 plates; "There are 100
  triple-junction points ... There are no quadruple or higher-order junctions"; "There are 150 plate boundaries". Bird states the
  formulas junctions = 2(plates - 2) and boundaries = 3(plates - 2) himself. So the plan's check is Bird's own, and we credit it to
  him. Anderson, "How many plates?", Geology 30 (2002) 411-414 (year checked).
- Counted events in plate reconstructions: none found. Cosmic voids:
  - Sutter et al. 2014, arXiv:1403.7525 (read): merger trees; mergers rare (about 5% violent, almost all voids a single line of
    descent); destruction at most about 4% per snapshot early on; neighbour changes not tracked;
  - Wojtak, Powell & Abel 2016, arXiv:1602.08541 (abstract only): a continuous mapping instead of matching.
- Sources checked (pages): zenodo.org/records/15863930; arXiv 1912.04628 (abstract and PDF); EarthByte Morra et al. 2013 PDF; a free
  Bird 2003 PDF (university e-learning copy); ar5iv 1403.7525; EGU23-12628; github.com/GPlates/gplately; pypi.org/project/pygplates;
  the EarthByte Müller 2019 page with its data folder and License.txt; authors.library.caltech.edu/95264. Abstract pages: arXiv
  1602.08541, 1804.01870, 1807.07479, 1501.05444.
- Search snippets only: DeRosa & Toomre 2004; Solar Phys. 221 (both papers); Schrijver et al. 1997; A&A 282 (1994); BAICz 31, 362
  (1980); Anderson 2002.
- Blocked: nature.com (paywall); Springer; NASA ADS (HTTP 405); AGU/Wiley (HTTP 403); peterbird.name.
- Searches with no relevant hit: "T1" OR "neighbour exchange" solar granulation topological network granules; granulation
  "Aboav-Weaire" OR "Lewis law"; "Delaunay"/"Voronoi" "topological" granules "neighbor exchange"/"T1 process" photosphere; plate
  tectonic reconstruction topology graph network "triple junction" statistics neighbours evolution.

## Pairing and persistence rules for swaps (scripts/pairing.py, tests scripts/test_pairing.py; runs in pairing/)

VERDICT (15 Nov 2026): the rule is fixed, tested and shared. It removes flicker and pairs split swaps, and it leaves exact swap counts
unchanged. It does NOT make swap counts step-independent, in the foam or on the Earth. The remaining step dependence has a different
cause, now measured: at a coarser step a swap falls into the same interval as a cell vanishing or appearing next to it, and the
logger then records one combined event (a clump, death or merge) instead of a swap. No pairing or persistence rule can undo that.
- Controls: on the moving-seed sphere the main rule (W = P = 2e-4) gives counts identical to the logger and to the Delaunay flips in
  all 4 runs at both steps (238, 168, 126 and 108 swaps). The wide rule (W = P = 1e-3) cancels one genuine swap-and-reverse pair in
  one run (168 -> 166, 1.2%; predicted at most 2%). The synthetic flickers collapse to zero, and a split swap 3 frames apart is
  paired at W >= 3 and not at W = 2 (tests, 18/18).
- Foam rung 1 (main rule W = P = 8 MCS): swaps per vanished cell 0.76 / 0.62 / 0.49 / 0.36 at steps 1 / 2 / 4 / 8 MCS (seed 1),
  0.77 / 0.60 / 0.46 / 0.34 (seed 2), against 0.80 / 0.68 / 0.53 / 0.35 without the rule. The prediction (within 15% over steps
  1 to 4) FAILED. At step 1 the rule pairs 272 split swaps, cancels 199 flickering swaps and 322 flickering halves, and leaves
  617 halves of 1356. Of the swaps counted at step 1 and missing at step 4 (400 and 436), 65% and 67% involve a cell that vanishes
  in that interval: the side-shedding of a shrinking cell just before it vanishes. A further 9% and 10% have a neighbouring cell
  change, and 27% and 22% are joined with other contact changes or left as halves. Against the published values, the step-1 count
  0.76 to 0.77 lies between 0.53 (macroscopic, Rutenberg & McCurdy 2006) and 1.5 (side-shedding included, Herdtle & Aref 1992).
  The step-4 count 0.46 to 0.49 is near 0.53, as expected if the coarse step merges side-shedding into the vanishing.
- Earth, Müller 2016 (main rule W = P = 5 Myr): swaps per 100 Myr 10.9 / 9.6 / 6.1 / 4.3 at steps 1 / 2 / 5 / 10 Myr (vector
  reading) and 12.6 / 10.9 / 8.3 / 4.8 (mesh reading, per boundary). Without the rule: 20.9 / 13.9 / 6.1 / 4.3 and 27.0 / 20.0 /
  8.3 / 4.8. Steps 1 and 2 now agree within 14%. Step 5 is still 34 to 44% lower, so the prediction (within 20% over steps 1 to 5)
  FAILED. At W = P = 10 Myr steps 1 and 2 are equal (18 / 18 vector, 16 / 17 mesh) and step 5 is 19 to 33% lower. Of the 12
  mesh swaps missing at step 5, 11 fall together with a split, birth or merge in the same 5 Myr interval; 1 is a cancellation.
  A 150 km tolerance makes it worse (many more halves; a hard cut makes events of its own, as the Earth-plates stream found).
- So the stable quantity is not "swaps" at any one step. Two cures remain: frames fine enough that no swap shares an interval with a
  cell change (the foam and Earth series already give step 1 as the finest), or a count defined to exclude swaps within a fixed
  physical time of a neighbouring cell change. The second is the macroscopic count of the foam literature. It is the next step, to
  be fixed before counting.

The problem, seen by three streams: a swap is often logged in two halves, one contact lost in one frame and the new contact gained
in a later one, so swap counts depend on the time step (foam rung 1: 831 + 525 single-contact clumps against 1085 clean swaps,
T1/T2 0.80 / 0.68 / 0.53 at steps 1 / 2 / 4; Earth, vector reading: 13 + 11 such clumps, swaps 48 / 14 / 10 at 1 / 5 / 10 Myr).
The null-model theory (studies/2026-11-15-tissue-null-models) says that with jittery boundaries swap counts scale with the frame
rate; only net counts are stable unless a persistence or pairing rule is fixed before counting. pairing.py fixes such a rule once,
for every stream. It runs eventlog.classify unchanged and post-processes; eventlog.py itself is not changed.

Rules (all times physical, never frame counts; W, P and tol are parameters logged in every output):
- T (tolerance tol, optional; needs boundary lengths): a contact shorter than tol is removed from the frame before logging. Its two
  end junctions merge into one four-fold junction, so Euler is unchanged.
- P (persistence): a contact change counts only if the new state lasts at least P. Otherwise it is a flicker and is cancelled, so a
  back-and-forth within P (lost and regained, gained and lost, a swap and its reverse) cancels both halves. A logged swap counts
  only if both its changes are accepted: the new contact survives P and the old contact stays lost P. A change that reaches the end
  of the record is accepted and reported as censored.
- W (pairing): a lost contact (a, b) and a gained contact (c, d) form one swap if a, b, c, d are four distinct cells, c and d were
  both neighbours of a and of b in the last frame before the loss (the 2-2 pattern), and the two times differ by at most W (gain
  before or after the loss). Losses in time order take the nearest admissible gain; each half is used once. Unpaired halves stay
  single-contact events.
Order: T, then the logger, then P, then W. The Earth-plates stream has its own rules (studies/2026-11-15-earth-plates/scripts/swaps.py:
a join through four-fold junctions and a two-sided persistence k measured before and after). pairing.py differs: W pairs halves without
requiring a four-fold junction in every frame between, and P is measured forward from each change.

Tests (scripts/test_pairing.py, 17/17; eventlog's own tests unchanged, 33/33): a flicker of whole swaps, of halves, and of mixed
halves each collapses to zero swaps. A swap split into halves 3 frames apart is paired at W = 3 and W = 5, not at W = 2, and the
window is physical (the same sequence at half the time step pairs at W = 1.5 and not at W = 1.0). A gain before its loss is paired.
A swap and its reverse 5 apart count 2 at P = 3 and 0 at P = 6. At P = W = 0 the count equals the logger's. NEGATIVE: a loss and a
gain that are not the 2-2 pattern stay unpaired. The tolerance turns a short boundary into a four-fold junction with Euler kept,
and a swap seen through shrinking boundaries is paired back into one swap when W covers the gap.

Parameters and predictions (written 15 Nov 2026 BEFORE any run in pairing/):
- Control, moving seeds on the sphere (2 Voronoi, 2 power runs, 100 seeds, t 0 to 0.5, steps 1e-5 and 1e-4): main rule W = P = 2e-4
  gives counts identical to the logger and to the Delaunay flips at both steps, in all 4 runs. A wide rule, W = P = 1e-3, is
  reported too. It may cancel a few genuine quick reversals; predicted to differ by at most 2%.
- Foam rung 1 (dry 2D Potts froth, seeds 1 and 2 as in the pilot, steps 1, 2, 4, 8 MCS): main rule W = P = 8 MCS, tol 0. Also
  W = P = 16 MCS and W = P = 8 MCS with tol = 2 pixel edges. Swaps per vanished cell with the main rule agree within 15% across
  steps 1 to 4 (step 8 equals the rule's own scale and may differ). The value lies between the macroscopic 0.53 and the 1.5 that
  includes side-shedding (Rutenberg & McCurdy 2006; Herdtle & Aref 1992), near 1.0.
- Earth, Müller 2016, 230 Ma to now (vector reading of this study and the 15 km mesh reading of the Earth-plates stream, both
  read only, steps 1, 2, 5, 10 Myr): main rule W = P = 5 Myr, also W = P = 10 Myr; contacts per pair and per boundary
  (by_segment); mesh also with tol = 150 km. With the main rule, swaps per 100 Myr agree within 20% across steps 1, 2 and 5; at
  10 Myr they are lower, because events closer than 10 Myr cancel in the frames themselves. The value is 8 to 15 per 100 Myr.

Results (pairing/results/*.json and *.log; jobs pairing-pilot, run twice, the first stopped by its own check on a label-type fault
in pairing.py, which was fixed and a test added; pairing-runs and pairing-diag, FINAL ok). Rule sets (20, 20) Myr for the Earth and
(32, 32) MCS for the foam were added after the pilot and before the runs.

| foam rung 1, swaps per vanished cell (vanished 1350 / 1339) | step 1 | 2 | 4 | 8 MCS |
|---|---|---|---|---|
| no rule, seed 1 / seed 2 | 0.804 / 0.787 | 0.675 / 0.628 | 0.528 / 0.469 | 0.350 / 0.328 |
| W = P = 8 (main) | 0.764 / 0.773 | 0.621 / 0.600 | 0.485 / 0.460 | 0.360 / 0.342 |
| W = P = 16 | 0.737 / 0.738 | 0.601 / 0.568 | 0.456 / 0.425 | 0.313 / 0.304 |
| W = P = 32 | 0.669 / 0.650 | 0.541 / 0.500 | 0.423 / 0.378 | 0.290 / 0.271 |
| W = P = 8, tol 2 pixel edges | 0.590 / 0.565 | 0.428 / 0.407 | 0.293 / 0.276 | 0.209 / 0.206 |

| Earth, Müller 2016, swaps (per 100 Myr) | step 1 | 2 | 5 | 10 Myr |
|---|---|---|---|---|
| vector reading, per pair, no rule | 48 (20.9) | 32 (13.9) | 14 (6.1) | 10 (4.3) |
| vector, per pair, W = P = 5 (main) | 25 (10.9) | 22 (9.6) | 14 (6.1) | 10 (4.3) |
| vector, per pair, W = P = 10 | 18 (7.8) | 18 (7.8) | 12 (5.2) | 10 (4.3) |
| vector, per boundary, W = P = 5 | 27 (11.7) | 23 (10.0) | 16 (7.0) | 9 (3.9) |
| mesh, per boundary, no rule | 62 (27.0) | 46 (20.0) | 19 (8.3) | 11 (4.8) |
| mesh, per boundary, W = P = 5 | 29 (12.6) | 25 (10.9) | 19 (8.3) | 11 (4.8) |
| mesh, per boundary, W = P = 10 | 16 (7.0) | 17 (7.4) | 13 (5.7) | 11 (4.8) |
| mesh, per boundary, W = P = 20 | 11 (4.8) | 10 (4.3) | 6 (2.6) | 4 (1.7) |
| mesh, per boundary, tol 150 km, W = P = 5 | 24 (10.4) | 16 (7.0) | 15 (6.5) | 6 (2.6) |

- Sphere control: identical with and without the main rule in all 8 cases (4 runs x 2 steps). Pairs found: 0, cancellations: 0.
  The power runs include births and deaths (38 and 26; 24 and 27), which the rules leave alone.
- The Earth mesh reading at W = P = 5 gives 29 / 19 at steps 1 / 5. The Earth-plates stream's two-sided rule (k = 5) gives 26 / 19
  on the same frames, so the two rules agree at the coarse step and differ by 3 swaps at the fine one.
- Foam frames: the dry2d branch of the foam ladder (same seeds and parameters as its pilot r1 runs; the raw counts reproduce the
  pilot's 1085 / 911 / 713 swaps exactly) rerun with every frame saved with its boundary lengths. The frames (5 MB each, gzip) stay
  on the compute machine and can be regenerated from the seed.
- Foams and the tissue picture: in Mughal, Cox, Weaire, Burke & Hutzler 2018 (Philos. Mag. Lett. 98, 358-364,
  doi:10.1080/09500839.2018.1552806; arXiv:1809.08421, read), a single layer of soap bubbles between two concentric cylinders forms
  scutoids: a T1 swap on the inner surface that is absent on the outer one, that is, a swap seen through the depth of one layer of
  cells. They show single configurations (Surface Evolver, 144 cells, and a first experiment). They count no T1s and give no rates.
  The counts here are the time-wise version of the same swap. DICTO pointed to the paper.
- Nothing is left running.

