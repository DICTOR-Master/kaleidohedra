# OG vs the uniform H4 polytopes (11-12 Nov 2026; DICTO 11 Nov: "so is it possible that the OG is the same form as a 4D polytope")
Question: does any slice or shadow of a uniform H4 polytope (axis = a 600-cell vertex, the icosahedral axis) have the OG's signature,
102 corners and 80 faces = 20 hexagons + 60 four-sided?

## Status: PARKED, no result (12 Nov)
- `scripts/og_4d_slices.py` (11 Nov pilot, 4 polytopes): face/corner count faulty (neighbour-chain merging; collinear points as corners).
- `scripts/og_4d_all.py` (12 Nov, all 15 by Wythoff construction): faults found by its controls and fixed: orbit float drift
  (near-duplicate vertices; now snapped keys + merge), per-name vertex counts now right in the pilot (e.g. runcitruncated 7200).
- STILL FAULTY: shadow face types fail the symmetry check (an H3-symmetric shadow has face classes made of orbits of 12, 20, 30, 60,
  120; the pilot gave e.g. 106 four-sided, 3 seven-sided). Corner/face incidence is not yet right for large hulls. No slice or shadow
  verdict may be taken from it.
- Before any rerun: add the orbit-size check as a control (every side class a sum of 12, 20, 30, 60, 120), find the incidence fault,
  then run on a compute machine (pilot did not finish 15 polytopes in 240 s).
