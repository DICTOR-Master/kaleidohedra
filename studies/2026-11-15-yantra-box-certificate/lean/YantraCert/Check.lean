/-!
# Kernel-evaluated box checks (Lean core only, no Mathlib)

This file holds only computable definitions; their soundness is proved in `YantraCert.Sound` and `YantraCert.Cover`.

* A polynomial in three variables with natural coefficients is a list of terms `c * x^a * y^b * z^e` (`NP`).  A signed polynomial
  `SP` is a pair `P⁺ - P⁻` with degree bounds `(Dx, Dy, Dz)`.
* Coordinates are rescaled to the unit cube.  A cell is the dyadic box `∏ [i_j / 2^d_j, (i_j + 1) / 2^d_j]`.
* Two enclosures, both sound because every coordinate is `≥ 0`:
  - the monotone split `P⁺(lo) - P⁻(hi) ≤ p ≤ P⁺(hi) - P⁻(lo)`, the natural interval extension of R. E. Moore
    (*Interval Analysis*, 1966) for this form;
  - the slope form of R. Krawczyk and A. Neumaier (*SIAM J. Numer. Anal.* 22, 1985),
    `p(y) = p(m) + Σ_j (y_j - m_j) A_j(y)`, with `x^a - m^a = (x - m) Σ_k x^k m^(a-1-k)`; on the grid of level `d + 1` the
    cell is `[L, H]` with centre `M = L + 1 = H - 1`, so the slope sums at the corners are `H^a - M^a` and `M^a - L^a`.
* Every quantity is scaled to a natural number, so the kernel computes with GMP (`decide +kernel` only).
  The functions use the recursors directly, so the kernel unfolds no `brecOn`.
* A certificate for one chart is a bisection tree in preorder (`TC`); the split rule is the one of the generator
  (`scripts/b2_bnb.py`): the coordinate of least depth, lowest index first.
-/

namespace YantraCert

/-- polynomial with natural coefficients: `nil`, or `c * x^a * y^b * z^e + rest` -/
inductive NP where
  | nil : NP
  | cons (c a b e : Nat) (t : NP) : NP

/-- `Σ c * fx a * fy b * fz e` -/
noncomputable def NP.ev (fx fy fz : Nat → Nat) (p : NP) : Nat :=
  NP.rec (motive := fun _ => Nat) 0 (fun c a b e _ ih => c * (fx a * fy b * fz e) + ih) p

/-- every exponent is within the degree bounds -/
noncomputable def NP.degLE (Dx Dy Dz : Nat) (p : NP) : Bool :=
  NP.rec (motive := fun _ => Bool) true (fun _ a b e _ ih => Nat.ble a Dx && Nat.ble b Dy && Nat.ble e Dz && ih) p

/-- scaled power at grid point `n` of level `d`, homogenised to degree `D`: `n^a * 2^((D-a) d)` -/
def sp (D d n a : Nat) : Nat := n ^ a <<< ((D - a) * d)

/-- the seven sums of the slope form -/
structure S7 where
  v : Nat
  ah : Nat
  al : Nat
  bh : Nat
  bl : Nat
  ch : Nat
  cl : Nat

/-- one term's contribution to the slope sums, from its scaled corner powers -/
def S7.add (s : S7) (c lx mx hx ly my hy lz mz hz : Nat) : S7 :=
  ⟨s.v + c * (mx * my * mz), s.ah + c * ((hx - mx) * hy * hz), s.al + c * ((mx - lx) * ly * lz),
   s.bh + c * (mx * (hy - my) * hz), s.bl + c * (mx * (my - ly) * lz),
   s.ch + c * (mx * my * (hz - mz)), s.cl + c * (mx * my * (mz - lz))⟩

/-- slope sums on the grid of levels `E`, with lower corner `L` (centre `L + 1`, upper corner `L + 2`) -/
noncomputable def slopeAcc (Dx Dy Dz Ex Ey Ez Lx Ly Lz : Nat) (p : NP) : S7 :=
  NP.rec (motive := fun _ => S7) ⟨0, 0, 0, 0, 0, 0, 0⟩ (fun c a b g _ ih =>
    ih.add c (sp Dx Ex Lx a) (sp Dx Ex (Lx + 1) a) (sp Dx Ex (Lx + 2) a)
      (sp Dy Ey Ly b) (sp Dy Ey (Ly + 1) b) (sp Dy Ey (Ly + 2) b)
      (sp Dz Ez Lz g) (sp Dz Ez (Lz + 1) g) (sp Dz Ez (Lz + 2) g)) p

