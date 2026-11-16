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
MACROSCOPIC COUNT (15 Nov 2026, last section; scripts/macro.py): swaps not near any cell event within tau ("free") are step-independent
in the foam (within 7% and 14.5% over steps 1 to 4, against 36 to 40% for all swaps), but their rate depends on tau and does not match
Rutenberg-McCurdy's 0.53. On the Earth model almost all swaps are attached to plate events; the 3 to 9 free ones give no rate.
RUTENBERG-McCURDY COUNT (15 Nov 2026, last section; scripts/rm_count.py): their exact rule is an area rule (a T1 counts if all four
bubbles exceed l^2 = rc sqrt(<A>)). By it the foam gives 0.30 macroscopic swaps per vanished cell (rc = 1 pixel), within 20% over
steps 1 to 4, but 0.14 to 0.46 for rc = 2 to 0.5: no scaling state, so 0.53 cannot be tested here. The vanishing rule without a
window removes 99% of the swaps (0.004 to 0.014 left). Total 0.76 against 1.5.
SCALING-STATE FROTH (15 Nov 2026, last section; scaling/): a 2048^2 Potts froth in a tested scaling state gives 0.48 +- 0.02
macroscopic T1 per T2 at rc = 1 pixel (paper 0.53 +- 0.05), step-independent, but 0.64 / 0.32 at rc = 0.5 / 2 and rising over the
window; its mu2 = 1.90 is not the dry froth's 1.24. Total 1.08 against 1.5; shares at l^2 26 / 67 / 6 % against 9 / 84 / 7.
LAW-BUILT FROTH (16 Nov 2026, last section; vfroth/): an off-lattice froth built only from Plateau's 120 degrees, Laplace arcs and
von Neumann's law (checked to 1e-9 degrees and 1e-10), with Rutenberg-McCurdy's own T1/T2 and counting rules, gives 0.250 +- 0.015
macroscopic T1 per T2 (N0 = 1000, 8 seeds), the same at c = 0.5 / 1 / 2 (0.256 / 0.250 / 0.242): the cut-off dependence was a
lattice artefact, but the value is half of 0.53. N0 = 2500 (7 seeds) in a window that passes the scaling test: 0.245 +- 0.011,
cut-off free; stationary mu2 1.59 (theirs 1.24). NOT CONFIRMED.
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


## Macroscopic count: free and attached swaps (scripts/macro.py, tests scripts/test_macro.py; runs in macro/)

VERDICT (15 Nov 2026): in the foam the free swaps are step-independent where all swaps are not, but their rate does not match
Rutenberg-McCurdy and depends on tau. On the Earth almost every swap is attached, and the few free swaps are too few to test.
- Controls pass. Moving-seed Voronoi (no cell ever vanishes): every swap is free, and swaps = logger = Delaunay flips (238 and 168)
  at both steps and every tau. Power runs (births and deaths): free + attached = swaps; attached 0 at tau = 2W, 3 to 4 of 126 at
  tau = 4W. Synthetic map: tests 15/15, with the known free and attached swaps and the free count unchanged when a coarse step
  absorbs an attached swap.
- Foam rung 1, tau = 16 MCS: free swaps per vanished cell 0.102 / 0.101 / 0.095 / 0.096 (seed 1) and 0.093 / 0.087 / 0.079 / 0.078
  (seed 2) at steps 1 / 2 / 4 / 8 MCS. Over steps 1 to 4 they fall by 7% and 14.5%; all swaps under the same rule fall by 36% and
  40%. The prediction (within 15% over steps 1 to 4) HELD, for seed 2 only just. The predicted drop (15 to 30%) was too pessimistic.
  At tau = 32 the free counts are flatter still (within 11% and 8% over all four steps); at tau = 8 they fall by 11% and 15%.
- The step dependence has moved into the attached swaps: sides shed per vanished cell 0.64 / 0.66 at step 1, 0.39 / 0.35 at step 4.
  Those values stay below the 0.98 implied by the literature, as predicted.
- Against 0.53 (Rutenberg-McCurdy): FAILED. The free rate is 0.09 to 0.10 at tau = 16, outside the predicted 0.3 to 0.6. It does not
  settle as tau grows (0.19, 0.10, 0.04 per vanished cell at tau = 8, 16, 32). In this froth nearly every swap involves a cell that
  vanishes within a few tens of sweeps, so the window count measures tau, not a fixed rate. Rutenberg-McCurdy remove only the
  shedding of the vanishing cell itself. Their 0.53 is therefore a different quantity from a window count, and the two cannot test
  each other.
- Earth, Müller 2016, tau = 10 Myr: free swaps 8 / 9 / 7 / 5 (mesh, 3.5 / 3.9 / 3.0 / 2.2 per 100 Myr) and 3 / 4 / 5 / 4 (vector,
  1.3 / 1.7 / 2.2 / 1.7) at steps 1 / 2 / 5 / 10 Myr, out of 29 and 25 swaps at step 1. The prediction (within 20% over steps 1, 2, 5)
  holds for the mesh reading (13%) and fails for the vector reading (+67%). Both are counts of 3 to 9, whose Poisson scatter
  (30 to 60%) is larger than the test, so neither reading decides it. At tau = 20 Myr 0 to 3 swaps are free. In this model
  nearly every swap lies within 10 Myr of a plate split, merge, birth or a clump with a vanishing or new plate, most often such a clump (12 to 13 of the attached
  swaps at step 1), then splits (5 to 7).
- So the macroscopic count makes the foam's swap rate step-independent, but only as a family indexed by tau. It is a defined
  statistic, not a constant to compare across scales. For the Earth model the swaps are mostly a by-product of plate
  reorganisations. The free count there gives no rate yet, and a second model or a longer record would be needed.
- Nothing is left running.

Why: the pairing section found that at a coarse step a swap falling in the same interval as a cell vanishing, splitting, appearing
or merging is absorbed into that event. The foam literature counts such swaps with the cell event ("macroscopic" T1s, Rutenberg &
McCurdy 2005: 0.53 per T2; 3/2 with side-shedding, Herdtle & Aref 1992). macro.py runs pairing.py and eventlog.classify unchanged
and splits the counted swaps in two.

Definitions (fixed 15 Nov 2026 before any run on foam, Earth or sphere frames):
- Cell event: a logger event in which a cell vanishes or appears (death, birth, split, merge, a clump with a born or died cell;
  not a relabel), timed at the later frame of its interval.
- Participants: its born and died cells; for a split, merge or clump also the kept partner of each born or died cell (dominant
  lineage when given, else the kept neighbour that passes eventlog's split/merge neighbourhood test, only when exactly one passes:
  when several pass, as for a four-sided cell vanishing inside one coarse interval, the event counts as a vanishing alone).
  Ring variant (secondary): plus the neighbours of each born or died cell.
