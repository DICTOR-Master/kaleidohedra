module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P477
open YantraCert

def cell : Cell := ⟨21, 1573783, 21, 948357, 20, 544894⟩
noncomputable def codes : TC := TC.ofList [25]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P477
