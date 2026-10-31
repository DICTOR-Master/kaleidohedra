# 3D ring renders calibrated to DICTO's photos (31 October 2026)

DICTO's idea: a photo-real render of his PET-bottle-cap security-ring builds (rings pulled into rounded triangles, tied at
two points per side with small clear zip ties; double scale: 4 rings per unit triangle, the central ring turned over),
checked against his photos of the first finished piece, the double tetrahedral pyramid (triangular bipyramid, 24 rings).

**Privacy:** the photos are DICTO's own and private. They, the photo/render sheets and every image made from them live only
in `~/Documents/ring-photos/`, `~/Documents/papers-to-read/` and on dicto-big-brother `~/kres-tmp/ring3d/`. This folder holds
code and the look settings only.

## Method

Renderer: **Blender 5.0.1, Cycles (CPU, 24 threads) on dicto-big-brother** (real subsurface scattering and transmission;
the apt build has no denoiser, so 400 samples with indirect clamp 2).

1. `scripts/ringmesh.py` — true 3D mesh of every ring: rounded-triangle centreline in the face plane (straight parts on the
   ring triangle's sides, where neighbours touch), swept across by the band height along a band direction, with wall
   thickness on the ring's inner side. Band direction = face normal tilted about the centreline: on sides inside a face by
   the cone angle (+ for corner rings, − for the turned-over central ring, so the touching walls stay parallel); on sides
   along an edge of the solid the band turns into the bisector plane of the two faces, so the two bands lie face to face;
   blended smoothly through each rounded corner (this gives the twisted bands seen at the solid's edges and vertices).
   Nine inner tabs per ring (one at each side midpoint, equally spaced), hinged at the narrow rim, standing square to the
   face. Zip ties: a strap loop around both walls at the two tie points of every shared side, square head on the outside.
   Open variant: no central rings, one more tie around the two touching tips at each big-edge midpoint. Output OBJ in metres.
2. `scripts/htile_rings.py` — the 48 ring triangles of the HexOct h-tile at λ = −1/8 (exact faces of
   studies/2026-10-31-hexoct-ring-build); on each face the minority ring orientation counts as 'central'.
3. `scripts/fitcam.py` — camera fit from the outline only: white plastic vs wood (saturation, brightness) → convex hull;
   model hull projected with a pinhole camera; IoU of hulls maximised. Final mode `REST=`: the model rests on one support of
   the bipyramid (face, edge or vertex), the phone is held upright (roll penalised); free: camera azimuth, elevation,
   position, focal length; the support with the best IoU is kept. (A free 6-dof fit matched the outline as well but stood
   the model on a vertex or tilted the table; the resting fit fixed that.) `overlay.py` draws the fitted edges on a photo.
4. `scripts/scene.py` — Cycles scene: OBJ, PET material (white, roughness 0.4, subsurface 0.4 with radius ~1.2 mm), nylon
   ties (translucent, transmission 0.45), procedural wood table (streak noise), warm disk area light (window) + cool world
   fill, AgX medium-high contrast. `scripts/run.py` builds the specs from `look.json`; `scripts/mkcam.py` makes a camera for
   a model without a photo (h-tile); `scripts/sheet.py` makes the photo/render sheet and puts the DICTO mark on renders.

Run (dicto-big-brother, `~/kres-tmp/ring3d`): `ringmesh.py bipyramid bip.obj`; `REST=0,8,6,15,18 FROMX=camN.old.json
fitcam.py photo.jpg bip.obj camN_rest.json`; `run.py look.json 1 2 3 clean open htile`; `sheet.py ...`.

## Measured parameters (units of the ring side s ≈ 40 mm)

| parameter | value | source |
|---|---|---|
| band height h | 0.12–0.14 measured, **0.16 used** | ring standing on edge (side photos a, b: band ≈ 70 px against a standing height ≈ 0.69 s ≈ 415 px); raised to 0.16 because the bands looked too thin beside photos 1–3 (DICTO's estimate 0.20 is above both) |
| cone (radial step between rims) | **0.10** (≈ 32°) | top view of flat rings (nets photo): white annulus ≈ 0.135 s wide; minus wall |
| which rim is wide | wide rim outside on corner rings, inside on central rings | my choice: a top view cannot tell, the side photos are not sharp enough |
| corner radius of centreline | **0.20** (0.07 at tied tips, open variant) | nets photo: side-midpoint / tip radius ≈ 0.72–0.80 |
| wall thickness | 0.016 | ~0.6 mm |
| inner tabs | 9 per ring (3 per side), 0.11 long, 0.6 h tall, 0.012 thick, hinged at the narrow rim | nets photo and photo 3 close-up |
| ties | at 0.32 and 0.68 of each side (1/4, 3/4 would sit on the rounded corners); strap 0.05 × 0.014; head 0.075 × 0.08 × 0.055 | photo 3 close-up |
| perimeter check | 3 s − 4.11 r = 2.18 s ≈ 87 mm for s = 40 mm | ring of ~28 mm diameter |

Camera fits (hull IoU): photo 1 rest on a face, elevation 52°, IoU 0.970; photo 2 rest on a face, elevation 47°, IoU 0.971;
photo 3 rest on an apex edge, elevation 48°, IoU 0.977.

## Findings

- The outline of all three views is matched to IoU 0.97–0.98 by the exact bipyramid geometry with bands of 0.16 s.
- The twisted bands at the solid's edges come out of one rule (bands of neighbouring faces lie face to face in the bisector
  plane) and read like the white curved ribbons in the photos.
- Still different: the real piece is puffier (rings bulge outward between ties, faces are not flat, sides bow), its rings
  look rounder and larger relative to the holes; real tabs and ties are smaller and less regular; the render's wood is a
  procedural streak pattern, lighter and more even than the real table; residual render grain (no denoiser); the true
  rim orientation and the exact band height remain uncertain (0.12–0.16 s).
- Open variant (18 rings, 54 ties): each face becomes three corner rings around a large triangular window bounded by their
  straight inner sides; through the windows the far faces show, so the piece reads as a lighter lattice in which the
  six big triangles are outlined twice (window + edge).

## Conclusion and status

Conclusion: a true 3D ring model on the exact bipyramid, with the cameras fitted to DICTO's photos, reproduces the outline
and the twisted-band look; the remaining gap is the softness of the real rings (bulge, bow), not the geometry.
Status: done (round 5 of the look); renders in ~/Documents/papers-to-read (ring-render-vs-photo.png, ring-render-bipyramid.png,
ring-render-bipyramid-open.png, ring-render-htile.png), awaiting DICTO's look.
