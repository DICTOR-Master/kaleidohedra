# Mahler volume product along the cube–octahedron sweep (2026-11-04) — test of Concordance 5.5 find (Iriyeh–Shibata, Duke 2020)
S(μ) = C ∩ μC*, C = [−1,1]^3; polar S° = conv(C*, C/μ). Exact (fitted cubic confirmed, then symbolic):
- 1 ≤ μ ≤ 2: |S| = 4μ³/3 − 4(μ−1)³, |S°| = 8/μ², so f(μ) = |S|·|S°| = −32(2μ³ − 9μ² + 9μ − 3)/(3μ²).
- 2 ≤ μ ≤ 3: |S| = 8 − 4(3−μ)³/3, |S°| = 4/μ.
- Ends: f = 32/3 at the octahedron and the cube — exactly Mahler's minimum (Iriyeh–Shibata), as it must be.
- Kelvin (μ = 3/2): f = 128/9; cuboctahedron (μ = 2): 40/3; Icosaxes (μ = φ): 544/3 − 224√5/3 ≈ 14.3736.
- Maximum at the root μ* ≈ 1.6312 of 2μ³ − 9μ + 6 = 0 (three real roots, trigonometric form μ* = √6 cos(⅓ arccos(−√(2/3)))), f ≈ 14.3751:
  just past Icosaxes (φ = 1.6180) but not at it — no golden station. Not symmetric under μ ↔ 3/μ or μ ↔ 3 − μ.
Verdict: consistent with Mahler; the sweep's "roundest" member (largest volume product) sits within 1% of Icosaxes, but is a cubic irrational, not golden.

## Parallel tests on the same sweep (DICTO's idea, 4 Nov: outside tests evaluating one another)
Third measure, isoperimetric quotient IQ = 36πV²/A³ (soap films / roundness by surface), exact for 1 < μ < 2:
V = 4μ³/3 − 4(μ−1)³, A = 12(μ−1)² + 2√3(2μ² − 6(μ−1)²); d log IQ/dμ ∝ −18μ(μ−1)(μ−√3).
=> the roundest member by surface is EXACTLY μ = √3, the fixed point of #81's core turn μ ↔ 3/μ (IQ = 0.78164).
Special points of the sweep by unrelated measures:
| measure (field) | special point | named station? |
| harmonic Q4 = 0 (physics, #94) | μ = φ | Icosaxes, exact |
| harmonic Q8 = 0 | φ and (√13 − 1)/2 | Icosaxes + bronze station |
| isoperimetric maximum (soap films) | μ = √3 | core-turn fixed point (#81), exact |
| Mahler product maximum (convex geometry) | root of 2μ³ − 9μ + 6 (≈ 1.6312) | none; within 1% of Icosaxes |
| diamond growth α = 3/μ (crystal growth) | α ↔ μ is the core turn itself | the turn's fixed point √3 again |
Two of the measures land exactly on stations our own work had named; the core turn's fixed point √3 is singled out twice (roundness, and as the point where α = μ).

## Second dual sweep CO ∩ μRD (RD at μ = 1, CO at μ = 2), 4 Nov
Exact pieces (fit to 1e-9, coefficients identified): (1, 4/3): V = −6μ³ + 24μ² − 24μ + 8, |S°| = 4(3μ + 2)/(3μ³); (4/3, 3/2): V = −24μ³ + 96μ² − 120μ + 152/3, |S°| = 6/μ²;
(3/2, 2): V = 8μ³ − 48μ² + 96μ − 172/3, |S°| = 4/μ.
- Ends: Mahler product 40/3 at the RD and at the CO (a polar pair; same value as the CO station of the first sweep).
- Mahler maximum ≈ 15.387 at the root μ ≈ 1.5997 of 12μ³ − 36μ² + 43 = 0: no named station.
- Isoperimetric maximum at μ ≈ 1.5227 (0.8525): no named station.
So on the second sweep neither roundness nor polar balance lands on a station: the exact √3 coincidence belongs to the cube–octahedron pair.

## Foam test (Kelvin's problem) on the CsCl pairs, 4 Nov
Tiling by P_μ and Q_μ = P_{3−μ} (#90 Prop. 6), two cells per lattice cell of volume 8; wall area per unit volume W(μ) = (A_P + A_Q)/16.
W is symmetric under μ ↔ 3 − μ (the pair swap) and is LARGEST at its fixed point μ = 3/2, Kelvin's foam (W = 1.67404),
decreasing to the end μ → 1, the cuboctahedron + octahedron honeycomb: W = (3 + 2√3)/4 ≈ 1.61603.
So within the family Kelvin's cell has the most wall area per cell; the unequal pairs have less. Kelvin's problem asks for EQUAL volumes,
which only μ = 3/2 satisfies; relaxing it, unequal cells win — the fixed point of the swap is again singled out, here as the maximum.
