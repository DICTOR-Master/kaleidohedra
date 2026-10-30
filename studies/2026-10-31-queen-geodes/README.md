# Queen Geodes (2026-10-31)

DICTO's idea: the shells of both Queens look like crystal geodes. Drawn here two ways for each Queen:
(1) a split geode, (2) a da Vinci sheet: part sepia line drawing in Leonardo's skeletal *vacuus* manner (his polyhedra for
Pacioli's *De Divina Proportione*), part filled.

**Conclusion:** both Queens read as geodes once the cut plane is turned off the five-fold axis and the innermost shells are left out as the hollow. The da Vinci sheets read once the filled part is cut open and the line cells in front of the cut are dropped.
**Status:** four pictures + 2×2 sheet done, delivered to `~/Documents/papers-to-read/` for DICTO to look at; not used in any paper yet.

## What was drawn
- **White Queen**: the 600-cell round v = (2,0,0,0) in perspective from an eye at height −21/10, the 15 Cleo shells (as the book plates).
  Shell 14 (round −v) wraps the whole picture in this projection and is never drawn.
- **Red Queen**: the 120 dodecahedra (corners = the White Queen's cell centres), 9 layers. Layers 7 and 8 are huge in this
  projection and are never drawn.
- Colours as the book: viridis 0.15–0.95 over the shells/layers, core gold.

## How
`scripts/queen_geodes.py` (geometry and z-buffer renderer copied from `papers/book-queens/plates/render_plates.py`, which runs its
argv at import), `scripts/run.sh` (copies the script to dicto-big-brother, renders there in the foreground, fetches `out/`).
Inputs on dicto-big-brother: `~/kres-tmp/4d/data/600cell-source.json` (same md5 as `studies/2026-10-27-white-queen-600/data/600cell-source.json`),
`~/kres-tmp/alicia-plates/dicto-logo.png`. Renderer additions: exact convex clipping of cells by a plane (hull of the corners
behind the plane and the edge crossings, cut face flagged), per-edge colour, depth-graded line width, parchment ground, caption, sheet.
Counts drawn are in `out/geodes.json`.

## Choices
| | Geode | da Vinci |
|---|---|---|
| White | rind = shells 10, 9 (clipped at the cut); crystals = shells 3–8, kept whole if wholly below the cut; shells 0–2 left out (the hollow); shells 11–13 not drawn | lines = shell 7 (30 of 60 cells: those behind the cut); filled = shells 0–6, cut open |
| Red | rind = layer 4; crystals = layers 1–3; layer 0 left out (the hollow) | lines = layer 4 (15 of 30 cells); filled = layers 0–3, cut open |

- **Geode cut**: a plane through the centre whose normal is the five-fold axis of the core turned by 17°. Cut square to the
  five-fold axis, the plane runs along cell faces, so the "cut" is only whole faces and the cavity is flat. Turned 17°, it makes true cuts.
- **Geode view**: 50° from the cut normal (the half geode seen from above at 40° over its cut face). Rind outside warm grey stone,
  cut faces lighter polished stone (two/three bands, one per rind shell), crystals solid in shell colours, edges 2 px dark (as the plates).
- **Hollow**: with every shell kept, the cut face was a flat mosaic. Leaving out the innermost shells gives the cavity, and
  the remaining shells' faces point inwards like crystals. So the gold core is **not** in the geodes (it is in the da Vinci sheets).
- **da Vinci view**: orthographic, five-fold axis up, elevation arctan(1/√2) = 35.26° (the isometric elevation). The filled part is cut by a plane through
  the centre (normal = view direction + 0.85 right + 0.45 up) so the nested bands show (gold core, then the viridis shells). Washes =
  64% shell colour + 36% parchment, gentle light. Line cells with centre in front of that plane are dropped; the rest drawn whole in sepia
  (#5b3a1e), 3.4 px near → 1.5 px far, hidden where the filled part is in front. Clean geometric lines, no wobble.
- Tried and rejected: White geode cut square to the five-fold axis (flat); a floor sunk 0.15R below the cut (took out the core and most inner crystals);
  Red rind of layers 4+5 (cut band too wide, cavity small); da Vinci with an uncut filled ball (only the outer shell visible, all one tone);
  all line cells kept (lines drawn over the cut face); Red lines = layer 3 only (sparse, lopsided).

## Unsure
- The geodes have no gold core: the hollow takes it out.
- The da Vinci cut face is seen nearly face-on, so the filled part reads more as a cut section than as a solid.
- The sheet is 1798 × 1984 px to stay ≤ 2000 px. The single pictures are 2000 px square.
