# The Heptagonal Queen: a heptagonal construction of a 600-cell (18 Nov 2026)

DICTO · dictospheres.com

**DICTO's proposal (approved 18 Nov 2026):** "a heptagonal construction of a 600[-cell], our own deconstruction". The queens-construct study took the 600-cell (the White Queen) apart into five orbits of the 5-cell's symmetry group S5 in sum-zero R⁵. This study runs the same construction with the heptagon in place of the pentagon. The setting is sum-zero R⁷ (a 6-dimensional space), with S7 permuting the coordinates and entries from the heptagon's field. Computation was done with Claude (Anthropic). Serves aim 2 (geometry gives laws) and the fair-die thread of God's Dice.

Labels: **exact** (integer arithmetic in the field, symbolic algebra, or a proof), **computed** (floating point). No label is upgraded.

## Answer

**The heptagon builds the Queen's frame, but not the Queen.** Four findings:

1. **The construction exists, and it is unique** (exact). The heptagon's side and diagonals are 1, ρ = 2cos(π/7) and σ = ρ² − 1. Use them as the gaps between the sorted coordinates, as φ and 1 are used in the golden case. Exactly one pair of orbits then shares a sphere, as A and B do in the 600-cell:
   - **A_h** = perms(0, ρ, ρσ, σ², σ², σ², σ²): 210 corners, a heptagonal cantitruncated 6-simplex.
   - **B_h** = perms(0, 1, 1, ρ², ρ², σ², σ²): 630 corners, a heptagonal stericantellated 6-simplex.

   B_h's gaps are A_h's gaps in reverse order, set on alternate nodes, which is exactly the golden pattern of A and B. Their union with the mirror images is the **Heptagonal Queen candidate Q_h** (1680 corners).
2. **No hidden symmetry, for any choice** (exact, by a theorem, and confirmed by computation). Every finite set in sum-zero R⁷ that S7 maps to itself has symmetry group S7 or S7 × {±1}. This holds for any entries, heptagonal or not. Q_h has |G| = 10080 and two kinds of corner. The 600-cell's construction works because the reflection group H4 contains A4. No finite reflection group of rank 6 contains A6. There is also no root orbit (C3) on Q_h's sphere.
3. **Hull** (exact facets). Q_h has f-vector 1680 / 20160 / 62020 / 78750 / 42938 / 7728, with 18 kinds of facet. Its only walls are the 21 S7 mirrors. 210 of its 42938 ridges lie on them.
4. **Die and line: none of the five targets appears.**
   - The fair die and the truncated cube are **ruled out by field degree** for every projection or section defined over Q(c), whatever the polytope.
   - Kelvin's truncated octahedron, the cuboctahedron and the rhombic dodecahedron are **not found**. The search covered every cubic-symmetric shadow, central section and corner layer of the candidates.

## Construction (exact; scripts/s1_symmetry.py, data/s1_symmetry.log, FINAL ok)

**The golden pattern.** In the 600-cell (queens-construct study), A = perms(0, φ, φ², φ², φ²) and B = perms(0, 1, 1, φ², φ²). Read as gaps between sorted coordinates (Dynkin labels up to the diagram flip):
- A has gaps (φ, 1) on two adjacent nodes;
- B has the reversed gaps (1, φ) on alternate nodes;
- both end at φ² = 1 + φ, the sum of side and diagonal.

C3 is φ times the A4 roots.

**The heptagonal pattern.** The heptagon has three lengths: side 1, short diagonal ρ, long diagonal σ. They obey ρ² = 1 + σ, ρσ = ρ + σ and σ² = 1 + ρ + σ (Steinbach 1997, "golden fields"; checked exactly). σ² is the analogue of φ²: the sum of all three lengths. ρ² = 2 + 2c with c = cos(2π/7), so Q(ρ) = Q(c), the field of the fair die.

**The search.** We tried all 120 "truncation-type" orbits: the three lengths in any order as gaps on any three of the six nodes. They fall into 59 spheres. Each of 58 spheres holds only an orbit and its mirror image. **Exactly one sphere holds two different orbits**, A_h (gaps ρ, σ, 1 on adjacent nodes) and B_h (gaps 1, σ, ρ on alternate nodes), with their mirror images. Among all 4095 orbits with gaps in {0, 1, ρ, σ} (1954 spheres), that sphere still holds only these four.

