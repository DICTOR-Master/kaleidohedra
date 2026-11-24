"""Item 1: the polar of every catalogued Aequus (fair die) about its centre, in ball arithmetic.

For a die P = {x : u_k.x <= d_k} (u_k unit, fair about 0), the polar P* = conv{p_k = u_k/d_k}.
 - Control A (Theorem 1): the angle defect of P* at p_k contains 4*pi/N (60-digit depths: arb balls; double depths: |err| < 1e-9).
 - Control B: the curvatures of P at its corners add to 4*pi (Descartes).
 - Test (Theorem 2): P* is itself fair  <=>  P has equal curvature at every corner. The curvature of P at a corner v is the
   solid angle of the cone spanned by the unit normals of the faces at v (exact directions over Q(sqrt5), as arb balls):
   it depends on the normals and the combinatorics only, not on the depths. Distinct balls prove unequal curvature.
Combinatorics: the earlier certification (study 2026-11-24-aequi-certify-extend and -certify-4404) proved the type constant
over a box round the depths; here it is rebuilt in floating point and the corner count is asserted equal to the recorded one.
Usage: polar_aequi.py OUT.jsonl NPROC [LIMIT]  -> prints PROGRESS lines, a summary, and FINAL ok only if every control passes.
"""
import os, sys, json, gzip, csv, time, itertools
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
ST = os.path.normpath(os.path.join(HERE, '..', '..'))
X = os.path.join(ST, '2026-11-24-aequi-certify-extend', 'scripts'); sys.path.insert(0, X)
import certify as C                       # DIRS, arbdir (exact directions), combinatorics, load_all, OH, IH
from flint import arb, ctx
ctx.prec = 200
PI = arb.pi(); FOURPI = 4 * PI

def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def sub(a, b): return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]

def records():
    E = os.path.join(ST, '2026-11-24-aequi-certify-extend', 'data')
    names = {}
    for r in csv.DictReader(open(os.path.join(E, 'certify-table.csv'))):
        names[(r['study'], int(r['row']))] = r['name']
    out = []
    for r in C.load_all():
        r = dict(r); r['part'] = '1232'; r['name'] = names.get((r['study'], r['sid']), ''); r['prec60'] = True; out.append(r)
    for r in json.load(open(os.path.join(ST, '2026-11-24-aequi-certify-4404', 'data', 'dice4404.json'))):
        r = dict(r); r['part'] = '4404'; r['name'] = ''; r['prec60'] = True; out.append(r)
    for s in ('2a', '2caps', '2caps2', '2caps3'):
        for r in json.load(open(os.path.join(E, 'dice%s-new.json' % s))):
            r = dict(r); r['part'] = s; r['name'] = ''; r['prec60'] = False; out.append(r)
    return out

DCACHE = {}
def udir(i):
    if i not in DCACHE: DCACHE[i] = C.arbdir(i)
    return DCACHE[i]

def corner_orbits(idx, sizes, inc):
    """orbits of the corners under the frame maps that keep every labelled face orbit (the die's symmetry for one depth per orbit)"""
    lab = np.repeat(np.arange(len(sizes)), sizes); P = C.DIRS[idx]; G = []
    for g in list(C.OH) + list(C.IH):
        img = P @ g.T; dd = np.linalg.norm(img[:, None, :] - P[None, :, :], axis=2); j = dd.argmin(1)
        if dd.min(1).max() < 1e-9 and all(lab[j] == lab) and len(set(j)) == len(j): G.append(j)
    key = {frozenset(I): c for c, I in enumerate(inc)}
    par = list(range(len(inc)))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for j in G:
        for c, I in enumerate(inc):
            c2 = key[frozenset(int(j[i]) for i in I)]; a, b = f(c), f(c2)
            if a != b: par[a] = b
    return len({f(c) for c in range(len(inc))}), len({tuple(j) for j in G}), [f(c) for c in range(len(inc))]

