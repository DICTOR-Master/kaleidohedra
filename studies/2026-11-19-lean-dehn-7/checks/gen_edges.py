# Generator of the Lean text of the edge data (IsEdgeData, study 5) of a solid with integer face normals,
# offsets and corners linear in a parameter t (exact fractions). Run on the compute host:
#   python3 gen_edges.py oct  > oct_block.lean
#   python3 gen_edges.py co   > co_block.lean
# It checks every fact it emits exactly (slack table, edges, determinants) before writing it; Lean checks it again.
import sys, itertools
from fractions import Fraction as Fr

class L:  # c0 + c1 t
    def __init__(s, c0=0, c1=0): s.c0 = Fr(c0); s.c1 = Fr(c1)
    def __add__(s, o): o = Lc(o); return L(s.c0 + o.c0, s.c1 + o.c1)
    __radd__ = __add__
    def __neg__(s): return L(-s.c0, -s.c1)
    def __sub__(s, o): return s + (-Lc(o))
    def __rsub__(s, o): return Lc(o) - s
    def __mul__(s, k):  # by a number
        assert not isinstance(k, L); return L(s.c0 * k, s.c1 * k)
    __rmul__ = __mul__
    def __eq__(s, o): o = Lc(o); return s.c0 == o.c0 and s.c1 == o.c1
    def __hash__(s): return hash((s.c0, s.c1))
    def at(s, t): return s.c0 + s.c1 * t
    def lean(s):
        def fr(x):
            return f"{x.numerator}" if x.denominator == 1 else f"({x.numerator} / {x.denominator})"
        c0, c1 = s.c0, s.c1
        if c1 == 0:
            return fr(c0) if c0 >= 0 else f"(-{fr(-c0)})"
        tt = "t" if abs(c1) == 1 else f"{fr(abs(c1))} * t"
        if c0 == 0:
            return tt if c1 > 0 else f"(-{tt})" if abs(c1) == 1 else f"(-({tt}))"
        if c1 > 0:
            return f"({tt} {'+' if c0 > 0 else '-'} {fr(abs(c0))})"
        return f"({fr(c0)} - {tt})" if c0 > 0 else f"(-{fr(-c0)} - {tt})"
def Lc(o): return o if isinstance(o, L) else L(o)

def dot(n, p): return sum((p[r] * n[r] for r in range(3)), L(0))
def det(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))

T = L(0, 1)
which = sys.argv[1]
if which == "oct":
    X = "oct"; param = False; samples = [Fr(0)]
    N = [list(s) for s in itertools.product([1, -1], repeat=3)]
    B = [L(1)] * 8
    P = []
    for i in range(3):
        for sg in (1, -1):
            p = [L(0)] * 3; p[i] = L(sg); P.append(p)
elif which == "co":
    X = "co"; param = True; samples = [Fr(7, 4), Fr(5, 4), Fr(3, 2)]
    N = []
    for i in range(3):
        for sg in (1, -1):
            n = [0, 0, 0]; n[i] = sg; N.append(n)
    N += [list(s) for s in itertools.product([1, -1], repeat=3)]
    B = [L(1)] * 6 + [T] * 8
    P = []
    for i in range(3):
        for sg in (1, -1):
            for j in range(3):
                if j == i: continue
                for sj in (1, -1):
                    p = [L(0)] * 3; p[i] = L(sg); p[j] = sj * (T - 1); P.append(p)
else:
    raise SystemExit("oct or co")
F = len(N); K = len(P)
S = [[B[m] - dot(N[m], P[k]) for k in range(K)] for m in range(F)]
# exact sign of a linear function on the open interval 1 < t < 2 (or a constant)
def sgn(v):
    if not param:
        return (v.c0 > 0) - (v.c0 < 0)
    a, b = v.at(1), v.at(2)
    if a == 0 and b == 0: return 0
    if a >= 0 and b >= 0: return 1
    if a <= 0 and b <= 0: return -1
    raise SystemExit("sign changes")
Z = [[sgn(S[m][k]) == 0 for k in range(K)] for m in range(F)]
for m in range(F):
    for k in range(K):
        assert sgn(S[m][k]) >= 0, (m, k)
        if Z[m][k]: assert S[m][k] == L(0)
