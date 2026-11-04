# DICTO's PET-ring RD cells (2026-11-04)
Ring = one per RD FACE (12/cell); tie = one per RD EDGE (24/cell); gap = at each RD CORNER (14/cell). Sphere model: r = R/2, ring plane at (√3/2)R, fcc centre distance √3 R,
so the ring towards a neighbour lies exactly in the shared RD face (shared ring), or two rings tie face to face.
scripts/ring_rd.py (single cell, three-fold axis upright: 3 top, 6 band, 3 bottom); scripts/ring_clusters.py (clusters, figure ring-tetrapod.png, data/ring-clusters.json).
Build sheet (shared rings / separate rings): 1 cell 12/12 rings, 24 ties; tetrapod 4 cells: 42 / 48 rings, 6 contacts, 76 tie points (16 of them join 3 rings) / 96 + k per contact;
octahedral 6: 60 / 72 rings, 12 contacts, 104 tie points (32 three-ring); fcc cube 14: 132 / 168 rings, 36 contacts, 224 tie points (80 three-ring).
Source brief: ~/Downloads/pet-ring-tetra-cluster.md (from DICTO's photos; items [confirm]).
