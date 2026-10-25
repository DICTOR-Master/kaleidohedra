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

NAMES (DICTO 2026-10-25): the gyrated pair = DICTO Sonsam (tet-hole piece) and DICTO Lahdeli (oct-hole piece); keyed: DICTO Sonsam-K, DICTO Lahdeli-K.
Keyed choice (DICTO 2026-10-25): keying 1 (tet->oct A, K = 0.8) = DICTO Sonsam-K + DICTO Lahdeli-K (files kg-TOA-*.obj).

TWIN STOPS (twin_stops.py, render_twin_stops.py → twin-stops.png): gyrated octet stops beyond the octet. 5/24: oct piece = 60° rhombohedron edge 1/3 (KNOWN, fcc primitive cell), tet piece 16 corners (6 tri, 3 sq, 4 hex) vol 0.340459; 3/8: oct vanish, tet piece 10 corners (6 tri, 3 sq, 1 hex) vol √2/4 = twinned counterpart of the Delian cube stop. Candidates for names after a literature check.
KEYED IAN DURY (keyed_iandury.py, render_keyed_iandury.py → keyed-iandury.png): stop 5/24, K = 0.8. Valid: 1 Ian Dury → rhombohedron cones (Ian Dury 0.311139, rhombohedron becomes a six-pointed star 0.084853); 2 teeth (0.327062 / 0.053007); 3 rhombohedron → Ian Dury cones (rhombohedron left a thin skeleton 0.009453). Reverse teeth invalid (genus 4).
