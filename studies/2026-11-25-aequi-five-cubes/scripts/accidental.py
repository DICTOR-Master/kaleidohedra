# Copy from study 2026-11-24-aequi-certify-extend, used unchanged except where marked 'study 2026-11-25' (groups.py here: the five-cube directions; mixed = RD directions from two or more cubes).
# Certify the dice whose fair point lies (to 60 digits) on a hyperplane h(x) = 0 of depth space where four or more
# face planes meet in one corner only for depths on that hyperplane ("accidental" corners). Across h = 0 the
# combinatorial type changes. Method: the two types T+ (h > 0) and T- (h < 0) are taken from the 60-digit solution
# moved by 1e-6 to each side; each type is certified on its closed half-box (every corner strictly inside every other
# half-space, except slacks that are multiples of h, which vanish only on h = 0); the fairness map F is continuous and
# piecewise smooth, so F(x) - F(y) lies in hull(J+(X), J-(X)) (x - y) on X, and Krawczyk's test with that hull proves
# one and only one zero in X. Then: a 1-dimensional (or lower) certification ON the hyperplane (the restricted
# system) for the zero there, when the solution is claimed to lie exactly on it (see README).
# usage: accidental.py OUT.json
import json, sys, os, itertools, functools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import certify as C
from flint import arb, arb_mat, ctx
ctx.prec = C.PREC

def side_die(rec, hcoef, sgn, delta=1e-6):
    """the die with the same faces at depths moved off the hyperplane by delta to side sgn"""
    x = np.array([float(v) for v in rec['depths'][1:]]); c = np.array(hcoef[1:], float)
    xs = x + sgn * delta * c / (c @ c)
    r2 = dict(rec); r2['depths'] = ['1.0'] + ['%.20f' % v for v in xs]
    s = C.Die(r2); s.setup()
    assert not s.accidental and s.graph_ok, 'side type not clean'
    s.allow_flat = True
    s.xt = [arb(v).mid() for v in rec['depths'][1:]]            # back to the solution's midpoint for the box
    return s

def slack_ok_halfbox(s, h, sgn, r):
    """every corner of s's type strictly inside every other half-space on X ∩ {sgn*h >= 0}, X = x~ ± r;
    slacks proportional to h (vanishing exactly on h = 0) are accepted when they have the sign of sgn*h"""
    bad = 0; prop = 0
    for vi, I in enumerate(s.full):
        A = s.A[vi]
        for f in range(s.N):
            if f in I: continue
            c = [C.dot(s.n[f], A[o]) for o in range(s.m)]; c[s.orb[f]] -= 1
            c = [-x for x in c]                       # slack = d_f - n_f.v = sum_o c_o d_o
            sl0 = c[0] + sum((c[k] * s.xt[k - 1] for k in range(1, s.m)), arb(0))
            L = sum((abs(c[k]) for k in range(1, s.m)), arb(0)) * r
            if (sl0 - L) > 0: continue
            # proportional to h?  c = lam * h with lam of sign sgn
            k0 = max(range(s.m), key=lambda k: abs(float(h[k].mid())))
            lam = c[k0] / h[k0]
            if all((c[k] - lam * h[k]).contains(0) and abs(float((c[k] - lam * h[k]).rad())) < 1e-60 for k in range(s.m)) and (lam * sgn) > 0:
                prop += 1; continue
            bad += 1
    return bad, prop


# ---- several hyperplanes (k forms): one type per feasible sign orthant; the Jacobian enclosure is the hull over all
def side_dice_multi(rec, Hf, delta=1e-6, tries=int(os.environ.get('TRIES', 4000))):
    """one type per sign orthant met by points x~ + delta*u (u: random unit directions, seed 1, plus the axes)"""
    x = np.array([float(v) for v in rec['depths'][1:]]); n = len(x); rng = np.random.default_rng(1)
    U = list(np.eye(n)) + list(-np.eye(n)) + [u / np.linalg.norm(u) for u in rng.normal(size=(tries, n))]
    out = {}
    for u in U:
        y = x + delta * u; hv = [h[0] + np.dot(h[1:], y) for h in Hf]
        if min(abs(v) for v in hv) < 1e-9 * delta: continue
        sg = tuple(1 if v > 0 else -1 for v in hv)
        if sg in out: continue
        r2 = dict(rec); r2['depths'] = ['1.0'] + ['%.20f' % v for v in y]
        sd = C.Die(r2); sd.setup()
        if sd.accidental or not sd.graph_ok: continue
        sd.allow_flat = True; sd.xt = [arb(v).mid() for v in rec['depths'][1:]]; out[sg] = sd
    return out
