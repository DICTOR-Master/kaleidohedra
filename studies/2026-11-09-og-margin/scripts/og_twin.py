# og_twin.py, DICTO 11 Nov 2026 ("maybe a 5D penrose type" -> "yes run the twin test"). In a cut-and-project (Penrose-type) set the
# Galois twins of the points (sqrt5 -> -sqrt5: the 'perpendicular space' of the 6D icosahedral picture) stay inside a bounded WINDOW,
# and the window fixes all averages. Test on the exact OG family D_0..D_K: twin of every corner, its radius range, whether the twin
# set is bounded across levels, convex position of the twin set, and the growth of denominators (a lattice shadow keeps them bounded).
# Exact Q(sqrt5) as exact_family.py. Controls: corner counts match the exact counts; real floats match the float family radii.
# usage: python -u og_twin.py <five-fold-octet dir> <K> <out.json>
import sys, os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exact_family.py')).read()
head = src.split("t0 = time.time()")[0]
_K, _OUT = int(sys.argv[2]), os.path.abspath(sys.argv[3])
sys.argv = [sys.argv[0], sys.argv[1], '0', '/dev/null']
exec(head)
K, OUT = _K, _OUT
from scipy.spatial import ConvexHull
EXACT_COUNTS = {0: 102, 1: 80, 2: 132, 3: 140, 4: 162, 5: 200, 6: 192, 7: 260, 8: 312, 9: 500}   # corners of D_k (cut_lemma table)
def twinf(x):                                             # exact-safe: a - b sqrt5 = (a^2 - 5 b^2) / (a + b sqrt5), no cancellation
    if x.b == 0: return float(x.a)
    re = float(x.a) + float(x.b) * S5
    if abs(re) < 1e-6: return float(x.a) - float(x.b) * S5
    return float(x.a * x.a - 5 * x.b * x.b) / re
def hull_edges(P):
    h = ConvexHull(P / np.abs(P).max()); E = set()
    for t in h.simplices:
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2])): E.add((min(a, b), max(a, b)))
    return E
