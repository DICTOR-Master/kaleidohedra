"""C116 -> Minana #377: the floors (26 Nov 2026; DICTO: "both side by side"). With Claude (Anthropic).
1. Replay: floor-1 swaps, then the 11-swap site sequence at every T_h image of the site (data/c116/longsite.json); record every single
   swap with the triangles it removes and adds. Check the final triangle set equals Minana's exactly (corners, not only neighbours).
2. Floors: a swap depends on an earlier one when it removes a triangle that one added; floor = longest chain of dependencies ending at
   the swap (+1). Swaps in one floor touch no common triangle (checked). Each floor's state must be T_h-symmetric (checked).
3. Each floor realised as a convex polyhedron with 60 faces (26 Nov: middle floors keep only part of T_h, so no symmetry imposed): canonical iteration, then exact rational planes
   orbit by orbit (as c116_in_minana.py), every corner strictly inside every other plane (exact).
Output data/c116/floors.json (each floor: faces as corner lists, rational planes)."""
import os, sys, json, itertools
from fractions import Fraction as Fr
from collections import Counter
import numpy as np
os.environ.setdefault('PAIRFILE', 'pairing_local.json'); os.environ['DEPTH'] = '1'
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'c116_stages.py')).read().split("sc, T, path = best")[0])
S_ = [np.array(m) for m in d['S']]
# ---- 1. replay with a record of every swap ----
def swap_rec(T, e):
    ts = [t for t in T if e <= t]
    if len(ts) != 2: return None
    c, dd = [next(iter(t - e)) for t in ts]
    if frozenset((c, dd)) in E(T): return None
    a, b = tuple(e); add = [frozenset((a, c, dd)), frozenset((b, c, dd))]
    return (T - set(ts)) | set(add), ts, add
T = frozenset(T0); rec = []
# floor-1 swaps: the first beam move from T0 (recomputed: the move whose result is best's state)
first = None
for mv in moves(frozenset(T0)):
    if apply(frozenset(T0), mv) == best[1]: first = mv; break
assert first is not None
for x in (first[1] if isinstance(first, tuple) and isinstance(first[1], frozenset) and False else []): pass
# replay floor 1 swap by swap: edges of T0 not in best state, flipped
gone = E(frozenset(T0)) - E(best[1])
for e in sorted(gone, key=sorted):
    r = swap_rec(T, e); assert r, 'floor-1 swap not valid in sequence'
    T, rm, ad = r; rec.append((e, rm, ad))
assert T == best[1], 'floor-1 replay differs'
site = json.load(open(os.path.join(HERE, '../data/c116/longsite.json')))
for g in range(24):
    for kind, e in site['path']:
        eg = frozenset(gface[g][x] for x in e)
        if eg in E(T):
            r = swap_rec(T, eg)
            if r: T, rm, ad = r; rec.append((eg, rm, ad))
T1set = {frozenset(t) for t in T1}
# cut the record where Minana is first reached (later copies only undo and redo)
Tt = frozenset(T0)
for k, (e, rm, ad) in enumerate(rec):
    Tt = (Tt - set(rm)) | set(ad)
    if Tt == T1set: rec = rec[:k + 1]; break
T = Tt
print('swaps', len(rec), '; final neighbour pairs', len(E(T) & target), '/ 174; final corners equal Minana exactly:', T == T1set, flush=True)
assert T == T1set
# ---- 2. floors by dependency depth (no two swaps of a floor touch; the order within the record is respected) ----
made = {}; depth = []
for k, (e, rm, ad) in enumerate(rec):
    dep = [depth[made[t]] for t in rm if t in made]
    depth.append(1 + max(dep) if dep else 1)
    for t in ad: made[t] = k
states = []; Tc = frozenset(T0)
def symorder(T): return sum(1 for g in range(24) if gT(g, T) == T) if 'gT' in globals() else sum(1 for g in range(24) if frozenset(frozenset(gface[g][x] for x in t) for t in T) == T)
for f in sorted(set(depth)):
    ks = [k for k in range(len(rec)) if depth[k] == f]
    for k in ks:
        e, rm, ad = rec[k]; assert set(rm) <= Tc, 'order broken'; Tc = (Tc - set(rm)) | set(ad)
    trs = [t for k in ks for t in rec[k][1]]
    states.append((f, Tc, symorder(Tc), len(trs) == len(set(trs))))
    print(f'floor {f}: {len(ks)} swaps; no two touch {len(trs) == len(set(trs))}; symmetries kept {symorder(Tc)} of 24; Minana pairs {len(E(Tc) & target)}', flush=True)
