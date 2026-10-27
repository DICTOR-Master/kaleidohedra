# Splash Rules (placeholder name) — DICTO 2026-10-27

**DICTO's idea:** the rule of halves was spotted in a picture of computed values; other such "splash" pictures of computed tables may hide a simple rule (halves, thirds, ...). This study builds a rule finder and runs it over our exact tables.

**Conclusion (run 1):** In the #57 weight walk, the octahedral pieces follow the rule of halves at every layer spacing tested (squashed to stretched, d² = ½ to 2 × ⅔). When the layers are squashed (d² = ½ and ¾ × ⅔), the tetrahedral pieces also feel the next layer, and a new exact rule appears, the **Swap Rule** (placeholder name): *the two mixed pieces add up to the two pure ones*, V(c under h) + V(h under c) = V(c under c) + V(h under h), in every window where all four exist.

**Step 1 done (shapes, exact): the Swap Rule's reason.** A mixed squashed tetrahedral piece, cut by the horizontal mid-plane of its gap, has a lower part congruent to the lower part of the pure piece of its lower layer's type and an upper part congruent to the upper part of the pure piece of its upper layer's type (exact squared distances of all corner pairs, cut points included). 224 checks, 224 pass (scripts/swap_cut.py; d² = ¾ and ½ × ⅔; 4 stackings; 4 weights each; data/swap_cut_all.txt). So the mixed tetrahedra are Janus pieces too, and the Swap Rule follows: V(c|h) + V(h|c) = [c-bottom + h-top] + [h-bottom + c-top] = V(c|c) + V(h|h). Picture: swap-rule.png (d² = ¾ × ⅔, λ = 1/10).

**Map (splash-map.png; 11 spacings ⅙ … 2, all exact, data/s_*.json):** no window anywhere lacks a rule. At #57's spacing and above: halves only. At EVERY squashed spacing tested (15/16 down to ¼) the Swap Rule appears, so it switches on the moment the layers come closer than true close packing (between 15/16 and 1). At ⅙ pieces reach two gaps: volume = one share per layer reached ("layer sums", 2 windows) or plus one share per neighbouring pair of layers ("layer + pair sums", 1 window; 8 numbers fit all 16 surroundings exactly). No thirds rule.

**Step 2 done (theorem, proof/PROOF.md):** for every stacking, every layer spacing s ≥ ½ and every weight λ of the cubic walk (λ from −1/4 − s/8 for c, −1/3 − s/8 for h, up to min(1/3 + s/24, 3s/8)), every hole piece cut at its gap's mid-plane = lower half of the pure piece of its lower layer's type ∪ upper half of the pure piece of its upper layer's type; hence the Swap Rule for all three roles. Border: the far half of a tetrahedral piece is the same for c and h iff s ≥ 1; for ½ ≤ s < 1 the c far half is a proper part of the h far half at some λ (Ganesha, the Janus c/h tetrahedral piece of squashed stackings). One exact Farkas certificate per outside hole covers all s ≥ ½ at once (1070 PASS; border 58 PASS; engine cross-check 4992 PASS). Sharp: s0 = ½ exactly (below it the octahedral hole of the next gap cuts past the mid-plane) and λ ≤ 3s/8 is needed for s < 1.

**Step 3 done (proof/PROOF.md part II):** below s = ½ the volume Swap Rule holds because the piece volume is ADDITIVE in the two layer types: the octahedral hole of the next gap carves one fixed set out of a piece whenever the shared layer is c, out of reach of the far layer, so V = A(t) + B(t′). Proved for ¼ ≤ s < ½ (1706 certificates PASS); s1 = ¼ exactly (below it holes two gaps away cut; at s = 1/5 volumes depend on four layers). Swap Rule proved for every s ≥ ¼.

