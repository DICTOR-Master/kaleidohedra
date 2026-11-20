# Grünbaum's zone question at k = 10 (Lean 4 + Mathlib)

Author: DICTO.

## The theorems

B. Grünbaum (*Math. Intelligencer* 32(4), 2010) asked: "Given an even integer k ≥ 4, is there a rhombic monohedral
parallelohedron such that every zone has exactly k faces?" The cases k = 4, 6 are classical, k = 8 is his, and he wrote
that "no information is available for any k ≥ 10". The Challenge proves an example for k = 10:

1. **`grunbaum_k10`**: there is a polyhedron `P` of spherical type (a compact solid, the closure of its interior, whose
   frontier is the union of its 30 distinct parallelogram faces and is homeomorphic to the sphere; faces meet in a
   common side, a common corner or not at all; adjacent faces are not coplanar), whose 30 faces are congruent rhombi
   with diagonals in the golden ratio, in which every zone has exactly 10 faces, and whose translates by a lattice
   cover space with pairwise disjoint interiors, face to face.
2. **`grunbaum_k10_parallelohedron`**: the same in Grünbaum's own terms (some set of translates tiles space).
3. **`cube_everyZoneHas`**, **`rhombicDodecahedron_everyZoneHas`**: calibration of the zone definition, which gives 4
   for the cube and 6 for the rhombic dodecahedron.

The witness is DICTO's Grünbaum–Escher Triacontahedron **GET B**: the rhombic triacontahedron less four oblate golden
rhombohedra, a union of 16 golden rhombohedra. It is not part of the statement.

- `Challenge.lean`: the definitions and the four statements, with every proof `sorry`. It imports only Mathlib.
- `Solution.lean`: the four proofs, from the library.
- `GET/`: the library (23 modules, namespace `GET`): exact arithmetic in ℤ[φ] with a verified embedding into ℝ; zone
  certificates with a generic soundness lemma; the cells, the lattice, separation of the cells and of the neighbouring
  translates; volume = covolume (20 + 32φ) and Mathlib's `ZSpan` fundamental domains for the cover; the frontier as
  the union of the 30 faces; faces meeting properly; the sphere by radial projection from an interior point.
  `GET/Statement.lean` repeats the Challenge's definitions word for word. The exact data and certificates are written
  by Python generators; every one of them is re-decided by the kernel (`decide +kernel`).

Toolchain `leanprover/lean4:v4.35.0-rc2`, Mathlib `v4.35.0-rc2`. The four theorems depend only on the axioms
`propext`, `Classical.choice` and `Quot.sound`. Neither `sorry` nor `native_decide` is used. Every Lean file uses the
module system.

## Earlier solids of this family

The rhombic triacontahedron with four corners indented was shown on the web as a space-filler before this work,
without proof, without zone sizes and without reference to Grünbaum's question: by D. Hall (Sketchfab, June 2016; the same
solid as G. Inchbald's dimpled rhombic triacontahedron, by 2023), and by J. Kostick (vZome, April 2022), whose
concavo-convex triacon array shows GET A, the sibling of GET B. GET B itself was not found in the sources checked.
`formalization.yaml` lists every source checked.

## How it was made

DICTO set the question, found and named the solids, and chose the witness. A Claude Code agent (Claude Opus, Anthropic)
wrote the definitions, the statements, the generators and the proofs, and ran the checks. `formalization.yaml`
(section `automation`) records this in full.

## Checks

`scripts/check-lean-sources.py` and `scripts/verify-comparator.sh` come from Palomar's entry template (PalomarRegistry).
They check the source rules and run `lake comparator` the way Palomar does.

## Licence

Apache-2.0 (see `LICENSE`). Copyright 2026 DICTO.

## Other work by DICTO

- ORCID (all works): https://orcid.org/0009-0001-2620-2036
- Website: https://dictospheres.com

## Paper

The statement formalized here is Theorem 1 of DICTO, *Ten Faces in Every Zone: Grünbaum's Question at k = 10* (paper #115), DICTO DOI 10.5281/zenodo.24389006.
