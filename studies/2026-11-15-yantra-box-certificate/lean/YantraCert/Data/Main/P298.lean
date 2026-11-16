module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P298
open YantraCert

def cell : Cell := ⟨3, 5, 3, 0, 2, 1⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 226, 0, 9, 9, 9, 0, 0, 226, 0, 0, 266, 234, 266, 226]

theorem ok : checkTree C 7 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P298