The radius is |x − mean|² = 2(−1 + 2ρ + 3ρ²) = 24.6896 (float). The two hulls are combinatorially the uniform cantitruncated and stericantellated 6-simplexes: f-vectors 210/630/805/560/210/35 and 630/3150/5040/3465/1050/105, which match the uniform rows in Wikipedia's "Uniform 6-polytope" table.

**No C3.** A scaled root orbit k(eᵢ − eⱼ) would lie on the sphere only if k² = −1 + 2ρ + 3ρ². Its norm polynomial y⁶ − 14y⁴ + 21y² − 7 is irreducible, so no such k exists in Q(ρ). No orbit with one or two nonzero gaps, drawn from 82 field values up to 5.5, lies on the sphere either.

| set | corners | symmetry group order | corner kinds | hull f-vector (f0…f5) |
|---|---|---|---|---|
| 600-cell = A ∪ −A ∪ C3 ∪ B ∪ −B (control, R⁵) | 120 | **14400 (H4)** | 1 (vertex-transitive) | 120/720/1200/600 |
| A alone (control) | 20 | 120 = \|S5\| | 1 | 20/40/30/10 |
| perms(0,1,1,3,3) ∪ negative (control) | 60 | 240 = \|S5 × ±1\| | 1 | – |
| A_h | 210 | 5040 = \|S7\| | 1 | 210/630/805/560/210/35 |
| B_h | 630 | 5040 | 1 | 630/3150/5040/3465/1050/105 |
| A_h ∪ B_h | 840 | 5040 | 2 | – |
| A_h ∪ −A_h | 420 | 10080 = \|S7 × ±1\| | 1 | – |
| B_h ∪ −B_h | 1260 | 10080 | 1 | – |
| **Q_h = A_h ∪ −A_h ∪ B_h ∪ −B_h** | **1680** | **10080** | **2 (420 + 1260)** | **1680/20160/62020/78750/42938/7728** |

Method: the symmetry group is the set of all linear isometries that map the set to itself. We enumerate them by backtracking on the images of a base of corners. Every inner-product condition is an exact integer test in the field, and each candidate map is verified on every corner by its inner-product signature. The control finds H4 (order 14400) and the 600-cell's 720 edges.

Q_h is far from regular:
- a corner sees 53 (A_h) or 59 (B_h) distinct inner products, against 9 in the 600-cell;
- the shortest edge (length √2) joins only 2100 pairs, and the corners have degree 2 or 4 in that graph.

## Why there is no hidden symmetry (exact proof)

Let G be the symmetry group of any finite set in sum-zero R⁷ that S7 maps to itself.
1. G is finite, fixes the centroid 0, and contains S7 = W(A6), which is generated by reflections.
2. The reflections in G generate a normal subgroup R, and R contains W(A6). So R is a finite irreducible reflection group of rank 6.
3. By the classification (Coxeter 1934), R is A6, B6, D6 or E6, of orders 5040, 46080, 23040 and 51840. Non-crystallographic groups (H3, H4, I2(p)) exist only up to rank 4. Only 5040 is divisible by 5040, so R = W(A6).
4. G normalises R, so G permutes the root lines of A6. Hence G ⊆ Aut(A6) = W(A6) × {±1}, of order 10080.
5. Corollary: the reflections in G are only the 21 transpositions. So the reflection closure of any orbit not made of roots is infinite. The 600-cell is the closure of A (120 corners).

The same test in rank 4 finds A4 ⊂ H4 (120 divides 14400), which is the 600-cell. A4 lies in no other rank-4 group: D4, B4 and F4 have orders 192, 384 and 1152. So φ is exactly what the pentagon needs, and **the heptagon has no H4.** In ranks 5 and 6, A5 and A6 lie in no larger group. The next cases are A7 ⊂ E7 and A8 ⊂ E8 (known; see LEADS).

## Hull and walls (exact facets; scripts/s2_hull.py, data/s2_hull.log, FINAL ok)

How the hull was computed:
- qhull gives the facets as corner sets.
- Each facet kind is certified exactly. Its normal comes from an exact rational null space over Q(ρ), and every corner is checked to lie on one side.
- The face lattice is built from one representative per orbit under the exact group.
- Euler's relation Σ(−1)ᵏfₖ = 0 holds for all three hulls.

Control: the golden truncated 5-cell A gives f = 20/40/30/10, as in queens-construct.

**Q_h's 18 kinds of facet** (corners per facet × number of facets):

100×42, 30×14, 18×70, 18×140, 15×840, 15×280, 14×210, 14×210, 12×210, 12×840, 12×420, 11×840 (three kinds), 10×42, 8×1260, 8×210, 7×420.

