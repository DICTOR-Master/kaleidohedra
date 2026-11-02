# DICTO solids as sections of the regular 4D polytopes (study, 3 Nov 2026)

One-line conclusion: of the 69 dataset solids, besides those DICTO took from the 600-cell and 120-cell atlases (#63, #65), four more are exact
sections of a regular 4D polytope in a main direction: Icosaxes (24-cell cell-first t = 1/φ², and 120-cell vertex-first at φ/2 of the way to the
corner), Unborn Axes (24-cell cell-first t = 1/φ), TI Star core (120-cell cell-first t = 3(√5 − 2)) and Cube Pearl (24-cell corner-first,
height 1/3 = 1/6 of the way to the tip, corners (±1,±1,0,0)); Delilah is every corner-first section of the 16-cell. Status: Icosaxes, Unborn
Axes, TI Star core, White Knight published in #88; Cube Pearl not yet published (exact cut compared in floating point to 1e-12; an exact
congruence check in Q(√2) is still to do). Golden Clasp, GTI, OG and the rest: not found in the four main directions (2,400 heights each).

Scripts: slices4d.py (the search, float), slice24.py, exact_cmp.py, tisc_check.py, two_checks.py (Icosaxes in the 120-cell; Cube Pearl in the
24-cell), wk_check.py. Data: slices4d.md (the 15 matches). Next: exact Cube Pearl check; then decide where it is published (a note in the
weekly batch, or a section of a future paper on DICTO solids as 4D sections).
