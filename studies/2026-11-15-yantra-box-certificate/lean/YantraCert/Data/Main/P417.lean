module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P417
open YantraCert

def cell : Cell := ⟨16, 49178, 15, 14816, 15, 17027⟩
noncomputable def codes : TC := TC.ofList [41]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P417
