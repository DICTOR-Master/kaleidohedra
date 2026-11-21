# Scutoid approximants: do real 1/1 cubic approximants realise the amber-cell geometry? (21 Nov 2026)

Study 1 of DICTO's scutoid thread. Question: an icosahedral core in a bcc mould, the resin cut by DICTO's combined method, gives true
scutoids, with all 30 Y-junctions on the core's 2-fold axes (amber-cell sweep, Y-junction study). Do the real 1/1 cubic approximants,
whose clusters sit on a bcc lattice with their 2-fold axes on the cube axes, realise this geometry at their real proportions?

## Result in five lines

1. The icosidodecahedral cluster shell of the real Tsai-type 1/1 approximants (4 structures) and Mackay-type 1/1 approximants
   (2 structures) fits its bcc Voronoi cell with room to spare: s_real/s0 = 1.124 to 1.130 (Tsai), 1.244 (Mackay).
2. At those real scales DICTO's combined method gives a valid division every time: 3 kinds, 20/32 scutoids (the 20 triangle pieces),
   30 Y vertices, all 30 exactly on the core's 2-fold axes (exact Q(sqrt5) test). Same pattern as the sweep's icosidodecahedron at 6/5 s0.
3. The outer shells do not fit: the Tsai triacontahedron (even the smallest one around the icosidodecahedron shell: s_real/s0 = 0.982)
   and the Bergman 60-atom shell (0.986): neighbouring clusters overlap there, so no amber cell at the real scale. The Bergman
   32-atom triacontahedron shell fits (1.333) but gives frustums only (0 scutoids, 0 Y), as in the sweep.
4. Real atoms between core and mould: none lies on a 2-fold axis (0 atoms within 0.3 A; random points would give 0.2 to 0.9).
   The Y vertices are 2.1 to 3.0 A from the nearest real atom, at the 74th to 91st percentile of random points in the same resin:
   the Y vertices sit in emptier than typical places, not at atoms. Only 2 independent Y positions per case (T_h orbits of 24 and 6),
   so this is a description, not a statistical finding.
5. New and relevant to the paper: with the 12 cap atoms of the real shell pair included (core = convex hull of the icosidodecahedron and
   the icosahedron on its five-fold axes, exactly icosahedral), the division is valid (60/80 scutoids), but only 6 of the 30 Y lie on
   2-fold axes; 24 are off by 7.1e-4 to 1.9e-3 core units (0.0025 to 0.0054 A). So "bcc mould + icosahedral core => all Y on 2-fold axes"
   is NOT true for every icosahedral core; it holds for the cores tested in the sweep (and for the icosidodecahedron at every real scale here).

Verdict: yes, at the level of geometry. Real 1/1 approximants carry an icosidodecahedral shell on a bcc lattice in exactly the
orientation and at a scale (1.12 to 1.25 s0) where the icosidodecahedron amber cell is a valid scutoid division with all Y on the
2-fold axes. The atoms do not mark the partition: no atom sits at a Y vertex or on a 2-fold axis outside the core. An atomic structure is
a set of points, the amber cell is a partition of space; the comparison above is coincidence statistics, not physics.

## Literature (task 1): what was confirmed and where

Facts used here were taken from the CIFs themselves (lattice, space group, atom positions); shells, orientation and scale were then
computed (scripts/shells.py, scripts/approx.py), not copied from text.

