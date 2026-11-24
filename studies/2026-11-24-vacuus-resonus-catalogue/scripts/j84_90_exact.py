#!/usr/bin/env python3
"""J84-J90: high-precision coordinates and their algebraic degrees (exploration step).

From the registry floats (vacuus-enumeration data/johnson-float-source.json) the solid is polished by
Gauss-Newton at high precision on its defining equations: every edge of length 1 and, for every square,
both diagonals of length sqrt 2 (an equilateral 4-cycle with equal diagonals sqrt 2 is a planar square).
It is then put in its symmetry frame (corner centroid at O; x = a mirror normal, z = the axis where two
mirrors meet, y = z x x). Each coordinate is then an algebraic number; PARI's algdep finds its degree.
Run with the 'alg' venv (cypari2, mpmath, numpy, scipy).
"""
import sys, json, os, time
import numpy as np
import mpmath as mp
from scipy.spatial import ConvexHull
import cypari2
pari = cypari2.Pari(); pari.allocatemem(4 * 10**9)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "../../2026-11-24-vacuus-enumeration/data/johnson-float-source.json")
NAMES = {"J84": "D12", "J85": "J85_SNUB_SQUARE_ANTIPRISM", "J86": "J86_SPHENOCORONA", "J87": "J87_AUGMENTED_SPHENOCORONA",
         "J88": "J88_SPHENOMEGACORONA", "J89": "J89_HEBESPHENOMEGACORONA", "J90": "J90_DISPHENOCINGULUM"}


def float_faces(P):
    h = ConvexHull(P); g = {}
    for s, e in zip(h.simplices, h.equations):
        g.setdefault(tuple(np.round(e, 6)), set()).update(int(i) for i in s)
    out = []
    for idx in g.values():
        idx = sorted(idx); cf = P[idx].mean(0)
        nf = np.cross(P[idx[1]] - P[idx[0]], P[idx[2]] - P[idx[0]]); nf /= np.linalg.norm(nf)
        u = P[idx[0]] - cf; u /= np.linalg.norm(u); w = np.cross(nf, u)
        out.append([i for _, i in sorted(zip([np.arctan2((P[i]-cf) @ w, (P[i]-cf) @ u) for i in idx], idx))])
    return out


def polish(P, faces, dps):
    """Gauss-Newton at dps digits; gauge: v0 fixed, v1 on a line, v2 in a plane (6 coordinates pinned)."""
    mp.mp.dps = dps + 30
    n = len(P)
    edges = sorted({(min(f[j], f[(j+1) % len(f)]), max(f[j], f[(j+1) % len(f)])) for f in faces for j in range(len(f))})
    sq = [f for f in faces if len(f) == 4]
    assert all(len(f) in (3, 4) for f in faces)
    # gauge frame: v0 at 0, v1 on +x, v2 in the xy-plane
    P = P - P[0]
    e1 = P[1] / np.linalg.norm(P[1]); t = P[2] - (P[2] @ e1) * e1; e2 = t / np.linalg.norm(t); e3 = np.cross(e1, e2)
    P = P @ np.array([e1, e2, e3]).T
    L = np.mean([np.linalg.norm(P[a] - P[b]) for a, b in edges]); P = P / L
    X = [[mp.mpf(float(x)) for x in v] for v in P]
    free = [(i, k) for i in range(n) for k in range(3) if not (i == 0 or (i == 1 and k > 0) or (i == 2 and k == 2))]
    for (i, k) in [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]: X[i][k] = mp.mpf(0)
    eqs = [(a, b, 1) for a, b in edges] + [(f[0], f[2], 2) for f in sq] + [(f[1], f[3], 2) for f in sq]
    col = {ik: c for c, ik in enumerate(free)}
    for it in range(60):
        F = mp.matrix(len(eqs), 1); J = mp.matrix(len(eqs), len(free))
        for r, (a, b, L2) in enumerate(eqs):
            d = [X[a][k] - X[b][k] for k in range(3)]
            F[r] = sum(x * x for x in d) - L2
            for k in range(3):
                if (a, k) in col: J[r, col[(a, k)]] += 2 * d[k]
                if (b, k) in col: J[r, col[(b, k)]] -= 2 * d[k]
        res = max(abs(x) for x in F)
        if res < mp.mpf(10) ** (-dps - 10): break
        JT = J.T
        dx = mp.lu_solve(JT * J, -(JT * F))
        for (i, k), c in col.items(): X[i][k] += dx[c]
    assert res < mp.mpf(10) ** (-dps), f"no convergence {res}"
    return X, edges, it


