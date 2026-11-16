module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P203
open YantraCert

def cell : Cell := ⟨8, 84, 8, 2, 7, 31⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 41, 0, 274, 0, 0, 41, 82, 258, 138]

theorem ok : checkTree C 8 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P203
