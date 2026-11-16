module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P580
open YantraCert

def cell : Cell := ⟨4, 13, 3, 3, 3, 4⟩
noncomputable def codes : TC := TC.ofList [0, 90, 0, 0, 82, 82, 0, 82, 9]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P580