- The 42 largest facets are perpendicular to the roots eᵢ − eⱼ. Each holds 40 corners of ±A_h and 60 of ±B_h, so these are the only facets where the two orbits meet in bulk.
- A_h's own 30-corner and 10-corner facets survive in Q_h (14 and 42 of them). Its 120-corner facets are cut away.
- No facet normal points at a corner of Q_h. In the 600-cell, every wall is perpendicular to a corner.

**Walls**, by the method of the walls study: the plate of a ridge is the central hyperplane through it.

| solid | ridges | on a mirror | plate perpendicular to a corner of Q_h | on neither |
|---|---|---|---|---|
| golden A (control, R⁵) | 30 | 30 H4 mirrors (10 of them S5 mirrors) | 30 | 0 |
| ordinary orbit (φ², φ², φ², 3/2, 0) (control) | 30 | 10 | 10 | 20 |
| A_h | 210 | 21 (S7 mirrors) | 0 | 189 |
| B_h | 1050 | 21 | 0 | 1029 |
| Q_h | 42938 | 210 | 0 | 42728 |

By the theorem, the 21 S7 mirrors are the only mirrors any of these sets can have. A_h therefore behaves like the ordinary golden orbit, not like A: almost all of its plates lie in no wall.

## Die and line test (scripts/s3_shadows.py, data/s3_shadows.log, FINAL ok)

**Targets:**
- the fair die P(μ_f), μ_f = 1 + √(2T), T = tan(π/14)tan(2π/7);
- Kelvin's truncated octahedron P(3/2);
- the cuboctahedron P(2);
- the truncated cube P(1 + √2);
- the rhombic dodecahedron.

**1. Field degree (exact; covers every polytope with corners in Q(c), not only the candidates).** Take any 3D shadow by a linear map with entries in Q(c), or any section by a flat defined over Q(c). Its corners have coordinates in Q(c), so every affine ratio of it lies in Q(c), a cubic field.
- The die's affine ratio b/(1 − b), with b = μ_f − 1 = √(2T), has degree 6 (b⁶ − 18b⁴ − 4b² + 8 is irreducible). The ratio of parallel edges in a hexagon of the die is b/(1 − b).
- The truncated cube's ratio a = √2 − 1 has degree 2, and a cubic field has no element of degree 2.

So **neither can be such a shadow or section, up to any affine map.**

With one square root √d adjoined (d in Q(c)):
- the die needs Q(c, √d) = Q(c, √(2T));
- the truncated cube needs d = 2 × (a square).

These maps were **not searched**.

**2. Cubic-symmetric search (computed; exact where noted).**
- S4 has exactly five faithful actions on 7 points, up to conjugacy: 4+1+1+1, 4+2+1, 4+3, 6+1 (edges of a tetrahedron) and 6+1 (cosets of C4).
- In each action, exactly one 3-dimensional irreducible occurs, with multiplicity 1. So the cubic-symmetric 3-space W and its projection are unique and defined over Q (exact character count). The three actions with a 4-block share the same W.
- For A_h, B_h, ±A_h, ±B_h and Q_h we computed: the shadow on W, the central section by W, and every corner layer parallel to W (the sets of corners in one translate of W, as in Coxeter's Table V). That is 50 shadows and sections and 1755 layers with 3D extent.

Controls:
- the 600-cell's corner layer through the centre, perpendicular to a cell centre, is a cuboctahedron (Coxeter, Table V);
- the 24-cell's vertex-first shadow is a rhombic dodecahedron;
- P(3/2), P(2), P(1 + √2) and P(μ_f) are recognised, with μ read back;
- perms(0,1,1,3), which has unequal edges, is not taken for a cuboctahedron.

Note: the 600-cell's solid central section there is not a cuboctahedron (84 corners). Coxeter's table lists corner layers.

| target | verdict | searched |
|---|---|---|
| fair die μ_f | **ruled out by field degree** (any polytope over Q(c), any map over Q(c)); also not found in the search | as in 1 and 2 |
| truncated cube 1 + √2 | **ruled out by field degree**; not found | as in 1 and 2 |
| Kelvin truncated octahedron 3/2 | **not found** | 2 |
| cuboctahedron 2 | **not found** | 2 |
| rhombic dodecahedron | **not found** | 2 |

**What did appear** (computed):
- 4-block actions:
  - the shadows of ±A_h and Q_h are centrally symmetric solids with 32 corners (6 squares + 12 hexagons);
  - B_h's central section has 24 corners on one sphere with 6 squares + 8 hexagons. It is a truncated octahedron with only tetrahedral symmetry (two kinds of hexagon), so it is not on the line.
- 6+1 actions:
  - every shadow, and every section of the centrally symmetric sets and of B_h, has the combinatorics of a truncated cuboctahedron (48 corners, on one sphere, unequal edges);
  - **A_h's central section is a cube** (equal edges, the line's end μ = 3, not a target).