- Free swap: a swap counted by pairing.py none of whose four cells is a participant of a cell event within tau of the swap's time
  span (before or after). Attached swap: the rest, each assigned to its nearest such event. Per event type: events, attached
  swaps, and for vanishings the sides shed (attached swaps before the event with the vanishing cell in the lost pair).
  free + attached = swaps is checked in every run.
- Parameters: the main pairing rules (foam W = P = 8 MCS, Earth W = P = 5 Myr, sphere W = P = 2e-4) and tau = 2W as the main
  value; tau = W and 4W reported beside it.
- The rule "only one partner" was added while writing the tests, before any run: the synthetic test at step 2 showed that a
  four-sided vanishing read as a merge passes several neighbours through the test, which attached an unrelated swap.

Tests (scripts/test_macro.py, 15/15; pairing 18/18 and eventlog 33/33 unchanged): a hand-built sphere map (octahedron with a
three-sided cell w) with four known swaps and one death. tau = 3: free 3, attached 1 (the side w sheds 1 before it vanishes);
ring variant free 2; tau = 15: free 2. At step 2 the shed side and the vanishing fall in one interval and are logged as one
event: the swap count drops from 4 to 3 and the free count stays 3. With lineage (w absorbed by z) the merge attaches the swap
of z. NEGATIVE: with no cell event every swap is free at tau 0 and 100; tau = 0 attaches nothing.

Predictions (written 15 Nov 2026 before the runs; one disclosure: a syntax smoke run of the Earth script was made on the local
machine before this section was written, and its last two output lines were seen: the attached swaps per event type for the mesh
reading at tau = 20, steps 5 and 10, small numbers; no free count was seen):
- Control, moving seeds (2 Voronoi, 2 power runs, as in the pairing section): Voronoi has no vanishing, so every swap is free and
  swaps = logger swaps = Delaunay 2-2 flips at both steps and every tau. Power runs: free + attached = swaps; attached at most 15%.
- Foam rung 1, tau = 16 MCS: test = free swaps per vanished cell within 15% over steps 1, 2, 4. Expected to FAIL mildly: the
  pairing diagnosis puts 258 of the 400 swaps lost at step 4 on a vanishing cell (attached, so harmless here), but 34 on a
  neighbouring cell change and 108 on swaps merged or cancelled within the step, which are free at step 1. Expected drop from step 1
  to 4: 15 to 30% (against 36% for all swaps). Value at step 1: 0.3 to 0.6 per vanished cell; it matches Rutenberg-McCurdy if within
  0.53 +- 0.10. Sides shed per vanished cell at step 1: below the 0.98 implied by the literature (the lattice froth lets cells
  vanish as four-sided in one sweep).
- Earth, Müller 2016, tau = 10 Myr: test = free swaps per 100 Myr within 20% over steps 1, 2, 5 (both readings). Expected to HOLD
  (11 of 12 mesh swaps lost at step 5 coincide with a split, birth or merge). Step 10 equals tau and may be lower. Value 3 to 8 per
  100 Myr. The ring variant gives fewer free swaps at every step.

