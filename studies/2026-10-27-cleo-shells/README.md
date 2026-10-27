# Cleo Shells (placeholder name) — study (DICTO 2026-10-27: "we have to do a shells study")

**Status: stage 0 (plan + first exact values).** Started 2026-10-27 from the White Queen study
(2026-10-27-white-queen-600: cleo_shells.py, data/cleo_shells.json, renders/cleo-shells.png).

**Known (exact):** the 600 cells of the 600-cell, grouped by the height of their centres along one vertex v, form 15 shells
of 20, 20, 30, 60, 60, 60, 20, 60, 20, 60, 60, 60, 30, 20, 20; each shell is one kind of piece in the perspective view from
just beyond the opposite vertex; the core is 20 Cleo-Icos filling a regular icosahedron.

## Values of each shell (exact; angle = 4D angle between v and the cell centres)
| shell | cells | running total | cos² of angle | angle |
|---|---|---|---|---|
| 0 (Cleo core) | 20 | 20 | 7/16 + 3√5/16 | 22.2388° |
| 1 | 20 | 40 | 5/8 | 37.7612° |
| 2 | 30 | 70 | 1/2 | 45° |
| 3 | 60 | 130 | 3/16 + √5/16 | 55.1059° |
| 4 | 60 | 190 | 1/8 | 69.2952° |
| 5 | 60 | 250 | 3/16 − √5/16 | 77.3786° |
| 6 | 20 | 270 | 7/16 − 3√5/16 | 82.2388° |
| 7 (equator) | 60 | 330 | 0 | 90° |
| 8–14 | mirror of 6–0 | 600 | same | 180° − angle |
Cell centres lie at radius² 7/4 + 3√5/4 (vertices at 4). Shell k and shell 14 − k are mirror images (angles add to 180°).

## Plan
1. For each shell: the piece itself (its six edge lengths, angles, volume) in the eye-independent 4D form and in the
   perspective view; how each shell sits on the one inside (which faces touch).
2. Changeovers: what changes from one shell's piece to the next (14 changeovers).
3. Links: Kyushindo shells (#43), Kepler's nested shells (Mysterium Cosmographicum, 1596), the shadow halves
   (front = shells 0–6, side-on = 7, back = 8–14).
4. Prior art: layer counts of the 600-cell round a vertex (Coxeter, Regular Polytopes; Wikipedia "600-cell"), Sadoc–Mosseri.
