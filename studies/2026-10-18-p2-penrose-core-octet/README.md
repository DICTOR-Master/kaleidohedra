# Project 2 — Penrose-core octet (DICTO 2026-10-18)

DICTO · dictospheres.com

Scope: studies/2026-10-18-kit-projects/SCOPE.md. Source: studies/2026-10-18-ocd-octet (keyless kit, steps 18–20; Fable review ba28bd0). DICTO: whole middle piece (minimal set). Octahedron edge for printing: 60 mm.
**Minimal set: notched octahedron + middle piece + notched tetrahedron (left and right) — 3 shapes (+ mirror).**

## Step 1 — the pieces (`scripts/p2_meshes.py` on dicto-node → `data/p2-meshes.json`; exact from the octet study)
- **Notched octahedron** = OCD + its 6 notched caps fused = octahedron minus its 12 middle-piece shares: exact **8/57 + 104√5/171 = 1.500299**; one solid; sphericity 0.621.
- **Middle piece** M₀ = hull of two facing five-kite stars minus both OCDs: exact **(310 + 26√5)/4617 = 0.079735**; one solid; sphericity 0.579; one per octahedron edge (6 per cell). The OCD's stars still shape it although the OCD is fused away. Its Penrose prisms (central thick rhombus + two flanking) are not cut out in this set.
- **Notched tetrahedron** = T+ minus its 6 middle-piece shares: exact **26/81 − 2√5/81 = 0.265776**; one solid; sphericity 0.517; left and right.
- Exact bookkeeping: 1 notched octahedron + 6 middle pieces + 2 tetrahedra = (32 + 16√5)/27 = the cell. ✓
## Step 2 — 3D page (`scripts/kit_viewer_template.html` (now takes a turn per placed piece), `scripts/p2_page.py` → `renders/p2-penrose-core-octet.html`, claude.ai/artifact/BAQrqDmtUuuNUeXe4aexg4)
- Views: the set, round one octahedron (12 middle pieces, 8 tetrahedra), network (middle pieces hidden so the notches show).
## Next
- Fable check of this fused set (queued); STL at 60 mm; names.
