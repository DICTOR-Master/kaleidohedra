"""B1: shadows of skeletons (edges + Vacuus struts, i.e. the segments from the centre O to every corner), exact.

3D skeletons (data/skeletons.json): 5 Platonic, 13 Archimedean (the truncated icosidodecahedron is the H3 permutahedron, the
hub), the four Kepler-Poinsot stars (30 true edges), the Dogstar and the Sunstar (visible-surface edges).
Directions:
- symmetry-adapted: the directions of the corners, edge midpoints and face centres of the polyhedron itself (Platonic and
  Archimedean; these contain every rotation axis, and the 3D Coxeter planes are the planes at right angles to the 5-, 3- and
  4/2-fold axes); for the stellation-cycle polyhedra the 31 axes of the icosahedral frame (corners, edge midpoints and face
  centres of I0). Directions giving identical exact signatures (sorted squared cosines with all corners) are run once.
- dense certified scan: every primitive integer direction (a, b, c) with max(|a|, |b|, |c|) <= NSCAN, one per +- pair.
4D: the 600-cell and the 120-cell (exact in Q(sqrt5); the 120-cell's corners are the 600 cell centres of the 600-cell,
its edges join cells sharing a triangle), edges + struts, projected orthographically onto
- the H4 Coxeter plane (field Q(2cos(2pi/30)), plane computed as in study 2026-11-25-plate-harmony, four_d.py);
- the planes at right angles to span(a, b): a = a 600-cell corner (vertex-first to 3D), b = a 5-, 3- or 2-fold axis of the
  icosahedral 3D image; a = a 600-cell cell centre (cell-first), b = a 3- or 2-fold axis of the tetrahedral 3D image.
  (Projecting to 3D along a and then to 2D along b is the orthographic projection onto span(a, b)^perp.)
Each shadow: marmas (points interior to three or more drawn lines, the projected centre excluded), their multiplicities,
mixed points, lines through the projected centre, the largest parallel class, and the combinatorial Sri Yantra test.
Writes data/shadows.json."""
import os, sys, json, time, itertools, math
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "../../2026-11-25-plate-harmony/scripts")))
from nf import NF, cheb_C
from flint import fmpz_poly
from shadow_core import Shadow, fl
import multiprocessing as mpr

NSCAN = int(os.environ.get("NSCAN", "4"))
T0 = time.time()
_F = {}


def field(fd):
    k = (tuple(fd["g"]), fd["eta"][:40])
    if k not in _F: _F[k] = NF(fd["g"], fd["eta"])
    return _F[k]


def dot(u, v):
    s = u[0] * v[0]
    for a, b in zip(u[1:], v[1:]): s = s + a * b
    return s


def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def load(row):
    F = field(row["field"])
    V = [tuple(F.from_coeffs(c) for c in v) for v in row["V"]]
    pts = list(V); key = {tuple(x.key() for x in v): i for i, v in enumerate(V)}
    O = (F.zero,) * 3
    if tuple(x.key() for x in O) not in key:
        key[tuple(x.key() for x in O)] = len(pts); pts.append(O)
    oi = key[tuple(x.key() for x in O)]
    segs = []
    if "E" in row:
        segs = [tuple(e) for e in row["E"]]
    else:
        for a, b in row["segments"]:
            ia = [tuple(F.from_coeffs(c) for c in a), tuple(F.from_coeffs(c) for c in b)]
            idx = []
            for p in ia:
                k = tuple(x.key() for x in p)
                if k not in key: key[k] = len(pts); pts.append(p)
                idx.append(key[k])
            segs.append(tuple(idx))
    nedge = len(segs)
    segs += [(oi, i) for i in range(len(V)) if i != oi]
    return F, V, pts, segs, oi, nedge


def basis3(F, d):
    e = min(range(3), key=lambda i: abs(fl(d[i])))
    ei = tuple(F.one if j == e else F.zero for j in range(3))
    w1 = cross(d, ei); w2 = cross(d, w1)
    return w1, w2


def shadow_of(pts, segs, oi, w1, w2):
    P = [(dot(w1, p), dot(w2, p)) for p in pts]
    S = Shadow(P, segs, oi)
    S.run()
    return S.summary()


