module

public import GET.ZPhi

@[expose] public section

/-!
# The six-axis model and the exact checks

A point of the model is `p : Fin 6 → ℤ`, standing for `Σ pᵢ eᵢ` with `eᵢ` the six 5-fold axes of the icosahedron.
A cell `(p; i j k)` is the golden rhombohedron `p + [0,1]eᵢ + [0,1]eⱼ + [0,1]eₖ`; a face `(p; a b; s)` is the golden
rhombus `p + [0,1]eₐ + [0,1]e_b`, with outward normal `s (eₐ × e_b)`. Each check below is a `Bool` computed on
`ZPhi` and integer data, so it can be decided by the kernel.
-/

namespace GET

open ZPhi

/-- a golden rhombohedron `p + [0,1]eᵢ + [0,1]eⱼ + [0,1]eₖ` -/
structure Cell where
  p : Fin 6 → ℤ
  i : Fin 6
  j : Fin 6
  k : Fin 6

/-- a golden rhombus `p + [0,1]eₐ + [0,1]e_b` with outward normal `s (eₐ × e_b)` -/
structure Face where
  p : Fin 6 → ℤ
  a : Fin 6
  b : Fin 6
  s : ℤ

/-- the six 5-fold axes `(1,φ,0), (-1,φ,0), (0,1,φ), (0,-1,φ), (φ,0,1), (-φ,0,1)` -/
def axis : Fin 6 → Fin 3 → ZPhi :=
  ![![1, phi, 0], ![-1, phi, 0], ![0, 1, phi], ![0, -1, phi], ![phi, 0, 1], ![-phi, 0, 1]]

/-- the 3 × 3 determinant by the explicit formula -/
def det3 (u v w : Fin 3 → ZPhi) : ZPhi :=
  u 0 * (v 1 * w 2 - v 2 * w 1) - u 1 * (v 0 * w 2 - v 2 * w 0) + u 2 * (v 0 * w 1 - v 1 * w 0)

/-- `det(eᵢ, eⱼ, eₖ)` -/
def D (i j k : Fin 6) : ZPhi := det3 (axis i) (axis j) (axis k)

/-- dot product -/
def dot (u v : Fin 3 → ZPhi) : ZPhi := u 0 * v 0 + u 1 * v 1 + u 2 * v 2

/-- sum of a list -/
def lsum (l : List ZPhi) : ZPhi := l.foldr (· + ·) 0

/-- the position `Σ pᵢ eᵢ` -/
def posn (p : Fin 6 → ℤ) : Fin 3 → ZPhi := fun c => lsum ((List.finRange 6).map fun i => ofInt (p i) * axis i c)

/-- the absolute value (for non-zero arguments the sign is decided by `pos`) -/
def zabs (x : ZPhi) : ZPhi := if pos x then x else -x

/-- the unit vector `e_c` of `ℤ⁶` -/
def unit (c : Fin 6) : Fin 6 → ℤ := fun i => if i = c then 1 else 0

/-- vectors as lists (for fast decidable equality) -/
def vl (p : Fin 6 → ℤ) : List ℤ := List.ofFn p

/-- the four corners of a face -/
def Face.corners (f : Face) : List (List ℤ) :=
  [vl f.p, vl (f.p + unit f.a), vl (f.p + unit f.b), vl (f.p + unit f.a + unit f.b)]

/-- the four sides of a face, each as (start, direction) -/
def Face.sides (f : Face) : List (List ℤ × Fin 6) :=
  [(vl f.p, f.a), (vl f.p, f.b), (vl (f.p + unit f.b), f.a), (vl (f.p + unit f.a), f.b)]

/-! ## The checks -/

/-- the zone of axis `c`: the number of faces with a side parallel to `e_c` -/
def zoneSize (F : List Face) (c : Fin 6) : ℕ := (F.filter fun f => f.a == c || f.b == c).length

/-- every side lies on exactly two faces -/
def edgeManifold (F : List Face) : Bool :=
  F.all fun f => f.sides.all fun e => (F.filter fun g => g.sides.contains e).length == 2

/-- two faces that share a side span different planes: their axis pairs differ (with `threeIndependent`) -/
def adjacentNotCoplanar (F : List Face) : Bool :=
  F.all fun f => F.all fun g =>
    !(f.sides.any fun e => g.sides.contains e) || (decide (f.a = g.a ∧ f.b = g.b ∧ vl f.p = vl g.p)) ||
      !(f.a == g.a && f.b == g.b)

/-- any three distinct axes are linearly independent -/
def threeIndependent : Bool :=
  (List.finRange 6).all fun i => (List.finRange 6).all fun j => (List.finRange 6).all fun k =>
    !(decide (i < j ∧ j < k)) || decide (D i j k ≠ 0)

/-- every two axes meet at the same angle: `|eᵢ|² = 2 + φ` and `|eᵢ · eⱼ| = φ` -/
def oneRhombus : Bool :=
  (List.finRange 6).all fun i => (List.finRange 6).all fun j =>
    if i = j then decide (dot (axis i) (axis j) = ⟨2, 1⟩) else decide (zabs (dot (axis i) (axis j)) = phi)

/-- number of distinct vertices and of distinct sides -/
def nVertices (F : List Face) : ℕ := (F.flatMap Face.corners).dedup.length
def nSides (F : List Face) : ℕ := (F.flatMap Face.sides).dedup.length

