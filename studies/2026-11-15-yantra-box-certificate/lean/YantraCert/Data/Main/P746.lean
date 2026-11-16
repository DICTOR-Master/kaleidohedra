module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P746
open YantraCert

def cell : Cell := ⟨7, 107, 7, 86, 7, 64⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 9, 0, 9, 0, 0, 9, 0, 9, 25, 0, 9, 0, 9, 25, 0, 9, 0, 9, 0, 0, 9, 0, 9, 0, 25, 25, 0, 9, 0, 9, 0, 0, 9, 25, 0, 9, 0, 9, 25]

theorem ok : checkTree C 12 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P746
