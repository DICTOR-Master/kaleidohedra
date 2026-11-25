# Do the Vacuus and the Resonus of the lattice space-fillers make a lattice of planes? (25 Nov 2026)

DICTO · data study for the paper "The Vacuus and the Resonus" (working title), V SF A project.
The question is **DICTO's idea**. He said: "yes definitely such a study, that was my instinct".

> **Status box.** Study note, not published. Every verdict is exact, using rational numbers and numbers a + b√3 with exact
> signs. Nothing is decided in floating point. Theorems 1–6 are proved below. Two items are OPEN, each with its blocker (see LEADS).
> Resume: everything committed; nothing running.

## Conclusion

| polyhedron (standard member) | Vacuus web | Resonus web | planes (V / R) | families that continue | lattice of planes made |
|---|---|---|---|---|---|
| cube | **yes** | **yes** | 6 / 3 | all 9 | R: the cubic lattice of planes x_i ∈ Z. V: the planes x_i ± x_j ∈ Z, the tetragonal-disphenoid honeycomb (12 regions per cell). R ∪ V: the B̃3 alcoves (24 regions per cell) |
| hexagonal prism | no | **yes** | 9 / 4 | R: all 4. V: only the 3 plates through the upright edges, which are Resonus planes | R: the triangular-prism honeycomb (6 regions per cell) |
| rhombic dodecahedron | **yes** | **yes** | 6 / 6 (R = V) | all 6 | the same disphenoid honeycomb as the cube's Vacuus, with the cells on the fcc sublattice (24 regions per cell; each region lies inside one cell) |
| elongated dodecahedron | no | no | 12 / 6 | R: the 2 hexagon planes. V: 4 plates, all containing the long axis | none (the planes that continue all contain one direction) |
| truncated octahedron | no | no | 15 / 7 | R: the 3 square planes. V: the same 3 planes | the 3 square planes alone: a cubic lattice of planes (4 regions per cell) |

The plate counts agree with the catalogue study (2026-11-24-vacuus-resonus-catalogue): 6/3, 9/4, 6/6 and 15/7.

- **(1) Continuation (Theorem 0).** A family continues exactly when the integer **k = 2h/d ≤ 2**. Here h is the half-width of
  the cell across the plane and d is the spacing of the lattice layers parallel to it. Every family that continues has k = 1 or 2.
  Every family that breaks has k = 3, 4, 6 or 8, or else no layer spacing at all. The equal-edged elongated dodecahedron is that
  last case, because √3 makes the layers dense. This is DICTO's integer signal, made exact: closure is the inequality k ≤ 2.
- **(2) General members (Theorems 1, 3 and 4).**
  - The Resonus continues for every parallelepiped, for every hexagonal prism whose base is an affine image of the regular
    hexagon, and for every affine image of the rhombic dodecahedron. It continues for **no** elongated dodecahedron and **no**
    truncated-octahedron-type polyhedron of any shape.
  - The Vacuus continues for every parallelepiped and for every affine image of the rhombic dodecahedron. It continues for no
    other member of the five types.
- **(3) Moving the centre (Theorems 2 and 5).**
  - Moving the centre never repairs a broken family.
  - The cube's Resonus survives any centre. Its Vacuus needs the true centre.
  - The rhombic dodecahedron needs the true centre for both.
  - No centre at all gives a Vacuus web for the hexagonal prism (proved for every shape), the elongated dodecahedron or the
    truncated octahedron. For the last two this is proved by an exhaustive exact search for the standard members.
- **(3) Choosing a different cell (Theorem 6).** Any two lattices are linear images of each other, and both families follow every
  linear map. So every lattice carries cells with both webs: a parallelepiped, or a linear image of the rhombic dodecahedron. No
  cell of the elongated-dodecahedron or truncated-octahedron type has a web for any lattice.
