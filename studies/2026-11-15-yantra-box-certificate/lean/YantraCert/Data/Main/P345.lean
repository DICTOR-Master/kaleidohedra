module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P345
open YantraCert

def cell : Cell := ⟨7, 94, 7, 55, 6, 32⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 25, 0, 25, 25, 25, 0, 0, 9, 0, 0, 0, 9, 25, 25, 0, 0, 9, 0, 0, 0, 9, 0, 25, 0, 41, 25, 25, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 41, 41, 25, 0, 9, 0, 41, 0, 0, 9, 0, 41, 9, 41, 9, 0, 9, 0, 0, 0, 9, 41, 25, 9, 0, 9, 0, 25, 0, 0, 9, 0, 25, 9, 0, 9, 25, 0, 9, 0, 25, 0, 0, 9, 0, 25, 25, 25]

theorem ok : checkTree C 19 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P345