Results (macro/results/*.json and *.log; jobs macro-pilot and macro-runs, FINAL ok; free = primary participants)

| foam rung 1, free swaps per vanished cell (seed 1 / seed 2) | step 1 | 2 | 4 | 8 MCS |
|---|---|---|---|---|
| all swaps, W = P = 8 (pairing section) | 0.764 / 0.773 | 0.621 / 0.600 | 0.485 / 0.460 | 0.360 / 0.342 |
| free, tau = 8 | 0.194 / 0.195 | 0.184 / 0.184 | 0.173 / 0.165 | 0.167 / 0.145 |
| free, tau = 16 (main) | 0.102 / 0.093 | 0.101 / 0.087 | 0.095 / 0.079 | 0.096 / 0.078 |
| free, tau = 32 | 0.040 / 0.038 | 0.039 / 0.037 | 0.036 / 0.035 | 0.038 / 0.037 |
| free, ring variant, tau = 16 | 0.023 / 0.025 | 0.020 / 0.022 | 0.017 / 0.016 | 0.015 / 0.013 |
| attached at tau = 16: sides shed per vanished cell | 0.64 / 0.66 | 0.51 / 0.48 | 0.36 / 0.35 | 0.23 / 0.21 |

| Earth, Müller 2016, free swaps (per 100 Myr) of all swaps | step 1 | 2 | 5 | 10 Myr |
|---|---|---|---|---|
| mesh per boundary, tau = 5 | 18 (7.8) of 29 | 19 (8.3) of 25 | 10 (4.3) of 19 | 11 (4.8) of 11 |
| mesh per boundary, tau = 10 (main) | 8 (3.5) | 9 (3.9) | 7 (3.0) | 5 (2.2) |
| mesh per boundary, tau = 20 | 2 (0.9) | 2 (0.9) | 3 (1.3) | 3 (1.3) |
| vector per pair, tau = 5 | 8 (3.5) of 25 | 10 (4.3) of 22 | 7 (3.0) of 14 | 10 (4.3) of 10 |
| vector per pair, tau = 10 (main) | 3 (1.3) | 4 (1.7) | 5 (2.2) | 4 (1.7) |
| vector per pair, tau = 20 | 0 | 0 | 1 (0.4) | 2 (0.9) |

- Foam cell events at step 1 (seed 1): 493 deaths, 749 merges (a four-sided or larger cell vanishing within one sweep, read as a merge
  into a single neighbour), 108 clumps with a vanished cell; at step 8: 237, 875, 142. Attached swaps per event at tau = 16 and step 1:
  deaths 0.96, merges 0.46, clumps 0.70.
- The ring variant attaches still more and leaves 1 to 2.5% of the foam swaps free, and 1 to 3 of the Earth's.
- Full per-event-type tables (events, attached, before / after, sides shed) for every step and tau are in the json files.


## Rutenberg-McCurdy count: side-shedding removed without a time window (scripts/rm_count.py, tests scripts/test_rm_count.py; runs in rm/)

VERDICT (15 Nov 2026): the paper's exact rule is an area rule, not a vanishing rule, and neither version gives 0.53 in this froth.
- Rule SS (the plan's rule, no window): in foam rung 1 it removes 99% of the swaps. Macroscopic swaps per vanished cell 0.004 /
  0.004 / 0.008 / 0.014 (seed 1) and 0.008 / 0.008 / 0.006 / 0.010 (seed 2) at steps 1 / 2 / 4 / 8 MCS: 5 to 19 swaps in all, far
  below 0.53. Every lost pair but one holds a cell that vanishes later (the froth coarsens from 1383 to 33 cells), and that cell
  almost never gains a side before it goes (median 3 to 4 MCS from the shed to the vanishing). So in a coarsening record this rule
  is nearly "every swap"; it is not the paper's count.
- Rule RM (the paper's own: all four cells larger than l^2 = rc sqrt(<A>)), rc = 1 pixel: 0.303 / 0.276 / 0.253 / 0.219 (seed 1) and
  0.296 / 0.270 / 0.238 / 0.208 (seed 2). Below 0.53, and within 20% over steps 1 to 4 (17% and 19%; the logger's swaps without the
  pairing rule fall by 30% and 32%). But it depends on rc: 0.46 / 0.44 at rc = 0.5 and 0.14 / 0.14 at rc = 2 (step 1). The paper
  expects no dependence on that factor only in the scaling regime; this froth is not in it, so the paper's number cannot be tested
  here. Every swap that rule RM calls microscopic is also side-shedding by rule SS.
- Total (W = P = 8): 0.764 / 0.773 per vanished cell at step 1 against Herdtle and Aref's 1.5, about half, and step-dependent
  (0.36 / 0.34 at step 8). Sides at l^2 (rc = 1): 3-sided 21%, 4-sided 65% / 61%, 5-sided 13% / 16% (paper: 9 / 84 / 7%).
- Control: moving-seed Voronoi (no vanishing): side-shedding 0 and macroscopic = swaps = logger = Delaunay flips (238, 168) at both
  steps. The regenerated foam frames are identical to the saved ones (1500 of 1500, both seeds).

The source, read in full (free arXiv version): A. D. Rutenberg and M. B. McCurdy, "Scaling state of dry two-dimensional froths:
universal angle-deviations and structure", Phys. Rev. E 73, 011403 (2006), arXiv cond-mat/0502287, section III C and Fig. 7. Their
model is a force-based vertex model of a dry froth (films with curvature, vertices in force balance, von Neumann's law, N0 = 10^4
bubbles, scaling regime at late times). Their exact rule, quoted: "We count T1 events distinctly if all bubbles involved are bigger
than l^2, and count T2n events if the bubble has n sides as it shrinks past the scale of l^2", where l = sqrt(rc L(t)) is the
geometric mean of the microscopic scale rc (vertices closer than rc enter a T1; the Plateau-border size) and the mean bubble size
L(t). "Any side-shedding that occurs at microscopic scales should simply be counted as the details of the associated T2 process."
Herdtle and Aref's 3/2 "included microscopic side-shedding events", so it is an upper bound to 0.53 (their words).
So their rule is an AREA rule on all four bubbles of a T1. It is not a rule on later vanishing: a side shed while the bubble is still
larger than l^2 counts as a macroscopic T1, and a T1 in which a bubble smaller than l^2 gains a side is excluded. The plan's
description ("remove only the side-shedding T1s of the cell that later vanishes") is close to it but not the same. Both are counted
here, and neither uses a time window:
- Rule SS (combinatorial, the plan's rule made precise): a counted swap is side-shedding when a cell x of its LOST pair vanishes
  later (first frame after the loss without x, time T_x) and x gains no contact in any counted swap between the loss and T_x.
  Macroscopic (SS) = counted swaps - side-shedding swaps. SS_any (no "no regain" condition) is reported beside it.
- Rule RM (the paper's own rule; needs cell areas): a counted swap is microscopic when one of its four cells has area below
  l^2(t) = rc sqrt(A_box / N(t)) in a frame from the one before its first change to the one of its last change. Macroscopic (RM) =
  counted swaps - microscopic swaps. Main rc = 1 pixel (the Potts froth's microscopic scale is the lattice spacing), also 0.5 and 2.
  Also the side number of each vanishing cell as it shrinks past l^2 (their 9 / 84 / 7 % for 3 / 4 / 5 sides).
- Counted swaps: pairing.py with the main rule W = P = 8 MCS ("paired + persistent"), and W = P = 0 (the logger's swaps) beside it.
  T2 = vanished cells.
- The saved foam frames carry no areas. rm/scripts/rm_foam.py regenerates rung 1 from its seed with the code of foam_pairing.py and
  compares every regenerated frame with the saved line; the areas are used only if all frames are identical.

Tests (scripts/test_rm_count.py; macro, pairing and eventlog tests unchanged): the octahedron map of test_macro.py. S1: four swaps,
one of them (w sheds a side 1 before vanishing) side-shedding, macroscopic 3; the swap in which w GAINS a side is not side-shedding
(negative). S2: w sheds, regains and sheds again before vanishing: side-shedding 1, SS_any 2. At step 2 the shed swap is absorbed
into the vanishing and the macroscopic count stays 3. Areas: rc = 1 makes only the shed swap microscopic; rc = 10 makes both swaps
of w microscopic; w passes l^2 with 4 sides. NEGATIVE: with no vanishing every swap is macroscopic.

Predictions (written 15 Nov 2026 BEFORE any run of rm_count.py, pilot included):
- Control, moving seeds on the sphere (2 Voronoi, 2 power runs, 100 seeds, t 0 to 0.5, steps 1e-4 and 1e-5, W = P = 2e-4): Voronoi
  has no vanishing, so side-shedding 0 and macroscopic = swaps = logger = Delaunay 2-2 flips (238 and 168) at both steps. Power runs:
  side-shedding swaps at most 1.5 per death (deaths 26 and 27).
- Foam rung 1 regeneration: all 1520 frames identical to the saved ones (both seeds).
- Foam rung 1, main rule, step 1: total per vanished cell 0.764 / 0.773 (known from the pairing section), about half of 1.5.
  Side-shedding (SS) per vanished 0.55 to 0.72. Macroscopic (SS) per vanished 0.05 to 0.20: FAILS 0.53 +- 0.10.
  Step test: macroscopic (SS) within 20% over steps 1 to 4 (uncertain: a quarter of the swaps lost at step 4 were not on a
  vanishing cell).
- Rule RM, rc = 1: l^2 grows from about 6 to about 45 pixels as the froth coarsens from 1383 to 33 cells. Macroscopic (RM) per
  vanished 0.25 to 0.50 at step 1, between the SS count and the total, below 0.53; within 20% over steps 1 to 4. The froth is not
  in a scaling state (it coarsens to 33 cells in a 256^2 box), so rc = 0.5 and rc = 2 differ by more than 15% (Rutenberg and
  McCurdy expect no change with the factor only in the scaling regime). Sides at l^2: more four-sided than at pixel size (27%),
  but not 84%: 3-sided 30 to 50%, 4-sided 35 to 55%.
- What a mismatch would mean: the Potts froth is a lattice model at temperature 0.3, with T1s at the lattice scale, no force
  balance at vertices and cells that vanish two- to four-sided within one sweep. It is a different microscopic dynamics from the
  vertex model, and it is small and short. Agreement with 0.53 is therefore not expected from the definitions alone. A count that
  matches in the vertex model may still differ here.

Results (rm/results/*.json and *.log; jobs rm-pilot and rm-runs, FINAL ok). Foam rung 1, per vanished cell (vanished 1350 / 1339 at
every step), seed 1 / seed 2:

| count | step 1 | 2 | 4 | 8 MCS |
|---|---|---|---|---|
| total, W = P = 8 | 0.764 / 0.773 | 0.622 / 0.600 | 0.485 / 0.460 | 0.360 / 0.342 |
| side-shedding (SS), W = P = 8 | 0.760 / 0.766 | 0.618 / 0.592 | 0.477 / 0.454 | 0.346 / 0.332 |
| macroscopic (SS), W = P = 8 | 0.004 / 0.008 | 0.004 / 0.008 | 0.008 / 0.006 | 0.014 / 0.010 |
| macroscopic (SS_any, no regain test), W = P = 8 | 0.000 / 0.001 | 0.000 / 0.001 | 0.000 / 0.001 | 0.000 / 0.001 |
| macroscopic (RM), rc = 1, W = P = 8 | 0.303 / 0.296 | 0.276 / 0.270 | 0.253 / 0.238 | 0.219 / 0.208 |
| macroscopic (RM), rc = 0.5 | 0.464 / 0.443 | 0.415 / 0.386 | 0.350 / 0.327 | 0.290 / 0.267 |
| macroscopic (RM), rc = 2 | 0.140 / 0.141 | 0.129 / 0.137 | 0.126 / 0.124 | 0.125 / 0.110 |
| total, logger's swaps (W = P = 0) | 0.804 / 0.787 | 0.675 / 0.628 | 0.528 / 0.469 | 0.350 / 0.328 |
| macroscopic (SS), W = P = 0 | 0.141 / 0.124 | 0.078 / 0.064 | 0.033 / 0.030 | 0.013 / 0.010 |
| macroscopic (RM), rc = 1, W = P = 0 | 0.425 / 0.385 | 0.358 / 0.325 | 0.298 / 0.260 | 0.214 / 0.201 |

- l^2 at rc = 1 grows from 6.9 to 44.6 pixels (seed 1) as the froth coarsens; at rc = 0.5, 82 to 91 cells vanish from above l^2
  within one sweep. Shed-to-vanish delays (SS, step 1): quartiles 2 / 4 / 9 MCS (seed 1), 2 / 3 / 9 (seed 2).
- Without the pairing rule (W = P = 0) the SS count keeps 0.14 / 0.12 at step 1: unpaired flicker that the rule removes. With the
  rule nearly nothing is left.
- Sides at l^2 (step 1; counts): rc = 1: 2: 12 / 15, 3: 282 / 280, 4: 878 / 822, 5: 178 / 219; rc = 2: 4-sided 55%, 5-sided 36%.
- Sphere power runs (deaths 26, 27): side-shedding 46 and 63, that is 1.8 and 2.3 per death, the same at both steps. In this model a
  cell vanishes only as a triangle, so it sheds n - 3 sides first.

How the findings compare with the predictions:
- Voronoi control: held. Power runs: FAILED (1.8 and 2.3 side-shedding swaps per death, predicted at most 1.5; the prediction
  forgot that these cells vanish only through 3-1).
- Regeneration: held, all frames identical. The prediction said 1520 frames; the record has 1500 (the 20 burn-in sweeps are not
  saved).
- Total at step 1: as known (0.764 / 0.773).
- Side-shedding (SS) 0.76 / 0.77: FAILED, just above the predicted 0.55 to 0.72. Macroscopic (SS) 0.004 / 0.008: FAILED, below the
  predicted 0.05 to 0.20; against 0.53 it fails, as predicted. Its step test cannot be decided: 5 to 19 swaps.
- Rule RM at rc = 1: 0.30 inside the predicted 0.25 to 0.50, below 0.53, within 20% over steps 1 to 4: held. rc = 0.5 against 2
  differs by a factor of 3: held (more than 15%). Sides at l^2: FAILED: 3-sided 21% (predicted 30 to 50%) and 4-sided 61 to 65%
  (predicted 35 to 55%), nearer the paper's 9 / 84% than expected.

What the model difference implies. Rutenberg and McCurdy count in a vertex model in its scaling state, where l^2 lies far from both
the vertex scale and the bubble scale. Our Potts froth is a lattice at temperature 0.3, 256^2 pixels, coarsening from 1383 to 33
cells. l^2 is only 7 to 45 pixels, so no window between the microscopic and macroscopic scales exists, and the count moves by a
factor of 3 when rc moves by a factor of 4. The paper's consistency, 0.53 macroscopic + 0.98 microscopic side-shedding = 1.5, reads
here 0.30 + 0.46 = 0.76: with the sides at l^2 the continuum would shed about 0.9 sides per vanishing cell at small scale, and the
lattice sheds about half of that. The rest vanish four-sided within one sweep, with no swap. So the two models agree on the form
(macroscopic T1s are a sizeable fraction of T2s) but not on the number, and the number here is not yet well defined. A fair test
of 0.53 needs a froth that reaches a scaling state with l^2 far from 1 pixel and far from <A>: rung 1 at 1024^2 or larger, run long,
the step already listed as the foam ladder's next step, with rule RM and rc = 0.5, 1, 2 fixed in advance.
- Nothing is left running.

## Scaling-state froth: Rutenberg-McCurdy count where it is meant to hold (scaling/; scripts scaling/scripts/froth_scaling.py, count_scaling.py)

VERDICT (15 Nov 2026): one of the two 2048^2 froths passes the scaling test fixed in advance. In it, the macroscopic T1 count by
the paper's own rule is 0.48 +- 0.02 per T2 at rc = 1 pixel, at the lower edge of Rutenberg-McCurdy's 0.53 +- 0.05. But the count
is not scale-free here: rc = 0.5 and 2 give 0.64 and 0.32, and the 500-MCS blocks rise from 0.45 to 0.56 as l^2 / <A> falls. So the
number agrees at the natural choice rc = 1 pixel, and the paper's claim that it does not depend on rc FAILS on the lattice.
- Scaling state: seed 2 (2048^2, t = 1000 to 4000 MCS, 3624 to 903 cells, <A> 1157 to 4645 pixels) passes all four quarters (p(n)
  within 0.009, mu2 within 0.05, KS 0.018, slope within 2.7%). Seed 1 fails narrowly in every window tried (mu2 0.056 and slope
  10.5% off in one quarter), and 1024^2 fails (only 948 to 233 cells), so seed 1 and 1024^2 are not counted.
- The stationary state is not the froth's: mu2 = 1.90 (n2, contacts of at least 2 pixel edges: 1.92) against 1.24 +- 0.01
  (Rutenberg-McCurdy) and 1.4 +- 0.1 (Stavans-Glazier experiment); p(3..9) = 0.008 / 0.109 / 0.278 / 0.291 / 0.175 / 0.089 / 0.035.
  Von Neumann's law holds exactly in form (n0 = 6.00, about 1.0 pixel per MCS per side), and <A> is linear in t, but growth over the
  von Neumann coefficient is 1.17 against their 0.898. The Potts froth at T = 0.3 has a wider side distribution than the vertex
  model and the experiment.
- Total counted swaps per T2: 1.08 (step 1), below Herdtle-Aref's 1.5. Side-shedding (rule SS) 0.97 per T2.
- Steps 1 / 2 / 4 / 8 MCS: rule RM 0.480 / 0.476 / 0.465 / 0.461 (step-independent, 4% from step 1 to 8); total 1.08 / 0.99 / 0.89 /
  0.79.
- T2 shares at l^2 (rc = 1), 3 / 4 / 5 sides: 26 / 67 / 6 % against 9 / 84 / 7 %; at rc = 2: 15 / 69 / 15 %.
- Block edges: blocks shifted by 250 MCS give 0.494 and 1.093 (3% and 1.5% from the main blocks).
- Nothing is left running. The frames (about 1 GB per run) stay on the compute machines and are not in git.

What the paper fixes (arXiv cond-mat/0502287v1, read again in full for this section, sections II and III): rc = 0.01 in their
length unit, with initial mean bubble area A0 = 10^3 and N0 up to 10^4 bubbles (box 10^7); T1 enters when two vertices come within
rc, T2 when a bubble's area falls below 10 rc^2. Scaling state: <A> = 0.94 (t~ - t~0) with t~ = t D sigma (von Neumann
dA/dt~ = (pi/3)(n - 6)), so growth over the von Neumann coefficient = 0.94 / (pi/3) = 0.898; mu2 = 1.24 +- 0.01 (they quote the
undrained experiment of Stavans and Glazier 1989 at 1.4 +- 0.1 and Herdtle-Aref at about 1.2); E/Ehex = 0.938; T2 shares at l^2
9 / 84 / 7 % (3 / 4 / 5 sides) +- 2; R_T1 / R_T2 = 0.53 +- 0.05, reached only after a transient of about a decade in t~ (Fig. 7:
t~ from about 10^5 to 10^6, where <A> is 10^5 to 10^6, so l^2 / <A> = rc / L is 1e-5 to 3e-5). Their only statement about
Herdtle-Aref's 3/2 is that it "included microscopic side-shedding events" and is therefore an upper bound; the difference
1.5 - 0.53 = 0.97 is ours, not theirs.

rc in pixels, fixed before any run: their rc is the distance at which vertices merge (the Plateau-border size). In the lattice froth
that distance is the lattice spacing, so rc = 1 pixel (main), with 0.5 and 2 beside it to test their claim that a constant factor in
l changes nothing in the scaling regime. The dimensionless ratio rc / L of the paper (about 1e-5) cannot be reached on any lattice
we can run (it needs bubbles about 10^5 pixels across); at 2048^2 it is 1e-2 at best. This is the one unremovable difference.

Model choice: the Potts froth of the foam ladder (rung 1, potts.py unchanged; Glazier, Gross & Stavans 1987) at T = 0.3, on a 2048^2
torus. The grains stream's curved vertex model (studies/2026-11-15-grains-polycrystals/scripts/vertex2d.py) was considered and not
used: its T1 length scales with the mean boundary (delta = eps <l>), so it has no fixed microscopic scale rc, and only three-sided
grains vanish, so the 3 / 4 / 5 shares are fixed by construction. One change from rung 1, fixed before any run: fragment clean-up is
applied to a copy of the label map for frames and statistics, so saving frames does not change the dynamics.

Rules fixed before any run (count_scaling.py doc): stats every 10 MCS from the start; frames at every MCS inside the window.
Scaling test: window cut into four quarters of equal log t; stationary if every quarter is within 0.015 of the whole window in p(n)
(n = 3 to 9), within 0.05 in mu2, within KS distance 0.03 in the A/<A> distribution, and has an <A>-against-t slope within 10% of the
whole window's; on failure the first quarter is dropped (at most twice). Count only inside the window that passes: rm_count.py
unchanged, blocks of 500 MCS, steps 1 / 2 / 4 / 8 MCS, W = P = 8 (main) and 0, rc = 1 (main), 0.5, 2; blocks shifted by 250 MCS at
step 1 for the block-edge effect. Main test: macroscopic T1 per T2 (rule RM, rc = 1, W = P = 8, step 1) against 0.53 +- 0.05;
total counted swaps per T2 against 1.5; T2 shares at l^2 against 9 / 84 / 7 %.

Predictions (written 15 Nov 2026 before any run of these scripts, pilot included):
- Scaling: reached at 2048^2 from <A> about 50 times the initial area; in the window p(n) stationary, mu2 between 1.1 and 1.5 (Potts
  froths and grain growth are reported near 1.2 to 1.4), <A> linear in t, growth over von Neumann coefficient 0.8 to 1.0.
- Count (rule RM, rc = 1, step 1): 0.35 to 0.55 per T2, higher than at 256^2 (0.30) because l^2 / <A> is smaller. Against
  0.53 +- 0.05: uncertain, more likely below. rc = 0.5 against rc = 2 still differs by more than 15% (separation only a factor L of
  about 30 to 90 between pixel and bubble), so the paper's rc-independence FAILS here.
- Total per T2 at step 1: 0.8 to 1.1, below 1.5 (the lattice loses small-scale shedding: cells vanish four-sided within a sweep).
- Steps: rule-RM count within 20% over steps 1 to 4; total falls by more than 30% from step 1 to step 8.
- T2 shares at l^2 (rc = 1): 4-sided 60 to 75%, 3-sided 15 to 25%, 5-sided 8 to 15%; nearer 9 / 84 / 7 than at 256^2 but not equal.
- Block edges: the shifted blocks agree with the main blocks within 3%.

Results (scaling/results/*_count.json, *.log, */stats.jsonl; scaling/scripts/summary.py prints them; jobs scale-pilot, scale-big,
scale-small, FINAL ok). Seed 2, 2048^2, window 1000 to 4000 MCS, W = P = 8, per T2 (T2 = 2719 at step 1):

