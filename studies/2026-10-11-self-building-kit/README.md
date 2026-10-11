# A self-building kit for the Chain of Karma (DICTO, 2026-10-11)

DICTO's aim: the Lotus seed already rebuilds itself one size up (Chain of Karma, #22). Can every other piece (AXE, FUJI,
CLEO) do the same, so that the whole kit grows without end? DICTO suggested looking at the famous tile set made
from 6D shadows (Mosseri–Sadoc).

## Where each piece stands
| Piece | Rebuilds itself? |
|---|---|
| Icosahedron | **Yes**: the Lotus seed, φ²·I = 12 I + I(1/φ) + 60 AXE + 20 FUJI + 20 CLEO (#22) |
| AXE | **By DICTO's pyramid rule (as FUJI).** A tetrahedron is a pyramid on any face: φ·AXE = AXE + AXE(1/φ) turned over (flat mirror) + sides with Dehn invariant 0 and volume 3·AXE; checked to fit on all four faces. (The six Mosseri–Sadoc tetrahedra alone cannot rebuild themselves, Papadopolos & Ogievetsky 2000, because of their equilateral faces; DICTO's rule is a different route.) |
| CLEO | **By DICTO's pyramid rule**, the same way (fits on all four faces) |
| FUJI | **By DICTO's pyramid rule (below).** φ·FUJI = FUJI tip + mirrored FUJI(1/φ) + sides with Dehn invariant zero |

**Correction (literature search, 2026-10-11).** An earlier version of this table said AXE and CLEO rebuild themselves through the
Mosseri–Sadoc inflation. That was wrong: the volume + Dehn screen passing is necessary only, and the faces block it. Equilateral
faces are the obstacle (Al Raisi, Koca, Koca & Koc 2026 say the same for icosahedra and every tile with three-fold faces).

**FUJI's hexagon is the way past the face obstacle.** FUJI's base is an equilateral triangle with its corners cut off, so an
equilateral triangle of side φ² = FUJI's hexagon (size 1) + 3 equilateral triangles of side 1 (exactly how each face of the Lotus
seed is covered), and one of side φ = the hexagon at size 1/φ + 3 triangles of side 1/φ. The tile sets that rule this out (the
six tetrahedra, Mosseri–Sadoc) have no hexagonal faces. DICTO (2026-10-11): use more tiles than Mosseri–Sadoc, and include them
all for thoroughness (Kramer's seven, Mosseri–Sadoc's four, Danzer's four, the Lotus kit).

## DICTO's FUJI rule: tip, mirror, sides
DICTO's steps (2026-10-11):
1. **Tip.** Cutting a pyramid parallel to its base leaves a smaller copy, so the whole FUJI is the tip of the next size:
   φ·FUJI = FUJI + **band**. Only the band has to be built from parts; each larger size is the same recipe scaled.
2. **Mirror.** Turn a FUJI of size 1/φ upside down in the middle of the band: its base lies centred on the tip's base and its
   apex just touches the band's floor (the band is 1/φ of FUJI's height, exactly the small FUJI's height).
3. **Sides.** What is left, a ring round the mirrored FUJI, is filled from parts.

Exact numbers (`scripts/dehn_screen_sides.py`, `logs/dehn_screen_sides.log`):
- Band volume = (φ³ − 1) FUJI = 2φ FUJI; sides = 2φ − φ⁻³ = **exactly 3 FUJI volumes**.
- Dehn invariant of the band = (φ − 1) D(FUJI) = D(FUJI)/φ = D(mirrored FUJI(1/φ)), so the sides have **Dehn invariant zero**:
  the condition for being cut and rearranged into a cube (Sydler), and the kind of region Danzer's ABCK tetrahedra fill.
- Part mixes that match volume and Dehn of the sides (fewest pieces): Kramer's seven, 5 pieces (t5 + t6 + T2 at φ⁰, t3 at φ⁻¹
  and φ⁻²); Danzer's ABCK alone, 6 pieces (2 A at φ⁰, K at φ⁻¹, C at φ⁻², K at φ⁻³, A at φ⁻⁴); our kit alone, 14 pieces.
- Not yet checked: an actual cut of the sides into those parts (geometric search, e.g. one of three equal parts by symmetry).

**The rule works for any pyramid.** Nothing above used FUJI's shape: for any pyramid P, φ·P = P (tip) + P(1/φ) turned over +
sides, and the band is always 1/φ of P's height, so the turned-over P(1/φ) always just touches the floor. The sides always have
volume φ³ − 1 − φ⁻³ = **3** times P and Dehn invariant (φ − 1 − 1/φ) D(P) = **0**. (For a point-mirror the turned base must fit
inside the tip's base; it does for the regular pentagon and FUJI's hexagon.)

**The sloping faces tile (face test, `scripts/face_tiling.py`, `logs/face-tiling.log`).** Each equilateral sloping face of the
ring is a 60° trapezoid (top 1, bottom φ, legs 1/φ). With the kit's face shapes (equilateral and golden triangles, FUJI's
hexagon, the pentagon) at sizes φ⁻¹ to φ⁻⁴ it tiles exactly as **2 triangles of side 1/φ + 2 of side 1/φ² + 1 FUJI hexagon of size
1/φ²** (a triangle 1/φ in each bottom corner; the middle is an upside-down triangle of side 1 with its point cut off = the hexagon +
2 small triangles). Area 0.7006 both ways. So the face obstacle does not block the pyramid rule, for J2 and for FUJI's three
equilateral faces; the solid pieces behind the faces are what the 3D searches look for.

