module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P538
open YantraCert

def cell : Cell := ⟨10, 769, 9, 231, 9, 266⟩
noncomputable def codes : TC := TC.ofList [0, 25, 0, 0, 25, 25, 9]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P538
