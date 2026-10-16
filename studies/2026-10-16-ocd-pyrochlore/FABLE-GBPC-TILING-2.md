# Fable, pass 2: two sizes in G′ (2026-10-16)

DICTO · dictospheres.com

The question: can G′ (the golden region minus the 24 GBPCs per bcc cell) be tiled face to face by prolate golden rhombohedra (edge λ = φ|v|/9) together with φ-smaller oblates (edge λ/φ = |v|/9)?

Script: `scripts/gbpc_two_size.py` (exact, about 1 min). Output: `data/gbpc-two-size.txt`.
Everything is exact in ℚ(√5) unless marked FLOAT. |v| is the five-fold vector, the icosahedron circumradius.

## Results first

1. **No face-to-face tiling mixes sizes (exact, elementary).** In a face-to-face tiling, two tiles that meet in a face share that whole face, so they share its edges. Golden rhombohedra have all edges equal. So neighbouring tiles have the same edge length. G′ is connected (FLOAT check in pass 1), so every tile in a face-to-face tiling of G′ has the same size. A big face (edge λ) cannot be covered by small faces either: in a golden plane, every rhombohedron face is a translate of one rhombus shape, and λ is not a whole multiple of λ/φ.
2. **So no face-to-face tiling of G′ by golden rhombohedra exists, of any sizes.** One size is ruled out by the count in pass 1 (66 prolate, −30 oblate per cell at λ = φ/9). Two or more sizes are ruled out by item 1.
3. **Correction to pass 1.** The "46 prolate + 10 small oblate" bookkeeping assumed face-to-face, and face-to-face tilings cannot mix sizes, so it is void. Two sizes are possible only in a tiling that is not face to face, and there the count does not apply. Paper Draft 3 §6, the conclusion and the "Open" list repeat the void claim; see the replacement text at the end.
4. **Nothing was built.** An Ammann–Kramer (cut-and-project) tiling is face to face with one size, so items 1–2 rule out any window restricted to G′. A search over tilings that are not face to face was not run within the cap.
5. **Tilings that are not face to face are still undecided.** They are the only case left. We tested the most direct obstruction, and it does not apply (next section).
6. **Check of the counting step (exact).** Applied to the Ammann–Kramer tiling, the same Galois count gives prolate : oblate = −σ(vol O)/σ(vol P) = φ. That is the known value. This tests the method on a known case. It does not derive −30 by a second route; that remains a proof sketch.

## What a tiling that is not face to face must do (exact)

**Which piece fits a convex edge.** Of the golden rhombohedra, only the oblate has a 36° dihedral angle (cos² = φ²/4, exact). So every point of each of the 48 convex 36° edges of G′ lies on the acute edge of some oblate. Each convex edge has length φ|v|/9 (exact).

**Edge-length test.** If the free 36° wedge stopped at both ends of a convex edge, the oblate edges along it would have to add up to exactly φ|v|/9. That would rule out small oblates (edge |v|/9) as the only acute pieces, because nothing makes m·(1/9) = φ/9.

**Result: the test does not apply.** We sampled 6 directions inside the free wedge at the midpoint of each edge (exact points, chosen after a FLOAT prefilter). At 1/100 and at 1/1000 of the edge length past each end, all 6 stay free, on all 48 edges. The wall just ends there, and the free space opens wider. So an oblate edge can run past the end of a convex edge, and edge lengths give no condition.

Also measured (exact):
- The 24 third side edges of the GBPCs are blocked at one end (inside an RT) and free at the other.
- Volumes: oblate (376 − 168√5), prolate (−232 + 104√5) = φ × oblate, in units of |v|³ for edge |v|.

## Summary

| Case | Status |
|---|---|
| Face to face, one size | impossible (pass 1 count; the count is a proof sketch) |
| Face to face, two or more sizes | impossible (exact, elementary) |
| Not face to face, any sizes | undecided after the cap; the wall test still forces one-size λ into ℚφ; the convex-edge length test does not apply |
| With Bodhi pieces | untested |

## Paragraph for the paper (replaces the two-size sentences)

A face-to-face tiling of G′ by golden rhombohedra cannot mix sizes: tiles sharing a face share its edges, all edges of a golden rhombohedron are equal, and G′ is connected. Together with the one-size count, this shows that G′ has no face-to-face tiling by golden rhombohedra of any sizes (exact; the counting step is a proof sketch, and it reproduces the known Ammann–Kramer ratio φ : 1). Only tilings that are not face to face remain. For one size, the wall test still forces the edge length to be a rational multiple of φ|v|, and no further obstruction is known: the free 36° wedges continue past the ends of the convex edges, so edge lengths set no condition. Whether such a tiling exists, with or without Bodhi pieces, is open.
