module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P689
open YantraCert

def cell : Cell := ⟨6, 50, 6, 37, 5, 16⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 9, 0, 25, 25, 26, 0, 0, 9, 0, 0, 0, 25, 25, 25, 0, 0, 0, 25, 25, 0, 25, 25, 0, 0, 25, 25, 0, 25, 25, 0, 9, 0, 0, 25, 25, 0, 0, 25, 25, 0, 25, 25]

theorem ok : checkTree C 10 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P689
