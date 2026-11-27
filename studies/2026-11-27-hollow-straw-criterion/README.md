# Hollow-straw criterion (27 November 2026)

DICTO · study. The question is DICTO's ("attack gap 1, the Hollow-straw criterion"; map MAP-VACUUS-AND-KNOWN-MATHEMATICS-2026-11-27).
With Claude (Anthropic). **Question:** for a core K and a fair die D with the same number of faces and a pairing of their faces, when is
DICTO's Hollow-straw transformation (both ends fixed; every face plane of K moves and turns into its partner plane of D, all together:
a_k(lam) = (1 - lam) a_k + lam m_sigma(k)) NESTED (each intermediate solid inside the next, so the straws fill the shell without
overlap), and when does it make exactly the needed neighbour changes?

Known case: C116 -> Minana #377, nested, exactly the 18 floor swaps, proved exactly (study 2026-11-24-aequi-vacuus-scutoids).

## Step 1: exploration (scripts/hs_general.py, run_explore.sh; logs/hs_*.log; data/hs_*.json) — numerical
Pilot: C116/#377 nested and minimal at core sizes 0.6 and 0.8 (also under a second pairing, 24 changes); C60/#1 (same pattern) no
changes; C60/#18 nested at size 0.6, NOT nested at 0.8 (first sign of a size condition). Full run: C60 x 354, C80 x 283, C140 x 28
dice, sizes 0.5, 0.7, 0.9 (core circumradius / die inradius). Results: below when the run ends.

## Sources checked for the gap (27 Nov)
Search "morphing between convex polyhedra of different combinatorial type, face-plane interpolation, flips, nested": closest found
A. Shapiro, A. Tal, Polyhedron realization for shape transformation (Technion; record only: vertex correspondence by merging the two
edge structures, then interpolating vertices; lists non-self-intersection as open); Gregory et al. (UNC TR 98-014, feature-based
morphing, record only); Erickson and Lin (planar morphs of one fixed graph, record only). Scutoids: Gómez-Gálvez et al. 2018 (opened):
Voronoi seeds on two surfaces. Nothing found on interpolating paired FACE PLANES between two fixed polyhedra, or on when that is nested.
Not a proof that it is new.

## Lemma (proved, 27 Nov): nested exactly when every intermediate solid lies inside the die
Planes a . x = 1; a_k(lam) = (1 - lam) a_k + lam m_k (m_k the partner plane of the die D). For x on face k of P(lam):
(1 - lam) a_k . x + lam m_k . x = 1, so a_k . x = (1 - lam m_k . x)/(1 - lam), and the rate at which face k moves at x is
d/dlam [a_k(lam) . x] = (m_k - a_k) . x = (m_k . x - 1)/(1 - lam)   (lam < 1).
So face k moves outward at x (the nesting condition checked numerically and exactly) iff m_k . x <= 1: the corner lies inside the
die's partner half-space. Hence: if every P(lam) lies inside D, the transformation is nested; conversely, if it is nested, then
P(lam) lies inside P(1) = D. **Nested <=> P(lam) is inside the die for every lam.** (Elementary; any core, any die, any pairing.)

## Step 1 data (C60 x 14, C80 x 28, C140 running; core sizes 0.5, 0.7, 0.9; numerical)
- Smallest core (0.5): nested in every pair so far (45/45). Middle (0.7): one C60 failure (die 91). Largest (0.9): many fail
  (C60 4 of 14, C80 14 of 28). Consistent with the lemma: a bigger core bulges the intermediate solids out through the die.
- Fewest changes ("minimal"): fails mainly for dice whose corners are not all three-way (they change by more than swaps) and for
  pairings where a neighbour pair is lost and later regained.
- Same pattern (no change needed): C60 always nested; C80 die 112 (same pattern) not nested at 0.9: nesting is not only about swaps.
Next: (1) test the FACING condition: each core face's normal points through its partner die face (the floating-resin aim); conjecture:
facing => nested for every small enough core; (2) finish C140; (3) exact proofs for the clean cases.
