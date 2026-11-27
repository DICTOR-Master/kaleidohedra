"""Data for the Hollow-straw page of the app (27 Nov 2026; DICTO: "yes build the Hollow-straw app"). With Claude (Anthropic).
Exactly the construction proved in c116_transform_exact.py (floats of it): C116 in its own shape -> Minana #377, a_k(lam) = (1 - lam) a_k
+ lam m_sigma(k). Writes one JSON for the page:
  frames : P(lam) on a grid of lam (dense near the swap times): corners, and each face k as its corner cycle;
  straws : the 60 straws (region swept by face k), lofted corner to corner between grid steps, hull of the two polygons across a swap;
           real edges only (the C116 face, the Minana face, the paths of the corners);
  colour : the Aequi page's colour of the Minana face each C116 face becomes; swaps: the 18 swap times (from transform_exact.json).
Checks: frame 0 has C116's pattern, the last frame Minana's; every frame is nested in the next (every corner of frame i inside frame i+1)."""
import os, sys, json
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
src = open(os.path.join(HERE, 'c116_transform.py')).read(); g = {'__file__': os.path.join(HERE, 'c116_transform.py'), '__name__': 'tf'}
exec(src[:src.index('def pairs_of')], g)
Ak, Mk, sig, S, A = g['Ak'], g['Mk'], g['sig'], g['S'], g['A']
import aequus_solid as AS
COL = {'C': '#488e48', 'O': '#e8c852', 'T': '#cd3e28', 'D': '#8a5cc4', 'I': '#3a70cd', 'RD': '#b3a489', 'RT': '#8e9aa5'}
def mix(a, b, t): return '#' + ''.join('%02x' % round(int(a[1 + 2 * i:3 + 2 * i], 16) * (1 - t) + int(b[1 + 2 * i:3 + 2 * i], 16) * t) for i in range(3))
def colOf(key): base = COL[key.replace('2', '')]; return mix(base, '#ffffff', 0.45) if key.endswith('2') else base
Dd = json.load(open(os.path.join(ROOT, 'src/dice.json'))); e = Dd['dice'][376]; ED = AS.C.exact_dirs(Dd['dirs']); lab = {}
for oi in e['o']:
    gr = Dd['groups'][e['g']][oi]
    for i in gr['dirs']: lab[A.key([AS.Q(c.a, c.b) for c in ED[i][0]])] = gr['col']
mcol = [lab[A.key(u)] for u, c in S['planes']]
col = [colOf(mcol[sig[k]]) for k in range(60)]
legend = {colOf(k): {'D': 'dodecahedron planes', 'I2': 'icosahedron planes', 'RD': 'rhombic dodecahedron planes', 'RT2': 'rhombic triacontahedron planes'}[k] for k in set(mcol)}
EX = json.load(open(os.path.join(ROOT, 'data/c116/transform_exact.json')))
swaps = [dict(lam=ev['lam'], lost=ev['lost'][0], gained=ev['gained'][0]) for ev in EX['events']]
def solid(lam):
    A_ = (1 - lam) * Ak + lam * Mk
    P = HalfspaceIntersection(np.hstack([A_, -np.ones((60, 1))]), np.zeros(3)).intersections
    sc = np.abs(P).max(); pts = []
    for p in P:
        if not any(np.linalg.norm(p - q) < 1e-9 * sc for q in pts): pts.append(p)
    P = np.array(pts); tight = np.abs(A_ @ P.T - 1) < 1e-8; faces = []
    for k in range(60):
        idx = list(np.where(tight[k])[0]); X = P[idx]; c0 = X.mean(0); n = A_[k] / np.linalg.norm(A_[k]); e1 = X[0] - c0; e2 = np.cross(n, e1)
        order = np.argsort(np.arctan2((X - c0) @ e2, (X - c0) @ e1)); faces.append([idx[i] for i in order])
    labs = [frozenset(np.where(tight[:, i])[0]) for i in range(len(P))]
    return P, faces, labs, A_
