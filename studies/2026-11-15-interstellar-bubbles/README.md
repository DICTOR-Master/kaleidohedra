# Foam ladder up to interstellar bubbles: One tissue, three scales (now four), interstellar-gas stream

DICTO, 15 Nov 2026: "yes add interstellar gas stream", then "simplest most basic foam and bubbles upwards". This stream is a ladder of
five rungs: (1) dry 2D soap froth, (2) wet 2D foam, (3) dry 3D foam, (4) foam with bubble births, (5) bubbles blown by supernovae in
interstellar gas. Every rung gets the same event census with the shared logger (studies/2026-11-15-event-logger, used unchanged,
md5 2e2b526f... recorded in every result). Each system makes its tiling for its own physical reasons. Nothing here assumes or tests any
influence of one system on another. The froth has the combinatorics of a simple tiling; its history is a scutoid tissue.

## VERDICT (pilot, 15 Nov 2026)
- **Rungs 1 to 4 are feasible now.** One cellular Potts code gives all four. Every frame tiles the box, and the mean neighbour number
  ends at exactly 6.0 on the torus, as Euler requires. All 11 pilot runs pass the logger balance (0 failures), and the negative control
  is caught in all 11.
- **Rate counts are not yet stable under the time step.** On a lattice, most neighbour swaps are logged in two halves: one contact is
  lost in one frame and the new contact is gained in a later one. Rung 1 (seed 1) has 831 "one contact lost" and 525 "one contact gained"
  clumps against 1085 clean swaps. Swaps per vanished cell are 0.80 / 0.68 / 0.53 at steps 1 / 2 / 4. This is the open single-contact
  clump problem of the Earth stream. It needs the same cure: a pairing rule (a loss and a gain among the same four cells within k
  frames count as one swap), with k and the tolerance fixed before counting.
- **The most stable number so far is a rung-4 count.** It is the count of injected bubbles: births 445 / 430 / 403 and splits
  242 / 242 / 237 at steps 1 / 2 / 4, with 709 injected and all 709 accounted for.
- **Rung 5 (toy) fails as a tiling under the stated cell rule.** The rule is: markers = hot gas below a density threshold; cells =
  watershed basins. Results:
  - A new bubble in dense gas starts as an island inside another cell: about 30 island cells per frame among about 60 cells.
  - Mean neighbours are only 2.2 to 3.4.
  - Euler fails in 223 of 240 frames even with islands allowed (nested islands; cells that are not discs).
  - Swaps are almost absent (0.01 per vanished cell).
  - Split and merge counts per unit time rise 2.8 times when the step is cut from 1 to 0.25. This is flicker, not physics.
  - The threshold (0.05 to 0.2) and the marker size (4 to 16 pixels) move the counts by +5% and -16%; a second seed moves them by +17%.
- **So the interstellar rung needs a different cell rule before any count means anything.** Candidates: hot regions as cells with the
  dense gas shared out by distance (a power-diagram-like rule, which keeps cells as discs); or the full 3D box, where an embedded bubble
  is a contact, not a hole.
- **Real ISM data give no usable time series for this.**
  - Observations give one epoch only (PHANGS-JWST bubbles, THINGS HI holes, Milky Way bubbles).
  - The public TIGRESS release (solar-neighbourhood model R8) has selected snapshots about 10 Myr apart. That is longer than a bubble's
    life, so it is too coarse. Snapshots every 1 Myr are "available on request".
  - FIRE-2 public snapshots are far coarser. No SILCC public release was found.

