# The DICTO Kepler–Poinsot–UP Cycle (tall PiTet): UP grown from the Kepler–Poinsot stars (DICTO 2026-10-19: "think stellation, think Gaudí", option 2; float first look)

DICTO noticed that the UP shells always come out flat. That is because each UP step is the tightest solid around the last one, and the hulls fill in every valley. Here every station is a true star instead, and the valleys stay open until the next hull.

**The cycle:**
- I → great stellated dodecahedron (20 spikes, tips at 3× the face distance) → its hull D1;
- D1 → small stellated dodecahedron (12 five-sided spires, tips at √5× the face distance) → its hull I2;
- **I2 = φ³ · I** (4.2360680), so the cycle repeats for ever.

**Spires** (height ÷ face radius): great stellated **φ²** (2.618), small stellated **φ** (1.618).

**Shell pieces** (`cleo_pattern.py`, float, every random point in exactly one piece):

| Shell | Pieces (volume each, I of edge 1) | Sum = valley |
|---|---|---|
| I → GSD | 20 spikes | — |
| GSD → D1 (valleys) | 12 inward pyramids (D1 face → I corner, 1.27719) + 30 valley tetrahedra (I edge + two tips, 0.35301) | 25.91641 |
| D1 → SSD | 12 spires | — |
| SSD → I2 (valleys) | 20 inward pyramids (I2 face → D1 corner, 2.41954) + 30 valley tetrahedra (D1 edge + two tips, 1.49536) | 93.25142 |

**The Cleo star's own pattern** (inward pyramids from the hull's faces, valley tetrahedra along the core's edges) **fills both valleys exactly**: "the same pattern, different solids". The Cleo star is the short version, with tips at 2×. Volumes: I 2.18169, GSD 6.54508 (3× I), D1 32.46149, SSD 72.58610, I2 165.83752.

**EXACT (`exact_kp.py`, `exact_kp.json`, ℚ(√5)):** I2 = φ³·I exactly. In each shell, the spikes, inward pyramids and valley tetrahedra together fill core → hull exactly, with no two overlapping (exact separating planes) and all inside the hull and outside the core. Each kind has one volume. Great stellated shell: spike 1/8 + √5/24 (= I/10, so the GSD = 3·I), inward pyramid 5/8 + 7√5/24, valley tetrahedron 1/6 + √5/12. Small stellated shell: spire 5/3 + 3√5/4, inward pyramid 29/24 + 13√5/24, valley tetrahedron 3/4 + √5/3.

**Perspective (DICTO, from Gothic figures and Michelangelo's David, made to look right from below; `perspective.py`, float).** A pinhole camera looks at the spire; in the picture, height (base centre → tip) is compared with the base's width. DICTO chose both viewpoints:
- **B, outside on the base plane at 6 base radii:** the true spires already look almost right (great stellated 1.59 against 1.51; small stellated 0.83 against 0.85). The "seen" heights differ by only ×0.94 and ×1.03.
- **A, inside, standing in the valley at a spike's foot:** the true spires look about three times squatter (0.53 against 1.51; 0.40 against 0.85), and **no height reads right from there**: from the foot, extra height is foreshortened away.
- **This corrects my first crude angle model**, which had asked for about ×2 everywhere.

This matches the sculptors' practice: the correction is made for a chosen, moderate viewing distance, not for the foot.

**Correction (2026-10-19) and golden reciprocity (EXACT, `exact_reciprocal.py`, `congruence.py`):** a first shape test compared only lists of edge lengths, and wrongly called the small shell's inward pyramid "CLEO again". The corner-matching test (`congruence.py`) shows it is not. CLEO is a tall point (height / base radius φ²); this piece is its golden reciprocal, φ⁻². Likewise the small star's spire (φ) and the great shell's cap (φ⁻¹). (h/r)² = φ⁴ and φ⁻⁴, φ² and φ⁻²: Galois conjugate pairs. This is DICTO's "opposite structures throughout", PiTet's own principle. The first shell's CLEO, cap and AXE identities are confirmed by the corner test.

**Prior art:** the nesting of the great and small stellated dodecahedra in their hulls is classical (Kepler, Coxeter). What may be new is filling the shells with this piece pattern, and pairing it with UP. To check.

**Next:**
- DICTO's perspective idea: spires lengthened so their *apparent* height, seen from inside a shell, keeps the golden proportion;
- Gaudí: the double-twist (left and right twisted copies intersected) and catenary profiles;
- Gaudí's own writings to the library.
