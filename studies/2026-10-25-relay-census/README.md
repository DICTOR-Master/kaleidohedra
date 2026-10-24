# Relay census (2026-10-25)

"Relay census", "soft relay", "hard relay" and "hinge" are working names from the Bond Relay study (`../2026-10-25-web-of-bonds/`). DICTO decides the names. The structures, cells and tilings below carry their names from the literature. DICTO's names are used only for DICTO's own things (the golden and Delian DICTONIC loops).

## Question

The Bond Relay study proved two things about DICTO's DICTONIC loops. Each loop is a power diagram of fixed sites, with one weight slid between the two kinds. Its web (one bond per shared face) is the 1-skeleton of the dual weighted-Delaunay subdivision. In the golden loop the two like bonds hand over softly, with no flip. In the Delian loop they hand over hard: there is one flip, at the octet, where only unlike bonds exist (the "hinge").

**This study asks whether other two-kind crystal networks, and one three-kind network, show the same kind of relay.** For each network it records:
- the weight range where both kinds have cells;
- the bond types present on each interval of that range;
- the flips, at exact parameter values;
- the coordination number of every piece;
- any parameter where only unlike bonds exist;
- named tilings at special weights.

## Method (exact)

**Set-up (`scripts/networks.py`).**
- Each network is a periodic set of sites in rational coordinates with a rational metric G. Hexagonal lattices use a 60° basis: G = [[1, ½], [½, 1]] in 2D, and G = [[1, ½, 0], [½, 1, 0], [0, 0, 8/3]] for ideal hcp. All bisectors are then rational. A power diagram in the metric G is an affine image of the Euclidean one, with the same combinatorics and the same weights.
- The weights are w_A = λ and w_B = 0, so **λ = w_A − w_B**.

**The engine (`scripts/engine.py`).** It generalises the Bond Relay study's `power_cell` to dimension 2 and 3, to any metric, and to weights affine in a parameter.
- Every corner is p(λ) = A⁻¹b(λ), which is affine in λ with rational coefficients. Every slack is therefore affine in λ.
- At a rational sample λ₀, the face lattice is constant on the open interval where no slack that is positive at λ₀ reaches 0. The interval's end points are rational.
- Floats (scipy `HalfspaceIntersection`, `linprog`) only pick the candidate corners. Each corner is then solved and tested exactly in Fractions.

**The walk (`scripts/census.py`).** It starts at λ = 0, finds the interval, and analyses the end point (the "stop"). It then steps just past the stop and repeats, until one kind's cell has volume 0. Each step is checked: the new interval must begin exactly at the stop.

**Checks on every interval:**
- the cell volumes, as polynomials in λ, add up to the lattice cell identically;
- every face appears in both of its cells with the same measure;
- Euler's formula holds for every 3D cell;
- a distance bound shows that the finite site list is enough over the whole closed interval.

**Checks at every stop:**
- the limit of the interval's corners equals the power cell computed from scratch at that exact λ;
- at an end stop, planes through a cell that has shrunk to a point are not counted as bonds.

**Other scripts:**
- `scripts/relay.py` computes the life of every bond type and every bond orbit (type @ squared site distance), the flips, the hinges and the relay class. It also solves the named stops exactly with sympy (all edges equal) and runs regressions against the Bond Relay study.
- `scripts/perovskite.py` handles the three-kind case (two weights). It finds exact chambers in the (λ, μ) plane, walks across every wall, and checks completeness: every interior wall segment must be covered by chambers on its other side.
- `scripts/crosscheck.py` gives a float cross-check. Independent numpy/scipy cells at three random λ per interval are compared with the exact bond counts. It also computes the exact hulls of the dual cells at the two octet-type stops.
- `scripts/tables.py` writes `data/raw/tables.md`: every interval and stop of every network, with the cell face vectors and bonds per piece.

**Sanity checks, all PASS.** The equal-weight cells and the end cells reproduce the classical Voronoi cells:
- square: squares;
- triangular lattice: regular hexagons;
- honeycomb points: triangles;
- kagome points: rhombi (rhombille tiling);
- simple cubic lattice: cubes;
- fcc: rhombic dodecahedron (RD);
- bcc: truncated octahedron;
- diamond: triakis truncated tetrahedron (16 faces: 4 hexagons and 12 triangles);
- hcp octahedral holes, which form a simple hexagonal lattice: hexagonal prism;
- A15: the Weaire–Phelan cells (pentagonal dodecahedron, and the 14-face cell with 12 pentagons and 2 hexagons);
- C15: the 12-face cell (12 pentagons) and the 16-face cell (12 pentagons and 4 hexagons).

