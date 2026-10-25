# Hidden bonds (2026-10-25, DICTO: "hiding in plain sight?!", "another rhythm … tripling", "a different but cohesive bond network", "is there a keyed pair possible too")

- hidden_bonds.py → hidden_bonds.txt/json: meaning points (piece-volume ratio 1, 2, 3, 4 and inverses, φ^±1, φ^±2, silver) on 7 census walks (floats).
- equal_volume_exact.py → equal_volume_exact.txt, exact_roots.txt: exact equal-volume points.
  Delian: lam = 3/8 − ∛4/4 (the Delian cube root itself). Gyrated octet (hcp holes): root of 1536l³+5184l²−3384l+11 (≈0.003266957, irreducible),
  pieces: tet 19 corners (6 triangles, 3 pentagons, 3 hexagons, one 9-gon — the 9-gon is a tet|tet face across the twin plane), oct 12 corners (2 triangles, 6 pentagons).
  C15: root of 7l³−39l²−1779l−1093 (≈−0.6238783, irreducible), Frank–Kasper Z12/Z16 cells, 64/3 each (known).
  NOTE: sympy solve + is_real dropped the two cubic roots; solved with Poly.nroots.
  Equal volume itself is trivial (same site density → average volume); the shapes are the content.
- keyed_gyrated.py (K env = key size) → keyed_gyrated_K*.png/txt: keyed gyrated pair. BUG FIXED: a removed key whose base lay exactly on the face
  became an internal hollow (volume still "conserved"); base now pushed 1e-4 past the face. At K = 0.8: tet→oct A, tet→oct B, oct→tet A give single
  genus-0 pieces; oct→tet B overlaps (genus 4). Renders here are flat; proper renders with render_keyed.py style still to do.
- Sunstar reading (not yet written): #42's dodecahedra + Dogstars sit on rock salt's switch point (cubes), keyed by Euclid's six roofs
  (dodeca 14.472 + Dogstar 1.528 = 16 = two cubes, edge 2).
