# Bond Relay of the DICTONIC loops (2026-10-25)

"Bond Relay" is a working name. DICTO decides the names. The names of the loops, solids and stops are the ones used in papers #48 and #51 and in the app.

## Question

The DICTONIC world draws a **web**: one bond for every face that two pieces share, weighted by the face's area (`webOf`, k-dshells `src/app/world-dictonic.js`, branch dictonic-shells). Float runs on a size-2 network suggested that bonds trade places along each loop. This study answers five questions exactly:
(1) is each loop a power diagram (Laguerre / weighted Voronoi diagram) of fixed sites with a moving weight;
(2) what are the face shapes and areas of each bond type, and where is each bond type born and where does it die;
(3) how many bonds does each piece have (its coordination number);
(4) one main theorem;
(5) prior art.

**The loops, as the code defines them** (the code is the reference; part C checks the frame):
- **Golden.** T(x) = hull of all permutations of (±(1+x), ±x, 0), scaled so its squares sit at L/2 with L = φ. T(x) sits on the simple-cubic points n·φ/2 with every n even ("big"); T(1/x) sits on the cube centres, every n odd ("small"). x runs from 0 to ∞. Write **s = x/(1+x)** ∈ [0, 1]. Then T(x) is the set of signed permutations of (1, s, 0)·L/2, and T(1/x) is the same with s replaced by 1 − s.
- **Delian.** krp-core `tetPiece` / `octPiece`, at t ∈ [0, 1]. The tetrahedron pieces are centred on the unit-cube centres (Z + ½)³. The octahedron pieces are centred on the odd integer points. a = 3(1 − t)/2. The app scales by 1/√2, so the octet edge is 1.

## Method

Everything below is exact. Python Fractions are used over the fields Q, Q(√5), Q(√2), Q(√6), Q(∛2) and Q(∛6), and sympy is used for anything that depends on the parameter. Floats are used only to choose candidate plane triples and as the cross-check in part C. A number is zero only if all of its field coefficients are zero. The sign of a nonzero number comes from an 80-digit evaluation.

- **A, `scripts/symbolic.py` (symbolic, whole regimes).** Regimes: golden s ∈ (0, 1); Delian t ∈ (0, 1/3) and t ∈ (1/3, 1).
  - A1: every corner of the app's piece satisfies every power-diagram inequality against every site within D, with slack ≥ 0 on the whole open interval. The slacks are linear, and the script checks they have no root inside.
  - A2: the facet planes are bisectors. Their own vertex enumeration gives back exactly the piece's corners. The normals sum to 0 and have rank 3, so the region they bound is bounded. Together with A1 this gives **piece = power cell**.
  - A3: the closed-form area of every bond face.
  - A4: the volumes add up to the lattice cell.
  - A5: faces pair up face to face.
  - A6: monotonicity, birth and death points, the x ↔ 1/x swap, and equality at x = 1.
  - A7: a uniform distance bound shows the finite site list is enough.
- **B, `scripts/samples.py` (exact, sample parameters).** The power cells are built from scratch among the fixed sites, with no use of the app's pieces. Golden x = 0, 1/3, 1/2, 1, 2, 3, τ, 1/τ, √2, ∞. Delian t = 0, 1/6, 1/4, 1/3, 1/2, 2/3, 1 and the irrational stops: equilateral RD (2√6 − 3)/15, half 1 − ∛6/3, Delian bond 1 − (2/3)·2^(−1/3), equilateral cube 5/3 − (2/3)√2.
  - B1: power cell = the app's piece.
  - B2: areas = the closed forms.
  - B3: bond counts.
  - B4: volumes.
  - B5: faces pair up face to face.
  - B6: how many cells meet at each corner, and of which kinds.
  - B7: distance bound.
  - B8: the dual weighted-Delaunay cells tile space, with exact volumes.
- **C, `scripts/app_dump.mjs` + `check_app.py` (floats).** The app's own `goldenT`, `delianFamily`, `tetPiece`, `octPiece` and `webOf`, on a size-2 network.
  - C1: frame and scale assert.
  - C2: every app bond area matches the closed form (max error < 1e-9).
  - C3: the float findings.
  - C4: bonds of the central pieces.

Sanity cases inside the checks:
- Kelvin (x = 1): square L²/8 and hexagon (3√3/16)L², with all edges equal.
- Octet triangle: √3/4 at edge 1.
- Rhombic dodecahedron rhombus: √2/4 at octet edge 1 (√2/2 in tetPiece units).
- Cube face: 1/2 (tetPiece unit 1).
- The volumes of #51: 9t³ and 2 − 18t³; 1 − (2/3)a³ and (4/3)a³.

## Results

