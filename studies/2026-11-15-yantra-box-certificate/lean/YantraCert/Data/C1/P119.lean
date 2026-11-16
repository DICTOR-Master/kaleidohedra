module

public import YantraCert.Data.C1.Polys

@[expose] public section

namespace YantraCert.Data.C1.P119
open YantraCert

def cell : Cell := ⟨4, 4, 4, 8, 4, 3⟩
noncomputable def codes : TC := TC.ofList [1]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.C1.P119