ev = sorted({round(s['lam'], 4) for s in swaps})
grid = sorted(set(np.round(np.concatenate([np.linspace(0, 1, 61)] + [np.linspace(t - 0.003, t + 0.003, 9) for t in ev]), 6)))
grid = [x for x in grid if 0 <= x <= 1]
F = [solid(l) for l in grid]
r4 = lambda X: np.round(np.asarray(X), 3).tolist()
frames = [dict(lam=float(l), v=r4(P), f=[[int(i) for i in fc] for fc in faces]) for l, (P, faces, labs, A_) in zip(grid, F)]
nested = all((((1 - grid[i + 1]) * Ak + grid[i + 1] * Mk) @ F[i][0].T <= 1 + 1e-9).all() for i in range(len(grid) - 1))
def pairs(faces):
    return {(k, l) for k in range(60) for l in range(k + 1, 60) if len(set(faces[k]) & set(faces[l])) >= 2}
inv = {v: k for k, v in sig.items()}
def pairs_of(fl):
    at = {}
    for k, Fk in enumerate(fl):
        for v in Fk: at.setdefault(v, set()).add(k)
    return {(a, b) for S_ in at.values() for a in S_ for b in S_ if a < b}
C116f = json.load(open(os.path.join(ROOT, 'data/c116/pairing.json')))['faces']
ok_ends = pairs(F[0][1]) == pairs_of(C116f) and pairs(F[-1][1]) == {tuple(sorted((inv[a], inv[b]))) for a, b in pairs_of([vs for vs, kk in S['faces']])}
# straws on a coarser grid
sgrid = [i for i, l in enumerate(grid) if abs(l * 20 - round(l * 20)) < 1e-9 or any(abs(l - t) <= 0.003 + 1e-9 for t in ev)]
straws = []
for k in range(60):
    V, T, E = [], [], []
    def add(p): V.append(p); return len(V) - 1
    def cap(P, cyc):
        ids = [add(P[i]) for i in cyc]
        for a in range(1, len(ids) - 1): T.append([ids[0], ids[a], ids[a + 1]])
        for a in range(len(ids)): E.append([ids[a], ids[(a + 1) % len(ids)]])
    cap(F[0][0], F[0][1][k]); cap(F[-1][0], F[-1][1][k])
    for a, b in zip(sgrid, sgrid[1:]):
        P0, f0, l0, _ = F[a]; P1, f1, l1, _ = F[b]
        L0 = [l0[i] for i in f0[k]]; L1 = [l1[i] for i in f1[k]]
        if set(L0) == set(L1) and len(L0) == len(L1):
            m = {lb: i for lb, i in zip(L1, f1[k])}; n = len(L0)
            ia = [add(P0[i]) for i in f0[k]]; ib = [add(P1[m[lb]]) for lb in L0]
            for q in range(n):
                r = (q + 1) % n; T.append([ia[q], ia[r], ib[r]]); T.append([ia[q], ib[r], ib[q]]); E.append([ia[q], ib[q]])
        else:
            X = np.vstack([P0[f0[k]], P1[f1[k]]]); n0 = len(f0[k]); h = ConvexHull(X); base = len(V)
            for p in X: V.append(p)
            for t in h.simplices:
                if all(i < n0 for i in t) or all(i >= n0 for i in t): continue
                T.append([base + int(i) for i in t])
    straws.append(dict(k=k, v=r4(V), t=T, e=E))
out = dict(title='C116 into Minana #377: Hollow-straw', colour=col, legend=legend, swaps=swaps, frames=frames, straws=straws,
           checks=dict(ends_ok=bool(ok_ends), nested_frames=bool(nested)))
dst = os.environ.get('OUT', os.path.join(ROOT, 'renders/hollow-straw-c116-minana.json'))
json.dump(out, open(dst, 'w'), separators=(',', ':'))
print('frames', len(frames), 'straws', len(straws), 'size', os.path.getsize(dst), 'bytes; ends ok', ok_ends, '; frames nested', nested, flush=True)
print('FINAL ok' if ok_ends and nested and len(straws) == 60 else 'FINAL FAIL')
