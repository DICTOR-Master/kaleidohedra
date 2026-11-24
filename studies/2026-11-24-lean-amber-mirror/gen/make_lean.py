"""Write AmberMirror/Data.lean ... AmberMirror/Main.lean from cert.json (export.py).  Nothing here is trusted: the generator only
proposes the exact matrices and the coefficients of each linear combination; Lean's `linear_combination` (ring normalisation)
checks every one.  Exact arithmetic throughout (fractions; numbers a + b*s with s = sqrt 5; polynomials in s for the
unreduced expressions Lean sees, reduced with s^2 = 5 by exact division by s^2 - 5).
Also cross-checks that the three planes derived here are exactly the rows printed by odd_edges.py.
Usage: python make_lean.py  (reads cert.json, writes ../AmberMirror/*.lean)"""
import json, os
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "../AmberMirror")
C = json.load(open(os.path.join(HERE, "cert.json")))
# ---- polynomials in s (unreduced), dict deg -> Fraction ----
def P(*c): return {i: F(x) for i, x in enumerate(c) if F(x) != 0}
def padd(a, b):
    r = dict(a)
    for k, v in b.items(): r[k] = r.get(k, 0) + v
    return {k: v for k, v in r.items() if v != 0}
def pneg(a): return {k: -v for k, v in a.items()}
def psub(a, b): return padd(a, pneg(b))
def pmul(a, b):
    r = {}
    for i, x in a.items():
        for j, y in b.items(): r[i+j] = r.get(i+j, 0) + x*y
    return {k: v for k, v in r.items() if v != 0}
def pdivmod5(a):   # a = q*(s^2-5) + r, deg r <= 1
    a = dict(a); q = {}
    for d in sorted(a, reverse=True):
        if d >= 2 and a.get(d, 0) != 0:
            c = a[d]; q[d-2] = q.get(d-2, 0) + c; a[d] = 0; a[d-2] = a.get(d-2, 0) + 5*c
    return {k: v for k, v in q.items() if v != 0}, {k: v for k, v in a.items() if v != 0}
def red(a): return pdivmod5(a)[1]
def q5inv(a):   # a reduced p + q s
    p, q = a.get(0, F(0)), a.get(1, F(0)); n = p*p - 5*q*q; assert n != 0
    return P(p/n, -q/n)
def q5mul(a, b): return red(pmul(a, b))
# ---- linear forms: dict var -> poly, var '1' = constant ----
def ladd(a, b):
    r = dict(a)
    for k, v in b.items(): r[k] = padd(r.get(k, {}), v)
    return {k: v for k, v in r.items() if v}
def lsc(c, a): return {k: pmul(c, v) for k, v in a.items() if pmul(c, v)}
def lsub(a, b): return ladd(a, lsc(P(-1), b))
def lred(a): return {k: red(v) for k, v in a.items() if red(v)}
def ldiv5(a):
    out = {}
    for k, v in a.items():
        q, r = pdivmod5(v); assert not r, ("not divisible", k, v)
        if q: out[k] = q
    return out
# ---- Lean printing ----
def fr(x): return f"({x.numerator}:ℝ)" if x.denominator == 1 else f"({x.numerator}/{x.denominator}:ℝ)"
def pstr(a):
    if not a: return "0"
    t = []
    for d in sorted(a):
        t.append(fr(a[d]) if d == 0 else (f"{fr(a[d])}*s" if d == 1 else f"{fr(a[d])}*s^{d}"))
    return "(" + " + ".join(t) + ")"
def vstr(v): c, r = v; return f"(x {c}).{r}"
def lstr(a):
    t = [pstr(a[k]) if k == '1' else f"{pstr(a[k])}*{vstr(k)}" for k in sorted(a, key=str)]
    return " + ".join(t) if t else "0"
PHI = P(F(1, 2), F(1, 2))
def proj(v):
    v = [P(t) for t in v]
    return [padd(psub(v[2], v[3]), pmul(PHI, psub(v[4], v[5]))),
            padd(psub(v[0], v[1]), pmul(PHI, padd(v[2], v[3]))),
            padd(pmul(PHI, padd(v[0], v[1])), padd(v[4], v[5]))]
def vsub(a, b): return [psub(x, y) for x, y in zip(a, b)]
def cross(a, b): return [psub(pmul(a[1], b[2]), pmul(a[2], b[1])), psub(pmul(a[2], b[0]), pmul(a[0], b[2])),
                         psub(pmul(a[0], b[1]), pmul(a[1], b[0]))]
