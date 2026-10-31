# Queen Geodes (2026-10-31)

DICTO's idea: the shells of both Queens look like crystal geodes. Drawn here two ways for each Queen:
(1) a split geode, (2) a da Vinci sheet: part sepia line drawing in Leonardo's skeletal *vacuus* manner (his polyhedra for
Pacioli's *De Divina Proportione*), part filled.

**Conclusion (round 2):** the pale gem crystals now stand out against the dark basalt rind, and the gold core stands up out of the one-tone crystal section in the da Vinci sheets. **Round 1:** both Queens read as geodes once the cut plane is turned off the five-fold axis and the innermost shells are left out as the hollow. The da Vinci sheets read once the filled part is cut open and the line cells in front of the cut are dropped.
**Status:** round 2 (DICTO: stand out more, pale translucent sparkly, core alone in 3D) rendered; four pictures + 2×2 sheet delivered to `~/Documents/papers-to-read/` for DICTO to look at; not used in any paper yet.

## What was drawn
- **White Queen**: the 600-cell round v = (2,0,0,0) in perspective from an eye at height −21/10, the 15 Cleo shells (as the book plates).
  Shell 14 (round −v) wraps the whole picture in this projection and is never drawn.
- **Red Queen**: the 120 dodecahedra (corners = the White Queen's cell centres), 9 layers. Layers 7 and 8 are huge in this
  projection and are never drawn.
- Colours: round 1 as the book (viridis, core gold); then diamond / ruby gems (DICTO); round 2 pale gems, see below.

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

## Round 2 (DICTO 2026-10-31: "stand out more ... core cells alone in 3D ... pale translucent sparkly")
- **Geode rind**: basalt, deep blue-black grey (#2f343e / #343a44 outside), cut face a slightly lighter polished band (#565e6b / #5e6673);
  matt stone shading, near-black edges.
- **Geode crystals**: pale. Diamond near-white #f7fafd to faint ice-blue #c3d6e8 outwards; ruby pale rose #ffd3dd to clear pink-red
  #e2456a outwards. Gem shading: soft body light plus a mirror highlight (half-vector of light and view, exponent 40, plus a broad
  sheen) that flashes the faces facing the mirror direction to near-white.
- **Translucency**: the edges of the crystal cells behind the visible crystal faces are drawn thin (1.1 px) in white at 42 % opacity,
  only where the face in front is crystal and no deeper than 160 px behind it (deeper ones would clutter).
- **Glints**: crisp four-pointed stars (white, thin ice-blue / rose outline) at the brightest visible crystal corners (brightness = the
  strongest highlight among the corner's faces), at least 4.5 % of the picture apart, only where the corner sits mostly on crystal.
  The White geode gets 12, the Red 23 (the White cavity shows fewer separate bright corners at that spacing).
- **da Vinci**: the core cells alone drawn whole, solid gold: the White Queen's 20 core tetrahedra (Cleo-Icos), the Red Queen's core
  dodecahedron **whole** (it is one cell; splitting it into 12 pentagonal pyramids would draw lines that are not cell edges).
  The other filled shells (White 1-6, Red 1-3) all one pale crystal tone (White #dbe7f2, Red #f3b7c6), cut faces light (#f6f9fc /
  #fce4ea), gem shading, hidden edges faintly through (sepia, 28 %), 16 glints each.
- **da Vinci cut** turned to face mostly up (normal = 0.7 towards viewer + 0.3 right + 1.0 up) so the gold core stands up out of
  the cut plane; the line cells kept are now the far half (centre behind the plane through the centre facing the viewer), so the
  cage frames the section from behind and nothing is drawn over the cut. White: line shells 7 and 8 (DICTO), Red: layer 4.

## Unsure
- The geodes have no gold core: the hollow takes it out (the core is in the da Vinci sheets).
- Round 2: the White geode has 12 glints, not a few dozen; more would need closer spacing (busier).
- Round 2: on the parchment the diamond-pale section is close to the paper tone; it reads by its sepia edges and the cooler white.
- The sheet is 1798 × 1984 px to stay ≤ 2000 px. The single pictures are 2000 px square.
