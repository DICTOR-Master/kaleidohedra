#!/usr/bin/env python3
"""The Vacuus and the Resonus of the whole catalogue, exact (24 Nov 2026).

Vacuus (#110, Section 2): one plane (plate) through the centre O and each edge.
Resonus (DICTO, 24 Nov): one plane through O parallel to each face; parallel faces share one plane.

Reuses the exact code of study 2026-11-24-vacuus-enumeration unchanged: its builders (uniform solids, prism
family, Johnson solids J1-J83, J91, J92) and its analyse() (exact hull checks, plates, sheets, kinds, slices,
mirrors). Added here:
  * signs are decided by interval arithmetic (mpmath iv) around an enclosure of the field generator, raising
    the precision until the interval excludes 0 (the earlier code read signs from an 80-digit float);
  * J84-J90 in their own number fields (stage 1, j84_90_exact.py), with exact arithmetic by python-flint
    (fmpq_poly modulo the defining polynomial) and signs by Arb ball arithmetic at a certified real root;
  * for every solid: the Resonus and Vacuus as exact plane sets, their intersection, which planes are mirrors
    (exact reflection), and both central arrangements on the sphere: vertices, edges, regions, every region's
    number of sides (exact face tracing), simplicial or not;
  * the polar quantities R*(P) (planes at right angles to the corner directions of P) and V*(P) (planes at
    right angles to the edge directions of P), which are the Resonus and Vacuus of the polar P* (Theorem 1 of
    the resonus study);
  * independent checks (each an assert): Euler; every edge on exactly one plate; Resonus count = faces minus
    parallel pairs (pairs found by a zero cross product); Theorem 1(b) on every edge; mirror flags recomputed by
    exact reflection agree with analyse(); arrangement counts by face tracing agree with the formula
    f2 = 1 - f0 + f1; the Resonus is the same about both centres of a Johnson solid.
Run (venv with sympy + python-flint): python scripts/catalogue.py [uniform|prisms|johnson|all]
"""
import os, sys, json, time, functools, itertools
from collections import Counter
import multiprocessing as mpr

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
VE = os.path.normpath(os.path.join(HERE, "../../2026-11-24-vacuus-enumeration"))
sys.path.insert(0, os.path.join(VE, "scripts"))
_cwd = os.getcwd(); os.chdir(VE)
import vacuus_exact as VX
import johnson_exact as JX
os.chdir(_cwd)
import sympy as sp
import mpmath as mp
from flint import fmpq_poly, fmpz_poly, fmpq, arb, acb, arb_poly, ctx
from vacuus_exact import vadd, vsub, vneg, dot, cross, scal, canon, vkey, fl

# ---------------------------------------------------------------- rigorous signs for the sympy fields
_ALPHA = {}

def _alpha_iv(F, dps):
    k = (id(F), dps)
    if k not in _ALPHA:
        s = sp.N(F.K.ext.as_expr(), dps + 30)
        a = mp.mpf(str(s)); r = mp.mpf(10) ** (-dps) * (1 + abs(a))
        _ALPHA[k] = (a - r, a + r)
    return _ALPHA[k]

_SIGN = {}

def rig_sign(self, a):
    if not a: return 0
    k = (id(self), self.key(a))
    s = _SIGN.get(k)
    if s is not None: return s
    for dps in (60, 200, 800, 3000):
        with mp.workdps(dps + 20):
            lo, hi = _alpha_iv(self, dps)
            mp.iv.dps = dps + 20
            A = mp.iv.mpf([lo, hi])
            v = mp.iv.mpf(0)
            for co in k[1]:
                v = v * A + mp.iv.mpf(int(co.numerator)) / int(co.denominator)
            if v.a > 0: s = 1; break
            if v.b < 0: s = -1; break
    else:
        raise AssertionError("sign not certified")
    _SIGN[k] = s
    return s

VX.Fld.sign = rig_sign

