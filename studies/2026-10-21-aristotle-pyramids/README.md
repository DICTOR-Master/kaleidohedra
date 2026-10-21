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

DICTO · dictospheres.com
