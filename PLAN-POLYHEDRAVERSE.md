# Step D: Polyhedraverse rewritten into the joined app

DICTO, 2026-10-08: "step D next". Polyhedraverse (today a Next.js/React site, ~11,500 lines, repo
`polyhedraverse`) is rebuilt in the joined app's own plain JavaScript, as a third app beside
Kaleidohedra and Rhombiverse: same 3D scene, same controls, same DICTO, its own space in green.
Then polyhedraverse.vercel.app becomes the third front door of this repo.

## Decisions (DICTO, 2026-10-08)

- **Full rewrite** into the joined app (not a bundled React island).
- **Code moves into this repo**; the `polyhedraverse` repo becomes history only (like `rhombiverse`).
- **Saves stay per door**: polyhedraverse.vercel.app keeps reading its own saved build (same storage
  key); from the other two doors Polyhedraverse starts empty. Export/Import moves builds between them.
- **Welcome**: the shared one, with Polyhedraverse's turning **dodecahedron** in green.
- **DICTO list**: **3D** and **4D**, then the families (3D: its families as turning wireframes;
  4D: the 4D Polytopes and RCP-C2B). Picking a family opens the shape browser on it.
- **Everything carries over**: face / vertex (+ twist) / duoprism attach, Transform to…, Delete;
  4D RCP-C2B and the star, radial-projection and duoprism viewers; Compare, Favourites, Recent,
  Scene; running build name, Golden helper bar, Nets with fold slider and A4 PDF.
- **Controls are the joined app's**: World View (Solid / Translucent / Skeleton, as P has now),
  Colour + Paint, Undo (hold to scrub), autosave, Settings → Export / Import World, tools column.
  Polyhedraverse's header goes.
- **Attach flow**: Polyhedraverse's steps in the joined app's look: tap a face or vertex → Attach… →
  the shape browser shows only shapes that fit (partners first) → pick → drag to cycle its turns →
  Confirm.
- **View tools in its space**: Spherical (◯) yes. (Answer read as "Spherical; it has World View
  already"; X-Ray, Section and Duality hidden there unless DICTO says otherwise.)
- **Colours**: one setting for all apps: app colour (cyan / orange / green) / Type (Polyhedraverse's
  family colours there) / Pick, with Paint.
- **Switchover**: the Next.js site keeps serving polyhedraverse.vercel.app until the rewrite does
  everything above; then DICTO re-points that Vercel project here (`SITE=polyhedraverse`).

## How it fits

- Polyhedraverse's space is one more own-3D world (`src/app/poly/`), like Sunstar or EKP: it registers
  snapshot/restore with undo and autosave, follows World View, colours and Paint, and draws in the
  shared renderer and camera. Its 4D builds are a second world in the 4D tier.
- The pure logic is not rewritten by hand where it is already plain maths: P's `app/lib` (assembly
  graph, face attach and registration, build naming, face kinds, piece colours, golden builds,
  ~2,700 lines of TypeScript) moves into **krp-core** as JS + `.d.ts`, like the polyhedra geometry in
  v0.6.0. The old Next.js site switches to it too, so both run the same code until switchover and the
  new world can be checked against the old one shape by shape.
- The UI is rewritten: `ShapeViewer.tsx` (3D placement, picking, drag-to-cycle, RCP-C2B) becomes the
  world's own scene code; the React shape browser and its screens become plain DOM, in the DICTO
  wizard's style.
- `site.js`: Polyhedraverse gets `inside: true`; its theme already exists (green).

## Stages

Each stage ships on its own (commit, push, CI, changelog when user-facing) and is checked on
dicto-node, phone first. Until D6 the new space is reached from DICTO in the other two doors.

1. **D1 Core.** P's `app/lib` logic into krp-core (new minor version); the Next.js site switches to
   it; all 312 shapes and P's checks identical.
2. **D2 Space.** Polyhedraverse inside DICTO: 3D / 4D cards, families with wireframes; its world:
   start with a shape, World View, colours (app colour / Type / Pick) and Paint, Spherical, undo,
   autosave, Export/Import; the welcome's dodecahedron.
3. **D3 Building.** Selecting faces and vertices; face attach (all matching faces × turns, drag to
   cycle, best fits first), vertex attach with twist, duoprism attach, Transform to…, Delete; running
   build name; Golden helper bar.
4. **D4 Shape browser.** Home (families, Recent, Favourites), Search (name, family, face shape,
   face count), Scene, Favourites, Full Catalog with its sections and pairs; details (stats, preview,
   Add to Scene, Favourite, Compare, Net + PDF, star / radial / duoprism viewers, View 4D); Compare;
   the fit-filtered attach mode.
5. **D5 4D.** RCP-C2B (next cell / shell, remove, Open / Closed, RCP-Coordinates, shell colours) and
   the 4D Polytopes with Build.
6. **D6 Front door.** `site/polyhedraverse/` (head, changelog, icons), the Polyhedraverse chapter of
   the DICTO guide (from its 7-language guide), its Playwright specs ported to this repo, a
   `SITE=polyhedraverse` build; DICTO re-points the Vercel project; the old repo's README points here.

## Open (ask before the stage that needs it)

- D3: on a phone, how a face vs a vertex is selected when they're close (P uses hover tooltips on
  desktop).
- D4: the browser as a full-screen overlay (as now) or a panel beside the scene on wide screens.
- D6: whether the old Next.js code is deleted from the `polyhedraverse` repo or the repo is left as is
  with a pointer README.
