module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P654
open YantraCert

def cell : Cell := ⟨6, 54, 5, 24, 5, 15⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 9, 26, 306]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P654
