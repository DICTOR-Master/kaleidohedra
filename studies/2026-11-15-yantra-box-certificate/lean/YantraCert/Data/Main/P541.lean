module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P541
open YantraCert

def cell : Cell := ⟨8, 193, 7, 57, 7, 66⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 25, 0, 9, 0, 25, 25]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P541
