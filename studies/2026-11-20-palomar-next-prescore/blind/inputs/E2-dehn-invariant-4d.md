# Candidate E2: the Dehn invariant in four dimensions, read from the set (a proposed Lean entry)

## Abstract (neutral)

In ℝ⁴ the Dehn invariant of a polytope is Σ over its 2-faces (ridges) F of area(F) ⊗ θ_F in ℝ ⊗_ℚ (ℝ/ℚπ), where θ_F is the dihedral angle between the two cells (facets) meeting at F. It is preserved by scissors congruence (cutting into finitely many polytopes, moving them by isometries, refitting). Jessen (1972) proved that in four dimensions volume and this invariant are a complete set of scissors-congruence invariants (the four-dimensional Dehn–Sydler theorem); Dupont and Sah later gave proofs through group homology. Lagarias and Moews (1995) proved that a polytope that tiles ℝ⁴ by congruent copies is scissors congruent to a 4-cube.

The proposed entry builds on a registered Palomar entry, **PALOMAR-2026-11-20-000003, the Dehn invariant read from the solid, with the bridge from convex dissections**. That entry, in three dimensions, defines the invariant of a subset P of a 3-dimensional real inner product space from the set itself: at each point the cone of directions, its lineality space, the wedge angle 2π · area(cone ∩ unit disc of the complement) / area(unit disc) when the lineality space is a line, the angle class modulo ℚπ, and `dehnSet P = Σ_θ μH[1]{x : class θ} ⊗ θ`. It proves the edge-sum identity for convex polytopes, the bridge "scissors-congruent convex polytopes (and finite unions) have equal invariant", Hilbert's third problem for point sets and Dehn's theorem (tetrahedron and cube).

The proposed entry carries the same construction to a 4-dimensional real inner product space E:

1. **Definition.** `dehnSet4 P = Σ_θ μH[2]{x ∈ P : the lineality space of the cone of directions at x is a plane K and the wedge angle in K^⊥ has class θ} ⊗ θ` (2-dimensional Hausdorff measure; the wedge angle is 2π · area(cone ∩ unit disc of K^⊥) / area(unit disc of K^⊥)).
2. **Ridge-sum identity.** For every convex 4-polytope with interior points, `dehnSet4 P = Σ_ridges area(F) ⊗ (interior dihedral angle at F mod ℚπ)`, the ridges and the cell normals also read from the set.
3. **The bridge.** Scissors-congruent convex 4-polytopes, and finite unions of convex 4-polytopes, have equal `dehnSet4` (plane-cut identity along hyperplanes, invariance under affine isometries, common refinement).
4. **The six regular convex 4-polytopes.** Their dihedral angles (checked from coordinates and against Coxeter, *Regular Polytopes*, Table I(ii), as reproduced on Wikipedia):

   | polytope | dihedral angle | in ℚπ? | `dehnSet4` |
   |---|---|---|---|
   | 5-cell {3,3,3} | arccos(1/4) ≈ 75.52° | no | nonzero |
   | tesseract {4,3,3} | π/2 | yes | 0 |
   | 16-cell {3,3,4} | 2π/3 | yes | 0 |
   | 24-cell {3,4,3} | 2π/3 | yes | 0 |
   | 120-cell {5,3,3} | 4π/5 | yes | 0 |
   | 600-cell {3,3,5} | arccos(−(1+3√5)/8) = π/3 + arccos(−1/4) ≈ 164.48° | no | nonzero |

   Irrationality: if θ ∈ ℚπ then 2 cos θ is an algebraic integer; 2 cos θ is 1/2 for the 5-cell and −(1+3√5)/4 (a root of 4x² + 2x − 11) for the 600-cell, neither an algebraic integer. Moreover θ_600 = 4π/3 − θ_5, so θ_600 ≡ −θ_5 modulo ℚπ: the two non-zero invariants are A₅ ⊗ [θ_5] and −A₆₀₀ ⊗ [θ_5] with A₅, A₆₀₀ > 0 the total ridge areas.

