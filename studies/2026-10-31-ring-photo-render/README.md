# Photo-real ring renders, first test (31 October 2026)

DICTO's idea: combine his photos of real PET-bottle-cap security rings with the exact ring models, so a ring build can be
seen as it would look before it is built. First test on one photo (three big triangles of 4 tied rings, top view, on tatami).

**Privacy:** the photo is DICTO's own and private. It, the cut-outs, the renders and the sheet live only in
`~/Documents/ring-photos/` (derived files in `derived/`), `~/Documents/papers-to-read/ring-photo-test.png` and on
dicto-big-brother `~/kres-tmp/ringphoto/`. This folder holds the scripts only; no image made from the photo may be added here.

## Method

1. `scripts/cutout.py` — white plastic vs tatami (low saturation, brightness against a blurred background), morphological
   clean-up; the 12 open ring centres are the holes of the white mask; a watershed from the holes splits touching rings;
   tatami streaks removed by an opening; three rounded tips per ring from the polar outline; RGBA cut-out per ring rotated
   one tip up; six zip-tie patches cut across tied sides (tie centres picked by eye on a 3x zoom); `cutouts.json`.
2. `scripts/render.py` — ring triangles of (a) one big triangle, (b) a regular tetrahedron of edge 1 (16 rings), (c) the
   HexOct h-tile at λ = −1/8 (48 rings, exact faces from studies/2026-10-31-hexoct-ring-build). Each cut-out is mapped by
   its tips (affine; orthographic view), then pulled 45 % of the way to the model's rounded triangle. The band is a conical
   height field (distance from the outer outline → wide rim to narrow rim, ±h/2 along the face normal, h = 0.13 side,
   assumed), rendered as dense points with a supersampled z-buffer. Central ring of each 4-ring face turned over (DICTO):
   corner rings wide rim outside, central rings narrow rim outside, central cut-outs on central positions; a ring seen
   from inside uses a cut-out of the other kind, mirrored. On h-tile faces the minority grid orientation counts as central.
   Shading by face normal (interior dimmer), zip-tie patches folded over shared sides, ground shadow along the light.
3. `scripts/sheet.py` — comparison sheet with the DICTO mark.

Run on dicto-big-brother (env vars in each script header).

## Findings

- Segmentation: all 12 rings found and split cleanly (12 holes, 10.4k–12.4k px each). Cut-outs clean on 8 of 12; ring 5
  keeps tatami threads on one side, ring 6 has tatami inside its band, ring 3 a little fringe. Renders use the 8 clean
  corner rings and central rings 1 and 9.
- The two sides: central rings (turned over) look about 2 % larger, more triangular (side-midpoint / tip radius 0.72 vs
  0.80: tipfrac 0.69 vs 0.63) and slightly brighter (V 0.835 vs 0.820); apparent band width the same (23.5 vs 23.1 px). A
  top view cannot show which rim is wide; the renders assume corner rings lie wide rim up.
- Fake: edge-on bands (stretched top view, streaky; band height assumed), inside of each ring is a top-view photo, ties are
  flat decals and drawn at 0.32/0.68 of a side (rings still bow away at 1/4, 3/4), no translucency or bounce light.

## Conclusion and status

Conclusion: photo cut-outs on the exact ring triangles already read as a real ring build in top and three-quarter views;
side photos are needed for the band walls. Status: first test done; awaiting DICTO's look and the side-view photos.
