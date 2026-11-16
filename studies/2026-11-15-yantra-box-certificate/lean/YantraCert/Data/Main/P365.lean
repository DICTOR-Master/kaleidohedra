module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P365
open YantraCert

def cell : Cell := ⟨8, 190, 7, 57, 7, 66⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 25, 0, 25, 25, 9, 0, 0, 25, 25, 9]

theorem ok : checkTree C 6 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P365
