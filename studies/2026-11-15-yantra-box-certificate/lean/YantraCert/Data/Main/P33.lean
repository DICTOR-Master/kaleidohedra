module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P33
open YantraCert

def cell : Cell := ⟨10, 261, 10, 5, 9, 114⟩
noncomputable def codes : TC := TC.ofList [290]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P33
