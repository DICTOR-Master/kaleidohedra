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
