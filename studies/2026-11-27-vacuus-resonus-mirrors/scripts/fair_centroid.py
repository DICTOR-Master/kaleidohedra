"""Step 8 (27 Nov 2026): are the fair-sized dice of fairsearch.py FAIR dice? With Claude (Anthropic).
fairsearch.py gives face patterns whose faces subtend equal solid angles from O. A die is fair when this holds from its centre
of mass. For each pattern: keep its face cones (n_k - n_l parallel to the shared great circle's normal m, pointing into k) and
move the planes (the free edge sizes and the free shift) until the centre of mass is O; numerical least squares, then checked:
every piece centre still sees its own face first (pattern kept), and every face's solid angle from the centre of mass is 4 pi / N
to 1e-9. Numerical evidence (exact certification is a later step)."""
import os, sys, json, itertools
import numpy as np
from scipy.optimize import least_squares, linprog
from scipy.spatial import HalfspaceIntersection, ConvexHull
HERE_ = os.path.dirname(os.path.abspath(__file__))
PAIR_ = os.environ.get('PAIR')   # step 12 (27 Nov): any pair, from fairsearch_any.py's merged file; SHARD=k/K splits the list
if PAIR_:
    os.environ.pop('MERGE', None); os.environ.pop('SUB', None)
    src = open(os.path.join(HERE_, 'fairsearch_any.py')).read()
    exec(src[:src.index("if os.environ.get('MERGE')")])
    import gzip
    R = json.load(gzip.open(os.path.join(HERE_, '../fairdice_' + PAIR_.split('|')[0].replace(' ', '-') + '_symmetric.json.gz')))
else:
    src = open(os.path.join(HERE_, 'fairsearch.py')).read()
    exec(src[:src.index('from ortools.sat.python import cp_model')])
    R = json.load(open(os.path.join(HERE_, '../fairdice.json'))); GO = 48
SH = os.environ.get('SHARD'); SK, SKK = (int(x) for x in SH.split('/')) if SH else (0, 1)
LIM = int(os.environ.get('LIMIT', 10 ** 9))
def pairs_of(faces):
    owner = {i: k for k, F in enumerate(faces) for i in F}; out = {}
    for e, L in edges.items():
        if len(L) != 2: continue
        i, j = L; k, l = owner[i], owner[j]
        if k == l: continue
        a, b = tuple(e); m = np.cross(np.array(a), np.array(b)); m /= np.linalg.norm(m)
        if m @ np.mean([np.array(v) for v in VK[i]], axis=0) < 0: m = -m
        if k > l: k, l, m = l, k, -m      # one entry per face pair (both directions differ only by rounding)
        out.setdefault((k, l), m)
    return owner, out
def lp_start(N, pr):
    lam = list(pr.items()); nv = 3 * N + len(lam); Aeq, beq = [], []
    for t, ((k, l), m) in enumerate(lam):
        for q in range(3):
            r = np.zeros(nv); r[3 * k + q] = 1; r[3 * l + q] = -1; r[3 * N + t] = -m[q]; Aeq.append(r); beq.append(0)
    for q in range(3):
        r = np.zeros(nv); r[q:3 * N:3] = 1; Aeq.append(r); beq.append(0)
    cost = np.zeros(nv); rng = np.random.default_rng(int(os.environ.get('SEED', 0)))
    if os.environ.get('SEED'): cost[3 * N:] = rng.uniform(0, 1, len(lam))
    res = linprog(cost, A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=[(None, None)] * (3 * N) + [(1, None)] * len(lam), method='highs')
    return res.x[:3 * N].reshape(N, 3)
def poly(n):
    hs = np.hstack([n, -np.ones((len(n), 1))]); H = HalfspaceIntersection(hs, np.zeros(3)); P = H.intersections
    if not PAIR_: return P
    # step 12: polish every vertex on its own planes (least squares n_A p = 1), relative tolerance, duplicates merged
    sc = np.abs(P).max(); out = []
    for p in P:
        A = n[np.abs(n @ p - 1) < 1e-6]
        if len(A) >= 3: p = np.linalg.lstsq(A, np.ones(len(A)), rcond=None)[0]
        if not any(np.linalg.norm(p - q) < 1e-9 * sc for q in out): out.append(p)
    return np.array(out)
def centroid(P):
    h = ConvexHull(P); c0 = P.mean(0); vol = 0; acc = np.zeros(3)
    for s in h.simplices:
        a, b, c = P[s]; v = abs(np.dot(a - c0, np.cross(b - c0, c - c0))) / 6; vol += v; acc += v * (a + b + c + c0) / 4
    return acc / vol
def tri_angle(a, b, c):
    a, b, c = (x / np.linalg.norm(x) for x in (a, b, c))
    return 2 * np.arctan2(abs(a @ np.cross(b, c)), 1 + a @ b + b @ c + c @ a)
def face_angles(n, cpt):
    P = poly(n); out = []
    for k in range(len(n)):
        on = [p for p in P if abs(n[k] @ p - 1) < (1e-7 if PAIR_ else 1e-9)]
        if len(on) < 3: return None
        on = np.array(on); c = on.mean(0); e1 = on[0] - c; e2 = np.cross(n[k], e1)
        on = on[np.argsort(np.arctan2((on - c) @ e2, (on - c) @ e1))]
        out.append(sum(tri_angle(on[0] - cpt, on[i] - cpt, on[i + 1] - cpt) for i in range(1, len(on) - 1)))
    return np.array(out)
