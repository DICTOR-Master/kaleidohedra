# Atmosphere and sea ice: cloud cells, floes and polygon ground as changing tilings (One tissue, many scales; 15 Nov 2026)

DICTO, 15 Nov 2026: "atmospheric convection and clouds, ice sheets and sea ice". This study adds two systems to the plan "One tissue,
three scales" (14 Nov 2026): the cells of shallow convection seen from a weather satellite, and the floes of sea ice (with a look at
ice-sheet and permafrost surface patterns). Each system makes its tiling for its own physical reasons; nothing here assumes or tests
any influence of one on another. The cloud field has the combinatorics of a simple tiling; its history is a scutoid tissue.

## VERDICT (15 Nov 2026)
- **Atmospheric convection: FEASIBLE; rates NOT yet stable.** Free geostationary images (Himawari-9, Japan area, 2.5-minute frames,
  0.5 km) of a winter cold-air outbreak south of Japan (5 Feb 2025) give cell tilings that pass Euler in every frame at the smoother
  setting (0-3 of 145 frames fail; a third fail at the finer setting). Over 6 hours, 30 to 320 interior cells per frame, thousands of
  logged events. Swaps (neighbour exchanges) are present. With a two-sided persistence rule (old contact held 10 minutes before, new
  contact held 10 minutes after), swaps per cell-hour are step-independent within about 30% from 2.5 to 10-minute steps (smoother
  setting: 0.085 / 0.078 / 0.106 at marker depth 0.05), but they vary about threefold with smoothing and marker depth (0.03 to 0.15),
  and splits and merges are still dominated by flicker (their rate falls tenfold from 2.5 to 20-minute steps). So no rate goes into the
  comparison table yet. The test box mixes open cells with cloud streets (rolls), which are not cells; the next scene must be pure
  open or closed cells.
- **Sea ice: NOT feasible from the geostationary images; feasible in principle with finer images or a floe model.** Floes do not
  tile (open water between), so the cell rule is each floe's zone of influence (the Voronoi diagram of the floes as sets). In the
  Okhotsk Sea pilot (27 Feb 2025) the floes are 4-10 pixels across, confused with cloud streets in one visible band, and the
  brightness threshold drifts with the sun: 0 to 33 usable cells, events mostly clumps. The public floe library of the Ice Floe Tracker
  (Zenodo 4796845) holds only tracked floes (centroids, sizes, daily), not a full mosaic. A full mosaic with time exists in the
  open-source floe model SubZero (polygonal floes that fracture and weld).
- **Ice sheets and frozen ground: no usable time series.** Ice-wedge polygon networks are true tilings (cells meeting three at a
  point), but their topology changes over centuries; repeat imagery shows trough degradation, not new junctions. Supraglacial lake
  basins and crevasse fields do not tile. Ice grains belong to the grains stream. Only a network model (Plug & Werner 2002) would
  give events.
- **Prior art: nobody found counting swaps (neighbour exchanges) in cloud cells or sea ice.** Closest: Glassmeier & Feingold (2017)
  treat stratocumulus cells as a planar network (Lewis and Aboav-Weaire laws, cell division and merging, from simulations, no swap
  count); Haerter & Monroy (EGU 2025, 2026 abstracts) segment and track open cells in satellite images and report "rearrangement",
  no counts published in what we found. For hexagonal Bénard-Marangoni convection in the laboratory, neighbour switching is
  described among the elementary topological changes (see sources; full text not read).

## Comparison-table place
| system | cells per frame | dimension | time span | status |
|---|---|---|---|---|
| open-cell convection (Himawari-9, 1 km, 2.5 min) | 30-320 interior cells in a 400 x 400 km box | 2 (patch) | hours (6 h, daylight) | tilings pass Euler; swaps P10 0.03-0.15 per cell-hour, step-stable, threshold-dependent; splits/merges unstable |
| sea-ice floes (Himawari-9, 0.5 km) | 0-33 | 2 (patch) | hours | not feasible at this resolution (cloud, sun angle, floe size) |
| ice-wedge polygons | 10^2-10^4 per site | 2 | centuries | tiling exists, no event time series |

