"""Task 1: exact proof of the 42 same-scale coincidences (data/aequi.json `coincidences`; screen data/scan42.json).
Lemma (monotone cells) + shadow count, as in README, Theorem 8 and Lemma 9:
  For a set S of orbits of a fair die with depth vector d*, let d(s) = d* with every S depth multiplied by s. The union U(s) of the
  central projections of the S faces is {x : max_S u.x/(s d) >= max_rest u.x/d}; it shrinks strictly as s grows (O is inside, so the
  S maximum is positive on U(s), and U(s) has boundary arcs against non-S faces). So area U(s) = 4 pi |S|/N happens at one s only,
  and s = 1 (the fair die) is that s.
  We exhibit s0 with area U(s0) = 4 pi |S|/N EXACTLY: at s0 the S planes lie on the planes of one station (I_k, D_k) and the
  B planes (the faces next to them) on the planes of RT_k (or I_k) at the same k. Then
    (i)  Q = the polytope of the S and B planes alone is exact in Q(sqrt5) (unnormalised normals, station offsets below);
    (ii) every corner of every S face of Q lies strictly inside every plane of the other orbits at the certified depths
         (ball arithmetic on the certified enclosures), so the S faces of the die at s0 are the S faces of Q;
    (iii) every side of every S face of Q lies in a mirror of the icosahedron group and every corner on a rotation axis (exact),
         so by the shadow-dice theorem (study 2026-11-24-aequi-exact-dice, Theorem 2(a)) each S face projects onto a whole number
         k_i of the 120 mirror triangles; arb pins k_i; the check is sum k_i = 120 |S| / N.
  Hence s0 = 1: the die's S and B planes lie EXACTLY on the station planes, and its depth ratio is the station ratio.
Station offsets at scale 1 (plane q.x = h, q the unnormalised normal):
  two-fold C6 q = (1,0,0), h = phi; RT24 q = (1,phi,1/phi), h = 2 phi        (RT0: rhombi through the midsphere points, depth phi)
  three-fold O8 q = (1,1,1), I12 q = (0,1/phi,phi), h = phi^2                (I0 faces, depth phi^2/sqrt3)
  five-fold D12 q = (0,phi,1), h = phi^2                                       (D0 faces, depth phi^2/sqrt(phi+2))
-> data/exact42.json, prints FINAL ok only if all 42 are proved."""
import json, os, sys, itertools, gzip, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.normpath(os.path.join(HERE, '..', '..'))
EXD = os.path.join(ST, '2026-11-24-aequi-exact-dice', 'scripts'); sys.path.insert(0, EXD)
from groups import DIRS, DFAM
from qsqrt5 import K, PHI, IPHI, dot, cross, sub, scl, cyc_signs
from flint import arb, ctx
ctx.prec = 300
ONE, Z = K(1), K(0)
PAT = {'C6': (ONE, Z, Z), 'O8': (ONE, ONE, ONE), 'D12': (Z, PHI, ONE), 'I12': (Z, IPHI, PHI), 'RT24': (ONE, PHI, IPHI)}
H = {'C6': PHI, 'RT24': PHI * 2, 'O8': PHI * PHI, 'I12': PHI * PHI, 'D12': PHI * PHI}
FOLD = {'C6': 2, 'RT24': 2, 'O8': 3, 'I12': 3, 'D12': 5}
EX = {}
for i, f in enumerate(DFAM):
    if f not in PAT: continue
    m = [w for w in cyc_signs(PAT[f]) if np.abs(np.array([float(x) for x in w]) / np.linalg.norm([float(x) for x in w]) - DIRS[i]).max() < 1e-9]
    assert len(m) == 1; EX[i] = m[0]
MIRRORS = [EX[i] for i, f in enumerate(DFAM) if f in ('C6', 'RT24')]; AXES = [EX[i] for i in EX]
assert len(MIRRORS) == 30 and len(AXES) == 62      # 15 mirrors (each normal twice, +-)
S5 = arb(5).sqrt()
def A(x): return arb(x.a.numerator) / x.a.denominator + arb(x.b.numerator) / x.b.denominator * S5
def norm_arb(q): return (A(dot(q, q))).sqrt()
def det3(a, b, c): return dot(a, cross(b, c))
def solve3(q, h):
    """the point x with q[t].x = h[t] (Cramer, exact); None if the planes do not meet in one point"""
    D = det3(*q)
    if D.sign() == 0: return None
    cols = []
    for t in range(3):
        M = [list(r) for r in q]
        rows = [tuple(h[r] if c == t else M[r][c] for c in range(3)) for r in range(3)]
        cols.append(det3(*rows) / D)
    return tuple(cols)