res_all = []
ONLY = [int(x) for x in os.environ['IDX'].split(',')] if os.environ.get('IDX') else None
for idx, r in enumerate(R):
    if ONLY is not None and idx not in ONLY: continue
    if idx % SKK != SK or idx >= LIM: continue
    faces = r['faces']; N = len(faces); owner, pr = pairs_of(faces)
    if PAIR_:
        owner, pr = face_pairs(faces); n0 = realise_n(N, faces); AEQ, AUB = pattern_rows(faces)
        if n0 is None: res_all.append(dict(index=idx, N=N, symmetry_order=r['symmetry_order'], fair=False, lp_failed=True, centroid_offset=9.0, max_angle_dev=9.0, pattern_kept=False)); print(f'die {idx}: LP failed', flush=True); continue
    else: n0 = lp_start(N, pr)
    keys = list(pr.keys())
    def resid(z):
        n = z.reshape(N, 3); out = []
        for (k, l) in keys:
            d = n[k] - n[l]; m = pr[(k, l)]; out += list(np.cross(d, m)); out.append(min(0.0, d @ m - 0.05))
        try: out += list(10 * centroid(poly(n)))
        except Exception: out += [10.0, 10.0, 10.0]
        return np.array(out)
    if PAIR_:
        # step 12: move only inside the linear space L of plane sets keeping every face cone (cross(n_k - n_l, m) = 0), by
        # minimum-norm Gauss-Newton steps on the 3 centre-of-mass equations; damped so every cone stays open (d . m > 0)
        AE = AEQ.toarray()[:-3]; sv = np.linalg.svd(AE, compute_uv=False); Bm = np.linalg.svd(AE)[2]
        rk = int((sv > 1e-9 * sv[0]).sum()); B = Bm[rk:].T            # basis of L: plane sets with this face pattern's ties
        def cm_of(v):
            return centroid(poly(v.reshape(N, 3)))
        def openc(v):
            return float((-(AUB @ v)).min())
        v = n0.ravel().copy(); scale0 = openc(v)
        for it in range(30):
            c = cm_of(v)
            if np.linalg.norm(c) < 1e-13: break
            J = np.zeros((3, B.shape[1])); h = 1e-7
            for j in range(B.shape[1]): J[:, j] = (cm_of(v + h * B[:, j]) - c) / h
            st = B @ np.linalg.lstsq(J, -c, rcond=None)[0]; tt = 1.0
            while tt > 1e-4:
                w = v + tt * st
                try:
                    if openc(w) > 0.05 * scale0 and np.linalg.norm(cm_of(w)) < np.linalg.norm(c): v = w; break
                except Exception: pass
                tt /= 2
            else: break
        n = v.reshape(N, 3)
    else:
        sol = least_squares(resid, n0.ravel(), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=3000)
        n = sol.x.reshape(N, 3)
    try:
        P = poly(n); cm = centroid(P); kept = all(int(np.argmax(n @ cen[i])) == owner[i] for i in range(NP))
        ang = face_angles(n, cm); dev = float(np.abs(ang - 4 * np.pi / N).max()) if ang is not None else 9
    except Exception as e:
        cm, kept, dev = np.array([9, 9, 9]), False, 9
    fair = kept and dev < (1e-7 if PAIR_ else 1e-9) and np.linalg.norm(cm) < 1e-9   # step 12: dev is only a numerical cross-check (cones are whole pieces)
    res_all.append(dict(index=idx, N=N, symmetry_order=r['symmetry_order'], fair=bool(fair), centroid_offset=float(np.linalg.norm(cm)), max_angle_dev=dev, pattern_kept=bool(kept), normals=n.tolist()))
    if idx % (10 * SKK) == SK or not fair: print(f'die {idx}: N {N} sym {r["symmetry_order"]}: fair {fair} (centre offset {np.linalg.norm(cm):.1e}, angle dev {dev:.1e}, pattern kept {kept})', flush=True)
json.dump(res_all, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../fairdice_centroid' + (('_' + PAIR_.split('|')[0][:5]) if PAIR_ else '') + (('_shard%d' % SK) if SH else '') + ('_retry_s' + os.environ['SEED'] if os.environ.get('IDX') else '') + '.json'), 'w'))
from collections import Counter
for N in sorted({x['N'] for x in res_all}, reverse=True):
    rs = [x for x in res_all if x['N'] == N]
    print(f'N {N}: fair {sum(x["fair"] for x in rs)} of {len(rs)}; fair by symmetry order', sorted(Counter(x['symmetry_order'] for x in rs if x['fair']).items(), reverse=True), flush=True)
ctl = [x for x in res_all if x['symmetry_order'] == GO]
print('control: the four Catalan dice (full symmetry) fair:', all(x['fair'] for x in ctl), len(ctl))
print('FINAL ok' if (ONLY is not None) or (SH and len(res_all) > 0) or (ctl and all(x['fair'] for x in ctl)) else 'FINAL FAIL (control)')
