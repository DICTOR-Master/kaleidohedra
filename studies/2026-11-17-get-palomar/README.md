# GET for Palomar: the complete Solution (17 November 2026)

**Status: the Solution is complete. It has 0 `sorry`, no `native_decide`, and its four theorems depend only on
`propext`, `Classical.choice` and `Quot.sound`.** A clean staged build takes about 5 min of wall time. The largest
Lean process peaks at 8.1 GB, under Palomar's 16 GB runners. The comparator (Lean kernel, NanoDa, con-ron) accepts
the Solution (§3).

Two things still block submission. First, novelty: Senechal–Taylor 2023 is not yet read. Second, provenance: DICTO has
not yet chosen how GET is first published (see §5).

Nothing was pushed, submitted or created on GitHub. The Lean project is in `lean/` here. A working copy, with a local git
repository, is on the compute host as `get-palomar`. Nothing is left running.

## 1. The statement (`lean/Challenge.lean`, after the independent statement review)

There is a polyhedron `P` in Euclidean 3-space with these properties.
- **Spherical type** (Grünbaum 2010, p. 9):
  - `P` is compact and equal to the closure of its interior;
  - its frontier is the union of its **30 distinct** parallelogram faces, and that frontier is homeomorphic to the
    sphere;
  - two faces meet in a common side, a common corner, or not at all;
  - adjacent faces are not coplanar.
- **Rhombic monohedral, golden:** every face is a rhombus, any two faces are congruent, and the diagonals of every face
  are in the golden ratio (`Real.goldenRatio`).
- **Every zone has exactly 10 faces.** A zone is the belt reached by crossing sides parallel to one direction. Each belt
  is also the set of all faces with a side of that direction.
- **Lattice tiling, face to face:** the translates by a lattice cover space and have pairwise disjoint interiors.
  `FaceToFace` is a per-face matching condition: every face of `P` is a face of a translate by a non-zero lattice
  vector.

The theorems in `Challenge.lean`:
- `grunbaum_k10`: ∃ P, F : Fin 30 → Parallelogram, b with all of the above.
- `grunbaum_k10_parallelohedron`: Grünbaum's own form.
- `cube_everyZoneHas`, `rhombicDodecahedron_everyZoneHas`: the calibration theorems. `EveryZoneHas` gives 4 for the
  unit cube and 6 for the rhombic dodecahedron, so the zone definition does not force the answer.

The review fixes applied:
1. The main theorem is strengthened: 30 faces, distinct, golden rhombi, plus everything listed above.
2. The two calibration lemmas are stated in the Challenge and proved in the Solution.
3. The divergence line on `FaceToFace` is added, in the docstring and in the yaml.
4. Wording: "gives an example for k = 10", never "answers" or "new". The yaml carries the novelty sentence and
   `reviewers: []`. The counts 16 rhombohedra, 32 vertices and 60 edges are given as properties of the witness. The
   provenance block is a marked TODO with both options. Grünbaum's indentation remark and his zone wording are no
   longer quoted.

The divergences (yaml `fidelity.divergences`):
- faces are parallelograms;
- the spherical type is made precise as above;
- the zone is the belt, and it also equals the set of all faces with a side of that direction; the calibration
  theorems check this definition;
- the lattice tiling is stronger than Grünbaum's notion;
- `FaceToFace` is per face;
- congruence is Mathlib's `Congruent` on the corners.

## 2. The proof (Solution)

`Solution.lean` proves the four theorems from `GET.Main`. The definitions come from `GET/Statement.lean`, which
`scripts/gen_statement.py` generates from `Challenge.lean`, so the two texts are identical. The witness is GET A, the union of
the 16 cells `cellSet (CA i)`. Its faces are `FA i`, and its lattice basis is `bA`.

