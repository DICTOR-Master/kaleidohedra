# Generator of the Lean text of the edge data (IsEdgeData, study 5) of the dodecahedron and the icosahedron,
# coordinates in Q(sqrt5), exact (q5.py). Run on the compute host:
#   python3 gen_edges5.py dod > dod_block.lean
#   python3 gen_edges5.py ico > ico_block.lean
# Every emitted fact is checked here exactly first; Lean checks it again.
import sys
exec(open('q5.py').read())
from fractions import Fraction as Fr

LO, HI = Fr(2236, 1000), Fr(2237, 1000)   # LO < sqrt5 < HI
def pos(v):   # certified v > 0 from LO < sqrt5 < HI
    a, b = v.a, v.b
    return (a + b * (LO if b >= 0 else HI)) > 0
def nonzero(v): return pos(v) or pos(-v)

which = sys.argv[1]
z = Q(0)
def cyc(v): return [[v[(r - c) % 3] for r in range(3)] for c in range(3)]
def signs(v):
    out = []
    for s in itertools.product([1, -1], repeat=3):
        w = [v[r] * s[r] for r in range(3)]
        if w not in out: out.append(w)
    return out
ico_corners = []
for v in cyc([z, Q(2), Q(1, 1)]):
    ico_corners += signs(v)
dod_corners = signs([Q(2), Q(2), Q(2)])
for v in cyc([z, Q(1, 1), Q(-1, 1)]):
    dod_corners += signs(v)
if which == "dod":
    X = "dod"; N = ico_corners; P = dod_corners
elif which == "ico":
    X = "ico"; N = dod_corners; P = ico_corners
else:
    raise SystemExit("dod or ico")
F, K = len(N), len(P)
B = []
for m in range(F):
    vals = [dot(N[m], P[k]) for k in range(K)]
    mx = vals[0]
    for v in vals:
        if (v - mx).sign() > 0: mx = v
    B.append(mx)
S = [[B[m] - dot(N[m], P[k]) for k in range(K)] for m in range(F)]
Z = [[S[m][k] == Q(0) for k in range(K)] for m in range(F)]
for m in range(F):
    for k in range(K):
        assert Z[m][k] or pos(S[m][k]), (m, k)
faces_at = [[m for m in range(F) if Z[m][k]] for k in range(K)]
assert all(len(f) >= 3 for f in faces_at)
edges = []; vonly = {}; disj = []
for i in range(F):
    for j in range(i + 1, F):
        common = [k for k in range(K) if Z[i][k] and Z[j][k]]
        if len(common) == 2: edges.append((i, j, common[0], common[1]))
        elif len(common) == 1: vonly[(i, j)] = common[0]
        elif len(common) == 0: disj.append((i, j))
        else: raise SystemExit("more than two corners on two faces")
for (i, j, k, l) in edges:
    for m in range(F):
        if m not in (i, j): assert not (Z[m][k] and Z[m][l])
print(f"-- {F} faces, {K} corners, {len(edges)} edges, {len(vonly)} one-corner pairs, {len(disj)} disjoint pairs",
      file=sys.stderr)
print("-- offsets", set(B), file=sys.stderr)
cert = {}
for e, (i, j, k, l) in enumerate(edges):
    cs = [c for c in range(F) if c not in (i, j) and Z[c][l] and not Z[c][k] and nonzero(det(N[i], N[j], N[c]))]
    cps = [c for c in range(F) if c not in (i, j) and Z[c][k] and not Z[c][l]]
    c, cp = cs[0], cps[0]
    cert[(i, j)] = (e, k, l, c, cp, det(N[i], N[j], N[c]))
# one-corner pairs: n_c + mu n_c' = a n_i + a' n_j, mu > 0, det(n_i, n_j, n_c) != 0, c, c' through the corner
vcert = {}
for (i, j), k in vonly.items():
    found = None
    for c in faces_at[k]:
        if c in (i, j) or not nonzero(det(N[i], N[j], N[c])): continue
        for cp in faces_at[k]:
            if cp in (i, j, c): continue
            M = [[N[i][r], N[j][r], N[cp][r]] for r in range(3)]
            sol = solve3(M, N[c])
            if sol is None: continue
            assert all(sum((M[r][s] * sol[s] for s in range(3)), Q(0)) == N[c][r] for r in range(3))
            mu = -sol[2]
            if pos(mu):
                found = (c, cp, mu, sol[0], sol[1]); break
        if found: break
    assert found, (i, j)
    c, cp, mu, a, a2 = found
    for r in range(3): assert N[c][r] + mu * N[cp][r] == a * N[i][r] + a2 * N[j][r]
    vcert[(i, j)] = (k, c, cp, mu, a, a2, det(N[i], N[j], N[c]))
