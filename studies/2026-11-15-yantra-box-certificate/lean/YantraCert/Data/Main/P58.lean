module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P58
open YantraCert

def cell : Cell := ⟨8, 67, 8, 0, 7, 28⟩
noncomputable def codes : TC := TC.ofList [226]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P58
