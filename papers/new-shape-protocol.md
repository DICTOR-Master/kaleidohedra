# New-shape protocol (18 Nov 2026)

DICTO, 18 Nov 2026: "it is a new shape, it needs to be hit with everything that we ever do or find out about new shapes, where it fits in our studies exactly; if none, create."

No written procedure existed. This list collects every analysis the studies apply to a new shape. Its starting point is the Concordance's nine tests (`concordance.json` → `tests`). The first run is `studies/2026-11-18-fair-die-full`, whose scripts `s01`–`s07` are templates for each step.

**Rules for every step.** Work in a new dated study folder. Run on a compute machine and never on the interface machine. Every script carries controls (Kelvin's truncated octahedron, μ = 3/2, is the default control shape) and ends `FINAL ok` only if they pass. Label each result exact, certified or computed. If a test is outside its competence, write "n/a" and give the reason. Credit every borrowed method at the point of use. On novelty, write "not found in the sources checked", never "new".

| # | Question | Reuse | Output | Pass/fail control |
|---|---|---|---|---|
| 1 | What is it, exactly? | sympy; `fdlib.minpoly_of` (resultant method) | corner coordinates, minimal polynomials of its parameters | parameter recomputed from its definition to 50+ digits; matches the earlier study |
| 2 | What are its counts, symmetry group and orbits (isogonal? isohedral?) | `s01` step 2; `_lib/geomcheck.py` | V, E, F, Euler; group order; orbits of corners, edges and faces | Kelvin TO gives the same counts and orbits |
| 3 | Is it a known solid? | `s01` step 3; congruence by corner matching (rule: matching corners, not a resemblance) | similarity invariant (e.g. a ratio of parallel edges); screen against uniform, Johnson, Catalan, zonohedron and parallelohedron | control shape passes as itself |
| 4 | Is it a station of its family line? | `s01` step 4; the station list of the line's studies; definitions in `law-giving-census` | gcd of minimal polynomials with every named station; forced (P/E/X) or a crossing | at least one known station is re-found |
| 5 | Where do the turn and the swap send it? | `turn-theorem` closed form for t_min | partners, t_min, gap to the turn's maximum | Kelvin t_min = 3/2 |
| 6 | Volume, area, IQ, Mahler product, canonical form Ω = 3!·vol(polar) | `mahler-sweep`, `canonical-sweep`, `solids-canonical` | closed forms, exact at the shape | closed forms equal the hull at 5 or more sample points |
| 7 | Dehn invariant | exact Σ L ⊗ θ; `dehn-screen/scripts/dehn.py` (PSLQ) | coefficient; zero or not | cube and TO give zero, octahedron nonzero |
| 8 | Harmonic fingerprint (Q4/Q8, Q6, Ŵ) | `harmonic-fingerprint`, `_lib/methods.py` Q3d/W6; exact Q4 by the cubic invariant when the group is Oh | Q_l for l = 4…16 from the corners (and from face normals weighted by solid angle when landing matters) | fcc, bcc and icosahedron classical values |
| 9 | Does it tile alone? | Dehn (step 7) decides "no" (Debrunner 1980); if Dehn is zero, forced-sector search (`_lib/methods.py` sector_candidates, `tetra-sweep`) | yes / no / candidate tilings | calibrated on cube, RD, TO |
| 10 | Does it tile with partners (swap pair, octahedra, its line's mates)? | `_lib/methods.py` overlap; exact volume identity | tiling or not | an over-sized partner must overlap |
| 11 | Foam wall area (only if step 9 or 10 tiles) | `mahler-sweep` foam test | W per unit volume | Kelvin W = 1.67404 |
| 12 | Interlocking (only if the tiling has a flat one-tile-thick layer) | `interlock`, HexOct slab tests | locked / free | n/a otherwise, with the reason |
| 13 | Halves: is a turned half convex (ortho/gyro)? | `halves/scripts/sweep_twist.py` twist | convex / dented for each axis | the CO turned 60° is convex (J27); the TO is dented |
| 14 | Vacuus census | `dicto-vacuus`, `non-heart-vacuus` | fins, struts, isofin, rational-π (exact: 2cos θ must be an algebraic integer), kind (heart / inherited heart / non-heart) | CO fin 60° gives integral; cube fin gives non-integral |
| 15 | Origami nets | `vacuus-origami` | fan angle per face kind (< 360° folds), number of nets | fan angles recomputed from the fins |
| 16 | Centre pyramids | `pyramid-tilings`, `rt-pyramids`, `cuboctahedron-pyramids` | volumes, solid angles, Dehn of each pyramid, tilings | the cube's pyramid has Dehn zero |
| 17 | Field / 4D-host test: can it be a shadow, section or corner subset of the 600-cell, 120-cell, 24-cell …? | `s05` | degree of an affine invariant against [K:Q] of the host's field | Kelvin TO (rational) passes |
| 18 | Densest packing | none yet (Betke–Henk 2000 is in the library) | — | n/a until a script exists |
| 19 | Prior art and name | full text of the reference library (`s07`), OEIS digit search, `novelty-searches`, McCooey (blocked: `mccooey-comparison`), rules on known names | sources checked, each with what it says | a known control term is found |
| 20 | Placement | Concordance `tests` and `papers`, `apps-census/data/census.json` | Concordance patch JSON (never edit concordance.json directly; no placeholder names in it), papers, books, one app home (no crossover) | every proposed cell holds a checked value |
| 21 | Render and model | render standard (solid faces, see-through shell, pull-apart, DICTO mark); STL if buildable | figure; print file | figure script checks the geometry |

**Closing the study.** Put Question and Answer first in the README. Add one results row per step. Then give the placement, then the LEADS. Commit only the study folder.