| case | source (COD entry, paper) | space group, a | shells found around (0,0,0) (radius A, atoms) |
|---|---|---|---|
| Tsai 1/1 Sc3Zn17.7 | COD 4101359; Lin and Corbett, J. Am. Chem. Soc. 128 (2006) 13268, doi 10.1021/ja063897u | Im-3, 13.8629 | Zn tetrahedron (disordered, 1.5), Zn 12 + 8 (3.55, 3.89; the dodecahedron), Sc icosahedron 12 (4.91), Zn icosidodecahedron 30 (5.62 to 5.71), outer shell 24 + 48 + ... (7.1 to 8.2) |
| Tsai 1/1 Yb24Cd113.8Mg31.4 | COD 2021894; Yamada et al., Acta Cryst. B 73 (2017), doi 10.1107/S2052520617013270 | Im-3, 15.7531 | disordered tetrahedron, Cd dodecahedron (split sites), Yb icosahedron 12 (5.56), Cd icosidodecahedron 30 (6.41 to 6.48), outer 72 (8.2 to 8.4) |
| Tsai 1/1 Y24Cd109.9Mg35.3 | COD 2108845; Yamada, Fujita, Labib, Acta Cryst. B 77 (2021), "2/1 and 1/1 cubic approximants in the ternary R-Cd-Mg (R = Y, Er) systems" | Im-3, 15.4577 | dodecahedron 20 (3.95), Y icosahedron 12 (5.47), icosidodecahedron 30 (6.27 to 6.36), outer 72 (8.0 to 8.2) |
| Cd6Yb 1/1 (1971 model) | COD 1525048; Palenzona, J. Less-Common Met. 25 (1971) 367 | I23, 15.638 | ordered tetrahedron 4 (1.90), Yb icosahedron 12 (5.55), Cd icosidodecahedron 30 (6.36 to 6.47) |
| Bergman 1/1, Mg32(Al,Zn)49 type, Li20Mg32Zn85Al23 | COD 4319177; Lee and Miller, Inorg. Chem. 40 (2001) 338, doi 10.1021/ic0008363 | Im-3, 14.1109 | icosahedron 12 (2.53), dodecahedron 20 (4.58 to 4.60) + icosahedron 12 (5.03) = the 32 triacontahedron vertices, then 48 + 12 (6.67, 7.19) = the 60-atom truncated icosahedron shell |
| Mackay 1/1 alpha-AlMnSi | COD 2007194; Sugiyama, Kaji, Hiraga, Acta Cryst. C 54 (1998) 445, doi 10.1107/S0108270197015989 | Pm-3, 12.643 | two clusters, (0,0,0) and (1/2,1/2,1/2): icosahedron 12 (2.43 to 2.45), then Mn icosahedron 12 (4.73 to 4.82) + Al icosidodecahedron 30 (4.65 to 4.75) |
| Mackay 1/1 Al-Cu-Fe-Si | COD 1532186; Takeuchi and Mizutani, J. Alloys Compd. 342 (2002) 416 | Im-3, 12.48 | icosahedron 12 (2.43), Fe icosahedron 12 (4.75) + icosidodecahedron 30 (4.64 to 4.71) |

Orientation: in every case the shells match the ideal icosahedral solids with 2-fold axes on the cube axes (largest angular
deviation of an atom from its ideal direction: icosidodecahedron shells 0.26 to 3.9 deg, Bergman triacontahedron vertices 1.9 deg).
Inner icosahedron and icosidodecahedron of one cluster are in one common orientation (the icosidodecahedron vertices on the
icosahedron's edge midpoints). Every cluster in a cell has the same orientation (body centring, or for Pm-3 the two clusters checked
separately). Lattice parameter against cluster size: see the s_real/s0 column below.

Sources checked (all free): Crystallography Open Database through its mirror qiserver.ugr.es (the main site crystallography.net
did not answer from either machine on 21 Nov) with element, formula and text searches (Cd-Yb, Ca-Cd, Mg-Al-Zn, Li-Cu-Al, Mg-Al-Pd,
Al-Mn-Si, "approximant", "quasicrystal", "Mg32", "Bergman", "icosahedral", "Tsai"); arXiv 2108.03341 (Ishimasa, So, Mihalkovič,
"Planar defect in approximant: the case of Cu-Al-Sc alloy"): abstract read; the full PDF was too large to open with the tool; its
search excerpt states that the 1/1 bcc approximant has Im-3, that 6 of the 30 b-linkages (2-fold) and 8 of the 20 c-linkages (3-fold)
survive, and that the c-linkage overlap truncates the triacontahedron. Our computed overlaps agree (outer shells do not fit their bcc
cell). PMC article 7053224 (review): blocked by a browser check, not read. Not found in COD: CaCd6 1/1 (only the 2/1 Ca13Cd76,
COD 1536517, Pa-3) and the original Mg32(Al,Zn)49 refinement; the isotypic Li-Mg-Zn-Al phase (COD 4319177) is used instead.
AMCSD and Wikipedia: not used. Further Im-3/Pm-3 1/1 entries found but not run: COD 4109448 (Au-Ca-In), 4111936 (Cu-Ga-Mg-Sc),
1531995/1531996 (Al-Re-Si), 1533741 and 1532189 (Al-Cu-(Fe,Ru)-Si), 2108379 (Al-Cu-Li-Mg), 7209419 and relatives (Na-Au-Sn, Mg32(Al,Zn)49 type).

## Geometry (task 2): the approximants as amber cells

