module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P552
open YantraCert

def cell : Cell := ⟨8, 192, 8, 117, 8, 132⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 0, 25, 9, 25, 9]

theorem ok : checkTree C 6 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P552
