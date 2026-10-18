# Project 4 — Golden octet adaptor (DICTO 2026-10-18)

DICTO · dictospheres.com

**DICTO 10-18:** "wondering about fusing all as one piece, and as adaptor to any golden envelope solid — golden octet"; "and two shape set as solid too"; "as well as any golden envelope adaptor".
Source: studies/2026-10-18-p3-golden-envelope-octet (golden envelopes in the octet, exact 10/φ⁶).

## Step 1 — exact (`scripts/p4_adaptor.py` → `data/p4-adaptor.json`)
- Give every point to its nearest envelope centre: the fcc Voronoi cell, the **rhombic dodecahedron** |x|+|y|, |y|+|z|, |z|+|x| ≤ R (R = 2φ/3), volume = the cell (32 + 16√5)/27.
- **The golden envelope lies inside its rhombic dodecahedron (exact) and touches each of its 12 faces at one corner** — the 12 golden-section corners on the octahedron edges ((2/3, (√5 − 1)/3, 0) and its turns).
- **Adaptor = rhombic dodecahedron − envelope: 352/27 − 16√5/3 = 1.111341** (44.27% of space).
## Step 2 — the adaptor as a piece (`scripts/p4_mesh.py` on dicto-node → `data/p4-mesh.json`)
- One solid, centrosymmetric (no left/right), but a **closed shell (cavity)**: the envelope is sealed inside. To assemble, it **opens in two identical halves along z = 0** (each 0.555671, one solid, sphericity 0.37; the half-turn about the x axis maps one onto the other). (Each half has the same volume as a grown core piece of set 3.)
- Sets: **one-piece golden octet** = rhombic dodecahedron with the envelope fused: one shape, fills space alone (fcc). **Two-shape golden octet** = solid envelope + adaptor half (×2): 2 shapes, no mirror images. **Adaptor for any golden-envelope solid**: the cavity takes any solid whose golden envelope it is (the OCD, the envelope itself, …).
## Step 3 — 3D page (`scripts/p4_page.py` → `renders/p4-golden-octet-adaptor.html`, claude.ai/artifact/3Qw1XztMnTGiUuN1ntq1L9)
- Views: two shapes (envelope + two halves), adaptor round any golden-envelope solid (OCD shown), one piece network, see-through network, and set 3's two-shape set with a solid envelope (DICTO: "two shape set as solid too").
## Notes
- The rhombic dodecahedron is the classical fcc space-filler; the new content is the exact golden envelope inside it touching all 12 faces at golden-section points, and the adaptor shell. Prior-art check: as in the envelope-network note.
- Next: Fable check; STL (halves at 60 mm octahedron edge); names.

## Step 4 — hollow spherical chamber (outside the plan; DICTO 10-18: "1, hollow chamber also half RD networks open with golden envelope exposed on outside") (`scripts/p4_chamber.py` → `data/p4-chamber.json`)
- Cells of the golden octet with centres between radius 2.4 and 5.4 (octahedron "radius" R = 2φ/3 = 1.0787 as unit frame): 230 cells.
- Inside the wall: 68 full rhombic dodecahedra (envelope fused). **Outermost layer (162 cells with a neighbour beyond the outer radius): golden envelope + only the inward adaptor half**, so the envelopes are exposed on the outside. The adaptor halves split on a mirror plane (x = 0, y = 0 or z = 0); each outer cell uses the plane facing most outward (the three are turns of one another under the envelope frame's symmetry, so it is still one half-shape).
- 3D page (same link): "Chamber" and "Chamber, cut open". Geometry only — nothing structural is claimed.
- DICTO 10-18: "make the inner surface half-open too". Inner-surface cells (a neighbour inside the inner radius) now carry the envelope + only the OUTWARD adaptor half, so envelopes line the hollow centre too. Same chamber (radii 2.4–5.4): 162 outer cells, 60 inner-surface cells, 8 full rhombic dodecahedra between, 0 cells that are both (if a wall were one cell thick, those cells would be bare envelopes).

## The general idea (DICTO 10-18): a "half-RD network" of any golden-adaptable solid
- DICTO: "this could be a half RD pyrochlore network of any golden adaptable solid … I meant figuratively, with RD equivalent". Recorded as the general system: **RD-equivalent cells (golden envelope + adaptor), each cell full or half-open (adaptor half kept on one side), arranged in any network on the fcc lattice; any solid whose golden envelope this is can sit in each socket.** The chamber (step 4) is one instance.
- Two RD-equivalents are now known: the **envelope-centred** rhombic dodecahedron (adaptor shell round one envelope, opens in two halves; this project) and Fable's **vertex-centred** rhombic dodecahedron minus its 6 envelope bites (W, one solid glue piece, achiral; octet fable-review-2).
