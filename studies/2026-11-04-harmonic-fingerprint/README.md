# Harmonic fingerprint (2026-11-04)
DICTO: "start the harmonic fingerprint test" (Concordance 5.5, spherical harmonics find: Steinhardt–Nelson–Ronchetti 1983).
Method: Q_l and W_l-hat of a solid's corner directions, l = 4…12 (scripts/fingerprint.py, dicto-big-brother, data/fingerprint.log/json).
Validation: CO (fcc) .191/.575, J27 (hcp) .097/.485, bcc .036/.511, icosahedron Q4 0 Q6 .663 = the classical values.

## Results
1. On the sweep P_mu = C ∩ muC* (octahedron mu=1 to cube mu=3) the cubic part Q4 vanishes at exactly one point, Icosaxes mu = φ, and Q8 with it.
   Exact: for 1<mu<2 the corners are perms of (1, a, 0), a = mu-1; Q4 = 0 iff a^4 - 3a^2 + 1 = 0 iff a = 1/φ, mu = φ.
   For 2<mu<3 (corners perms of (1,1,b)) the condition b^4 - 6b^2 - 1 = 0 has no root in (0,1). Reason: Icosaxes' 24 corners are two icosahedra
   (cyclic perms of (0, ±1, ±1/φ) in both orders), so its harmonics are icosahedral up to l = 8: the one cubic solid on the sweep that "sounds" icosahedral.
2. Q6 vanishes at mu = 1 + a, a^2 = (17 - sqrt273)/4 (mu ≈ 1.3454) and at mu ≈ 2.4239 (a^6 - 15a^4 + 75a^2 - 13 = 0): near but not at Unborn Axes (1.382) and the truncated cube (2.414). No station.
3. Dual pairs: dodecahedron and icosahedron have the same |W6| with opposite sign (+0.1698 / -0.1698): the l = 6 invariant tells corner-type from face-type directions.
4. Even l cannot see inversion: tetrahedron = cube, RD = bcc shell in every Q_l. The tetrahedron's "antiparticle" -T needs odd l (l = 3).
## LEADS
- Fingerprint of the golden nests and OG shells (corner sets from the engine) — Q6 of the nests against Mackay/Bergman clusters.
- Odd-l fingerprint (l = 3, 7, 9) for the tetrahedral and chiral pieces.
- Q4 = 0 as a test for "icosahedral inside cubic" on other walks (Delian walk, #51; the golden cuts of #88/#89).

## Delian walk (#51), 4 Nov — harmonic test in its competence (icosahedral order hidden in cubic)
O(t) = RD cut at its 3-fold corners (planes s·x = 3(1−t)/2), T(t) = the tetrahedral piece (#93 pairing_checks.py definitions).
- O(t): Q4 = 0 exactly at t = 1/9 (factor (t − 1/9) of the exact sum over the 30 corners (±1,0,0), ((1+3t)/2, (1−3t)/2, (1−3t)/2)); Q8 = 0 near t ≈ 0.095 and 0.205 — not together.
- T(t): Q4 never zero; Q6 zero near t ≈ 0.560 and 0.774.
So the Delian walk has no hidden icosahedral station (unlike Icosaxes on the cube–octahedron sweep); its cubic tone is silent once, at the rational point t = 1/9.
