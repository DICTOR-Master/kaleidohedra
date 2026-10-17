# Fable 2026-10-17 — DICTO's scutoid group, flat layer version.
# Construction: a periodic flat layer of 8 cells per group (the smallest colouring found by fable_search.py).
# Each piece is a 3D Laguerre (power) cell: power_i(x,z) = |x - X_i|^2 + c_i + z*t_i, so every face is planar, every piece convex.
# Middle of the layer (z=0): every cell a hexagon. Top cut (z=+1): the 4 "T" cells are pentagons (each pinched at one corner where 4 pieces meet),
# bottom cut (z=-1): the 4 "B" cells are pentagons. So every cell is a pentagon at one end and a hexagon at the other.
# Free parameters (seed positions, lattice, c, t) are tuned (float, SLSQP) for regular-ish ends and chunky pieces. Labelled FLOAT.
import json, sys, numpy as np
from scipy.optimize import minimize
a, b, d = 2, 0, 4
bits = (1, 0, 0, 0, 1, 1, 0, 1)
n = a * d
def red(u, v):
    q = v // d; v2 = v - q * d; u2 = u - q * b; m = u2 // a; return (u2 - m * a, v2), (m, q)   # rep, shift (m along L1, q along L2)
idx = {(i, j): j * a + i for j in range(d) for i in range(a)}
NB = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
def flank(dd): return [m for m in NB if (m[0] - dd[0], m[1] - dd[1]) in NB]
# contracted edges
M = {+1: [], -1: []}
for (i, j), k in idx.items():
    for dd in [(1, 0), (0, 1), (-1, 1)]:
        o = (i + dd[0], j + dd[1]); f = [(i + x, j + y) for x, y in flank(dd)]
        col = [bits[idx[red(*c)[0]]] for c in [(i, j), o] + f]
        if col[0] == col[1] and col[2] != col[0] and col[3] != col[0]:
            M[+1 if col[0] == 1 else -1].append(((i, j), o, f[0], f[1]))
assert len(M[1]) == 2 and len(M[-1]) == 2
def unpack(p):
    X = p[:2 * n].reshape(n, 2); L = p[2 * n:2 * n + 4].reshape(2, 2); c = p[2 * n + 4:3 * n + 4]; t = p[3 * n + 4:4 * n + 4]; return X, L, c, t
def seed(cell, X, L):
    r, (m, q) = red(*cell); return X[idx[r]] + m * L[0] + q * L[1]
def vert(cells, X, L, c, t, z):
    P = [seed(cc, X, L) for cc in cells]; o = [c[idx[red(*cc)[0]]] + z * t[idx[red(*cc)[0]]] for cc in cells]
    A = 2 * np.array([P[1] - P[0], P[2] - P[0]]); rhs = np.array([P[1] @ P[1] - P[0] @ P[0] + o[1] - o[0], P[2] @ P[2] - P[0] @ P[0] + o[2] - o[0]])
    return np.linalg.solve(A, rhs)
def ring(cell):
    # the 6 triangles around a cell, in CCW order, as cell triples
    i, j = cell; out = []
    for k in range(6):
        p, q = NB[k], NB[(k + 1) % 6]; out.append([(i, j), (i + p[0], j + p[1]), (i + q[0], j + q[1])])
    return out
def polygon(cell, p, z):
    X, L, c, t = unpack(p); return np.array([vert(tr, X, L, c, t, z) for tr in ring(cell)])
def edges_all():
    E = []
    for (i, j) in idx:
        for k in range(3):
            dd = [(1, 0), (0, 1), (-1, 1)][k]; o = (i + dd[0], j + dd[1]); f = [(i + x, j + y) for x, y in flank(dd)]; E.append(((i, j), o, f[0], f[1]))
    return E
E = edges_all()
def elen(e, p, z):
    X, L, c, t = unpack(p); A, B, C, D = e
    v1 = vert([A, B, C], X, L, c, t, z); v2 = vert([A, B, D], X, L, c, t, z)
    dvec = seed(B, X, L) - seed(A, X, L); nrm = np.array([-dvec[1], dvec[0]]) / np.linalg.norm(dvec)
    s = np.sign((seed(C, X, L) - seed(D, X, L)) @ nrm)
    return s * (v1 - v2) @ nrm
def angles(P):
    # merge coincident vertices
    Q = [P[0]]
    for v in P[1:]:
        if np.linalg.norm(v - Q[-1]) > 1e-6: Q.append(v)
    if np.linalg.norm(Q[0] - Q[-1]) < 1e-6: Q.pop()
    Q = np.array(Q); m = len(Q); ang = []
    for k in range(m):
        u = Q[k - 1] - Q[k]; w = Q[(k + 1) % m] - Q[k]
        ang.append(np.degrees(np.arccos(np.clip(u @ w / np.linalg.norm(u) / np.linalg.norm(w), -1, 1))))
    return np.array(ang), Q
