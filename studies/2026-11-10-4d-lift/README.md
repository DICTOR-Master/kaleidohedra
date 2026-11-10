# The 4D lift of #61's cells (10 Nov 2026; DICTO: "the corners [of the chamber map] sound familiar with shapes ... from 4th dimension";
"yes run the 4D lift test / run in parallel")
Exact fact behind it: a power diagram is the slice x4 = 0 of the ordinary Voronoi diagram of the lifted sites (p, √(C − w)); λ = how
far the tetrahedral holes are lifted into the 4th dimension relative to the octahedral ones. The lifting heights are linear in (s, λ),
so the #61 chamber map is a flat 2D slice of the secondary fan (GKZ), the cell network of a higher-dimensional polytope.
TEST 1 (scripts/lift4d.py, data-lift4d.json): a two-height lift gives open-ended 4D cells (no polytope possible) - replaced by a
PERIODIC lift: octahedral holes at x4 in T·Z, tetrahedral at t + T·Z (each 3D slice is one of our power diagrams). Scan: words ABC, AC;
s = 1/8 … 1; T = 0.4 … 3.0 (27); t/T = 0.05 … 0.5 (10): 4860 lifts, ALL 36 450 cells closed and computed (FINAL ok; a first run left 6 913 cells open at large T - NaN - and was caught by the FINAL check: fixed by always including the home sites one period up and down). NO cell is a regular 4D polytope (5-cell,
16-cell, tesseract, 24-cell); the "most regular" are many-vertex cells at the scan edge (T = 3). Caveat: the facet counter splits facets
(rounding), so facet counts are rough; vertex counts and radius spread alone exclude the regular polytopes. NEGATIVE.
TEST 2: corners (s = 1/4, 1/7; λ = −9/32, −5/32, −9/56; slopes 9/8, 5/8, 1/8, 3/8) against the event heights of the 4D studies
(4d-shadows, 4d-sections, 600cell-slices, yantra-4d, harmonic-4d): no match; near numbers 0.157 (600-cell Q4-silent slice) ~ 5/32 and
0.277 (600-cell Q12) ~ 9/32 are different quantities in different units: coincidences. NEGATIVE.
What stands: the exact slice/shadow relations (power diagram = slice of a 4D Voronoi diagram; chamber map = slice of the secondary fan).
LEADS: the secondary-fan reading made concrete - name each #61 wall's flip (which holes gain/lose a shared face); the exact D4 picture
(atoms + holes of close packing as slices of D4 / the 24-cell honeycomb) needs the atoms as sites too.
