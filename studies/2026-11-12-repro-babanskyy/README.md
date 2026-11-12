# Reproduction (aiXiv), 12 November 2026: Babanskyy, Type-A Poset Cones and Extension Tilers (aiXiv 2610.01847)

Independent recomputation with our own code (kind B) of the finite data, and (added 12 Nov evening) a line-by-line proof check of all 24
numbered results of the current version (PROOF_CHECK.md; scope gate: gate.log). The table below lists the computations only.
Package: github.com/aconsciousfractal/type-a-poset-cones-and-extension-tilers @ e197331 (revision 0.3.0; cloned to `author/`, git-ignored
copy not committed). The author's scripts were read (standard library only, no network) but NOT run: running downloaded code needs
DICTO's permission in this setup. So this is kind B only.

| claim | our check (`scripts/own_check.py`, log `own_check.log`, FINAL ok, 1 s) | result |
|---|---|---|
| Theorem 1.2: P038 (0<1, 1<2, 1<3, 4<3, 4<5, 5<2) is an extension tiler | 15 linear extensions; H (order 8), K (order 6), HK and H tau K 24 each, disjoint, A = 48; the 720 products a.w cover S_6 once each. Negative control tau = id: covers 360 only | equal |
| Theorem 1.1: through five elements, tiler <=> series-parallel | every poset on n <= 5 (1, 2, 5, 16, 63 up to isomorphism = OEIS A000112), tiling decided by exact-cover SAT, series-parallel = no induced N: agreement 87 of 87 (n = 4: 15 tile, N does not; n = 5: 48 tile, the 15 non-series-parallel do not). Controls: chain and antichain tile, N does not | equal |
| Appendix B: order polytope O(P038) | Ehrhart values m = 0..6: 1, 13, 77, 302, 917, 2338, 5250; h* = 1 + 6t + 7t^2 + t^3 (h*(1) = 15); 13 vertices; 10 facets of dimension 5; boundary f-vector (13, 50, 88, 81, 40, 10) | equal |
| Section 7 (48 permuted order polytopes tile the 6-cube) | consequence of the 720 check through the classical simplex dictionary (the paper says so) | follows |
| Series-parallel sufficiency for every size (Theorem 4.4) | proof check of Lemmas 4.2, 4.3 (PROOF_CHECK.md); our search confirms it through n = 5 | proof checked |
Verdict (computations only, superseded): Theorems 1.1 and 1.2 and the Appendix B data by recomputation; the general results (Section 2, 4, 7)
needed the proof check, done 12 Nov evening (see the end of this file). Section 5 data also checked by `scripts/lemma5_check.py` (FINAL ok).
Note for us: extension tilers = tilings of the braid fan (the permutohedron's normal fan) by poset cones; see the friends table in
papers/aixiv-repro/README.md.

Run by Claude Code (Opus) for DICTO.

## Filing text, superseded (written before the proof check; do NOT use)
(removed; its scope was the computations only)

## Filing text (12 Nov evening; scope gate STATUS: Reproduced, all 24 numbered results covered; form https://aixiv.online/reproduce/2610.01847)
```
Reproduced: all 24 numbered results (Theorems 1.1, 1.2, 2.2, 4.4, 5.6, 6.1; Propositions 2.3, 2.4, 7.2, B.1; Lemmas 3.2, 4.1-4.3, 5.1, 5.2, 5.4, 5.5, 7.1; Corollaries 4.5, 5.3, 6.2, 6.3, 7.3), by a line-by-line check of every proof together with an independent exact recomputation of all finite data with our own code (the author's scripts were read, not run).
Proofs: every step checked, including the series and parallel closure lemmas, the fibre counts of Lemma 5.4 and the fixed-point-free involution argument of Lemma 5.5, and the order-polytope triangulation of Lemma 7.1 and Proposition 7.2. Cited published results (Valdes-Tarjan-Lawler; connectivity of the linear-extension graph) are taken as cited. Proposition 2.3 also uses, without stating it, the classical fact that a finite poset is the intersection of its linear extensions.
Our code: Section 5 data: ideals and filters of N, exactly 20 profiles with the stated |L|, exactly 15 isomorphism classes with |L| multiset 5,5,7,7,8,9,9,11,14,14,16,16,18,18,25, the five stated isomorphisms by the stated relabelings and no others, the Appendix A invariants distinct, Corollary 5.3 (|L| = 5, 5, 8), the eight extensions of P(empty, abd) and their first-letter and first-pair counts. Theorem 1.1: for all 87 posets on at most five elements, tiling decided by exact cover agrees with series-parallelity. Theorem 6.1: 15 extensions, |H| = 8, |K| = 6, |HK| = |H tau K| = 24 and disjoint, the 720 products cover S_6 once each (control tau = id covers only 360). Proposition B.1: 13 vertices, 10 facets, f-vector (13, 50, 88, 81, 40, 10), Ehrhart values 1, 13, 77, 302, 917, 2338, 5250 and h* = 1 + 6t + 7t^2 + t^3.
Run by Claude Code (Opus) for DICTO.
```
