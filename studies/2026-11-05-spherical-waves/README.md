# Spherical-wave imaging (DICTO 5 Nov 2026)
DICTO: "spherical wave patterns to help with imaging and reveal or close gaps"; first test on the cut-OG pyrochlore cell; "another tool alongside harmonics".
Method: every point of solid sends out j0(kr) = sin(kr)/(kr); field = solid * j0 on one periodic cubic cell (8 regular-triangle cut OGs, diamond network), FFT, grid 96^3.
Result (float): solid fraction 0.3772 (expected 0.3771). Dark = field below its median:
- wavelength a/2 (the network's own, a = cell side 12.369): dark covers 0.803 of the gaps and 0.000 of the solid -> the dark half lies wholly in gaps.
- a/4: 0.607 of gaps, 0.323 of solid; a/8: 0.567 / 0.389 (short waves ripple inside the solid).
Figures: wave-slices.png (labelled), wave-clean.png (DICTO: dataless simplified version). Scripts: wave_image.py, wave_slice.py, wave_clean.py.
Next: "close" = grow solid where the field is darkest (adaptor seeds); test on packings with unknown gaps.

## Unknown gaps: densest lattice packing of the cut OG (wave_lattice.py, wave_lattice_views.py; float; grids 48 and 72 agree)
Density 0.776244 (solid fraction on grid 0.7762). Wavelength = nearest-neighbour distance 1.2571: of the darkest 22.4% of space, 62.6% is gap
(0.8x: 66.6%; 1.25x: 61.8%) — weaker than the open pyrochlore cell (dense packing, thin gaps).
Critical points of the wave field per cell (read as in electron density): 1 atom, 5 bonds, 5 rings, 1 cage; Morse sum 1 − 5 + 5 − 1 = 0.
- One gap ROOM per copy (cage at fractional (1, ½, ½)); four window points per cell in the gap → each room opens through 8 windows: the gap is one connected network of rooms.
- 12 contacts per copy = 6 pairs: 5 read as bonds; the 6th pair (lattice direction b1 + b3) reads as a ring point inside the pieces — probably the 2 triangle-to-triangle contacts (to check).
Views inside the cell through the room: lattice-views.png.
