# Plan: an exact language of shapes (working name; the name is DICTO's)

DICTO, 18 Nov 2026: "math and geometry need a computer language of geometric shapes themselves that only calculates
perfectly and is therefore always checkable … whether it is ultimately achievable or not it is a worthy aim."

Aim served: **laws** (geometry gives laws), and the base under all three aims: every study of the bridge, the laws and
the one piece would run on one exact, checked core instead of code copied from study to study.

## What it is

A small language whose words are shapes and the moves on them (cell, rhombohedron, zonotope, cut, union, remove a
corner, polar, section, projection, Vacuus plates), computed only in exact numbers, where every result carries its own
certificate: the list of checks that prove it, which anyone can re-run without trusting the program.

## Built on (credited, not reinvented)

- Exact geometric computation: C. Yap (1990s); the exact kernels of CGAL.
- Proof assistants: Lean 4 with Mathlib (used for the Yantra and GET entries); GeoCoq (Euclid's and Tarski's axioms).
- Algebraic provers: Wu's method (1978); GeoGebra's automated prover.
- SAT certificates: DRAT proofs checked by drat-trim (#110).
- Our own pieces: exact Z[phi] arithmetic and the Z^n face form (zsurf.py, GET studies), exactlib.py / atomlib.py
  (DICTO Solids model files), mixlib.py (exact overlaps in Q(phi)), the "FINAL ok" control discipline, and the code map of
  the Concordance (340 functions copied in 3 or more studies).

## Stages (each ends in an outcome; pilot first)

1. **Kernel of exact numbers.** One library for Q, Q(sqrt5), Q(sqrt2), Q(sqrt3), Q(sqrt6) and the cubic fields our
   shapes need, with exact signs and comparisons. Built from the existing copies; every copy's tests pass on it.
   Outcome: one module replaces the copies.
2. **Shapes as exact objects.** Polytopes held both by corners and by face planes, checked to agree; zonotopes and their
   cells in the Z^n face form; the moves (cut, union, minus, Minkowski sum, polar, truncation, section, projection from
   4D). Every move returns the shape and its certificate. Outcome: the DICTO Solids model checks rebuilt on it.
3. **Certificates that stand alone.** A certificate format: exact identities, overlap and volume checks, SAT/DRAT
   proofs; a separate small checker that reads only the certificate. Outcome: GET's tiling and Valley Charge's counts
   re-checked by the checker alone.
4. **Three flagship studies moved over.** GET (k = 10 tilings, mixing), Valley Charge, the DICTOnary atoms; outputs
   compared with the originals line by line. Outcome: same results, one code base.
5. **Bridge to Lean.** Certificates of the simple kinds (finite exact checks) turned automatically into Lean statements
   with kernel-checked proofs, as was done by hand for GET. Outcome: one result goes from the language to a Lean proof
   with no hand-written step.
6. **The language itself.** A short written form in DICTO's words, e.g. "the triacontahedron minus four oblate corners,
   tetrahedral" → the shape, its tiling check and its certificate. Outcome: a page of DICTO's shapes written in it.

## What is achievable, and what is not

- **Achievable:** everything polyhedral with corners in algebraic number fields, which is nearly all of the work:
  exact construction, exact decisions, a certificate for each answer.
- **Harder:** curved shapes (Reuleaux bodies, spheres of #45 and the CLEO sphere) need exact algebraic surfaces or
  certified intervals instead of exact numbers (as the Yantra's 2^-21 interval in Lean).
- **Not possible in general:** a language that decides every question. Whether a set of tiles tiles space is
  undecidable in general (Berger, 1966), and no consistent system proves all true statements about numbers (Gödel,
  1931). So the language promises that whatever it states is checkable, not that it can answer everything; open
  questions stay open, stated exactly.

## First step

Stage 1: list every exact-number module in the studies (the code map), merge them into one kernel with all their tests,
and run every test. A pilot on the three most-copied modules first.

## Words, grammar and scores (DICTO, 18 Nov 2026)

DICTO: "minimal amount of pieces value … derivative forms are degrees"; "pieces are words, degrees are steps"; "tiles that
fill space"; "the lattice is the grammar".

- **Words.** The base words are tiles that fill space. The five base words are Fedorov's five parallelohedra (E. S. Fedorov,
  1885): cube, hexagonal prism, rhombic dodecahedron, elongated dodecahedron, truncated octahedron. Smaller words cut them:
  the cube's centre pyramid (square base a, height a/2) builds both the cube (6) and the rhombic dodecahedron (12).
  The truncated octahedron is 8 identical octant pieces (cut by its three mirror planes through the centre; with corners
  at the permutations of (0, ±1, ±2), volume 32, each piece 4: one whole hexagon and three quarter-squares); the 8
  hexagons face the 8 nearest neighbours of the bcc lattice. It is also degree 1 from the octahedron (truncation), so it
  joins the words and the steps.
- **Grammar.** The lattice says where words go and how they join. Each base word is the Voronoi cell of its lattice: cube,
  simple cubic; rhombic dodecahedron, face-centred cubic; truncated octahedron, body-centred cubic; hexagonal prism,
  hexagonal; elongated dodecahedron, a stretched lattice. Example: in a checkerboard of cubes, each cube of one colour
  takes the centre pyramids of its 6 neighbours and becomes a rhombic dodecahedron on the fcc lattice.
- **Score.** The fewest space-filling words that build a shape.
- **Degrees.** Steps from a word or built shape (Conway's polyhedron operators for the steps). The Platonic solids are
  built shapes; the Archimedean solids are degree 1 from them.
- **Golden side.** AXE and CLEO (Mosseri–Sadoc tiles t6 and t4, scaled by 1/φ; Koca et al. 2020) as words of the
  icosahedral tilings, entering at golden enlargement steps.
- **Credits.** Plato (*Timaeus*: solids from two right triangles); Aristotle (*De Caelo* III.8: regular tetrahedra
  fill space, refuted; history in Lagarias and Zong 2012); Archimedes (the thirteen solids, via Pappus); the *Nine
  Chapters* and Liu Hui (pyramid dissections of the cube); Dehn 1901 (a cube is not cut into regular tetrahedra);
  Fedorov 1885; Conway.
- **Open.** Smaller words for the hexagonal prism and elongated dodecahedron; scores of the
  dodecahedron and icosahedron, which do not fill space.
