# Scutoids in compound eyes: a testable prediction (scope study)

DICTO, 16 Nov 2026 (continues next step 2 of studies/2026-11-15-scutoid-lenses, and #104 Scutoid Tissues). His proposal: scutoids
should appear in unevenly curved compound eyes. Ommatidia run as columns from the cornea (outer surface) to the basement membrane
(inner, smaller surface). If the two surfaces shrink evenly in every direction, the columns are plain frusta and keep their
neighbours. If they shrink unevenly, the columns may have to change neighbours on the way down: scutoids (Gómez-Gálvez et al.
2018; Mughal, Cox, Weaire, Burke, Hutzler 2018 for foams between concentric cylinders).

Every source checked is listed in [PRIOR_ART.md](PRIOR_ART.md). Numbers come from data/eyeswap-pilot.json (script
scripts/eyeswap.py, run on the compute machine in 40 s, FINAL ok, all 5 checks passed; log data/eyeswap-pilot.log).

## VERDICT (16 Nov 2026)

1. **Not reported before, as far as we could find.** No paper describes scutoids, or neighbour changes between the facet layer
   and the retina, in any compound eye. Facet-mosaic defects (5-7 pairs, size disorder) are measured at the surface only (Kim et
   al. 2016; butterfly corneal nipple arrays). The micro-CT and synchrotron analyses (ODA-3D, butterfly eyes) reduce each
   ommatidium to one point or one cone. The whole-eye electron-microscope reconstruction of a 29-ommatidium wasp segments every
   cell but does not discuss neighbours at different depths.
2. **Law, exact for a perfect hexagonal mosaic.** Columns that converge unevenly change neighbours when the outer-to-inner
   anisotropy A = (1 − dΔφ_min/D)/(1 − dΔφ_max/D) reaches √3, if the strong convergence runs across the facet rows. Then
   exactly one family of edges flips (control: 1024 of 3039 edges at A = 1.74, none at 1.72). If it runs along the rows, no flip
   happens at any A (control: none up to A = 10). Even convergence (A = 1) never swaps (control: 0 swaps in all four eyes at every depth).
3. **On real facet mosaics the threshold is soft.** Columns run along the smoothed cone axes of four open micro-CT eyes. Swaps begin
   well below √3 at near-tied edges. Pooled over the bee, fly and D. elpenor eyes (depths 10-200 µm), the share of swapped edges is
   0.2% for A < 1.2, 2.7% at 1.2-1.4, 5.7% at 1.4-1.6, 9-13% around √3, 23% at 2-2.5 and 33% at 2.5-3 (table B).
   So the "one third" of the perfect mosaic is reached only near A ≈ 2.5-3, and a scattering of swaps comes first.
4. **Prediction, model run on the real mosaics** (columns straight along smoothed axes; the depth of the basement membrane is not in the data):
   - **Honeybee (oval eye): swaps occur and are patchy.** 2.1% of interior edges at 100 µm, 4.7% at 150, 8.9% at 200, 21% at
     300 µm (predicted 5-20% at basement-membrane depth). The axes converge unevenly: median Δφ 2.0° in one direction, 0.6° in the other.
     The first swap depth d* has median 316 µm, and 165 µm in the most anisotropic tenth of the eye. At 150 µm the swaps gather
     in two of nine regions of the scan's (inclination, azimuth) frame (8.5-8.8% of their edges), and one region has 0 of 1671
     (table C). Naming those regions anatomically needs the scan's orientation.
   - **Fruit fly (D. mauritiana): fewer than predicted only at shallow depth.** 0.1% at 50 µm and 1.3% at 100 µm, but 10% at
     150 µm. Its eye is more anisotropic than assumed (median Δφ 4.1° against 3.0°, not equal). So under 2% holds only if the
     retina is no deeper than about 100-110 µm.
   - **Hawkmoths: about none, as predicted.** D. elpenor 0.1% at 100-200 µm and 0.4% at 300 µm. M. sexta 0.0% to 400 µm (but
     its table has only pre-smoothed axes).
5. **The open cone-axis data cannot test the prediction.** The raw cone axes scatter by 7-16° (rms) about their smoothed values.
   Extended 100 µm, that scatter alone swaps 27-76% of edges in the noise control, and the raw axes give 5-52%. The swaps in those
   rows are noise, not scutoids. A real test needs ommatidia traced through the depth in a volume where the retina is resolved.
6. **The data to do it are open.** First choice: the butterfly synchrotron volumes on BossDB (Paukner et al. 2024; 7 eyes,
   0.6 µm voxels, uint8, 3.8-19 G voxels in the four eyes checked; public; no licence stated, so ask before any public reuse of images). Second: the
   whole wasp eye in volume EM (Makarova et al. 2025; 29 ommatidia, oval eye; on a Flatiron Institute viewer; no licence stated).
   It is tiny, but every cell is segmented. The moth micro-CT stacks in the ODA zip (CC BY 4.0, 0.8 and 2.2 GB) make a negative
   control: they predict about 0 swaps. The bee stack (5 µm voxels, 22 µm facets) is too coarse to trace a retina.

**Status: prediction stated and timestamped (commit 2bf1098a) before the data. The geometric law is proved for the perfect
mosaic and calibrated on four real mosaics. No scutoid has been observed yet: the open data hold no depth traces.** The
prediction to test: in an oval eye, swaps appear in the lower half of the ommatidia, where the one-sided convergence of the axes
is strongest. In a near-spherical eye they are about absent.

## Next steps (in order)
1. Butterfly volume (BossDB paukner2024, one eye at hierarchy level 1, a few GB on the compute machine). Segment the crystalline
   cones (bright) and follow each ommatidium down to the rhabdom layer (the method of the ODA cone clustering, applied slice by
   slice). Compare Delaunay neighbour sets at the cone tips and at the rhabdom layer with this counter. Run first on a 1 mm³
   corner (pilot ≤ 5 min).
2. Negative control on the D. elpenor stack (ODA zip, CC BY 4.0): trace the cones and the deep layer. Prediction: about 0 swaps.
3. Wasp eye (29 ommatidia): read the neighbour sets of cone cells and of rhabdomeres from the published segmentation, if the
   viewer exports meshes. Prediction for an oval eye of 29: at most a few swaps, if any (too few cells for statistics).
4. Bee: orient the scan (frontal, dorsal) from the Taylor et al. head volume to name the swap regions anatomically.

## PREDICTION (stated 16 Nov 2026, before any neighbour graph of real eye data was computed)

Only the column headers of the four ODA-3D tables and their first three rows had been seen when this was written.

**Model.** Each ommatidium is a straight column along its own optical axis. Neighbouring axes differ in angle by the
interommatidial angle Δφ, and neighbouring facets are D apart. At depth d below the cornea the column spacing in a direction is
D − dΔφ in that direction, so the outer-to-inner map shrinks lengths by 1 − dΔφ/D, a different factor along the two principal
directions (largest and smallest Δφ). Its anisotropy is

  A(d) = (1 − d·Δφ_min/D) / (1 − d·Δφ_max/D).

Isotropic convergence (A = 1, a similarity) can never change a neighbour set, however disordered the facet mosaic (control C1
below). The neighbour graph is taken as the Delaunay graph of the column centres at each depth (the Voronoi model that
Gómez-Gálvez et al. used for epithelia).

**Threshold (exact for a perfect hexagonal mosaic).** The pair of triangles on an edge flips when their rhombus becomes a
rectangle, i.e. when a 60° lattice angle is opened to 90°. Compressing perpendicular to a row of facets does this at A = √3
(the √3 found in the lens study). Compressing along a row never does it (the angles tend to 90° only as A → ∞). So the threshold
T(ψ) depends on the angle ψ between the lattice rows and the principal directions, with T ≥ √3. When it is passed, one whole
family of edges flips: about one third of the local edges. In a real, slightly disordered mosaic (Kim et al. 2016 measure the
disorder) near-tied edges flip earlier, so swaps begin sparsely below the threshold.

**First swap depth** for a favourable orientation: d* = D(√3 − 1) / (√3·Δφ_max − Δφ_min).

**Predictions, from literature values only:**

1. **Honeybee worker (Apis mellifera), oval eye.** Frontal acute zone (Δφ about 0.9° vertical, 1.6° horizontal; D about 20-25 µm):
   d* ≈ 450 µm or more, beyond the retina (ommatidium length about 300-400 µm, from memory, to be checked): **no swaps frontally.**
   Lateral and posterior eye, where horizontal Δφ is several degrees (about 3-5°, from memory) and vertical about 1-2°:
   d* ≈ 120-250 µm, inside the retina: **swaps expected there, in bands along the facet rows, at depths in the lower half of the
   ommatidium, reaching up to about a third of the edges where the rows lie favourably and few where they lie along the long
   direction.** Eye-wide, of the order of 5-20% of interior edges at basement-membrane depth.
2. **Fruit fly (Drosophila mauritiana), near-spherical eye** (Δφ about 4.5-5° in both directions, D about 16 µm, retina about
   100 µm, from memory): A stays below about 1.2: **close to no swaps away from the rim** (under 2% of interior edges, only at
   near-tied edges).
3. **Hawkmoths (Deilephila elpenor, Manduca sexta), large near-spherical superposition eyes:** A close to 1 through the cone
   layer: **close to no swaps** (under 2% of interior edges away from the rim).
4. **Where to look in general:** swaps follow the fastest one-sided convergence of axes (large Δφ_max/D), not the cornea's
   shape alone: band-shaped and oval eyes on the side where facets are small and Δφ large; the boundary between an acute zone and
   the rest of the eye, where Δφ changes fast in one direction; eye rims (excluded here, because the rim lattice is broken anyway).
5. **Rival outcome that would refute the Voronoi reading:** a traced retina in which columns keep all six neighbours and instead
   flatten into hexagons of aspect A (above √3) would mean the pigment-cell lattice pins the neighbour set, and the scutoid
   prediction fails for compound eyes even where the geometry asks for it.

## Pilot plan (before the run)

The open ODA-3D tables give, per ommatidium, the crystalline-cone centre and the cone's own axis (raw and smoothed over
neighbours). They do not trace ommatidia to the basement membrane. The pilot therefore extends each column along its axis to
depths 0-400 µm and compares the neighbour graph at the cone layer with that at depth. This tests the geometric premise (do real
eyes' axis fields and real facet mosaics give A ≥ √3 within plausible depths, and how often do edges flip) and measures P(swap | A)
on real, disordered mosaics. It is a model of the eye, not an observation of scutoids.
Controls: C1 similarity shrink (must give 0 swaps); C2 synthetic hexagonal mosaic, compressed across rows (first swap at √3) and
along rows (none); C3 axis noise: smoothed axes plus random tilts as large as the raw-minus-smoothed scatter.

## Tables (pilot, columns along smoothed cone axes unless named)

### A. Share of interior edges swapped (%) by depth
| eye | facets used | interior edges | 50 µm | 100 | 150 | 200 | 300 | 400 | median Δφ max / min | d* p10 / p50 µm |
|---|---|---|---|---|---|---|---|---|---|---|
| honeybee (Apis mellifera) | 5039 | 12701 | 0.8 | 2.1 | 4.7 | 8.9 | 21.0 | 30.3 | 2.03° / 0.62° | 165 / 316 |
| fruit fly (D. mauritiana) | 979 | 2163 | 0.1 | 1.3 | 10.4 | 30.3 | 78.8* | 47.8* | 4.14° / 3.02° | 122 / 176 |
| hawkmoth (D. elpenor) | 13689 | 38200 | 0.0 | 0.1 | 0.1 | 0.1 | 0.4 | 1.0 | 1.37° / 1.04° | 635 / 895 |
| hawkmoth (M. sexta)† | 26542 | 76091 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.98° / 0.75° | 1005 / 1425 |
| control: even shrink (all four) | | | 0 | 0 | 0 | 0 | 0 | 0 | | |
| bee, raw cone axes | | | 25.9 | 52.1 | 70.0 | 80.4 | 91.0 | 94.5 | | |
| bee, noise control | | | 43.1 | 74.5 | 87.7 | 93.6 | 97.0 | 98.2 | | |
| fly, raw cone axes | | | 3.8 | 22.0 | 46.9 | 69.7 | 94.7 | 79.9 | | |
| D. elpenor, raw cone axes | | | 0.9 | 5.1 | 19.2 | 36.0 | 57.5 | 71.5 | | |

\* Fly columns along smoothed axes meet at about 250 µm (spacing 17.9 µm ÷ 4.1°): 170 of 755 interior points are folded at 200 µm,
583 at 300 µm. Folded points are left out, so these rows are not comparable. The fly retina is far shallower.
† The M. sexta table holds only one axis per cone, already smooth (0.13° rms from its own neighbour average), so its raw and noise
rows say nothing.
Facet spacing (µm) equals the ODA lens diameter within 0.2-2.4% in all four eyes (bee 22.2, fly 17.9, D. elpenor 28.5, M. sexta
32.6), so the tables are in micrometres. Δφ is from the 10 µm convergence tensor of the smoothed axes. d* is the first-swap depth
for a favourable row orientation.

### B. Share of edges swapped by local anisotropy A (depths 10-200 µm pooled; edges / % swapped)
| A | 1-1.2 | 1.2-1.4 | 1.4-1.6 | 1.6-√3 | √3-2 | 2-2.5 | 2.5-3 | > 3 |
|---|---|---|---|---|---|---|---|---|
| bee | 62691 / 0.8 | 15609 / 3.2 | 5074 / 5.9 | 1583 / 9.0 | 1524 / 12.1 | 1227 / 20.5 | 468 / 28.8 | 653 / 45.9 |
| fly | 9058 / 0.1 | 2179 / 1.1 | 1017 / 5.5 | 423 / 10.6 | 507 / 16.0 | 491 / 30.1 | 254 / 39.8 | 563 / 46.7 |
| D. elpenor | 265337 / 0.1 | 1813 / 0.0 | 218 / 1.4 | 21 / 4.8 | 11 / 0.0 | | | |
| perfect hexagonal mosaic, across rows | 0 | 0 | 0 | 0 | 33.7 | 33.7 | 33.7 | 33.7 |
An edge's A is the larger of its two ends' A.

### C. Honeybee, swapped edges by region (terciles of ODA inclination θ and azimuth φ in the scan frame; edges, swapped)
| depth | θ low, φ low | θ low, φ mid | θ low, φ high | θ mid, φ low | θ mid, φ mid | θ mid, φ high | θ high, φ low | θ high, φ mid | θ high, φ high |
|---|---|---|---|---|---|---|---|---|---|
| 150 µm | 2148, 81 | 1757, 155 | 228, 21 | 1671, 0 | 1680, 22 | 1121, 18 | 313, 6 | 1217, 74 | 2566, 217 |
| 300 µm | 2092, 351 | 1445, 435 | 167, 62 | 1671, 77 | 1680, 130 | 1010, 289 | 311, 18 | 1217, 200 | 2015, 880 |

## Method (pilot)
Data: ODA-3D ommatidial tables (Currea et al. 2023, figshare 10.6084/m9.figshare.21521142, CC BY 4.0), four members of the 17.1 GB
benchmark zip fetched by HTTP range requests (scripts/fetch_oda.py; checksums in data/raw_sha256.txt; the CSVs are not kept in
git). Columns per the ODA code (MIT licence): cone centre x_, y_, z_; smoothed axis dx_, dy_, dz_; raw cone axis dx, dy, dz.
For each depth d, each column point moves to p + d·axis (axes turned inward towards the fitted sphere centre). The neighbour
graph at each depth is the Delaunay graph in each point's tangent plane (its 25 nearest points, normal = smoothed axis); an edge
counts if both ends list each other. Interior = more than two rings from the rim, not folded (local map with negative determinant
or a principal stretch under 0.05), not on the patch hull at depth. Swapped = an interior edge of the cone layer that is missing at
depth d. A = ratio of the singular values of the least-squares 2×2 map of each point's neighbour offsets, cone layer to depth d.
Noise control: smoothed axes plus random tilts with the measured rms raw-to-smoothed tilt (seed 7).

## 16 Nov: first butterfly eye volume fetched (DICTO approved the override, '2 override check')

Paukner et al. 2024 (BossDB paukner2024, butterfly_retina_xray_grp02_gw05), scale 2400_2400_600: array 1004 × 566 × 419 (z, y, x), FINAL ok.
The volume stays on the compute machine and is never redistributed (no licence stated). Preview slices in figures/ are low-resolution
derived views for locating anatomy only. Seen by eye: the z = 502 slice cuts the eye across. The corneal lenses run as a bead row
along the outer arc, the ommatidia run radially inward through a dark layer to the cut rhabdom layer, and the optic lobe is on the left.
The x = 209 slice runs along the ommatidia: the facet lenses down the left edge, with the fibre pattern converging inward.
The depth axis is RADIAL (curved), not a grid axis, so the trace must follow each ommatidium along its own direction.
Next: a sub-block at 1200_1200_600 around the arc's middle; segment the cone and rhabdom cross-sections at successive radii and count
neighbour changes with depth (the scutoid test of the prediction stated before the data).

## 16 Nov: depth trace on the butterfly volume (ledger [270], [271])

**Conclusion: UNDECIDED.** In the cone layer, 10 of about 1330 neighbour pairs change over 35-100 µm depth (0.75%), against
4.2 ± 2.1 from position noise alone (image null). That is a weak excess, and it sits where the cone lattice ends. In the retina,
an apparent 8.0% of pairs change per 20 µm (206 of about 2560, null 96 ± 10), but inspection shows that most of these are long
edges across ommatidia the segmentation missed, so they are not trusted. Neither layer follows cornea curvature: Spearman
ρ = 0.00 (p = 0.99, 17 patches). This eye is nearly spherical, and its clear zone breaks the trace between cones and retina.
**No scutoid-like neighbour change is established, and the curvature prediction is neither confirmed nor refuted by this eye.**

Data: Paukner et al. 2024, BossDB collection paukner2024, experiment butterfly_retina_xray_grp02_gw05, channel
032019_DP_full_vol. Scale 600_600_600 (1676 × 2264 × 1004 voxels, 0.6 µm; 6 absent chunks in z 1000-1003 were left as
background). No licence is stated, so the volumes stay on the compute machine, outside git, and are not redistributed. Only
derived counts (data/eyetrace-summary.json) and two small, low-resolution figures are kept here. Scripts: scripts/eyeshells.py,
eyetrace.py, eyerun.py, eyesum.py, eyefig.py. Jobs eye-fetch600, eye-fetch600full (first run failed on an absent chunk: fixed,
rerun FINAL ok) and eye-trace (FINAL ok, 714 s).

### What the volume shows
- Cornea: fitted sphere R = 660 µm (rms 4.4 µm). A free quadric gives semi-axes within 3% of each other. In 17 patch tiles
  (0.2 × 0.2 rad), local principal radii have medians of 571 and 669 µm and the unevenness U = (k1 − k2)/(k1 + k2) has a median of
  0.11 (IQR 0.05-0.16). This is a near-spherical eye, not the strongly uneven case the prediction is about.
- Layers along the radius: lens and cone (0-40 µm), pigmented band (40-130 µm), a structureless band 130-280 µm (as a clear zone),
  then the retina (about 300-460 µm) with columns that run 11-24° off the sphere radius and bend by about 25° (structure tensor).
  No column could be followed through the 130-280 µm band, so cone and retina could not be paired one to one.
- Retina cross-sections: the bright dots (about 5 µm apart) form a honeycomb at the corners between ommatidia. The ommatidial
  lattice (about 9 µm, the count expected from the facets) is the set of dark centres. The cone layer is a clean lattice of bright discs.

### Method (as run)
Cone layer: concentric shells about the fitted sphere, at 1 µm steps from 10 to 130 µm. Each patch is 400 × 400 px at 1 mrad per px.
The depth window is chosen automatically where detections persist (median 34-97 µm). Retina: planes perpendicular to the
locally measured column direction (re-measured every 10 µm), stepped along it from 300 µm below the cornea for 180 µm
(500 × 500 px at 0.3 µm per px), in 20 µm segments; ommatidia are the dark centres of a band-pass image. Every shell or plane:
local maxima, watershed regions, weighted centroids. Tracks: predictive Hungarian linking, gaps of up to 3 shells, kept only if
linking bottom-up reproduces them (≥ 95%) and they never jump (< 0.25 period). Neighbour graph: Delaunay of ALL detections in the
shell (so every counted pair is a true lattice neighbour), counted only between trusted interior cells. A change is a pair present
at the top (majority of 5 shells) and absent at the bottom. Nulls: (1) image null, where straight columns at the measured top
positions plus every other detected cell are rendered with per-shell jitter calibrated to the measured centroid noise and run
through the same pipeline (10 seeds); (2) a bootstrap of the measured residual series. The patches are 0.2 rad apart and overlap,
so each cell and each change is counted once, in the patch tile that contains its direction from the eye centre.

### Controls (all through the image pipeline)
| control | result | expected |
|---|---|---|
| straight-column lattice | 0 of 120 pairs | 0 |
| lattice compressed across rows to A = 2 (past √3) | 28 of 86 (33%) | about 1/3 |
| jittered, disordered lattice (5 seeds, 0.05 period) | 3 lost vs image null 5.6 ± 3.0 | null rate |
| same, 0.12 period | 2 lost vs 7.8 ± 2.8 | null rate (the null errs high: conservative) |

### Results (tile-partitioned, smoothed tracks)
| layer | patches | cells / pairs | changed pairs | image null | bootstrap null | README model (table B) |
|---|---|---|---|---|---|---|
| cone (35-100 µm) | 19 | 574 / 1328 | 10 (0.75%) | 4.2 ± 2.1 | 1.4 ± 1.2 | 12.2 |
| retina, 90 segments of 20 µm | 19 | 19 per segment, 46% of detections tracked / 2563 | 206 (8.0%) | 96 ± 10 | 14 ± 4 | 50 |

Retina by depth below the cornea (changed / pairs, null): 300-340 µm 38/468 (28.7); 340-380 94/1200 (37.3); 380-420 57/725
(23.8); 420-460 17/169 (6.5). Against curvature: the more uneven half of the tiles has 103 changes against a null of 46, and the
more even half has 89 against 45. Spearman ρ of the retina excess with U is 0.00 (p 0.99), with convergence anisotropy A −0.20
(p 0.44), and with column bend +0.40 (p 0.12), n = 17.

**Inspection, which decides the reading.** Close-ups of the lost retina pairs (strongest segment: 33 of 149) show cells 1.5-2
lattice periods apart with undetected ommatidia between them. These are near-tied long Delaunay edges across detection gaps
(only 46% of detections are tracked), which the synthetic null does not reproduce, so the retina excess is a segmentation
effect until shown otherwise. The 26 cone-layer events (before tiling) are true neighbour pairs (length 0.9-1.1 period), but most
lie at the bottom of the window, where the cone lattice turns into pigment texture, and the clean ones are near-square rhombi.
Touching-region (watershed) adjacency changes much more often (cone 156/1221), because contacts at triple points flicker, so it
was not used for the verdict.

Figures (DICTO mark; low resolution): figures/eye-crosssection.png (cone shell and a retina segment, top and bottom, with the
neighbour graph; red = pairs that part) and figures/eye-swapmap.png (counted cells and changes on the eye surface, tiles shaded by U).

### LEADS
1. Retina segmentation: track the bright honeycomb corners (twice as many, well resolved) and take each ommatidium as the
   hexagon they ring; or use a 3D watershed on the band-pass volume. Aim for over 90% of cells tracked before counting.
2. Validate the retina reading on the volume-EM wasp eye (Makarova et al. 2025), where every cell is segmented: are retinula
   bundles' neighbour sets constant from cone tip to basement membrane?
3. Test the prediction where it applies: an apposition eye (no clear zone) with strongly uneven curvature. Check the other six
   Paukner eyes for species, clear zone and quadric anisotropy first (from their 2400 nm levels, a few minutes each).
4. Cone layer: extend the window into the cone tips, using the pigment-cell ring as the marker, to see whether the 10 changes
   persist or are end effects.
5. Measure the axis anisotropy A directly from cone tracks (the README's Δφ tensor). A median of 1.10 in the cone layer means
   the model expects few changes; compare per patch once the retina is trusted.

## 16 Nov: survey of the seven butterfly eyes for the next trace (ledger [272])

**Conclusion: trace gw16 next.** It is an apposition eye (no clear zone), and its columns can be followed from the cone
tips down through the retina. Its cornea is the most cleanly fitted, and moderately uneven (local radii about 805 and 1030 µm).
None of the five measurable eyes is uneven beyond what this survey can resolve. So gw16 tests the "no clear zone" half of the
question cleanly, but it is not the strongly oval eye that the prediction is about.

Data: Paukner et al. 2024 (Ecology and Evolution, CC BY 4.0 article; BossDB paukner2024, DOI 10.60533/boss-2023-okgx), seven
eyes from six species (*Heliconius cydno*, *Strymon melinus*, *Calycopis cecrops*, *Polygonia interrogationis*, *Polites peckius*,
two *Pieris rapae*). Neither the paper (first 100,000 characters of the PMC text, read) nor its code says which volume is which animal. Only gw07 is named by its channel folder
(CYD_102017_DP_full_vol, so most likely *H. cydno*). Every eye was read at scale 2400_2400_600 (2.4 × 2.4 × 0.6 µm). That is the
coarsest scale all seven share, and the one used for gw05. Four eyes also have 4800 and 9600 levels, but those are too coarse
to show columns. Fetch: job eye-survey-fetch (gw06 pilot 40 s; five eyes 3.6 GB, FINAL ok, no absent chunks). bossfetch.py now
finds the channel folder itself. The volumes stay on the compute machine, outside git. Committed here are
data/eyesurvey-summary.json (derived numbers) and figures/eye-survey.png (low-resolution sections and depth profiles). Scripts:
scripts/eyesurvey.py and eyesurveyfig.py (job eye-survey, FINAL ok on the second launch; the first stopped when two cornea
sheets broke after a mask change, which was fixed).

| rank | eye (volume, voxels) | clear zone | cornea quadric max/min, mid/min | local U median (IQR); radii | columns from the surface inward | problems |
|---|---|---|---|---|---|---|
| 1 | **gw16** (grp03; 2496 × 2547 × 1155) | none: thin pointed cones run straight into the retina | 1.27, 1.16 | 0.13 (0.08-0.18); 805 / 1030 µm | seen by eye as a continuous fan from cones to basement membrane; aligned 60-77 and 115-341 µm | retina partly detached from the brain behind it; tomography rings around the volume centre |
| 2 | gw07 (grp04, *H. cydno*?; 2975 × 2975 × 2162) | none | 1.34, 1.16 | 0.21 (0.15-0.41); 934 / 1416 µm | strongest column signal (aligned 55-96 and 391-598 µm) | three z blocks with brightness seams; eye cut at the field edges; cornea fit mixed with other surfaces (sphere rms 26 µm); 19 G voxels at 0.6 µm |
| 3 | gw06 (grp03; 1844 × 2626 × 1035) | none: same cone type as gw16 | 1.17, 1.12 | 0.12 (0.09-0.18); 616 / 793 µm | aligned 127-290 µm; fibres seen continuously below the cones | tomography rings; the roundest of the apposition eyes |
| 4 | gw17 (grp03; 2216 × 2960 × 1200) | none (thin pointed cones) | not measured | not measured | faint | very low contrast (eye interior about 3 grey levels against 0.3 outside); inside a sample tube; the cornea was found only in a patch (2 discs) |
| 5 | gw14 (grp02; 2451 × 3339 × 1100) | yes: large bright cones, pigment band, structureless band below about 130 µm | 2.21, 1.83 (fit mixed with other surfaces; 1.27 in a pilot) | 0.16 (0.10-0.44) | cones only (53-127 µm), then no column signal | tears between the cone layer and the retina; grey medium around the eye |
| 6 | gw05 (grp02; traced) | yes, 130-280 µm | trace: within 3%; this survey 1.45 | trace 0.11; this survey 0.25 | cones only (36-94 µm) | trace UNDECIDED (section above) |
| 7 | gw13 (grp02; 3424 × 3424 × 1200) | probably: same large bright cones as gw05 and gw14 | not measured | not measured | not judged | eye at the z edge of the volume and cut off; torn tissue; grey medium; sample tube |

How the columns were judged: by eye on three orthogonal slices of each volume, and by the share of voxels whose structure-tensor
column axis lies within 30° of the surface normal, at each depth (runs where the share is at least 0.5; profiles in the figure).
The three grp02 eyes (gw05, gw13, gw14) share large oval cones, a pigment band and a structureless band, so they read as clear-zone
eyes. The grp03 and grp04 eyes (gw06, gw16, gw17, gw07) have thin pointed cones whose fibres continue without a gap, so they read as
apposition eyes.

**Limits of the curvature numbers.** The cornea is found automatically. A local sphere is fitted through one seed point per eye,
read off the slices by eye. Rays are then cast from its centre, and the connected height map that keeps lens texture is kept.
On gw05 this survey gives U 0.11-0.25 and a quadric ratio of 1.15-1.45 across mask variants, where the careful trace gave 0.11
and 1.03. So U is good to about ±0.1 here. A free quadric on a cap is poorly posed: its bootstrap spread is small (±0.01), but
it moves with the choice of surface points. The ranking therefore rests on the clear zone and the columns. On curvature it says
only that gw07 may be the most uneven eye. Tried and dropped: a single sphere for the whole volume (it locked onto the sample
tube in gw13 and gw17 and onto the head capsule in gw16), and lens-boundary voxels as the sheet (too sparse to connect).
A radius-based clear-zone call misread fine apposition retina as a clear zone (gw06), so the clear-zone column is a visual call.

### Wasp eye (Makarova et al. 2025) as a validation set: facts checked, nothing downloaded
- Published: Makarova et al. 2025, eLife 14:RP103247, doi 10.7554/eLife.103247 (article CC BY 4.0). *Megaphragma viggianii*:
  29 ommatidia, 478 cells, FIB-SEM at 8 × 8 × 8 nm over 64 × 96 × 98.6 µm.
- Where: a public CATMAID server (waspem-lamina.flatironinstitute.org, readable without login). It holds one project
  ("Megaphragma wasp 0416"), an image stack of 8000 × 12000 × 12331 voxels at 8 nm served as JPEG tiles (about 1.2 T voxels, about
  1.2 TB raw), 685 skeleton tracings, and 253 annotations per ommatidium and cell type (for example ommatidia_C1, R1R4, R7,
  rhabdom_centerline, nuc_PR), plus two mesh volumes (an alpha shape and a training region).
- Segmentation: the paper's per-cell models (manual Imaris segmentation, Blender) are not released in any repository found. No
  EMPIAR, Zenodo or Dryad entry exists, and Supplementary file 1 holds measurements only. What is public is the CATMAID
  skeletons (centrelines, not cell volumes).
- Licence: none stated for the data (only the article is CC BY 4.0), so the same rule applies as for BossDB: analysis only,
  cited, nothing redistributed.
- Use: the photoreceptor and rhabdom centreline skeletons would give neighbour sets along depth directly, with no segmentation.
  Next step: read the R1-R8 skeletons per ommatidium (a few MB through the API).

### LEADS
1. Trace gw16 with the gw05 pipeline (a cone shell window, then planes that follow the columns). Its columns are continuous, so
   pair the cones and the retina one to one (impossible in gw05), and compare neighbour sets at the cone tips and at about 300 µm.
2. If gw16 shows no swaps, run gw07 as the more uneven eye: mask the z-block seams, and refit its cornea on one block only.
3. Wasp eye: fetch the R1-R8 and rhabdom-centreline skeletons from the public CATMAID API, and compute neighbour sets of the 29
   ommatidia along depth.
4. Cornea curvature: fit gw16 and gw07 at 1200 nm (cleaner surface) before claiming U, because this survey's U is only good to ±0.1.

## 16 Nov: depth trace of the apposition eye gw16 (ledger [273])

**Conclusion: NOT CONFIRMED.** No scutoid-like neighbour change is established in gw16. In the retina (120-340 µm), 799 of 4786
neighbour pairs (16.7%) change within 55 µm segments, against an image null of 809 ± 34. Sorted by eye, 0 of the 1505 flagged changes
in all layers is a true neighbour exchange. Only 54% of detections were tracked (median; target over 90%), so a small true rate cannot
be excluded. The changes do not follow cornea unevenness (Spearman ρ −0.18, p 0.63, 10 patches). This eye's convergence is nearly even
(A ≈ 1.03 per 55 µm segment, about 1.14 over 300 µm from the cornea radii), and for such an eye the prediction expects about 1%
scattered changes, which is below what this trace can resolve.

Data: Paukner et al. 2024, BossDB paukner2024, butterfly_retina_xray_grp03_gw16, channel 032019_DP_full_vol, scale 600_600_600. The
fetched block is x 100-1900, y 200-2300, all z (1155 × 2100 × 1800 voxels, 4.4 GB, 0 absent chunks; job eye16-fetch, FINAL ok). As
before, the volume stays on the compute machine, outside git. Committed here: data/eyetrace16-summary.json (derived counts, per patch and
per segment, with every flagged change and its sorting), data/eyetrace16-inspection.json (the by-eye calls with reasons), and two small
figures. Scripts: eyerun16.py (driver), eyesum16.py (pooling), eyefig16.py, eyesheets16.py (contact sheets for inspection, kept on the
compute machine). eyetrace.py gained a column-following tracker (`tracker='follow'`). eyeshells.make_fibre_stack gained a per-plane
pixel scale and a direction guard. eyesurvey.py now also saves the cornea sheet and the sphere centre. Job eye16-trace: FINAL ok, 1403 s.

### Method (as run)
- **Cornea and patches.** The survey's cornea sheet for gw16 was re-run and saved (same numbers: sphere R 961 µm, rms 7.9 µm). The
  volume holds only the upper part of the eye (693 µm in z), so 10 sheet points, 150 µm apart, have plane stacks that stay inside the
  block from 40 to 355 µm deep.
- **Planes.** Each plane is perpendicular to the cornea normal, 300 µm wide (600 px of 0.5 µm at the top), with planes 1 µm apart.
  The pixel shrinks as (961 − d)/(961 − d0), so even convergence (a similarity, which never changes a neighbour set) is taken out and
  the lattice period stays about constant in pixels (13.5 µm at 80 µm deep, measured on the cone lattice). A fresh stack is made
  for each depth segment.
- **Segments.** The cone window is 68-92 µm (clean bright discs), the cone tips 92-120 µm, and the retina 120-340 µm in four
  segments of 55 µm. One more whole-range stack (120-340 µm) measures how many columns can be followed through the entire retina.
- **Tracking (new: column following).** Cells are detected (band-pass, local maxima, watershed, weighted centroids) in the top,
  middle and bottom plane of a segment. Each is followed up and down through every plane by mean shift (weighted centre within
  0.35 period). A column counts only when tracks from two different seed planes agree within 0.25 period in every plane, which is the
  forward-backward test, and when no other column merges with it. Counting then follows the gw05 trace: the Delaunay graph of all
  detections, pairs between trusted interior columns, top versus bottom (majority of 5 planes), the image null (8 seeds plus 2
  calibration runs per segment), the bootstrap null, and the tile partition (each cell and change counted in the patch whose
  top-plane centre is nearest).
- **Cornea curvature per patch.** The surface was re-found at 0.6 µm along the sheet normals, and a quadric was fitted in 9 variants
  (disc radius 100, 132 or 180 µm × surface threshold at 30, 50 or 70% from outside to lens grey). The spread over the variants is
  the uncertainty of U.

**Pilots that set the method** (each 5 min or less, on two patches):
- The column-following frame (structure-tensor axis) tracked the cone window at 0.39 and the fixed-normal frame at 0.88. The measured
  axis follows the layering where the cones end (it turned 20-25° off the normal there). So the planes stay on the cornea normal.
  This departs from "trace along the measured direction", because the measured direction made tracking worse.
- Retina: dark centres tracked 0.58 (as in gw05). Bright cores with stronger smoothing (0.25 period in the plane, 8 µm in depth)
  tracked 0.87 on 150-210 µm in one patch and 0.51-0.63 elsewhere.
- Whole ranges fail. Following 60-340 µm tracked 0.13-0.20, and 120-340 µm tracked 0.29: columns are not reproduced from both ends
  through the cone tips (92-120 µm, little lattice signal; the survey's column-alignment gap at 77-115 µm) or through the deeper
  retina. That is why the count is per segment.
- The FFT period estimate locked onto wrong rings (55-107 px) in the retina, so the period is set from the cone lattice and scaled.

### Controls (same tracker and settings as the retina)
| control | result | expected |
|---|---|---|
| straight-column lattice | 0 of 170 pairs | 0 |
| lattice compressed across rows to A = 2 (past √3) | 40 of 120 (33%) | about 1/3 |
| jittered lattices, 0.05 period (5 seeds) | 6 lost vs image null 15.0 ± 4.6 | null rate (the null errs high) |
| jittered lattices, 0.12 period (5 seeds) | 18 lost vs 19.4 ± 7.2 | null rate |

### Results (tile-partitioned)
| layer | segments | tracked share (median, range) | counted cells / pairs | changed pairs | image null | bootstrap null | by eye: true |
|---|---|---|---|---|---|---|---|
| cone window 68-92 µm | 10 | 0.73 (0.51-0.90) | 1030 / 2430 | 448 (18.4%) | 133 ± 12 | 22 ± 4 | 0 |
| cone tips 92-120 µm | 10 | 0.58 (0.50-0.65) | 759 / 1285 | 258 (20.1%) | 242 ± 16 | 11 ± 3 | 0 |
| retina 120-340 µm | 40 | 0.54 (0.27-0.96) | 2862 / 4786 | 799 (16.7%) | 809 ± 34 | 34 ± 5 | 0 |

Retina by segment (changed / pairs, image null): 120-175 µm 124/942 (235); 175-230 µm 190/1638 (193); 230-285 µm 279/1171 (190);
285-340 µm 206/1036 (191). Whole-range following, 120-340 µm: tracked 0.19 (median), 286 trusted columns in 10 patches.
The best-tracked unit (patch 1, 175-230 µm, 96% tracked, 233 columns) has 42 of 613 pairs changing against an image null of 10.1.
Its lattice is clearly resolved (figure), but inspection shows no exchange (below).

**Inspection, which decides the reading.** All 1505 flagged changes were looked at on contact sheets: the top, middle and bottom
plane of each change, with the pair and its two opposite columns marked. Before the sheets were viewed, a rule pre-sorted them:
256 "clear flip", 129 "near-tie" and 1120 "artefact". By eye, none is a true neighbour exchange:
- **Cone window and tips (706).** The four columns of the pair keep their places, with bright discs at the top and middle. The pair is
  lost at the bottom of the window, where the cones taper out and texture detections fall between them. Where a flip is real in
  the graph, it is the diagonal of a near-square four-cone cell. These are layer-end effects. The rule had already marked 378 of the
  448 cone-window changes as artefacts: one cell of the pair was seen in under 80% of the planes, or the pair was still a Delaunay
  edge among the tracked columns at the bottom.
- **Retina (799).** The flagged pairs are 1.6-2 lattice periods long (median; over 1.3 periods for 88-99% of them), so they are
  diagonals across near-cocircular groups of four, not contacts. In single planes the ommatidia show as rings or blobs, and no
  opposite pair is seen coming into contact. In patches 7-9, tomography ring streaks and the detached retina cross the crops.
- So the cone-window excess over the image null (448 against 133) is an end-of-layer effect, and the retina total equals its null.

**Curvature and convergence.** Local cornea radii have medians of 765 and 981 µm. U per patch has a median of 0.12 (IQR 0.08-0.21,
range 0.06-0.29, 10 patches). The honest uncertainty of U is the spread over the 9 fit variants: median 0.06, and up to 0.17-0.22
in two patches (patch 0 0.06-0.23; patch 7 0.04-0.26). That agrees with the survey's ±0.1, so a patch's U is known to about ±0.03
at best and ±0.1 at worst. Across patches, retina changes minus the null show no link to U (ρ −0.18, p 0.63) and a weak, not
significant one to the segment convergence anisotropy A (ρ +0.55, p 0.10; A only 1.02-1.06 per segment). U and A are unrelated
(ρ −0.01). The more uneven half of the patches has 307 changes against a null of 347, and the more even half 492 against 462.
Since no true exchange was found, there is nothing to test against curvature beyond these null-level counts.

Figures (DICTO mark; low resolution; also in papers-to-read as RENDER-eye-gw16-*.png): figures/eye-gw16-crosssection.png (the
best-tracked retina segment, top, middle and bottom, with the neighbour graph and the 42 flagged pairs) and figures/eye-gw16-swapmap.png
(counted columns and flagged retina changes on the eye, patches shaded by U, and per-patch changes minus the null against U with
the U variant ranges).

### LEADS
1. Count only contacts. Restrict changes to pairs shorter than 1.3 periods at the top, and run the same restriction and rule pre-sort
   inside the image null, so that true-looking flips can be compared with the null (here the null was not sorted).
2. Retina segmentation is still below 90% (median 54%). Not yet tried on gw16: a 3D watershed on the column-smoothed band-pass
   volume, and the honeycomb-corner rings. Try them on patch 1 (96% in 175-230 µm), where the lattice is clean, before any count.
3. Cone window per patch: end it where the cone discs stop (from the disc contrast profile), so that the taper does not produce
   changes. Then the cone-tip-to-retina pairing (whole-range following, 19% now) can be chained segment to segment.
4. gw07 (U median 0.21 in the survey) is the more uneven apposition eye. Trace it with this pipeline after the z-block seams are
   masked. The prediction for gw16-like convergence (A ≈ 1.1) is about 1%, below this method's floor.
5. Wasp eye (Makarova et al. 2025): R1-R8 skeletons from the public CATMAID API need no segmentation, so they are the cleanest test
   of whether retinula bundles keep their neighbours.
