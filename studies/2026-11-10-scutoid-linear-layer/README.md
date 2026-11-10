# Scutoid linear layer L (DICTO 6 Nov 2026, opened 10 Nov)
DICTO 6 Nov: "adapt it to a linear transition between octet and hexagonal and pentagonal prisms"; "a spherical skin version and a
linear layer version, both filling space"; S and L separate, connected projects (football search A the third, linked). 10 Nov:
"what happened to scutoids … disappeared from my desired projects?" → never started, re-listed; "yes open L".

**Construction (sketch, 10 Nov).** Bottom of a layer: hexagonal prisms. In every hexagon exactly one edge shrinks to a point going up
(brick pairing of neighbouring cells; the shrinking edges never touch), so at the middle level every cell is a PENTAGON (a
pentagonal-prism level) with four cells meeting at each shrunk point. Edges keep their three directions, so every side face of a
cell stays flat (trapezoids, and one triangle where the edge vanishes). Realised with exact closure (residual 3e-15), every kept edge
positive (0.19–0.77 of the hexagon edge). Figure: l-levels-sketch.png (scripts/levels.py).
**Found by hand (10 Nov):** above the middle, the points reopen across and cells get new neighbours; with the brick pairing half the
cells in a row end with 7 sides and half with 5 (each gains two or none), the classical scutoid mix, not hexagons everywhere.
All-hexagon tops need a pairing in which every cell sits at the tip of exactly one shrinking edge: open.
**Next:** (1) DICTO's read of the sketch; (2) search pairings for the all-hexagon top; (3) the octet start (triangles) in place of
hexagons; (4) 3D cells (prism + transition + prism), their volumes and the stacked space-fill.

## Step 3 (10 Nov, DICTO "scutoids?!"): free edge directions (scripts/free_dirs.py)
Least squares on a periodic 4 x 4 patch, bottom and middle corners free, conditions: paired edges collapse, every other edge parallel
between the levels (flat trapezoid side faces), convex cells, edge floors. Every start stalls at the same violation 1.25 = the floor
penalty of a BOTTOM edge forced towards zero: to keep all side faces flat the solver must collapse an edge that is not paired.
Same obstruction as the three-direction LP. **Conjecture: with hexagons again at the top (double-row pairing) the side faces cannot all
be flat, for any edge directions.** (Search evidence, not a proof; a proof would go through the cycle space of the parallel conditions.)
**The choice for DICTO:** (a) the brick pairing: every side face flat (exact polyhedral cells), top a mix of 5- and 7-sided cells (the
classic scutoid mix); (b) the double-row pairing: hexagons everywhere at the top, side faces bent (as in living scutoids, whose faces
are curved). Either gives a space-filling layer stack.

## Step 4: the geometric scutoid solid (10 Nov, DICTO "did we get a scutoid solid … like a geometric one"; scripts/scutoid_solid.py)
Brick layer (version a), all side faces flat at both stages: middle by LP (kept edges parallel to the hexagon edges, shortest 0.30),
top by LP (each collapsed point reopened across into a horizontal edge, every other edge parallel to its middle edge, shortest 0.25),
each level kept as close as possible to the one below. Top side counts in the patch: 12 pentagons, 12 heptagons.
A cell that gains nothing: bottom hexagon (z = 0) → middle pentagon (z = 1, one edge shrunk to a point: the Y) → top pentagon (z = 2):
a GEOMETRIC SCUTOID with 13 faces, every face flat (8.6e-16). Data: data-scutoid-solid.json; render in papers-to-read.
Next (DICTO: "as a block linear group and as a near sphere"; "as a core a football"): (1) the block: the whole brick layer as a group
of scutoids; (2) the near sphere: a skin of scutoids round a truncated icosahedron core.

## Step 5: the block (DICTO "as a block linear group")
Top polygons are now the faces of the actual top tiling, traced geometrically (the earlier bookkeeping put 14 edges that are not in the
top tiling; fixed). 16 interior cells: bottom hexagon → middle pentagon for all; top 5 (8 cells), 6 (4), 8 (4); average 6 as it must be.
Every face of every cell flat (7.4e-15). The top polygons tile with no overlap (3.6e-15) and no holes; 42 of 48 convex (the 8-gons are not).
Data data-scutoid-block.json; render papers-to-read/scutoid-block.png. Next: the near sphere (skin round a truncated icosahedron core).

