# Kulaichev's Śrī Yantra is unique (Lean 4 + Mathlib)

Author: DICTO.

## The theorem

Draw a circle of diameter 1 and nine isosceles triangles `t1, …, t9` on one vertical axis, `t1–t5` pointing down and
`t6–t9` pointing up. Ask for the classical conditions of the Śrī Yantra in Huet's form, as given by Chiodo: the two great
triangles are inscribed, seven apexes lie on bases, and the 18 marmas (points where three lines meet) and the 6 corner
touches hold. Add A. P. Kulaichev's four conditions: the two great triangles are congruent, the corners of `t1` and of
`t9` lie on the circle, and the centre of the circle is the incentre of the innermost triangle. Finally ask that the
figure be well formed (admissible, as in DICTO's paper #103): the bases in order, every half-width positive, every apex
on the correct side of its base, and every corner in the disc. Then **exactly one figure exists**, and its slope `w7/b7`
lies in an interval of width 2⁻²¹ around 0.75043851602221…

Kulaichev asked this question in 1984 (*Indian Journal of History of Science* 19.3, pp. 284–285). A. Chiodo
(*Comptes Rendus Mathématique* 359, 2021, pp. 381, 387) described it as still open.

- `Challenge.lean`: the statement, with every proof `sorry`.
- `Solution.lean`: the same statement, word for word, with proofs.
- `YantraCert/`: the library behind the proofs:
  - a kernel-evaluated box checker, proved sound, and a certificate of 64,613 rational boxes in 10 charts, checked by
    `decide +kernel`;
  - a Krawczyk box, giving uniqueness by a contraction and existence by Banach's fixed-point theorem from Mathlib;
  - a verified sparse-polynomial normaliser for the identities between the geometry and the certificate;
  - the chart coverings, the case split, and the rebuilt figure.
- The modules under `YantraCert/Data` and `YantraCert/Deriv`, `YantraCert/KBoxData.lean` and a few top-level ones are
  generated. Their generators are in the study linked below.

Toolchain `leanprover/lean4:v4.35.0-rc2`, Mathlib `v4.35.0-rc2`. The two theorems depend only on the axioms `propext`,
`Classical.choice` and `Quot.sound`. Neither `sorry` nor `native_decide` is used. Every Lean file uses the module system.

## How it was made

DICTO set the question and the order of the work. A Claude Code agent (Claude Opus, Anthropic) wrote the statements, the
proofs and the generators, and ran the checks. `formalization.yaml` (section `automation`) records this in full.

## Related work

- C. S. Rao, *Śrīyantra: A Study of Spherical and Plane Forms*, *IJHS* 33.3 (1998) 203–227. It computes the same figure
  numerically, as Rao's constraints 1, 2, 8, 9, 20, and makes no claim of uniqueness.
- S.-E. Gherbi, *sri-yantra-constraint-engine* (doi:10.5281/zenodo.20617730). It reimplements Rao's constraint system and
  corrects four transcription errata in Rao's printed equations. It makes no uniqueness claim. The statement here uses
  Huet's and Kulaichev's conditions, not Rao's equations.
- `formalization.yaml` lists every source checked, with pages.

## The study

The certificate, its generators, the controls and the full check record are in the study
[studies/2026-11-15-yantra-box-certificate](https://github.com/DICTOR-Master/kaleidohedra/tree/research-fig3/studies/2026-11-15-yantra-box-certificate)
of DICTOR-Master/kaleidohedra (branch `research-fig3`). This repository holds only the Lean project, as assembled by that
study's `scripts/c14_palomar_entry.py`.

`scripts/check-lean-sources.py` and `scripts/verify-comparator.sh` come from Palomar's entry template
(PalomarRegistry). They check the source rules and run `lake comparator` the way Palomar does.

## Licence

Apache-2.0 (see `LICENSE`). Copyright 2026 DICTO.

## Other work by DICTO

- ORCID (all works): https://orcid.org/0009-0001-2620-2036
- Website: https://dictospheres.com
- *The DICTO Yantra* (#103), the companion paper on this figure. DICTO DOI: [10.5281/zenodo.24052633](https://doi.org/10.5281/zenodo.24052633)
- *Silent Running: Twisted Silence* (#109). DICTO DOI: [10.5281/zenodo.24272473](https://doi.org/10.5281/zenodo.24272473)
- *Walls of Silence: The Walls of the Six Hundred* (#110). DICTO DOI: [10.5281/zenodo.24272477](https://doi.org/10.5281/zenodo.24272477)
- *DICTO: Collected Geometric Works*. DICTO DOI: [10.5281/zenodo.23345699](https://doi.org/10.5281/zenodo.23345699)
- OEIS [A400949](https://oeis.org/A400949): closed non-backtracking walks on the diamond network.