# ---------------------------------------------------------------- number fields for J84-J90 (python-flint)
class NFE:
    __slots__ = ("F", "p")
    def __init__(self, F, p): self.F = F; self.p = p
    def _c(self, o):
        if isinstance(o, NFE): return o.p
        return fmpq_poly([fmpq(o)])
    def __add__(self, o): return NFE(self.F, self.p + self._c(o))
    __radd__ = __add__
    def __sub__(self, o): return NFE(self.F, self.p - self._c(o))
    def __rsub__(self, o): return NFE(self.F, self._c(o) - self.p)
    def __mul__(self, o): return NFE(self.F, (self.p * self._c(o)) % self.F.g)
    __rmul__ = __mul__
    def __truediv__(self, o):
        q = self._c(o)
        if q.degree() <= 0:
            assert not q.is_zero(); return NFE(self.F, self.p * (fmpq(1) / q[0]))
        return NFE(self.F, (self.p * self.F.inv(q)) % self.F.g)
    def __rtruediv__(self, o): return NFE(self.F, (self._c(o) * self.F.inv(self.p)) % self.F.g)
    def __neg__(self): return NFE(self.F, -self.p)
    def __bool__(self): return not self.p.is_zero()
    def __eq__(self, o): return (self.p - self._c(o)).is_zero()
    def __ne__(self, o): return not self.__eq__(o)
    def __hash__(self): return hash(tuple(str(c) for c in self.p.coeffs()))
    def to_list(self): return [str(c) for c in reversed(self.p.coeffs())] or ["0"]


class NF:
    """Q(eta) = Q[x]/(g), eta the real root of g nearest the given decimal value (certified isolated by Arb)."""
    def __init__(self, coeffs, eta):
        self.g = fmpq_poly([fmpq(*map(int, c.split("/"))) if "/" in c else fmpq(int(c)) for c in coeffs])
        assert self.g.degree() == len(coeffs) - 1
        self.eta_str = eta
        self.alpha = mp.mpf(eta)
        self.zero = NFE(self, fmpq_poly([0])); self.one = NFE(self, fmpq_poly([1]))
        self._balls = {}
        self._sign = {}
    def inv(self, q):
        d, s, t = q.xgcd(self.g)
        assert d == 1, "not invertible"
        return s
    def c(self, x): return NFE(self, fmpq_poly([fmpq(x)]))
    def from_coeffs(self, cl):
        return NFE(self, fmpq_poly([fmpq(*map(int, c.split("/"))) if "/" in c else fmpq(int(c)) for c in cl]) % self.g)
    def key(self, a): return tuple(a.to_list())
    def ball(self, prec):
        if prec not in self._balls:
            old = ctx.prec; ctx.prec = prec
            den = self.g.denom()
            gz = fmpz_poly([int(c * den) for c in self.g.coeffs()])
            roots = [r for r, m in gz.complex_roots()]          # certified isolating balls (Arb)
            near = [r for r in roots if abs(float(acb(r).real.mid()) - float(self.alpha)) < 1e-9 and abs(float(acb(r).imag.mid())) < 1e-9]
            assert len(near) == 1, "root not isolated"
            r = acb(near[0])
            # a real polynomial: the conjugate of a root in this ball lies in the mirror-image ball; the balls isolate,
            # so if the ball meets the real line symmetrically (imag midpoint 0) the root is real
            assert r.imag.contains(0) and r.imag.mid() == 0 or r.imag == 0, "root not certified real"
            r = r.real
            assert abs(mp.mpf(r.mid().str(60, radius=False)) - self.alpha) < mp.mpf(10) ** -40, "root differs from eta"
            self._balls[prec] = r
            ctx.prec = old
        return self._balls[prec]
    def val(self, a):
        v = mp.mpf(0)
        for co in reversed(a.p.coeffs()):
            v = v * self.alpha + mp.mpf(int(co.p)) / int(co.q)
        return v
    def sign(self, a):
        if not a: return 0
        k = self.key(a)
        s = self._sign.get(k)
        if s is not None: return s
        for prec in (400, 1600, 6400, 20000):
            old = ctx.prec; ctx.prec = prec
            x = self.ball(prec)
            v = arb_poly([arb(c) for c in a.p.coeffs()])(x)
            ctx.prec = old
            if v > 0: s = 1; break
            if v < 0: s = -1; break
        else:
            raise AssertionError("sign not certified")
        self._sign[k] = s
        return s

# ---------------------------------------------------------------- arrangements on the sphere
def tdot(m, r, q):
    """sign-relevant inner product of the projections of r and q on the plane at right angles to m (times |m|^2)"""
    return dot(r, q) * dot(m, m) - dot(r, m) * dot(q, m)

