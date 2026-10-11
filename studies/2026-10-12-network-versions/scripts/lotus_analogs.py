# Network versions, step 2 (2026-10-12): every icosahedral form X has a Lotus seed: X(phi^2) holds copies X(1) at all its corners
# (touching) and X(1/phi) at the centre (network_screen.py). Here: the gap left in each, cut by the face planes of the outer form,
# the corner copies and the centre (a binary space partition), keeping the cells that lie in the gap. Reported: the gap volume, the
# number of cells and how many different shapes they come in (congruence classes up to the symmetry). The icosahedron's case must
# give back the Lotus seed's AXE, FUJI and CLEO (60, 20, 20) as a check of the method.
import sys, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
exec(open(__file__.replace('lotus_analogs.py', 'network_screen.py')).read().split('def sat_overlap')[0])
def _group():
    I = ref['I']; G = []
    e = min(np.linalg.norm(I[0] - w) for w in I[1:])
    nb = [m for m in range(12) if abs(np.linalg.norm(I[m] - I[0]) - e) < 1e-6]
    b_ = nb[0]; c_ = [m for m in nb if abs(np.linalg.norm(I[m] - I[b_]) - e) < 1e-6][0]
    Ai = np.linalg.inv(np.array([I[0], I[b_], I[c_]]).T)
    for i, j, k in itertools.permutations(range(12), 3):
        R = np.array([I[i], I[j], I[k]]).T @ Ai
        if np.allclose(R @ R.T, np.eye(3), atol=1e-6) and all(np.min(np.linalg.norm(I - y, axis=1)) < 1e-6 for y in I @ R.T): G.append(R)
    return G
GROUP = _group(); assert len(GROUP) == 120, len(GROUP)
def planes_of(V):
    E = []
    for e in ConvexHull(V).equations:
        if not any(np.linalg.norm(e - q) < 1e-7 for q in E): E.append(e)
    return E
def interior(H):
    A = np.array(H); n = np.linalg.norm(A[:, :3], axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A[:, :3], n], b_ub=-A[:, 3], bounds=[(None, None)] * 3 + [(0, None)], method='highs')
    return (r.x[:3], r.x[3]) if r.success else (None, 0)
def verts(H):
    x, r = interior(H)
    if x is None or r < 1e-7: return None
    V = HalfspaceIntersection(np.array(H), x).intersections
    out = []
    for v in V:
        if all(np.linalg.norm(v - w) > 1e-7 for w in out): out.append(v)
    return np.array(out)
def side_range(H, p):           # min and max of p.x + d over the cell
    A = np.array(H)
    lo = linprog(p[:3], A_ub=A[:, :3], b_ub=-A[:, 3], bounds=[(None, None)] * 3, method='highs')
    hi = linprog(-p[:3], A_ub=A[:, :3], b_ub=-A[:, 3], bounds=[(None, None)] * 3, method='highs')
    return lo.fun + p[3], -hi.fun + p[3]
def inside_poly(x, P):
    return all(x @ e[:3] + e[3] < -1e-9 for e in P)
def lotus(X):
    Xv = ref[X]; outer = Xv * PHI ** 2; centre = Xv / PHI
    copies = []
    for y in Xv:
        d = y / np.linalg.norm(y); j = np.argmax(Xv @ d); copies.append(Xv + (y * PHI ** 2 - Xv[j]))
    solids = [planes_of(c) for c in copies] + [planes_of(centre)]
    cut = []
    for P in solids:
        for e in P:
            if not any(np.linalg.norm(e - q) < 1e-7 or np.linalg.norm(e + q) < 1e-7 for q in cut): cut.append(e)
    cells = [list(planes_of(outer))]
    for e in cut:
        nxt = []
        for H in cells:
            lo, hi = side_range(H, e)
            if lo < -1e-7 and hi > 1e-7: nxt += [H + [e], H + [-e]]
            else: nxt.append(H)
        cells = nxt
    gapcells = []
    for H in cells:
        x, r = interior(H)
        if x is None or r < 1e-9: continue
        if any(inside_poly(x, P) for P in solids): continue
        V = verts(H)
        if V is not None: gapcells.append(V)
    # merge neighbouring cells while the union stays convex, the same join at all 120 symmetric places at once
    key = lambda v: tuple(np.round(v, 5))
    pieces = {i: V for i, V in enumerate(gapcells)}; nid = len(pieces)
    cmap = lambda V: key(V.mean(0))
    while True:
        ids = list(pieces); cens = np.array([pieces[i].mean(0) for i in ids])
        from scipy.spatial import cKDTree; ctree = cKDTree(cens)
        def near(c):
            d, k = ctree.query(c); return ids[k] if d < 1e-4 else None
        vmap = {}
        for i, V in pieces.items():
            for v in V: vmap.setdefault(key(v), set()).add(i)
        vols = {i: ConvexHull(V).volume for i, V in pieces.items()}
        done = False
        for i in sorted(pieces, key=lambda i: vols[i]):
            V = pieces[i]
            for j in sorted(set().union(*[vmap[key(v)] for v in V]) - {i}, key=lambda j: vols[j]):
                W = pieces[j]
                if sum(1 for v in V if key(v) in {key(w) for w in W}) < 3: continue
                U = np.vstack([V, W]); H = ConvexHull(U)
                if abs(H.volume - vols[i] - vols[j]) > 1e-9: continue
                pairs = set()
                ok = True
                for g in GROUP:
                    gi, gj = near(V.mean(0) @ g.T), near(W.mean(0) @ g.T)
                    if gi is None or gj is None or gi == gj: ok = False; break
                    pairs.add(tuple(sorted((gi, gj))))
                flat = [x for p in pairs for x in p]
                if not ok or len(flat) != len(set(flat)): continue
                for gi, gj in pairs:
                    U = np.vstack([pieces[gi], pieces[gj]]); H = ConvexHull(U)
                    del pieces[gi], pieces[gj]; pieces[nid] = U[H.vertices]; nid += 1
                done = True; break
            if done: break
        if not done: break
    gapcells = list(pieces.values())
    vol = sum(ConvexHull(V).volume for V in gapcells)
    total = ConvexHull(outer).volume - len(copies) * ConvexHull(Xv).volume - ConvexHull(centre).volume
    sig = lambda V: (len(V), round(ConvexHull(V).volume, 6), tuple(np.round(sorted(np.linalg.norm(a - b) for a, b in itertools.combinations(V, 2)), 4)))
    classes = {}
    for V in gapcells: classes.setdefault(sig(V), []).append(V)
    print(f'\n{X}: Lotus seed analog = {len(copies)} corner copies + 1 centre; gap volume {total:.6f}, cells found {len(gapcells)} '
          f'(volume {vol:.6f}), {len(classes)} different shapes', flush=True)
    for (n, v, _), L in sorted(classes.items(), key=lambda kv: -len(kv[1])):
        print(f'   {len(L):4d} x  {n} corners, volume {v}', flush=True)
for X in (sys.argv[1:] or ['I', 'D', 'ID', 'RT', 'TI']): lotus(X)
