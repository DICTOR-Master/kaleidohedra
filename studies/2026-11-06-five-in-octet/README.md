# All five Platonic solids in the octet (DICTO 11-06)
DICTO: "we only need to get them all in octet and then make the adaptors out of the pieces themselves"; "a lattice of five shapes, the
Platonic solids"; "do we need the shapes inside each other too? do they shake into the spaces"; "if we had a few different combis of the
nesting they might be easier to place together at slightly different scales"; "how about the 3d wave and harmonics angles".

**Conclusion so far:** (1) Kepler's nest in every octahedron of the octet (edge 1): O 1 > I sqrt2/phi^2 (Pacioli) > D 0.2913 > C sqrt2/3 >
T 2/3, the octet's tetrahedra between: one lattice holding all five Platonic solids, periodic in three directions (answers #47's question
4 for the all-five mix, with freely sized solids). The nest's cube is exactly the octahedron's dual cube (corners at its face centres), so
the dodecahedron touches the octahedron at 8 points. (2) 12 classical inscriptions, 14 chains through all five. BOTH octet cells hold a
five-chain: T 1 > O 1/2 (edge midpoints) > I > D > C is the octahedron's chain at half size; so every cell of the octet carries all five,
at two scales a factor 2 apart. Status: nest exact-checked (float), catalogue done; shaken (gravel) version next.

- scripts/nest.py: the nest, every solid regular, each inside the next, volumes; per fcc cell 4 nests + 8 tetrahedra = the cell volume.
  Gaps per octahedron: O-I 0.127520 (Admiral Caps), I-D 0.154379, D-C 0.084750 (Euclid's six roofs), C-T 0.069838 (four corner pyramids).
- scripts/nest_catalogue.py -> data-nest-catalogue.txt: inscriptions with edge and volume ratios, and the 14 five-chains.
  Notable: D 1 > C phi > I 1: the icosahedron inside the cube inside the dodecahedron has the dodecahedron's own edge.
  C 1 > I 1/phi > D 1/3. T 1 > O 1/2 > ... = O-chain at half size.
- figure five-nest.png (papers-to-read/five-platonic-nest-in-octet.png).
- Prior art: the single inscriptions are classical (Pacioli, Kepler's Mysterium and Harmonices, Euclid XIII, Coxeter); a full table of chains
  and the octet lattice of nests: to check before any claim.
- Next: gravel ("shake into the spaces"): pieces placed at the 3D wave field's darkest points and turned by the gaps' harmonics; mixes
  of nests at near-matching scales.
