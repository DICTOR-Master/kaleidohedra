module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P509
open YantraCert

def cell : Cell := ⟨17, 98363, 16, 29637, 16, 34056⟩
noncomputable def codes : TC := TC.ofList [0, 25, 0, 41, 9]

theorem ok : checkTree C 4 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P509