## Step 6: the near sphere (DICTO "as a near sphere", core a truncated icosahedron; scripts/scutoid_sphere.py)
Inner truncated icosahedron (circumradius 1) → middle icosidodecahedron (1.18): every hexagon-hexagon edge shrinks to a point (the Y) →
outer truncated dodecahedron (1.42): each point reopens ACROSS, the new edge now between the two pentagon cells (a true T1).
32 cells: 12 pentagon scutoids 5 → 5 → 10 (pentagon below, decagon above) and 20 hexagon scutoids 6 → 3 → 3.
Every face flat (4e-13; by mirror symmetry each inner edge is parallel to its middle edge, so flat for ANY radii); every cell volume
positive (0.111 .. 0.287); the 32 volumes add to V(TD) − V(TI) = 5.6660707968 exactly (shell filled once). Render papers-to-read/scutoid-near-sphere.png.
Block question ("how many to fill space"): the LP block has 16 different cells (not forced to repeat); its pattern repeats in tops
2 pentagons : 1 hexagon : 1 octagon, so the periodic version needs 4 cells (+ mirror layer to return to hexagons). Next: periodic block.

## Earlier scutoid work (found 10 Nov after DICTO asked; should have been read FIRST)
- 2026-10-17-scutoids: the 8-piece flat scutoid GROUP that tiles a layer (Fable; every piece swaps 5 <-> 6, convex, chunky ψ 0.825-0.835),
  DICTO liked it; red granite renders (renders/red-group.png, red-stack.png); queued: grey-granite castle wall (ishigaki). Also the
  32-cell thick scutoid layer round a truncated icosahedron core (route B). Brief: memory scutoid-bundle-brief.
  → answers "how many to fill space in a block": 8 pieces (already found).
- 2026-11-06-football-scutoids: truncated icosahedra on a layer linked pentagon-to-hexagon, space cut into one cell per ball, every cell
  makes the scutoid move twice; exact stacking (h = 3.437...). Logged then: skin round a football (B) and an icosahedron-to-football shell.
What steps 4-6 here add: a FLAT-FACED geometric scutoid (13 faces) and the exact near-sphere shell TI -> ID -> TD (32 cells, every face
flat for any radii, volumes exact) - this is the 11-06 "skin round a football" idea made exact.

## Step 7: polar swap of the core (DICTO 10 Nov "polar swap of core"; "B first then A"; "disregard shrinking triangle route")
B (scripts/scutoid_polar.py): the polar of TI → ID → TD is PD (pentakis dodecahedron) → RT (rhombic triacontahedron) → TK (triakis
icosahedron). On triangle cells the scutoid move cannot run (a triangle losing a side vanishes; route dropped by DICTO). In the polar the
move becomes a FLIP: each pair of PD triangles across a 6-6 edge flattens into one RT rhombus and folds the other way (TK triangles across
the 10-10 edge). True polars (PD r3/r5 = 1.026531522 from TI, TK 0.854818176 from TD; RT flat at 0.910592997). 30 cells, one per rhombus,
ALL CONGRUENT (volume 0.2155 each at RT scale 1.25, TK 1.55), side faces in mirror planes through the centre (flat, 1e-16); the 30 add
to V(TK) − V(PD) = 6.4660211935 exactly. Render papers-to-read scutoid-polar-shell-B.png.
A (inside out, scutoid_sphere.py 0.95 0.90): TD core → ID → TI outside: decagon cells 10 → 5 → 5, triangle cells 3 → 3 → 6;
every face flat (2.6e-13), all 32 cells one orientation, volumes add to the shell exactly. Render scutoid-inside-out-shell-A.png.
NEXT (DICTO "can we do a cycle of them"): iterate, outer surface → next core, alternating scutoid move and flip; does it close?

## Step 8: the cycle (DICTO 10 Nov "can we do a cycle of them I wonder what they might yield"; scripts/scutoid_cycle.py)
The scutoid move is its own inverse (TI → TD → TI), and so is the flip (PD → TK → PD); with the polar swaps they make one square
TI → TD (scutoid move) → TK (polar) → PD (flip) → TI (polar): period 4. Built as nested shells (flatness holds at any radii):
- SCUTOID ONION: S (TI 1 → ID 1.18 → TD 1.42) + A (TD 1.42 → ID 1.499 → TI 1.578), repeated at scale λ = 1.42/0.90 = 1.5778 per
  period. Interfaces match corner for corner (60); over 3 periods the cell volumes = V(TI λ³) − V(TI) = 216.5210825662 exactly.
  All of space but the centre is filled by FOUR cell shapes (5→5→10, 6→3→3, 10→5→5, 3→3→6) at scales λ^k, k in Z.
