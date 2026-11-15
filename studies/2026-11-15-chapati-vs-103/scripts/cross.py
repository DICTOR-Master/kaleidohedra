"""Run Chapati & Chapati's own enumerator (MIT, their src/) on #103's yantras.
usage: python3 -I cross.py <chapati src dir> <k-research-like root>"""
import sys, json, re
from fractions import Fraction as Fr
import numpy as np
src, root = sys.argv[1], sys.argv[2]
sys.path.insert(0, src)
import huet_build as H, gate1_complete as G1
from geometry import Triangle
from faces import planar_faces, area, simplify
from scipy.optimize import least_squares


def from_bwa(b, w, a):
    # #103 frame: depth d down from top; Chapati frame: y up, y = 1 - d.
    YQ = 1 - b[3]; YJ = 1 - b[7]; YP = 1 - b[6]
    XF = w[1] * (b[3] - a[1]) / (b[1] - a[1])          # t1's leg at depth b3 (point F)
    XA = w[3] * (1 - b[8]) / (1 - b[3])                 # t3's leg at depth b8 (point A)
    return YQ, XF, YP, XA, YJ


def faces_of(params):
    T = [Triangle(a_, b_, w_, a_ > b_, n) for n, a_, b_, w_ in H.triangles(*params)]
    segs = [s for t in T for s in t.segments()]
    faces, V = planar_faces(segs, 1e-6)
    inner = [f for f in faces if area(f, V) > 1e-12]
    return T, inner, V


def sgn(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])


def parity(T, inner, V):
    """containment depth of each face's centroid (#103 Proposition 3 rule)."""
    out = {}
    for f in inner:
        c = V[simplify(f, V)].mean(0)
        k = 0
        for t in T:
            d1, d2, d3 = sgn(t.apex, t.vl, c), sgn(t.vl, t.vr, c), sgn(t.vr, t.apex, c)
            if (d1 > 0 and d2 > 0 and d3 > 0) or (d1 < 0 and d2 < 0 and d3 < 0):
                k += 1
        out.setdefault(k, []).append(len(simplify(f, V)))
    return out


def true_corners(f, V, tol=1e-6):
    """corners with a turn angle above tol radians (a vertex where a line only ends on a side is not a corner)."""
    P = V[list(f)]; n = len(P); k = 0
    for i in range(n):
        a, b, c = P[i-1], P[i], P[(i+1) % n]
        u, v = b - a, c - b
        cr = u[0]*v[1] - u[1]*v[0]; dt = u @ v
        if abs(np.arctan2(cr, dt)) > tol: k += 1
    return k


CHECKS = []


def report(name, params):
    res = H.closure(*params)
    T, inner, V = faces_of(params)
    sides = [len(simplify(f, V)) for f in inner]
    par = parity(T, inner, V)
    odd = sum(len(par.get(k, [])) for k in (1, 3, 5, 7, 9))
    oddtri = sum(par.get(k, []).count(3) for k in (1, 3, 5, 7, 9))
    results, assigned, _, _ = G1.enumerate_chambers(*params, verbose=False)
    star = sum(r[2] for r in results)
    tc = [true_corners(f, V) for f in inner]
    oddtc = []
    for f, k in zip(inner, tc):
        c = V[simplify(f, V)].mean(0)
        dep = sum(1 for t in T if (lambda d: all(x > 0 for x in d) or all(x < 0 for x in d))(
            (sgn(t.apex, t.vl, c), sgn(t.vl, t.vr, c), sgn(t.vr, t.apex, c))))
        if dep % 2: oddtc.append(k)
    CHECKS.append((name, abs(res) < 1e-12, odd, len(oddtc), oddtc.count(3), star))
    print(f"  {name}: by true corners (turn > 1e-6 rad): all {len(tc)} faces = tri {tc.count(3)}, quad {tc.count(4)}, other {len(tc)-tc.count(3)-tc.count(4)}; odd regions {len(oddtc)} = tri {oddtc.count(3)}, quad {oddtc.count(4)}", flush=True)
    print(f"{name}: closure {res:.1e}; bounded faces {len(inner)} "
          f"(tri {sides.count(3)}, quad {sides.count(4)}, other {len(sides)-sides.count(3)-sides.count(4)}); "
          f"odd-depth {odd} ({oddtri} triangles) by depth {[len(par.get(k, [])) for k in (1, 3, 5, 7, 9)]}; "
          f"star-point rule {star} {[(r[0], r[1], r[2]) for r in results]}", flush=True)


for nm, (XF, YP, XA, YJ, y0) in {"Huet classical (Gate-1 point YP=0.4627)": (0.126, 0.4627, 0.187, 0.398, 0.6677),
                                "Huet classical (YP=0.463)": (0.126, 0.463, 0.187, 0.398, 0.668)}.items():
    YQ = least_squares(lambda p: [H.closure(p[0], XF, YP, XA, YJ)], [y0], xtol=1e-15, ftol=1e-15).x[0]
    report(nm + f" YQ={YQ:.12f}", (YQ, XF, YP, XA, YJ))

st = root + "/studies/2026-11-08-sri-yantra/"
g = json.load(open(st + "figures/golden_family.json"))["GF1"]
fl = lambda z: float(Fr(z["a"])) if isinstance(z, dict) else float(z)
b = {int(k): fl(v) for k, v in g["b"].items()}; w = {int(k): fl(v) for k, v in g["w"].items()}
a = {int(k): fl(v) for k, v in g["apex"].items()}
p = from_bwa(b, w, a)
P, Ln, D = H.build(*p)
print("GF1 mapping check: |YL-(1-b9)|=%.1e |YV-(1-b1)|=%.1e |YG-(1-b2)|=%.1e" % (
    abs(D['YL']-(1-b[9])), abs(D['YV']-(1-b[1])), abs(D['YG']-(1-b[2]))))
report("DICTO Yantra GF1", p)

txt = open(st + "data/kulaichev-numeric-data.txt").read()
bk = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"b(\d) = ([0-9.]+)", txt)}
wk = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"w(\d) = ([0-9.]+)", txt)}
ak = {8: bk[1], 6: bk[2], 9: bk[3], 1: bk[6], 5: bk[7], 4: bk[8], 2: bk[9], 3: 1.0, 7: 0.0}
p = from_bwa(bk, wk, ak)
P, Ln, D = H.build(*p)
print("KRP mapping check: |YL-(1-b9)|=%.1e |YV-(1-b1)|=%.1e" % (abs(D['YL']-(1-bk[9])), abs(D['YV']-(1-bk[1]))))
report("Kulaichev-Rao-Pustynski", p)
ok = (len(CHECKS) == 4 and all(c[1] for c in CHECKS)
      and [c[2] for c in CHECKS] == [43, 43, 43, 45] and [c[4] for c in CHECKS] == [43, 43, 43, 41]
      and all(c[5] == 43 for c in CHECKS)
      and abs(D['YL'] - (1 - bk[9])) < 1e-12)
print("FINAL ok" if ok else f"FINAL FAIL {CHECKS}")
