# Perovskites and battery cathodes: Pauling's third rule made exact (DICTO 10-28) — QUEUED, next study
Starting point: #71 Theorem: face-sharing octahedral pairs per close-packed atom = h (any stacking).
1. Hexagonal perovskites ABX3: close-packed AX3 layers, B in the X6 octahedra; face-sharing octahedra at the hexagonal layers
   (2H BaNiO3 all face-sharing; 4H, 6H BaTiO3, 9R, 12R...). Law: shares of corner- vs face-sharing octahedra linear in h; compare with
   Goldschmidt's tolerance factor; data: published lattice volumes / energies per polytype (library + literature).
2. Layered oxide cathodes: oxygen close-packed layers, Li and transition metal in octahedra. O3 (cubic, LiCoO2), O2 / O1 (hexagonal),
   H1-3 in Ni-rich NMC at high charge. Law: face-sharing Li-M octahedra per oxygen layer vs h; stacking changes during charge.
Method: exact counts with explicit coordinates (as hydrogen_sites.py), literature data, prior art first (Katz and Ward 1964 on
hexagonal perovskite stacking; Delmas' O3/P2 notation). Sources checked to be listed.

## Progress 10-28: 1. BaRuO3 (baruo3.py, baruo3.out) — DONE
Sources read: Jin et al., PNAS 105, 7115 (2008) (PMC2438213: Table 1 cubic a = 4.0059 A; interfaces CFFCFFCFF / CFCF / FCCFCC / CCC;
synthesis 4H 3 GPa, 6H 5 GPa, 3C 18 GPa); Cava et al. review arXiv 2006.05864 (pp. 1-3: notation (chh)3 = 9R; Ba1-xSrxRuO3 9R -> 4H -> 3C
at x ~ 1/6, 1/3, Donohue, Katz and Ward 1966); arXiv 2107.07165 (4H, 9R cells as quoted). 6H cell second-hand (Longo 1968, c ~ 14 A).
Results: face-sharing share = h exactly (2/3, 1/2, 1/3, 0) = #71 Theorem (ii) applied to the BaO3 stacking. Volume per BaRuO3 on the
law line V = 64.25 + 6.82 h within 0.06-0.22% for 3C, 4H, 9R; 6H 1% low but its c is two-figure (c = 14.14 A would put it on the line).
Volume rises with h, so by #70's Proposition pressure lowers h at first order: the observed sequence 9R -> 4H -> 6H -> 3C runs down h.
Not law-shaped: the face-sharing cluster sizes (dimers, trimers, chains = runs of h layers), which drive the magnetism Jin et al. report.
CONCLUSION: the tolerance-factor rule (t > 1 -> hexagonal) becomes quantitative: pair counts and volume linear in h; pressure and
smaller A-site cations walk h down.

## 2. Cathodes — counts DONE (geometry), data next
Layered LiMO2: oxygen close-packed layers, Li and M in alternate octahedral interlayers. By #71 Theorem (ii) a Li octahedron shares a
face with an M octahedron across each hexagonal oxygen layer: face-sharing Li-M pairs per Li = 2h (2 oxygen layers per LiMO2).
O3 (LiCoO2, h = 0): 0, edges only; O2 (h = 1/2): 1 (face on one side); O1 (h = 1, CdI2-like): 2; H1-3 (O3/O1 hybrid, h = 1/2): 1.
Next: published c-axis / volume data along charge (LiCoO2 O3 -> H1-3 -> O1; Ni-rich NMC H2 -> H3) against h; prior art Delmas 1980.