def sph_area(P):
    P = [[A(x) for x in v] for v in P]; tot = arb(0)
    def d3(a, b, c): return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])
    def dt(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    for i in range(1, len(P) - 1):
        a, b, c = P[0], P[i], P[i + 1]
        la, lb, lc = dt(a, a).sqrt(), dt(b, b).sqrt(), dt(c, c).sqrt()
        tot += 2 * arb.atan2(abs(d3(a, b, c)), la * lb * lc + dt(a, b) * lc + dt(a, c) * lb + dt(b, c) * la)
    return tot
def fam(o): return o.split('/')[0].split('+')

# ---------- data: dice and certified enclosures (depths relative to orbit 0 = 1) ----------
def load_die(src, sid):
    if src == '4553':
        for f in glob.glob(os.path.join(ST, '2026-11-19-aequi-complete', 'data', 'dice', '%04d-*.json' % int(sid))):
            d = json.load(open(f))
            if str(d['sid']) == str(sid):
                return dict(idx=d['face_directions'], sizes=d['orbit_sizes'], orbits=d['orbits'], N=int(d['N']), depths=d['depths_60_digits'])
    b = src.split()[1]
    for d in json.load(open(os.path.join(ST, '2026-11-24-aequi-certify-extend', 'data', 'dice%s-new.json' % b))):
        if str(d['sid']) == str(sid):
            lab = d['label'].split(': ', 1)[1]; ev = lambda x: eval(x) if isinstance(x, str) else x
            return dict(idx=ev(d['idx']), sizes=ev(d['sizes']), orbits=[o.strip() for o in lab.split(' + ')], N=int(d['N']), depths=ev(d['depths']))
def enclosure(src, sid):
    """certified enclosure of the fair depths (orbits 1..m-1; orbit 0 = 1), with where it comes from"""
    def parse(t): t = eval(t) if isinstance(t, str) else t; return t['ok'], [arb(s) for s in t['enclosure']]
    if src == '4553':
        for l in gzip.open(os.path.join(ST, '2026-11-24-aequi-certify-4404', 'data', 'certify4404.jsonl.gz'), 'rt'):
            d = json.loads(l)
            if str(d['sid']) == str(sid) and d['status'] == 'certified': ok, e = parse(d['tight']); return ok, e, 'certify-4404 tight box'
        for d in json.load(open(os.path.join(ST, '2026-11-24-aequi-certify-4404', 'data', 'accidental4404.json'))):
            if str(d['sid']) == str(sid): ok, e = parse(d['tight']); return ok and d['split_krawczyk']['ok'], e, 'certify-4404 split box (tight)'
        for l in open(os.path.join(ST, '2026-11-24-aequi-certify-extend', 'data', 'certify-pass1.jsonl')):
            d = json.loads(l)
            if d['study'] == '2026-11-19-aequi-complete' and str(d['sid']) == str(sid) and d['status'] == 'certified':
                ok, e = parse(d['tight']); return ok, e, 'certify-extend Part 1 tight box'
    b = src.split()[1]
    for l in gzip.open(os.path.join(ST, '2026-11-24-aequi-certify-extend', 'data', 'certify%s.jsonl.gz' % b), 'rt'):
        d = json.loads(l)
        if str(d['sid']) == str(sid) and d['status'] == 'certified': ok, e = parse(d['tight']); return ok, e, 'certify-extend %s tight box' % b
    raise KeyError((src, sid))

def step(die, dep, S, B):
    """prove: S orbits (jointly) and B orbits sit on one station's planes at the same scale in the fair die"""
    o2f = {}; planes = []
    for o, sz in enumerate(die['sizes']):
        for t in range(sz): o2f.setdefault(o, []).append(len(planes)); planes.append((o, die['idx'][len(planes)]))
    fams = {}
    for k, (o, i) in enumerate(planes): fams[k] = DFAM[i]
    SB = [k for k, (o, i) in enumerate(planes) if o in S + B]
    q = {k: EX[planes[k][1]] for k in range(len(planes))}; h = {k: H[fams[k]] for k in SB}
    # S faces of Q, exact
    faces = {}; ok_mirror = ok_axis = True; ksum = 0; kper = []
    for f in [k for k in SB if planes[k][0] in S]:
        C = []
        for j, l in itertools.combinations([k for k in SB if k != f], 2):
            x = solve3([q[f], q[j], q[l]], [h[f], h[j], h[l]])
            if x is None: continue
            if all((h[k] - dot(q[k], x)).sign() >= 0 for k in SB) and x not in C: C.append(x)
        if len(C) < 3: return dict(ok=False, why='S face with < 3 corners in Q')
        Cf = np.array([[float(t) for t in x] for x in C]); c = Cf.mean(0); e1 = Cf[0] - c; e2 = np.cross(np.array([float(t) for t in q[f]]), e1)
        order = sorted(range(len(C)), key=lambda v: np.arctan2((Cf[v] - c) @ e2, (Cf[v] - c) @ e1)); C = [C[v] for v in order]
        for a in range(len(C)):
            v, w = C[a], C[(a + 1) % len(C)]
            ok_mirror &= any(dot(m, v).sign() == 0 and dot(m, w).sign() == 0 for m in MIRRORS)
            ok_axis &= any(all(t.sign() == 0 for t in cross(ax, v)) and dot(ax, v).sign() > 0 for ax in AXES)
        ar = sph_area(C) * 120 / (4 * arb.pi()); k = int(round(float(ar.mid())))
        if not bool(abs(ar - k) < arb(1) / 4): return dict(ok=False, why='area not near an integer')
        ksum += k; kper.append(k); faces[f] = C
    # (ii) S faces of Q strictly inside the other orbits' planes at the certified depths. Scale: B's first plane at its depth.
    bk = [k for k in SB if planes[k][0] in B][0]
    lam = dep[planes[bk][0]] * norm_arb(q[bk]) / A(h[bk])      # Q is built at scale 1; the die at s0 is lam * Q
    slack = None
    for f, C in faces.items():
        for x in C:
            for k in range(len(planes)):
                if planes[k][0] in S + B: continue
                g = dep[planes[k][0]] * norm_arb(q[k]) - lam * A(dot(q[k], x))
                if not g > 0: return dict(ok=False, why='an S corner of Q is not strictly inside plane %d' % k)
                slack = g if slack is None else (g if g.mid() < slack.mid() else slack)
    nS = sum(die['sizes'][o] for o in S); target = 120 * nS / die['N']
    # the station ratio of S to B (normalised depths) and its agreement with the certified depths (sanity, not used)
    sk = [k for k in SB if planes[k][0] in S][0]
    exact_ratio = (A(h[sk]) / norm_arb(q[sk])) / (A(h[bk]) / norm_arb(q[bk]))
    cert_ratio = dep[planes[sk][0]] / dep[planes[bk][0]]
    agree = bool(abs(exact_ratio - cert_ratio) < arb(10) ** -25)
    return dict(ok=bool(ok_mirror and ok_axis and ksum == target and agree), mirror=ok_mirror, axis=ok_axis, k_per_face=kper, k=ksum, target=target,
                corners_per_face=sorted({len(C) for C in faces.values()}), min_slack=str(slack)[:30], fold_S=sorted({FOLD[fams[k]] for k in SB if planes[k][0] in S}),
                fold_B=sorted({FOLD[fams[k]] for k in SB if planes[k][0] in B}), ratio_S_to_B=float(exact_ratio.mid()), certified_ratio=str(cert_ratio)[:40])

def full_step(die, dep):
    """every orbit on station planes at one scale (the die 310 case): the whole polytope Q is exact; if each orbit's union of faces
    is bounded by mirror arcs with corners on axes and covers 120 |orbit| / N mirror triangles, then Q is fair (faces of one orbit
    are congruent under the die's group), and by Alexandrov's uniqueness Q is the catalogue die."""
    planes = []
    for o, sz in enumerate(die['sizes']):
        for t in range(sz): planes.append((o, die['idx'][len(planes)]))
    q = [EX[i] for o, i in planes]; h = [H[DFAM[i]] for o, i in planes]; n = len(planes)
    faces = {}
    for f in range(n):
        C = []
        for j, l in itertools.combinations([k for k in range(n) if k != f], 2):
            x = solve3([q[f], q[j], q[l]], [h[f], h[j], h[l]])
            if x is None: continue
            if all((h[k] - dot(q[k], x)).sign() >= 0 for k in range(n)) and x not in C: C.append(x)
        if len(C) < 3: return dict(ok=False, why='face %d has < 3 corners' % f)
        Cf = np.array([[float(t) for t in x] for x in C]); c = Cf.mean(0); e1 = Cf[0] - c; e2 = np.cross(np.array([float(t) for t in q[f]]), e1)
        order = sorted(range(len(C)), key=lambda v: np.arctan2((Cf[v] - c) @ e2, (Cf[v] - c) @ e1)); faces[f] = [C[v] for v in order]
    on = lambda k, x: (h[k] - dot(q[k], x)).sign() == 0
    ok = True; ks = []
    for o in range(len(die['sizes'])):
        F = [f for f in range(n) if planes[f][0] == o]
        for f in F:
            C = faces[f]
            for a in range(len(C)):
                v, w = C[a], C[(a + 1) % len(C)]
                other = [g for g in range(n) if g != f and on(g, v) and on(g, w)]
                if any(planes[g][0] != o for g in other):
                    ok &= any(dot(m, v).sign() == 0 and dot(m, w).sign() == 0 for m in MIRRORS)
                    ok &= all(any(all(t.sign() == 0 for t in cross(ax, x)) and dot(ax, x).sign() > 0 for ax in AXES) for x in (v, w))
        ar = sum((sph_area(faces[f]) for f in F), arb(0)) * 120 / (4 * arb.pi()); k = int(round(float(ar.mid())))
        ok &= bool(abs(ar - k) < arb(1) / 4) and k == 120 * die['sizes'][o] / die['N']; ks.append(k)
    rat = [str((A(h[next(f for f in range(n) if planes[f][0] == o)]) / norm_arb(q[next(f for f in range(n) if planes[f][0] == o)])) / dep[o])[:30] for o in range(len(die['sizes']))]
    return dict(ok=bool(ok), S=['all orbits'], B=[], k_per_orbit=ks, scale_check=rat)

co = json.load(open(os.path.join(HERE, '..', 'data', 'aequi.json')))['coincidences']
SCAN = {(r['src'], str(r['id'])): r['shadow_unions'] for r in json.load(open(os.path.join(HERE, '..', 'data', 'scan42.json')))}
SPECIAL = {('4553', 310): 'full'}
out = []; nok = 0
for c in co:
    die = load_die(c['src'], c['id']); okc, enc, where = enclosure(c['src'], c['id'])
    assert all('p' not in o for o in die['orbits'])
    dep = [arb(1)] + enc
    assert len(dep) == len(die['sizes'])
    names = die['orbits']
    if (c['src'], int(c['id'])) in SPECIAL: plan = SPECIAL[(c['src'], int(c['id']))]
    else:
        # S = the orbit of the pair that is not two-fold; B = the orbits next to it (data/scan42.json: boundary of S)
        a, b = c['best'][1], c['best'][2]; s0 = b if FOLD[fam(a)[0]] == 2 else a
        bd = [u for u in SCAN[(c['src'], str(c['id']))] if u['S'] == [s0]][0]['boundary_orbits']
        plan = [([s0], [o for o in bd if o != s0])]
    res = []
    if plan == 'full': res.append(full_step(die, dep)); plan = []
    for S, B in plan:
        r = step(die, dep, [names.index(s) for s in S], [names.index(s) for s in B]); r.update(S=S, B=B); res.append(r)
    ok = okc and all(r['ok'] for r in res); nok += ok
    out.append(dict(src=c['src'], id=c['id'], label=c['label'], N=die['N'], certified=where, steps=res, proved=ok))
    print(c['src'], c['id'], c['label'], 'N', die['N'], 'PROVED' if ok else 'NOT', [(r['S'], r['B'], r.get('k'), r.get('target'), r.get('k_per_face', [None])[0], r.get('corners_per_face'), r.get('fold_S'), r.get('fold_B'), round(r.get('ratio_S_to_B', 0), 9), r.get('min_slack'), r.get('why')) for r in res], flush=True)
json.dump(out, open(os.path.join(HERE, '..', 'data', 'exact42.json'), 'w'), indent=1)
print('proved', nok, 'of', len(out))
print('FINAL ok' if nok == len(out) == 42 else 'FINAL FAIL')
