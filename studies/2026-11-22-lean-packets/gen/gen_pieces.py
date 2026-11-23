# Generator of the Lean text of the edge data (IsEdgeData, study 5) of the dodecahedron and the icosahedron,
# coordinates in Q(sqrt5), exact (q5.py). Run:
#   python3 gen_edges5.py dod > dod_block.lean
#   python3 gen_edges5.py ico > ico_block.lean
# Every emitted fact is checked here exactly first; Lean checks it again.
import sys
FIELD = 2 if sys.argv[1] == 'tco' else 5
exec(open('q2.py' if FIELD == 2 else 'q5.py').read())
from fractions import Fraction as Fr

LO, HI = (Fr(1414, 1000), Fr(1415, 1000)) if FIELD == 2 else (Fr(2236, 1000), Fr(2237, 1000))   # LO < sqrt5 < HI
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
if which == "ti":
    X = "ti"; N = ico_corners + dod_corners
    P = []
    for base in ([z, Q(2), Q(3, 3)], [Q(2), Q(5, 1), Q(2, 2)], [Q(1, 1), Q(4), Q(4, 2)]):
        for v in cyc(base): P += signs(v)
    Zpt = [z, z, z]
elif which in ("pyrD", "pyrI"):
    X = which
    n0, corners = (ico_corners[0], dod_corners) if which == "pyrD" else (dod_corners[0], ico_corners)
    vals = [dot(n0, v) for v in corners]
    mx = vals[0]
    for v in vals:
        if (v - mx).sign() > 0: mx = v
    base = [v for v in corners if dot(n0, v) == mx]
    nb = len(base)
    d2 = lambda u, v: dot(sub(u, v), sub(u, v))
    m2 = min((d2(u, v) for u in base for v in base if u != v), key=lambda q: q.f())
    sides = []
    for i in range(nb):
        for j in range(i + 1, nb):
            if d2(base[i], base[j]) == m2:
                nv = cross(base[i], base[j])
                other = [w for w in base if w is not base[i] and w is not base[j]][0]
                if dot(nv, other).sign() > 0: nv = [-c for c in nv]
                sides.append(nv)
    assert len(sides) == nb
    N = [n0] + sides
    P = [[z, z, z]] + base
    Zpt = [sum((w[r] for w in base), Q(0)) / (2 * nb) for r in range(3)]
elif which == "td":
    X = "td"; N = ico_corners + dod_corners
    P = []
    for bse in ([z, Q(5, 1), Q(-1, 1)], [Q(-1, 1), Q(2, 2), Q(1, 1)], [Q(1, 1), Q(3, 1), Q(4)]):
        for v in cyc(bse): P += signs(v)
    Zpt = [z, z, z]
elif which == "dh":
    X = "dh"; N = ico_corners; P = dod_corners; Zpt = [z, z, z]
elif which == "ih":
    X = "ih"; N = dod_corners; P = ico_corners; Zpt = [z, z, z]
elif which == "to":
    X = "to"
    N = []
    for v in cyc([Q(1), z, z]): N += signs(v)
    N += signs([Q(1), Q(1), Q(1)])
    P = []
    for bse in ([z, Q(1), Q(2)], [z, Q(2), Q(1)]):
        for v in cyc(bse): P += signs(v)
    Zpt = [z, z, z]
elif which == "tid":
    X = "tid"
    phi = Q(Fr(1, 2), Fr(1, 2)); iphi = phi - 1
    sq = []
    for v in cyc([Q(2), z, z]): sq += signs(v)
    for v in cyc([Q(1), phi * phi, phi]): sq += signs(v)
    N = ico_corners + dod_corners + sq
    P = []
    for bse in ([iphi, iphi, 3 + phi], [2 * iphi, phi, 1 + 2 * phi], [iphi, phi * phi, -1 + 3 * phi],
                [2 * phi - 1, Q(2), 2 + phi], [phi, Q(3), 2 * phi]):
        for v in cyc([bse[0], bse[2], bse[1]]): P += signs(v)
    Zpt = [z, z, z]
