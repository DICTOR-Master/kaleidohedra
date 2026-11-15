# Filigree: the Platonic connectors as gold round stones (15 Nov 2026) - DICTO · dictospheres.com

**Verdict (15 Nov 2026): every jewellery figure of the Platonic book's Chapter 10 (Filigree) is drawn from exact coordinates, and its exact checks pass (render_jewels.py, FINAL ok; job filigree-render2 on the compute host).**

DICTO, 15 Nov 2026: "yes write it in the Platonic book" (plan: studies/2026-11-14-chat-handoff, 03-session-addendum.md, section C);
additions of the same day: pierced bands and closed loops (at least one whole stone in every design), satellite stones on every kind of
piece, chains of solids linked by connector pieces; filigree designs stay the core, the others are variations.

## Checks (exact; X lines of data/render.log)
| check | result |
|---|---|
| octet ring: the layer cells sharing an edge with one octahedron are 6 T + 6 O, one face-sharing cycle of 12, alternating, all in the layer; the missing octahedron has a face on each plane (tunnel) | PASS (integer coordinates) |
| octet band satellites: one tetrahedron on the top face of each ring octahedron, apex on the next plane, all distinct | PASS |
| satellite tetrahedron on an octahedron face of edge phi^2/sqrt2: all edges exact | PASS (Q(sqrt5)) |
| pendant: octahedron + 4 tetrahedra on alternate faces = tetrahedron of edge 2 phi^2/sqrt2 (apex distances and volumes exact) | PASS |
| claw (octahedron with Pacioli's icosahedron): 12 rotations; none carries face +++ to -++, so the satellite earring is chiral (left/right pair) | PASS |
| piece counts of every figure (COUNT lines) equal the captions | PASS |

Golden pieces (cells, Admiral Caps, caps, Dogstars, R, Z) come from the checked builders of studies/2026-11-14-platonic-hybrid
(golden.py, hybrid.py); the gold shares of Table 10.2 are #106 Table 1 volumes divided by the cell (15 + 7 sqrt5)/4, rationalised by
hand and checked against floats; Table 10.3 is read from data/hybrid-full.log (K lines) of the hybrid study and data-free.log of
studies/2026-11-10-free-scale-mixes.

## Files
- scripts/jewels_lib.py: renderer (depth buffer, crisp edges, 3x supersampling, two materials, DICTO mark); scripts/render_jewels.py: checks + 7 figures.
- data/ring.png, bracelet.png, brooch.png, band-loop.png, earrings.png, variations.png, satellites.png; data/render.log.

## Open (book §10.9)
Smallest kit / least metal; one edging piece for R and Z; edge-1 settings for C, T, O; face to face; 3-periodicity; interlocking
pierced links (clearance unchecked); necklace of the golden cycle; nest pendant drawn with its gold.
