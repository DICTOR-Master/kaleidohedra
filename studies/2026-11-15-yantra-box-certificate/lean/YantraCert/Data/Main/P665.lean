module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P665
open YantraCert

def cell : Cell := ⟨6, 48, 5, 16, 5, 16⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 0, 0, 0, 25, 25, 0, 9, 9, 26, 0, 0, 0, 25, 0, 0, 9, 25, 25, 0, 25, 0, 0, 0, 25, 25, 9, 0, 25, 9, 0, 0, 25, 0, 25, 25, 0, 25, 0, 25, 25, 0, 9, 0, 26, 0, 0, 0, 25, 25, 0, 25, 25, 0, 0, 25, 25, 0, 25, 25]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P665