/-- `|a - b|` -/
def adist (a b : Nat) : Nat := (a - b) + (b - a)

/-- radius of the slope form -/
def S7.rad (P N : S7) : Nat :=
  max (adist P.ah N.al) (adist P.al N.ah) + max (adist P.bh N.bl) (adist P.bl N.bh) + max (adist P.ch N.cl) (adist P.cl N.ch)

/-- signed polynomial `pp - pn` with degree bounds -/
structure SP where
  Dx : Nat
  Dy : Nat
  Dz : Nat
  pp : NP
  pn : NP

/-- a cell: levels and indices -/
structure Cell where
  dx : Nat
  ix : Nat
  dy : Nat
  iy : Nat
  dz : Nat
  iz : Nat

/-- sign code by the monotone split: 1 positive, 2 negative, 0 unknown -/
noncomputable def SP.signMono (p : SP) (c : Cell) : Nat :=
  cond (Nat.blt (p.pn.ev (sp p.Dx c.dx (c.ix + 1)) (sp p.Dy c.dy (c.iy + 1)) (sp p.Dz c.dz (c.iz + 1)))
                (p.pp.ev (sp p.Dx c.dx c.ix) (sp p.Dy c.dy c.iy) (sp p.Dz c.dz c.iz))) 1
   (cond (Nat.blt (p.pp.ev (sp p.Dx c.dx (c.ix + 1)) (sp p.Dy c.dy (c.iy + 1)) (sp p.Dz c.dz (c.iz + 1)))
                (p.pn.ev (sp p.Dx c.dx c.ix) (sp p.Dy c.dy c.iy) (sp p.Dz c.dz c.iz))) 2 0)

/-- the slope sums of both halves -/
noncomputable def SP.accP (p : SP) (c : Cell) : S7 :=
  slopeAcc p.Dx p.Dy p.Dz (c.dx + 1) (c.dy + 1) (c.dz + 1) (2 * c.ix) (2 * c.iy) (2 * c.iz) p.pp
noncomputable def SP.accN (p : SP) (c : Cell) : S7 :=
  slopeAcc p.Dx p.Dy p.Dz (c.dx + 1) (c.dy + 1) (c.dz + 1) (2 * c.ix) (2 * c.iy) (2 * c.iz) p.pn

/-- sign code from the slope sums -/
def signOf (P N : S7) : Nat :=
  cond (Nat.blt (N.v + S7.rad P N) P.v) 1 (cond (Nat.blt (P.v + S7.rad P N) N.v) 2 0)

/-- sign code by the slope form -/
noncomputable def SP.signSlope (p : SP) (c : Cell) : Nat := signOf (p.accP c) (p.accN c)

/-- sign code by method `m` (0 monotone split, otherwise slope form) -/
noncomputable def SP.sign (p : SP) (m : Nat) (c : Cell) : Nat :=
  cond (Nat.beq m 0) (p.signMono c) (p.signSlope c)

/-- a rational box in unit-cube coordinates: `xl/xlq ≤ x ≤ xh/xhq` etc. -/
structure HB where
  xl : Nat
  xlq : Nat
  xh : Nat
  xhq : Nat
  yl : Nat
  ylq : Nat
  yh : Nat
  yhq : Nat
  zl : Nat
  zlq : Nat
  zh : Nat
  zhq : Nat

/-- one coordinate of the cell `[i, i+1] / 2^d` lies in `[l/lq, h/hq]` -/
def inIv (d i l lq h hq : Nat) : Bool := Nat.ble (l * 2 ^ d) (i * lq) && Nat.ble ((i + 1) * hq) (h * 2 ^ d)

def HB.contains (h : HB) (c : Cell) : Bool :=
  inIv c.dx c.ix h.xl h.xlq h.xh h.xhq && inIv c.dy c.iy h.yl h.ylq h.yh h.yhq && inIv c.dz c.iz h.zl h.zlq h.zh h.zhq

/-- the data of one chart: equations, tests `(N, D)`, holes -/
structure Chart where
  F : List SP
  T : List (SP × SP)
  H : List HB

def dSP : SP := ⟨0, 0, 0, .nil, .nil⟩
def dHB : HB := ⟨1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1⟩

