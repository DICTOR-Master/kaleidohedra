module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P581
open YantraCert

def cell : Cell := ⟨3, 6, 3, 3, 3, 5⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 9, 0, 9, 9, 0, 90, 0, 0, 9, 9, 9]

theorem ok : checkTree C 6 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P581