**What is proved.** Every piece of the kit regrows one φ-step larger from itself: the icosahedron through the Lotus seed, and
AXE, CLEO, FUJI and the pentagonal pyramid through DICTO's pyramid rule, each up to sides with Dehn invariant zero. By Sydler's
theorem such sides can always be cut into finitely many pieces that form a cube: the aperiodic kit regrows itself up to a
periodic (cube-equivalent) remainder. **Not yet proved:** that the sides can be cut into kit pieces (searches running).

## DICTO's dodecahedral Chain
DICTO (2026-10-11): start from a smaller dodecahedron tiled with pentagonal pyramids; the pyramid caps mask it while it grows,
and each cycle ends as a dodecahedron, so the other steps are the icosahedron's.
- **Stage 0** (`scripts/dodeca_chain.py`, `data/dodeca-chain-stage0.json`), taken from the Lotus seed's own pieces:
  **D(1) = 12 pentagonal pyramids (J2, edge 1) + I(1/φ) + 30 AXE + 20 CLEO.** The pyramids stand on D's 12 faces, points inward,
  and each point lands exactly on a corner of the small icosahedron (inradius 1.1135 − pyramid height 0.5257 = 0.5878 = the small
  icosahedron's circumradius). Checks: the 12 bases make a regular dodecahedron (20 corners, all edges 1); 30 AXE and 20 CLEO lie
  inside it and no Lotus piece crosses its surface; volume 7.663119 both ways. (This is the inside of DICTO's 2026-10-05 build,
  Lotus seed = dodecahedron + 12 J11 + 30 AXE + 20 FUJI, Icosa-13 study §10.)
- **Each cycle:** the icosahedron at the core grows by the Chain of Karma (I(1/φ) → Lotus seed of edge φ → …) while the pyramids
  grow by the pyramid rule above; at the end of the cycle the shape is a regular dodecahedron again:
  D(φ²ⁿ) = Chain-grown I(φ²ⁿ⁻¹) + 12 J2 + 30 AXE + 20 CLEO at the stage's size (63, 175 and 1,631 pieces for D(1), D(φ²), D(φ⁴)).
- Relation: Al Raisi et al. (2026) grow the dodecahedron with whole dodecahedra inside; here the dodecahedron grows round
  icosahedra.

## The 600-cell, flattened
DICTO (2026-10-11): the graphics look "remarkably similar to a 4D polytope". The 600-cell seen down one vertex (circumradius 1)
has shells 1, 12 (icosahedron, r 0.587785), 20 (dodecahedron, r 0.866025), 12 (icosahedron, r 0.951057), 30
(icosidodecahedron, r 1), …, alternating icosahedron and dodecahedron. Exact matches (`scripts/cell600_match.py`,
`logs/cell600_match.log`): the Lotus seed's small icosahedron = the first shell (edge 1/φ, r 0.587785); the 13 icosahedron
centres = the centre vertex + its 12 neighbours scaled by φ² (r 1.538842, spacing φ). Reading: the Lotus seed is a flattened
piece of the 600-cell (Sadoc & Mosseri's geometrical frustration), AXE, FUJI and CLEO filling the gaps that curved 4D space closes;
the match is in projection only.

## The fullerene chain
DICTO (2026-10-11). `scripts/fullerene_surface.py`, `logs/fullerene_surface.log`, area checked to 10⁻⁶:
- **Step 1 (Lotus seed):** 60 triangles (edge 1) in 12 pentagonal caps + 20 hexagons (sides 1, 1/φ) = C60's face pattern.
- **Step 2:** 180 triangles (60 in the 12 caps), 60 hexagons (1, 1/φ) + 20 hexagons (φ, φ²); still 12 caps. 80 hexagons = C180's
  count, but not a Goldberg polyhedron (flat triangles remain): fullerenes inside fullerenes, like carbon onions (Ugarte 1992).
- 3D page: Fullerene tab.

## FUJI cut into simpler pieces
- Apex fan over alternate base corners: FUJI = **cube corner** (edges 1, 1, 1 at right angles at the apex, volume 1/6) + 3
  pieces each with exactly CLEO's volume (edges 1/φ, 1, 1, 1, 1, √2; not CLEO's shape). The apex is a dodecahedron corner, so
  the cube corner is the cube inside the dodecahedron.
- DICTO's six tetrahedra (apex, base centre, two neighbouring base corners), halved again into 12 right-angled pieces: two
  kinds, face slopes exactly **41.81°** (on the long sides) and **37.38°** (on the short sides), the family's two key angles.
  They bring in a third angle (22.24° at the centre), so on their own they cannot rebuild themselves at sizes φ⁰ … φ⁻⁶
  (`scripts/dehn_screen_ortho.py`); with Kramer's seven they pass.

## Checks
**Volume + Dehn screen** (`scripts/dehn_screen.py`, `scripts/dehn_screen_ms.py`; logs in `logs/`). Every piece at sizes φ⁰ down
to φ⁻⁴ (φ⁻⁶ with the tiles). Coordinates snapped to Q(√5), 50 digits, angle and length bases by PSLQ, whole-number counts
by integer programming. These are necessary conditions only; passing does not prove a dissection.
- Dihedral angles of the whole family span two directions mod 180°: 37.377° and 41.810° (= arccos(√5/3)).
- Sanity: the Lotus seed passes; Danzer's φ·A, B, C, K pass; Mosseri–Sadoc φ·t1 … t6 pass; Koca's icosahedron passes.
- With mixed sizes, nothing is ruled out: φ·I, AXE, FUJI, CLEO and φ²·I, AXE, FUJI, CLEO all have whole-number recipes from
  our own kit. (The single-size result of the Chain of Karma study, which ruled them out, still stands for one size.)
- Danzer's ABCK tetrahedra (Frettlöh's coordinates) all have **Dehn invariant zero**, so they can only balance volume.
- Kramer's seven tiles = Mosseri–Sadoc t1 … t6 + T2 (T2 = t2 ∪ t4, opposite edges 1 and τ², the rest τ).