def dot(a, b): return padd(padd(pmul(a[0], b[0]), pmul(a[1], b[1])), pmul(a[2], b[2]))
R = "xyz"
# ---- per wall: reduced affine map y = M u + t, and the Lean proof ----
walls = {int(k): v for k, v in C["walls"].items()}
wallrows = {}    # k -> list of 3 reduced linear forms (lhs - rhs) == 0, i.e. y_r - sum m u - t
lean_w = []
for k in sorted(walls):
    w = walls[k]; a, b = w["a"], w["b"]; X = [proj(c) for c in w["corners"]]
    n = cross(vsub(X[1], X[0]), vsub(X[3], X[0])); Dp = dot(n, n); qD, Dr = pdivmod5(Dp); Dinv = q5inv(Dr)
    pr, qr = Dr.get(0, F(0)), Dr.get(1, F(0)); assert pr + qr*F(2236, 1000) > 0 and pr + qr*F(2237, 1000) > 0
    u = [{(a, r): P(1)} for r in R]; y = [{(b, r): P(1)} for r in R]
    # n . (u - X0) as linear form
    nd = {}
    for i in range(3): nd = ladd(nd, ladd(lsc(n[i], u[i]), {'1': pneg(pmul(n[i], X[0][i]))}))
    rows, proofs, stmts = [], [], []
    for r in range(3):
        ar = ladd(lsc(Dr, lsub(y[r], u[r])), lsc(pmul(P(2), n[r]), nd))   # lemma: D*(y-u) - (-2 nd n_r) = 0
        lr = lred(lsc(Dinv, ar))                                         # reduced: y_r - (M u + t)_r
        assert lr.get((b, R[r])) == P(1)
        rhs = {kk: pneg(v) for kk, v in lr.items() if kk != (b, R[r])}
        Q = ldiv5(lsub(lr, lsc(Dinv, ar)))
        stmts.append(f"(x {b}).{R[r]} = {lstr(rhs)}")
        proofs.append(f"linear_combination {pstr(Dinv)} * e{R[r]}" + (f" + ({lstr(Q)}) * hs" if Q else ""))
        rows.append(lr)
    wallrows[k] = rows
    cs = ", ".join("proj " + " ".join(f"({t})" for t in c) for c in w["corners"])
    lean_w.append((k, a, b, w["corners"], stmts, proofs, Dr, qD))
# ---- Data.lean ----
L = ["import AmberMirror.Basic", "", "/-! Data of the three-edge certificate (generated by gen/make_lean.py from gen/cert.json).",
     "Each wall: its two cells (patch numbering) and its four corners, 6D lattice points of the patch, projected by `proj`. -/", "",
     "namespace AmberMirror", "noncomputable section", ""]
for k, a, b, cor, *_ in lean_w:
    L.append(f"/-- wall {k} of the patch, between cells {a} and {b} -/")
    L.append(f"def w{k} : Wall := ⟨{a}, {b}, " + ", ".join("proj " + " ".join(f"({t})" for t in c) for c in cor) + "⟩")
L.append("")
for i, e in enumerate(C["edges"], 1):
    ws = e["path_walls"] + e["walls"]
    L.append(f"/-- odd edge {i}: lattice points {e['edge'][0]} – {e['edge'][1]}; cells round it in order {e['cells']} "
             f"({len(e['cells'])} cells, walls {e['walls']}); tree path from the start cell {e['path']} (walls {e['path_walls']}) -/")
    L.append(f"def edgeWalls{i} : List Wall := [" + ", ".join(f"w{k}" for k in ws) + "]")
allw = sorted(walls)
L.append(""); L.append("/-- all 14 walls used by the certificate -/")
L.append("def walls : List Wall := [" + ", ".join(f"w{k}" for k in allw) + "]")
L += ["", "end", "end AmberMirror", ""]
os.makedirs(OUT, exist_ok=True); open(os.path.join(OUT, "Data.lean"), "w").write("\n".join(L))
# ---- Walls.lean: each mirror as an explicit affine map ----
L = ["import AmberMirror.Data", "", "/-! Each wall's mirror, written out: `x b = mirror … (x a)` gives three linear equations with",
     "coefficients in ℚ(√5) (generated; every coefficient checked by `linear_combination`). -/", "",
     "namespace AmberMirror", "noncomputable section", ""]
