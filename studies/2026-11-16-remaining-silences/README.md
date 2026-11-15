# Remaining silences: the last open zeros of the hidden-zeros census (16 Nov 2026)

**Verdict.** All three open families are now explained, with exact checks. None of them needs a new kind of symmetry. The census missed them because it tested symmetry on the wrong scale: on the whole 3-sphere instead of on the polytope, and inside H4 instead of inside W(E8).

| case (census §2) | (a) full symmetry | (b) rings | (c) linkage | (d) twisted | verdict |
|---|---|---|---|---|---|
| 600-cell, degree 8: 30/60-point unions of [C3 × C5], [C5 × C5], [C3 × C10], [C5 × C5].2 orbits (8 sets) | no: Sym(S) = stabiliser (15, 50, 60, 200), with 3, 1, 2, 1 invariant harmonics of degree 8 | **yes, Hopf rings**: the Hopf image is the six 5-fold axes, each hit 5 or 10 times | **yes**: on the stabiliser-invariant weightings, T₄ = 0 forces T₈ = 0 | no | **explained** |
| 120-cell, degree 8: 240-point union of two [C5 × 2T] orbits (2 sets) | no: Sym(S) = stabiliser (120), with 1 invariant of degree 8 | **yes, Hopf rings**, reduced to one identity on the 2-sphere (below) | no | no | **explained down to one exact 3D identity** |
| E8, degree 4: 120 roots, stabiliser 576 or 144 (4 sets) | **yes**: Sym(S) has order 14400 (not 576 or 144), and each S is a W(E8)-image of a 600-cell shell | **yes, bizonal swap pairs** | no | no | **explained** |

All checks passed: 73 of 73 in the main run and 5 of 5 in the E8 follow-up. Computation, proofs and drafting were done with Claude (Anthropic). "Hopf rings" and "bizonal swap" are working names, and DICTO may rename them.

## 1. Hopf rings (600-cell and 120-cell)

**Law (exact).** Let S be a set of points on S³ that is invariant under left multiplication x ↦ lx by a cyclic group C₅ or C₁₀ of unit quaternions with axis p. Let h(x) = x̄ p x be the Hopf map onto the 2-sphere, and let M = h(S), counted with multiplicity. Then for l ≤ 4

  Σ_{x,y∈S} U₂ₗ(⟨x,y⟩) = Σ_{u,v∈M} Pₗ(⟨u,v⟩)

with Chebyshev U on the left and Legendre P on the right. So **S is silent in degree 2l exactly when its Hopf image is silent in degree l on the 2-sphere.** The same holds for a right-invariant S, with h(x) = x p x̄.

*Reason.* C₅ fixes only weight 0 of spin l ≤ 4, so every degree-2l content of S is invariant under the whole circle through p. Circle-invariant harmonics of degree 2l are exactly the Hopf pull-backs of degree-l spherical harmonics. The C₅-orbits play the part that latitude circles play in the zonal rule.

*Check.* The ratio T₂ₗ(S)|S|² / toneₗ(M) is exactly 1/(2l + 1) for l = 1 to 4. It was tested on all 10 cases, on 800 random C₅-invariant sets (400 in the 600-cell and 400 in the 120-cell), and on all 14 explained census sets with a C₅ or C₁₀ factor. The criterion reproduces their even zeros up to degree 8.

**600-cell consequence (new, exact).** For x in 2I, h(x) always lands on one of the 12 vertices of the icosahedron. Even functions on the six axes split as 1 + 5 (the 5 is the A5 irreducible), and both degree 2 and the 5-part of degree 4 detect that 5. Hence:

> *A subset of the 600-cell invariant under left (or right) multiplication by an order-5 cyclic group is silent in degree 4 ⟺ silent in degree 8 ⟺ its Hopf image covers the six 5-fold axes equally often.*

All eight open sets have exactly this Hopf image: six axes, each hit 5 times (the 30-point sets) or 10 times (the 60-point sets). Since the icosahedron is a 5-design, both degrees vanish. Checked on 200 random sets built to cover the axes equally: all were silent in degrees 4 and 8. Among 400 random C₅-invariant sets, the only silent one also passed the axis test.

**The same zero, seen as linkage (c).** On the stabiliser-invariant rational weightings V (dimension 8, 7 or 4), the exact kernels satisfy K₄ ⊆ K₈. The census computed linkage only on all weightings, where T₈ ⇒ T₄ holds and nothing more. Restricted to V, the converse T₄ ⇒ T₈ holds as well. Reason: degree 8 on the 600-cell lives in the A5 blocks 4 ⊠ 4 and 5 ⊠ 5, and the C₅ factor kills the 4-block, because χ₄(order-5 element) = −1 gives no fixed vector. What is left is the 5-block, which is degree 4. The census had already explained degree 4 (SPAN), so degree 8 follows.

