module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P65
open YantraCert

def cell : Cell := ⟨8, 66, 7, 0, 7, 29⟩
noncomputable def codes : TC := TC.ofList [9]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P65
