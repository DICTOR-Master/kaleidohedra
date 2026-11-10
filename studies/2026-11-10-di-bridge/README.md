# D–I bridge B: the flat Chain of Karma layer (DICTO 22 Oct idea; "both, A first" → "start B now" / "go on with B", 10 Nov)
Setting: world 1 (cubic grid φ; dodecahedra of edge 1 on alternating cubes, Dogstars between) fills space, so a flat (111) plane through
it cuts each crossed cell in two; the bridge layer is made of those cut parts. Above the plane: the octet, icosahedron faces in the plane.
- gap.py: under the corner-touching plane the leftover gap is ONE connected region (2.52 per period, 1.86 deep): it must be cut.
- cuts.py: the six natural plane levels in one period, with the cut parts of every crossed cell.
- **Level 0.467086 (relative to a dodecahedron-layer centre): every crossed Dogstar leaves exactly one CLEO below the plane** —
  volume 0.051503 exact, height 0.9342 exact, apex on a 3-fold axis at a cube corner (a dodecahedron corner), plane square to the axis:
  so base equilateral of edge 1/φ and side edges 1 (cleo_tip.py; the sampled hull only undershoots). This is Karma's CLEO arrangement
  (base on an icosahedron face, apex at a dodecahedron corner), flattened. Its base = the face of the Karma icosahedron (edge 1/φ).
- Same level: the crossed dodecahedral cells' parts above the plane have volume 1.765028 = 3 roofs + 1 CLEO exactly (numerically).
Next: (1) the dodecahedron cap = 3 roofs + CLEO as shapes; (2) the octet above with Pacioli icosahedra of edge 1/φ (octet edge φ/√2),
period and offset so that icosahedron faces land on the CLEO bases; (3) the full layer check.
- **Step 3 (octet_on_cleo.py, data-octet-on-cleo.log, FINAL ok): EXACT face-to-face meeting.** The CLEO base = the three dodecahedron
  corners one edge from the apex A (edges 1/φ, level exactly φ/(2√3), apex height 0.934172). The octet of edge φ/√2 with an octahedron
  face centred on the CLEO base (octahedron centre B + (φ/6)(1,1,1), axis-parallel): Pacioli's icosahedron in it (edge 1/φ), mirror form
  cyclic(0, ±φ, ±1)/(2φ), has its face in the plane EXACTLY on the CLEO base (max corner distance 0); the other chirality misses (0.27).
  So the flat layer carries Karma's chain icosahedron face → CLEO → dodecahedron corner across a plane. Also: the plane level φ/(2√3)
  = the inradius of the Karma icosahedron (edge 1/φ), so the Karma cells' icosahedra just below touch the plane with a face.
Next: (4) which skin pieces of the crossed Karma cells the plane cuts (kit consequences); density: one CLEO per φ√2-period cell, one
octet octahedron face in four sits on a CLEO; (5) the full two-sided layer check by points.