- **(5) The Resonus = Vacuus pair.** The rhombic dodecahedron (from the overlaps study) continues fully. Its six planes form the
  disphenoid honeycomb, whose corners are the bcc lattice. The same honeycomb is the cube's Vacuus web.
- **Striking fact.** One arrangement of planes, {x_i ± x_j ∈ Z}, is at once:
  - the Vacuus web of the cubic tiling (cells on Z³);
  - the Resonus = Vacuus web of the rhombic-dodecahedron tiling (cells on the fcc lattice);
  - the Delone tiling of the bcc lattice, which is the dual of the truncated-octahedron tiling (Wikipedia, "Tetragonal disphenoid
    honeycomb": its corners are the bcc lattice, it is the dual of the bitruncated cubic honeycomb, and each cell is 1/12 of a
    cube).

  The truncated octahedron itself does not continue. The web of its neighbours is its own dual.

## 1. Setting and definitions (no new ones)

- **Vacuus** (#110): one plate through the centre O and each edge. **Resonus** (DICTO): one plane through O parallel to each
  face; parallel faces share one plane.
- **Parallelohedra.** These are the five types of Fedorov (1885). Every 3D parallelohedron is a zonohedron whose belts all have 4
  or 6 faces (Wikipedia, "Parallelohedron", citing Fedorov 1885, Coxeter 1968 and Senechal & Taylor 2023). Each type is
  P = Z(λ_1u_1, …, λ_mu_m), the sum of the segments [−λ_ku_k/2, λ_ku_k/2], with λ_k > 0 and a fixed vector system (`webs.py`,
  `TYPES`):
  - cube: e1, e2, e3;
  - hexagonal prism: e1, e2, e3, e1+e2;
  - rhombic dodecahedron: e1, e2, e3, e1+e2+e3;
  - elongated dodecahedron: e1, e2, e3, e1+e2, e1+e2+e3;
  - truncated octahedron: e1, e2, e3, e1+e2, e2+e3, e1+e2+e3. These are the edges 01, 12, 23, 02, 13, 03 of K4. The opposite
    pairs are (e1, e3), (e2, e1+e2+e3) and (e1+e2, e2+e3).
- **Realisations.** Each vector system has only one realisation up to a linear map. So every member of a type is a linear image of
  one Z(λu), and the type has 0, 2, 3, 4 and 5 shape parameters beyond linear maps.
- **Standard members.** These have all λ = 1 and are linear images of the familiar Euclidean polyhedra. The exception is the
  equal-edged elongated dodecahedron, which has axis λ = √3/2 against 1 for the four diagonal zones.
- **Lattice.** The tiling is the face-to-face lattice tiling, whose lattice is generated by the facet vectors (twice the face
  centres). In this frame Λ = G Z³ with G = U diag(λ) Uᵀ. The script checks this for every member: each facet vector lies in
  G Z³, and the facet vectors generate it (index 1).
- **Affine.** The task said the Vacuus is not affine-invariant. That is not right for these polyhedra. Both the Vacuus and the
  Resonus are **affine-equivariant**: a plate through O and an edge, and a plane through O parallel to a face, go to the same
  kind of object under any affine map, and O (the centre of symmetry) goes to the centre. What is not affine-invariant is the
  shape: a general hexagonal prism, elongated dodecahedron or truncated octahedron is **not** an affine image of the standard
  one. This is why the general members (λ arbitrary) are treated separately below.

## 2. Proofs

**Theorem 0 (the exact test).** Let a plane through O have normal n. Its translates by Λ meet the interior of a cell P + μ without
passing through μ exactly when some ν ∈ Λ has 0 < |n·ν| < h(n), where h(n) = max over P of n·x = Σ λ_k|n·u_k|/2. So the family
continues as a web if and only if n·Λ is discrete, with gap d ≥ h, which is the same as k = 2h/d ≤ 2. When the test holds, a plane
through the interior of a cell passes through its centre and has the same normal, so it is that cell's own plate or plane.
*Proof.* The plane n·x = n·λ meets the interior of P + μ exactly when |n·(λ − μ)| < h. ∎
In lattice coordinates, n·Λ is the group generated by the three numbers n·Ge_i.

**Theorem 1 (Resonus, every member).** Let F be a face, S the zones lying in it and T the other zones. Take the normal with
n·u_k ∈ {0, ±1}; this is possible because the vector systems are unimodular. Then n·Λ = {Σ_{k∈T} ±λ_k m_k : m ∈ M_T}, where M_T
is the image of y ↦ (u_k·y)_{k∈T} on Z³, and h = Σ_T λ_k/2.
- (a) Suppose M_T = Z^T. If the λ_k are commensurable with gcd d, each λ_k ≥ d, so h ≥ |T|d/2. Hence the face family continues
  **if and only if |T| ≤ 2 and the λ_k with k in T are equal**. If they are not commensurable, n·Λ is dense and the family breaks.
- (b) Cases of (a):
  - The cube (|T| = 1) always continues.
  - Hexagonal prism: the hexagon plane (T = {e3}) always continues. The three side planes need λ2 = λ4, λ1 = λ4 and λ1 = λ2
    respectively. All four together hold exactly when the base hexagon is an affine image of the regular hexagon.
  - Rhombic dodecahedron: the face with zones {i, j} continues iff the other two λ are equal. All six continue iff all λ are
    equal, that is, for the affine images of the rhombic dodecahedron.
  - Elongated dodecahedron: the two hexagon planes need λ3 = λ5 and λ1 = λ2. **The four rhombus planes have |T| = 3 and never
    continue.**
  - Truncated octahedron: **the four hexagon planes have |T| = 3 and never continue.**
- (c) Truncated-octahedron squares. Here |T| = 4 and M_T is the rank-3 lattice a + d = b + c. For the square of the pair (e1, e3)
  this gives n·Λ = αZ + βZ + γZ, with α = λ2 − λ6, β = λ4 + λ6 and γ = λ5 + λ6, and h = (α + β + γ)/2.
  - If α > 0, then h ≥ 3d/2.
  - If α < 0, then β, γ > λ6 > |α|, so β/d and γ/d are at least |α|/d + 1, which forces 2h/d ≥ 3.
  - So the square continues **iff α = 0 and β = γ**, that is, iff the other two opposite pairs of zones each have equal lengths.
  The other two squares follow by symmetry. ∎
- Exact check: on the grid λ ∈ {1, 2, 3}^m (621 members, 3 672 face planes) the predictions match the exact test with no mismatch
  (`general.py`, part A).

**Theorem 2 (Resonus with a moved centre).** Put the centre at c in every cell. A face family with normal n continues iff
d ≥ h + |n·c|. *Proof.* The planes are n·x = n·c + kd, and the cell P + μ spans n·μ ± h. ∎
- So moving the centre never repairs a broken family.
- A working family keeps working iff |n·c| ≤ d − h. For the cube, d − h = h, so any interior centre works. For the side planes of
  the hexagonal prism, and for every rhombic-dodecahedron plane, d − h = 0. So the prism's Resonus needs c on the prism axis, and
  the rhombic dodecahedron's needs c = O.

**Theorem 3 (an edge in three cells).** Let e be an edge in a belt of six faces. In the tiling such an edge lies in exactly three
cells. If the plate of P through e continues, it contains the face shared by the other two cells at e. So it is parallel to a face:
**it is a Resonus plane**, and it continues exactly when that Resonus family does.
*Proof.*
- Project along e. Near e the three cells are three wedges. Each wedge is the angle of the six-sided shadow of P at the vertex
  that cell has at e.
- Beyond e, the plate's line either runs along a wall, or enters the open wedge of a neighbour Q.
- Suppose it enters Q. By Theorem 0 the line passes through Q's centre. Then Q's vertex at e points exactly opposite to P's. By
  central symmetry it is the opposite vertex −v, so P's and Q's wedges are vertically opposite angles.
- The third cell's wedge would then be the rest of the plane around e. That rest is two separate opposite sectors, but a wedge of
  a convex cell is one sector. This is a contradiction. ∎
- Consequences, with the centre at O. Each zone of a six-face belt has three plates, parallel to the three face directions of its
  belt.
  - Elongated dodecahedron: zone e1 has belt directions hexagon, rhombus and rhombus. Truncated octahedron: every zone has hexagon,
    hexagon and square.
  - By Theorem 1 the rhombus planes of the elongated dodecahedron and the hexagon planes of the truncated octahedron never continue.
    So at least two plates of such a zone break, **for every shape**.
  - In a rhombic-dodecahedron-type polyhedron every edge is in three cells. So its whole Vacuus continues iff every shadow is an
    affine regular hexagon, which happens iff all λ are equal (the affine rhombic dodecahedron). Then R = V.
  - Hexagonal prism: the upright plates (zone e3) continue iff the matching side Resonus plane does.
- Exact check on the 621-member grid: every plate through a three-cell edge that continues is a Resonus plane that continues.
  The plates that continue and are not Resonus planes all go through four-cell edges: all 6 of the cube's, and the 2 axis plates
  of the elongated dodecahedron.

**Theorem 4 (hexagonal prism: no Vacuus web for any shape or centre).**
- Use an affine map to make the prism right, of height 1, with the base hexagon in |x| ≤ 1 and the top edge E on the line x = 1.
  Let the centre c have x = x_c < 1 and height c_z < 1/2. Put η = 1/2 − c_z.
- The plate through c and the top edge E × {1/2} is f = η(x − x_c) − (1 − x_c)(z − c_z) = 0.
- Let E′ and E″ be the two base edges next to E, with in-layer facet vectors t′ and t″. Their x-values s′ and s″ lie in (0, 2) and
  add up to 2 (from t′ + t″ = t_E). So one of them, say s′, is at most 1.
- The cell P + (t′, 0) lies in the same layer. f takes the value ηs′ > 0 at that cell's centre. Its half-width across the plate is
  η + (1 − x_c)/2, which is greater than ηs′.
- So the plate cuts the side neighbour across a base edge next to E, and misses that neighbour's centre. ∎
- In the regular prism the plate crosses the side wall diagonally. The crossing runs from the midpoint of an upright edge to the
  far top corner of E.
- A second, independent proof: by Theorem 5's four-cell argument, every horizontal zone forces c onto its own line through O.
  That forces c = O, and Theorem 0 gives k = 4 there.

**Theorem 5 (Vacuus with a moved centre, exhaustive for the standard members).**
- A plate through c and an edge e (midpoint m_e, zone u) continues iff its normal is a primitive dual-lattice vector n₀
  (n₀·Λ = Z) with n₀·u = 0, n₀·c = n₀·m_e and h(n₀) + |n₀·m_e| ≤ 1.
- Since h(n₀) ≤ 1 forces |λ_k n₀·u_k| ≤ 2, there are finitely many such n₀, and the search box contains them all (`general.py`,
  part B).
- The admissible centres are the interior points of ∩_e ∪_{n₀} {n₀·x = n₀·m_e}, computed exactly. Results:
  - cube: only c = O;
  - rhombic dodecahedron: only c = O;
  - hexagonal prism: none;
  - truncated octahedron: none (each edge allows one plate, and the plates have no common point);
  - elongated dodecahedron, both with axis λ = 1 and with axis λ = √3/2: none. 16 of its 28 edges allow no plate at all, whatever
    the centre.
- For a four-cell edge with a parallelogram shadow, the plate must run through the diagonal cell's centre (the other options lie
  on P's boundary). That puts c on the line through O and the edge's direction. For the cube, the three zones give c = O.

**Theorem 6 (another cell for the same lattice).** For any lattice Λ, take the linear map A that sends Z³ (respectively the fcc
lattice) to Λ. Then A(cube) and A(rhombic dodecahedron) tile with lattice exactly Λ, and their webs are the images of the
standard webs. So both webs exist for every lattice, including the bcc lattice of the truncated octahedron. Within the
elongated-dodecahedron and truncated-octahedron types, Theorems 1 and 3 rule out a web for every lattice. ∎

## 3. The webs and their integers

The table comes from `webs.py`. Regions per cell are counted on the 3-torus R³/Λ by the toric form of Zaslavsky's count
(Ehrenborg, Readdy and Slone 2009): the regions equal the sum over corners p of 1 − n_p + Σ_lines (m_L − 1). This count is checked
three ways:
- the cube's Resonus gives 1 region per cell;
- the cube's Vacuus gives 12, which matches Wikipedia's "1/12 of a cube";
- the rhombic dodecahedron gives 24 regions, equal to its 24 pieces.

| web | plane families | pieces per cell | regions per cell | corners per cell | k of each family |
|---|---|---|---|---|---|
| cube R | 3 | 8 | 1 | 1 (Z³) | 1 |
| cube V | 6 | 24 | 12 | 2 (bcc ⊃ Z³, index 2) | 2 |
| cube R ∪ V | 9 | 48 | 24 | 5 | 1, 2 |
| hexagonal prism R | 4 | 12 | 6 | 3 (a triangular lattice 3 times finer, × Z) | 1 (hexagon), 2 (sides) |
| rhombic dodecahedron R = V | 6 | 24 | 24 | 4 (bcc ⊃ fcc, index 4) | 2 |
| truncated octahedron, squares only | 3 | 8 | 4 | 4 (cubic ⊃ bcc, index 4) | 2 |

- **Identification of the webs**:
  - cube R: the cubic lattice of planes, with corners at the cell centres;
  - cube V and the rhombic dodecahedron: {x_i ± x_j ∈ Z}, whose regions are the tetragonal disphenoids with corners (0,0,0),
    (1,0,0), (½,½,½), (½,½,−½) and volume 1/12;
  - cube R ∪ V: {x_i ∈ Z, x_i ± x_j ∈ Z}, whose regions are the alcoves 0 < x3 < x2 < x1, x1 + x2 < 1 of the affine Weyl group of
    type B̃3 (volume 1/24);
  - hexagonal prism R: equilateral triangles × Z.
- **Pieces against regions.**
  - Cube: 2 pieces per region, glued across a wall.
  - Rhombic dodecahedron: 1 piece per region, so each disphenoid lies inside one cell. The cell is the union of 24 disphenoids, each
    the centre joined to half a rhombus.
  - Hexagonal prism: 2 pieces per region, glued across the top face.

## 4. Method and files

- `scripts/webs.py`: the exact field Q(√3) (class Q3), the zonotope frame, the lattice check, the test of Theorem 0 with a
  shortest witness ν for each broken family, central and toric region counts. It runs on 9 standard members (including the prism
  with height 2 and √3, and the elongated dodecahedron with axis 1, 2 and √3/2). Output: `data/webs-standard.json`.
- `scripts/general.py`:
  - part A checks Theorems 1 and 3 and the horizontal-plate part of Theorem 4 on 621 members (λ ∈ {1, 2, 3}^m; for the
    truncated octahedron, the members with at most two distinct λ). It finds 0 mismatches.
  - part B is the exhaustive moved-centre search of Theorem 5.
  - Output: `data/general.json`.
- `logs/lattice-webs.log`: the run, which ends in `FINAL ok`. It was run on a compute host after a pilot.
- The catalogue study's plane counts (catalogue.py, on vacuus_exact) are reproduced here rather than re-imported. That code
  builds Euclidean coordinates, and this test needs the lattice frame. The plane sets agree in number for the four polyhedra the
  catalogue holds; the elongated dodecahedron is not in the catalogue.

## 5. Sources checked

- Wikipedia, "Parallelohedron" (opened 25 Nov 2026): Fedorov 1885 (the five types); parallelohedra are zonohedra (Coxeter 1968);
  belts of 4 or 6 (Senechal & Taylor 2023); Delone 1929 (every parallelohedron is affinely a Voronoi cell, via Austin 2013);
  generator counts 3, 4, 4, 5, 6.
- Wikipedia, "Tetragonal disphenoid honeycomb" (opened): corners = bcc; dual of the bitruncated cubic honeycomb; each cell 1/12 of
  a cube.
- R. Ehrenborg, M. Readdy, M. Slone, "Affine and toric hyperplane arrangements", Discrete Comput. Geom. 2009, arXiv:0810.0295
  (abstract opened): Zaslavsky's region count for toric arrangements. The formula used here is checked independently, as stated
  in Section 3.
- arXiv listings on the Voronoi conjecture (opened):
  - Garber, Gavrilyuk and Magazinov, arXiv:1212.1019;
  - Garber, arXiv:1104.0401 (zonotopes) and arXiv:1906.05193 (dimension 5);
  - Dutour Sikirić, Garber and Magazinov, arXiv:1812.02964 (Venkov complex);
  - Magazinov, arXiv:1308.6225.
  These are context for the Venkov–McMullen and Voronoi–Delone line. None of them treats planes through cell centres.
- Not opened (no free copy found in this pass): Fedorov 1885 itself; Voronoi 1908/09 (Crelle); Venkov 1954; McMullen 1980;
  Erdahl 1999 (lattice dicings). Erdahl's dicings are families of lattice planes whose corners are all lattice points. They are
  close kin to the webs here but not the same: the webs pass through the cell centres, and dicing planes are normal to the zone
  vectors.
- **Prior art for the question itself:** none found in these sources. No source asks whether the planes through a cell's centre
  and its edges, or parallel to its faces, continue through the tiling.

## 6. Home paper

All results go to **the Vacuus and Resonus paper**, as one section ("lattice webs": Theorems 0–6 and the table). One alternative,
**if DICTO agrees**: a short separate paper, "One arrangement, three tilings", on the striking fact that {x_i ± x_j ∈ Z} is the
cube's Vacuus web, the rhombic dodecahedron's web and the Delone tiling of bcc.

## LEADS

1. **OPEN: moved centre for general members.** Theorem 5 is exhaustive only for the standard members of each type. With the centre
   at O, Theorems 1, 3 and 4 already cover all shapes. Blocker: the search depends on λ. A proof would need Theorem 3 for an
   off-centre point; the vertically-opposite-angle step uses central symmetry.
2. **OPEN: sliding tilings.** The cube and the hexagonal prism also tile by lattices that are not face-to-face (shifted columns or
   layers). Blocker: not yet set up. For the cube's Resonus, a shift of exactly ½ still continues, by Theorem 0.
3. **Observed, not yet proved:** the elongated dodecahedron's two axis plates (the only plates that continue without being Resonus
   planes) continued on the grid exactly when λ1 = λ2 and λ3 = λ5.
4. **4D.** In 4D the 24-cell (Resonus = Vacuus, overlaps study) and the 4D permutohedron are parallelotopes. Theorem 0 carries over
   unchanged (k ≤ 2). Test whether the 24-cell's web is the D̃4 alcove arrangement.
5. **Lean.** Theorem 0 and the cube and rhombic-dodecahedron webs are finite integer statements, which suits the Lean study
   2026-11-25-lean-vacuus-resonus.
6. **One piece, any stacking.** The disphenoid web is shared by the cubic and rhombic-dodecahedron tilings. Decorations keyed to
   it would be seen the same way in both, which could serve the aim of one piece forcing aperiodic stacking.