**Tiles in the Lotus frame** (`scripts/ms_in_frame.py`, `data/ms-kit.json`). All seven found as vertex sets of the Lotus seed
(t3 from the Chain of Karma step 2), so they sit in the Lotus frame's icosahedral orientation. `ms-kit.json` = the 113
Lotus pieces + one copy of each tile.

**Geometric searches** (`scripts/selfbuild.py`, `scripts/selfbuild_ms.py`, `scripts/blockcut.py`)
- No φ·, φ²· or φ³·CLEO, AXE or FUJI region made of whole pieces exists inside the 1,569-piece Chain of Karma step 2
  (only icosahedra, i.e. the Lotus seed again): `logs/blockcut.log`.
- φ·CLEO from our kit only, small placement set: proved infeasible (`logs/selfbuild-cleo.log`). The larger run was stopped
  by DICTO in favour of the Mosseri–Sadoc route.
- φ·FUJI from our kit + Kramer's seven at φ⁰ and φ⁻¹ (36,875 placements, tip allowed): **no fit** (proved infeasible for
  these placements, 250 s): `logs/selfbuild-ms-fuji1.log`.
- The band alone at φ⁰ … φ⁻² (184,558 placements): stopped by DICTO before the solve, once the mirror rule above was found
  (`scripts/selfbuild_band.py`, `logs/selfbuild-band1.log`).

Not checked: the 6D-lattice lift of the vertices in this study depended on the chosen basis and is not reported.

## Prior art
- Mosseri & Sadoc 1982; Kramer 1982 (seven tiles); Papadopolos & Ogievetsky 1999, *On inflation rules for Mosseri–Sadoc
  tilings* (arXiv math-ph/9911005): the Dehn-invariant vector is an eigenvector of the inflation matrix with eigenvalue τ.
- Koca, Koc, Koca & Al-Siyabi 2020 (arXiv 2009.07048): the tiles' table, the icosahedron from tiles, and the statement that
  the tiles alone do not inflate the icosahedron past edge τ (the Lotus seed reaches φ² with whole icosahedra).
- Sydler 1965 (Dehn invariant zero and equal volume is enough for scissors congruence to a cube).
- Danzer 1989; Frettlöh, *Icosahedral tilings in R³: the ABCK tilings* (coordinates, inflation matrix).
- R. W. Gray (2002), icosahedron scaling pages: nested icosahedra at every φ-power, "each icosahedron at pⁿ contains a center
  at pⁿ⁻³ and 12 at pⁿ⁻²" (the Lotus seed's icosahedra and the Chain's hierarchy of icosahedra; the gap filling, the solid
  replacement rule and the Dehn and face analysis are not there).
- The Sierpinski icosahedron (n-flake; Kunnen & Schlicker 1998, Bourke): 12 corner icosahedra at 1/φ², gaps left empty.
- R. Al Raisi, N. O. Koca, M. Koca, R. Koc (2026), *Modified Mosseri–Sadoc tiles from D6*, arXiv:2604.03988: the regular
  **dodecahedron** grows by τⁿ for every n with whole dodecahedra inside, d(τ²) = 7 d(1) + tiles; they state icosahedra cannot be
  done with their tiles (equilateral faces). The Chain of Karma is the icosahedral counterpart, done with whole icosahedra and
  FUJI's hexagons. Closest known work.
- Papadopolos & Ogievetsky (2000): the six tetrahedra admit no stone inflation (Dehn invariants and faces).
- Janot and de Boissieu: quasicrystal models built recursively from pseudo-Mackay atomic clusters (clusters of clusters).
- Credit: AXE = Mosseri–Sadoc t6 and CLEO = t4 (already credited in the Icosa-13 study). Names Lotus seed, AXE, FUJI,
  CLEO and Chain of Karma: DICTO.

Renders: none yet (to follow with a geometric cut of the sides).
