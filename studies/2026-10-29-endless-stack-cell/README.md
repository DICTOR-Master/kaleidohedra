# Endless Stack Cell (placeholder name) — DICTO's idea, 29 Oct 2026
Idea (DICTO, from a dream): the Janus c/h halves of #57 behave like the EKP network: one set fills one unit, joins across neighbouring units, cycling without end.
Conjecture to test: the slab round layer k (top halves of gap k−1's octahedral pieces, bottom halves of gap k's, tetrahedral pieces nearest layer k) is fixed by layer k's type alone (#57 theorem), so every close-packed stacking is a string of two layer tiles, c-tile and h-tile, along the whole weight walk.
Open check: do tetrahedral pieces cross the octahedral cut planes? If yes the tile faces are not flat but interlock (EKP-like).
## Prior art checked (29 Oct)
Library (ask-library, 4 queries): Gabbrielli–Jiao–Torquato 2012 PRE 86 041141 (tet/oct tilings; sliding along planes gives nonperiodic ones; read p.1–4); Lalvani 1990 NASA TM-102635 (octet unit cell = rhombohedron, 2 tet + 1 oct; layered sections; read p.5–6); Wikipedia tetrahedral-octahedral honeycomb; Kallus–Elser–Gravel 2009, Torquato–Jiao 2009, Kramer 1982, Smith et al. 2023 hat, Tsiokos 2026 (hits, not relevant: packings/aperiodic monotiles).
Web: OD theory (Dornberger-Schiff & Grell-Niemann 1961; IUCr B 2025 dk5140; vicinity condition) — layers as building units with local stacking rules: the closest frame, credit it. arXiv 1407.0692 (fcc/hcp split between layers into tet/oct by triangle). Radical-Voronoi interstitial work (arXiv 2010.01354; Sci Data 2020 CAVD): no layer tiles of hole pieces.
Own: #57 (rule of halves), book The Laws of Stacking: no layer-tile statement found.
Verdict: layer-units framework known (OD theory); two layer tiles of the halves for all stackings and all λ not found.
## Result (29 Oct, dicto-big-brother, scripts/tiles.py → tiles.out)
Exact, 32 five-layer contexts (types of layers L−2..L+2 fix the tile: its two gaps depend on layers L−3..L+3, #57 Step 1) × 10 sample λ = 320 cases.
- One motion per tile: 320/320 — the whole tile (4 pieces) is carried onto the pure c-tile (ABC) or h-tile (AB) by one lattice symmetry about the layer's ball, z kept. So every close-packed stacking = a string of two tiles.
- Joint: the octahedral section on the cut plane is one shape at each λ, shared by c and h — any tile sits on any tile.
- Flat faces only at the low end (λ = −7/16, −5/12); from λ = −1/4 up the tetrahedral pieces cross the cut planes (to ±5/8 at −1/4, ±13/16 at −3/16, ±1 = the next ball's height for λ ≥ −1/16): tiles interlock. Switch point to pin (expect a stop, −3/8).
Status: holds at sample λ; stretch-by-stretch proof not yet run. Picture: tiles_1_10.png.
## Proof (29 Oct, scripts/prove.py → prove.out)
All 32 contexts, whole walk −11/24 ≤ λ ≤ 3/8: on every sub-interval between breakpoints (of the tile's 4 cells and the pure tile's) the tile, mapped by one lattice symmetry, equals the pure tile as identical rational functions of λ (sympy); at every breakpoint exactly. 32/32 PASS, no failures.
Flat/interlock switch: λ = −7/24 exactly, the same for c and h tiles: for λ ≤ −7/24 the tiles meet on flat planes (the octahedral cut planes); for λ > −7/24 the tetrahedral pieces cross into the next layer. Not a stop of the walk.
STATUS: theorem proved (exact) — "Two-Tile Theorem" (placeholder). Conclusion: every close-packed stacking at every weight is a string of two layer tiles; any tile sits on any tile; flat below λ = −7/24, interlocking above.
## Test print (29 Oct, scripts/make_slabs.py → print/)
c-slab (layer 0) and h-slab (layer 1) of ABAC at λ = 1/10, 15 mm per ball spacing, cut by one vertical hexagonal prism (circumradius 39 mm) so they mate: hexagonal bricks 78 × 67.5 × 24.5 mm, each one watertight body (genus 0), c 49.2 cm³, h 47.7 cm³. Exact fit = zero clearance: print with slicer horizontal expansion about −0.1 mm and supports (both faces toothed).