### 1. Both loops are power diagrams of fixed sites (Q1: yes)

| loop | sites (app units) | weight difference | range |
|---|---|---|---|
| Golden | B = φZ³ (big), S = φZ³ + (φ/2)(1,1,1) (small): the bcc points | w_B − w_S = (φ²/4)·(x − 1)/(x + 1) = (L/2)²(2s − 1) | −φ²/4 (x = 0) … 0 (Kelvin) … +φ²/4 (x = ∞); at τ: 1/(4φ) |
| Delian | Q = ((Z + ½)³)/√2 (tet), O = {n ∈ Z³ : Σn odd}/√2 (oct) | w_Q − w_O = (3/8)(2t − 1) | −3/8 (RD) … −1/8 (octet) … +3/8 (cubes); at the Delian bond: 3/8 − 2^(2/3)/4 |

The power cell is defined by |p − c_i|² − w_i ≤ |p − c_j|² − w_j. The weight is linear in s = x/(1+x) for the golden loop and linear in t for the Delian loop. At the ends no weight is infinite. In the Delian loop, the cell of the vanishing kind shrinks to a single point: the Q cells at t = 0 and the O cells at t = 1 (B1). These weights agree with #51's cube Remark, w = (x − 1)/(4(x + 1)) at cube edge 1, and with `octet_exact.py` (w_T = (3/4)(2t − 1), tetPiece units). This study proves both for every parameter, not only at samples. So **the web is the 1-skeleton of the dual regular (weighted-Delaunay) subdivision**: two sites are bonded exactly when they span an edge of a dual cell.

### 2. Bond faces and areas (app units: golden L = φ, Delian octet edge 1)

| bond | face | area | born / dies | monotone? |
|---|---|---|---|---|
| golden big–small | hexagon (triangle at x = 0, ∞) | (√3/8)φ²·(x² + 4x + 1)/(1 + x)² | never: ≥ (√3/8)φ² ≈ 0.5668 at both ends | no: rises on (0, 1), falls on (1, ∞), max (3√3/16)φ² ≈ 0.8502 at Kelvin |
| golden big–big | square, diagonal sL | φ²x² / (2(1 + x)²) | born at x = 0⁺, → φ²/2 as x → ∞ | strictly increasing |
| golden small–small | square, diagonal (1 − s)L | φ² / (2(1 + x)²) | from φ²/2 at x = 0, dies as x → ∞ | strictly decreasing |
| Delian oct–tet | triangle | (9√3/4)t² for t ≤ 1/3; (9√3/16)(1 − t)² for t ≥ 1/3 | alive exactly on (0, 1) | no: rises to √3/4 (octet triangle) at 1/3, then falls; a corner at 1/3 (slopes 3√3/2 and −3√3/4) |
| Delian oct–oct | hexagon (rhombus at t = 0) | (√2/4)(1 − 9t²) | from √2/4 at t = 0, dies exactly at t = 1/3 | strictly decreasing |
| Delian tet–tet | hexagon (square with two opposite corners cut; square at t = 1) | (3t − 1)(5 − 3t)/8 = (1 − a²)/2 | born exactly at t = 1/3, → 1/2 at t = 1 | strictly increasing |

Sample values:
- Kelvin, x = 1: big–big = small–small = **φ²/8 ≈ 0.32725**.
- x = τ: big–big = **1/2**, small–small = **1/(2φ²) ≈ 0.19098**, big–small = (√3 + 3√15)/16 ≈ 0.8344.
- Delian bond: oct–tet = 2^(1/3)√3/8 ≈ 0.2728, tet–tet = 1/2 − 2^(1/3)/4 ≈ 0.1850.
- Volumes, in units of (L/2)³: golden (4/3)(1 + u)³ − 4u³ with u = s (big) or 1 − s (small), always adding to L³. The Delian volumes are those of #51.

Proofs of the golden birth/death, swap and equality claims:
- **Swap x ↔ 1/x.** s ↔ 1 − s flips the sign of the weight. The translation by (φ/2)(1,1,1) swaps B and S, so the diagram at 1/x is the diagram at x translated, with big and small exchanged. Hence big–big(1/x) = small–small(x), and big–small is invariant.
- **Equality at x = 1 only.** The ratio is big–big / small–small = x², so the two are equal only at x = 1.

### 3. Bonds per piece (coordination numbers, exact; B3/C4)

| | x = 0 | 0 < x < ∞ | x = ∞ |
|---|---|---|---|
| golden big | 8 (8 big–small; octahedron) | 14 = 8 big–small + 6 big–big | 14 = 8 + 6 (cuboctahedron) |
| golden small | 14 = 8 + 6 small–small (cuboctahedron) | 14 = 8 big–small + 6 small–small | 8 (octahedron) |