| count | step 1 | 2 | 4 | 8 MCS |
|---|---|---|---|---|
| total counted swaps | 1.077 | 0.991 | 0.892 | 0.789 |
| macroscopic (RM), rc = 1 | 0.480 | 0.476 | 0.465 | 0.461 |
| macroscopic (RM), rc = 0.5 | 0.642 | 0.639 | 0.615 | 0.586 |
| macroscopic (RM), rc = 2 | 0.316 | 0.315 | 0.310 | 0.310 |
| side-shedding (SS) | 0.967 | 0.880 | 0.780 | 0.660 |
| macroscopic (RM), rc = 1, W = P = 0 | 0.509 | 0.475 | 0.453 | 0.428 |

Per block (step 1, rc = 1): 0.447 / 0.493 / 0.462 / 0.522 / 0.575 / 0.561 for t = 1000-1500 ... 3500-4000 (T2 1198 / 592 / 368 /
245 / 193 / 123; l^2 34 to 68 pixels). Statistical error of 0.48: about 0.02 (counts 1305 of 2719). Side numbers at l^2 (rc = 1,
step 1): 2: 27, 3: 706, 4: 1810, 5: 176.
Scaling tests (fixed rule; quarters of equal log t): seed 2 [1000, 4000] passes. Seed 1 fails [1000, 4000] (first quarter mu2 2.04
against 1.89), [1420, 4000] (one quarter mu2 off by 0.056) and [1840, 4000] (slope off by 10.5 to 13.8%). 1024^2 fails all three
(mu2 per quarter 1.81 to 2.25, slopes off by up to 21%). mu2 per window: 1.89 / 1.86 / 1.86 (seed 1), 1.90 (seed 2), 2.01 (1024^2).
Froth simulation time 85 min per 2048^2 run (two in parallel), 55 min for 1024^2.

