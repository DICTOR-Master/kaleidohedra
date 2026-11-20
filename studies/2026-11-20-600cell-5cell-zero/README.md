# A 600-cell and 120 5-cells: Dehn invariant zero

Study, 20 Nov 2026. Outside the plan. DICTO approved it "as a study".

**Verdict:** one regular 600-cell of edge a together with **120** regular 5-cells of the same edge a has Dehn invariant zero. 120 is the only equal-edge count, so it is also the smallest. The 5-cells can sit on 120 of the 600-cell's tetrahedral facets as one solid. That solid is star-shaped and **not convex**. Its 120 capped facets use every edge of the 600-cell exactly once and no two of them share a triangle. The apexes of the caps form a larger regular 600-cell of radius √2 (with circumradius 1). The solid's volume is **5√5 φ² a⁴**. By Jessen's theorem, any such union is scissors congruent to a 4-cube of edge **5^(3/8) √φ a ≈ 2.32599 a**. This is an existence result only: no dissection is claimed. **Part 2 (below):** the five cell sets are, by their centres, one state of Coxeter's compound of ten 600-cells in the dual 120-cell, and the five cosets of the binary tetrahedral group in the binary icosahedral group; the tip 600-cell is √2 times one of those ten, and the convex hull of the solid; every ridge of the solid lies on the 600-cell's mirrors.

