module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P415
open YantraCert

def cell : Cell := ⟨15, 24588, 14, 7408, 14, 8513⟩
noncomputable def codes : TC := TC.ofList [25]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P415