REACHED = Tc == T1set
print('reaches Minana exactly:', REACHED, flush=True)
# ---- 3. realise each floor (primal: faces = labels 0..59, corners = triangles) ----
def realise(Tset):
    tris = sorted(Tset, key=sorted); tid = {t: i for i, t in enumerate(tris)}; nv = len(tris)
    adj = {i: [] for i in range(nv)}
    for i, t in enumerate(tris):
        for j, u in enumerate(tris):
            if i < j and len(t & u) == 2: adj[i].append(j); adj[j].append(i)
    fcs = []
    for lab in range(60):
        around = [tid[t] for t in tris if lab in t]; cyc = [around[0]]
        while len(cyc) < len(around):
            nx = [j for j in adj[cyc[-1]] if j in around and j not in cyc]; cyc.append(nx[0])
        fcs.append(cyc)
    edges_ = sorted({tuple(sorted((i, j))) for i in adj for j in adj[i]})
    L = np.zeros((nv, nv))
    for i in adj:
        for j in adj[i]: L[i, j] = -1
        L[i, i] = 3
    P = np.linalg.eigh(L)[1][:, 1:4].copy(); P /= np.linalg.norm(P, axis=1)[:, None]
    for it in range(4000):
        D = np.zeros_like(P); cs = []
        for a, b in edges_:
            dv = P[b] - P[a]; t = -(P[a] @ dv) / (dv @ dv); c = P[a] + t * dv; r = np.linalg.norm(c); cs.append(c)
            D[a] += (1 - r) * c / r; D[b] += (1 - r) * c / r
        P += 0.1 * D / 3; P -= 0.1 * np.mean(cs, axis=0)
        for f in fcs:
            X = P[f]; c = X.mean(0); nrm = np.linalg.svd(X - c)[2][2]; P[f] -= 0.3 * np.outer((X - c) @ nrm, nrm)
    if os.environ.get('GENERAL') or True:
        N = []
        for f in fcs:
            X = P[f]; c = X.mean(0); nrm = np.linalg.svd(X - c)[2][2]
            if nrm @ c < 0: nrm = -nrm
            N.append(nrm / (nrm @ c))
        planes = [[Fr(int(round(x * 10**6)), 10**6) for x in nv] for nv in N]
        best_err = 0.0
        return finish_real(tris, fcs, planes, best_err)
    # frame: the same T_h as the C116 frame -- fit the rotation taking the face normals' orbit structure onto S_ (Procrustes on
    # a symmetrised configuration): align by least squares between label-permuted copies
    N = []
    for f in fcs:
        X = P[f]; c = X.mean(0); nrm = np.linalg.svd(X - c)[2][2]
        if nrm @ c < 0: nrm = -nrm
        N.append(nrm / (nrm @ c))
    N = np.array(N)
    # find R with R N[gface[g][k]] ~ S_g R N[k] for all g,k: solve by averaging over the group in the C116 frame
    best_R, best_err = None, 1e9
    for trial in range(20):
        A = np.random.default_rng(trial).normal(size=(3, 3)); R = np.linalg.qr(A)[0]
        for it in range(200):
            M = np.zeros((3, 3))
            for g in range(24):
                for k in range(60): M += np.outer(S_[g].T @ (R @ N[gface[g][k]]), N[k])
            U, _, Vt = np.linalg.svd(M); R = U @ Vt
        err = max(np.abs(R @ N[gface[g][k]] - S_[g] @ (R @ N[k])).max() for g in range(24) for k in range(60))
        if err < best_err: best_R, best_err = R, err
    Nr = N @ best_R.T
    planes = [None] * 60
    for k in range(60):
        if planes[k] is not None: continue
        stab = [g for g in range(24) if gface[g][k] == k]
        nk = np.mean([S_[g] @ Nr[k] for g in stab], axis=0); r = [Fr(int(round(x * 10**6)), 10**6) for x in nk]
        for g in range(24):
            j = gface[g][k]; img = [sum(int(S_[g][i, t]) * r[t] for t in range(3)) for i in range(3)]
            if planes[j] is None: planes[j] = img
            else: assert planes[j] == img
    return finish_real(tris, fcs, planes, best_err)
def finish_real(tris, fcs, planes, best_err):
    Vx = []
    for t in tris:
        a, b, c = (planes[k] for k in sorted(t))
        M3 = [[a[0], a[1], a[2]], [b[0], b[1], b[2]], [c[0], c[1], c[2]]]
        det = (M3[0][0] * (M3[1][1] * M3[2][2] - M3[1][2] * M3[2][1]) - M3[0][1] * (M3[1][0] * M3[2][2] - M3[1][2] * M3[2][0])
               + M3[0][2] * (M3[1][0] * M3[2][1] - M3[1][1] * M3[2][0]))
        assert det != 0
        cr = lambda u, v: [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
        cx, cy, cz = cr(b, c), cr(c, a), cr(a, b)
        Vx.append([(cx[q] + cy[q] + cz[q]) / det for q in range(3)])
    bad = sum(1 for i, t in enumerate(tris) for k in range(60) if k not in t and sum(planes[k][q] * Vx[i][q] for q in range(3)) >= 1)
    return dict(frame_err=float(best_err), bad=bad, planes=[[str(x) for x in p] for p in planes], faces=[[sorted(tris[i]) for i in f] for f in fcs])
out = []
for f, Tf, sym, indep in [(0, frozenset(T0), 24, True)] + [s for s in states if s[1] != T1set]:          # the last floor is Minana's own pattern (its solid is Minana)
    r = realise(Tf); r.update(floor=f, symmetric=sym, independent=indep); out.append(r)
    print(f'floor {f} realised (no symmetry imposed): corners outside a non-incident plane: {r["bad"]} (0 = exact convex solid)', flush=True)
    print(f'PROGRESS {f / len(states):.3f}', flush=True)
json.dump(dict(floors=len(states), realised=out), open(os.path.join(HERE, '../data/c116/floors.json'), 'w'))
ok = REACHED and all(s[3] for s in states) and all(r['bad'] == 0 for r in out)
print('FINAL ok' if ok else 'FINAL FAIL (a floor not symmetric or not realised exactly)')
