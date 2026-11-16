module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P716
open YantraCert

def cell : Cell := ⟨4, 13, 4, 9, 4, 9⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 9, 0, 9, 9, 9]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P716
