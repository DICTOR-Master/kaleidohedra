module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P609
open YantraCert

def cell : Cell := ⟨8, 218, 7, 92, 7, 63⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 9, 0, 0, 9, 0, 25, 0, 25, 25, 0, 9, 0, 25, 25, 0, 9, 0, 9, 0, 0, 9, 0, 25, 25, 0, 9, 0, 25, 25]

theorem ok : checkTree C 9 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P609
