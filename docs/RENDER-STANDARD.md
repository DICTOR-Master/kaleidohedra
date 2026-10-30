# Render standard (DICTO, 2026-10-30)

DICTO: "we have to have general standards laid down; this can't afford to happen again" — after the White and Red Queen worlds
were drawn with far less definition than the Polyhedraverse Kepler–Poinsot stars.

**Reference:** the Polyhedraverse door's Kepler–Poinsot stars (world-poly.js). Every 3D world must reach that definition.

1. **Solid by default.** Opaque `MeshStandardMaterial`, `flatShading`, `polygonOffset` (factor 1, units 1) so edges sit on the faces.
   See-through glass is an option the viewer can choose, never the only view of a solid.
2. **Crisp edges.** Antialiased screen-space lines (`LineSegments2` + `LineMaterial`, three/examples/jsm/lines), width ≥ 1.5 px
   (scaled by the device pixel ratio), never 1-px `LineBasicMaterial` hairlines for the main edges. Outline (hull) edges at full
   opacity; inner edges, when shown, shaded by depth (near bright, far dim) rather than a flat low opacity.
3. **No haze.** No milky emissive washes on faces or glass; glass opacity chosen so the faces still read as facets.
4. **Light.** The app's key + fill lights; metal surfaces get an environment map for reflections.
5. **Resolution.** Renderer pixel ratio follows the device (render.js quality settings); never below 1 × devicePixelRatio on "high".
6. **Compare before shipping.** Each new or changed world is screenshotted on dicto-node beside the reference star at the same size,
   the pictures are looked at, and only then is "into the deploy queue?" asked.
7. **Audit.** Existing worlds are checked against this list; shortfalls are logged in open-work and fixed one by one.

Applies also to figures made for papers and books (sharp edges, solid faces unless glass is the point, no haze).
