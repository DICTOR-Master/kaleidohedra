module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P336
open YantraCert

def cell : Cell := ⟨7, 92, 6, 25, 6, 32⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 0, 25, 25, 0, 9, 25, 25, 0, 0, 9, 0, 0, 0, 0, 25, 0, 41, 25, 0, 9, 0, 41, 25, 0, 25, 25, 0, 0, 9, 0, 0, 0, 0, 41, 0, 25, 41, 9, 0, 0, 41, 41, 9, 0, 25, 0, 0, 0, 25, 41, 9, 0, 0, 25, 25, 25, 0, 9, 0, 0, 41, 25, 0, 0, 0, 41, 9, 0, 41, 25, 0, 0, 41, 9, 0, 41, 41, 0, 9, 0, 25, 0, 0, 9, 0, 25, 0, 0, 41, 41, 41, 0, 9, 0, 25, 25, 0, 9, 9, 0, 0, 25, 0, 0, 9, 0, 25, 25, 0, 9, 25, 0, 9, 9]

theorem ok : checkTree C 15 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P336
