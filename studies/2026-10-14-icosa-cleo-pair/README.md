# Icosahedral Cleo + one partner fills space (Fable study for DICTO, 2026-10-14)

Question (DICTO): can the Icosahedral Cleo (the icosahedron's central pyramid on one face; edge 2/√5 icosahedron) fill space with
exactly one other polyhedron? **Yes, with a convex partner, periodically, face to face, no mirror images.**

- The Cleo is exactly the sharp corner of the **prolate golden rhombohedron**: the vectors u, v, w from the icosahedron's centre to
  one face's corners meet at arccos(1/√5) = 63.43°, the golden rhombohedron's face angle (edge R = 0.851, dihedrals 72° and 108°).
- In coordinates along u, v, w the rhombohedron is 0 ≤ x, y, z ≤ 1; the planes x + y + z = 1 and 2 cut it into **Cleo + A + Cleo**.
- **A** = conv(u, v, w, u + v, v + w, w + u): a convex trigonal antiprism (D3d), 2 equilateral caps (edge 2/√5), 6 side faces
  congruent to the Cleo's (0.851, 0.851, 0.894); dihedrals 110.905° (= 180° − 69.095°) at the cap edges, 108° at the side edges.
- Volumes: Cleo (3 + √5)/(30√5) = icosahedron/20; A = 4 Cleos; rhombohedron = 6 Cleos.
- Tiling: the rhombohedral lattice Zu + Zv + Zw, every cell cut the same way; every rhombus is cut along the same diagonal from both
  sides, so the tiling is face to face; Cleo : A = 2 : 1.
- Checks (scripts/cleo_pair.py → cleo-pair-checks.json): 9³-cell patch, 2,187 tiles; 104,189 random points each in exactly one tile;
  604 interior faces matched; 432 interior edges sum to 2π; 79 interior vertices sum to 4π.
- Dehn invariant: D(Cleo) ≠ 0, so no zero-Dehn space-filler (cube, rhombohedron, ...) can be the partner; D(A) = −2·D(Cleo), so the
  2 : 1 densities balance exactly.
- Other partners exist (rhombohedron minus a Cleo, not face to face; a 3-parameter family of parallelepipeds minus a Cleo); A is the
  most symmetric found and the only face-to-face one found. A second split (at a base corner) gives the same two tiles.
- Side result (count-level only): 20 rhombohedra round the icosahedron's faces have outer corners at radii 0.851 (12), 1.447 (30),
  2.028 (20), consistent with the rhombic hexecontahedron (known as 20 acute golden rhombohedra); if so it is 20 Cleos + 20 A + 20 Cleos.
- Prior art: the underlying facts (golden rhombohedron's face angle = the icosahedron's central angle) are classical; the split is the
  golden analogue of "rhombohedron = 2 tetrahedra + octahedron" (the tetrahedral–octahedral honeycomb). Present as an observation, and
  read Hafner's icosahedron dissections (Conway–Radin–Sadun paper models) and the Wolfram Demonstration "A Dissection of a Prolate Golden
  Rhombohedron" before any public claim.
- Open: is A the smallest convex partner? Only periodic? In Ammann rhombohedral tilings the same split gives aperiodic tilings with three
  shapes (Cleo, A, oblate rhombohedron). Name for A: DICTO's choice.

Correction (main session): earlier today we said a partner must supply a 41.81° wedge at the base edges. That was one option only: A's
110.905° cap edges meet the Cleo's 69.095° edges in a flat face (69.095° + 110.905° = 180°), which also closes.

DICTO · dictospheres.com
