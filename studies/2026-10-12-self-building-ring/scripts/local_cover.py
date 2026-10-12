# Local test (2026-10-12). Any cut of the ring R into convex pieces covers a small ball round each boundary point p of R exactly:
# the tangent cones at p of the pieces that contain p (a corner cone, an edge wedge or a face half-space) tile R's own tangent
# cone at p, T(p) = T_band(p) minus T_hole(p). A tangent cone does not depend on the piece's size or on where the rest of the piece
# goes. So, with the pieces restricted to the 120 orientations of the Lotus frame, the possible cones at p form a FINITE list, and
# "can T(p) be tiled by them" is a finite exact-cover problem on the sphere. If it has no solution at some p, R cannot be cut
# into kit pieces of ANY sizes (golden or not) in the frame's orientations.
# Method: list every cone (piece x corner/edge/face x 120 orientations) that lies inside T(p) and misses the hole's cone;
# sample directions in T(p); exact cover (each sample in exactly one chosen cone) by MILP. Fewer constraints than the true problem
# (only sampled directions), so "infeasible" is a proof; "feasible" is only a candidate, re-checked with denser samples.
import sys, os, itertools, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring_core as rc
from kit_exact import KIT
from scipy.optimize import milp, LinearConstraint, Bounds, linprog
from scipy.sparse import lil_matrix, csr_matrix
PHI = rc.PHI
RING = sys.argv[1] if len(sys.argv) > 1 else 'J2'
NS = int(os.environ.get('NS', '20000')); MAXSOL = int(os.environ.get('MAXSOL', '400'))
EXCL = set(os.environ.get('EXCL', '').split(',')) - {''}
EXTRA_P = os.environ.get('POINTS', 'all')
# the 120 frame symmetries (from the big icosahedron)
I = KIT['I'] - KIT['I'].mean(0); G = []
e = min(np.linalg.norm(I[0] - w) for w in I[1:]); nb = [m for m in range(12) if abs(np.linalg.norm(I[m] - I[0]) - e) < 1e-6]
b_ = nb[0]; c_ = [m for m in nb if abs(np.linalg.norm(I[m] - I[b_]) - e) < 1e-6][0]; Ai = np.linalg.inv(np.array([I[0], I[b_], I[c_]]).T)
for i, j, k in itertools.permutations(range(12), 3):
    R = np.array([I[i], I[j], I[k]]).T @ Ai
    if np.allclose(R @ R.T, np.eye(3), atol=1e-6) and all(np.min(np.linalg.norm(I - y, axis=1)) < 1e-6 for y in I @ R.T): G.append(R)
assert len(G) == 120
pieces = {k: V for k, V in KIT.items() if k not in EXCL}
# pentagonal antiprism (icosahedron minus two opposite caps): a J11 part
far = np.argmax(np.linalg.norm(KIT['I'] - KIT['I'][0], axis=1))
if 'AP' not in EXCL: pieces['AP'] = np.delete(KIT['I'], [0, far], axis=0)

def local_cones(V):
    """All tangent cones of convex polytope V at its corners, edge interiors and face interiors, as arrays of unit normals (n.x <= 0)."""
    E = rc.planes(V); out = []
    on = [set(np.where(np.abs(V @ f[:3] + f[3]) < 1e-7)[0]) for f in E]
    for v in range(len(V)):
        out.append(('corner', np.array([E[a][:3] for a in range(len(E)) if v in on[a]])))
    for a, b in itertools.combinations(range(len(E)), 2):
        if len(on[a] & on[b]) >= 2: out.append(('edge', np.array([E[a][:3], E[b][:3]])))
    for a in range(len(E)): out.append(('face', np.array([E[a][:3]])))
    return out
def rays(N):
    """Generators of the cone {x: N x <= 0} (pointed or not): extreme rays from pairs of planes + lineality directions."""
    R = []
    if len(N) == 1:
        n = N[0]; a = np.cross(n, [1, 0, 0] if abs(n[0]) < .9 else [0, 1, 0]); a /= np.linalg.norm(a); b = np.cross(n, a)
        return np.array([a, -a, b, -b, -n])
    if len(N) == 2:
        d = np.cross(N[0], N[1]); d /= np.linalg.norm(d)
        u1 = np.cross(d, N[0]); u1 = u1 if u1 @ N[1] < 0 else -u1
        u2 = np.cross(d, N[1]); u2 = u2 if u2 @ N[0] < 0 else -u2
        return np.array([d, -d, u1 / np.linalg.norm(u1), u2 / np.linalg.norm(u2)])
    for a, b in itertools.combinations(range(len(N)), 2):
        d = np.cross(N[a], N[b]); nd = np.linalg.norm(d)
        if nd < 1e-9: continue
        d /= nd
        for s in (d, -d):
            if np.all(N @ s <= 1e-9): R.append(s)
    return np.unique(np.round(R, 9), axis=0)

cand = {}
for name, V in pieces.items():
    for kind, N in local_cones(V):
        for g in G:
            Ng = np.round(N @ g.T, 9); key = tuple(sorted(map(tuple, Ng)))
            if key not in cand: cand[key] = (name, kind, Ng)
print(f'{RING} ring: {len(pieces)} piece types ({", ".join(pieces)}), {len(cand)} distinct tangent cones in the 120 orientations', flush=True)

rc.KIT.update(KIT)   # build the ring from the snapped (exact) pieces
r = rc.ring(RING); band, hole = r['band'], r['hole']
Fb, Fh = rc.planes(band), rc.planes(hole)
def tcone(F, p):
    return np.array([f[:3] for f in F if abs(p @ f[:3] + f[3]) < 1e-9])
