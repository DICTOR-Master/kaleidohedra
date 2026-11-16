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

## Step 3: the Fibonacci line and its hop (fib_hop.py, FINAL ok; DICTO chose option A)

**Theorem (the hop).** On the Sturmian line (s = short tiles per long tile; rational s a crystal, s = 1/φ the Fibonacci
quasicrystal) the Fibonacci substitution L → LS, S → L carries the crystal at s to the crystal at h(s) = 1/(1+s) (checked exactly for
all 489 rational slopes with period ≤ 40, up to a cyclic shift). h has the single fixed point 1/φ and carries the approximants
F(n−1)/F(n) → F(n)/F(n+1), closing in on 1/φ from alternating sides. A line without the 8-fold symmetry has no turn; its
quasicrystal is the fixed point of a hop instead.

**Extremal at the fixed point (classical).** By Hurwitz (1891) every irrational x has q²|x − p/q| < 1/√5 for infinitely many
fractions, and 1/√5 is attained only by the golden class: the Fibonacci quasicrystal is the point of its line farthest from every
crystal. By Markov (1879–80) the next value is 1/√8, the class of √2, which contains the AB turning point 1/√2. Measured on the
convergents: 0.4472136 (1/φ) and 0.35355339 (1/√2).

**Two kinds of turning point.** With symmetry (AB, 8-fold): the quasicrystal is the fixed point of a turn, an involution pairing
crystals across it, and turn-invariant quantities are extreme there (step 2). Without symmetry (Fibonacci): it is the fixed point
of a hop, a contraction carrying each crystal to the next. The two fixed points are the first two points of Markov's spectrum.

## Step 4: the icosahedral line (ico_line.py, FINAL ok)

**Theorem (the icosahedral hop).** With physical star P(x) = [(1,x,0), (−1,x,0), (0,1,x), (0,−1,x), (x,0,1), (−x,0,1)] (x = φ the
icosahedral quasicrystal of golden rhombohedra; x = F(n+1)/F(n) = 1/1, 2/1, 3/2, 5/3 … the cubic approximants), the integer matrix
A = [[2,1,1,−1,1,−1], [1,2,1,−1,−1,1], [1,1,2,1,1,1], [−1,−1,1,2,1,1], [1,−1,1,1,2,−1], [−1,1,1,1,−1,2]] (det −1, a map of Z⁶)
satisfies P(x)·A = (2x+1)·P(g(x)) identically in x, with g(x) = (3x+2)/(2x+1) = h(h(h(x))), h the Fibonacci hop. g has the single
fixed point φ (scale 2φ+1 = φ³, the classical inflation of the primitive icosahedral lattice) and hops every third approximant:
2/1 → 8/5 → 34/21, 3/2 → 13/8 → 55/34, 5/3 → 21/13 → 89/55. A was found as the unique solution with physical scale φ³ and internal
scale (−1/φ)³ (Galois pair), then checked on the whole line symbolically.
Not yet checked: that the 3D tilings themselves (not only the projection data) are related by inflation along the line.

**Verdict for aim 1 so far.** Ammann–Beenker (8-fold) sits at a TURN; Fibonacci and the icosahedral quasicrystal (no cubic or
1D symmetry to turn by) sit at HOPS, the icosahedral one at the third power of the Fibonacci hop. Next: the tile-level check in 3D,
and an extremal property at the icosahedral fixed point (the analogue of steps 2 and 3).

## Step 5: the icosahedral line at tile level, and what is extreme at φ (ico_tiles.py, ico_extremal.py, both FINAL ok; 16 Nov 2026)

**Setting.** The scheme at x: lattice Z⁶, physical map P(x) (step 4), internal map Q_x = P(−1/x) (its rows are orthogonal to those of
P(x): P(x)·P(y)ᵀ = (2 + 2xy)·I), strip direction E(x) = row space of P(x), window W_x = Q_x([−½, ½]⁶) (a zonohedron). T(x, w) is the
canonical cut-and-project tiling with lifted vertex set L(x, w) = {n ∈ Z⁶ : Q_x n ∈ W_x + w}, w a generic shift. Rational x gives a crystal,
x = φ the icosahedral quasicrystal of golden rhombohedra. k(x) = −x/(3x + 2), g(x) = (3x + 2)/(2x + 1) as in step 4.

