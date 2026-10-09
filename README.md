<p align="center"><img src="assets/brand/kaleidohedra-logo.jpg" alt="Kaleidohedra logo: a glowing many-coloured polyhedron with a square face at its centre, on a starfield" width="360"></p>

# KALEIDOHEDRA by DICTO

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23173809.svg)](https://doi.org/10.5281/zenodo.23173809)

*In development* — live at **[kaleidohedra.vercel.app](https://kaleidohedra.vercel.app)** and **[rhombiverse.vercel.app](https://rhombiverse.vercel.app)**. Since 2026-10-08 this repository is one app with two front doors: **Kaleidohedra** (orange), lattices you can shear and slide continuously, every piece moving with the lattice, and **Rhombiverse** (cyan), lattices of space-filling shapes from 1D to 6D. Each door has its own address, welcome, colours, guide and saved worlds; behind them the worlds, typography and controls are shared. The **DICTO** menu (top left) opens on the app you came in by, with the others a button away; [Polyhedraverse](https://polyhedraverse.vercel.app)'s space is inside it too, building included (KRP, DICTO's plan for the three). The geometry all three share is [krp-core](https://github.com/DICTOR-Master/krp-core).

- Per-app content (head, changelog, icons): `site/<app>/`; the one DICTO User Guide (shared sections, a chapter per app, 7 languages): `site/guide/`. The apps' table (names, colours, which tools each has): `src/app/site.js`; one type scale for all: `src/app/tokens.css`.
- Building a front door: `SITE=kaleidohedra npm run build` or `SITE=rhombiverse npm run build` (each Vercel project sets its own). Locally, `index.html?site=rhombiverse` opens Rhombiverse's door.

It began with two shapes DICTO found by building with their hands: a golden leaning hexagonal prism, and a skewed rhombic dodecahedron that fills space as a sheared FCC lattice (first notes in Polyhedraverse's `docs/`). Everything since grew from asking what else such shapes can do.

- `DISCOVERIES.md` — what has been found so far, how each is verified, and whether it is known.
- `TARGETS.md` — the target list: the 160 equal-edge space-filling cells whose edges meet only at special angles, searched both ways (`discover.py`, `discover_run.py`, output `data/geometry-targets.json`). All 160 can be seen in the app's **Targets** world (DICTO → 3D+), alone, with their face neighbours or as a 3×3×3 block; `scripts/verify-targets.mjs` rebuilds each from its data and checks it tiles space.
- `enumerate.py` — the earlier, smaller list (`targets.json`), all included in the new one.
- `assets/brand/` — the logo, with the name (`kaleidohedra-logo.jpg`) and without (`kaleidohedra-mark.jpg`), plus the site icons and preview image, drawn as an orange wireframe of the same shape. The logo shows the regular-hexagon elongated dodecahedron (DISCOVERIES.md #5), which is also the app's live symbol: it turns as a wireframe on Kaleidohedra's welcome screen.

## Findings and attribution

Geometry found by **DICTO** in this project, each checked numerically by a script in CI and dated by
the commit that first recorded it (full list, verification and literature status in `DISCOVERIES.md`):

| Finding | First recorded | Literature status |
|---|---|---|
| DICTO skewed rhombic dodecahedron (60° and 72° rhombi, tiles as a sheared FCC) | 2026-10-01 | not found — candidate |
| Regular-hexagon elongated dodecahedron (4 regular hexagons, 4 squares, 4 60° rhombi), reached independently by a new route (the Bain stretch) | 2026-10-01 | known — the truncated octahedron with one zone removed (Grünbaum 2010) |
| DICTO skewed elongated dodecahedra (two forms) | 2026-10-01 | not yet searched |
| Euclid–Kepler–Pacioli cell: cube, dodecahedron, icosahedron, great stellated dodecahedron, octahedron, stella octangula and Pacioli's golden rectangles in one cell, 13 nodes, Pm-3 | 2026-10-06 | not found — candidate |
| Euclid–Kepler–Pacioli network: Kepler's great stellated dodecahedra and icosahedra sharing only corners | 2026-10-06 | not found — candidate |
| EKP windows: carving the six neighbouring stella octangulas out of the dodecahedron leaves 12 Penrose thick rhombi (72°) at its own face angles | 2026-10-08 | not found — candidate |
| Stretched dodecahedron: 8 regular pentagons, 4 hexagons and 2 rectangles at any stretch, squares at one edge | 2026-10-08 | not found — candidate |
| Study of the windows (10a): pushed out by √(7 − 4φ), a convex 74-face solid of 12 Penrose thick rhombi, 6 golden rhombi, 8 equilateral triangles and 48 triangles; buildable from a flat net | 2026-10-08 | study of the windows, not a separate claim |

"Not found" means a web-level search turned up nothing, not proof of novelty. Cite as
*DICTO, Kaleidohedra discoveries, #N (first recorded date), https://doi.org/10.5281/zenodo.23173809*. Each release is archived on Zenodo under that DOI; the latest, [v2026.10.09-octet](https://doi.org/10.5281/zenodo.23256623), adds #14 DICTO-Star, #15 the DICTO Jewel clusters and #16 the Sunstar clusters; [v2026.10.09-cluster](https://doi.org/10.5281/zenodo.23247392) added #13, the 13-dodecahedron cluster made solid; [v2026.10.08-star-chain](https://doi.org/10.5281/zenodo.23226716) #12, the Star Chain Reaction, and study 12a, the Jewel chain (archived as the Dragon chain); [v2026.10.08-checkerboard](https://doi.org/10.5281/zenodo.23223555) added study 10b; [v2026.10.08-convex](https://doi.org/10.5281/zenodo.23220833) the windows made convex (now study 10a); [v2026.10.08](https://doi.org/10.5281/zenodo.23220273) #10 and #11.

## Shared geometry

The shared geometry (lattices, cells, quasicrystals, rhombic dodecahedron pieces) lives in
[krp-core](https://github.com/DICTOR-Master/krp-core), shared with Rhombiverse and pinned here as a git
submodule at `src/krp-core`. Clone with it:

```
git clone --recurse-submodules https://github.com/DICTOR-Master/kaleidohedra
# or, in an existing clone: git submodule update --init
```
