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

## Step 2: what is extremal at the turn (ab_extremal.py, FINAL ok)

**Theorem (extremal at the turn).** On the AB line, per window area 1 + 4t + 2t², the tiles occur as: squares with edges at 0°/90°
in proportion 1, squares at 45°/135° in proportion 2t², each of the four rhombus types in proportion t (window area of the
complementary pair, the classical frequency formula of cut-and-project tilings). Hence
(1) the four edge directions occur in the ratio (1+2t) : (2t+2t²) : (1+2t) : (2t+2t²): all four equally often exactly at t = 1/√2,
    and the turn swaps the two ratios (each partner has the reciprocal);
(2) squares per rhombus, f(t) = (1+2t²)/(4t) = 1/(4t) + t/2, is invariant under the turn and smallest exactly at t = 1/√2
    (f′ = −1/(4t²) + 1/2 = 0 ⇔ t² = 1/2), with value 1/√2, the Ammann–Beenker ratio 1 : √2.
So the quasicrystal is the one member of the line with all edge directions balanced and the most rhombi: the same pattern as the
Turn Theorem (a quantity extreme exactly at the fixed point of the turn).

**Check against the tilings.** The edge-direction frequencies, counted from the raw vertex stars of T(t) in exact rationals, match (1)
at all 11 slopes from 0.55 to 0.9; the diagonal/axis ratio passes 1 between 12/17 (0.998565) and 17/24 (1.001437). (2) follows
from the tile proportions, which (1) confirms through their edges.

**Next (step 3):** the same on the Fibonacci/Sturmian line (1D cut-and-project with slope α; turn and fixed point at the golden
mean); then step 4, the 3D golden rhombohedra.
