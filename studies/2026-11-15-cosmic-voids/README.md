# Cosmic voids as a changing tiling: One tissue, three scales, Section 3

VERDICT (15 Nov 2026; true strength stated for each finding)
1. TOY, exact: generic moving foams gain and lose contacts one at a time, as #104 Theorem 1′ says.
   - 30,758 events in three generic motions (Voronoi, wiggling weights, weight walk; N = 512; the first two also rerun at half the
     base step): 0 simultaneous changes at a 1e-9 time floor, 0 clumps.
   - The power diagrams add only births and deaths with 4 contacts (the 1-4 and 4-1 moves).
   - The negative control, centres passing through the cubic lattice, is caught (10 simultaneous changes).
   - The event lists are identical at two time steps.
   - Two cross-checks agree: 15.56 contact changes per cell per spacing of r.m.s. displacement against 15.61 ± 0.03 from the project's
     null-model study, and 15.534 ± 0.012 neighbours against Meijering's 15.535.
   - Strength: a computation, not a proof. It checks the generic statement on these motions.
2. VOID BASINS, from a small simulation we ran ourselves. Public code pmwd; 256^3 particles in 256 Mpc/h; watershed basins at fixed
   smoothing R = 3, 4, 6 Mpc/h; two seeds; snapshots down to Delta a = 1/512. Contact changes are mostly, but not all, single.
   - The share that come alone rises as the snapshots get closer: R = 4 gives 0.23 at Delta a = 1/16 and 0.60 at 1/512.
   - The rise slows, so the share approaches roughly 0.65-0.7 (an extrapolation).
   - At the finest spacing, 20% of contact changes still clump with other contact changes. That is more than a one-at-a-time foam
     gives when sampled at the same rate.
   - Cause, decided by the follow-up below: the discreteness of the tiling (voxels, or tracer particles), not the physics. In both
     families the excess clumping over the exact foam, at the same rate of changes, falls when the units get finer: voxel basins
     0.163 -> 0.076 (1 -> 0.5 Mpc/h voxels, same field), tracer zones by about 0.08 (131k -> 1M tracers). The clumps sit on small
     walls; they do not gather at merges or on denser walls. Strength: two resolutions per family; that the excess reaches 0 in the continuum is
     an extrapolation, not a measurement.
3. Ratio: about 25 contact changes per basin that merges away; 23-27 over R = 3-6, both seeds and the fine spacings. It is steady as the
   spacing shrinks. Per NET basin lost (z = 3 to 0, R = 4), about 117, because many merges and splits undo one another. Merges are
   not 4-1 deaths: a whole wall dissolves, so a merge carries several contact changes by its nature.
4. Neighbours per void basin: 17.2-18.0 when any shared voxel face counts; 13.7-15.4 when a wall needs 10 faces. With the physical rule
   fixed in the follow-up (a wall counts if its area is at least 0.002 of the cell size Vbar^(2/3)), 16.7 on both grids, ABOVE
   Meijering's 15.535. At the same cut, Poisson-Voronoi cells have 14.93, so the basins have 1.8 more. Over cuts eps 0.002-0.02 all six
   void tilings (two voxel grids, four tracer tilings) have 0.3-3.1 more neighbours than Poisson-Voronoi cut the same way; at eps 0.05
   the voxel basins come level (-0.16 to +0.19). Aragón-Calvo 2014 (about 14) used a different void definition.
5. We found no earlier count of contacts gained or lost between neighbouring voids (sources listed below).

## Question and wording
DICTO, 15 Nov 2026: "throw all possible resources at the new scutoid work". The plan "One tissue, three scales" (14 Nov 2026), Section 3,
follows #104 (Scutoid Tissues in Four Dimensions), whose Theorem 1′ says that generic 3D cells gain and lose contacts one at a time.
Here: do cosmic-void basins in a simulation do the same, how many contact changes come per merge, and how many neighbours does a void
have against the Voronoi value? Each system makes its tiling for its own physical reasons; nothing here assumes or tests any influence of
one system on another. If the same ratios appear at several scales, the common cause would be geometry.

## Prior art (free sources only; 15 Nov 2026; FT = full text read, AB = abstract only, 2nd = known from other papers' citations)
- Sutter, Elahi, Falck, Onions, Hamaus, Knebe, Srisawat & Schneider 2014, "The life and death of cosmic voids", MNRAS, arXiv:1403.7525 [FT].
  ZOBOV voids in 62 snapshots (z about 30 to 0). Each void is matched to its main progenitor by shared particles, using the halo merger-tree
  code VELOCIraptor. Voids have on average little more than one progenitor, mergers are rare (about 5% violent), and neighbour changes are
  not tracked.
- Wojtak, Powell & Abel 2016, "Voids in cosmological simulations over cosmic time", MNRAS, arXiv:1602.08541 [FT]. Gadget-2, 256^3
  particles in 250 Mpc/h, snapshots every Delta a/a = 0.05, density on a 256^3 grid. Watershed basins (26-neighbour) merged into voids as in
  ZOBOV. Their warning: matching voids between adjacent snapshots gives spurious "instantaneous reconfigurations". Half of the voids change
  volume by more than 50% between adjacent snapshots, because the order of minima and saddles that decides how basins merge into voids
  reshuffles at random (unresolved small-scale modes, rounding). Matching by particles is worse than matching by grid volume, since most
  particles sit on void boundaries. Their remedy is to track the watershed BASINS, not the merged voids, linking basins that contain each
  other's minimum. Basins merge (more common) or split (less common), seen as bifurcations of the links. We follow this remedy: basins
  only, no merging into voids, grid volume, the minimum-containment link.
- Neyrinck 2008, ZOBOV, MNRAS 386, 2101, arXiv:0712.3049 [FT]. The density is the inverse of each particle's Voronoi cell volume. Each
  particle points to its lowest-density Voronoi neighbour, and a zone = everything draining to one minimum (the steepest-descent
  watershed used here, on a grid). Zones are merged by a rising water level. Zone adjacency is used only for merging; it is never counted
  or tracked. ZOBOV quotes 48π²/35 + 2 ≈ 15.54 Voronoi neighbours.
- Sutter et al. 2015, VIDE, arXiv:1406.1191 [AB]: ZOBOV-based toolkit with a void hierarchy. The abstract mentions no time tracking.
  Platen, van de Weygaert & Jones 2007, Watershed Void Finder, arXiv:0706.2788 [AB]: a single snapshot.
- Voronoi foam models of the cosmic web [abstracts or citations only]:
  - Icke & van de Weygaert 1987, A&A 184, 16 [2nd];
  - van de Weygaert & Icke 1989, A&A 213, 1 [2nd];
  - van de Weygaert 2002, arXiv:astro-ph/0206427 [AB];
  - van de Weygaert 2007, arXiv:0707.2877 [AB].
  No abstract makes a statement on topology changes of the void network in time. The 153-page 2002 review was not read in full.
- Aragón-Calvo 2014, "The Universe as a Cellular System", arXiv:1409.8661 [FT]: the closest prior work.
  - Two voids are adjacent when they share a wall.
  - Lewis and Aboav laws hold, and a von Neumann-type relation is stated.
  - Voids of the typical radius (about 7 Mpc/h at z = 0) have about 14 neighbours, and the mean is closer to the Voronoi 15.54 at z = 10.
  - Snapshots are linked by more than 70% volume overlap.
  - The degree is counted per snapshot only. The paper counts no contacts gained or lost.
- Aragón-Calvo 2020, arXiv:2009.00977 [FT]: degree distribution peaks near 13; Eulerian merger tree at 75% shared volume; no neighbour
  tracking. Aragón-Calvo & Szalay 2013, arXiv:1203.0248 [FT]: hierarchy across smoothing scales at one time. Sheth & van de Weygaert
  2004, arXiv:astro-ph/0311260 [AB]: void-in-void and void-in-cloud, analytic.
- Poisson-Voronoi mean faces per cell 48π²/35 + 2 = 15.535: Meijering 1953, Philips Res. Rep. 8, 270 (credited via the papers below; the
  original was not seen). Lazar, Mason, MacPherson & Srolovitz 2013, arXiv:1401.1736, find 15.535 in 250 million cells [snippet].
- Moving Voronoi diagrams: Albers, Guibas, Mitchell & Roos 1998, IJCGA 8, 365 [FT pp. 1-4]. The diagram changes only when d + 2 points
  become cospherical; in 3D, generically, this is a 2-3 or 3-2 flip, which is one contact gained or lost. This is the computational-
  geometry form of the generic statement that #104 Theorem 1′ makes for 3D cells. For power diagrams, the 1-4 and 4-1 flips (a cell appears
  or vanishes) are standard (Edelsbrunner & Shah 1996, Algorithmica 15, 223 [2nd]). We found no free source stating that in kinetic form;
  the toy checks it directly.
