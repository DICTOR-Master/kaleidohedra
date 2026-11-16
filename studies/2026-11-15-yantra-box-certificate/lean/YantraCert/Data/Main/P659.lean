module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P659
open YantraCert

def cell : Cell := ⟨6, 55, 6, 49, 5, 15⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 0, 9, 0, 9, 186, 186, 0, 26, 0, 0, 0, 0, 0, 0, 26, 0, 0, 178, 0, 25, 9, 178, 0, 26, 9, 26, 186, 9, 0, 0, 26, 186, 9]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P659
