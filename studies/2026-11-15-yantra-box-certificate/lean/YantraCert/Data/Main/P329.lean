module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P329
open YantraCert

def cell : Cell := ⟨2, 3, 1, 0, 1, 0⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 98, 226, 0, 0, 226, 0, 0, 9, 9, 0, 266, 266, 226, 0, 0, 98, 0, 0, 9, 9, 0, 9, 9, 0, 0, 0, 0, 9, 9, 0, 0, 282, 0, 9, 0, 82, 82, 282, 0, 0, 9, 9, 0, 0, 0, 9, 0, 0, 0, 9, 9, 0, 9, 9, 82, 0, 9, 0, 0, 0, 9, 9, 0, 9, 9, 0, 0, 9, 9, 0, 9, 9, 0, 90, 0, 9, 0, 82, 82, 0, 0, 0, 266, 234, 0, 266, 234, 0, 0, 282, 0, 266, 0, 98, 282, 0, 282, 0, 266, 282]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P329
