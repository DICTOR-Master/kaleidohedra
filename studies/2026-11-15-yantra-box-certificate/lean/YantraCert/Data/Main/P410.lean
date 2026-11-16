module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P410
open YantraCert

def cell : Cell := ⟨11, 1537, 10, 462, 10, 532⟩
noncomputable def codes : TC := TC.ofList [0, 25, 0, 25, 9]

theorem ok : checkTree C 4 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P410
