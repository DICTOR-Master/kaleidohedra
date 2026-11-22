# Generator of the Lean text of the edge data (IsEdgeData, study 5) of the dodecahedron and the icosahedron,
# coordinates in Q(sqrt5), exact (q5.py). Run on the compute host:
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
# integer codes: each normal scaled by its own denominator, all corners (and the interior point) by one factor
from math import lcm
def den(q): return lcm(q.a.denominator, q.b.denominator)
def vden(v): return lcm(*[den(c) for c in v])
N = [[c * vden(n) for c in n] for n in N]
sP = lcm(*[vden(p) for p in P])
P = [[c * sP for c in p] for p in P]
Zpt = [c * sP for c in Zpt]
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


# boundedness certificates: each signed axis direction = sum mu_c n_c, mu >= 0
bnd = []
for r in range(3):
    for sg in (1, -1):
        dv = [Q(sg if t == r else 0) for t in range(3)]
        found = None
        for tri in itertools.combinations(range(F), 3):
            rows = [[N[m][t] for m in tri] for t in range(3)]
            so = solve3(rows, dv)
            if so is None or not all(x == Q(0) or pos(x) for x in so): continue
            bd = sum((so[t] * B[tri[t]] for t in range(3)), Q(0))
            if found is None or bd.f() < found[2].f(): found = (tri, so, bd)
        assert found, (r, sg)
        bnd.append(found[:2])
# interior point z / lam
lamZ = lcm(*[den(c) for c in Zpt])
Zc = [c * lamZ for c in Zpt]
for m in range(F): assert pos(Q(lamZ) * B[m] - dot(N[m], Zc)), m
# kinds of edges by Gram values
kinds = []; kd = []
for (i, j, k, l) in edges:
    t = (dot(N[i], N[j]), dot(N[i], N[i]), dot(N[j], N[j]))
    if t not in kinds: kinds.append(t)
    kd.append(kinds.index(t))

def iq(q):   # integer code of a number of Z[sqrt d]
    assert q.a.denominator == 1 and q.b.denominator == 1, q
    return f"({q.a.numerator}, {q.b.numerator})"
def iv(v): return "![" + ", ".join(iq(c) for c in v) + "]"
def scale(qs):   # common positive integer factor making all coordinates integral
    L = lcm(*[den(q) for q in qs])
    return L, [q * L for q in qs]
def vec(v): return "!₂[" + ", ".join(x.lean() for x in v) + "]"

def flat_list(name, ints, per_line):
    """`name : List ℤ`, in chunks of at most 240 numbers (each chunk elaborated on its own)."""
    rows = [", ".join(ints[i:i + per_line]) for i in range(0, len(ints), per_line)]
    chunks = [ints[i:i + 240] for i in range(0, len(ints), 240)]
    if len(chunks) == 1:
        return f"def {name} : List ℤ :=\n  [" + ",\n    ".join(rows) + "]\n"
    out = ""
    for c, ch in enumerate(chunks):
        rs = [", ".join(ch[i:i + per_line]) for i in range(0, len(ch), per_line)]
        out += f"def {name}{c} : List ℤ :=\n  [" + ",\n    ".join(rs) + "]\n"
    return out + f"def {name} : List ℤ := " + " ++ ".join(f"{name}{c}" for c in range(len(chunks))) + "\n"

BIG = F > 40 or K > 100
def table(name, n, typ, elems, default, sep=", "):
    """A lookup table: `![...]` when small; a list with `getD` when large (cheap to elaborate)."""
    if not BIG:
        return f"def {name} : Fin {n} → {typ} :=\n  ![" + sep.join(elems) + "]"
    if typ == "V3":   # a flat list of integers, six per vector
        import re as _re
        ints = [x for e in elems for x in _re.findall(r"-?\d+", e)]
        assert len(ints) == 6 * n
        return (flat_list(f"{name}L", ints, 6) +
                f"def {name} (i : Fin {n}) : V3 := fun t : Fin 3 =>\n" +
                f"  ({name}L.getD (6 * i.val + 2 * t.val) 0, {name}L.getD (6 * i.val + 2 * t.val + 1) 0)")
    if typ == "Zd":   # a flat list of integers, two per number
        import re as _re
        ints = [x for e in elems for x in _re.findall(r"-?\d+", e)]
        assert len(ints) == 2 * n
        return (flat_list(f"{name}L", ints, 12) +
                f"def {name} (i : Fin {n}) : Zd := ({name}L.getD (2 * i.val) 0, {name}L.getD (2 * i.val + 1) 0)")
    return (f"def {name}L : List ({typ}) :=\n  [" + sep.join(elems) + "]\n" +
            f"def {name} (i : Fin {n}) : {typ} := {name}L.getD i.val {default}")