| Step | Module | How | Build | Peak |
|---|---|---|---|---|
| exact vectors: `ev`, inner products, cross products, parallelism, independence | `Exact` | ℤ[φ] evaluation | 5 s | 2.9 GB |
| zones: segment equality, belt certificate ⇒ `EveryZoneHas` | `Zones`, `Certs` | generic soundness + `decide +kernel` | 8 s | 2.9 GB |
| calibration: cube 4, rhombic dodecahedron 6 | `Calib` | zone certificates | 10 s | 3.5 GB |
| faces: golden rhombi, congruence (through a reference rhombus, after relabelling), zones 10, adjacent ⇒ not coplanar (3 independent axes) | `Faces` | `decide +kernel` + norms | 42 s | 5.9 GB |
| sign test complete; cells; slab bounds; thin sets are null; cell = closure of interior | `Solid` | convexity, `addHaar_affineSubspace` | 6 s | 2.9 GB |
| lattice = integer combinations; separation of cells and of the 26 neighbouring translates; dual normals: no other translate meets `P`; `P ∩ (t + P)` null; **disjoint interiors** | `Tiling` | `decide +kernel` (6,656 cell pairs) | 36 s | 5.7 GB |
| vol P = covol = 20 + 32φ; fundamental domain; complement of the union is invariant and null; local finiteness ⇒ union closed ⇒ **cover** | `Cover` | `ZSpan.isAddFundamentalDomain'`, `measure_eq_tsum`, `LocallyFinite.isClosed_iUnion` | 6 s | 2.9 GB |
| contact test of two cells (forced parameters along the 15 normals) and its soundness | `Contact` | `extreme_params`, three segment steps | 7 s | 2.9 GB |
| every contact of a cell of `P` with a cell of a neighbouring translate lies in one face of `P` | `ContactData` | `decide +kernel` (6,656 pairs) | 52 s | 8.1 GB |
| **frontier = union of the 30 faces** (⊇ by face matching and disjoint interiors; ⊆ by cover + local finiteness + contacts); `closure (interior P) = P` | `Frontier` | | 6 s | 3.2 GB |
| **faces meet properly** (870 ordered pairs: disjoint, common corner, or common side) | `Meet` | forced parameters of the first face | 11 s | 3.9 GB |
| **sphere**: radial projection from a point of `K` off the frontier is a homeomorphism if it is injective on the frontier | `Sphere` | `homeoOfEquivCompactToT2` | 4 s | 2.9 GB |
| injectivity for GET A from the centre c₀ = (0, φ, 1 + φ) (a point of cell 14): face planes miss c₀; 435 cone-separation normals | `SphereData`, `SphereA` | `scripts/gen_sphere.py` + `decide +kernel` | 24 s | 6.5 GB |
| distinct faces (from `MeetProperly`), face to face, assembly | `Main`, `Solution` | | 4 s | 2.9 GB |

**Size.** There are 4,174 Lean lines in all (with `BChecks`): `Challenge.lean` (194), `Solution.lean` (63) and `GET/*.lean`. Of these,
861 are generated: `Data` (121), `Certs` (123), `SphereData` (449) and `Statement` (168). The pilot accounts for 611.

**Build.** A clean build was run in four stages, each under 5 min, with a 14 GB memory cap. It took 2:17 + 0:54 + 1:20
+ 0:35, about 5:06 of wall time. The peak resident memory of a single Lean process was 8.1 GB (`ContactData`).

**Axioms.** `#print axioms` on all four theorems gives `[propext, Classical.choice, Quot.sound]`. There is no `sorry`
outside `Challenge.lean`, and no `native_decide`.

**Generators.**
- `scripts/gen_certs.py` writes the exact face data `XA`, the zone certificates and the matching `MA`.
- `scripts/gen_sphere.py` writes the cone-separation normals.
- `scripts/getgeom.py` holds the shared exact arithmetic.
- `scripts/gen_statement.py` writes `GET/Statement.lean`.

All exact checks are re-decided in the kernel; the generators only propose certificates.

## 3. Kernel checks (comparator)

**The comparator accepts the solution: "Your solution is okay!".** All three kernels accept it:
- **con-ron** accepts 46,286 declarations in `--verified` mode. It runs with 1 worker, takes 392 s, and stays under
  3–5 GB.
- **NanoDa** accepts the solution.
- **Lean's default kernel** (leanchecker) accepts the solution.

The whole run (job get-comparator3) took 10 min 51 s of wall time inside a 14 GB memory cage and ended FINAL ok. It
uses `lean/scripts/run_comparator_lowmem.sh`, which is the template's `verify-comparator.sh` with only the con-ron
worker count set.

Two earlier attempts were stopped by the 14 GB cage (OOM kill):
- get-comparator: con-ron with its default 16 workers;
- get-comparator2: con-ron with 2 workers. It stopped after 45,000 of 45,355 checks, on the heavy kernel-decide records.

Palomar runs con-ron with its own settings, so on a 16 GB runner its worker count may matter. Its verdict does not
depend on the worker count.

**Source rules.** `scripts/check-lean-sources.py` passes: every file uses the module system and is under 10,000
lines. `Challenge.lean` has 194 lines.

