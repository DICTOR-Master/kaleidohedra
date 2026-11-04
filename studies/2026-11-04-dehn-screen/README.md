# General Dehn screen; OG family (4 Nov 2026) — Concordance 6.1, Dehn column of the "Golden nests / OG / AXE networks" row
scripts/dehn.py: Dehn(P) = Σ L_e ⊗ θ_e (interior dihedrals, works for non-convex input with ordered faces). Method: find integer relations among the distinct dihedral
angles and π (PSLQ, coefficients ≤ 300, tol 1e-8), reduce to a basis β_j independent mod Qπ; Dehn = 0 iff for every β_j the coefficient-weighted sum of edge lengths is 0.
(First version identified lengths in Q(√2, √5) and FAILED calibration — RD edges are √3, and float PSLQ on lengths gave spurious relations; replaced.)
Calibration (11/11 at tol 1e-8): zero — cube, RD, truncated octahedron, RT, T(4) minus corners; nonzero — tetrahedron, octahedron, icosahedron, dodecahedron,
Archimedean truncated tetrahedron. (At tol 1e-10 the RT's 144° = 4π/5 is missed from its float corners: tolerance matters.)
RESULT: all nine OG-family solids (TQHD, TQP, TQH, TPH, OG, KRE, PHE, TPP, DPHP; corners from 2026-10-19-five-fold-octet/data/og-family-solids.json, all convex)
have NONZERO Dehn invariant, at tol 1e-8 and 1e-9 alike (coefficient sums 20–1500 edge units, far from 0). Hence none tiles space alone and none is scissors-congruent to a cube.
Not automatic for icosahedral solids (the RT is icosahedral with Dehn zero). Status: calibrated numerical screen; an exact proof needs the exact dihedral angles.
Data: data/dehn-screen.json.