D = FIELD
o = []
w = o.append
w(f"""/-
Generated by gen/gen_pieces.py ({which}), adapted from the Dehn Canon's checks/gen_edges5.py: exact arithmetic in
Q(sqrt{D}), every fact checked in Python first and again by Lean, by evaluation on integer codes (Packets.Exact).
Edge data (`IsEdgeData`), interior point, boundedness and the Gram values of the face normals at each edge.
No `sorry`.
-/
module

public import Packets.Exact

@[expose] public section

open scoped RealInnerProductSpace Real
open Set Module

namespace PacketsGen

open DehnCanon.Library

set_option maxRecDepth 20000
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option linter.unnecessarySeqFocus false
""")
w(f"/-- Outward face normals. -/")
w(f"noncomputable def {X}N : Fin {F} → R3 :=\n  ![" + ",\n    ".join(", ".join(vec(n) for n in N[i:i + 4])
                                                    for i in range(0, F, 4)) + "]")
w(f"\n/-- Offsets. -/")
w(f"noncomputable def {X}B : Fin {F} → ℝ := ![" + ", ".join(b.lean() for b in B) + "]")
w(f"\n/-- The solid. -/\ndef {X}Set : Set R3 := sol {X}N {X}B")
w(f"\n/-- Integer codes of the normals, offsets and corners (`x.1 + x.2 √{D}`). -/")
w(table(f"{X}Nc", F, "V3", [iv(n) for n in N], "(fun _ => (0, 0))", ",\n    "))
w(table(f"{X}Bc", F, "Zd", [iq(b) for b in B], "(0, 0)"))
w(table(f"{X}Pc", K, "V3", [iv(p) for p in P], "(fun _ => (0, 0))", ",\n    "))
w(f"\n/-- The {len(edges)} edges: the two faces of each edge and its two corners. -/")
w(table(f"{X}Fi", len(edges), f"Fin {F}", [str(e[0]) for e in edges], "0"))
w(table(f"{X}Fj", len(edges), f"Fin {F}", [str(e[1]) for e in edges], "0"))
w(table(f"{X}Vk", len(edges), f"Fin {K}", [str(e[2]) for e in edges], "0"))
w(table(f"{X}Vl", len(edges), f"Fin {K}", [str(e[3]) for e in edges], "0"))
w(f"\n/-- Three faces through each corner. -/")
w(table(f"{X}T", K, f"Fin {F} × Fin {F} × Fin {F}", [f"({f[0]}, {f[1]}, {f[2]})" for f in faces_at], "(0, 0, 0)"))
w(f"\ndef {X}Sol : Solid {D} {F} {K} {len(edges)} := ⟨{X}Nc, {X}Bc, {X}Pc, {X}Fi, {X}Fj, {X}Vk, {X}Vl⟩")
w(f"\n/-- Corners. -/\nnoncomputable def {X}P : Fin {K} → R3 := {X}Sol.p")
# certificates
def cert_text(i, j):
    if (i, j) in cert:
        e, k, l, c, cp, Dt = cert[(i, j)]
        return f".edge {e} {c} {cp}"
    if (i, j) in vcert:
        k, c, cp, mu, a, a2, Dt = vcert[(i, j)]
        L, (mu2, a3, a4) = scale([mu, a, a2])
        return f".corner {k} {c} {cp} ({L}, 0) {iq(mu2)} {iq(a3)} {iq(a4)}"
    a, a2, lst, gap = dcert[(i, j)]
    qs = [a, a2] + [mu for (m, mu) in lst]
    L, sc = scale(qs)
    (c1, _), (c2, _), (c3, _) = lst
    return f".farkas {iq(sc[0])} {iq(sc[1])} {c1} {c2} {c3} {iq(sc[2])} {iq(sc[3])} {iq(sc[4])}"
rows = []
for i in range(F):
    rows.append("![" + ", ".join(cert_text(i, j) if i < j else ".none" for j in range(F)) + "]")
w(f"\n/-- How each two faces meet (edge, corner, or a Farkas certificate that they do not). -/")
if BIG:
    lrows = ["[" + r[2:-1] + "]" for r in rows]
    w(f"def {X}CtL : List (List (Cert {F} {K} {len(edges)})) :=\n  [" + ",\n    ".join(lrows) + "]")
    w(f"def {X}Ct (i j : Fin {F}) : Cert {F} {K} {len(edges)} := ({X}CtL.getD i.val []).getD j.val .none")
else:
    w(f"def {X}Ct : Fin {F} → Fin {F} → Cert {F} {K} {len(edges)} :=\n  ![" + ",\n    ".join(rows) + "]")
bl = []
for (tri, so) in bnd:
    L, sc = scale(list(so))
    bl.append(f"⟨{tri[0]}, {tri[1]}, {tri[2]}, {iq(sc[0])}, {iq(sc[1])}, {iq(sc[2])}, ({L}, 0)⟩")
