# Knitted HexOct — construction specification (2 November 2026)

DICTO proposed (agreed 2026-11-02): one continuous multi-layer knitted fabric like a spacer fabric; each sheet = one close-packed
layer (triangular lattice of nodes); links between neighbouring sheets = each ball's 3 bonds to the next layer; c/h carried by the
linking (c: links go on in the same sense, A→B→C; h: turn back, A→B→A); cells closed by sheets and links = HexOct tile pieces (#75).

**Conclusion:** links all of length a at 54.7356°, sheet spacing √(2/3) a; at a c sheet each link up is collinear with a link down,
at an h sheet it is the mirror image of one in the sheet; taut links centre each sheet exactly (greatest spacing only at the right
place); at λ = −1/8 the #75 tile pieces are exactly the fabric's cells (tetrahedra with 4 nodes, octahedral halves with 3 nodes +
6 link midpoints). Test pieces T-c (A-B-C) and T-h (A-B-A): 27 nodes, 42 links each.
**Status:** spec typeset `knitted-hexoct-spec.pdf` (also ~/Documents/papers-to-read), awaiting DICTO's read; nothing knitted yet.

## Files
- `scripts/check.py` → `data/check.out` (compute-host, python3, in a folder with the #75 scripts of
  studies/2026-10-29-endless-stack-cell): link offsets/lengths/tilts (exact), c collinear / h mirror, self-centring (random shifts),
  test-piece node and link counts, λ = −1/8 tile pieces vs fabric cells (5 layers: ABC, AB, ABCB ×2, ABCACB).
- `scripts/fig.py` → `figs/section.svg`, `figs/plan.svg` (construction schematics, line drawings only).
- `paper.html` → `knitted-hexoct-spec.pdf`, printed on compute-host with papers/print.mjs (footer text changed to
  "specification, not published" in the copy used; no DOI).
Background: studies/2026-11-02-knitted-octet (research note). No new source search for this spec.