| | t = 0 | 0 < t < 1/3 | t = 1/3 | 1/3 < t < 1 | t = 1 |
|---|---|---|---|---|---|
| Delian oct | 12 oct–oct (RD) | 20 = 12 oct–oct + 8 oct–tet | 8 oct–tet | 8 oct–tet | none (point) |
| Delian tet | none (point) | 4 oct–tet | 4 oct–tet | 10 = 4 oct–tet + 6 tet–tet | 6 tet–tet (cube) |

Each golden piece's 6 squares always bond to its own kind (big–big, or small–small). The like bonds are not swapped between pieces; at an end, one kind's squares shrink to points.

### Dual weighted-Delaunay cells (B6, B8: exact volumes, tetPiece / L/2 units)

- **Golden, 0 < x < ∞:** one subdivision throughout, bcc disphenoid tetrahedra (2 big + 2 small, volume 2/3). There is **no flip**.
- **Golden, x = 0 and x = ∞:** square bipyramids (2 + 4 sites, volume 8/3).
- **Delian, t < 1/3:** octahedra (6 O, volume 4/3) and tetrahedra (3 O + 1 Q, volume 1/12).
- **Delian, t = 1/3:** rhombic dodecahedra (6 O + 8 Q, volume 2).
- **Delian, t > 1/3:** cubes (8 Q, volume 1) and square pyramids (1 O + 4 Q, volume 1/6).
- **Delian ends:** at t = 0 the dual is the octet (fcc Delaunay); at t = 1 it is cubes.

At t = 1/3 each RD rhombus trades its long diagonal (oct–oct) for its short one (tet–tet). This is a single flip.

## Main theorem (working name: Bond Relay Theorem; DICTO decides the name)

**In plain words:** each DICTONIC loop is one fixed crowd of points of two kinds with one weight slid between the kinds. The bonds are the edges of the dual weighted-Delaunay web, and the bond between unlike pieces never breaks inside the loop. The two like bonds hand over: gradually in the golden loop (both alive all the way, equal at Kelvin), and all at once in the Delian loop (at the octet).

**Statement.**
(i) For every x ∈ [0, ∞] the golden network is the power diagram of the bcc sites B ∪ S with w_B − w_S = (φ²/4)(x − 1)/(x + 1). For every t ∈ [0, 1] the Delian network is the power diagram of Q ∪ O with w_Q − w_O = (3/8)(2t − 1). At t = 0 the Q cells are points, and at t = 1 the O cells are points.
(ii) The web is the 1-skeleton of the dual regular subdivision. The bond areas are those of the table in §2.
(iii) *Golden (soft relay).* For 0 < x < ∞ all three bond types are present and the face lattice is constant. Big–big rises strictly from 0 and small–small falls strictly to 0. Their ratio is x², the diagonals of the two square faces add up to the lattice spacing φ, and the two areas are equal only at x = 1. The whole picture is symmetric under x ↔ 1/x.
*Delian (hard relay).* Oct–tet is present exactly on (0, 1). Oct–oct is present exactly on [0, 1/3), and tet–tet exactly on (1/3, 1]. **t = 1/3 is the only parameter where both pieces exist and every face is of one bond type** (the web is bipartite there). The ends t = 0 and t = 1 have a single bond type only because one piece has vanished. The golden loop never has a single bond type: at x = 0 there are two (big–small and small–small), and at x = ∞ two (big–small and big–big).

**Proof sketch.**
- Choosing the weights in (i) makes every facet plane of every app piece a bisector of the two sites that share it (A2). Every corner satisfies all the other bisector inequalities (A1; the slacks are linear in s or t with no root inside a regime), and the site list is enough (A7). So piece = power cell for every parameter, and the ends follow from B1 at exact end values.
- Power diagrams are dual to regular subdivisions (Aurenhammer 1987), which gives (ii). The faces are computed directly (A3).
- (iii) follows from the closed forms (A6) and the incidence counts (B6). The golden swap is the translation (φ/2)(1,1,1).

**Corollaries.**
1. **Coordination numbers:** the tables in §3.
2. **Mixed-bond maxima.** The mixed bond peaks at Kelvin, smoothly, at (3√3/16)φ² in the golden loop. In the Delian loop it peaks at the octet, with a corner, at √3/4.
3. **Weight geometry.** Both weight lines are segments in the space of weights for fixed sites (the secondary fan). The golden segment stays inside one chamber except at its ends. The Delian segment crosses exactly one wall, at t = 1/3, and the regular subdivision there is the rhombic dodecahedra.
4. **Delian bond.** w_Q − w_O = 3/8 − 2^(2/3)/4 ≈ −0.0218, which is close to, but not at, the unweighted Voronoi point (t = 1/2). Oct–tet / tet–tet = 2^(1/3)√3 / (4 − 2·2^(1/3)).

