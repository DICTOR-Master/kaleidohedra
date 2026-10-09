# The DICTO Hexa (DICTO, 2026-10-09)

DISCOVERIES.md #18. Names by DICTO. Design study with Claude (Fable), checked in krp-core v0.10.0.

## What it is
- **DICTO Hexa:** eight exact DICTO Jewels on a 2 × 2 × 2 block of cells, passing through each other
  inside, as one solid: a cube of edge 4 with the 24 outward roofs (volume 80 = 6⅔ Jewels at cube
  edge 2 per cell). DICTO saw it in Kaleidohedra's Studies (Windows, shear as copies).
- **DICTO Hexa-Key:** the gap between Hexas, 8 stella octangulas and 12 double roofs (volume 48 = 4
  Jewels). Hexas meet window to window (two whole windows per neighbour, 12 neighbours) and with
  Hexa-Keys fill space as a checkerboard, 5 : 3.
- **Parts:** the Hexa as 8 cubes + 24 roofs (split A) or 4 whole + 4 trimmed Jewels (split B); the
  Hexa-Key as 8 stellas + 24 roofs.
- **Clusters of eight Hexas:** rhombohedral (window to window, a Hexa-Key inside, 688) and diamond
  (sharing 7 corner Jewels, 556). The diamond network: Hexas sharing 4 corner Jewels each, stellas in
  every cell between.
- No shear makes eight exact Jewels meet face to face as a cube; no join in these packings turns.

## Data (`data/`)
Each file holds `vertices`, `faces`, `faceTags`, `pieces` (each closed, with its volume) and
`checks`; `-raw` is cube edge 2 per cell, `-unit` scales the Hexa's inner cube to edge 1.
- `jewel-cube-unified`, `jewel-cube-jewels-view`, `jewel-cube-pieces-A`, `jewel-cube-pieces-B`
- `g-unified`, `g-pieces` (the Hexa-Key)
- `jewel-cube-cluster-R-*`, `jewel-cube-cluster-D-*` (unified, as Hexas, as Jewels)

## Checks
krp-core `scripts/verify-hexa.mjs`, every push: closed and outward surfaces; exact volumes; 24 whole
Jewel windows and stella-matching walls on the Hexa; every parts view adding up. In the study: overlap
by sampling, exact contact areas, watertight Hexa-Key, the mating scan and the turning table.

## Renders (`renders/`)
`side-by-side-cube-vs-rhombohedron`, `C-cube-34`, `C-cube-face`, `G-gap`, `parts-A`, `parts-B`,
`cluster-R`, `cluster-D`, `network-sparse` (three Hexas round a Hexa-Key), `network-patch`,
`two-cubes`, and `side-by-side-cube-vs-A1-sheared` (the sheared version, not kept).

## Prior art
Not found (web search 2026-10-09) for a cube built from carved dodecahedra or this block of eight.
Credited: the stella octangula and octahedron space filling; the cube, octahedron and stella in the
rhombic dodecahedron; the FCC primitive cell as a squashed cube.

## DICTO's decisions
Names DICTO Hexa and DICTO Hexa-Key, others following them; both splits and both clusters kept; the
diamond network and the checkerboard as arrangements; lattice scale (faces match the Jewel and the
stella); a physical 3D puzzle noted as a future idea.
