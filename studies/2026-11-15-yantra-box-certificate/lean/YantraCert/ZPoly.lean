import YantraCert.Check

/-!
# Sparse polynomials in three variables with integer coefficients, evaluated by the kernel (Lean core only)

A reflective normaliser for polynomial identities (step 2 of the Lean plan). A polynomial is a list of terms
`c * x^a * y^b * z^e`. `add` merges two lists that are sorted in the lexicographic order of `(a, b, e)`, combining equal monomials
and dropping zero coefficients, so sums and products of sorted lists are sorted and have no repeated monomial. An identity
`p = q` is checked by computing `p - q` and testing that it is the empty list (`ZP.isNil`). Soundness (`YantraCert.ZPolySound`)
needs no sortedness: every operation is proved to commute with evaluation, whatever the order of the terms.
All functions use the recursors directly, so the kernel unfolds no `brecOn`.
-/

namespace YantraCert

inductive ZP where
  | nil : ZP
  | cons (c : Int) (a b e : Nat) (t : ZP) : ZP

/-- concatenation (long polynomials are written in chunks) -/
noncomputable def ZP.app (p q : ZP) : ZP := ZP.rec (motive := fun _ => ZP) q (fun c a b e _ ih => .cons c a b e ih) p

/-- lexicographic order on exponent triples -/
def mlt (a b e a' b' e' : Nat) : Bool :=
  Nat.blt a a' || (Nat.beq a a' && (Nat.blt b b' || (Nat.beq b b' && Nat.blt e e')))
def meq (a b e a' b' e' : Nat) : Bool := Nat.beq a a' && Nat.beq b b' && Nat.beq e e'

/-- merge the term `c x^a y^b z^e`, followed by `f` (the merge of the rest of the first list), into `q` -/
noncomputable def ZP.ins (c : Int) (a b e : Nat) (f : ZP → ZP) (q : ZP) : ZP :=
  ZP.rec (motive := fun _ => ZP) (cond (c == 0) (f .nil) (.cons c a b e (f .nil)))
    (fun c' a' b' e' q' ih =>
      cond (mlt a' b' e' a b e) (.cons c' a' b' e' ih)
        (cond (meq a b e a' b' e')
          (cond (c + c' == 0) (f q') (.cons (c + c') a b e (f q')))
          (cond (c == 0) (f (.cons c' a' b' e' q')) (.cons c a b e (f (.cons c' a' b' e' q')))))) q

noncomputable def ZP.add (p q : ZP) : ZP :=
  ZP.rec (motive := fun _ => ZP → ZP) (fun q => q) (fun c a b e _ ih q => ZP.ins c a b e ih q) p q

noncomputable def ZP.neg (p : ZP) : ZP := ZP.rec (motive := fun _ => ZP) .nil (fun c a b e _ ih => .cons (-c) a b e ih) p

noncomputable def ZP.sub (p q : ZP) : ZP := ZP.add p (ZP.neg q)

/-- multiply by one term -/
noncomputable def ZP.scale (c : Int) (a b e : Nat) (q : ZP) : ZP :=
  ZP.rec (motive := fun _ => ZP) .nil (fun c' a' b' e' _ ih => .cons (c * c') (a + a') (b + b') (e + e') ih) q

noncomputable def ZP.mul (p q : ZP) : ZP :=
  ZP.rec (motive := fun _ => ZP) .nil (fun c a b e _ ih => ZP.add (ZP.scale c a b e q) ih) p

def ZP.one : ZP := .cons 1 0 0 0 .nil
def ZP.const (c : Int) : ZP := .cons c 0 0 0 .nil

noncomputable def ZP.pow (p : ZP) (n : Nat) : ZP := Nat.rec (motive := fun _ => ZP) ZP.one (fun _ ih => ZP.mul ih p) n

/-- `p(X, Y, Z)` for polynomials `X, Y, Z` -/
noncomputable def ZP.subst (X Y Z : ZP) (p : ZP) : ZP :=
  ZP.rec (motive := fun _ => ZP) .nil
    (fun c a b e _ ih => ZP.add (ZP.mul (ZP.const c) (ZP.mul (ZP.mul (ZP.pow X a) (ZP.pow Y b)) (ZP.pow Z e))) ih) p

/-- homogenised substitution with a rational third argument: `Σ c X^a Y^b Zn^e Zd^(d-e)` (that is `p(X, Y, Zn/Zd) Zd^d`) -/
noncomputable def ZP.substH (X Y Zn Zd : ZP) (d : Nat) (p : ZP) : ZP :=
  ZP.rec (motive := fun _ => ZP) .nil
    (fun c a b e _ ih => ZP.add (ZP.mul (ZP.const c)
      (ZP.mul (ZP.mul (ZP.mul (ZP.pow X a) (ZP.pow Y b)) (ZP.pow Zn e)) (ZP.pow Zd (d - e)))) ih) p

/-- the largest exponent of the third variable is at most `d` -/
noncomputable def ZP.zdeg (d : Nat) (p : ZP) : Bool :=
  ZP.rec (motive := fun _ => Bool) true (fun _ _ _ e _ ih => Nat.ble e d && ih) p

noncomputable def ZP.isNil (p : ZP) : Bool := ZP.rec (motive := fun _ => Bool) true (fun _ _ _ _ _ _ => false) p

/-- the identity check `p = q` -/
noncomputable def ZP.eqv (p q : ZP) : Bool := (ZP.sub p q).isNil

/-- every coefficient is positive (and the list is nonempty with a positive constant term first: see `posConst`) -/
noncomputable def ZP.allPos (p : ZP) : Bool := ZP.rec (motive := fun _ => Bool) true (fun c _ _ _ _ ih => decide (0 < c) && ih) p

/-- product of a list of polynomials -/
noncomputable def ZP.prod (l : List ZP) : ZP := List.rec (motive := fun _ => ZP) ZP.one (fun p _ ih => ZP.mul p ih) l

/-! ## Expressions in named quantities, and their fractions -/

/-- an expression in named real quantities `V i` and integer constants -/
inductive Ex where
  | v (i : Nat) : Ex
  | c (z : Int) : Ex
  | add (a b : Ex) : Ex
  | sub (a b : Ex) : Ex
  | mul (a b : Ex) : Ex

/-- numerator and denominator of an expression, from the table `T` of the quantities' numerators and denominators
(no cancellation, except that equal denominators are kept once) -/
noncomputable def Ex.frac (T : List (ZP × ZP)) (e : Ex) : ZP × ZP :=
  Ex.rec (motive := fun _ => ZP × ZP) (fun i => nth (ZP.nil, ZP.one) T i) (fun z => (ZP.const z, ZP.one))
    (fun _ _ fa fb => cond (ZP.eqv fa.2 fb.2) (ZP.add fa.1 fb.1, fa.2)
      (ZP.add (ZP.mul fa.1 fb.2) (ZP.mul fb.1 fa.2), ZP.mul fa.2 fb.2))
    (fun _ _ fa fb => cond (ZP.eqv fa.2 fb.2) (ZP.sub fa.1 fb.1, fa.2)
      (ZP.sub (ZP.mul fa.1 fb.2) (ZP.mul fb.1 fa.2), ZP.mul fa.2 fb.2))
    (fun _ _ fa fb => (ZP.mul fa.1 fb.1, ZP.mul fa.2 fb.2)) e

/-- the largest index used is below `n` -/
noncomputable def Ex.within (n : Nat) (e : Ex) : Bool :=
  Ex.rec (motive := fun _ => Bool) (fun i => Nat.blt i n) (fun _ => true) (fun _ _ a b => a && b) (fun _ _ a b => a && b)
    (fun _ _ a b => a && b) e

/-- the positive and the negative part of a polynomial, as polynomials with natural coefficients -/
noncomputable def ZP.posNP (p : ZP) : NP :=
  ZP.rec (motive := fun _ => NP) .nil (fun c a b e _ ih => cond (decide (0 < c)) (.cons c.toNat a b e ih) ih) p
noncomputable def ZP.negNP (p : ZP) : NP :=
  ZP.rec (motive := fun _ => NP) .nil (fun c a b e _ ih => cond (decide (c < 0)) (.cons (-c).toNat a b e ih) ih) p

/-- a polynomial as a signed polynomial with degree bounds -/
noncomputable def ZP.toSP (Dx Dy Dz : Nat) (p : ZP) : SP := ⟨Dx, Dy, Dz, p.posNP, p.negNP⟩

/-- the kernel facts of one step -/
noncomputable def stepOK (T : List (ZP × ZP)) (i : Nat) (d n : Ex) (K : ZP) : Bool :=
  d.within i && n.within i &&
  ZP.eqv (ZP.mul (nth (ZP.nil, ZP.one) T i).2 K) (ZP.mul (Ex.frac T d).1 (Ex.frac T n).2) &&
  ZP.eqv (ZP.mul (nth (ZP.nil, ZP.one) T i).1 K) (ZP.mul (Ex.frac T n).1 (Ex.frac T d).2)

end YantraCert
