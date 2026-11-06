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

## The overlap version (scripts/overlap.py -> data-overlap.txt; float, the three thresholds checked to machine precision)
In the octet of edge 1, grow every Pacioli icosahedron about its centre by s:
- at s = 1 its 8 faces lie in the octet's (111) layer planes (the octahedron's faces), and its 3 golden rectangles lie in the cube planes
  through the octahedral sites, which hold whole square arrays of sites: the rectangles of all those cells share one plane (EKP's rectangles);
- neighbours first touch at s = sqrt5/2 (1.118034);
- the tetrahedral holes' centres are reached at s = 3/2;
- the grown icosahedra cover ALL of space exactly at s = phi; the last points covered are the octet's own corners (gauge = phi exactly).
So between sqrt5/2 and phi the icosahedra overlap EKP-fashion; at phi they alone fill space with overlaps (78% of space counted twice).
Next: where faces of overlapping neighbours become coplanar and continue (EKP's roofs); the same for the grown dodecahedra.

## Roofs (scripts/roofs.py on dicto-big-brother -> data-roofs.txt)
Coplanar faces of neighbouring cells (offset perpendicular to the face normal) meet edge to edge at:
- icosahedra (touch at sqrt5/2): the 8 faces in the (111) layer planes at s = 1 + sqrt5/2 (2.118034, 18 coplanar neighbours); the other
  12 (golden) faces at s = phi^2 (2.618034, 2 coplanar neighbours each);
- dodecahedra: touch at s = 3/2; coplanar faces meet at s = 3 exactly.
So the octet's roofs form deep in the overlap (beyond phi, where the icosahedra already fill space): a stronger-overlap analogue of EKP.
