# Fable review 4 — the keyed star-centred W (2026-10-18)

DICTO · dictospheres.com — DICTO: "I want this piece if possible to have the rhombi pattern continued along its edges as a key with itself … they all have to show because they are all keying joints, I don't need the star on the edges just a lobe or two, same scale as star though." Built and checked by Claude Fable 5.1. Research branch only.

**3D page:** `renders/p4-keyed-W.html` (study renders; copy here in `renders/`) — published at https://claude.ai/artifact/9WH92CtD2ZLovmrqjY369u (private until DICTO shares it). Views: one keyed W · bump meets dent (pull apart along the face normal) · 12 round one OCD · the set · unkeyed W for comparison · network.

Scripts: `scripts/explore_face.py` (what the bump face looks like: socket rim, OCD shadow, kite shape, where the star's edges pierce the face), `scripts/fable4_keyed_W.py` (the geometry, from exact OCD data → `data/keyed-W-geometry.json`), `scripts/fable4_node.py` (dicto-node, manifold3d: build + checks + 6 000 000 sample points → `data/fable4-node.json`), `scripts/fable4_page.py` (the page).

## 1. The design, and why
- **Which faces bump, which dent.** The 8 flat W–W faces of the star-centred W pair bipartitely across the structure (p4_key_pairing): across a face F the neighbour is g(W) with g a 3-fold turn about the OCD centre, and the face it presents is g(F′) with F′ in the other class. Bump faces = the four containing an edge end together with the OCD centre of the same side (A0E0T±, A1E1T±); dent faces = A0E1T±, A1E0T±. The pattern is defined on one bump face and carried to the other three by W's own 2/m symmetry (mirror x = 0, inversion through the edge midpoint); each dent is the g⁻¹-image of the bump of its partner face. That is the only choice that keeps **one identical piece** whose bump fills its neighbour's dent exactly, for every placement of the piece in the structure (the pattern's 2/m invariance makes the placement unique up to the site symmetry).
- **"Continuing the star pattern".** The socket shows one five-fold star of the OCD (5 kites round the star centre). On each bump face exactly **two rim edges of that star** (long kite edges, 0.2379) pierce the face plane inside the face triangle. The key tile is a planar **kite congruent to the star's kite** (long edge 0.2379, short edge 0.1971, angles 55.7° / 117.8° / 68.6° / 117.8°), set with its 55.7° apex just beyond the piercing point and one long edge running along the pierced edge's line, so the kite reads as the star's next kite carried onto the flat face — "a lobe", same scale as the star. Only one of the two pierced edges leaves room for a kite inside the face (the other runs out of the face at once), so each bump face carries **one kite** = 4 bumps + 4 dents per W; every face shows a key.
- **Clearances, honestly.** The continued edge line is also the OCD's silhouette in that face plane, so a kite exactly on it would touch the OCD. The kite stands **1.4 mm beside** the line (parallel), its apex **2.0 mm** along the line from the rim, and it is **turned 4°** so that it keeps 1.4 mm from the piece's edges and 1.3 mm from the OCD (grid search over shift / clearance / turn; an exact 0° continuation leaves < 1 mm somewhere). The step-8/9 lattice drawings are not used.
- **Relief.** Bump = kite frustum, height 2.0 mm (0.05), walls 30° off the face normal (the top kite is 70 % of the base, long edge 6.5 mm); dent = the same frustum sunk. Sloped walls are what lets the pieces be pushed together one by one.

## 2. Checks (dicto-node, manifold3d)
- Keyed W: **one solid, genus 0**, volume = unkeyed W to 1e-15 (bumps 0.006035 = dents 0.006035, one key 0.001509), 108 corners, ψ 0.647; sharpest edge 75.4° (the cell's own edge, unchanged), no slivers.
- Pair across a face (W and g(W)): overlap 0, union = both cells minus the OCDs, gap 0 — the bump fills the dent exactly.
- 12 keyed W round one OCD: 66 pairs, max overlap 2e-19, union = 12 W + OCD exactly.
- Tiling OCD + keyed W: 2 000 000 uniform + 2 000 000 near-relief + 2 000 000 near-face points: **0 uncovered, 0 double**. (Exact statement: cells tile, OCDs are disjoint, every bump is the exact image of the dent it fills, all bumps lie inside the neighbour's cell and outside the OCDs — checked on the frusta's vertices and by the booleans.)
- Locking: a pair separates only by translations within 43° of the shared face normal (47 of 312 outward directions tested); in the 12-ring round an OCD **no W can be translated out** (0 of 600 directions; the unkeyed W: 41 free). Assembly: set the OCD, add the W pieces one by one, each pushed on along its bump-face normal (its two bump faces touching already placed pieces are the A0E0-type pair, whose normals are 60° apart — the 30° walls and the 43° cone make the common push direction possible); the ring closes with the last piece pushed radially onto the OCD.

## 3. Buildability at a 60 mm octahedron edge (1 unit = 39.33 mm)
- W_star body: 60 × 42 mm lens, 7.5 mm thick at the centre (unchanged by the keys).
- Keys: kite 9.4 / 7.8 mm edges, 14.7 mm long, 2.0 mm high, top 6.5 mm; walls 30° off normal; 1.4 mm from the piece's edges, 1.3 mm from the OCD socket; dent walls to the adjacent face ≥ 1.4 mm thick. Nothing thinner than 1.3 mm anywhere; no edge below 75°.
- Print tolerance: a 0.1–0.2 mm offset of the bump (or dent) will be needed for a fit; not applied in the model.

## 4. Open points
- One kite per face is the honest limit at star scale; a second lobe would have to be smaller (not "same scale").
- Should the dents rather be on the A0E0/A1E1 faces and bumps on the others? Geometrically equivalent (swap g and g⁻¹); the choice only decides which faces look raised.