Both DICTONIC loops are reproduced exactly as regressions. The golden areas match, and so do the Delian areas, the flip at t = 1/3, and the equilateral-RD and equilateral-cube stops (t = (2√6 − 3)/15 and t = 5/3 − (2/3)√2).

## Results

### Summary table

- "Overlap" = both like bonds are alive on a common open interval, bounded by two flips (soft relay).
- "Touch" = one like bond dies exactly where the other is born, at a hinge where only unlike bonds exist (hard relay).
- Flips are the interior stops where the face lattice changes, all exact.
- λ is in the units stated under "Units" below.

| network (kinds A, B; λ = w_A − w_B) | coexistence range | relay type | flips at | hinge (only unlike bonds)? | named tilings at stops / special λ |
|---|---|---|---|---|---|
| golden-loop sites = CsCl (bcc two-kind: big, small) [regression] | (−3, 3) | **overlap** on (−1, 1) | −1, 1 | none | 0: bitruncated cubic honeycomb (truncated octahedra; Voronoi of bcc). ±1: octahedra + cuboctahedra. (−3, −1) and (1, 3): truncated cubes + octahedra; all edges equal at λ = ±(2√2 − 1), the uniform truncated cubic honeycomb (faces regular by the cells' symmetry). ±3: cubes |
| Delian-loop sites = fluorite (fcc "oct" + all tetrahedral holes "tet") [regression] | (−3/8, 3/8) | **touch** at −1/8 | −1/8 | **yes, −1/8 (the octet)** | −1/8: octet (regular octahedra and tetrahedra; dual = RD). Ends: RD (fcc Voronoi), cubes |
| 1. square lattice + centres (2D CsCl analogue; corner, centre) | (−2, 2) | **touch** at 0 | 0 | **yes, 0 = equal weights** (square tiling, rotated 45°) | (−2, 0) and (0, 2): 4.8.8 (truncated square tiling) combinatorially; uniform 4.8.8 at λ = ±(2√2 − 2). Ends: square tiling |
| 2a. honeycomb + hexagon centres (triangular lattice 2:1; honeycomb, centre) | (−1, 1) | **touch** at −1/2 | −1/2 | **yes, −1/2**: the trihexagonal (kagome) tiling 3.6.3.6, exactly uniform (one edge length, √3/2) | (−1, −1/2): 3.12.12 combinatorially; uniform truncated hexagonal tiling at λ = 1 − √3. (−1/2, 1): hexagonal tiling, regular at 0. Ends: hexagons; triangles |
| 2b. kagome + hexagon centres (triangular lattice 3:1; kagome, centre) | (−1, 1) | **no relay**: one chamber, no flip | none | none | hexagonal tiling throughout; regular at 0. Ends: rhombille (kagome Voronoi); hexagons. Centre–centre bonds exist only at the end λ = −1, where the kagome cells are points |
| 3. rock salt NaCl (fcc + fcc; Na, Cl) | (−1, 1) | **touch** at 0 | 0 | **yes, 0 = equal weights** (cubic honeycomb; dual cells: cubes of 4 Na + 4 Cl) | (0, 1): Na = 6 squares + 12 hexagons (the face vector of the chamfered cube) + Cl cubes; all edges equal at λ = 4 − 2√3. Mirror image for λ < 0. Ends: RD (fcc Voronoi) |
| 4. zinc blende ZnS / diamond (fcc + one set of tetrahedral holes; Zn, S) | (−3, 3) | **overlap** on (−1, 1) | −1, 1 | none | 0: diamond Voronoi (triakis truncated tetrahedra). ±1: 16-triangle cells + tetrahedra. ±3: RD |
| 5. hcp holes: octahedral + tetrahedral holes of ideal hcp (the cell centres of the gyrated tetrahedral–octahedral honeycomb; oct, tet) | (−11/24, 3/8) | **overlap** on (−11/24, 5/24) at type level. Contains the octet's own hard switch at orbit level | −1/8, 5/24 | **none** (the gyrated octet at −1/8 keeps oct–oct and tet–tet bonds across its layers) | −1/8: gyrated tetrahedral–octahedral honeycomb (regular octahedra and tetrahedra; the dual cell at an atom is the trapezo-rhombic dodecahedron). −11/24: hexagonal prisms (Voronoi of the simple hexagonal octahedral holes) |
| 6a. A15 Cr₃Si (Si, Cr) | (−5/4, 5/4) | **overlap** on (1/4, 3/4) | 1/4, 3/4 | none | 0: Weaire–Phelan cells. 3/4: Si = 20 triangles with 12 corners of degree 5 (combinatorially an icosahedron) + Cr tetrahedra (only unlike bonds on Cr). 5/4: truncated octahedra (bcc Voronoi of Si) |
| 6b. C15 Laves MgCu₂ (Mg, Cu) | (−11, 11) | **overlap** on (−5, 9) | −5, 7, 9 | none | 0: the C15 Voronoi cells (12- and 16-face). 11: triakis truncated tetrahedra (diamond Voronoi of Mg) |
| 6c. perovskite ABX₃ (three kinds; λ = w_A − w_X, μ = w_B − w_X) | rectangle −2 ≤ λ ≤ 2, −1 ≤ μ ≤ 1 (area 8) | **overlap** (A–A / X–X); no hinge anywhere | 3 straight walls: λ = 0 (A–A born), λ + 2μ = 0 (A–B born), λ + μ = 1 (X–X dies); 5 chambers | none (no chamber and no chamber corner with only unlike bonds) | (0, −1): A and X cells are RD (B a point). B–B bonds never exist while all three kinds have cells |

**PASS: 643 / 643 exact and float checks, 0 FAIL.** The split, from `data/checks/`:

| part | PASS |
|---|---|
| census walks | 543 |
| relay analysis, including the 9 regressions against the Bond Relay study | 41 |
| perovskite chambers | 47 |
| float cross-check and exact hinge dual cells | 12 |

Every claim in the table is exact, except the uses of the word "combinatorially", which rest on face vectors and corner degrees (both exact).

### Units

| network | units |
|---|---|
| CsCl | half cube edge L/2 = 1. The golden loop x ∈ [0, ∞] is λ = (x − 1)/(x + 1) ∈ [−1, 1] |
| fluorite (Delian) | octet edge 1, the app's units. λ = (3/8)(2t − 1) |
| square | square edge 2: corners 2Z², centres 2Z² + (1, 1) |
| triangular lattices | edge 1 |
| NaCl | Na–Cl distance 1 |
| zinc blende | cubic cell edge 4: Zn–S distance √3, Zn–Zn distance 2√2 |
| hcp holes | hcp edge 1, the same units as the Delian run |
| A15 | cubic cell edge 2 |
| C15 | cubic cell edge 8 |
| perovskite | cubic cell edge 2: A–X distance √2, B–X distance 1 |

### Lives of the bonds (exact; "@" = squared site distance in the network's units)

| network | unlike bond | A–A | B–B |
|---|---|---|---|
| CsCl | big–small (−3, 3) | big–big (−1, 3] | small–small [−3, 1) |
| fluorite (Delian) | oct–tet (−3/8, 3/8) | tet–tet@1/2 (−1/8, 3/8] | oct–oct@1 [−3/8, −1/8) |
| square | (−2, 2) | corner–corner (0, 2] | centre–centre [−2, 0) |
| honeycomb + centres | (−1, 1) | honeycomb–honeycomb@1 (−1/2, 1] | centre–centre@3 [−1, −1/2) |
| kagome + centres | (−1, 1) | kagome–kagome@1 (−1, 1] | centre–centre@4 only at λ = −1 (the kagome cells are points there) |
| NaCl | (−1, 1) | Na–Na (0, 1] | Cl–Cl [−1, 0) |
| zinc blende | (−3, 3) | Zn–Zn@8 (−1, 3] | S–S@8 [−3, 1) |
| hcp holes | oct–tet@3/8 (−11/24, 3/8) | tet–tet@1/2 and tet–tet@1 (−1/8, 3/8]; **tet–tet@1/6 (−11/24, 3/8]** | oct–oct@1 [−11/24, −1/8); **oct–oct@2/3 [−11/24, 5/24)** |
| A15 | Cr–Si (−5/4, 5/4) | Si–Si@3 (1/4, 5/4]; Si–Si@4 (3/4, 5/4] | Cr–Cr@1 and Cr–Cr@3/2 [−5/4, 3/4) |
| C15 | Mg–Cu (−11, 11) | Mg–Mg@12 (−5, 11]; Mg–Mg@32 (7, 11] | Cu–Cu@8 [−11, 9) |

In every two-kind network here, **the unlike bond lives on the whole open coexistence range**: it never breaks while both kinds have cells. This is the same as in both DICTONIC loops. It fails for the three-kind perovskite, where A–B lives only on λ + 2μ > 0.

Coordination numbers per piece, for every interval and stop, are in `data/raw/tables.md`.

### Notes per network

**1. Square + centres.** This is a hard relay, exactly like the Delian loop. The hinge is at equal weights:
- The tiling at λ = 0 is the square tiling (rotated 45°). Every bond is unlike (4 each).
- Its dual cells are squares with alternating corner and centre vertices. At λ = 0 each such square trades its corner–corner diagonal for its centre–centre one.
- On each side the tiling is combinatorially 4.8.8. It is uniform at λ = ±(2√2 − 2), which in square-edge-1 units is ±(√2 − 1)/2.
- Like-bond length: centre–centre = |λ|. Unlike-bond length: |λ − 2|/√2 for λ ≥ 0, and (λ + 2)/√2 for λ ≤ 0. Both are exact.

**2a. Honeycomb + centres.** This is a hard relay with the hinge at λ = −1/2, not at equal weights.
- The hinge tiling is the trihexagonal tiling 3.6.3.6, with a single edge length (edge² = 3/4) and regular faces by symmetry. Its dual cells are rhombi (2 centres + 2 honeycomb points).
- This is the 2D counterpart of the Delian octet/RD picture: at the hinge the dual rhombi trade one like diagonal for the other.
- Edge lengths: honeycomb–honeycomb (2λ + 1)/√3; centre–honeycomb (1 − λ)/√3 for λ > −1/2, and √3(λ + 1) for λ < −1/2; centre–centre −(2λ + 1).

**2b. Kagome + centres.** There is **no flip in the whole coexistence range.** The tiling stays combinatorially the hexagonal tiling.
- The centres never bond to each other while kagome cells exist, so there is no relay: only one like bond (kagome–kagome) ever lives.
- Formally the hand-over is a "touch" pushed onto the end point λ = −1, where the kagome cells vanish.

**3. NaCl.** This is a hard relay with the hinge at equal weights (λ = 0).
- At the hinge every cell is a cube with 6 unlike faces.
- At the hinge the dual cubes (4 Na + 4 Cl) trade the Cl–Cl face diagonals for the Na–Na face diagonals.
- Like-bond area (Na–Na): λ(2 − λ)/√2. Unlike-bond area (1 − |λ|)².
- Ends: RD (fcc Voronoi). The 6-square + 12-hexagon cell has all edges equal at λ = 4 − 2√3.

**4. Zinc blende / diamond.** This is a soft relay, overlapping on (−1, 1).
- Its closed forms have exactly the same λ-dependence as the CsCl two-kind network, up to constant factors:
  - like bonds: area (1 ± λ)²/(2√2) here, against (1 ± λ)²/2 in CsCl;
  - unlike bonds: √3(3 − λ²) here, against (√3/4)(3 − λ²);
  - volumes: −2(λ³ − 9λ − 12)/3 here, against −(λ³ − 9λ − 12)/3;
  - the same flips at ±1 and the same ends at ±3.
- In both, the second kind sits at the deep hole of the first kind's lattice, at squared distance 3. This coincidence is exact but **not explained** here.
- No hinge exists.

**5. hcp holes, the "gyrated octet" sites (DICTO's #37a: the gyrated tetrahedral–octahedral honeycomb).** The question was whether the switch moves or splits.
- **The octet's switch does not move.** The in-layer bonds hand over at exactly the octet's parameter, λ = −1/8: oct–oct@1 dies, and tet–tet@1/2 is born together with tet–tet@1.
- **But the hinge is lost.** The gyrated octet itself, at λ = −1/8, has oct–oct bonds (octahedron to octahedron across each layer, 2 per oct) and tet–tet bonds (tetrahedron to tetrahedron in each triangular bipyramid, 1 per tet).
- Of those two cross-layer like bonds:
  - tet–tet@1/6 lives over the whole range;
  - oct–oct@2/3 dies only at a **second flip, λ = 5/24**.
- So **the switch splits**: one hard flip at −1/8, as in the octet, plus a soft tail ending at 5/24.
- The lower end of the range also moves: from −3/8 (fluorite) to −11/24. In hcp the tets also have a tet neighbour, at squared distance 1/6; whether that explains the later vanishing is not examined here. This is the only two-kind network here whose range is not ± (unlike nearest distance)².
- The dual cell at an atom at λ = −1/8 is the trapezo-rhombic dodecahedron, the Voronoi cell of hcp (exact hull: 6 faces with two pairs of parallel sides, 6 faces with one). In fluorite at −1/8 it is the RD (12 parallelograms).

**6a. A15.** This is a soft relay, overlapping on (1/4, 3/4).
- At λ = 3/4 the Cr–Cr bonds (both orbits) die exactly where a second Si–Si orbit (@4) is born. This is a hard hand-over at orbit level, but the first Si–Si orbit has been alive since 1/4.
- At 3/4 the Cr cells are tetrahedra with only unlike bonds, and the Si cells are combinatorially icosahedra.
- Some Si–Si face area equals some Cr–Cr face area at two exact parameters, λ ≈ 0.4134 and λ ≈ 0.5318. Which orbit pairs these are is not resolved here; the closed forms are in `data/raw/relay-summary.json`.

**6b. C15.** This is a soft relay, overlapping on (−5, 9).
- There is a third flip at λ = 7, inside the overlap. No bond type changes there, but a second Mg–Mg orbit (@32) is born.

**6c. Perovskite (two-parameter family).**
- The coexistence region is the rectangle −2 ≤ λ ≤ 2, −1 ≤ μ ≤ 1. The A cells vanish at λ = −2, the X cells at λ = 2 and at μ = 1, and the B cells at μ = −1.
- It is cut by three straight walls into 5 chambers. **Each wall is the birth or death line of exactly one bond type:**
  - λ = 0 for A–A;
  - λ + 2μ = 0 for A–B;
  - λ + μ = 1 for X–X.
- B–B never appears.
- The like bonds A–A and X–X overlap on the chamber 0 < λ < 1 − μ. The two switch lines meet only at the corner (0, 1) of the region, where the X cells vanish. So the hand-over would become a "touch" only at the edge of the region.
- No chamber, wall corner or region corner has only unlike bonds.

### Anything surprising

1. **The golden loop is exactly the soft chamber of the CsCl family.** The full CsCl weight range is (−3, 3). The golden loop x ∈ [0, ∞] covers precisely the overlap interval [−1, 1], from one flip to the other. Its ends x = 0 and x = ∞ are those flips: the octahedron + cuboctahedron honeycombs. The Delian loop covers the whole fluorite range.
2. **The pattern.** Hard relays (a hinge) occur in square + centres, honeycomb + centres, NaCl and fluorite. In each, at the hinge, every like pair is a diagonal of the same dual quadrilateral, and the like bonds trade those diagonals in a single flip:
   - square + centres: dual squares;
   - honeycomb + centres: rhombille rhombi;
   - NaCl: cube faces;
   - fluorite: RD rhombi.

   Soft relays occur in CsCl, zinc blende, A15, C15 and hcp holes. There the two like bonds die at different flips. *This is an observation from the dual-cell compositions at the hinges (exact). It is not proved in general.*
3. Zinc blende and CsCl share identical λ-polynomials (unexplained).
4. In the hcp holes the octet's switch stays at −1/8, but it splits: a second flip appears at 5/24, and there is no hinge.

## Prior art

**DICTO's library** (`~/bin/ask-library`, 5 queries; `~/Documents/kaleidohedra-references/INDEX.html` searched for Laguerre, power diagram, Aurenhammer, weighted Voronoi, Frank–Kasper, Weaire, Laves, A15, zinc blende, trapezo, radical, chamfered, trihexagonal, truncated cubic honeycomb, Tilings and Patterns, Andreini).

**In the library** (added for paper #52, "The Web of Bonds", or earlier; link-only unless noted; not re-read here):
- Aurenhammer 1987 (power diagrams) and 1991 (survey); Imai, Iri & Murota 1985 (Laguerre Voronoi).
- Gelfand, Kapranov & Zelevinsky 1994 (regular subdivisions).
- Alexeev 2002 §5.12 (secondary polytopes for periodic decompositions); Erdahl & Rybnikov 2001 (L-types); Dutour Sikirić, Schürmann & Vallentin 2008; Schürmann 2010 (Delone subdivisions changing at walls).
- **E. Koch 1973**, Z. Kristallogr. 138, 196–215: Dirichlet-domain types of cubic lattice complexes changing at critical positional parameters. This is unweighted, and the closest crystallographic analogue of this census.
- Gellatly & Finney 1982; Richard et al. 1998; Wang et al. 2018 (a CsCl-type radical tessellation); Hopkins, Stillinger & Torquato 2012; Murray & Sanders 1980 (binary packings).
- Frank & Kasper 1958 (complex alloy structures as sphere packings).
- Conway, Burgiel & Goodman-Strauss 2008 (*The Symmetries of Things*: uniform tilings and honeycombs).
- Wikipedia 2026, Tetrahedral–octahedral honeycomb (including the gyrated form), as a PDF.

**Classical, cited from general knowledge (not in the library):**
- the Voronoi cells of the simple cubic, fcc, bcc, diamond and hcp lattices, and the simple hexagonal prism;
- the uniform tilings 4.8.8, 3.12.12, 3.6.3.6 and the rhombille tiling (Grünbaum & Shephard, *Tilings and Patterns*, 1987);
- the uniform truncated cubic and bitruncated cubic honeycombs (Andreini 1905);
- the Weaire–Phelan foam as the A15 Voronoi structure (Weaire & Phelan 1994);
- the C15 Laves Voronoi cells (Frank–Kasper);
- the fact that every Delaunay tessellation is the power diagram of its circumspheres.

**DICTO's own draft #52** (`papers/2026-10-25-web-of-bonds/`) already reads the golden loop as the CsCl structure and the Delian loop as the fluorite structure. This census uses those names and does not re-check the draft.

**Not found in DICTO's library** (no web search was made in this study):
- the weight walks of NaCl, zinc blende, A15, C15, perovskite, hcp holes and the 2D networks, with their exact flips;
- the soft/hard classification across networks;
- the honeycomb + centres hinge at the trihexagonal tiling;
- the hcp split (−1/8 and 5/24);
- the zinc blende = CsCl polynomial coincidence.

Several of these may be easy, or already known in the radical-tessellation and crystallography literature. Koch 1973 and the radical-tessellation papers should be read, and a web search made, before any novelty claim.

## Run times (dicto-big-brother, `nice -n 10`, load < 1 throughout, one job at a time)

| step | time |
|---|---|
| walks: square / honeycomb / kagome / CsCl | 0.1–1.2 s each |
| walk: fluorite | 15.2 s |
| walk: NaCl | 8.8 s |
| walk: zinc blende | 7.3 s |
| walk: hcp holes | 15.7 s |
| walk: A15 | 9.2 s |
| walk: C15 | 75.7 s |
| relay analysis | about 10 s |
| perovskite | 38.7 s |
| float cross-check | 15.9 s |
| **total** | **about 3.5 min** |

## Files

- `scripts/engine.py`: the exact power-cell engine (any metric, weights affine in 1 or 2 parameters).
- `scripts/networks.py`: the exact site sets and the classical sanity expectations.
- `scripts/census.py`: the weight walk and the per-interval and per-stop checks. Writes `data/raw/<net>.json` and `data/checks/<net>-checks.txt`.
- `scripts/relay.py`: bond lives, flips, hinges, named stops and regressions. Writes `data/raw/relay-summary.json` and `data/checks/relay-checks.txt`.
- `scripts/perovskite.py`: the three-kind chamber map. Writes `data/raw/perovskite.json` and `data/checks/perovskite-checks.txt`.
- `scripts/crosscheck.py`: float cross-check and exact hinge dual cells. Writes `data/checks/crosscheck-checks.txt`.
- `scripts/tables.py`: writes `data/raw/tables.md`, the full tables of cells and bonds per interval and stop.
- `scripts/run.sh`: reruns everything on dicto-big-brother.
