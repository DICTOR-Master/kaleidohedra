# The premise challenge: why pieces stack freely in HexOct but not in #47 (DICTO 11-06)
DICTO, on HexOct's Fibonacci figure (Figure 7.1, rock salt at lambda = 1/3): "you can clearly see cubes, tetrahedrons and could be
octahedrons stacking freely together", against #47's limits for regular C + T + O; "I could question an assumption or premise".
DICTO proposed the answer: the freedom comes from the premise; let the pieces deform. Worked out here ("yes work it out").

**Conclusion:** in a close-packed stacking with rock-salt sites (balls and octahedral holes weight lambda, tetrahedral holes 0), the pieces
in cubic stretches are always regular: for lambda >= 3/8 exact cubes (edge 1/sqrt2), for lambda < 3/8 cubes with their corners cut by
REGULAR octahedra of edge 2(3/8 - lambda) (the tetrahedral holes' pieces; a non-uniform truncated cubic honeycomb). All the freedom of
stacking is carried by the few pieces that touch a hexagonal layer, which deform, and their shape depends only on the layer kinds
(Rule of Halves). No regular tetrahedron occurs at any lambda: the tetrahedral holes give octahedra (cubic) or a 7-cornered piece
(4 triangles, 3 squares, equal edges; next to hexagonal layers). Status: worked out (float, exact checks to do); for DICTO.

| lambda | cubic stretch (S:c, O:cc) | tetrahedral holes | ball in h layer (S:h) | octahedral hole next to h (O:ch = O:hc) |
|---|---|---|---|---|
| >= 3/8 | cube, edge 0.7071, vol 0.353553 | none | 14 corners: 6 triangles + 6 pentagons, vol 0.368285 | 10 corners: 1 triangle, 3 squares, 3 pentagons, vol 0.346188 |
| 1/3 (Fig. 7.1) | truncated cube (8 triangles + 6 octagons), vol 0.353281 | regular octahedra edge 1/12 (cubic); 7-corner pieces (hexagonal) | 36 corners | 24 corners, vol 0.345949 |
| 0.30 | truncated cube | regular octahedra edge 0.15 | 36 corners | 24 corners |

- Octahedron edge = 2(3/8 - lambda) at 0.30, 1/3, 0.35 (0.15, 0.0833, 0.05); they vanish at 3/8, where the cubes close: 3/8 is HexOct's own
  end of the walk (#75: c pieces become cubes, h pieces Narcissus).
- Against #47: there, regular C, T, O of edge 1 fill space only in flat slabs and never face to face (Theorem 2). Here cubes and regular
  octahedra fill space together in every stacking order, face to face in the cubic stretches, because the pieces at hexagonal layers
  are free to take other shapes: the stacking's freedom lives in two deformed pieces (lambda >= 3/8).
- scripts/cell_shapes.py <lambda>: exact power cells (same sites and weights as fibonacci tower69.py / #64), per kind, for pure cubic,
  pure hexagonal and the 16-layer Fibonacci word. Float; exact (rational / sqrt2) coordinates to do.
- Open: names of the deformed pieces (DICTO's); exact forms; whether the 7-cornered tetrahedral-hole piece has a classical name; prior art
  (truncated cubic honeycomb and rock-salt power cells are classical; the per-layer split is #57's Rule of Halves).
