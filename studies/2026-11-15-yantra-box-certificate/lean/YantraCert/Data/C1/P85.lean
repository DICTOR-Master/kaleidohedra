module

public import YantraCert.Data.C1.Polys

@[expose] public section

namespace YantraCert.Data.C1.P85
open YantraCert

def cell : Cell := ⟨7, 37, 7, 64, 7, 22⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 25, 25, 0, 25, 25, 25, 0, 0, 1, 0, 0, 25, 25, 0, 25, 25, 25, 0, 1, 25, 0, 0, 1, 0, 0, 0, 1, 0, 0, 25, 25, 0, 25, 25, 25, 0, 0, 1, 0, 0, 25, 25, 0, 25, 25, 25, 0, 1, 25, 0, 1, 41, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 25, 25, 0, 25, 25, 25, 0, 0, 1, 0, 0, 25, 25, 0, 25, 25, 25, 0, 1, 25, 0, 0, 1, 0, 0, 0, 1, 0, 0, 25, 25, 9, 25, 9, 0, 1, 0, 25, 9, 0, 1, 0, 41, 41, 0, 1, 41, 9, 0, 1, 41, 9, 194, 9]

theorem ok : checkTree C 22 cell codes = true := by decide +kernel

end YantraCert.Data.C1.P85