def slack_ok_orthant(s, Hs, sg, r):
    bad = 0
    for vi, I in enumerate(s.full):
        A = s.A[vi]
        for f in range(s.N):
            if f in I: continue
            c = [C.dot(s.n[f], A[o]) for o in range(s.m)]; c[s.orb[f]] -= 1; c = [-x for x in c]
            sl0 = c[0] + sum((c[k] * s.xt[k - 1] for k in range(1, s.m)), arb(0))
            L = sum((abs(c[k]) for k in range(1, s.m)), arb(0)) * r
            if (sl0 - L) > 0: continue
            okp = False
            for h, sgn in zip(Hs, sg):
                k0 = max(range(s.m), key=lambda k: abs(float(h[k].mid()))); lam = c[k0] / h[k0]
                if all((c[k] - lam * h[k]).contains(0) and abs(float((c[k] - lam * h[k]).rad())) < 1e-60 for k in range(s.m)) and (lam * sgn) > 0: okp = True; break
            if not okp: okp = cone_comb(c, Hs, sg)
            bad += not okp
    return bad
def cone_comb(c, Hs, sg):
    """is the slack form c (vanishing at the corner point) a nonnegative combination of the forms sg_i h_i?
    (then it is >= 0 on the orthant, zero only on its boundary). Support from NNLS in floats, coefficients then
    solved in ball arithmetic and the identity c = sum lam_i sg_i h_i checked coefficient by coefficient."""
    from scipy.optimize import nnls
    m = len(c); G = np.array([[sgn * float(h[k].mid()) for h, sgn in zip(Hs, sg)] for k in range(m)])
    lam, res = nnls(G, np.array([float(x.mid()) for x in c]))
    if res > 1e-9: return False
    S = [i for i in range(len(Hs)) if lam[i] > 1e-12]
    if not S: return False
    # choose |S| rows giving an invertible system, solve exactly in arb
    for rows in itertools.combinations(range(m), len(S)):
        M = arb_mat([[sg[i] * Hs[i][k] for i in S] for k in rows])
        try: L = M.solve(arb_mat([[c[k]] for k in rows]))
        except Exception: continue
        lams = [L[j, 0] for j in range(len(S))]
        if not all(l > 0 for l in lams): return False
        return all((c[k] - sum((lams[j] * sg[S[j]] * Hs[S[j]][k] for j in range(len(S))), arb(0))).contains(0)
                   and float((c[k] - sum((lams[j] * sg[S[j]] * Hs[S[j]][k] for j in range(len(S))), arb(0))).rad()) < 1e-60 for k in range(m))
    return False
def regions_expected(Hf):
    """regions of a central arrangement: 2k in the plane (k distinct lines); on the sphere (n = 3) by Euler's formula"""
    H = np.array([h[1:] for h in Hf], float); H = H / np.linalg.norm(H, axis=1)[:, None]; n = H.shape[1]
    if n == 1: return 2
    if n == 2: return 2 * len(H)
    if len(H) == 2 and np.linalg.matrix_rank(H, tol=1e-9) == 2: return 4   # study 2026-11-25: two distinct central hyperplanes cut R^n into 4 regions, any n
    if n != 3: return None
    lines = []
    for i, j in itertools.combinations(range(len(H)), 2):
        d = np.cross(H[i], H[j]); d /= np.linalg.norm(d)
        if not any(abs(abs(d @ L) - 1) < 1e-9 for L in lines): lines.append(d)
    return 2 - 2 * len(lines) + sum(2 * sum(1 for L in lines if abs(h @ L) < 1e-9) for h in H)
