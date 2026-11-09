# Merged sliders: one plane from the cube–RD and cube–octahedron sliders (DICTO 10 Nov 2026)
DICTO: "two of our sliders could be merged to generate the piece with the necessary pattern: one slider goes from cube to RD and
the other from cube to octahedron". Chosen: option A (search the merged plane) for the c/h layering keys.

**The plane.** P(λ, μ) = cube {|xᵢ| ≤ 1} ∩ λ·RD {|xᵢ|+|xⱼ| ≤ λ} ∩ octahedron {Σ|xᵢ| ≤ μ}, λ ∈ [1, 2] (2 cube, 1 Kepler's RD),
μ ∈ [1, 3] (3 no cut, 1 octahedron). It holds the cube, RD, octahedron, cuboctahedron (2, 2), truncated octahedron (λ ≥ 1.5, μ = 3/2)
and the Delian walk's O(t) (RD with its corners cut by octahedron planes).

**Step 1, the Dehn map (dehn_map.py, grid 0.02, FINAL ok).** Every dihedral angle is a rational multiple of π plus k·θ,
θ = arccos(1/√3), so the Dehn invariant is L ⊗ θ with L = Σ edge length × k, and a piece can fill space only where L = 0.
- L = 0 throughout the part without an octahedron cut: the whole cube → RD slider (angles 90°, 120°, 135° only).
- L = 0 exactly on the line μ = 3λ − 3, λ ∈ [1.5, 2], from the truncated octahedron's corner (1.5, 1.5) to the cube (2, 3):
  pieces with all 26 faces (6 cube, 12 RD, 8 octahedron: the rhombicuboctahedron's pattern); |L| < 10⁻¹⁴ at (1.55, 1.65),
  (1.75, 2.25), (1.95, 2.85).
- L = 0 at the truncated octahedron (μ = 3/2). Octahedron +33.94, cuboctahedron −33.94 (neither fills space, as known).
Dehn zero is necessary, not sufficient. Among convex pieces with full cubic symmetry, the ones filling space by translation are the
parallelohedra: cube, RD, truncated octahedron.

**Next, step 2 (the keys).** Cut only the two corners on the layering axis [111] (top and bottom) with octahedron planes, which
leaves two triangular faces whose orientation (0° or 60°) is a key; test the Dehn condition for these 3-fold pieces across the plane,
then on stacks of 2–3 layers whether the triangles force c, force h, or allow both.

## Step 2, the keys: geometry first (hole_count.py, FINAL ok)
Correction to the plan above: a cell's corner on the layering axis points into a tetrahedral hole where FOUR cells meet, not into
the cell above; cutting only those two corners leaves holes no single piece can fill.
Repair: between two close-packed layers every tetrahedral hole has exactly one 'axis' cell (its top or bottom 3-fold corner points
straight at the hole), and every cell is the axis cell of exactly two holes, one above and one below (checked for ABC, AB, ABCACB,
ABCBAB). So a consistent bump-and-notch scheme exists for ANY stacking: each cell's two axis corners become bumps (triangular pyramids
cut by octahedron planes, size set by the slider μ), and at each hole the three other cells' corners are notched to receive the bump.
The bump's triangle fixes how the next layer turns; top and bottom bumps opposite (RD-like, D3d) force c, alike (TRD-like, D3h) force h.
Consequence: one piece with fixed keys forces pure c or pure h; an aperiodic c/h word needs keys that carry hierarchy information
(Chair44-type), e.g. via Kamenetsky's frame-marking (arXiv 2610.00916, study 2026-11-10-arxiv-scan).
Next: (a) build the RD-based bump/notch piece across μ and check volume, Dehn and the pure-c forcing on 3-layer stacks; (b) the
TRD version for pure h; (c) the hierarchy layer.
