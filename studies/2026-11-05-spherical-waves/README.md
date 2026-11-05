# Spherical-wave imaging (DICTO 5 Nov 2026)
DICTO: "spherical wave patterns to help with imaging and reveal or close gaps"; first test on the cut-OG pyrochlore cell; "another tool alongside harmonics".
Method: every point of solid sends out j0(kr) = sin(kr)/(kr); field = solid * j0 on one periodic cubic cell (8 regular-triangle cut OGs, diamond network), FFT, grid 96^3.
Result (float): solid fraction 0.3772 (expected 0.3771). Dark = field below its median:
- wavelength a/2 (the network's own, a = cell side 12.369): dark covers 0.803 of the gaps and 0.000 of the solid -> the dark half lies wholly in gaps.
- a/4: 0.607 of gaps, 0.323 of solid; a/8: 0.567 / 0.389 (short waves ripple inside the solid).
Figures: wave-slices.png (labelled), wave-clean.png (DICTO: dataless simplified version). Scripts: wave_image.py, wave_slice.py, wave_clean.py.
Next: "close" = grow solid where the field is darkest (adaptor seeds); test on packings with unknown gaps.

## Unknown gaps: densest lattice packing of the cut OG (wave_lattice.py, wave_lattice_views.py; float; grids 48 and 72 agree)
Density 0.776244 (solid fraction on grid 0.7762). Wavelength = nearest-neighbour distance 1.2571: of the darkest 22.4% of space, 62.6% is gap
(0.8x: 66.6%; 1.25x: 61.8%) — weaker than the open pyrochlore cell (dense packing, thin gaps).
Critical points of the wave field per cell (read as in electron density): 1 atom, 5 bonds, 5 rings, 1 cage; Morse sum 1 − 5 + 5 − 1 = 0.
- One gap ROOM per copy (cage at fractional (1, ½, ½)); four window points per cell in the gap → each room opens through 8 windows: the gap is one connected network of rooms.
- 12 contacts per copy = 6 pairs: 5 read as bonds; the 6th pair (lattice direction b1 + b3) reads as a ring point inside the pieces — probably the 2 triangle-to-triangle contacts (to check).
Views inside the cell through the room: lattice-views.png.

## Closing the room (close_room.py, render_room_adaptor.py; float, manifold booleans)
Room centre = fractional (0, ½, ½) (grid index offset corrected), an inversion centre of the packing. Adaptor = Voronoi cell of the room-centre
lattice minus all cut-OG copies. Result: ONE solid, genus 0, volume 0.326555 = gap per copy exactly; adaptor copies overlap 0, overlap with the
cut OGs 0; cut OG (77.6%) + adaptor (22.4%) fill space, both by translation only. Adaptor / convex hull 0.307, sphericity 0.374.
Central symmetry about the room centre holds by the packing's symmetry (the vertex check failed on boolean mesh artefacts; corner filter to do).
Figure room-adaptor.png. Open: exact form, name (DICTO's), whether a flatter split (wave basins instead of Voronoi) gives a nicer piece.

## Growing rhombi into the room (DICTO: "together with harmonics, with growing golden or regular rhombi"; grow_rhombi.py, grow_rhombi2.py; float, voxels N=72)
Harmonics of the room (radius from the room centre): odd l all 0 (room symmetric through its centre); l=4 holds 0.50 of the non-round part (cubic tone), l=6 0.14, l=8 0.11, l=10 0.08.
Greedy growth, darkest wave points first. One size: golden 27/33/39% (edges 0.16/0.11/0.075), regular 20/29/37%.
Growing in phi-steps (edges 0.16, /phi, /phi^2, ...): golden 27 -> 42 -> 58 -> 78 -> 84%; regular 21 -> 37 -> 53 -> 68 -> 81%; golden + regular together 84.2% (regular adds almost nothing).
Golden beats regular although the room's tone is cubic (golden rhombohedra share the cut OG's five-fold directions). The smallest step (edge 0.023) is near the voxel size: treat the last step as rough.
Dehn: golden and regular rhombohedra have dihedral angles that are rational multiples of pi (Dehn 0); the room's adaptor has Dehn = −Dehn(cut OG) ≠ 0 (exact, Theorem 2 of Pentagons for the Kites) → rhombi can never fill the room exactly; the leftover slivers carry the Dehn invariant.

## Golden fill rendered, leftover traced (golden_fill.py, render_golden_fill.py; float, voxels N=72)
4377 golden rhombohedra in 5 phi-steps fill 83.7%. Leftover 0.0534 of 0.3266: 371 pieces, but ONE connected piece holds 93% (it runs through the
whole packing); 274 pieces of 1-2 voxels (grid dust) hold 2.5%. Skin test: 42% of the leftover lies within 1 voxel of the cut-OG surface
(19% of all gap does), 58% within 2 (37%), 73% within 3 (58%). So the leftover = a skin on the cut-OG walls + a web through the room centre
where rhombi grown from different seeds meet (grain boundaries, the cross in the picture). Next: grow ONE coherent golden grain (a patch of
an icosahedral rhombohedral tiling, cut-and-project) to remove the grain boundaries; what remains is then the skin that carries the Dehn invariant.
Figure: golden-fill.png.

## The room completed (complete_room2.py; float, manifold booleans)
One coherent golden tiling (de Bruijn dual grid on the cut OG's six five-fold axes), 3 phi-steps (tile edges 0.100, 0.062, 0.038), tiles kept only
when wholly inside the room (checked one by one) and clear of every kept tile (checked pair by pair: 0 overlaps; the all-at-once union of
1055 face-sharing tiles loses 0.05% to the boolean tool, so it is not used for accounting).
COMPLETE: room 0.326554827 = 1055 whole golden rhombohedra (0.125707) + 12172 golden rhombohedra of the finest step trimmed by the cut-OG walls
and the room faces (0.200871); sum 0.326578, diff 2.4e-05 (7e-5 relative, float accumulation over 12k pieces).
Every piece is a golden rhombohedron, whole or trimmed; only the trimmed ones carry the Dehn invariant. Trimmed pieces hold 61.5% of the room
at this depth (coarse tiles may not cross the room faces). Practical kit not yet: too many trimmed pieces; deeper steps and tiles crossing room
faces would raise the whole share.

## Bull-horns basis (DICTO 5 Nov: "how about using bullhorns as basis"; bh_golden.py)
Room = the Bull-horns OG adaptor rebuilt from its definition (Voronoi cell of the hole among all holes minus the 6 OGs): volume 0.111898 = published.
(The stored mesh bh-full.json is rounded to 6 decimals; on import the boolean tool re-joins nearly flat triangles and gains 0.4% → always rebuild.)
One coherent golden tiling on the OG's five-fold axes, 3 phi-steps (edges 0.080, 0.049, 0.031): 994 whole golden rhombohedra = 48.7% of the
adaptor; 7473 trimmed = 51.3%; sum = adaptor within 7e-5 (float). Deeper run (5 steps) on DBB: bh-golden-5.log.
