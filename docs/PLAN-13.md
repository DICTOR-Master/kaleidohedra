# The 13s: build sets, a world and a paper (DICTO, 2026-10-13)

Twelve around one, six ways. DICTO's decisions (2026-10-13): both a viewing world in Kaleidohedra and every kit buildable piece by
piece in Polyhedraverse with outlines for the next piece (as the Admiral Cap's); all six members; every kit we have, as a choice.

## Members and kits

| 13 | Kits |
|---|---|
| DICTO Dodeca-13 (#13) | 13 dodecahedra + wedges + needles; centre + 12 units; 13 dodecahedra + 20 stars |
| DICTO Icosa-13 / Lotus seed (#19) | 13 icosahedra + 60 wedges + 20 hexagonal pyramids + 20 needles (113); dodecahedron + 12 J11 + 30 Axe + 20 FUJI (63) |
| UNITY (#19) | icosidodecahedron + 12 J11, dimples closed by VAJRA |
| Bodhi seed (#24) | 13 rhombic triacontahedra + Kit A (Vajra fine, Chatra, Mudra) or Kit B (Vajra fine, Crown Jewel, Diadems) |
| DICTO-Star (#14) | icosidodecahedron + 12 dodecahedra + 20 J63 |
| RD 13 (periodic) | 13 rhombic dodecahedra (FCC) |

## RD 13 tiles space alone (checked 2026-10-13)

DICTO asked for a Hexa analog (a 13 that fills space with a partner, as the Hexa does with its Key). Checked: the 13-RD cluster
needs no partner. Of the 183 index-13 sublattices of FCC, 8 have the cluster as a complete set of coset representatives, so
translates of the cluster fill space exactly (RDs are FCC's Voronoi cells). Translations have length sqrt10 in coordinates where
neighbours are sqrt2 apart (sqrt5 neighbour spacings), e.g. (3, 1, 0); the 8 are one arrangement in two hands (left and right
twist), the 3D analogue of the seven-hexagon flower tiling. Likely known as a perfect 1-code in the FCC lattice (coding theory):
literature search before any claim.

## Stages

1. Data: each kit as [role, vertices, faces] from the checked study data (Dodeca-13: krp-core DODECA13_PARTS; Icosa-13 and UNITY:
   studies/2026-10-10-icosa-13; Bodhi: papers/bodhi-seed/fig/bodhi-data.json; DICTO-Star: idStar(); RD 13: FCC). Faces merged
   flat (scripts/build-seeds-data.py rule). Every kit checked: pieces closed, volumes summing to the hull.
2. The 13 world (Kaleidohedra, createLayeredWorld): one entry per 13, its kits as views, Pull apart, Top shell, Crystal; RD 13
   also as the space-filling block (a few blocks, both hands).
3. Polyhedraverse kits: each kit's pieces as DICTO pieces (no crossover: pieces live in P, the world links to them), and hint rules
   so the outlines show where each next piece goes, from the centre out.
4. Paper: the six 13s side by side (counts, volumes, what fills the gaps), RD 13 as the periodic member. Never uploaded without
   DICTO's OK.

Pushes batched: at most one or two a day.
