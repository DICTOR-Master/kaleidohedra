# Scutoids in compound eyes: a testable prediction (scope study)

DICTO, 16 Nov 2026 (continues next step 2 of studies/2026-11-15-scutoid-lenses, and #104 Scutoid Tissues). His proposal: scutoids
should appear in unevenly curved compound eyes. Ommatidia run as columns from the cornea (outer surface) to the basement membrane
(inner, smaller surface). If the two surfaces shrink evenly in every direction, the columns are plain frusta and keep their
neighbours. If they shrink unevenly, the columns may have to change neighbours on the way down: scutoids (Gómez-Gálvez et al.
2018; Mughal, Cox, Weaire, Burke, Hutzler 2018 for foams between concentric cylinders).

VERDICT: (written after the pilot, below)

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
