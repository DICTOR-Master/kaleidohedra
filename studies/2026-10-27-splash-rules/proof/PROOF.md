# The Swap Rule theorem — proof (DICTO 2026-10-27)

Family: the #57 hole weight walk (DICTO DOI 10.5281/zenodo.23647898) on close-packed stackings with the layer spacing scaled, d² = s·(2/3) (s = 1 is #57). Holes of the gap between layers X (below) and Y (above), third position Z: octahedral hole over Z at mid-gap (weight 0), tetrahedral hole over X at 3/4 of the gap ("tetX", weight λ), tetrahedral hole under Y at 1/4 ("tetY", weight λ). Pieces = power (Laguerre) cells. A layer is **c** if its two neighbours differ, **h** if they coincide. Pure references: cubic ABC (all c), hexagonal AC (all h).

Name: for s < 1 the mixed tetrahedral pieces are **Ganesha, the Janus c/h tetrahedral piece of squashed stackings**. The rule: **Swap Rule**.

## Theorem (proved)

Let s ≥ 1/2 and put
λ₋(c) = −1/4 − s/8, λ₋(h) = −1/3 − s/8, U(s) = min(1/3 + s/24, 3s/8)  (U = 3s/8 for s ≤ 1, U = 1/3 + s/24 for s ≥ 1).

In every close-packed stacking (periodic or not), for every hole piece P of a gap whose lower layer has type t and upper layer type t′, and every λ with max(λ₋(t), λ₋(t′)) ≤ λ ≤ U(s):

