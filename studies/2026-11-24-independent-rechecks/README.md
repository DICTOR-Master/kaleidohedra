# Independent rechecks: Aequi exact dice (Theorems 1, 2) and the A402191 Vacuus (Theorem A, type-B count) (24 November 2026)

DICTO · dictospheres.com · study 2026-11-24-independent-rechecks · with Claude (Anthropic).

**Verdict: every item checked agrees.**

| item | statement checked | verdict |
|---|---|---|
| 1a | CIRT-30: 2Ω(RT24/12a) − Ω(C6) = 4π/30 for t ≥ t₀ = (7/4)/√3, at several t, to ≥ 50 digits | **agrees** (to 1e-177) |
| 1b | the claimed t₀ | **agrees** (the identity holds at and above t₀; t₀ is a limit of the proof, not of the identity) |
| 1c | the fair t* = x/√3, x the root near 1.7579 of 16x⁴ − 40x³ − 100x² + 130x + 145; t* = 1.01493580273976… | **agrees** (enclosed to ±1e-40/√3) |
| 2a | the 14 shadow dice: every edge on a mirror, exactly | **agrees** (14 of 14) |
| 2b | each face covers \|G\|/N mirror triangles, exactly | **agrees** (14 of 14) |
| 2c | the screen: no other catalogued die is a shadow die | **agrees** on 500 random non-hits (0 pass), and also on all 15 178 non-hits |
| 3a | Theorem A plate equation c(a+b)·Σ_{B₁}y + a(b+c)·Σ_{B₃}y = 0, n = 3..7, from the geometry | **agrees** (every ridge, every n) |
| 3b | distinct plates = A402191(n) | **agrees**: 3, 15, 65, 225, 770 |
| 3c | uniform type B: (5ⁿ − 2·3ⁿ + 1)/2 plates, n = 2..5 | **agrees**: 4, 36, 232, 1320 |

All code is new. The original scripts were not imported or copied; the statements were taken from the two READMEs. One exception, stated in item 2: the catalogue stores face directions as indices into a list of 122 directions, and no README gives the order inside each family. That order (a Python set iteration order) was read from six lines of the original groups.py and rebuilt here. It was then validated independently: under it, all 15 192 catalogued dice come out fair to 4.9e-12 by our own solid angles. Each of the eight other natural orders fails (residual 1.7 or more).

## 1. Theorem 1 (CIRT-30): agrees

**Method** (scripts/cirt30_girard.py, logs/cirt30_girard.log, data/cirt30.json). This method differs from the original region tests. The die is C6 (offset 1), RT24/12a (normals the cyclic shifts of (φ, 1/φ, 1) with an even number of minus signs, offset 2, i.e. depth 1) and I12 (normals (0, ±1/φ, ±φ) cyclic, offset s, i.e. depth t = s/√3).
- For rational s, every corner is found exactly in Q(√5): every triple of planes is solved and kept if it satisfies all 30 inequalities.
- Each face's cycle is ordered and checked strictly convex exactly. Euler's formula V − E + F = 2 is checked.
- Each face's solid angle is its spherical polygon's area by Girard's formula (interior angles minus (k − 2)π), in arb ball arithmetic at 600 bits.
- Controls: the faces of each orbit agree, and the total is 4π to 1e-150.

**Identity.** Rigorous enclosure of 2Ω_R − Ω_C − 4π/30:

| s = t√3 | 1.75 (t₀) | 1.751 | 1.758 | 1.76 | 1.8 | 2.0 | 2.5 | 3.0 |
|---|---|---|---|---|---|---|---|---|
| \|value\| ≤ | 5.1e-178 | 7.4e-178 | 7.2e-178 | 7.2e-178 | 6.1e-178 | 3.4e-178 | 1.1e-178 | 1.1e-178 |

In every case the ball contains 0. At s = 2.5 and 3 the I12 faces are absent (20 corners), and the identity still holds there, as the theorem says.

