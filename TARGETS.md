# Kaleidoverse target list

*Kaleidoverse by DICTO — private working notes.*

The first quantified set of space-filling variants to find: every **equal-edge zonohedral parallelohedron** whose edge directions are among the 15 two-fold axes of icosahedral symmetry (the directions DICTO's first shapes came from). They are counted **exactly, up to congruence**. Two equal-edge zonohedra are congruent exactly when their direction sets have the same angles up to sign and order, and these solids are centrally symmetric, so mirror images count once (`enumerate.py`, output `targets.json`).

This is a starting catalogue, not a boundary: Kaleidoverse's sliders reach every shear, and new targets will come from there too.

| Type (Fedorov) | Tiles as | Count | Built |
|---|---|---|---|
| parallelepiped (cube type) | sheared simple-cubic | 11 | 4 |
| hexagonal prism | sheared hexagonal | 15 | 1 |
| rhombic dodecahedron | sheared FCC | 15 | 1 |
| elongated dodecahedron | sheared ED lattice | 22 | 0 |
| truncated octahedron | sheared BCC | 7 | 0 |
| **total** | | **70** | **6** |

Volumes are exact at edge 1. **Line angles** are the angles between the edge directions (as lines), one per pair of directions. Four pairs of shapes share the same line angles but differ in volume: their edges meet at 60° in one and 120° in the other, so the volume tells them apart.

## Parallelepiped (cube type) — sheared simple-cubic

| # | Directions | Line angles | Volume | Status |
|---|---|---|---|---|
| 1 | 3 | 36, 36, 36 | (-1+φ)/2 | to find |
| 2 | 3 | 36, 36, 60 | (-1+φ)/2 | to find |
| 3 | 3 | 36, 60, 60 | 1/2 | to find |
| 4 | 3 | 36, 60, 72 | 1/2 | to find |
| 5 | 3 | 36, 60, 90 | (-1+φ)/2 | to find |
| 6 | 3 | 36, 72, 90 | 1/2 | to find |
| 7 | 3 | 60, 60, 72 | 1/2 | **DICTO flattened rhombohedron** (P; R DICTO Blocks) |
| 8 | 3 | 60, 72, 72 | φ/2 | **DICTO all-rhombus block** (P; R DICTO Blocks) |
| 9 | 3 | 60, 72, 90 | φ/2 | **DICTO square-faced block** (P) |
| 10 | 3 | 72, 72, 72 | φ/2 | to find |
| 11 | 3 | 90, 90, 90 | 1 | cube (P, R) |

## Hexagonal prism — sheared hexagonal

| # | Directions | Line angles | Volume | Status |
|---|---|---|---|---|
| 1 | 4 | 36, 36, 36, 36, 60, 72 | (-1+2φ)/2 | to find |
| 2 | 4 | 36, 36, 36, 60, 72, 90 | (-1+2φ)/2 | to find |
| 3 | 4 | 36, 36, 36, 72, 72, 90 | (1+φ)/2 | to find |
| 4 | 4 | 36, 36, 60, 60, 60, 90 | (-3+3φ)/2 | to find |
| 5 | 4 | 36, 36, 60, 60, 72, 72 | (2+φ)/2 | to find |
| 6 | 4 | 36, 36, 60, 60, 72, 72 | (1+φ)/2 | to find |
| 7 | 4 | 36, 36, 60, 60, 72, 90 | (-1+2φ)/2 | to find |
| 8 | 4 | 36, 36, 60, 72, 72, 90 | (1+φ)/2 | to find |
| 9 | 4 | 36, 36, 60, 72, 72, 90 | (2+φ)/2 | to find |
| 10 | 4 | 36, 36, 72, 72, 72, 90 | (2+φ)/2 | to find |
| 11 | 4 | 36, 60, 60, 60, 60, 72 | 3/2 | to find |
| 12 | 4 | 36, 60, 60, 72, 72, 90 | (1+2φ)/2 | to find |
| 13 | 4 | 36, 60, 72, 72, 72, 72 | (1+2φ)/2 | to find |
| 14 | 4 | 36, 60, 72, 72, 72, 90 | (1+2φ)/2 | to find |
| 15 | 4 | 60, 60, 60, 72, 72, 90 | 3φ/2 | **DICTO leaning hexagonal prism** (P Parallelohedra) |

## Rhombic dodecahedron — sheared FCC

| # | Directions | Line angles | Volume | Status |
|---|---|---|---|---|
| 1 | 4 | 36, 36, 36, 60, 60, 60 | φ | to find |
| 2 | 4 | 36, 36, 36, 60, 60, 90 | (-2+3φ)/2 | to find |
| 3 | 4 | 36, 36, 60, 60, 72, 72 | 2 | to find |
| 4 | 4 | 36, 36, 60, 60, 72, 90 | (2+φ)/2 | to find |
| 5 | 4 | 36, 36, 60, 60, 72, 90 | (-1+3φ)/2 | to find |
| 6 | 4 | 36, 36, 60, 72, 72, 90 | (1+2φ)/2 | to find |
| 7 | 4 | 36, 36, 60, 72, 90, 90 | φ | to find |
| 8 | 4 | 36, 60, 60, 60, 72, 90 | (1+2φ)/2 | to find |
| 9 | 4 | 36, 60, 60, 72, 72, 90 | (3+φ)/2 | to find |
| 10 | 4 | 36, 60, 60, 72, 72, 90 | 3φ/2 | to find |
| 11 | 4 | 36, 60, 60, 72, 90, 90 | -1+2φ | to find |
| 12 | 4 | 36, 60, 72, 72, 90, 90 | 1+φ | to find |
| 13 | 4 | 36, 60, 72, 90, 90, 90 | 1+φ | to find |
| 14 | 4 | 60, 60, 60, 72, 72, 72 | 1+φ | **DICTO skewed RD** (P Parallelohedra + 3D+ Bridges; R DICTO FCC world) |
| 15 | 4 | 60, 60, 72, 72, 72, 90 | (1+3φ)/2 | to find |

## Elongated dodecahedron — sheared ED lattice

| # | Directions | Line angles | Volume | Status |
|---|---|---|---|---|
| 1 | 5 | 36, 36, 36, 36, 36, 36, 60, 60, 72, 72 | 2φ | to find |
| 2 | 5 | 36, 36, 36, 36, 36, 60, 60, 60, 72, 72 | (1+4φ)/2 | to find |
| 3 | 5 | 36, 36, 36, 36, 36, 60, 60, 72, 72, 90 | (-1+5φ)/2 | to find |
| 4 | 5 | 36, 36, 36, 36, 60, 60, 60, 60, 72, 90 | (-2+5φ)/2 | to find |
| 5 | 5 | 36, 36, 36, 36, 60, 60, 60, 72, 90, 90 | -2+3φ | to find |
| 6 | 5 | 36, 36, 36, 36, 60, 60, 72, 72, 72, 90 | (3+3φ)/2 | to find |
| 7 | 5 | 36, 36, 36, 36, 60, 72, 72, 72, 72, 90 | 1+2φ | to find |
| 8 | 5 | 36, 36, 36, 36, 60, 72, 72, 72, 90, 90 | (1+4φ)/2 | to find |
| 9 | 5 | 36, 36, 36, 60, 60, 60, 60, 60, 72, 72 | 2+φ | to find |
| 10 | 5 | 36, 36, 36, 60, 60, 60, 60, 72, 72, 90 | (2+3φ)/2 | to find |
| 11 | 5 | 36, 36, 36, 60, 60, 60, 72, 72, 72, 90 | 1+2φ | to find |
| 12 | 5 | 36, 36, 36, 60, 60, 72, 72, 72, 72, 90 | (4+3φ)/2 | to find |
| 13 | 5 | 36, 36, 36, 60, 60, 72, 72, 72, 90, 90 | 1+2φ | to find |
| 14 | 5 | 36, 36, 36, 60, 72, 72, 72, 72, 90, 90 | (3+4φ)/2 | to find |
| 15 | 5 | 36, 36, 60, 60, 60, 60, 60, 60, 72, 72 | 4 | to find |
| 16 | 5 | 36, 36, 60, 60, 60, 60, 60, 72, 72, 72 | 3+φ | to find |
| 17 | 5 | 36, 36, 60, 60, 60, 60, 72, 72, 72, 90 | (5+3φ)/2 | to find |
| 18 | 5 | 36, 36, 60, 60, 60, 72, 72, 72, 72, 72 | (3+4φ)/2 | to find |
| 19 | 5 | 36, 36, 60, 60, 72, 72, 72, 72, 72, 72 | 2+2φ | to find |
| 20 | 5 | 36, 36, 60, 60, 72, 72, 72, 72, 72, 90 | (2+5φ)/2 | to find |
| 21 | 5 | 36, 60, 60, 60, 60, 72, 72, 72, 72, 90 | (3+5φ)/2 | to find |
| 22 | 5 | 36, 60, 60, 60, 72, 72, 72, 72, 90, 90 | 1+3φ | to find |

## Truncated octahedron — sheared BCC

| # | Directions | Line angles | Volume | Status |
|---|---|---|---|---|
| 1 | 6 | 36, 36, 36, 36, 36, 36, 60, 60, 60, 60, 60, 60, 72, 72, 90 | 4φ | to find |
| 2 | 6 | 36, 36, 36, 36, 36, 36, 60, 60, 60, 72, 72, 72, 90, 90, 90 | (-3+10φ)/2 | to find |
| 3 | 6 | 36, 36, 36, 36, 36, 36, 60, 60, 72, 72, 72, 72, 72, 72, 90 | 2+4φ | to find |
| 4 | 6 | 36, 36, 36, 36, 36, 60, 60, 60, 60, 60, 72, 72, 72, 72, 90 | (7+6φ)/2 | to find |
| 5 | 6 | 36, 36, 36, 36, 60, 60, 60, 60, 60, 72, 72, 72, 72, 72, 90 | (7+6φ)/2 | to find |
| 6 | 6 | 36, 36, 36, 60, 60, 60, 72, 72, 72, 72, 72, 72, 90, 90, 90 | (5+10φ)/2 | to find |
| 7 | 6 | 36, 36, 60, 60, 60, 60, 60, 60, 72, 72, 72, 72, 72, 72, 90 | 4+4φ | to find |

## Other quantified targets

- **4D parallelohedra:** 52 combinatorial types (Delone; Štogrin), the 4D counterpart of Fedorov's five.
- **Natural-cell events:** in Kaleidoverse's natural-cell mode, the exact slider values where a lattice's own cell changes type (truncated octahedron → rhombic dodecahedron → elongated dodecahedron → hexagonal prism → cube) are export points to find.
