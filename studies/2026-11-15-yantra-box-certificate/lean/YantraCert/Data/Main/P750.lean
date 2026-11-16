module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P750
open YantraCert

def cell : Cell := ⟨8, 214, 7, 87, 7, 65⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 9, 0, 9, 25, 0, 9, 25, 0, 0, 9, 0, 25, 0, 25, 25, 0, 9, 0, 25, 25, 0, 0, 0, 0, 25, 25, 9, 0, 25, 9, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9, 0, 0, 0, 0, 9, 25, 25, 0, 0, 9, 0, 25, 25, 0, 9, 0, 25, 25, 0, 0, 0, 25, 9, 25, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9]

theorem ok : checkTree C 9 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P750
