module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P305
open YantraCert

def cell : Cell := ⟨4, 11, 3, 1, 3, 3⟩
noncomputable def codes : TC := TC.ofList [0, 266, 0, 0, 9, 9, 0, 82, 258]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P305
