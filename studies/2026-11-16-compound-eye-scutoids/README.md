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