**Status:** run 1 + step 1 + map + steps 2–3 (proof) + run 2 (all 14 frameworks decided, below) done. Not yet run: Web of Bonds (#53), keyed web, #56 twinned-octet walk.

## Method (scripts/splash.py, exact, on dicto-big-brother)
- Family: the #57 hole walk (octahedral hole weight 0, tetrahedral weight λ) on close-packed stackings, layer spacing scaled d² = s·⅔, s ∈ {½, ¾, 1, 3/2, 2}; s = 1 is #57.
- Stackings: all primitive words up to 6 layers, up to symmetry: 2H (AC), 3C (ABC), 4H (ACBC), 5-layer ACABC, 6-layer ACBCAC and ACBABC. Census engine checks: 0 failures in all 30 walks.
- Each piece is labelled by its role (octahedral; tetrahedral over the lower layer; under the upper layer) and the layer steps within r gaps of its own gap (mirror-merged). **Locality:** r = 1 fixes every exact volume at every spacing (0 clashes).
- **Mix:** each volume is fitted exactly as a·V(pure c) + b·V(pure h) with constant a, b (sympy, coefficient matching).
- Census volumes are per unit cell height; multiplied by the number of layers (a slip in the first sanity run, caught when 4H/5-layer mixes came out as 3/10, 1/5 instead of ½, ½).

## Results (data/s_*.json; picture splash-run1.png)
| d² / (⅔) | windows | octahedral pieces | tetrahedral pieces |
|---|---|---|---|
| 2, 3/2 | 6 | pure c, pure h, halves | own layer only (pure c / pure h) |
| 1 (#57) | 4 | pure c, pure h, halves | own layer only |
| ¾ | 10 | pure c, pure h, halves | mixed ones: Swap Rule (5 windows) |
| ½ | 9 | pure c, pure h, halves | mixed ones: Swap Rule (4 windows) |

The Swap Rule was found by an exact null-space search over the four tetrahedral volumes in each window (relation [1, −1, 1, −1] in every window where all four exist). It says the tetrahedral volume splits as (own-layer part) + (next-layer part); at s ≥ 1 the next-layer part is zero, which is why #57 saw no such effect.

No thirds appeared in run 1: the reach never exceeded one gap.

## Prior art (default step) — sources checked
See prior-art.md.

## Run 2 (2026-10-27): the finder on other frameworks
**Conclusion run 2:** the rule of halves and the 4 : 5 : 6 end ratio belong to the octahedral holes of close packing only; the Swap Rule is the one rule that carries over (pyrochlore stackings, exact in every window); every other framework tested has a single arrangement, so there is nothing to mix, and no constant ratio between its own pieces either.

Questions per framework: **halves** = every piece is a whole pure piece or ½ pure c + ½ pure h (exact constant mix); **swap** = V(c under h) + V(h under c) = V(c under c) + V(h under h); **end ratio** = a constant ratio between matching pieces of the arrangements in a window, like 4 : 5 : 6. N/A = not applicable, with the reason.

| framework | arrangements compared | halves? | swap? | end ratio | evidence |
|---|---|---|---|---|---|
| close packing ABAC (4H), s = 1 (#57) | pure c (ABC) and pure h (AC), 6 words ≤ 6 layers | YES: octahedral pieces whole or ½ + ½; tetrahedral pieces whole (own layer) | YES (theorem, proof/PROOF.md, every s ≥ ¼; at s = 1 it follows from halves) | YES: 4 : 5 : 6 (cubic : Janus : hexagonal octahedral), 5/24 < λ < 3/8 | data/s_1.json, data/end_ratios.log, run2/run2c.log |
| close packing ABCACB (6H), s = 1 | same | YES (same) | YES (same) | YES: 4 : 5 : 6; in this word's own walk oct/oct = 5/4 | same; run2/run2c.log |
| pyrochlore (#60), ABC and AB + the 4 mixed words | pure 3C (ABC) and pure 2H (AC), 6 words ≤ 6 layers, 6 windows of −11/36 < λ < 1/4 | NO as volumes: O never a constant mix of the pure pieces, Y not for λ < −3/20 (from −3/20 on Y is whole, own lower layer); S, C whole (own layer). YES as cut halves (#60's exact theorem: each half congruent to the pure half), so for at least one pure O piece (c or h) the two halves differ in volume | YES, exact, all 6 windows, all 4 roles (follows from #60's cut theorem as in step 1) | NO: pure h / pure c and mixed / pure c vary with λ in every window | run2/pyro_mix.log, run2/out/pyro_mix.json, splash-run2.png; ../2026-10-27-pyrochlore-halves/exact/ |
| Delian loop sites (fcc + all tetrahedral holes) | one; it IS run 1's pure c holes (s = 1): same volume functions in every window, all three roles, run 1 / relay = ½ (volume units differ) | N/A alone (one arrangement); with hcp holes = run 1 (YES) | N/A alone; with hcp holes = run 1 (YES) | N/A alone; with hcp holes = 4 : 5 : 6 | run2/relay_vs_run1.py, run2/relay_vs_run1.log; run2/run2c.log |
| hcp holes (octahedral + tetrahedral holes of hcp) | one; it IS run 1's pure h holes (run 1 / relay = 2) | N/A alone, as above | N/A alone, as above | N/A alone, as above | run2/relay_vs_run1.log; run2/run2c.log |
| A15 (Cr3Si) | one | N/A: one arrangement | N/A: one arrangement | N/A; no constant ratio between its pieces in any window | run2/run2c.log |
| zinc blende / diamond | one | N/A | N/A | N/A; none in any window | run2/run2c.log |
| square lattice + centres (2D) | one | N/A | N/A | N/A; none in any window | run2/run2c.log |
| bcc two-kind (golden loop sites) | one | N/A | N/A | N/A; none in any window | run2/run2c.log |
| C15 Laves (MgCu2) | one | N/A | N/A | N/A; none in any window | run2/run2c.log |
| honeycomb + centres (2D) | one | N/A | N/A | N/A; none in any window | run2/run2c.log |
| kagome + centres (2D) | one | N/A | N/A | N/A; none in any window | run2/run2c.log |
| rock salt NaCl | one | N/A | N/A | N/A; none in any window | run2/run2c.log |
| perovskite ABX3 (two weights λ, μ) | one | N/A | N/A | N/A; none in any of the 5 chambers | run2/run2c.log |

**How each line was decided (all exact; floats only in the picture):**
- *Single walks* (run2/finder2.py, run2/run2c.log, rerun 2026-10-27 on all 14 frameworks): per window, the distinct piece volumes as polynomials in λ; constant ratios V_i/V_j by exact cancellation; integer relations among [V_1 … V_k, 1] by exact null space, the plain total (counts × volumes = cell) removed. finder2.py now also reads two-weight chamber files (perovskite failed in run2.log for this reason). The two-kind networks show nothing beyond the total; run2.log printed the total itself (filter added for run2b.log).
- *Pyrochlore mix* (run2/pyro_mix.py, new): #60's walk (~/kres-tmp/pyro/pyro_walk.py net, #57's census engine unchanged, 0 failed census checks on all 6 words) on every primitive stacking up to 6 layers; each piece labelled by role and the 3 layer steps round its gap (0 clashes: 4 layers fix every volume, as #60's locality bound says); each mixed volume fitted as a·V(pure c) + b·V(pure h) by coefficient matching in λ; the Swap identity checked by exact expansion.
- *Delian and hcp holes = run 1's pure pieces:* run 1's pure c (Delian) or pure h (hcp holes) piece at s = 1 (data/s_1.json) divided by the relay volume of the same role is the constant ½ (Delian) or 2 (hcp holes) in every window, all three roles (run2/relay_vs_run1.py); the two runs use different volume units.
- *Not tested:* the natural c/h partners of zinc blende (wurtzite) and rock salt (NiAs) were not in the run; with them, those two lines become c/h comparisons like the pyrochlore one.

**Earlier run 2 notes (single walks, kept):**
- #57 stackings ABAC, ABCACB: (i) oct − oct = tet(c) − tet(h) in every window, which is #57's "each layer takes the same space in c and h", re-found; (ii) **in the last window, 5/24 < λ < 3/8, the three octahedral pieces have volumes in the exact ratio 4 : 5 : 6 (cubic : Janus : hexagonal)**, all proportional to (3 − 8λ)³ (they vanish together at λ = 3/8); 5 is the mean of 4 and 6, the halves rule. Not stated in #57.

**Why 4 : 5 : 6 (exact):** for 5/24 < λ < 3/8 each octahedral piece shrinks to its centre, bounded only by its tetrahedral neighbours, all at the same distance. Cubic: 8 tetrahedral face-neighbours → regular octahedron |x|+|y|+|z| ≤ 1 (volume 4/3). Hexagonal: octahedral holes stack face to face along the axis, so only 6 tetrahedral neighbours → rhombohedron |x+y−z|, |x−y+z|, |−x+y+z| ≤ 1 (volume 8/|det| = 2). Ratio 2 : 3 = 4 : 6; the Janus piece = half of each = 5. (DICTO asked about 3:4:5 → 6:8:10: coincidence of pattern only.) For #61 as a corollary.

## Scutoid test (DICTO 2026-10-27: "the scutoids are similar to Janus c/h"; scripts/scutoid_test.py, data/scutoid_test.log, exact)
Slab = the gap between a piece's two layer planes; cross-sections just above the lower plane and just below the upper plane; corners strictly inside where the crossing faces change. Scutoid in the sense of Gómez-Gálvez et al. 2018 (Nat. Commun. 9:2960): different polygons or neighbours on the two surfaces, with a vertex in between.
- Chucky window (ABAC, λ = −3/8, Janus octahedral pieces): 9-gon below, 9-gon above, 3 neighbours swapped, 2 inner corners → scutoid.
- Ganesha (ACBC, s = ¾, λ = 1/10): 6-gon below, 12-gon above, 2 inner corners → scutoid; its mirror: 6-gon below, 3-gon above.
- Fang window (λ = 5/24): the Janus pieces do not span the gap (z 0.33–1 or 0–0.67) → not slab cells, test not applicable.
- CONTROL, pure cubic tetrahedral piece (s = ¾): 6-gon and 6-gon, 3 neighbours swapped → also a scutoid in this sense.
**Conclusion:** in a layered stacking almost every piece that spans its gap is scutoid-shaped, pure ones included, so "scutoid" does not single out the Janus pieces. The likeness DICTO saw is real but different in kind: a scutoid joins two different arrangements of neighbours; a Janus piece joins two different *pure orders* — its bottom polygon is the cubic one and its top the hexagonal one. Same family idea (a cell borrowing its two ends from two arrangements), not the same object. Status: done; the tissue version (cells between two curved surfaces) stays queued under Splash Rules.

## Counting rule across spacings (DICTO 2026-10-27 "do 2"; scripts/end_ratios.py, data/end_ratios.log)
Last-window octahedral ratios hexagonal : cubic and Janus : cubic, exact: s = 1 (#57): 3/2 and 5/4 (4 : 5 : 6); s = 3/2 and 2: 1 and 1 (the three pieces end equal); every squashed spacing 15/16 … 1/4: no window with a constant ratio (the pieces do not shrink together). **4 : 5 : 6 is special to true close packing**, as #61's Corollary 3 states (only for s = 1).
