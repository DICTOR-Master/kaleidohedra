# Kaleidohedra target list

*Kaleidohedra by DICTO — private working notes, 2026-10-01.*

**The target:** every space-filling cell (a zonohedral parallelohedron, Fedorov's five types) with **all edges equal** whose edge directions meet only at **special angles**: 36°, 45°, 60°, arccos(1/3) ≈ 70.53°, 72° and 90° (the regularity meter's set). Its faces are then squares, rhombi of those angles, and equal-edged hexagons, regular when their three angles are all 60°. Shapes are counted exactly, up to congruence; mirror images count once (these solids are centrally symmetric).

**Searched both ways** (`discover.py`, `discover_run.py`, output `data/geometry-targets.json`):

- **Top-down:** every direction set built exactly from its angles: three independent directions fixed by their three angles, every further one by its angles to those three, then kept if it fills space (every direction in belts of 4 or 6 faces).
- **Bottom-up:** an independent continuous search over every cell shape of each type (the space the sliders move through), 6,000 random starts per type, each polished until its angles land on the special set.

The two agree: bottom-up found **158 of the 160** and **nothing outside them**. The two it missed are the regular rhombic dodecahedron and the Bain RD, both highly symmetric points that random starts rarely land on, and both already verified in this repo's checks.

| Type (Fedorov) | Tiles as | Count | Found bottom-up | In Polyhedraverse |
|---|---|---|---|---|
| parallelepiped | sheared simple-cubic | 64 | 64 | 8 |
| hexagonal prism | sheared hexagonal | 31 | 31 | 3 |
| rhombic dodecahedron | sheared FCC | 27 | 25 | 3 |
| elongated dodecahedron | sheared ED lattice | 28 | 28 | 4 |
| truncated octahedron | sheared BCC | 10 | 10 | 1 |
| **total** | | **160** | **158** | **19** |

## The most regular: 9 cells

Every equal-edge space-filler whose faces are only **squares, regular hexagons and 60° rhombi** (each two equilateral triangles). The list is complete: those faces need only 60° and 90° angles, which the search covers exactly.

| Type | Faces | Volume (edge 1) | In Polyhedraverse |
|---|---|---|---|
| parallelepiped | 6 rhombus 60 | 0.707107 | RHOMBOHEDRON_60 |
| parallelepiped | 4 rhombus 60, 2 square | 0.707107 | LEANING_SQUARE_PRISM |
| parallelepiped | 4 square, 2 rhombus 60 | 0.866025 | RHOMBIC_PRISM_60 |
| parallelepiped | 6 square | 1 | CUBE |
| hexagonal prism | 4 rhombus 60, 2 regular hexagon, 2 square | 2.12132 | LEANING_HEX_PRISM_60 |
| hexagonal prism | 6 square, 2 regular hexagon | 2.59808 | PRISM_6 |
| rhombic dodecahedron | 8 rhombus 60, 4 square | 2.82843 | BAIN_RD |
| elongated dodecahedron | 4 regular hexagon, 4 rhombus 60, 4 square | 5.65685 | REGULAR_HEX_ED |
| truncated octahedron | 8 regular hexagon, 6 square | 11.3137 | TRUNCATED_OCTAHEDRON |

