# Kaleidoverse plan

*Kept as simple and easy to operate as possible (DICTO, 2026-10-01).*

## The one control

**One slider** moves the lattice along a straight path from the ordinary lattice
through DICTO's shear and beyond. Every point on it is an exact space-filling
tiling (a linear image of the lattice), and all geometry moves with it.

| Slider | Stop |
|---|---|
| 0 | FCC (the ordinary rhombic dodecahedron packing) |
| 1 | halfway stop |
| 2 | **DICTO FCC** (DICTO's skewed RD, volume φ² at edge 1) |
| ≈ 6.8 | wall: the cells flatten to zero volume (the slider stops just before) |
| negative | the opposite shear, which never collapses |

The stops live in one small table in the code, so they can be moved, renamed or
added to later. In matrix terms: A(s) = (1 − s/2)·I + (s/2)·M, where M is DICTO's
shear (Rhombiverse `dicto-fcc.js`).

| Slider | Cell volume vs FCC |
|---|---|
| −2 | 1.08 |
| 1 | 0.94 |
| 2 | 0.85 |
| 4 | 0.60 |
| 6 | 0.21 |

## Other sliders: one slider, many paths

A lattice's shape (ignoring turning and resizing) has 5 independent
directions of change. Kaleidoverse keeps **one slider** and adds a small
**"towards…" picker** that chooses its destination: DICTO FCC first, then any
target from `TARGETS.md` (such as the 14 other RD-type cells, all sheared
FCCs). Each target gives its own straight path from the start lattice, with
its own stops and wall. Later, a hidden **advanced panel** gives full freedom
(five sliders, or the six lattice parameters).

## Population members

At any slider value, **Export** saves a named member: the slider value, the
matrix and the cell. Members go to Rhombiverse (as a lattice world, like DICTO
FCC) or Polyhedraverse (as pieces, like the skewed RD and its blocks). Each
export carries a check that it tiles.

## Build order

1. Engine: fork Rhombiverse's 3D engine (FCC world, lattice view, saving) into
   this private repo; apply A(s) as a scene transform, so building stays exactly
   as in Rhombiverse.
2. The slider with its stops, and the wall; the "towards…" picker (DICTO FCC first, then the TARGETS.md cells).
3. Export of members.
4. More starting lattices (BCC, simple cubic, hexagonal, ED) on the same
   slider idea; then 2D; 4D later.
5. Later: the hidden advanced panel (full freedom), a "natural cell" mode showing where the lattice's own cell changes
   type, and the targets in `TARGETS.md` as stops to find.