def sym_dirs(row, F, V):
    if row["family"] in ("Platonic", "Archimedean"):
        out = [("corner", v) for v in V]
        out += [("edge midpoint", tuple(a + b for a, b in zip(V[i], V[j]))) for i, j in row["E"]]
        for f in row["faces"]:
            out.append((f"centre of {len(f)}-gon", tuple(sum((V[i][k] for i in f), F.zero) for k in range(3))))
        return out
    s5 = F.gen(); phi = (s5 + 1) / 2; o = F.one; z = F.zero
    I0 = []
    for a, b in itertools.product((phi, -phi), (o, -o)):
        base = (z, a, b)
        for r in range(3): I0.append(tuple(base[(k - r) % 3] for k in range(3)))
    e2 = min(fl(dot(tuple(x - y for x, y in zip(I0[0], v)), tuple(x - y for x, y in zip(I0[0], v)))) for v in I0[1:])
    adj = lambda a, b: abs(fl(dot(tuple(x - y for x, y in zip(a, b)), tuple(x - y for x, y in zip(a, b)))) - e2) < 1e-9
    out = [("5-fold axis", v) for v in I0]
    out += [("2-fold axis", tuple(x + y for x, y in zip(a, b))) for a, b in itertools.combinations(I0, 2) if adj(a, b)]
    out += [("3-fold axis", tuple(x + y + w for x, y, w in zip(a, b, c))) for a, b, c in itertools.combinations(I0, 3) if adj(a, b) and adj(b, c) and adj(a, c)]
    return out


def signature(V, d):
    dd = dot(d, d)
    return tuple(sorted(((dot(v, d) * dot(v, d)) / dd).key() for v in V))


def task3(args):
    ri, kind, label, dco = args
    row = ROWS[ri]
    F, V, pts, segs, oi, nedge = load(row)
    d = tuple(F.from_coeffs(c) if isinstance(c, list) else F.c(c) for c in dco)
    w1, w2 = basis3(F, d)
    t = time.time()
    s = shadow_of(pts, segs, oi, w1, w2)
    s.update({"polyhedron": row["name"], "kind": kind, "direction": label, "secs": round(time.time() - t, 2)})
    return s


def prepare3():
    tasks = []
    meta = []
    for ri, row in enumerate(ROWS):
        F, V, pts, segs, oi, nedge = load(row)
        meta.append({"polyhedron": row["name"], "family": row["family"], "corners": len(V), "edges": nedge, "struts": len(segs) - nedge})
        seen = {}
        for lab, d in sym_dirs(row, F, V):
            if all(not x for x in d): continue
            sg = signature(V, d)
            if sg in seen: continue
            seen[sg] = lab
            tasks.append((ri, "symmetric", lab, [[str(c) for c in x.p.coeffs()] or ["0"] for x in d]))
        meta[-1]["symmetric_directions"] = len(seen)
        ns = 0
        for a, b, c in itertools.product(range(-NSCAN, NSCAN + 1), repeat=3):
            if (a, b, c) == (0, 0, 0) or math.gcd(math.gcd(abs(a), abs(b)), abs(c)) != 1: continue
            if (a, b, c) < (-a, -b, -c): continue
            tasks.append((ri, "scan", f"({a},{b},{c})", [str(a), str(b), str(c)])); ns += 1
        meta[-1]["scan_directions"] = ns
    return tasks, meta


# ---------------------------------------------------------------- 4D
def z5(F, x): s5 = F.gen(); return F.c(x[0]) + (s5 + 1) / 2 * x[1]


def cells4(F):
    import importlib.util
    spec = importlib.util.spec_from_file_location("four_d", os.path.normpath(os.path.join(HERE, "../../2026-11-25-plate-harmony/scripts/four_d.py")))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    V = m.cell600()
    adj = {i: [j for j in range(120) if j != i and m.dotz(V[i], V[j]) == (0, 2)] for i in range(120)}
    E6 = sorted({tuple(sorted((i, j))) for i in adj for j in adj[i]})
    tets = set()
    for i in range(120):
        for j, k, l in itertools.combinations(adj[i], 3):
            if k in adj[j] and l in adj[j] and l in adj[k]: tets.add(tuple(sorted((i, j, k, l))))
    tets = sorted(tets)
    assert len(E6) == 720 and len(tets) == 600
    tri = {}
    for ti, t in enumerate(tets):
        for f in itertools.combinations(t, 3): tri.setdefault(f, []).append(ti)
    E12 = sorted({tuple(sorted(v)) for v in tri.values()})
    assert len(E12) == 1200 and all(len(v) == 2 for v in tri.values())
    return m, V, E6, tets, E12