- Grain growth (nearest measured analogue): Wakai, Shinoda, Ishihara & Domínguez-Rodríguez 2001, J. Mater. Res. 16, 2136 [AB]. They count,
  per vanishing grain, 3.7 face creations and 13.2 face eliminations. Mason et al. 2015, arXiv:1507.03379 [FT part]: steady-state mean
  faces 13.77 in grain growth.
- Conclusion of the search: we found no count of contacts gained or lost between neighbouring voids over time. Sutter et al. 2014 track
  mergers, and Aragón-Calvo 2014/2020 measure degree per snapshot. The counts below appear to be new; the claim is limited to the
  sources listed.
- Sources checked:
  - Fetched: arXiv abstract pages 0712.3049, 1406.1191, 0706.2788, 1403.7525, 1409.8661, astro-ph/0206427, astro-ph/0311260, 0707.2877,
    1507.03379, 1209.5434, physics/0302018;
  - ar5iv 0712.3049, 1403.7525, 1203.0248, 1507.03379;
  - arXiv HTML 1409.8661v1, 2009.00977v1, 1709.09086;
  - arXiv PDF 1602.08541;
  - the Cambridge abstract page of Wakai et al. 2001; a free PDF of Albers et al. 1998; the Nordic J. Computing page of Roos 1997.
  - Blocked: NASA ADS (HTTP 405), pubs.rsc.org (403), a TU Delft PDF (connection refused).
  - Searches: void network topology evolution neighbours per void; Aragon-Calvo Szalay hierarchy; topological events 3D grain growth;
    Voronoi diagrams of moving points; 48π²/35 Meijering; kinetic Delaunay 2-3/3-2 and regular 1-4/4-1; Icke van de Weygaert fragmenting
    the universe; void-void neighbours Hamaus Ricciardelli Lavaux; cosmic voids neighbour exchange / T1 / topological transitions;
    kinetic power diagram; 3D foam coarsening T1 per bubble.

## Method
### Toy: a moving foam where every event is exact (scripts/toy_foam.py; independent test scripts/test_toy.py)
- N centres in a periodic unit box move in straight lines, x_i(t) = x_i(0) + v_i t (mod 1). The v_i are Gaussian with r.m.s. 0.5 mean
  spacings per unit time per component; the run lasts T = 1.
- Weights: 'voronoi' (all zero: the Voronoi foam); 'wiggle' (each weight w_i(t) = h^2 sin(omega_i t + phi_i), independent, h = mean
  spacing, about one period per run: a power diagram in which cells shrink to nothing and come back); 'walk' (half the centres, chosen at
  random, lose weight linearly to -2h^2: the weight walk of #51, #53 and #56 on random centres); 'lattice' (NEGATIVE CONTROL: all centres
  pass through the simple cubic lattice at t = 1/2, where 8 centres lie on each empty sphere).
- Geometry: the power diagram is dual to the lower convex hull of the lifted points (x, |x|^2 - w) in 4D (the Delaunay triangulation when
  the weights are equal). Qhull (Barber, Dobkin & Huhdanpaa 1996) computes the hull, called through scipy. Centres within a margin of the
  faces are copied across the box. Every kept simplex must have its orthosphere inside the copied region, and no simplex may hold two
  copies of one centre; otherwise the frame fails. Two cells touch when they share a face (a hull edge). A cell exists when its centre is a
  hull vertex.
- Checks on every frame:
  - Euler's formula for the 3-torus, cells - contacts + edges - corners = 0;
  - the same frame recomputed after a random shift of all centres (the same foam from different floating-point input) must give the same
    contacts;
  - the margin check above.
  - test_toy.py also compares the contacts with an independent periodic Delaunay call (all 27 copies, no margin): equal in 6 of 6 frames.
- Events: between two frames, if more than one elementary change happened, the interval is halved until each piece holds at most one
  change, down to a floor of 1e-9. An elementary change is one contact gained, one contact lost, a cell born with its 4 contacts, or a cell
  dying with its 4. A piece still holding several changes at the floor is a simultaneous event. The frames at all piece ends go, in time
  order, to the shared event logger (studies/2026-11-15-event-logger, eventlog.py, imported unchanged; its 3D vocabulary: contact gained,
  contact lost, birth, death, split, merge, relabel, clump).
- Step independence: the same runs at base steps 0.02 and 0.01 must give identical event lists.
- Coarse logs: the base frames alone at 1, 2, 5 and 10 base steps, with no halving, through the same logger. They show what fixed-step
  sampling does to the counts.

### Cosmic web: a small N-body run we made ourselves (scripts/nbody_pm.py)
- Code: pmwd, a public particle-mesh N-body code in JAX (Li, Lanusse, Modi et al. 2022, arXiv:2211.09958; BSD-3-Clause). We call its
  functions (2LPT initial conditions, leapfrog particle-mesh steps, cloud-in-cell assignment) and copy none of its code.
- Cosmology: Planck 2018 as packaged in pmwd.
- Size: 256^3 particles in a periodic box of 256 Mpc/h, force mesh 512^3, start at a = 1/32, steps of Delta a = 1/128.
- Output: the density contrast on a 256^3 grid (1 Mpc/h cells) saved at every step from z = 3 to 0 (97 snapshots), for two independent
  seeds. A third run (seed 1) uses steps of Delta a = 1/512 from a = 0.75 to 1, for the snapshot-spacing test.
- This set-up matches Wojtak et al. 2016 (256^3 particles, 250 Mpc/h, 256^3 grid), but uses a particle-mesh code rather than Gadget-2. The
  force resolution is about 0.5 Mpc/h, coarse for haloes but enough for basins smoothed at 3 Mpc/h or more.
- Controls: mass is conserved on every grid; the density spread grows at every snapshot; the power at k < 0.06 h/Mpc against pmwd's
  linear power at z = 0 is 0.71 (seed 1) and 0.90 (seed 2). Only 38 modes, so the expected scatter is about ±23%.
- Data stay on the compute machine (about 6 GB per run; nothing downloaded).

### Void basins and their events (scripts/void_basins.py)
- The density contrast is smoothed with a Gaussian of r.m.s. width R, FIXED through each run: R = 3, 4 and 6 Mpc/h.
- Basins: each voxel points to its lowest neighbour among the 26 around it, if that neighbour is lower. A basin is everything draining to
  one minimum. This is the ZOBOV zone on a grid, as in Wojtak et al. 2016, with no merging of basins into larger voids, so the basins tile
  the box and nesting plays no part.
- Contact: two basins touch when they share a wall, i.e. at least one voxel face (6-connectivity). Variant: only walls of at least 10 voxel
  faces (10 (Mpc/h)^2) count.
- Tracking (Wojtak et al. 2016 rule, by grid volume): an earlier basin is linked to the later basin containing its minimum voxel, and a
  later basin to the earlier basin containing its minimum.
  - A later basin keeps the label of the earlier basin it is linked to both ways (if none, of the largest earlier basin whose minimum it
    holds).
  - Earlier basins that lose their label have merged into the basin holding their minimum.
  - A later basin holding no earlier minimum is new; its parent is the earlier basin holding its minimum (a split).
  - This lineage goes to the logger.
- Variants: every k-th snapshot, k = 1, 2, 4, 8 (Delta a = 1/128 to 1/16; Delta a/a = 0.008 to 0.0625 at z = 0, around Wojtak et al.'s
  0.05); both seeds at R = 4; all three R for seed 1; the Delta a = 1/512 run.
- Derived counts: every contact change is assigned to one of three groups:
  - "alone": a logger event of one contact gained or lost;
  - "clumped": in a clump with other contact changes and no cell change;
  - "with a merge/split".
  When a basin merges, the survivor takes over some of its walls, so a merge carries contact gains by construction. The logger then calls
  it a clump; we count it as a merge-type event.

## Results