def disjoint(Nc, Nh):
    """interiors of cones {Nc x <= 0} and {Nh x <= 0} disjoint?  LP: find x with Nc x <= -1, Nh x <= -1 (common interior point)."""
    A = np.vstack([Nc, Nh]); res = linprog(np.zeros(3), A_ub=A, b_ub=-np.ones(len(A)), bounds=[(-1e3, 1e3)] * 3, method='highs')
    return res.status != 0
def inside(Nc, Nb):
    R = rays(Nc); return len(Nb) == 0 or np.all(R @ Nb.T <= 1e-9)
def test_point(p, label):
    Nb = tcone(Fb, p)
    on_hole = np.all(p @ Fh[:, :3].T + Fh[:, 3] <= 1e-9)        # a hole face plane, extended, can pass through p without p on the hole
    Nh = tcone(Fh, p) if on_hole else np.zeros((0, 3))
    ok = []
    for key, (name, kind, N) in cand.items():
        if not inside(N, Nb): continue
        if len(Nh) and not disjoint(N, Nh): continue
        ok.append((name, kind, N))
    # samples: directions in T(p) = T_band minus T_hole, away from every candidate boundary
    rng = np.random.default_rng(5); S = rng.normal(size=(NS * 8, 3)); S /= np.linalg.norm(S, axis=1)[:, None]
    if len(Nb): S = S[np.all(S @ Nb.T < -1e-6, axis=1)]
    if len(Nh): S = S[~np.all(S @ Nh.T <= 1e-6, axis=1)]
    S = S[:NS]
    if not ok:
        print(f'  {label}: NO kit cone fits at all -> impossible', flush=True); return False, []
    A = lil_matrix((len(S), len(ok)), dtype=np.int8); keep = np.ones(len(S), bool)
    for j, (name, kind, N) in enumerate(ok):
        m = S @ N.T
        keep &= ~np.any(np.all(m < 1e-6, axis=1) & np.any(np.abs(m) < 1e-6, axis=1)) if False else keep
        hit = np.where(np.all(m < -1e-9, axis=1))[0]; A[hit, j] = 1
    A = csr_matrix(A); cov = np.asarray(A.sum(1)).ravel()
    if np.any(cov == 0):
        print(f'  {label}: {len(ok)} cones fit; {int((cov == 0).sum())} sample directions lie in no fitting cone -> impossible', flush=True)
        return False, ok
    cons = [LinearConstraint(A, 1, 1)]; sols = []
    while len(sols) < MAXSOL:
        res = milp(np.ones(len(ok)), constraints=cons, integrality=np.ones(len(ok)), bounds=Bounds(0, 1), options={'time_limit': 600})
        if res.x is None: break
        sup = np.where(res.x > .5)[0]; sols.append(sup)
        row = np.zeros(len(ok)); row[sup] = 1; cons.append(LinearConstraint(row[None, :], -np.inf, len(sup) - 1))
    if not sols:
        print(f'  {label}: {len(ok)} cones fit; exact cover of {len(S)} directions: none -> impossible', flush=True); return False, ok
    from collections import Counter
    desc = [', '.join(f'{c} x {n} {k}' for (n, k), c in sorted(Counter((ok[j][0], ok[j][1]) for j in sup).items())) for sup in sols]
    print(f'  {label}: {len(ok)} cones fit; {len(sols)}{"+" if len(sols) == MAXSOL else ""} exact covers; kinds: ' + ' | '.join(sorted(set(desc))), flush=True)
    return True, [ok[j] for j in sols[0]]

# the ring's boundary points to test: every corner, every edge midpoint, and the hole apex
pts = []
for P, nm in ((r['floor'], 'floor corner'), (r['top'], 'top corner'), (r['hole_base'], 'hole rim corner')):
    for v in P: pts.append((v, nm))
pts.append((r['hole_apex'], 'hole apex on the floor'))
def poly_edges(P):
    c = P.mean(0); n = np.cross(P[1] - c, P[0] - c); a = P[0] - c; b = np.cross(n, a)
    o = np.argsort([np.arctan2((q - c) @ b, (q - c) @ a) for q in P]); return [(P[o[i]], P[o[(i + 1) % len(o)]]) for i in range(len(o))]
for P, nm in ((r['floor'], 'floor edge'), (r['top'], 'top edge'), (r['hole_base'], 'hole rim edge')):
    for a, b in poly_edges(P): pts.append(((a + b) / 2, nm + ' midpoint'))
for a, b in zip(r['floor'], r['top']): pts.append(((a + b) / 2, 'side edge midpoint'))
for b in r['hole_base']: pts.append(((b + r['hole_apex']) / 2, 'hole edge midpoint'))
# one representative per kind (the rings are symmetric), unless POINTS=all-copies
seen = set(); results = []
for p, nm in pts:
    if EXTRA_P != 'all-copies' and nm in seen: continue
    seen.add(nm); good, ch = test_point(p, nm)
    results.append({'point': p.tolist(), 'kind': nm, 'tileable': good, 'cover': [(n, k) for n, k, _ in ch] if good else None})
json.dump(results, open(os.path.join(rc.HERE, f'../data/local-{RING}{"-ex-" + "-".join(sorted(EXCL)) if EXCL else ""}.json'), 'w'), indent=1)
print('summary:', {d['kind']: d['tileable'] for d in results})