# the same tight table at every sample value of t (where it is defined)
for t in samples:
    for m in range(F):
        for k in range(K):
            assert (S[m][k].at(t) == 0) == Z[m][k] or (param and t == Fr(3, 2) and False)
corners_of = [[k for k in range(K) if Z[m][k]] for m in range(F)]
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
# order edges: kind A (square-hexagon, or all for oct) first
def kind(e):
    i, j = e[0], e[1]
    g = sum(N[i][r] * N[j][r] for r in range(3))
    return (sum(x * x for x in N[i]), sum(x * x for x in N[j]), g)
edges.sort(key=lambda e: (kind(e), e))
kinds = sorted(set(kind(e) for e in edges))
print("-- kinds (|n_i|^2, |n_j|^2, <n_i,n_j>) and counts:",
      [(kd, sum(1 for e in edges if kind(e) == kd)) for kd in kinds], file=sys.stderr)
for (i, j, k, l) in edges:
    for m in range(F):
        if m not in (i, j): assert not (Z[m][k] and Z[m][l])
    d2 = sum(((P[k][r] - P[l][r]) * 1 for r in range(3)), L(0))
# certificates for the edges
cert = {}
for e, (i, j, k, l) in enumerate(edges):
    cs = [c for c in range(F) if c not in (i, j) and Z[c][l] and not Z[c][k] and det(N[i], N[j], N[c]) != 0]
    cps = [c for c in range(F) if c not in (i, j) and Z[c][k] and not Z[c][l]]
    c, cp = cs[0], cps[0]
    cert[(i, j)] = (e, k, l, c, cp, det(N[i], N[j], N[c]))
print(f"-- {F} faces, {K} corners, {len(edges)} edges, {len(vonly)} pairs on one corner, {len(disj)} disjoint pairs",
      file=sys.stderr)

o = []
w = o.append
def vec(v): return "!₂[" + ", ".join(x.lean() for x in v) + "]"
targ = "(t : ℝ) " if param else ""
tt = " t" if param else ""
hyp = "(ht1 : 1 < t) (ht2 : t < 2) " if param else ""
hypuse = " ht1 ht2" if param else ""
w(f"/-- Outward face normals. -/")
w(f"noncomputable def {X}N : Fin {F} → R3 :=\n  ![" + ",\n    ".join(vec([L(x) for x in n]) for n in N) + "]")
w(f"\n/-- Offsets. -/")
w(f"noncomputable def {X}B {targ}: Fin {F} → ℝ := ![" + ", ".join(b.lean() for b in B) + "]")
w(f"\n/-- Corners. -/")
w(f"noncomputable def {X}P {targ}: Fin {K} → R3 :=\n  ![" + ",\n    ".join(vec(p) for p in P) + "]")
w(f"\n/-- The table \"face `m` passes through corner `k`\". -/")
w(f"def {X}Z : Fin {F} → Fin {K} → Bool :=\n  ![" + ",\n    ".join(
    "![" + ", ".join("true" if Z[m][k] else "false" for k in range(K)) + "]" for m in range(F)) + "]")
w(f"\n/-- The values `b m − ⟪n m, p k⟫`. -/")
w(f"noncomputable def {X}S {targ}: Fin {F} → Fin {K} → ℝ :=\n  ![" + ",\n    ".join(
    "![" + ", ".join(S[m][k].lean() for k in range(K)) + "]" for m in range(F)) + "]")
# slack lemma split per face (cheaper elaboration)
for m in range(F):
    w(f"""
lemma {X}_slack_{m} {targ}(k : Fin {K}) : {X}B{tt} {m} - ⟪{X}N {m}, {X}P{tt} k⟫ = {X}S{tt} {m} k := by
  fin_cases k <;> simp [{X}B, {X}N, {X}P, {X}S, inner3] <;> ring""")
w(f"""
lemma {X}_slack {targ}(m : Fin {F}) (k : Fin {K}) : {X}B{tt} m - ⟪{X}N m, {X}P{tt} k⟫ = {X}S{tt} m k := by
  fin_cases m""" + "".join(f"\n  · exact {X}_slack_{m}{tt} k" for m in range(F)))