def ang_sort(F, m, pts):
    """exact counterclockwise order (around the axis m) of the vectors pts (indices into a list), all not parallel to m"""
    if len(pts) <= 1: return list(pts)
    ref = pts[0][1]
    def half(q):
        d = F.sign(dot(m, cross(ref, q)))
        if d > 0: return 0
        if d < 0: return 1
        return 0 if F.sign(tdot(m, ref, q)) > 0 else 1
    H = {i: half(q) for i, q in pts}
    def cmp(a, b):
        if H[a[0]] != H[b[0]]: return H[a[0]] - H[b[0]]
        s = F.sign(dot(m, cross(a[1], b[1])))
        assert s != 0, "two equal directions"
        return -s
    return [i for i, _ in sorted(pts, key=functools.cmp_to_key(cmp))]

def arrangement(F, N, trace=True):
    """Central arrangement of the planes with normals N in R^3, read on the unit sphere."""
    n = len(N)
    if n == 0: return {"planes": 0}
    if n == 1:
        return {"planes": 1, "rank": 1, "sphere_V": 0, "sphere_E": 0, "regions": 2, "region_sides": {}, "simplicial": False}
    pts = {}
    for i in range(n):
        for j in range(i + 1, n):
            c = cross(N[i], N[j])
            assert any(c), "equal planes in an arrangement"
            p = canon(F, c); k = vkey(F, p)
            pts.setdefault(k, [p, set()])[1].update((i, j))
    f0 = len(pts)
    mult = Counter(len(s) for _, s in pts.values())
    if f0 == 1:   # all planes through one line: a pencil (rank 2), 2n wedge regions
        return {"planes": n, "rank": 2, "sphere_V": 2, "sphere_E": 2 * n, "regions": 2 * n, "region_sides": {"2": 2 * n},
                "point_multiplicities": {str(k): v for k, v in sorted(mult.items())}, "simplicial": False}
    f1 = sum(len(s) for _, s in pts.values())
    f2 = 1 - f0 + f1
    out = {"planes": n, "rank": 3, "sphere_V": 2 * f0, "sphere_E": 2 * f1, "regions": 2 * f2,
           "point_multiplicities": {str(k): v for k, v in sorted(mult.items())}, "simplicial": 2 * f1 == 3 * f2}
    if not trace: return out
    # independent count: face tracing with exact angular orders
    verts = []; on = []
    for _, (p, s) in pts.items():
        for v in (p, vneg(p)):
            verts.append(v); on.append(s)
    nbr = {i: set() for i in range(len(verts))}
    for i in range(n):
        ids = [k for k in range(len(verts)) if i in on[k]]
        cyc = ang_sort(F, N[i], [(k, verts[k]) for k in ids])
        assert len(cyc) >= 4
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            nbr[a].add(b); nbr[b].add(a)
    rot = {u: ang_sort(F, verts[u], [(w, verts[w]) for w in nbr[u]]) for u in nbr}
    pos = {u: {w: t for t, w in enumerate(rot[u])} for u in rot}
    seen = set(); sides = Counter()
    for u in rot:
        for w in rot[u]:
            if (u, w) in seen: continue
            a, b, k = u, w, 0
            while (a, b) not in seen:
                seen.add((a, b)); k += 1
                r = rot[b]; c = r[(pos[b][a] - 1) % len(r)]
                a, b = b, c
            sides[k] += 1
    nV, nE, nF = len(verts), sum(len(s) for s in nbr.values()) // 2, sum(sides.values())
    assert nV - nE + nF == 2, "Euler on the sphere"
    assert (nV, nE, nF) == (2 * f0, 2 * f1, 2 * f2), "face tracing disagrees with the formula"
    assert min(sides) >= 3
    out["region_sides"] = {str(k): v for k, v in sorted(sides.items())}
    assert out["simplicial"] == (set(sides) == {3})
    return out

