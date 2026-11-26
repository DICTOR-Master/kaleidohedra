"""Hollow-straw, version 3: flat-walled straws (27 Nov 2026; DICTO's idea: start and end shapes fixed, a balloon-like drinking straw
between each pair of faces, all straws pumped up together until they meet). With Claude (Anthropic).
Model. Each straw k has a "pressure" that is an affine function f_k(x) = g_k . x + h_k; a point of the shell belongs to the straw
with the highest pressure there, so every wall between two straws is the flat plane f_j = f_k and every straw is convex (an
intersection of half-spaces). Straw k must hold its core face k and its end face sigma(k): at each core corner (faces a, c, d) the
three pressures are equal and no other straw is higher; the same at each Minana corner. Then each piece = straw k between the core
plane k and the Minana plane sigma(k), a CONVEX Scutoid-Frustum (argument in the README).
Unknowns: the 60 core planes (the core's shape and place float; Minana is fixed, at its own size) and the 60 pressures.
Equations: equal pressures at the 116 core corners and the 116 Minana corners. Solved by least squares from many starts; a state
counts only if the equations hold to 1e-12 AND every inequality holds with margin (no other straw higher at any corner, core
convex with C116's pattern, core strictly inside Minana). Numerical first; exact form only if a solution exists.
Usage: python c116_straw.py [sym|float]   (pairing: the symmetric 30-swap one or the floating 18-swap one)"""
import os, sys, json
import numpy as np
from scipy.optimize import least_squares
argv = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
sys.argv = argv
HERE = os.path.dirname(os.path.abspath(__file__))
which = argv[1] if len(argv) > 1 else 'sym'
d = json.load(open(os.path.join(HERE, '../data/c116/pairing.json'))); faces, mf, P = d['faces'], d['minana_faces'], np.array(d['P'])
sig = {int(k): int(v) for k, v in json.load(open(os.path.join(HERE, '../data/c116/' + ('onefloor.json' if which == 'sym' else 'onefloor_float.json'))))['pairing'].items()}
iv = {v: k for k, v in sig.items()}
Dm = A.build("aequus-377")
MV = np.array([[float(c) for c in v] for v in Dm["V"]]); MV /= np.abs(MV).max()
MN = np.array([[float(x) for x in u] for u, c in Dm["planes"]]); MC = np.array([float(c) for u, c in Dm["planes"]])
MC = MC / (np.linalg.norm(MN, axis=1)); MN = MN / np.linalg.norm(MN, axis=1)[:, None]
# Minana planes at the vertex scale used: recompute offsets from the vertices
mverts = [vs for vs, kk in Dm["faces"]]
MC = np.array([np.mean(MV[vs] @ MN[k]) for k, vs in enumerate(mverts)])
def corners(fl):
    at = {}
    for k, f in enumerate(fl):
        for v in f: at.setdefault(v, set()).add(k)
    return at
cc = corners(faces); T0 = [tuple(sorted(s)) for v, s in sorted(cc.items())]
mc = corners(mverts); T1 = [(tuple(sorted(iv[x] for x in s)), v) for v, s in sorted(mc.items())]   # core labels, Minana vertex
assert len(T0) == 116 and len(T1) == 116
# initial core: C116 turned onto Minana by the pairing (Procrustes, mirror allowed), scaled inside
C = []
for f in faces:
    X = P[f]; c0 = X.mean(0); n = np.linalg.svd(X - c0)[2][2]; C.append(n if n @ c0 > 0 else -n)
C = np.array(C); U, _, Vt = np.linalg.svd(C.T @ MN[[sig[k] for k in range(60)]]); R = (U @ Vt).T
Pc = P @ R.T
E0 = next(k for k in range(60) if k not in T0[0] and len(set(faces[k]) & set(faces[T0[0][0]])) == 2)
def unpack(z): return z[:180].reshape(60, 3), z[180:420].reshape(60, 4)
def corner_core(N, t):
    return np.linalg.solve(N[list(t)], np.ones(3))