The elongated dodecahedron has exactly one such form, the regular-hexagon ED (DISCOVERIES.md #5); the rhombic dodecahedron exactly one, the Bain RD (#4).

Volumes are at edge 1. **Line angles** are the angles between the edge directions (as lines), one per pair. Shapes with the same line angles can still differ (edges meeting at 60° in one, 120° in the other); the volume tells them apart.

## Parallelepiped — sheared simple-cubic (64)

| # | Faces | Line angles | Volume | Status |
|---|---|---|---|---|
| 1 | 6 rhombus 36 | 36, 36, 36 | 0.309017 | to find |
| 2 | 4 rhombus 36, 2 rhombus 45 | 36, 36, 45 | 0.341464 | to find |
| 3 | 4 rhombus 36, 2 rhombus 60 | 36, 36, 60 | 0.309017 | to find |
| 4 | 4 rhombus 36, 2 rhombus 70.53 | 36, 36, 70.53 | 0.127322 | to find |
| 5 | 4 rhombus 45, 2 rhombus 36 | 36, 45, 45 | 0.393076 | to find |
| 6 | 2 rhombus 36, 2 rhombus 45, 2 rhombus 60 | 36, 45, 60 | 0.409332 | to find |
| 7 | 2 rhombus 36, 2 rhombus 45, 2 rhombus 70.53 | 36, 45, 70.53 | 0.340227 | to find |
| 8 | 2 rhombus 36, 2 rhombus 45, 2 rhombus 72 | 36, 45, 72 | 0.321797 | to find |
| 9 | 4 rhombus 60, 2 rhombus 36 | 36, 60, 60 | 0.5 | to find |
| 10 | 2 rhombus 36, 2 rhombus 60, 2 rhombus 70.53 | 36, 60, 70.53 | 0.504036 | to find |
| 11 | 2 rhombus 36, 2 rhombus 60, 2 rhombus 72 | 36, 60, 72 | 0.5 | to find |
| 12 | 2 rhombus 36, 2 rhombus 60, 2 square | 36, 60, 90 | 0.309017 | to find |
| 13 | 4 rhombus 70.53, 2 rhombus 36 | 36, 70.53, 70.53 | 0.550501 | to find |
| 14 | 2 rhombus 36, 2 rhombus 70.53, 2 rhombus 72 | 36, 70.53, 72 | 0.552771 | to find |
| 15 | 2 rhombus 36, 2 rhombus 70.53, 2 square | 36, 70.53, 90 | 0.484128 | to find |
| 16 | 4 rhombus 72, 2 rhombus 36 | 36, 72, 72 | 0.555893 | to find |
| 17 | 2 rhombus 36, 2 rhombus 72, 2 square | 36, 72, 90 | 0.5 | to find |
| 18 | 4 square, 2 rhombus 36 | 36, 90, 90 | 0.587785 | to find |
| 19 | 6 rhombus 45 | 45, 45, 45 | 0.45509 | to find |
| 20 | 4 rhombus 45, 2 rhombus 60 | 45, 45, 60 | 0.5 | to find |
| 21 | 4 rhombus 45, 2 rhombus 70.53 | 45, 45, 70.53 | 0.471405 | to find |
| 22 | 4 rhombus 45, 2 rhombus 72 | 45, 45, 72 | 0.462088 | to find |
| 23 | 4 rhombus 60, 2 rhombus 45 | 45, 60, 60 | 0.594604 | to find |
| 24 | 2 rhombus 45, 2 rhombus 60, 2 rhombus 70.53 | 45, 60, 70.53 | 0.612039 | to find |
| 25 | 2 rhombus 45, 2 rhombus 60, 2 rhombus 72 | 45, 60, 72 | 0.610751 | to find |
| 26 | 2 rhombus 45, 2 rhombus 60, 2 square | 45, 60, 90 | 0.5 | to find |
| 27 | 4 rhombus 70.53, 2 rhombus 45 | 45, 70.53, 70.53 | 0.347337 | to find |
| 28 | 4 rhombus 70.53, 2 rhombus 45 | 45, 70.53, 70.53 | 0.659479 | to find |
| 29 | 2 rhombus 45, 2 rhombus 70.53, 2 rhombus 72 | 45, 70.53, 72 | 0.384351 | to find |
| 30 | 2 rhombus 45, 2 rhombus 70.53, 2 rhombus 72 | 45, 70.53, 72 | 0.662623 | to find |
| 31 | 2 rhombus 45, 2 rhombus 70.53, 2 square | 45, 70.53, 90 | 0.62361 | to find |
| 32 | 4 rhombus 72, 2 rhombus 45 | 45, 72, 72 | 0.417099 | to find |
| 33 | 4 rhombus 72, 2 rhombus 45 | 45, 72, 72 | 0.66638 | to find |
| 34 | 2 rhombus 45, 2 rhombus 72, 2 square | 45, 72, 90 | 0.63601 | to find |
| 35 | 4 square, 2 rhombus 45 | 45, 90, 90 | 0.707107 | to find |
| 36 | 6 rhombus 60 | 60, 60, 60 | 0.707107 | built: RHOMBOHEDRON_60 |
| 37 | 4 rhombus 60, 2 rhombus 70.53 | 60, 60, 70.53 | 0.471405 | to find |
| 38 | 4 rhombus 60, 2 rhombus 70.53 | 60, 60, 70.53 | 0.745356 | to find |
| 39 | 4 rhombus 60, 2 rhombus 72 | 60, 60, 72 | 0.5 | built: DICTO_FLATTENED_RHOMBOHEDRON |
| 40 | 4 rhombus 60, 2 rhombus 72 | 60, 60, 72 | 0.747674 | to find |
| 41 | 4 rhombus 60, 2 square | 60, 60, 90 | 0.707107 | built: LEANING_SQUARE_PRISM |
| 42 | 4 rhombus 70.53, 2 rhombus 60 | 60, 70.53, 70.53 | 0.645497 | to find |
| 43 | 4 rhombus 70.53, 2 rhombus 60 | 60, 70.53, 70.53 | 0.799305 | to find |
| 44 | 2 rhombus 60, 2 rhombus 70.53, 2 rhombus 72 | 60, 70.53, 72 | 0.66362 | to find |
| 45 | 2 rhombus 60, 2 rhombus 70.53, 2 rhombus 72 | 60, 70.53, 72 | 0.803992 | to find |
| 46 | 2 rhombus 60, 2 rhombus 70.53, 2 square | 60, 70.53, 90 | 0.799305 | to find |
| 47 | 4 rhombus 72, 2 rhombus 60 | 60, 72, 72 | 0.680827 | to find |
| 48 | 4 rhombus 72, 2 rhombus 60 | 60, 72, 72 | 0.809017 | built: DICTO_ALL_RHOMBUS_BLOCK |
| 49 | 2 rhombus 60, 2 rhombus 72, 2 square | 60, 72, 90 | 0.809017 | built: DICTO_SQUARE_FACED_BLOCK |
| 50 | 4 square, 2 rhombus 60 | 60, 90, 90 | 0.866025 | built: RHOMBIC_PRISM_60 |
| 51 | 6 rhombus 70.53 | 70.53, 70.53, 70.53 | 0.7698 | built: RHOMBOHEDRON |
| 52 | 6 rhombus 70.53 | 70.53, 70.53, 70.53 | 0.860663 | to find |
| 53 | 4 rhombus 70.53, 2 rhombus 72 | 70.53, 70.53, 72 | 0.783336 | to find |
| 54 | 4 rhombus 70.53, 2 rhombus 72 | 70.53, 70.53, 72 | 0.866578 | to find |
| 55 | 4 rhombus 70.53, 2 square | 70.53, 70.53, 90 | 0.881917 | to find |
| 56 | 4 rhombus 72, 2 rhombus 70.53 | 70.53, 72, 72 | 0.796395 | to find |
| 57 | 4 rhombus 72, 2 rhombus 70.53 | 70.53, 72, 72 | 0.872678 | to find |
| 58 | 2 rhombus 70.53, 2 rhombus 72, 2 square | 70.53, 72, 90 | 0.890729 | to find |
| 59 | 4 square, 2 rhombus 70.53 | 70.53, 90, 90 | 0.942809 | to find |
| 60 | 6 rhombus 72 | 72, 72, 72 | 0.809017 | to find |
| 61 | 6 rhombus 72 | 72, 72, 72 | 0.878944 | to find |
| 62 | 4 rhombus 72, 2 square | 72, 72, 90 | 0.899454 | to find |
| 63 | 4 square, 2 rhombus 72 | 72, 90, 90 | 0.951057 | to find |
| 64 | 6 square | 90, 90, 90 | 1 | built: CUBE |

## Hexagonal prism — sheared hexagonal (31)

| # | Faces | Line angles | Volume | Status |
|---|---|---|---|---|
| 1 | 4 rhombus 36, 2 hexagon 144/144/72, 2 rhombus 60 | 36, 36, 36, 36, 60, 72 | 1.11803 | tentative: built as HEX_TARGET_1 (Polyhedraverse 63e00ac; corners measured 144/144/72, label corrected) |
| 2 | 2 hexagon 144/144/72, 2 rhombus 36, 2 rhombus 60, 2 square | 36, 36, 36, 60, 72, 90 | 1.11803 | tentative: built as HEX_TARGET_2 (Polyhedraverse 63e00ac; corners measured 144/144/72, label corrected) |
| 3 | 4 rhombus 36, 2 hexagon 144/108/108, 2 square | 36, 36, 36, 72, 72, 90 | 1.30902 | confirmed: built as HEX_TARGET_3 (Polyhedraverse 98f529c) |
| 4 | 4 rhombus 36, 2 regular hexagon, 2 square | 36, 36, 60, 60, 60, 90 | 0.927051 | confirmed: built as HEX_TARGET_4 (Polyhedraverse 98f529c) |
| 5 | 4 rhombus 60, 2 hexagon 144/108/108, 2 rhombus 36 | 36, 36, 60, 60, 72, 72 | 1.30902 | confirmed: built as HEX_TARGET_5 (Polyhedraverse 98f529c) |
| 6 | 4 rhombus 60, 2 hexagon 144/144/72, 2 rhombus 72 | 36, 36, 60, 60, 72, 72 | 1.80902 | tentative: built as HEX_TARGET_6 (Polyhedraverse 63e00ac; corners measured 144/144/72, label corrected) |
| 7 | 4 rhombus 60, 2 hexagon 144/144/72, 2 square | 36, 36, 60, 60, 72, 90 | 1.11803 | tentative: built as HEX_TARGET_7 (Polyhedraverse 63e00ac; corners measured 144/144/72, label corrected) |
| 8 | 2 hexagon 144/108/108, 2 rhombus 36, 2 rhombus 60, 2 square | 36, 36, 60, 72, 72, 90 | 1.30902 | confirmed: built as HEX_TARGET_8 (Polyhedraverse 98f529c) |
| 9 | 2 hexagon 144/144/72, 2 rhombus 60, 2 rhombus 72, 2 square | 36, 36, 60, 72, 72, 90 | 1.80902 | tentative: built as HEX_TARGET_9 (Polyhedraverse 63e00ac; corners measured 144/144/72, label corrected) |
| 10 | 4 rhombus 70.53, 2 hexagon 144/144/72, 2 square | 36, 36, 70.53, 70.53, 72, 90 | 1.75159 | tentative: built as HEX_TARGET_10 (Polyhedraverse 63e00ac; corners measured 144/144/72, label corrected) |
| 11 | 4 rhombus 72, 2 hexagon 144/144/72, 2 square | 36, 36, 72, 72, 72, 90 | 1.80902 | tentative: built as HEX_TARGET_11 (Polyhedraverse 63e00ac; corners measured 144/144/72, label corrected) |
| 12 | 6 square, 2 hexagon 144/144/72 | 36, 36, 72, 90, 90, 90 | 2.12663 | tentative: built as HEX_TARGET_12 (Polyhedraverse 63e00ac; corners measured 144/144/72, label corrected) |
| 13 | 4 rhombus 45, 2 hexagon 144/108/108, 2 square | 36, 45, 45, 72, 72, 90 | 1.66509 | confirmed: built as HEX_TARGET_13 (Polyhedraverse 98f529c) |
| 14 | 2 regular hexagon, 2 rhombus 36, 2 rhombus 60, 2 rhombus 72 | 36, 60, 60, 60, 60, 72 | 1.5 | confirmed: built as HEX_TARGET_14 (Polyhedraverse 98f529c) |
| 15 | 4 rhombus 60, 2 hexagon 144/108/108, 2 square | 36, 60, 60, 72, 72, 90 | 2.11803 | confirmed: built as HEX_TARGET_15 (Polyhedraverse 98f529c) |
| 16 | 4 rhombus 72, 2 hexagon 144/108/108, 2 rhombus 60 | 36, 60, 72, 72, 72, 72 | 2.11803 | confirmed: built as HEX_TARGET_16 (Polyhedraverse 98f529c) |
| 17 | 2 hexagon 144/108/108, 2 rhombus 60, 2 rhombus 72, 2 square | 36, 60, 72, 72, 72, 90 | 2.11803 | confirmed: built as HEX_TARGET_17 (Polyhedraverse 98f529c) |
| 18 | 4 rhombus 70.53, 2 hexagon 144/108/108, 2 square | 36, 70.53, 70.53, 72, 72, 90 | 2.33196 | confirmed: built as HEX_TARGET_18 (Polyhedraverse 98f529c) |
| 19 | 4 rhombus 72, 2 hexagon 144/108/108, 2 square | 36, 72, 72, 72, 72, 90 | 2.3548 | confirmed: built as HEX_TARGET_19 (Polyhedraverse 98f529c) |
| 20 | 6 square, 2 hexagon 144/108/108 | 36, 72, 72, 90, 90, 90 | 2.4899 | confirmed: built as HEX_TARGET_20 (Polyhedraverse 98f529c) |
| 21 | 4 rhombus 60, 2 hexagon 135/135/90, 2 rhombus 45 | 45, 45, 45, 60, 60, 90 | 1.70711 | confirmed: built as HEX_TARGET_21 (Polyhedraverse 98f529c) |
| 22 | 2 hexagon 135/135/90, 2 rhombus 45, 2 rhombus 60, 2 square | 45, 45, 45, 60, 90, 90 | 1.70711 | confirmed: built as HEX_TARGET_22 (Polyhedraverse 98f529c) |
| 23 | 4 rhombus 45, 2 regular hexagon, 2 square | 45, 45, 60, 60, 60, 90 | 1.5 | confirmed: built as HEX_TARGET_23 (Polyhedraverse 98f529c) |
| 24 | 4 rhombus 60, 2 hexagon 135/135/90, 2 square | 45, 45, 60, 60, 90, 90 | 1.70711 | confirmed: built as HEX_TARGET_24 (Polyhedraverse 98f529c) |
| 25 | 4 rhombus 70.53, 2 hexagon 135/135/90, 2 square | 45, 45, 70.53, 70.53, 90, 90 | 2.12914 | confirmed: built as HEX_TARGET_25 (Polyhedraverse 98f529c) |
| 26 | 4 rhombus 72, 2 hexagon 135/135/90, 2 square | 45, 45, 72, 72, 90, 90 | 2.17147 | confirmed: built as HEX_TARGET_26 (Polyhedraverse 98f529c) |
| 27 | 6 square, 2 hexagon 135/135/90 | 45, 45, 90, 90, 90, 90 | 2.41421 | confirmed: built as HEX_TARGET_27 (Polyhedraverse 98f529c) |
| 28 | 4 rhombus 60, 2 regular hexagon, 2 square | 60, 60, 60, 60, 60, 90 | 2.12132 | built: LEANING_HEX_PRISM_60 |
| 29 | 4 rhombus 70.53, 2 regular hexagon, 2 square | 60, 60, 60, 70.53, 70.53, 90 | 2.39792 | confirmed: built as HEX_TARGET_29 (Polyhedraverse 98f529c) |
| 30 | 4 rhombus 72, 2 regular hexagon, 2 square | 60, 60, 60, 72, 72, 90 | 2.42705 | built: DICTO_LEANING_HEX_PRISM |
| 31 | 6 square, 2 regular hexagon | 60, 60, 60, 90, 90, 90 | 2.59808 | built: PRISM_6 |

**Tentative builds (to investigate):** rows 1, 2, 6, 7, 9, 10, 11 and 12 were listed as "hexagon 144/144/108". That label came from a formula that read the wrap-around corner as 180 minus its angle, which is wrong for that corner. Measured on the built polygons, the corners are 144/144/72 (repeated), which sum to 720°, as the table requires. The label is now computed from the directions (discover.py and targets.js, `hex_corners`), and the 26 rows that carried the old label are relabelled. The rows stay tentative until the source table is checked: the table itself may still carry the 108.

## Rhombic dodecahedron — sheared FCC (27)

Status: *to find* means predicted by the enumeration, not yet built or checked. *confirmed* means verified by construction: built from four edge directions, with volumes matching this table. Whether a confirmed shape is new or already known is a separate question, not settled by building it.

| # | Faces | Line angles | Volume | Status |
|---|---|---|---|---|
| 1 | 6 rhombus 36, 6 rhombus 60 | 36, 36, 36, 60, 60, 60 | 1.61803 | confirmed: built as RD_TARGET_1 (Polyhedraverse 9599e14) |
| 2 | 6 rhombus 36, 4 rhombus 60, 2 square | 36, 36, 36, 60, 60, 90 | 1.42705 | confirmed: built as RD_TARGET_2 (Polyhedraverse 9599e14) |
| 3 | 6 rhombus 60, 4 rhombus 36, 2 rhombus 70.53 | 36, 36, 60, 60, 60, 70.53 | 1.87268 | confirmed: built as RD_TARGET_3 (Polyhedraverse 9599e14) |
| 4 | 4 rhombus 36, 4 rhombus 60, 4 rhombus 72 | 36, 36, 60, 60, 72, 72 | 2 | confirmed: built as RD_TARGET_4 (Polyhedraverse 9599e14) |
| 5 | 4 rhombus 36, 4 rhombus 60, 2 rhombus 72, 2 square | 36, 36, 60, 60, 72, 90 | 1.80902 | confirmed: built as RD_TARGET_5 (Polyhedraverse 9599e14) |
| 6 | 4 rhombus 36, 4 rhombus 60, 2 rhombus 72, 2 square | 36, 36, 60, 60, 72, 90 | 1.92705 | confirmed: built as RD_TARGET_6 (Polyhedraverse 9599e14) |
| 7 | 4 rhombus 36, 4 rhombus 72, 2 rhombus 60, 2 rhombus 70.53 | 36, 36, 60, 70.53, 72, 72 | 2 | confirmed: built as RD_TARGET_7 (Polyhedraverse 9599e14) |
| 8 | 4 rhombus 36, 4 rhombus 72, 2 rhombus 60, 2 square | 36, 36, 60, 72, 72, 90 | 2.11803 | confirmed: built as RD_TARGET_8 (Polyhedraverse 9599e14) |
| 9 | 4 rhombus 36, 4 square, 2 rhombus 60, 2 rhombus 72 | 36, 36, 60, 72, 90, 90 | 1.61803 | confirmed: built as RD_TARGET_9 (Polyhedraverse 9599e14) |
| 10 | 6 rhombus 60, 2 rhombus 36, 2 rhombus 72, 2 square | 36, 60, 60, 60, 72, 90 | 2.11803 | confirmed: built as RD_TARGET_10 (Polyhedraverse 9599e14) |
| 11 | 4 rhombus 60, 4 rhombus 72, 2 rhombus 36, 2 square | 36, 60, 60, 72, 72, 90 | 2.30902 | confirmed: built as RD_TARGET_11 (Polyhedraverse 9599e14) |
| 12 | 4 rhombus 60, 4 rhombus 72, 2 rhombus 36, 2 square | 36, 60, 60, 72, 72, 90 | 2.42705 | confirmed: built as RD_TARGET_12 (Polyhedraverse 9599e14) |
| 13 | 4 rhombus 60, 4 square, 2 rhombus 36, 2 rhombus 72 | 36, 60, 60, 72, 90, 90 | 2.23607 | confirmed: built as RD_TARGET_13 (Polyhedraverse 9599e14) |
| 14 | 4 rhombus 72, 4 square, 2 rhombus 36, 2 rhombus 60 | 36, 60, 72, 72, 90, 90 | 2.61803 | confirmed: built as RD_TARGET_14 (Polyhedraverse 9599e14) |
| 15 | 6 square, 2 rhombus 36, 2 rhombus 60, 2 rhombus 72 | 36, 60, 72, 90, 90, 90 | 2.61803 | confirmed: built as RD_TARGET_15 (Polyhedraverse 9599e14) |
| 16 | 8 rhombus 45, 2 rhombus 60, 2 rhombus 70.53 | 45, 45, 45, 45, 60, 70.53 | 1.94281 | confirmed: built as RD_TARGET_16 (Polyhedraverse 9599e14) |
| 17 | 6 rhombus 60, 4 rhombus 45, 2 square | 45, 45, 60, 60, 60, 90 | 2.20711 | confirmed: built as RD_TARGET_17 (Polyhedraverse 9599e14) |
| 18 | 4 rhombus 45, 4 square, 2 rhombus 60, 2 rhombus 70.53 | 45, 45, 60, 70.53, 90, 90 | 2.41421 | confirmed: built as RD_TARGET_18 (Polyhedraverse 9599e14) |
| 19 | 6 square, 4 rhombus 45, 2 rhombus 60 | 45, 45, 60, 90, 90, 90 | 2.41421 | confirmed: built as RD_TARGET_19 (Polyhedraverse 9599e14) |
| 20 | 6 square, 4 rhombus 60, 2 rhombus 45 | 45, 60, 60, 90, 90, 90 | 2.70711 | confirmed: built as RD_TARGET_20 (Polyhedraverse 9599e14) |
| 21 | 10 rhombus 60, 2 rhombus 70.53 | 60, 60, 60, 60, 60, 70.53 | 2.35702 | confirmed: built as RD_TARGET_21 (Polyhedraverse 9599e14) |
| 22 | 8 rhombus 60, 4 square | 60, 60, 60, 60, 90, 90 | 2.82843 | built: BAIN_RD (top-down only) |
| 23 | 6 rhombus 60, 4 rhombus 72, 2 rhombus 70.53 | 60, 60, 60, 70.53, 72, 72 | 2.61803 | confirmed: built as RD_TARGET_23 (Polyhedraverse 9599e14) |
| 24 | 6 rhombus 60, 4 square, 2 rhombus 70.53 | 60, 60, 60, 70.53, 90, 90 | 2.82843 | confirmed: built as RD_TARGET_24 (Polyhedraverse 9599e14) |
| 25 | 6 rhombus 60, 6 rhombus 72 | 60, 60, 60, 72, 72, 72 | 2.61803 | built: DICTO_SKEWED_RD |
| 26 | 6 rhombus 72, 4 rhombus 60, 2 square | 60, 60, 72, 72, 72, 90 | 2.92705 | confirmed: built as RD_TARGET_26 (Polyhedraverse 9599e14) |
| 27 | 12 rhombus 70.53 | 70.53, 70.53, 70.53, 70.53, 70.53, 70.53 | 3.0792 | built: RHOMBIC_DODECAHEDRON (top-down only) |

## Elongated dodecahedron — sheared ED lattice (28)

| # | Faces | Line angles | Volume | Status |
|---|---|---|---|---|
| 1 | 4 hexagon 144/144/72, 4 rhombus 36, 4 rhombus 60 | 36, 36, 36, 36, 36, 36, 60, 60, 72, 72 | 3.23607 | to find |
| 2 | 6 rhombus 60, 4 hexagon 144/144/72, 2 rhombus 36 | 36, 36, 36, 36, 36, 60, 60, 60, 72, 72 | 3.73607 | to find |
| 3 | 4 hexagon 144/144/72, 4 rhombus 60, 2 rhombus 36, 2 square | 36, 36, 36, 36, 36, 60, 60, 72, 72, 90 | 3.54508 | to find |
| 4 | 4 rhombus 36, 2 hexagon 144/144/72, 2 regular hexagon, 2 rhombus 60, 2 square | 36, 36, 36, 36, 60, 60, 60, 60, 72, 90 | 3.04508 | to find |
| 5 | 4 rhombus 36, 4 square, 2 hexagon 144/144/72, 2 regular hexagon | 36, 36, 36, 36, 60, 60, 60, 72, 90, 90 | 2.8541 | to find |
| 6 | 4 rhombus 60, 2 hexagon 144/108/108, 2 hexagon 144/144/72, 2 rhombus 36, 2 square | 36, 36, 36, 36, 60, 60, 72, 72, 72, 90 | 3.92705 | to find |
| 7 | 2 hexagon 144/108/108, 2 hexagon 144/144/72, 2 rhombus 36, 2 rhombus 60, 2 rhombus 72, 2 square | 36, 36, 36, 36, 60, 72, 72, 72, 72, 90 | 4.23607 | to find |
| 8 | 4 hexagon 144/144/72, 4 square, 2 rhombus 60, 2 rhombus 72 | 36, 36, 36, 36, 60, 72, 72, 72, 90, 90 | 3.73607 | to find |
| 9 | 4 rhombus 36, 4 rhombus 60, 2 hexagon 144/108/108, 2 regular hexagon | 36, 36, 36, 60, 60, 60, 60, 60, 72, 72 | 3.61803 | to find |
| 10 | 4 rhombus 36, 2 hexagon 144/108/108, 2 regular hexagon, 2 rhombus 60, 2 square | 36, 36, 36, 60, 60, 60, 60, 72, 72, 90 | 3.42705 | to find |
| 11 | 6 rhombus 60, 2 hexagon 144/108/108, 2 hexagon 144/144/72, 2 square | 36, 36, 36, 60, 60, 60, 72, 72, 72, 90 | 4.23607 | to find |
| 12 | 4 rhombus 60, 2 hexagon 144/108/108, 2 hexagon 144/144/72, 2 rhombus 72, 2 square | 36, 36, 36, 60, 60, 72, 72, 72, 72, 90 | 4.42705 | to find |
| 13 | 4 rhombus 60, 4 square, 2 hexagon 144/108/108, 2 hexagon 144/144/72 | 36, 36, 36, 60, 60, 72, 72, 72, 90, 90 | 4.23607 | to find |
| 14 | 4 hexagon 144/108/108, 4 square, 2 rhombus 36, 2 rhombus 60 | 36, 36, 36, 60, 72, 72, 72, 72, 90, 90 | 4.73607 | to find |
| 15 | 4 regular hexagon, 4 rhombus 36, 4 rhombus 72 | 36, 36, 60, 60, 60, 60, 60, 60, 72, 72 | 4 | to find |
| 16 | 4 rhombus 60, 4 rhombus 72, 2 hexagon 144/144/72, 2 regular hexagon | 36, 36, 60, 60, 60, 60, 60, 72, 72, 72 | 4.61803 | built: DICTO_SKEWED_ED_16 |
| 17 | 4 rhombus 72, 2 hexagon 144/144/72, 2 regular hexagon, 2 rhombus 60, 2 square | 36, 36, 60, 60, 60, 60, 72, 72, 72, 90 | 4.92705 | to find |
| 18 | 6 rhombus 60, 4 hexagon 144/108/108, 2 rhombus 72 | 36, 36, 60, 60, 60, 72, 72, 72, 72, 72 | 4.73607 | built: DICTO_SKEWED_ED_18 |
| 19 | 4 hexagon 144/108/108, 4 rhombus 60, 4 rhombus 72 | 36, 36, 60, 60, 72, 72, 72, 72, 72, 72 | 5.23607 | to find |
| 20 | 4 hexagon 144/108/108, 4 rhombus 60, 2 rhombus 72, 2 square | 36, 36, 60, 60, 72, 72, 72, 72, 72, 90 | 5.04509 | to find |
| 21 | 4 rhombus 72, 2 hexagon 144/108/108, 2 regular hexagon, 2 rhombus 60, 2 square | 36, 60, 60, 60, 60, 72, 72, 72, 72, 90 | 5.54509 | to find |
| 22 | 4 rhombus 72, 4 square, 2 hexagon 144/108/108, 2 regular hexagon | 36, 60, 60, 60, 72, 72, 72, 72, 90, 90 | 5.8541 | to find |
| 23 | 8 rhombus 60, 4 hexagon 135/135/90 | 45, 45, 45, 45, 60, 60, 60, 60, 90, 90 | 4.82843 | built: BAIN_ED |
| 24 | 4 rhombus 45, 4 square, 2 hexagon 135/135/90, 2 regular hexagon | 45, 45, 45, 45, 60, 60, 60, 90, 90, 90 | 4.41421 | to find |
| 25 | 4 hexagon 135/135/90, 4 rhombus 60, 4 square | 45, 45, 45, 45, 60, 60, 90, 90, 90, 90 | 5.12132 | to find |
| 26 | 6 square, 4 hexagon 135/135/90, 2 rhombus 60 | 45, 45, 45, 45, 60, 90, 90, 90, 90, 90 | 5.32843 | to find |
| 27 | 4 rhombus 60, 2 hexagon 135/135/90, 2 regular hexagon, 2 rhombus 45, 2 square | 45, 45, 45, 60, 60, 60, 60, 60, 90, 90 | 4.62132 | to find |
| 28 | 4 regular hexagon, 4 rhombus 60, 4 square | 60, 60, 60, 60, 60, 60, 60, 60, 90, 90 | 5.65685 | built: REGULAR_HEX_ED |

## Truncated octahedron — sheared BCC (10)

| # | Faces | Line angles | Volume | Status |
|---|---|---|---|---|
| 1 | 4 hexagon 144/144/72, 4 regular hexagon, 4 rhombus 36, 2 square | 36, 36, 36, 36, 36, 36, 60, 60, 60, 60, 60, 60, 72, 72, 90 | 6.47214 | to find |
| 2 | 6 hexagon 144/144/72, 6 square, 2 regular hexagon | 36, 36, 36, 36, 36, 36, 60, 60, 60, 72, 72, 72, 90, 90, 90 | 6.59017 | to find |
| 3 | 4 hexagon 144/108/108, 4 hexagon 144/144/72, 4 rhombus 60, 2 square | 36, 36, 36, 36, 36, 36, 60, 60, 72, 72, 72, 72, 72, 72, 90 | 8.47214 | to find |
| 4 | 4 hexagon 144/144/72, 4 rhombus 60, 2 hexagon 144/108/108, 2 regular hexagon, 2 square | 36, 36, 36, 36, 36, 60, 60, 60, 60, 60, 72, 72, 72, 72, 90 | 8.3541 | to find |
| 5 | 4 hexagon 144/108/108, 4 rhombus 60, 2 hexagon 144/144/72, 2 regular hexagon, 2 square | 36, 36, 36, 36, 60, 60, 60, 60, 60, 72, 72, 72, 72, 72, 90 | 8.3541 | to find |
| 6 | 6 hexagon 144/108/108, 6 square, 2 regular hexagon | 36, 36, 36, 60, 60, 60, 72, 72, 72, 72, 72, 72, 90, 90, 90 | 10.5902 | to find |
| 7 | 4 hexagon 144/108/108, 4 regular hexagon, 4 rhombus 72, 2 square | 36, 36, 60, 60, 60, 60, 60, 60, 72, 72, 72, 72, 72, 72, 90 | 10.4721 | to find |
| 8 | 6 hexagon 135/135/90, 6 square, 2 regular hexagon | 45, 45, 45, 45, 45, 45, 60, 60, 60, 90, 90, 90, 90, 90, 90 | 9.74264 | to find |
| 9 | 4 hexagon 135/135/90, 4 regular hexagon, 4 rhombus 60, 2 square | 45, 45, 45, 45, 60, 60, 60, 60, 60, 60, 60, 60, 90, 90, 90 | 9.65685 | to find |
| 10 | 8 regular hexagon, 6 square | 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 90, 90, 90 | 11.3137 | built: TRUNCATED_OCTAHEDRON |

## The earlier list

`enumerate.py` (output `targets.json`) counted the 70 equal-edge cells whose directions all come from one fixed set of 15 directions with mutual angles 36°, 60°, 72° and 90°. All 70 are in the list above.

## Other quantified targets

- **4D parallelohedra:** 52 combinatorial types (Delone; Štogrin), the 4D counterpart of Fedorov's five.
- **Natural-cell events:** in Kaleidohedra's natural-cell mode, the exact slider values where a lattice's own cell changes type (truncated octahedron → rhombic dodecahedron → elongated dodecahedron → hexagonal prism → cube) are export points to find.
