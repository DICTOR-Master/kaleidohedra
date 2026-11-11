"""Stacking-friendly tablets? (DICTO 11 Nov: "maybe stacking friendly shapes"; "go on with the tablet stacking study").
For each 3D tablet (HeiCuBeDa PLY, CC BY-SA 4.0): principal axes (length, width, thickness by PCA); the two big faces (the vertices on
either side of the mid-plane, outer quarter in thickness): flatness = sag / T, the largest gap between the face and its best-fit plane
over the face's central 80 % (so the rounded rim does not count), the flatter and the rounder face compared; RESTING on each of the six
sides (both faces, both long edges, both short edges): on a table perpendicular to that axis, the contact patch = hull points within
0.5 mm of the lowest point; the side is STABLE when the centre of mass (centroid of the convex hull, a solid-clay estimate) projects
inside the patch's convex hull, with margin = distance to the patch boundary / tablet width (negative = it tips).
usage: tablet_stacking.py ZIPFILE [MAX]   -> tablet_stacking_<zip>.json and one summary line per tablet; FINAL ok if every tablet
read and every number finite.  Control: a synthetic box (stable on all six sides, flat faces) and a synthetic ellipsoid (unstable
everywhere, sag > 0) are measured first and must come out that way."""
import sys, json, zipfile, io, math, re
import numpy as np
from scipy.spatial import ConvexHull, Delaunay
import trimesh
def measure(V):
    c0 = V.mean(0); X = V - c0
    w, U = np.linalg.eigh(np.cov(X.T)); U = U[:, ::-1]; Y = X @ U              # axes: 0 length, 1 width, 2 thickness
    L, W, T = (Y.max(0) - Y.min(0))
    h = ConvexHull(Y); com = Y[h.vertices].mean(0)
    # better solid centroid: hull tetrahedra
    tet = Delaunay(Y[h.vertices]); P = Y[h.vertices]; vol = 0; cm = np.zeros(3)
    for s in tet.simplices:
        a, b, c, d = P[s]; v = abs(np.dot(b - a, np.cross(c - a, d - a))) / 6; vol += v; cm += v * (a + b + c + d) / 4
    com = cm / vol
    out = {'L_cm': L / 10, 'W_cm': W / 10, 'T_cm': T / 10}
    # faces: flatness
    for side, sgn in (('pos', 1), ('neg', -1)):
        z = sgn * Y[:, 2]; m = (z >= np.quantile(z, 0.75))
        F = Y[m]; r = np.max(np.abs(F[:, :2]) / (np.array([L, W]) / 2), axis=1); F = F[r < 0.8]
        A = np.c_[F[:, :2], np.ones(len(F))]; coef = np.linalg.lstsq(A, F[:, 2], rcond=None)[0]
        res = F[:, 2] - A @ coef; out[f'sag_{side}'] = float((res.max() - res.min()) / T)
    out['sag_flat'] = min(out['sag_pos'], out['sag_neg']); out['sag_round'] = max(out['sag_pos'], out['sag_neg'])
    # resting: the height of the centre of mass above a table under it, h(u) = max over hull points of u.(x - com), for the
    # downward direction u; stable resting positions are the local minima of h on the sphere; a tablet dropped in orientation u
    # rolls downhill on h to one of them. Fine sphere grid (Fibonacci, 6000 points), 8 nearest neighbours, steepest descent.
    HV = Y[h.vertices] - com
    n = 6000; k = np.arange(n) + 0.5; ph = np.arccos(1 - 2 * k / n); th = np.pi * (1 + 5 ** 0.5) * k
    U = np.c_[np.cos(th) * np.sin(ph), np.sin(th) * np.sin(ph), np.cos(ph)]
    hh = (U @ HV.T).max(1)
    from scipy.spatial import cKDTree
    # EXACT stable positions of a convex body: the hull's faces (coplanar triangles merged, normals within 2 degrees, the merged face
    # = convex hull of its points) onto which the centre of mass projects inside the face.
    HH = ConvexHull(HV); faces = []
    for simp, eq in zip(HH.simplices, HH.equations):
        nrm = eq[:3]
        for f in faces:
            if f['n'] @ nrm > np.cos(np.radians(2)) and abs(f['d'] - eq[3]) < 0.3: f['pts'].update(simp.tolist()); break
        else: faces.append({'n': nrm, 'd': eq[3], 'pts': set(simp.tolist())})
    stable = []
    for f in faces:
        Q = HV[list(f['pts'])]; n_ = f['n']; e1 = np.linalg.svd(np.c_[n_].T)[2][1:]   # in-plane basis
        q2 = Q @ e1.T; c2 = np.zeros(2)                                                # the COM is the origin
        if len(Q) >= 3 and np.linalg.matrix_rank(q2 - q2.mean(0)) == 2:
            ph2 = ConvexHull(q2)
            if np.all(ph2.equations[:, :2] @ c2 + ph2.equations[:, 2] < -0.5): stable.append(n_ / np.linalg.norm(n_))   # at least 0.5 mm inside: survives a nudge
    S = np.array(stable)
    # drops: a tablet dropped with downward direction u ends, as it rolls, on the stable face reached by steepest descent of h;
    # approximated by descent on the grid with wide neighbourhoods, each sink then assigned to the nearest stable face normal
    nb = cKDTree(U).query(U, k=31)[1][:, 1:]
    down = np.where(hh[nb].min(1) < hh, nb[np.arange(n), hh[nb].argmin(1)], np.arange(n))
    sink = np.arange(n)
    for _ in range(400):
        nxt = down[sink]
        if np.array_equal(nxt, sink): break
        sink = nxt
    lab = np.argmax(U[sink] @ S.T, axis=1) if len(S) else np.zeros(n, int)
    minima = list(range(len(S)))
    # classify each stable position by the axis its downward direction is closest to
    sflat = 1 if out['sag_pos'] <= out['sag_neg'] else -1
    def kind(u):
        a = np.argmax(np.abs(u))
        if a == 2: return 'face_flat' if np.sign(u[2]) == sflat else 'face_round'
        return 'long_edge' if a == 1 else 'short_edge'
    share = {'face_flat': 0.0, 'face_round': 0.0, 'long_edge': 0.0, 'short_edge': 0.0}
    for m in minima: share[kind(S[m])] += float(np.mean(lab == m))
    out['stable_positions'] = int(len(minima))
    for kk, v in share.items(): out[f'drop_{kk}'] = v
    out['can_stand_on_edge'] = bool(out['drop_long_edge'] + out['drop_short_edge'] >= 0.02)   # at least 2 % of drops end on an edge
    return out
