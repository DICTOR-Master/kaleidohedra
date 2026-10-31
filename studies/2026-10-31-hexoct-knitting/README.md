# HexOct as a knitted pattern: one exact 4H slice and its chart (31 October 2026)

## The idea (DICTO, 31 Oct 2026)

The HexOct structure read as a knitted pattern. The knitted fabric is an exact edge-on slice through a close-packed
stacking: stitch = ball, row(s) = layer; the layer positions A, B, C appear in the slice as lateral offsets 0, 1/3, 2/3 of
the repeat. The knitting places each layer by bias shifting (decrease at one end, increase at the other, so the row moves
one stitch sideways; one layer step = 1/3 repeat): a c layer shifts the same way as the step before, an h layer shifts
back, so cubic knits as a straight bias slant and hexagonal as a chevron. Colour = the pieces themselves: every area of
the slice is coloured by the HexOct piece it belongs to; by DICTO's Rule of Halves (#57) each piece is two halves, the
half nearer layer k belongs to layer k and takes its colour, gold for a c layer, blue for an h layer; tetrahedral pieces
darker, octahedral lighter (book colours). This study checks ONE chart (4H) before any full pattern.

## Method (`scripts/knit.py`, run on dicto-big-brother)

- Ball spacing a = 1, layer spacing h = √(2/3). Exact integer coordinates x = X/2, y = Y·√3/6, z = Z·h; A sites
  (2m+n, 3n), B = A + (1,1), C = A + (2,2). All slice polygons computed with Fractions in (S, Z), S = −Y (unit √3/6).
- Pieces: the classical Delaunay cells of the close packing (= HexOct pieces at λ = −1/8, as in the ring builds): in each
  gap up-tetrahedra (base in the lower layer), down-tetrahedra, octahedra. Slice of a convex piece = hull of the points
  where its vertex-to-vertex segments meet the plane; each slice polygon cut at the gap mid-plane Z = g + 1/2.
- Check: the halves cover the window (2 repeats × 8 gaps) exactly once (area 96 = 96, exact).
- Stacking 4H = ABCB, layers A B C B A B C B A (two periods); A and C are h, B is c.
- `CATALOGUE=1` also writes `out/pieces-in-slice.json` (whole pieces and halves, exact corners, sides, angles).

## Plane

x = 0: the plane perpendicular to a close-packed row, i.e. a {11-20} plane (seen along ⟨11-20⟩, rows end-on); it
contains the stacking axis and the [1-100] direction. Lateral repeat in the slice = √3 (not √3/2 as in the projection).
On this plane every layer has exactly one ball centre per repeat: A at 0, B at 1/3, C at 2/3 of the repeat (exact). All
other ball centres lie at distance 1/2 = the ball radius from the plane, so those balls only touch it at one point. So in
the slice each layer shows one great-circle disk per repeat: one ball = one stitch per layer per repeat, consistent.
Neighbouring on-plane balls of adjacent layers are 1 apart (they touch), and that contact segment is a tetrahedron edge.

## Exact results: what the pieces cut (lengths in units of a)

- Tetrahedron: the plane contains one edge (joining two touching on-plane balls of adjacent layers) and the midpoint of
  the opposite edge: an isosceles triangle, sides 1, √3/2, √3/2, angles 54.74°, 54.74°, 70.53° (arccos 1/3).
  Halves: the apex side is a small triangle (1/2, √3/4, √3/4); the base side a trapezoid (√3/2 along the layer,
  sides √3/2, √3/4, 1/2, √3/4 in order, 1/2 lying in the mid-plane; angles 54.74°, 70.53°, 109.47°, 125.26°).
- Octahedron: a rhombus of side √3/2, angles 70.53°/109.47°, with two sides lying in the layer planes.
  Halves: two congruent parallelograms, sides √3/2 (in layer / mid-plane) and √3/4.
- Reading the slice (`out/slice-4H.png`): at an h layer the colours mirror across the layer line: dark meets dark
  (tetrahedra base to base), light meets light; at a c layer dark meets light (tetrahedron meets octahedron). Every
  c/h gap holds pieces whose two halves differ in hue (gold half + blue half): the Janus pieces.

## Chart (`out/chart-4H.png`)

- Gauge: k = 4 → repeat = 12 stitches, r = 7 rows per layer, stitch 5 wide : 4 tall. True ratio repeat/layer =
  √3/√(2/3) = 2.1213; chart gives 12·1.25/7 = 2.1429 (1.0 % wide). Ball row of layer k = row 7k + 1 (1-based); the
  mid-plane falls on a row boundary, so halves split cleanly between rows.
- Bias: 4 bias rows per gap (one stitch each = 1/3 repeat), at gap rows 2, 3, 5, 6 (symmetric about the mid-plane).
  The chart is in fabric coordinates: true position = chart column + cumulative shift (printed at the right); every
  ball stitch then sits in chart columns 1 and 13. Shift pattern R R R R / L L L L … : A→B→C right, C→B→A left.
- Each cell takes the colour by area majority over 4 × 4 sample points; 116 of 1368 cells were exact ties (mostly ball
  rows, where the cell is half the piece above, half below, both the same layer's hue) and were given the darker
  (tetrahedral) shade. This is a choice; the other choice changes shade only, never hue.
- Colours a knitter needs: 4 (gold dark, gold light, blue dark, blue light); ball stitches are marked by a symbol
  (e.g. a bobble or duplicate stitch) rather than a fifth colour. Counts in the chart: blue dark 358, blue light 338,
  gold dark 384, gold light 288 stitches.

## Uncertain / to check with DICTO

- Whether the knitted bias shift can really be read as "true position = column + shift" for this gauge (one stitch per
  bias row, 4 bias rows out of 7); a swatch would show it.
- Tie rule for the ball rows (dark shade) as above.

## Conclusion and status

Conclusion: on the {11-20} plane the 4H slice is made of tetrahedron triangles (1, √3/2, √3/2) and octahedron rhombi
(side √3/2), cut at mid-planes into small triangles + trapezoids and parallelograms; at k = 4, r = 7 it becomes a 24 × 57
four-colour chart with bias rows R/L.
Status: done, exact; one chart awaiting DICTO's check. No other stackings, no full pattern.

## Files

`scripts/knit.py`; `out/slice-4H.png`, `out/chart-4H.png`, `out/slice-4H.json` (shapes incl. window-cut pieces, gauge,
shift per row), `out/pieces-in-slice.json`, `out/run.log`. Copies: ~/Documents/papers-to-read/knit-slice-4H.png,
knit-chart-4H.png.
