# certified_orbit.py, DICTO 11 Nov 2026 ("yes take it to 40"): CERTIFIED t_min(D_k) <= 3/phi^2 for k up to 40, built for size.
# Same rigour as certified_family.py (which reached k = 30 but checks every face against every point in ball arithmetic: days at k = 40).
# Changes, each with its own guarantee:
#  1. ORBIT STORAGE. Exact Q(sqrt5) to D_K0, then Arb balls (600 bits) only for ONE foot point per face orbit; every point of the next
#     level is (rep r, group element g) and its ball is g.(ball of r) with the exact I_h matrix (generated on demand).
#  2. LABELS BY SEPARATION. The I_h action on points and faces is read from float kd-trees; it is exact because the true sets are exactly
#     I_h-invariant (point g.p IS a point), every float point is within DELTA of its true point, and distinct points are > SEP apart
#     (checked: nearest-neighbour distance > SEP, every match within MATCH_TOL << SEP).
#  3. FLOAT WITH A PROVED ERROR BOUND for the bulk inequalities. For a face plane (unit normal m, distance d, from balls) and a point w,
#     the float value v = m.w - d differs from the true value by at most ERR = 1e-12 (|w| <= 2, coordinates and m, d accurate to
#     ~1e-15, three-term dot product; ERR has a factor > 100 to spare; |w| <= 2 is checked). So v <= -EPS (EPS = 1e-10 > ERR) proves
#     "strictly inside". Every point with v > -EPS that is not a member is checked in ball arithmetic (must be certified < 0).
#  4. t_min UPPER BOUND in float + ERR_T (1e-10, same argument for m.v/d with d >= 1 checked), compared with 3/phi^2 (margin >= 0.1).
#  5. Forced coplanarity (stabiliser orbit or mirror rule) and closure (every polygon edge in exactly two faces, built from rep polygons
#     mapped by the exact labels; face set closed under I_h) exactly as certified_family.py.
# Validation: t_min(D_k) for k = 10 .. 30 must match certified-family-30.json (t_min_float) to 1e-9.
# Checkpoint per level (rep balls as strings + labels) so a crash resumes. PROGRESS lines; FINAL ok only if every check passed.
# usage: python -u certified_orbit.py <five-fold-octet dir> <K0> <KMAX> <out.json> <checkpoint dir> [resume]
import sys, os, json, time, itertools
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exact_family.py')).read()
head = src.split("t0 = time.time()")[0]
_K0, _KMAX, _OUT, _CK = int(sys.argv[2]), int(sys.argv[3]), os.path.abspath(sys.argv[4]), os.path.abspath(sys.argv[5])
_RESUME = len(sys.argv) > 6
_VAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'certified-family-30.json')
sys.argv = [sys.argv[0], sys.argv[1], '0', '/dev/null']
exec(head)
import numpy as np, flint
from scipy.spatial import ConvexHull, cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
flint.ctx.prec = 600
K0, KMAX, OUT, CK = _K0, _KMAX, _OUT, _CK
os.makedirs(CK, exist_ok=True)
VALID = {int(k): v['t_min_float'] for k, v in json.load(open(_VAL))['k'].items()}
r5 = flint.arb(5).sqrt()
def ball(x): return flint.arb(int(x.a.numerator)) / int(x.a.denominator) + flint.arb(int(x.b.numerator)) / int(x.b.denominator) * r5
FULLX = GX + [tuple(tuple(-x for x in row) for row in M) for M in GX]
FULLB = [[[ball(x) for x in row] for row in M] for M in FULLX]
FULLF = np.array([[[x.f() for x in row] for row in M] for M in FULLX])
REFL = set(g for g, M in enumerate(FULLX) if g >= 60 and (M[0][0] + M[1][1] + M[2][2]) == R5(1))
TGT = flint.arb(9) / 2 - flint.arb(3) / 2 * r5; TGTF = float(TGT.mid())
bdot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
bsub = lambda u, v: (u[0] - v[0], u[1] - v[1], u[2] - v[2])
bcross = lambda u, v: (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
bapp = lambda M, v: tuple(M[i][0] * v[0] + M[i][1] * v[1] + M[i][2] * v[2] for i in range(3))
SEP, MATCH_TOL, EPS, ERR_T = 1e-8, 1e-11, 1e-10, 1e-10
def fail(msg): print('FINAL FAIL:', msg, flush=True); sys.exit(1)
t0 = time.time()

def perm_maps(P, what):
    """I_h action on the rows of P (points or unit normals) as int32 arrays (120, n); exact by separation (guarantee 2)."""
    tr = cKDTree(P); dd = tr.query(P, k=2, workers=-1)[0][:, 1]
    if dd.min() <= SEP: fail(f'{what}: two entries closer than {SEP} ({dd.min():.2e})')
    out = np.empty((120, len(P)), np.int32)
    for g in range(120):
        d, j = tr.query(P @ FULLF[g].T, workers=-1)
        if d.max() > MATCH_TOL: fail(f'{what}: not closed under I_h (g {g}, miss {d.max():.2e})')
        if np.bincount(j, minlength=len(P)).max() != 1: fail(f'{what}: g {g} is not a permutation')
        out[g] = j
    return out

def hull_faces(Wf, tol=1e-9):
    """float hull, coplanar triangles merged (vectorised union over hull adjacency): member arrays + unit normals."""
    h = ConvexHull(Wf); E = h.equations; n = len(E)
    a = np.repeat(np.arange(n), 3); b = h.neighbors.ravel()
    same = np.abs(E[a] - E[b]).max(1) < tol
    G = coo_matrix((np.ones(int(same.sum())), (a[same], b[same])), shape=(n, n))
    nc, lab = connected_components(G, directed=False)
    pairs = np.unique(np.stack([np.repeat(lab, 3), h.simplices.ravel()], 1), axis=0)
    split = np.searchsorted(pairs[:, 0], np.arange(1, nc))
    mems = np.split(pairs[:, 1], split)
    Nf = np.zeros((nc, 3)); np.add.at(Nf, lab, E[:, :3]); Nf /= np.linalg.norm(Nf, axis=1)[:, None]
    return mems, Nf

def polygon_order(P):
    c0 = P.mean(0); B = np.linalg.svd(P - c0)[2][:2]; Q = (P - c0) @ B.T
    return np.argsort(np.arctan2(Q[:, 1], Q[:, 0]))

# ---------------- level K0: exact phase (or resume)
res = {'mark': 'DICTO #43 Conjecture 1, certified t_min of the OG downward family to k = 40 (orbit storage), 2026-11-11 · DICTO · dictospheres.com',
       'K0': K0, 'k': {}}
if _RESUME and os.path.exists(os.path.join(CK, 'last.json')):
    st = json.load(open(os.path.join(CK, 'last.json'))); kstart = st['k']
    footB = [tuple(flint.arb(s) for s in v) for v in st['footB']]; prep = np.array(st['prep'], np.int64); pg = np.array(st['pg'], np.int64)
    prevWf = np.load(os.path.join(CK, 'prevWf.npy')) if st.get('has_prev') else None
    if os.path.exists(OUT): res = json.load(open(OUT))
    print(f'RESUMED at D_{kstart}', flush=True)
    pointB = lambda p: bapp(FULLB[pg[p]], footB[prep[p]])
    Wf = np.einsum('pij,pj->pi', FULLF[pg], np.array([[float(x.mid()) for x in v] for v in footB])[prep])
else:
    W = [tuple(cv(x) for x in v) for v in OG]
    for k in range(K0):
        idx = {v: i for i, v in enumerate(W)}; Wfx = np.array([fl(v) for v in W])
        F, ne, _ = exact_faces(W, idx, Wfx); feet = {}
        for n, d, _ in F.values():
            s = d / dot(n, n); feet[tuple(s * x for x in n)] = 1
        W = list(feet); print(f'exact D_{k + 1}: {len(W)} points ({time.time() - t0:.0f} s)', flush=True)
    WB0 = [tuple(ball(x) for x in v) for v in W]
    pointB = lambda p: WB0[p]
    Wf = np.array([[float(x.mid()) for x in v] for v in WB0]); prevWf = None; kstart = K0
ok_all = True
for k in range(kstart, KMAX + 2):
    t = time.time(); N = len(Wf)
    if np.linalg.norm(Wf, axis=1).max() > 2: fail(f'D_{k}: a point with |w| > 2 (error bound assumes <= 2)')
    pm = perm_maps(Wf, f'D_{k} points')
    mems, Nf = hull_faces(Wf); F = len(mems)
    fm = perm_maps(Nf, f'D_{k} face normals')
    orbit_min = fm.min(0); reps = np.unique(orbit_min); R = len(reps); ridx = {int(r): i for i, r in enumerate(reps)}
    rep_of = np.array([ridx[int(x)] for x in orbit_min]); gof = -np.ones(F, np.int64)
    for g in range(120):
        img = fm[g][reps[rep_of]]; hit = (img == np.arange(F)) & (gof < 0); gof[hit] = g
    if (gof < 0).any(): fail(f'D_{k}: a face not reached from its orbit representative')
    # ---- certify each representative face
    NF = np.zeros((R, 3)); DF = np.zeros(R); planes = []; unforced = 0; polys = []
    for i, r in enumerate(reps):
        mm = np.array(sorted(mems[r])); P = Wf[mm]
        if len(mm) == 3: best = (0, 1, 2)
        else:
            cand = itertools.combinations(range(len(mm)), 3) if len(mm) <= 24 else [(0, len(mm) // 3, 2 * len(mm) // 3)]
            best = max(cand, key=lambda c: np.linalg.norm(np.cross(P[c[1]] - P[c[0]], P[c[2]] - P[c[0]])))
        a, b, c = (pointB(int(mm[q])) for q in best)
        n = bcross(bsub(b, a), bsub(c, a)); d = bdot(n, a)
        if float(d.mid()) < 0: n = tuple(-x for x in n); d = -d
        nn = bdot(n, n)
        if not nn > 0 or not d > 0: fail(f'D_{k}: degenerate face or origin not inside (rep {r})')
        nl = nn.sqrt(); mu = tuple(x / nl for x in n); du = d / nl
        NF[i] = [float(x.mid()) for x in mu]; DF[i] = float(du.mid()); planes.append((n, d))
        if len(mm) > 3:
            stab = [g for g in range(120) if fm[g][r] == r]
            orb = set(int(pm[g][mm[0]]) for g in stab)
            forced = orb == set(mm.tolist()) or any(len(set(frozenset((int(j), int(pm[g][j]))) for j in mm)) <= 2 for g in stab if g in REFL)
            if not forced: unforced += 1
        polys.append(mm[polygon_order(P)])
    if unforced: fail(f'D_{k}: {unforced} coplanar face orbits not forced by symmetry')
    # non-members strictly inside: float with proved error bound, balls for close calls (guarantee 3)
    near = [[] for _ in range(R)]; CH = max(1, int(2e8 // max(R, 1)))
    for s0 in range(0, N, CH):
        V = Wf[s0:s0 + CH] @ NF.T - DF[None, :]
        pi, ri = np.nonzero(V > -EPS)
        for p, q in zip(pi + s0, ri): near[q].append(int(p))
    close_calls = 0
    for i, r in enumerate(reps):
        ms = set(mems[r].tolist()); extra = [p for p in near[i] if p not in ms]
        if not ms.issubset(set(near[i])): fail(f'D_{k}: a member of face {r} is not on its plane in float')
        n, d = planes[i]
        for p in extra:
            close_calls += 1
            if not (bdot(n, pointB(p)) - d < 0): fail(f'D_{k}: point {p} not certified strictly inside face {r}')
    # closure: every polygon edge in exactly two faces (faces = images of rep polygons under the exact labels)
    E = []
    for i, r in enumerate(reps):
        J = np.where(rep_of == i)[0]; poly = polys[i]; e = np.stack([poly, np.roll(poly, -1)], 1)
        mapped = pm[gof[J]][:, e]                         # (|J|, m, 2)
        E.append(np.sort(mapped.reshape(-1, 2), axis=1))
    E = np.concatenate(E); _, cnt = np.unique(E, axis=0, return_counts=True)
    if not (cnt == 2).all(): fail(f'D_{k}: faces do not close up ({int((cnt != 2).sum())} bad edges)')
    # certified t_min(D_{k-1}) against the faces of D_k (guarantee 4)
    if prevWf is not None:
        if DF.min() < 1: fail(f'D_{k}: a face distance below 1 (t bound assumes d >= 1)')
        tmax = -1.0
        for s0 in range(0, len(prevWf), CH):
            tmax = max(tmax, float(((prevWf[s0:s0 + CH] @ NF.T) / DF[None, :]).max()))
        up = tmax + ERR_T; below = up < TGTF - 1e-6
        chk = ''
        if (k - 1) in VALID:
            okx = abs(tmax - VALID[k - 1]) < 1e-9; chk = f'  certified-30 {VALID[k - 1]:.12f} {"MATCH" if okx else "MISMATCH"}'; ok_all &= okx
        ok_all &= bool(below)
        res['k'][str(k - 1)] = {'t_min_upper': up, 't_min_float': tmax, 'below_3_over_phi2_certified': bool(below), 'faces_of_next': F}
        print(f'  t_min(D_{k - 1}) <= {up:.12f} certified < 3/phi^2: {below}{chk}', flush=True)
        json.dump(res, open(OUT, 'w'), indent=1)
    print(f'D_{k}: {N} points, {F} faces certified ({R} orbits, all coplanarities forced), {len(E) // 2} edges, {close_calls} close calls in balls ({time.time() - t:.0f} s)', flush=True)
    print(f'PROGRESS {(k - K0 + 1) / (KMAX - K0 + 2):.3f} level {k}', flush=True)
    if k == KMAX + 1: break
    # next level: one foot point per face orbit, in balls
    footB = []
    for i in range(R):
        n, d = planes[i]; s = d / bdot(n, n); footB.append(tuple(s * x for x in n))
    rads = max(float(x.rad()) for v in footB for x in v)
    if rads > 1e-60: fail(f'D_{k}: ball radii grew to {rads:.1e}')
    footf = np.array([[float(x.mid()) for x in v] for v in footB])
    prep, pg = rep_of.astype(np.int64), gof.astype(np.int64)
    prevWf = Wf
    Wf = np.einsum('pij,pj->pi', FULLF[pg], footf[prep])
    pointB = (lambda fb, pr, gg: (lambda p: bapp(FULLB[gg[p]], fb[pr[p]])))(footB, prep, pg)
    json.dump(dict(k=k + 1, footB=[[x.str(200, radius=True) for x in v] for v in footB], prep=prep.tolist(), pg=pg.tolist(), has_prev=True),
              open(os.path.join(CK, 'last.json'), 'w'))
    np.save(os.path.join(CK, 'prevWf.npy'), prevWf)
    print(f'  next: {len(Wf)} foot points from {R} orbit balls, largest ball radius {rads:.1e}', flush=True)
print(f'done in {time.time() - t0:.0f} s')
print('FINAL ok' if ok_all else 'FINAL FAIL: a certified bound or a validation failed')