How the findings compare with the predictions:
- Scaling reached at 2048^2: held for seed 2, FAILED for seed 1 (narrowly). mu2 between 1.1 and 1.5: FAILED (1.90). Growth over the
  von Neumann coefficient 0.8 to 1.0: FAILED (1.17 to 1.21). <A> linear in t: held.
- Rule RM, rc = 1, step 1, 0.35 to 0.55: held (0.48). Against 0.53 +- 0.05: at its lower edge, inside by the combined errors.
  rc = 0.5 against rc = 2 differs by more than 15%: held (factor 2.0), so their rc-independence fails here.
- Total 0.8 to 1.1 below 1.5: held (1.08).
- Rule RM within 20% over steps 1 to 4: held (3%). Total falls by more than 30% from step 1 to 8: FAILED (27%).
- T2 shares at l^2: 4-sided 60 to 75%: held (67%); 3-sided 15 to 25%: FAILED (26%); 5-sided 8 to 15%: FAILED (6.5%).
- Block edges within 3%: held (2.9% and 1.5%).

What the model difference implies. The lattice froth reaches a stationary state with the von Neumann law, but its side distribution
is wider (mu2 1.9) than the dry froth's (1.24 to 1.4), and l^2 / <A> is about 1/60 here against about 1e-5 in the vertex model. The
macroscopic count therefore still moves with rc (factor 2 for a factor 4 in rc) and drifts upward as the separation grows (0.45 to
0.56 over the window), as expected if it tends to an rc-free value only when l^2 is far from both scales. The count at rc = 1 pixel
lands on 0.53 within errors, and its drift points towards 0.53 or above, but on a lattice of this size the agreement cannot be
separated from the choice of rc. A fair test needs a froth whose own mu2 is that of a dry froth: a vertex model with a fixed
microscopic rc and T2n deaths (as in Rutenberg-McCurdy), not the Potts lattice.