elif which == "tco":
    X = "tco"
    N = []
    for v in cyc([Q(1), Q(1), z]): N += signs(v)
    N += signs([Q(1), Q(1), Q(1)])
    for v in cyc([Q(1), z, z]): N += signs(v)
    P = []
    for bse in ([Q(1), Q(1, 1), Q(1, 2)], [Q(1), Q(1, 2), Q(1, 1)]):
        for v in cyc(bse): P += signs(v)
    Zpt = [z, z, z]
else:
    raise SystemExit("unknown piece")
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
WEIGHTS = [(Q(1), Q(1)), (Q(2), Q(1)), (Q(1), Q(2)), (Q(3), Q(1)), (Q(1), Q(3)), (Q(3), Q(2)), (Q(2), Q(3)),
           (Q(Fr(1, 2), Fr(1, 2)), Q(1)), (Q(1), Q(Fr(1, 2), Fr(1, 2)))]
for (i, j) in disj:
    found = None
    if all(N[i][r] + N[j][r] == Q(0) for r in range(3)):
        found = (Q(1), Q(1), [])
    else:
        nrm = lambda v: math.sqrt(sum(x.f() ** 2 for x in v))
        dirv = [N[i][r].f() / nrm(N[i]) + N[j][r].f() / nrm(N[j]) for r in range(3)]
        others = [m for m in range(F) if m not in (i, j)]
        cand = sorted(others, key=lambda m: -sum(N[m][r].f() * dirv[r] for r in range(3)) / nrm(N[m]))[:16]
        for (wa, wb) in WEIGHTS:
            tgt = [wa * N[i][r] + wb * N[j][r] for r in range(3)]
            best = None
            for pool in (cand, others):
                for tri in itertools.combinations(pool, 3):
                    rows = [[N[m][r] for m in tri] for r in range(3)]
                    sol = solve3(rows, tgt)
                    if sol is None: continue
                    if not all(s == Q(0) or pos(s) for s in sol): continue
                    gap = wa * B[i] + wb * B[j] - sum((sol[t] * B[tri[t]] for t in range(3)), Q(0))
                    if not pos(gap): continue
                    cplx = sum(abs(s.a.numerator) + abs(s.b.numerator) + s.a.denominator + s.b.denominator for s in sol)
                    if best is None or cplx < best[0]:
                        best = (cplx, [(tri[t], sol[t]) for t in range(3) if sol[t] != Q(0)])
                    if pool is others: break
                if best: break
            if best:
                found = (wa, wb, best[1]); break
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
w(f"""/-
Generated by gen/gen_pieces.py ({which}), adapted from the Dehn Canon's checks/gen_edges5.py: exact arithmetic in
Q(sqrt5), every fact checked in Python first and again by Lean. Edge data (`IsEdgeData`), interior point,
boundedness and the Gram values of the face normals at each edge.
No `sorry`.
-/
module

public import DehnCanon.Dehn7Dodeca

@[expose] public section

open scoped RealInnerProductSpace Real
open Set Module

namespace PacketsGen

open DehnCanon.Library

set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option linter.unnecessarySeqFocus false
set_option maxHeartbeats 800000
set_option maxRecDepth 20000
""")
def vec(v): return "!₂[" + ", ".join(x.lean() for x in v) + "]"
w(f"/-- Outward face normals. -/")
w(f"noncomputable def {X}N : Fin {F} → R3 :=\n  ![" + ",\n    ".join(", ".join(vec(n) for n in N[i:i + 4])
                                                    for i in range(0, F, 4)) + "]")
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
  ind3 (D := {D.lean()}) (by have ht := sqrt5_sq; simp [{X}N] <;> grind) (by s5ne) v h1 h2 h3
