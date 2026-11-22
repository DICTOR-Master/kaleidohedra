# Dehn Packets in Lean: two icosahedral pairs that cannot fill space (Lean 4 + Mathlib)

Author: DICTO.

## The theorems

The pieces are convex polytopes: bounded intersections of finitely many closed half-spaces with interior points.
A tiling (`ConvexTiling`) covers 3-space with such pieces, with disjoint interiors, locally finite; it need not be
face to face. A copy of a piece is its image under a similarity: a motion, a reflection, a positive scaling.

- **Lemma 3** (`lemma3`): π, α = arctan φ, β = arccos(1/√6) and γ = arccos(√(2/3)) are linearly independent over ℚ.
- **Lemma 2** (`lemma2`): at a point inside an edge of a tiling, the dihedral angles of the tiles meeting there
  (with π for a tile whose face passes through the point and 2π for one containing it inside) sum to 2π.
- **Theorem 4 (a)** (`theorem4a_copies`): in a tiling by copies of the dodecahedron centre pyramid, the truncated
  icosahedron, the dodecahedron, the icosahedron, the truncated octahedron, the truncated cuboctahedron, and any
  convex pieces whose dihedral angles are all rational multiples of π, no tile is a copy of the pyramid or of the
  truncated icosahedron.
- **Theorem 4 (b)** (`theorem4b_copies`): the same for the icosahedron centre pyramid and the truncated dodecahedron.
- `theorem4a_tiling`, `theorem4b_tiling` (in the library): the same for any convex tiles whose dihedral angles lie in
  the stated lists, given as a hypothesis.

Each named solid is built from exact coordinates, in Q(√5) or Q(√2), and its dihedral angles are read from the set
itself (`X_edgeAngle` in `Packets/Solids.lean`), using the set-defined angle of the Dehn Canon.

- `Challenge.lean`: the definitions and the four statements, with every proof `sorry`. It imports only Mathlib.
- `Solution.lean`: the proofs, from the library.
- `Packets/`: the library (namespaces `Packets`, `PacketsGen`, and `DehnCanon.Library` in `Packets/Canon/`).

Toolchain `leanprover/lean4:v4.35.0-rc2`, Mathlib `v4.35.0-rc2`. The theorems depend only on the axioms `propext`,
`Classical.choice` and `Quot.sound`. Neither `sorry` nor `native_decide` is used. Every Lean file uses the module
system.

## How to check

```
lake exe cache get
lake build
```

## Files

| file | content |
|---|---|
| `Packets/Angles.lean` | Lemma 3: independence of π, α, β, γ over ℚ (Niven's theorem and a field argument) |
| `Packets/Rings.lean` | the angle lists as rational coordinates; Theorem 4 (c) |
| `Packets/Tiling.lean` | Theorem 4 (a), (b) from the ring condition |
| `Packets/Cones.lean`, `Packets/Lemma2.lean` | Lemma 2 for every convex tiling |
| `Packets/Pieces.lean` | angles under similarities; angles from edge data |
| `Packets/Gen*.lean` | generated edge data of the solids (by `scripts/gen_pieces.py`) |
| `Packets/Values.lean`, `Packets/Solids.lean` | the angles of each solid |
| `Packets/Copies.lean` | Theorem 4 (a), (b) for copies |
| `Packets/Canon/` | 26 modules of DICTO's Dehn Canon, unchanged from its registered commit except that their imports read `Packets.Canon` |

The Dehn Canon (https://github.com/DICTOR-Master/dehn-canon-lean, commit `9ea20f6dfd64fc3f10f64b1fb59a754a77e5cf57`,
Palomar PALOMAR-2026-11-20-000003) is included in `Packets/Canon/` rather than required as a Git dependency: its
repository has its own root modules `Challenge` and `Solution`, which would shadow this entry's.

## Earlier work

The Lean statements are Lemma 2, Lemma 3 and Theorem 4 (a), (b) of the paper below (#117), where the result was first
found. Lemma 2 there is taken from DICTO's *Aristotle's Pyramid* (Lemma 1); it is the edge count behind Debrunner's
theorem (Arch. Math. 35, 1980). `formalization.yaml` lists every source checked.

## Papers

- DICTO, *From Dehn Packets to Scutoids: How the Fullerene Star Fills Space*, Zenodo, DICTO DOI:
  10.5281/zenodo.24411660 (where the result was first found).
- DICTO, *The Dehn Canon: Hilbert's Third Problem, Machine-Checked*, Zenodo, DICTO DOI: 10.5281/zenodo.24383552.

## How it was made

DICTO set the question and the order of the work, with Claude (Anthropic): the Lean code was written by a Claude Code
agent. `formalization.yaml` (section `automation`) records this in full.

## Checks

`scripts/check-lean-sources.py` and `scripts/verify-comparator.sh` come from Palomar's entry template (PalomarRegistry).
They check the source rules and run `lake comparator` the way Palomar does. `scripts/gen_pieces.py` (with `q5.py`,
`q2.py` and `mk_solids.py`) writes the generated solids.

## Licence

Apache-2.0 (see `LICENSE`). Copyright 2026 DICTO.

## Other work by DICTO

- ORCID (all works): https://orcid.org/0009-0001-2620-2036
- Website: https://dictospheres.com
