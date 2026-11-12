# Aim 2, chunk 4: the associahedron sanity case (12 Nov 2026; `scripts/abhy.py`, log `data/abhy.log`, FINAL ok)

**Question.** Do our canonical-form tools (Warren's vertex formula, chunk 3; the triangulation formula, chunk 2) reproduce the
known case where a polytope's canonical form IS a physical amplitude: the kinematic associahedron of Arkani-Hamed, Bai, He and
Yan, whose canonical form is the bi-adjoint scalar tree amplitude m_n = Σ over planar cubic trees of ∏ 1/X over the tree's
propagators? (N. Arkani-Hamed, Y. Bai, S. He, G. Yan, "Scattering forms and the positive geometry of kinematics, color and the
worldsheet", JHEP 05 (2018) 096, arXiv:1711.09102.)

**Answer: yes, exactly, for n = 4, …, 10** (dimension 1 to 7; up to 1430 vertices and 35 facets).

**Setup.** Planar variables X_{i,j} (j ≥ i+2, (i,j) ≠ (1,n)); X_{i,i+1} = X_{1,n} = 0; s_{a,b} = X_{a,b+1} + X_{a+1,b} − X_{a,b} −
X_{a+1,b+1}; the ABHY slice s_{a,b} = −c_{a,b} (random positive rationals) for 1 ≤ a < b ≤ n−1, b ≥ a+2; coordinates
y = (X_{1,3}, …, X_{1,n−1}); A_n = {every X_d ≥ 0}. Ω(Y) = Σ over vertices |det(∇X_d, d tight)| / ∏ X_d(Y).

**Checks (all held, 48):**
- every triangulation of the n-gon gives a feasible simple vertex; count = Catalan(n−2) (2, 5, 14, 42, 132, 429, 1430);
  for n ≤ 8 an independent search through ALL (n−3)-subsets of facets (up to 15 504) finds no other vertex;
- every vertex has |det| = 1 (unimodular);
- **Ω = m_n exactly** at 3 random rational interior points for every n, and identically (symbolic) for n ≤ 6;
- the chunk-2 triangulation formula (Delaunay, any dimension) gives the same Ω for n = 5, 6, 7 (3, 17, 148 simplices);
- negative controls: m_n with one tree dropped differs from Ω; a tilted slice s_{1,3} = −c_{1,3} + X_{1,3} still cuts a simple
  polytope with Catalan many vertices, but some vertices get |det| = 2 and Ω ≠ m_n (n = 6, 7).

**Fault fixed on the way.** The first negative control tilted along X_{1,4}; that is only a shear of the coordinates (every |det|
stayed 1, Ω = m_n still), so it controlled nothing. Replaced by the X_{1,3} tilt above. This also shows the identity needs the
unimodular slice, not just the shape of an associahedron.

**What this gives the aim.** The tools used on the Hopscotch sweeps (chunks 2-3) reproduce the one textbook case where geometry
hands out a physical law; so their outputs on our sweeps can be read in the same language. Credit: the theorem is Arkani-Hamed,
Bai, He, Yan; the check and code are ours.
NEXT (chunk 5): DICTO's solids (OG, Narcissus, Cleo-Icos, Yantra cones) as positive geometries.
