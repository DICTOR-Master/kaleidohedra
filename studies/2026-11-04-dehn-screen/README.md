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

## HexOct tiles (#75) and their pieces — scripts/hexoct_dehn.py, hexoct_quarter.py, data/hexoct-dehn.json
Multi-piece mode (Dehn additive): the whole c-tile and h-tile sum to zero at every λ tested (≈1e-10) — as they must, they tile (calibration).
Individual pieces: c-tile pieces nonzero at every λ tested (1/10 … 1/3). h-tile (AB) pieces: nonzero for λ < 5/24 (coefficient falls linearly: 0.46 at 1/5,
0.18 at 0.205, 0.07 at 0.207), ZERO for 5/24 ≤ λ < 3/8 (octahedral piece 10 corners, tetrahedral 19 — 16 exactly at 5/24), and zero beyond 3/8 where the
octahedral pieces vanish and the 10-corner tetrahedral piece has only rational-π dihedrals. Below: λ = −1/16, −1/4, −3/8 all nonzero.
LEAD: 5/24 is a known special stretch (Janus kit rods, 2026-10-26); the Dehn screen finds it independently as the onset of Dehn-zero h-pieces. Next: why
(which faces appear at 5/24), and whether an h-piece tiles alone for λ in [5/24, 3/8) (Dehn zero is only necessary).
SHAPES (hpiece_shape.py, hpiece_congruent.py): for λ ≥ 5/24 the h octahedral piece has only dihedrals α = arccos(1/3) and π − α (6 and 9 edges), so its Dehn invariant is
(L_α − L_{π−α}) ⊗ α and the lengths balance from 5/24 on (same mechanism as the truncated tetrahedra of 2026-11-04-tetra-sweep). In every h-tile the two octahedral
pieces are mirror images, and so are the two tetrahedral pieces.
λ ≥ 3/8: the octahedral pieces are gone and the h-tile is TWO MIRROR COPIES of one fixed solid (identical corners at 3/8, 2/5, 9/20, 1/2: the stretch saturates).
So that solid TILES SPACE ALONE (with its mirror image). Corners (layer height h = √(2/3)): a regular hexagon of side 1/√3 at z = 0; three corners at z = −h/2 under
alternate hexagon corners; apex at z = −h on the ball centre below the hexagon's centre. Faces 6 triangles, 3 quadrilaterals, 1 hexagon; dihedrals 90° (9), 135° (6),
120° (3); volume √2/4 = half the volume per ball (= half a TRD). NAMED Narcissus by DICTO (4 Nov): it is its own mirror image (3 mirror planes, C3v), so copies of ONE piece tile space by rotations. NEXT: prior-art check before any claim of novelty.

## Admiral Cap network (scripts/admiral_dehn.py, data/admiral-dehn.json)
Piece kinds Q′ (4 corners), I (icosahedron), A (Admiral Cap, 5 corners): Dehn nonzero for each — none fills space alone; only the mixture can.

## Delian walk O(t) (scripts/delian_dehn.py)
Dehn(O(t)) = (total triangle–rhombus edge length) ⊗ arccos(−√(2/3)) (144.74°; RD edges 120° rational): nonzero for every t > 0, zero only at t = 0 (the RD). Checked at 5 t.

## Batch IQ / Mahler / Q6 (scripts/batch_iq_mahler.py, data/batch-iq-mahler.json) — filled 13 grid cells
Delian O(t): IQ max at t ≈ 0.18325 = Lindelöf point t = 1 − √6/3 ≈ 0.1835 (rhombi at 1/√2, triangles at √3(1−t)/2 equal) — Lindelöf again. Mahler max 13.852 at t ≈ 0.135, no station.
CO–RD sweep: Q6 changes sign once, μ ≈ 1.65. OG family: IQ 0.938–0.969, Mahler 16.59–17.13 (DPHP roundest by both; ball (4π/3)² = 17.55).
Admiral: A cap IQ 0.414, Mahler ≈ 9.000 (exact value?), Q6 0.358. Pyramids: T Mahler 64/9 (any tetrahedron), C6 = R12 8.681 (affine images: calibration). Fixed HexOct h-piece: IQ 0.487, Mahler ≈ 34/3 (to confirm exactly).
