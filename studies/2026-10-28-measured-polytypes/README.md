# Measured polytypes and the Hexagonality Law (DICTO 10-28)
Status 10-28: SiC done (sic_linear.py, sic_linear.json). Conclusion: the computed volumes per Si-C pair of 2H, 4H, 15R, 6H and 3C
lie on a straight line in the hexagonality to within the rounding of the published numbers (all three DFT sets); the measured values
scatter between sources by more than the whole effect, so they neither confirm nor refute the line.

Data: S. Kawanishi and T. Mizoguchi, "Effect of van der Waals interactions on the stability of SiC polytypes", arXiv 1512.04626,
Table I: experimental a and c/p (Schulz-Thiemann 1979; Wyckoff 1963; Stockmeier et al. 2009; Tairov-Tsvetkov; Gomes de Mesquita 1967;
Landolt-Boernstein 1982) and their GGA, LDA and GGA(vdW) values. Volume per pair V = (sqrt3/2) a^2 (c/p).

Results (A^3 per Si-C pair; rounding of a and c/p to 0.001 A gives ~0.011):
- GGA:      V = 21.0037 - 0.0125 h, max |residual| 0.0077
- LDA:      V = 20.3164 + 0.0000 h, max |residual| 0.0112
- GGA(vdW): V = 20.6341 + 0.0568 h, max |residual| 0.0076
- Exp. (8 values, 6 sources): V = 20.676 + 0.011 h, max |residual| 0.130 (one 4H value); scatter between sources >> the h effect
- a and c/p separately are linear too (DFT): c/p rises with h (+0.008 to +0.015 A), a falls (-0.005 to -0.006 A), residuals <= 0.0009.
The whole change from cubic to hexagonal is below 0.3% of the volume. Physics note: linear in h = no pair terms between layers for
this quantity (Heine's ANNNI picture); the law (#66) is the exact geometric statement of that form for the weighted pieces.
Not a claim that the law explains SiC: the real crystal relaxes, the law is ideal geometry.
