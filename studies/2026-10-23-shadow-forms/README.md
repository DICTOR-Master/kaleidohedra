# Shadow forms of the simple cubic icosahedron networks (2026-10-23)

DICTO's idea (2026-10-23): complementary ("shadow") ways of breaking up the AXE networks' space, to find new pieces; aim (DICTO): unit pieces without odd protrusions, and flat top/bottom fills. Float computations unless marked; exact check of the golden split still to do.

Scripts run from this folder's `scripts/` with ~/k-mix study data (sc-star-H-unit.json) and ~/axe-gap geometry.

1. **Fusions** (fuse1–5): face-sharing pairs convex only Tricap+Unborn and Unborn + k Tricaps; 16 chunky 2–3-piece fusions (fill ≥ 85%, elongation ≤ 1.8), best AXE+icosahedron 95.7%.
2. **Two-piece AXE assignment** (fuse6): each AXE to its lower icosahedron (or Unborn) gives icosahedron+6 AXE / Unborn (and twin); fills (point test 0/0) but spiky: 68% / 49% of hull.
3. **Flat layers** (flat1–5): no lattice plane misses every piece; the icosahedron-equator plane cuts only icosahedra + AXE. Best single layer unit 84.0% of hull (sliding copies), turned twins no better (84.0%; C 78.5%). Note: layer A turned-twin groups mostly skipped by an orbit-count check (possible bug).
4. **Golden split of the AXE** (axesplit1–4): cone each AXE from a point p on its axis (t = 0 long-edge midpoint … 1 short-edge midpoint) into 4 pyramids, each joining the piece across that face. Icosahedron + 12 pyramids is convex for t ≤ 1/φ, Unborn + 12 pyramids for t ≥ 1/φ: **at t = 1/φ both are convex** (float: fill − 1 ≈ 4e-16 and −1.6e-10). Both are **truncated octahedra** (24 corners, 8 hexagons, 6 squares): the same hexagon (sides alternating 1/√2 and 1/(φ√2)), big squares 1/√2 on the padded icosahedron, small squares 1/(φ√2) on the padded Unborn; volumes 2.490712 + 1.745356 = φ³. Body-centred two-piece fill, point test 500,000 points: 0 uncovered, 0 doubled. Pictures: ~/Documents/papers-to-read/golden-split/.

Open: exact ℚ(√5) proof of the golden split; prior art (two unequal truncated octahedra on bcc are a known Laguerre/power-diagram family — the golden member with the icosahedron and the Unborn inside is not yet checked: library + web before any claim).