## Law-built froth: the macroscopic count off the lattice (vfroth/; scripts vfroth/scripts/vfroth.py, vf_count.py)

DICTO, 16 Nov 2026: "otherwise we build a model that matches the laws". Real foams obey established laws (Plateau; von Neumann 1952,
confirmed in real 2D foams by Glazier, Gross & Stavans 1987; Lewis; Aboav), so a model froth that obeys them stands in for real
bubbles through the laws. Rutenberg and McCurdy's 0.53 also comes from a law-based model (a force-based vertex model), so a match is
agreement between two law-built derivations, not an observation of real foam. Nothing below is tuned towards 0.53: the laws go in,
the rate comes out, and 0.53 is only the check.

The model (written here; vfroth.py): films are circular arcs of curvature (p_l - p_r) / sigma (Laplace); three films meet at every
vertex with their unit tangents summing to zero (Plateau, 120 degrees exactly); the froth is held in this equilibrium at every
instant (Newton's method on force balance and areas; the quasi-static limit of Rutenberg and McCurdy's model, the limit Herdtle and
Aref implement); every bubble's area changes exactly by von Neumann's law dA/dt = (pi/3)(n - 6) (sigma D = 1, initial mean area 1).
The only topological moves are T1 (a film shorter than rc) and T2_n (a bubble below 10 rc^2, its n-fold vertex resolved by the
highest-force rule), both Rutenberg and McCurdy's rules; rc = 3.162e-4, their rc / sqrt(A0) = 0.01 / sqrt(1000). After every move
the films relax at fixed areas by implicit gradient flow of the total film length (the tension force is minus its gradient), with
any T1 on the way logged at the same instant. Start: periodic Voronoi of N0 random points relaxed to equilibrium (as they start).
The grains study's vertex2d.py was not reused: it moves boundaries by curvature (grain growth), not by gas diffusion at mechanical
equilibrium, its T1 length scales with the mean boundary, and only three-sided grains vanish; its von Neumann slope of 0.76 comes
from straight short boundaries (angles away from 120 degrees at short films) and three-point boundaries, which this model does not
have: here the slope is pi/3 by construction of exact 120-degree arcs, and it is measured as a check, not assumed.

Rutenberg and McCurdy re-read (arXiv cond-mat/0502287v1, 16 Nov 2026, sections II and III; the source of the rules above): T1 when
two vertices come within rc, the new film of length rc along the highest force; T2_n when a bubble's area falls below 10 rc^2;
sigma = gamma = 1, Gamma = 0.5, D = 0.2 (and 1), dt = 0.01, rc = 0.01, A0 = 10^3, N0 up to 10^4, at least 50 samples; macroscopic
rule as quoted above with l = sqrt(rc L(t)), L = sqrt(<A>); "Scaling l by a constant factor can significantly change the duration
of initial transients, but it should not change results in the scaling regime"; their fit interval is t~ in [2 x 10^4, 2 x 10^5]
(<A> about 20 to 200 A0); results for D = 1 lie higher (0.6 to 0.9) with very long transients. Their model has finite vertex and
curvature mobilities (angles deviate from 120 degrees as t^-1/2); ours is their D -> 0 limit. Our rc definition matches theirs in
both roles (T1 distance and l), and our T2 rule is theirs.