**Theorem 5a (the hop at tile level).** For every x > 0:
(i) Q_g(x)·A = k(x)·Q_x, alongside step 4's P(x)·A = (2x + 1)·P(g(x)). So A carries the lattice and strip of T(x) onto those of
    T(g(x)), and A·L(x, w) = {m ∈ Z⁶ : Q_g(x) m ∈ k(x)(W_x + w)}. The inflated crystal at x is the model set of the next strip, with window
    k(x)·W_x.
(ii) |k(x)|·W_x ⊂ W_g(x). Hence A·L(x, w) ⊂ L(g(x), k(x)w): every vertex of the inflated crystal at x is a vertex of the crystal at g(x).
    These vertices are the fraction |k|³ vol W_x / vol W_g(x) of all its vertices (φ⁻⁹ at φ).
(iii) A maps the period lattice of T(x) onto that of T(g(x)). Drawn with P, the periods of T(g(x)) are s(x) times those of T(x), with
    s(x) = (2x + 1)(1 + g(x)²)/(1 + x²) (s(φ) = φ³). The vertices follow the s(x)-inflation up to a bounded phason displacement:
    P(g)A − s·P(x) vanishes on E(x), so the displacement is linear in the internal coordinate. It is zero only at φ.
(iv) |k(x)|·W_x is a homothetic copy of W_g(x) only at x = φ. The window generator (1, −1/x, 0) fixes x, and −1/x = −1/g(x) only at φ.
So off φ, T(g(x)) is not the inflation of T(x). The inflated crystal is a proper sub-selection of the next crystal, with a window of a
different shape. Only at φ does the window return to itself (−φ⁻³W ⊂ W, the classical self-similarity of the icosahedral model set).

**Proof.** (i) is an identity in x (symbolic). (ii) A convex body lies in a zonohedron iff its support function is at most the zonohedron's at
every facet normal. The facet normals of W_g are the 15 products q_i × q_j of its generators, and the support function of a zonohedron is
½Σ|u·q_l|. Both sides are piecewise rational in x. An exact sign analysis on every interval between the sign changes, for all x > 0, gives
strict inequality throughout. The largest λ with λ|k|W_x ⊂ W_g is 203/100 at x = 1/100, 93/29 at 1/2, 49/13 at 1, 337/81 at 3/2,
4 at 2, 21/5 at 5/3, 151/50 at 100 and φ³ at φ. The inclusion follows: n ∈ L(x, w) gives Q_g(An) = k·Q_x n ∈ k(W_x + w) ⊂ W_g + kw. The
density follows from Q_g(Z⁶) = k·Q_x(Z⁶). (iii) A is unimodular and symmetric, so A·E(x) = E(g(x)) and A(Z⁶ ∩ E(x)) = Z⁶ ∩ E(g(x)).
(iv) A zonohedron with pairwise non-parallel generators determines its generators up to sign. ∎

**What is proved, exactly.** (i)–(iv) hold for every x > 0. This is a match of the actual vertex sets and windows: a one-sided inclusion
with an exact window and density, not only the lattice data. **Not true:** equal tile or vertex frequencies (the analogue of step 1).
The tile proportions of T(x) and T(g(x)) differ, for example T(2) has volume classes 4 : 7 : 8 : 9 in counts 24 : 28 : 48 : 36, and T(8/5)
has 1548 : 2548 : 3840 : 2400 for the volumes 387/125, 637/125, 128/25 and 16/5. The proportions agree only in the limit φ.
**Not tested:** mutual local derivability. For crystals it holds through the shared period lattice, so it says nothing here. At φ the
inclusion A·L ⊂ L is the classical inflation of the vertex set; whether T(φ) and its φ³-inflation are mutually locally derivable was not
re-derived here.

**Checks** (ico_tiles.py). Exact enumeration per primitive period for 1/1 → 5/3 (16 → 1220 vertices), 2/1 → 8/5 (136 → 10336),
3/2 → 13/8 (576 → 43784), 5/3 → 21/13 (1220 → 92736), and off the Fibonacci chain 1/2 → 7/4 (136 → 6440). For each pair:
- vertex count = vol W / covolume of the internal lattice;
- every vertex n of T(x), lifted to Z⁶, has A·n a vertex of the independently enumerated T(g(x)) (computed from A·n, not from (i));
- the density formula holds;
- A carries periods to periods, the periods scale by s(x), and the cell volume ratio is s³;
- tile counts of all 20 types, from the face criterion of Oguey–Duneau–Katz, equal |det Q_(I^c)|/covolume and are proportional to tile
  volume; total tile volume = cell volume.