def frame(X, dps):
    n = len(X)
    c = [sum(v[k] for v in X) / n for k in range(3)]
    V = [[v[k] - c[k] for k in range(3)] for v in X]
    tol = mp.mpf(10) ** (-dps // 2)
    def near(p): return min(max(abs(p[k] - q[k]) for k in range(3)) for q in V) < tol
    mir = []
    for i in range(n):
        for j in range(i + 1, n):
            m = [V[i][k] - V[j][k] for k in range(3)]; nm = mp.sqrt(sum(x * x for x in m)); m = [x / nm for x in m]
            if abs(sum(x*x for x in V[i]) - sum(x*x for x in V[j])) > tol: continue
            if any(abs(abs(sum(a * b for a, b in zip(m, q))) - 1) < tol for q in mir): continue
            if all(near([p[k] - 2 * sum(a * b for a, b in zip(p, m)) * m[k] for k in range(3)]) for p in V): mir.append(m)
    return V, mir


def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]



def to_pari(x, dps): return pari(mp.nstr(x, dps))


def find_poly(px, D, dps):
    """algdep of degree exactly D at a working precision suited to D, then accepted only with a tiny residual
    at full precision, an irreducible result, and coefficients far smaller than the precision."""
    lo = min(dps, 40 * (D + 1) + 120)
    p = pari.algdep(pari.precision(px, lo), D)
    if pari.poldegree(p) != D or not pari.polisirreducible(p): return None
    if abs(pari.subst(p, 'x', px)) > pari(f"1e-{dps - 100}"): return None
    h = max(abs(c) for c in pari.Vec(p))
    if (D + 1) * len(str(h)) > dps * 0.6: return None
    return p


def degree_of(px, dps, Dmax=128, cands=None):
    for D in (cands or range(1, Dmax + 1)):
        p = find_poly(px, D, dps)
        if p is not None: return D, p
    return None, None


def in_field(px, th, d, dps):
    """px as a rational polynomial in th of degree < d (lindep), or None."""
    vec = pari(f"[{0}]")
    vec = pari.concat(pari.Vec([px]), pari.Vec([th ** k for k in range(d)]))
    rel = pari.lindep(vec)
    if rel[0] == 0: return None
    poly = sum(-rel[k + 1] / rel[0] * pari(f"y^{k}") for k in range(d))
    if abs(pari.subst(poly, 'y', th) - px) > pari(f"1e-{dps - 100}"): return None
    hmax = max(len(str(c)) for c in pari.Vec(rel))
    if d * hmax > dps * 0.6: return None
    return poly


