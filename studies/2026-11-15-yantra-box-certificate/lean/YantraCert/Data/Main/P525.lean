module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P525
open YantraCert

def cell : Cell := ⟨11, 1536, 11, 927, 10, 532⟩
noncomputable def codes : TC := TC.ofList [0, 25, 9]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P525
