module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P355
open YantraCert

def cell : Cell := ⟨6, 46, 5, 14, 5, 16⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 26, 0, 0, 0, 25, 9, 0, 25, 25, 0, 25, 25, 9, 26]

theorem ok : checkTree C 8 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P355