""")
i_cov0 = len(o)
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
          {m3.lean()} * {X}B {c3}) = {gap.lean()} := by simp [{X}B] <;> grind
      have h1 := sqrt5_gt; have h2 := sqrt5_lt
      linarith)
    hx hi hj).elim
""")
i_cov1 = len(o)
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


# boundedness certificates: each signed axis d = sum mu_c n_c, mu >= 0
def le_comb_lemma():
    return f"""
lemma {X}_le_of_comb3 {{c₁ c₂ c₃ : Fin {F}}} {{μ₁ μ₂ μ₃ : ℝ}} {{d : R3}} (h₁ : 0 ≤ μ₁) (h₂ : 0 ≤ μ₂)
    (h₃ : 0 ≤ μ₃) (hrel : d = μ₁ • {X}N c₁ + μ₂ • {X}N c₂ + μ₃ • {X}N c₃) {{x : R3}} (hx : x ∈ sol {X}N {X}B) :
    ⟪d, x⟫ ≤ μ₁ * {X}B c₁ + μ₂ * {X}B c₂ + μ₃ * {X}B c₃ := by
  rw [hrel, inner_add_left, inner_add_left, real_inner_smul_left, real_inner_smul_left, real_inner_smul_left]
  have e1 := mul_le_mul_of_nonneg_left (hx c₁) h₁
  have e2 := mul_le_mul_of_nonneg_left (hx c₂) h₂
  have e3 := mul_le_mul_of_nonneg_left (hx c₃) h₃
  linarith
"""
bnd = []; Cb = 0
for r in range(3):
    for sg in (1, -1):
        d = [Q(sg if t == r else 0) for t in range(3)]
        found = None
        for tri in itertools.combinations(range(F), 3):
            rows = [[N[m][t] for m in tri] for t in range(3)]
            so = solve3(rows, d)
            if so is None or not all(x == Q(0) or pos(x) for x in so): continue
            bd = sum((so[t] * B[tri[t]] for t in range(3)), Q(0))
            if found is None or bd.f() < found[2].f(): found = (tri, so, bd)
        assert found, (r, sg)
        tri, so, bd = found
        Cb = max(Cb, int(bd.f()) + 1)
        bnd.append((r, sg, tri, so, bd))