w(f"\n/-- Bounds along the six axis directions. -/")
w(f"def {X}Bd : Fin 6 → BCert {F} := ![" + ", ".join(bl) + "]")
w(f"\n/-- An interior point (times {lamZ}). -/\ndef {X}Zc : V3 := {iv(Zc)}")
for m in range(F):
    w(f"""lemma {X}N_eq_{m} : {X}N {m} = {X}Sol.n {m} := by
  rw [Solid.n, show {X}Sol.N {m} = {iv(N[m])} by decide +kernel]
  ext t; fin_cases t <;> simp [{X}N, evv, ev] <;> ring
""")
w(f"""
lemma {X}N_eq : {X}N = {X}Sol.n := by
  funext m; fin_cases m""" + "".join(f"\n  · exact {X}N_eq_{m}" for m in range(F)) + f"""

""")
for m in range(F):
    w(f"""lemma {X}B_eq_{m} : {X}B {m} = {X}Sol.b {m} := by
  rw [Solid.b, show {X}Sol.B {m} = {iq(B[m])} by decide +kernel]
  simp [{X}B, ev] <;> ring
""")
w(f"""
lemma {X}B_eq : {X}B = {X}Sol.b := by
  funext m; fin_cases m""" + "".join(f"\n  · exact {X}B_eq_{m}" for m in range(F)) + f"""

lemma {X}_bd : ∀ t, {X}Sol.bOK (Solid.axis t) ({X}Bd t) = true := by decide +kernel

theorem {X}_bounded : Bornology.IsBounded (sol {X}N {X}B) := by
  rw [{X}N_eq, {X}B_eq]; exact {X}Sol.bounded_of (by norm_num) {X}Bd {X}_bd

theorem isPoly_{X} : DehnCanon.Library.IsPoly {X}Set := ⟨{X}_bounded, Fin {F}, inferInstance, {X}N, _, rfl⟩

theorem {X}_interior : (interior (sol {X}N {X}B)).Nonempty := by
  rw [{X}N_eq, {X}B_eq]; exact {X}Sol.interior_of (by norm_num) {X}Zc ({lamZ}, 0) (by decide +kernel) (by decide +kernel)

lemma {X}_mem : ∀ m k, {X}Sol.tight m k = true ∨ {X}Sol.below m k = true := by decide +kernel

lemma {X}_three : ∀ k, ({X}T k).1 ≠ ({X}T k).2.1 ∧ ({X}T k).1 ≠ ({X}T k).2.2 ∧ ({X}T k).2.1 ≠ ({X}T k).2.2 ∧
    {X}Sol.tight ({X}T k).1 k = true ∧ {X}Sol.tight ({X}T k).2.1 k = true ∧
    {X}Sol.tight ({X}T k).2.2 k = true := by decide +kernel

lemma {X}_lt : ∀ e, {X}Sol.fi e < {X}Sol.fj e := by decide +kernel

lemma {X}_inj : ∀ e e', {X}Sol.fi e = {X}Sol.fi e' → {X}Sol.fj e = {X}Sol.fj e' → e = e' := by decide +kernel

lemma {X}_tight : ∀ e, {X}Sol.tight ({X}Sol.fi e) ({X}Sol.vk e) = true ∧
    {X}Sol.tight ({X}Sol.fi e) ({X}Sol.vl e) = true ∧ {X}Sol.tight ({X}Sol.fj e) ({X}Sol.vk e) = true ∧
    {X}Sol.tight ({X}Sol.fj e) ({X}Sol.vl e) = true := by decide +kernel

lemma {X}_other : ∀ e m, m ≠ {X}Sol.fi e → m ≠ {X}Sol.fj e →
    {X}Sol.below m ({X}Sol.vk e) = true ∨ {X}Sol.below m ({X}Sol.vl e) = true := by decide +kernel

lemma {X}_cov : ∀ i j, i < j → {X}Sol.certOK i j ({X}Ct i j) = true := by decide +kernel

theorem {X}_isEdgeData : IsEdgeData {X}N {X}B {X}P {X}Fi {X}Fj {X}Vk {X}Vl := by
  rw [{X}N_eq, {X}B_eq]
  exact {X}Sol.isEdgeData_of (by norm_num) ({X}Sol.bounded_of (by norm_num) {X}Bd {X}_bd) {X}_mem {X}T
    {X}_three {X}_lt {X}_inj {X}_tight {X}_other {X}Ct {X}_cov""")
