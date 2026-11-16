module

public import YantraCert.ZPoly2

@[expose] public section

/-!
# Signs on a box with a common denominator, Lean core only (copies of `spq`, `NP.vq`, `SP.boxSign` of `Krawczyk`/`Frac`,
with the corners passed as numerals, so that the kernel checks need no Mathlib)
-/

namespace YantraCert

def spqC (D Q n a : Nat) : Nat := n ^ a * Q ^ (D - a)
noncomputable def NP.vqC (Dx Dy Dz Q nx ny nz : Nat) (p : NP) : Nat := p.ev (spqC Dx Q nx) (spqC Dy Q ny) (spqC Dz Q nz)
noncomputable def SP.boxSignN (p : SP) (Q l0 l1 l2 h0 h1 h2 : Nat) : Nat :=
  cond (Nat.blt (p.pn.vqC p.Dx p.Dy p.Dz Q h0 h1 h2) (p.pp.vqC p.Dx p.Dy p.Dz Q l0 l1 l2)) 1
    (cond (Nat.blt (p.pp.vqC p.Dx p.Dy p.Dz Q h0 h1 h2) (p.pn.vqC p.Dx p.Dy p.Dz Q l0 l1 l2)) 2 0)

end YantraCert