bnd_lines = ""
for (r, sg, tri, so, bd) in bnd:
    dv = vec([Q(sg if t == r else 0) for t in range(3)])
    bnd_lines += f"""  have b{r}{'p' if sg > 0 else 'm'} := {X}_le_of_comb3 (d := {dv}) (c₁ := {tri[0]}) (c₂ := {tri[1]}) (c₃ := {tri[2]})
    (μ₁ := {so[0].lean()}) (μ₂ := {so[1].lean()}) (μ₃ := {so[2].lean()}) (by s5nn) (by s5nn) (by s5nn)
    (by have ht := sqrt5_sq; ext t; fin_cases t <;> simp [{X}N] <;> grind) hx
  simp only [{X}B, inner3] at b{r}{'p' if sg > 0 else 'm'}
  norm_num at b{r}{'p' if sg > 0 else 'm'}
"""
w(le_comb_lemma())
# interior point
SZ = [B[m] - dot(N[m], Zpt) for m in range(F)]
assert all(pos(v) for v in SZ)
w(f"""
/-- An interior point. -/
noncomputable def {X}Z0 : R3 := {vec(Zpt)}

noncomputable def {X}SZ : Fin {F} → ℝ := ![""" + ", ".join(v.lean() for v in SZ) + f"""]

lemma {X}_int_slack (m : Fin {F}) : {X}B m - ⟪{X}N m, {X}Z0⟫ = {X}SZ m := by
  have ht := sqrt5_sq
  fin_cases m <;> simp [{X}B, {X}N, {X}Z0, {X}SZ, inner3] <;> grind

lemma {X}SZ_pos (m : Fin {F}) : 0 < {X}SZ m := by
  fin_cases m <;> simp [{X}SZ] <;> s5pos

theorem {X}_interior : (interior (sol {X}N {X}B)).Nonempty := by
  refine ⟨{X}Z0, mem_interior_iff_mem_nhds.2 (Filter.mem_of_superset ((isOpen_iInter_of_finite
    fun m => isOpen_lt (by fun_prop : Continuous fun x : R3 => ⟪{X}N m, x⟫) continuous_const).mem_nhds
    (Set.mem_iInter.2 fun m => ?_)) fun x hx m => (Set.mem_iInter.1 hx m).le)⟩
  have h1 := {X}_int_slack m
  have h2 := {X}SZ_pos m
  show ⟪{X}N m, {X}Z0⟫ < {X}B m
  linarith

def {X}Set : Set R3 := sol {X}N {X}B

theorem {X}_bounded : Bornology.IsBounded (sol {X}N {X}B) := by
  refine bounded_of_coords {Cb} (fun x hx i => ?_)
  have h1 := sqrt5_gt; have h2 := sqrt5_lt; have h5 := sqrt5_sq
""" + bnd_lines + f"""
  fin_cases i <;> simp only [Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk] <;> rw [abs_le] <;>
    constructor <;> linarith

theorem isPoly_{X} : DehnCanon.Library.IsPoly {X}Set := ⟨{X}_bounded, Fin {F}, inferInstance, {X}N, _, rfl⟩

theorem {X}_isEdgeData : IsEdgeData {X}N {X}B {X}P {X}Fi {X}Fj {X}Vk {X}Vl where
  bounded := {X}_bounded
  corner_mem := fun k m => {X}_le m k
  corner_three := fun k => by
    obtain ⟨h1, h2, h3, t1, t2, t3⟩ := {X}T_spec k
    exact ⟨_, _, _, h1, h2, h3, {X}_tight _ _ t1, {X}_tight _ _ t2, {X}_tight _ _ t3⟩
  faces_ne := fun e => ({X}E_lt e).ne
  faces_inj := fun e e' h => by
    rcases Set.pair_eq_pair_iff.1 h with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact {X}E_inj e e' h1 h2
    · have a := {X}E_lt e
      rw [h1, h2] at a
      exact absurd a (lt_asymm ({X}E_lt e'))
  tight := fun e => by
    obtain ⟨t1, t2, t3, t4⟩ := {X}E_tight e
    exact ⟨{X}_tight _ _ t1, {X}_tight _ _ t2, {X}_tight _ _ t3, {X}_tight _ _ t4⟩
  other := fun e m h1 h2 => by
    rcases {X}E_other e m h1 h2 with h | h
    · exact Or.inl ({X}_lt _ _ h)
    · exact Or.inr ({X}_lt _ _ h)
  cover := fun x hx i j hij hi hj => {X}_cover hx i j hij hi hj""")
# gram kinds
kinds = []; kd = []
for (i, j, k, l) in edges:
    t = (dot(N[i], N[j]), dot(N[i], N[i]), dot(N[j], N[j]))
    if t not in kinds: kinds.append(t)
    kd.append(kinds.index(t))
w(f"""
/-- The kinds of edges, by the Gram values (⟪n i, n j⟫, ⟪n i, n i⟫, ⟪n j, n j⟫) of their two faces. -/
def {X}Kd : Fin {len(edges)} → Fin {len(kinds)} := ![""" + ", ".join(str(c) for c in kd) + f"""]
noncomputable def {X}Gg : Fin {len(kinds)} → ℝ := ![""" + ", ".join(t[0].lean() for t in kinds) + f"""]
noncomputable def {X}GX : Fin {len(kinds)} → ℝ := ![""" + ", ".join(t[1].lean() for t in kinds) + f"""]
noncomputable def {X}GY : Fin {len(kinds)} → ℝ := ![""" + ", ".join(t[2].lean() for t in kinds) + f"""]

lemma {X}_gram (e : Fin {len(edges)}) : ⟪{X}N ({X}Fi e), {X}N ({X}Fj e)⟫ = {X}Gg ({X}Kd e) ∧
    ⟪{X}N ({X}Fi e), {X}N ({X}Fi e)⟫ = {X}GX ({X}Kd e) ∧ ⟪{X}N ({X}Fj e), {X}N ({X}Fj e)⟫ = {X}GY ({X}Kd e) := by
  have ht := sqrt5_sq
  rw [inner3', inner3', inner3']
  fin_cases e <;> refine ⟨?_, ?_, ?_⟩ <;> simp [{X}N, {X}Fi, {X}Fj, {X}Kd, {X}Gg, {X}GX, {X}GY, inner3] <;> grind""")
