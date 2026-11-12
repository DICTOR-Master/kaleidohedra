# Proof check: Babanskyy, Type-A Poset Cones and Extension Tilers (aiXiv 2610.01847)

Line-by-line read of every numbered result of the current version (24 results, including Appendix B), 12 Nov 2026, by Claude Code
(Opus) for DICTO. Finite parts: our own exact code (`scripts/own_check.py` -> `own_check.log`; `scripts/lemma5_check.py` ->
`lemma5_check.log`, both FINAL ok). The author's scripts were read but not run (kind B only). No error found; no gap in the paper's
own arguments. Cited published results (Valdes–Tarjan–Lawler: series-parallel = induced-N-free; connectivity of the linear-extension
graph) are taken as given, as cited; we note where the paper uses one classical fact without stating it.

| result | what we checked | verdict |
|---|---|---|
| Theorem 2.2 | Proof read (a consistent set of halfspace choices is acyclic; its closure P; chambers = L(P); converse). | correct |
| Proposition 2.3 | Proof read (L(tau P) = tau L(P)). For the bijection with isomorphism classes the proof also needs that L(P) determines P, the classical fact that a finite poset is the intersection of its linear extensions (Szpilrajn); used without statement, standard. | correct (one classical step unstated) |
| Proposition 2.4 | Proof by citation (Stanley EC1 Sec. 3.5; Pruesse–Ruskey); we also checked the exchange argument (move the next letter of the target extension left past incomparable elements). | correct |
| Lemma 3.2 | Proof read ((a f^-1) L(fP) = a L(P)). | correct |
| Lemma 4.1 | Proof read. | correct |
| Lemma 4.2 | Proof read: each tile is L(Q1;Q2) with Q1, Q2 relabelings on Y and Z, a relabeling of P1;P2; sigma lies in it iff its first p letters are Y and its restrictions lie in the component tiles, so the family partitions S_X. | correct |
| Lemma 4.3 | Proof read: each tile is L(Q1 parallel Q2) = all shuffles; sigma lies in it iff its restrictions lie in the component tiles; partition. | correct |
| Theorem 4.4 | Proof read (closure under both operations; singletons). | correct |
| Corollary 4.5 | Proof read (tile sizes). | correct |
| Lemma 5.1 | Proof read (D ideal, U filter, d < u; D and U disjoint follows; converse keeps N induced). Our code: every one of the 20 profiles keeps N induced. Uses Valdes–Tarjan–Lawler as cited. | correct |
| Lemma 5.2 | Our code: ideals and filters of N (8 each) as listed; exactly 20 valid profiles; |L| of each equals the matrix (read from the PDF and Appendix A); exactly 15 isomorphism classes; |L| multiset 5,5,7,7,8,9,9,11,14,14,16,16,18,18,25; the five stated isomorphisms hold by the stated relabelings and are the only identifications. | correct |
| Corollary 5.3 | Our code: classes with |L| dividing 120 have |L| = 5, 5, 8. | correct |
| Lemma 5.4 | Proof read (first/last-letter fibres of size 24, 5 does not divide 24). | correct |
| Lemma 5.5 | Our code: the 8 extensions as listed; first letters x 5, c 3; pairs xc 3, xa 2, cx 3; 5a + 3b = 24 has only (0, 8), (3, 3). Proof read: the sum of alpha is 15 excludes (0, 8); the pair fibre equation 3N_uv + 3N_vu + 2C_uv = 6 gives C_uv in {0, 3}, one f(u) per u, and f(u) = v iff f(v) = u: a fixed-point-free involution on 5 labels, impossible. | correct |
| Theorem 5.6 | Proof read; also our exact-cover search over all 63 five-element posets: the 48 series-parallel ones tile, the 15 others do not. | correct |
| Theorem 1.1 | n <= 3 all series-parallel; n = 4 only N (5 does not divide 24); n = 5 Theorem 5.6. Our search agrees for all 87 posets with n <= 5. | correct |
| Theorem 6.1 | Our code: 15 extensions; |H| = 8, |K| = 6, |HK| = |H tau K| = 24, disjoint; the 720 products cover S_6 exactly once (negative control tau = id covers 360). Induced N on {1, 2, 3, 5} checked by hand. | correct |
| Theorem 1.2 | Theorem 6.1 plus Theorem 1.1 (six is the smallest size). | correct |
| Corollary 6.2 | Immediate from Theorem 6.1. | correct |
| Corollary 6.3 | Proof read (left relabeling preserves adjacent-transposition adjacency). | correct |
| Lemma 7.1 | Proof read (sort coordinates, break ties by a linear extension of P). | correct |
| Proposition 7.2 | Proof read (the standard triangulation; each simplex in exactly one piece). | correct |
| Corollary 7.3 | Proposition 7.2 + Theorem 6.1; volume 15/720 = 1/48. | correct |
| Proposition B.1 | Our code: 13 vertices, 10 facets, boundary f-vector (13, 50, 88, 81, 40, 10), Ehrhart values m = 0..6 (1, 13, 77, 302, 917, 2338, 5250), h* = 1 + 6t + 7t^2 + t^3; degree-6 polynomial fixed by 7 values. | correct |