for k, a, b, cor, stmts, proofs, Dr, qD in lean_w:
    X = [proj(c) for c in cor]; n = cross(vsub(X[1], X[0]), vsub(X[3], X[0])); pl = dot(n, vsub(X[2], X[0]))
    qp, rp = pdivmod5(pl); assert not rp
    L.append(f"/-- wall {k} is flat: its fourth corner lies on the plane through the other three (the mirror plane) -/")
    L.append(f"theorem w{k}_flat : V3.dot (nrm w{k}.c0 w{k}.c1 w{k}.c3) (V3.sub w{k}.c2 w{k}.c0) = 0 := by")
    L.append(f"  simp only [w{k}, nrm, V3.dot, V3.cross, V3.sub, proj, φ]" + (f"; linear_combination ({pstr(qp)}) * hs" if qp else "; ring"))
    L.append(f"theorem w{k}_eq (x : ℕ → V3) (h : x w{k}.b = mirror w{k}.c0 w{k}.c1 w{k}.c3 (x w{k}.a)) :")
    L.append("    " + " ∧\n    ".join(stmts) + " := by")
    L.append(f"  simp only [w{k}] at h")
    L.append(f"  obtain ⟨ex, ey, ez⟩ := mirror_poly h (D := {pstr(Dr)})")
    L.append(f"    (by simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ]; linear_combination ({pstr(qD)}) * hs)")
    L.append(f"    (by have := s_lo; have := s_hi; apply ne_of_gt; linarith)")
    L.append(f"  simp only [nrm, V3.dot, V3.cross, V3.sub, proj, φ] at ex ey ez")
    L.append(f"  refine ⟨?_, ?_, ?_⟩")
    for p_ in proofs: L.append("  · " + p_)
    L.append("")
L += ["end", "end AmberMirror", ""]
open(os.path.join(OUT, "Walls.lean"), "w").write("\n".join(L))
# ---- linear solver over Q(sqrt5) for certificates ----
def solve_comb(rows, target):
    """find c_j (reduced) with sum c_j rows_j == target (reduced linear forms)"""
    keys = sorted({k for r in rows + [target] for k in r}, key=str)
    m = len(rows)
    A = [[rows[j].get(kk, {}) for j in range(m)] + [target.get(kk, {})] for kk in keys]
    piv = []; rk = 0
    for c in range(m):
        p = next((i for i in range(rk, len(A)) if A[i][c]), None)
        if p is None: continue
        A[rk], A[p] = A[p], A[rk]; iv = q5inv(A[rk][c]); A[rk] = [q5mul(iv, z) for z in A[rk]]
        for i in range(len(A)):
            if i != rk and A[i][c]:
                f = A[i][c]; A[i] = [red(psub(z, pmul(f, w))) for z, w in zip(A[i], A[rk])]
        piv.append(c); rk += 1
    assert all(not A[i][m] for i in range(rk, len(A))), "target not in span"
    cvec = [{} for _ in range(m)]
    for i, c in enumerate(piv): cvec[c] = A[i][m]
    chk = {}
    for j in range(m): chk = ladd(chk, lsc(cvec[j], rows[j]))
    assert lred(lsub(chk, target)) == {}
    return cvec
def q5parse(t):
    t = t.replace("+-", "-"); 
    if "r5" not in t: return P(F(t))
    t = t.replace("r5", "")
    i = max(t.rfind("+"), t.rfind("-", 1)) if ("+" in t[1:] or "-" in t[1:]) else 0
    if i <= 0: return P(0, F(t) if t not in ("", "-") else F(t + "1"))
    return P(F(t[:i]), F(t[i:].lstrip("+")))
st = C["start"]
L = ["import AmberMirror.Walls", "", "/-! Theorem 3 (iv) of paper #118: the three odd edges of one rhombic face (wall 3). -/", "",
     "namespace AmberMirror", "noncomputable section", ""]
planes = []
for i, e in enumerate(C["edges"], 1):
    pl = [q5parse(t) for t in e["plane"]]; planes.append(pl)
    pd = [f"{pstr(pl[r])}*p.{R[r]}" for r in range(3) if pl[r]]
    L.append(f"/-- the mirror-plane condition of odd edge {i}, exactly the row printed by odd_edges.py: {e['plane']} -/")
    L.append(f"def plane{i} (p : V3) : Prop := " + " + ".join(pd) + f" = {pstr(pl[3])}")
