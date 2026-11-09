# The Ammann–Beenker line: the quasicrystal is the turning point of a line of crystals (aim 1, step 1; 10 Nov 2026)

**Theorem (the turn on the AB line).** Let T(t) be the canonical cut-and-project tiling from Z⁴ with physical star
e_k = (cos kπ/4, sin kπ/4) and window vectors ε(t) = (−t, t), (1, 0), (−t, −t), (0, 1) (study 2026-11-09-ab-turn). For rational t,
T(t) is periodic (a crystal); T(1/√2) is the Ammann–Beenker quasicrystal. Then T(t) and T(1/(2t)) are the same tiling turned by 45°.
The turn t ↦ 1/(2t) has the single positive fixed point 1/√2, and it exchanges the Pell approximants pairwise across it.

**Proof.** The 45° rotation R maps e_k to e_{k+1}. The map (1/(√2 t))·R maps ε_k(t) to ±ε_{k+1}(1/(2t)) for k = 0..3 (direct
computation). So the basis shift k → k+1 with signs, a lattice automorphism of Z⁴, carries the scheme at t onto the scheme at
1/(2t), turned by 45° and rescaled; sign changes translate the window, which keeps the local patterns and their frequencies. ∎

**Checks** (ab_turn_check.py, FINAL ok): (1) the map, symbolically; (2) for the Pell pairs 2/3 ↔ 3/4, 5/7 ↔ 7/10,
12/17 ↔ 17/24, 29/41 ↔ 41/58 the six vertex stars have exactly equal frequencies (rational arithmetic, zono.py). The pairs straddle
1/√2 at distances −0.0404/+0.0429, +0.0072/−0.0071, −0.0012/+0.0012, +0.00021/−0.00021.

**Credit.** The Hopscotch, the turn, and the aim "the quasicrystal is the turning point of a line of crystals" are DICTO's.
Ammann–Beenker tiling: R. Ammann, B. Grünbaum, G. C. Shephard (1992); F. P. M. Beenker (1982); cut-and-project: de Bruijn (1981),
Duneau–Katz (1985). Pell approximants of AB are classical (e.g. Baake–Grimm, Aperiodic Order I).

**Next (step 2):** an extremal property at the turn, as in the Turn Theorem (t_min largest at the fixed point): which quantity of
T(t) is extremal exactly at 1/√2? Candidates: isotropy (8-fold balance of edge directions), the spread of the star frequencies, the
diffraction's Bragg-peak concentration. Then step 3: Fibonacci/Sturmian line; step 4: 3D golden rhombohedra.