Bug found and fixed before any production run (pilot, 16 Nov): the segment area of a curved film was given to the wrong bubble (a
film bulging into the right bubble enlarges the LEFT one). The force-balanced states then were not minima of film length; the
check that found it compares the tension force with the numerical gradient of the total length at fixed areas, now equal to 1e-8.

Controls (all in vfroth.py test=hex and vf_count.py --selftest, run before the production runs; FINAL ok):
- Known answers: a regular honeycomb is an exact equilibrium (forces 2e-15, angles 120 degrees to 1e-13 degrees, flux 0); one bubble's
  area halved: Newton restores 120 degrees to 1e-13 degrees and every bubble's geometric gas flux equals (pi/3)(n - 6) = 0 to 1e-15;
  a driven T1 (two bubbles on a film shrink, the two at its ends grow) produces exactly that swap (20, 19, 27, 11) and ends with two
  5- and two 7-sided bubbles whose flux obeys von Neumann exactly (slope 1.0471975512 = pi/3, zero 6.0000000).
- Count rule on a hand-made event list: macroscopic 3 / 1 / 1 at c = 0.5 / 1 / 2 as expected (an area equal to l^2 is not counted).
- Negative controls that must fail: a vertex moved off equilibrium shows a 14.3-degree angle error; the deliberately wrong rule
  "every T1 macroscopic" gives 3 instead of 1 at c = 2; the run law=wrong (dA/dt = (pi/3)(n - 6) + (2 pi/3)(A / <A> - 1), area-
  conserving but not von Neumann) must fail the check "geometric gas flux = imposed dA/dt" (planned below).

Pilot seen before these predictions (N0 = 400, one seed, 400 -> 40 bubbles, too small for a scaling state): macroscopic T1 per T2
0.20 / 0.19 / 0.18 at c = 0.5 / 1 / 2 in the candidate window, T2 sides 89 / 8 / 4 % (4 / 3 / 5), total T1 per T2 0.30, E / E_hex
0.938, angles 120 degrees to 3e-8 degrees, flux = (pi/3)(n - 6) to 2e-9.

