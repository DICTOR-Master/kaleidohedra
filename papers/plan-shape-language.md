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

- **Pragmatism first** (DICTO: "pragmatism is the key to the language, not originality"). Choose the standard, simplest,
  most reusable rule for each word and step; known methods are preferred and credited.
  "No reinventing of the wheel" (DICTO): use established methods and libraries wherever they exist (exact algebraic
  numbers: FLINT/Calcium, SymPy; polytopes: polymake, CGAL; proofs: Lean/Mathlib); our own code is the thin layer of
  shapes, words and certificates on top.
- **Words.** The base words are tiles that fill space. The five base words are Fedorov's five parallelohedra (E. S. Fedorov,
  1885): cube, hexagonal prism, rhombic dodecahedron, elongated dodecahedron, truncated octahedron. Smaller words cut them:
  the cube's centre pyramid (square base a, height a/2) builds both the cube (6) and the rhombic dodecahedron (12).
  The truncated octahedron is 8 identical octant pieces (cut by its three mirror planes through the centre; with corners
  at the permutations of (0, ±1, ±2), volume 32, each piece 4: one whole hexagon and three quarter-squares); the 8
  hexagons face the 8 nearest neighbours of the bcc lattice. It is also degree 1 from the octahedron (truncation), so it
  joins the words and the steps.
  The hexagonal prism is 3 identical rhombic prisms (the hexagon as 3 rhombi of 60°, the cube seen along its diagonal);
  the rhombic prism is the unit cell of the hexagonal lattice, so this word is the lattice's own.
  **One rule for all five (DICTO 18 Nov, pragmatism, no reinventing):** every Fedorov word is a zonohedron, so each is
  split by the standard zonotopal tiling into one parallelepiped per independent triple of its edge directions (volume
  formula of Shephard 1974 and McMullen): cube 1, hexagonal prism 3 (the rhombic prisms), rhombic dodecahedron 4
  rhombohedra, elongated dodecahedron 8 (the 4 rhombohedra + 4 slanted prisms), truncated octahedron 16. This replaces
  the centre pyramids and octants as the standard split; those stay as named alternative splits.
- **Grammar.** The lattice says where words go and how they join. Each base word is the Voronoi cell of its lattice: cube,
  simple cubic; rhombic dodecahedron, face-centred cubic; truncated octahedron, body-centred cubic; hexagonal prism,
  hexagonal; elongated dodecahedron, a stretched lattice. Example: in a checkerboard of cubes, each cube of one colour
  takes the centre pyramids of its 6 neighbours and becomes a rhombic dodecahedron on the fcc lattice.
- **Scores (two, DICTO 18 Nov).** *Filling score*: the fewest space-filling words (parallelepipeds of the zonotopal
  split) that build a shape. *Pyramid score*: the centre pyramids, one per face, so the number of faces; it applies to
  every convex solid and its pieces are the Vacuus's pyramids: tetrahedron 4, cube 6, octahedron 8, dodecahedron 12,
  icosahedron 20. The dodecahedron and icosahedron have no filling score from the five words: their Dehn invariants
  are nonzero, every space-filling tile has Dehn invariant zero (Debrunner 1980), and Dehn invariants add over pieces;
  for the same reason their centre pyramids do not fill space alone.
- **Degrees.** Steps from a word or built shape (Conway's polyhedron operators for the steps). The Platonic solids are
  built shapes; the Archimedean solids are degree 1 from them.
- **Scales** (DICTO: "all the measurement scales of golden etc should be in the language"). Every word comes in every
  scale, and scores and degrees are counted within a scale. Scales and their number fields: golden φ (Q(√5)); silver
  1 + √2 (Q(√2)); bronze (3 + √13)/2 (Q(√13)); the heptagon's ρ = 2cos(π/7) and σ = ρ² − 1 (the cubic field
  Q(cos 2π/7); Steinbach 1997, to be checked). Stage 1's kernel carries each of these fields exactly.
- **Plate score (2D, DICTO 18 Nov).** The number of central planes that carry the Vacuus's fins (one fin O–A–B per edge),
  with each plate's form recorded: a whole central disc (the fins fill a polygon round O) or separate fins (e.g. the
  cube's bow-ties: two fins of opposite edges meeting only at O). Read from the Vacuus census (studies/2026-11-02-dicto-vacuus,
  data/vacuus-census.json, field fin_planes): tetrahedron 6 (single fins), cube 6 (bow-ties), octahedron 3 (square discs),
  dodecahedron 15, icosahedron 15, cuboctahedron 4 (hexagon discs), icosidodecahedron 6 (decagon discs), truncated
  octahedron 15. The fin, strut and pyramid counts are the face counts E, V, F (the face fan), so they are not separate
  scores; the plate score is new information and ties the language to the walls (#110).
- **Golden side.** AXE and CLEO (Mosseri–Sadoc tiles t6 and t4, scaled by 1/φ; Koca et al. 2020) as words of the
  icosahedral tilings, entering at golden enlargement steps.
- **Credits.** Plato (*Timaeus*: solids from two right triangles); Aristotle (*De Caelo* III.8: regular tetrahedra
  fill space, refuted; history in Lagarias and Zong 2012); Archimedes (the thirteen solids, via Pappus); the *Nine
  Chapters* and Liu Hui (pyramid dissections of the cube); Dehn 1901 (a cube is not cut into regular tetrahedra);
  Fedorov 1885; Conway.
- **Golden-side filling scores** (read 18 Nov from N. Ozdes Koca, R. Koc, M. Koca and A. Al-Siyabi, "Dodecahedral
  structures with Mosseri–Sadoc tiles", 2020, in the library). The six Mosseri–Sadoc tiles t1–t6 (AXE = t6/φ, CLEO =
  t4/φ) fill space together, not one alone. Icosahedron of edge 1: i(1) = 7t1 + 6t2 + 2t5 + t6 = **16 tiles** (their
  eq. 7). Dodecahedron of edge 1: d(1) = 3T1 + 4T2 + 4T4 (eq. 15) with T1 = t1 + 2t4 + 2t3 + t6, T2 = t2 + t4,
  T4 = t5 + t6 + t3, so 3t1 + 4t2 + 10t3 + 10t4 + 4t5 + 7t6 = **38 tiles** (our count from their definitions; volumes
  sum exactly to the solids' volumes 5φ²/6 and (15 + 7√5)/4 = (4 + 7φ)/2 from their Table 1). These are counts of their constructions, not proved
  minima. The icosahedron cannot be inflated past edge φ with these tiles (their text after eq. 11); the dodecahedron can.
- **Sphere as the perfect value (DICTO 18 Nov; confirmed: "then all previous work ties in perfectly").** DICTO: "with the computation if it's of a
  sphere as perfect value … not tetrahedra or cube". Reading: every score is read against the sphere (perfect = 1), not
  built up from the tetrahedron or cube. Standard measures that do this: isoperimetric quotient 36πV²/S³ (Pólya), in/out
  radius ratio r/R, and landing isotropy Q_l (Steinhardt–Nelson–Ronchetti 1983; sphere 0). Next: re-read the existing scores (IQ, r/R, Q_l already in the studies) on this one scale.
- **Open.** Whether 16 and 38 are the fewest; the tile counts at the AXE/CLEO scale (one golden step down).