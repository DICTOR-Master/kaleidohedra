# Project 3 — Golden envelope octet (DICTO 2026-10-18)

DICTO · dictospheres.com

Scope: studies/2026-10-18-kit-projects/SCOPE.md. Source: studies/2026-10-18-ocd-octet steps 21–27; prior art: studies/2026-10-18-envelope-network. Octahedron edge for printing: 60 mm.
Golden envelope (rhombic triacontahedron) on every octahedron of the octet; envelopes never overlap and fill exactly 10/φ⁶ = 55.73%. The OCD is optional (a passenger inside).

## Sets
- **3 · Two-shape set:** envelope + grown core piece (cube of edge R round each tetrahedron centre, minus the envelopes), 0.555671, left and right. Fable review running (octet study fable-review-2).
- **3b · Cuboctahedron set:** envelope + φ⁻² vertex cuboctahedron ((−320 + 160√5)/81, exactly ⅓ of the envelope) + wedge (0.005504) + cut-down tetrahedron L/R (256/81 − 104√5/81 = 0.289493). 4 shapes (+ mirror).
- **3c · Cuboctahedron + dodecahedron set (new, DICTO 10-18):** as 3b with each cut-down tetrahedron split into
  - the **central dodecahedron** (`scripts/p3c_dodeca.py` → `data/p3c-dodeca.json`, exact corners): **12 pentagons, 20 corners, volume −146/27 + 22√5/9 = 0.058537**, three edge lengths (squared 5/9 − 2√5/9, 4 − 16√5/9, 50/9 − 22√5/9), face angles 63.43°/116.57° (golden), 90°, 121.72°, 148.28°; it keeps only the 12 turns of the tetrahedron (no mirror) → **left and right**, the symmetry of a tetartoid; centred on the tetrahedron centre; **sphericity 0.855** (the chunkiest piece after the envelope);
  - the **shell** round it (`scripts/p3c_split.py` on dicto-node → `data/p3c-split.json`): **one solid**, 0.230956, sphericity 0.48, left and right.
  - 3c = envelope, cuboctahedron, wedge, dodecahedron L/R, shell L/R: 5 shapes (+ mirrors).
## 3D page (`scripts/p3_page.py` + `kit_viewer_template.html` → `renders/p3-golden-envelope-octet.html`, claude.ai/artifact/FBjG7XTk3xFykgUCfyGQXS)
- Views: 3 two-shape set, 3b cuboctahedron set, 3c cuboctahedron + dodecahedron set (all round one envelope), and the 3c pieces laid out.
## Next
- Fable verdict on 3 (running); Fable check of 3b/3c; exact volume of the 3c shell (= cut-down tetrahedron − dodecahedron = 256/81 − 104√5/81 − (−146/27 + 22√5/9)); STL at 60 mm; names.

## Fable review 2 (octet study fable-review-2, 8af2336)
- Set 3 (two-shape) PROVED EXACTLY. The central dodecahedron of 3c is exactly a **tetartoid**.
- **3b and 3c contain the step-24 wedges, which are spikes attached by slivers (not buildable)** — to rework without wedges before STL. Fable's alternative: **envelope + W** (W = rhombic dodecahedron round each octet vertex minus its 6 envelope bites; achiral; contains the φ⁻² cuboctahedron) — two shapes, no mirror pair.
