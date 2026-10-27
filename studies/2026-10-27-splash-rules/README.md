# Splash Rules (placeholder name) — DICTO 2026-10-27

**DICTO's idea:** the rule of halves was spotted in a picture of computed values; other such "splash" pictures of computed tables may hide a simple rule (halves, thirds, ...). This study builds a rule finder and runs it over our exact tables.

**Conclusion (run 1):** In the #57 weight walk, the octahedral pieces follow the rule of halves at every layer spacing tested (squashed to stretched, d² = ½ to 2 × ⅔). When the layers are squashed (d² = ½ and ¾ × ⅔), the tetrahedral pieces also feel the next layer, and a new exact rule appears, the **Swap Rule** (placeholder name): *the two mixed pieces add up to the two pure ones*, V(c under h) + V(h under c) = V(c under c) + V(h under h), in every window where all four exist.

**Step 1 done (shapes, exact): the Swap Rule's reason.** A mixed squashed tetrahedral piece, cut by the horizontal mid-plane of its gap, has a lower part congruent to the lower part of the pure piece of its lower layer's type and an upper part congruent to the upper part of the pure piece of its upper layer's type (exact squared distances of all corner pairs, cut points included). 224 checks, 224 pass (scripts/swap_cut.py; d² = ¾ and ½ × ⅔; 4 stackings; 4 weights each; data/swap_cut_all.txt). So the mixed tetrahedra are Janus pieces too, and the Swap Rule follows: V(c|h) + V(h|c) = [c-bottom + h-top] + [h-bottom + c-top] = V(c|c) + V(h|h). Picture: swap-rule.png (d² = ¾ × ⅔, λ = 1/10).

**Map (splash-map.png; 11 spacings ⅙ … 2, all exact, data/s_*.json):** no window anywhere lacks a rule. At #57's spacing and above: halves only. At EVERY squashed spacing tested (15/16 down to ¼) the Swap Rule appears, so it switches on the moment the layers come closer than true close packing (between 15/16 and 1). At ⅙ pieces reach two gaps: volume = one share per layer reached ("layer sums", 2 windows) or plus one share per neighbouring pair of layers ("layer + pair sums", 1 window; 8 numbers fit all 16 surroundings exactly). No thirds rule.

**Step 2 done (theorem, proof/PROOF.md):** for every stacking, every layer spacing s ≥ ½ and every weight λ of the cubic walk (λ from −1/4 − s/8 for c, −1/3 − s/8 for h, up to min(1/3 + s/24, 3s/8)), every hole piece cut at its gap's mid-plane = lower half of the pure piece of its lower layer's type ∪ upper half of the pure piece of its upper layer's type; hence the Swap Rule for all three roles. Border: the far half of a tetrahedral piece is the same for c and h iff s ≥ 1; for ½ ≤ s < 1 the c far half is a proper part of the h far half at some λ (Ganesha, the Janus c/h tetrahedral piece of squashed stackings). One exact Farkas certificate per outside hole covers all s ≥ ½ at once (1070 PASS; border 58 PASS; engine cross-check 4992 PASS). Sharp: s0 = ½ exactly (below it the octahedral hole of the next gap cuts past the mid-plane) and λ ≤ 3s/8 is needed for s < 1.

**Step 3 done (proof/PROOF.md part II):** below s = ½ the volume Swap Rule holds because the piece volume is ADDITIVE in the two layer types: the octahedral hole of the next gap carves one fixed set out of a piece whenever the shared layer is c, out of reach of the far layer, so V = A(t) + B(t′). Proved for ¼ ≤ s < ½ (1706 certificates PASS); s1 = ¼ exactly (below it holes two gaps away cut; at s = 1/5 volumes depend on four layers). Swap Rule proved for every s ≥ ¼.

**Status:** run 1 + step 1 + map + steps 2–3 (proof) done. Next: run 2 = the same finder on the #60 pyrochlore walk, relay census, Web of Bonds (#53), keyed web, #55 A15 walk and #56 twinned-octet walk.

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

## Run 2 (2026-10-27): exact relations inside any one weight walk (run2/finder2.py)
For each window: constant ratios between piece volumes and small integer relations among them (the plain total, pieces × volumes = cell, removed).
- Two-kind networks of the relay census (A15, bcc, C15, Delian, hcp holes, honeycomb, kagome, NaCl, zinc blende, square): nothing beyond the total (two piece types per window leave no room for a rule).
- #60 pyrochlore stackings (ABC, AB): nothing within one walk (its halves link different stackings, as in run 1).
- #57 stackings ABAC, ABCACB: (i) oct − oct = tet(c) − tet(h) in every window, which is #57's "each layer takes the same space in c and h", re-found; (ii) **new small rule: in the last window, 5/24 < λ < 3/8, the three octahedral pieces have volumes in the exact ratio 4 : 5 : 6 (cubic : Janus : hexagonal)**, all proportional to (3 − 8λ)³ (they vanish together at λ = 3/8); 5 is the mean of 4 and 6, the halves rule. Not stated in #57.
Conclusion run 2: no new rule in the two-kind networks; one new exact ratio (4 : 5 : 6) in the #57 walk.
**Why 4 : 5 : 6 (exact):** for 5/24 < λ < 3/8 each octahedral piece shrinks to its centre, bounded only by its tetrahedral neighbours, all at the same distance. Cubic: 8 tetrahedral face-neighbours → regular octahedron |x|+|y|+|z| ≤ 1 (volume 4/3). Hexagonal: octahedral holes stack face to face along the axis, so only 6 tetrahedral neighbours → rhombohedron |x+y−z|, |x−y+z|, |−x+y+z| ≤ 1 (volume 8/|det| = 2). Ratio 2 : 3 = 4 : 6; the Janus piece = half of each = 5. (DICTO asked about 3:4:5 → 6:8:10: coincidence of pattern only.) For #61 as a corollary.
