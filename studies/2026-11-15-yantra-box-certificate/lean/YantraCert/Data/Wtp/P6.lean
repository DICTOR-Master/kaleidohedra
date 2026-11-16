module

public import YantraCert.Data.Wtp.Polys

@[expose] public section

namespace YantraCert.Data.Wtp.P6
open YantraCert

def cell : Cell := ⟨2, 2, 2, 3, 2, 3⟩
noncomputable def codes : TC := TC.ofList [0, 82, 0, 82, 0, 82, 9]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Wtp.P6