## Ladder: what each rung is, and how it differs
| rung | system | driver | births? | cells (pilot) | dimension | time span (pilot) |
|---|---|---|---|---|---|---|
| 1 | dry 2D froth | surface tension; gas diffuses from small to large bubbles (coarsening; von Neumann's law) | no: only swaps (T1) and vanishings (T2) | 1383 to 33 | 2 (torus 256^2) | 1500 MCS |
| 2 | wet 2D foam (liquid 14-16%) | as 1, with liquid in the Plateau borders | no | 1262 to 30 | 2 | 1500 MCS |
| 3 | dry 3D foam | as 1, in space | no | 444 to 19 | 3 (torus 40^3) | 300 MCS |
| 4 | 2D foam with a gas source | as 1, plus bubbles nucleated at triple junctions and inflated for 100 MCS (pressure-driven) | yes | 1383 to 139 | 2 | 1500 MCS |
| 5 | supernova bubbles in gas (TOY) | explosive: imposed growth, stall, cooling; hot regions join | yes, as islands | about 60, steady | 2 (slice) | 60 time units |

## Pilot results (job ism-ladder-pilot, FINAL ok; results/pilot/*.json and *.log)
The logger counts are at step 1. "Vanished" means all cells that disappeared, whatever their logged type. "Swaps/vanished" uses clean
swaps only (3D: contact gains plus losses).

| run | swap | death | merge | clump | birth / split | vanished | swaps/vanished at steps 1 / 2 / 4 | Euler: strict / islands allowed |
|---|---|---|---|---|---|---|---|---|
| r1 dry 2D, seed 1, T 0.3 | 1085 | 493 | 749 | 1625 | 0 | 1350 | 0.80 / 0.68 / 0.53 | 6 / 0 fail of 1500 |
| r1 dry 2D, seed 2 | 1054 | 476 | 751 | 1607 | 0 | 1339 | 0.79 / 0.63 / 0.47 | 11 / 0 |
| r1 dry 2D, T 0 | 1126 | 531 | 886 | 2014 | 0 | 1558 | 0.72 / 0.61 / 0.51 | 0 / 0 |
| r2 wet 2D | 3405 | 499 | 618 | 4335 | 0 | 1232 | 2.76 / 1.90 / 1.19 | 10 / 0 |
| r3 dry 3D | lost 1366, gained 678 | 72 | 0 | 1200 | 0 | 425 | 4.81 / 3.13 / 1.64 | not built (no edges or corners) |
| r4 births | 2198 | 743 | 1041 | 3393 | 445 / 242 | 1953 | 1.13 / 1.02 / 0.87 | 7 / 0 |
| r5 toy, dt 0.25 | 7 | 33 | 326 | 751 | 2 / 339 | 664 | 0.011 | 240 / 227 |
| r5 toy, dt 1 | 2 | 9 | 118 | 366 | 4 / 120 | 720 | 0.003 | 60 / 55 |
| r5 toy, theta 0.2 | 9 | 34 | 339 | 772 | 1 / 357 | 672 | 0.013 | 240 / 223 |
| r5 toy, amin 16 | 6 | 33 | 274 | 651 | 4 / 285 | 538 | 0.011 | 240 / 224 |
| r5 toy, seed 2 | 10 | 48 | 363 | 920 | 4 / 395 | 902 | 0.011 | 240 / 223 |

- **Reference values for rung 1** (from Rutenberg & McCurdy 2006; the tissue-null-models stream lists them too):
  - T1 per T2 = 0.53 ± 0.05 counted macroscopically.
  - 3/2 when side-shedding at small scale is included (Herdtle & Aref 1992, as quoted there).
  - Our step-1 value of 0.72 to 0.80 lies between the two.
  - Pairing the split halves of swaps would move it up, towards 1.2. This is an estimate from the clump counts, not yet a measurement.
- **Sides of vanishing cells** (rung 1, seed 1, 1350 cells): 2-sided 20%, 3-sided 51%, 4-sided 27%, 5-sided 1.4%. Rutenberg & McCurdy find 9 / 84 / 7 %
  for 3 / 4 / 5 sides. Their sides are taken when the cell reaches a fixed small area. Ours are taken one frame before the cell
  vanishes, at pixel size, where lattice cells shed sides (2-sided lenses are lattice artefacts). This is not yet a like-for-like
  comparison. Recording the side number at a fixed small area is the fix.
- **Rung 2:**
  - It has 3.5 times the swaps of rung 1 per vanished cell.
  - Part of that may come from the tiling rule (liquid joins the nearest bubble), which makes four-fold corners flicker at Plateau
    borders. Its step dependence is the strongest of the 2D rungs.
  - The liquid fraction stayed between 13.7% and 16.3% (target 15%).
- **Rung 3:**
  - The box coarsened to 19 cells, too few by the end. The mean contact number fell from 13.8 to 11.2 (finite size).
  - The 3D analogue of the split swap is the clump "1 lost, 1 gained" (434). The full run needs a larger box (at least 96^3) and the
    pairing rule.
- **Rung 4:** births at triple junctions are logged as birth (1-3) or split. Swaps per new cell = 3.1.

## Method
- **Potts foam (scripts/potts.py), rungs 1 to 4.**
  - The large-Q Potts model of froth: each bubble is a domain of one label, and the energy is the number of unlike neighbour pairs.
    Glazier, Gross & Stavans 1987 used it for 2D froth; Anderson, Srolovitz, Grest & Sahni 1984 for grain growth; Glazier 1993 in 3D.
  - The area-constraint term of the cellular Potts model (Graner & Glazier 1992) is used for the liquid (rung 2) and for gas-fed
    newborn bubbles (rung 4).
  - Interactions reach the 8 nearest sites in 2D and the 26 nearest in 3D. Metropolis copy-a-neighbour moves on parity sub-lattices.
  - Start: periodic Voronoi of N random seeds.
  - Rung 2 settings: liquid-bubble energy 0.6, so films stay dry and the liquid sits in the borders.
  - Rung 4 settings: Poisson nucleation, mean 0.5 per MCS, at random triple junctions. Disc radius 3, then the target area grows
    2 pixels per MCS for 100 MCS, after which the bubble is free.
- **Cells and graphs (scripts/tiles.py).**
  - The 2D graph, junction, segment, loop and matching code is copied unchanged from the Sun stream (credited in the file), so both
    streams tile alike.
  - After each recorded frame, every label is made one connected piece: stray fragments join their majority neighbour, and the moved
    pixels are logged.
  - Torus Euler V - E + F = 0 is checked per frame by this script. The logger checks Euler only on spheres. The "islands allowed"
    check is V - E + F = number of island loops.
  - 3D frames have contacts only, so no 3D Euler check is made.
- **Bubble toy (scripts/ism_toy.py), rung 5.** Clearly a toy.
  - Picture: the three-phase picture of McKee & Ostriker 1977.
  - Bubbles appear at random places and times. Radius grows as age^0.4 (Sedov-Taylor), stalls, then shrinks to 0 (cooling).
    Superbubbles: 20% of sites have 2.5 times the stall radius.
  - Densities: hot gas 0.01; a dense swept-up shell outside each bubble; a slowly changing lognormal background (sigma 0.5,
    correlation 6 px).
  - Cell rule: markers = connected regions with density below theta (0.05, varied to 0.2), smaller than amin pixels dropped (4,
    varied to 16); cells = watershed basins of log density from the markers. Cells are matched by mutual largest overlap with area
    lineage.
  - Settings: box 256^2, median stall radius 5 px, 8 sites per time unit, hot filling factor 0.29 to 0.33.
- **Census (scripts/ladder.py).** Logger at steps 1, 2 and 4 on the same frames. Vanished cells by side number, swaps per vanished and
  per new cell, and a negative control (one cell-changing event retyped as a swap must fail the balance).
- **Pilot (scripts/pilot.sh).** 11 runs in parallel on the compute machine, under the plan ism-ladder-pilot.

## Literature (free sources; 15 Nov 2026)
Marks: FT = full text read, AB = abstract only, 2nd = known from other papers' citations, memory = recalled, not verified.

- **Key question:** has anyone treated ISM bubbles, or foams with continuous births, as a tiling over time and counted swaps, mergers
  and births? None found. The closest:
  - Watkins et al. 2023: a single epoch. Nested bubbles (31%) are read as merging or triggering.
  - Chen et al. 2026 and Angress et al. 2026: bubble segmentation and lifetimes in simulations; no event counts in the abstracts.
  - THESAN 2024: merger trees of ionised bubbles in the reionization era. Intergalactic, not ISM.
- **Prior work (scutoids in foam):** A. Mughal, S. J. Cox, D. Weaire, S. R. Burke and S. Hutzler, "Demonstration and
  interpretation of 'scutoid' cells formed in a quasi-2D soap froth", Philos. Mag. Lett. 98 (2018) 358-364,
  doi:10.1080/09500839.2018.1552806, arXiv:1809.08421 [FT; author list checked against the arXiv copy: Aberystwyth and Trinity
  College Dublin]. DICTO pointed to it. A single layer of soap bubbles between two concentric cylinders (curved, not parallel,
  bounding surfaces) forms scutoids. A T1 swap happens on the inner surface and not on the outer one, so the swap is seen through
  the depth of one layer of cells. This is the tissue picture of this stream (a swap in time read as a scutoid in a stack). Surface
  Evolver simulation (144 cells; the T1 is triggered by hand) and a first experiment (inner cylinder 21 mm, outer 39 mm, bubbles
  about 8 mm). They describe single configurations only. They count no T1s and give no rates, and there is no coarsening in time.
- **Rung 1:**
  - Rutenberg & McCurdy 2006, PRE 73, 011403, arXiv cond-mat/0502287 [FT]. T1/T2 = 0.53 ± 0.05 macroscopic. Vanishing cells
    9 / 84 / 7 % with 3 / 4 / 5 sides. mu2 = 1.24.
  - Herdtle & Aref 1992, J. Fluid Mech. 241, 233 [2nd via Rutenberg & McCurdy]: T1/T2 = 3/2 including side-shedding.
  - Glazier, Gross & Stavans 1987, PRA 36, 306 [AB/2nd]: experiment, side distribution, von Neumann check; T2 events of 4- and
    5-sided cells seen.
  - Stavans & Glazier 1989, PRL 62, 1318; Glazier & Stavans 1989, PRA 40, 7398; Stavans 1993, Rep. Prog. Phys. 56, 733; Glazier &
    Weaire 1992, J. Phys. Cond. Matt. 4, 1867 [2nd].
  - von Neumann 1952; Weaire & Kermode 1983; Weaire & Rivier 1984; Anderson, Srolovitz, Grest & Sahni 1984; Glazier, Anderson &
    Grest 1990 [memory].
  - Levitan & Domany 1995, arXiv cond-mat/9505073 [AB]; Tam, Rutenberg et al. 1999, cond-mat/9906217 [AB].
  - No open data found.
- **Rung 2:**
  - Roth, Jones & Durian 2013, PRE 87, 042304, arXiv 1207.0146 [AB]: scaling-state statistics independent of liquid fraction;
    coarsening up to 4 times slower.
  - Schimming & Durian 2017, arXiv 1706.01392 [AB].
  - Dennin 2004, PRE 70, 041406, arXiv cond-mat/0405489 [AB]: T1s in sheared bubble rafts.
  - Tewari et al. 1999 [AB]: bubble model under shear.
  - Bragg & Nye 1947 [memory].
  - No coarsening T1/T2 count found for wet 2D foam.
- **Rung 3:**
  - Lambert et al. 2007, PRL 99, 058304, arXiv cond-mat/0702685 [AB]: ESRF tomography, 7000 bubbles, growth law G_f ~ f - f0;
    Lambert et al. 2010, PRL 104, 248304 [2nd]. No public tomography data found.
  - Roth, Chen & Durian 2013, arXiv 1306.2939 [FT]: surface bubble creation at an "insignificant rate".
  - Thomas et al. 2015, arXiv 1502.03366 [AB]: 3D cellular Potts wet foam.
  - Mason, Lazar, MacPherson & Srolovitz 2015, PRE 92, 063308 [AB]: steady grain-growth structure.
  - MacPherson & Srolovitz 2007, Nature 446, 1053; Glazier 1993, PRL 70, 2170; Weaire & Phelan 1994; Monnereau & Vignes-Adler 1998
    [memory].
  - A Soft Matter 2024 paper on T1/T2 in 3D coarsening (d4sm00555d) was blocked (403).
  - No 3D T1-per-T2 number found.
- **Rung 4:**
  - Kroo, Bull & Prakash 2022, arXiv 2204.00937 [AB]: one bubble cyclically inflated in a 2D foam; T1s near the source.
  - No event census found for nucleation-fed foams.
- **Rung 5:**
  - Watkins et al. 2023, ApJL 944, L24 [AB]: 1694 bubbles in NGC 628.
  - Barnes et al. 2023, ApJL 944, L22 [AB].
  - Bagetakos et al. 2011, AJ 141, 23 [AB]: THINGS HI holes, open table VizieR J/AJ/141/23. LITTLE THINGS holes: VizieR J/AJ/160/66.
  - Makarenko et al. 2018, arXiv 1804.04688 [AB], and 2017, arXiv 1708.04558 [AB]: static topology (Betti numbers) of HI and MHD
    turbulence; no events.
  - Kim, Ostriker & Raileanu 2017, arXiv 1610.03092 [part FT]: one superbubble per run.
  - Breitschwerdt & de Avillez, astro-ph/0402446 [AB]: Local Bubble and Loop I merging.
  - Chen et al. 2026, arXiv 2603.27741 [AB]; Angress et al. 2026, arXiv 2605.08534 [AB]; THESAN 2024, arXiv 2411.08943 [AB].
  - Icke 1988, Voronoi foams [2nd].
  - McKee & Ostriker 1977, ApJ 218, 148; Cox & Smith 1974; Heiles 1979, 1984; Ehlerová & Palouš 2005, 2013; Zucker et al. 2022
    (Nature); Watson et al. 2023 (PHANGS-JWST); Anderson et al. 2014 (WISE HII regions); Simpson et al. 2012 and Jayasinghe et al.
    2019 (Milky Way Project); Walch et al. 2015, Girichidis et al. 2016 (SILCC); Kim & Ostriker 2017 (TIGRESS) [memory, cited for
    context only].
- **Simulation data:**
  - TIGRESS: public release of R8 only, at 2 pc, via Globus (Princeton DataSpace, DOI 10.34770/ackh-7y71). Selected snapshots about
    10 Myr apart; every 1 Myr on request (princetonuniversity.github.io/astro-tigress/intro.html, fetched). No sizes are stated.
    Our estimate: about 5 GB per MHD snapshot, from a 1 kpc box at 2 pc (box size from memory). So 50 snapshots at 1 Myr would fit
    the 50 GB limit.
  - FIRE-2: Wetzel et al. 2023, arXiv 2202.06969 [AB]; at most 39 snapshots per run.
  - SILCC: no release found.
- **Sources checked:**
  - Searches: Rutenberg McCurdy T1 T2; TIGRESS public data release; superbubble merging tessellation; Makarenko persistent homology;
    Herdtle Aref; Roth Jones Durian 2013; Lambert 2007 tomography; FIRE-2 release size; SILCC public data; Watkins/Watson PHANGS
    bubbles; Lazar/Mason 3D grain growth topological; 2D foam continuous injection; HI holes Voronoi/foam porosity; superbubble
    tracking merger tree; Bagetakos THINGS holes; ISM bubbles network topology; 3D foam T1 count Potts/Surface Evolver; Glazier Gross
    Stavans 1987; Kim Ostriker Raileanu 2017; bubble raft T1 count.
  - Pages fetched: arxiv.org/pdf/cond-mat/0502287; arxiv.org/abs/2605.08534, 2603.27741, 2202.06969; ar5iv 1306.2939, 1610.03092;
    princetonuniversity.github.io/astro-tigress/intro.html; wetzel.ucdavis.edu/fire-data-release-1/.
  - Blocked: the Princeton DataSpace record (bot check); pubs.rsc.org d4sm00555d (403).

## Fit in the comparison table
| system | cells | dimension | time span | status |
|---|---|---|---|---|
| foam ladder rungs 1-4 (simulated) | 10^1 to 10^3 per run, more on demand | 2 and 3 | as long as wanted (MCS) | feasible; pairing rule needed first |
| interstellar bubbles | about 10^2 bubbles per kpc^2 slice (toy) | 3 (2D slice in the toy) | tens of Myr in simulations | toy rule fails as a tiling; real time series only on request (TIGRESS 1 Myr) |

## NEXT (decided)
1. Pairing rule for split swaps: a loss and a gain among the same four cells within k frames make one swap. Fix k and the tolerance
   before counting; validate on the moving-Voronoi null model of the tissue-null-models stream (exact T1 rate known). Share the rule
   with the Earth stream.
   DONE 15 Nov 2026 in studies/2026-11-15-event-logger (pairing section): the shared rule (W = P = 8 MCS) pairs split swaps and removes
   flicker. Rung 1 swaps per vanished cell are still step-dependent (0.76 / 0.62 / 0.49 / 0.36 at steps 1 / 2 / 4 / 8). About two
   thirds of the swaps lost at step 4 are side-shedding by a cell that vanishes in the same interval.
2. Rung 1 at 1024^2 with two seeds, the side number taken at a fixed small area. Compare with Rutenberg & McCurdy and the null-model
   table. Rung 3 at 96^3 or more.
3. Rung 5: replace the watershed-threshold rule by hot regions plus a distance share of the dense gas (so cells stay discs), or go to
   3D. Pilot again before any count. Ask the TIGRESS team for R8 at 1 Myr only once the toy rule is settled.
