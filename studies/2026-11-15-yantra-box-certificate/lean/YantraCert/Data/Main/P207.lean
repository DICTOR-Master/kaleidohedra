module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P207
open YantraCert

def cell : Cell := ⟨6, 21, 6, 1, 5, 7⟩
noncomputable def codes : TC := TC.ofList [0, 1, 0, 306, 9]

theorem ok : checkTree C 4 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P207