w(f"""
""")
for m in range(F):
    w(f"""lemma {X}S_spec_{m} {targ}{hyp}(k : Fin {K}) :
    ({X}Z {m} k = true → {X}S{tt} {m} k = 0) ∧ ({X}Z {m} k = false → 0 < {X}S{tt} {m} k) := by
  fin_cases k <;> simp [{X}Z, {X}S]{' <;> linarith' if param else ''}
""")
w(f"""lemma {X}S_spec {targ}{hyp}(m : Fin {F}) (k : Fin {K}) :
    ({X}Z m k = true → {X}S{tt} m k = 0) ∧ ({X}Z m k = false → 0 < {X}S{tt} m k) := by
  fin_cases m""" + "".join(f"\n  · exact {X}S_spec_{m}{tt}{hypuse} k" for m in range(F)))
w(f"""

lemma {X}_tight {targ}{hyp}(m : Fin {F}) (k : Fin {K}) (h : {X}Z m k = true) :
    ⟪{X}N m, {X}P{tt} k⟫ = {X}B{tt} m := by
  have h1 := {X}_slack{tt} m k
  have h2 := ({X}S_spec{tt}{hypuse} m k).1 h
  linarith

lemma {X}_lt {targ}{hyp}(m : Fin {F}) (k : Fin {K}) (h : {X}Z m k = false) :
    ⟪{X}N m, {X}P{tt} k⟫ < {X}B{tt} m := by
  have h1 := {X}_slack{tt} m k
  have h2 := ({X}S_spec{tt}{hypuse} m k).2 h
  linarith

lemma {X}_le {targ}{hyp}(m : Fin {F}) (k : Fin {K}) : ⟪{X}N m, {X}P{tt} k⟫ ≤ {X}B{tt} m := by
  cases h : {X}Z m k
  · exact ({X}_lt{tt}{hypuse} m k h).le
  · exact ({X}_tight{tt}{hypuse} m k h).le""")
# coordinates of the inequalities
ineqs = []
for m in range(F):
    terms = " + ".join(f"({N[m][r]} : ℝ) * x {r}" for r in range(3))
    ineqs.append(f"{terms} ≤ {B[m].lean()}")
w(f"""
/-- The face inequalities in coordinates. -/
lemma {X}_ineqs {{{'t : ℝ} {' if param else ''}x : R3}} (hx : x ∈ sol {X}N ({X}B{tt})) :
    """ + " ∧\n    ".join(ineqs) + " :=\n  ⟨" + ",\n   ".join(f"by have h := hx {m}; simp [{X}N, {X}B, inner3] at h; linarith" for m in range(F)) + "⟩")
# edges
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
def {X}Cover {targ}(x : R3) (i j : Fin {F}) : Prop :=
  (∃ e, ({{i, j}} : Set (Fin {F})) = {{{X}Fi e, {X}Fj e}} ∧
    x ∈ segment ℝ ({X}P{tt} ({X}Vk e)) ({X}P{tt} ({X}Vl e))) ∨ ∃ k, x = {X}P{tt} k""")
# independent triples
inds = set()
for (i, j), (e, k, l, c, cp, D) in cert.items(): inds.add((i, j, c, D))
w("")
for (i, j, c, D) in sorted(inds):
    w(f"""lemma {X}_ind_{i}_{j}_{c} (v : R3) (h1 : ⟪{X}N {i}, v⟫ = 0) (h2 : ⟪{X}N {j}, v⟫ = 0)
    (h3 : ⟪{X}N {c}, v⟫ = 0) : v = 0 :=
  ind3 (D := {D}) (by norm_num [{X}N]) (by norm_num) v h1 h2 h3
