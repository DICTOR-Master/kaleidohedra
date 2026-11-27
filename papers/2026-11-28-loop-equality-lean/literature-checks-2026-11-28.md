# #125 literature checks (28 Nov 2026), countdown items 18-20
Sources opened by the check; verbatim quotes. Wayback used where the publisher blocks automated access.

18 THORPE "FIRST FORMAL PROOF": safe as "As far as we know". Searched: GitHub Lean code (Thorpe, polytype, wurtzite, residual entropy);
physlib (leanprover-community/physlib: fcc, hcp, diamond bond graphs, coordination, Ising; no walk counts); facebookresearch/atlas-lean
(DombNumber.lean = binomial sum only, no walks; CrystalPacking.lean; HoneycombConnectiveConstantWanted = unproved theorem_wanted);
google-deepmind/formal-conjectures (no hits); Mathlib (adjMatrix_pow_apply_eq_card_walk, general only); web for Coq/Rocq, Isabelle,
HOL, Mizar (nothing). Not checked: AFP index (empty page), Agda/Metamath beyond web search. ADD: credit physlib's Lean fcc/hcp/diamond
graphs and Mathlib's walk-counting lemma as prior infrastructure.
Thorpe, J. Math. Phys. 13 (1972) 294-299, doi 10.1063/1.1665973: "the total number of walks, starting and ending at the same point and
having the same number of steps, is the same for all polytype structures ... and is independent of the starting point."

19 OPEN PROBLEMS:
(a) diamond connective constant OPEN. Bauerschmidt-Duminil-Copin-Goodman-Slade arXiv:1206.2092: "Except for trivial cases, this is the
only lattice for which the connective constant is known explicitly." Grimmett-Li arXiv:1704.05884v2 (2019). Honeycomb: Duminil-Copin-
Smirnov, Ann. Math. 175 (2012) 1653-1665.
(b) exact ice residual entropy OPEN. Li-Cen-Wang-Yang, PRB 110, 195414 (2024), arXiv:2404.13897: "The exact solutions for the residual
entropy of realistic three-dimensional ice systems remain unknown." Chen-Ran arXiv:2608.07613v2: rigorous bounds 1.503360 <= w <= 1.540196.
(c) Ih = Ic entropy OPEN, WORDING: S_h >= S_c proved (Onsager, per Li et al.); Xu-Lin-Zhang PRB 113, 214416 (2026), arXiv:2511.22477:
equality follows IF an operator is normal, normality verified numerically ("rigorous evidence supporting the equality"); Chen-Ran
arXiv:2608.07613 (preprint): hexagonal maximal among periodic uniform-registry polytypes; "equality of the cubic and hexagonal entropy
constants remains unresolved." (Chen-Ran proofs not checked by us; abstract only.)

20 BENITO ET AL. OPENED: J. Benito, U. Urrutia, N. Ch. Karayiannis, M. Laso, "Enumeration of Self-Avoiding Random Walks on Lattices as
Model Chains in Polymer Crystals", Crystals 13(9) 1316 (2023), doi 10.3390/cryst13091316, CC BY. Exhaustive enumeration to N = 12:
fcc = hcp for N <= 5; N = 6: 1,573,716 (fcc) vs 1,573,728 (hcp); hcp larger for 6 <= N <= 12. Enumeration, no proof.
Paper line: "Benito et al. (2023) found by exhaustive enumeration up to N = 12 that self-avoiding walk counts on hcp and fcc agree for
N <= 5 and first differ at N = 6 (1,573,728 vs 1,573,716)."