def work(rec):
    t0 = time.time()
    idx, sizes = rec['idx'], rec['sizes']; N = len(idx)
    dfl = [float(x) for x in rec['depths']]
    V, inc = C.combinatorics(idx, sizes, rec['depths'])
    out = dict(part=rec['part'], study=rec['study'], sid=rec['sid'], name=rec['name'], label=rec.get('label', ''), group=rec['group'],
               m=len(sizes), N=N, corners=len(V), corners_recorded=rec['corners'])
    if len(V) != rec['corners']: out['fail'] = 'corner count'; return out
    Df = np.repeat(dfl, sizes)
    if rec['prec60']:
        dep = [arb(str(x)) for x in rec['depths']]; dep = [arb(x.mid(), 1e-55) for x in dep]
    else:
        dep = [arb(x) for x in dfl]
    Dk = [dep[o] for o in np.repeat(np.arange(len(sizes)), sizes)]
    U = [udir(i) for i in idx]
    Pp = [[c / Dk[k] for c in U[k]] for k in range(N)]                 # polar corners p_k = u_k/d_k
    nf = C.DIRS[idx]
    kap = []; cyc = []
    for c, I in enumerate(inc):
        mvec = sum(nf[i] for i in I); mvec = mvec / np.linalg.norm(mvec)
        e1 = np.cross(mvec, [1, 0, 0] if abs(mvec[0]) < 0.9 else [0, 1, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(mvec, e1)
        order = sorted(I, key=lambda i: np.arctan2(nf[i] @ e2, nf[i] @ e1))
        cyc.append(order)
        a = U[order[0]]; s = arb(0)
        for i in range(1, len(order) - 1):
            b, cc = U[order[i]], U[order[i + 1]]
            s += 2 * arb.atan2(dot(a, cross(b, cc)), 1 + dot(a, b) + dot(b, cc) + dot(cc, a))
        kap.append(s)
    tot = sum(kap, arb(0))
    out['controlB_sum_4pi'] = bool(tot.overlaps(FOURPI)) and tot.rad() < 1e-20
    # control A: angle defect of the polar at each p_k
    ang = [arb(0)] * N
    for order in cyc:
        L = len(order)
        for t in range(L):
            k = order[t]; a = sub(Pp[order[t - 1]], Pp[k]); b = sub(Pp[order[(t + 1) % L]], Pp[k])
            ang[k] = ang[k] + arb.acos(dot(a, b) / (dot(a, a) * dot(b, b)).sqrt())
    target = FOURPI / N; worst = 0.0; okA = True
    for k in range(N):
        dfc = 2 * PI - ang[k]
        if rec['prec60']: okA &= bool(dfc.overlaps(target)) and dfc.rad() < 1e-30
        else: okA &= abs(float((dfc - target).mid())) < 1e-9
        worst = max(worst, abs(float((dfc - target).mid())))
    out['controlA_polar_defect_4pi_over_N'] = bool(okA); out['controlA_worst'] = worst
    # curvature classes of P (= solid angles of the faces of the polar)
    srt = sorted(range(len(kap)), key=lambda c: float(kap[c].mid()))
    clusters = [[srt[0]]]
    for c in srt[1:]:
        if kap[c].overlaps(kap[clusters[-1][-1]]): clusters[-1].append(c)
        else: clusters.append([c])
    nor, gord, orb = corner_orbits(idx, sizes, inc)
    out.update(curv_classes=len(clusters), corner_orbits=nor, sym_order_labelled=gord,
               curv_min=float(kap[srt[0]].mid()), curv_max=float(kap[srt[-1]].mid()),
               unequal_proved=len(clusters) >= 2,
               polar_face_sides=sorted(collections_count(len(I) for I in inc).items()),
               polar_radii=[1 / x for x in dfl], polar_face_distance_classes=len({round(1 / float(np.linalg.norm(v)), 9) for v in V}),
               polar_resonus_float=len({tuple(np.round(v / np.linalg.norm(v) * (1 if next(x for x in v / np.linalg.norm(v) if abs(x) > 1e-9) > 0 else -1), 9)) for v in V}))
    # a coincidence across corner orbits: two corner orbits with overlapping curvature balls
    reps = {}
    for c in range(len(inc)): reps.setdefault(orb[c], c)
    R = list(reps.values()); cross_eq = 0; unexpl = 0
    for a, b in itertools.combinations(R, 2):
        if kap[a].overlaps(kap[b]):
            cross_eq += 1
            # explained exactly when a frame map (exact matrix over Q(sqrt5)) carries the normals at a onto those at b
            A = nf[list(inc[a])]; B = nf[list(inc[b])]
            ok = len(A) == len(B) and any(np.linalg.norm((A @ g.T)[:, None, :] - B[None, :, :], axis=2).min(1).max() < 1e-9
                                          for g in list(C.OH) + list(C.IH))
            unexpl += 0 if ok else 1
    out['orbit_pairs_equal_curvature'] = cross_eq; out['orbit_pairs_equal_unexplained'] = unexpl
    out['sec'] = round(time.time() - t0, 2)
    return out

def collections_count(it):
    d = {}
    for x in it: d[x] = d.get(x, 0) + 1
    return d

if __name__ == '__main__':
    outp, npr = sys.argv[1], int(sys.argv[2]); lim = int(sys.argv[3]) if len(sys.argv) > 3 else None
    recs = records()
    print('dice', len(recs), {p: sum(1 for r in recs if r['part'] == p) for p in ('1232', '4404', '2a', '2caps', '2caps2', '2caps3')}, flush=True)
    if lim: recs = recs[:lim // 2] + recs[-(lim - lim // 2):]
    res = []; t0 = time.time()
    with Pool(npr) as pool, open(outp, 'w') as fo:
        for k, o in enumerate(pool.imap(work, recs, chunksize=4)):
            res.append(o); fo.write(json.dumps(o) + '\n')
            if (k + 1) % 500 == 0: print('PROGRESS %.3f %d dice %.0fs' % ((k + 1) / len(recs), k + 1, time.time() - t0), flush=True)
    bad = [o for o in res if 'fail' in o or not o['controlB_sum_4pi'] or not o['controlA_polar_defect_4pi_over_N']]
    eq = [o for o in res if not o.get('unequal_proved', True)]
    hidden = [o for o in res if o.get('orbit_pairs_equal_curvature', 0) > 0]
    unex = [o for o in res if o.get('orbit_pairs_equal_unexplained', 0) > 0]
    print('of these, pairs NOT explained by a congruence of normal cones:', len(unex), [(o['part'], o['sid'], o['label']) for o in unex[:20]])
    print('candidates with one corner orbit (equal curvature proved by symmetry):', sum(1 for o in eq if o['corner_orbits'] == 1), 'of', len(eq))
    print('dice run', len(res), '| failures', len(bad), [(o['part'], o['sid'], o.get('fail')) for o in bad[:10]])
    print('polar fair candidates (all corner curvatures overlap):', len(eq), [(o['part'], o['sid'], o['label'], o['corner_orbits']) for o in eq[:20]])
    print('dice with two corner orbits of equal curvature (ball overlap):', len(hidden), [(o['part'], o['sid'], o['label']) for o in hidden[:20]])
    print('curvature classes histogram:', sorted(collections_count(o['curv_classes'] for o in res if 'curv_classes' in o).items()))
    if not bad: print('FINAL ok')
