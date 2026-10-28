# Pressure and the stacking variants (DICTO queue item 2, 10-28)
Status 10-28: first-order estimate done (pressure.py, pressure.json). Conclusion: the volume term predicts the right direction for SiC
(pressure favours 3C, as experiments find); for Si it tilts toward the hexagonal-type stackings, and there the volume couplings beyond
the nearest (absent in the law's ideal form) do much of the work.

Method: enthalpy E + PV per atom pair; in the ANNNI expansion (Keller et al. convention) the volume couplings J^V add P J^V to the
energy couplings (1 GPa A^3 = 6.24 meV). If the volume were exactly linear in hexagonality (the Hexagonality Law's form, #66, #68),
pressure would shift only the nearest term J1: the balance cubic vs hexagonal, not the order among 4H, 6H, 15R. First-order: couplings
and volumes at P = 0 (no compression of the couplings themselves).
Data: SiC energies (vdW-corrected) 2H 15, 4H 2.7, 6H 1.3 meV/pair above 3C, volumes from the same set (Kawanishi and Mizoguchi 2015);
Si, Ge energies and volumes PBEsol (Keller et al. 2023).
Results:
- SiC: volume couplings 78% nearest (close to the law's form); volume rises with hexagonality, so pressure ADDS to the stability of 3C
  against 6H (+0.13 meV/pair per GPa), 4H (+0.11) and 2H (+0.17). Experiments: 3C becomes more stable with pressure; 6H turns into
  3C above about 4.5 GPa at 2500 C (Sugiyama and Togaya 2001; review, Daviau and Lee 2018). Direction agrees.
- Si: volume couplings only 39% nearest; volume falls with hexagonality; first-order the 3C margin over 6H closes near 8 GPa, over 4H
  near 14 GPa (but Si turns to beta-tin near 11 GPa, so this is not a prediction of a phase; it says pressure tilts Si toward hexagonal-type
  order, mainly through J2). Ge: margins close only at 24-50 GPa, beyond its beta-tin transition (~10 GPa): pressure tilts, never reorders.
Caveats: first order only; real compression changes the couplings; the law is ideal geometry. Section candidate with #68.
Sources: Kawanishi-Mizoguchi arXiv 1512.04626 (energies p. 5, Table I); Keller et al. arXiv 2302.10822 (Tables I, II); web summaries:
Sugiyama & Togaya 2001 (Hokkaido pdf), Daviau & Lee 2018 review (Yale pdf), Karch et al. PRB 1996, Maitani et al. 2024.
