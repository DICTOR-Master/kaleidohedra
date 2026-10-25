# Number audit — "David and Goliath" (draft, #54 or #55), 2026-10-25

Every number and checkable claim in paper.src.html checked against: **E** = studies/2026-10-25-david-goliath/exact_a15.txt (Fraction, exact);
**P** = checks/exact_pairs.txt (exact, Q(√3); 22 PASS 0 FAIL, run on dicto-big-brother); **PA** = study prior-art.md; **R53** = relay-census README
"Results"/"Lives of the bonds"; **J** = relay-census data/raw/<net>.json stops; **CR** = Crossref lookup 2026-10-25 (this audit or PA/#53); **hand** = recomputed here.

| # | Claim / number | Where | Source | Result |
|---|---|---|---|---|
| 1 | A15 sites: Si 2ℤ³, +(1,1,1); Cr six sites listed; cell edge 2; w_Si = λ, w_Cr = 0 | Main thm, §2 | exact_a15.py; R53 units | PASS |
| 2 | Walk range (−5/4, 5/4); flips 1/4, 3/4 | §1 | R53 row 6a | PASS |
| 3 | Goliath corners (0,±1/2,±1) cyclic | Main thm (i),(iv) | E "= Jessen set: True"; P | PASS |
| 4 | 20 triangles, 12 corners deg 5, 30 edges, vol 7/2 | Main thm (i) | E; P | PASS |
| 5 | Edges: 6 of length 1, 24 of √(3/2) | Main thm (i), Fig. 1 | P (edge² 1 ×6, 3/2 ×24) | PASS |
| 6 | 8 equilateral faces ↔ Si at d² 3; 12 isosceles (1, √1.5, √1.5) ↔ Cr at d² 5/4 | Main thm (i), Fig. 1 | P (face types by neighbour) | PASS |
| 7 | David corners (0,±1/2,1),(1,0,1/2),(1,0,3/2); vol 1/6; 2 opposite edges 1, 4 of √(3/2) | Main thm (ii) | E "David corners"; P | PASS |
| 8 | David centroid = Cr site; four congruent isosceles faces | Main thm (ii) | P (centroid); disphenoid ⇒ congruent faces (hand) | PASS |
| 9 | David's 4 faces all to Si (only unlike bonds) | Main thm (ii), §3, Obs. 1 | J a15 λ=3/4: Cr bonds {Si: 4} | PASS |
| 10 | 2·7/2 + 6·1/6 = 8 | Main thm (iii), proof | E; P | PASS |
| 11 | Proof: sites within squared distance 6 used; superset + equal volume ⇒ equal | Proof | exact_a15.py R2=6; argument (hand) | PASS |
| 12 | Corner (0,1/2,1): power 1/2 to Si (0,0,0),(0,0,2),(±1,1,1) and Cr (±1/2,0,1),(0,1,1/2),(0,1,3/2); ≥ 2 to all others | Proof | hand (Fraction scan of 7³ cells, this session: next power 2) | PASS |
| 13 | At 3/4: Cr–Cr @1, @3/2 die; Si–Si @4 born; Si–Si @3 alive since 1/4; not a switch point | §3 | R53 bond lives: Cr–Cr [−5/4,3/4), Si–Si@3 (1/4,5/4], Si–Si@4 (3/4,5/4] | PASS |
| 14 | 12 Cr nearest Si(1,1,1) = Goliath + (1,1,1); David + (1,1,1) = Cr4 tetrahedron | Cor. 1 | P | PASS |
| 15 | Z12 at origin = (±1/2,0,±1) cyclic = Goliath turned 90° | Cor. 1 | PA (exact, Fraction) | PASS |
| 16 | (1,1,1) maps Si→Si, Cr→6d and back; corners of tiling = 6d sites | Cor. 2 | P (Goliath+(1,1,1) ⊂ Cr) + (2,2,2) lattice vector (hand); figure script asserts corners ⊂ Cr+(1,1,1) | PASS |
| 17 | Each icosahedron = 20 SiCr3 Delaunay tetrahedra; 2 + 6 per cell | Cor. 2 | PA | PASS (PA, not recomputed) |
| 18 | Fractional Cr (±1/4,0,±1/2) cyclic ~ (0,±1,±2) cyclic | Cor. 3 | PA; hand (×4, quarter turn) | PASS |
| 19 | Cr on 6c, Si on 2a, Pm3̄n | §2 | standard A15 (Frank–Kasper); PA | PASS |
| 20 | WP at λ=0: 14-faced (12 pent + 2 hex) + pentagonal dodecahedron, 6:2; family to 1/4 | Table 1 | R53 row 6a, #53 Cor. 5 | PASS |
| 21 | Octet at fluorite λ = −1/8, 1:2 per oct site | Table 1 | J delian λ=−1/8 (oct 8 tri, tet 4); #52 | PASS |
| 22 | CsCl ±1: cuboctahedra + octahedra, 1:1 | Table 1 | J bcc λ=±1 | PASS |
| 23 | Rock salt ±(4−2√3): Na 6 sq + 12 hex, 32 corners, 48 edges; Cl cube; all edges 2√3−3 | Table 1, §5 | P | PASS |
| 24 | Rock salt volumes 137 − 78√3, 78√3 − 135; sum 2 | Table 1, §5 | P; (2√3−3)³ = 78√3 − 135 (hand) | PASS |
| 25 | Zinc blende ±1: tetrahedron edge² 8, vol 8/3; capped octahedron 16 tri, edges² 8 (×12), 3 (×12), vol 40/3; 4·40/3 + 4·8/3 = 64 | Table 1, §5 | P | PASS |
| 26 | Octahedron corners at distance 2 on cube axes; cap apices at the 4 empty tet holes | §5 | P (corner-position check) | PASS |
| 27 | Cap = 1/4 of regular tetrahedron of edge 2√2 (vol 2/3, lateral edge √3 = circumradius) | §5 | hand: (8/3)/4 = 2/3; R = √(3/8)·2√2 = √3 | PASS |
| 28 | Obs. 1: smaller piece only unlike bonds in 5 of 6 pairs; WP exception | §5 | R53 bond lives: S–S [−3,1), Cl–Cl [−1,0), small–small [−3,1), Cr–Cr [−5/4,3/4); octet switch; WP: Cr–Cr alive at 0 | PASS |
| 29 | Rock salt per cell 4:4; zinc blende 4:4 | Table 1 | site counts (hand) | PASS |
| 30 | References [5]–[8], [10], [11], [17], [18]: as in #53 (CR there) | Refs | #53 refs + audit | PASS |
| 31 | [12]–[15], [19]–[22]: titles, venues, volumes, pages, years | Refs | CR this session | PASS — **note: PA lists 10.1107/S0567740869003694 as "Shoemaker & Shoemaker 1969"; Crossref: W. B. Pearson, C. B. Shoemaker. Paper uses Crossref.** |
| 32 | Bezdek–Carrigan year 2016 (vol 57; online 2015) | Ref [20] | CR: issued 2015-05-29 (online), vol 57 is 2016 | PASS (cite as 2016, vol 57) |
| 33 | [9] Jessen 1967, Nordisk Mat. Tidskr. 15 90–96, JSTOR 24524998 (no DOI) | Ref | PA | PASS (PA; not on Crossref) |
| 34 | #48, #51, #52, #53 DICTO DOIs | Refs | #53 refs; open-work (#53 concept 23631140) | PASS |

Not claimed as new: the tiling itself (Cor. 2), Jessen hull (classical), all of Table 1 except row 1. "Not found" items: (a) λ = 3/4 landing, (b) Z12 = Jessen hull stated — both per PA verdicts 3 and 1c.
