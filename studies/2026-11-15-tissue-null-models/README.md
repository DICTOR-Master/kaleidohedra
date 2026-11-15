# Tissue null models: reference values for "One tissue, three scales" (2026-11-15)

**Verdict.** Swaps per birth is NOT fixed by 2D topology: Euler fixes only the net cell count (births + splits − deaths − merges) and
with it edges, junctions and mean sides; T1 swaps are free. It IS fixed once a 2D tissue is the moving section of a 3D cell complex:
**swaps per birth = k̄/2 − 3** exactly (k̄ = mean 3D neighbours per cell), for every generic direction and every normal 3D tessellation;
the closed form is #104's h₂/h₁ = (f₂ − 3f₃ + 6)/(f₃ − 4). For the Poisson–Voronoi null model (= a 2D power diagram with linearly
changing weights) this gives **24π²/35 − 2 = 4.7677**, confirmed by simulation 4.7669 ± 0.0006. Moving Voronoi with fixed seeds has no
births at all; under Brownian seed motion T1 counts depend on frame rate (∝ 1/δ), so only net counts or linear-motion rates are usable.
Derivations: THEORY.md. Status at hand-back: job results below marked PENDING were still running. 15 Nov 16:55: tnull-sweep ended FINAL ok (20 checks, 0 failed) and its rows are filled; tnull-move2 and tnull-move3 are still running (alive, 86% of runs done; the long Brownian runs keep their logs quiet for an hour, not a hang).

## Reference table (quantity · null model · value ± error · source)

| quantity | null model | value | source |
|---|---|---|---|
| mean sides per cell | any triple-junction tiling, sphere, F cells | 6 − 12/F exactly | Euler (THEORY §1); checked: sphere PV N=1000 gives 5.988 |
| mean sides per cell | plane (periodic) | 6 exactly | Euler; checked PV 2D, PV 3D section |
| swaps per birth | section of any normal 3D tessellation, periodic | k̄/2 − 3 exactly | THEORY §2 (new derivation, extends #104 Thm 1) |
| swaps per birth | simple 4-polytope (closed 3-sphere sweep) | (f₂ − 3f₃ + 6)/(f₃ − 4) = h₂/h₁ | #104 Thm 1; table data/sweep.json (26 simple uniform 4-polytopes) |
| swaps per birth | 120-cell / truncated 120-cell / bitruncated 600-cell | 366/116, 966/716, 2166/716 | #104 Thm 2; recomputed (Wythoff + Qhull) |
| swaps per birth | 5-cell, tesseract, bitruncated 24-cell, omnitruncated 120-cell | 1, 3/2, 9/2, 9126/2636 | this study |
| rosette share | simple polytopes / generic Voronoi / truncated 600-cell | 0 / 0 / all | #104 Lemma 5; general position |
| swaps per birth | 3D Poisson–Voronoi swept by a plane (= 2D power diagram, linear weights) | 24π²/35 − 2 = 4.76773; sim 4.7669 ± 0.0006 (10 × 200 000 seeds) | Meijering 1953, Miles 1970, Møller 1989 + THEORY §2 |
| swap participations per cell lifetime | same | 96π²/35 − 8 = 19.071 | THEORY §3 |
| swaps per birth | perturbed bcc or fcc lattice (14-face cells) | 4 exactly (sim exact) | THEORY §2 control |
| contact changes per birth (3D tissue) | 4D Poisson–Voronoi swept (= 3D power diagram, linear weights) | 286/9 − 2 = 29.778 (half gains, half losses); sim 29.790 ± 0.009 (16 × 40 000 seeds, tnull-sweep FINAL ok) | Møller 1989 formula evaluated; data/sweep.json |
| swaps per birth | random simple 4-polytope (n cells) | rises to 24π²/35 − 2: n=100 3.970 ± 0.020, 1000 4.579 ± 0.006, 10 000 4.722 ± 0.002, 100 000 4.758 ± 0.002, 300 000 4.76291 ± 0.00004; deficit ∝ n^−0.65 | this study; data/sweep.json (tnull-sweep) |
| births per cell | moving Voronoi, fixed seeds | 0 (swaps per birth infinite) | THEORY §4 |
| T1 per cell per spacing of rms displacement | 2D PV, linear Gaussian seed motion | 3.058 ± 0.005 (integral); sim agrees (pilot 3.07 ± 0.15) | this study, two methods; full sim PENDING |
| contact changes per cell per spacing | 3D PV, linear motion (2-3 + 3-2 flips) | 15.61 ± 0.03 (integral); pilot sim 15.47 ± 0.31 | this study, two methods |
| T1 count | Brownian seeds | not a rate: ∝ δ^−1 (pilot exponent −0.99 2D, −1.02 3D) | THEORY §4 (negative control) |
| net contacts changed per cell after 0.3 spacing | 2D PV, linear or Brownian | ≈ 5.0–5.2 per cell per spacing-normalised (pilot) | this study, frame-rate independent |
| p(n), μ₂, Aboav a, Lewis slope | 2D PV | μ₂ 1.7813 (2 000 000 cells; lit. 1.781), a = 0.646, Lewis slope 0.2252 | Hinde–Miles 1980; data/sweep.json (tnull-sweep) |
| same | planar section of 3D PV | μ₂ 2.854, a = 0.910, Lewis slope 0.313 (14 518 section cells) | this study; data/sweep.json (tnull-sweep) |
| T1 per T2 | 2D coarsening froth (von Neumann) | 0.53 ± 0.05 macroscopic; 3/2 incl. side-shedding; vanishing cells 9/84/7 % 3/4/5-sided | Rutenberg–McCurdy 2005; Herdtle–Aref 1992; consistency 0.53+0.98=1.51 |

## Controls
Pass: 120-cell, truncated 120-cell, bitruncated 600-cell, 5-cell, tesseract h-vectors; truncated 600-cell non-simple; sweep identities
(births = deaths = cells, i = 0, d+1 absent, 4D i₂ = i₃) exact in every sample; bcc exactly 4; torus mean 6; sphere 6 − 12/N; areas tile;
2D made = lost; linear-motion rates step-independent; integral and simulation agree. Fail as intended: Brownian counts step-dependent;
PV value ≠ bcc 4. One pilot check failed and was rescoped (random polytopes at n ≤ 1000 are far from the limit; finite-size deficit).

## Files
scripts/nulllib.py, sweeps.py, moving.py, kinetic_integral.py; data/ (pilot JSON + logs; full runs land as data/sweep.json, move2.json,
move3.json, kinetic.json). Jobs: tnull-sweep, tnull-move3 (big machine), tnull-move2 (node), each with its watcher and alert.
