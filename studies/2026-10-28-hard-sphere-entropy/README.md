# Hard-sphere stacking entropy and the Hexagonality Law (DICTO queue item 1, 10-28)
Status 10-28: literature comparison done. Conclusion: at close packing the stacking entropy of hard spheres is mostly of the law's
form (a field term only, linear in hexagonality); the departures grow toward melting.

Read: S.-C. Mau and D. A. Huse, Stacking entropy of hard-sphere crystals, Phys. Rev. E 59, 4396 (1999), arXiv cond-mat/9810287
(15 pp); V. Elser, Phonon contribution to the entropy of hard-sphere crystals (2014), arXiv 1403.1784 (6 pp). Both in the library.
- Mau-Huse write the stacking entropy per sphere as an Ising chain in the LAYER TYPES (c/h = sigma_i): a field h (one layer type,
  i.e. three consecutive layers), a coupling J between neighbouring layer types (four layers), and h', J' (five layers).
  Values (units 1e-5 kB per sphere): close packing (h, J) = (55, 6); near melting (h, J, h') = (37, 18, 9). All favour fcc.
  fcc - hcp entropy difference 0.00115 kB per sphere at close packing (Elser 2014: 0.001164(8)).
- The Hexagonality Law (#66) is exactly the field-only case for the weighted piece volumes: J = h' = J' = 0, total linear in
  hexagonality. In Mau-Huse's numbers the stacking ENTROPY is field-dominated at close packing (J/h = 6/55 = 0.11) and much less so
  near melting (J/h = 0.49, plus h'). So near close packing the entropy is ~90% of the law's form; the rest grows as the spheres rattle.
- Elser: in the single-cage (free-volume) approximation the fcc-hcp entropy difference is exactly zero (Stillinger et al.); the
  difference is mostly collective (phonon) entropy. Consistent: our law concerns the geometry of fixed sites; entropy differences come
  from collective motion, whose stacking dependence is mostly local (field-like) at close packing.
Possible paper section: "Stacking entropy against the law" with this table; no new computation needed. Caveat: entropy is not volume;
we compare the FORM (field-only vs couplings), not the quantity.
