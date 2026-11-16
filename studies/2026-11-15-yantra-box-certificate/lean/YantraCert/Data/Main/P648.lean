module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P648
open YantraCert

def cell : Cell := ⟨2, 3, 2, 3, 2, 0⟩
noncomputable def codes : TC := TC.ofList [0, 98, 0, 0, 9, 9, 19]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P648
