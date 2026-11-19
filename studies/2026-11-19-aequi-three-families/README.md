# More Aequi: fair dice with three face families (19 November 2026)

**Verdict (pilot, double precision): all 20 sets of three face orbits of the pyritohedral group give exactly one fair die each** (one orbit at depth 1, two free depths; every face 4π/N to 1e-9; one solution per set from a 9 × 9 grid of starts on [0.7, 1.8]²). The set O8 + RD12 + I12 is D191 Aequus RDI-32 (its depths, rescaled, match study 2026-11-19-aequus-rd-ico), a control.

Orbits used (face directions along axes of the cube and icosahedron frames, as in Equanimity §2): C6, O8, RD12 (cubic), D12, I12 (the icosahedron's 20 less O8), RT24 (the triacontahedron's 30 less C6). Method: half-space intersection, solid angles by Van Oosterom–Strackee (1983), fsolve. Script scripts/three_fam.py; log run1.log.

Not yet: exactness (100 digits), shapes, symmetry check per die, the tetrahedral groups, sets of four or more orbits, the whole-orbit Ih set D12 + I20 + RT30.

LEADS: the full enumeration (every group, every orbit set) to make the family complete; names and numbers are DICTO's.