# ---------------------------------------------------------------- the extended analysis of one solid about O = 0
def extend(F, V, faces, r):
    n = len(V)
    vk = {vkey(F, v) for v in V}
    edges = sorted({(min(f["verts"][j], f["verts"][(j + 1) % len(f["verts"])]), max(f["verts"][j], f["verts"][(j + 1) % len(f["verts"])]))
                    for f in faces for j in range(len(f["verts"]))})
    assert n - len(edges) + len(faces) == 2
    def is_mirror(m):
        mm = dot(m, m)
        return all(vkey(F, vsub(v, scal(2 * dot(m, v) / mm, m))) in vk for v in V)
    vac = {}
    for a, b in edges:
        m = canon(F, cross(V[a], V[b])); vac.setdefault(vkey(F, m), m)
    assert len(vac) == r["plates"]
    for a, b in edges:
        assert sum(1 for m in vac.values() if not dot(m, V[a]) and not dot(m, V[b])) == 1, "edge not on exactly one plate"
    res = {}; cnt = Counter()
    for f in faces:
        m = canon(F, f["N"]); k = vkey(F, m); res.setdefault(k, m); cnt[k] += 1
    assert len(res) == r["face_plates"]
    par = sum(1 for i in range(len(faces)) for j in range(i + 1, len(faces)) if not any(cross(faces[i]["N"], faces[j]["N"])))
    assert len(res) == len(faces) - par, "Resonus count != faces - parallel pairs"
    assert max(cnt.values()) <= 2
    # Theorem 1(b) on every edge: the plate of AB is at right angles to the dual edge a_F - a_G
    ef = {}
    for t, f in enumerate(faces):
        p = f["verts"]
        for j in range(len(p)):
            e = (min(p[j], p[(j + 1) % len(p)]), max(p[j], p[(j + 1) % len(p)])); ef.setdefault(e, []).append(t)
    polar = [tuple(x / f["d"] for x in f["N"]) for f in faces]
    for (a, b), (s, t) in ef.items():
        assert vkey(F, canon(F, vsub(polar[s], polar[t]))) == vkey(F, canon(F, cross(V[a], V[b]))), "Theorem 1(b)"
    Rstar = {vkey(F, canon(F, v)) for v in V}                                  # Resonus of the polar
    Vstar = {vkey(F, canon(F, vsub(V[a], V[b]))) for a, b in edges}           # Vacuus of the polar
    mV = {k for k, m in vac.items() if is_mirror(m)}
    mR = {k for k, m in res.items() if is_mirror(m)}
    assert len(mV) == r["plates_on_mirrors"] and len(mR) == r["face_plates_on_mirrors"], "mirror flags disagree"
    both = set(vac) & set(res)
    # which edges and faces make the shared planes
    both_info = []
    for k in both:
        es = [e for e in edges if vkey(F, canon(F, cross(V[e[0]], V[e[1]]))) == k]
        fs = [len(f["verts"]) for f in faces if vkey(F, canon(F, f["N"])) == k]
        both_info.append({"edges": len(es), "faces_parallel": sorted(fs), "mirror": k in mV})
    sheets = Counter()
    for c in r["plate_classes"]: sheets[c["sheet"]] += c["count"]
    t0 = time.time()
    arV = arrangement(F, list(vac.values()))
    arR = arrangement(F, list(res.values()))
    return {"V": n, "E": len(edges), "F": len(faces), "centrally_symmetric": r["centrally_symmetric"], "mirrors": r["mirrors"],
            "vacuus_plates": len(vac), "vacuus_full": sheets["full"], "vacuus_shared": sheets["shared"], "vacuus_single": sheets["single"],
            "vacuus_kind": r["kind"], "vacuus_on_mirrors": len(mV), "vacuus_arr": arV,
            "resonus_planes": len(res), "resonus_two_faces": sum(1 for k in cnt if cnt[k] == 2), "resonus_one_face": sum(1 for k in cnt if cnt[k] == 1),
            "resonus_on_mirrors": len(mR), "resonus_arr": arR,
            "both": len(both), "both_on_mirrors": len(both & mV), "both_info": sorted(both_info, key=str),
            "polar_resonus": len(Rstar), "polar_vacuus": len(Vstar),
            "vacuus_meets_polar_resonus": len(set(vac) & Rstar), "resonus_meets_polar_vacuus": len(set(res) & Vstar),
            "plate_classes": r["plate_classes"], "face_plate_classes": r["face_plate_classes"],
            "_keys": {"vac": sorted(map(str, vac)), "res": sorted(map(str, res)), "Rstar": sorted(map(str, Rstar)), "Vstar": sorted(map(str, Vstar))},
            "arr_secs": round(time.time() - t0, 1)}

