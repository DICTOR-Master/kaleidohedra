# DICTO #43 Conjecture 1 (the OG's margin), 9 Nov 2026: CERTIFIED t_min(D_k) <= 3/phi^2 beyond the exact range, by ball arithmetic.
# DICTO asked for the route from k = 13 to 20 ("we are closer to a solution on #43, should take priority").
# Why this is rigorous (coincidence pilot, README section 7): from D_5 on every exact coplanarity of the family is forced by its
# symmetry I_h (rotations + mirrors), and no listed point lies on a face without being a corner. So:
#  - exact Q(sqrt5) arithmetic up to D_K0; there the full symmetry action on point labels is computed exactly (act[g][i]);
#  - from D_K0 on, points are Arb balls (python-flint), carried with their exact label permutations: the foot point of face g.F is
#    g.(foot point of F), so the true point set is exactly I_h-invariant and the labels are exact;
#  - each face (float hull proposes it) is CERTIFIED: 3 members with certified non-zero area span its plane; every non-member is
#    certified strictly inside (ball < 0); its member set must be FORCED coplanar by its stabiliser (one stabiliser orbit, or a mirror
#    in the stabiliser with <= 2 classes: two mirror pairs are always coplanar) -> otherwise FAIL (never assume an unproved equality);
#  - closure: every polygon edge in exactly two faces and the face set closed under I_h -> these are all the faces;
#  - t_min(D_{k-1}) <= max over listed points v of D_{k-1} and face representatives (m, d) of D_k of m.v/d: certified UPPER bound,
#    certified <= 3/phi^2. Validation: certified intervals must contain the exact values for k = K0..13 (og-exact-13).
# usage: python -u certified_family.py <five-fold-octet dir> <K0> <KMAX> <out.json>
import sys, os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exact_family.py')).read()
head = src.split("t0 = time.time()")[0]
_K0, _KMAX, _OUT = int(sys.argv[2]), int(sys.argv[3]), os.path.abspath(sys.argv[4])
sys.argv = [sys.argv[0], sys.argv[1], '0', '/dev/null']
exec(head)
import flint
flint.ctx.prec = 600
K0, KMAX, OUT = _K0, _KMAX, _OUT
EXACT = {10: 1.008772389918, 11: 1.018734403814, 12: 1.020351534966, 13: 1.027602382772}   # og-exact-13 (t_min(D_k))
r5 = flint.arb(5).sqrt()
def ball(x): return flint.arb(int(x.a.numerator)) / int(x.a.denominator) + flint.arb(int(x.b.numerator)) / int(x.b.denominator) * r5
FULLX = GX + [tuple(tuple(-x for x in row) for row in M) for M in GX]          # I_h = rotations x {+-1}
FULLB = [[[ball(x) for x in row] for row in M] for M in FULLX]
FULLF = np.array([[[x.f() for x in row] for row in M] for M in FULLX])
REFL = [g for g, M in enumerate(FULLX) if g >= 60 and (M[0][0] + M[1][1] + M[2][2]) == R5(1)]
TGT = flint.arb(9) / 2 - flint.arb(3) / 2 * r5                                   # 3/phi^2
bdot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
bsub = lambda u, v: (u[0] - v[0], u[1] - v[1], u[2] - v[2])
bcross = lambda u, v: (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
bapp = lambda M, v: tuple(M[i][0] * v[0] + M[i][1] * v[1] + M[i][2] * v[2] for i in range(3))
fail = lambda msg: (print('FINAL FAIL:', msg, flush=True), sys.exit(1))
t0 = time.time()
# ---- exact phase: D_0 .. D_K0
W = [tuple(cv(x) for x in v) for v in OG]
for k in range(K0):
    idx = {v: i for i, v in enumerate(W)}; Wf = np.array([fl(v) for v in W])
    F, ne, _ = exact_faces(W, idx, Wf); feet = {}
    for n, d, _ in F.values():
        s = d / dot(n, n); feet[tuple(s * x for x in n)] = 1
    W = list(feet); print(f'exact D_{k + 1}: {len(W)} points ({time.time() - t0:.0f} s)', flush=True)
idx = {v: i for i, v in enumerate(W)}
act = []
for M in FULLX:
    row = []
    for v in W:
        j = idx.get(app(M, v))
        if j is None: fail(f'D_{K0} point set not closed under I_h')
        row.append(j)
    act.append(row)
WB = [tuple(ball(x) for x in v) for v in W]; prev = None
print(f'switch to balls at D_{K0}: {len(WB)} points, I_h action exact ({time.time() - t0:.0f} s)', flush=True)
res = {'mark': 'DICTO #43 Conjecture 1, certified t_min of the OG downward family (ball arithmetic), 2026-11-09 · DICTO · dictospheres.com',
       'K0': K0, 'k': {}}
ok_all = True
for k in range(K0, KMAX + 2):
    t = time.time(); N = len(WB)
    Wf = np.array([[float(x.mid()) for x in v] for v in WB])
    h, groups = float_faces(Wf)
    mems = [frozenset(int(j) for f in g for j in h.simplices[f]) for g in groups]
    fidx = {m: i for i, m in enumerate(mems)}
    if len(fidx) != len(mems): fail(f'D_{k}: repeated member set')
    # I_h action on faces (combinatorial, exact labels) and closure under I_h
    fact = []
    for g in range(120):
        row = []
        for m in mems:
            j = fidx.get(frozenset(act[g][i] for i in m))
            if j is None: fail(f'D_{k}: face set not closed under I_h')
            row.append(j)
        fact.append(row)
    # closure: every polygon edge in exactly two faces
    edges = {}
    for m in mems:
        mm = sorted(m); P = Wf[mm]; c0 = P.mean(0); B = np.linalg.svd(P - c0)[2][:2]
        o = [mm[q] for q in np.argsort(np.arctan2((P - c0) @ B[1], (P - c0) @ B[0]))]
        for e in zip(o, o[1:] + o[:1]): edges[frozenset(e)] = edges.get(frozenset(e), 0) + 1
    if not all(v == 2 for v in edges.values()): fail(f'D_{k}: faces do not close up')
    # orbit representatives and the group element carrying the rep to each face
    rep_of = [None] * len(mems); reps = []
    for i in range(len(mems)):
        if rep_of[i] is not None: continue
        reps.append(i)
        for g in range(120):
            j = fact[g][i]
            if rep_of[j] is None: rep_of[j] = (i, g)
    # certify each representative face
    planes = {}; unforced = 0
    for i in reps:
        mm = sorted(mems[i]); P = Wf[mm]
        best = max(itertools.combinations(range(len(mm)), 3), key=lambda c: np.linalg.norm(np.cross(P[c[1]] - P[c[0]], P[c[2]] - P[c[0]])))
        a, b, c = (WB[mm[q]] for q in best)
        n = bcross(bsub(b, a), bsub(c, a)); d = bdot(n, a)
        nn = bdot(n, n)
        if not nn > 0: fail(f'D_{k}: degenerate face triple')
        out = [w for w in range(N) if w not in mems[i]]
        vals = [bdot(n, WB[w]) - d for w in out]
        if any(not (v < 0) for v in vals):
            if all(v > 0 for v in vals): n = tuple(-x for x in n); d = -d; vals = [-v for v in vals]
        if any(not (v < 0) for v in vals): fail(f'D_{k}: non-member not certified strictly inside face {i} ({sum(1 for v in vals if not v < 0)} unresolved)')
        if len(mm) > 3:
            stab = [g for g in range(120) if fact[g][i] == i]
            orb = set(act[g][mm[0]] for g in stab)
            forced = orb == set(mm) or any(len(set(frozenset((j, act[g][j])) for j in mm)) <= 2 for g in stab if g in REFL)
            if not forced: unforced += 1
        planes[i] = (n, d)
    if unforced: fail(f'D_{k}: {unforced} coplanar face orbits not forced by symmetry (an equality balls cannot prove)')
    # certified t_min(D_{k-1}) against the faces of D_k
    if prev is not None:
        PB, PN = prev; best_up = None; best_mid = -1
        for i in reps:
            n, d = planes[i]
            for v in PB:
                q = bdot(n, v) / d
                if q.mid() > best_mid: best_mid = float(q.mid())
                u = q.upper() if hasattr(q, 'upper') else q.mid() + q.rad()
                if best_up is None or u > best_up: best_up = u
        up = flint.arb(best_up)
        below = up < TGT
        chk = ''
        if (k - 1) in EXACT:
            okx = abs(best_mid - EXACT[k - 1]) < 1e-10; chk = f'  exact {EXACT[k - 1]:.12f} {"MATCH" if okx else "MISMATCH"}'; ok_all &= okx
        ok_all &= bool(below)
        res['k'][k - 1] = {'t_min_upper': str(up), 't_min_float': best_mid, 'below_3_over_phi2_certified': bool(below), 'faces_of_next': len(mems)}
        print(f'  t_min(D_{k - 1}) <= {float(up.mid()):.12f} certified < 3/phi^2: {bool(below)}{chk}', flush=True)
        json.dump(res, open(OUT, 'w'), indent=1)
    print(f'D_{k}: {N} points, {len(mems)} faces certified ({len(reps)} orbits, all coplanarities forced), {len(edges)} edges ({time.time() - t:.0f} s)', flush=True)
    if k == KMAX + 1: break
    # next level: one foot point per face, generated from the rep by its group element; labels follow the face labels
    footrep = {}
    for i in reps:
        n, d = planes[i]; s = d / bdot(n, n); footrep[i] = tuple(s * x for x in n)
    NB = []
    for j in range(len(mems)):
        i, g = rep_of[j]; NB.append(bapp(FULLB[g], footrep[i]))
    act = fact; prev = (WB, N); WB = NB
    rads = max(float(x.rad()) for v in WB for x in v)
    print(f'  next: {len(WB)} foot points, largest ball radius {rads:.1e}', flush=True)
print(f'done in {time.time() - t0:.0f} s')
print('FINAL ok' if ok_all else 'FINAL FAIL: a certified bound or a validation failed')