## Float findings: verdict

| finding (size-2 float run) | verdict |
|---|---|
| Golden: every piece keeps 8 big–small bonds at all x | **confirmed** exactly, including x = 0 and ∞ |
| Big–big and small–small (6 per piece) trade; big–big → 0 as x → 0, small–small → 0 as x → ∞ | **confirmed**, with one precision: a big piece's 6 squares are always big–big and a small piece's 6 are always small–small; it is their areas that trade (ratio x²) |
| Equal at x = 1, area 0.3273 | **confirmed**: φ²/8 = 0.327254… |
| x ↔ 1/x swaps them exactly (0.5000 and 0.1910 at τ) | **confirmed**: 1/2 and 1/(2φ²) |
| Delian regimes (oct–oct only at 0; both for 0 < t < 1/3; only oct–tet at 1/3; tet–tet + oct–tet above; only tet–tet at 1) | **confirmed** exactly |
| "t = 1/3 is the ONLY single-web t" (the question's wording) | **true only with a qualifier**: t = 0 and t = 1 also carry a single bond type, but there one piece is absent. t = 1/3 is the only single-type t at which both pieces exist |

Nothing contradicts the float findings.

## Prior art

**DICTO's reference library.** Five `ask-library` queries were run: power diagram / Laguerre / weighted Voronoi; contact graph of a space-filling; Koca truncated-octahedron family on bcc; octet / RD / cube family; regular triangulation / flips / secondary polytope. INDEX.html, READING-LIST.md and README.md were also searched for "Laguerre", "power diagram", "Aurenhammer", "weighted Voronoi", "contact graph", "secondary polytope", "regular triangulation", "Gelfand" and "Knoll". **Nothing on power diagrams, Laguerre tessellations, contact graphs or secondary polytopes was found in the library.** It has Koca et al. 2015 (the T(x) orbit, already cited in #48) and Erdahl 1999 / Garber 2019 (Voronoi's theory of lattice Delaunay subdivisions, which is related but treats lattices, not two-kind weighted sites).

**Known (standard, from the literature as cited in #48 and #51, and general knowledge; not re-read for this study):**
- Power diagrams and their duality with regular triangulations: Aurenhammer, SIAM J. Comput. 16 (1987).
- Regular subdivisions changing only at the walls of the secondary fan: Gelfand–Kapranov–Zelevinsky 1994; De Loera–Rambau–Santos 2010.
- Radical (power) tessellations of two-size sphere packings in materials science, for example Gellatly & Finney 1982.
- Two unequal truncated octahedra on bcc as Laguerre cells: general.
- The octet / RD / cube connections: Knoll & Morgan, Bridges 2003, cited in #51.
- DICTO's own #51 Remark and `octet_exact.py` already gave the two weights.

**Not found in DICTO's library (no web search in this study):**
- the bond-area closed forms of both loops;
- the soft-relay versus hard-relay contrast (no flip in the golden loop, a single flip at the octet in the Delian loop);
- the like-bond ratio x² and the diagonal sum φ;
- the sequence of dual cells (disphenoids; octahedra + tetrahedra → rhombic dodecahedra → cubes + square pyramids);
- t = 1/3 as the unique bipartite-web member.

These may well be easy consequences of the standard theory. A web search is needed before any claim of novelty.

## PASS / FAIL

| part | checks | PASS | FAIL |
|---|---|---|---|
| A symbolic (whole regimes) | A1–A7 | 55 | 0 |
| B exact samples (10 golden, 11 Delian; rational and irrational) | B1–B8 | 211 | 0 |
| C app float cross-check (frame, areas, counts, float findings) | C1–C4 | 105 | 0 |
| **total** | | **371** | **0** |

Run times on dicto-big-brother (load < 0.4, `nice -n 10`):
- A: 13.8 s
- B: 30.2 s

Part C ran on the Pi (app dump 1 s, check < 1 s).

## Files

- `scripts/lib.py`: exact field arithmetic, power cell, faces, volume, distance bound.
- `scripts/symbolic.py`: part A, giving `data/raw/symbolic.json` and `data/checks/symbolic-checks.txt`.
- `scripts/samples.py`: part B, giving `data/raw/samples.json` and `data/checks/samples-checks.txt`.
- `scripts/app_dump.mjs` (+ `reg.mjs` and `hooks.mjs`, which only resolve `three` for the import): the app's pieces and web, giving `data/raw/app-dump.json`.
- `scripts/check_app.py`: part C, giving `data/checks/app-checks.txt`.
- `scripts/run.sh`: reruns everything.
