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
   - Cause NOT settled: the voxel grid (not a generic tiling) or the physics. Strength: one box, one grid, one void definition.
3. Ratio: about 25 contact changes per basin that merges away; 23-27 over R = 3-6, both seeds and the fine spacings. It is steady as the
   spacing shrinks. Per NET basin lost (z = 3 to 0, R = 4), about 117, because many merges and splits undo one another. Merges are
   not 4-1 deaths: a whole wall dissolves, so a merge carries several contact changes by its nature.
4. Neighbours per void basin: 17.2-18.0 when any shared voxel face counts; 13.7-15.4 when a wall needs 10 faces. The Poisson-Voronoi
   15.54 lies between, and no rule-free number comes out (Aragón-Calvo 2014: about 14).
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
- Grid refinement: the same smoothing on a 512^3 density grid. If the 20% clumped share falls, it is the voxel grid; if it stays, it is
  physics. The same test with Voronoi (particle) basins as in ZOBOV.
- Do the clumps sit where walls flicker? Compare them with the lost-and-regained-next-step contacts.
- Comparison table (plan Section 4) gets these candidate numbers:
  - void basins: contact changes per merged basin about 25;
  - toy power diagram: 15.9 per birth or death (31.8 per death);
  - grain growth: 16.9 per vanishing grain (Wakai et al. 2001);
  - null-model study: 29.78 contact changes per birth in a swept 4D Poisson-Voronoi.

## Files
- scripts/toy_foam.py (toy, exact events, adapter to the shared logger); test_toy.py (independent checks: ALL OK); toy_check.py;
  toy_coarse.py (fixed-step sampling curve); toy_static.py (neighbours by N).
- scripts/nbody_pm.py (pmwd run); void_basins.py (basins, contacts, tracking, logger); summarise.py (tables).
- results/*.json: every number above. The density grids (about 6-8 GB per run) stay on the compute machine and are not in git.
- The event logger studies/2026-11-15-event-logger/scripts/eventlog.py is imported unchanged.
