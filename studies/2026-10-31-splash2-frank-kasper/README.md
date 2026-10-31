# Splash Rules II: Frank–Kasper phases (DICTO 2026-10-31)

**DICTO's idea (Splash Rules, 27 Oct):** plot a whole family of exactly computed values and look for one simple rule that covers
the known local ones. Second outside run, after the perovskites (study 2026-10-31-splash2-perovskite, the Window Law).

**Conclusion:** one number covers the known rules, but the rule is old. Every topological count per atom is a line in the
disclination density ρ = six-fold bonds per atom (identity Z̄ = 12 + 2ρ). The study plan's candidate (ours, not DICTO's) "hexagonality of tetrahedral packing",
the non-icosahedral share m = 1 − x12, also works on every real phase: Z̄ = 66/5 + (2/5)m exactly (Yarmolyuk–Kripyakevich 1974,
Z̄ = 13.6 − 0.4·x12; gives Frank–Kasper's range 13⅓–13½). Not a theorem: three hypothetical structures (Dutour Sikirić, Delgado
Friedrichs, Deza 2010) leave the line, only through the YK defect a0: Z̄ = 68/5 − (2/5)x12 − (6/5)a0 — the Window-Law shape with a0
in the place of the Swap defect. In both layered families the Window Law holds with windows 1 and 2, Swap defects +1, −2, +1, and
the Laves c/h letter changes no count.

**Status:** done (counts). Open: the shell relation (below), testable only on a structure off the YK plane (the 2010 counterexamples;
no coordinates in reach). Not run: volumes (weight walk) — counts only, as for the perovskites.

## Method
- Engine scripts/fk.py: CIF parse + space-group expansion; periodic Delaunay (scipy, supercell covering ~3 neighbour distances,
  canonical tetrahedra modulo translation); checks per site: closed triangulated shell, Euler 2, folds 5/6, Z = 12 + #6-bonds, no
  adjacent 6-vertices; empty-sphere margin recorded. Floats only in the Delaunay step; all counts integers, all tests Fractions.
- Census per cell: N_Z, Z̄, tetrahedra, bonds by fold and end types, neighbour types, tetrahedra by corner types and number of
  6-edges, six-fold bonds inside each shell (σ), rings of 6-bonds (Z12 count), major skeleton (components, valences, rank of the
  translation lattice: lines / layer net / 3D net).
- Families: scripts/sqtri.py (square–triangle row tilings, Sullivan / Sadoc–Mosseri Z16-free decoration; S = A15, T = Z, ST = H,
  STT = J); scripts/fk59.py (kagome slabs, steps t ∈ {0,+,−}: ± Laves slab, 0 Z slab; + = C15, +− = C14, 0 = Z, 0+ = μ,
  0+0− = K7Cs6), rules read off AFLOW C14, C36, Zr4Al3, Fe7W6 and COD 9R. Ideal coordinates.
- Splash (scripts/splash.py, dicto-big-brother, 22 processes, ~30 s): 18 real phases + 62 square–triangle words (all primitive up
  to 7 + 30 random of 20) + 119 kagome words (all up to 6 + 40 random of 14) = 199 TCP structures; 4 non-TCP checks. Per-atom
  global fits (constant / line in Z̄ / line in x12 / plane (x12, a0) / site-additive); per-unit window fits over unit words (exact
  elimination); scripts/report.py (tables, checks, stacking-blindness); scripts/relations.py, relations2.py (sympy nullspaces);
  scripts/figs.py (matplotlib on dicto-big-brother).

## Sources of coordinates (data/cif/)
AFLOW prototype encyclopedia CIFs: A3B_cP8_223_c_a-001 (A15 Cr3Si), A2B_cF24_227_c_b-001 (C15 MgCu2), AB2_hP12_194_f_ah-001 (C14
MgZn2), A3BC2_hP12_194_h_a_f-002 (U2Cr3Si), AB2_hP24_194_ef_fgh-001 (C36 MgNi2), A3B4_hP7_191_f_de-001 (Z, Zr4Al3),
A4B4C4DE2_tP30_136_i_j_i_a_f-001 (σ), A7B6_hR13_166_ah_3c-001 (μ, Fe7W6), AB32C48_cI162_204_a_2efg_2gh-001 (Bergman T),
A_cI58_217_ac2g-001 (α-Mn), A30B23_hR53_148_5f_a2c3f-001 (Mg23Al30). COD: 2310246 (δ MoNi, Shoemaker & Shoemaker 1963), 2311049
(P phase), 2310299 (R Mo–Co–Cr), 2107202 (R Mn–Si), 2106034 (ν Mn81.5Si18.5), 2106167 (σ), 1522206, 2105354, 2105334 (Laves 9R and
long-period, Komura et al.), 1576218 (Mg17Al12), 2013036 (Mg21Zn25). Not processed: COD 2310313 (P phase, ops/cell settings
disagree), 1523827 (Mg51Zn20, degenerate). Counts only: Deza–Delgado Friedrichs–Dutour Sikirić table (K, F, J, H, K*, K7Cs6, pσ,
M, C, I, SM, X, Mg4Zn7 + hypothetical fractions).