The vertex ratios 76.25, 76, 76.01, 76.01 approach φ⁹ = 76.013. Controls:
- positive: the turn below maps L(2) onto L(1/2) exactly (136 = 136);
- negative: A carries a period of T(x) out of the strip of h(x) (one Fibonacci hop) and of g(g(x)) (pairing with the wrong crystal fails);
- negative: the all-x containment routine run with 5|k| in place of |k| reports failure, as it must.

**Found on the way: the icosahedral line also has a turn.** x·P(1/x) = R·P(x)·S, with R swapping the first two coordinates and S a signed
permutation of Z⁶. Also Q_1/x = −x·R·Q_x·S. So T(1/x) is the mirror image of T(x) (S⁻¹L(x, w) = L(1/x, −xRw), checked equal at x = 2).
The turn x ↦ 1/x fixes x = 1, the 1/1 crystal (cubic, symmetry order 48), and pairs the two golden points φ and 1/φ, which are one
quasicrystal and its mirror image. This refines step 4's verdict. The icosahedral line does have a turn, but its fixed point is a crystal.
The quasicrystal sits at the hop g (fixed point φ), not at the turn.

**Theorem 5b (what is extreme at φ).**
(1) *Symmetry.* The signed permutations of the six edge directions that preserve the Gram matrix of P(x) are the point symmetries of the
    whole scheme (star, window and lattice). They form a group of order 24 for every x > 0 except x = 1 (order 48) and x = φ, 1/φ
    (order 120, icosahedral). The Gram entries ±x, ±(x² − 1) and 1 + x² coincide up to sign only at 1/φ, 1 and φ, so the group can change
    only there. The six edge directions are equiangular exactly at x = φ and 1/φ (|x² − 1| = x).
(2) *Tiles.* The 20 rhombohedra fall into four volume classes: 2x² (6 types), 1 + x³ (4), 2x (6) and |x³ − 1| (4). Every type occurs with
    frequency proportional to its volume, because |det P_I| = x³·|det Q_(I^c)|: orthogonal complements have equal Plücker coordinates on
    complementary index sets. With the window-volume frequency rule this gives the proportionality. Only at x = φ and 1/φ do the twenty
    types take just two volumes with none flat. These are the 10 prolate and 10 oblate golden rhombohedra, with frequency ratio φ per
    type. At x = 1 the volumes are 2, 2, 2 and 0 (one class flat and absent). Everywhere else there are at least three volumes.
(3) *Farthest from every crystal, in 3D.* At x = φ every nonzero n ∈ Z⁶ satisfies |π(n)|·|π⊥(n)| ≥ ½, where π and π⊥ are the orthogonal
    projections to physical and internal space. Equality holds for the unit vectors and for all their images A^j e_i, which are infinitely
    many (|n|² = 1, 9, 161, 2889, 51841, …). The inflation A keeps the product fixed (×φ³ and ×φ⁻³): a hop-invariant quantity, as the
    turn-invariant f(t) was in step 2. At every crystal the product is 0 on its periods. So at φ no lattice vector of physical length L comes
    closer than 1/(2L) to physical space, while at a crystal the periods lie in it.

**Proof of (3).** The coordinates of P(φ)n are a_i + φb_i with integers a_i, b_i. So α = |P(φ)n|² ∈ Z[φ], and its Galois conjugate is
|Q n|². Hence |Pn|²·|Qn|² = N(α), a positive integer. Since P(φ)ᵀP(φ)/(2√5 φ) + Q(φ)ᵀQ(φ)·φ/(2√5) = I, the product is
|π n||π⊥ n| = √N(α)/(2√5). A multiplies α by the unit φ⁶, so N is A-invariant. Applying a power of A brings α/σ(α) into [φ⁻⁶, φ⁶];
then |n|² ≤ φ³√N/2. So N ≤ 4 would need |n|² ≤ φ³ < 5. The 484 nonzero n with |n|² ≤ 4 all have N ≥ 5, with N = 5 at e_1, giving ½. ∎
(1) and (2) are proved symbolically: case analysis of the Gram entries and of all set partitions of the four volume classes (Gröbner bases).

**Open.** (a) Whether T(φ) is mutually locally derivable from its φ³-inflation (classical statements exist; not re-derived here).
(b) Whether φ maximises the asymptotic constant liminf over |n| → ∞ of |π_x(n)||π⊥_x(n)| over the whole line (a full 3D Hurwitz theorem
along the line). (3) proves only the value ½ at φ and the value 0 at the crystals.

