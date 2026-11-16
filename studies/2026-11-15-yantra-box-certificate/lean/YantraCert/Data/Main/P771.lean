module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P771
open YantraCert

def cell : Cell := ⟨7, 108, 7, 89, 7, 65⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 0, 0, 25, 9, 9, 0, 0, 25, 9, 9, 9, 9, 0, 0, 0, 0, 0, 25, 9, 9, 0, 0, 25, 9, 9, 9, 9, 9]

theorem ok : checkTree C 9 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P771
