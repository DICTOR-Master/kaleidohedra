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
- Names: Humpty Dumpty = Slice-48 (DICTO 2026-10-27). Carroll material belongs to #63 only.