Plan and predictions (written 16 Nov 2026 before any production run):
- Runs: N0 = 2500, seeds 1 to 8 and N0 = 1000, seeds 1 to 8 (two sizes, pooled per size); rc = 3.162e-4; until N = 50. (First
  launched with N0 = 6400, seeds 1 to 4, in place of N0 = 1000; stopped after 12 minutes, before any count was read, because at the
  shared machine's load it needed about 20 hours.) Side check:
  N0 = 2500 with rc four times larger (seeds 1, 2), for their statement that results do not depend on rc. Negative control:
  law=wrong, N0 = 400.
- Window and scaling test fixed in advance (vf_count.py doc): <A> >= 4 to N >= 100, quarters of equal log t, the Potts study's
  tolerances, first quarter dropped on failure (at most twice), runs of one size pooled.
- Laws in the window: angles 120 degrees within 1e-6 degrees and flux = (pi/3)(n - 6) within 1e-6 at every record (by construction;
  the check is of the solver); mu2 1.2 to 1.5 (Rutenberg-McCurdy 1.24 +- 0.01, undrained experiment 1.4 +- 0.1); E / E_hex 0.93 to
  0.95 (theirs 0.938 +- 0.001); growth of <A> over pi/3 0.85 to 1.0 (theirs 0.898); Aboav-Weaire a 0.8 to 1.4; Lewis: areas rise
  with n, slope reported (froths are known not to follow Lewis's linear law closely; no number predicted).
- T2 shares at l^2: 4-sided 80 to 90 % (theirs 84 +- 2).
- Count: macroscopic T1 per T2 at c = 1: 0.15 to 0.35, BELOW 0.53 +- 0.05 (the pilot's 0.19); c = 0.5 and 2 within 20 % of c = 1
  (cut-off free off the lattice); the two sizes and the seeds agree within errors. Total T1 per T2 0.25 to 0.5, below Herdtle-Aref's
  1.5 (most bubbles vanish four-sided at 10 rc^2 without shedding).
- Verdict rule (from the task): ESTABLISHED only if 0.53 +- 0.05 is matched at fixed rc across at least two cut-offs, two sizes and
  two seeds with the laws checked; CONSISTENT if only at the natural cut-off; NOT CONFIRMED otherwise. Never upgraded.
- What a mismatch would mean: the two law-built derivations differ. Ours is the exact quasi-static limit (D -> 0); theirs has finite
  mobilities, and their own D = 1 runs lie higher than D = 0.2, so the count may depend on the ratio of gas diffusion to film
  relaxation, which no law fixes. Then 0.53 is a property of their model's parameters, not of the laws alone.

Results (16 Nov 2026; vfroth/results/: count_n1000.json, per-run folders with events, stats, crossings and final.json; the
snapshots stay on the compute machine). N0 = 1000, seeds 1 to 8, all FINAL ok, no anomalies, 1192 T2 and 425 T1 in the candidate
windows (149 T2 per run). N0 = 2500 (seeds 1 to 8, main machine) and the rc x 4 side check (N0 = 2500, seeds 1 and 2, second
machine) were still running when this was written (N about 2250 of 2500 after 22 to 33 minutes, at a shared load of 46 on 24
cores; several hours to go); they are a dated follow-up and are not in any number below.

| N0 = 1000, 8 seeds pooled | c = 0.5 | c = 1 (main) | c = 2 |
|---|---|---|---|
| macroscopic T1 per T2 | 0.256 +- 0.015 | 0.250 +- 0.015 | 0.242 +- 0.014 |
| spread between seeds (sd) | 0.023 | 0.021 | 0.021 |
| per seed | 0.21 to 0.28 | 0.21 to 0.27 | 0.21 to 0.26 |

- Total T1 per T2 0.357 (Herdtle-Aref, side-shedding included, 1.5). T2 sides at l^2 (c = 1): 3 / 4 / 5 = 3.4 / 88.1 / 8.5 %
  (Rutenberg-McCurdy 9 / 84 / 7 +- 2).
- Laws, every record in the windows (536 records): largest angle deviation from 120 degrees 7.7e-10 degrees; largest
  |geometric gas flux - (pi/3)(n - 6)| 5.2e-11; regression of flux on n: slope 1.0471975512 (pi/3) and zero 6.0000000 in every
  record. Growth of <A> over pi/3: 1.02 (runs 0.83 to 1.27; Rutenberg-McCurdy 0.898). E / E_hex 0.940 (theirs 0.938 +- 0.001).
  mu2 1.58 (theirs 1.24 +- 0.01; undrained experiment 1.4 +- 0.1). Aboav-Weaire on 90,200 bubble samples: a = 1.11, intercept 8.2505
  against 6a + mu2 = 8.2499 (Weaire's identity holds); Poisson-Voronoi has a = 0.646 (tissue-null-models). Lewis: A_n / <A> =
  0.09 / 0.22 / 0.44 / 0.95 / 1.50 / 2.04 / 2.61 / 3.61 / 4.38 for n = 3 to 11, linear fit slope 0.50 with zero at n0 = 4.0; the
  curve bends at small n (froths are reported to follow a quadratic rather than linear Lewis law; abstract-level, not re-read).
- Scaling test (fixed rule, runs pooled): FAILED in all three windows tried (quarters within tolerance in p(n), KS and mu2 but the
  slope of <A> against t is off by 9 to 24 % in one quarter each time; mu2 1.58 is still above the dry froth's 1.24). So the
  N0 = 1000 count is NOT in a tested scaling state. It is reported as the candidate-window count, not as a scaling-state value.
- Negative control law=wrong (N0 = 400, second machine): FINAL ok, that is it FAILED the check as required: geometric flux against
  the imposed dA/dt differs by up to 6.94, while the geometry itself still obeys von Neumann (flux against (pi/3)(n - 6) 6e-14,
  angles 1.5e-11 degrees off 120): the check catches a growth law that is not von Neumann's.

How the findings compare with the predictions (N0 = 1000 only):
- Laws at the solver's precision: held. mu2 1.2 to 1.5: FAILED (1.58). E / E_hex 0.93 to 0.95: held (0.940). Growth 0.85 to 1.0:
  FAILED narrowly (1.02). Aboav a 0.8 to 1.4: held (1.11). T2 4-sided 80 to 90 %: held (88 %).
- Count at c = 1 0.15 to 0.35, below 0.53: held (0.250 +- 0.015, about 19 standard errors below 0.53, and below its lower edge 0.48 by
  at least 0.2 in every seed). c = 0.5 and 2 within 20 % of c = 1: held (2.4 % and 3.2 %): off the lattice the count is cut-off
  free, which the Potts lattice was not (factor 3.3 at 256^2 and 2.0 at 2048^2 for the same factor 4 in c). Total 0.25 to 0.5:
  held (0.357). Sizes agree: not yet tested (N0 = 2500 running).

VERDICT (16 Nov 2026): rung 4 is NOT CONFIRMED. A froth built only from Plateau's and von Neumann's laws, with Rutenberg and
McCurdy's own T1, T2 and counting rules, gives 0.25 +- 0.02 macroscopic T1 per T2, the same at every cut-off (0.26 / 0.25 / 0.24 at
c = 0.5 / 1 / 2), against their 0.53 +- 0.05. The cut-off dependence of the Potts count is therefore a lattice artefact, but the
lattice's agreement at rc = 1 pixel (0.48) was not: the law-built value is half of 0.53. Limits, stated plainly: one size so far,
the windows did not pass the fixed scaling test (mu2 1.58, not yet the dry froth's 1.24), and our model is the quasi-static limit
of theirs (D -> 0), while their own D = 1 runs lie higher than D = 0.2; so the difference may come from the dynamics between the
laws (how fast films relax compared with gas diffusion), which no law fixes. Either way 0.53 is not a value the laws alone deliver.
Next (decided): read the N0 = 2500 and rc x 4 counts when they finish (same scripts, same rules; a dated follow-up), and if a
scaling window is wanted, run N0 >= 10^4 on a free machine with a local (patch) Jacobian, which the present global solver is too
slow for.
Operations note: the first launch (N0 = 6400) was stopped by killing its wrapper and runs; its own script survived and later
wrote a FINAL FAIL line into the log file of the relaunch. Nothing of its data was used. Stop a job by its process group.

Update (16 Nov 2026, same day, after the report): N0 = 2500 finished (count_n2500.json). Seeds 1 to 4 and 6 to 8 ended done (to
N = 50); seed 5 stopped at N = 1700 when the Newton solve failed (stuck-linesearch; before its window, so not counted, and the
main job therefore ended FINAL FAIL by its own rule). The seven runs pooled PASS the fixed scaling test after the first quarter is
dropped (all quarters within p(n) 0.014, mu2 0.046, KS 0.013, slope 6.8 %). In that tested scaling window (2109 T2, 776 T1):

| N0 = 2500, 7 seeds, scaling window | c = 0.5 | c = 1 (main) | c = 2 |
|---|---|---|---|
| macroscopic T1 per T2 | 0.249 +- 0.011 | 0.245 +- 0.011 | 0.237 +- 0.011 |
| spread between seeds (sd) | 0.015 | 0.015 | 0.015 |

Seeds 0.22 to 0.26 at c = 1. Total T1 per T2 0.368; T2 sides at l^2 4.7 / 85.8 / 9.4 % (3 / 4 / 5); angles within 7.3e-10 degrees of
120; flux = (pi/3)(n - 6) within 4.7e-11; growth 1.05 x pi/3; E / E_hex 0.939; mu2 1.59 (stationary in this froth, not the 1.24 of
their model); Aboav a 1.11; Lewis slope 0.51, n0 4.0. The two sizes agree (0.250 +- 0.015 and 0.245 +- 0.011 at c = 1), and the
count is cut-off free at both. VERDICT unchanged and now on a tested scaling state at the larger size: NOT CONFIRMED, 0.245 +- 0.011
(seed sd 0.015) against 0.53 +- 0.05. The rc x 4 side check (second machine) was at N = 1500 of 2500 and is still a follow-up.
rc x 4 side check (N0 = 2500, rc = 1.2648e-3, seeds 1 and 2, second machine; count_n2500_rc4.json; both runs FINAL ok): 1040 T2 in
the candidate windows, which did NOT pass the scaling test with only two runs pooled. Macroscopic T1 per T2 0.222 / 0.215 / 0.206
+- 0.014 at c = 0.5 / 1 / 2 (seeds 0.19 and 0.24 at c = 1); total 0.363; mu2 1.56; laws held as above. A four times larger
microscopic scale lowers the count by about 12 % (1.6 Poisson errors; the two seeds differ by more), far less than the gap to 0.53;
it is consistent with Rutenberg and McCurdy's statement that rc matters little, and it does not move the verdict.