def resid(z):
    N, F = unpack(z); r = []
    for t in T0:
        v = corner_core(N, t); fv = F[list(t), :3] @ v + F[list(t), 3]; r += [fv[0] - fv[1], fv[0] - fv[2]]
    for t, w in T1:
        x = MV[w]; fv = F[list(t), :3] @ x + F[list(t), 3]; r += [fv[0] - fv[1], fv[0] - fv[2]]
    r += list(1e-3 * (F[0] - F0ref))     # gauge: pressures are fixed only up to a common affine function
    # scale: equal pressures everywhere solve the equations trivially; at the first core corner the nearest other straw must be
    # 0.1 lower (any positive number: pressures scale freely)
    t0 = T0[0]; v = corner_core(N, t0); fv = F[:, :3] @ v + F[:, 3]
    r.append(fv[t0[0]] - fv[E0] - 0.1)
    return np.array(r)
def check(z, margin=1e-7):
    N, F = unpack(z); bad = 0
    V = [corner_core(N, t) for t in T0]
    for v, t in zip(V, T0):
        fv = F[:, :3] @ v + F[:, 3]; top = fv[list(t)].max()
        bad += int(sum(1 for k in range(60) if k not in t and fv[k] > top - margin))
        bad += int(sum(1 for k in range(60) if k not in t and N[k] @ v > 1 - margin))         # core convex, C116's pattern
        bad += int(sum(1 for k in range(60) if MN[k] @ v > MC[k] - margin))                   # core strictly inside Minana
    for t, w in T1:
        x = MV[w]; fv = F[:, :3] @ x + F[:, 3]; top = fv[list(t)].max()
        bad += int(sum(1 for k in range(60) if k not in t and fv[k] > top - margin))
    return bad
rng = np.random.default_rng(3); NST = int(os.environ.get('NSTART', 60)); out = []
for s in range(NST):
    sc = rng.uniform(0.55, 0.9); jit = 0.02 * (s > 0)
    Pk = Pc * sc / np.abs(Pc).max()
    N0 = []
    for k, f in enumerate(faces):
        X = Pk[f]; c0 = X.mean(0); n = np.linalg.svd(X - c0)[2][2]; n = n if n @ c0 > 0 else -n; N0.append(n / (n @ c0))
    N0 = np.array(N0) * (1 + jit * rng.normal(size=(60, 3)))
    G = np.array([(N0[k] / np.linalg.norm(N0[k]) + MN[sig[k]]) for k in range(60)]); G /= np.linalg.norm(G, axis=1)[:, None]
    F0 = np.hstack([G * (1 + jit * rng.normal(size=(60, 3))), np.zeros((60, 1))])
    F0ref = F0[0].copy()
    sol = least_squares(resid, np.concatenate([N0.ravel(), F0.ravel()]), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
    res = float(np.abs(np.concatenate([resid(sol.x)[:-5], resid(sol.x)[-1:]])).max()); bad = check(sol.x)
    out.append(dict(start=s, scale=round(sc, 3), max_residual=res, inequality_violations=bad))
    print(f'start {s}: core scale {sc:.3f}  max equation residual {res:.2e}  inequality violations {bad}', flush=True)
    if res < 1e-12 and bad == 0:
        json.dump(dict(pairing=which, z=sol.x.tolist()), open(os.path.join(HERE, f'../data/c116/straw_{which}.json'), 'w'))
        print('FOUND: flat-walled Hollow-straw layer (numerical); saved', flush=True); break
    print(f'PROGRESS {(s + 1) / NST:.2f}', flush=True)
best = min(out, key=lambda r: (r['max_residual'] > 1e-12, r['inequality_violations'], r['max_residual']))
print('BEST:', best)
found = best['max_residual'] < 1e-12 and best['inequality_violations'] == 0
print('RESULT:', 'flat-walled straws EXIST (numerically) for this pairing' if found else 'no flat-walled solution found from these starts')
print('FINAL ok' if len(out) > 0 and all(np.isfinite(r['max_residual']) for r in out) else 'FINAL FAIL')
