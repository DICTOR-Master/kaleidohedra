# DICTO OCD Stella seed: the gap cut into convex cells (float exploration for the piece kits, DICTO 2026-10-16: "exact piece kits").
# Bodies: centre S/φ, twelve S + φv_i, outer φ²S. Space inside the outer form is cut by every face plane of the 13 bodies (BSP); cells
# inside a body are dropped; the rest are the gap's elementary convex cells. Then cells are sorted into orbits of the seed's symmetry
# (the OCD Stella's 24 signed permutations, in its cube frame) and kinds (sorted edge lengths + volume). -> data/stella-seed-cells.json/.txt
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
R = json.load(open('data/stella-seed.json')); S = np.array(R['stella']['v']); PHI = (1 + 5 ** .5) / 2
def planes(V):
    P = []
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e, q, atol=1e-8) for q in P): P.append(e)
    return np.array(P)
PS = planes(S)
rr = np.linalg.norm(S, axis=1); far = S[rr > rr.max() - 1e-9]
bodies = [S / PHI] + [S + PHI * v for v in far]
outer = S * PHI ** 2
BP = [planes(B) for B in bodies]
cut = {}
for P in BP + [planes(outer)]:
    for e in P:
        n = e[:3] / np.linalg.norm(e[:3]); d = -e[3] / np.linalg.norm(e[:3])
        if d < 0: n, d = -n, -d
        cut.setdefault((tuple(np.round(n, 7)), round(d, 7)), (n, d))
CUTS = list(cut.values()); print('distinct cut planes', len(CUTS))
def split(V, n, d, eps=1e-9):
    s = V @ n - d
    if s.max() <= eps or s.min() >= -eps: return None
    h = ConvexHull(V); E = {tuple(sorted(p)) for f in h.simplices for p in itertools.combinations(f, 2)}
    new = [V[i] + (V[j] - V[i]) * (s[i] / (s[i] - s[j])) for i, j in E if s[i] * s[j] < 0 and abs(s[i]) > eps and abs(s[j]) > eps]
    onp = [V[i] for i in range(len(V)) if abs(s[i]) <= eps]
    A = np.array([V[i] for i in range(len(V)) if s[i] < -eps] + new + onp); B = np.array([V[i] for i in range(len(V)) if s[i] > eps] + new + onp)
    return A, B
def vol(V):
    try: return ConvexHull(V).volume
    except Exception: return 0.0
cells = [outer]
for k, (n, d) in enumerate(CUTS):
    nxt = []
    for V in cells:
        r = split(V, n, d)
        if r is None: nxt.append(V); continue
        for W in r:
            if len(W) >= 4 and vol(W) > 1e-10: nxt.append(W)
    cells = nxt
inside = lambda P, x: np.all(P[:, :3] @ x + P[:, 3] <= 1e-9)
gap = [V for V in cells if not any(inside(P, V.mean(0)) for P in BP)]
vO = vol(outer); vg = sum(vol(V) for V in gap)
out = [f'cells {len(cells)}, gap cells {len(gap)}; gap volume {vg:.6f} = {vg / vO:.6f} of the outer form (exact −69 + 31√5 = {-69 + 31 * 5 ** .5:.6f})']
def sig(V):
    h = ConvexHull(V); W = V[h.vertices]
    return (round(vol(V), 7), tuple(np.round(np.sort([np.linalg.norm(a - b) for a, b in itertools.combinations(W, 2)]), 5)))
kinds = {}
for V in gap: kinds.setdefault(sig(V), []).append(V)
out.append(f'kinds (congruent up to mirror) {len(kinds)}; counts {sorted((len(v) for v in kinds.values()), reverse=True)}')
print('\n'.join(out)); open('data/stella-seed-cells.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'cells': [V.tolist() for V in gap]}, open('data/stella-seed-cells.json', 'w'))