Core = ideal shell polyhedron in the sweep's own solids (scripts of the amber-cell sweep, unchanged), scaled by a least-squares fit
to the real radii (k, Angstrom per core unit); mould = bcc Voronoi cell at the real lattice parameter, so s_real = a/k; s0 = smallest
scale with the core inside its cell. amber.py (sweep) run at s = s_real rounded to 1/1000, bcc, centroid seeds. Every valid run passes
the sweep's own checks (closed oriented pieces, embedded, exact volume gap 0, 0 miscounted sampling points); log.txt re-checks all.

| case | core | atoms vs ideal vertices (rms, max A) | s_real / s0 | valid | kinds | scutoids | Y | Y on 2-fold axes (exact) |
|---|---|---|---|---|---|---|---|---|
| Tsai Sc-Zn | icosidodecahedron | 0.18, 0.20 | 3.9395 / 3.4907 = 1.129 | yes | 3 | 20/32 | 30 | 30/30 |
| Tsai Yb-Cd-Mg | icosidodecahedron | 0.39, 0.44 | 1.129 | yes | 3 | 20/32 | 30 | 30/30 |
| Tsai Y-Cd-Mg | icosidodecahedron | 0.34, 0.36 | 1.130 | yes | 3 | 20/32 | 30 | 30/30 |
| Cd6Yb (1971) | icosidodecahedron | 0.25, 0.27 | 1.124 | yes | 3 | 20/32 | 30 | 30/30 |
| Mackay alpha-AlMnSi | icosidodecahedron | 0.07, 0.08 | 4.3412 / 3.4907 = 1.244 | yes | 3 | 20/32 | 30 | 30/30 |
| Mackay Al-Cu-Fe-Si | icosidodecahedron | 0.03, 0.05 | 1.244 | yes | 3 | 20/32 | 30 | 30/30 |
| Tsai Sc-Zn, Yb-Cd-Mg | icosidodecahedron + 12 caps | as above | as above | yes | 5 | 60/80 | 30 | 6/30 (24 off by 0.0025 to 0.0028 A) |
| Mackay alpha-AlMnSi, Al-Cu-Fe-Si | icosidodecahedron + 12 caps | as above | as above | yes | 5 | 60/80 | 30 | 6/30 (24 off by 0.0047 to 0.0054 A) |
| Bergman Li-Mg-Zn-Al | triacontahedron (32 vertex atoms) | 0.11, 0.17 | 5.3300 / 4 = 1.333 | yes | 2 | 0/30 | 0 | - |
| Bergman Li-Mg-Zn-Al | truncated icosahedron (60 atoms) | 0.22, 0.42 | 0.986 | does not fit | | | | |
| Tsai Sc-Zn | triacontahedron (smallest around the 30 shell) | | 0.982 | does not fit | | | | |

- Caps: the 12 atoms on the five-fold axes (Sc/Yb in Tsai, Mn/Fe in Mackay) stick out of the icosidodecahedron's pentagon planes by
  0.06 to 0.07 A in Tsai (below the 0.18 to 0.39 A by which the atoms miss the ideal shell, so the plain icosidodecahedron is the fair
  model there) and by 0.77 to 0.79 A in Mackay (the capped core is the fair model there). Capped core = convex hull of the
  icosidodecahedron and the icosahedron at the real radius ratio (rational, denominator <= 200), exact in Q(sqrt5), checked invariant
  under all 15 half-turns. Its scutoids are the 60 cap triangles (3 neighbours on the core, 5 on the mould); the 20 icosidodecahedron
  triangles become frustums. In the plain icosidodecahedron the 20 triangles are the scutoids (3 neighbours on the core, 6 on the mould),
  the 12 pentagons frustums.
- alpha-AlMnSi is Pm-3: its two clusters are not equivalent (core radius fit k = 2.912 overall; the two centres differ by under 1 %);
  one common core is used for both, as the bcc mould requires.