def control():
    g = np.mgrid[-30:31:2, -20:21:2, -8:9:2].reshape(3, -1).T.astype(float)
    box = g[(np.abs(g[:, 0]) == 30) | (np.abs(g[:, 1]) == 20) | (np.abs(g[:, 2]) == 8)]
    u = np.random.default_rng(0).normal(size=(4000, 3)); u /= np.linalg.norm(u, axis=1)[:, None]; ell = u * [30, 20, 8]
    b, e = measure(box), measure(ell)
    ok = b['stable_positions'] == 6 and b['can_stand_on_edge'] and b['sag_flat'] < 0.01 and e['stable_positions'] == 2 and not e['can_stand_on_edge'] and e['sag_flat'] > 0.05
    print('control box', {k: round(v, 3) for k, v in b.items() if k.startswith(('stable', 'drop', 'sag', 'can'))}); print('control ellipsoid', {k: round(v, 3) for k, v in e.items() if k.startswith(('stable', 'drop', 'sag', 'can'))})
    return ok
if __name__ == '__main__':
    ok = control(); print('controls', 'ok' if ok else 'FAIL', flush=True)
    zf = zipfile.ZipFile(sys.argv[1]); names = [n for n in zf.namelist() if n.lower().endswith('.ply')]
    mx = int(sys.argv[2]) if len(sys.argv) > 2 else len(names); res = {}; bad = 0
    for k, n in enumerate(names[:mx]):
        try:
            m = trimesh.load(io.BytesIO(zf.read(n)), file_type='ply', process=False)
            V = np.asarray(m.vertices, float)
            if len(V) > 120000: V = V[np.random.default_rng(1).choice(len(V), 120000, replace=False)]
            r = measure(V); hs = re.search(r'HS_?(\d+[a-z]?)', n); r['hs'] = 'HS ' + hs.group(1) if hs else n
            if not all(math.isfinite(v) for v in r.values() if isinstance(v, float) and not isinstance(v, bool)): raise ValueError('non-finite')
            res[n] = r
            print(f"PROGRESS {k + 1}/{mx} {r['hs']}: sag flat {r['sag_flat']:.3f} round {r['sag_round']:.3f}; stable {r['stable_positions']}; drops flat {r['drop_face_flat']:.2f} round {r['drop_face_round']:.2f} long edge {r['drop_long_edge']:.2f} short edge {r['drop_short_edge']:.2f}; stands on edge {r['can_stand_on_edge']}", flush=True)
        except Exception as ex:
            bad += 1; print(f'PROGRESS {k + 1}/{mx} {n}: unreadable ({ex})', flush=True)
    json.dump(res, open(f"tablet_stacking_{sys.argv[1].rsplit('/', 1)[-1]}.json", 'w'), indent=1)
    print(f'read {len(res)}, unreadable {bad}')
    print('FINAL ok' if ok and len(res) > 0 and bad <= 0.05 * mx else 'FINAL FAIL')
