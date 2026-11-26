# Vacuus + Resonus and mirror planes (27 Nov 2026)
DICTO's conjecture (from his cube and octahedron models): when the Vacuus and Resonus planes are aligned, the gaps between the two
shapes become linear trigonometry for space filling. With Claude (Anthropic). Script scripts/mirrors.py (exact, Q(sqrt2)/Q(sqrt5),
the K class of the Vacuus-Solids study); log logs/mirrors.log; table mirrors.json. Snub cube and snub dodecahedron left out (chiral:
no mirror planes; coordinates need cubic irrationals).

## Step 1 (exact): which planes are mirror planes
Control: mirror counts dodecahedron 15, icosahedron 15, cube 9, tetrahedron 6, octahedron 9: correct.
- Vacuus + Resonus = ALL mirror planes, exactly: **cube** (6 Vacuus + 3 Resonus = 9) and **rhombic triacontahedron** (15 + 15, the
  same 15 planes twice). No other solid of the 27.
- Vacuus planes are all mirrors for every Platonic solid and every Catalan solid; Resonus planes are all mirrors only for cube,
  rhombic dodecahedron, rhombic triacontahedron, and (9 or 15 of their 13 or 31) the rhombicuboctahedron, truncated cuboctahedron,
  rhombicosidodecahedron, truncated icosidodecahedron.
- **Correction to the chat of 27 Nov ~04:15**: the octahedron does NOT give the same 9 planes as the cube. Its Vacuus is the 3
  coordinate planes (mirrors) but its Resonus is the 4 planes x +- y +- z = 0, which are not mirrors. Cube + octahedron together:
  9 mirrors + 4 further planes.
- What still holds for every solid here: its Vacuus + Resonus planes form a set invariant under the solid's full symmetry group,
  so the pieces they cut from any gap repeat by symmetry; one mirror chamber's pieces, reflected, give all of them. For cube +
  octahedron: each of the 48 chambers (0 < z < y < x) is cut once more, by x = y + z, so the gap's pieces come in 2 shapes, 96 pieces
  (by hand from the plane list; to be checked exactly in step 2).

## Next
2. Per solid pair: cut the gap by all planes exactly; count pieces and shapes per chamber.
3. Line lattices on face planes; 4. repeated planes in space (affine arrangements); 5. cells of the periodic arrangements
(classical ones credited: Sommerville, Goldberg; icosahedral families -> de Bruijn multigrid / Ammann planes, quasiperiodic).