Mean neighbours of interior cells 5.5-5.8 (distinct neighbours; interior cells are biased small), variance mu2 3.1-3.5 (smoother
setting) or 5.7-6.4 (finer): wider than the planar Poisson-Voronoi value 1.78 and than mu2 about 2 of Glassmeier & Feingold's
simulated stratocumulus networks (their network is the Voronoi diagram of cell centres, which narrows mu2). Reference values:
studies/2026-11-15-tissue-null-models (swaps per birth 24pi^2/35 - 2 = 4.77 for sections of Poisson-Voronoi; mean sides exactly 6 in
the plane).

## Data (free, no login)
- Himawari-9 Advanced Himawari Imager, Japan-area Level 1b files (Himawari Standard Data), observed by JMA, mirrored by NOAA on AWS
  open data (bucket noaa-himawari9, prefix AHI-L1b-Japan). The Japan area is scanned four times every 10 minutes (files JP01-JP04),
  band 3 (0.64 um) at 0.5 km. One frame is a 17 MB compressed file. Read with our own minimal reader (scripts/hsd.py), written from
  JMA's "Himawari Standard Data User's Guide" v1.3; navigation by the standard geostationary projection formulae; checked against
  the coastline of Korea and Hokkaido in quicklooks.
- Atmosphere scene: 5 Feb 2025, 00:00-06:00 UTC (09-15 JST), a strong winter monsoon outbreak (heavy snow on the Sea of Japan coast
  that week); open cells cover the sea south of Japan. Region 33.6 N 128.8 E to 22.3 N 140.3 E, averaged to 1 km; 145 frames,
  1.1 GB as float32 (kept on the compute machine, not in git).
- Sea-ice scene: 27 Feb 2025, 00:00-03:00 UTC, 10-minute frames, Okhotsk Sea north of Shiretoko (about 47.9 N 141.4 E to 44.5 N
  146.4 E), 0.5 km; 19 frames.
- Downloads in all: about 3.2 GB, deleted after cropping.

## Cell rules (fixed before counting; scripts/cellcensus.py)
- **Open cells:** cloud-free centres with their share of the cloud walls. Basins of a marker watershed on the smoothed brightness
  (albedo); markers are the regional minima of depth at least h (h-minima). Every pixel belongs to a cell; boundaries run along the
  bright walls. Varied: smoothing sigma 1.5 and 3 km; h = 0.03, 0.05, 0.08 albedo.
- **Floes:** connected regions brighter than h (at least 6 pixels); each floe's cell is its zone of influence (watershed of the
  distance to the nearest floe, seeded by the floes): leads and open water are cut along the median lines between floes. Varied:
  h = 0.35, 0.5.
- **Patch:** the box is ringed by one outside cell, so box + outside = a sphere and Euler V - E + F = 2 is checked in every frame.
  Events count only when no cell of the event is the outside cell or touches it before or after (cells wholly inside the box).
- **Moving box:** the box follows the mean drift of the pattern, measured frame to frame by phase correlation (scikit-image). The
  cloud field drifts 1 and 2 pixels per 2.5 minutes (south and east), about 15 m/s; over 6 hours the box moved 144 x 289 km.
- **Neighbour graph and matching:** the Sun stream's tiles.py (graph from 2 x 2 pixel junction blocks; mutual best overlap matching,
  with area shares as lineage), imported unchanged; the shared event logger (eventlog.py), imported unchanged.
- **Swaps:** elementary swaps inside every logged event (a lost contact and a gained contact among the same four cells, the 2-2
  move), and two-step swaps through a four-fold meeting, as in the Sun stream's census.
- **Persistence:** (1) flicker: a swap undone by the reverse swap within W minutes is removed with its reverse; a piece split off and
  merged back within W is removed. (2) two-sided (as in the Earth stream): a swap counts when its old contact held in every frame of
  the previous P minutes and its new contact in every frame of the next P minutes; swaps within P of either end are not judged.
  W, P = 10, 20, 40 minutes (5, 10, 20 in the pilot).

