module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P498
open YantraCert

def cell : Cell := ⟨17, 98361, 17, 59273, 16, 34055⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 25, 0, 0, 9, 0, 25, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 25, 0, 0, 0, 0, 0, 9, 0, 25, 41, 25, 9, 0, 0, 0, 0, 9, 0, 41, 0, 41, 9, 9, 25, 41, 0, 0, 25, 9, 0, 25, 0, 0, 0, 25, 41, 9, 0, 0, 25, 0, 41, 25, 9, 25, 0, 41, 0, 9, 0, 0, 0, 9, 0, 0, 0, 0, 0, 41, 25, 41, 9, 0, 0, 25, 41, 9, 41, 0, 9, 0, 25, 0, 41, 0, 0, 25, 9, 0, 25, 41, 41, 0, 9, 0, 25, 0, 0, 9, 0, 0, 0, 9, 0, 25, 0, 0, 25, 0, 25, 0, 41, 25, 25, 25, 0, 0, 9, 0, 0, 41, 0, 9, 0, 0, 41, 25, 41, 41, 0, 9, 0, 0, 0, 9, 0, 25, 41, 25, 41, 0, 9, 0, 25, 0, 0, 9, 0, 25, 0, 0, 9, 0, 25, 9, 25, 25, 9, 0, 9, 0, 25, 9, 25]

theorem ok : checkTree C 24 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P498
