# What could Aristotle have meant? The Platonic face pyramids (DICTO, 2026-10-21)

DICTO's question: Aristotle (On the Heavens III.8) said only "the pyramid and the cube" fill space; could he have meant Cleo-Icos?
Test: the five face pyramids (cone from the centre over one face of a Platonic solid; the icosahedron's is Cleo-Icos), alone and in
pairs. Angles (`angle_relations.py`, `angle-relations.log`): base edge = half the solid's dihedral; side edge (centre to corner) =
360°/(faces at that corner).

| pyramid | base edge | side edge |
|---|---|---|
| cube | 45° | 120° |
| tetrahedron | α/2 = 35.26° | 120° |
| octahedron | (180° − α)/2 = 54.74° | 90° |
| dodecahedron | θ_D/2 = 58.28° | 120° |
| icosahedron (Cleo-Icos) | θ_I/2 = 69.09° | 72° |

α = arccos(1/3), θ_D = arccos(−1/√5), θ_I = arccos(−√5/3). π, α, θ_D, θ_I are rationally independent (Conway, Radin & Sadun,
"On angles whose squared trigonometric functions are rational", Discrete Comput. Geom. 22 (1999) 321–332; NOT in the library yet —
check before any paper; PSLQ at 80 digits finds no relation, consistent).

Argument (as in #20): round any stretch of edge the angles of the pieces there add up to 360° (or 180° where it lies on a face).
Take a rational-linear map h with h(π) = 0 and h(one irrational angle) = 1, h(others) = 0: every angle sum there has h = 0.
- Alone: only the cube pyramid fills (6 make a cube). Each other pyramid has one irrational base angle (h = 1/2 > 0) and rational
  side angles, so round its base edges h > 0: impossible.
- Pairs: the tetrahedron and octahedron pyramids fill together (cut the octet: each octahedron into 8, each tetrahedron into 4;
  equal numbers of each). Their base angles have h = +1/2 and −1/2 (2 × 35.26° + 2 × 54.74° = 180°). Every other pair fails: the
  dodecahedron and icosahedron pyramids each sit alone in their own angle class, and the cube pyramid's angles are all rational,
  so it cannot help any other.
- So Cleo-Icos needs a partner that is not a face pyramid: Antonius (#20: 2 Cleo-Icos + Antonius = prolate golden rhombohedron).

Reading for DICTO: if "the pyramid" is a face pyramid, Aristotle is right for the cube's (trivially) and the octet pair is the
classical fix; the golden counterpart is Cleo-Icos + Antonius. Exact proof for alone/pairs among the five, given the cited theorem.

Exact checks for paper #44 (`pyramid_checks.py`, `pyramid-checks.log`, 46 PASS; also the slabs that let cube pyramids join the octet): every angle identity in exact Q(sqrt5)
arithmetic (via cos^2 and the sign of cos), the facts fed to the Conway-Radin-Sadun theorems (tan^2 = 8, 4, 4/5; (2 cos)^2 = 4/9,
4/5, 20/9 not integers, so no angle is a rational multiple of pi), the h test over all 31 sets of face pyramids (only {cube},
{tetrahedron, octahedron} and {cube, tetrahedron, octahedron} pass), the octet cell (octahedron 4/3 + 2 x 1/3 = 2; 8 + 8 pyramids)
and Cleo-Icos + Antonius + Cleo-Icos (volumes 1 : 4 : 1; Antonius 110.91 deg at its triangle edges). Figures: `aristotle_figs.py`
(viewer of 2026-10-19-five-fold-octet), `jewel-shots.mjs` on dicto-node, `aristotle_compose.py` -> figures/.

DICTO · dictospheres.com

Library (2026-10-21): Conway-Radin-Sadun 1999 now in the reference library (arXiv math-ph/9812019). Their Splitting Theorem: the
three angles have tangents in different square classes (tan alpha = 2 sqrt2, tan theta_D = -2, tan theta_I = -2/sqrt5), so no
rational relation mixes them; by their Theorem 2 none is a rational multiple of pi. This backs the argument above.
