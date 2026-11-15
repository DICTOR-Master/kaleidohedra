# The octahedral constant 3 in Lean

A Lean 4 / Mathlib formalisation of **Theorem 4 of DICTO's paper #43**,
*Kyushindo Cores* (Zenodo 2026, version 3,
[doi:10.5281/zenodo.24153218](https://doi.org/10.5281/zenodo.24153218)).

Author and maintainer: DICTO. The Lean code was written with an AI agent
(Claude Code, Opus); see `formalization.yaml`, section `automation`.

## The result

Write a convex polytope containing the origin as S = {x : ⟪nᵢ, x⟫ ≤ hᵢ} with
unit normals nᵢ and distances hᵢ > 0. The foot point of the face plane i is
hᵢnᵢ, the point of that plane nearest to the origin, and P(S) is the convex hull
of the foot points.

* **Theorem 4** (`octahedral_nesting`). If the family of face planes is carried
  to itself by the 24 rotations of the octahedral group, then S ⊆ 3·P(S).
* **Sharpness** (`octahedral_nesting_sharp`, `cube_admissible`). For the cube
  [−1, 1]³, P is the octahedron conv{±eᵢ}, and the corner (1, 1, 1) is not in
  c·P for any 0 ≤ c < 3.
* **Covering lemma** (`covering`). For all unit vectors u, w some octahedral
  rotation g has ⟪gu, w⟫ ≥ 1/√3.

## What is known and what is not

* The covering lemma is **known**. It is the upper bound diam(S²/O) ≤ arccos(1/√3)
  for the orbit space S²/O, whose diameter is exactly that value (attained by a
  three-fold against a four-fold axis), a value recorded by S. Greenwald (Indiana Univ. Math.
  J. 49 (2000) 1449–1479) and in Table 2 of W. D. Dunbar, S. J. Greenwald,
  J. McGowan and C. Searle (Differential Geom. Appl. 27 (2009) 307–319). The
  proof formalised here is the one in #43: the octahedral orbits are spherical
  3-designs (Delsarte–Goethals–Seidel 1977; Goethals–Seidel 1981), and a cubic
  polynomial argument over the 24 rotations gives the bound.
* The containment S ⊆ 3·P(S) for the foot-point hull, with sharpness for the
  cube, is stated in #43 (Theorem 4). We did not find it stated elsewhere in
  the sources checked (listed below). It follows from the known orbit-space
  diameter by a short elementary argument, and we make no stronger novelty
  claim.
* We found no earlier Lean formalisation of either statement (a text search of
  Mathlib v4.35.0-rc2 finds "octahedral" only in triangulated categories and
  nothing on pedal or foot-point hulls; a general web search found nothing).

**Sources checked** (15 November 2026): web and arXiv searches for orbit-space
diameters of finite subgroups of SO(3), covering radii of group orbits and of
spherical designs (Fazekas–Levenshtein 1995, Boyvalenkov–Stoyanova
arXiv:2007.05599), circumradius-to-inradius ratios of symmetric convex bodies
(Barvinok–Blekherman arXiv:math/0312268; arXiv:1310.4368; arXiv:2606.30241),
pedal and foot-point polytopes (Smarandache's face pedal polyhedron,
arXiv:1003.2153; arXiv:2108.08293, arXiv:1008.0110), containment in dilates of
hulls of facet contact points, and Lean or Mathlib formalisations of these
notions; the Palomar database; the author's reference library (77 full-text
sources searched for #43 in October 2026, and its catalogue again in November
2026). Not read: the indexes of Grünbaum's *Convex Polytopes* and Schneider's
*Convex Bodies* (no copy at hand), and MathOverflow (not reachable).

## Files

- `Challenge.lean`: the statement surface (definitions and statements, every
  proof `sorry`), 4 compared theorems; read this first.
- `Solution.lean`: the Challenge word for word, with proofs. Each proof
  transfers a theorem of the proof library by definitional unfolding.
- `Kyushindo/Proof.lean`: the proof library (namespace `KyushindoProof`, whose
  definitions are copies of the Challenge's); `Kyushindo/Axioms.lean` prints
  the axioms used.
- `comparator.json`: the 4 compared theorems and the permitted axioms.
- `formalization.yaml`: metadata (v0.4).

## Proof account

1. **The group.** The 24 rotations are an explicit list of signed permutations;
   `decide` checks that each has determinant 1, that there are no repeats, and
   that every rotation of the group is in the list.
2. **Covering lemma, general form** (`covering_general`): ‖u‖‖w‖/√3 ≤ ⟪gu, w⟫
   for some g. With t_g = ⟪gu, w⟫, the sums Σt, Σt² and Σt³ over the list are
   0, 8‖u‖²‖w‖² and 0 (`ring` identities). With M = ‖u‖‖w‖/√3, if every t_g < M
   then Σ(M − t)(t + M)² would be positive, but the moments make it 0. This is
   #43's cubic (t − m)(t + 1/(3m))² at m = 1/√3.
3. **Separation.** A point outside a finite convex hull is strictly separated
   from it (Mathlib's `geometric_hahn_banach_closed_point`, then the Riesz
   vector).
4. **Theorem 4.** For x in S, each distance satisfies hᵢ ≥ ‖x‖/√3 (covering
   with u = nᵢ, w = x, and symmetry). Every direction v has a normal nⱼ with
   ⟪v, nⱼ⟫ ≥ ‖v‖/√3, so ⟪v, hⱼnⱼ⟫ ≥ ‖v‖‖x‖/3 ≥ ⟪v, x/3⟫. No v separates x/3
   from P, so x/3 ∈ P. Neither boundedness nor hᵢ > 0 is used.
5. **Sharpness.** The cube's foot points satisfy ⟪(1,1,1), y⟫ ≤ 1, so the hull
   does too, while ⟪(1,1,1), (1,1,1)⟫ = 3.

## Fidelity notes

1. The group is in the standard frame; #43's statement for any frame follows by
   rotating S.
2. Any nonempty finite invariant family of half-spaces is allowed; for the facet
   family of a symmetric S this is Theorem 4 exactly, and redundant half-spaces
   only enlarge P.
3. Sharpness is stated for factors c ≥ 0. For c ≤ −3 the cube does lie in c·P,
   because P is centrally symmetric.

## Checking

```
lake exe cache get
lake build
./scripts/verify-comparator.sh
```

Toolchain `leanprover/lean4:v4.35.0-rc2`, Mathlib `v4.35.0-rc2`.

## Licence

Apache-2.0 (`LICENSE`). The paper #43 is CC BY-SA 4.0.