**t₀.** Ω_I(t₀) − 4π/30 = +0.0198895184909686 and Ω_I(1.76/√3) − 4π/30 = −0.00513381071536969. Both agree with the README's +0.019890 and −0.005134. The identity also holds at s = 1.65, 1.70, 1.72 and 1.74, below t₀. It fails at s = 1.6 (−0.0596), 1.5, 1.4 and 1.3 (logs/cirt30_below_t0.log). So t₀ is a valid sufficient bound. The README claims only that the proof stops there, which matches. The identity itself breaks down somewhere in (1.60, 1.65)/√3.

**t\*.** The quartic root is x = 1.75792037676598405848060692086167670298…, so x/√3 = 1.014935802739769241603950729393898891237. Ω_I − 4π/30 is +2.4775e-40 at x − 1e-40 and −2.4775e-40 at x + 1e-40 (rigorous). Ω_I decreases in t (the README's argument), so t* lies within 1e-40/√3 of x/√3. There, Ω_C and Ω_R are within 3e-40 of 4π/30. This agrees with t* = 1.01493580273976… and with t* ∈ (1.75, 1.76)/√3.

## 2. Theorem 2 (shadow dice): agrees

**Exact check of the 14** (scripts/shadow_exact.py, logs/shadow_exact.log, data/shadow_exact.json). Our method is our own:
- *Exact offsets.* Each face's plane offset h_i = d_i·|n_i| (with n_i the unnormalised Q(√5) normal) was recognised in Q(√5) by PSLQ from the catalogue depths. These are 60 digits for studies 11-19 and 11-20 and 14 digits for certify-extend. The recognised values agree with the catalogue to 1e-60 and 1e-11 respectively. Everything after this step is exact; the recognition only has to be correct, and the exact checks below confirm it.
- *Corners and faces.* All corners are found exactly. Every corner satisfies every inequality, and every face cycle is strictly convex. Every edge lies in exactly two faces, and V − E + F = 2.
- *Edges on mirrors.* Both ends of every edge lie exactly on one mirror. The mirrors are 9 for Oh (normals C6, RD12) and 15 for Ih (normals C6 + RT24, or C6 + RT24′ for the second placement).
- *Triangle counts.* The reflection group was generated exactly from its mirrors; its order is 48 or 120, as it should be. Then the orbit of a generic point (1, 3/7, 1/11 + √5/13), which lies on no mirror, gives one interior point in each chamber. Each such ray is assigned to the face it meets first (exact argmax of n_i·x/h_i), and no ties occur. This counts by points, not by areas as the original does.

| die | G | N | corners | triangles per face | (depth ratio)², exact |
|---|---|---|---|---|---|
| 11-19 row 83 | Ih | 20 | 22 | 6 | 1 |
| 11-19 row 89 | Ih | 20 | 12 | 6 | 1, (3+√5)/6 = φ²/3 |
| 11-19 row 787 | Oh | 8 | 8 | 6 | 1 |
| 11-19 row 844 | Ih | 10 | 12 | 12 | 1 |
| 11-20 row 95 | Oh | 48 | 26 | 1 | 1, (5+√5)/8 = cos²18° |
| 2a 272 | Oh | 24 | 14 | 2 | 1, (5+2√5)/10 |
| 2a 273 | Oh | 24 | 14 | 2 | 1, 5/6 |
| 2a 274, 275, 276 | Oh | 24 | 14 | 2 | 1, (25−10√5)/3 |
| 2a 1509 | Oh | 48 | 26 | 1 | 1, cos²18° |
| 2a 3268, 3269 | Oh | 16 | 10 | 3 | 1, cos²18° |
| 2a 3270 | Oh | 16 | 10 | 3 | 1, 3/4 = cos²30° |

In every row the count is |G|/N, so every face subtends exactly 4π/N. Corners, counts and depth ratios all match the original table.

**Screen** (scripts/screen_sample.py with die_num.py; logs/screen_sample500.log, data/screen_sample500.json). This is double precision, like the original.
- *Sample.* 500 non-hits were drawn at random (seed 20261124) from the 15 178.
- *Test.* For each die we rebuilt the corners and edges. An edge counts as on a mirror when both unit ends are within 1e-7 of one mirror plane; a die passes for G when all its edges do. This was tested for Oh, Ih and the second Ih placement.
- *Result.* 0 of 500 pass. The smallest miss is 9.9e-2. The 14 hits all pass (largest miss 3.5e-12), which is the positive control.
- *Extra run.* The same test on all 15 178 non-hits (logs/screen_all.log, data/screen_all.json.gz) also gives 0 passes. The smallest miss is 2.4e-2 (11-19 row 251), so the margin is large.

Our miss measure is the edge-to-mirror distance only, so it is not the same number as the original's 9.2e-3 (which also counts corner-to-axis distance). Both measures give the same verdict. Our own solid angles make all 15 192 dice fair to 4.9e-12.

## 3. A402191 Vacuus: agrees

**Type A** (scripts/vacuus_check.py A, logs/vacuus_A.log). For n = 3..7:
- *Facets.* The n! vertices are listed. Each inequality Σ_S x ≥ |S|(|S|+1)/2 was tested on every vertex. Each tight set was checked to have rank n − 1, so each is a facet.
- *Ridges.* Ridges are the pairs of facets whose common vertices have rank n − 2 (centred coordinates). Their numbers are 6, 36, 150, 540 and 1806, which equal 3ⁿ − 3·2ⁿ + 3. Every ridge is tight for exactly two of the listed facets, so the facet list is complete.
- *Plates.* Each plate was solved from the ridge's own vertices, as the null space of the ridge's vertex vectors together with (1, …, 1).
- *Equation.* For every ridge, the plate equals the stated plane c(a+b)·Σ_{B₁}y + a(b+c)·Σ_{B₃}y = 0. Here B₁ is the smaller facet's set, B₂ the difference, and B₃ the rest.
- *Counts.* There are 3, 15, 65, 225 and 770 distinct plates. A402191 (OEIS, fetched 24 Nov, data/A402191.txt, offset 3) begins 3, 15, 65, 225, 770, 2443, …, so they agree. For n = 7 the plates carry 2, 6 or 20 ridges, as stated.

**Type B, uniform** (scripts/vacuus_check.py B, logs/vacuus_B.log). For n = 2..5 everything is exact in Q(√2), with values λ_k = 1 + (n − k)√2.
- *Facets.* The 2ⁿ·n! signed-permutation vertices are listed. All 3ⁿ − 1 signed-subset inequalities were tested on every vertex, and each is a facet (rank n).
- *Ridges.* Ridges are the facet pairs whose common vertices have rank n − 1. There are 8, 72, 464 and 2640 of them, which equals 5ⁿ − 2·3ⁿ + 1.
- *Plates.* Each plate is the null space of its ridge's vertices. There are 4, 36, 232 and 1320 distinct plates, which equals (5ⁿ − 2·3ⁿ + 1)/2.
- *Pairs.* Every plate carries exactly one ridge and its opposite (vertex set negated).

## Sources checked

- READMEs of studies 2026-11-24-aequi-exact-dice and 2026-11-24-a402191-vacuus (the statements); README of 2026-11-19-aequi-complete (the frame directions).
- Catalogue data: 2026-11-19-aequi-complete data/dice, 2026-11-20-aequi-two-placements data/aequi.json, 2026-11-24-aequi-certify-extend data/aequi2*.json.gz; 2026-11-24-aequi-exact-dice data/shadow_hits.json (the 14 hits).
- OEIS A402191.
- Methods: Girard's theorem for spherical polygon area; PSLQ (Ferguson–Bailey) through mpmath; arb ball arithmetic (Johansson) through python-flint 0.9.0.

## LEADS

1. The CIRT-30 identity holds for s down to 1.65 at least and fails by s = 1.60. A finer mirror region could push Theorem 1 down to that threshold (this is LEAD 1 of the original study, now with a target interval).
2. The chamber-point count of item 2 is exact and quick (no areas). It could replace the ball-arithmetic area step in prove_shadow.py.

## Files

- scripts/: qr.py (exact Q(√r)), cirt30_girard.py, dirs.py (122 exact directions and catalogue loader), calibrate_order.py, die_num.py, shadow_exact.py, screen_sample.py, vacuus_check.py.
- data/: cirt30.json, calibrate_order.json, shadow_exact.json, screen_sample500.json, screen_all.json.gz, A402191.txt.
- logs/: one per run (FINAL ok where the script prints one).

Each run took under five minutes on one core of a compute host.