## Predictions (written before the first census)
- Euler holds in most frames; failures come from pixel-scale artefacts (cells enclosed in cells, four cells in a 2 x 2 block).
- Rigid drift of one frame (nothing changes) gives no interior event; added pixel noise gives splits and merges that flicker.
- Raw counts depend strongly on the time step; a persistence rule makes the swap rate step-independent.
- Sea ice at 0.5 km: few floes, cloud confusion; likely not feasible.

## Results
Pilot (job atmice-pilot, FINAL ok): 1 h of cloud frames, 3 h of ice frames, two thresholds each, steps 1/2/4 frames. Run 2 (job
atmice-run2, FINAL ok): 6 h of cloud frames, 6 settings x 4 steps (2.5, 5, 10, 20 min). Full table: results/run2/table.md.

Controls:
- Rigid drift (one frame cut at an origin moving 1 and 2 pixels per frame, 24 frames): 0 interior events in pilot and run 2
  (as predicted). Box tracking found the drift exactly.
- Noise (same, plus Gaussian noise 0.02 albedo each frame): 10 splits, 12 merges, 2 clumps, 0 swaps; the flicker rule removed 5 of the
  10 splits at W = 20 min. So segmentation noise makes split/merge flicker, not swaps.
- Logger negative control (one event retyped): caught at every step of every run; the balance (births + splits - deaths - merges +
  clump net = change in cells) held at every step.

Run 2, swaps per cell-hour under the two-sided rule with P = 10 min (persistent / judged):

| setting | 2.5 min | 5 min | 10 min | 20 min* | splits + births per cell-hour (2.5 / 20 min) | Euler-bad frames (2.5 min) |
|---|---|---|---|---|---|---|
| sigma 3, h 0.03 (78 cells) | 0.088 (39/346) | 0.083 | 0.145 | 0.115 | 0.68 / 0.06 | 3 / 145 |
| sigma 3, h 0.05 (52 cells) | 0.085 (25/206) | 0.078 | 0.106 | 0.090 | 0.59 / 0.04 | 0 / 145 |
| sigma 3, h 0.08 (30 cells) | 0.077 (13/59) | 0.053 | 0.059 | 0.054 | 0.54 / 0.06 | 0 / 145 |
| sigma 1.5, h 0.03 (322 cells) | 0.030 (55/1592) | 0.040 | 0.055 | 0.038 | 0.82 / 0.05 | 47 / 145 |
| sigma 1.5, h 0.05 (180 cells) | 0.027 (27/739) | 0.038 | 0.043 | 0.043 | 1.01 / 0.06 | 48 / 145 |
| sigma 1.5, h 0.08 (86 cells) | 0.025 (12/298) | 0.045 | 0.045 | 0.028 | 1.08 / 0.08 | 49 / 145 |

*At the 20-minute step the 10-minute window holds no frame besides the event's own, so every swap passes; that column is not an
independent check.
- How the findings compare with the predictions: Euler held as predicted at the smoother setting; at sigma 1.5 a third of the frames
  fail (pixel artefacts: cells with one or two neighbours, tens of four-fold 2 x 2 blocks per run). Raw counts are strongly
  step-dependent (as predicted): elementary swaps 1640 / 726 / 238 / 69 at 2.5 / 5 / 10 / 20 min (sigma 1.5, h 0.03). The flicker rule
  alone (W) does not fix this; the two-sided rule does for swaps at P = 10 min (within about 30%), but at P = 20 and 40 min almost
  every swap at the fine step fails (contacts flicker more often than every 20 minutes), so the rate depends on P: 0.085 / 0.029 /
  0.008 per cell-hour at P = 10 / 20 / 40 (sigma 3, h 0.05, 2.5 min). This P-dependence is a finding about how long cloud contacts last,
  not yet a rate.
- Splits and merges do not settle: 0.5-1.1 per cell-hour at 2.5 min, 0.04-0.08 at 20 min. Deaths are 0 in every run: a vanishing
  cell always leaves most of its area to one neighbour, so with lineage it reads as a merge; births (a new three-sided cell with no
  dominant parent) are logged. So births/deaths and splits/merges are not separable at this resolution and are pooled.
