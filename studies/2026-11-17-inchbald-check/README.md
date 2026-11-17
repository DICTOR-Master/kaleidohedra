# Inchbald's dimpled triacontahedron and the k = 10 solids (17 November 2026)

**Question (DICTO):** is Inchbald's dimpled rhombic triacontahedron one of the GET solids, and does it really tile?

**Source.** G. Inchbald, "A 3-D Quasicrystal Structure?", steelpillow.com, section "Tilings and the dimpled rhombic
triacontahedron" (page updated 6 Dec 2024; the dimpling text is first in the Wayback snapshot of 23 Mar 2023, absent on
31 Mar 2022): the rhombic triacontahedron with four of its eight cube-corner triplets of faces dimpled, alternating with
tetrahedral symmetry, is a space-filler with cubic periodicity.

## 1. Which solid it is (exact)

`scripts/inchbald.py` builds T in the Z^6 face form of study 2026-11-15-grunbaum-k10 and indents its four even cube-corner
3-valent corners (the odd four give its mirror image). Result: 30 faces, a sphere, 12 symmetries (the tetrahedral
rotations). Compared exactly with the three depth-4 solids of `search6.json` under all 120 symmetries and translation:

| solid | symmetries | congruent to Inchbald's |
|---|---|---|
| candidate 0 = GET A | 4 | no |
| candidate 1 = GET B | 3 | no |
| candidate 2 | 12 | **yes** |

So Inchbald's solid is candidate 2. GET A and GET B are different solids of the same family (four corner indentations of T).

## 2. Can it be cut into golden rhombohedra? (exact)

Its four scooped-out corner cells are oblate golden rhombohedra, pairwise disjoint. `scripts/lifts.py` (120 regular
tilings of T) and `scripts/flips.py` (160 tilings of T reached by flips from a regular one, each checked exactly) find no
tiling of T that holds all four: at most three (counts by how many they hold: 0: 4, 1: 92, 2: 60, 3: 4). This is why
the 2026-11-15 study could not certify it with a cell decomposition. (Flip-connectivity of the tilings of T is not proved
here, so "no tiling at all" is not claimed.)

## 3. Does it tile? (floating point, not exact)

`scripts/overlap_float.py` (scipy, run in a venv on the compute host): the solid as 17 cells of a tiling of T that holds
three of the corners, minus the fourth corner cell. Its own face-pair lattice has rank 3, basis
(1,0,0,−1,0,−1), (0,−1,0,1,1,0), (0,0,1,1,1,1).
- volume 71.777087640 = covolume 71.777087640 (exactly 20 + 32φ in the study's exact check);
- overlap volume with each of the 136 lattice translates within 2R: at most 9·10⁻¹⁶.

So it tiles by translation, face to face lattice, to floating-point accuracy, as Inchbald says. Not exact: an exact
certificate needs either a cell decomposition (none found) or exact intersection volumes.

## Conclusion

Inchbald's solid answers Grünbaum's k = 10 question too (every zone 10 faces; tiling float-checked), published 2022–23,
before GET; he does not mention zones or Grünbaum. It is a third k = 10 example besides GET A and GET B, and the most
symmetric. Credit: "the dimpled rhombic triacontahedron (Inchbald, 2023)". GET A and GET B are not his.

**Update 17 Nov 2026 (study 2026-11-17-get-mixing):** the tiling is now PROVED exactly: the solid written as 17 cells minus one corner cell, overlap volumes computed exactly in Q(phi) with each of its 14 lattice translates within reach are exactly 0, and volume = covolume = 20 + 32phi.