w("\nend PacketsGen")
for c, t in enumerate(kinds):
    print(f"-- kind {c}: gram {t} first edge {kd.index(c)} count {kd.count(c)}", file=sys.stderr)
out = "\n".join(o)
if FIELD == 2:
    out = (out.replace("√5", "√2").replace("sqrt5_sq", "pk_sqrt2_sq").replace("s5pos", "pk2pos")
           .replace("s5nn", "pk2nn").replace("s5ne", "pk2ne").replace("sqrt5_gt", "pk_sqrt2_gt")
           .replace("sqrt5_lt", "pk_sqrt2_lt"))
    out = out.replace("set_option maxRecDepth 20000", """set_option maxRecDepth 20000

lemma pk_sqrt2_sq : (√2 : ℝ) ^ 2 = 2 := Real.sq_sqrt (by norm_num)

lemma pk_sqrt2_gt : (1414 / 1000 : ℝ) < √2 := (Real.lt_sqrt (by norm_num)).2 (by norm_num)

lemma pk_sqrt2_lt : √2 < (1415 / 1000 : ℝ) := (Real.sqrt_lt' (by norm_num)).2 (by norm_num)

/-- Signs of numbers a + b√2 from 1.414 < √2 < 1.415. -/
macro "pk2pos" : tactic => `(tactic| (have h1 := pk_sqrt2_gt; have h3 := pk_sqrt2_lt; linarith))

macro "pk2nn" : tactic => `(tactic| (have h1 := pk_sqrt2_gt; have h3 := pk_sqrt2_lt; linarith))

macro "pk2ne" : tactic => `(tactic| (have h1 := pk_sqrt2_gt; have h3 := pk_sqrt2_lt; intro h; linarith))""", 1)
if X == "tid":
    hdr = o[0]
    body = [x for x in o[1:i_cov0]]
    covers = o[i_cov0:i_cov1]
    tail = o[i_cov1:]
    parts = [body]
    cur = []; cnt = 0
    for c in covers:
        n = c.count("\n") + 1
        if cnt + n > 8500 and cur:
            parts.append(cur); cur = []; cnt = 0
        cur.append(c); cnt += n
    parts.append(cur)
    parts.append(tail)
    for k, part in enumerate(parts, 1):
        h = hdr if k == 1 else hdr.replace("public import DehnCanon.Dehn7Dodeca", f"public import Packets.GenTID{k - 1}")
        txt = h + "\n" + "\n".join(part)
        if "end PacketsGen" not in txt: txt += "\n\nend PacketsGen\n"
        open(f"../Packets/GenTID{k}.lean", "w").write(txt)
    print(f"-- wrote {len(parts)} files", file=sys.stderr)
else:
    print(out)
for (i, j, k, l) in edges:
    d2 = sum(((P[k][r] - P[l][r]) * (P[k][r] - P[l][r]) for r in range(3)), Q(0))
    g = dot(N[i], N[j]); X1 = dot(N[i], N[i]); Y1 = dot(N[j], N[j])
    print(f"--  edge {i} {j} corners {k} {l} len2 {d2} gram {X1} {Y1} {g}", file=sys.stderr)
