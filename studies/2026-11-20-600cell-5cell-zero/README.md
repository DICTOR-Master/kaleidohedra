# A 600-cell and 120 5-cells: Dehn invariant zero

Study, 20 Nov 2026. Outside the plan. DICTO approved it "as a study".

**Verdict:** one regular 600-cell of edge a together with **120** regular 5-cells of the same edge a has Dehn invariant zero. 120 is the only equal-edge count, so it is also the smallest. The 5-cells can sit on 120 of the 600-cell's tetrahedral facets as one solid. That solid is star-shaped and **not convex**. Its 120 capped facets use every edge of the 600-cell exactly once and no two of them share a triangle. The apexes of the caps form a larger regular 600-cell of radius √2 (with circumradius 1). The solid's volume is **5√5 φ² a⁴**. By Jessen's theorem, any such union is scissors congruent to a 4-cube of edge **5^(3/8) √φ a ≈ 2.32599 a**. This is an existence result only: no dissection is claimed.

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

## LEADS
- Is the √2 apex 600-cell a sign of a compound or nesting? It is the 600-cell × √2 in another position. Worth a look at the hull of the union.
- The edge-partition property: the 120 capped facets cover every edge exactly once, as alternate faces do on the octahedron. Is this a known partition of the 600-cell's facets? Check the literature on "Clifford-parallel" cell sets.
- The 3D rhombohedron shows that an octet union can fill space. A 4D union that fills space would need angle sums of 2π around every ridge. With only θ₅ and 4π/3 − θ₅ available, that needs other pieces. No search was made.
- If DICTO wants it, an actual 4D dissection to the cube (Jessen gives existence only).

FINAL ok
