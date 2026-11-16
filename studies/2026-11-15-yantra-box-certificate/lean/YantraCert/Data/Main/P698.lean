module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P698
open YantraCert

def cell : Cell := ⟨6, 50, 5, 19, 5, 16⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 26, 0, 0, 9, 0, 25, 0, 25, 25, 26, 26]

theorem ok : checkTree C 9 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P698