Tables made by scripts/summarise.py from results/*.json.

### Toy runs (exact events)

| run | N | base step | contact gained | contact lost | births | deaths | clumps | simultaneous at 1e-9 | Euler / shift / margin / balance failures | mean contacts per cell | contact changes per cell per unit time |
|---|---|---|---|---|---|---|---|---|---|---|---|
| lattice | 512 | 0.02 | 1159 | 1127 | 0 | 0 | 6 | 10 | 1 / 1 / 0 / 0 | 15.639 | 4.46 |
| voronoi | 512 | 0.01 | 3457 | 3443 | 0 | 0 | 0 | 0 | 0 / 0 / 0 / 0 | 15.601 | 13.48 |
| voronoi | 512 | 0.02 | 3457 | 3443 | 0 | 0 | 0 | 0 | 0 / 0 / 0 / 0 | 15.602 | 13.48 |
| walk | 512 | 0.02 | 2696 | 3628 | 1 | 251 | 0 | 0 | 0 / 0 / 0 / 0 | 15.083 | 12.35 |
| wiggle | 512 | 0.01 | 8151 | 8109 | 511 | 511 | 0 | 0 | 0 / 0 / 0 / 0 | 14.516 | 31.76 |
| wiggle | 512 | 0.02 | 8151 | 8109 | 511 | 511 | 0 | 0 | 0 / 0 / 0 / 0 | 14.515 | 31.76 |

### Fixed-step sampling of the toy (no halving): share of seen contact changes that come alone

| run | step | seen contact changes per cell per step | share alone |
|---|---|---|---|
| voronoi N=512 | 0.005 | 0.067 | 0.836 |
| voronoi N=512 | 0.01 | 0.134 | 0.738 |
| voronoi N=512 | 0.02 | 0.268 | 0.579 |
| voronoi N=512 | 0.04 | 0.532 | 0.385 |
| voronoi N=512 | 0.08 | 1.044 | 0.200 |
| voronoi N=512 | 0.16 | 2.031 | 0.066 |
| wiggle N=512 | 0.005 | 0.249 | 0.573 |
| wiggle N=512 | 0.01 | 0.482 | 0.386 |
| wiggle N=512 | 0.02 | 0.911 | 0.203 |
| wiggle N=512 | 0.04 | 1.631 | 0.071 |
| wiggle N=512 | 0.08 | 2.592 | 0.014 |
| wiggle N=512 | 0.16 | 3.093 | 0.001 |

### Void basins

| run | R (Mpc/h) | a range | spacing Delta a | wall min (faces) | basins first / last | mean contacts first / last | contact changes seen | per basin per step | share alone | clumped with other contact changes | with a merge or split | basins merged | basins split | contact changes per merged basin | lost and regained next step | balance failures |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s1-R3 | 3 | 0.25-1 | 0.007812 | 1 | 3267 / 2702 | 17.23 / 17.28 | 64879 | 0.226 | 0.433 | 0.291 | 0.276 | 2633 | 2068 | 24.6 | 3236 of 62174 lost | 0 |
| s1-R3 | 3 | 0.25-1 | 0.01562 | 1 | 3267 / 2702 | 17.23 / 17.28 | 56801 | 0.396 | 0.345 | 0.314 | 0.341 | 2458 | 1893 | 23.1 | 4638 of 56166 lost | 0 |
| s1-R3 | 3 | 0.25-1 | 0.03125 | 1 | 3267 / 2702 | 17.23 / 17.28 | 45321 | 0.633 | 0.250 | 0.294 | 0.456 | 2206 | 1641 | 20.5 | 5239 of 47511 lost | 0 |
| s1-R3 | 3 | 0.25-1 | 0.0625 | 1 | 3267 / 2702 | 17.23 / 17.28 | 32029 | 0.894 | 0.172 | 0.230 | 0.598 | 1833 | 1268 | 17.5 | 3861 of 36346 lost | 0 |
| s1-R3 | 3 | 0.25-1 | 0.007812 | 10 | 3267 / 2702 | 13.65 / 13.76 | 49775 | 0.174 | 0.488 | 0.217 | 0.295 | 2633 | 2068 | 18.9 | 3334 of 47357 lost | 0 |
| s1-R3 | 3 | 0.25-1 | 0.03125 | 10 | 3267 / 2702 | 13.65 / 13.76 | 32197 | 0.450 | 0.319 | 0.245 | 0.435 | 2206 | 1641 | 14.6 | 3765 of 34966 lost | 0 |
| s1-R4-late | 4 | 0.75-1 | 0.007812 | 1 | 1327 / 1257 | 17.49 / 17.49 | 6116 | 0.148 | 0.504 | 0.253 | 0.243 | 256 | 186 | 23.9 | 253 of 5918 lost | 0 |
| s1-R4-late | 4 | 0.75-1 | 0.01562 | 1 | 1327 / 1257 | 17.49 / 17.49 | 5510 | 0.267 | 0.427 | 0.286 | 0.287 | 246 | 176 | 22.4 | 339 of 5501 lost | 0 |
| s1-R4-late | 4 | 0.75-1 | 0.03125 | 1 | 1327 / 1257 | 17.49 / 17.49 | 4650 | 0.450 | 0.323 | 0.306 | 0.371 | 234 | 164 | 19.9 | 427 of 4922 lost | 0 |
| s1-R4-late | 4 | 0.75-1 | 0.0625 | 1 | 1327 / 1257 | 17.49 / 17.49 | 3535 | 0.684 | 0.233 | 0.271 | 0.496 | 204 | 134 | 17.3 | 387 of 4025 lost | 0 |
| s1-R4-late | 4 | 0.75-1 | 0.007812 | 10 | 1327 / 1257 | 14.41 / 14.44 | 4682 | 0.113 | 0.549 | 0.179 | 0.272 | 256 | 186 | 18.3 | 230 of 4582 lost | 0 |
| s1-R4-late | 4 | 0.75-1 | 0.03125 | 10 | 1327 / 1257 | 14.41 / 14.44 | 3336 | 0.323 | 0.381 | 0.240 | 0.379 | 234 | 164 | 14.3 | 326 of 3710 lost | 0 |
| s1-R4 | 4 | 0.25-1 | 0.007812 | 1 | 1477 / 1257 | 17.55 / 17.49 | 25635 | 0.195 | 0.477 | 0.269 | 0.254 | 1022 | 802 | 25.1 | 1311 of 24391 lost | 0 |
| s1-R4 | 4 | 0.25-1 | 0.01562 | 1 | 1477 / 1257 | 17.55 / 17.49 | 22352 | 0.341 | 0.391 | 0.304 | 0.306 | 946 | 726 | 23.6 | 1900 of 21861 lost | 0 |
| s1-R4 | 4 | 0.25-1 | 0.03125 | 1 | 1477 / 1257 | 17.55 / 17.49 | 17949 | 0.547 | 0.292 | 0.305 | 0.403 | 846 | 626 | 21.2 | 2113 of 18520 lost | 0 |
| s1-R4 | 4 | 0.25-1 | 0.0625 | 1 | 1477 / 1257 | 17.55 / 17.49 | 12832 | 0.782 | 0.214 | 0.272 | 0.514 | 709 | 489 | 18.1 | 1564 of 14310 lost | 0 |
| s1-R4 | 4 | 0.25-1 | 0.007812 | 10 | 1477 / 1257 | 14.46 / 14.44 | 19691 | 0.150 | 0.522 | 0.197 | 0.281 | 1022 | 802 | 19.3 | 1368 of 18938 lost | 0 |
| s1-R4 | 4 | 0.25-1 | 0.03125 | 10 | 1477 / 1257 | 14.46 / 14.44 | 12966 | 0.395 | 0.351 | 0.244 | 0.404 | 846 | 626 | 15.3 | 1493 of 14014 lost | 0 |
| s1-R6 | 6 | 0.25-1 | 0.007812 | 1 | 522 / 443 | 17.91 / 17.70 | 6572 | 0.142 | 0.567 | 0.242 | 0.191 | 241 | 162 | 27.3 | 374 of 5970 lost | 0 |
| s1-R6 | 6 | 0.25-1 | 0.01562 | 1 | 522 / 443 | 17.91 / 17.70 | 5739 | 0.248 | 0.491 | 0.284 | 0.225 | 223 | 144 | 25.7 | 449 of 5371 lost | 0 |
| s1-R6 | 6 | 0.25-1 | 0.03125 | 1 | 522 / 443 | 17.91 / 17.70 | 4718 | 0.407 | 0.380 | 0.335 | 0.284 | 208 | 129 | 22.7 | 509 of 4662 lost | 0 |
| s1-R6 | 6 | 0.25-1 | 0.0625 | 1 | 522 / 443 | 17.91 / 17.70 | 3508 | 0.606 | 0.277 | 0.307 | 0.416 | 181 | 102 | 19.4 | 404 of 3800 lost | 0 |
| s1-R6 | 6 | 0.25-1 | 0.007812 | 10 | 522 / 443 | 15.40 / 15.20 | 5246 | 0.113 | 0.597 | 0.191 | 0.212 | 241 | 162 | 21.8 | 365 of 4891 lost | 0 |
| s1-R6 | 6 | 0.25-1 | 0.03125 | 10 | 522 / 443 | 15.40 / 15.20 | 3524 | 0.304 | 0.439 | 0.259 | 0.302 | 208 | 129 | 16.9 | 380 of 3716 lost | 0 |
| s1f-R4 | 4 | 0.75-1 | 0.001953 | 1 | 1328 / 1258 | 17.49 / 17.51 | 6603 | 0.040 | 0.597 | 0.197 | 0.206 | 263 | 193 | 25.1 | 63 of 6219 lost | 0 |
| s1f-R4 | 4 | 0.75-1 | 0.003906 | 1 | 1328 / 1258 | 17.49 / 17.51 | 6399 | 0.077 | 0.563 | 0.220 | 0.217 | 257 | 187 | 24.9 | 140 of 6060 lost | 0 |
| s1f-R4 | 4 | 0.75-1 | 0.007812 | 1 | 1328 / 1258 | 17.49 / 17.51 | 6047 | 0.146 | 0.512 | 0.256 | 0.232 | 248 | 178 | 24.4 | 216 of 5787 lost | 0 |
| s1f-R4 | 4 | 0.75-1 | 0.01562 | 1 | 1328 / 1258 | 17.49 / 17.51 | 5479 | 0.265 | 0.423 | 0.308 | 0.268 | 236 | 166 | 23.2 | 330 of 5357 lost | 0 |
| s1f-R4 | 4 | 0.75-1 | 0.001953 | 10 | 1328 / 1258 | 14.42 / 14.45 | 5313 | 0.032 | 0.629 | 0.136 | 0.235 | 263 | 193 | 20.2 | 100 of 4931 lost | 0 |
| s1f-R4 | 4 | 0.75-1 | 0.007812 | 10 | 1328 / 1258 | 14.42 / 14.45 | 4651 | 0.112 | 0.551 | 0.181 | 0.268 | 248 | 178 | 18.8 | 229 of 4486 lost | 0 |
| s2-R4 | 4 | 0.25-1 | 0.007812 | 1 | 1493 / 1263 | 17.74 / 17.97 | 26402 | 0.200 | 0.483 | 0.288 | 0.229 | 1023 | 793 | 25.8 | 1304 of 24415 lost | 0 |
| s2-R4 | 4 | 0.25-1 | 0.01562 | 1 | 1493 / 1263 | 17.74 / 17.97 | 23264 | 0.352 | 0.395 | 0.319 | 0.286 | 953 | 723 | 24.4 | 1929 of 22100 lost | 0 |
| s2-R4 | 4 | 0.25-1 | 0.03125 | 1 | 1493 / 1263 | 17.74 / 17.97 | 18472 | 0.559 | 0.303 | 0.320 | 0.377 | 844 | 614 | 21.9 | 2156 of 18432 lost | 0 |
| s2-R4 | 4 | 0.25-1 | 0.0625 | 1 | 1493 / 1263 | 17.74 / 17.97 | 13095 | 0.792 | 0.209 | 0.278 | 0.513 | 702 | 472 | 18.7 | 1571 of 14159 lost | 0 |
| s2-R4 | 4 | 0.25-1 | 0.007812 | 10 | 1493 / 1263 | 14.56 / 14.60 | 21151 | 0.160 | 0.534 | 0.222 | 0.245 | 1023 | 793 | 20.7 | 1513 of 19441 lost | 0 |
| s2-R4 | 4 | 0.25-1 | 0.03125 | 10 | 1493 / 1263 | 14.56 / 14.60 | 13816 | 0.418 | 0.364 | 0.267 | 0.369 | 844 | 614 | 16.4 | 1575 of 14252 lost | 0 |

### Mean contacts per cell, periodic Poisson-Voronoi (4 seeds each; target 48π²/35 + 2 = 15.5355)

| N | mean | error of mean |
|---|---|---|
| 512 | 15.5762 | 0.0592 |
| 1000 | 15.5345 | 0.0117 |
| 4096 | 15.5334 | 0.0052 |
| 8000 | 15.5366 | 0.0070 |

### What the toy shows (exact events)
- One at a time, as #104 Theorem 1′ says for generic cells. In every generic run, every change was single: one contact gained, one
  contact lost, one cell born with its 4 contacts, or one cell died with its 4. There were 0 simultaneous changes at the 1e-9 floor and 0
  clumps in the logger: 6,900 events (Voronoi), 17,282 events (wiggling weights) and 6,576 events (weight walk), all at N = 512.
  Every frame passed Euler (3-torus), the shift test, the margin test and the logger balance. The power diagrams add exactly the 1-4 and
  4-1 moves (births and deaths), nothing else.
- Negative control works. When the centres pass through the cubic lattice (8 centres on each empty sphere), the toy finds 10
  simultaneous changes at the floor and the logger 6 clumps. The exactly degenerate frame also fails one Euler check and one shift test.
  So the method can see clumping when it is there.
- Step independence: base steps 0.02 and 0.01 give IDENTICAL event lists, the same events with the same cells in the same order (Voronoi
  6,900 of 6,900; wiggle 17,282 of 17,282).
- Rate cross-check against an independent study. The Voronoi foam has 13.48 contact changes per cell per unit time. The r.m.s. 3D speed is
  0.866 mean spacings per unit time, so this is 15.56 per cell per mean spacing of r.m.s. displacement (one run of 6,900 events,
  Poisson error about 1.2%). The null-model study of the same project (studies/2026-11-15-tissue-null-models) gets 15.61 ± 0.03 from an
  integral over the Poisson-Delaunay simplex. They agree.
- Neighbours per cell: 15.534 ± 0.012 (N = 1000), 15.533 ± 0.005 (N = 4096) and 15.537 ± 0.007 (N = 8000), 4 seeds each. These match
  48π²/35 + 2 = 15.535 (Meijering 1953). The single N = 512 event run gives 15.60, inside the seed scatter at that size (±0.06). With
  wiggling weights the power diagram has 14.52; with the weight walk, 15.08.
- Contact changes per cell lifetime (wiggling weights, the only run with complete lives): 219 cells were born and died inside the run.
  They have a mean lifetime of 0.233 time units and 37.4 contact changes per life. Over the whole run there are 15.9 contact changes per
  birth or death (16,260 / 1,022). For comparison, Wakai et al. 2001 count 16.9 face switches per vanishing grain in 3D grain growth
  (3.7 + 13.2); that is a different process.
- Fixed-step sampling manufactures clumps (the sampling artefact). Logging the same exact foam at fixed steps, without halving, makes
  the share of seen contact changes that come alone fall smoothly with the seen contact changes per cell per step: 0.84 at 0.067, 0.58
  at 0.27, 0.38 at 0.53, 0.20 at 1.04. Wiggling weights follow nearly the same curve (0.57 at 0.25, 0.39 at 0.48, 0.20 at 0.91), so the
  curve depends mainly on how many changes fall in a step. This curve is the yardstick for the void data, which have fixed snapshots.

### What the void basins show
- Separate or clumped? At the finest spacing available, under half to 60% of seen contact changes come alone. At Delta a = 1/128:
  - 0.43 at R = 3, 0.48 at R = 4 (seed 2: 0.48), 0.57 at R = 6;
  - with walls of at least 10 voxel faces: 0.49, 0.52, 0.60.
  The share rises at every halving of the spacing (R = 4: 0.21, 0.29, 0.39, 0.48 for Delta a = 1/16 to 1/128), in both seeds and at
  all three scales. That is what sampling a one-at-a-time process does, so the data do not show that clumping is intrinsic.
- But compared at the same number of changes per cell per step, the basins come out MORE clumped than the toy foam. a = 0.75-1, R = 4:
  - 0.50 alone at 0.148 changes per basin per step, where the foam curve gives about 0.72 (linear interpolation);
  - 0.43 at 0.27 (foam 0.58);
  - 0.32 at 0.45 (foam about 0.45);
  - 0.23 at 0.68 (foam about 0.33).
  The excess is real in these data, but its cause is not settled. Two candidates:
  - the voxel tiling is not generic (several basins meet along voxel edges, and one voxel changing hands can make or break two contacts
    at once);
  - basin walls jitter: about 5% of lost contacts come back at the very next snapshot (R = 4: 1,311 of 24,391), rising to 11% at four
    times the spacing.
  The null-model study warns that jittery boundaries give frame-rate-dependent counts. Here the seen contact changes grow as the spacing
  shrinks (R = 4: 12,832, 17,949, 22,352, 25,635), so the totals are not rates.
- The commonest clump is "lost 1, gained 1" among mutually touching basins: two single changes falling in one interval (in 3D a generic
  event never does this by itself).
- Contact changes per merge: about 25 seen contact changes per basin that merged away at Delta a = 1/128 (R = 3: 24.6, R = 4: 25.1 and
  25.8, R = 6: 27.3). The ratio falls with coarser spacing (to 17.5-19.4 at 1/16) and with the 10-face wall rule (18.3-21.8).
  Merges and splits are themselves partly back-and-forth: at R = 4, 1,022 basins merged away and 802 new basins split off, a net loss of
  220 from z = 3 to 0. Per NET basin lost, there are about 117 contact changes. Neither number is a stable rate yet; the per-merge
  number is the steadier of the two across scale and seed (24.6-27.3).
- Neighbours per void basin: 17.2 to 18.0 when any shared voxel face counts (R = 3 to 6, both seeds, z = 3 and z = 0), ABOVE the
  Poisson-Voronoi 15.54. With walls of at least 10 voxel faces it is 13.7, 14.4-14.6 and 15.2-15.4 at R = 3, 4, 6, BELOW it. So the
  neighbour count depends on how small a wall still counts, and no rule-free number comes out. Aragón-Calvo 2014 reports about 14 for
  typical voids, which falls between our two rules. The count hardly changes from z = 3 to z = 0 at fixed R.
- Stable: the rise of the alone share with finer spacing; the alone share at fixed spacing across seeds (0.477 / 0.483); contact
  changes per merged basin across scale and seed (about 25 at Delta a = 1/128); the mean contacts at fixed R and wall rule (to within
  0.5 between seeds).
- Not stable: total contact changes (they grow as the spacing shrinks); merges and splits counted separately (flicker); the mean
  neighbour count under a change of wall rule (about 3 neighbours).

### Finer snapshots (Delta a = 1/512, seed 1, a = 0.75-1, R = 4)
- Same initial conditions, PM step 4 times finer. Control: at Delta a = 1/128 it reproduces the coarse run over the same range (share
  alone 0.512 against 0.504; 6,047 against 6,116 contact changes; the PM time step differs).
- Share alone at Delta a = 1/128, 1/256, 1/512: 0.512, 0.563, 0.597. With 10-face walls: 0.551 at 1/128, 0.629 at 1/512. The gains per
  halving shrink: +0.09, +0.05, +0.035. At 0.040 changes per basin per step, the exact foam would give about 0.9. So the void basins
  approach a share of roughly 0.65-0.7, not 1 (an extrapolation of three points, not a measurement).
- At the finest spacing, 40% of seen contact changes still share a place and a step with another change:
  - 20% with other contact changes;
  - 21% with a merge or split.
- Contact changes per merged basin are steady as the spacing shrinks: 23.2, 24.4, 24.9, 25.1 (Delta a = 1/64 to 1/512). Total contact
  changes converge (5,479, 6,047, 6,399, 6,603). Lost-and-regained-next-step falls to 1% (63 of 6,219).
- Merges are not 4-1 deaths. A basin merges when a density minimum and a saddle annihilate, a generic event in a changing density field.
  The surviving basin then takes over a whole wall, so a merge carries several contact changes at once by its nature. Theorem 1′ speaks
  of generic contact changes between cells; a basin merge is a different event, so the 21% does not count against it. The 20% of
  contact changes clumped with other contact changes, with no merge, is the part that still stands against "one at a time" here.


## Follow-up: grid or physics? (15 Nov 2026; predictions written BEFORE the runs)
Question: at the finest snapshot spacing (Delta a = 1/512, R = 4 Mpc/h), 20% of contact changes clump with other contact changes and no
merge. Is that the voxel grid or the physics of the density field?
Tests:
- (1) Finer grid on the same field. The R = 4 smoothed field has no power above the 256^3 grid's Nyquist frequency (the Gaussian factor
  there is e^-79), so the same continuous field can be sampled on a 512^3 grid (0.5 Mpc/h voxels) by Fourier zero-padding, exactly.
  Basins, walls and tracking as before. Only the voxel size changes.
- (2) Grid-free basins. A fixed random subset of the particles (tracers) is followed through the same run. Walls are faces of the
  tracers' periodic Voronoi tessellation, so cells meet generically (3 along an edge, 4 at a corner), not as cubes (4 along an edge).
  (a) ZOBOV zones (Neyrinck 2008): density = 1 / Voronoi volume, each tracer points to its lowest-density Voronoi neighbour.
  (b) The same watershed on the R = 4 smoothed field read at the tracers, so the zones match the voxel basins in scale.
- Neighbour rule: a wall counts if its area is at least eps * Vbar^(2/3) (Vbar = mean basin volume at that snapshot). eps is fixed as the
  smallest value in {0.001, 0.002, 0.005, 0.01, 0.02, 0.05} at which the 256^3 and 512^3 grids agree on the mean neighbour count to 1%
  ("walls both grids resolve"). The same cut is applied to Poisson-Voronoi cells for a like-for-like reference; uncut, 15.535.
Predictions:
- P1. If the clumps are the grid: at 512^3 the share clumped with other contact changes falls from 0.20 to 0.12 or less, and the share
  alone rises above 0.65 toward the exact foam's ~0.9 at the same rate of changes per basin per step. If physics: within 0.03 of 0.20.
  Either way, the basin count stays within 1% (same field, same minima).
- P2. Voronoi zones (b) clump no more than the 512^3 voxels at the same rate; ZOBOV zones (a) flicker more (no smoothing) but, at matched
  changes per zone per step, lie near the exact-foam curve if the clumps are the grid.
- P3. With the physical wall rule, neighbours per basin = 14.5 +- 1, below Meijering's 15.535 (Aragon-Calvo 2014: about 14).
- P4. Any clumps left are mostly "lost 1, gained 1" on small walls next to merges and splits.

### Follow-up verdict (decided 15-16 Nov 2026)
- GRID, more exactly: the discreteness of the units the basins are built from. Not physics.
  - Same continuous field, voxels halved (1 -> 0.5 Mpc/h), finest spacing: the share of non-merge contact changes that clump falls
    0.243 -> 0.186 (any face) and 0.189 -> 0.158 (physical rule). Against the exact foam at the same rate, the excess falls
    0.163 -> 0.076 and 0.119 -> 0.077. It roughly halves with the voxel size.
  - Grid-free walls (Voronoi faces of tracer particles) do NOT remove the clumping: tracer zones clump MORE (0.28-0.45), because a
    tracer (spacing 2.5-8 Mpc/h) is a coarser unit than a voxel. Within that family it also falls with resolution: smoothed-field
    zones 131k -> 1M tracers, at matched rate about 0.08 lower.
  - Where the clumps sit: on small walls (voxel basins, physical rule: median area 0.016-0.020 Vbar^(2/3) against 0.011 for single
    changes); near a merge or split only 4-16% (single changes 2-8%); they change again in the next step about as often as single
    changes do; wall density the same as for single changes
    once tiny walls are cut (1.72 against 1.79 for 256^3). The commonest clumps are "lost 1, gained 1", "lost 2", "gained 2": pairs of
    small walls that one unit changing hands makes or breaks together. No sign of a physical place (filament, merge) for them.
  - Strength: two resolutions in each family, one seed, R = 4, a = 0.875-1. That the excess goes to 0 in the continuum is an
    extrapolation. Not run: the 512^3-particle simulation (about 10 times the 70-minute 256^3 run and some 30 GB on a shared machine);
    the field test above changes only the voxel size, which is the cleaner grid test.
- Predictions against outcome: P1 partly (clumped share 0.20 -> 0.148 any face, 0.118 physical rule; predicted <= 0.12; basin count
  1309 -> 1311, within 1%). P2 wrong (tracer zones clump more than voxels; the tracer is the coarser unit). P3 wrong (16.7, above
  15.535, not 14.5). P4 partly (small walls yes; near merges no).
- Neighbour rule, as fixed before the runs: the smallest eps at which 256^3 and 512^3 agree to 1% is 0.002 (16.74 and 16.73). This
  agreement is a crossing of two curves; at eps 0.005-0.05 the 512^3 counts lie 2-3% lower. The firmer statement is the comparison
  with Poisson-Voronoi at the same cut: at eps 0.002-0.02 every void tiling has more neighbours (0.3-3.1), at eps 0.05 the voxel
  basins come level (table below). Uncut Poisson-Voronoi here:
  15.551 +- 0.009 (Meijering 15.535).

### Follow-up method
- Test 1 (scripts/grid_refine.py): run s1f, a = 0.875-1 (65 snapshots, Delta a = 1/512), R = 4. The smoothed field is band-limited
  (Gaussian weight at the 256^3 Nyquist frequency 2e-36 of the peak), so Fourier zero-padding samples the same field on 512^3; control:
  the 512^3 field at the old voxels equals the 256^3 field to 9e-15 of its spread. Basins, walls (area in (Mpc/h)^2, mean field on the
  wall), tracking and logger as before (scripts/basin_events.py, a generalised copy of the earlier stage 2 with per-change records).
- Test 2 (scripts/nbody_tracers.py, tracer_zones.py): the s1f run repeated with the same code and seed, saving a fixed random 1/8 of the
  particles at every step; the densities are bit-identical to the earlier run (control at 5 snapshots: deviation 0). Periodic Voronoi
  cells of the tracers from Qhull's Delaunay triangulation with copies across the box (circumsphere margin check; volumes sum to L^3 to
  2e-16; degree on Poisson points 15.54). freud 3.6.1 was tried first and dropped (its neighbour list was not symmetric and gave 14.60
  on Poisson points). ZOBOV zones (Neyrinck 2008; density = 1 / Voronoi volume) for 262,144 and 32,768 tracers; smoothed-field zones
  (the R = 4 field of all particles read at the tracers) for 1,048,576 and 131,072 tracers. Zones are not merged into voids.
- Yardstick: the exact foam sampled at fixed steps, now down to 0.017 changes per cell per step (toy_coarse.py, base step 0.00125; its
  rows at 0.067-0.53 repeat the earlier curve exactly). Compared quantity: among contact changes not tied to a merge or split, the
  share clumped with other contact changes, at the same number of such changes per cell per step.
- Wall rules: native (any face), 10 (Mpc/h)^2, and eps * Vbar^(2/3) (pv_walls.py gives Poisson-Voronoi under the same cut).
- Limits: tracer zones under-sample voids (tracers follow mass), so 131k tracers find only about 800 zones against 1309 voxel basins;
  1M tracers find 1259. Tracer walls are rough at the tracer spacing, which raises their neighbour counts.

### Follow-up tables (scripts/summarise_followup.py)
#### Grid refinement and grid-free zones: share of contact changes alone and clumped

| run | tiling | spacing Delta a | wall rule | basins first / last | mean contacts | contact changes | per basin per step | share alone | clumped with contact changes | with a merge or split | non-merge changes per basin per step | clumped share of non-merge changes | exact foam at the same rate | contact changes per merged basin | balance failures |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grid-s1f-R4-G256 | voxels 256^3 (1 Mpc/h) | 0.001953125 | faces 1 | 1309 / 1258 | 17.44 | 2874 | 0.035 | 0.592 | 0.190 | 0.218 | 0.027 | 0.243 | 0.080 | 21.9 | 0 |
| grid-s1f-R4-G256 | voxels 256^3 (1 Mpc/h) | 0.001953125 | phys 10 | 1309 / 1258 | 14.40 | 2429 | 0.029 | 0.620 | 0.142 | 0.238 | 0.023 | 0.186 | 0.067 | 18.5 | 0 |
| grid-s1f-R4-G256 | voxels 256^3 (1 Mpc/h) | 0.001953125 | eps 0.01 | 1309 / 1258 | 15.25 | 2537 | 0.031 | 0.624 | 0.145 | 0.231 | 0.024 | 0.189 | 0.070 | 19.4 | 0 |
| grid-s1f-R4-G256 | voxels 256^3 (1 Mpc/h) | 0.00390625 | faces 1 | 1309 / 1258 | 17.44 | 2797 | 0.068 | 0.561 | 0.215 | 0.224 | 0.053 | 0.276 | 0.139 | 21.7 | 0 |
| grid-s1f-R4-G256 | voxels 256^3 (1 Mpc/h) | 0.00390625 | phys 10 | 1309 / 1258 | 14.40 | 2320 | 0.056 | 0.589 | 0.156 | 0.255 | 0.042 | 0.210 | 0.116 | 18.0 | 0 |
| grid-s1f-R4-G256 | voxels 256^3 (1 Mpc/h) | 0.00390625 | eps 0.01 | 1309 / 1258 | 15.25 | 2458 | 0.060 | 0.604 | 0.156 | 0.240 | 0.045 | 0.205 | 0.124 | 19.1 | 0 |
| grid-s1f-R4-G256 | voxels 256^3 (1 Mpc/h) | 0.0078125 | faces 1 | 1309 / 1258 | 17.44 | 2675 | 0.130 | 0.518 | 0.246 | 0.237 | 0.099 | 0.322 | 0.219 | 21.4 | 0 |
| grid-s1f-R4-G256 | voxels 256^3 (1 Mpc/h) | 0.0078125 | phys 10 | 1309 / 1258 | 14.40 | 2127 | 0.103 | 0.540 | 0.182 | 0.278 | 0.075 | 0.252 | 0.179 | 17.0 | 0 |
| grid-s1f-R4-G256 | voxels 256^3 (1 Mpc/h) | 0.0078125 | eps 0.01 | 1309 / 1258 | 15.24 | 2288 | 0.111 | 0.565 | 0.176 | 0.260 | 0.082 | 0.237 | 0.193 | 18.3 | 0 |
| grid-s1f-R4-G512 | voxels 512^3 (0.5 Mpc/h) | 0.001953125 | faces 1 | 1311 / 1284 | 18.07 | 4122 | 0.050 | 0.650 | 0.148 | 0.201 | 0.040 | 0.186 | 0.110 | 23.7 | 0 |
| grid-s1f-R4-G512 | voxels 512^3 (0.5 Mpc/h) | 0.001953125 | phys 10 | 1311 / 1284 | 14.00 | 2780 | 0.033 | 0.633 | 0.103 | 0.264 | 0.025 | 0.140 | 0.073 | 16.0 | 0 |
| grid-s1f-R4-G512 | voxels 512^3 (0.5 Mpc/h) | 0.001953125 | eps 0.01 | 1311 / 1284 | 14.88 | 3093 | 0.037 | 0.627 | 0.118 | 0.255 | 0.028 | 0.158 | 0.081 | 17.8 | 0 |
| grid-s1f-R4-G512 | voxels 512^3 (0.5 Mpc/h) | 0.00390625 | faces 1 | 1311 / 1284 | 18.07 | 3916 | 0.094 | 0.616 | 0.167 | 0.217 | 0.074 | 0.213 | 0.177 | 23.4 | 0 |
| grid-s1f-R4-G512 | voxels 512^3 (0.5 Mpc/h) | 0.00390625 | phys 10 | 1311 / 1284 | 14.00 | 2517 | 0.060 | 0.584 | 0.122 | 0.294 | 0.043 | 0.173 | 0.118 | 15.1 | 0 |
| grid-s1f-R4-G512 | voxels 512^3 (0.5 Mpc/h) | 0.00390625 | eps 0.01 | 1311 / 1284 | 14.88 | 2780 | 0.067 | 0.586 | 0.129 | 0.285 | 0.048 | 0.181 | 0.130 | 16.6 | 0 |
| grid-s1f-R4-G512 | voxels 512^3 (0.5 Mpc/h) | 0.0078125 | faces 1 | 1311 / 1284 | 18.07 | 3490 | 0.168 | 0.568 | 0.201 | 0.230 | 0.129 | 0.262 | 0.257 | 22.8 | 0 |
| grid-s1f-R4-G512 | voxels 512^3 (0.5 Mpc/h) | 0.0078125 | phys 10 | 1311 / 1284 | 14.00 | 2131 | 0.102 | 0.532 | 0.143 | 0.325 | 0.069 | 0.211 | 0.168 | 13.9 | 0 |
| grid-s1f-R4-G512 | voxels 512^3 (0.5 Mpc/h) | 0.0078125 | eps 0.01 | 1311 / 1284 | 14.88 | 2413 | 0.116 | 0.532 | 0.169 | 0.299 | 0.081 | 0.241 | 0.191 | 15.8 | 0 |
| zones-smooth-131k | Voronoi tracers, smooth, 131072 tracers | 0.001953125 | faces 0 | 804 / 791 | 18.43 | 2987 | 0.059 | 0.619 | 0.323 | 0.058 | 0.055 | 0.343 | 0.144 | 74.7 | 0 |
| zones-smooth-131k | Voronoi tracers, smooth, 131072 tracers | 0.001953125 | eps 0.01 | 804 / 791 | 16.72 | 2645 | 0.052 | 0.620 | 0.312 | 0.068 | 0.048 | 0.334 | 0.130 | 66.1 | 0 |
| zones-smooth-131k | Voronoi tracers, smooth, 131072 tracers | 0.00390625 | faces 0 | 804 / 791 | 18.43 | 2804 | 0.110 | 0.563 | 0.373 | 0.064 | 0.103 | 0.398 | 0.224 | 70.1 | 0 |
| zones-smooth-131k | Voronoi tracers, smooth, 131072 tracers | 0.00390625 | eps 0.01 | 804 / 791 | 16.72 | 2520 | 0.099 | 0.567 | 0.355 | 0.078 | 0.091 | 0.385 | 0.207 | 63.0 | 0 |
| zones-smooth-131k | Voronoi tracers, smooth, 131072 tracers | 0.0078125 | faces 0 | 804 / 791 | 18.43 | 2564 | 0.202 | 0.471 | 0.433 | 0.097 | 0.182 | 0.479 | 0.331 | 64.1 | 0 |
| zones-smooth-131k | Voronoi tracers, smooth, 131072 tracers | 0.0078125 | eps 0.01 | 804 / 791 | 16.72 | 2311 | 0.182 | 0.493 | 0.401 | 0.106 | 0.162 | 0.448 | 0.305 | 57.8 | 0 |
| zones-smooth-1m | Voronoi tracers, smooth, 1048576 tracers | 0.001953125 | faces 0 | 1259 / 1230 | 19.22 | 9937 | 0.125 | 0.569 | 0.391 | 0.040 | 0.120 | 0.407 | 0.246 | 118.3 | 0 |
| zones-smooth-1m | Voronoi tracers, smooth, 1048576 tracers | 0.001953125 | eps 0.01 | 1259 / 1230 | 16.59 | 7018 | 0.088 | 0.680 | 0.269 | 0.051 | 0.084 | 0.284 | 0.195 | 83.5 | 0 |
| zones-smooth-1m | Voronoi tracers, smooth, 1048576 tracers | 0.00390625 | faces 0 | 1259 / 1230 | 19.22 | 8363 | 0.210 | 0.496 | 0.452 | 0.052 | 0.199 | 0.476 | 0.353 | 99.6 | 0 |
| zones-smooth-1m | Voronoi tracers, smooth, 1048576 tracers | 0.00390625 | eps 0.01 | 1259 / 1230 | 16.59 | 6192 | 0.155 | 0.606 | 0.333 | 0.060 | 0.146 | 0.355 | 0.281 | 73.7 | 0 |
| zones-smooth-1m | Voronoi tracers, smooth, 1048576 tracers | 0.0078125 | faces 0 | 1259 / 1230 | 19.22 | 6845 | 0.343 | 0.408 | 0.513 | 0.079 | 0.317 | 0.557 | 0.469 | 82.5 | 0 |
| zones-smooth-1m | Voronoi tracers, smooth, 1048576 tracers | 0.0078125 | eps 0.01 | 1259 / 1230 | 16.58 | 5261 | 0.264 | 0.514 | 0.405 | 0.081 | 0.243 | 0.440 | 0.399 | 63.4 | 0 |
| zones-zobov-262k | Voronoi tracers, zobov, 262144 tracers | 0.001953125 | faces 0 | 1879 / 1741 | 17.40 | 5718 | 0.050 | 0.512 | 0.321 | 0.167 | 0.041 | 0.385 | 0.114 | 24.2 | 0 |
| zones-zobov-262k | Voronoi tracers, zobov, 262144 tracers | 0.001953125 | eps 0.01 | 1879 / 1741 | 16.01 | 5387 | 0.047 | 0.514 | 0.316 | 0.170 | 0.039 | 0.381 | 0.108 | 22.8 | 0 |
| zones-zobov-262k | Voronoi tracers, zobov, 262144 tracers | 0.00390625 | faces 0 | 1879 / 1741 | 17.40 | 5462 | 0.095 | 0.475 | 0.335 | 0.189 | 0.076 | 0.414 | 0.182 | 23.1 | 0 |
| zones-zobov-262k | Voronoi tracers, zobov, 262144 tracers | 0.00390625 | eps 0.01 | 1879 / 1741 | 16.01 | 5186 | 0.090 | 0.475 | 0.341 | 0.184 | 0.073 | 0.418 | 0.176 | 22.0 | 0 |
| zones-zobov-262k | Voronoi tracers, zobov, 262144 tracers | 0.0078125 | faces 0 | 1879 / 1741 | 17.39 | 5136 | 0.178 | 0.412 | 0.367 | 0.222 | 0.138 | 0.471 | 0.268 | 21.9 | 0 |
| zones-zobov-262k | Voronoi tracers, zobov, 262144 tracers | 0.0078125 | eps 0.01 | 1879 / 1741 | 16.01 | 4906 | 0.170 | 0.417 | 0.370 | 0.213 | 0.133 | 0.470 | 0.261 | 21.0 | 0 |
| zones-zobov-32k | Voronoi tracers, zobov, 32768 tracers | 0.001953125 | faces 0 | 329 / 315 | 17.78 | 829 | 0.040 | 0.492 | 0.391 | 0.117 | 0.036 | 0.443 | 0.099 | 29.6 | 0 |
| zones-zobov-32k | Voronoi tracers, zobov, 32768 tracers | 0.001953125 | eps 0.01 | 329 / 315 | 16.19 | 875 | 0.042 | 0.496 | 0.401 | 0.103 | 0.038 | 0.447 | 0.106 | 31.2 | 0 |
| zones-zobov-32k | Voronoi tracers, zobov, 32768 tracers | 0.00390625 | faces 0 | 329 / 315 | 17.78 | 812 | 0.079 | 0.472 | 0.385 | 0.143 | 0.068 | 0.450 | 0.164 | 29.0 | 0 |
| zones-zobov-32k | Voronoi tracers, zobov, 32768 tracers | 0.00390625 | eps 0.01 | 329 / 315 | 16.19 | 851 | 0.082 | 0.469 | 0.405 | 0.126 | 0.072 | 0.464 | 0.174 | 30.4 | 0 |
| zones-zobov-32k | Voronoi tracers, zobov, 32768 tracers | 0.0078125 | faces 0 | 329 / 315 | 17.78 | 764 | 0.148 | 0.420 | 0.415 | 0.165 | 0.124 | 0.497 | 0.250 | 27.3 | 0 |
| zones-zobov-32k | Voronoi tracers, zobov, 32768 tracers | 0.0078125 | eps 0.01 | 329 / 315 | 16.19 | 803 | 0.156 | 0.427 | 0.428 | 0.144 | 0.133 | 0.501 | 0.261 | 28.7 | 0 |

#### Where the contact changes happen (finest spacing; wall area in units of Vbar^(2/3))

| run | wall rule | group | contact changes | median wall area | share with wall area < 0.01 | share < 0.03 | mean smoothed field on the wall | share near a merge or split (same or adjacent step) | share that change again in an adjacent step | share lost (rest gained) |
|---|---|---|---|---|---|---|---|---|---|---|
| grid-s1f-R4-G256 | faces 1 | alone | 1701 | 0.0018 | 0.945 | 0.986 | 2.087 | 0.060 | 0.036 | 0.487 |
| grid-s1f-R4-G256 | faces 1 | clumped | 546 | 0.0036 | 0.689 | 0.844 | 2.528 | 0.101 | 0.042 | 0.498 |
| grid-s1f-R4-G256 | faces 1 | merge | 627 | 0.0465 | 0.255 | 0.413 | 1.410 | 1.000 | 0.043 | 0.388 |
| grid-s1f-R4-G256 | eps 0.01 | alone | 1582 | 0.0109 | 0.000 | 0.968 | 1.791 | 0.052 | 0.061 | 0.489 |
| grid-s1f-R4-G256 | eps 0.01 | clumped | 369 | 0.0199 | 0.000 | 0.626 | 1.715 | 0.095 | 0.030 | 0.504 |
| grid-s1f-R4-G256 | eps 0.01 | merge | 586 | 0.0875 | 0.000 | 0.239 | 1.163 | 1.000 | 0.036 | 0.391 |
| grid-s1f-R4-G512 | faces 1 | alone | 2681 | 0.0005 | 0.984 | 0.996 | 2.302 | 0.066 | 0.091 | 0.502 |
| grid-s1f-R4-G512 | faces 1 | clumped | 612 | 0.0009 | 0.812 | 0.889 | 2.628 | 0.155 | 0.108 | 0.471 |
| grid-s1f-R4-G512 | faces 1 | merge | 829 | 0.0278 | 0.351 | 0.511 | 1.717 | 1.000 | 0.090 | 0.510 |
| grid-s1f-R4-G512 | eps 0.01 | alone | 1940 | 0.0105 | 0.000 | 0.987 | 1.652 | 0.073 | 0.231 | 0.513 |
| grid-s1f-R4-G512 | eps 0.01 | clumped | 364 | 0.0159 | 0.000 | 0.676 | 1.723 | 0.157 | 0.154 | 0.481 |
| grid-s1f-R4-G512 | eps 0.01 | merge | 789 | 0.0933 | 0.000 | 0.276 | 1.236 | 1.000 | 0.089 | 0.513 |
| zones-smooth-131k | faces 0 | alone | 1849 | 0.0014 | 0.813 | 0.939 | 3.289 | 0.025 | 0.140 | 0.491 |
| zones-smooth-131k | faces 0 | clumped | 964 | 0.0074 | 0.548 | 0.739 | 3.126 | 0.040 | 0.082 | 0.494 |
| zones-smooth-131k | faces 0 | merge | 174 | 0.0563 | 0.178 | 0.368 | 1.856 | 1.000 | 0.006 | 0.460 |
| zones-smooth-131k | eps 0.01 | alone | 1640 | 0.0155 | 0.000 | 0.814 | 2.784 | 0.033 | 0.118 | 0.505 |
| zones-smooth-131k | eps 0.01 | clumped | 824 | 0.0272 | 0.000 | 0.530 | 2.338 | 0.040 | 0.052 | 0.498 |
| zones-smooth-131k | eps 0.01 | merge | 181 | 0.0888 | 0.000 | 0.249 | 1.722 | 1.000 | 0.022 | 0.470 |
| zones-smooth-1m | faces 0 | alone | 5655 | 0.0003 | 0.938 | 0.982 | 3.559 | 0.043 | 0.275 | 0.494 |
| zones-smooth-1m | faces 0 | clumped | 3888 | 0.0006 | 0.834 | 0.915 | 4.783 | 0.043 | 0.289 | 0.503 |
| zones-smooth-1m | faces 0 | merge | 394 | 0.0257 | 0.350 | 0.525 | 2.339 | 1.000 | 0.079 | 0.396 |
| zones-smooth-1m | eps 0.01 | alone | 4772 | 0.0128 | 0.000 | 0.911 | 2.604 | 0.038 | 0.235 | 0.498 |
| zones-smooth-1m | eps 0.01 | clumped | 1890 | 0.0174 | 0.000 | 0.705 | 2.608 | 0.039 | 0.167 | 0.507 |
| zones-smooth-1m | eps 0.01 | merge | 356 | 0.0773 | 0.000 | 0.292 | 1.534 | 1.000 | 0.045 | 0.404 |
| zones-zobov-262k | faces 0 | alone | 2930 | 0.0019 | 0.734 | 0.902 | 109.642 | 0.066 | 0.111 | 0.498 |
| zones-zobov-262k | faces 0 | clumped | 1834 | 0.0169 | 0.397 | 0.606 | 56.890 | 0.051 | 0.051 | 0.489 |
| zones-zobov-262k | faces 0 | merge | 954 | 0.1077 | 0.180 | 0.301 | 16.719 | 1.000 | 0.013 | 0.303 |
| zones-zobov-262k | eps 0.01 | alone | 2769 | 0.0173 | 0.000 | 0.754 | 23.562 | 0.077 | 0.090 | 0.512 |
| zones-zobov-262k | eps 0.01 | clumped | 1702 | 0.0422 | 0.000 | 0.399 | 11.722 | 0.046 | 0.040 | 0.492 |
| zones-zobov-262k | eps 0.01 | merge | 916 | 0.1656 | 0.000 | 0.158 | 7.670 | 1.000 | 0.016 | 0.293 |
| zones-zobov-32k | faces 0 | alone | 408 | 0.0027 | 0.691 | 0.877 | 16.992 | 0.037 | 0.051 | 0.542 |
| zones-zobov-32k | faces 0 | clumped | 324 | 0.0228 | 0.312 | 0.565 | 9.535 | 0.040 | 0.028 | 0.506 |
| zones-zobov-32k | faces 0 | merge | 97 | 0.0757 | 0.237 | 0.299 | 1.971 | 1.000 | 0.021 | 0.392 |
| zones-zobov-32k | eps 0.01 | alone | 434 | 0.0193 | 0.000 | 0.721 | 7.783 | 0.041 | 0.067 | 0.523 |
| zones-zobov-32k | eps 0.01 | clumped | 351 | 0.0450 | 0.000 | 0.373 | 3.310 | 0.037 | 0.020 | 0.499 |
| zones-zobov-32k | eps 0.01 | merge | 90 | 0.1451 | 0.000 | 0.078 | 1.772 | 1.000 | 0.022 | 0.378 |

#### Top clump patterns (finest spacing, native wall rule)

- grid-s1f-R4-G256 (faces 1): born 0 died 0 lost 1 gained 1 x70; born 0 died 0 lost 2 gained 0 x38; born 0 died 0 lost 0 gained 2 x33; born 0 died 1 lost 0 gained 1 x20; born 0 died 1 lost 0 gained 2 x15
- grid-s1f-R4-G512 (faces 1): born 0 died 0 lost 1 gained 1 x85; born 0 died 0 lost 0 gained 2 x53; born 0 died 0 lost 2 gained 0 x36; born 0 died 1 lost 0 gained 1 x32; born 0 died 1 lost 0 gained 2 x15
- zones-smooth-131k (faces 0): born 0 died 0 lost 2 gained 0 x83; born 0 died 0 lost 0 gained 2 x83; born 0 died 0 lost 1 gained 1 x69; born 0 died 0 lost 2 gained 1 x17; born 0 died 0 lost 1 gained 2 x14
- zones-smooth-1m (faces 0): born 0 died 0 lost 1 gained 1 x345; born 0 died 0 lost 2 gained 0 x309; born 0 died 0 lost 0 gained 2 x298; born 0 died 0 lost 2 gained 1 x78; born 0 died 0 lost 1 gained 2 x77
- zones-zobov-262k (faces 0): born 0 died 0 lost 0 gained 2 x134; born 0 died 0 lost 2 gained 0 x132; born 0 died 0 lost 1 gained 1 x123; born 0 died 1 lost 0 gained 1 x40; born 0 died 0 lost 2 gained 1 x39
- zones-zobov-32k (faces 0): born 0 died 0 lost 2 gained 0 x26; born 0 died 0 lost 0 gained 2 x23; born 0 died 0 lost 1 gained 1 x15; born 0 died 1 lost 0 gained 1 x9; born 0 died 1 lost 0 gained 2 x8

#### Neighbours per basin against the wall rule: a wall counts if its area >= eps * Vbar^(2/3) (mean over snapshots)

| tiling | eps 0 | eps 0.001 | eps 0.002 | eps 0.005 | eps 0.01 | eps 0.02 | eps 0.05 |
|---|---|---|---|---|---|---|---|
| Poisson-Voronoi (N = 8000, 8 seeds) | 15.551 +- 0.009 | 15.117 +- 0.006 | 14.933 +- 0.006 | 14.573 +- 0.007 | 14.158 +- 0.005 | 13.537 +- 0.005 | 12.274 +- 0.007 |
| grid-s1f-R4-G256 | 17.44 | 17.44 | 16.74 | 16.22 | 15.25 | 14.13 | 12.46 |
| grid-s1f-R4-G512 | 18.07 | 17.21 | 16.73 | 15.77 | 14.88 | 13.83 | 12.12 |
| zones-smooth-131k | 18.43 | 17.96 | 17.73 | 17.26 | 16.72 | 15.92 | 14.40 |
| zones-smooth-1m | 19.22 | 18.39 | 18.02 | 17.31 | 16.59 | 15.59 | 13.91 |
| zones-zobov-262k | 17.40 | 16.98 | 16.80 | 16.44 | 16.01 | 15.33 | 14.06 |
| zones-zobov-32k | 17.78 | 17.36 | 17.16 | 16.69 | 16.19 | 15.50 | 14.13 |

## Limits
- The simulation is particle-mesh: force resolution about 0.5 Mpc/h, one 256 Mpc/h box. The basins are watershed basins at a fixed
  smoothing, not the hierarchical ZOBOV/VIDE voids, chosen so that they tile space and nesting plays no part.
- A voxel tiling is not a generic tiling. Several basins can meet along voxel edges, and one voxel can change two contacts at once. So
  the void data cannot test Theorem 1′ in its exact form; they measure how close a real-looking tiling comes.
- The finest spacing, Delta a = 1/512, is the PM step itself, so no finer snapshots exist without a finer run. Counts of contact
  changes depend on the spacing; the share alone and the per-merge ratio are the quantities to compare.
- One run was stopped and replaced: the toy N = 1000 event run on the smaller compute machine made no visible progress in 68 minutes
  on a shared, overloaded host. Its output went to /dev/null, so the log had no PROGRESS lines. The lattice control was rerun on the
  larger host, and the neighbour count was measured directly at N = 512-8000 (toy_static.py), which is all that run would have added.
  Guard for next time: pipe job output through grep PROGRESS, never to /dev/null.

## Leads
- Done (follow-up): grid refinement and Voronoi (particle) basins; the clumping is the discreteness of the units. Next, if wanted: a
  third voxel size (768^3, about 25 GB per worker) to test that the excess falls linearly with voxel size.
- Done (follow-up): clumps change again about as often as single changes, sit on small walls, and are rarely at merges.
- Comparison table (plan Section 4) gets these candidate numbers:
  - void basins: contact changes per merged basin about 25;
  - toy power diagram: 15.9 per birth or death (31.8 per death);
  - grain growth: 16.9 per vanishing grain (Wakai et al. 2001);
  - null-model study: 29.78 contact changes per birth in a swept 4D Poisson-Voronoi.

## Files
- scripts/toy_foam.py (toy, exact events, adapter to the shared logger); test_toy.py (independent checks: ALL OK); toy_check.py;
  toy_coarse.py (fixed-step sampling curve); toy_static.py (neighbours by N).
- scripts/nbody_pm.py (pmwd run); void_basins.py (basins, contacts, tracking, logger); summarise.py (tables).
- Follow-up: grid_refine.py, basin_events.py, nbody_tracers.py, tracer_zones.py, pv_walls.py, summarise_followup.py; results/grid-*.json,
  zones-*.json, pv-walls.json, toy-coarse-voronoi-fine.json.
- results/*.json: every number above. The density grids (about 6-8 GB per run) stay on the compute machine and are not in git.
- The event logger studies/2026-11-15-event-logger/scripts/eventlog.py is imported unchanged.