- Corner layers: octahedra (μ = 1, 135 layers), tetrahedra, truncated tetrahedra, cantellated tetrahedra with unequal edges, and 8-corner hexahedra with unequal edges.

## Prior art and sources checked (18 Nov 2026)

- **P. Steinbach, "Golden fields: a case for the heptagon", Math. Mag. 70 (1997) 22–31.** Citation verified from the bibliography of arXiv:2408.13125 (a survey of de Casteljau's work), which also cites Steinbach, "Sections beyond golden", Bridges 2000, 35–44. We did not read the paper itself (JSTOR did not load). Credited for ρ, σ as the heptagon's golden numbers and the identities used.
- Koca, Koca, Al-Ajmi 2011/12 (library, bridges/; arXiv:1106.2957): the five S5 orbits of the 600-cell, through the queens-construct study.
- Library search (MANIFEST files) for heptagon / 7-fold / Klein quartic / duoprism / Coxeter plane / non-crystallographic. Relevant hits, abstracts read:
  - Ozdes Koca, Al-Siyabi, Koca, Koc 2018, "Prototiles and tilings from Voronoi and Delone cells of the root lattice A_n" (arXiv:1811.12176). 7-fold tilings come from the A6 Coxeter plane: the heptagon enters A6 through its Coxeter plane, as a planar projection, not through a larger symmetry.
  - Ozdes Koca, Koca, Al Reasi 2026, "Tiles from projections of the root and weight lattices of A_n" (arXiv:2604.10574).
  - Twarock, Valiunas, Zappa 2015, "Orbits of crystallographic embedding of non-crystallographic groups" (title only).

  None constructs heptagonal S7 orbits on one sphere.
- Wikipedia, read 18 Nov 2026:
  - "Coxeter group": classification; orders of A6, B6, D6, E6; non-crystallographic only H3, H4, I2(p).
  - "Uniform 6-polytope": cantitruncated and stericantellated 6-simplex counts, matching ours.
  - "Duoprism": the 7-7 duoprism is 4D, 49 corners, symmetry order 392. Its 7-fold symmetry is not S7.
  - "Klein quartic": the map {3,7}₈, symmetry 168 (336), has no convex Euclidean realisation.
  - "Order-7 tetrahedral honeycomb": {3,3,7} is hyperbolic.
- Not opened: Coxeter, Regular Polytopes (Table V cited through the coordinator's note and our control); Humphreys, Reflection Groups and Coxeter Groups; Conway–Sloane SPLAG (E8 in A8 coordinates).

The same-sphere pair A_h, B_h and its uniqueness were **not found in the sources checked**. We do not claim them as new.

## Files

- `scripts/hlib.py`: exact field arithmetic (Q(φ), Q(ρ) as integer coefficient vectors), orbits, exact symmetry-group search.
- `scripts/s1_symmetry.py`: construction, sphere classes, no-C3 proof, group orders with controls.
- `scripts/s2_hull.py`: hulls, certified facets, face lattices, walls.
- `scripts/s3_shadows.py`: field degrees, cubic-symmetric shadows, sections and layers, with controls.
- `data/*.log`: each ends FINAL ok. `data/*.json`: results. `data/*_facet_eqs.npy`: float facet equations.
- All runs were pilots under 1 minute on the compute machine.

## LEADS

1. **The true analogue is E8 ⊃ A8 (and E7 ⊃ A7).** These are the next ranks where S_{n+1} hides in a larger reflection group. The 240 E8 roots are the 72 A8 roots plus two orbits of 84 in sum-zero R⁹ (known; not checked here). This is the "integer Queen". Run the same deconstruction (orbits, walls, cat/steak) there.
2. Search the die over Q(c, √(2T)): projections whose single square root is √(2T), the only door left open by the field-degree argument.
3. Name and draw Q_h's 42 large facets (100 corners each, perpendicular to the roots), where ±A_h and ±B_h meet.
4. Find the heptagonal pairs for other node patterns, outside the truncation type: gaps from sums and powers of ρ and σ, three or more nonzero.
5. The A6 Coxeter-plane projection of Q_h (7-fold picture), in the style of the queens-construct figure.
