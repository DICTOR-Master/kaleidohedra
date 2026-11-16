module

public import YantraCert.Data.C1.Polys

@[expose] public section

namespace YantraCert.Data.C1.P19
open YantraCert

def cell : Cell := ⟨9, 130, 9, 257, 8, 45⟩
noncomputable def codes : TC := TC.ofList [0, 1, 41]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.C1.P19
