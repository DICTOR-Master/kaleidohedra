# Spherical-wave imaging (DICTO 5 Nov 2026)
DICTO: "spherical wave patterns to help with imaging and reveal or close gaps"; first test on the cut-OG pyrochlore cell; "another tool alongside harmonics".
Method: every point of solid sends out j0(kr) = sin(kr)/(kr); field = solid * j0 on one periodic cubic cell (8 regular-triangle cut OGs, diamond network), FFT, grid 96^3.
Result (float): solid fraction 0.3772 (expected 0.3771). Dark = field below its median:
- wavelength a/2 (the network's own, a = cell side 12.369): dark covers 0.803 of the gaps and 0.000 of the solid -> the dark half lies wholly in gaps.
- a/4: 0.607 of gaps, 0.323 of solid; a/8: 0.567 / 0.389 (short waves ripple inside the solid).
Figures: wave-slices.png (labelled), wave-clean.png (DICTO: dataless simplified version). Scripts: wave_image.py, wave_slice.py, wave_clean.py.
Next: "close" = grow solid where the field is darkest (adaptor seeds); test on packings with unknown gaps.
