# OCD in its octahedron: an Admiral Cap analog — DICTO 2026-10-17/18

DICTO · dictospheres.com

**Questions (DICTO, 10-17 night):** are the 72 gap pieces reciprocal to the structures? Is there an Admiral Cap analog? Can interlocking tetrahedra and octahedra be formed? "yes sketch it"; "is there an octet truss set that can be built from these pieces". (Started in the session lost at 04:24 JST 10-18; recovered and finished here.)

## Found (float, sampled volumes — not exact yet)
- The 8 joint hexagons lie on the faces of a regular octahedron, edge 1.5255. OCD fills 68.8% of it.
- The 12 five-fold corners stop at 0.887 of the way to the octahedron edges → the 31.1% shell is ONE connected piece (icosahedron case: 6 separate Admiral Caps).
- Cut by corner regions (z ≥ |x|,|y| and turns): 6 congruent caps, each one piece, vol 0.0865 (5.17%); each covers 10 kites + 6 hexagons.
- Golden key on each joint hexagon (edge 0.2379): 3 ridges to alternate corners, faces at 20.905° down to the 3 two-fold corners, height 0.0454 (0.191 × edge).

## Octet truss set (reasoning, not computed)
- OCD + 6 caps = octahedron; with regular tetrahedra of the same edge → octet truss (as #21). Each joint hexagon then faces a tetrahedron.
- The two tetrahedron orientations each meet one tetrahedral set of 4 octahedron faces = the bump/dent layout. Set: 1 OCD + 6 caps + T(4 dents) + T(4 bumps). Key height 0.0454 ≪ tetrahedron inradius 0.3114.
- Open: exact values; can caps and tetrahedra merge into fewer pieces?

## Files
- `scripts/ocd_octa.py` → `data/ocd-octa-check.txt`; `scripts/ocd_sketch.py` → `data/ocd-octa-sketch.json` (both read the OCD from 2026-10-16-polar-dharma); `scripts/draw_sketch.py` + `template.html` → `renders/ocd-octahedron-caps.html`
- Page: claude.ai/artifact/W3pfa4bBwQhnedhgafwtbU