# disjoint pairs: a n_i + a' n_j = sum mu_c n_c (mu_c >= 0, up to three faces), sum mu_c b_c < a b_i + a' b_j
dcert = {}
for (i, j) in disj:
    found = None
    if all(N[i][r] + N[j][r] == Q(0) for r in range(3)):
        found = (Q(1), Q(1), [])
    else:
        tgt = [N[i][r] + N[j][r] for r in range(3)]
        best = None
        for tri in itertools.combinations([m for m in range(F) if m not in (i, j)], 3):
            rows = [[N[m][r] for m in tri] for r in range(3)]
            sol = solve3(rows, tgt)
            if sol is None: continue
            if not all(s == Q(0) or pos(s) for s in sol): continue
            gap = B[i] + B[j] - sum((sol[t] * B[tri[t]] for t in range(3)), Q(0))
            if not pos(gap): continue
            cplx = sum(abs(s.a.numerator) + abs(s.b.numerator) + s.a.denominator + s.b.denominator for s in sol)
            if best is None or cplx < best[0]:
                best = (cplx, [(tri[t], sol[t]) for t in range(3) if sol[t] != Q(0)])
        if best: found = (Q(1), Q(1), best[1])
    assert found, (i, j)
    a, a2, lst = found
    while len(lst) < 3: lst = lst + [(i, Q(0))]
    for r in range(3):
        assert a * N[i][r] + a2 * N[j][r] == sum((mu * N[m][r] for (m, mu) in lst), Q(0))
    gap = a * B[i] + a2 * B[j] - sum((mu * B[m] for (m, mu) in lst), Q(0))
    assert pos(gap)
    dcert[(i, j)] = (a, a2, lst, gap)

o = []
w = o.append
def vec(v): return "!₂[" + ", ".join(x.lean() for x in v) + "]"
w(f"/-- Outward face normals. -/")
w(f"noncomputable def {X}N : Fin {F} → R3 :=\n  ![" + ",\n    ".join(vec(n) for n in N) + "]")
w(f"\n/-- Offsets. -/")
w(f"noncomputable def {X}B : Fin {F} → ℝ := ![" + ", ".join(b.lean() for b in B) + "]")
w(f"\n/-- Corners. -/")
w(f"noncomputable def {X}P : Fin {K} → R3 :=\n  ![" + ",\n    ".join(vec(p) for p in P) + "]")
w(f"\n/-- The table \"face `m` passes through corner `k`\". -/")
w(f"def {X}Z : Fin {F} → Fin {K} → Bool :=\n  ![" + ",\n    ".join(
    "![" + ", ".join("true" if Z[m][k] else "false" for k in range(K)) + "]" for m in range(F)) + "]")
w(f"\n/-- The values `b m − ⟪n m, p k⟫`. -/")
w(f"noncomputable def {X}S : Fin {F} → Fin {K} → ℝ :=\n  ![" + ",\n    ".join(
    "![" + ", ".join(S[m][k].lean() for k in range(K)) + "]" for m in range(F)) + "]")
for m in range(F):
    w(f"""
lemma {X}_slack_{m} (k : Fin {K}) : {X}B {m} - ⟪{X}N {m}, {X}P k⟫ = {X}S {m} k := by
  have ht := sqrt5_sq
  fin_cases k <;> simp [{X}B, {X}N, {X}P, {X}S, inner3] <;> grind""")
w(f"""
lemma {X}_slack (m : Fin {F}) (k : Fin {K}) : {X}B m - ⟪{X}N m, {X}P k⟫ = {X}S m k := by
  fin_cases m""" + "".join(f"\n  · exact {X}_slack_{m} k" for m in range(F)))
w("")
for m in range(F):
    w(f"""lemma {X}S_spec_{m} (k : Fin {K}) :
    ({X}Z {m} k = true → {X}S {m} k = 0) ∧ ({X}Z {m} k = false → 0 < {X}S {m} k) := by
  have h1 := sqrt5_gt; have h2 := sqrt5_lt
  fin_cases k <;> simp [{X}Z, {X}S] <;> linarith
""")
w(f"""lemma {X}S_spec (m : Fin {F}) (k : Fin {K}) :
    ({X}Z m k = true → {X}S m k = 0) ∧ ({X}Z m k = false → 0 < {X}S m k) := by
  fin_cases m""" + "".join(f"\n  · exact {X}S_spec_{m} k" for m in range(F)))