/-- the six faces of a cell, with outward signs -/
def Cell.faces (c : Cell) : List Face :=
  let fs : List (Fin 6 × Fin 6 × Fin 6) := [(c.i, c.j, c.k), (c.i, c.k, c.j), (c.j, c.k, c.i)]
  fs.flatMap fun (a, b, o) =>
    let so : ℤ := if pos (D a b o) then 1 else -1
    [⟨c.p, a, b, -so⟩, ⟨c.p + unit o, a, b, so⟩]

/-- a face as a comparable key -/
def Face.key (f : Face) : List ℤ × Fin 6 × Fin 6 × ℤ := (vl f.p, f.a, f.b, f.s)
def Face.keyU (f : Face) : List ℤ × Fin 6 × Fin 6 := (vl f.p, f.a, f.b)

/-- the faces of `F` are exactly the cell faces that lie on one cell only, with the same outward sign -/
def facesAreBoundary (C : List Cell) (F : List Face) : Bool :=
  let all := C.flatMap Cell.faces
  let bd := all.filter fun f => (all.filter fun g => g.keyU == f.keyU).length == 1
  (F.map Face.key).Nodup && bd.length == F.length && bd.all fun f => (F.map Face.key).contains f.key

/-- the lattice vector `Σ xᵣ Bᵣ` -/
def latVec (B : List (Fin 6 → ℤ)) (x : Fin 3 → ℤ) : Fin 6 → ℤ :=
  fun c => ((List.finRange 3).zip B).foldr (fun (r, v) acc => x r * v c + acc) 0

/-- face matching: face `i` and face `j` are opposite and differ by a lattice vector -/
def faceMatch (F : List Face) (B : List (Fin 6 → ℤ)) (M : List (ℕ × (Fin 3 → ℤ))) : Bool :=
  M.length == F.length && (F.zip M).all fun (f, (j, x)) =>
    match F[j]? with
    | none => false
    | some g => g.a == f.a && g.b == f.b && g.s == -f.s && vl f.p == vl (g.p + latVec B x)

/-- `|det|` of a cell, `|det|` of the lattice, and volume = covolume -/
def cellVol (c : Cell) : ZPhi := zabs (D c.i c.j c.k)
def covol (B : List (Fin 6 → ℤ)) : ZPhi :=
  match B with
  | [b0, b1, b2] => zabs (det3 (posn b0) (posn b1) (posn b2))
  | _ => 0
def volEqCovol (C : List Cell) (B : List (Fin 6 → ℤ)) : Bool := lsum (C.map cellVol) == covol B

/-! ## Separation of two cells (projection on the 15 normals `eₓ × e_y`) -/

/-- `n_xy · posn p` with `n_xy = eₓ × e_y` -/
def proj (x y : Fin 6) (p : Fin 6 → ℤ) : ZPhi := lsum ((List.finRange 6).map fun i => ofInt (p i) * D x y i)

/-- the projection interval of a cell on `n_xy` -/
def interval (x y : Fin 6) (c : Cell) : ZPhi × ZPhi :=
  [c.i, c.j, c.k].foldl (fun (lo, hi) d =>
    let v := D x y d
    if pos v then (lo, hi + v) else (lo + v, hi)) (proj x y c.p, proj x y c.p)

/-- the 15 pairs `x < y` -/
def pairs15 : List (Fin 6 × Fin 6) :=
  (List.finRange 6).flatMap fun x => (List.finRange 6).filterMap fun y => if x < y then some (x, y) else none

/-- two cells have disjoint interiors: some normal separates them (weakly) -/
def separated (c d : Cell) : Bool :=
  pairs15.any fun (x, y) =>
    let (a0, a1) := interval x y c
    let (b0, b1) := interval x y d
    nonneg (b0 - a1) || nonneg (a0 - b1)

/-- the translate of a cell -/
def Cell.shift (c : Cell) (t : Fin 6 → ℤ) : Cell := ⟨c.p + t, c.i, c.j, c.k⟩

/-- the cells of `P` have pairwise disjoint interiors -/
def cellsSeparated (C : List Cell) : Bool :=
  C.zipIdx.all fun (c, i) => C.zipIdx.all fun (d, j) => !(decide (i < j)) || separated c d

/-- the coefficient box `{-1,0,1}³ \ {0}` -/
def box1 : List (Fin 3 → ℤ) :=
  ([-1, 0, 1] : List ℤ).flatMap fun a => ([-1, 0, 1] : List ℤ).flatMap fun b =>
    ([-1, 0, 1] : List ℤ).filterMap fun c => if a = 0 ∧ b = 0 ∧ c = 0 then none else some ![a, b, c]

/-- every cell of `P` is separated from every cell of `t + P`, for the lattice vectors `t` of the box -/
def translatesSeparated (C : List Cell) (B : List (Fin 6 → ℤ)) (X : List (Fin 3 → ℤ)) : Bool :=
  X.all fun x => C.all fun c => C.all fun d => separated c (d.shift (latVec B x))

/-- strict star shape from the centre `(1/2, …, 1/2)`: the plane of every face misses the centre, which lies on its
inner side (`2 n · (posn p - centre) > 0`) -/
def starFromCentre (F : List Face) : Bool :=
  F.all fun f => pos (ofInt f.s * lsum ((List.finRange 6).map fun i => ofInt (2 * f.p i - 1) * D f.a f.b i))

end GET