- The real Tsai scale (1.124 to 1.130 s0) lies between s0 (where the sweep's icosidodecahedron fails, a Y on the core at contact points)
  and 6/5 s0 (valid); the real Mackay scale 1.244 lies above 6/5. New valid scales for the icosidodecahedron.

## Glue and resin atoms against the Y vertices and the 2-fold axes

Resin atoms = real atoms inside the bcc Voronoi cell of the cluster and outside its ideal core, the core shell (and cap) atoms
themselves excluded. For the Y distances all resin atoms of the neighbouring cells count too. Baseline = 40000 uniform random points
of the same resin.

| case | resin atoms per cell (labels) | Y orbit 24: nearest atom, percentile | Y orbit 6: nearest atom, percentile | atoms within 0.3 A of a 2-fold axis (random expectation) |
|---|---|---|---|---|
| Tsai Sc-Zn | 24 (Zn2, Zn6) | 2.66 A (Zn2), 0.89 | 2.60 A (Zn2), 0.87 | 0 (0.25) |
| Tsai Yb-Cd-Mg | 24 (Cd1, Cd6/Mg6) | 3.01 A (Cd1), 0.88 | 2.96 A (Cd1), 0.87 | 0 (0.17) |
| Tsai Y-Cd-Mg | 24 (Cd1, Cd6/Mg6) | 2.96 A (Cd1), 0.88 | 2.91 A (Cd1), 0.87 | 0 (0.20) |
| Cd6Yb (1971) | 36 (Cd3, Cd5) | 3.01 A (Cd3), 0.89 | 2.87 A (Cd3), 0.85 | 0 (0.29) |
| Mackay alpha-AlMnSi, cluster (0,0,0) | 36 (Al6, Al7) | 2.35 A (Al7), 0.78 | 2.31 A (Al7), 0.76 | 0 (0.59) |
| Mackay alpha-AlMnSi, cluster (1/2,1/2,1/2) | 12 (Al3/Si3) | 2.53 A (Al6), 0.83 | 2.59 A (Al6), 0.86 | 0 (0.21) |
| Mackay Al-Cu-Fe-Si | 36 (Al4, Cu4/Si1, Si2) | 2.11 A (Al4), 0.74 | 2.47 A (Cu4/Si1), 0.89 | 0 (0.60) |
| Bergman Li-Mg-Zn-Al (no Y) | 48 (A1, M3, M4) | - | - | 0 (0.90) |

(capped runs: same numbers within 0.003 A; data/approx_*.json.) What this shows: (i) no real atom lies at or near a Y vertex; the
nearest atom is 2.1 to 3.0 A away, about one atomic diameter; (ii) Y vertices fall in emptier than typical parts of the resin
(percentiles 0.74 to 0.91); with only two independent Y positions per structure this is not significant; (iii) outside the core no atom
lies on a 2-fold axis of its cluster. In the Tsai 1/1 the space between core and mould is filled by atoms of the shared outer
(triacontahedral) shells; there are no separate glue atoms in the sense of the 2/1. The comparison is between points and a partition:
it can show coincidences or their absence, never that the partition is physical.

## Which result belongs in the paper

- Yes, one remark (with Proposition 17 / Table 3): the icosidodecahedral shells of real Tsai-type and Mackay-type 1/1 approximants
  (COD 4101359, 2021894, 2108845, 1525048, 2007194, 1532186) sit on a bcc lattice at s/s0 = 1.12 to 1.13 and 1.24; the icosidodecahedron
  amber cell is valid there, 20/32 scutoids, all 30 Y exactly on the 2-fold axes.
- Yes, a correction: the Y-on-2-fold-axes statement must name its cores. The capped icosidodecahedron (an icosahedral core, the real
  Mackay shell pair) in the bcc mould puts 24 of its 30 Y off the axes (exact test).
- No: the glue-atom comparison (null result: atoms avoid the Y vertices and the 2-fold axes outside the core). Keep it in this study.

## Files

- data/cif/*.cif and data/cif/SOURCES.txt: the seven CIFs with source URLs and checksums.
- scripts/cif_cell.py: CIF reader and cell expansion (data/cells/cell_*.json).
- scripts/shells.py: radial shells and their match to the ideal solids.
- scripts/approx.py: cores, frames, scales, amber runs (the sweep's amber.py with the Y dump of the Y-junction study,
  generated as scripts/_amber_patched.py), atom comparison. Output data/approx_*.json, data/amber_*.json, data/ydump_*.json,
  data/run_*.log, data/approx_summary.txt.
- scripts/shim/solids.py: the sweep's solids plus the capped icosidodecahedron.
- scripts/checks.py: re-checks every run and tests every Y exactly; log.txt ends FINAL ok.
Run on the compute host (foreground, each run under 30 s).

LEADS
1. The capped core breaks the axis property by a tiny amount: is there a seed or Y rule (not the cluster mean) that puts all Y back
   on the 2-fold axes for every icosahedral core?
2. 2/1 approximants (Pa-3, COD 1536517 Ca13Cd76, 2108846 Y-Cd-Mg, 4101360 Sc-Zn): clusters on the 2/1 lattice with glue atoms; the
   mould is no longer one Voronoi cell, so DICTO's combined method needs a multi-cluster mould.
3. Bergman: the 32-atom triacontahedron gives no scutoids; a core between it and the overlapping 60-atom shell (e.g. the 60-atom shell
   truncated by the hexagon planes) is the only Bergman candidate left.
