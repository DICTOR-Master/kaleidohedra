# Reproduction: Winter, A relation between Mahler volume and flag number for convex polytopes (aiXiv 2610.00447, arXiv 2610.09990)
DICTO 12 Nov 2026 ("proceed with 1 and 2"; many birds: the Makai volume vol(P) vol((P-P)^o) is a new exact measure for our polar
sweeps P ∩ μP* and #43's iterated polar steps). Kind B: no author code exists; (1) proof read line by line, (2) our own computation.
## 1. Proof checked (every step)
- Corollary 2 from Theorem 1: (P - P)^o = (2P)^o = P^o / 2 for centrally symmetric P, so vol((P-P)^o) = 2^-d vol(P^o). Correct.
- Pulling triangulation indexed by flags: for a vertex order, Delta_v(F) = conv{v(F_0), ..., v(F_d)} with v(F_k) the least vertex of
  F_k; the non-degenerate ones triangulate P (standard, [2, 6] of the paper). Q_v = {t in Q : <t, v_1> <= ... <= <t, v_n>} over the n!
  labelings tile Q up to measure zero. So vol(P) vol(Q) = sum_v sum_F vol(Delta_v(F)) vol(Q_v); swapping the sums is fine. Correct.
- (3): F_{k-1} ⊂ F_k, so the least-index vertex of F_k comes no later than that of F_{k-1}; for t in Q_v the order is <t, .>, so
  <t, v(F_{k-1})> >= <t, v(F_k)>. Correct.
- Lemma 4 (i): (D_v t)_k = <t, v(F_{k-1})> - <t, v(F_k)> >= 0 by (3); the sum telescopes to <t, v(F_0)> - <t, v(F_d)> <= max - min
  of <t, .> on P <= 1, which is exactly t in (P - P)^o. So D_v Q_v ⊆ Delta_d; vol(Delta_v(F)) = |det D_v| / d!. Correct.
- Lemma 4 (ii), disjointness: an interior common point needs D_v, D_w non-singular, so no v(F_k) lies in F_{k-1} (a repeated vertex
  gives a zero row). Put v(F_0) = w(F_0) = 0 (translation changes neither Q nor the orders). phi = t_v - t_w vanishes on F_{k-1} (induction);
  the two displayed inequalities give phi(w(F_k)) >= 0 >= phi(v(F_k)); both points lie strictly on the same side of aff F_{k-1} in
  aff F_k, where phi is a multiple of the signed distance, so the multiple is 0 and phi vanishes on F_k. At k = d, phi = 0, t_v = t_w,
  an interior point of Q_v and Q_w, so v = w. Correct (the "same side" step needs the non-singularity, which the paper has).
- (4) and the final sum: sum_v vol(D_v Q_v) <= vol(Delta_d) = 1/d!, so each flag contributes at most 1/(d!)^2. Correct.
Verdict: the proof is complete and correct as written; no gap found.
## 2. Our own numerical test (`scripts/winter_check.py`, log winter_check.log, FINAL ok)
108 polytopes in dimensions 2, 3, 4: regular polygons, the five Platonic solids, prisms and bipyramids, the 4-cube, 16-cell, 24-cell,
4-simplex, 75 random polytopes (points in a ball, on a sphere, centrally symmetric sets, 4D). Flags from the face lattice, volumes by
hulls, (P - P)^o by polarity. Every case satisfies (1), and (2) where centrally symmetric. Equality (ratio 1 to 1e-9) exactly for:
square, cube, octahedron, 4-cube, 16-cell (Hanner polytopes) and triangle, tetrahedron, triangular prism, 4-simplex (faces of Hanner
polytopes): all consistent with Conjecture 3 (ii). Largest ratio among the random cases below 1. Examples: icosahedron and dodecahedron
0.527864, 24-cell 0.5, regular n-gons 1 (n = 3, 4), 0.854 (5), 0.75 (6).
One slip on the way: the first central-symmetry test sorted coordinate columns apart and called the tetrahedron symmetric; fixed.
Run by Claude Code (Opus) for DICTO.