# ---------------------------------------------------------------- tasks
CATALAN = {"truncated tetrahedron": "triakis tetrahedron", "cuboctahedron": "rhombic dodecahedron",
           "truncated cube": "triakis octahedron", "truncated octahedron": "tetrakis hexahedron",
           "rhombicuboctahedron": "deltoidal icositetrahedron", "truncated cuboctahedron": "disdyakis dodecahedron",
           "snub cube": "pentagonal icositetrahedron", "icosidodecahedron": "rhombic triacontahedron",
           "truncated icosahedron": "pentakis dodecahedron", "truncated dodecahedron": "triakis icosahedron",
           "rhombicosidodecahedron": "deltoidal hexecontahedron", "truncated icosidodecahedron": "disdyakis triacontahedron",
           "snub dodecahedron": "pentagonal hexecontahedron"}
PLATONIC = ("dodecahedron", "icosahedron", "cube", "tetrahedron", "octahedron")
S = None

def uniform_task(nm):
    F, gen, grp = S[nm]
    if nm == "snub dodecahedron":
        V = None
        for cand in gen:
            Vc = VX.build_set(F, cand)
            try:
                if len(Vc) == 60: VX.analyse("probe", F, Vc, True); V = Vc; break
            except AssertionError:
                pass
    else:
        V = VX.build_set(F, gen)
    rows = []
    r, faces = VX.analyse(nm, F, V, True)
    row = {"name": nm, "family": "Platonic" if nm in PLATONIC else "Archimedean", "group": grp, **extend(F, V, faces, r)}
    D = VX.dual_vertices(F, faces)
    dn = {"cube": "octahedron (polar of the cube)", "octahedron": "cube (polar of the octahedron)", "tetrahedron": "tetrahedron (polar)",
          "dodecahedron": "icosahedron (polar of the dodecahedron)", "icosahedron": "dodecahedron (polar of the icosahedron)"}.get(nm, CATALAN.get(nm))
    r2, faces2 = VX.analyse(dn, F, D, False)
    row2 = {"name": dn, "family": "Catalan" if nm in CATALAN else "Platonic polar", "group": grp, "dual_of": nm, **extend(F, D, faces2, r2)}
    # Theorem 1 across the pair: Resonus(P*) = R*(P), Vacuus(P*) = V*(P), and back
    assert row2["_keys"]["res"] == row["_keys"]["Rstar"] and row2["_keys"]["vac"] == row["_keys"]["Vstar"], "polar link fails"
    assert row["_keys"]["res"] == row2["_keys"]["Rstar"] and row["_keys"]["vac"] == row2["_keys"]["Vstar"], "polar link fails (back)"
    row["dual"] = dn; row2["dual"] = nm
    return [row, row2]

def prism_task(n):
    F, pr, ap = VX.prism_family(n)
    rows = []
    for nm, V0, fam, dn, dfam in ((f"{n}-gonal prism", pr, "prism", f"{n}-gonal bipyramid", "bipyramid"),
                                  (f"{n}-gonal antiprism", ap, "antiprism", f"{n}-gonal trapezohedron", "trapezohedron")):
        V = VX.build_set(F, V0)
        r, faces = VX.analyse(nm, F, V, True)
        row = {"name": nm, "family": fam, "n": n, **extend(F, V, faces, r)}
        D = VX.dual_vertices(F, faces)
        r2, faces2 = VX.analyse(dn, F, D, False)
        row2 = {"name": dn, "family": dfam, "n": n, "dual_of": nm, **extend(F, D, faces2, r2)}
        assert row2["_keys"]["res"] == row["_keys"]["Rstar"] and row2["_keys"]["vac"] == row["_keys"]["Vstar"], "polar link fails"
        row["dual"] = dn; row2["dual"] = nm
        rows += [row, row2]
    return rows

def johnson_solid(nm):
    if nm in JX.BUILT:
        F, V, recipe = JX.BUILT[nm]
        return F, V, recipe
    J = nm.split("_")[0]
    d = J8X[J]
    F = NF(d["poly"], d["eta"])
    V = [tuple(F.from_coeffs(c) for c in v) for v in d["coords"]]
    return F, V, f"exact number field of degree {F.g.degree()} (stage 1: polished, minimal polynomials, PARI compositum, exact checks)"

