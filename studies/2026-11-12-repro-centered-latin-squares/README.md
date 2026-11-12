# Reproduction (aiXiv), 12 November 2026

Independent recomputation with our own code (kind B), every claim in the stated scope.

| aiXiv | paper | code | result |
|---|---|---|---|
| 2609.03275 | Determinant Divisibility of Centered Latin Squares (ai-discovered; repo aconsciousfractal/Determinant-Divisibility-of-Centered-Latin-Squares @ff9431c) | Kind B, our own code from the paper's definitions (`scripts/latin6.py`, log latin6.log; the author's replays need the user present) | order-six census all equal: 9408 reduced squares; 36 divides det(E_std) for 8832, only 18 for 576; 1252 parity patterns, 84 with full-rank A mod 2, 0 mixed; binary criterion (36 does not divide det iff rank_F2(A) = 5) holds on all 9408; 80 group tables, 36 of them counterexamples. 1.8 s |

Run by Claude Code (Opus) for DICTO.
