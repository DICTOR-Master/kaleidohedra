# The onions of the DICTONIC atoms (2026-10-25)

Follows the web-of-bonds study (`../2026-10-25-web-of-bonds`, paper #52). Names are the published ones (#48, #51, #52) and the app's
(k-dshells `src/app/world-dictonic.js`, i18n `dictonic.stop.*`). Nothing is renamed; no new names.

## Question

DICTO, 2026-10-25: "do the atoms contain alternating shell arrangements?" and "does up and down remove or add a shell?"

**Short answer.** Each slider step moves a shell from one kind of atom to the other. One kind's onion gains a shell, and the other
kind's onion loses the same volume. The shell crosses the unlike-bond faces (golden hexagons, Delian triangles). Those faces slide like
pistons. The like-bond faces never move: they stay on fixed planes and only grow or shrink within them.

Inside one atom the shells do not alternate. They are all that atom's own cells at earlier slider positions, nested in order. What
alternates is the two kinds in space (bcc in the golden loop, octet sites in the Delian loop). Neighbouring atoms of the two kinds
hold complementary parts of the loop:
- **Golden.** At x, a big atom holds the shells T(y) for y ≤ x, and a small atom holds T(y) for y ≤ 1/x. Both onions are the same
  family T(y), read from opposite ends. At Kelvin (x = 1) both hold exactly the same shells.
- **Delian.** The two onions differ. The tet onion runs from tetrahedra to cut cubes; the oct onion runs from octahedra to cut rhombic
  dodecahedra. Both onions change type at the same stop, the octet (t = 1/3). This is the loop's one bond flip, seen from inside
  each atom.

## Method

The two loops are power diagrams of fixed sites with one weight slid between the two kinds (#52):
- golden: w_big − w_small = (φ²/4)(x − 1)/(x + 1);
- Delian: w_tet − w_oct = (3/8)(2t − 1), app units.

A power cell is {p : |p − c_i|² − w_i ≤ |p − c_j|² − w_j for all j}.

Units:
- golden: L/2 = 1, app = × φ/2;
- Delian: krp-core tetPiece units, app = × 1/√2.

Scripts (`scripts/`):
- `onions_exact.py`, exact (sympy, plus the exact field arithmetic of the web-of-bonds `lib.py` and `samples.py`):
  - N1: the lemma.
  - N2: the closed-form onions.
  - N3: the stop order and the nesting of the stop shells.
  - N4: power cells built from scratch at every stop and at regime interiors, compared with the closed form; face tables and
    named-shape properties.
  - N5: the closed form is the whole power cell on every regime.
- `app_dump.mjs` + `check_app.py` (floats): the app's `goldenT`, `tetPiece`, `octPiece` and stop values, and DICTO's Polyhedraverse
  pieces, against the closed-form shells.
- `geom.py`, `blender_render.py` (Blender 5.0.1, Cycles), `compose.py` (matplotlib): the figures.
- `run.sh` reruns everything. The exact part, the renders and the composition ran on dicto-big-brother with `nice -n 10`. The exact
  part takes 43 s; each render 0.2–1.5 min at 1400 px.

### Proof of the nesting (N1, N2)

**Lemma.** Write slack_j(p) = (|p − c_j|² − w_j) − (|p − c_i|² − w_i). Its derivative in w_i − w_j is 1, and does not depend on p.
In both loops:
- same-kind weight differences are 0;
- unlike differences are ±Δ(parameter);
- Δ is strictly increasing: golden dΔ/dx = φ²/(2(1 + x)²) > 0; Delian dΔ/dt = 3/4.

So when the parameter rises, every inequality of a big or tet atom loosens, and every inequality of a small or oct atom tightens.
Hence cell(p₁) ⊆ cell(p₂) whenever the atom's weight rises. This holds for all four atoms.

**Closed form (N2).** Every half-space below is checked to be the power bisector of a nearest neighbour, identically in the parameter:

| atom | fixed part (like bonds) | moving part (unlike bonds) |
|---|---|---|
| golden big | cube \|p_i\| ≤ 1 | ±p₁ ± p₂ ± p₃ ≤ 1 + s, with s = x/(1+x) rising |
| golden small | cube \|p_i\| ≤ 1 | ±p₁ ± p₂ ± p₃ ≤ 2 − s, falling |
| Delian tet | cube \|p_i − q_i\| ≤ ½ | d·(p − q) ≤ 3t/4 over its 4 oct corners d, rising |
| Delian oct | rhombic dodecahedron \|p_i\| + \|p_j\| ≤ 1 | \|p\|₁ ≤ 3(1 − t)/2, falling |

Only the unlike-bond planes move, and only outward for the growing kind. This gives a second proof of the nesting, and also the
"pistons" picture.

Volumes are strictly monotone, and the two kinds' volumes add to a constant:
- golden: V = (4/3)(1 + u)³ − 4u³ with u = s or 1 − s; dV/du = 4(1 + 2u − 2u²) > 0 on [0, 1]; V_big + V_small = 8 = L³;
- Delian: 9t³ / 2 − 18t³ and 1 − (2/3)a³ / (4/3)a³; 8V_tet + 4V_oct = 8.

**Where the gained shell comes from.** Suppose the parameter moves from p₁ to p₂ and a point q joins atom i. At p₁, q lay in some
cell m. If m were of i's own kind, then cell m would also have grown, and q would lie in both cell_m(p₂) and cell_i(p₂), which only
happens on a boundary. So the shell an atom gains is cut from its unlike neighbours, across the moving faces. The two kinds trade
exactly one shell per step.

## Results: the onions, inside out (N3, all PASS)

**Golden big** (grows with x):

| stop | shell |
|---|---|
| x = 0 | regular octahedron |
| x = 1/τ | T(1/τ), the Unborn Axes (same solid as the small piece at x = τ; here at a big site, by the swap x ↔ 1/x) |
| x = 1 | Kelvin's truncated octahedron |
| x = τ | Icosaxes (the golden bond) |
| x → ∞ | cuboctahedron |

**Golden small** (grows as x falls; the same shells read in reverse):

| stop | shell |
|---|---|
| x → ∞ | octahedron |
| x = τ | Unborn Axes (the golden bond) |
| x = 1 | Kelvin's truncated octahedron |
| x = 1/τ | T(τ), the Icosaxes |
| x → 0 | cuboctahedron |

x = 1/τ is not an app stop. The shells there are named because #48 Theorem 4 identifies T(τ) and T(1/τ) with the Icosaxes and the
Unborn Axes.

**Delian tetrahedron atom** (grows with t):

| stop | shell |
|---|---|
| t = 0 | point (the site) |
| equilateral (a), (2√6 − 3)/15 ≈ 0.1266 | regular tetrahedron |
| t = 1/3 | octet tetrahedron |
| half and half, 1 − ∛6/3 ≈ 0.3943 | cut cube |
| Delian bond, 1 − (2/3)·2^(−1/3) ≈ 0.4709 | Samson |
| equilateral (b), 5/3 − (2/3)√2 ≈ 0.7239 | cut cube, all edges equal |
| t = 1 | cube |

**Delian octahedron atom** (grows as t falls):

| stop | shell |
|---|---|
| t = 1 | point (the site) |
| equilateral (b) | regular octahedron |
| Delian bond | Delilah |
| half and half | octahedron |
| t = 1/3 | octet octahedron |
| equilateral (a) | rhombic dodecahedron with 8 cut corners, all edges equal |
| t = 0 | Kepler's rhombic dodecahedron |

For every atom, each stop shell lies inside the next one and is not equal to it (exact sympy).

Note: the shells are nested but not strictly inside one another everywhere. Their like-bond faces lie on the same fixed planes
(golden squares on the cube planes; Delian tet–tet faces on the cube planes for t ≥ 1/3; Delian oct–oct faces on the rhombic
dodecahedron planes for t ≤ 1/3). The panels show this: on the cut faces, the bands are separate only across the moving faces.

### Where a shell changes shape (faces born or dying = the bond flips; N4, exact face tables)

| atom | regime | faces |
|---|---|---|
| golden big | 0 < x < ∞ | always 8 hexagons (big–small) + 6 squares (big–big): one face type throughout, **no flip** |
| golden big | x = 0 | the 6 squares are born as points at the octahedron's corners |
| golden big | x → ∞ | each hexagon's 3 hexagon–hexagon edges shrink to points (24 corners → 12): hexagons → triangles, cuboctahedron |
| golden small | mirror image | the same events: squares born at x → ∞, hexagons → triangles at x → 0 |
| Delian tet | t → 0⁺ | born from a point with 4 triangles (tet–oct) |
| Delian tet | t = 1/3 | **6 tet–tet hexagons are born** on the tetrahedron's 6 edges (tetrahedron → cut cube) |
| Delian tet | t = 1 | the 4 triangles die at the cube's corners (cube) |
| Delian oct | t = 0 | 12 rhombi (oct–oct) |
| Delian oct | t → 0⁺ | 8 triangles (oct–tet) are born at the 3-fold corners; rhombi → hexagons |
| Delian oct | t = 1/3 | **the 12 oct–oct hexagons die** onto the octahedron's 12 edges |
| Delian oct | t = 1 | shrinks to a point |

So the Delian flip at t = 1/3 shows in both onions at the same stop. The golden onions keep one combinatorial type, the truncated
octahedron, from their core to their skin.

### Named shapes (N4 exact, C2 floats), all PASS

- Golden:
  - x = 0: regular octahedron.
  - x = 1: Kelvin, 36 equal edges.
  - x → ∞: cuboctahedron.
  - x = τ: the 12 cyclic corners of T(τ) span the regular icosahedron, edge 1 (#48 Main theorem (e)).
  - x = 1/τ: those of T(1/τ) span the Unborn, with 24 edges of 1 and 6 of 1/φ (#48).
  - App: Polyhedraverse **Icosaxes** = big shell at x = τ, and **Unborn Axes** = small shell at x = τ (= big shell at x = 1/τ).
- Delian:
  - t = 0: rhombic dodecahedron, 12 rhombi.
  - Equilateral (a) and (b): every edge of both pieces equal.
  - t = 1/3: octet tetrahedron and octet octahedron, both regular with edge √2 in tetPiece units (octet edge 1 in the app).
  - Half and half: 8V_tet = 4V_oct = 4.
  - Delian bond: both pieces have volume 2/3. Samson is twice the octet tetrahedron. Delilah is half the octet octahedron, with
    corners at 2^(−1/3) on the axes.
  - t = 1: cube.
  - App: Polyhedraverse **Samson** and **Delilah** = the tet and oct shells at the Delian bond (/√2).

## Checks

| part | PASS | FAIL |
|---|---|---|
| exact `onions_exact.py` (N1–N5; `data/checks/onions-checks.txt`) | 106 | 0 |
| app floats `check_app.py` (C1 frame and scale of goldenT, tetPiece and octPiece at every stop; C2 the four named pieces; C3 stop values; `data/checks/app-checks.txt`) | 23 | 0 |
| **total** | **129** | **0** |

The first exact run had 2 FAILs. Both were bugs in the check itself: a field element was compared to the integer 2 by hash. After
the fix, 106/106 PASS.

## Figures (`figures/`, copies in `~/Documents/papers-to-read/atom-onions/`, 3200 × 3120 px, DICTO mark bottom right)

**`fig1-golden-onions.png`:**
- (a) big atom and (b) small atom, quarter cut open. The wedge round the +x axis is removed; its cut planes x = ±y contain the
  moving-face normals. Stop shells are translucent and coloured: Icosaxes green and Unborn Axes orange as in the app, Kelvin cyan,
  octahedron purple, cuboctahedron slate. The cut faces carry the onion bands and rings; the grey rings are the in-between shells.
  The labels give the stop and the name. (a) and (b) are the same geometry with reversed readings.
- (c) meshing at x = τ: Icosaxes and Unborn Axes filling space, cut by the plane x = y. Every cut cell shows its own onion.
- (d) the same plane, flat and exact. Big atom: 4 stop shells (octahedron, Unborn Axes, Kelvin, Icosaxes). Small atom: 2 (octahedron,
  Unborn Axes).

**`fig2-delian-onions.png`:**
- (a) tet atom and (b) oct atom, cut the same way (Samson gold, Delilah blue).
- (c) meshing at the Delian bond (Samsons and Delilahs).
- (d) the flat plane x = y. Samson: 4 stop shells (tetrahedron (a), octet tetrahedron, half and half, Samson). Delilah: 2
  (octahedron (b), Delilah).
- In odd cubes the tetrahedron piece is the mirror image, as in krp-core `tetPiece`.

## Files

- `scripts/`: `onions_exact.py`, `app_dump.mjs` (+ `reg.mjs`, `hooks.mjs`), `check_app.py`, `geom.py`, `blender_render.py`, `compose.py`, `run.sh`.
- `data/raw/`:
  - `onions.json`: sequences, face tables, named checks;
  - `app-dump.json`;
  - `scene-*.json`: render geometry;
  - `slices.json`: the exact sections for panel (d).
- `data/checks/`: `onions-checks.txt`, `app-checks.txt`.
- `renders/`: the Blender panels (1400 px, transparent) and the projected label anchors.
- `figures/`: the two figures.

Prior art: none claimed. Nested power cells under a monotone weight are a standard property of power diagrams (Aurenhammer 1987); the
named shells are from #48, #51 and #52.