t0 = time.time(); rows = []; ok = True
W = [tuple(cv(x) for x in v) for v in OG]
for k in range(K + 1):
    idx = {v: i for i, v in enumerate(W)}; Wf = np.array([fl(v) for v in W])
    F, ne, cors = exact_faces(W, idx, Wf)
    corners = sorted(set(i for mem in F for i in mem))      # face member sets are the keys; corners = points on some face
    C = [W[i] for i in corners]
    Cr = np.array([fl(v) for v in C]); Ct = np.array([[twinf(x) for x in v] for v in C])
    rr, rt = np.linalg.norm(Cr, axis=1), np.linalg.norm(Ct, axis=1)
    hv = len(ConvexHull(Ct / np.abs(Ct).max()).vertices) if len(Ct) > 3 else 0
    Er, Et = hull_edges(Cr), hull_edges(Ct)                  # scutoid-type exchange between the twins: neighbour pairs kept / swapped
    shared = len(Er & Et) / len(Er)
    # VACUUS TEST (DICTO 11-11 "its a vacuus"): each real face's member set in twin coordinates spans a plane; its distance from O
    # relative to the twin size of the face (max twin radius of its members). -> 0 means the twin faces become sheets through the centre.
    ti = {i: j for j, i in enumerate(corners)}; vac = []
    for mem in F:
        mm = [ti[i] for i in mem if i in ti]
        if len(mm) < 3: continue
        P = Ct[mm]; c0 = P.mean(0); nrm = np.linalg.svd(P - c0)[2][2]
        vac.append(abs(nrm @ c0) / np.linalg.norm(P, axis=1).max())
    vac = np.array(vac)
    vreal = []                                                # same ratio with real coordinates (control: a real face is far from O)
    for mem in F:
        mm = [ti[i] for i in mem if i in ti]
        if len(mm) < 3: continue
        P = Cr[mm]; c0 = P.mean(0); nrm = np.linalg.svd(P - c0)[2][2]; vreal.append(abs(nrm @ c0) / np.linalg.norm(P, axis=1).max())
    vreal = np.array(vreal); ok &= bool(vreal.min() > 0.5)
    # NON-CONVEX SHEETS (DICTO 11-11): each face's corners in their REAL cyclic order, drawn in twin coordinates in the twin plane:
    # convex / non-convex (turns change sign) / self-crossing (turning number not +-1). Control: in real coordinates all convex.
    def shape(P, order):
        c0 = P.mean(0); B = np.linalg.svd(P - c0)[2][:2]; Q = (P[order] - c0) @ B.T
        e = np.roll(Q, -1, 0) - Q; cr = e[:, 0] * np.roll(e, -1, 0)[:, 1] - e[:, 1] * np.roll(e, -1, 0)[:, 0]
        ang = np.arctan2(cr, (e * np.roll(e, -1, 0)).sum(1)); turn = round(abs(ang.sum()) / (2 * np.pi))
        if turn != 1: return 'crossing'
        return 'convex' if (cr > 0).all() or (cr < 0).all() else 'nonconvex'
    kinds = {'convex': 0, 'nonconvex': 0, 'crossing': 0}; real_all_convex = True
    for mem in F:
        mm = [ti[i] for i in mem if i in ti]
        if len(mm) < 4: kinds['convex'] += 1; continue           # triangles are always convex
        P = Cr[mm]; c0 = P.mean(0); B = np.linalg.svd(P - c0)[2][:2]; Q = (P - c0) @ B.T
        order = np.argsort(np.arctan2(Q[:, 1], Q[:, 0]))         # real cyclic order
        real_all_convex &= shape(Cr[mm], order) == 'convex'
        kinds[shape(Ct[mm], order)] += 1
    ok &= bool(real_all_convex)
    dig = max(x.digits() for v in C for x in v)
    cnt_ok = (k not in EXACT_COUNTS) or len(C) == EXACT_COUNTS[k]
    ok &= bool(cnt_ok)
    if k <= 7:                                                   # control: exact-safe twin = plain twin where no cancellation
        ok &= bool(abs(twinf(C[0][0]) - (float(C[0][0].a) - float(C[0][0].b) * S5)) < 1e-12)
    row = dict(k=k, corners=len(C), real_R=float(rr.max()), real_r_min=float(rr.min()), twin_max=float(rt.max()), twin_min=float(rt.min()),
               twin_over_real=float(rt.max() / rr.max()), twin_hull_vertices=hv, max_digits=int(dig), vacuus_ratio_median=float(np.median(vac)), sheet_kinds=kinds, vacuus_ratio_max=float(vac.max()), vacuus_ratio_min=float(vac.min()), edges_real=len(Er), edges_twin=len(Et), shared_edge_share=shared)
    rows.append(row)
    print(f'PROGRESS {(k + 1) / (K + 1):.3f}', flush=True)
    print(f"k {k:2d}: corners {len(C):5d} (count ok {cnt_ok}) | real radius {rr.min():.4f}..{rr.max():.4f} | TWIN radius {rt.min():.3e}..{rt.max():.3e} "
          f"| twin/real {rt.max() / rr.max():.3e} | twin hull vertices {hv}/{len(C)} | neighbour pairs shared real/twin {shared:.3f} ({len(Er & Et)}/{len(Er)}; twin {len(Et)}) | VACUUS ratio twin median {np.median(vac):.3e} max {vac.max():.3e} (real: {np.median(vreal):.3f}) | twin sheets {kinds} | max digits {dig} | {time.time() - t0:.0f}s", flush=True)
    feet = {}
    for n, d, _ in F.values():
        s = d / dot(n, n); feet[tuple(s * x for x in n)] = 1
    W = list(feet)
json.dump(rows, open(OUT, 'w'), indent=1)
tw = [r['twin_max'] for r in rows]
print('twin radius by level:', [f'{x:.3e}' for x in tw])
print('bounded window? twin max grows by factor', f'{tw[-1] / tw[0]:.3e}', 'over the run; digits', [r['max_digits'] for r in rows])
print('FINAL ok' if ok else 'FINAL FAIL: corner counts differ from the exact counts')
