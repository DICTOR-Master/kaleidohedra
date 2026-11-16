module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P745
open YantraCert

def cell : Cell := ⟨7, 106, 6, 43, 6, 32⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 0, 0, 9, 0, 9, 0, 25, 25, 0, 9, 0, 9, 25, 0, 0, 9, 0, 0, 0, 9, 25, 25, 0, 0, 0, 25, 25, 0, 25, 9, 0, 0, 25, 25, 0, 25, 9, 0, 9, 0, 0, 25, 25, 0, 0, 25, 0, 25, 9, 0, 25, 25, 0, 9, 0, 0, 0, 9, 0, 9, 25, 26, 0, 0, 9, 0, 25, 0, 25, 25, 0, 9, 0, 25, 0, 25, 25]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P745
