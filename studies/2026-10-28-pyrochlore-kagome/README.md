# Pyrochlore spin ice and kagome metals: the Swap Rule and the Rule of Halves on magnetic and electronic materials (DICTO 10-28)
LAST study of the materials line (DICTO: "draw a line after those"). Placeholder paper: #74 "Halves and Swaps in Magnets and Metals".
Geometry: pyrochlore = corner-sharing tetrahedra (DICTO Janus c/h Pyrochlore #59, pyrochlore halves); kagome = corner-sharing
triangles (Kagome Hulls). Questions, as decisions:
1. Spin ice (Dy2Ti2O7, Ho2Ti2O7): Pauling ice rule 2-in-2-out per tetrahedron; residual entropy (1/2) R ln(3/2) per spin
   (Ramirez et al. 1999). Test: does the Rule of Halves (#57) count the ice-rule states / monopoles exactly?
2. Kagome metals (CsV3Sb5, FeSn, Co3Sn2S2): kagome layers stacked; flat band and Dirac points from corner-sharing triangles.
   Test: do the Swap Rule (#64) stackings match the known kagome stackings (AA in CsV3Sb5, AB-type in others)?
Method: exact counts from coordinates first (as tetra_counts.py), prior art first (Pauling 1935, Anderson 1956, Bramwell-Gingras
2001, Castelnovo-Moessner-Sondhi 2008; kagome: Syozi 1951, Mielke flat bands, Ortiz et al. 2019 CsV3Sb5). Sources to be listed.

## Plan refined 10-28 (after re-reading #57, #61, #64 and pyrochlore-halves)
Key link: along [111] the pyrochlore network is kagome layers alternating with triangular layers, and it is the bond-midpoint
network of diamond (pyrochlore-halves paper), so it stacks 3C/2H/... exactly like ice and diamond (#73). Spin ice on any stacking:
- Step A (exact, Pi): kagome/triangular layer decomposition and corner-sharing counts on 3C, 2H, 4H, 6H stackings (tetra_counts style).
- Step B (dbb): residual (Pauling) entropy of the ice rule per spin, W(h), on 3C, 2H, 4H, 6H by exact transfer-matrix/enumeration on
  small cells + Monte Carlo thermodynamic integration. Prior art: Pauling 1935 (W = 3/2 for all stackings), Nagle 1966 (series),
  Herrero and Ramirez 2014 (ice polymorphs W). Test: is the small correction linear in h (law) or not?
- Step C: kagome metals - stacking of kagome layers (CsV3Sb5 AA; Fe3Sn2 bilayers; Co3Sn2S2 ABC) vs Swap Rule pieces; literature only.
CONCLUSION target: one exact statement + one numerical test per material; then #74 and the materials line closes.

## Progress 10-28: Step A — DONE (pyro_counts.py, loops.py, coordseq.py on dbb; outputs .out)
Exact on 3C, 2H, 4H, 6H, 9R: pyrochlore sites 2 per atom, always 1/4 in triangular layers and 3/4 in kagome layers; per tetrahedron
eclipsed corner-sharing pairs h/2, boat 6-loops 3h/2, chair 6-loops 2 - 3h/2 (total 2, fixed); 8-loops 3 (fixed).
SURPRISE: closed non-backtracking walks per site are IDENTICAL on 3C, 6H, 4H, 2H for every length up to 20 (24, 48, 480, 3432, ...),
although the networks differ (control: coordination sequences 3C 4,12,24,42,64,92; 2H 4,12,25,44,67,96, = known values; 4H between).
Meaning: the loop structure that corrects Pauling's ice-rule entropy is the same on all stackings through loops of 20 bonds, so the
residual entropy of spin ice (and of water ice Ih vs Ic) should be stacking-independent to very high order: a law with zero slope.
Fits Nagle 1966 (Ih and Ic entropies equal within his series). Step B becomes: confirm W(h) flat; prior art check on "same loop
counts" (Ihara zeta of diamond vs lonsdaleite) FIRST. Coordination shells: shell 3 = 24 + h and shell 4 = 42 + 2h (law-shaped);
shell 5 not (4H 66.5 vs line 65.5).

## Progress 10-28: Step B — DONE (loops2.py, loops2.out on dbb)
Large cell (36 x 36 in plane, >= 36 layers), walks counted from one column only, neighbours checked geometrically: closed
non-backtracking walks per atom are IDENTICAL on 3C, 2H, 4H, 6H, 9R for every even length 6..34 (24, 48, 480, 3432, 25704, 194256,
..., 27416593190640). (The small-cell run loops.py was slightly inflated from L = 16 by wrap-around walks: 194262 vs 194256 - superseded.)
Placeholder name: the Loop Equality. Status: computed through length 34 on five stackings; proof for all lengths open (CONJECTURE).
Prior art: Pauling 1935 (W = 3/2 any stacking); Onsager (in Nagle's thesis): S_h >= S_c; Nagle 1966 series W = 1.50685(15) both;
Herrero and Ramirez 2014 (arXiv 1406.5929) thermodynamic integration, 1.50786 / 1.50778; Kolafa 1.5074674 / 1.5074660;
Xu, Lin and Zhang, arXiv 2511.22477 v3 (2026, READ pp. 1, 7-8): tensor networks, w = 1.5074584 for BOTH, "numerical evidence
supporting the equality between Sh and Sc"; they name complex stackings as an open challenge (non-Hermitian transfer matrices).
New here: (1) loop counts equal on EVERY stacking tested, not only 3C/2H, to length 34 - a combinatorial reason for the equality;
(2) consequence (conjecture): residual entropy of water ice and of spin ice is the same for every stacking, stacking-disordered ice
included - the Hexagonality Law with zero slope. Searches: no source found on equal non-backtracking walks of diamond vs lonsdaleite
(web: Ihara zeta crystal nets; residual entropy Ih vs Ic).
CONCLUSION B: spin-ice/ice entropy is stacking-blind (Loop Equality to length 34, conjecture for all lengths).
Next: Step C kagome metals (literature).