L.append("")
for i, e in enumerate(C["edges"], 1):
    ws = list(dict.fromkeys(e["path_walls"] + e["walls"])); rows = []; names = []
    for k in ws:
        for r in range(3): rows.append(wallrows[k][r]); names.append(f"h{k}{R[r]}")
    pl = planes[i-1]
    target = {(st, R[r]): pl[r] for r in range(3) if pl[r]}; target['1'] = pneg(pl[3])
    cv = solve_comb(rows, target)
    # unreduced: Lean sees c_j * (lhs_j - rhs_j) with lhs - rhs = rows_j (rows are printed reduced) -> residual divisible
    tot = {}
    for c, r in zip(cv, rows): tot = ladd(tot, lsc(c, r))
    Q = ldiv5(lsub(target, tot))
    L.append(f"/-- odd edge {i} ({len(e['cells'])} cells round it): if every two neighbouring cores along the tree path and round "
             f"the edge are mirror images in their shared wall, the core of the start cell {st} lies on plane {i}. -/")
    L.append(f"theorem edge{i}_plane (x : ℕ → V3) (h : ∀ w ∈ edgeWalls{i}, x w.b = mirror w.c0 w.c1 w.c3 (x w.a)) :")
    L.append(f"    plane{i} (x {st}) := by")
    for k in ws:
        L.append(f"  obtain ⟨h{k}x, h{k}y, h{k}z⟩ := w{k}_eq x (h w{k} (by simp [edgeWalls{i}]))")
    L.append(f"  unfold plane{i}")
    comb = " + ".join(f"{pstr(c)} * {nm}" for c, nm in zip(cv, names) if c)
    L.append(f"  linear_combination {comb}" + (f" + ({lstr(Q)}) * hs" if Q else ""))
    L.append("")
# core
prow = []
for i, pl in enumerate(planes):
    prow.append({**{('p', R[r]): pl[r] for r in range(3) if pl[r]}, '1': pneg(pl[3])})
cv = solve_comb(prow, {'1': P(1)})
tot = {}
for c, r in zip(cv, prow): tot = ladd(tot, lsc(c, r))
Q = ldiv5(lsub({'1': P(1)}, tot)); assert not Q or set(Q) <= {'1'}
def pv(a): return lstr(a).replace("(x p).", "p.")
L.append("/-- the algebraic core: the three mirror-plane conditions have no common solution. -/")
L.append("theorem planes_no_common_point : ¬ ∃ p : V3, plane1 p ∧ plane2 p ∧ plane3 p := by")
L.append("  rintro ⟨p, h1, h2, h3⟩")
L.append("  unfold plane1 at h1; unfold plane2 at h2; unfold plane3 at h3")
L.append("  have : (1:ℝ) = 0 := by")
L.append("    linear_combination " + " + ".join(f"{pstr(c)} * h{j+1}" for j, c in enumerate(cv) if c) + (f" + ({pv(Q)}) * hs" if Q else ""))
L.append("  exact one_ne_zero this")
L.append("")
L += ["/-- the two odd edges with 5 cells round them together force z = 0 -/",
      "theorem plane1_plane3_z (p : V3) (h1 : plane1 p) (h3 : plane3 p) : p.z = 0 := by",
      "  unfold plane1 at h1; unfold plane3 at h3; linear_combination h3 - h1", "",
      "/-- the odd edge with 3 cells round it forces z = −(1+√5)/2 = −φ -/",
      "theorem plane2_z (p : V3) (h2 : plane2 p) : p.z = -(1 + s)/2 := by",
      "  unfold plane2 at h2; linear_combination (-1/2:ℝ) * h2", "",
      "/-- **Theorem 3 (iv), certificate form.** No placement of the cores' centres in the cells of the patch makes every two",
      "neighbouring cores mirror images in their shared wall: already the 14 walls of the tree path and of the three odd edges",
      "of wall 3 admit none. -/",
      "theorem no_mirror_placement :", "    ¬ ∃ x : ℕ → V3, ∀ w ∈ walls, x w.b = mirror w.c0 w.c1 w.c3 (x w.a) := by",
      "  rintro ⟨x, h⟩",
      "  have sub : ∀ l : List Wall, (∀ w ∈ l, w ∈ walls) → ∀ w ∈ l, x w.b = mirror w.c0 w.c1 w.c3 (x w.a) :=",
      "    fun l hl w hw => h w (hl w hw)",
      "  exact planes_no_common_point ⟨x " + str(st) + ","]
L += [f"    edge{i}_plane x (sub _ (by simp [edgeWalls{i}, walls]))" + ("," if i < 3 else "⟩") for i in (1, 2, 3)]
L += ["", "end", "end AmberMirror", ""]
open(os.path.join(OUT, "Main.lean"), "w").write("\n".join(L))
# cross-check: the planes follow from the reduced wall maps (done in solve_comb asserts); print summary
print("walls", allw); print("planes", [[pstr(x) for x in pl] for pl in planes]); print("core coefficients", [pstr(c) for c in cv])
ok = (len(allw) == 14 and [len(e["cells"]) for e in C["edges"]] == [5, 3, 5]
      and all(len(wallrows[k]) == 3 for k in allw) and lred(lsub(tot, {'1': P(1)})) == {})
print("FINAL ok" if ok else "FINAL FAIL (see checks above)")
