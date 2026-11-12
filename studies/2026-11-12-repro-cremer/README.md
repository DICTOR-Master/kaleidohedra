# Reproduction (aiXiv), 12 November 2026

Independent recomputation with our own code (kind B), every claim in the stated scope.

| aiXiv | paper | code | result |
|---|---|---|---|
| 2610.01289 | Cremer, Lower bounds for Ramsey numbers: R(6,8) >= 135 and R(8,10) >= 345 (ai-discovered) | Kind B: the author's colourings (repo fritzcremer/ramsey-lower-bounds v1.1.0; SHA-256 equal to the paper's Appendix A) checked with OUR OWN exact max-clique search (`scripts/maxclique.c`, Tomita-style branch and bound; validated against brute force on 40 random graphs, 0 mismatches); log ramsey_own.log | all 7 colourings equal Table 1: K134 red 3913, omega red 5, omega blue 7 (R(6,8) >= 135); K344 nos. 1-2 red 25854 / 25855, omega 7 / 9 (R(8,10) >= 345); K343 nos. 1-4 red 25770 / 25809 / 25795 / 25795, omega 7 / 9. 2-3 s each |

Run by Claude Code (Opus) for DICTO.
