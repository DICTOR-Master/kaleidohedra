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

## Progress 10-28: 2. Cathodes, LiCoO2 data — DONE (cathodes.py, cathodes.out)
Exact counts from the oxygen letters: O3 h 0, per-gap face pairs [0]; O1 h 1, [2]; O2 h 1/2, [1,1]; H1-3 h 1/2, [0,2,0,2...].
Mean per gap = 2h in all four (Theorem (ii) of #71). The split matters: O2 spreads the faces (every Li faces one Co); H1-3 packs
all faces into the O1 gaps, and those are exactly the gaps that are EMPTY (Motohashi; Van der Ven et al.): Li sits only at 0 faces.
Data (Motohashi et al., PRB 80, 165114 (2009), arXiv 0909.3556, Table I, measured, ICP Li): d per CoO2 layer O1 4.24, H1-3 4.52,
O3 x=0.35-0.50 4.81, x=1 4.68 A. Law line at h = 1/2: (4.24+4.81)/2 = 4.525 vs 4.52 measured (+0.11%).
Rule (stable phases): Li occupies only gaps with 0 face-sharing Co, so x <= 1 - h_gap, h_gap = share of O1 gaps (same shape as the
hydride bound h <= 2 - x in #71). Motohashi's stable phases all obey it (O1 x=0, H1-3 x=0.12 <= 1/2, O3 x <= 1).
Exception named: O2-LiCoO2 (Delmas, Braconnier, Hagenmuller, Mater. Res. Bull. 17, 117 (1982)) is made only by ion exchange and is
metastable; it has one face-sharing Li-Co pair per Li, and Carlier et al. (Solid State Ionics 2001) report the ions displaced away
from that common face by Li+-Co3+ repulsion. So it is an energy penalty per face pair, not a prohibition.
Ni-rich NMC H2 -> H3: both stay O3 (R-3m, c collapse with no stacking change), h = 0 throughout: the law says nothing; dropped.
Prior art: Delmas, Fouassier, Hagenmuller, Physica B 99, 81 (1980) (O/P notation); Van der Ven, Aydinol, Ceder, Kresse, Hafner,
PRB 58, 2975 (1998) (H1-3 predicted as O1/O3 hybrid); Amatucci, Tarascon, Klein, JES 143, 1114 (1996) (O1 CoO2); arXiv 2212.14667
(H1-3 = alternating O1/O3 blocks). Additivity of gallery heights in staged intercalates is long known (graphite, Daumas-Herold), so
the 4.525 match is expected; new here: the face-pair count 2h and its split, giving the Li-filling bound in the same law as #71.
Sources checked: arXiv 0909.3556 (full Table I); AFLOW prototype ABC2_hP8_186_b_b_ab-001 (O2-LiCoO2, cites Delmas 1982, Yabuuchi
et al. Inorg. Chem. 52, 9131 (2013)); web searches "LixCoO2 H1-3 O1 lattice parameters", "O2-LiCoO2 Carlier Delmas"; arXiv 2212.14667
abstract only. Not read in full: Carlier 2001, Van der Ven 1998, Chen-Lu-Dahn 2002.
CONCLUSION: cathode stacking during charge obeys the #71 count; Li fills only zero-face gaps in stable phases (x <= 1 - h_gap).
Study complete: perovskites + cathodes = material for #72 "The Hexagonality Law in Real Materials IV: Oxides" (placeholder).

## Progress 10-28: 3. BaMnO3 (bamno3.py, bamno3.out) — DONE
Chen and Millis, arXiv 1509.06650, Table II (DFT, per Mn; 2H h 1, 4H h 1/2, cubic h 0). Volume near the line: 4H 0.5% (AFM) / 1.3% (FM)
below it. Energy far off: 4H lies 278 meV/Mn (AFM) below the line; the cubic cell is strongly unstable (t > 1, Ba too big).
CONCLUSION: in BaMnO3 the volume follows the law, the energy does not (large J2-type term) -> named limit in #72.
Extra sources checked 10-28: web searches BaIrO3 polytypes (Cheng et al. JACS 131, 7461 (2009) found, cell volumes not reachable),
Carlier 2001 (Solid State Ionics 144, 263; title "On the metastable O2-type LiCoO2"; abstract server 503), Van der Ven 1998
(abstract via METU repository: staged compound, Li in every other plane), Katz and Ward (not reachable; cited via Cava review).
