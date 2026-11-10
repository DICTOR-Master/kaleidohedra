# The permutohedron (10 Nov 2026; DICTO: "is this the shape of the permutahedron?!", "can we build a permutahedron", "the space filling
non repeating shape we have been trying to build can that be seen too")
- data-perm4.json (scripts/perm4_data.py, FINAL ok): the 4D permutohedron: 120 corners, 240 edges, 30 cells (10 truncated octahedra,
  20 hexagonal prisms), simple; generic sweep 26 births, 66 swaps, 26 deaths = h (1, 26, 66, 26, 1).
- Page "The 4D Permutohedron" (private): https://claude.ai/artifact/4JBSn6kB49hM3saKKMeN12 (Build: Schlegel view from just outside one
  truncated octahedron, pull apart, cell kinds; Sweep: the 66 swaps lit). Source the-4d-permutohedron.html.
## Slice test (scripts/slice_test.py): slices of the 4D permutohedron honeycomb (Voronoi cells of A4*) as power diagrams
Distinct cell shapes (congruence, 5-digit squared distances) in balls of radius 2.4 / 3.0 / 3.4 round the origin, slice offset 0.1234567:
- rational direction [1,-1,0,0,0]: ONE shape (89, 265 cells) - a repeating one-piece filling.
- generic directions (t = 0.1 … 0.9 towards golden): new shapes almost as fast as cells (e.g. t = 0.9: 130 / 215 / 296 of 159 / 298 / 458).
- GOLDEN [1, φ, φ², φ³, φ⁴]: 80 / 114 / 139 shapes of 154 / 306 / 462 cells: strong recurrence, share of new shapes falling 52 → 37 → 30 %;
  not levelled off within the reliable sizes. (Radius 4.4 unreliable: lattice edge; discarded.)
Reading: a non-repeating filling is seen as a golden slice of the repeating 4D permutohedron filling; plain slicing gives no finite shape set
(yet). NEXT options: count by combinatorial type; the projection (window) route that gives Penrose-type finite tile sets; larger balls for
the golden slice.
## Count by combinatorial type (DICTO "yes count shapes by type"): NOT YET TRUSTWORTHY
Face-corner graph hash per cell (tolerant merging 1e-6). Rational: 1 type (89 / 173 / 265 cells). Generic t = 0.5: 64 / 101 / 137 types.
Golden: 58 / 98 / 145 types - MORE than its 139 congruence classes at radius 3.4, impossible: golden slices have near-degenerate faces
(corners nearly meeting) that floating point cannot resolve. First run (no tolerance) gave even more (141 at r 2.4): discarded.
NEXT: exact golden arithmetic (as #81's chains) for the golden slice's combinatorial types.
## The 4D Vacuus (DICTO: "B the 4D vacuus is its form"; scripts/vacuus4d.py, FINAL ok)
As the 3D Vacuus solids are built from central great polygons carrying all edges (octahedron 3 squares, cuboctahedron 4 hexagons), the 4D
one is built from central 3D slices carrying all 2-faces. The 4D permutohedron's 150 2-faces (60 hexagons, 90 squares) lie in 65 central
hyperplanes; the slices: 20 x (24 corners, 14 faces: 6 squares + 8 hexagons, 2 hexagons carried), 13 x (32 corners, 22 faces), 10 x
(24 corners, 20 faces), 6 x (34), 5 x (36, 30 faces), 5 x (36, 28 faces), 1 x (40), and 5 x (24 corners, 14 faces = TRUNCATED OCTAHEDRA,
each carrying 6 squares): the 3D permutohedron sits at the centre of the 4D one five times - DICTO's "does it infinitely nest in itself".
(Slice shapes from float hulls; types by corner and face counts; congruence of the TO slices to be checked exactly.) No build wanted
(DICTO: "I dont need a build im just in a state of wonder").
## The 4D Vacuus, EXACT (11 Nov; scripts/vacuus4d_exact.py, data-vacuus4d-exact.json, FINAL ok) - SUPERSEDES the float slice types above
65 central hyperplanes carry the 150 2-faces (each face in exactly one). Under S5 x (+-1) they form FOUR congruence classes (the float run
split one class by rounding):
- 30 x normal (8,3,3,-7,-7) [split (1,2,2)]: 32 corners, 52 edges, 22 faces (14 squares, 8 hexagons); carries 2 squares
- 20 x (9,-1,-1,-1,-6) [split (1,1,3)]: 24 corners, 14 faces (6 sq, 8 hex) = truncated-octahedron TYPE, edges^2 2 and 56/9; carries 2 hexagons
- 10 x (3,3,-2,-2,-2) [split (1,3,1)]: 24 corners, 42 edges, 20 faces (18 sq, 2 hex); carries 2 hexagons
-  5 x (4,-1,-1,-1,-1) [split (2,1,2)] = slices "x_i = 3, the middle value" = permutohedron of (1,2,4,5): truncated octahedron TYPE,
   edges^2 2 (24) and 8 (12): regular squares, hexagons with sides alternating sqrt2, 2sqrt2; carries 6 squares (its own 6 squares).
Every face of every class verified exactly (plane + all corners strictly on one side), Euler 2.
## The five central truncated octahedra slot together (scripts/crossing5.py, exact, PASS)
Two of them (x_i = 3, x_j = 3) cross in the central plane x_i = x_j = 3: no corner or edge of the 4D solid lies on it; the section is a
REGULAR HEXAGON, corners the permutations of (2, 0, -2) on the other three coordinates, side^2 = radius^2 = 8. Ten such hexagons; three
central TOs share a segment; all five meet only at the centre.
## The Vacuus count in every dimension (scripts/vacuus_general.py, brute force n = 3..9, FINAL ok)
Ridge = ordered split (B1,B2,B3), sizes (a,b,c); its central hyperplane has normal c1 = bc(b+c) on B1, c2 = -ac(a+2b+c) on B2,
c3 = ab(a+b) on B3 (closed form checked against exact elimination for every ridge). N(n) = three-valued + two-valued:
three-valued = sum over a<c of n!/(a!b!c!); two-valued = 2^(n-1) - 1 (n odd), 2^(n-2) - 1 (n even) (FIRST formula C(n,b) per a=c FAILED
for even n: (a,b,a) and (b/2,2a,b/2) give the same hyperplane when b is even - corrected and rechecked).
N = 3, 15, 65, 225, 770, 2443, 7761 for n = 3..9 (dimensions 2..8). OEIS 11 Nov: no match for 3,15,65,225,770,2443 nor for the three-valued
part 3,12,50,210,707,2380 (prior-art search continues before any novelty claim).