def johnson_task(nm):
    F, V, recipe = johnson_solid(nm)
    Oc, Ov = JX.centroids(F, V)
    row = {"name": nm, "J": int(nm.split("_")[0][1:]), "family": "Johnson", "recipe": recipe,
           "same_centre": all(not (a - b) for a, b in zip(Oc, Ov))}
    if isinstance(F, NF): row["field_degree"] = F.g.degree(); row["field_poly"] = str(F.g)
    for lab, O in (("corner", Oc), ("volume", Ov)):
        W = [vsub(v, O) for v in V]
        r, faces = VX.analyse(nm, F, W, True, None, check_centre=False)
        row[lab] = extend(F, W, faces, r)
    assert row["corner"]["_keys"]["res"] == row["volume"]["_keys"]["res"], "Resonus depends on the centre?"
    return [row]

def run(task):
    kind, arg = task
    t0 = time.time()
    try:
        rows = {"uniform": uniform_task, "prism": prism_task, "johnson": johnson_task}[kind](arg)
    except Exception as e:
        import traceback
        return {"task": task, "error": repr(e), "tb": traceback.format_exc()}
    return {"task": task, "rows": rows, "secs": round(time.time() - t0, 1)}

J8X = {}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    only = sys.argv[2:]          # optional names (pilot)
    procs = int(os.environ.get("PROCS", "20"))
    tasks = []
    if which in ("all", "uniform"):
        S = VX.uniform_solids()
        tasks += [("uniform", nm) for nm in S]
    if which in ("all", "prisms"):
        tasks += [("prism", n) for n in range(3, 13)]
    if which in ("all", "johnson"):
        os.chdir(VE)
        for m in (3, 4, 5, 6, 8, 10): JX.axial(m)
        JX.prisms_augmented(); JX.gyrobifastigium(); JX.platonic_archimedean_based()
        JX.recognise("J91_BILUNABIROTUNDA", [sp.sqrt(5)], [sp.Integer(1), sp.sqrt(5)])
        JX.recognise("J92_TRIANGULAR_HEBESPHENOROTUNDA", [sp.sqrt(3), sp.sqrt(5)], [sp.Integer(1), sp.sqrt(3), sp.sqrt(5), sp.sqrt(15)])
        os.chdir(_cwd)
        J8X.update(json.load(open(os.path.join(STUDY, "data/j84_90_exact.json"))))
        names = sorted(set(JX.BUILT) | {k for k in JX.REG if k.split("_")[0] in J8X}, key=lambda s: int(s.split("_")[0][1:]))
        assert len(names) == 92, f"{len(names)} Johnson solids"
        tasks += [("johnson", nm) for nm in names]
    if only:
        tasks = [t for t in tasks if str(t[1]) in only or str(t[1]).split("_")[0] in only]
    # biggest first
    heavy = ("snub dodecahedron", "truncated icosidodecahedron", "rhombicosidodecahedron", "truncated icosahedron", "truncated dodecahedron", "snub cube")
    tasks.sort(key=lambda t: (t[1] not in heavy, str(t)))
    print("tasks", len(tasks), flush=True)
    out, bad = [], []
    ctxm = mpr.get_context("fork")
    with ctxm.Pool(procs) as pool:
        for i, res in enumerate(pool.imap_unordered(run, tasks)):
            if "error" in res:
                bad.append(res); print("ERROR", res["task"], res["error"], "\n", res["tb"], flush=True)
            else:
                out += res["rows"]
                for r in res["rows"]:
                    a = r.get("corner", r)
                    print(f"PROGRESS {(i + 1) / len(tasks):.3f} {r['name']}: Vacuus {a['vacuus_plates']} {a['vacuus_kind']} | Resonus {a['resonus_planes']}"
                          f" regions {a['resonus_arr'].get('regions')} simpl {a['resonus_arr'].get('simplicial')} | both {a['both']} ({res['secs']}s)", flush=True)
    tag = which if not only else which + "-pilot"
    json.dump(out, open(os.path.join(STUDY, f"data/catalogue-{tag}.json"), "w"), default=str)
    print("rows", len(out), "errors", len(bad), flush=True)
    if not bad:
        print("FINAL ok", len(out), "rows", flush=True)
