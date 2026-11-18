# text generator for Dehn5Fuji.lean (certificates computed exactly on the compute host by fuji2.py)
ind = {(0,1,6):"-4 + 4 * √5",(0,2,6):"4 - 4 * √5",(0,3,1):"24 - 8 * √5",(0,4,1):"-8 + 8 * √5",(0,5,1):"16",
 (0,6,2):"-4 + 4 * √5",(1,2,0):"-24 + 8 * √5",(1,3,6):"-4 + 4 * √5",(1,4,0):"8 - 8 * √5",(1,5,0):"-16",
 (1,6,3):"4 - 4 * √5",(2,3,0):"16",(2,4,0):"-8 + 8 * √5",(2,5,6):"4 - 4 * √5",(2,6,5):"-4 + 4 * √5",
 (3,4,6):"-4 + 4 * √5",(3,5,0):"-(16 * √5)",(3,6,4):"4 - 4 * √5",(4,5,6):"-4 + 4 * √5",(4,6,5):"4 - 4 * √5",
 (5,6,4):"-4 + 4 * √5"}
# (i,j): (e, k, l, c, c', swapped)
edge = {(0,1):(0,0,1,6,2,0),(0,2):(1,0,2,6,1,0),(0,6):(6,1,2,2,1,1),(1,3):(2,0,3,6,0,1),(1,6):(9,1,3,3,0,0),
 (2,5):(3,0,4,6,0,1),(2,6):(10,2,4,5,0,0),(3,4):(4,0,5,6,0,0),(3,6):(7,3,5,4,1,1),(4,5):(5,0,6,6,0,1),
 (4,6):(11,5,6,5,3,0),(5,6):(8,4,6,4,2,1)}
# (i,j): (c, c', mu, a, a')
non = {(0,3):(1,2,"(3 - √5) / 2","(√5 - 1) / 2","(3 - √5) / 2"),(0,4):(1,2,"1","1","(√5 - 1) / 2"),
 (0,5):(1,2,"(3 + √5) / 2","(1 + √5) / 2","1"),(1,2):(0,3,"(√5 - 1) / 2","(1 + √5) / 2","(√5 - 1) / 2"),
 (1,4):(0,3,"(1 + √5) / 2","(3 + √5) / 2","1"),(1,5):(0,3,"1","√5","(3 - √5) / 2"),
 (2,3):(0,4,"(1 + √5) / 2","(1 + √5) / 2","1"),(2,4):(0,5,"(1 + √5) / 2","(3 + √5) / 2","1"),
 (3,5):(0,4,"(5 + 3 * √5) / 2","(3 + √5) / 2","(3 + √5) / 2")}
o=[]
o.append("/-! ### Independent triples of normals (determinants computed exactly in ℚ(√5)) -/\n")
for (i,j,c),D in ind.items():
    o.append(f"""lemma fuji_ind_{i}_{j}_{c} (v : R3) (h1 : ⟪fujiN {i}, v⟫ = 0) (h2 : ⟪fujiN {j}, v⟫ = 0)
    (h3 : ⟪fujiN {c}, v⟫ = 0) : v = 0 :=
  ind3 (D := {D}) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3
""")
o.append("/-! ### The cover: every pair of faces -/\n")
names=[]
for i in range(7):
  for j in range(i+1,7):
    if (i,j) in edge:
        e,k,l,c,cp,sw=edge[(i,j)]
        eq = "Set.pair_comm _ _" if sw else "rfl"
        o.append(f"""lemma fuji_cover_{i}_{j} {{x : R3}} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN {i}, x⟫ = fujiB {i})
    (hj : ⟪fujiN {j}, x⟫ = fujiB {j}) : FujiCover x {i} {j} :=
  Or.inl ⟨{e}, {eq}, mem_segment_of_tight fuji_ind_{i}_{j}_{c}
    (fuji_tight {i} {k} (by decide)) (fuji_tight {i} {l} (by decide)) (fuji_tight {j} {k} (by decide))
    (fuji_tight {j} {l} (by decide)) (fuji_tight {c} {l} (by decide)) (fuji_lt {c} {k} (by decide))
    (fuji_tight {cp} {k} (by decide)) (fuji_lt {cp} {l} (by decide)) hx hi hj⟩
""")
    else:
        c,cp,mu,a,ap=non[(i,j)]
        o.append(f"""lemma fuji_cover_{i}_{j} {{x : R3}} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN {i}, x⟫ = fujiB {i})
    (hj : ⟪fujiN {j}, x⟫ = fujiB {j}) : FujiCover x {i} {j} :=
  Or.inr ⟨0, eq_of_tight fuji_ind_{i}_{j}_{c}
    (fuji_tight {c} 0 (by decide)) (fuji_tight {cp} 0 (by decide)) (fuji_tight {i} 0 (by decide))
    (fuji_tight {j} 0 (by decide)) (μ := {mu}) (a := {a}) (a' := {ap}) (by sqrt5_pos)
    (by have ht := sqrt5_sq; ext t; fin_cases t <;> simp [fujiN] <;> grind) hx hi hj⟩
""")
    names.append((i,j))
alts="\n    ".join(f"| exact fuji_cover_{i}_{j} hx hi hj" for (i,j) in names)
o.append(f"""lemma fuji_cover_lt {{x : R3}} (hx : x ∈ sol fujiN fujiB) : ∀ i j : Fin 7, i < j →
    ⟪fujiN i, x⟫ = fujiB i → ⟪fujiN j, x⟫ = fujiB j → FujiCover x i j := by
  intro i j hij hi hj
  fin_cases i <;> fin_cases j <;> first
    | exact absurd hij (by decide)
    {alts}
""")
open('gen_out.lean','w').write("\n".join(o))