- Clumps are many (4202 at the finest setting and step); the commonest are one contact lost or gained alone, and two lost with two
  gained: contact flicker of the same kind the Earth stream met.
- Sea ice (pilot): at h 0.35, 33 interior cells on average, 4 swaps, 5 births, 7 splits, 11 merges, 25 clumps at 10 min; at 20 and 30
  min almost no events; at h 0.5 no floe at all. The brightest 1% of the box rises from 0.29 to 0.44 albedo between 00 and 03 UTC
  (sun angle, no correction applied), and the box is mostly cloud streets (figure results/pilot/ice_frame0_h025.png).

Figures: results/run2/atm_s3_frame0.png (frame 1 with the cells, sigma 3, h 0.05: open cells top right, cloud streets lower left),
results/pilot/atm_frame0.png (sigma 1.5), results/pilot/ice_frame0_h025.png.

## NEXT (decided)
1. Pure cellular scenes: choose boxes wholly in open cells (top-right part of this scene; and a second outbreak day), and a closed-cell
   stratocumulus scene (Himawari full disk sees the Sc decks west of Australia; GOES-18 over California and GOES-16/19 off Peru are on
   AWS open data in netCDF). Same rules.
2. Count splits and merges with the two-sided rule too (the new cell, or the joined cell, must last P minutes), then swaps per new
   cell for the comparison with 4.77.
