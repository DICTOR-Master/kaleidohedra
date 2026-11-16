module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P540
open YantraCert

def cell : Cell := ⟨9, 385, 8, 115, 8, 133⟩
noncomputable def codes : TC := TC.ofList [0, 25, 0, 25, 9]

theorem ok : checkTree C 4 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P540
