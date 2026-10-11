# A self-building kit for the Chain of Karma (DICTO, 2026-10-11)

DICTO's aim: the Lotus seed already rebuilds itself one size up (Chain of Karma, #22). Can every other piece (AXE, FUJI,
CLEO) do the same, so that the whole kit grows without end? DICTO suggested looking at the famous tile set made
from 6D shadows (Mosseri–Sadoc).

## Where each piece stands
| Piece | Rebuilds itself? |
|---|---|
| Icosahedron | **Yes**: the Lotus seed, φ²·I = 12 I + I(1/φ) + 60 AXE + 20 FUJI + 20 CLEO (#22) |
| AXE | **Yes, with Mosseri–Sadoc tiles.** AXE *is* Mosseri–Sadoc t6 at scale 1/φ, so φ·AXE = t6, and the six tiles inflate by φ into each other (Mosseri & Sadoc's Stein inflation) |
| CLEO | **Yes, the same way.** CLEO is t4 at scale 1/φ |
| FUJI | **Tentative (DICTO's rule, below).** φ·FUJI = FUJI tip + mirrored FUJI(1/φ) + sides with Dehn invariant zero |

The icosahedron is itself a union of the tiles: I = 7 t1 + 6 t2 + 2 t5 + t6 (Koca et al. 2020). So if FUJI works, the kit
{I, FUJI, t1 … t6} rebuilds itself completely: the Chain of Karma joined to the Mosseri–Sadoc inflation.

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
- Credit: AXE = Mosseri–Sadoc t6 and CLEO = t4 (already credited in the Icosa-13 study). Names Lotus seed, AXE, FUJI,
  CLEO and Chain of Karma: DICTO.

Renders: none yet (to follow with a geometric cut of the sides).