def soft_angles(P, five):
    # angles of the 6-gon with the pinched edge treated as merged (for the objective); uses all 6 vertices
    m = len(P); ang = []
    for k in range(m):
        u = P[k - 1] - P[k]; w = P[(k + 1) % m] - P[k]
        nu, nw = np.linalg.norm(u), np.linalg.norm(w)
        if nu < 1e-9 or nw < 1e-9: continue
        ang.append(np.degrees(np.arccos(np.clip(u @ w / nu / nw, -1, 1))))
    return np.array(ang)
cells = list(idx)
import os
AREAW = float(os.environ.get('AREAW', '0'))
PENW = float(os.environ.get('PENW', '0')); LOWANG = float(os.environ.get('LOWANG', '90'))
MINANG = float(os.environ.get('MINANG', '0'))
def obj(p):
    s = 0
    for z in (1, -1):
        for cc in cells:
            five = bits[idx[cc]] == (1 if z == 1 else 0)
            P = polygon(cc, p, z)
            if five:
                # drop the zero edge: find the shortest edge and merge it
                el = [np.linalg.norm(P[(k + 1) % 6] - P[k]) for k in range(6)]; k = int(np.argmin(el)); P = np.delete(P, (k + 1) % 6, 0)
                tgt = 108
            else: tgt = 120
            an, _ = np.array(soft_angles(P, five)), None
            s += ((an - tgt) ** 2).sum() + PENW * (np.maximum(0, LOWANG - an) ** 2).sum()
            # side lengths even
            sl = np.array([np.linalg.norm(P[(k + 1) % len(P)] - P[k]) for k in range(len(P))]); s += 300 * ((sl / sl.mean() - 1) ** 2).sum()
    if AREAW:
        for z in (1, 0, -1):
            ar = np.array([abs(np.sum(Q[:, 0] * np.roll(Q[:, 1], -1) - np.roll(Q[:, 0], -1) * Q[:, 1])) / 2 for Q in (polygon(cc, p, z) for cc in cells)])
            s += AREAW * ((ar / ar.mean() - 1) ** 2).sum()
    return s / 100
def cons_eq(p): return np.array([elen(e, p, z) for z in (1, -1) for e in M[z]])
def cons_in(p):
    out = []
    Ms = set((e[0], e[1]) for z in (1, -1) for e in M[z])
    for e in E:
        for z in (1, 0, -1):
            Lz = elen(e, p, z)
            if (e[0], e[1]) in Ms and z != 0 and any(e[0] == f[0] and e[1] == f[1] for f in M[z]): continue
            out.append(Lz - 0.12)
    for z in (1, -1):
        for cc in cells:
            Pp = polygon(cc, p, z)
            if bits[idx[cc]] == (1 if z == 1 else 0):
                el = [np.linalg.norm(Pp[(k + 1) % 6] - Pp[k]) for k in range(6)]; k = int(np.argmin(el)); Pp = np.delete(Pp, (k + 1) % 6, 0)
            out += list(soft_angles(Pp, 0) - MINANG)
    X, L, c, t = unpack(p); out.append(abs(L[0, 0] * L[1, 1] - L[0, 1] * L[1, 0]) - n * np.sqrt(3) / 2 * 0.999)
    out.append(n * np.sqrt(3) / 2 * 1.001 - abs(L[0, 0] * L[1, 1] - L[0, 1] * L[1, 0]))
    return np.array(out)
def init():
    e1 = np.array([1, 0.]); e2 = np.array([.5, np.sqrt(3) / 2])
    X = np.array([i * e1 + j * e2 for j in range(d) for i in range(a)]); L = np.array([a * e1, b * e1 + d * e2])
    t = np.array([.25 if bb else -.25 for bb in bits]); c = np.zeros(n)
    return np.r_[X.ravel(), L.ravel(), c, t]
if __name__ == '__main__':
    p0 = init()
    if os.environ.get('START'): p0 = np.array(json.load(open(os.environ['START']))['p'])
    print('init eq', np.round(cons_eq(p0), 6), 'obj', obj(p0))
    best = None
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 6):
        p = p0 + (rng.normal(0, .05, p0.size) if trial else 0)
        r = minimize(obj, p, method='SLSQP', constraints=[{'type': 'eq', 'fun': cons_eq}, {'type': 'ineq', 'fun': cons_in}], options=dict(maxiter=int(os.environ.get('MAXIT', '800')), ftol=1e-12))
        ok = np.abs(cons_eq(r.x)).max() < 1e-9 and cons_in(r.x).min() > -1e-9
        print(trial, r.success, r.message, r.nit, r.fun, ok, flush=True)
        if ok and (best is None or r.fun < best.fun): best = r
    json.dump(dict(p=best.x.tolist(), fun=best.fun), open(sys.argv[3] if len(sys.argv) > 3 else 'fable_best.json', 'w'))
    for z in (1, 0, -1):
        print('z', z)
        for cc in cells:
            an, Q = angles(polygon(cc, best.x, z)); print(' ', idx[cc], len(Q), np.round(an, 1))