""")
cov = f"{{{'t : ℝ} {' if param else ''}x : R3}} {hyp}(hx : x ∈ sol {X}N ({X}B{tt}))"
hyp_ = "(_ht1 : 1 < t) (_ht2 : t < 2) " if param else ""
cov_ = f"{{{'t : ℝ} {' if param else ''}x : R3}} {hyp_}(hx : x ∈ sol {X}N ({X}B{tt}))"
for i in range(F):
    for j in range(i + 1, F):
        cv = cov if (i, j) in cert else cov_
        head = (f"lemma {X}_cover_{i}_{j} {cv} (hi : ⟪{X}N {i}, x⟫ = {X}B{tt} {i})\n"
                f"    (hj : ⟪{X}N {j}, x⟫ = {X}B{tt} {j}) : {X}Cover{tt} x {i} {j} :=")
        if (i, j) in cert:
            e, k, l, c, cp, D = cert[(i, j)]
            a = f"{hypuse}"
            w(head + f"""
  Or.inl ⟨{e}, rfl, mem_segment_of_tight {X}_ind_{i}_{j}_{c}
    ({X}_tight{tt}{a} {i} {k} (by decide)) ({X}_tight{tt}{a} {i} {l} (by decide))
    ({X}_tight{tt}{a} {j} {k} (by decide)) ({X}_tight{tt}{a} {j} {l} (by decide))
    ({X}_tight{tt}{a} {c} {l} (by decide)) ({X}_lt{tt}{a} {c} {k} (by decide))
    ({X}_tight{tt}{a} {cp} {k} (by decide)) ({X}_lt{tt}{a} {cp} {l} (by decide)) hx hi hj⟩
""")
        elif (i, j) in vonly:
            k = vonly[(i, j)]
            assert not param
            w(head + f""" by
  have H := {X}_ineqs hx
  simp [{X}N, {X}B, inner3] at hi hj
  refine Or.inr ⟨{k}, ?_⟩
  obtain ⟨""" + ", ".join(f"h{m}" for m in range(F)) + f"""⟩ := H
  ext r; fin_cases r <;> simp [{X}P] <;> linarith
""")
        else:
            w(head + f""" by
  have H := {X}_ineqs hx
  simp [{X}N, {X}B, inner3] at hi hj
  obtain ⟨""" + ", ".join(f"h{m}" for m in range(F)) + f"""⟩ := H
  exfalso; linarith
""")
# dispatcher with bullets in the order of fin_cases
lines = [f"""lemma {X}_cover_lt {cov} :
    ∀ i j : Fin {F}, i < j → ⟪{X}N i, x⟫ = {X}B{tt} i → ⟪{X}N j, x⟫ = {X}B{tt} j → {X}Cover{tt} x i j := by
  intro i j hij hi hj
  fin_cases i <;> fin_cases j"""]
for i in range(F):
    for j in range(F):
        if i < j:
            lines.append(f"  · exact {X}_cover_{i}_{j}{hypuse} hx hi hj")
        else:
            lines.append(f"  · exact absurd hij (by decide)")
w("\n".join(lines))
w(f"""
lemma {X}_cover {cov} (i j : Fin {F}) (hij : i ≠ j)
    (hi : ⟪{X}N i, x⟫ = {X}B{tt} i) (hj : ⟪{X}N j, x⟫ = {X}B{tt} j) : {X}Cover{tt} x i j := by
  rcases lt_or_gt_of_ne hij with h | h
  · exact {X}_cover_lt{hypuse} hx i j h hi hj
  · rcases {X}_cover_lt{hypuse} hx j i h hj hi with ⟨e, he, hseg⟩ | hk
    · exact Or.inl ⟨e, (Set.pair_comm i j).trans he, hseg⟩
    · exact Or.inr hk""")
print("\n".join(o))
# summary for the README / for the hand-written part
print("-- edges (i, j, k, l, kind):", [(e[0], e[1], e[2], e[3], kind(e)) for e in edges], file=sys.stderr)
for e in edges:
    k, l = e[2], e[3]
    d2 = sum(((P[k][r] - P[l][r]).c0 ** 2 for r in range(3)), Fr(0)) if not param else None
    if param:
        diffs = [(P[k][r] - P[l][r]) for r in range(3)]
        print("--  edge", e, "diff", [(d.c0, d.c1) for d in diffs], file=sys.stderr)
    else:
        print("--  edge", e, "len2", d2, file=sys.stderr)
