# Project 1 — Golden-key octet (DICTO 2026-10-18)

DICTO · dictospheres.com

Scope: studies/2026-10-18-kit-projects/SCOPE.md. Source: studies/2026-10-18-ocd-octet (keyed kit, step 5; Fable review ba28bd0).
**Minimal set: keyed octahedron + dented tetrahedron (left and right) — 2 shapes (+ mirror).** Octahedron edge for printing: 60 mm (DICTO).

## Step 1 — the pieces (`scripts/p1_meshes.py` on dicto-node → `data/p1-meshes.json`)
- **Keyed octahedron** = the octahedron |x|+|y|+|z| ≤ 2φ/3 with its 8 golden-envelope corner keys (the OCD and its 6 caps fused). Exact volume −32/9 + 64√5/27 = **1.744754** (octahedron (64 + 32√5)/81 + 8 keys (−44 + 20√5)/81); one solid; **sphericity 0.852**.
- **Dented tetrahedron** = T+ minus the 4 keys entering it: 64/27 − 8√5/9 = **0.382754**; one solid; sphericity 0.620; chiral (T− is its mirror image, Fable).
- Exact bookkeeping: keyed octahedron + 2 tetrahedra = (32 + 16√5)/27 = the cell. ✓
- Mesh note: the union is made with each key given a small inward tip inside the octahedron (`tipped`), so float round-off cannot leave a hair gap at the key bases; the volume is unchanged (1.744754).
## Step 2 — 3D page (`scripts/kit_viewer_template.html` (reusable for all kit projects), `scripts/p1_page.py` → `renders/p1-golden-key-octet.html`, claude.ai/artifact/BMcKgGY7iAYGZsWbQMWpE9)
- Views: the set (2 shapes + mirror), round one octahedron (8 tetrahedra), network.
## Next
- Fable check of the fused set (queued after the running two-shape review); STL at 60 mm edge; names (DICTO's scheme) — propose, then DICTO approves.
