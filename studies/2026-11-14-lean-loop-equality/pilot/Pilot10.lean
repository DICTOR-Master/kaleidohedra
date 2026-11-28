/-! M0 kernel pilot (28 Nov 2026): the half network of halves.py as a Nat computation; arcs from the origin boundary
atom and raw meeting triples, compared with Python (30/168/1038 arcs; 384/5760/61704 triples at fmax 6/8/10).
Atoms are Nat codes ((j * 128 + x) * 128 + y) * 2 + t with x, y offset by 64. -/

def enc (j x y t : Nat) : Nat := ((j * 128 + x) * 128 + y) * 2 + t
def lvl (a : Nat) : Nat := a / 2 / 128 / 128
def ax (a : Nat) : Nat := a / 2 / 128 % 128
def ay (a : Nat) : Nat := a / 2 % 128
def at' (a : Nat) : Nat := a % 2

/-- the three slanted steps: D1 = (1,1), (-2,1), (1,-2); D2 = their negatives (offset +2) -/
def steps (d1 : Bool) : List (Nat × Nat) :=
  if d1 then [(3, 3), (0, 3), (3, 0)] else [(1, 1), (4, 1), (1, 4)]

def letter (c : List Nat) (j : Nat) : Nat := c.getD j 0

def nbrs (c : List Nat) (a : Nat) : List Nat :=
  let j := lvl a; let x := ax a; let y := ay a
  if at' a == 1 then
    (if j ≥ 1 then [enc j x y 0] else []) ++
      (steps ((letter c (j + 1) + 3 - letter c j) % 3 == 1)).map (fun d => enc (j + 1) (x + d.1 - 2) (y + d.2 - 2) 0)
  else
    [enc j x y 1] ++
      (steps ((letter c (j - 1) + 3 - letter c j) % 3 == 1)).map (fun d => enc (j - 1) (x + d.1 - 2) (y + d.2 - 2) 1)

def origin (c : List Nat) : Nat := enc 0 (64 + letter c 0) (64 + letter c 0) 1

/-- all arcs (as reversed atom lists, head = last atom) from the origin with at most `n` more bonds -/
def dfs (c : List Nat) (o : Nat) : Nat → List Nat → List (List Nat)
  | 0, path => match path with
    | a :: _ :: _ => if lvl a == 0 && at' a == 1 then [path] else []
    | _ => []
  | n + 1, path => match path with
    | [] => []
    | a :: rest =>
      let here := match rest with
        | _ :: _ => if lvl a == 0 && at' a == 1 then [path] else []
        | [] => []
      here ++ (nbrs c a).foldr (fun b acc =>
        if path.contains b || (a == o && lvl b == 0) then acc else dfs c o n (b :: path) ++ acc) []

def arcs (c : List Nat) (amax : Nat) : List (List Nat) := dfs c (origin c) amax [origin c]

def insertNew (l : List Nat) (v : Nat) : List Nat := if l.contains v then l else v :: l

/-- translation code: (dx + 64) * 256 + (dy + 64) -/
def shiftsMeeting (A B : List Nat) : List Nat :=
  A.foldl (fun acc a => B.foldl (fun acc b =>
    if lvl a == lvl b && at' a == at' b then insertNew acc ((ax a + 64 - ax b) * 256 + (ay a + 64 - ay b)) else acc) acc) []

def shiftAtom (s : Nat) (b : Nat) : Nat := enc (lvl b) (ax b + s / 256 - 64) (ay b + s % 256 - 64) (at' b)

def endPt (a : Nat) : Nat := ax a * 128 + ay a

def distinct4 (p q r s : Nat) : Bool := p != q && p != r && p != s && q != r && q != s && r != s

def rawTriples (c : List Nat) (fmax : Nat) : Nat :=
  let as := arcs c (fmax - 2)
  as.foldl (fun acc A => as.foldl (fun acc B =>
    if A.length - 1 + (B.length - 1) > fmax then acc else
    (shiftsMeeting A B).foldl (fun acc s =>
      let Bt := B.map (shiftAtom s)
      let p1 := endPt (A.getLast!) ; let p2 := endPt (A.head!)
      let p3 := endPt (Bt.getLast!) ; let p4 := endPt (Bt.head!)
      if distinct4 p1 p2 p3 p4 && Bt.any (fun b => A.contains b) then acc + 1 else acc) acc) acc) 0

def cubic : List Nat := [0, 1, 2, 0, 1, 2, 0, 1, 2]


set_option maxHeartbeats 0 in
theorem raw10 : rawTriples cubic 10 = 61704 := by decide +kernel