**GET B.** `GET/BChecks.lean` runs the same no-overlap checks for GET B: its 16 cells do not cross, its 26
neighbouring translates do not cross it, and the dual-normal bound holds, so no other translate meets it. The build
takes 31 s and peaks at 5.6 GB. GET B is not used in the theorems.

## 4b. Route table of the morning (all steps now done)

Steps L1–L19 of the morning's plan are all done. They differ from the plan in four places:
- **L7** (soundness of separation): the bound lemma `cell_bounds` plus `plane` null sets.
- **L16** (frontier ⊆ faces): no per-contact certificates. The kernel recomputes the forced parameters of each touching
  pair.
- **L17** (sphere): no strict star-shapedness. The proof combines a generic radial lemma with injectivity on rays, from
  cone separation.
- **L12** (meet): forced parameters, as in L16.

## 4. The pilot (17 November, first half; kept as the base of the Solution)

Toolchain `leanprover/lean4:v4.35.0-rc2` and Mathlib `v4.35.0-rc2`, the same as the Kulaichev entry. The project uses
the module system. `decide +kernel` only, no `native_decide`.

| Module | What it proves | Build | Peak memory |
|---|---|---|---|
| `GET/ZPhi.lean` | ℤ[φ]: `toReal` is additive and multiplicative (`φ² = φ + 1`), `pos_sound`, `nonneg_sound`, `toReal_injective` | 2.4 s | 2.9 GB |
| `GET/Defs.lean`, `GET/Data.lean` | the model, the checks as `Bool` functions, and the data of A and B | 2–3 s each | 2.9 GB |
| `GET/Checks.lean` | for **A and B**: the faces are exactly the unshared cell faces (outward signs included); 30 faces; every zone has 10 faces; each side lies on exactly two faces; V = 32, E = 60; adjacent faces are not coplanar (with `threeIndependent`); volume = covolume, = 20 + 32φ for A; every face is matched by the opposite face of a lattice translate; the plane of every face misses the centre on its inner side; the 16 cells pairwise do not cross. Also `oneRhombus`: \|eᵢ\|² = 2 + φ and \|eᵢ · eⱼ\| = φ for all i ≠ j | 22 s | 3.5 GB |
| `GET/Translates.lean` | for A: no cell of P crosses any cell of t + P, t ∈ {−1,0,1}³ \ 0 (6,656 pairs) | 22 s | 6.1 GB |
| `GET/Real.lean` | for A over ℝ: Σ over the cells of \|det(eᵢ,eⱼ,eₖ)\| = \|det(lattice basis)\| = 20 + 32φ | 2.1 s | 2.9 GB |
| `GET/CellVolume.lean` | `volume (p +ᵥ parallelepiped v) = ofReal \|det\|` in `EuclideanSpace ℝ (Fin 3)`; a golden rhombohedron has volume \|D i j k\| | 3.2 s | 2.9 GB |
| `Challenge.lean` | the statement (2 `sorry`) | 2.2 s | 2.9 GB |

`#print axioms` on `A_volume_eq_covolume_real`, `volume_cell`, `A_zones` and `B_match` gives only `propext`,
`Classical.choice` and `Quot.sound`. `A_translates_separated` uses `propext` only.

**Python cross-check.** `scripts/gen_data.py` recomputes the same facts from the 2026-11-15 study data. It confirms that
the 30 faces rebuilt from the 16 cells equal the flip-search faces of candidates 0 and 1 up to translation, and writes
`data/get-data.json`. For A it finds:
- 14 touching translates in the box `{−2..2}³`, and no crossing among its 31,744 cell pairs;
- dual-basis norm 0.2701 and diameter 6.155, so any translate meeting P has coefficients |xᵣ| ≤ 1.66, hence in
  `{−1,0,1}`. This is the basis of L8; it is a floating-point estimate, and the exact version is L8.

**Face planes and the centre (pilot check).** For GET A and GET B, every face plane has the centre ½Σeᵢ strictly on
its inner side; this is checked exactly. On its own this does not prove star-shapedness. The Solution uses only the
weaker fact that the planes miss the centre (`A_planes`), together with cone separation.

## 5. Blockers before any submission

1. **Novelty (FIRM).** Senechal & Taylor, *Acta Cryst. A* 79 (2023) 273–279, is unread (closed access). The entry must
   not say "new" or "first" until it is checked. The free routes are an NDL copy or a library visit. R. Williams,
   *Natural Structure* (1972), p. 196, is also unread.
