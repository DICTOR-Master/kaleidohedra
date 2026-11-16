module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P356
open YantraCert

def cell : Cell := ⟨6, 47, 6, 28, 6, 32⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 0, 25, 0, 0, 9, 0, 25, 25, 0, 9, 25, 0, 9, 0, 25, 0, 25, 25, 0, 0, 9, 0, 0, 0, 9, 9, 0, 9, 9, 9, 0, 9, 0, 0, 0, 9, 9, 0, 9, 9, 9]

theorem ok : checkTree C 9 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P356
