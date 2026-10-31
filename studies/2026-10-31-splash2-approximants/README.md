# Splash Rules II: quasicrystal approximants (DICTO 2026-10-31)

**DICTO's idea (Splash Rules, 27 Oct):** plot a whole family of exactly computed values and look for one simple rule that covers
the known local ones. Third outside run (after perovskites and Frank–Kasper), aimed at DICTO's long-term aim, the bridge between
periodic and aperiodic order: periodic approximants converging to a quasicrystal.

**Conclusion:** one number orders the approximants, the share of one tile (S in 1D, squares in Ammann–Beenker, prolate in 3D).
On the chamber of approximants that holds the quasicrystal every count is a straight line in it and the quasicrystal lies on every
line; window-2 counts need no second number because approximants are exactly the patterns with the Window Law's defect term at
zero. The defect lives only beyond the chamber walls: in 1D a kink equal to twice the Swap defect, in 2D a forbidden vertex star
growing as a square, 2(3a − 2b)² or (4a − 3b)², with a fixed transfer vector on the other counts. It does not shrink towards the
limit; inside the chamber it is already zero, and only the phason strain (distance along the line) shrinks.

**Status:** done (1D and 2D counts, 3D tile counts). Not run, decided: Penrose rhombus approximants (2D covered by AB), 3D vertex
types (3D acceptance arrangement; only if DICTO wants it).

## Method
- scripts/qf.py: exact arithmetic in Q(√d) (exact sign, floor). scripts/zono.py: integer kernels (unimodular column reduction),
  zonogons, exact polygon clipping, acceptance-domain arrangement, lattice points in a zonogon.
- 1D, scripts/sturm.py: mechanical words s_n = ⌊(n+1)a + r⌋ − ⌊na + r⌋ (S = 1, L = 0, a = share of S), r = 1/(2q) generic. All 1101
  fractions p/q, q ≤ 60; windows g = 1..9; checks: balanced, complexity min(g+1, q), counts = interval lengths, ≤ 3 frequencies;
  Farey-cell linearity (exact), kink vectors, Fibonacci limit 1/φ² in Q(√5), convergent rule (g ≤ 300), phason-strain identity,
  all 747 primitive periodic words up to 12 letters in the (a, p_SS) plane.
- 2D, scripts/ab.py (+ ablaw.py, abfam.py): Z⁴, AB star; rational plane → period lattice Λ = Z⁴ ∩ E′, integer quotient map Z⁴ → Z²
  with kernel Λ; one period of vertices = integer points of a zonogon with integer edges (generic offset, 3 offsets per plane);
  stars classified up to D8; tiles counted from vertices; edges by end-star pair; offset averages = exact arrangement areas.
  Square approximants t = a/b (rows (b, a, 0, −a), (0, a, b, a)), 1/2 ≤ t ≤ 1, b ≤ 40 (246) + Pell ones to 99/140; 240 random
  planes of the same orientation. AB limit in Q(√2).
- 3D, scripts/ico.py: Z⁶, icosahedral star; φ → F(k+1)/F(k) for 1/1 … 55/34; tile counts = |3×3 minors| of Λ; sign check.
- scripts/figs.py (matplotlib, dicto-big-brother): fig/splash2-approximants.png, fig/patches.png. All runs on dicto-big-brother
  (~/studies/splash2-approximants), seconds each.

## Results (data/*.log, data/*.json)
| law | exact on | status |
|---|---|---|
| 1D: window-g frequencies are lines in a between Farey fractions of order g (kinks exactly there); ≤ 3 values; complexity g+1 | 1101 approximants, g ≤ 9 | classical (Morse–Hedlund 1940; Berthé 1996; three-distance) |
| 1D: Fibonacci frequencies on these lines (Q(√5)); F(n−2)/F(n) on the window-g line iff g < F(n+2); deviation = slope × (p/q − 1/φ²) | g ≤ 300 / g ≤ 9 | known in substance; statement not found |
| 1D: approximants = lower edge p_SS = max(0, 2a − 1) of the Window-Law plane; kink at 1/2 = 2 × Swap defect (LL +2, LS −2, SL −2, SS +2) | 747 words | elementary; ours as framing |
| tiles per period = Plücker coordinates; vertices = tiles | every plane and offset | classical |
| AB, square approximants 2/3 ≤ t ≤ 3/4: F = Q, E = 2R − 2Q, D = −4R + 6Q, C = 10R − 14Q, B = −12R + 17Q, A = 5R − 7Q; no other star; AB values on every line; 9 edge-pair kinds also linear | 42 approximants (+ Pell) | Pell-sequence counts known (Jagannathan–Duneau 2023, Table 1); chamber law not found, new |
| AB walls 2/3, 3/4; defect star (two squares side by side) X = 2(3a−2b)² (t<2/3), (4a−3b)² (t>3/4) per N_u = b²+4ab+2a²; counts = chamber line + κX, κ(F,E,D,C,B,A,def) = (0,0,−1,+2,−3,+1,+1) | 246 approximants, 1722 counts | not found, new |
| AB non-square planes: star counts depend on the offset | 229 of 240 | known in substance (phason flips) |
| 3D cubic cell: prolate 4(p³+3p²q+q³), oblate 4(p³+3pq²−q³); 1/1 = 20+12, 2/1 = 84+52, 3/2 = 356+220; prolate share F(3k+2)/F(3k+3) | 9 approximants | formula not found; method classical |

## Prior art — sources checked (31 Oct 2026)
- Reference library (ask-library, 7 queries: Sturmian factor frequencies three distance; periodic approximants cut and project;
  AB vertex configuration frequencies; Penrose vertex types de Bruijn; phason strain approximant linear; icosahedral cubic approximant
  1/1 prolate oblate; Christoffel balanced words). Read: Kléman 2013 (pp. 1–5); Baake 1999 guide (§13 and refs); Hann–Socolar–
  Steinhardt 2016 (p. 3). Catalogue only: Goldman–Kelton 1993; Yamada et al. 2021; de Bruijn 1981; Fujita et al. 2013; Kramer 2011;
  Akiyama et al. 2026.
- Web: Berthé 1996 TCS 165:295–309 (bibliographic entry + citing surveys, full text not read); A. Jagannathan, M. Duneau,
  arXiv 2308.07701 (read §§2.2, 3, 3.1, 3.2; Table 1 = our Pell counts); summaries of arXiv 1009.0136, 2212.09406; two searches on
  1/1 tile counts (no source; summaries of cond-mat/0402370, 2108.03341, cond-mat/0405298).
- In-house: #69 (Fibonacci stacking; built on, not repeated), Splash Rules II perovskite and Frank–Kasper runs.
- Cited, not read: Morse–Hedlund 1940; Lothaire; Baake–Grimm 2013; Duneau–Mosseri–Oguey 1989; Elser–Henley 1985; Katz 1988.

## Files
scripts/ qf.py zono.py sturm.py ab.py ablaw.py abfam.py ico.py figs.py; data/ sturm.json/.log, ab.json, ablaw.log, abfam.json/.log,
ico.json/.log; fig/; results/paper.html → results/splash2-approximants.pdf (also ~/Documents/papers-to-read/splash2-approximants.pdf).