**Credit.** The line, the turn and hop reading, and the aim "the quasicrystal is the turning point of a line of crystals" are DICTO's.
- Cut-and-project and canonical windows: de Bruijn (1981), Duneau–Katz (1985), Elser (1986), Katz–Duneau (1986, icosahedral).
- Icosahedral tiling of golden rhombohedra: Kramer–Neri (1984), Ogawa (1985), Socolar–Steinhardt (1986).
- Cubic rational approximants: Elser–Henley (1985).
- Face criterion for tiles: Oguey–Duneau–Katz (1988).
- Frequencies from window volumes and self-similar windows: Baake–Grimm, Aperiodic Order I (2013).
- Plücker duality of orthogonal complements: classical.
- The 1D model of (3): Hurwitz (1891).

**Sources checked.** This study's steps 1–4. The reference library's records (study 2026-11-03-reference-library) for the works above.
The notes of study 2026-11-13-golden-slice-window, where Baake's 1999 guide was read. The works named above were not re-read in this
step: they are credited for the methods used, and nothing here rests on a statement quoted from them.

**LEADS.**
- Prove or refute mutual local derivability of T(φ) with its φ³-inflation, via the window algebra: is W in the Boolean algebra generated
  by lattice translates of φ⁻³W?
- The 3D Hurwitz question along the line ((b) above): compute the least |π_x n||π⊥_x n| over non-periods for the approximants and for
  badly approximable x such as √2.
- Turn and hop together generate a group acting on the line (x ↦ 1/x, g). Describe it, and ask whether the AB line also has a hop.
- The φ⁹ vertex ratio of consecutive hops (76.25, 76, 76.01, 76.01) as an exact function of x: |k|³ vol W_x / vol W_g(x).

**Ready Concordance ledger lines**

```json
{"question": "Aim 1 step 5a: is the icosahedral hop g = h^3 an inflation of the actual 3D tilings T(x) -> T(g(x)), not only of the projection data", "method": "exact: symbolic Q_g A = k Q_x, k = -x/(3x+2); window containment |k|W_x in W_g for all x > 0 by support functions at the 15 facet normals with exact sign analysis; exact enumeration of vertices and the 20 tile types per period for 1/1->5/3, 2/1->8/5, 3/2->13/8, 5/3->21/13, 1/2->7/4; controls: turn x -> 1/x (positive), h(x), g(g(x)) strips and 5|k| containment (negative) (studies/2026-11-10-ab-line, ico_tiles.py)", "status": "SETTLED", "result": "PROVED for all x > 0: A L(x) = model set of the strip of g(x) with window k(x)W_x, and |k|W_x is inside W_g(x), so every vertex of the inflated crystal at x is a vertex of the crystal at g(x) (density |k|^3 vol W_x / vol W_g, phi^-9 at phi; vertex ratios 1220/16, 10336/136, 43784/576, 92736/1220 -> phi^9); periods scale by s(x) = (2x+1)(1+g^2)/(1+x^2); window shapes equal only at phi, so off phi T(g(x)) is not the inflation of T(x) and frequencies differ; found: the line has a turn x -> 1/x (T(1/x) = mirror of T(x)) fixing the 1/1 crystal; MLD not tested", "retry": "never; only MLD of T(phi) with its phi^3 inflation remains", "study": "studies/2026-11-10-ab-line", "date": "2026-11-16"}
{"question": "Aim 1 step 5b: what is extremal at the icosahedral fixed point phi of the line", "method": "exact sympy: signed permutations preserving the Gram matrix of P(x); tile volumes and Pluecker duality |det P_I| = x^3 |det Q_(I^c)|; set partitions of the four volume classes by Groebner bases; norm form N(|P(phi)n|^2) in Z[phi] with A-balancing and exhaustion of |n|^2 <= 4 (studies/2026-11-10-ab-line, ico_extremal.py)", "status": "SETTLED", "result": "PROVED: symmetry order 24 for all x > 0 except 48 at x = 1 and 120 exactly at phi, 1/phi (six directions equiangular only there); tile frequency proportional to tile volume, four classes 2x^2, 1+x^3, 2x, |x^3-1| that reduce to two non-flat volumes (golden prolate/oblate, ratio phi) only at phi, 1/phi; at phi every nonzero n in Z^6 has |pi n||pi_perp n| >= 1/2, equality on the A-orbits of the unit vectors (A-invariant), crystals give 0. OPEN: whether phi maximises liminf |pi_x n||pi_perp_x n| over the whole line", "retry": "only the full 3D Hurwitz question along the line", "study": "studies/2026-11-10-ab-line", "date": "2026-11-16"}
```