def run_multi(rec, s0, H):
    # distinct hyperplanes up to scale
    Hs = []
    for c in H:
        k0 = max(range(s0.m), key=lambda k: abs(float(c[k].mid())))
        cn = [x / c[k0] for x in c]
        if not any(all((a - b).contains(0) for a, b in zip(cn, d)) for d in Hs): Hs.append(cn)
    n = s0.m - 1
    # refine the arrangement: every slack form that vanishes at the point in some side type is a further wall
    for it in range(5):
        Hf = [[float(x.mid()) for x in h] for h in Hs]; sides = side_dice_multi(rec, Hf); added = 0
        for sd in sides.values():
            for vi, I in enumerate(sd.full):
                A = sd.A[vi]
                for f in range(sd.N):
                    if f in I: continue
                    c = [C.dot(sd.n[f], A[o]) for o in range(sd.m)]; c[sd.orb[f]] -= 1; c = [-x for x in c]
                    sl0 = c[0] + sum((c[k] * sd.xt[k - 1] for k in range(1, sd.m)), arb(0))
                    if abs(float(sl0.mid())) > 1e-50: continue
                    k0 = max(range(s0.m), key=lambda k: abs(float(c[k].mid()))); cn = [x / c[k0] for x in c]
                    if not any(all((a - b).contains(0) for a, b in zip(cn, d)) for d in Hs): Hs.append(cn); added += 1
        if not added: break
    if not sides: out = dict(n_hyperplanes=len(Hs)); out['split_krawczyk'] = out['tight'] = dict(ok=False, why='no clean side type'); return out
    out = dict(regions_expected=regions_expected(Hf), n_hyperplanes=len(Hs), hyperplanes=[[x.str(20, radius=False) for x in h] for h in Hs], orthants=len(sides),
               h_at_midpoint=[(h[0] + sum((h[k] * s0.xt[k - 1] for k in range(1, s0.m)), arb(0))).str(5) for h in Hs])
    def attempt(r):
        ra = arb(r); Js = []
        for sg, sd in sides.items():
            if slack_ok_orthant(sd, Hs, sg, r): return None
            X = [C.D(arb(v, ra), [arb(1) if j == i else arb(0) for j in range(n)]) for i, v in enumerate(sd.xt)]
            Fx, sok = sd.F(X)
            if not sok: return None
            Js.append([[Fx[i].g[j] for j in range(n)] for i in range(n)])
        J = arb_mat([[functools.reduce(lambda a, b: a.union(b), [Jx[i][j] for Jx in Js]) for j in range(n)] for i in range(n)])
        sd = next(iter(sides.values())); F0, _ = sd.F([C.D(v, [arb(0)] * n) for v in sd.xt])
        f0 = arb_mat([[F0[i].v] for i in range(n)])
        Jm = arb_mat([[arb(J[i, j].mid()) for j in range(n)] for i in range(n)]); Cm = Jm.inv()
        Cq = arb_mat([[arb(Cm[i, j].mid()) for j in range(n)] for i in range(n)])
        Id = arb_mat([[arb(1) if i == j else arb(0) for j in range(n)] for i in range(n)])
        K = -(Cq * f0) + (Id - Cq * J) * arb_mat([[arb(0, ra)] for _ in range(n)])
        if all(K[i, 0].abs_upper() < ra for i in range(n)):
            return dict(ok=True, r=r, dev=max(float(K[i, 0].abs_upper()) for i in range(n)),
                        h_on_enclosure=[(h[0] + sum((h[k] * (sd.xt[k - 1] + K[k - 1, 0]) for k in range(1, s0.m)), arb(0))).str(5) for h in Hs])
        return None
    res = None
    for e in range(4, 25):
        res = attempt(10.0 ** (-e / 2))
        if res: break
    out['split_krawczyk'] = res or dict(ok=False); out['tight'] = attempt(1e-40) or dict(ok=False)
    return out

