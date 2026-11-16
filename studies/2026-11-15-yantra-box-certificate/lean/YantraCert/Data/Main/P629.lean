module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P629
open YantraCert

def cell : Cell := ⟨8, 220, 7, 94, 7, 62⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 9, 9, 0, 9, 0, 9, 9]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P629
