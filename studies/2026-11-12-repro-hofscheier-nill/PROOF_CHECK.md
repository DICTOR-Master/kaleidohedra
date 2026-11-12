# Hofscheier-Nill 2611.00775: check of the claims beyond Theorems 2.1 and 2.2 (12 Nov 2026)
Scope: every numbered claim the scope gate lists. Theorems 2.1 and 2.2 were reproduced earlier (exact recomputation, README).
Exact checks: `scripts/lemmas_check.py`, log `lemmas_check.log` (FINAL ok; control: a base with a facet distance not dividing k_0
gives a non-reflexive P). A first run showed FAIL only because our random-base generator produced 2 usable bases (< 50 required);
the generator was fixed (simplex built to match each base) and the rerun tested 120 bases.

| claim | proof read | exact check | verdict |
|---|---|---|---|
| Lemma 3.1 (unit partition -> reflexive simplex) | cited, no proof in the paper; our proof below | all 18 unit partitions with m <= 3; the paper's (6,3,2) and (42,7,3,2) simplices | holds |
| Lemma 3.2 (m-fold pyramid is reflexive, |F(B)| + m facets) | yes, every step (H1) | 120 random bases (dim 2, 3) with their simplices | holds |
| Lemma 4.1 (B_h: interior, vertices, 2 tau(h) + 1 facets, distances divide h^2) | yes (facet lines checked by hand: (c-d)(c-d') >= 0, (a-1)^2 >= 0) | h = 2..3000 | holds |
| Corollary 4.3 | yes: Theorem 4.2 with a = H - 1, b = H, eps = 1/2 gives k <= (16/log 2 + 1/2) log log H < 23.6 log log H <= 25 log log H | - | holds, given Theorem 4.2 |
| Theorem 4.5 (doubly exponential facets) | yes, every inequality (H2) | free-sum distance step, h = 2..60 | holds, given Theorem 4.2 |
| Theorem 4.2 | quoted from Bloom-van Doorn (hexagon:2610.00407), not the authors' claim | applied correctly (hypotheses 1 <= a < b, b >= b0(eps)) | not ours to check |

Our proof of Lemma 3.1: K = lcm(k_i), lambda = (K/k_0, ..., K/k_m) is primitive; in the lattice Z^{m+1}/Z lambda let v_i be the
image of e_i. Then sum (K/k_i) v_i = 0, and phi_i(x) = k_i x_i - sum_j x_j kills lambda (K - K sum 1/k_j = 0), so it is an integral
functional with phi_i(v_j) = k_i delta_ij - 1: every facet of conv(v_i) is at lattice distance 1, and 0 is interior.
Gaps found (none is an error):
- H1 (low) Lemma 3.2: "combinatorially an m-fold pyramid" is asserted; it holds since the apices (0, v_1), ..., (0, v_m) and the base
  hyperplane y_2 = v_0 are affinely independent (v_0, ..., v_m span a simplex).
- H2 (low) Theorem 4.5: "this is also true for the free sum of r copies" is stated without argument; it holds since a facet of a
  free sum has primitive normal (L/h_1 a_1, L/h_2 a_2) at distance L = lcm(h_1, h_2) (gcd(L/h_1, L/h_2) = 1), checked for B_h o B_h.
- Dependency: Corollary 4.3 and Theorem 4.5 rest on Theorem 4.2 (Bloom-van Doorn, a preprint), cited and correctly applied.
