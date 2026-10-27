# The Red Queen 120-cell — study (DICTO 2026-10-27: "a polar swap of the White Queen"; name DICTO 2026-10-28)

**Status: stages 0–2 done (13/13 exact, red-queen-plan.pdf); stages 3–6 after the frugal week.** The polar (dual) of the 600-cell is the 120-cell: 120 dodecahedral cells, 600 vertices.
Polar swap: each vertex of the 600-cell ↔ a dodecahedral cell of the 120-cell; each tetrahedral cell ↔ a vertex.

**Expected by duality (to be checked exactly):**
- the 600 vertices of the 120-cell, round one dodecahedral cell, fall into the same 15 shells as the Cleo shells
  (20, 20, 30, 60, …): the core is the central dodecahedron's own 20 vertices — the polar swap of the Cleo core
  (20 Cleo-Icos filling an icosahedron ↔ 20 vertices of a dodecahedron);
- the 120 dodecahedra round one dodecahedron fall into layers 1, 12, 20, 12, 30, 12, 20, 12, 1 (the vertex layers of the
  600-cell round a vertex).

## Plan
1. Exact source model of the 120-cell (from the 600-cell by polarity), with checks (120 cells, 720 faces, 1200 edges,
   600 vertices; every cell a regular dodecahedron).
2. Polar atlas: slices and shadows in the four main directions (as #63), shells round a cell.
3. The swaps: how the slices and shells of the White Queen and her polar correspond.
4. Pictures; a polar view in the White Queen world (after the current stages).
5. Prior art: Coxeter, Regular Polytopes; Alicia Boole Stott's 120-cell section models; Schlegel diagrams of the 120-cell.

## Atlas (stage 3), 2026-10-28

**Verdict.** The 120-cell has 124 slice patterns on the near side of its centre in its four main directions (vertex-first
31, edge-first 45, pentagon-first 33, cell-first 15, tips included; 24, 40, 30 and 8 of them combinatorially distinct),
all exact in Q(√5); 17/17 exact checks pass. #63's one-pattern-per-gap lemma holds here too (checked: the cuts at 1/4,
1/2 and 3/4 of every gap have identical faces, and each face is the cross-section of exactly one dodecahedral cell).
Slice faces run from triangles to decagons; the largest slices have 120 vertices. Each shadow splits exactly into a front
half and a back half, each tiling it once.

Scale: corners = cell centres of the #63 600-cell (radius² 7/4 + 3/4√5, edge 1/2). Directions d = a corner, an edge
midpoint, a pentagon centre, a cell centre (= the 600-cell's cell-, triangle-, edge-, vertex-first directions; checked).

| direction | corner heights | gaps | patterns | face sizes | largest slice | tip |
|---|---|---|---|---|---|---|
| vertex-first | 16 | 15 | 31 | 3–8 | 108 v (gaps at 3/32+1/32√5, 7/32+3/32√5) | a corner |
| edge-first | 23 | 22 | 45 | 3–9 | 114 v (gaps at 3/64+1/64√5, 7/64+3/64√5) | an edge |
| face-first (pentagon) | 17 | 16 | 33 | 3–8, 10 | 120 v, 62 faces (gap at 5/32+11/160√5) | a pentagon |
| cell-first | 8 | 7 | 15 | 3,4,5,6,8,10 | 120 v, 62 faces (gaps at 9/32+1/8√5, 29/64+13/64√5) | the cell |

Uniform solids among the slices (exact: regular faces, one edge, one vertex type, inscribed, right dihedral count):
cell-first rhombicosidodecahedron (corner height 11/32+5/32√5), truncated icosahedron (mid-gap 47/64+21/64√5),
icosidodecahedron (9/8+1/2√5), truncated dodecahedron (mid-gap 19/16+17/32√5), regular dodecahedra from 5/4+9/16√5 (edge
φ × the cell's) to the tip (the cell); vertex-first regular tetrahedron at 13/8+3/4√5 and through the gap to the tip;
edge-first regular triangular prism (51/32+23/32√5); face-first regular pentagonal prism (3/2+27/40√5). The truncated
icosahedron and truncated dodecahedron are uniform only at mid-gap (two edge lengths at 1/4 and 3/4). The only
all-pentagon slices are the three cell-first dodecahedra. Regular decagons appear in face-first (centre, 2) and
cell-first (mid-gap 29/64+13/64√5, 12) slices; enneagons only edge-first.

Shadows (exact hulls): vertex-first 158 v, 240 e, 84 f (72 pentagons + 12 decagons); edge-first 180, 282, 104 (96
pentagons + 6 decagons + 2 12-gons); pentagon-first 160, 250, 92 (80 pentagons + 10 octagons + 2 regular decagons);
cell-first 80, 120, 42 (12 regular pentagons + 30 hexagons). Every non-pentagon face is a side-on cell flattened.
Front/back/side-on cells: 54/54/12, 56/56/8, 54/54/12, 45/45/30; front and back each tile the shadow once (exact volume).
Polar checks: each 120-cell shadow is the polar of the 600-cell's central slice in the same direction, and each 120-cell
central slice the polar of the 600-cell's shadow (V, E, F swapped, against #63's data).

- `scripts/atlas120.py` → `data/atlas120.json` (every slice: height, counts, face sizes, exact face kinds, vertex
  configurations, edge lengths, dihedrals; shadows; checks), `data/atlas120.pkl` (geometry for drawing). Runs in ~6 s on
  dicto-big-brother (12 processes).
- `scripts/render_atlas120.py` → `renders/atlas120-page.png` (one-page atlas), `renders/shadows120.png` (four shadows and
  their front halves).