def run(rec):
    s0 = C.Die(rec); s0.setup()
    if rec.get('refine') and s0.accidental:
        # refine the double-precision depths first with one side's type (F is C^1 across h = 0)
        e = s0.accidental[0]; A = s0.A[e['corner']]
        h0 = [C.dot(s0.n[e['plane']], A[o]) for o in range(s0.m)]; h0[s0.orb[e['plane']]] -= 1
        sd = side_die(rec, [float(x.mid()) for x in h0], 1); sd.newton()
        rec = dict(rec, depths=['1.0'] + [x.str(75, radius=False) for x in sd.xt], refine=False)
        s0 = C.Die(rec); s0.setup()
    acc = s0.accidental
    # all accidental forms must be one hyperplane (up to scale)
    H = []
    for e in acc:
        f = e['plane']; t = e['triple']; A = s0.A[e['corner']]
        c = [C.dot(s0.n[f], A[o]) for o in range(s0.m)]; c[s0.orb[f]] -= 1; H.append(c)
    h = H[0]; k0 = max(range(s0.m), key=lambda k: abs(float(h[k].mid())))
    one = all(all((c[k] - (c[k0] / h[k0]) * h[k]).contains(0) for k in range(s0.m)) for c in H)
    hval = h[0] + sum((h[k] * s0.xt[k - 1] for k in range(1, s0.m)), arb(0))
    out = dict(label=rec['label'], sid=rec['sid'], study=rec['study'], n_accidental=len(acc), one_hyperplane=bool(one),
               h=[x.str(30, radius=False) for x in h], h_at_midpoint=hval.str(5))
    if not one:
        out.update(run_multi(rec, s0, H)); return out
    sides = {}
    for sgn in (1, -1):
        s = side_die(rec, [float(x.mid()) for x in h], sgn); sides[sgn] = s
    n = s0.m - 1
    def attempt(r):
        ra = arb(r)
        ok_types = True; Js = []
        for sgn, s in sides.items():
            bad, prop = slack_ok_halfbox(s, h, sgn, r)
            if bad: ok_types = False; break
            X = [C.D(arb(v, ra), [arb(1) if j == i else arb(0) for j in range(n)]) for i, v in enumerate(s.xt)]
            Fx, sok = s.F(X)
            if not sok: ok_types = False; break
            Js.append([[Fx[i].g[j] for j in range(n)] for i in range(n)])
        if not ok_types: return None
        J = arb_mat([[Js[0][i][j].union(Js[1][i][j]) for j in range(n)] for i in range(n)])
        # F at the midpoint, with the type of the side the midpoint is on (both agree on h = 0 by continuity)
        sg = 1 if hval > 0 else (-1 if hval < 0 else 1)
        s = sides[sg]
        F0, _ = s.F([C.D(v, [arb(0)] * n) for v in s.xt])
        f0 = arb_mat([[F0[i].v] for i in range(n)])
        Jm = arb_mat([[arb(J[i, j].mid()) for j in range(n)] for i in range(n)])
        Cm = Jm.inv(); Cq = arb_mat([[arb(Cm[i, j].mid()) for j in range(n)] for i in range(n)])
        Id = arb_mat([[arb(1) if i == j else arb(0) for j in range(n)] for i in range(n)])
        K = -(Cq * f0) + (Id - Cq * J) * arb_mat([[arb(0, ra)] for _ in range(n)])
        if all(K[i, 0].abs_upper() < ra for i in range(n)):
            return dict(ok=True, r=r, dev=max(float(K[i, 0].abs_upper()) for i in range(n)), fres=max(float(f0[i, 0].abs_upper()) for i in range(n)),
                       enclosure=[(s.xt[i] + K[i, 0]).str(30, radius=True) for i in range(n)],
                       h_on_enclosure=(h[0] + sum((h[k] * (s.xt[k - 1] + K[k - 1, 0]) for k in range(1, s0.m)), arb(0))).str(5))
        return None
    res = None
    for e in range(4, 25):
        res = attempt(10.0 ** (-e / 2))
        if res: break
    out['split_krawczyk'] = res or dict(ok=False)
    out['tight'] = attempt(1e-40) or dict(ok=False)
    return out

if __name__ == '__main__':
    outs = []
    if os.environ.get('DICE'):      # usage: DICE=dice.json CERT=certify-out.jsonl accidental.py OUT.json
        recs = json.load(open(os.environ['DICE'])); acc = {json.loads(L)['sid'] for L in open(os.environ['CERT']) if json.loads(L)['status'] == 'accidental'}
        todo = [r for r in recs if r['sid'] in acc]
    else:
        recs = C.load_all(); todo = [[x for x in recs if x['study'].startswith(st) and x['sid'] == sid][0]
                                     for st, sid in [('2026-11-19', 504), ('2026-11-20', 95), ('2026-11-20', 124)]]
    for rec in todo:
        o = run(rec); print(json.dumps(o)); outs.append(o)
    json.dump(outs, open(sys.argv[1], 'w'), indent=1)
    print('FINAL ok' if all(o['split_krawczyk'].get('ok') and o['tight'].get('ok') and o.get('orthants', 0) == o.get('regions_expected', 0) for o in outs) else 'NOT all certified')
