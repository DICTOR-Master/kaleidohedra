# Cleo core step 1 (DICTO 2026-10-15): is the hollow ID(1) exactly the core I(1) + 12 flat pentagonal pyramids (window base, point on a
# core corner) + 20 triangular antiprisms (ID triangle over core face)? Frame: the DICTO-Star's own centre (krp-core idStar).
import itertools, json, sys, numpy as np
from scipy.spatial import ConvexHull
S = json.load(open(sys.argv[1])); ID = np.array(S['centre'])
H = ConvexHull(ID); F = []
for e in H.equations:
    idx = tuple(sorted(i for i in range(30) if abs(ID[i] @ e[:3] + e[3]) < 1e-9))
    if idx not in [f for f, _ in F]: F.append((idx, e))
tri = [(ID[list(i)], e[:3]) for i, e in F if len(i) == 3]; pent = [(ID[list(i)], e[:3]) for i, e in F if len(i) == 5]
R = (10 + 2 * 5 ** .5) ** .5 / 4
core = np.array([n * R for _, n in pent]); CH = ConvexHull(core)
cf = [core[s] for s in CH.simplices]
pyr = [np.vstack([P, n * R]) for P, n in pent]
anti = []
for T, n in tri:
    face = max(cf, key=lambda Q: Q.mean(0) @ n)            # the core face under this triangle
    anti.append(np.vstack([T, face]))
vol = lambda P: ConvexHull(P).volume
def axes(P):
    h = ConvexHull(P); A = [e[:3] for e in h.equations]
    E = {tuple(np.round(P[j] - P[i], 12)) for s in h.simplices for i, j in itertools.combinations(s, 2)}
    return A, [np.array(x) for x in E]
def sep(P, Q):
    a1, e1 = axes(P); a2, e2 = axes(Q); best = -1e9
    for m in a1 + a2 + [np.cross(u, w) / np.linalg.norm(np.cross(u, w)) for u in e1 for w in e2 if np.linalg.norm(np.cross(u, w)) > 1e-12]:
        p, q = P @ m, Q @ m; best = max(best, q.min() - p.max(), p.min() - q.max())
    return best
out = []
tot = vol(core) + sum(map(vol, pyr)) + sum(map(vol, anti))
out.append(f'1. volumes: core {vol(core):.12f} + 12 pyramids {sum(map(vol, pyr)):.12f} + 20 antiprisms {sum(map(vol, anti)):.12f} = {tot:.12f}; ID {vol(ID):.12f}; difference {tot - vol(ID):.1e}')
allp = [core] + pyr + anti
worst = min(sep(a, b) for a, b in itertools.combinations(allp, 2))
out.append(f'2. no overlaps among the 33 solids: worst separation {worst:.1e}')
# sampled cover: random points in the ID each in exactly one piece
inside = lambda P, x: all(e[:3] @ x + e[3] <= 1e-9 for e in ConvexHull(P).equations)
rng = np.random.default_rng(3); hits = {0: 0, 1: 0, 2: 0}
eqs = H.equations
for x in rng.uniform(-1.62, 1.62, size=(40000, 3)):
    if all(e[:3] @ x + e[3] < -1e-9 for e in eqs):
        k = sum(inside(P, x) for P in allp); hits[min(k, 2)] += 1
out.append(f'3. sampled points inside the ID: covered once {hits[1]}, not covered {hits[0]}, covered twice {hits[2]}')
# shapes
h5 = np.linalg.norm(pyr[0][5]) - 0; pd = -[e for e in eqs][0][3]
pyr_h = min(abs(np.linalg.norm(P[:5].mean(0)) - R) for P in pyr)
ed = lambda P: sorted({round(np.linalg.norm(a - b), 6) for a, b in itertools.combinations(P, 2)})
A0 = anti[0]; side = sorted(round(np.linalg.norm(a - b), 6) for a in A0[:3] for b in A0[3:])
twist = np.degrees(np.arccos(np.clip(((A0[0] - A0[:3].mean(0)) @ (A0[3] - A0[3:].mean(0))) / np.linalg.norm(A0[0] - A0[:3].mean(0)) / np.linalg.norm(A0[3] - A0[3:].mean(0)), -1, 1)))
out.append(f'4. pentagonal pyramid: base edge 1, height {pyr_h:.6f}, side edges {sorted(set(round(np.linalg.norm(pyr[0][5] - v), 6) for v in pyr[0][:5]))}, volume {vol(pyr[0]):.6f}')
out.append(f'5. antiprism: two edge-1 triangles {np.linalg.norm(A0[:3].mean(0)) - np.linalg.norm(A0[3:].mean(0)):.6f} apart; ID-to-core edges {sorted(set(side))[:3]}; faces {len(ConvexHull(A0).simplices)} triangles; volume {vol(A0):.6f}')
# do neighbouring pieces meet in whole faces? count shared triangles between pyramids and antiprisms
def tris(P):
    h = ConvexHull(P); return {tuple(sorted(map(tuple, np.round(P[s], 6)))) for s in h.simplices}
shared = sum(len(tris(p) & tris(a)) for p in pyr for a in anti)
out.append(f'6. whole-face contacts between pyramids and antiprisms: {shared} triangles (60 expected if every pyramid side meets an antiprism side)')
print('\n'.join(out)); open('core_step1.txt', 'w').write('\n'.join(out) + '\n')