## Method
- Dehn invariant in 4D (Hadwiger's form for codimension 2): D(P) = Σ over the 2-faces (ridges) of area ⊗ dihedral angle, taken in ℝ ⊗_ℚ ℝ/ℚπ.
- Jessen: in ℝ⁴, two polytopes are scissors congruent if and only if they have equal volume and equal Dehn invariant. This rests on Jessen's algebraic proof of the Dehn–Sydler theorem (Math. Scand. 22, 1968) and was carried to dimension 4 in Jessen, *Zur Algebra der Polytope*, Göttinger Nachr. 1972. Sources: Dupont, *Scissors congruences, group homology and characteristic classes* (2001); Dupont and Sah, *Scissors congruences II*, J. Pure Appl. Algebra 25 (1982); Sah, *Hilbert's third problem: scissors congruence* (1979); Lagarias and Moews, Discrete Comput. Geom. 13 (1995). A cube has invariant 0 because all its angles are π/2.
- The arithmetic is exact. Numbers are held as p + q√5 with p, q rational. The 600-cell is built as the 120 unit quaternions of the binary icosahedral group. Edges, triangles and facets are found by exact inner products. Volumes and the angle identity are checked in sympy. Floats are used only for the symmetry count and for printed values.
- The prior relation θ₆₀₀ = 4π/3 − θ₅ is taken from the prescore study of the same day (checks/relation_600_5.py there) and is re-proved here in sympy.

## Results
1. **Invariants.** Write θ₅ = arccos(1/4). It is not a rational multiple of π, because 2cos θ₅ = 1/2 is not an algebraic integer.
   - 600-cell, edge a: 1200 triangles, total ridge area 300√3 a². The dihedral angle is 4π/3 − θ₅, so D = −300√3 a² ⊗ θ₅ (mod ℚπ).
   - 5-cell, edge b: 10 triangles, total ridge area (5√3/2) b², so D = (5√3/2) b² ⊗ θ₅.
   - One 600-cell plus n 5-cells has D = 0 **iff n b² = 120 a²**. The map x ↦ x ⊗ θ₅ is injective because θ₅ ≠ 0 in ℝ/ℚπ.
   - With equal edges, n = 120: the only and smallest solution. If b/a is rational and n is a whole number, then b/a = 1/q with n = 120q², or b/a = 2/q with q odd and n = 30q². The smallest such n is 30, with b = 2a. If b/a may be irrational, any n works, with b = a√(120/n).
2. **Arrangement.** A 5-cell glued to a facet of edge a is a cap: a pyramid over that tetrahedron.
   - Each cap lies inside the cone from the centre over its own facet, and these cones do not overlap. So any set of caps gives one solid with no self-overlap, and that solid is star-shaped from the centre.
   - The interior angle where a cap meets an uncapped facet is θ₅ + θ₆₀₀ = 4π/3 = 240°. That is more than 180°, so the solid is **not convex**, whichever facets are capped. Where two caps share a triangle the angle would be 4π/3 + θ₅ ≈ 315.52°.
   - **Natural choice:** left multiplication by the 120 vertex quaternions splits the 600 facets into 5 orbits of 120. Take one orbit:
     - no two capped facets share a triangle;
     - each edge of the 600-cell lies in exactly one capped facet, so 120 × 6 = 720 edges;
     - each vertex lies in 4 capped facets;
     - the apexes are at radius exactly √2 (with circumradius 1) and form a regular 600-cell;
     - the solid keeps 1440 of the 600-cell's rotations and no reflections, so it is chiral. Its mirror image comes from the right-multiplication orbits.
     All 5 left orbits pass the same checks.
   - **Direct check of the invariant** from the solid's own boundary: 720 old ridges at 4π/3 − θ₅ give −720. 480 ridges at 4π/3 give 0, since 4π/3 is a rational multiple of π. 720 cap side ridges at θ₅ give +720. The total is 0 · (√3/4)a² ⊗ θ₅.
   - **3D comparison (octet truss):** the octahedron's angle is π − arccos(1/3), so one octahedron plus two tetrahedra has invariant 0. There the two angles add to exactly π, the faces merge flat, and the union can be convex: tetrahedra on two opposite faces give the 60° rhombohedron, which fills space. In 4D the angles add to 4π/3, not π. So the 4D union is never convex, and it is not claimed to fill space.
   - DICTO's earlier 4D work (the 600-cell* as world and paper #63, Walls of Silence #110, the Alicia book) treats the 600-cell's walls, shells and projections. No construction there glues 5-cells onto the facets, in the memory and paper notes checked.
3. **Volumes.**
   - V(600-cell) = (25/4)(2+√5) a⁴ = (25/4)φ³ a⁴ ≈ 26.47542 a⁴.
   - V(5-cell) = (√5/96) a⁴, so 120 of them give (5√5/4) a⁴ ≈ 2.79508 a⁴.
   - Total = (25+15√5)/2 a⁴ = **5√5 φ² a⁴** ≈ 29.27051 a⁴.
   - 4-cube edge = (5√5 φ²)^(1/4) a = **5^(3/8) √φ a ≈ 2.325989 a**.
   - The variant with n = 30 and b = 2a has total (25/2 + 45√5/4) a⁴ ≈ 37.65576 a⁴, and cube edge ≈ 2.477182 a.
4. **Picture:** none made. A projection of a non-convex spiked 4D solid would not show the angle facts, and those facts carry the result.

\* Named the White Queen in DICTO's books.

## Credits
Dehn (1901); Hadwiger (the higher-dimensional invariants, *Vorlesungen über Inhalt, Oberfläche und Isoperimetrie*, 1957); Jessen (1968, 1972); Dupont and Sah (1982), Dupont (2001); Schläfli (the 600-cell, 1852). Computation by DICTO with Claude (Anthropic).

## Prior art (sources checked)
- Web searches: "600-cell" with "5-cell"/"pentachoron" and "Dehn invariant"/"scissors congruent"; "augmented 600-cell"/pentachora capping cells.
- Pages and papers seen: the Encyclopedia of Mathematics entry "Dehn invariant"; Wikipedia "Hilbert's third problem", "600-cell" and "5-cell"; Lagarias–Moews 1995; Calegari's notes on scissors congruence; arXiv 1910.07112, 1410.7120, 2210.08082 and 1710.11247; Banchoff, *Beyond the Third Dimension* §5.8; R. Schwartz's notes on Jessen; Freire's star polychora page.
- Result: the 600-cell + 120 5-cells zero-invariant relation, the edge-partition cap set, and the √2 apex 600-cell were **not found in the sources checked**. The general theory (Jessen's criterion in 4D) is standard.

## Checks (all run on a remote host; logs alongside)
- checks/dehn600.py → checks/dehn600.log: 21 PASS lines, FINAL ok. It covers the counts, the exact dihedral cosine −(1+3√5)/8, the angle identity, irrationality, the n-condition, the orbits, the direct boundary sum, the reflex angle, the apex radius, the volumes, the cube edge, the 3D comparison and the symmetry count.
- checks/apexes.py → checks/apexes.log: FINAL ok. It covers all 5 left orbits (edge partition, no shared triangle, apexes forming a regular 600-cell), the right orbits, and the mirror relation.

## Part 2: against the earlier 600-cell work (20 Nov 2026)

DICTO, 20 Nov: "those 4D questions need to be juxtaposed against our earlier 600-cell work." Each question below is answered from exact checks: checks/part2_queens.py → checks/part2_queens.log, 50 PASS lines, FINAL ok. It imports dehn600.py and uses its coordinates (the 120 unit quaternions of the binary icosahedral group 2I, radius 1, edge 1/φ). Every step is exact: numbers p + q√5 with p, q rational, or integer tables built from exact quaternion products. Run on a remote host in 67 s.

Sources compared: #63, #65, #76 v2, #107, #109, #110 v3, Alicia in Wonderland chapters 9–11, and the studies 2026-11-16-600cell-walls, 2026-11-16-redqueen-cats and 2026-11-17-valley-charge.

Words used here:
- **left sets**: the 5 sets of 120 cells made by left multiplication;
- **right sets**: the 5 made by right multiplication (the mirror choice);
- **centres**: the 600 cell centres;
- **P**: the 600-cell;
- **dual 120-cell**: the 120-cell whose corners are the centres. This is #65's 120-cell, built from the 600-cell's cell centres (checked: nearest centres are exactly the cells that share a triangle, 4 each, 1200 edges).

### 1. Are the 5 sets a known partition? Yes, exactly.
- **Coxeter's compound, one state (confirmed).** The 120 centres of each left set, and of each right set, are the corners of a regular 600-cell. The ten 600-cells are distinct. Every cell is in one left set and one right set, and each left set meets each right set in 24 cells, whose centres form a 24-cell. So the ten sets are, by their centres, the compound of ten 600-cells inscribed in the 120-cell (Coxeter, *Regular Polytopes*, Table VII; Denney et al.), placed in the dual 120-cell. The left sets are one state of five and the right sets the other. This is exactly #110 Theorem B(a), read in the dual 120-cell. In #110's Theorem B′, P is the 600-cell dual to the 120-cell Q, so the centres are Q's corners.
- **Cosets of 2T (confirmed).** The right symmetries of each left set form a binary tetrahedral group 2T of order 24. The five left sets have the five different 2T's, which are conjugate in 2I. The right sets have the same five as left symmetries. Fix one centre c₀ with group T₀. The left set of the centre c₀r⁻¹ depends exactly on the coset rT₀. So the five sets are the five cosets of 2T in 2I. The index 5 and the five conjugates are classical: Coxeter; Conway and Smith, *On Quaternions and Octonions* (2003); Du Val, *Homographies, Quaternions and Rotations* (1964), for rotations as quaternion pairs.
- **Symmetry.** Each set is kept by x ↦ l x r⁻¹ with l in 2I and r in its 2T. That gives 120 × 24 / 2 = 1440 rotations, which equals Part 1's count. So the group is ±[I×T] in Conway and Smith's notation. It is also the stabiliser, inside the 600-cell's group, of one of Coxeter's ten 600-cells.
- **The 24-cell splits (related, not the same partition).** The cosets of the five 2T's give #110 B′(f)'s 10 splits of P into 5 disjoint 24-cells: 25 different 24-cells, each in exactly 2 splits, one of each state. Each left set belongs with one 2T, and through it with one left split and one right split. The two partitions are of different things (cells and corners). Every capped cell has its 4 corners in 4 different 24-cells of every split, so the splits do not tell the cells apart.
- **The S5 orbits behind A, B and C3 (refuted as the same partition; linked exactly).** Four roots in an A4 pattern generate S5 (120 elements). S5 splits the corners 20, 20, 20, 30, 30, as in Koca et al. The orbit that matches #110's A by Gram values is A, and its antipode is −A. S5 does not keep the sets:
  - its 60 rotations permute the five left sets as the full group A5 on five points, so each left set corresponds to one coordinate k;
  - its odd elements swap left sets with right sets;
  - the elements of S5 that keep a left set are exactly 12 rotations, an A4.

  The link: A has exactly 5 tetrahedral cells that are cells of P. The A4 that fixes left set k fixes exactly two cells, A's tetrahedron k and its opposite in −A. Their axis is the normal of C3's cross wall "coordinate k = mean": it carries 12 of C3's 20 corners (#110 Table 1). The 120 A copies in P (A and −A for each of its 60 S5's) have 600 tetrahedra, every cell exactly once. This is the dual form of #110 B′(f), where each corner of Q is in exactly one A* copy. Every A copy takes one tetrahedron from each left set and one from each right set.

### 2. The tip 600-cell (confirmed exactly)
- **Inscribed in the dual 120-cell.** Scaled to radius 1, the tips of a left choice are the centres of that left set. So the tip 600-cell is √2 times one of the ten 600-cells inscribed in the dual 120-cell. It is in the state of left multiplication, and a mirror choice gives a tip 600-cell in the other state.
- **A one-handed turn.** The unit tip 600-cell is P·ĉ, which is P right-multiplied by a unit quaternion (the unit cell centre ĉ). The smallest such turn has cos² = (7+3√5)/16 ≈ 0.85676: the angle from a corner to the nearest cell centre. It is not u·P for any u, because ĉ⁻¹ 2I ĉ ≠ 2I. Mirror choices give ĉ·P, the other hand.
- **The relation runs both ways.** P is inscribed in the tip 600-cell's dual 120-cell: the tip 600-cell's 600 cell centres, at radius 1, include all 120 corners of P. The ten tip 600-cells (5 left choices and 5 mirror choices) have ten different dual 120-cells, each holding P. P is a left orbit of 2I in the five from left choices and a right orbit in the five from mirror choices.
- **These are all the 120-cells that hold P.** A 600-cell lies in exactly 10 of the 120-cells of its size, by #110 B(a) read the other way: both groups have order 14400, and a 120-cell holds 10 600-cells. So the duals of the ten tip 600-cells are all the 120-cells of #110's kind (its Q, Theorem B) that hold P.
- **A nesting, not a compound.** P lies strictly inside the tip 600-cell, inside its insphere, since 2·cc/16 > 1 with cc = 7+3√5. So **the convex hull of the capped solid is the tip 600-cell.** This answers Part 1's lead. The volume ratio of the solid to its hull is 5√5φ² / (25φ³) = 1/(√5 φ) ≈ 0.27639.

### 3. Walls (confirmed exactly)
- **Every ridge plate is a mirror.** #110 defines plates for convex solids; the definition is taken here to this star-shaped solid, about P's centre. Every ridge plate of the solid lies on one of P's 60 mirrors: the 1200 old triangles (#110 Lemma 3a) and all 720 cap side triangles. None lies on a cross wall. Each mirror carries 20 old triangles and 12 cap sides. Each plate carries every ridge together with its opposite, so the solid is of the heart kind (#110 Lemma 1).
- **Pentagons and cap sides pair off.** A cap side triangle (tip, u, v) lies on the mirror perpendicular to the opposite edge wx of its cell. That mirror also carries the pentagon of the dual 120-cell that is dual to wx (#107 Corollary 2), and the tip lies on the ray through one of its corners. So on each mirror, #107's 12 pentagons and the 12 cap sides pair off one to one.
- **Every cap is hidden.** Each cap (a 5-cell) has its 10 two-face plates, about P's centre, on 10 different mirrors. So every cap is hidden in P's mirrors in #110's sense, with the centre stated as #110 requires.
- **The tips.** As points, each tip lies on exactly 6 mirrors and 27 cross walls. The tip 600-cell's own 1200 triangles lie on 60 of P's 300 cross walls, 20 on each: its own mirrors. Conversely, P's 60 mirrors are cross walls of the tip 600-cell. This is #110 Theorem B(c) and Table 4 (an inscribed 600-cell lies on Q's 300 corner-axis walls), seen from the cap side.

### 4. Symmetry against A, B and the duals (refuted exactly)
- The solid has ±[I×T]: 1440 rotations and no reflections.
- A and B have S5 (120 elements, including reflections), and so do their polar duals A*, B* and C3*, since polarity keeps the symmetry group.
- Neither group contains the other. They meet in exactly an A4 of 12 rotations, for every left set and so, by symmetry, for every right set.

### 5. Further connections
- **The octahedron analogue (confirmed, and it shows where 4D differs).**
  - In 3D, the octahedron's 4 alternate faces cover its 12 edges once. Tetrahedra on them give a regular tetrahedron of twice the edge, which is convex, with the caps' tips at its corners. The face centres of one set form a tetrahedron in the dual cube, and the two sets form Kepler's stella octangula.
  - In 4D, the five left sets cover the 720 edges once each. One set's centres form a 600-cell in the dual 120-cell, and the five sets form one state of Coxeter's compound. The capped solid is not convex, and its hull is the tip 600-cell.
  - There are 2 alternate sets in 3D and 5 + 5 here, and here each set is chiral.
- **At one corner.** The 20 cells round a corner are the 20 faces of the icosahedral vertex figure. The left sets split them into 5 sets of 4 faces, each meeting all 12 neighbours once. Their face centres form 5 regular tetrahedra: the compound of five tetrahedra (Hess, 1876) in the dodecahedron of face centres. The right sets give the mirror-image compound, and no tetrahedron is in both.
- **#110's exact splits.** #110 B(d) splits the 1200 triangles among the 120 B copies. Here, each left set's 120 cells split the 720 edges, the 120 A copies split the 600 cells, and each A copy is a transversal of both states.
- **#63's shells.** All 15 shells round one corner (sizes 20, 20, 30, 60, 60, 60, 20, 60, 20, 60, 60, 60, 30, 20, 20) split into five equal parts among the left sets, and among the right sets.
- **Designs (#76, Alicia ch. 9).** P together with the unit tip 600-cell (240 points) is an 11-design, since both parts are (Goethals and Seidel, 1981). It is not a 12-design: the exact degree-12 zonal sum is 19800. So the pair gives no new design. The 19-design of #76 is not met here.
- **Not examined:** Valley Charge (#110 Proposition 6) and the bitruncated midpoint (#76, #104). Their corners are not on the cells used here, and no check was made.

### Answers in one line each
1. The 5 sets are one state of Coxeter's ten 600-cells, by centres, and the cosets of 2T in 2I: **confirmed exactly.** The same partition as the S5 orbits or the 24-cell splits: **refuted** (different objects), with exact links through A's tetrahedra and the 2T's.
2. The tip 600-cell is √2 × one of the ten 600-cells inscribed in P's dual 120-cell, P turned by right multiplication. Left choices give one state and mirror choices the other. The solid's hull is the tip 600-cell, and the duals of the ten tip 600-cells are the ten 120-cells holding P: **confirmed exactly.**
3. All ridge plates lie on mirrors, the caps are hidden, and the tip 600-cell's triangles lie on P's cross walls: **confirmed exactly.**
4. The solid's symmetry matches A, B or their duals: **refuted exactly.** It meets S5 in an A4.
5. The octahedron analogue holds for the edge cover and the centres, and fails for convexity: **confirmed exactly.**

### Prior art (sources checked, Part 2)
- Web searches:
  - "600-cell" with "5-cell" caps or augmented pentachora;
  - partition of the 600-cell's cells into five sets of 120;
  - cosets of the binary tetrahedral group in 2I;
  - compounds of 600-cells in the 120-cell.
- Pages read or seen:
  - Wikipedia "600-cell", "120-cell", "Compound of five tetrahedra" and "Binary icosahedral group";
  - Freire's star polychora and constructibility pages;
  - Banchoff, *Beyond the Third Dimension* §5.8;
  - Koca et al. on the snub 24-cell (arXiv 0906.2109);
  - the 24-cell page of the Error Correction Zoo;
  - the software3d forum on 4D compounds;
  - Denney et al. as cited in #110.
- Found, and credited above:
  - the compound of ten 600-cells in the 120-cell;
  - the 120-cell as five disjoint 600-cells;
  - the 10 ways to split the 600-cell into 5 24-cells;
  - 2T of index 5 in 2I with 5 conjugates.
- **Not found in the sources checked:**
  - the reading of the edge-once cell sets as one state of Coxeter's compound, through their centres;
  - the tip 600-cell, and the fact that the duals of the ten tip 600-cells are the ten 120-cells holding P;
  - the 5-cell caps on the 600-cell;
  - A's tetrahedra as transversals of both states;
  - the pairing of cap sides with #107's pentagons.

\*\* The 120-cell is named the Red Queen in DICTO's books (#65).

Computation by DICTO with Claude (Anthropic).

## LEADS
- Are the ten sets the only sets of 120 cells that cover every edge exactly once with no shared triangle? Not tested (an exact-cover search).
- The 3D rhombohedron shows that an octet union can fill space. A 4D union that fills space would need angle sums of 2π around every ridge. With only θ₅ and 4π/3 − θ₅ available, that needs other pieces. No search was made.
- If DICTO wants it, an actual 4D dissection to the cube (Jessen gives existence only).
- A picture for DICTO's books: the compound of five tetrahedra at one corner, coloured by the five sets.

FINAL ok