w(f"""
lemma {X}_tight (m : Fin {F}) (k : Fin {K}) (h : {X}Z m k = true) : ⟪{X}N m, {X}P k⟫ = {X}B m := by
  have h1 := {X}_slack m k
  have h2 := ({X}S_spec m k).1 h
  linarith

lemma {X}_lt (m : Fin {F}) (k : Fin {K}) (h : {X}Z m k = false) : ⟪{X}N m, {X}P k⟫ < {X}B m := by
  have h1 := {X}_slack m k
  have h2 := ({X}S_spec m k).2 h
  linarith

lemma {X}_le (m : Fin {F}) (k : Fin {K}) : ⟪{X}N m, {X}P k⟫ ≤ {X}B m := by
  cases h : {X}Z m k
  · exact ({X}_lt m k h).le
  · exact ({X}_tight m k h).le""")
ineqs = []
for m in range(F):
    terms = " + ".join(f"{N[m][r].lean()} * x {r}" for r in range(3))
    ineqs.append(f"{terms} ≤ {B[m].lean()}")
w(f"""
/-- The face inequalities in coordinates. -/
lemma {X}_ineqs {{x : R3}} (hx : x ∈ sol {X}N {X}B) :
    """ + " ∧\n    ".join(ineqs) + " :=\n  ⟨" + ",\n   ".join(
    f"by have h := hx {m}; simp [{X}N, {X}B, inner3] at h; linarith" for m in range(F)) + "⟩")
w(f"\n/-- The {len(edges)} edges: the two faces of each edge … -/")
w(f"def {X}Fi : Fin {len(edges)} → Fin {F} := ![" + ", ".join(str(e[0]) for e in edges) + "]")
w(f"def {X}Fj : Fin {len(edges)} → Fin {F} := ![" + ", ".join(str(e[1]) for e in edges) + "]")
w(f"/-- … and its two corners. -/")
w(f"def {X}Vk : Fin {len(edges)} → Fin {K} := ![" + ", ".join(str(e[2]) for e in edges) + "]")
w(f"def {X}Vl : Fin {len(edges)} → Fin {K} := ![" + ", ".join(str(e[3]) for e in edges) + "]")
w(f"\n/-- Three faces through each corner. -/")
w(f"def {X}T : Fin {K} → Fin {F} × Fin {F} × Fin {F} :=\n  ![" + ", ".join(
    f"({f[0]}, {f[1]}, {f[2]})" for f in faces_at) + "]")
w(f"""
lemma {X}T_spec : ∀ k, ({X}T k).1 ≠ ({X}T k).2.1 ∧ ({X}T k).1 ≠ ({X}T k).2.2 ∧
    ({X}T k).2.1 ≠ ({X}T k).2.2 ∧ {X}Z ({X}T k).1 k = true ∧ {X}Z ({X}T k).2.1 k = true ∧
    {X}Z ({X}T k).2.2 k = true := by decide

lemma {X}E_lt : ∀ e, {X}Fi e < {X}Fj e := by decide

lemma {X}E_inj : ∀ e e', {X}Fi e = {X}Fi e' → {X}Fj e = {X}Fj e' → e = e' := by decide

lemma {X}E_tight : ∀ e, {X}Z ({X}Fi e) ({X}Vk e) = true ∧ {X}Z ({X}Fi e) ({X}Vl e) = true ∧
    {X}Z ({X}Fj e) ({X}Vk e) = true ∧ {X}Z ({X}Fj e) ({X}Vl e) = true := by decide

lemma {X}E_other : ∀ e m, m ≠ {X}Fi e → m ≠ {X}Fj e →
    {X}Z m ({X}Vk e) = false ∨ {X}Z m ({X}Vl e) = false := by decide

/-- The statement of `IsEdgeData.cover`. -/
def {X}Cover (x : R3) (i j : Fin {F}) : Prop :=
  (∃ e, ({{i, j}} : Set (Fin {F})) = {{{X}Fi e, {X}Fj e}} ∧
    x ∈ segment ℝ ({X}P ({X}Vk e)) ({X}P ({X}Vl e))) ∨ ∃ k, x = {X}P k""")
