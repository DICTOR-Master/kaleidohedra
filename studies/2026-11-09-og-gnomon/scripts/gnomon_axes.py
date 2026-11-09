# DICTO #43 Conjecture 1, gnomon study 2026-11-09 (DICTO proposed a gnomon argument): where the inradius can fall.
# Float run of the OG's downward family D_k = P(D_{k-1}) recording, for each k:
#   persistent normals (face normals of both D_k and D_{k+1}); Lemma G1 check f_{k+1}(n) >= f_k(n) on them
#   r split into persistent faces and new faces: r_{k+1} >= min(r_k, smallest new-face distance) (exact consequence of G1)
#   the face that attains r_{k+1}: its spanning foot points (corners of D_{k+1}) and their lengths against r_k (the loss mechanism)
#   support h_k on the 5-, 3- and 2-fold axes and what sits there (face / corner / edge): the axis rhythm rules
#     R1 (5- and 3-fold): a corner at k is followed by a face at k+1;  R2: h_{k+1}(a) >= h_k(a) when D_k has a face on a;
#     R3: when D_{k+1} has a corner on a, h_{k+1}(a) = f_k(a) (that corner is the foot point of D_k's axis face)
# usage: python -u gnomon_axes.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json, time
import numpy as np
from scipy.spatial import ConvexHull, cKDTree
OUT = os.path.abspath(sys.argv[3])
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
src = open('exact_upward.py').read(); exec(src.split("def kinds(S)")[0])
KMAX = int(sys.argv[2])
OGf = np.array([[x.f() for x in v] for v in OG]); Gf = np.array([[[x.f() for x in row] for row in M] for M in G])

def faces(V, tol=1e-9):
    h = ConvexHull(V); E = h.equations; n = len(E); par = np.arange(n)
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if g > f and np.abs(E[f] - E[g]).max() < tol: par[find(f)] = find(g)
    roots = np.array([find(i) for i in range(n)]); u, inv = np.unique(roots, return_inverse=True)
    M = np.zeros((len(u), 3)); Dd = np.zeros(len(u)); cnt = np.bincount(inv)
    np.add.at(M, inv, E[:, :3]); np.add.at(Dd, inv, -E[:, 3]); M /= np.linalg.norm(M, axis=1)[:, None]; Dd /= cnt
    vs = [set() for _ in range(len(u))]
    for t, s in zip(inv, h.simplices): vs[t].update(s.tolist())
    return M, Dd, np.unique(h.vertices), [sorted(s) for s in vs]

def symmetrise(W):
    X = np.vstack([W @ g.T for g in Gf]); X = X[np.lexsort(X.T[::-1])]
    t = cKDTree(X); groups = {}
    for i, js in enumerate(t.query_ball_point(X, 1e-8)): groups.setdefault(min(js), []).append(i)
    return np.array([X[g].mean(0) for g in groups.values()])

AX = {5: [], 3: [], 2: []}
for g in Gf:
    c = (np.trace(g) - 1) / 2
    if c > 1 - 1e-9: continue
    ang = np.degrees(np.arccos(np.clip(c, -1, 1)))
    o = 5 if min(abs(ang - 72), abs(ang - 144)) < 1e-4 else 3 if abs(ang - 120) < 1e-4 else 2
    w, v = np.linalg.eig(g); a = np.real(v[:, np.argmin(np.abs(w - 1))]); AX[o].append(a / np.linalg.norm(a))
AXR = {o: np.unique(np.round(np.array(AX[o]), 9), axis=0)[0] for o in AX}     # one representative axis per type
AXR = {o: a / np.linalg.norm(a) for o, a in AXR.items()}

def what_on(a, M, Vc):
    if (M @ a > 1 - 1e-9).any(): return 'face'
    if ((Vc / np.linalg.norm(Vc, axis=1)[:, None]) @ a > 1 - 1e-9).any(): return 'corner'
    return 'edge'

res = {'mark': 'DICTO #43 Conjecture 1, gnomon study (axes, persistence), float, 2026-11-09 · DICTO · dictospheres.com', 'k': []}
t0 = time.time(); ok = True; prev = None
V = OGf; FF = faces(V)
for k in range(KMAX + 1):
    M, Dd, cor, fv = FF; Vc = V[cor]
    W = symmetrise(M * Dd[:, None]); FN = faces(W); M2, D2, cor2, fv2 = FN; Wc = W[cor2]
    tr = cKDTree(M); dd, jj = tr.query(M2)
    pers = dd < 1e-9                                     # normals of D_{k+1} that are also normals of D_k
    g1 = float((D2[pers] - Dd[jj[pers]]).min()) if pers.any() else None
    newmin = float(D2[~pers].min()) if (~pers).any() else None
    persmin = float(D2[pers].min()) if pers.any() else None
    r, r1 = float(Dd.min()), float(D2.min())
    i1 = int(np.argmin(D2)); spanlen = np.linalg.norm(W[fv2[i1]], axis=1)
    ang = np.degrees(np.arccos(np.clip((W[fv2[i1]] / spanlen[:, None]) @ M2[i1], -1, 1)))
    hax = {o: float((Vc @ a).max()) for o, a in AXR.items()}
    on = {o: what_on(a, M, Vc) for o, a in AXR.items()}
    row = {'k': k, 'faces': len(M), 'r': r, 'r_next': r1, 'persistent_normals': int(pers.sum()), 'G1_min': g1,
           'r_next_persistent': persmin, 'r_next_new': newmin, 'r_next_on_new_face': bool(newmin is not None and newmin <= r1 + 1e-12),
           'rmin_face_span_min_len': float(spanlen.min()), 'rmin_face_span_min_len_over_r': float(spanlen.min() / r),
           'rmin_face_angular_radius_deg': float(ang.max()), 'h_axis': hax, 'on_axis': on}
    # rules
    ok &= g1 is None or g1 > -1e-9
    ok &= r1 >= min(r, newmin if newmin is not None else 9) - 1e-9
    if prev is not None:
        for o in (5, 3):
            if prev['on_axis'][o] == 'corner': ok &= on[o] == 'face'
        for o in (5, 3, 2):
            if prev['on_axis'][o] == 'face': ok &= hax[o] >= prev['h_axis'][o] - 1e-9
    row['F_axis'] = {o: float(Dd[np.argmax(M @ a)]) if on[o] == 'face' else None for o, a in AXR.items()}
    if prev is not None:
        for o in (5, 3, 2):
            if on[o] == 'corner' and prev['on_axis'][o] == 'face': ok &= abs(hax[o] - prev['F_axis'][o]) < 1e-9
    res['k'].append(row); prev = row
    print(f"k {k:2d} F {len(M):6d} r {r:.6f} -> r_next {r1:.6f} | persistent {int(pers.sum()):4d} (G1 min {g1 if g1 is None else round(g1, 12)}) "
          f"pers-min {persmin if persmin is None else round(persmin, 6)} new-min {newmin if newmin is None else round(newmin, 6)} | r_next face: span min {spanlen.min():.6f} "
          f"(= {spanlen.min() / r:.5f} r_k), ang.rad {ang.max():.3f} deg | axes "
          + ' '.join(f"{o}:{on[o][0]} h={hax[o]:.6f}" for o in (5, 3, 2)) + f" ({time.time() - t0:.0f}s)", flush=True)
    V, FF = W, FN
    json.dump(res, open(OUT, 'w'))
print('FINAL ok' if ok else 'FINAL FAIL: G1, the new-face bound or an axis rule failed')
