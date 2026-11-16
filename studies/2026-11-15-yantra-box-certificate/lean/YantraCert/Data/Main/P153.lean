module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P153
open YantraCert

def cell : Cell := ⟨7, 37, 7, 0, 7, 31⟩
noncomputable def codes : TC := TC.ofList [1]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P153
