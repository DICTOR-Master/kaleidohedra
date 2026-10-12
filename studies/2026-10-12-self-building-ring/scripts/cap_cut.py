# Cut an exact kit complex by a target region and identify the pieces it leaves (2026-10-12).
# Target: the cap phi^m * J2 at a corner of the Lotus seed (step 1: icosahedron of edge phi^2 = 113 pieces), and the band / ring
# inside it. For every complex piece: inside, outside, or straddling; a straddling piece contributes its intersection with the target,
# identified (corners, volume, all distances) against the kit pieces at golden sizes. If every intersection is a kit piece, the
# target is a union of kit pieces.
import sys, os, json, itertools, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring_core as rc
from kit_exact import KIT
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
rc.KIT.update(KIT); PHI = rc.PHI
src = open(os.path.join(rc.HERE, 'ring_blockcut.py')).read()
os.environ.setdefault('TARGETS', '')
exec(src[:src.index('found = []')].replace("STEP = sys.argv[1] if len(sys.argv) > 1 else '2'", "STEP = os.environ.get('STEP', '1')"))
far = np.argmax(np.linalg.norm(KIT['I'] - KIT['I'][0], axis=1)); KIT['AP'] = np.delete(KIT['I'], [0, far], axis=0)
def sig(V):
    V = V[ConvexHull(V).vertices]; U = []
    for v in V:
        if all(np.linalg.norm(v - u) > 1e-5 for u in U): U.append(v)
    V = np.array(U)
    keep = []
    for i in range(len(V)):          # drop points that are convex combinations of the others (on an edge or face)
        O_ = np.delete(V, i, axis=0)
        res = linprog(np.zeros(len(O_)), A_eq=np.vstack([O_.T, np.ones(len(O_))]), b_eq=np.r_[V[i], 1], bounds=[(0, None)] * len(O_), method='highs')
        if not (res.success and np.linalg.norm(O_.T @ res.x - V[i]) < 1e-7): keep.append(i)
    V = V[keep]; return len(V), np.array(sorted(np.linalg.norm(a - b) for a, b in itertools.combinations(V, 2)))
KS = {}
for k in ('I', 'AXE', 'FUJI', 'CLEO', 'J2', 'J11', 'AP', 't1', 't2', 't3', 't5', 'T2'):
    for m in range(-6, 3):
        n_, d = sig(KIT[k] * PHI ** m); KS[(k, m)] = (n_, d)
def ident(V):
    n_, d = sig(V)
    return [f'{k}@phi^{m}' for (k, m), (n2, d2) in KS.items() if n2 == n_ and np.allclose(d, d2, atol=1e-6)]
def clip(V, F):
    """convex piece V intersected with the convex region {F x <= 0}"""
    H = np.vstack([rc.planes(V), F]); A = H[:, :3]; nn = np.linalg.norm(A, axis=1)
    res = linprog([0, 0, 0, -1], A_ub=np.c_[A, nn], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)], method='highs')
    if not res.success or res.x[3] < 1e-9: return None
    P = HalfspaceIntersection(H, res.x[:3]).intersections; out = []
    for p in P:
        if all(np.linalg.norm(p - q) > 1e-5 for q in out): out.append(p)
    if len(out) < 4: return None
    out = np.array(out)
    try:
        if ConvexHull(out).volume < 1e-12: return None
    except Exception:
        return None
    return out
# the Lotus seed's 12 outer corners and its centre
allp = np.vstack(PVs); dd = np.linalg.norm(allp, axis=1); _c = allp[dd > dd.max() - 1e-6]; _, _ci = np.unique(np.round(_c, 6), axis=0, return_index=True); C12 = _c[np.sort(_ci)]   # exact values
A_ = C12[0]; nbrs = C12[np.argsort(np.linalg.norm(C12 - A_, axis=1))[1:6]]
print(f'Lotus seed: corner A at {np.round(A_, 4)}, its 5 neighbours at distance {np.linalg.norm(nbrs[0] - A_):.6f}', flush=True)
results = {}
for m in (2, 1):                       # cap phi^m * J2 at A: corners A + phi^(m-2) (neighbours - A)
    base = A_ + PHI ** (m - 2) * (nbrs - A_); cap = np.vstack([A_[None], base])
    tip = np.vstack([A_[None], A_ + PHI ** (m - 3) * (nbrs - A_)])
    c1 = tip[1:].mean(0); hole = np.vstack([c1 - (tip - c1) / PHI])          # point mirror of J2(phi^(m-2)) through c1
    for label, region, minus in (('cap', cap, None), ('band', cap, tip), ('ring', cap, [tip, hole])):
        F = rc.planes(region)
        parts, bad, tot = [], [], 0.0
        for i, V in enumerate(PVs):
            W = clip(V, F)
            if W is None or rc.vol(W) < 1e-10: continue
            pieces = [W]
            for M in ([] if minus is None else ([minus] if isinstance(minus, np.ndarray) else minus)):
                # subtract a convex solid: split each part by M's planes, keep cells outside M
                nxt = []
                for P_ in pieces:
                    cells = [P_]
                    for e in rc.planes(M):
                        new = []
                        for Q in cells:
                            a = clip(Q, e[None, :]); b = clip(Q, -e[None, :])
                            new += [x for x in (a, b) if x is not None and rc.vol(x) > 1e-10]
                        cells = new
                    nxt += [Q for Q in cells if not np.all(Q.mean(0) @ rc.planes(M)[:, :3].T + rc.planes(M)[:, 3] < -1e-9)]
                pieces = nxt
            for P_ in pieces:
                tot += rc.vol(P_); idn = ident(P_)
                whole = abs(rc.vol(P_) - VOL[i]) < 1e-9
                parts.append((B[i]['r'], whole, idn, P_))
                if not idn: bad.append((B[i]['r'], len(P_), rc.vol(P_)))
        tv = rc.vol(region) - (0 if minus is None else sum(rc.vol(M) for M in ([minus] if isinstance(minus, np.ndarray) else minus)))
        from collections import Counter
        print(f'\ncap phi^{m} J2 at a Lotus corner, {label}: volume {tv:.9f}, parts {len(parts)} (volume {tot:.9f}); '
              f'whole pieces {sum(p[1] for p in parts)}, cut pieces {sum(not p[1] for p in parts)}, cut parts that are NOT kit pieces {len(bad)}', flush=True)
        print('   kit parts: ' + str(dict(Counter((p[0], 'whole' if p[1] else 'cut', p[2][0] if p[2] else '?') for p in parts))), flush=True)
        if bad: print('   unidentified: ' + str(Counter((r_, n_, round(v, 6)) for r_, n_, v in bad)), flush=True)
        results[f'{label}-{m}'] = [{'from': p[0], 'whole': bool(p[1]), 'is': p[2], 'vertices': p[3].tolist()} for p in parts]
json.dump(results, open(os.path.join(rc.HERE, '../data/cap-cut-step1.json'), 'w'))
