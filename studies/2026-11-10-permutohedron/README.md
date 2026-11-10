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
