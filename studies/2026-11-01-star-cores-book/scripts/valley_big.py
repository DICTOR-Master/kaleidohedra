# Star Cores book: DICTO's valley rule (star_valley.run of #79, the same steps and bisections) for Hamlet and Ophelia, which #79 left out
# (over 200 faces). Only change: candidate pieces for each clash test come from a k-d tree of piece centres (pieces whose bounding spheres
# cannot meet are skipped, as clash() itself would skip them), and no 2500-triangle cap. Usage: valley_big.py <ds> <slug> <D> <phi|2> <out>
import sys, os, json, numpy as np
from scipy.spatial import cKDTree
DS, SLUG, DN, T, OUT = sys.argv[1:6]; sys.argv = [sys.argv[0], DS, '/tmp', '/tmp']
sys.path.insert(0, os.path.expanduser('~/kres-tmp/star-cores/scripts'))
from star_core import faces_info, polyvol, vol, load
from star_valley import clash, geo
phi = (1 + 5 ** .5) / 2; t = phi if T == 'phi' else 2.0
d, V, F = load('solids/' + SLUG + '.json'); V = V - V.mean(0)
old = [np.vstack([V[f], np.zeros(3)]) for f in F]; OG = [geo(Q) for Q in old]; below = list(old)
steps = []; R0 = np.linalg.norm(V, axis=1).max(); VOL0 = polyvol(V, F)
def ctr(Q): return Q.mean(0)
def rad(Q): return np.linalg.norm(Q - Q.mean(0), axis=1).max()
for k in range(1, 4):
    FI = faces_info(V, F); base = []
    for (f, n, c), P in zip(FI, below):
        h = (P - V[f[0]]) @ n; A = P[np.abs(h - h.min()) < 1e-9].mean(0); foot = A + (c - A @ n) * n; base.append((f, A, foot))
    spike = lambda i, s: np.vstack([V[base[i][0]], base[i][1] + s * (base[i][2] - base[i][1])])
    OC = np.array([ctr(Q) for Q in old]); ORr = np.array([rad(Q) for Q in old]); tree = cKDTree(OC); RM = ORr.max()
    def free_old(i, s):
        Q = spike(i, s); g = geo(Q); c0, r0 = ctr(Q), rad(Q)
        return not any(clash(Q, g, old[j], OG[j]) for j in tree.query_ball_point(c0, r0 + RM + 1e-9))
    S = []
    for i in range(len(base)):
        if free_old(i, t): S.append(t); continue
        lo, hi = 1.0, t
        for _ in range(30):
            mid = (lo + hi) / 2
            if free_old(i, mid): lo = mid
            else: hi = mid
        S.append(lo)
    for _ in range(12):
        Qs = [spike(i, s) for i, s in enumerate(S)]; Gs = [geo(Q) if s > 1 + 1e-9 else None for Q, s in zip(Qs, S)]
        idx = [i for i in range(len(S)) if Gs[i]]
        if not idx: break
        Cs = np.array([ctr(Qs[i]) for i in idx]); Rs = np.array([rad(Qs[i]) for i in idx]); tr = cKDTree(Cs)
        cand = tr.query_pairs(2 * Rs.max() + 1e-9)
        pairs = sorted((idx[a], idx[b]) for a, b in cand if clash(Qs[idx[a]], Gs[idx[a]], Qs[idx[b]], Gs[idx[b]]))
        if not pairs: break
        for i, j in pairs:
            lo, hi = 1.0, min(S[i], S[j])
            for _ in range(30):
                mid = (lo + hi) / 2; A_, B_ = spike(i, min(S[i], mid)), spike(j, min(S[j], mid))
                if clash(A_, geo(A_), B_, geo(B_)): hi = mid
                else: lo = mid
            S[i] = min(S[i], lo); S[j] = min(S[j], lo)
    V2 = list(V); F2 = []; B2 = []
    for i, (f, A, foot) in enumerate(base):
        if S[i] <= 1 + 1e-9: F2.append(list(f)); B2.append(below[i]); continue
        tip = A + S[i] * (foot - A); ti = len(V2); V2.append(tip); Q = np.vstack([V[f], tip]); old.append(Q); OG.append(geo(Q))
        for a in range(len(f)): F2.append([f[a], f[(a + 1) % len(f)], ti]); B2.append(Q)
    V2 = np.array(V2); R = np.linalg.norm(V2, axis=1).max(); VOL = polyvol(V2, F2)
    fr = [(s - 1) / (t - 1) for s in S]
    steps.append(dict(step=k, triangles=len(F2), full=sum(1 for x in fr if x > 1 - 1e-9), flat=sum(1 for x in fr if x < 1e-9),
                      height_kinds=sorted({round(x, 4) for x in fr}), radius_over_last=R / R0, volume_over_last=VOL / VOL0))
    print(json.dumps(steps[-1]), flush=True)
    V, F, below, R0, VOL0 = V2, F2, B2, R, VOL
    json.dump(dict(name=d['name'], D=DN, t=T, steps=steps), open(OUT, 'w'), indent=1)
print('done')
