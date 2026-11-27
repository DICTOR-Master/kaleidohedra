# C116 to Minana #377 (outline, 27 Nov 2026)

DICTO · paper · with Claude (Anthropic). Home decided by DICTO 27 Nov: its own paper (not the Scutoid-Frusta paper).
Gold standard #43 v3; Winston style; first paragraph = known, new, question answered. Data: study 2026-11-24-aequi-vacuus-scutoids.


## CORRECTION 27 Nov (DICTO: "I have never wanted or asked for the core to be the same as the outer... it is a transformation!!!")
DICTO's Hollow-straw fixes BOTH ends: C116 in its own shape inside, Minana #377 outside; the straws are swept as each C116 face plane
turns and moves into its die face plane, all together (a transformation). The flat-walled layer (hollow_straw.py, hollow_straw_exact.py)
moved the core parallel to the die: it is MY variant, not his method, and its certificate is not a certificate of his method.
DONE 27 Nov: his method built (c116_transform.py) and proved EXACT (c116_transform_exact.py): C116 in its own shape -> Minana #377, nested,
exactly the 18 floor swaps. This is Theorem 1. Lead figure: RENDER-c116-minana-transform.png. The flat-walled variant: a remark at most.

## Working title
From a Fullerene to a Fair Die: C116 Turned into Minana #377 by One Layer of Scutoid-Frusta

## First paragraph (known, new, question)  [rewritten 27 Nov evening to the day's results]
Known: fair dice (Aequi, #105/#118 catalogue); fullerenes and their enumeration (fullgen; OEIS A007894: C116 has 1,207,119 isomers);
scutoids in epithelia, where cells change neighbours between two surfaces (Gomez-Galvez et al. 2018, Voronoi seeds on two surfaces);
Scutoid-Frusta (DICTO, #118). Question: can a fullerene core turn into a fair die through one layer of pieces, both shapes fixed, one
piece per face, and how few neighbour changes does it take?
New: DICTO's Hollow-straw transformation turns the T_h fullerene C116, in its own shape, into the fair die Minana #377: every face plane
moves and turns into its partner face, all together; every intermediate solid lies inside the next (nested), and the neighbours change
by exactly 18 swaps. Proved in exact arithmetic (inputs rounded as stated). A short lemma explains nesting: the transformation is nested
exactly when every intermediate solid lies inside the die. The same method works for the Goldberg cores C60, C80, C140 with every
catalogue Aequus of their face count once the core is small enough (70 of 70 pairs at half the die's size; numerical).

## Arc
- Pledge. A fullerene and a fair die with 60 faces each, the same orbit sizes under T_h (12+12+12+24). Turn one into the other, both
  fixed; where neighbours differ, the change is a swap (four faces meet at a point).
- Turn. The obvious face pairing (pentagons to squares) needs 90 swaps; the best symmetric pairing 30 (one floor); DICTO's floating
  resin finds a pairing with 18 (one floor).
- Prestige. DICTO's Hollow-straw: every face moves into its partner, all at once, and the solid only grows: 60 straws fill the space
  between C116 and the die exactly, with exactly the 18 swaps. Proved exactly. And why it works: nested <=> always inside the die.

## Sections
1. Introduction: promise (Theorem 1 in one sentence), vision figure (the transformation: start, halfway, pulled apart, end), contributions.
2. Background: Minana #377 (catalogue no. 377, T_h, 12 squares, 12 heptagons, 36 hexagons); C116 T_h among 1,207,119 isomers;
   face patterns as triangulations; swaps = dual edge flips (the T1 process of foams); neighbour pairs kept; swaps >= pairs to gain.
3. Theorem 2 (symmetric pairings): best 144 of 174 kept, 30 swaps, one floor; near miss pentagons -> squares 108 kept, 90 swaps.
4. Proposition 3 (floating resin, DICTO): 156 kept, 18 swaps, one floor, symmetry S6 (best found; a solver bound of 165, stated as such).
5. Theorem 1 (DICTO's Hollow-straw transformation, exact): definition a_k(lam) = (1-lam) a_k + lam m_sigma(k); nested; every face
   throughout; exactly the 18 floor swaps at isolated times; certificate method (exact Q(sqrt5), root isolation, event sweep: kinetic
   data structures, Basch-Guibas-Hershberger 1999); inputs rounded (C116 planes 1e-9, Minana's 15-digit depth stand-ins).
   Lemma 4 (proved): nested <=> P(lam) inside the die for all lam.
6. Other cores and dice: C60, C80, C140 with all 14 / 28 / 28 catalogue Aequi of their face counts: nested for every core size up to a
   threshold >= 0.66 (numerical), 70/70 at 0.5; fewest changes fail mainly for dice with four-way corners. Conjecture.
7. Contributions; open questions (156 vs 165; exact certificates for other pairs; the conjecture; which pairings give fewest changes).
Remark (one paragraph, marked as Claude's variant): pressing the core parallel to the die gives flat-walled convex straws (a weighted
straight skeleton, credited there), but the core then keeps only C116's face pattern, not its shape.
Sources checked; data and reproducibility; references.

## Figures
1. Lead: the transformation, start / halfway / pulled apart / end (RENDER-c116-minana-transform.png), Aequi colours.
2. C116 in its own shape with its 60 straws, Aequi colours (RENDER-c116-minana-aequi.png).
3. The three routes: 90 / 30 / 18 swaps (face-pattern diagrams).
4. The nesting threshold over the 70 Goldberg pairs (chart).
App: the Hollow-straw page (kaleidohedra.dictospheres.com/hollow-straw/).

## Before drafting: decisions (mine; say no by number)
1. Title as above.
2. Theorem 1 = DICTO's Hollow-straw TRANSFORMATION (exact); Theorem 2 = symmetric optimum (30 swaps); Proposition 3 = floating resin (best found); Lemma 4 = nested iff inside the die.
3. EXACT first: Theorem 1 is exact (done 27 Nov). The 165 bound stays a solver bound unless certified; Section 6 is numerical and says so.
4. Prior art (corrected 27 Nov): the weighted straight skeleton (Aichholzer et al. 1995; Eppstein-Erickson 1999; Aurenhammer 2008;
   Barequet et al. 2008; Aurenhammer-Walzl 2016) describes ONLY my flat-walled VARIANT (faces moved parallel, core pressed into the die's
   planes). It is NOT DICTO's Hollow-straw: his fixes both ends and each C116 face turns and moves into its die face (a transformation),
   which is not a straight skeleton. The skeleton credit goes nowhere near his method; it appears only if the variant is reported, as mine.
   Prior art for HIS method: to search once it is built (what it actually is decides what to search).
5. Names: Hollow-straw and floating resin are DICTO's, first use explained; Scutoid-Frusta hyphenated; "Scutoid-bubble Frusta"
   not used (Occam, as decided).
