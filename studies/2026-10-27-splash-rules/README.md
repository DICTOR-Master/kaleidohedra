# Splash Rules (placeholder name) — DICTO 2026-10-27

**DICTO's idea:** the rule of halves was spotted in a picture of computed values; other such "splash" pictures of computed tables may hide a simple rule (halves, thirds, ...). This study builds a rule finder and runs it over our exact tables.

**Conclusion (run 1):** In the #57 weight walk, the octahedral pieces follow the rule of halves at every layer spacing tested (squashed to stretched, d² = ½ to 2 × ⅔). When the layers are squashed (d² = ½ and ¾ × ⅔), the tetrahedral pieces also feel the next layer, and a new exact rule appears, the **Swap Rule** (placeholder name): *the two mixed pieces add up to the two pure ones*, V(c under h) + V(h under c) = V(c under c) + V(h under h), in every window where all four exist.

**Step 1 done (shapes, exact): the Swap Rule's reason.** A mixed squashed tetrahedral piece, cut by the horizontal mid-plane of its gap, has a lower part congruent to the lower part of the pure piece of its lower layer's type and an upper part congruent to the upper part of the pure piece of its upper layer's type (exact squared distances of all corner pairs, cut points included). 224 checks, 224 pass (scripts/swap_cut.py; d² = ¾ and ½ × ⅔; 4 stackings; 4 weights each; data/swap_cut_all.txt). So the mixed tetrahedra are Janus pieces too, and the Swap Rule follows: V(c|h) + V(h|c) = [c-bottom + h-top] + [h-bottom + c-top] = V(c|c) + V(h|h). Picture: swap-rule.png (d² = ¾ × ⅔, λ = 1/10).

**Status:** run 1 + step 1 done. Next: run 2 = the same finder on the #60 pyrochlore walk, relay census, Web of Bonds (#53), keyed web, #55 A15 walk and #56 twinned-octet walk; step 2 = make it a theorem for every stacking and every spacing (locality bound as in #57/#60; layer spacing as a symbol to find exactly where the tetrahedra start to feel the second layer, between ¾ and 1).

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
