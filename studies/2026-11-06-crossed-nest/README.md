# The crossed nest (DICTO 11-06: "the stella octangula stood for the tetrahedron in EKP and the Kepler star; I wonder if there could be a
further refinement crossing further elements"; "that was the interesting part of EKP: overlap of cells, which made the roofs work throughout
and the rectangles")
Every level a Kepler-style compound of crossed solids whose common core is the next solid. scripts/compounds.py -> data-compounds.txt.

**Results (float, cores by a robust plane-triple method; the first core routine was wrong and is replaced):**
- cube (or octahedron's face centres): 2 tetrahedra crossed (stella octangula) -> core = octahedron.
- dodecahedron corners: 5 cubes crossed -> core = rhombic triacontahedron; 10 tetrahedra crossed -> core = icosahedron (edge = D edge / phi);
  each of the two chiral 5-tetrahedra compounds -> core = the same icosahedron.
- icosahedron edge midpoints: 5 octahedra crossed -> core = icosahedron of edge 1/phi, same orientation: a CROSSED GOLDEN LOOP,
  icosahedron > 5 octahedra > icosahedron > ..., shrinking by 1/phi each turn.
All these compounds and cores are classical (Kepler, Coxeter's compounds). Next (DICTO's EKP point): the overlap version - let solids cross
the octet's cell walls as EKP's dodecahedra cross the cube faces, and look for faces continuing through the lattice (roofs, golden rectangles).