P ∩ {below the gap's mid-plane} is, by a symmetry of the layer lattice, the lower half of the same-role piece of the pure stacking of type t, and P ∩ {above} is the upper half of the same-role piece of the pure stacking of type t′.

This holds for all three roles (octahedral, tetX, tetY), and for every s ≥ 1/2 at once (the range s → ∞ included).

The λ-range covers the whole walk of the cubic stacking: lemma W (below) shows the cubic walk lies inside [λ₋(c), U(s)], and the walks of all other stackings lie inside [λ₋(h), 1/3 + s/24]. For s ≥ 1, U(s) = 1/3 + s/24, so the range is every walk. For 1/2 ≤ s < 1, mixed stackings walk on past U(s) = 3s/8, and there the theorem is false (sharpness B).

### Corollaries
1. **Swap Rule** (volumes, every role): V(c|h) + V(h|c) = V(c|c) + V(h|h), where V(t|t′) is the piece over a t layer and under a t′ layer, for λ in [λ₋(c), U(s)] and s ≥ 1/2. Proof: V(t|t′) = L(t) + R(t′), with L and R the pure lower and upper half volumes.
2. **Border at s = 1.** Take the far half of a tetrahedral piece (below the mid-plane for tetX, above it for tetY; the mirror maps one to the other).
   - For s ≥ 1 it is the same for a c and an h layer at every λ: there the tetrahedral pieces are the pure piece of their nearest layer, as in #57.
   - For every s in [1/2, 1) there is some λ in the cubic walk where the c far half is a proper subset of the h far half. Its volume is then strictly smaller, so the two far halves are not congruent. These mixed pieces are the Ganesha pieces.
   - At s = 1 the two far halves coincide. The c-only sites of the gap below only touch the far half there (g = 0).

### Sharp ends (proved where marked, otherwise exact engine evidence)
A. **s0 = 1/2.** For s < 1/2 a hole of the next gap reaches past this gap's mid-plane and cuts the lower half of the octahedral and tetX pieces. The cutting site is the octahedral hole of the gap above, and the cut happens only when that gap's upper layer makes the shared layer c.
   - Proved exactly: the cutting function g_j (see method) is 0 at q = 1/3, which is s = 1/2. It is > 0 at q = 1/3 − 10⁻⁶ for 8 critical (role, type, site) cases, and > 0 on a q-grid down to 1/15.
   - Engine evidence (whole stackings) at s = 2/5: 112 halves are not the pure half, at λ = −29/100 and −27/100.
   - This s0 lies above the 1/6–1/4 expected from the volume locality. Below 1/2 the volumes still follow the Swap Rule, but the halves rule does not (see Open).
B. **λ ≤ U(s) is needed.** For s < 1 and λ > 3s/8, the tetrahedral hole of the next gap, standing straight over an octahedral hole, takes the octahedral hole's own point. It then cuts below the mid-plane.
   - Engine evidence at s = 3/4, λ = 5/16 and 21/64: 112 halves differ.
   - In the same runs the volumes are no longer fixed by the two layer types (12 clashes), and the Swap Rule fails (for example, −1/1536 for the octahedral pieces).
   - Control inside the range: 0 of 378 halves differ.

## Proof structure

**Linearisation (the key step).** Lateral hexagonal coordinates (x, y), height ζ in layer spacings, q = d² = 2s/3. Put u = q·ζ. Then each bisector condition pow_i(p) ≤ pow_j(p) becomes
(2d₁ + d₂)x + (d₁ + 2d₂)y + 2Δζ·u − q(ζ_j² − ζ_i²) − λ(t_i − t_j) ≤ Q(c_j) − Q(c_i).
This is linear in the five variables z = (q, λ, x, y, u) with a constant right side. So the following all form ONE convex polyhedron in z-space: every cell, its cut at ζ ≤ 1/2 (u ≤ q/2), and the parameter domain (q ≥ q0, λ₋ ≤ λ ≤ U, all affine in q). Two consequences:
- (a) A single Farkas certificate y ≥ 0 with yᵀM = c and yᵀm ≤ β proves c·z ≤ β for every (s, λ, p) of the domain together, the unbounded direction s → ∞ included.
- (b) For each site j, the set of (q, λ) where j cuts the half-piece is convex, since g_j is concave.

No combinatorial regions and no symbolic corners are needed.

**Step 0, lemma W (walkends.py, sympy, symbolic in q and λ).** Sum the bisector inequalities of a site against neighbours whose weighted offsets add to zero. A negative constant then means the cell is empty. The four cases:
1. an octahedral hole against its 6 tetrahedral holes: empty for λ > 1/3 + q/16;
2. an octahedral hole against tetrahedral holes straight above and below (both its layers c, as in the cubic stacking): empty for λ > 9q/16;
3. a tetrahedral hole next to an h layer: empty for λ < −1/3 − 3q/16;
4. a tetrahedral hole next to a c layer: empty for λ < −1/4 − 3q/16.

4/4 PASS.

**Step 1, reduction.**
- Fix the gap: layer 0 = A at ζ = 0, layer 1 = B, third position C. Layer −1 is C (layer 0 is c) or B (layer 0 is h).
- K(role, t) is the cell against the holes of the gap itself and of the gap below. These are fixed by layers −1, 0 and 1, so by t alone. Cut it at ζ ≤ 1/2.
- If no other hole of any stacking cuts K(role, t) ∩ {ζ ≤ 1/2}, then the lower half of the piece equals K ∩ {ζ ≤ 1/2} in every stacking with that t, including the pure one.
- The upper half follows by the mirror ζ → 1 − ζ, which swaps tetX and tetY and maps the gap above to a gap below.

Three arguments make the finite lists complete:
- **Lateral.** The 6 same-level neighbours confine K to a hexagonal prism of circumradius 1/√3. Within each level, the hole nearest to p laterally dominates all the others (same height, same weight). It lies within Q ≤ 4/3 of the site, and the lists keep all holes with Q ≤ 2.
- **Vertical, above.** Holes 3 or more gaps above are dominated by the same lateral point at the same fraction in the superset of gap 2 (all three positions), since pow difference = q(m−2)(m + 2 + 2f − 2ζ) > 0 for ζ ≤ 1/2.
- **Vertical, below.** Holes 4 or more gaps below are dominated by the superset of gap −3 when ζ > −2.75. The bound ζ ≥ −1 on the half is certified.

Both choices of layer 2 (gap 1) and of layer −2 (gap −2) are listed explicitly.

**Step 2, locality certificates for all s ≥ 1/2 (locality.py 1/3).** For 6 cases (3 roles × 2 types), one exact Farkas certificate for each outside hole j: pow_i ≤ pow_j on the lifted half-piece polyhedron with q ≥ 1/3, λ in the range, ζ ≤ 1/2. Plus ζ ≥ −1 for each case. **1070 PASS, 0 FAIL.** Each certificate is re-checked exactly by check_cert.

**Step 3, threshold (threshold.py).** g_j(q) = max over λ and p of pow_i − pow_j, at fixed q (exact LP), is concave in q. The exact grid from 1/15 to 2/3 finds the 46 sites that ever cut; all of them cut only below q = 1/3. Bisection and exact interpolation give the crossing q0 = 1/3 exactly: g = 0 at q0, > 0 just below, < 0 just above, for each of the 8 critical sites. Hence **s0 = 1/2**.

**Step 4, border (border.py).**
- (a) For q ≥ 2/3, every hole of the gap below (19 for c, 19 for h) satisfies pow_i ≤ pow_j on the tetX cell against its own gap only, cut at ζ ≤ 1/2. **38 PASS.** So the far half is the same for c and h.
- (b) For 6 c-only holes j of the gap below, g_j at q = 1/3 equals 1/12 or 1/6, and at q = 2/3 equals 0. These values are taken over the h far half, with λ in the cubic range. Concavity gives g_j > 0 for all q in [1/3, 2/3). **PASS.**
- (c) The c far half lies inside every halfspace of the 12 h-only holes, for q in [1/3, 2/3]. **12 PASS.** So c far half ⊆ h far half.
- (d) The h far half has interior points at q = 1/3 and q = 2/3, rational and strictly feasible, so also at every q between them. **2 PASS.** With (b) this gives an open set in the h far half outside the c far half: proper subset, strictly smaller volume.

**Step 5, independent check (validate.py, census engine).**
- What is compared: every half of every piece of 6 stackings (ABC, AC, ACBC, ACABC, ACBCAC, ACBABC), built from scratch by the engine as a whole periodic stacking, against the proof's model half K. The comparison uses exact corner-pair fingerprints with cut points included.
- Where: s ∈ {1/2, 5/8, 3/4, 1, 3/2, 2}, with 5 or 6 sample λ each, spread over the range.
- Result: **4992 PASS, 0 FAIL** (936 + 780 + 780 + 936 + 780 + 780).
- Earlier step (swap_cut.py, data/swap_cut_all.txt): 224/224 at s = 3/4 and 1/2.

**Sharpness runs (sharp.py, swapvol_below.py):** see A and B above. Logs: logs/log_sharp_*.txt and logs/log_swapvol_*.txt. In logs/log_model_vs_engine_*, the model is used outside its range, and failures there are expected.

## What is proved vs checked
- **Proved** (exact certificates, every s ≥ 1/2 and every λ in the range): the theorem, the Swap Rule, and the border in both directions. The proof is complete given exactness of rational arithmetic. Floats only proposed LP bases. Every certificate and every primal/dual point was verified in Fractions.
- **Proved:** the threshold value q0 = 1/3 for the certificate method. Below it, a hole of the next gap provably cuts the reduced half-piece K.
- **Checked** (exact engine at samples): that this cut makes the actual halves differ from the pure halves for s < 1/2 (s = 2/5) and for λ > U(s) (s = 3/4). Also that the cubic walk equals [λ₋(c), U(s)] at the sampled spacings (lemma W proves only ⊆).

## Open
- **Volume Swap Rule below s0.** At s = 2/5 the volume rule still holds exactly, at λ = −29/100, −27/100 and −1/4, including where the halves rule fails (logs/log_swapvol_below_s0.txt). The splash map also shows it at s = 1/3 and 1/4. Below 1/2 the mechanism is not the mid-plane cut. A proof for 1/4 ≤ s < 1/2 would need a different split, for example accounting for the chunk that the octahedral hole of the gap above takes. Not done.
- **s < 1/4** (pieces reaching two gaps, s = 1/6) is untouched.

## Files
- `swapgeom.py`: frame, site lists, linearised rows, domain, exact LP (float basis proposal with an exact primal and dual check; exact dual fallback for degenerate vertices), certificate checker.
- `walkends.py`: lemma W. `locality.py`: step 2. `threshold.py`: step 3. `border.py`: step 4.
- `validate.py`: step 5. `sharp.py`, `swapvol_below.py`: sharpness and the volume check below s0.
- `explore_bad.py`: exploration of where outside holes cut at fixed q (used to find the U(s) bound).
- `logs/`: all run outputs. `prior-art.md`, `data/library-queries.txt`: prior art.
- Machine: dicto-big-brother, `~/geom/bin/python`, work directory `~/kres-tmp/swap/`. The engine is in `~/kres-tmp/st57/scripts/`.