inds = {}
for (i, j), (e, k, l, c, cp, D) in cert.items(): inds[(i, j, c)] = D
for (i, j), (k, c, cp, mu, a, a2, D) in vcert.items(): inds[(i, j, c)] = D
w("")
for (i, j, c), D in sorted(inds.items()):
    w(f"""lemma {X}_ind_{i}_{j}_{c} (v : R3) (h1 : ⟪{X}N {i}, v⟫ = 0) (h2 : ⟪{X}N {j}, v⟫ = 0)
    (h3 : ⟪{X}N {c}, v⟫ = 0) : v = 0 :=
  ind3 (D := {D.lean()}) (by have ht := sqrt5_sq; simp [{X}N]; grind) (by s5ne) v h1 h2 h3
""")
cov = f"{{x : R3}} (hx : x ∈ sol {X}N {X}B)"
for i in range(F):
    for j in range(i + 1, F):
        head = (f"lemma {X}_cover_{i}_{j} {cov} (hi : ⟪{X}N {i}, x⟫ = {X}B {i})\n"
                f"    (hj : ⟪{X}N {j}, x⟫ = {X}B {j}) : {X}Cover x {i} {j} :=")
        if (i, j) in cert:
            e, k, l, c, cp, D = cert[(i, j)]
            w(head + f"""
  Or.inl ⟨{e}, rfl, mem_segment_of_tight {X}_ind_{i}_{j}_{c}
    ({X}_tight {i} {k} (by decide)) ({X}_tight {i} {l} (by decide))
    ({X}_tight {j} {k} (by decide)) ({X}_tight {j} {l} (by decide))
    ({X}_tight {c} {l} (by decide)) ({X}_lt {c} {k} (by decide))
    ({X}_tight {cp} {k} (by decide)) ({X}_lt {cp} {l} (by decide)) hx hi hj⟩
""")
        elif (i, j) in vcert:
            k, c, cp, mu, a, a2, D = vcert[(i, j)]
            w(head + f"""
  Or.inr ⟨{k}, eq_of_tight {X}_ind_{i}_{j}_{c}
    ({X}_tight {c} {k} (by decide)) ({X}_tight {cp} {k} (by decide)) ({X}_tight {i} {k} (by decide))
    ({X}_tight {j} {k} (by decide)) (μ := {mu.lean()}) (a := {a.lean()}) (a' := {a2.lean()}) (by s5pos)
    (by have ht := sqrt5_sq; ext t; fin_cases t <;> simp [{X}N] <;> grind) hx hi hj⟩
""")
        else:
            a, a2, lst, gap = dcert[(i, j)]
            (c1, m1), (c2, m2), (c3, m3) = lst
            w(head + f"""
  (false_of_comb (i := {i}) (j := {j}) (c₁ := {c1}) (c₂ := {c2}) (c₃ := {c3}) (a := {a.lean()}) (a' := {a2.lean()})
    (μ₁ := {m1.lean()}) (μ₂ := {m2.lean()}) (μ₃ := {m3.lean()}) (by s5nn) (by s5nn) (by s5nn)
    (by have ht := sqrt5_sq; ext t; fin_cases t <;> simp [{X}N] <;> grind)
    (by
      have ht := sqrt5_sq
      have e : {a.lean()} * {X}B {i} + {a2.lean()} * {X}B {j} - ({m1.lean()} * {X}B {c1} + {m2.lean()} * {X}B {c2} +
          {m3.lean()} * {X}B {c3}) = {gap.lean()} := by simp [{X}B]; grind
      have h1 := sqrt5_gt; have h2 := sqrt5_lt
      linarith)
    hx hi hj).elim
""")
lines = [f"""lemma {X}_cover_lt {cov} :
    ∀ i j : Fin {F}, i < j → ⟪{X}N i, x⟫ = {X}B i → ⟪{X}N j, x⟫ = {X}B j → {X}Cover x i j := by
  intro i j hij hi hj
  fin_cases i <;> fin_cases j"""]
for i in range(F):
    for j in range(F):
        lines.append(f"  · exact {X}_cover_{i}_{j} hx hi hj" if i < j else "  · exact absurd hij (by decide)")
w("\n".join(lines))
w(f"""
lemma {X}_cover {cov} (i j : Fin {F}) (hij : i ≠ j)
    (hi : ⟪{X}N i, x⟫ = {X}B i) (hj : ⟪{X}N j, x⟫ = {X}B j) : {X}Cover x i j := by
  rcases lt_or_gt_of_ne hij with h | h
  · exact {X}_cover_lt hx i j h hi hj
  · rcases {X}_cover_lt hx j i h hj hi with ⟨e, he, hseg⟩ | hk
    · exact Or.inl ⟨e, (Set.pair_comm i j).trans he, hseg⟩
    · exact Or.inr hk""")
print("\n".join(o))
for (i, j, k, l) in edges:
    d2 = sum(((P[k][r] - P[l][r]) * (P[k][r] - P[l][r]) for r in range(3)), Q(0))
    g = dot(N[i], N[j]); X1 = dot(N[i], N[i]); Y1 = dot(N[j], N[j])
    print(f"--  edge {i} {j} corners {k} {l} len2 {d2} gram {X1} {Y1} {g}", file=sys.stderr)
