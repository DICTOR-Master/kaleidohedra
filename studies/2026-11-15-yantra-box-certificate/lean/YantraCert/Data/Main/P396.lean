module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P396
open YantraCert

def cell : Cell := ⟨9, 384, 9, 230, 8, 133⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 25, 0, 0, 0, 25, 0, 0, 0, 25, 0, 0, 9, 25, 9, 25, 9, 25, 9, 25, 9]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P396
