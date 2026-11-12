# Reproduction (aiXiv), 12 November 2026

Independent recomputation with our own code (kind B), every claim in the stated scope.

| aiXiv | paper | code | result |
|---|---|---|---|
| 2610.00950 | OpenAI, A product counterexample to the simplex maximum for projection-body volume (ai-authored; openai/math result 088) | Kind B, our own exact code (`scripts/projection_body.py`, log projection_body.log) | Theorem 1: R(T10 x T10) / R(T20) = 5588869/5505024 = 22355476/22020096 exactly (1.0152306); projection bodies as zonotopes of facet area-normals, volumes as exact sums of 20 x 20 determinants. Controls: R(triangle) = 6, R(tetrahedron) = 18, sheared tetrahedron 18 (affine invariance). 0.5 s |

Run by Claude Code (Opus) for DICTO.
