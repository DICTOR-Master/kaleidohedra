# Reproduction (aiXiv), 12 November 2026

Independent recomputation with our own code (kind B), every claim in the stated scope.

| aiXiv | paper | code | result |
|---|---|---|---|
| 2610.00950 | OpenAI, A product counterexample to the simplex maximum for projection-body volume (ai-authored; openai/math result 088) | Kind B, our own exact code (`scripts/projection_body.py`, log projection_body.log) | Theorem 1: R(T10 x T10) / R(T20) = 5588869/5505024 = 22355476/22020096 exactly (1.0152306); projection bodies as zonotopes of facet area-normals, volumes as exact sums of 20 x 20 determinants. Controls: R(triangle) = 6, R(tetrahedron) = 18, sheared tetrahedron 18 (affine invariance). 0.5 s |

Run by Claude Code (Opus) for DICTO.

## Complete reproduction (12 Nov 2026, later): every claim of the paper
**Proofs checked line by line (by Claude Code for DICTO), no gap found:** Lemma 2 (Cauchy facet formula: Jacobian |<nu_F,u>|, two facet
interiors per generic line, null exceptions; segment support functions); Proposition 3 (facets of A x B are F x B and A x G, area-normals
(|B| s_F nu_F, 0) and (0, |A| s_G nu_G), support functions add, volume exponents |A|^(1-r) |B|^(1-s)); Lemma 4 (area-normals transform by
|det L| L^-t via the unit-height prism; |det| of that map = |det L|^(d-1); the limit argument: P in lambda_m P_m gives
F - f_m <= (lambda_m^(d-1) - 1) kappa_(d-1) R^(d-1)); Proposition 5 (coordinate facets -e_i/(d-1)!, slanted facet w/(d-1)! via Jacobian
1/sqrt d; Pi T_d a translate of ([0,1]^d + [0,w])/(d-1)!; fibre argument |Q + [0,w]| = 1 + h_PiQ(w) = d + 1; R = (d+1) d^d / d!);
Theorem 1 (c10^2/c20 = 121 C(20,10)/(21 * 2^20)); the product test formula; Corollary 6 (e < 11/4 from tail ratios < 1/3;
c_n < (n+1) e^n since n^n/n! < e^n; the lower bound chain (A/lambda^10)^k/(10k + d_r + 1) -> infinity in each residue class).

**Exact computation, our own code** (`scripts/projection_body_all.py`, log `projection_body_all.log`, 13 s; all values computed directly as
zonotope volumes, not from the paper's formulas): Proposition 5 for d = 2..6; R(T_r x T_s) = c_r c_s and the closed product test for every
2 <= r <= s, r + s <= 7; Lemma 4 on 9 random rational simplices and a random triangle x tetrahedron; Theorem 1's integers; Corollary 6's
c10 = 17187500/567, A = 1638400000000/1336956340797 > 1, c_n < (n+1)(11/4)^n for n <= 200, and an explicit instance: lambda = 1.001 works
for every n from 21 to 2999 (it fails only at n = 20, where the ratio is 1.0152 < 1.001^20; the corollary asks only for some N).
Result: every claim confirmed. FINAL ok.