/-- `k`-th element (recursor form) -/
noncomputable def nth {α : Type} (d : α) (l : List α) (k : Nat) : α :=
  List.rec (motive := fun _ => Nat → α) (fun _ => d)
    (fun a _ ih k => Nat.rec (motive := fun _ => α) a (fun j _ => ih j) k) l k

/-- leaf tests -/
noncomputable def Chart.leafF (C : Chart) (k m : Nat) (c : Cell) : Bool :=
  Nat.blt 0 ((nth dSP C.F k).sign m c)

noncomputable def Chart.leafT (C : Chart) (k mN mD : Nat) (c : Cell) : Bool :=
  let q := nth (dSP, dSP) C.T k
  let sN := q.1.sign mN c
  let sD := q.2.sign mD c
  (Nat.beq sN 1 && Nat.beq sD 2) || (Nat.beq sN 2 && Nat.beq sD 1)

noncomputable def Chart.leafH (C : Chart) (k : Nat) (c : Cell) : Bool := (nth dHB C.H k).contains c

/-- bisection: the coordinate of least depth, lowest index first; `b` = 0 lower half, 1 upper half -/
def Cell.split (c : Cell) (b : Nat) : Cell :=
  cond (Nat.ble c.dx c.dy && Nat.ble c.dx c.dz) ⟨c.dx + 1, 2 * c.ix + b, c.dy, c.iy, c.dz, c.iz⟩
    (cond (Nat.ble c.dy c.dz) ⟨c.dx, c.ix, c.dy + 1, 2 * c.iy + b, c.dz, c.iz⟩ ⟨c.dx, c.ix, c.dy, c.iy, c.dz + 1, 2 * c.iz + b⟩)

/-- bisection tree in preorder -/
inductive TC where
  | done : TC
  | node (t : TC) : TC
  | leafF (k m : Nat) (t : TC) : TC
  | leafT (k mN mD : Nat) (t : TC) : TC
  | leafH (k : Nat) (t : TC) : TC

/-- walk the tree from cell `c`; returns the codes after the subtree, or `none` if a leaf fails -/
noncomputable def go (C : Chart) (fuel : Nat) : Cell → TC → Option TC :=
  Nat.rec (motive := fun _ => Cell → TC → Option TC) (fun _ _ => none)
    (fun _ ih c t => TC.casesOn (motive := fun _ => Option TC) t none
      (fun t => Option.casesOn (motive := fun _ => Option TC) (ih (c.split 0) t) none (fun t' => ih (c.split 1) t'))
      (fun k m t => cond (C.leafF k m c) (some t) none)
      (fun k mN mD t => cond (C.leafT k mN mD c) (some t) none)
      (fun k t => cond (C.leafH k c) (some t) none)) fuel

/-- the Bool fact proved by `decide +kernel` in each certificate file -/
noncomputable def checkTree (C : Chart) (fuel : Nat) (c : Cell) (t : TC) : Bool :=
  Option.casesOn (motive := fun _ => Bool) (go C fuel c t) false (fun _ => true)

/-- degree bounds of every polynomial of a chart -/
noncomputable def SP.degOK (p : SP) : Bool := p.pp.degLE p.Dx p.Dy p.Dz && p.pn.degLE p.Dx p.Dy p.Dz

noncomputable def Chart.degOK (C : Chart) : Bool :=
  C.F.all SP.degOK && C.T.all (fun q => q.1.degOK && q.2.degOK)

/-- decode the preorder codes: `8 j + kind`, kind 0 node, 1 equation leaf (`j = 2 k + m`), 2 test leaf (`j = 4 k + 2 mN + mD`),
3 hole leaf (`j = k`) -/
noncomputable def TC.ofList (l : List Nat) : TC :=
  List.foldr (fun n t =>
    cond (Nat.beq (n % 8) 0) (TC.node t)
      (cond (Nat.beq (n % 8) 1) (TC.leafF (n / 8 / 2) (n / 8 % 2) t)
        (cond (Nat.beq (n % 8) 2) (TC.leafT (n / 8 / 4) (n / 8 / 2 % 2) (n / 8 % 2) t) (TC.leafH (n / 8) t)))) TC.done l

/-- concatenation (long polynomials are written in chunks) -/
noncomputable def NP.app (p q : NP) : NP := NP.rec (motive := fun _ => NP) q (fun c a b e _ ih => NP.cons c a b e ih) p

end YantraCert
