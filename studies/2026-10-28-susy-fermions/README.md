# Supersymmetric lattice fermions and close-packed stackings (DICTO idea, 10-28)
Status 10-28: first comparison done (count.py, counts.json). Conclusion: same combinatorial setting, a clean dictionary, no physical identity.

Source read: P. Fendley, K. Schoutens, J. de Boer, Lattice models with N = 2 supersymmetry, PRL 90, 120402 (2003), arXiv hep-th/0210161
(4 pp, in the reference library): spinless fermions with hard cores (no two on neighbouring sites), H = {Q+, Q-}; on the periodic
N-site chain the ground states have f = int((N+1)/3) fermions (filling 1/3); N = 3p: two ground states, Witten index W = 2(-1)^p;
N = 3p +- 1: one, W = (-1)^p; six sites: states 1, 6, 9, 2 by f = 0..3.

Dictionary: a periodic stacking of N layers <-> its cyclic string of layer types; hexagonal layer h = a fermion on the site.
1. Stackings in which no two hexagonal layers touch (the Fibonacci stacking among them, #69) are exactly the hard-core configurations of
   the FSdB chain. Counts reproduced: N = 6 gives 1, 6, 9, 2 (total 18, a Lucas number), W = 2; all N = 2..15 agree with W = 2(-1)^p / (-1)^p.
2. Not every hard-core string is a stacking: a periodic stacking must CLOSE. The step signs close only for an even number of h
   (so stackings live in the even-fermion sector, (-1)^F = +1), and the positions close only when the steps sum to 0 mod 3.
   Counts of closing strings by f in counts.json (e.g. N = 6: f = 0: 1 (3C), f = 2: 3 = the 6H stacking hcc in its 3 positions).
3. The FSdB ground-state filling 1/3 is the hexagonality of 6H (hcc), the commonest SiC polytype; at N = 6 the ground states sit at
   f = 2, exactly the sector of 6H. (At N = 9, f = 3 is odd: no stacking there.)
4. Physics differs: FSdB fermions interact (hopping + repulsion); the Hexagonality Law (#66) says the volume carried by each
   hexagonal layer does NOT depend on the others (no interaction). The Fibonacci stacking's density 1/phi^2 = 0.382 lies between the
   ground-state filling 1/3 and the hard-core maximum 1/2.
No claim beyond this dictionary. Possible next: whether an ANNNI-type stacking energy can be written as {Q+, Q-} on the closing sector.