def exact_coords(W, dps):
    """Common number field of all coordinates, built exactly: each coordinate value u gets its minimal polynomial
    h (PARI algdep, low degree), and the field Q(theta) is joined with Q(u) by PARI polcompositum; the numerical
    values only choose which factor of the compositum (which embedding) is the real solid."""
    pari.set_real_precision(dps)
    tol = pari(f"1e-{dps // 2}")
    vals = []
    for v in W:
        for x in v:
            if abs(x) > mp.mpf(10) ** (-dps // 2) and not any(abs(abs(x) - u) < mp.mpf(10) ** (-dps // 2) for u in vals): vals.append(abs(x))
    f = pari("x"); th = pari(0); known = []          # known: list of (numeric value, Mod(poly, f))
    dl = []
    for u in vals:
        pu = to_pari(u, dps); t0 = time.time()
        du, h = degree_of(pu, dps, Dmax=96)
        assert du, "no polynomial for a coordinate"
        dl.append((du, u, pu, h, time.time() - t0))
    dl.sort(key=lambda t: -t[0])                  # the value of highest degree first: often it generates the field
    print("   coordinate degrees", [t[0] for t in dl], flush=True)
    for du, u, pu, h, tdeg in dl:
        t0 = time.time() - tdeg; t1 = time.time()
        if pari.poldegree(f) > 1 and du > 1:      # already in Q(theta)?  first a linear relation (lindep), then exact factoring
            lin = in_field(pu, th, pari.poldegree(f), dps)
            if lin is not None and pari.subst(h, 'x', pari.Mod(pari.subst(lin, 'y', 'x'), f)) == 0:
                known.append((pu, pari.Mod(pari.subst(lin, 'y', 'x'), f)))
                print(f"   value {mp.nstr(u, 8)}: degree {du}, in the field (linear relation, exact check of its polynomial) ({time.time()-t1:.1f}s)", flush=True)
                continue
        if pari.poldegree(f) > 1 and du > 1 and pari.poldegree(f) * du <= 64:
            fy = pari.subst(f, 'x', 'y')
            fac = pari.nffactor(fy, h)[0]
            mem = None
            for q in fac:
                if pari.poldegree(q, 'x') == 1:
                    r = -pari.polcoef(q, 0, 'x') / pari.polcoef(q, 1, 'x')        # a Mod(poly(y), f(y))
                    if abs(pari.subst(pari.lift(r), 'y', th) - pu) < tol: mem = r; break
            if mem is not None:
                known.append((pu, pari.Mod(pari.subst(pari.lift(mem), 'y', 'x'), f)))
                print(f"   value {mp.nstr(u, 8)}: degree {du} ({t1-t0:.1f}s), in the field ({time.time()-t1:.1f}s)", flush=True)
                continue
        comps = pari.polcompositum(f, h, 1)
        hit = None
        for c in comps:
            R, a, bb, k = c[0], c[1], c[2], c[3]
            rho = pu + k * th          # PARI: the root of R is b + k a
            if abs(pari.subst(R, 'x', rho)) < tol * (1 + abs(rho)) ** pari.poldegree(R) * 10 ** 10:
                if abs(pari.subst(pari.lift(a), 'x', rho) - th) < tol and abs(pari.subst(pari.lift(bb), 'x', rho) - pu) < tol:
                    hit = (R, a, bb, rho); break
        assert hit, "no compositum factor matches"
        R, a, bb, rho = hit
        known = [(val, pari.Mod(pari.subst(pari.lift(m), 'x', pari.lift(a)), R)) for val, m in known]
        known.append((pu, pari.Mod(pari.lift(bb), R)))
        if pari.poldegree(R) != pari.poldegree(f): print(f"   value {mp.nstr(u, 8)}: degree {du} ({t1-t0:.1f}s); field degree now", pari.poldegree(R), f"({time.time()-t1:.1f}s)", flush=True)
        f, th = R, rho
    # a smaller defining polynomial (PARI polredbest), and the new root eta
    red = pari.polredbest(f, 1); g = red[0]; a = red[1]          # theta = a(eta) mod g
    b = pari.modreverse(a)                                       # eta = b(theta) mod f
    eta = pari.subst(pari.lift(b), 'x', th)
    assert abs(pari.subst(pari.lift(a), 'x', eta) - th) < tol
    known = [(val, pari.Mod(pari.subst(pari.lift(m), 'x', pari.lift(a)), g)) for val, m in known]
    for val, m in known:
        assert abs(pari.subst(pari.lift(m), 'x', eta) - val) < tol, "coordinate value lost"
    coords = []
    for v in W:
        row = []
        for x in v:
            if abs(x) <= mp.mpf(10) ** (-dps // 2): row.append(pari.Mod(0, g)); continue
            px = to_pari(x, dps)
            m = next(mm for val, mm in known if abs(val - abs(px)) < tol)
            row.append(m if px > 0 else -m)
        coords.append(row)
    return g, eta, coords


def exact_checks(coords, edges, faces):
    """Exact in Q(eta): every edge has length 1; every square has both diagonals of squared length 2 and is planar."""
    def d2(a, b): return sum((coords[a][k] - coords[b][k]) ** 2 for k in range(3))
    assert all(d2(a, b) == 1 for a, b in edges), "edge length"
    for f in faces:
        if len(f) == 4:
            assert d2(f[0], f[2]) == 2 and d2(f[1], f[3]) == 2, "square diagonals"
            u = [coords[f[1]][k] - coords[f[0]][k] for k in range(3)]; v = [coords[f[2]][k] - coords[f[0]][k] for k in range(3)]
            w = [coords[f[3]][k] - coords[f[0]][k] for k in range(3)]
            det = u[0]*(v[1]*w[2]-v[2]*w[1]) - u[1]*(v[0]*w[2]-v[2]*w[0]) + u[2]*(v[0]*w[1]-v[1]*w[0])
            assert det == 0, "square not planar"
    return True


if __name__ == "__main__":
    which = sys.argv[1:] or list(NAMES)
    dps = int(os.environ.get("DPS", "3000"))
    reg = json.load(open(SRC))
    out = {}
    for J in which:
        P = np.array(reg[NAMES[J]]["vertices"], float)
        faces = float_faces(P)
        X, edges, it = polish(P, faces, dps)
        n = len(X)
        if J == "J87":   # one mirror only: use the frame of the sphenocorona left when the pyramid apex is removed
            for apex in range(n):
                rest = [X[i] for i in range(n) if i != apex]
                Vr, mir = frame(rest, dps)
                if len(mir) == 2: break
            c = [sum(v[k] for v in rest) / len(rest) for k in range(3)]
            V = [[X[i][k] - c[k] for k in range(3)] for i in range(n)]
            _, mall = frame(X, dps)
            print(J, "apex", apex, "mirrors of J87", len(mall), flush=True)
        else:
            V, mir = frame(X, dps)
        print(J, "V", n, "E", len(edges), "F", len(faces), "Newton its", it, "mirrors", len(mir), flush=True)
        e1 = mir[0]; e3 = cross(mir[0], mir[1]); nn = mp.sqrt(sum(x*x for x in e3)); e3 = [x / nn for x in e3]; e2 = cross(e3, e1)
        W = [[sum(a * b for a, b in zip(v, e)) for e in (e1, e2, e3)] for v in V]
        if J in ("J86", "J87", "J88", "J89"):
            # symmetry C2v (Cs for J87): no point is fixed, and the corner centroid mixes all coordinates (high degree);
            # put the origin on the axis at the level of the most populous ring of corners instead
            lv = []
            for v in W:
                for L in lv:
                    if abs(L[0] - v[2]) < mp.mpf(10) ** (-dps // 2): L[1] += 1; break
                else: lv.append([v[2], 1])
            z0 = max(lv, key=lambda L: (L[1], -abs(L[0])))[0]
            W = [[v[0], v[1], v[2] - z0] for v in W]
        g, eta, coords = exact_coords(W, dps)
        exact_checks(coords, edges, faces)
        print(J, "field degree", pari.poldegree(g), "polynomial", str(g)[:200], "eta", mp.nstr(mp.mpf(str(pari.real(eta))), 30) if False else str(eta)[:40], flush=True)
        print(J, "exact checks passed: edges 1, squares (diagonals, planarity)", flush=True)
        out[J] = {"poly": [str(c) for c in pari.Vecrev(g)], "eta": str(pari.precision(eta, 200)),
                  "coords": [[[str(c) for c in pari.Vecrev(pari.lift(x))] if x != 0 else ["0"] for x in v] for v in coords],
                  "edges": edges, "faces": faces}
        json.dump(out, open(os.path.join(HERE, f"../data/j84_90_exact_{'_'.join(which)}.json"), "w"))
    print("FINAL ok", len(out), "solids exact", flush=True)
