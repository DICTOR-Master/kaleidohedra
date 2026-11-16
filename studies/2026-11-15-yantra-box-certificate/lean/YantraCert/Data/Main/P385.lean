module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P385
open YantraCert

def cell : Cell := ⟨5, 23, 5, 15, 4, 8⟩
noncomputable def codes : TC := TC.ofList [0, 0, 306, 0, 0, 0, 26, 0, 0, 9, 0, 25, 9, 0, 9, 0, 25, 9, 0, 0, 26, 25, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 9, 0, 0, 25, 0, 0, 9, 25, 25, 0, 26, 0, 0, 25, 9, 25, 0, 9, 9]

theorem ok : checkTree C 10 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P385