2. **Provenance (DICTO's choice).** The witness study is unpublished. There are two options:
   - an original-proof entry;
   - a DICTO paper on GET is published first, and the entry `formalizes` it.

   The yaml carries both as a TODO.
3. **Grünbaum 2010.** The DOI and journal pages are not yet looked up. Further remarks of the same passage, such as the
   one on indentations of T, are not quoted until they are checked against the journal pages.
4. **Scope check** before any paper draft: list every shape and result with its home project. GET B is a remark only.

## Files

- `lean/Challenge.lean`: the statement, with 4 `sorry`.
- `lean/Solution.lean`: the proof.
- `lean/GET/*.lean`: the library.
- `lean/comparator.json`: the Comparator file. It lists the four theorems and the three axioms.
- `lean/scripts/`: the source checks and the comparator scripts, from the Palomar template via the Kulaichev entry,
  plus `run_comparator_lowmem.sh`.
- `lean/build.sh`: a staged build on the compute host, with a 280 s limit and a 14 GB cap.
- `formalization.draft.yaml`: the metadata draft, with review fixes and the provenance TODO.
- `scripts/`: `gen_data.py`, `gen_certs.py`, `gen_sphere.py`, `gen_statement.py`, `getgeom.py`.
- `data/get-data.json`: the exact data.

Credits: the question and D1, D2 are Grünbaum's (2010). The solid and its name are DICTO's (study 2026-11-15). The Lean
code is with Claude (Anthropic).

## 6. Novelty check (17 November 2026, free sources only)

- **Grünbaum 2010** is now checked against the free preprint (University of Washington, hdl 1773/15593, version 2/3/10):
  Math. Intelligencer 32(4) (2010) 5–15, DOI 10.1007/s00283-010-9138-7. The open problem (preprint p. 17): "Given an
  even integer k ≥ 4, is there a rhombic monohedral parallelohedron such that every zone has exactly k faces? … No
  information is available for any k ≥ 10." On indentations (preprint p. 15): "An eightfold indentation of the
  triacontahedron T is shown in [39, page 196] … None of the other isozonohedra obtainable by indentation of F or T seem
  to be parallelohedra."
- **Inchbald's solid is not GET A or GET B: it is the study's candidate 2.** G. Inchbald, "A 3-D Quasicrystal
  Structure?", steelpillow.com (page updated 6 Dec 2024), section "Tilings and the dimpled rhombic triacontahedron": the
  rhombic triacontahedron with four of its eight cube-corner triplets dimpled, alternating with tetrahedral symmetry
  ("a conventional rhombic triacontahedron with an oblate hexahedron scooped out" at each), is a space-filler with cubic
  periodicity. Wayback: absent on 31 Mar 2022, dimpling text present on 23 Mar 2023. Symmetry check of the three
  depth-4 solids of `2026-11-15-grunbaum-k10/data/search6.json` (all 120 symmetries of the six-axis star, vertices
  centred; script `scratchpad getsym.py`, run on the compute host): GET A has 4 symmetries (2 rotations), GET B has 3
  (3 rotations), candidate 2 has 12 (the 12 rotations of the tetrahedral group). Only candidate 2 has Inchbald's
  tetrahedral symmetry, so his solid is candidate 2, which the 2026-11-15 study left undecided (covered exactly once,
  no exact certificate). GET A and GET B are different, lower-symmetry members of the same family (four corner
  indentations of T). Inchbald does not mention zones or Grünbaum's question; his solid, if it tiles by translation,
  is itself a k = 10 example, published before GET, and must be credited as such.
- **Senechal & Taylor 2023**, "Parallelohedra, old and new", Acta Cryst. A 79, 273–279, DOI 10.1107/S2053273323001444
  (closed access; no free copy found via Europe PMC, Unpaywall, arXiv). Abstract: "three new nonconvex parallelohedra
  are produced, a counterexample to a statement by Grünbaum." The statement is very likely the indentation sentence
  above, so the tetrahedrally indented T may be one of their three. Still unread.
- **Consequence.** The entry credits Inchbald's tetrahedral solid as an earlier k = 10 example of the same family
  (four corner indentations of T). GET A itself is not in Inchbald or Grünbaum; it may still be among Senechal–Taylor's
  three, so no "new" claim until that paper is read. GET A and GET B keep DICTO's name; Inchbald's solid goes by his name, the dimpled rhombic
  triacontahedron (Inchbald).
