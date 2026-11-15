# Candidate group Y: exact Śrī Yantra statements (Zenodo preprint, not peer reviewed)

## The published problem
- A. P. Kulaichev, "Śrīyantra and its mathematical properties", Indian Journal of History of Science 19.3 (1984) 279–292. He imposes the classical incidence conditions (i)–(iii) below plus four extra conditions (a)–(d), argues that a solution exists by iterated approximation (p. 284), and asks whether it is unique (p. 285); he reduces the system to one polynomial of degree not higher than 12544 and judges the question out of reach.
- A. Chiodo, "On the construction of the Śrī Yantra", Comptes Rendus Mathématique 359 (2021) 377–397, doi:10.5802/crmath.163: §1.2.4 (p. 387) "The search for a unique Śrī Yantra" restates Kulaichev's problem; the French version (p. 384) says Kulaichev "se pose la question (toujours ouverte) de l'unicité" (the question of uniqueness, still open).
- V.-V. Pustynski, "On mathematical complexity of Śrīyantra", Indian Journal of History of Science 49.3 (2014) 268–277: solves the system numerically to 15 figures (Table 1), argues uniqueness from plots of residuals on dense grids (pp. 273–275), and writes (p. 275): "purely analytical solution of the final two steps is probably impossible since the corresponding equations are too unwieldy."

## Model
Circle of diameter 1. Nine isosceles triangles t1..t9 with axis the vertical diameter (t1–t5 apex down, t6–t9 apex up); ti has base depth b_i, half-width w_i, apex depth a_i. t7 has apex at the top point and its base corners on the circle (leg slope u); t3 has apex at the bottom point and base corners on the circle (leg slope v).
Conditions (Huet 2002 / Chiodo 2021):
(i) seven apex-on-base incidences a8=b1, a6=b2, a9=b3, a1=b6, a5=b7, a4=b8, a2=b9;
(ii) 18 triple concurrences (9 mirror pairs) of a down-leg, a base and an up-leg: (1,2,7),(2,3,7),(1,3,8),(1,4,6),(1,5,9),(4,6,9),(2,7,9),(3,7,8),(3,8,9);
(iii) six corner touches (4,4,8),(5,5,6),(2,6,6).
Kulaichev's extra conditions: (a) t3 ≅ t7 (u = v); (b) t1's base corners on the circle; (c) t9's base corners on the circle; (d) the incircle of the innermost triangle (between t1's legs and t5's base) is centred at the circle's centre.
Admissible: all triangles non-degenerate, each apex on the correct side of its base, all corners in the closed disc.

## Statements to score
Y1 (proved, certified computation). There is an admissible configuration satisfying (i)–(iii) and (a)–(d) whose slope u = v is the real root near 0.750438516022214 of an explicit irreducible integer polynomial f348 of degree 348 (even; 175 terms; leading coefficient 2^20·5^2, constant −2^8·3^5). Proof: elimination by resultants; irreducibility from factorisation patterns mod 7, 11, 13, 19; existence by an interval-Newton (Krawczyk) enclosure of the full system at 520 digits, with every dropped factor certified nonzero on the box and exact Sturm root selection. So the yantra's slope has degree exactly 348 (Kulaichev's bound: 12544), and the arrangement of its 27 sides, certified, has 45 regions lying inside an odd number of triangles (not the traditional 43): two extra tiny triangles, confirming Pustynski's remark.

Y2 (not yet proved; scored as a target). Y1 plus uniqueness: the admissible configuration satisfying (i)–(iii) and (a)–(d) is unique. (Plan: every admissible solution's u is a real root of the full eliminant of degree 1744, factors 1^178, 1^274, 1^178, 2^185, 348, 396; each real root is tested for admissibility by exact/interval arithmetic, with the degenerate loci of the elimination handled separately.)

Y3 (proved, same methods). With conditions (i)–(iii), (b), (c), (d) and, in place of (a), u·v = 2/φ^3 (φ the golden ratio), there is an admissible configuration whose odd regions number exactly the traditional 43, all triangles, with 24 points where exactly two sides cross; u has degree 160 over Q.

Y4 (proved, exact rational arithmetic). With u = 19/24, v = 2/3, b6 = 8/15, b9 = 8/9, conditions (i)–(iii) hold with every coordinate rational (a Śrī Yantra in whole-number fractions); more generally every rational choice of (u, v, b6, b9) in the admissible region gives all conditions exact in one quadratic field Q(√Δ).
