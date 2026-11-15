# Kulaichev's Śrī Yantra is unique (Lean 4 + Mathlib)

`Challenge.lean` states the theorem: nine isosceles triangles in a circle that meet Huet's conditions (Chiodo's form),
Kulaichev's (a)–(d) and #103's admissibility form exactly one figure, whose slope `w7/b7` lies in a stated interval.
`Solution.lean` repeats it word for word with proofs. The proofs come from the library `YantraCert`:

* `Check`, `Sound`, `Cover`: a kernel-evaluated box checker (monotone split, after R. E. Moore; slope form, after R. Krawczyk
  and A. Neumaier) proved sound; `Data/*`: the 64,613-box certificate in 10 charts, checked by `decide +kernel`.
* `Krawczyk`, `KBox`: Krawczyk's test; uniqueness by a contraction, existence by Banach's fixed-point theorem (Mathlib).
* `ZPoly`, `Frac`, `Deriv/*`: a verified sparse-polynomial normaliser and the identities between the geometry and the
  certificate's polynomials; `Geom*`: the construction forced by the conditions.
* `Charts`, `BoxBounds`, `Unique*`: the box bounds, the chart coverings and the case split; `Exist*`: the rebuilt figure.

Toolchain `leanprover/lean4:v4.35.0-rc2`, Mathlib `v4.35.0-rc2`. Axioms: `propext`, `Classical.choice`, `Quot.sound`.
Nothing here has been submitted.
