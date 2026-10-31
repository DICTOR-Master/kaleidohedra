# Splash Rules II: perovskite polytypes (DICTO 2026-10-31)

**DICTO's idea (Splash Rules, 27 Oct):** plot a whole family of exactly computed values and look for one simple rule that covers
the known local ones. First outside run: ABX3 hexagonal perovskites on every stacking of their AX3 layers.

**Conclusion:** one counting law covers every local rule found, the **Window Law** (placeholder name): a count read from g
consecutive layers is a straight line in the frequencies of the c/h words of length g. g = 1 is the Hexagonality Law; at g = 2 the
only new number is p_hh (share of neighbouring hh layer pairs), and its coefficient is exactly the Swap defect
F(cc) + F(hh) − F(ch) − F(hc), so the Swap Rule is the test that a pair count falls back to a line in h. Of 36 quantities, 16 are
lines in h (6 of them constants), 9 are planes in (h, p_hh), 11 need windows of 3 to 6 layers. New exact items: face-sharing clusters per B = 1 − h
(mean cluster 1/(1 − h)); every gap of every polytype holds the same holes (stacking-blind); A neighbours per B = 8 − 2h;
the B–B shell formulas; the perovskite table of windows. Known: face sharing 2h / corner 6(1 − h) (#72, classical in substance), the
window structure itself (stacking-disorder theory; ANNNI J1–J2 for energies).

**Status:** done (counts). Not run: the #57 weight walk (power-diagram volumes) on the perovskite net — decided against for this run:
the counts already fix the law's shape, the walk needs a new 2×2-cell net for the census engine, and the hole kinds turned out the
same in every gap, so the walk can only differ through far-layer shapes. Queue it only if DICTO wants volumes.

## Method
- Model (scripts/perov.py): X and A equal close-packed balls (X–X = 1), AX3 layers with A on a 2×2 sublattice, B in the octahedral
  holes with X only. Integer coordinates (lateral in thirds of the lattice basis, height in quarters of the layer spacing d² = 2/3),
  so 72·r² = 8(x² + xy + y²) + 3z² is an integer: every distance and every count is exact.
- A positions are forced: in each gap exactly one octahedral hole avoids the A of the lower layer; the A of the upper layer must
  avoid it, which fixes its coset uniquely (asserted for every layer of every stacking). The A pattern never doubles the period.
- Stackings: all 505 primitive c/h bracelets of length 1–12 (every polytype up to period 12, up to turning over), plus 50 random
  stackings of 48 layers from a two-state Markov chain (P(h|h), P(h|c) ∈ {1/10, 3/10, 1/2, 7/10, 9/10}, seed 20261031; periods
  48–144 layers) so that h and p_hh vary independently. 555 stackings in all.
- Splash (scripts/splash.py, run on dicto-big-brother, 22 processes, ~5 s): per formula unit, exact Fractions. Each quantity is
  tested as (1) a line in h, (2) a plane in (h, p_hh), (3) a linear form in the frequencies of c/h words of length m, smallest m found
  (exact Gaussian elimination over all 555 rows; no floats). Per-site locality: the smallest window of layer types around a B's gap
  that fixes its value. Swap test for per-gap quantities fixed by the gap's two layers.
- Figures: scripts/figs.py (matplotlib on dicto-big-brother) → fig/splash2-perovskite.png, fig/shells.png.
- Known polytypes: scripts/table.py → data/known_polytypes.md (Ramsdell symbol recomputed from the letters: all 11 match).

## Results (data/splash2_perovskite.json, data/splash.log; per B = per ABX3)
| quantity | exact on all 555 | window | status |
|---|---|---|---|
| face-sharing partners per B | 2h | 1 | known (#72; classical in substance) |
| corner-sharing partners per B | 6(1 − h) | 1 | known (#72) |
| edge-sharing partners | 0 | – | classical |
| X in a shared face (B–X–B = arccos 1/3 = 70.53°) | share h | 1 | classical in substance |
| X in a straight B–X–B (180°) | share 1 − h | 1 | classical |
| A cuboctahedral / anticuboctahedral | 1 − h / h | 1 | classical |
| A neighbours per B (r² = 3/2) | 8 − 2h | 1 | not found; new (elementary) |
| B–B at r² = 2/3, 2, 14/3 | 2h, 6 − 6h, 12h | 1 | 2/3, 2 = the face/corner counts; 14/3 new |
| face-sharing clusters per B (incl. single octahedra) | 1 − h | 1 | not found; new |
| A per X, X per X, X per A | 4 (2 in the layer, 1 above, 1 below), 8, 12 | 0 | classical (3C), here for every stacking (X: 505 bracelets, 0 exceptions) |
| empty octahedral holes per gap | 3, each A2X4 with the two A opposite (r² = 2) | 0 | not found; new |
| tetrahedral holes per gap | 8, each AX3 (6 with A in the base, 2 with A at the apex) | 0 | not found; new |
| B with 0 / 1 / 2 shared faces | 1 − 2h + p_hh / 2h − 2p_hh / p_hh | 2 | Swap fails (defect +1, −2, +1) |
| strings of ≥ 2 octahedra per B | h − p_hh | 2 | new as stated |
| B–B at r² = 8/3, 4, 20/3, 8 | 2p_hh, 12 − 6p_hh, 12p_hh, 6 − 6p_hh | 2 | new |
| B–B at r² = 6, 22/3, 10, 34/3 | – | 3 | new (window) |
| B–B at r² = 32/3, 12 | – | 4 | new (window) |
| clusters of L octahedra per B | f(c h^(L−1) c) (L = 1: f(cc)) | L + 1 | classical in substance (strings = runs of h) |

Theorem (Window Law, g = 2). For a per-gap quantity F fixed by the types of the gap's two layers,
mean F = F(cc) + [F(ch) + F(hc) − 2F(cc)]·h + Δ·p_hh, Δ = F(cc) + F(hh) − F(ch) − F(hc).
Proof: the gap types occur with frequencies f(cc) = 1 − 2h + p_hh, f(ch) = f(hc) = h − p_hh, f(hh) = p_hh. ∎
Δ = 0 is the Swap Rule, and then the mean is a line in h (#66). The splash confirms both directions on the perovskite: the 6
per-gap quantities that pass the Swap test are lines in h; the 3 that fail are planes with c = Δ.

Clusters (exact, all stackings except 2H): the face-sharing octahedra form chains; components = vertices − edges, with one B per gap
and one face bond per h layer, so clusters per B = 1 − h and the mean cluster has 1/(1 − h) octahedra (2H: one endless chain).
Same h, different p_hh: 4H (hc) and 12R (hhcc) both h = 1/2, p_hh = 0 and 1/4; 10H (hhhcc) and 10H′ (hhchc) both h = 3/5,
p_hh = 2/5 and 1/5 — same face count, different B types and strings.

Holes (exact): the three sites of every hole triangle lie in three different A cosets, each layer has one A per 2×2 cell and the
B hole avoids the A of both its layers; so the other three octahedral holes take exactly one A from each layer, and every
tetrahedral hole takes exactly one A. This is the same in every gap whatever the stacking: the AX3 net has no c/h-dependent hole kinds.

## Known polytypes (data/known_polytypes.md)
3C (c) SrTiO3; 2H (h) BaNiO3; 4H (hc) 4H-BaRuO3, SrMnO3; 6H (hcc) hexagonal BaTiO3; 9R (hhc) BaRuO3; 8H (hhhc), 15R (hhhhc)
BaMnO3−x (Adkin and Hayward 2007; sequences from the Ramsdell symbol + "strings share corners", Cava et al.); 10H (hhhcc)
Ba5Sb1−xMn4+xO15 (tetramers, Cava et al.); 10H′ (hhchc) Ba5Fe4NiO13.5 (trimers + dimers, Cava et al.); 12R (hhcc) Ba4Fe3NiO12;
5H (hhccc) Ba5Ta4O15. Real compounds with vacancies or two B kinds: the model is the stacking only.

## Prior art — sources checked (31 Oct 2026)
- Reference library (ask-library, 4 queries: hexagonal perovskite polytypes / face-sharing fraction; Katz–Ward and Jagodzinski
  notation; stacking-disorder correlations; face-sharing clusters): hits Keller et al. 2023 (Si/Ge polytypes, hexagonality,
  generalized Ising model), Kawanishi–Mizoguchi 2015 (SiC hexagonality table), Yi–Canright 1995, Ganesh–Nasr 2023 (correlations in
  randomly stacked solids: layer correlations n apart via a 1D Ising moment-generating function), Hart–Hansen–Kuhs 2021 (Markov
  description, reichweite), Rodriguez-Horta et al. 2017. None treats perovskite B networks.
- Web: Cava et al., "Hexagonal perovskites as quantum materials", arXiv 2006.05864 (read via pdftotext: notation (chh)3 = 9R,
  (ch)2 = 4H, (chc)2 = 6H; dimers/trimers/tetramers; strings share corners in 4H, 8H, 9R, bridged by single octahedra in 5H, 6H,
  10H, 12R, 21R); Jin et al., PNAS 105, 7115 (2008) (via the 10-28 study); Adkin and Hayward, Chem. Mater. 19, 755 (2007) (abstract:
  15R, 8H, 6H′, 10H BaMnO3−x; ordering temperatures depend on the fraction of cubic layers); Darriet and Subramanian, J. Mater.
  Chem. 5, 543 (1995) (abstract only); Katz and Ward, Inorg. Chem. 3, 205 (1964) (not reachable; cited via Cava et al.); arXiv
  2105.05206 (Ba-Sr-Mn-Ce screening: face- vs corner-sharing per polytype). Web queries: "hexagonal perovskite polytypes stacking
  sequence 2H 4H 6H 8H 9R 10H 12R 15R…", "Adkin Hayward BaMnO3-x revisited…", "Katz Ward 1964 Inorganic Chemistry…",
  "Darriet Subramanian 1995 …".
- In-house: #57 (rule of halves), #64 (Swap Rule in crystals), #66 (Swap ⇔ line in h, in the book), #72 (face 2h / corner 6(1 − h),
  BaRuO3 volumes), studies 2026-10-28-perovskites-cathodes (perovskite_counts.py), 2026-10-25-relay-census (cubic perovskite walk only).
- Classical, cited not read: Hendricks and Teller (1942) and Jagodzinski (1949) stacking-disorder theory (correlations between
  layers depend on the stacking word between them); ANNNI polytype energies (J1, J2, J3), the energy form of the Window Law.
- Verdict on novelty: the Window Law itself is elementary and classical in substance. New here: the exact perovskite catalogue
  (which count sits at which window, with formulas), clusters per B = 1 − h, the stacking-blind holes, A per B = 8 − 2h, B–B shells,
  and the Swap defect named as the p_hh coefficient (count version of #66).

## Files
scripts/perov.py (exact model), scripts/splash.py (driver, fits, locality, swap), scripts/figs.py, scripts/table.py;
data/splash2_perovskite.json (all 555 stackings, every quantity exact), data/splash.log, data/known_polytypes.md;
fig/; results/paper.html → results/splash2-perovskite.pdf (also ~/Documents/papers-to-read/splash2-perovskite.pdf).