- FLIP ONION: B (PD 1 → RT 1.25 → TK 1.55) + back (TK → RT → PD), λ = 1.55/0.86 = 1.8023. Interfaces 32 corners; 3 periods
  = V(PD λ³) − V(PD) = 737.4739317134 exactly. Space but the centre filled by TWO shapes (one per shell, all congruent) at scales λ^k.
Renders papers-to-read scutoid-onion-cycle.png, scutoid-flip-onion-cycle.png (cut in half).
LEADS: can the back-flip cell be made congruent to the forward one (ONE shape at scales λ^k)? radii giving golden λ (φ or φ²)?

## Step 9: partial moves, conserve or dissipate (DICTO 10 Nov "whether a more irregular solid might form"; "how geometry conserves or
dissipates"; scripts/scutoid_partial.py, scutoid_conserve.py)
Partial move = only some hexagon-hexagon edges shrink and reopen. Faces kept flat by LINEAR conditions: middle edges parallel to their
core edges, outer edges parallel to their source core edges, every NEW edge along the meeting line of its two faces' core planes (A side
→ B side; without this a decagon with 5 new edges was not held flat - fixed). Moves applied one at a time on the current faces (moving
all 30 at once interferes otherwise - fixed). Unique choice: least squares nearest the radial scalings 1.18 / 1.42 (an LP picked
lopsided optima and faked dissipation: 32 shapes even for the full move - rejected as a solver artefact). New edges held at LNEW × mean.
Shell after shell, outer surface = next core, each later shell undoes the previous move. Every shell: every face flat (≤3e-13), cell
volumes add exactly, all positive.
- ALL 30 (control): 2 shapes every shell, drift 0 (1e-14); period 2 from the start. CONSERVED.
- SIX (cube-aligned, LNEW 0.4; 0.6 and 1.0 turn an edge over): 3 shapes every shell; pentagons stay exact, hexagon face distances spread
  3.70% / 4.18% alternately, forever. CONSERVED, irregularity locked in (period 2).
- ONE edge (LNEW 1.0): 12 shapes every shell; spread 7.4% in the move shells, 0.0487% after each undo: the undo heals 99.3%, a fixed scar
  stays, period 2. Neither dissipates nor grows.
Reading: under this rule the number of shapes is fixed by the symmetry of the chosen edge set (Ih 2, Th 3, one edge 12) and is conserved;
the shape settles at once into a 2-cycle. Caveat: the rule (least squares) is linear, which forces quick settling; other rules
(e.g. equal volumes, or edges fixed in length) could behave differently - next test of the question.

## Step 10: second rule, equal edges (DICTO: "so they dont exchange freely like regular solids")
Rule 2 (scutoid_conserve.py ... edges): after the least-squares start, all middle and outer edges as equal as possible (non-linear),
with barriers: no edge below 0.15 of its core edge, every cell volume ≥ 0.03 (without them cells turned inside out, vol −0.11: rejected).
Volumes vectorised (the loop version hit its cap at 280 s and was stopped; now 5 s a shell). Every shell: faces flat, volumes exact.
- ALL 30 (control): face-distance spread stays ~1e-8 for 6 shells: regular solids exchange freely. (Shape counts wobble 2–4 in shells
  where the volume floor binds: shape counts under this rule are NOT reliable; spread is.)
- ONE edge: spread grows every round trip: 25/38% → 32/29% → 64/50% → 55/62% → 89/77% → 79/89% → 113/103% → 103/116% (8 shells):
  the irregularity SPREADS (dissipates outwards), steadily, no sign of settling.
- SIX edges: spread jumps from 1.8% to ~4–9% and then stays bounded (3.3–4.4% pentagons, 5–9% hexagons, period 2): locked.
Reading so far: regular → conserved under both rules; a single defect is conserved under the gentle rule but spreads under the
equal-edge rule; the cube-symmetric defect stays bounded under both. The memory of the defect depends on the rule ("exchange" is free
only for the regular solids).
