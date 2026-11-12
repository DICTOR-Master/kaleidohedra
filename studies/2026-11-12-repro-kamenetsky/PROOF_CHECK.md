# Kamenetsky 2610.00139: check of the claims beyond Theorems A and B (12 Nov 2026)
Scope: every numbered claim the scope gate lists. Theorems A and B were reproduced earlier (our own code; README).
Exact checks: `scripts/proof_claims_check.py`, log `proof_claims_check.log` (38 ok, FINAL ok; controls: unreflected children do not
dissect 2C_3; a cube set with a cube removed does not give N 2^N panels).

| claim | proof read | exact check | verdict |
|---|---|---|---|
| Lemma 4.2 (1) volume 2^N - 1 | yes | N = 2..7 | holds |
| Lemma 4.2 (2) star-shaped, a ball | the paper's proof does not argue (2) (K1) | segment test N = 2..7 | holds by our argument below |
| Lemma 4.2 (3) N 2^N panels, 3N facets | yes (panel count, facet list) | N = 2..7 | holds |
| Theorem 5.1 rep-2^N dissection | yes, every step (blocks B_v, T_0 meets each in u_v, remainder = reflected chair; parity note) | explicit children, disjoint, union = 2C_N, N = 2..7 | holds |
| Proposition 7.1 finite certificate | yes, every step (K2, K3 small) | central child shares a panel with every other child, N = 2..7 | holds |
| Theorem 11.1 conditional strong aperiodicity | yes, every step | - | holds |

Our argument for Lemma 4.2 (2): if p in [0,1]^N and x in C_N, a point of the segment with all coordinates > 1 forces x_i > 1 for all i
(p_i <= 1), so x in (1,2]^N, impossible. So C_N is star-shaped about every point of [0,1]^N, a set with interior; a compact set
star-shaped about every point of a ball has a continuous radial function about its centre, hence is homeomorphic to the closed ball.

Gaps found (none is an error):
- K1 (low) Lemma 4.2 (2): the printed proof covers (1) and (3) only. Star-shapedness about the origin (a boundary point) alone would
  not give a ball; the argument above closes it.
- K2 (low) Proposition 7.1: applying (Pr) to "the actual enclosure of T_0(S(T))" needs T_0(S(T)) to be present. It is: T_0 shares
  a panel with every other child (true for all N: T_0 meets block B_v in the corner cube u_v next to T_v), so a compatible S puts
  T_0 on a panel of T, where the tile of E must be T_0 itself.
- K3 (wording) Proposition 7.1: halving supertile poses needs all supertile translations in one coset of 2Z^N; it follows from
  Sigma(P*) = 2P* up to one global translation.
Theorem 11.1: the proof is complete as written (finite order of R, w = sum R^j v, large supertiles force w = 0, injectivity of L).
