# The White Queen 600-cell (#63) — study

**One-line conclusion (step 1).** The 600-cell has 62 slice types on the near side of its centre in its four main
directions (vertex-first 9, edge-first 17, face-first 21, cell-first 15, tips included), all computed exactly in Q(√5);
every slice between two vertex heights has triangles and squares, and the all-triangle slices are exactly the
vertex-height ones listed in #62.

**Status.** Step 1 (complete slice atlas, four shadows, Humpty Dumpty picture) done 2026-10-27. Equal-edged forms are
solved with full symmetry; forms with less symmetry may exist and are queued as a separate later study (QUEUED,
low priority).

- `scripts/atlas600.py` — slices at every vertex height and one inside every gap (one combinatorial type per gap),
  exact hulls; uses the modules of study 2026-10-27-4d-shadows. Output `data/atlas600.json`, `.pkl`.
- `scripts/render_atlas.py` — `renders/atlas600.png` (all slice types), `renders/shadows600.png` (four shadows;
  the 48-vertex cell-first slice beside Humpty Dumpty = Slice-48 of #62).
- Names (DICTO 2026-10-27): Humpty Dumpty = the real 48-vertex cell-first slice (the egg); Fallen Humpty (placeholder) = its equal-edged form, Slice-48 of #62. Carroll material belongs to #63 only.

## White Queen world, step 1: the source model (2026-10-27)
`scripts/export_source.py` → `data/600cell-source.json` (40 KB): the 600-cell from its definition, exact (each coordinate
a + b√5), with edges, triangles and cells FOUND by measurement. 13 exact checks, all PASS: 120 vertices on radius 2;
720 edges all √5 − 1; degree 12; 1200 triangles; 600 cells; Euler 0; each triangle in 2 cells, each edge in 5, each vertex
in 20; every vertex figure an icosahedron; every cell regular. The app world will read only this file (step 2) and a test
will match its slices to atlas600.json (step 3).

## Squares = cell mid-cuts (DICTO: "the squares can be octahedrons"), 2026-10-27
`scripts/squares_midcuts.py` (exact): a four-sided face is a cell cut through four edges. Exactly 46 of the atlas's
four-sided faces are mid-cuts of a cell (cut parallel to two opposite edges, halfway between them = the equator of the
cell's midpoint octahedron): 30 at the vertex-first gap at height (3+√5)/2 ≈ 2.618, 5 + 5 at two edge-first gaps, 6 at the
cell-first centre. This equals the 46 true squares found by shape (Fable check, floats), so the squares of the atlas are
exactly the octahedron equators.