**120-cell.** Here the C₁₀ factor is on the left. The Hopf image is 24 directions, each hit 10 times, forming two orbits of 12 under the tetrahedral rotation group of the 2T factor. That group has no invariant of degree 2, and only one of degree 4: the cubic quartic q = x⁴ + y⁴ + z⁴ − 3/5 (unit vectors, frame of the three 2-fold axes). On the two orbits it takes the values

  q = +√5/10 (120 points) and q = −√5/10 (120 points),

which are Galois conjugates with zero rational part, so they cancel exactly. The degree-8 silence of the 240-point set is therefore the 3D statement that x⁴ + y⁴ + z⁴ = 3/5 ± √5/10 on these two orbits. Each pair of directions averages to the icosahedral value 3/5, and Double Vision cancels the rest. That last number identity is exact but not yet derived from a symmetry (lead 1).

## 2. E8: the open sets are 600-cell shells in disguise (a), and bizonal swap pairs (b)

- **(a)** The stabiliser chain over Gram automorphisms gives |Sym(S)| = 14400 for all four sets. The group acts transitively on S, and it does **not** preserve the 4 + 4 split used to build E8. An exact isometry search then finds, for each S, an orthogonal map w sending shell 1 onto S. The float check confirms that w maps all 240 roots to roots, so w lies in W(E8). So S is a 600-cell shell for a *different* icosian structure of E8, and its zeros are the shell's: odd degrees and degree 4, the latter by the bizonal root 5s² − 5s + 1 = 0 of that structure. The census had grouped sets only up to the diagonal H4 (order 14400), so it could not see this equivalence. Control: a random 120-subset of the roots is not such an image.
- **(b)** Each set is shell 1 with some of its inscribed 24-cells moved to shell 2: 1 or 4 of them (stabiliser 576), 2 or 3 of them (stabiliser 144). Exactly:
  - The 600-cell has 25 inscribed 24-cells. For each of them, C in shell 1 and its copy φ⁻¹C in shell 2 are orthogonal (B = 0 for all pairs), so they span complementary 4-spaces.
  - The difference C(2) − C(1) is silent in degree 4 and not in degree 2, for all 25. Reason: the 24-cell is a 5-design in its own 4-space, and the only O(4) × O(4)-invariant harmonic of degree 4, h = |a|⁴ − 3|a|²|b|² + |b|⁴, has h(s = 0) = h(s = 1) = 1. The degree-2 invariant 2s − 1 changes sign instead.
  - So S = shell 1 + Σ (C(2) − C(1)) is silent in degree 4.
  - Control: 22 disjoint mismatched pairs C(2) − C′(1) are never silent.

## 3. What each test said, and controls

- **(a)** Our own stabiliser-chain search reproduces the census symmetry orders for all ten 4D sets, and gives the whole-polytope orders 14400 (600-cell), 1152 (24-cell) and 696729600 (E8 roots). Molien was computed over all elements.
- **(c)** The exact kernels on V reproduce every census zero. Soundness check: in 68 random unions of stabiliser orbits, a zero in a forcing degree always came with the open zero. The 120-cell and E8 cases have no forcing degree among their zeros (their other zeros are all symmetry-forced and impose nothing on V).
- **(d)** Not applicable. None of the sets is a twisted class or a union of twisted classes (census TW empty; 120-cell and E8 points are not group elements).
- **Random unions** are not silent and not explained (above). Known explained sets come out explained (Hopf criterion: 14 of 14).

## Leads

1. Derive the 120-cell identity x⁴ + y⁴ + z⁴ = 3/5 ± √5/10 on the two tetrahedral orbits of the Hopf image from a symmetry (is one orbit the Double-Vision image of the other?).
2. The Hopf-ring law for C₃ and C₆ factors (valid up to degree 4) and for higher degrees with C₁₀: list which census zeros it explains on its own.
3. E8: count the icosian structures (H4 subgroups of W(E8) up to conjugacy) whose shells lie in the root system; every such shell, and every bizonal swap of it, is silent in degree 4.

## Files

- `scripts/rs_main.py`: tests (a), (c), Hopf rings, bizonal swap pairs, and all controls. It uses the census modules in `../2026-11-15-hidden-zeros-h4/scripts`.
- `scripts/rs_iso.py`: the E8 shell-image search.
- `data/remaining-silences.json`: per-case results. `data/e8-shell-images.json`. Logs in `data/logs/`.
- Jobs: rs-pilot (33/33), rs-full (73/73) and rs-iso (5/5), all FINAL ok.
