# What is left of the ring once the forced corner pieces are in? (2026-10-12)
# Ring = band - hole; take out the corner pieces (J2(1/phi) for the J2 ring, FUJI(1/phi) for the FUJI ring, each phi*P shrunk by
# 1/phi^2 about a floor corner, apex at the band's top corner); cut the rest by every face plane of these solids (exact BSP), keep
# the cells outside every solid, and merge neighbouring cells while the union stays convex (greedy, symmetric under the ring's
# turns). Report the convex blocks left: corners, volumes, edge lengths, and whether each is a kit piece at a golden size.
import sys, os, itertools, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring_core as rc
from kit_exact import KIT
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
from scipy.spatial import HalfspaceIntersection
rc.KIT.update(KIT); PHI = rc.PHI
RING = sys.argv[1] if len(sys.argv) > 1 else 'J2'
CORNER = os.environ.get('CORNER', '1') == '1'
r = rc.ring(RING); band, hole = r['band'], r['hole']
big = np.vstack([r['floor'], r['apex'][None]])
solids = [hole] + ([B + (big - B) / PHI ** 2 for B in r['floor']] if CORNER else [])
FB = rc.planes(band); FS = [rc.planes(S) for S in solids]
def interior(H):
    A = np.array(H); n = np.linalg.norm(A[:, :3], axis=1)
    res = linprog([0, 0, 0, -1], A_ub=np.c_[A[:, :3], n], b_ub=-A[:, 3], bounds=[(None, None)] * 3 + [(0, None)], method='highs')
    return (res.x[:3], res.x[3]) if res.success else (None, 0)
def verts(H):
    x, rr = interior(H)
    if x is None or rr < 1e-9: return None
    V = HalfspaceIntersection(np.array(H), x).intersections; out = []
    for v in V:
        if all(np.linalg.norm(v - w) > 1e-8 for w in out): out.append(v)
    return np.array(out)
def side(H, p):
    A = np.array(H)
    lo = linprog(p[:3], A_ub=A[:, :3], b_ub=-A[:, 3], bounds=[(None, None)] * 3, method='highs')
    hi = linprog(-p[:3], A_ub=A[:, :3], b_ub=-A[:, 3], bounds=[(None, None)] * 3, method='highs')
    return lo.fun + p[3], -hi.fun + p[3]
cut = []
for F in FS:
    for e in F:
        if not any(np.linalg.norm(e - q) < 1e-9 or np.linalg.norm(e + q) < 1e-9 for q in cut): cut.append(e)
cells = [list(FB)]
for e in cut:
    nxt = []
    for H in cells:
        lo, hi = side(H, e)
        if lo < -1e-9 and hi > 1e-9: nxt += [H + [e], H + [-e]]
        else: nxt.append(H)
    cells = nxt
rest = []
for H in cells:
    x, rr = interior(H)
    if x is None or rr < 1e-10: continue
    if any(np.all(x @ F[:, :3].T + F[:, 3] < 0) for F in FS): continue
    rest.append(verts(H))
vr = sum(rc.vol(W) for W in rest); RV = rc.vol(band) - rc.vol(hole); vs = sum(rc.vol(S) for S in solids[1:])
print(f'{RING} ring {RV:.9f}; corner pieces {vs:.9f}; residual {RV - vs:.9f}; BSP cells {len(rest)} (volume {vr:.9f})', flush=True)
# greedy convex merging (largest first)
key = lambda v: tuple(np.round(v, 7))
blocks = list(rest)
changed = True
while changed:
    changed = False
    vols = [rc.vol(W) for W in blocks]
    order = np.argsort(vols)
    for a in order:
        A = blocks[a]; ka = {key(v) for v in A}
        best = None
        for b in range(len(blocks)):
            if b == a: continue
            Bk = blocks[b]
            if len(ka & {key(v) for v in Bk}) < 3: continue
            U = np.vstack([A, Bk]); H = ConvexHull(U)
            if abs(H.volume - vols[a] - vols[b]) < 1e-10:
                if best is None or H.volume > best[1]: best = (b, H.volume, U[H.vertices])
        if best:
            b, _, U = best; blocks = [W for i, W in enumerate(blocks) if i not in (a, b)] + [U]; changed = True; break
print(f'convex blocks after merging: {len(blocks)}', flush=True)
kitvol = {k: rc.vol(KIT[k]) for k in ('AXE', 'CLEO', 'FUJI', 'J2', 't1', 't2', 't3', 't5', 'T2', 'I', 'J11')}
sig = {}
for W in blocks:
    W = W[ConvexHull(W).vertices]
    d = sorted(np.round([np.linalg.norm(a - b) for a, b in itertools.combinations(W, 2)], 6))
    s = (len(W), round(rc.vol(W), 9), tuple(d)); sig.setdefault(s, []).append(W)
for (nv, v, d), L in sorted(sig.items(), key=lambda t: -t[0][1]):
    match = [f'{k}@phi^{m}' for k, kv in kitvol.items() for m in range(-6, 1) if abs(kv * PHI ** (3 * m) - v) < 1e-9]
    E = rc.convex_edges(L[0])
    print(f'  {len(L)} x block: {nv} corners, volume {v:.9f}{" = " + ",".join(match) + " by volume" if match else ""}; edges ' +
          ', '.join(sorted(set(f'{l:.4f}' for i, j, l, dd in E))) + '; dihedrals ' + ', '.join(sorted(set(f'{dd:.2f}' for i, j, l, dd in E))), flush=True)
json.dump([W.tolist() for W in blocks], open(os.path.join(rc.HERE, f'../data/residual-{RING}{"" if CORNER else "-nocorner"}.json'), 'w'))