5. **Non-congruence results (the 4D Hilbert-type statements).** Since four of the six invariants vanish, the results are framed on the pairs that actually differ:
   - no similar copy of the regular 5-cell is scissors congruent to a similar copy of the tesseract, the 16-cell, the 24-cell or the 120-cell (the 4D analogue of Dehn's tetrahedron-versus-cube theorem);
   - the same for the 600-cell;
   - no similar copy of the 5-cell is scissors congruent to a similar copy of the 600-cell (their invariants point in opposite directions on the same line, so they differ at every scale).

   The pairs among the tesseract, 16-cell, 24-cell and 120-cell are **not** distinguished by the invariant: all four have invariant zero, and by Jessen's theorem any two of them of equal volume are scissors congruent. That converse is not proved in the entry.

Limits stated by the submitter: Jessen's sufficiency theorem is not proved; only Euclidean 4-space; the invariant is the classical one (Jessen's, Sah's), not new mathematics; the dihedral-angle table is classical. What is claimed new is the set-defined 4D invariant with a machine-checked ridge-sum identity and bridge, and machine-checked non-congruence of the regular 4-polytopes above.

Facts on the proof: not yet built. The statements above are the ones to be proved; the 3D development (registered entry) supplies the pattern (cones of directions, wedge angles, plane-cut identity, common refinement).

## Sources (exact citations)

- **M. Dehn**, "Über den Rauminhalt", *Math. Ann.* 55 (1901) 465–478.
- **B. Jessen**, "The algebra of polyhedra and the Dehn–Sydler theorem", *Math. Scand.* 22 (1968) 241–256 (the tensor form; higher-dimensional invariants).
- **B. Jessen**, "Zur Algebra der Polytope", *Nachr. Akad. Wiss. Göttingen Math.-Phys. Kl. II* (1972) 47–53: the Dehn–Sydler theorem in dimension 4 (read through citations).
- **J. L. Dupont**, *Scissors Congruences, Group Homology and Characteristic Classes*, World Scientific, 2001 (not read in full).
- **C.-H. Sah**, *Hilbert's Third Problem: Scissors Congruence*, Pitman, 1979 (not read).
- **J. C. Lagarias, D. Moews**, "Polytopes that fill ℝⁿ and scissors congruence", *Discrete Comput. Geom.* 13 (1995) 573–583, doi:10.1007/BF02574064: in dimensions ≤ 4 a space-filling polytope is scissors congruent to a cube; in dimension 4 volume and the invariant suffice (Jessen).
- **H. S. M. Coxeter**, *Regular Polytopes*, 3rd ed., Dover, 1973, Table I(ii) (dihedral angles; seen as cited on the Wikipedia pages "5-cell" (arccos 1/4 ≈ 75.52°), "Tesseract" (90°), "16-cell" (120°), "120-cell" (144°), "600-cell" (π/3 + arccos(−1/4) ≈ 164.48°)).
- **I. Zakharevich**, survey and papers on scissors congruence as K-theory (arXiv:1101.3833 and later): Dehn–Sydler–Jessen complete in dimensions 3 and 4, open in dimension ≥ 5 (seen).

## Prior formalizations (searched 20 Nov 2026)

- The registered entry above (Lean, three dimensions only).
- FormalBook ch. 10 (Lean): three dimensions, abstract model, no invariant in dimension 4.
- facebookresearch/atlas-lean (Lean): a Dehn invariant of an edge list in three dimensions; nothing in dimension 4.
- Mathlib: no Dehn invariant. No formalization of a Dehn invariant in dimension 4 (or of Hadwiger's higher invariants) was found in Lean, Isabelle AFP, Coq/Rocq, HOL Light, Metamath or Mizar.
- No source was found that states the 4D Dehn invariants of the six regular 4-polytopes as a table, or the relation θ_600 ≡ −θ_5 (mod ℚπ), although both follow at once from the classical dihedral angles.

## What is claimed

A machine-checked, set-defined Dehn invariant in four dimensions with the ridge-sum identity and the scissors-congruence bridge, and the non-congruence of the 5-cell and the 600-cell with each other and with the four regular 4-polytopes whose invariant vanishes. Not claimed: Jessen's theorem; any new invariant.

## Statement to score

E2. Items 1–5 above (definition, ridge-sum identity, bridge, the six invariants, the non-congruence results), scored as one result group, building on PALOMAR-2026-11-20-000003.