w(f"""
/-- The kinds of edges, by the Gram values (⟪n i, n j⟫, ⟪n i, n i⟫, ⟪n j, n j⟫) of their two faces. -/
""" + table(f"{X}Kd", len(edges), f"Fin {len(kinds)}", [str(c) for c in kd], "0") + f"""
noncomputable def {X}Gg : Fin {len(kinds)} → ℝ := ![""" + ", ".join(t[0].lean() for t in kinds) + f"""]
noncomputable def {X}GX : Fin {len(kinds)} → ℝ := ![""" + ", ".join(t[1].lean() for t in kinds) + f"""]
noncomputable def {X}GY : Fin {len(kinds)} → ℝ := ![""" + ", ".join(t[2].lean() for t in kinds) + f"""]
def {X}GgC : Fin {len(kinds)} → Zd := ![""" + ", ".join(iq(t[0]) for t in kinds) + f"""]
def {X}GXC : Fin {len(kinds)} → Zd := ![""" + ", ".join(iq(t[1]) for t in kinds) + f"""]
def {X}GYC : Fin {len(kinds)} → Zd := ![""" + ", ".join(iq(t[2]) for t in kinds) + f"""]

lemma {X}_gram (e : Fin {len(edges)}) : ⟪{X}N ({X}Fi e), {X}N ({X}Fj e)⟫ = {X}Gg ({X}Kd e) ∧
    ⟪{X}N ({X}Fi e), {X}N ({X}Fi e)⟫ = {X}GX ({X}Kd e) ∧ ⟪{X}N ({X}Fj e), {X}N ({X}Fj e)⟫ = {X}GY ({X}Kd e) := by
  have hc : ∀ e, zdot {D} ({X}Sol.N ({X}Fi e)) ({X}Sol.N ({X}Fj e)) = {X}GgC ({X}Kd e) ∧
      zdot {D} ({X}Sol.N ({X}Fi e)) ({X}Sol.N ({X}Fi e)) = {X}GXC ({X}Kd e) ∧
      zdot {D} ({X}Sol.N ({X}Fj e)) ({X}Sol.N ({X}Fj e)) = {X}GYC ({X}Kd e) := by decide +kernel
  have hv : ∀ k, ev {D} ({X}GgC k) = {X}Gg k ∧ ev {D} ({X}GXC k) = {X}GX k ∧ ev {D} ({X}GYC k) = {X}GY k := by
    intro k; fin_cases k <;> refine ⟨?_, ?_, ?_⟩ <;> simp [ev, {X}GgC, {X}GXC, {X}GYC, {X}Gg, {X}GX, {X}GY] <;> ring
  obtain ⟨h1, h2, h3⟩ := hc e
  obtain ⟨v1, v2, v3⟩ := hv ({X}Kd e)
  rw [{X}N_eq, Solid.inner_n, Solid.inner_n, Solid.inner_n]
  exact ⟨by rw [h1, v1], by rw [h2, v2], by rw [h3, v3]⟩

/-- The two normals at each edge are not parallel (`⟪u, v⟫² < ⟪u, u⟫ ⟪v, v⟫`). -/
lemma {X}_gram_lt (e : Fin {len(edges)}) : ⟪{X}N ({X}Fi e), {X}N ({X}Fj e)⟫ ^ 2 <
    ⟪{X}N ({X}Fi e), {X}N ({X}Fi e)⟫ * ⟪{X}N ({X}Fj e), {X}N ({X}Fj e)⟫ := by
  have hc : ∀ e, zpos {D} (zsub (zmul {D} (zdot {D} ({X}Sol.N ({X}Fi e)) ({X}Sol.N ({X}Fi e)))
      (zdot {D} ({X}Sol.N ({X}Fj e)) ({X}Sol.N ({X}Fj e))))
      (zmul {D} (zdot {D} ({X}Sol.N ({X}Fi e)) ({X}Sol.N ({X}Fj e)))
        (zdot {D} ({X}Sol.N ({X}Fi e)) ({X}Sol.N ({X}Fj e))))) = true := by decide +kernel
  have h := zpos_spec (by norm_num) (hc e)
  rw [ev_sub, ev_mul, ev_mul] at h
  rw [{X}N_eq, Solid.inner_n, Solid.inner_n, Solid.inner_n, sq]
  linarith

end PacketsGen
""")
out = "\n".join(o)
fname = {"pyrD": "GenPyrD", "ti": "GenTI", "pyrI": "GenPyrI", "td": "GenTD", "dh": "GenDH", "ih": "GenIH",
         "to": "GenTO", "tco": "GenTCO", "tid": "GenTID"}[which]
open(f"../Packets/{fname}.lean", "w").write(out + "\n")
print(f"-- wrote {fname}.lean, {out.count(chr(10)) + 1} lines", file=sys.stderr)
for (i, j, k, l) in edges:
    pass
for c, t in enumerate(kinds):
    print(f"-- kind {c}: gram {t} first edge {kd.index(c)} count {kd.count(c)}", file=sys.stderr)
