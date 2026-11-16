module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P737
open YantraCert

def cell : Cell := ⟨8, 212, 7, 84, 7, 65⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 9, 0, 0, 9, 0, 9, 0, 0, 9, 0, 25, 0, 0, 0, 9, 41, 0, 25, 41, 0, 0, 9, 25, 0, 25, 25, 0, 9, 0, 25, 0, 25, 25, 0, 9, 0, 9, 0, 0, 9, 0, 25, 25, 0, 9, 25, 0, 9, 0, 9, 0, 0, 9, 0, 9, 0, 25, 25, 0, 9, 0, 9, 25]

theorem ok : checkTree C 14 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P737
