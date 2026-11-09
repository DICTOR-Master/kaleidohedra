# DICTO #43, 9 Nov ("continue"): are the lagging largest faces SLIVERS, and are they split within a few steps?
# Per level k: the face with the largest angular radius gamma (new or not): number of corners, aspect (long/short spread of its corners
# in its plane), equivalent radius sqrt(area/pi) as an angle. Tracking: for the top face of level k, the face of level k+m (m = 1..4)
# whose normal is nearest to it, and that face's gamma: the ratio gamma_{k+m}(same direction) / gamma_k.
# usage: python -u sliver_track.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json, time, math
import numpy as np
from scipy.spatial import ConvexHull, cKDTree
OUT = os.path.abspath(sys.argv[3]); sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
src = open('exact_upward.py').read(); exec(src.split("def kinds(S)")[0]); KMAX = int(sys.argv[2])
W = np.array([[float(x.a) + float(x.b) * 5 ** .5 for x in v] for v in OG])
def faces(W, tol=1e-9):
    h = ConvexHull(W); E = h.equations; n = len(E); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if g > f and np.abs(E[f] - E[g]).max() < tol: par[find(f)] = find(g)
    G = {}
    for f in range(n): G.setdefault(find(f), []).append(f)
    N, D, M = [], [], []
    for g in G.values():
        N.append(h.equations[g[0], :3]); D.append(-h.equations[g[0], 3]); M.append(sorted(set(int(j) for f in g for j in h.simplices[f])))
    return np.array(N), np.array(D), M
def gamma(W, n, mem):
    P = W[mem]; rr = np.linalg.norm(P, axis=1); return float(np.arccos(np.clip((P @ n) / rr, -1, 1)).max())
def shape(W, n, d, mem):
    P = W[mem]; c = P.mean(0); B = np.linalg.svd(P - c)[2][:2]; Q = (P - c) @ B.T; s = np.linalg.svd(Q - Q.mean(0), compute_uv=False)
    area = ConvexHull(Q).volume if len(mem) > 2 else 0.0
    return float(s[0] / max(s[1], 1e-15)), float(math.degrees(math.sqrt(area / math.pi) / d)), len(mem)
levels = []; t0 = time.time()
for k in range(KMAX + 1):
    N, D, M = faces(W)
    gam = np.array([gamma(W, n, m) for n, m in zip(N, M)])
    order = np.argsort(-gam)[:5]
    tops = []
    for j in order:
        asp, eqr, nc = shape(W, N[j], D[j], M[j]); tops.append({'gamma_deg': float(np.degrees(gam[j])), 'aspect': asp, 'eq_radius_deg': eqr, 'corners': nc, 'normal': N[j].tolist()})
    levels.append({'k': k, 'F': len(N), 'tree': (N, gam), 'tops': tops})
    t = tops[0]
    print(f"k {k:2d} F {len(N):6d} top gamma {t['gamma_deg']:.3f} deg, corners {t['corners']}, aspect {t['aspect']:.2f}, equal-area radius {t['eq_radius_deg']:.3f} deg"
          f" | top5 aspects {', '.join(f'{x['aspect']:.1f}' for x in tops)} ({time.time() - t0:.0f} s)", flush=True)
    if k == KMAX: break
    W = N * D[:, None]
print('tracking the top face of level k (ratio of gamma in the same direction after m steps):')
for L in levels:
    if L['k'] < 12: continue
    u = np.array(L['tops'][0]['normal']); g0 = L['tops'][0]['gamma_deg']; out = []
    for m in (1, 2, 3, 4):
        if L['k'] + m > KMAX: break
        N2, g2 = levels[L['k'] + m]['tree']; j = cKDTree(N2).query(u)[1]; out.append(np.degrees(g2[j]) / g0)
    print(f"  k {L['k']:2d}: gamma {g0:.3f} -> " + ', '.join(f'm{m + 1} {x:.3f}' for m, x in enumerate(out)))
for L in levels: del L['tree']
json.dump({'mark': 'DICTO #43 sliver tracking, 2026-11-09 · DICTO · dictospheres.com', 'levels': levels}, open(OUT, 'w'), indent=1)
print('FINAL ok' if len(levels) == KMAX + 1 else 'FINAL FAIL: run incomplete')