3. A control of known answer: a moving Voronoi tiling drawn as bright walls on a dark field, at the cell size and noise of the clouds,
   to measure how many true swaps the image pipeline recovers at each P (the Sun stream's control, made non-periodic).
4. Sea ice: the SubZero floe model as the toy (full polygon mosaic, fracture and welding); for real floes, 250 m MODIS daily images
   with the Ice Floe Tracker's cloud filtering, or Sentinel-2 where revisits allow. Ice-wedge polygons: none unless a network model is
   wanted.

## Files
scripts/hsd.py (HSD reader), fetch.py (download, crop, average, delete raw), quicklook.py and crop_ql.py (scene choice), cellcensus.py
(cell rules, moving box, logger, swaps, persistence), control.py (rigid and noise controls), render.py (figures), summarize.py (table),
pilot.sh, run2.sh. results/pilot, results/run2 (JSON per setting, logs, table.md, figures). Jobs atmice-pilot and atmice-run2 ran on
the compute machine through the job guard with plan files; nothing is left running. Downloaded data stay on the compute machine.

## Sources checked (15 Nov 2026; free sources only; "abstract" = only the abstract or a summary was read)
Searches (web): "Glassmeier Feingold network approach patterns stratocumulus clouds Voronoi Aboav Lewis"; "open cellular convection
cell tracking neighbour exchange T1 topological cloud cells satellite"; "Ice Floe Tracker Lopez-Acosta 2019 MODIS floe trajectories
dataset"; "sea ice floes Voronoi tessellation floe size distribution model fracture welding SubZero"; "ice-wedge polygon network
evolution Plug Werner; sorted patterned ground Kessler Werner"; "Hopkins Thorndike floe formation; Herman floe size; Rayleigh-Benard
hexagon defects"; "Rayleigh-Benard hexagonal convection topological changes T1 neighbor switching penta-hepta"; "Kessler Werner 2003
sorted patterned ground; ice-wedge polygon repeat imagery".
- T. Glassmeier and G. Feingold, Network approach to patterns in stratocumulus clouds, PNAS 114 (2017) 10578-10583,
  doi:10.1073/pnas.1706495114 (abstract and press summaries; EGU2017-1555 abstract): Voronoi network of cell centres from large-eddy
  simulations; mean 6, variance about 2, Aboav-Weaire 0.9, Lewis 0.16; open and closed networks almost the same; division and
  merging rules; no swap count.
- J. Haerter and D. Monroy (Merida), Morphological cellular analysis of pockets of open cells on marine stratocumulus, EGU25-20182
  and EGU26-14944 (abstracts): segmentation and tracking of open cells in satellite images; "continuous rearrangement"; no counts
  stated.
- G. Feingold, I. Koren, H. Wang, H. Xue and W. A. Brewer, Precipitation-generated oscillations in open cellular cloud fields,
  Nature 466 (2010) 849-852, doi:10.1038/nature09314 (abstract).
- Lang et al., open and closed mesoscale cellular convection from three years of Himawari-8 with a neural network, Atmos. Chem.
  Phys. 22 (2022) 2135 (search summary only; authors beyond the first to check).
- EUMETSAT training manual, "Open and closed cells" (eumetrain.org satmanu): cell depth 1-2 km, honeycomb description.
- From memory, to check: E. M. Agee, T. S. Chen and K. E. Dowell, A review of mesoscale cellular convection, Bull. Amer. Meteor. Soc.
  54 (1973) 1004; R. Wood and D. L. Hartmann, Spatial variability of liquid water path in marine low cloud: the importance of
  mesoscale cellular convection, J. Climate 19 (2006) 1748; I. Koren and G. Feingold, Aerosol-cloud-precipitation system as a
  predator-prey problem, PNAS 108 (2011) 12227; P. Cerisier, S. Rahal and N. Rivier, topological correlations in Bénard-Marangoni
  convection, Phys. Rev. E 54 (1996) 5086 (the hexagon-convection paper with neighbour switching found in the search is probably
  from this group; not opened).
- Rayleigh-Bénard hexagons (search summaries): penta-hepta defects and dislocations in non-Boussinesq convection (arXiv
  patt-sol/9305001, nlin/0207056, nlin/0307048); "Defect dynamics in hexachaos" (APS DFD 2005 abstract). Defect dynamics, not swap
  counts.
- J. Lopez-Acosta, M. Schodlok and M. M. Wilhelmus, Ice Floe Tracker, Remote Sens. Environ. 234 (2019) 111406 (abstract): MODIS
  floe tracking, East Greenland, 1061 trajectories. Floe library, Zenodo 10.5281/zenodo.4796845 (record and variable list read:
  floe sizes, centroids, daily velocities, rotation, ellipticity; masks; tracked floes only).
- G. E. Manucharyan and B. P. Montemuro, SubZero, J. Adv. Model. Earth Syst. (2022); B. P. Montemuro and G. E. Manucharyan, JOSS 8
  (2023) 5039 (software paper; Voronoi initial floes, fracture and welding); arXiv:2604.10292 (2026, power laws in the floe size
  distribution from fracture and welding rates; abstract).
- M. Gherardi and M. Cosentino Lagomarsino, Characterizing the size and shape of sea ice floes, Sci. Rep. 5 (2015) 10226 (search
  summary: floe shapes matched by a Voronoi coalescence model).
- M. A. Hopkins and A. S. Thorndike, Floe formation in Arctic sea ice, J. Geophys. Res. 111 (2006) C11S23 (abstract); D. A. Rothrock
  and A. S. Thorndike, Measuring the sea ice floe size distribution, J. Geophys. Res. 89 (1984) (abstract); H. L. Stern et al., On
  reconciling disparate studies of the sea-ice floe size distribution, Elementa 6 (2018) 49 (abstract).
- L. J. Plug and B. T. Werner, Nonlinear dynamics of ice-wedge networks and resulting sensitivity to severe cooling events, Nature 417
  (2002) 929-933 (abstract); Burn (2004) comment and Plug & Werner (2008) reply, Permafrost Periglac. Process. (abstracts); ice-wedge
  degradation from repeat imagery (Environ. Res. Lett. 2013; EGUsphere-2026-5192; abstracts). From memory, to check: M. A. Kessler
  and B. T. Werner, Self-organization of sorted patterned ground, Science 299 (2003) 380.
- Software credited where used: scikit-image (van der Walt et al. 2014, PeerJ 2:e453; BSD) for watershed, h-minima and phase
  correlation; SciPy (BSD); NumPy; Pillow. Data: JMA Himawari-9 via NOAA Open Data Dissemination on AWS.
