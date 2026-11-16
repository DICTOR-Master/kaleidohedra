module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P192
open YantraCert

def cell : Cell := ⟨8, 81, 8, 3, 7, 31⟩
noncomputable def codes : TC := TC.ofList [18]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P192
