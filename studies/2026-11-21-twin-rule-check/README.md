# Twin rule check, 21 Nov 2026
Rule tested: "two golden cuts of a solid are Galois twins exactly when some field automorphism sends K to -K".
Script: scripts/twin_rule_check.py (exact sympy); log: data/twin_rule_check.log (ends FINAL ok); table: data/table.json.
Twins = some automorphism maps the greater cut exactly onto the lesser (all depths). K = k (corner-side factor) for Platonic and Kepler-Poinsot solids, #89 Thm 3's K for RD and RT.

| solid | field | K | some sigma: K -> -K | ... with sqrt5 -> -sqrt5 too | twins |
|---|---|---|---|---|---|
| Dodecahedron | Q(sqrt5) | phi | no | no | no (greater 1/3 fixed; sigma(lesser) = phi^3 cut) |
| Icosahedron | Q(sqrt5) | 1 | no | no | no (conjugates over-cut) |
| Cube | Q(sqrt2,sqrt5) | sqrt2 | yes | yes | yes |
| Tetrahedron | Q(sqrt5) | 1 | no | no | no |
| Octahedron | Q(sqrt5) | 1 | no | no | no |
| Rhombic dodecahedron | Q(sqrt2,sqrt3,sqrt5) | (2sqrt3+sqrt6)/4 | yes (2 maps) | yes (1 map) | yes (that map) |
| Rhombic triacontahedron | Q(s), s^2=(5+sqrt5)/2 | phi s/2 | YES (s -> -s, sqrt5 fixed) | no | no |
| Great dodecahedron, great icosahedron | as dodecahedron, icosahedron | phi, 1 | no | no | no |
| Small, great stellated dodecahedron | Q(sqrt5) | 1/phi | no | no | no |

Controls (cube, RD, RT) reproduce the earlier results. Not tested: icosidodecahedron and snub dodecahedron (#89 Thm 2: golden-or-regular cuts, no K defined).

Verdict: the rule as worded holds on every solid except the rhombic triacontahedron. Counterexample: s -> -s (fixing sqrt5) sends K = phi s/2 to -K, yet the conjugate cuts have negative depths (no solid) and are not the other cut. It holds on all 11 solids when the automorphism must also negate sqrt5 (the map that sends phi to -1/phi, i.e. the one that exchanges the two cut formulas b = 1/(1+phi K) and 1/(1+K/phi)): "sigma(K) = -K and sigma(sqrt5) = -sqrt5".