## Results (data/results.md, data/summary.json, data/splash2_fk.json)
| law | exact on | status |
|---|---|---|
| per atom: tetrahedra 5 + ρ, bonds 6 + ρ, 5-bonds 6, triangles 10 + 2ρ, Z̄ = 12 + 2ρ | all 199 (identity, proved) | known (Frank–Kasper, Nelson) |
| no tetrahedron has two 6-edges at a corner; 0, 1 or 2 (then opposite) | all 199 (proved) | elementary, classical in substance |
| YK: 6N12 = 2N14 + 7N15 + 12N16 ⇔ Z̄ = 68/5 − 2x12/5 = 66/5 + 2m/5; ρ = (3+m)/5 | 18 real + 13 listed + both families (theorem there) | known (YK 1974); fails for 3 hypotheticals (2010) |
| Z̄ = 68/5 − (2/5)x12 − (6/5)a0 in general | identity | elementary; a0 as "Swap defect" analogue new as framing |
| real phases = whole sums of YK units A15 + Laves + Z (e.g. R = 6+24+9, T = 0+40+6, ν = 20+12+10) | 18 real | known (YK / Gvozdetskyi et al. formula) |
| families: site/topological counts window 1 (per row: S 8/T 7 sites; per slab: ± 6/0 7) | 62 + 119 | composition matrices known (Sadoc–Mosseri; FK59 slabs) |
| families: all counts by kind need ≤ window 2; every window-2 count fails Swap, defects +1, −2, +1 (×k) | 62 + 119 | new (catalogue) |
| kagome family stacking-blind: all 119 counts per slab depend only on the Z/L pattern | 22 patterns with ≥2 stackings | new as stated (elementary) |
| shell relation: Σ_Z14 (σ−4) + 2·Σ_Z12 (6−σ) = 8·N15 | all 199 | new, empirical, unexplained (fixed only modulo YK) |
| 3 further relations neighbour types ↔ shell counts; census of real phases spans 8 of 12 free dimensions | all 199 | new, empirical |

Real phases (per cell, Z12:Z14:Z15:Z16, Z̄): A15 2:6:0:0 27/2; Laves (C15, C14, C36, 9R, long period) 2:0:0:1 40/3; Z 3:2:2:0 94/7;
σ 10:16:4:0 202/15; μ 21:6:6:6 174/13; δ and P 24:20:8:4 94/7; R 81:36:18:24 710/53; ν 74:80:20:12 1250/93; Bergman T
98:12:12:40 1082/81. Not TCP: χ (α-Mn), Mg17Al12 (4-fold bonds), Mg23Al30, Mg21Zn25.

## Prior art — sources checked (31 Oct 2026)
- Reference library (ask-library, 6 queries: FK polyhedra Z14–16; YK mean coordination; disclination network Nelson; space
  fullerenes FK enumeration; Shoemaker kagome layers σ μ Laves; Sadoc–Mosseri decoration): no FK paper in the library; Sadoc–Mosseri
  2016 catalogue entry only.
- Read: Sadoc & Mosseri, arXiv 1609.01624 (pp. 1–7); Deza, Delgado Friedrichs, Dutour Sikirić, talk "Space fullerenes"
  (poivs.tsput.ru, full); Gvozdetskyi, Gladyshevskii, Hlukhyy, Chem. Met. Alloys 7 (2014) (YK eqs. 10–12, Hellner–Pearson,
  counterexamples); Dutour Sikirić et al., Acta Cryst. A66, 602 (2010), abstract only (PDF embargoed at ANU).
- Web queries: "Dutour Sikirić Delgado-Friedrichs Deza space fullerenes … Yarmolyuk Kripyakevich"; "Frank-Kasper structures
  Yarmolyuk Kripyakevich fractions Z12 Z14 Z15 Z16 A15 C15 Zr4Al3 linear combination"; "Dutour Sikirić Frank-Kasper structures 84
  data files Delaney symbols download" (no data found). COD and AFLOW searches as listed.
- Cited, not read: Frank & Kasper 1958/59; Yarmolyuk & Kripyakevich 1974; Nelson 1983; Nelson & Spaepen 1989; Shoemaker & Shoemaker
  1986; Sinha 1972; Sullivan; Hellner & Pearson; Rivier & Aste 1996; Coxeter.

## Files
scripts/ fk.py sqtri.py fk59.py splash.py report.py relations.py relations2.py figs.py; data/ splash2_fk.json (every structure,
exact census), results.md, summary.json, relations*.txt, splash.log, cif/; fig/; results/paper.html → results/splash2-frank-kasper.pdf
(also ~/Documents/papers-to-read/splash2-frank-kasper.pdf).
