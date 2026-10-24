# Relay census, part D (floats, independent of the exact pipeline): at 3 random float parameters inside every exact interval, build
# every power cell with plain numpy/scipy (half-space intersection, Euclidean coordinates from a Cholesky factor of G, facets
# grouped by neighbour) and compare the bond counts by neighbour kind with the exact interval record. Also: the dual cells at the
# two octet-type hinges (Delian lam = -1/8, hcp holes lam = -1/8), exact hull facets of the 14 sites meeting at one corner.
import json, sys
from fractions import Fraction as Fr
from itertools import product, combinations
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import HalfspaceIntersection
from networks import NETS
from engine import Cell, Net
rng = np.random.default_rng(20261025); checks = []
def check(n, ok, det=""):
    checks.append(("PASS" if ok else "FAIL", n, det)); print(("PASS " if ok else "FAIL ") + n + (" " + det if det else ""), flush=True)

def float_cell(spec, i, lam, K=3):
    G = np.array([[float(x) for x in r] for r in spec["G"]]); Lc = np.linalg.cholesky(G).T  # |v|_G = |Lc v|
    T = np.array([[float(x) for x in v] for v in spec["T"]]); mot = [(k, np.array([float(x) for x in c])) for k, c in spec["motif"]]
    w = {k: float(v[0]) + float(v[1]) * lam for k, v in spec["w"].items()}
    ki, ci = mot[i]; ci = Lc @ ci; d = len(G); S = []
    for kv in product(range(-K, K + 1), repeat=d):
        t = np.array(kv) @ T
        for j, (kj, cj) in enumerate(mot):
            c = Lc @ (cj + t)
            if np.linalg.norm(c - ci) < 1e-12 or np.linalg.norm(c - ci) ** 2 > float(spec["D2"]) * 1.5: continue
            S.append((kj, c))
    A = np.array([2 * (c - ci) for _, c in S]); b = np.array([c @ c - ci @ ci + w[ki] - w[kj] for kj, c in S])
    nr = np.linalg.norm(A, axis=1)
    res = linprog(np.r_[np.zeros(d), -1], A_ub=np.c_[A, nr], b_ub=b, bounds=[(None, None)] * d + [(0, None)], method="highs")
    V = HalfspaceIntersection(np.c_[A, -b], res.x[:d]).intersections
    cnt = {}
    for k, (kj, c) in enumerate(S):
        on = V[np.abs(V @ A[k] - b[k]) < 1e-7 * max(1, nr[k])]
        if len(on) >= d and np.linalg.matrix_rank(on[1:] - on[0], tol=1e-7) == d - 1:
            cnt[kj] = cnt.get(kj, 0) + 1
    return cnt

for key in [k for k in NETS if k in (sys.argv[1:] or NETS)]:
    spec = NETS[key]; d = json.load(open(f"../data/raw/{key}.json")); ok = True; n = 0
    for r in d["intervals"]:
        lo, hi = float(Fr(r["lo"])), float(Fr(r["hi"]))
        for lam in lo + (hi - lo) * rng.uniform(0.05, 0.95, 3):
            for s in r["sites"]:
                got = float_cell(spec, s["i"], lam); n += 1
                if got != s["bonds"]:
                    ok = False; print(key, lam, s["i"], got, s["bonds"])
    check(f"{key}: float power cells at 3 random parameters per interval give the exact bond counts", ok, f"{n} cells")

def hull_faces(P):
    """Exact facets of the hull of rational points P (affine; metric irrelevant): list of point-index sets."""
    faces = set()
    for a, b, c in combinations(range(len(P)), 3):
        u = [P[b][q] - P[a][q] for q in range(3)]; v = [P[c][q] - P[a][q] for q in range(3)]
        n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
        if n == (0, 0, 0): continue
        s = [sum(n[q] * (P[k][q] - P[a][q]) for q in range(3)) for k in range(len(P))]
        if all(x >= 0 for x in s) or all(x <= 0 for x in s):
            faces.add(frozenset(k for k in range(len(P)) if s[k] == 0))
    return faces

def parallel_pairs(P, f):
    """For a quadrilateral face: the number of pairs of parallel opposite sides (rhombus/parallelogram 2, trapezoid 1)."""
    f = list(f)
    import numpy as np
    Q = np.array([[float(x) for x in P[k]] for k in f]); c = Q.mean(0); n = np.cross(Q[1] - Q[0], Q[2] - Q[0])
    u = Q[0] - c; v = np.cross(n, u); ang = np.arctan2((Q - c) @ v, (Q - c) @ u); f = [f[k] for k in np.argsort(ang)]
    side = [tuple(P[f[(k + 1) % 4]][q] - P[f[k]][q] for q in range(3)) for k in range(4)]
    par = lambda a, b: all(a[q] * b[r] - a[r] * b[q] == 0 for q in range(3) for r in range(3))
    return int(par(side[0], side[2])) + int(par(side[1], side[3]))

for key, want in (("delian", "rhombic dodecahedron: 12 rhombi"), ("hcpholes", "trapezo-rhombic dodecahedron: 6 rhombi + 6 trapezoids")):
    spec = NETS[key]; net = Net(key, spec["G"], spec["T"], spec["motif"], spec["w"])
    c = Cell(net, 0, (Fr(-1, 8),), Fr(spec["D2"]))
    q = max(c.corners, key=lambda p: len(p["on"]))
    P = [c.c] + [c.H[k]["c"] for k in q["on"]]
    F = hull_faces(P); sizes = sorted(len(f) for f in F); pp = sorted(parallel_pairs(P, f) for f in F if len(f) == 4)
    ok = len(P) == 14 and sizes == [4] * 12 and (pp == [2] * 12 if key == "delian" else pp == [1] * 6 + [2] * 6)
    check(f"{key}: at the octet-type stop lam = -1/8 the dual cell at an atom is the {want} (exact hull)", ok, f"{len(P)} sites, faces {sizes}, parallel pairs {pp}")
with open("../data/checks/crosscheck-checks.txt", "w") as fh:
    for s, n, det in checks: fh.write(f"{s} {n} {det}\n")
print(sum(c[0] == "PASS" for c in checks), "/", len(checks))
