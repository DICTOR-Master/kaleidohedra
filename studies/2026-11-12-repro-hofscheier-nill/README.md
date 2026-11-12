# Reproduction (aiXiv), 12 November 2026

Independent recomputation with our own code (kind B), every claim in the stated scope.

| aiXiv | paper | code | result |
|---|---|---|---|
| 2611.00775 | Hofscheier and Nill, Reflexive polytopes can have doubly exponentially many vertices (GPT-6.1 found the counterexamples) | Kind B, our own exact code from the paper's vertex data (`scripts/reflexive.py`, log reflexive.log) | Theorem 2.1: P8 has 44 vertices and 1371 facets (> 6^4 = 1296), every facet a.x = 1 with a integer (reflexive); Theorem 2.2: P9 has 48 vertices and 3378 facets (> 6^4.5 = 3174.5), reflexive. Facet planes recomputed in exact rationals and checked supporting against every point. Control: the free sum of four hexagons gives exactly 1296. 14 s |

Run by Claude Code (Opus) for DICTO.