def task4(args):
    poly, plane = args
    t = time.time()
    if plane == "Coxeter plane (H4)":
        K, pts, segs, oi, p1, p2 = COX[poly]
        s = shadow_of(pts, segs, oi, p1, p2)
    else:
        F, pts, segs, oi, planes = FOUR[poly]
        w1, w2 = planes[plane]
        s = shadow_of(pts, segs, oi, w1, w2)
    s.update({"polyhedron": poly, "kind": "4D", "direction": plane, "secs": round(time.time() - t, 2)})
    return s


def kernel_basis(F, rows, dim=4):
    """basis of the vectors at right angles to all rows (exact Gaussian elimination)"""
    A = [list(r) for r in rows]; piv = []; r = 0
    for c in range(dim):
        p = next((i for i in range(r, len(A)) if A[i][c]), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]; iv = A[r][c].inv(); A[r] = [x * iv for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                f = A[i][c]; A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv.append(c); r += 1
    out = []
    for fc in [c for c in range(dim) if c not in piv]:
        v = [F.zero] * dim; v[fc] = F.one
        for i, pc in enumerate(piv): v[pc] = -A[i][fc]
        out.append(tuple(v))
    return out


def prepare4():
    F = NF([-5, 0, 1], "2.2360679774997896964091736687312762354406183596115")
    m, Vz, E6, tets, E12 = cells4(F)
    V6 = [tuple(z5(F, x) for x in v) for v in Vz]
    C12 = [tuple(sum((V6[i][k] for i in t), F.zero) for k in range(4)) for t in tets]
    O = (F.zero,) * 4
    polys = {"600-cell": (V6 + [O], E6 + [(120, i) for i in range(120)], 120),
             "120-cell": (C12 + [O], E12 + [(600, i) for i in range(600)], 600)}
    # planes: span(a, b)^perp
    a = V6[0]
    nb = [v for v in V6 if v != a and abs(fl(dot(v, a)) - fl(dot(a, a)) * (1 + 5 ** .5) / 4) < 1e-9]
    assert len(nb) == 12
    perp = lambda v, a: tuple(x - (dot(v, a) / dot(a, a)) * y for x, y in zip(v, a))
    ico = [perp(v, a) for v in nb]
    d2 = sorted({round(fl(dot(tuple(x - y for x, y in zip(ico[0], v)), tuple(x - y for x, y in zip(ico[0], v)))), 9) for v in ico[1:]})
    e2 = d2[0]
    adj = lambda p, q: abs(fl(dot(tuple(x - y for x, y in zip(p, q)), tuple(x - y for x, y in zip(p, q)))) - e2) < 1e-9
    i5 = ico[0]
    i2 = next(tuple(x + y for x, y in zip(ico[0], q)) for q in ico[1:] if adj(ico[0], q))
    i3 = next(tuple(x + y + w for x, y, w in zip(ico[0], q, r)) for q, r in itertools.combinations(ico[1:], 2) if adj(ico[0], q) and adj(ico[0], r) and adj(q, r))
    c = C12[0]; cv = [V6[i] for i in tets[0]]
    tet = [perp(v, c) for v in cv]
    c3 = tet[0]; c2 = tuple(x + y for x, y in zip(tet[0], tet[1]))
    planes = {}
    for lab, (u, w) in {"vertex-first, then 5-fold axis": (a, i5), "vertex-first, then 3-fold axis": (a, i3), "vertex-first, then 2-fold axis": (a, i2),
                        "cell-first, then 3-fold axis": (c, c3), "cell-first, then 2-fold axis": (c, c2)}.items():
        kb = kernel_basis(F, [u, w]); assert len(kb) == 2
        planes[lab] = kb
    four = {}
    for nm, (pts, segs, oi) in polys.items(): four[nm] = (F, pts, segs, oi, planes)
    # Coxeter plane, field K = Q(2cos(2pi/30)) (as four_d.py of the plate-harmony study)
    K = NF([int(cc) for cc in fmpz_poly.cos_minpoly(30).coeffs()], "1.9562952014676112738")
    x = K.gen(); s5 = cheb_C(6, x, K.one) * 2 + 1
    assert s5 * s5 == 5 and s5.sign() > 0
    ph = (s5 + 1) / 2
    toK = lambda zz: K.c(zz[0]) + ph * zz[1]
    roots = [list(v) for v in Vz]
    w = [(1, 0), (3, 0), (7, 0), (19, 0)]
    pos = [r for r in roots if m.sgn(m.dotz(r, w)) > 0]
    pk = {tuple(r) for r in pos}
    simple = []
    for r in pos:
        okk = True
        for xx in pos:
            if tuple(xx) == tuple(r): continue
            dd = m.dotz(xx, r)
            y = [m.sb(xx[t], (lambda hh: (hh[0] // 2, hh[1] // 2))(m.m(dd, r[t]))) for t in range(4)]
            if tuple(y) not in pk: okk = False; break
        if okk: simple.append(r)
    assert len(simple) == 4
    I = [[K.one if i == j else K.zero for j in range(4)] for i in range(4)]
    def refm(r):
        rk = [toK(t) for t in r]
        return [[I[i][j] - rk[i] * rk[j] / 2 for j in range(4)] for i in range(4)]
    def mul(A, B): return [[sum((A[i][k] * B[k][j] for k in range(4)), K.zero) for j in range(4)] for i in range(4)]
    Cm = refm(simple[0])
    for r in simple[1:]: Cm = mul(Cm, refm(r))
    C2 = mul(Cm, Cm)
    M = [[C2[i][j] - x * Cm[i][j] + I[i][j] for j in range(4)] for i in range(4)]
    kb = kernel_basis(K, [tuple(rw) for rw in M]); assert len(kb) == 2
    p1, p2 = kb
    # check: the plane is invariant under the Coxeter element
    for p in (p1, p2):
        cp = tuple(sum((Cm[i][j] * p[j] for j in range(4)), K.zero) for i in range(4))
        rows = [p1, p2, cp]
        assert len(kernel_basis(K, rows)) == 2, "Coxeter plane not invariant"
    cox = {}
    for nm, (pts, segs, oi) in polys.items():
        def toKel(cc):
            co = cc.p.coeffs()
            if not co: return K.zero
            return K.c(co[0]) + (s5 * co[1] if len(co) > 1 else K.zero)
        ptsK = [tuple(toKel(cc) for cc in p) for p in pts]
        cox[nm] = (K, ptsK, segs, oi, p1, p2)
    return four, cox, planes


def run_any(x): return task4(x[1]) if x[0] == "4" else task3(x[1])


if __name__ == "__main__":
    procs = int(os.environ.get("PROCS", "3"))
    ROWS = json.load(open(os.path.join(STUDY, "data/skeletons.json")))
    only = os.environ.get("ONLY")
    if only: ROWS = [r for r in ROWS if r["name"] in only.split(",")]
    if os.environ.get("SCANOFF"): NSCAN = 0
    tasks3, meta = prepare3()
    print(f"[{time.time() - T0:.0f} s] 3D tasks {len(tasks3)}", flush=True)
    do4 = os.environ.get("NO4D") is None
    if do4:
        FOUR, COX, PL = prepare4()
        tasks4 = [(nm, pl) for nm in ("120-cell", "600-cell") for pl in ["Coxeter plane (H4)"] + list(PL)]
        if os.environ.get("FOURONLY"): tasks4 = [t for t in tasks4 if t[0] in os.environ["FOURONLY"].split(",")]
        print(f"[{time.time() - T0:.0f} s] 4D tasks {len(tasks4)}", flush=True)
    else:
        tasks4 = []
    res = []
    with mpr.get_context("fork").Pool(procs) as pool:
        allt = [("4", t) for t in tasks4] + [("3", t) for t in sorted(tasks3, key=lambda t: -len(ROWS[t[0]]["V"]))]
        for i, s in enumerate(pool.imap_unordered(run_any, allt)):
            res.append(s)
            if s["kind"] != "scan" or s["marmas"]:
                print(f"PROGRESS {(i + 1) / len(allt):.3f} {s['polyhedron']} | {s['direction']} | marmas {s['marmas']} {s['marma_hist']} "
                      f"mixed {s['mixed_points']} centre {s['centre_lines']} par {s['max_parallel']} yantra {s['yantra_test']['pass']} ({s['secs']} s)", flush=True)
            elif i % 200 == 0:
                print(f"PROGRESS {(i + 1) / len(allt):.3f} scan", flush=True)
    out = {"meta": meta, "nscan": NSCAN, "shadows": res}
    json.dump(out, open(os.path.join(STUDY, "data/shadows.json" if not only else "data/shadows-pilot.json"), "w"), default=str)
    yes = [s for s in res if s["yantra_test"]["pass"]]
    print(f"shadows {len(res)}; yantra-test passes {len(yes)}; max marmas {max(s['marmas'] for s in res)}", flush=True)
    if len(res) == len(allt): print("FINAL ok shadows", flush=True)
