# DICTO · Vacuus-Solids: EXACT version of core_or_planes.py for the eleven special members of Theorem 1 (27 Nov 2026).
# DICTO: "is it really mathematically sound to include the figs with the far more complex inner cores?"; "continue with the exact check".
# With Claude (Anthropic). Exact arithmetic in Q(sqrt r) (exact_check.py's K, solids, faces, rotations, walls); floats only to pick
# candidates. For each member (P, s, Q) with its rotation M and scale lam (found exactly as in exact_check.py):
#  (1) each pit tip t against lamQ = {x : N_q . x <= lam d_q}: at a corner of lamQ (>= 3 independent planes tight, none violated),
#      on a face, inside, or outside;
#  (2) each pit wall against lamQ: the wall triangle and the face of lamQ in the same plane, as 2D convex polygons (exact separating-
#      axis test): overlap (positive area), touch (common points, no area), or apart;
#  (3) each pit separated from lamQ by one of its own wall planes (pit on the far side): then no pit enters lamQ.
# Kinds: CORE = every corner of lamQ is a pit tip and every tip a corner, no overlap; TOUCH = some tips at corners of lamQ, no tip
# inside, no overlap; PLANES = no tip on or in lamQ and no wall touches it; anything else printed as found.
import os, sys, itertools
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'exact_check.py')).read(); exec(src[:src.index('fails = 0')])
def check_M(Pn, Qn, s, r):
    VP = body(Pn, r); FP = faces(VP); VQ = body(Qn, r); FQ = faces(VQ)
    walls = []
    for fi, (idx, N, d) in enumerate(FP):
        p = scl(d / dot(N, N), N); ap = scl(s, p)
        for i, j in zip(idx, idx[1:] + idx[:1]):
            u, v = VP[i], VP[j]; walls.append((cross(sub(u, ap), sub(v, ap)), u, v, ap, fi))
    for M in FRAMES:
        Q = [(rot(M, N), d) for _, N, d in FQ]; Qf = [flt(N) / np.linalg.norm(flt(N)) for N, _ in Q]
        lam = None; ok = True; wq = []
        for m, u, v, ap, fi in walls:
            mf = flt(m); mf /= np.linalg.norm(mf); good = False
            for q in [q for q in range(len(Q)) if abs(abs(mf @ Qf[q]) - 1) < 1e-6]:
                w, h = Q[q]
                if not all(x.iszero() for x in cross(m, w)): continue
                i = next(t for t in range(3) if not w[t].iszero()); kk = m[i] / w[i]; L = dot(m, u) / (kk * h)
                if L.sign() <= 0: continue
                if lam is None: lam = L
                if not (L == lam): continue
                good = True; wq.append(q); break
            if not good: ok = False; break
        if ok: return dict(VP=VP, FP=FP, walls=walls, wq=wq, M=M, lam=lam, VQ=[scl(lam, rot(M, v)) for v in VQ], FQ=[(idx, rot(M, N), lam * d) for idx, N, d in FQ])
    return None
def proj2(pts, N):
    k = max(range(3), key=lambda t: abs(float(N[t])))
    keep = [t for t in range(3) if t != k]; return [(p[keep[0]], p[keep[1]]) for p in pts]
def cyc_order(P2):
    X = np.array([[float(a), float(b)] for a, b in P2]); c = X.mean(0); o = np.argsort(np.arctan2(X[:, 1] - c[1], X[:, 0] - c[0]))
    return [P2[i] for i in o]
def sat2(A, B):
    """exact 2D convex polygons (vertex lists, cyclic): 'apart', 'touch' or 'overlap'"""
    gap0 = False
    for poly in (A, B):
        n = len(poly)
        for i in range(n):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]; nx, ny = y2 - y1, x1 - x2
            pa = [nx * x + ny * y for x, y in A]; pb = [nx * x + ny * y for x, y in B]
            amax = max(pa, key=float); amin = min(pa, key=float); bmax = max(pb, key=float); bmin = min(pb, key=float)
            s1 = (bmin - amax).sign(); s2 = (amin - bmax).sign()
            if s1 > 0 or s2 > 0: return 'apart'
            if s1 == 0 or s2 == 0: gap0 = True
    return 'touch' if gap0 else 'overlap'
res = []
for Pn, Qn, s, r in TWELVE:
    D = check_M(Pn, Qn, s, r); assert D is not None, (Pn, Qn)
    VP, FP, walls, wq, VQ, FQ = D['VP'], D['FP'], D['walls'], D['wq'], D['VQ'], D['FQ']
    tips = []
    for idx, N, d in FP: tips.append(scl(s, scl(d / dot(N, N), N)))
    tip_kind = []
    for t in tips:
        g = [dot(N, t) - d for _, N, d in FQ]; sg = [x.sign() for x in g]
        if max(sg) > 0: tip_kind.append('outside'); continue
        tight = [q for q in range(len(FQ)) if sg[q] == 0]
        if not tight: tip_kind.append('inside'); continue
        rank = np.linalg.matrix_rank(np.array([flt(FQ[q][1]) for q in tight]))
        tip_kind.append('corner' if rank == 3 else 'face')
    corners_hit = sum(1 for v in VQ if any(all((a - b).iszero() for a, b in zip(v, t)) for t in tips))
    contact = []
    for (m, u, v, ap, fi), q in zip(walls, wq):
        idx, N, d = FQ[q]
        A2 = cyc_order(proj2([u, v, ap], N)); B2 = cyc_order(proj2([VQ[i] for i in idx], N))
        contact.append(sat2(A2, B2))
    sep = 0
    for fi, (idx, N, d) in enumerate(FP):
        pv = [VP[i] for i in idx] + [tips[fi]]
        ok = False
        for (m, u, v, ap, f2), q in zip(walls, wq):
            if f2 != fi: continue
            _, NQq, dq = FQ[q]
            if all((dot(NQq, x) - dq).sign() >= 0 for x in pv): ok = True; break
        sep += ok
    from collections import Counter
    tk, ck = Counter(tip_kind), Counter(contact)
    if corners_hit == len(VQ) and tk == Counter({'corner': len(tips)}) and ck['overlap'] == 0: kind = 'CORE'
    elif tk['corner'] > 0 and tk['inside'] == 0 and ck['overlap'] == 0: kind = 'TOUCH'
    elif tk['corner'] == tk['face'] == tk['inside'] == 0 and ck['touch'] == ck['overlap'] == 0: kind = 'PLANES'
    else: kind = 'OTHER'
    res.append((Pn, Qn, kind))
    print(f'{Pn:24s} on {Qn:26s} s = {s}: tips {dict(tk)}; corners of lamQ that are tips {corners_hit} of {len(VQ)}; '
          f'walls vs lamQ faces {dict(ck)}; pits separated by a wall plane {sep} of {len(FP)} -> {kind}', flush=True)
expect = {('dodecahedron', 'icosahedron'): 'CORE', ('icosahedron', 'dodecahedron'): 'CORE', ('dodecahedron', 'deltoidal hexecontahedron'): 'TOUCH',
          ('icosahedron', 'deltoidal hexecontahedron'): 'TOUCH', ('tetrahedron', 'triakis octahedron'): 'TOUCH'}
agree = all(k == expect.get((P, Q), 'PLANES') for P, Q, k in res)
print('exact kinds agree with the numerical check (2 CORE, 3 TOUCH, 6 PLANES):', agree)
print('FINAL ok' if len(res) == 11 else 'FINAL FAIL')
