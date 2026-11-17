# God's Dice (18 Nov 2026)

DICTO · dictospheres.com

**DICTO's question:** "what if the ultimate lawgiving shape was actually a truncated cube". He asked for all three readings below to be tested. The title is his. It echoes Einstein's "God does not play dice" (letter to Max Born, 4 December 1926: "Jedenfalls bin ich überzeugt, daß der nicht würfelt"). Serves aim 2 (geometry gives laws).

Labels: **exact** (symbolic algebra or a proof), **certified** (interval arithmetic), **computed** (floating point or Monte Carlo). No label is upgraded.

## Setting

The line is S(μ) = C ∩ μ·C\*, with C = [−1, 1]³ and C\* = {|x| + |y| + |z| ≤ 1}. It runs octahedron (μ = 1) → cuboctahedron (2) → cube (3) (#90, #94, the Turn Law draft). It has two chambers:
- Chamber I, 1 < μ < 2: 6 squares and 8 hexagons, corners perms(±1, ±b, 0), b = μ − 1.
- Chamber II, 2 < μ < 3: 6 octagons and 8 triangles, corners perms(±1, ±1, ±a), a = μ − 2.

Every member has 14 faces, 36 edges and 24 corners (checked at 6 points).

**The uniform truncated cube is S(1 + √2)** (exact). The octagons are regular when 2a = √2(1 − a), so a = √2 − 1. The cut sits at the silver mean.

## Plan (written before computing)
1. **Turn point.** Find the fixed point of DICTO's turn μ ↦ 3/μ, the walls, the equal-edge and midsphere points, and the swap of the Delian-bond power line. Is 1 + √2 one of them? Exact.
2. **The √2 station.** Evaluate every measure the laws papers use along the whole line, piece by piece and exactly: Ω(S;0) = 3!·vol(polar), Mahler product, isoperimetric quotient, Q4/Q6/Q8 zeros (and Q_l up to l = 16 at the truncated cube), Dehn invariant, filling with octahedra. List every special point and compare. Put the truncated cube beside its icosahedral twin.
3. **The die.** Solid-angle model from the centre of mass, which is the centre by symmetry. Give the truncated cube's face probabilities in closed form and certify them. Find the fair point (every face 1/14) on the line in exact form. Cheap side check: a quasi-static rolling Monte Carlo, labelled computed.

## Results

| Measure or station | Special points on the line (1, 3) | Truncated cube 1 + √2 = 2.41421? |
|---|---|---|
| Turn μ ↦ 3/μ (insphere point) | fixed point √3 (exact) | no. Its turn is 3(√2 − 1) = 1.24264, in chamber I. The truncated cube is not tangential (face distances 1 and 1.39385) |
| Walls (Hopscotch) | 1, 2, 3 | no (inside chamber II) |
| Power line (Delian bond #51, Remark): μ = 3/2 − 2w | swap w ↦ −w is μ ↦ 3 − μ; fixed point Kelvin 3/2 (exact) | no. It is the member w = 1/4 − 1/√2 of #51 |
| **Equal edges = midsphere (all edges tangent to one sphere)** | **3/2 (Kelvin), 2 (cuboctahedron), 1 + √2** (exact) | **yes. It is the only one in chamber II** |
| Ω(S;0) = 3!·vol(polar) | 48/μ² on I, 24/μ on II: kinks at the walls only, no interior point | no; value 24(√2 − 1) |
| Mahler product | global maximum 14.37509 at the root 1.63122 of 2μ³ − 9μ + 6; local minimum 40/3 at the wall 2; **local maximum 13.38817 at the root 2.08525 of 2μ³ − 9μ² + 21 (new detail)** (exact) | no; value 224(3 − 2√2)/3 = 12.81077 |
| Isoperimetric quotient | one maximum, √3 (0.78164); none in chamber II (exact) | no; value 0.61303 |
| Q4 = 0 | φ only (Icosaxes) | no. In chamber II, Q4 = 0 would need a⁴ − 6a² − 1 = 0, which has no root in (0, 1) |
| Q6 = 0 | 1.34543 (b⁴ − (17/2)b² + 1 = 0); **2.42393 (a⁶ − 15a⁴ + 75a² − 13 = 0)** (exact) | **near, not at**: 0.0097 apart, and the minimal polynomials differ. Q6(truncated cube) = 0.0196 |
| Q8 = 0 | (√13 − 1)/2, φ | no |
| Q_l at the truncated cube, l = 4..16 | Q4 .3239, Q6 .0196, Q8 .1975, Q10 .1959, Q12 .5269, Q14 .1522, Q16 .2274 | none vanishes (exact) |
| Dehn invariant D(μ) ⊗ arccos(1/√3) | D = 24√2(3 − 2μ) on I, −24√2(3 − μ) on II; zero only at 3/2 and 3 (exact) | no. D = −24√2(2 − √2) ≠ 0, cancelled exactly by its one octahedron per cell |
| Fills space with regular octahedra | every μ in [2, 3]: the corner pieces at a lattice vertex form |x| + |y| + |z| ≤ 3 − μ (exact) | not special: the whole chamber fills |
| Fair die (solid angle, every face 1/14) | **μ_f = 1 + √(2 tan(π/14) tan(2π/7)) = 1.7565821359…** (exact; next section) | no |

**Icosahedral twin** (exact). Use the Turn Law's scale λ = μ/(hR), where the turn is λ ↦ 1/λ.
- Cube line: truncated octahedron at λ = √3/2; truncated cube at λ = (1 + √2)/√3 = 1.39385.
- Icosahedral line: truncated icosahedron at λ = 0.974154 (361λ⁴ − 390λ² + 45); truncated dodecahedron at λ = 1.169839 (45λ⁴ − 150λ² + 121).

On neither line does the turn pair the two uniform truncations. On the cube line the turn pairs Kelvin's 3/2 with the cuboctahedron 2. The truncated cube's twin is the truncated dodecahedron, the regular-decagon station. The golden station of the cube line (Icosaxes, μ = φ) is a different kind of point: there a harmonic falls silent.

### The die (test 3)
The truncated cube in the solid-angle model:
- Triangle face: tan(Ω₃/2) = (√2 − 1)/((1 + 2√2)·√(5 − 2√2)) (exact; Van Oosterom–Strackee formula).
- **p(triangle) = arctan(t)/(2π) = 0.0116642900826586850814153334030865799644**
- **p(octagon) = 1/6 − arctan(t)/(3π) = 0.1511142798897884198914462221292178933808** (certified by interval arithmetic; the octagon also checked by an independent fan of 8 triangles to 40 digits).

So each octagon is 12.96 times as likely as each triangle. The 6 octagons together take 90.67% of rolls and the 8 triangles 9.33%.

Along the whole line (exact closed forms):
- Each cube-plane face: p_C = (1/π)·arctan(b²/(2√(1 + b²))) on chamber I.
- On chamber II: p_C = 1/6 − (2/(3π))·arctan((1 − a)²(a + 2)/(√(a² + 2)(a² + 6a + 5))).
- p_C is continuous and strictly increasing from 0 (octahedron) to 1/6 (cube). The faces grow as nested sets, so it is strictly monotone.

**The fair point is unique**, and it is in chamber I because p_C(2) = arctan(1/(2√2))/π > 1/14 (exact):
- μ_f = 1 + √(2 tan(π/14) tan(2π/7)) = 1.7565821359450421390992118226804176649 (certified).
- Minimal polynomial μ⁶ − 6μ⁵ − 3μ⁴ + 52μ³ − 97μ² + 74μ − 13 (irreducible).

The derivation is short. A square of half-diagonal b at distance 1 subtends 4·arctan(b²/(2√(1 + b²))), so setting it equal to 4π/14 gives b⁴ − 4T²b² − 4T² = 0 with T = tan(π/14), and sec x + tan x = tan(π/4 + x/2).

The fair solid has 6 squares of side √2(μ_f − 1) = 1.06997 and 8 non-regular hexagons. It is none of the named stations (exact: the minimal polynomials differ, and it has no common factor with the Mahler or canonical-anisotropy roots). It lies 0.0245 past the turn's fixed point √3. At √3 the solid-angle probabilities are 0.06778 (each square) and 0.07417 (each hexagon).

**Quasi-static rolling check (computed, Monte Carlo, N = 80 000).** The die lands with a uniformly random down-direction and rolls downhill without bouncing (steepest descent of the centre's height; after Varkonyi and Domokos). The controls hold: cube 1/6, octahedron 1/8. The results agree with the solid-angle model within about 2 standard errors at every station tested:

| μ | quasi-static p_C | solid-angle p_C |
|---|---|---|
| 3/2 | 0.03559 ± 0.00024 | 0.03544 |
| √3 | 0.06761 ± 0.00029 | 0.06778 |
| μ_f | 0.07136 ± 0.00029 | 0.07143 |
| 2 | 0.10767 ± 0.00028 | 0.10817 |
| 1 + √2 | 0.15098 ± 0.00017 | 0.15111 |

The quasi-static fair point is μ ≈ 1.7572, by bisection at N = 40 000 (statistical). This does not test bouncing dice.

## Verdicts
1. **Turn point: NO** (exact). The turn's fixed point is √3, the power line's swap point is Kelvin 3/2, and the walls are 1, 2, 3. The truncated cube's turn partner is 3(√2 − 1), which is no station. The truncated cube **is** a named station of a different kind: the line's equal-edge and midsphere stations are exactly 3/2, 2 and 1 + √2. The turn pairs 3/2 with 2, but it sends 1 + √2 off the set.
2. **√2 station: NO law singles it out** (exact). Ω, Mahler, isoperimetric quotient, Q4, Q8 and Dehn all have their special points elsewhere. Space filling with octahedra holds for the whole chamber II. The Q6 silence at 2.42393 is near the truncated cube but not at it (confirms #94's study). Its only special property on this line is the one it is defined by: regular octagons, which is the same as equal edges and the midsphere. Its icosahedral counterpart is the truncated dodecahedron, not a φ-station.
3. **The die: NOT fair, and the fair point is new to us** (exact or certified). The truncated cube is a heavily loaded die: octagon 0.151114, triangle 0.011664. The one fair member of the line is μ_f = 1 + √(2 tan(π/14) tan(2π/7)) = 1.75658, a squares-and-hexagons solid close to the turn's tangent solid √3. It is not the uniform truncated cube or any named station. We did not find it in the sources checked; we do not claim it as new.

## Prior art and sources checked
- Diaconis and Keller, "Fair dice", *Amer. Math. Monthly* 96 (1989) 337–339. Bibliographic record and secondary summaries only, not read. Their result: dice are fair by symmetry when the symmetry group is transitive on the faces. The line's members are not face-transitive, so fairness at μ_f rests on the model alone.
- The solid-angle model is attributed to Singmaster (1981), per secondary sources; not read.
- Riemer, Stoyan and Obreschkow, "Cuboidal dice and Gibbs distributions", arXiv:1302.3925, abstract read. Simple geometric models do not fit cuboid dice in experiments, the landing surface changes the probabilities, and they fit a one-parameter Gibbs model.
- Yong and Mahadevan, "Probability and dynamics in the toss of a non-bouncing thick coin", arXiv:1008.4559, abstract read. The rigid-body dynamics of spin and precession set the outcome.
- **Where the solid-angle model is known to fail** (from these and an APS 2006 abstract seen in search): tall and squat prisms and cylinders, bouncing and energetic throws, and surface-dependent rolls. Bouncing is not modelled here.
- Varkonyi and Domokos (J. Nonlinear Sci. 2006), the quasi-static rolling model: bibliographic record only.
- US patent 11033806 (fair N-sided dice by equal solid angles) and US 2025/0387698 "Low Probability Dice" were seen in search. 11033806 was not read beyond the search snippet; 2025/0387698 was read on one patent page (no 14-face fair truncation). No source found computes μ_f.
- Our own records: the Turn Law draft (2026-11-13), Geometry Gives Laws draft (2026-11-12), #51 Delian Bond (power line remark), #94 Silent Golden Station and its study 2026-11-04-harmonic-fingerprint (Q6 near the truncated cube), 2026-11-04-mahler-sweep, and 2026-11-10-canonical-sweep (Ω pieces, anisotropy root 1.69259 cited, not recomputed).
- Classical: the truncated cube and truncated dodecahedron (Archimedes; Kepler's names), and the truncated-cube + octahedron honeycomb (uniform truncated cubic honeycomb).

## LEADS
1. **The fair 14-face die μ_f** (degree 6, built from tan(π/14)). Does it also come out fair in a bouncing simulation, or in a physical print? This is a testable object for DICTO's studio, and the truncated cube would be the unfair control.
2. **Midsphere stations as the edge-counterpart of the turn.** The turn's fixed point is the insphere point. The midsphere points are 3/2, 2, 1 + √2, and the turn pairs only 3/2 ↔ 2. Is there an edge-turn, an involution fixing the midsphere solids? The icosahedral line gives the second test case.
3. **Quasi-static basins equal solid angles here to within 2 SE everywhere.** Is that exact for corner-transitive solids with all corners on one sphere? A proof or a counterexample is the next step.
4. The Mahler product's second local maximum at 2.08525 (root of 2μ³ − 9μ² + 21) is not in the earlier sweep notes. It belongs in the sweep record. Into the Concordance (DICTO's call where).
5. Outside the plan: the regular octagon links the truncated cube to the Ammann–Beenker line of the Turn Law (field ℚ(√2), turn at 1/√2). No computed connection yet.

## Files and runs
- `scripts/gods_dice.py`: tests 1–3, exact (sympy) and certified (mpmath intervals). 51/51 checks, FINAL ok, 12 s on a compute host. Log `data/gods-dice.log`, data `data/gods-dice.json`.
- `scripts/roll_sim.py`: quasi-static Monte Carlo (numpy), N = 80 000. FINAL ok, 256 s. Pilot N = 20 000 in `data/roll-sim-pilot.log`. Log `data/roll-sim.log`, data `data/roll-sim.json`.
- `scripts/fig_gods_dice.py` → `figures/gods-dice.png`: (a) the truncated cube in cube-family green #488e48; (b) face probabilities along the line with the stations. FINAL ok.
- Faults fixed on the way: a signed determinant (wrong sign of tan) was replaced by its absolute value and checked; mpmath intervals have no atan, so atan2 is used; the monotonicity sample was moved off the cube end, where the derivative is 0.
