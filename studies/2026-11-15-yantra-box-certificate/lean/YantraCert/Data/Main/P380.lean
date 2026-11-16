module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P380
open YantraCert

def cell : Cell := ⟨9, 383, 9, 231, 8, 132⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 25, 0, 0, 9, 0, 25, 0, 0, 9, 0, 25, 0, 0, 9, 0, 25, 25, 25, 25, 25]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P380
